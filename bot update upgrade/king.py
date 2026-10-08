"""
👑 KING — Bot Update Upgrade (CHUNKS + 8 AI + FULL WORKING)
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

# Strong IGNORE — kuch bhi backup/cache ka scan nahi hoga
IGNORE = {
    "__pycache__", ".git", ".github", "output",
    "_work", "_backups", "venv", "node_modules",
    "bot update upgrade", "Code editor", "_temp_builder",
    "htmlcov", ".pytest_cache", ".mypy_cache",
}

# AI chunk size — 30 files per chunk (safe limit)
CHUNK_SIZE = 30

# Timeout (300 sec = 5 min per AI)
TIMEOUT = 300


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
    except Exception as e:
        print(f"❌ Telegram: {e}")
        return False


# ═══════════════════════════════════════════════
# COLLECT
# ═══════════════════════════════════════════════
def collect():
    files = []
    for root, dirs, fnames in os.walk(BOT_ROOT):
        # Strong ignore — dir name ya path ka koi bhi hissa match kare
        dirs[:] = [d for d in dirs if d not in IGNORE
                   and not any(ig in os.path.join(root, d) for ig in IGNORE)]
        for fn in fnames:
            if fn.endswith(".py"):
                full = os.path.join(root, fn)
                # Skip agar path mein kuch ignore wala hai
                if any(ig in full for ig in IGNORE):
                    continue
                files.append(os.path.relpath(full, BOT_ROOT))
    return sorted(files)


# ═══════════════════════════════════════════════
# CHUNKS — Files ko chhote groups mein baanto
# ═══════════════════════════════════════════════
def make_chunks(files, size=CHUNK_SIZE):
    """Split files into chunks."""
    chunks = []
    for i in range(0, len(files), size):
        chunks.append(files[i:i + size])
    return chunks


def combine_chunk(files, chunk_idx):
    """Combine chunk files into 1 string."""
    os.makedirs(WORK, exist_ok=True)
    path = f"{WORK}/chunk_{chunk_idx}.txt"
    with open(path, "w", encoding="utf-8") as out:
        out.write(f"# Chunk {chunk_idx} — {len(files)} files\n\n")
        for rel in files:
            full = os.path.join(BOT_ROOT, rel)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception:
                code = ""
            out.write(f"═══ FILE: {rel} ═══\n{code}\n═══ END ═══\n\n")
    size_kb = os.path.getsize(path) // 1024
    print(f"  📦 Chunk {chunk_idx}: {len(files)} files → {size_kb} KB")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ═══════════════════════════════════════════════
# AI CALLS
# ═══════════════════════════════════════════════
PROMPT = """You are a senior Python engineer. Upgrade this bot code to be WORLD #1.

CRITICAL RULES:
1. Return ALL {file_count} files from input — do NOT skip any
2. Do NOT summarize — return FULL code for each file
3. KEEP EXACT SAME FORMAT:
   ═══ FILE: path ═══
   <full code>
   ═══ END ═══
4. Make code BETTER, cleaner, faster, well-documented
5. Fix bugs, add error handling, add fallbacks
6. Remove any copyright text
7. Return ONLY the code — NO explanations, NO markdown, NO chat

