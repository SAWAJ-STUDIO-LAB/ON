"""
👑 KING — Single File Mode
Saara code ek file mein → AI → Wapas alag files mein
"""
import os
import re
import ast
import json
import time
import shutil
import requests
from datetime import datetime

# ═══════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════
BOT_ROOT = "sawajstudiobot"
WORK = "bot update upgrade/_work"
BACKUP = "bot update upgrade/_backups"
LOG_DIR = "bot update upgrade/_logs"

ROOT_SKIP = "bot update upgrade"
CODE_EXT = {".py"}
TEXT_EXT = {".py", ".txt", ".md", ".json", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".env", ".example"}
TIMEOUT = 600
MAX_TOKENS = 16000

ALL_AIS = [
    "OpenRouter", "Groq", "Gemini", "Mistral",
    "Cerebras", "Cohere", "NVIDIA", "HuggingFace"
]


# ═══════════════════════════════════════════════
# TELEGRAM
# ═══════════════════════════════════════════════
def tg_send(msg, silent=False):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat:
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": msg[:4000],
                  "parse_mode": "HTML",
                  "disable_web_page_preview": True,
                  "disable_notification": silent},
            timeout=15)
        return r.status_code == 200
    except Exception:
        return False


# ═══════════════════════════════════════════════
# SKIP CHECK
# ═══════════════════════════════════════════════
def is_skipped(full_path):
    parts = full_path.replace("\\", "/").split("/")
    for p in parts:
        if p in ("__pycache__", ".git", "output", "_work",
                 "_backups", "_logs", "venv", "node_modules"):
            return True
    if ROOT_SKIP in full_path:
        return True
    if "Code editor" in full_path:
        return True
    if "_temp_builder" in full_path:
        return True
    return False


# ═══════════════════════════════════════════════
# SCAN ALL FILES
# ═══════════════════════════════════════════════
def scan_all():
    """Scan all text files + all folders."""
    files = []
    folders = set()
    for root, dirs, fnames in os.walk(BOT_ROOT):
        dirs[:] = [d for d in dirs if not is_skipped(os.path.join(root, d))]
        rel_dir = os.path.relpath(root, BOT_ROOT)
        if rel_dir != ".":
            folders.add(rel_dir)
        for fn in fnames:
            full = os.path.join(root, fn)
            if is_skipped(full):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in TEXT_EXT or fn.startswith(".env"):
                rel = os.path.relpath(full, BOT_ROOT)
                files.append(rel)
    return sorted(files), sorted(folders)


# ═══════════════════════════════════════════════
# BUILD SINGLE FILE
# ═══════════════════════════════════════════════
def build_single_file(files, folders):
    """Create one combined file with full structure."""
    os.makedirs(WORK, exist_ok=True)
    path = f"{WORK}/all_code.txt"

    with open(path, "w", encoding="utf-8") as out:
        out.write("# ═══════════════════════════════════════════\n")
        out.write("# SAWAJSTUDIOBOT — FULL CODE\n")
        out.write(f"# Files: {len(files)}\n")
        out.write(f"# Folders: {len(folders)}\n")
        out.write("# ═══════════════════════════════════════════\n\n")

        # Folder structure
        out.write("═══ FOLDER STRUCTURE ═══\n")
        for f in folders:
            out.write(f"{f}/\n")
        out.write("═══ END FOLDERS ═══\n\n")

        # Files
        for rel in files:
            full = os.path.join(BOT_ROOT, rel)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception:
                code = ""
            out.write(f"═══ FILE: {rel} ═══\n")
            out.write(code)
            out.write(f"\n═══ END ═══\n\n")

    size_kb = os.path.getsize(path) // 1024
    print(f"  📦 Single file: {size_kb} KB")
    return path, size_kb


# ═══════════════════════════════════════════════
# AI CALLS
# ═══════════════════════════════════════════════
def _post(url, headers, payload, timeout=TIMEOUT, retries=2):
    for attempt in range(1, retries + 1):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(attempt * 3)
                continue
            return None
        except requests.exceptions.Timeout:
            time.sleep(3)
        except Exception:
            time.sleep(2)
    return None


