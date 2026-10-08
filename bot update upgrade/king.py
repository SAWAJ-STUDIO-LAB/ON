"""
👑 KING — Consensus Mode
Ek AI nahi, saare 8 AI milke decide karenge.
Sab "Haan" → tab karo
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

IGNORE = {
    "__pycache__", ".git", ".github", "output",
    "_work", "_backups", "_logs", "venv", "node_modules",
    "bot update upgrade", "Code editor", "_temp_builder",
    "htmlcov", ".pytest_cache", ".mypy_cache",
}

CODE_EXT = {".py"}
CONFIG_EXT = {".json", ".yml", ".yaml", ".toml", ".txt", ".md", ".cfg", ".ini"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico"}

TIMEOUT = 300
MAX_RETRIES = 3
MAX_ROUNDS = 5
MAX_CHUNK_KB = 400
MIN_CONSENSUS = 6   # 8 AI mein se 6 ka "Haan" chahiye


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
def deep_scan():
    result = {"code": [], "config": [], "images": [],
              "folders": [], "empty_files": [], "total_size_kb": 0}
    for root, dirs, fnames in os.walk(BOT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE
                   and not any(ig in os.path.join(root, d) for ig in IGNORE)]
        rel_dir = os.path.relpath(root, BOT_ROOT)
        if rel_dir != ".":
            result["folders"].append(rel_dir)
        for fn in fnames:
            full = os.path.join(root, fn)
            if any(ig in full for ig in IGNORE):
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
            elif ext in CONFIG_EXT:
                result["config"].append(rel)
            elif ext in IMAGE_EXT:
                result["images"].append(rel)
            if size == 0:
                result["empty_files"].append(rel)
    for k in ("code", "config", "images", "folders", "empty_files"):
        result[k] = sorted(result[k])
    return result


# ═══════════════════════════════════════════════
# SINGLE AI CALL
# ═══════════════════════════════════════════════
def _post(url, headers, payload, timeout=TIMEOUT):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(attempt * 5)
                continue
            return None
        except requests.exceptions.Timeout:
            time.sleep(5)
        except Exception:
            time.sleep(3)
    return None


def call_one_ai(ai_name, prompt, max_tokens=8000):
    """Call one specific AI. Returns text or None."""
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
        d = _post("https://api.groq.com/openai/v1/chat/completions",
                  {"Authorization": f"Bearer {key}"},
                  {"model": "llama-3.3-70b-versatile",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": max_tokens, "temperature": 0.3})
        return d["choices"][0]["message"]["content"] if d else None

    if ai_name == "Gemini":
        key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not key:
            return None
        d = _post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
            {},
            {"contents": [{"parts": [{"text": prompt}]}],
             "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.3}})
        return d["candidates"][0]["content"]["parts"][0]["text"] if d else None

    if ai_name == "Mistral":
        key = os.environ.get("MISTRAL_API_KEY", "").strip()
        if not key:
            return None
        d = _post("https://api.mistral.ai/v1/chat/completions",
                  {"Authorization": f"Bearer {key}"},
                  {"model": "mistral-small-latest",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": max_tokens, "temperature": 0.3})
        return d["choices"][0]["message"]["content"] if d else None

    if ai_name == "Cerebras":
        key = os.environ.get("CEREBRAS_API_KEY", "").strip()
        if not key:
            return None
        d = _post("https://api.cerebras.ai/v1/chat/completions",
                  {"Authorization": f"Bearer {key}"},
                  {"model": "llama3.1-8b",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": max_tokens, "temperature": 0.3})
        return d["choices"][0]["message"]["content"] if d else None

    if ai_name == "Cohere":
        key = os.environ.get("COHERE_API_KEY", "").strip()
        if not key:
            return None
        d = _post("https://api.cohere.com/v1/chat",
                  {"Authorization": f"Bearer {key}"},
                  {"model": "command-r-plus", "message": prompt})
        return d["text"] if d else None

    if ai_name == "NVIDIA":
        key = os.environ.get("NVIDIA_API_KEY", "").strip()
        if not key:
            return None
        d = _post("https://integrate.api.nvidia.com/v1/chat/completions",
                  {"Authorization": f"Bearer {key}"},
                  {"model": "meta/llama-3.1-70b-instruct",
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": max_tokens, "temperature": 0.3})
        return d["choices"][0]["message"]["content"] if d else None

    if ai_name == "HuggingFace":
        key = os.environ.get("HUGGINGFACE_API_KEY", "").strip()
        if not key:
            return None
        d = _post(
            "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-70B-Instruct/v1/chat/completions",
            {"Authorization": f"Bearer {key}"},
            {"model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
             "messages": [{"role": "user", "content": prompt}],
             "max_tokens": min(max_tokens, 8000), "temperature": 0.3})
        return d["choices"][0]["message"]["content"] if d else None

    return None


ALL_AIS = ["OpenRouter", "Groq", "Gemini", "Mistral",
           "Cerebras", "Cohere", "NVIDIA", "HuggingFace"]


# ═══════════════════════════════════════════════
# CONSENSUS — sab AI se poochho
# ═══════════════════════════════════════════════
VERIFY_PROMPT = """You are a WORLD #1 senior Python engineer reviewing a proposed upgrade.

