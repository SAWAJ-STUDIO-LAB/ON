"""A17_tg_file_start.py — Sirf file_start."""
import time
from A_core.A13_tg_buffer import LOG_BUFFER, FILE_TIMERS, STEP_COUNTER


def file_start(filename, purpose=""):
    FILE_TIMERS[filename] = time.time()
    STEP_COUNTER["total"] += 1
    line = f"📂 <b>{filename}</b>"
    if purpose:
        line += f" — <i>{purpose}</i>"
    LOG_BUFFER.append(line)
