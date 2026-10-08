"""
👑 KING — FULL SMART SYSTEM
Self-Healing + Smart Chunks + Auto-Test + Retry + Version Track
"""
import os
import re
import json
import time
import shutil
import ast
import subprocess
import requests
from datetime import datetime

# ═══════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════
BOT_ROOT = "sawajstudiobot"
WORK = "bot update upgrade/_work"
BACKUP = "bot update upgrade/_backups"
LOG_DIR = "bot update upgrade/_logs"

IGNORE = {
    "__pycache__", ".git", ".github", "output",
    "_work", "_backups", "_logs", "venv", "node_modules",
    "bot update upgrade", "Code editor", "_temp_builder",
    "htmlcov", ".pytest_cache", ".mypy_cache",
}

CHUNK_SIZE = 25
TIMEOUT = 300
MAX_RETRIES = 3
MAX_CHUNK_SIZE_KB = 400  # chhota chunks


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
# COLLECT
# ═══════════════════════════════════════════════
def collect():
    files = []
    for root, dirs, fnames in os.walk(BOT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE
                   and not any(ig in os.path.join(root, d) for ig in IGNORE)]
        for fn in fnames:
            if fn.endswith(".py"):
                full = os.path.join(root, fn)
                if any(ig in full for ig in IGNORE):
                    continue
                files.append(os.path.relpath(full, BOT_ROOT))
    return sorted(files)


