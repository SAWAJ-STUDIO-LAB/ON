"""
upgrade.py
Saari files → combined file → AI → best pick → split → apply
"""
import os
import re
import json
import base64
import time
import shutil
from datetime import datetime

# ═══════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════
BOT_ROOT = "sawajstudiobot"
WORK_DIR = "bot update upgrade/_work"
BACKUP_DIR = "bot update upgrade/_backups"
COMBINED = f"{WORK_DIR}/combined.txt"
UPGRADED = f"{WORK_DIR}/upgraded.txt"

IGNORE_DIRS = {"__pycache__", ".git", ".github", "output", "_work", "_backups", "venv", "node_modules"}


# ═══════════════════════════════════════════════
# 1. COLLECT ALL FILES
# ═══════════════════════════════════════════════
def collect_files():
    """Collect all .py files from bot root."""
    files = []
    for root, dirs, filenames in os.walk(BOT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fn in filenames:
            if fn.endswith(".py"):
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, BOT_ROOT)
                files.append(rel)
    return sorted(files)


# ═══════════════════════════════════════════════
# 2. COMBINE INTO ONE FILE
# ═══════════════════════════════════════════════
def combine(files):
    """Combine all files into single txt."""
    os.makedirs(WORK_DIR, exist_ok=True)
    with open(COMBINED, "w", encoding="utf-8") as out:
        out.write("# BOT CODE COMBINED\n")
        out.write(f"# Total files: {len(files)}\n")
        out.write("# " + "=" * 60 + "\n\n")
        for rel in files:
            full = os.path.join(BOT_ROOT, rel)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception:
                code = ""
            out.write(f"═══ FILE: {rel} ═══\n")
            out.write(code)
            out.write("\n═══ END: {0} ═══\n\n".format(rel))
    size = os.path.getsize(COMBINED)
    print(f"✅ Combined: {len(files)} files → {size // 1024} KB")
    return COMBINED


# ═══════════════════════════════════════════════
# 3. AI CALLS (4 providers)
# ═══════════════════════════════════════════════
PROMPT = """You are a senior Python engineer. Upgrade the following bot code.

RULES:
1. Make code BETTER, cleaner, faster, documented
2. Fix bugs, add error handling
3. Remove any copyright text
4. Keep the SAME file structure (═══ FILE: path ═══)
5. Return the FULL upgraded code in the SAME format
6. Do NOT add explanations, just the code

CODE:
"""


def call_openrouter(code):
    import requests
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "openai/gpt-4o-mini",
                  "messages": [{"role": "user", "content": PROMPT + code[:100000]}],
                  "max_tokens": 8000}, timeout=120)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenRouter err: {e}")
    return None


def call_groq(code):
    import requests
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "llama-3.3-70b-versatile",
                  "messages": [{"role": "user", "content": PROMPT + code[:100000]}],
                  "max_tokens": 8000}, timeout=120)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq err: {e}")
    return None


def call_gemini(code):
    import requests
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
            json={"contents": [{"parts": [{"text": PROMPT + code[:200000]}]}]}, timeout=120)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini err: {e}")
    return None


def call_mistral(code):
    import requests
    key = os.environ.get("MISTRAL_API_KEY", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "mistral-small-latest",
                  "messages": [{"role": "user", "content": PROMPT + code[:80000]}],
                  "max_tokens": 8000}, timeout=120)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Mistral err: {e}")
    return None


def call_all(code):
    """Call all AI providers, return list of responses."""
    responses = []
    for name, fn in [("OpenRouter", call_openrouter), ("Groq", call_groq),
                     ("Gemini", call_gemini), ("Mistral", call_mistral)]:
        print(f"🤖 Calling {name}...")
        try:
            res = fn(code)
            if res and "═══ FILE:" in res:
                responses.append({"ai": name, "code": res})
                print(f"  ✅ {name} OK")
            else:
                print(f"  ⚠️ {name} failed/empty")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
    return responses


# ═══════════════════════════════════════════════
# 4. PICK BEST
# ═══════════════════════════════════════════════
def pick_best(responses):
    """Pick longest (most complete) response."""
    if not responses:
        return None
    best = max(responses, key=lambda x: len(x["code"]))
    print(f"🏆 Best: {best['ai']} ({len(best['code'])} chars)")
    return best


# ═══════════════════════════════════════════════
# 5. BACKUP
# ═══════════════════════════════════════════════
def backup():
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dest = f"{BACKUP_DIR}/{ts}"
    os.makedirs(dest, exist_ok=True)
    shutil.copytree(BOT_ROOT, f"{dest}/sawajstudiobot")
    print(f"💾 Backup: {dest}")


# ═══════════════════════════════════════════════
# 6. SPLIT & APPLY
# ═══════════════════════════════════════════════
def split_and_apply(text):
    """Split combined upgraded text back into files."""
    pattern = r"═══ FILE: (.+?) ═══\n(.*?)\n═══ END:"
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        print("❌ No files found in upgraded text")
        return 0
    count = 0
    for rel, code in matches:
        rel = rel.strip()
        if not rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.strip())
        count += 1
    print(f"✅ Applied: {count} files")
    return count


# ═══════════════════════════════════════════════
# 7. MAIN
# ═══════════════════════════════════════════════
def run():
    print("═" * 50)
    print("🤖 BOT UPGRADE STARTED")
    print("═" * 50)

    # Step 1
    files = collect_files()
    print(f"📁 Files found: {len(files)}")
    if not files:
        print("❌ No files")
        return 0

    # Step 2
    combined_path = combine(files)
    with open(combined_path, "r", encoding="utf-8") as f:
        combined_text = f.read()

    # Step 3
    responses = call_all(combined_text)
    if not responses:
        print("❌ All AI failed")
        return 0

    # Step 4
    best = pick_best(responses)

    # Step 5
    backup()

    # Step 6
    count = split_and_apply(best["code"])

    # Save report
    with open(f"{WORK_DIR}/report.json", "w", encoding="utf-8") as f:
        json.dump({
            "files": len(files),
            "upgraded": count,
            "best_ai": best["ai"],
            "time": datetime.now().isoformat(),
        }, f, indent=2)

    print("═" * 50)
    print(f"🎉 DONE: {count} files upgraded by {best['ai']}")
    print("═" * 50)
    return count


if __name__ == "__main__":
    run()
