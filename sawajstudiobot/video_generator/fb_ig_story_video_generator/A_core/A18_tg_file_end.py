"""A18_tg_file_end.py — Sirf file_end."""
import time
from A_core.A13_tg_buffer import LOG_BUFFER, FILE_TIMERS, STEP_COUNTER


def file_end(filename, status="success", note=""):
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