OTHER AI PROPOSED THIS TASK:
TASK: {task}
TARGET: {target}

BOT CODE:
{code}

QUESTION: Is this upgrade task REALLY NEEDED and SAFE?

Reply ONLY in this format:
VERDICT: YES  (if needed and safe)
VERDICT: NO   (if not needed or risky)
REASON: <one short sentence>

NO other text.
"""


def get_consensus(task, code):
    """Ask all 8 AI if this task is good. Return (yes_count, no_count, votes)."""
    prompt = VERIFY_PROMPT.format(
        task=task.get("task", ""),
        target=task.get("target", "ALL"),
        code=code[:80000])

    votes = {}
    yes = no = 0

    for ai in ALL_AIS:
        print(f"      🗳️ {ai} voting...")
        text = call_one_ai(ai, prompt, max_tokens=200)
        if not text:
            votes[ai] = "ABSTAIN"
            print(f"         ⚪ abstain")
            continue

        upper = text.upper()
        if "VERDICT: YES" in upper or "VERDICT:YES" in upper:
            votes[ai] = "YES"
            yes += 1
            print(f"         ✅ YES")
        elif "VERDICT: NO" in upper or "VERDICT:NO" in upper:
            votes[ai] = "NO"
            no += 1
            print(f"         ❌ NO")
        else:
            votes[ai] = "ABSTAIN"
            print(f"         ⚪ unclear")

    return yes, no, votes


# ═══════════════════════════════════════════════
# TASKS FINDER
# ═══════════════════════════════════════════════
FIND_TASKS_PROMPT = """You are a WORLD #1 senior Python engineer.
List up to 5 tasks that NEED upgrading in this bot.

Format (one per line, no extra text):
TASK: <what to do>
TARGET: <file path or "ALL">
PRIORITY: <1-10>

If nothing needs upgrading, write: TASK: DONE

BOT CODE:
{code}
"""


def find_tasks(code):
    """Ask one AI to find tasks."""
    for ai in ALL_AIS:
        print(f"    🔍 {ai} finding tasks...")
        text = call_one_ai(ai, FIND_TASKS_PROMPT.format(code=code),
                           max_tokens=2000)
        if text and "TASK:" in text:
            tasks = parse_tasks(text)
            if tasks:
                return tasks, ai
    return [], None


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


# ═══════════════════════════════════════════════
# UPGRADE (sab AI se best pick)
# ═══════════════════════════════════════════════
UPGRADE_PROMPT = """You are a WORLD #1 senior Python engineer.
Upgrade these files based on this task:

TASK: {task}
TARGET: {target}

RULES:
1. Return ONLY upgraded files
2. KEEP FORMAT: ═══ FILE: path ═══  code  ═══ END ═══
3. NEVER delete — only modify or create new
4. New file: ═══ NEW FILE: path ═══  code  ═══ END ═══
5. NO explanations

