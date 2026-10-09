# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A3_telegram.py                            ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A3_telegram.py                     ║
# ║  🎯 PURPOSE:   Combined Telegram report — buffer + send  ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📱 TELEGRAM MODULE                                     ║
║   ═════════════════════                                  ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Saare logs ko ek combined message mein bhejna      ║
║                                                          ║
║   📖 How it works:                                       ║
║      1. Har step log buffer mein add hota hai            ║
║      2. End pe poora buffer Telegram pe bheja jata hai   ║
║      3. Auto-split at 3800 chars (Telegram limit)        ║
║                                                          ║
║   📊 Output:                                             ║
║      • Message 1: Run start                              ║
║      • Message 2: Full report (1-2 parts)                ║
║      • Message 3: Summary                                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import time
import requests
from datetime import datetime


# ═══════════════════════════════════════════════════════════
# ① SESSION + GLOBAL STATE
# ═══════════════════════════════════════════════════════════

_session = requests.Session()

LOG_BUFFER = []
FILE_TIMERS = {}
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}
START_TIME = None
RUN_HEADER = "📖 STORY VIDEO RUN"


# ═══════════════════════════════════════════════════════════
# ② HELPERS
# ═══════════════════════════════════════════════════════════

def _now():
    """Current time HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")


def _creds():
    """Get Telegram credentials from env."""
    return os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")


def _send_raw(msg, silent=False):
    """Send message to Telegram (max 4000 chars)."""
    token, chat_id = _creds()
    if token and chat_id:
        try:
            _session.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": msg[:4000],
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "disable_notification": silent,
                },
                timeout=15,
            )
        except Exception:
            pass
    print(msg, flush=True)


# ═══════════════════════════════════════════════════════════
# ③ RUN START
# ═══════════════════════════════════════════════════════════

def run_start(title="📖 STORY VIDEO RUN"):
    """Initialize run — resets all buffers."""
    global START_TIME, RUN_HEADER, LOG_BUFFER
    START_TIME = time.time()
    RUN_HEADER = title
    LOG_BUFFER = []
    STEP_COUNTER.update({"total": 0, "success": 0, "failed": 0})
    _send_raw(f"▶️ <b>{title} STARTED</b>\n🕐 {_now()}", silent=True)


# ═══════════════════════════════════════════════════════════
# ④ FILE START
# ═══════════════════════════════════════════════════════════

def file_start(filename, purpose=""):
    """Log start of a module (adds to buffer)."""
    FILE_TIMERS[filename] = time.time()
    STEP_COUNTER["total"] += 1
    line = f"📂 <b>{filename}</b>"
    if purpose:
        line += f" — <i>{purpose}</i>"
    LOG_BUFFER.append(line)


# ═══════════════════════════════════════════════════════════
# ⑤ FILE END
# ═══════════════════════════════════════════════════════════

def file_end(filename, status="success", note=""):
    """Log end of a module (adds to buffer)."""
    elapsed = time.time() - FILE_TIMERS.get(filename, time.time())
    if status == "success":
        STEP_COUNTER["success"] += 1
        icon = "✅"
    else:
        STEP_COUNTER["failed"] += 1
        icon = "❌"
    line = f"{icon} <b>{filename}</b> done in {elapsed:.2f}s"
    if note:
        line += f" — {note}"
    LOG_BUFFER.append(line)


# ═══════════════════════════════════════════════════════════
# ⑥ STEP
# ═══════════════════════════════════════════════════════════

def step(filename, action, result="ok", detail=""):
    """Log a step (adds to buffer)."""
    icon = {
        "ok": "✅", "fail": "❌", "skip": "⏭️",
        "warn": "⚠️", "info": "ℹ️",
    }.get(result, "ℹ️")
    line = f"{icon} <b>{filename}</b> → {action}"
    if detail:
        line += f" ({detail})"
    LOG_BUFFER.append(line)


# ═══════════════════════════════════════════════════════════
# ⑦ API CALL
# ═══════════════════════════════════════════════════════════

def api_call(filename, api_name, status, detail=""):
    """Log an API call (adds to buffer)."""
    icon = {
        "success": "🟢", "failed": "🔴",
        "fallback": "🟡", "skipped": "⚪",
    }.get(status, "⚫")
    line = f"{icon} <b>{api_name}</b> [{status.upper()}]"
    if detail:
        line += f" — {detail}"
    LOG_BUFFER.append(line)


# ═══════════════════════════════════════════════════════════
# ⑧ ERROR
# ═══════════════════════════════════════════════════════════

def file_error(filename, error, tb=""):
    """Log error (adds to buffer)."""
    STEP_COUNTER["failed"] += 1
    line = f"🚨 <b>{filename}</b> ERROR: {str(error)[:150]}"
    if tb:
        line += f"\n<code>{tb[:200]}</code>"
    LOG_BUFFER.append(line)


# ═══════════════════════════════════════════════════════════
# ⑨ HEADER
# ═══════════════════════════════════════════════════════════

def header(title):
    """Add a section header to buffer."""
    LOG_BUFFER.append(f"\n<b>━━━ {title} ━━━</b>")


# ═══════════════════════════════════════════════════════════
# ⑩ DIRECT SEND
# ═══════════════════════════════════════════════════════════

def send_tg(msg, silent=False):
    """Send message to Telegram immediately."""
    _send_raw(msg, silent=silent)


# ═══════════════════════════════════════════════════════════
# ⑪ FULL REPORT — auto-split
# ═══════════════════════════════════════════════════════════

def send_full_report(extra_sections=None, silent=False):
    """Send all buffered logs as Telegram message(s)."""
    total_time = time.time() - (START_TIME or time.time())
    head = (
        f"<b>{RUN_HEADER} — FULL REPORT</b>\n"
        f"🕐 {_now()}  |  ⏱️ {total_time:.1f}s\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    )
    body = "\n".join(LOG_BUFFER)
    extras = ""
    if extra_sections:
        extras = "\n\n" + "\n".join(extra_sections)
    full = head + body + extras

    # Auto-split at 3800 chars
    chunks = []
    current = ""
    for line in full.split("\n"):
        if len(current) + len(line) + 1 > 3800:
            chunks.append(current)
            current = line
        else:
            current += ("\n" if current else "") + line
    if current:
        chunks.append(current)

    for i, chunk in enumerate(chunks, 1):
        prefix = f"📄 <b>Report {i}/{len(chunks)}</b>\n" if len(chunks) > 1 else ""
        _send_raw(prefix + chunk, silent=silent)


# ═══════════════════════════════════════════════════════════
# ⑫ SUMMARY
# ═══════════════════════════════════════════════════════════

def send_summary(silent=False):
    """Send final summary message."""
    total = STEP_COUNTER["total"]
    ok = STEP_COUNTER["success"]
    fail = STEP_COUNTER["failed"]
    total_time = time.time() - (START_TIME or time.time())
    icon = "🎉" if fail == 0 else "⚠️"
    msg = (
        f"{icon} <b>RUN COMPLETE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📁 Files: <b>{total}</b>\n"
        f"✅ Success: <b>{ok}</b>\n"
        f"❌ Failed: <b>{fail}</b>\n"
        f"⏱️ Time: <b>{total_time:.1f}s</b>\n"
        f"🕐 Finished: <b>{_now()}</b>"
    )
    _send_raw(msg, silent=silent)