INPUT CODE:
"""


def _post(url, headers, payload, timeout=TIMEOUT):
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        print(f"    ⚠️ HTTP {r.status_code}: {r.text[:80]}")
    except Exception as e:
        print(f"    ❌ {str(e)[:80]}")
    return None


def ai_openrouter(code, fc):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://openrouter.ai/api/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "openai/gpt-4o-mini",
               "messages": [{"role": "user",
                             "content": PROMPT.format(file_count=fc) + code}],
               "max_tokens": 16000,
               "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_groq(code, fc):
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://api.groq.com/openai/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "llama-3.3-70b-versatile",
               "messages": [{"role": "user",
                             "content": PROMPT.format(file_count=fc) + code}],
               "max_tokens": 16000,
               "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_gemini(code, fc):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    d = _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
        {},
        {"contents": [{"parts": [{"text": PROMPT.format(file_count=fc) + code}]}],
         "generationConfig": {"maxOutputTokens": 16000, "temperature": 0.3}})
    return d["candidates"][0]["content"]["parts"][0]["text"] if d else None


def ai_mistral(code, fc):
    key = os.environ.get("MISTRAL_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://api.mistral.ai/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "mistral-small-latest",
               "messages": [{"role": "user",
                             "content": PROMPT.format(file_count=fc) + code}],
               "max_tokens": 16000,
               "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_cerebras(code, fc):
    key = os.environ.get("CEREBRAS_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://api.cerebras.ai/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "llama3.1-8b",
               "messages": [{"role": "user",
                             "content": PROMPT.format(file_count=fc) + code}],
               "max_tokens": 16000,
               "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_cohere(code, fc):
    key = os.environ.get("COHERE_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://api.cohere.com/v1/chat",
              {"Authorization": f"Bearer {key}"},
              {"model": "command-r-plus",
               "message": PROMPT.format(file_count=fc) + code})
    return d["text"] if d else None


def ai_nvidia(code, fc):
    key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not key:
        return None
    d = _post("https://integrate.api.nvidia.com/v1/chat/completions",
              {"Authorization": f"Bearer {key}"},
              {"model": "meta/llama-3.1-70b-instruct",
               "messages": [{"role": "user",
                             "content": PROMPT.format(file_count=fc) + code}],
               "max_tokens": 16000,
               "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_huggingface(code, fc):
    key = os.environ.get("HUGGINGFACE_API_KEY", "").strip()
    if not key:
        return None
    d = _post(
        "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-70B-Instruct/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {"model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
         "messages": [{"role": "user",
                       "content": PROMPT.format(file_count=fc) + code}],
         "max_tokens": 8000,
         "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_all(code, fc):
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
        print(f"    🤖 {name}...")
        try:
            res = fn(code, fc)
            if res and "═══ FILE:" in res:
                files_in_res = res.count("═══ FILE:")
                responses.append({"ai": name, "code": res, "files": files_in_res})
                print(f"      ✅ {name}: {files_in_res} files, {len(res)} chars")
            else:
                print(f"      ⚠️ {name}: invalid")
        except Exception as e:
            print(f"      ❌ {name}: {str(e)[:60]}")
    return responses


# ═══════════════════════════════════════════════
# PICK BEST
# ═══════════════════════════════════════════════
def pick_best(responses):
    if not responses:
        return None

    def score(r):
        return r["files"] * 10000 + len(r["code"])

    best = max(responses, key=score)
    return best


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
    except Exception as e:
        print(f"⚠️ Backup: {e}")
        return None


# ═══════════════════════════════════════════════
# APPLY
# ═══════════════════════════════════════════════
def apply(text):
    modified = 0
    created = 0
    deleted = 0

    # DELETE
    for match in re.findall(r"═══ DELETE: (.+?) ═══", text):
        rel = match.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        if os.path.exists(full):
            try:
                os.remove(full)
                deleted += 1
            except Exception:
                pass

    # NEW FILES
    for rel, code in re.findall(r"═══ NEW FILE: (.+?) ═══\n(.*?)\n═══ END ═══",
                                text, re.DOTALL):
        rel = rel.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        created += 1

    # MODIFY
    for rel, code in re.findall(r"═══ FILE: (.+?) ═══\n(.*?)\n═══ END ═══",
                                text, re.DOTALL):
        rel = rel.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        modified += 1

    return modified, created, deleted


# ═══════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════
def send_report(data):
    ts = data["time"]
    files = data["files"]
    modified = data["modified"]
    created = data["created"]
    deleted = data["deleted"]
    score = data["score"]
    backup_path = data["backup"] or "N/A"
    chunk_reports = data.get("chunk_reports", [])

    bar = "█" * score + "░" * (10 - score)

    chunk_lines = []
    for c in chunk_reports:
        chunk_lines.append(
            f"   • Chunk {c['idx']}: {c['files']} files → "
            f"🏆 {c['winner']} ({c['picked_files']} upgraded)")
    chunk_text = "\n".join(chunk_lines)

    msg = (
        "👑 <b>KING REPORT — FULL UPGRADE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <code>{ts}</code>\n"
        "\n"
        "📁 <b>SCAN:</b>\n"
        f"   • Files scanned: <b>{files}</b>\n"
        "\n"
        "🔧 <b>ACTIONS:</b>\n"
        f"   ✏️ Modified: <b>{modified}</b>\n"
        f"   📁 Created: <b>{created}</b>\n"
        f"   🗑️ Deleted: <b>{deleted}</b>\n"
        "\n"
        "📦 <b>CHUNKS:</b>\n"
        f"{chunk_text}\n"
        "\n"
        f"💾 Backup: <code>{backup_path}</code>\n"
        "\n"
        "📈 <b>BOT SCORE:</b>\n"
        f"   {bar} <b>{score}/10</b>\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>World #1 in progress</b>"
    )
    tg_send(msg)


# ═══════════════════════════════════════════════
# RATE
# ═══════════════════════════════════════════════
def rate_bot(files, total_changes):
    if total_changes == 0:
        return 1
    ratio = total_changes / max(files, 1)
    score = int(4 + ratio * 6)
    return min(10, max(1, score))


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════
def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("═" * 50)
    print("👑 KING STARTED — CHUNKS MODE")
    print("═" * 50)

    tg_send(f"👑 <b>KING ACTIVATED</b>\n🕐 {ts}\nWorking...", silent=True)

    # Collect
    files = collect()
    print(f"📁 Files: {len(files)}")
    if not files:
        tg_send("⚠️ No files found.")
        return

    # Chunks
    chunks = make_chunks(files)
    print(f"📦 Chunks: {len(chunks)}")

    # Backup before anything
    backup_path = backup()

    # Process each chunk
    chunk_reports = []
    total_modified = 0
    total_created = 0
    total_deleted = 0

    for idx, chunk_files in enumerate(chunks, 1):
        print(f"\n{'═' * 40}")
        print(f"📦 CHUNK {idx}/{len(chunks)} — {len(chunk_files)} files")
        print(f"{'═' * 40}")

        combined = combine_chunk(chunk_files, idx)
        fc = len(chunk_files)

        print(f"  🤖 Calling 8 AI...")
        responses = ai_all(combined, fc)

        if not responses:
            print(f"  ❌ Chunk {idx}: All AI failed")
            chunk_reports.append({
                "idx": idx, "files": fc,
                "winner": "NONE", "picked_files": 0,
            })
            continue

        best = pick_best(responses)
        print(f"  🏆 Winner: {best['ai']} ({best['files']} files)")

        m, c, d = apply(best["code"])
        total_modified += m
        total_created += c
        total_deleted += d

        chunk_reports.append({
            "idx": idx, "files": fc,
            "winner": best["ai"], "picked_files": m + c,
        })
        print(f"  ✅ Applied: {m} modified, {c} created, {d} deleted")

    # Rate
    score = rate_bot(len(files), total_modified + total_created)

    # Report
    send_report({
        "files": len(files),
        "modified": total_modified,
        "created": total_created,
        "deleted": total_deleted,
        "score": score,
        "backup": backup_path,
        "time": ts,
        "chunk_reports": chunk_reports,
    })

    print("\n" + "═" * 50)
    print(f"👑 DONE: {total_modified} modified, "
          f"{total_created} created, {total_deleted} deleted")
    print("═" * 50)


if __name__ == "__main__":
    main()