def call_ai(ai_name, prompt, max_tokens=MAX_TOKENS):
    """Call one AI."""
    if ai_name == "OpenRouter":
        key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not key:
            return None
        d = _post("https://openrouter.ai/api/v1/chat/completions",
                  {"Authorization": f"Bearer {key}"},
                  {"model": "openai/gpt-4o-mini",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": max_tokens, "temperature": 0.3})
        return d["choices"][0]["message"]["content"] if d else None

    if ai_name == "Groq":
        key = os.environ.get("GROQ_API_KEY", "").strip()
        if not key:
            return None
        for model in ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile",
                      "llama-3.1-8b-instant", "llama3-70b-8192"]:
            d = _post("https://api.groq.com/openai/v1/chat/completions",
                      {"Authorization": f"Bearer {key}"},
                      {"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": min(max_tokens, 8000), "temperature": 0.3})
            if d:
                return d["choices"][0]["message"]["content"]
        return None

    if ai_name == "Gemini":
        key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not key:
            return None
        for model in ["gemini-2.0-flash-exp", "gemini-1.5-flash-latest",
                      "gemini-1.5-flash", "gemini-1.5-pro-latest", "gemini-pro"]:
            d = _post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                {},
                {"contents": [{"parts": [{"text": prompt}]}],
                 "generationConfig": {"maxOutputTokens": max_tokens,
                                      "temperature": 0.3}})
            if d:
                try:
                    return d["candidates"][0]["content"]["parts"][0]["text"]
                except Exception:
                    continue
        return None

    if ai_name == "Mistral":
        key = os.environ.get("MISTRAL_API_KEY", "").strip()
        if not key:
            return None
        for model in ["mistral-small-latest", "open-mistral-7b",
                      "mistral-tiny", "open-mixtral-8x7b"]:
            d = _post("https://api.mistral.ai/v1/chat/completions",
                      {"Authorization": f"Bearer {key}"},
                      {"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": min(max_tokens, 8000), "temperature": 0.3})
            if d:
                return d["choices"][0]["message"]["content"]
        return None

    if ai_name == "Cerebras":
        key = os.environ.get("CEREBRAS_API_KEY", "").strip()
        if not key:
            return None
        for model in ["llama-3.3-70b", "llama-3.1-70b", "llama3.1-70b",
                      "llama-3.1-8b", "llama3.1-8b"]:
            d = _post("https://api.cerebras.ai/v1/chat/completions",
                      {"Authorization": f"Bearer {key}"},
                      {"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": min(max_tokens, 8000), "temperature": 0.3})
            if d:
                return d["choices"][0]["message"]["content"]
        return None

    if ai_name == "Cohere":
        key = os.environ.get("COHERE_API_KEY", "").strip()
        if not key:
            return None
        for model in ["command-r-plus-08-2024", "command-r-plus",
                      "command-r", "command"]:
            d = _post("https://api.cohere.com/v1/chat",
                      {"Authorization": f"Bearer {key}"},
                      {"model": model, "message": prompt})
            if d:
                return d["text"]
        return None

    if ai_name == "NVIDIA":
        key = os.environ.get("NVIDIA_API_KEY", "").strip()
        if not key:
            return None
        for model in ["meta/llama-3.3-70b-instruct", "meta/llama-3.1-70b-instruct",
                      "meta/llama-3.1-8b-instruct", "meta/llama3-70b-instruct"]:
            d = _post("https://integrate.api.nvidia.com/v1/chat/completions",
                      {"Authorization": f"Bearer {key}"},
                      {"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": min(max_tokens, 8000), "temperature": 0.3})
            if d:
                return d["choices"][0]["message"]["content"]
        return None

    if ai_name == "HuggingFace":
        key = os.environ.get("HUGGINGFACE_API_KEY", "").strip()
        if not key:
            return None
        for model in ["meta-llama/Meta-Llama-3.1-8B-Instruct",
                      "mistralai/Mistral-7B-Instruct-v0.3",
                      "Qwen/Qwen2.5-7B-Instruct"]:
            d = _post(
                f"https://api-inference.huggingface.co/models/{model}/v1/chat/completions",
                {"Authorization": f"Bearer {key}"},
                {"model": model,
                 "messages": [{"role": "user", "content": prompt}],
                 "max_tokens": 4000, "temperature": 0.3})
            if d:
                try:
                    return d["choices"][0]["message"]["content"]
                except Exception:
                    continue
        return None

    return None


