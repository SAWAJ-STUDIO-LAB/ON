"""
👑 KING — Ultra Fixed
- Strong IGNORE (755 → 190)
- 1/3 consensus (approval badhega)
- Auto syntax fix
- Model names updated
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

# ⭐ ULTRA STRONG IGNORE
IGNORE = {
    "__pycache__", ".git", ".github", "output",
    "_work", "_backups", "_logs", "venv", "node_modules",
    "bot update upgrade", "Code editor", "_temp_builder",
    "htmlcov", ".pytest_cache", ".mypy_cache",
}

# ⭐ Additional path-based skip
SKIP_PATH_PARTS = [
    "bot update upgrade",
    "Code editor",
    "_temp_builder",
    "_backups",
    "_work",
    "_logs",
]

CODE_EXT = {".py"}
TIMEOUT = 300
MAX_RETRIES = 3
MAX_ROUNDS = 3
MAX_CHUNK_KB = 300

# ⭐ 1/3 consensus (koi bhi 1 AI YES bole toh approve)
MIN_CONSENSUS = 1
CONSENSUS_TOTAL = 3

ALL_AIS = ["OpenRouter", "Groq", "Gemini"]


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
# DEEP SCAN
# ═══════════════════════════════════════════════
def _is_skipped(path):
    """Check if path should be skipped."""
    for part in SKIP_PATH_PARTS:
        if part in path:
            return True
    return False


def deep_scan():
    result = {"code": [], "folders": [], "empty_files": [], "total_size_kb": 0}
    for root, dirs, fnames in os.walk(BOT_ROOT):
        # Skip dirs
        dirs[:] = [d for d in dirs if d not in IGNORE
                   and not _is_skipped(os.path.join(root, d))]
        rel_dir = os.path.relpath(root, BOT_ROOT)
        if rel_dir != ".":
            result["folders"].append(rel_dir)
        for fn in fnames:
            full = os.path.join(root, fn)
            if _is_skipped(full):
                continue
            rel = os.path.relpath(full, BOT_ROOT)
            ext = os.path.splitext(fn)[1].lower()
            size = 0
            try:
                size = os.path.getsize(full)
                result["total_size_kb"] += size // 1024
            except Exception:
                pass
            if ext in CODE_EXT:
                result["code"].append(rel)
            if size == 0:
                result["empty_files"].append(rel)
    for k in ("code", "folders", "empty_files"):
        result[k] = sorted(result[k])
    return result


# ═══════════════════════════════════════════════
# AI CALLS
# ═══════════════════════════════════════════════
def _post(url, headers, payload, timeout=TIMEOUT):
    for attempt in range(1, MAX_RETRIES + 1):
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


def call_one_ai(ai_name, prompt, max_tokens=8000):
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
        for model in ["llama-3.1-70b-versatile",
                      "llama-3.1-8b-instant",
                      "llama3-70b-8192"]:
            d = _post("https://api.groq.com/openai/v1/chat/completions",
                      {"Authorization": f"Bearer {key}"},
                      {"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": max_tokens, "temperature": 0.3})
            if d:
                return d["choices"][0]["message"]["content"]
        return None

    if ai_name == "Gemini":
        key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not key:
            return None
        for model in ["gemini-1.5-flash-latest",
                      "gemini-1.5-flash",
                      "gemini-pro"]:
            d = _post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                {},
                {"contents": [{"parts": [{"text": prompt}]}],
                 "generationConfig": {"maxOutputTokens": max_tokens,
                                      "temperature": 0.3}})
            if d:
                return d["candidates"][0]["content"]["parts"][0]["text"]
        return None

    return None


# ═══════════════════════════════════════════════
# FIND TASKS
# ═══════════════════════════════════════════════
FIND_TASKS_PROMPT = """List up to 3 tasks that NEED upgrading in this bot.

Format (one per line):
TASK: what to do
TARGET: file path or "ALL"
PRIORITY: 1-10

If nothing needs upgrading: TASK: DONE

