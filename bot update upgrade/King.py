"""
👑 KING — Bot Update Upgrade
8 AI se poochhta, best pick karta, khud upgrade karta, Telegram pe report.
"""
import os
import re
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
IGNORE = {"__pycache__", ".git", ".github", "output",
          "_work", "_backups", "venv", "node_modules"}

# ═══════════════════════════════════════════════
# TELEGRAM
# ═══════════════════════════════════════════════
def tg_send(msg, silent=False):
    """Send message to Telegram."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat:
        print("⚠️ Telegram not configured")
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
    except Exception as e:
        print(f"❌ Telegram: {e}")
        return False


# ═══════════════════════════════════════════════
# STEP 1: COLLECT ALL FILES
# ═══════════════════════════════════════════════
def collect():
    """Collect all .py files."""
    files = []
    for root, dirs, fnames in os.walk(BOT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE]
        for fn in fnames:
            if fn.endswith(".py"):
                files.append(os.path.relpath(os.path.join(root, fn), BOT_ROOT))
    return sorted(files)


# ═══════════════════════════════════════════════
# STEP 2: COMBINE
# ═══════════════════════════════════════════════
def combine(files):
    """Combine all files into 1 txt."""
    os.makedirs(WORK, exist_ok=True)
    path = f"{WORK}/combined.txt"
    with open(path, "w", encoding="utf-8") as out:
        out.write(f"# Total files: {len(files)}\n\n")
        for rel in files:
            full = os.path.join(BOT_ROOT, rel)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception:
                code = ""
            out.write(f"═══ FILE: {rel} ═══\n{code}\n═══ END ═══\n\n")
    size = os.path.getsize(path)
    print(f"📦 Combined: {len(files)} files → {size // 1024} KB")
    return path


# ═══════════════════════════════════════════════
# STEP 3: AI CALLS (8 AI)
# ═══════════════════════════════════════════════
PROMPT = """You are a senior Python engineer. Upgrade this bot code.

RULES:
1. Make code BETTER, cleaner, faster, well-documented
2. Fix bugs, add error handling
3. Remove any copyright text
4. KEEP SAME FORMAT: ═══ FILE: path ═══  code  ═══ END ═══
5. Return ONLY the upgraded code. No explanations.
6. Do not skip any file