INPUT:
{code}
"""


def get_best_upgrade(task, code):
    """Call all 8 AI, pick longest response."""
    prompt = UPGRADE_PROMPT.format(
        task=task.get("task", ""),
        target=task.get("target", "ALL"),
        code=code)

    responses = []
    for ai in ALL_AIS:
        print(f"      🔧 {ai} upgrading...")
        text = call_one_ai(ai, prompt, max_tokens=16000)
        if text and "═══ FILE:" in text:
            fcount = text.count("═══ FILE:")
            responses.append({"ai": ai, "code": text, "files": fcount})
            print(f"         ✅ {fcount} files")
        else:
            print(f"         ⚠️ invalid")

    if not responses:
        return None
    return max(responses, key=lambda r: r["files"] * 10000 + len(r["code"]))


# ═══════════════════════════════════════════════
# COMBINE + CHUNK
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
def apply(text):
    modified, created = 0, 0

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

    return modified, created


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
    total_modified = data["modified"]
    total_created = data["created"]
    rounds = data["rounds"]
    tasks_total = data["tasks_total"]
    tasks_approved = data["tasks_approved"]
    tasks_rejected = data["tasks_rejected"]
    score = data["score"]
    backup_path = data["backup"] or "N/A"
    syntax_failed = data["syntax_failed"]
    round_details = data["round_details"]

    bar = "█" * score + "░" * (10 - score)

    round_lines = []
    for r in round_details:
        round_lines.append(
            f"   • R{r['n']}: {r['found']} found, "
            f"{r['approved']} ✅, {r['rejected']} ❌, "
            f"{r['modified']}M")
    round_text = "\n".join(round_lines) if round_lines else "   (none)"

    msg = (
        "👑 <b>KING — CONSENSUS REPORT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <code>{ts}</code>\n"
        "\n"
        "📁 <b>SCAN:</b>\n"
        f"   • Files: <b>{files}</b>\n"
        "\n"
        "🗳️ <b>VOTING (8 AI):</b>\n"
        f"   • Tasks found: <b>{tasks_total}</b>\n"
        f"   • ✅ Approved: <b>{tasks_approved}</b>\n"
        f"   • ❌ Rejected: <b>{tasks_rejected}</b>\n"
        f"   • Threshold: <b>{MIN_CONSENSUS}/8</b> YES\n"
        "\n"
        "🔁 <b>ROUNDS: {rounds}</b>\n"
        f"{round_text}\n"
        "\n"
        "🔧 <b>ACTIONS:</b>\n"
        f"   ✏️ Modified: <b>{total_modified}</b>\n"
        f"   📁 Created: <b>{total_created}</b>\n"
        f"   🗑️ Deleted: <b>0</b>\n"
        "\n"
        f"✅ Syntax: {len(syntax_failed)} failed\n"
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
# MAIN — CONSENSUS LOOP
# ═══════════════════════════════════════════════
def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("═" * 60)
    print("👑 KING — CONSENSUS MODE")
    print("═" * 60)

    tg_send(f"👑 <b>KING ACTIVATED</b>\n🕐 {ts}\nConsensus mode...", silent=True)

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

    total_modified = 0
    total_created = 0
    total_tasks = 0
    total_approved = 0
    total_rejected = 0
    round_details = []

    for round_n in range(1, MAX_ROUNDS + 1):
        print(f"\n{'═' * 50}")
        print(f"🔁 ROUND {round_n}/{MAX_ROUNDS}")
        print(f"{'═' * 50}")

        # Step 1: Find tasks (one AI)
        chunks = chunk_by_size(files)
        all_tasks = []
        for ci, chunk in enumerate(chunks, 1):
            combined = combine_files(chunk, f"find_r{round_n}_c{ci}")
            tasks, ai_used = find_tasks(combined)
            if tasks:
                print(f"    📋 Found {len(tasks)} tasks (by {ai_used})")
                all_tasks.extend(tasks)

        if not all_tasks:
            print(f"  ✅ No tasks — DONE")
            break

        total_tasks += len(all_tasks)

        # Step 2: CONSENSUS — sab AI se verify
        approved_tasks = []
        for ti, task in enumerate(all_tasks, 1):
            print(f"\n  🗳️ Task {ti}/{len(all_tasks)}: {task['task'][:50]}")
            combined = combine_files(files, f"verify_r{round_n}_t{ti}")

            yes, no, votes = get_consensus(task, combined)

            print(f"      Votes: ✅{yes}  ❌{no}")

            if yes >= MIN_CONSENSUS:
                approved_tasks.append(task)
                total_approved += 1
                print(f"      ✅ APPROVED (consensus)")
            else:
                total_rejected += 1
                print(f"      ❌ REJECTED (not enough votes)")

        if not approved_tasks:
            print(f"\n  ⏹️ No tasks approved — STOP")
            round_details.append({
                "n": round_n, "found": len(all_tasks),
                "approved": 0, "rejected": len(all_tasks),
                "modified": 0, "created": 0,
            })
            break

        # Step 3: Upgrade approved tasks
        round_modified = 0
        round_created = 0

        for ti, task in enumerate(approved_tasks, 1):
            print(f"\n  🔧 Upgrade {ti}/{len(approved_tasks)}: {task['task'][:50]}")
            combined = combine_files(files, f"upgrade_r{round_n}_t{ti}")

            best = get_best_upgrade(task, combined)

            if not best:
                print(f"      ⚠️ No upgrade")
                continue

            print(f"      🏆 Best: {best['ai']} ({best['files']} files)")
            m, c = apply(best["code"])
            round_modified += m
            round_created += c
            print(f"      ✅ {m}M {c}C")

        total_modified += round_modified
        total_created += round_created

        round_details.append({
            "n": round_n, "found": len(all_tasks),
            "approved": len(approved_tasks),
            "rejected": len(all_tasks) - len(approved_tasks),
            "modified": round_modified, "created": round_created,
        })

        if round_modified + round_created == 0:
            print(f"\n  ⏹️ No changes — STOP")
            break

    # Final test
    print("\n🧪 Final test...")
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
    print(f"  Failures: {len(syntax_failed)}")

    score = rate_bot(len(files), total_modified + total_created,
                     len(syntax_failed))

    send_report({
        "time": ts, "files": len(files),
        "modified": total_modified, "created": total_created,
        "rounds": len(round_details),
        "tasks_total": total_tasks,
        "tasks_approved": total_approved,
        "tasks_rejected": total_rejected,
        "score": score, "backup": backup_path,
        "syntax_failed": syntax_failed,
        "round_details": round_details,
    })

    log_file = f"{LOG_DIR}/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "time": ts, "files": len(files),
            "modified": total_modified, "created": total_created,
            "tasks_total": total_tasks,
            "tasks_approved": total_approved,
            "tasks_rejected": total_rejected,
            "score": score,
            "round_details": round_details,
            "syntax_failed": syntax_failed,
        }, f, indent=2)

    print("\n" + "═" * 60)
    print(f"👑 DONE: {total_modified}M {total_created}C — Score {score}/10")
    print(f"   Tasks: {total_tasks} found, {total_approved} approved")
    print("═" * 60)


if __name__ == "__main__":
    main()
