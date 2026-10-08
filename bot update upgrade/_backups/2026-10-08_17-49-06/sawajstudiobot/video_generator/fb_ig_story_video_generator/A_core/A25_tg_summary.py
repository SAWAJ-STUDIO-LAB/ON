"""A25_tg_summary.py — Sirf summary."""
import time
from A_core.A13_tg_buffer import STEP_COUNTER, START_TIME, now
from A_core.A15_tg_send_raw import send_raw


def send_summary(silent=False):
    total = STEP_COUNTER["total"]
    ok = STEP_COUNTER["success"]
    fail = STEP_COUNTER["failed"]
    total_time = time.time() - (START_TIME[0] or time.time())
    icon = "🎉" if fail == 0 else "⚠️"
    msg = (f"{icon} <b>RUN COMPLETE</b>\n"
           f"━━━━━━━━━━━━━━━━━━━━━━━\n"
           f"📁 Files: <b>{total}</b>\n"
           f"✅ Success: <b>{ok}</b>\n"
           f"❌ Failed: <b>{fail}</b>\n"
           f"⏱️ Time: <b>{total_time:.1f}s</b>\n"
           f"🕐 Finished: <b>{now()}</b>")
    send_raw(msg, silent=silent)