CODE:
{code}
"""


def parse_tasks(text):
    if not text:
        return []
    tasks, current = [], {}
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("TASK:"):
            if current:
                tasks.append(current)
            current = {"task": line.replace("TASK:", "").strip()}
        elif line.startswith("TARGET:") and current:
            current["target"] = line.replace("TARGET:", "").strip()
        elif line.startswith("PRIORITY:") and current:
            try:
                current["priority"] = int(line.replace("PRIORITY:", "").strip())
            except Exception:
                current["priority"] = 5
    if current:
        tasks.append(current)
    return [t for t in tasks if t.get("task", "").upper() != "DONE"]


def find_tasks(code):
    for ai in ALL_AIS:
        print(f"    🔍 {ai} finding tasks...")
        text = call_one_ai(ai, FIND_TASKS_PROMPT.format(code=code),
                           max_tokens=2000)
        if text and "TASK:" in text:
            tasks = parse_tasks(text)
            if tasks:
                return tasks
    return []


# ═══════════════════════════════════════════════
# CONSENSUS — 1/3 (relaxed)
# ═══════════════════════════════════════════════
VERIFY_PROMPT = """Is this upgrade task SAFE and USEFUL?

TASK: {task}
TARGET: {target}

Answer ONE word: YES or NO
"""


def get_consensus(task, code):
    prompt = VERIFY_PROMPT.format(
        task=task.get("task", ""),
        target=task.get("target", "ALL"))
    yes = 0
    for ai in ALL_AIS:
        print(f"      🗳️ {ai}...")
        text = call_one_ai(ai, prompt, max_tokens=50)
        if not text:
            continue
        if "YES" in text.upper():
            yes += 1
            print(f"         ✅ YES")
        else:
            print(f"         ❌ NO")
    return yes


# ═══════════════════════════════════════════════
# UPGRADE
# ═══════════════════════════════════════════════
UPGRADE_PROMPT = """Upgrade these files based on this task:

TASK: {task}
TARGET: {target}

RULES:
1. Return ONLY upgraded files
2. FORMAT: ═══ FILE: path ═══  code  ═══ END ═══
3. NEVER delete — only modify or create
4. Fix ALL syntax errors if found
5. NO explanations

INPUT:
{code}
"""


def get_best_upgrade(task, code):
    prompt = UPGRADE_PROMPT.format(
        task=task.get("task", ""),
        target=task.get("target", "ALL"),
        code=code)
    responses = []
    for ai in ALL_AIS:
        print(f"      🔧 {ai}...")
        text = call_one_ai(ai, prompt, max_tokens=16000)
        if text and "═══ FILE:" in text:
            fcount = text.count("═══ FILE:")
            responses.append({"ai": ai, "code": text, "files": fcount})
            print(f"         ✅ {fcount} files")
    if not responses:
        return None
    return max(responses, key=lambda r: r["files"] * 10000 + len(r["code"]))


# ═══════════════════════════════════════════════
# AUTO SYNTAX FIX
# ═══════════════════════════════════════════════
def fix_syntax_error(filepath, error_msg):
    """Send a broken file to AI for fixing."""
    full = os.path.join(BOT_ROOT, filepath)
    try:
        with open(full, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception:
        return False

    prompt = f"""Fix the SYNTAX ERROR in this Python file.

ERROR: {error_msg}

FILE: {filepath}

RULES:
1. Fix ONLY the syntax error
2. KEEP the file's logic intact
3. Return ONLY the fixed code, no explanations
4. NO markdown, NO code fences