# ═══════════════════════════════════════════════
# PROMPT
# ═══════════════════════════════════════════════
PROMPT = """You are a WORLD #1 senior Python engineer.

UPGRADE the following complete bot code to WORLD #1 quality.

INPUT FORMAT:
- Section "FOLDER STRUCTURE" contains the project folders
- Each "═══ FILE: path ═══" contains one file's full code

RULES:
1. Return ALL files in EXACT SAME FORMAT
2. Do NOT skip any file
3. Keep folder structure intact
4. FORMAT for each file:
   ═══ FILE: path ═══
   <full code>
   ═══ END ═══
5. To CREATE a new file:
   ═══ NEW FILE: path ═══
   <code>
   ═══ END ═══
6. NEVER DELETE any file
7. Fix ALL bugs, add error handling, add fallbacks
8. Add docstrings, comments, type hints
9. Remove any copyright text
10. Make code production-ready, WORLD #1
11. Return ONLY the code, no explanations

CODE:
"""


# ═══════════════════════════════════════════════
# APPLY
# ═══════════════════════════════════════════════
def apply_response(text):
    """Apply AI response — write files back."""
    # New files
    for rel, code in re.findall(r"═══ NEW FILE: (.+?) ═══\n(.*?)\n═══ END ═══",
                                text, re.DOTALL):
        rel = rel.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.rstrip() + "\n")

    # Modified files
    modified = 0
    for rel, code in re.findall(r"═══ FILE: (.+?) ═══\n(.*?)\n═══ END ═══",
                                text, re.DOTALL):
        rel = rel.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.rstrip() + "\n")
        modified += 1

    return modified


# ═══════════════════════════════════════════════
# BACKUP
# ═══════════════════════════════════════════════
def backup():
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dest = f"{BACKUP}/{ts}"
    os.makedirs(dest, exist_ok=True)
    try:
        shutil.copytree(BOT_ROOT, f"{dest}/sawajstudiobot")
        return dest
    except Exception:
        return None


# ═══════════════════════════════════════════════
# SYNTAX CHECK
# ═══════════════════════════════════════════════
def check_syntax(files):
    failed = []
    for rel in files:
        if not rel.endswith(".py"):
            continue
        full = os.path.join(BOT_ROOT, rel)
        try:
            with open(full, "r", encoding="utf-8") as f:
                ast.parse(f.read())
        except SyntaxError as e:
            failed.append({"file": rel, "error": str(e)[:80]})
        except Exception:
            pass
    return failed


# ═══════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════
def send_report(data):
    ts = data["time"]
    files_total = data["files_total"]
    modified = data["modified"]
    ai_used = data["ai_used"]
    ai_all = data["ai_all"]
    size_kb = data["size_kb"]
    score = data["score"]
    backup_path = data["backup"] or "N/A"
    syntax_failed = data["syntax_failed"]

    bar = "█" * score + "░" * (10 - score)

    ai_lines = []
    for a in ai_all:
        icon = "🏆" if a["name"] == ai_used else "✅"
        ai_lines.append(f"   {icon} {a['name']}: {a['files']} files")
    ai_text = "\n".join(ai_lines) if ai_lines else "   (none)"

    msg = (
        "👑 <b>KING REPORT — SINGLE FILE MODE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <code>{ts}</code>\n"
        "\n"
        "📁 <b>SCAN:</b>\n"
        f"   • Files: <b>{files_total}</b>\n"
        f"   • Combined size: <b>{size_kb} KB</b>\n"
        "\n"
        "🤖 <b>AI RESPONSES:</b>\n"
        f"{ai_text}\n"
        f"\n"
        f"🏆 <b>Best:</b> <b>{ai_used}</b>\n"
        "\n"
        "🔧 <b>APPLIED:</b>\n"
        f"   ✏️ Modified: <b>{modified}</b>\n"
        f"   🗑️ Deleted: <b>0</b>\n"
        "\n"
        f"⚠️ Syntax fail: {len(syntax_failed)}\n"
        f"💾 Backup: <code>{backup_path}</code>\n"
        "\n"
        "📈 <b>SCORE:</b>\n"
        f"   {bar} <b>{score}/10</b>\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>World #1 in progress</b>"
    )
    tg_send(msg)

    if syntax_failed:
        s = "⚠️ <b>SYNTAX FAILURES:</b>\n"
        for x in syntax_failed[:15]:
            s += f"• <code>{x['file']}</code>\n"
        tg_send(s)