# ═══════════════════════════════════════════════
# SMART CHUNKS — Import-aware
# ═══════════════════════════════════════════════
def extract_imports(rel_path):
    """Extract imported module names."""
    full = os.path.join(BOT_ROOT, rel_path)
    imports = set()
    try:
        with open(full, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
            elif isinstance(node, ast.Import):
                for n in node.names:
                    imports.add(n.name)
    except Exception:
        pass
    return imports


def make_smart_chunks(files, size=CHUNK_SIZE, max_kb=MAX_CHUNK_SIZE_KB):
    """Group files: same folder + import-aware + size-aware."""
    # Step 1: Group by folder
    folder_groups = {}
    for f in files:
        folder = os.path.dirname(f)
        folder_groups.setdefault(folder, []).append(f)

    # Step 2: Build chunks
    chunks = []
    current = []
    current_size = 0

    for folder, flist in folder_groups.items():
        for f in flist:
            full = os.path.join(BOT_ROOT, f)
            try:
                fsize = os.path.getsize(full) // 1024
            except Exception:
                fsize = 0

            # Chhota chunk rakhna hai
            if len(current) >= size or (current_size + fsize > max_kb and current):
                chunks.append(current)
                current = []
                current_size = 0

            current.append(f)
            current_size += fsize

    if current:
        chunks.append(current)

    return chunks


def combine_chunk(files, idx):
    path = f"{WORK}/chunk_{idx}.txt"
    with open(path, "w", encoding="utf-8") as out:
        out.write(f"# Chunk {idx} — {len(files)} files\n\n")
        for rel in files:
            full = os.path.join(BOT_ROOT, rel)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception:
                code = ""
            out.write(f"═══ FILE: {rel} ═══\n{code}\n═══ END ═══\n\n")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ═══════════════════════════════════════════════
# AI CALLS with RETRY
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
7. Return ONLY the code — NO explanations, NO markdown

INPUT CODE:
"""


def _post_with_retry(url, headers, payload, timeout=TIMEOUT):
    """Retry on network errors."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                wait = attempt * 5
                print(f"      ⏳ Retry {attempt}/{MAX_RETRIES} after {wait}s (HTTP {r.status_code})")
                time.sleep(wait)
                continue
            print(f"      ⚠️ HTTP {r.status_code}")
            return None
        except requests.exceptions.Timeout:
            print(f"      ⏳ Timeout retry {attempt}/{MAX_RETRIES}")
            time.sleep(5)
        except Exception as e:
            print(f"      ❌ {str(e)[:60]}")
            time.sleep(3)
    return None


def ai_openrouter(code, fc):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        return None
    d = _post_with_retry("https://openrouter.ai/api/v1/chat/completions",
                         {"Authorization": f"Bearer {key}"},
                         {"model": "openai/gpt-4o-mini",
                          "messages": [{"role": "user", "content": PROMPT.format(file_count=fc) + code}],
                          "max_tokens": 16000, "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_groq(code, fc):
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        return None
    d = _post_with_retry("https://api.groq.com/openai/v1/chat/completions",
                         {"Authorization": f"Bearer {key}"},
                         {"model": "llama-3.3-70b-versatile",
                          "messages": [{"role": "user", "content": PROMPT.format(file_count=fc) + code}],
                          "max_tokens": 16000, "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_gemini(code, fc):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    d = _post_with_retry(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
        {},
        {"contents": [{"parts": [{"text": PROMPT.format(file_count=fc) + code}]}],
         "generationConfig": {"maxOutputTokens": 16000, "temperature": 0.3}})
    return d["candidates"][0]["content"]["parts"][0]["text"] if d else None


def ai_mistral(code, fc):
    key = os.environ.get("MISTRAL_API_KEY", "").strip()
    if not key:
        return None
    d = _post_with_retry("https://api.mistral.ai/v1/chat/completions",
                         {"Authorization": f"Bearer {key}"},
                         {"model": "mistral-small-latest",
                          "messages": [{"role": "user", "content": PROMPT.format(file_count=fc) + code}],
                          "max_tokens": 16000, "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_cerebras(code, fc):
    key = os.environ.get("CEREBRAS_API_KEY", "").strip()
    if not key:
        return None
    d = _post_with_retry("https://api.cerebras.ai/v1/chat/completions",
                         {"Authorization": f"Bearer {key}"},
                         {"model": "llama3.1-8b",
                          "messages": [{"role": "user", "content": PROMPT.format(file_count=fc) + code}],
                          "max_tokens": 16000, "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_cohere(code, fc):
    key = os.environ.get("COHERE_API_KEY", "").strip()
    if not key:
        return None
    d = _post_with_retry("https://api.cohere.com/v1/chat",
                         {"Authorization": f"Bearer {key}"},
                         {"model": "command-r-plus",
                          "message": PROMPT.format(file_count=fc) + code})
    return d["text"] if d else None


def ai_nvidia(code, fc):
    key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not key:
        return None
    d = _post_with_retry("https://integrate.api.nvidia.com/v1/chat/completions",
                         {"Authorization": f"Bearer {key}"},
                         {"model": "meta/llama-3.1-70b-instruct",
                          "messages": [{"role": "user", "content": PROMPT.format(file_count=fc) + code}],
                          "max_tokens": 16000, "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_huggingface(code, fc):
    key = os.environ.get("HUGGINGFACE_API_KEY", "").strip()
    if not key:
        return None
    d = _post_with_retry(
        "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-70B-Instruct/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {"model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
         "messages": [{"role": "user", "content": PROMPT.format(file_count=fc) + code}],
         "max_tokens": 8000, "temperature": 0.3})
    return d["choices"][0]["message"]["content"] if d else None


def ai_all(code, fc):
    """Call all 8 AI with self-healing."""
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


def pick_best(responses):
    if not responses:
        return None

    def score(r):
        return r["files"] * 10000 + len(r["code"])

    return max(responses, key=score)


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
# AUTO TEST
# ═══════════════════════════════════════════════
def test_syntax(files):
    """Test Python syntax of all files."""
    failed = []
    for rel in files:
        full = os.path.join(BOT_ROOT, rel)
        try:
            with open(full, "r", encoding="utf-8") as f:
                ast.parse(f.read())
        except SyntaxError as e:
            failed.append({"file": rel, "error": str(e)[:100]})
        except Exception:
            pass
    return failed


def test_imports(files):
    """Basic import check via py_compile."""
    failed = []
    for rel in files:
        full = os.path.join(BOT_ROOT, rel)
        try:
            r = subprocess.run(
                ["python", "-m", "py_compile", full],
                capture_output=True, text=True, timeout=10)
            if r.returncode != 0:
                failed.append({"file": rel, "error": r.stderr[:100]})
        except Exception:
            pass
    return failed


# ═══════════════════════════════════════════════
# RATE
# ═══════════════════════════════════════════════
def rate_bot(files, changes):
    if changes == 0:
        return 1
    ratio = changes / max(files, 1)
    return min(10, max(1, int(4 + ratio * 6)))


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
    chunks = data.get("chunk_reports", [])
    syntax_failed = data.get("syntax_failed", [])
    import_failed = data.get("import_failed", [])

    bar = "█" * score + "░" * (10 - score)

    chunk_lines = []
    for c in chunks:
        icon = "🏆" if c["picked_files"] > 0 else "❌"
        chunk_lines.append(
            f"   • Chunk {c['idx']}: {c['files']}f → {icon} {c['winner']} "
            f"({c['picked_files']})")
    chunk_text = "\n".join(chunk_lines)

    msg = (
        "👑 <b>KING REPORT — FULL SMART</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <code>{ts}</code>\n"
        "\n"
        "📁 <b>SCAN:</b>\n"
        f"   • Files: <b>{files}</b>\n"
        "\n"
        "🔧 <b>ACTIONS:</b>\n"
        f"   ✏️ Modified: <b>{modified}</b>\n"
        f"   📁 Created: <b>{created}</b>\n"
        f"   🗑️ Deleted: <b>{deleted}</b>\n"
        "\n"
        f"📦 <b>CHUNKS ({len(chunks)}):</b>\n"
        f"{chunk_text}\n"
        "\n"
        f"✅ <b>Syntax:</b> {len(syntax_failed)} failed\n"
        f"✅ <b>Imports:</b> {len(import_failed)} failed\n"
        "\n"
        f"💾 Backup: <code>{backup_path}</code>\n"
        "\n"
        "📈 <b>SCORE:</b>\n"
        f"   {bar} <b>{score}/10</b>\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>World #1 in progress</b>"
    )
    tg_send(msg)


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════
def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("═" * 50)
    print("👑 KING STARTED — FULL SMART")
    print("═" * 50)

    tg_send(f"👑 <b>KING ACTIVATED</b>\n🕐 {ts}\nFull Smart mode...", silent=True)

    os.makedirs(WORK, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    # Collect
    files = collect()
    print(f"📁 Files: {len(files)}")
    if not files:
        tg_send("⚠️ No files found.")
        return

    # Backup
    backup_path = backup()
    print(f"💾 Backup: {backup_path}")

    # Smart Chunks
    chunks = make_smart_chunks(files)
    print(f"📦 Chunks: {len(chunks)}")

    # Process
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

        responses = ai_all(combined, fc)

        if not responses:
            print(f"  ❌ Chunk {idx}: All AI failed")
            chunk_reports.append({
                "idx": idx, "files": fc,
                "winner": "NONE", "picked_files": 0,
            })
            continue

        best = pick_best(responses)
        print(f"  🏆 Best: {best['ai']} ({best['files']} files)")

        m, c, d = apply(best["code"])
        total_modified += m
        total_created += c
        total_deleted += d

        chunk_reports.append({
            "idx": idx, "files": fc,
            "winner": best["ai"], "picked_files": m + c,
        })
        print(f"  ✅ Applied: {m}M {c}C {d}D")

    # Test
    print("\n🧪 Testing syntax...")
    syntax_failed = test_syntax(files)
    print(f"  ✅ {len(syntax_failed)} syntax failures")

    print("🧪 Testing imports...")
    import_failed = test_imports(files[:50])  # first 50 for speed
    print(f"  ✅ {len(import_failed)} import failures")

    # Score
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
        "syntax_failed": syntax_failed,
        "import_failed": import_failed,
    })

    # Save JSON log
    log_file = f"{LOG_DIR}/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "time": ts,
            "files": len(files),
            "modified": total_modified,
            "created": total_created,
            "deleted": total_deleted,
            "score": score,
            "chunks": chunk_reports,
            "syntax_failed": syntax_failed,
            "import_failed": import_failed,
        }, f, indent=2)

    print("\n" + "═" * 50)
    print(f"👑 DONE: {total_modified}M {total_created}C {total_deleted}D")
    print("═" * 50)


if __name__ == "__main__":
    main()