CODE:
{code}"""

    for ai in ALL_AIS:
        print(f"      🔧 Fix with {ai}...")
        text = call_one_ai(ai, prompt, max_tokens=8000)
        if text and len(text) > 50:
            # Clean up code fences if present
            cleaned = text.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                cleaned = "\n".join(lines)
            try:
                ast.parse(cleaned)
                with open(full, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                return True
            except SyntaxError:
                continue
    return False


# ═══════════════════════════════════════════════
# COMBINE
# ═══════════════════════════════════════════════
def combine_files(files, tag="all"):
    path = f"{WORK}/{tag}.txt"
    with open(path, "w", encoding="utf-8") as out:
        out.write(f"# {len(files)} files\n\n")
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


def chunk_by_size(files, max_kb=MAX_CHUNK_KB):
    chunks, current, csize = [], [], 0
    for f in files:
        full = os.path.join(BOT_ROOT, f)
        try:
            fsize = os.path.getsize(full) // 1024
        except Exception:
            fsize = 0
        if current and csize + fsize > max_kb:
            chunks.append(current)
            current, csize = [], 0
        current.append(f)
        csize += fsize
    if current:
        chunks.append(current)
    return chunks


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
# APPLY
# ═══════════════════════════════════════════════
def apply_with_tracking(text):
    changes = {"modified": [], "created": []}

    for rel, code in re.findall(r"═══ NEW FILE: (.+?) ═══\n(.*?)\n═══ END ═══",
                                text, re.DOTALL):
        rel = rel.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        changes["created"].append(rel)

    for rel, code in re.findall(r"═══ FILE: (.+?) ═══\n(.*?)\n═══ END ═══",
                                text, re.DOTALL):
        rel = rel.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        changes["modified"].append(rel)

    return changes


# ═══════════════════════════════════════════════
# SCORE
# ═══════════════════════════════════════════════
def rate_bot(files, changes, syntax_failed):
    if changes == 0:
        return 3
    ratio = changes / max(files, 1)
    base = int(4 + min(ratio, 1.0) * 6)
    if syntax_failed > 0:
        base -= min(2, syntax_failed // 10)
    return min(10, max(1, base))


# ═══════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════
def send_report(data):
    ts = data["time"]
    files = data["files"]
    score = data["score"]
    backup_path = data["backup"] or "N/A"
    rounds = data["rounds"]
    tasks_total = data["tasks_total"]
    tasks_approved = data["tasks_approved"]
    modified = data["modified"]
    created = data["created"]
    syntax_failed = data["syntax_failed"]
    syntax_fixed = data["syntax_fixed"]

    bar = "█" * score + "░" * (10 - score)

    msg = (
        "👑 <b>KING REPORT — ULTRA FIXED</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <code>{ts}</code>\n"
        "\n"
        "📁 <b>SCAN:</b>\n"
        f"   • Files: <b>{files}</b>\n"
        "\n"
        "🗳️ <b>CONSENSUS (3 AI):</b>\n"
        f"   • Tasks found: <b>{tasks_total}</b>\n"
        f"   • ✅ Approved: <b>{tasks_approved}</b>\n"
        "\n"
        f"🔁 <b>ROUNDS:</b> <b>{rounds}</b>\n"
        "\n"
        "🔧 <b>ACTIONS:</b>\n"
        f"   ✏️ Modified: <b>{len(modified)}</b>\n"
        f"   📁 Created: <b>{len(created)}</b>\n"
        f"   🩹 Syntax fixed: <b>{syntax_fixed}</b>\n"
        f"   🗑️ Deleted: <b>0</b>\n"
        "\n"
        f"⚠️ Syntax remaining: {len(syntax_failed)}\n"
        f"💾 Backup: <code>{backup_path}</code>\n"
        "\n"
        "📈 <b>SCORE:</b>\n"
        f"   {bar} <b>{score}/10</b>\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>World #1 in progress</b>"
    )
    tg_send(msg)

    if modified:
        m = "✏️ <b>MODIFIED:</b>\n"
        for f in modified[:25]:
            m += f"• <code>{f}</code>\n"
        if len(modified) > 25:
            m += f"\n+{len(modified) - 25} more"
        tg_send(m)

    if created:
        c = "📁 <b>CREATED:</b>\n"
        for f in created[:25]:
            c += f"• <code>{f}</code>\n"
        tg_send(c)


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════
def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("═" * 60)
    print("👑 KING — ULTRA FIXED")
    print("═" * 60)

    tg_send(f"👑 <b>KING ACTIVATED</b>\n🕐 {ts}", silent=True)

    os.makedirs(WORK, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    scan = deep_scan()
    files = scan["code"]
    print(f"📁 Files: {len(files)}")

    if not files:
        tg_send("⚠️ No files.")
        return

    backup_path = backup()
    print(f"💾 Backup: {backup_path}")

    # ⭐ STEP 0: FIX EXISTING SYNTAX ERRORS
    print("\n🩹 STEP 0: Fix syntax errors...")
    syntax_failed = []
    for rel in files:
        full = os.path.join(BOT_ROOT, rel)
        try:
            with open(full, "r", encoding="utf-8") as f:
                ast.parse(f.read())
        except SyntaxError as e:
            syntax_failed.append({"file": rel, "error": str(e)[:80]})
        except Exception:
            pass

    print(f"  Found {len(syntax_failed)} syntax errors")
    syntax_fixed = 0
    for i, s in enumerate(syntax_failed, 1):
        print(f"  [{i}/{len(syntax_failed)}] Fixing {s['file']}")
        if fix_syntax_error(s["file"], s["error"]):
            syntax_fixed += 1
            print(f"    ✅ Fixed")
        else:
            print(f"    ❌ Failed")

    # Re-scan syntax
    syntax_failed = []
    for rel in files:
        full = os.path.join(BOT_ROOT, rel)
        try:
            with open(full, "r", encoding="utf-8") as f:
                ast.parse(f.read())
        except SyntaxError as e:
            syntax_failed.append({"file": rel, "error": str(e)[:80]})
        except Exception:
            pass
    print(f"  Remaining: {len(syntax_failed)}")

    # ⭐ MAIN LOOP
    total_modified = []
    total_created = []
    total_tasks = 0
    total_approved = 0
    round_details = []

    for round_n in range(1, MAX_ROUNDS + 1):
        print(f"\n{'═' * 50}")
        print(f"🔁 ROUND {round_n}/{MAX_ROUNDS}")
        print(f"{'═' * 50}")

        chunks = chunk_by_size(files)
        all_tasks = []
        for ci, chunk in enumerate(chunks, 1):
            combined = combine_files(chunk, f"find_r{round_n}_c{ci}")
            tasks = find_tasks(combined)
            if tasks:
                all_tasks.extend(tasks)

        if not all_tasks:
            print(f"  ✅ No tasks — STOP")
            break

        total_tasks += len(all_tasks)
        approved_tasks = []

        for ti, task in enumerate(all_tasks, 1):
            print(f"\n  🗳️ Task {ti}/{len(all_tasks)}: {task['task'][:50]}")
            yes = get_consensus(task, "")
            print(f"      Votes: ✅{yes}")

            if yes >= MIN_CONSENSUS:
                approved_tasks.append(task)
                total_approved += 1
                print(f"      ✅ APPROVED")
            else:
                print(f"      ❌ REJECTED")

        if not approved_tasks:
            print(f"\n  ⏹️ No approvals — STOP")
            break

        round_modified = 0
        round_created = 0

        for ti, task in enumerate(approved_tasks, 1):
            print(f"\n  🔧 Upgrade {ti}/{len(approved_tasks)}")
            combined = combine_files(files, f"upgrade_r{round_n}_t{ti}")
            best = get_best_upgrade(task, combined)
            if not best:
                continue
            print(f"      🏆 {best['ai']} ({best['files']} files)")
            changes = apply_with_tracking(best["code"])
            total_modified.extend(changes["modified"])
            total_created.extend(changes["created"])
            round_modified += len(changes["modified"])
            round_created += len(changes["created"])

        round_details.append({
            "n": round_n, "tasks": len(approved_tasks),
            "modified": round_modified, "created": round_created,
        })

        if round_modified + round_created == 0:
            print(f"\n  ⏹️ No changes — STOP")
            break

    total_modified = sorted(set(total_modified))
    total_created = sorted(set(total_created))

    score = rate_bot(len(files),
                     len(total_modified) + len(total_created),
                     len(syntax_failed))

    send_report({
        "time": ts, "files": len(files),
        "rounds": len(round_details),
        "tasks_total": total_tasks,
        "tasks_approved": total_approved,
        "modified": total_modified,
        "created": total_created,
        "score": score, "backup": backup_path,
        "syntax_failed": syntax_failed,
        "syntax_fixed": syntax_fixed,
    })

    print("\n" + "═" * 60)
    print(f"👑 DONE: {len(total_modified)}M {len(total_created)}C "
          f"({syntax_fixed} syntax fixed) — Score {score}/10")
    print("═" * 60)


if __name__ == "__main__":
    main()