def rate_bot(files, changes, syntax_failed):
    if changes == 0:
        return 3
    ratio = changes / max(files, 1)
    base = int(4 + min(ratio, 1.0) * 6)
    if syntax_failed > 0:
        base -= min(2, syntax_failed // 10)
    return min(10, max(1, base))


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════
def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("═" * 60)
    print("👑 KING — SINGLE FILE MODE")
    print("═" * 60)

    tg_send(f"👑 <b>KING ACTIVATED</b>\n🕐 {ts}\nSingle File Mode...", silent=True)

    os.makedirs(WORK, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    # ═══ SCAN ═══
    print("\n📁 SCAN...")
    files, folders = scan_all()
    print(f"   Files: {len(files)}")
    print(f"   Folders: {len(folders)}")

    if not files:
        tg_send("⚠️ No files.")
        return

    # ═══ BACKUP ═══
    print("\n💾 BACKUP...")
    backup_path = backup()
    print(f"   {backup_path}")

    # ═══ SINGLE FILE ═══
    print("\n📦 BUILDING SINGLE FILE...")
    single_path, size_kb = build_single_file(files, folders)

    with open(single_path, "r", encoding="utf-8") as f:
        combined = f.read()

    # ═══ AI CALLS (saare 8) ═══
    print("\n🤖 CALLING 8 AI...")
    all_responses = []
    for ai in ALL_AIS:
        print(f"  🤖 {ai}...")
        try:
            res = call_ai(ai, PROMPT + combined)
            if res and "═══ FILE:" in res:
                fcount = res.count("═══ FILE:")
                all_responses.append({
                    "name": ai, "code": res, "files": fcount
                })
                print(f"     ✅ {fcount} files, {len(res)} chars")
            else:
                print(f"     ⚠️ invalid")
        except Exception as e:
            print(f"     ❌ {str(e)[:60]}")

    if not all_responses:
        tg_send("⚠️ All AI failed")
        return

    # ═══ PICK BEST ═══
    best = max(all_responses, key=lambda r: r["files"] * 10000 + len(r["code"]))
    print(f"\n🏆 Best: {best['name']} ({best['files']} files)")

    # ═══ APPLY ═══
    print("\n🔧 APPLYING...")
    modified = apply_response(best["code"])
    print(f"   Modified: {modified}")

    # ═══ TEST ═══
    print("\n🧪 TEST...")
    syntax_failed = check_syntax(files)
    print(f"   Syntax fail: {len(syntax_failed)}")

    # ═══ SCORE ═══
    score = rate_bot(len(files), modified, len(syntax_failed))

    # ═══ REPORT ═══
    send_report({
        "time": ts,
        "files_total": len(files),
        "modified": modified,
        "ai_used": best["name"],
        "ai_all": all_responses,
        "size_kb": size_kb,
        "score": score,
        "backup": backup_path,
        "syntax_failed": syntax_failed,
    })

    # ═══ LOG ═══
    log_file = f"{LOG_DIR}/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "time": ts,
            "files": len(files),
            "modified": modified,
            "best_ai": best["name"],
            "score": score,
            "syntax_failed": len(syntax_failed),
        }, f, indent=2)

    print("\n" + "═" * 60)
    print(f"👑 DONE: {modified} modified — Score {score}/10")
    print("═" * 60)


if __name__ == "__main__":
    main()
