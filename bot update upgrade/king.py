"""
👑 KING — Original, Live, Working System
+ Full Change Report on Telegram
"""
import os
import re
import ast
import json
import time
import shutil
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

CODE_EXT = {".py"}
CONFIG_EXT = {".json", ".yml", ".yaml", ".toml", ".txt", ".md", ".cfg", ".ini"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico"}

TIMEOUT = 300
MAX_RETRIES = 3
MAX_ROUNDS = 5
MAX_CHUNK_KB = 400
MIN_CONSENSUS = 6


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
# AI CALLS
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
# CONSENSUS
# ═══════════════════════════════════════════════
VERIFY_PROMPT = """Review this proposed upgrade. Is it NEEDED and SAFE?

TASK: {task}
TARGET: {target}

CODE:
{code}

Reply ONLY:
VERDICT: YES
REASON: <one line>

OR

VERDICT: NO
REASON: <one line>
"""


def get_consensus(task, code):
    prompt = VERIFY_PROMPT.format(
        task=task.get("task", ""),
        target=task.get("target", "ALL"),
        code=code[:80000])
    votes = {}
    yes = no = 0
    for ai in ALL_AIS:
        print(f"      🗳️ {ai}...")
        text = call_one_ai(ai, prompt, max_tokens=200)
        if not text:
            votes[ai] = "ABSTAIN"
            continue
        upper = text.upper()
        if "VERDICT: YES" in upper or "VERDICT:YES" in upper:
            votes[ai] = "YES"
            yes += 1
        elif "VERDICT: NO" in upper or "VERDICT:NO" in upper:
            votes[ai] = "NO"
            no += 1
        else:
            votes[ai] = "ABSTAIN"
    return yes, no, votes


# ═══════════════════════════════════════════════
# FIND TASKS
# ═══════════════════════════════════════════════
FIND_TASKS_PROMPT = """List up to 5 tasks that NEED upgrading in this bot.

Format (one per line):
TASK: <what>
TARGET: <file or "ALL">
PRIORITY: <1-10>

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
                return tasks, ai
    return [], None


# ═══════════════════════════════════════════════
# UPGRADE
# ═══════════════════════════════════════════════
UPGRADE_PROMPT = """Upgrade these files based on this task:

TASK: {task}
TARGET: {target}

RULES:
1. Return ONLY upgraded files
2. FORMAT: ═══ FILE: path ═══  code  ═══ END ═══
3. NEVER delete — only modify or create new
4. New file: ═══ NEW FILE: path ═══  code  ═══ END ═══
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
    if not responses:
        return None
    return max(responses, key=lambda r: r["files"] * 10000 + len(r["code"]))


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
# APPLY WITH FULL TRACKING
# ═══════════════════════════════════════════════
def apply_with_tracking(text):
    """Apply + return detailed changes."""
    changes = {
        "modified": [],   # list of file paths
        "created": [],    # list of file paths
        "deleted": [],    # list of file paths
        "size_diff": {},  # file: (before, after)
    }

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
        changes["created"].append(rel)
        changes["size_diff"][rel] = (0, os.path.getsize(full))
        print(f"        📁 Created: {rel}")

    # MODIFY
    for rel, code in re.findall(r"═══ FILE: (.+?) ═══\n(.*?)\n═══ END ═══",
                                text, re.DOTALL):
        rel = rel.strip()
        if not rel or ".." in rel:
            continue
        full = os.path.join(BOT_ROOT, rel)
        before = 0
        try:
            before = os.path.getsize(full)
        except Exception:
            pass
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        after = os.path.getsize(full)
        changes["modified"].append(rel)
        changes["size_diff"][rel] = (before, after)

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
# DETAILED REPORT
# ═══════════════════════════════════════════════
def send_detailed_report(data):
    """Send full detailed report to Telegram."""
    ts = data["time"]
    files = data["files"]
    score = data["score"]
    backup_path = data["backup"] or "N/A"
    rounds = data["rounds"]
    tasks_total = data["tasks_total"]
    tasks_approved = data["tasks_approved"]
    tasks_rejected = data["tasks_rejected"]
    all_changes = data["all_changes"]
    syntax_failed = data["syntax_failed"]

    # Merge all changes
    modified = []
    created = []
    deleted = []
    for c in all_changes:
        modified.extend(c.get("modified", []))
        created.extend(c.get("created", []))
        deleted.extend(c.get("deleted", []))

    modified = sorted(set(modified))
    created = sorted(set(created))
    deleted = sorted(set(deleted))

    bar = "█" * score + "░" * (10 - score)

    # ═══ MESSAGE 1: Header + Summary ═══
    msg1 = (
        "👑 <b>KING REPORT — FULL DETAILS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <code>{ts}</code>\n"
        "\n"
        "📁 <b>SCAN:</b>\n"
        f"   • Files: <b>{files}</b>\n"
        "\n"
        "🗳️ <b>CONSENSUS VOTING:</b>\n"
        f"   • Tasks found: <b>{tasks_total}</b>\n"
        f"   • ✅ Approved: <b>{tasks_approved}</b>\n"
        f"   • ❌ Rejected: <b>{tasks_rejected}</b>\n"
        f"   • Threshold: <b>6/8 YES</b>\n"
        "\n"
        f"🔁 <b>ROUNDS:</b> <b>{rounds}</b>\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>SUMMARY:</b>\n"
        f"   ✏️ Modified: <b>{len(modified)}</b>\n"
        f"   📁 Created: <b>{len(created)}</b>\n"
        f"   🗑️ Deleted: <b>{len(deleted)}</b>\n"
        f"   ✅ Syntax fail: <b>{len(syntax_failed)}</b>\n"
        f"   💾 Backup: <code>{backup_path}</code>\n"
        "\n"
        "📈 <b>SCORE:</b>\n"
        f"   {bar} <b>{score}/10</b>\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>World #1 in progress</b>"
    )
    tg_send(msg1)

    # ═══ MESSAGE 2: Created files ═══
    if created:
        msg2 = "📁 <b>FILES CREATED:</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
        for i, f in enumerate(created[:40], 1):
            msg2 += f"{i}. <code>{f}</code>\n"
        if len(created) > 40:
            msg2 += f"\n... +{len(created) - 40} more\n"
        tg_send(msg2)

    # ═══ MESSAGE 3: Modified files ═══
    if modified:
        msg3 = "✏️ <b>FILES MODIFIED:</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
        for i, f in enumerate(modified[:40], 1):
            msg3 += f"{i}. <code>{f}</code>\n"
        if len(modified) > 40:
            msg3 += f"\n... +{len(modified) - 40} more\n"
        tg_send(msg3)

    # ═══ MESSAGE 4: Deleted files ═══
    if deleted:
        msg4 = "🗑️ <b>FILES DELETED:</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
        for i, f in enumerate(deleted[:40], 1):
            msg4 += f"{i}. <code>{f}</code>\n"
        tg_send(msg4)
    else:
        tg_send("🗑️ <b>FILES DELETED:</b> None (never delete)")

    # ═══ MESSAGE 5: Syntax failures ═══
    if syntax_failed:
        msg5 = "⚠️ <b>SYNTAX FAILURES:</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
        for i, s in enumerate(syntax_failed[:20], 1):
            msg5 += f"{i}. <code>{s['file']}</code>\n   {s['error'][:80]}\n"
        tg_send(msg5)

    # ═══ MESSAGE 6: Change log (diff size) ═══
    size_diff = {}
    for c in all_changes:
        for f, (b, a) in c.get("size_diff", {}).items():
            if f not in size_diff:
                size_diff[f] = [0, 0]
            size_diff[f][0] += b
            size_diff[f][1] += a

    if size_diff:
        msg6 = "📊 <b>CHANGE LOG (size before → after):</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
        items = sorted(size_diff.items(),
                       key=lambda x: abs(x[1][1] - x[1][0]), reverse=True)
        for i, (f, (b, a)) in enumerate(items[:25], 1):
            diff = a - b
            arrow = "📈" if diff > 0 else ("📉" if diff < 0 else "➖")
            msg6 += f"{i}. {arrow} <code>{f[:40]}</code>\n"
            msg6 += f"   {b//1024}KB → {a//1024}KB ({diff:+d}B)\n"
        tg_send(msg6)

    # ═══ MESSAGE 7: Final ═══
    tg_send(
        f"✅ <b>KING WORK COMPLETE</b>\n"
        f"📅 {ts}\n"
        f"📁 {len(modified)} modified, {len(created)} created\n"
        f"📈 Score: <b>{score}/10</b>\n"
        f"👑 <b>World #1 in progress</b>"
    )


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════
def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("═" * 60)
    print("👑 KING — ORIGINAL + LIVE + DETAIL REPORT")
    print("═" * 60)

    tg_send(f"👑 <b>KING ACTIVATED</b>\n🕐 {ts}\nWorking...", silent=True)

    os.makedirs(WORK, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    scan = deep_scan()
    files = scan["code"]
    print(f"📁 Files: {len(files)}")

    if not files:
        tg_send("⚠️ No files found.")
        return

    backup_path = backup()
    print(f"💾 Backup: {backup_path}")

    total_modified = 0
    total_created = 0
    total_tasks = 0
    total_approved = 0
    total_rejected = 0
    round_details = []
    all_changes = []

    for round_n in range(1, MAX_ROUNDS + 1):
        print(f"\n{'═' * 50}")
        print(f"🔁 ROUND {round_n}/{MAX_ROUNDS}")
        print(f"{'═' * 50}")

        # Find tasks
        chunks = chunk_by_size(files)
        all_tasks = []
        for ci, chunk in enumerate(chunks, 1):
            combined = combine_files(chunk, f"find_r{round_n}_c{ci}")
            tasks, ai_used = find_tasks(combined)
            if tasks:
                print(f"    📋 {len(tasks)} tasks (by {ai_used})")
                all_tasks.extend(tasks)

        if not all_tasks:
            print(f"  ✅ No tasks — STOP")
            break

        total_tasks += len(all_tasks)

        # Consensus
        approved_tasks = []
        for ti, task in enumerate(all_tasks, 1):
            print(f"\n  🗳️ Task {ti}/{len(all_tasks)}: {task['task'][:50]}")
            combined = combine_files(files, f"verify_r{round_n}_t{ti}")
            yes, no, votes = get_consensus(task, combined)
            print(f"      Votes: ✅{yes}  ❌{no}")
            if yes >= MIN_CONSENSUS:
                approved_tasks.append(task)
                total_approved += 1
                print(f"      ✅ APPROVED")
            else:
                total_rejected += 1
                print(f"      ❌ REJECTED")

        if not approved_tasks:
            print(f"\n  ⏹️ No approvals — STOP")
            round_details.append({
                "n": round_n, "found": len(all_tasks),
                "approved": 0, "rejected": len(all_tasks),
                "modified": 0, "created": 0,
            })
            break

        # Upgrade
        round_modified = 0
        round_created = 0

        for ti, task in enumerate(approved_tasks, 1):
            print(f"\n  🔧 Upgrade {ti}/{len(approved_tasks)}: {task['task'][:50]}")
            combined = combine_files(files, f"upgrade_r{round_n}_t{ti}")
            best = get_best_upgrade(task, combined)
            if not best:
                continue
            print(f"      🏆 {best['ai']} ({best['files']} files)")

            changes = apply_with_tracking(best["code"])
            all_changes.append(changes)
            round_modified += len(changes["modified"])
            round_created += len(changes["created"])

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

    # Test
    print("\n🧪 Test...")
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

    score = rate_bot(len(files), total_modified + total_created,
                     len(syntax_failed))

    # Report
    send_detailed_report({
        "time": ts, "files": len(files),
        "modified": total_modified, "created": total_created,
        "rounds": len(round_details),
        "tasks_total": total_tasks,
        "tasks_approved": total_approved,
        "tasks_rejected": total_rejected,
        "score": score, "backup": backup_path,
        "syntax_failed": syntax_failed,
        "round_details": round_details,
        "all_changes": all_changes,
    })

    # Log
    log_file = f"{LOG_DIR}/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "time": ts, "files": len(files),
            "modified": total_modified, "created": total_created,
            "score": score, "round_details": round_details,
            "syntax_failed": syntax_failed,
        }, f, indent=2)

    print("\n" + "═" * 60)
    print(f"👑 DONE: {total_modified}M {total_created}C — Score {score}/10")
    print("═" * 60)


if __name__ == "__main__":
    main()