CODE:
"""


def _post(url, headers, payload, timeout=180):
    """Safe POST request."""
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        print(f"    ⚠️ HTTP {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"    ❌ {str(e)[:80]}")
    return None


# ─── AI 1: OpenRouter ───
def ai_openrouter(code):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://openrouter.ai/api/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "openai/gpt-4o-mini",
               "messages": [{"role": "user", "content": PROMPT + code[:100000]}],
               "max_tokens": 8000})
    return d["choices"][0]["message"]["content"] if d else None


# ─── AI 2: Groq ───
def ai_groq(code):
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://api.groq.com/openai/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "llama-3.3-70b-versatile",
               "messages": [{"role": "user", "content": PROMPT + code[:100000]}],
               "max_tokens": 8000})
    return d["choices"][0]["message"]["content"] if d else None


# ─── AI 3: Gemini ───
def ai_gemini(code):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    d = _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
        {}, {"contents": [{"parts": [{"text": PROMPT + code[:200000]}]}]})
    return d["candidates"][0]["content"]["parts"][0]["text"] if d else None


# ─── AI 4: Mistral ───
def ai_mistral(code):
    key = os.environ.get("MISTRAL_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://api.mistral.ai/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "mistral-small-latest",
               "messages": [{"role": "user", "content": PROMPT + code[:80000]}],
               "max_tokens": 8000})
    return d["choices"][0]["message"]["content"] if d else None


# ─── AI 5: Cerebras ───
def ai_cerebras(code):
    key = os.environ.get("CEREBRAS_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://api.cerebras.ai/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "llama3.1-8b",
               "messages": [{"role": "user", "content": PROMPT + code[:80000]}],
               "max_tokens": 8000})
    return d["choices"][0]["message"]["content"] if d else None


# ─── AI 6: Cohere ───
def ai_cohere(code):
    key = os.environ.get("COHERE_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://api.cohere.com/v1/chat",
              {"Authorization": f"Bearer {key}"},
              {"model": "command-r-plus",
               "message": PROMPT + code[:80000]})
    return d["text"] if d else None


# ─── AI 7: NVIDIA ───
def ai_nvidia(code):
    key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://integrate.api.nvidia.com/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "meta/llama-3.1-70b-instruct",
               "messages": [{"role": "user", "content": PROMPT + code[:80000]}],
               "max_tokens": 8000})
    return d["choices"][0]["message"]["content"] if d else None


# ─── AI 8: HuggingFace ───
def ai_huggingface(code):
    key = os.environ.get("HUGGINGFACE_API_KEY", "").strip()
    if not key:
        return None
    d = _post(
        "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-70B-Instruct/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {"model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
         "messages": [{"role": "user", "content": PROMPT + code[:60000]}],
         "max_tokens": 4000})
    return d["choices"][0]["message"]["content"] if d else None


def ai_all(code):
    """Call all 8 AI."""
    providers = [
        ("OpenRouter", ai_openrouter),
        ("Groq", ai_groq),
        ("Gemini", ai_gemini),
        ("Mistral", ai_mistral),
        ("Cerebras", ai_cerebras),
        ("Cohere", ai_cohere),
        ("NVIDIA", ai_nvidia),
        ("HuggingFace", ai_huggingface),
    ]
    responses = []
    for name, fn in providers:
        print(f"🤖 Calling {name}...")
        try:
            res = fn(code)
            if res and "═══ FILE:" in res:
                responses.append({"ai": name, "code": res})
                print(f"  ✅ {name}: {len(res)} chars")
            else:
                print(f"  ⚠️ {name}: empty/invalid")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:80]}")
    return responses


# ═══════════════════════════════════════════════
# STEP 4: PICK BEST
# ═══════════════════════════════════════════════
def pick_best(responses):
    """Pick longest (most complete)."""
    if not responses:
        return None
    # Score = length + file count bonus
    def score(r):
        return len(r["code"]) + r["code"].count("═══ FILE:") * 1000
    best = max(responses, key=score)
    print(f"🏆 Best: {best['ai']}")
    return best


# ═══════════════════════════════════════════════
# STEP 5: BACKUP
# ═══════════════════════════════════════════════
def backup():
    """Backup bot folder."""
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dest = f"{BACKUP}/{ts}"
    os.makedirs(dest, exist_ok=True)
    try:
        shutil.copytree(BOT_ROOT, f"{dest}/sawajstudiobot")
        print(f"💾 Backup: {dest}")
        return dest
    except Exception as e:
        print(f"⚠️ Backup: {e}")
        return None


# ═══════════════════════════════════════════════
# STEP 6: SPLIT & APPLY
# ═══════════════════════════════════════════════
def apply(text):
    """Split combined upgraded text back into files."""
    pattern = r"═══ FILE: (.+?) ═══\n(.*?)\n═══ END ═══"
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        print("❌ No files found in AI response")
        return 0
    count = 0
    for rel, code in matches:
        rel = rel.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        count += 1
    print(f"✅ Applied {count} files")
    return count


# ═══════════════════════════════════════════════
# STEP 7: RATE BOT
# ═══════════════════════════════════════════════
def rate_bot(files, applied):
    """Rate 1-10."""
    if applied == 0:
        return 3
    ratio = applied / max(files, 1)
    score = int(4 + ratio * 6)
    return min(10, max(1, score))


# ═══════════════════════════════════════════════
# STEP 8: REPORT
# ═══════════════════════════════════════════════
def send_report(data):
    """Send full report to Telegram."""
    files = data["files"]
    applied = data["applied"]
    ai = data["ai"]
    backup_path = data["backup"] or "N/A"
    score = data["score"]
    ts = data["time"]
    ai_responses = data.get("ai_responses", [])

    bar = "█" * score + "░" * (10 - score)

    # AI list
    ai_lines = []
    for r in ai_responses:
        icon = "🏆" if r["ai"] == ai else "✅"
        ai_lines.append(f"   {icon} {r['ai']}: {len(r['code'])//1000}K chars")
    ai_text = "\n".join(ai_lines) if ai_lines else "   ❌ None responded"

    msg = (
        "👑 <b>BOT UPDATE UPGRADE — KING REPORT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <code>{ts}</code>\n"
        "\n"
        "📁 <b>SCAN:</b>\n"
        f"   • Files scanned: <b>{files}</b>\n"
        f"   • Files upgraded: <b>{applied}</b>\n"
        "\n"
        "🤖 <b>AI RESPONSES (8):</b>\n"
        f"{ai_text}\n"
        "\n"
        f"🏆 <b>Winner:</b> <b>{ai}</b>\n"
        f"💾 Backup: <code>{backup_path}</code>\n"
        "\n"
        "📈 <b>BOT SCORE:</b>\n"
        f"   {bar} <b>{score}/10</b>\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>King is at your service</b>"
    )
    tg_send(msg)


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════
def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("═" * 50)
    print("👑 KING STARTED")
    print("═" * 50)

    tg_send(
        f"👑 <b>KING ACTIVATED</b>\n🕐 {ts}\nWorking...",
        silent=True)

    # Collect
    files = collect()
    print(f"📁 Files: {len(files)}")
    if not files:
        tg_send("⚠️ No files found.")
        return

    # Combine
    path = combine(files)
    with open(path, "r", encoding="utf-8") as f:
        combined = f.read()

    # AI
    print("🤖 Calling 8 AI...")
    responses = ai_all(combined)

    if not responses:
        print("❌ All AI failed")
        tg_send(
            f"⚠️ <b>King Report</b>\n"
            f"📅 {ts}\n"
            f"📁 Files: {len(files)}\n"
            "❌ All 8 AI failed.")
        return

    # Best
    best = pick_best(responses)

    # Backup
    backup_path = backup()

    # Apply
    applied = apply(best["code"])

    # Rate
    score = rate_bot(len(files), applied)

    # Report
    send_report({
        "files": len(files),
        "applied": applied,
        "ai": best["ai"],
        "backup": backup_path,
        "score": score,
        "time": ts,
        "ai_responses": responses,
    })

    print("═" * 50)
    print(f"👑 DONE: {applied} files upgraded by {best['ai']}")
    print("═" * 50)


if __name__ == "__main__":
    main()
