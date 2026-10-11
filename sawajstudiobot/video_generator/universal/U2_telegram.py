"""
U2_telegram.py — Universal Telegram Report Buffer
==================================================
Parametrized via set_header() — each generator calls it once at start.

Fixes:
  • HTML escaping (prevents Telegram rejection on <, >, &)
  • Safe truncation (no broken HTML tags)
  • Retry + plain-text fallback on 400
"""

import os
import time
import html
import requests
from datetime import datetime


_session = requests.Session()

LOG_BUFFER = []
FILE_TIMERS = {}
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}
START_TIME = None
RUN_HEADER = "🎬 VIDEO RUN"


def set_header(title):
    """Set the run header — Story/Short/Long call this once."""
    global RUN_HEADER
    RUN_HEADER = title


def _now():
    return datetime.now().strftime("%H:%M:%S")


def _creds():
    return (os.environ.get("TELEGRAM_BOT_TOKEN"),
            os.environ.get("TELEGRAM_CHAT_ID"))


def _esc(text):
    return html.escape(str(text), quote=False)


def _send_raw(msg, silent=False, retries=2):
    token, chat_id = _creds()
    if not (token and chat_id):
        print(msg, flush=True)
        return

    if len(msg) > 3900:
        msg = msg[:3900]
        last_nl = msg.rfind("\n")
        if last_nl > 3000:
            msg = msg[:last_nl]

    for attempt in range(retries + 1):
        try:
            r = _session.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": msg,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "disable_notification": silent,
                },
                timeout=15)
            if r.status_code == 200:
                print(msg, flush=True)
                return
            if r.status_code == 400:
                r2 = _session.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": msg,
                        "disable_web_page_preview": True,
                        "disable_notification": silent,
                    },
                    timeout=15)
                if r2.status_code == 200:
                    print(msg, flush=True)
                    return
        except Exception:
            if attempt < retries:
                time.sleep(1.5)
                continue
    print(msg, flush=True)


def run_start(title=None):
    global START_TIME, RUN_HEADER, LOG_BUFFER
    if title:
        RUN_HEADER = title
    START_TIME = time.time()
    LOG_BUFFER = []
    STEP_COUNTER.update({"total": 0, "success": 0, "failed": 0})
    _send_raw(f"▶️ <b>{_esc(RUN_HEADER)} STARTED</b>\n🕐 {_now()}",
              silent=True)


def file_start(filename, purpose=""):
    FILE_TIMERS[filename] = time.time()
    STEP_COUNTER["total"] += 1
    line = f"📂 <b>{_esc(filename)}</b>"
    if purpose:
        line += f" — <i>{_esc(purpose)}</i>"
    LOG_BUFFER.append(line)


def file_end(filename, status="success", note=""):
    elapsed = time.time() - FILE_TIMERS.get(filename, time.time())
    if status == "success":
        STEP_COUNTER["success"] += 1
        icon = "✅"
    else:
        STEP_COUNTER["failed"] += 1
        icon = "❌"
    line = f"{icon} <b>{_esc(filename)}</b> done in {elapsed:.2f}s"
    if note:
        line += f" — {_esc(note)}"
    LOG_BUFFER.append(line)


def step(filename, action, result="ok", detail=""):
    icon = {"ok": "✅", "fail": "❌", "skip": "⏭️",
            "warn": "⚠️", "info": "ℹ️"}.get(result, "ℹ️")
    line = f"{icon} <b>{_esc(filename)}</b> → {_esc(action)}"
    if detail:
        line += f" ({_esc(detail)})"
    LOG_BUFFER.append(line)


def api_call(filename, api_name, status, detail=""):
    icon = {"success": "🟢", "failed": "🔴",
            "fallback": "🟡", "skipped": "⚪"}.get(status, "⚫")
    line = f"{icon} <b>{_esc(api_name)}</b> [{status.upper()}]"
    if detail:
        line += f" — {_esc(detail)}"
    LOG_BUFFER.append(line)


def file_error(filename, error, tb=""):
    STEP_COUNTER["failed"] += 1
    line = f"🚨 <b>{_esc(filename)}</b> ERROR: {_esc(str(error)[:150])}"
    if tb:
        line += f"\n<code>{_esc(tb[:200])}</code>"
    LOG_BUFFER.append(line)


def header(title):
    LOG_BUFFER.append(f"\n<b>━━━ {_esc(title)} ━━━</b>")


def send_tg(msg, silent=False):
    _send_raw(msg, silent=silent)


def send_full_report(extra_sections=None, silent=False):
    total_time = time.time() - (START_TIME or time.time())
    head = (
        f"<b>{_esc(RUN_HEADER)} — FULL REPORT</b>\n"
        f"🕐 {_now()}  |  ⏱️ {total_time:.1f}s\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    )
    body = "\n".join(LOG_BUFFER)
    extras = ""
    if extra_sections:
        extras = "\n\n" + "\n".join(extra_sections)
    full = head + body + extras

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
        prefix = (f"📄 <b>Report {i}/{len(chunks)}</b>\n"
                  if len(chunks) > 1 else "")
        _send_raw(prefix + chunk, silent=silent)


def send_summary(silent=False):
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
