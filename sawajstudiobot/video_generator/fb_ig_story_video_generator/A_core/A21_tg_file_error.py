"""
A21_tg_file_error.py
Sirf file_error.
"""
from A_core.A13_tg_buffer import LOG_BUFFER, STEP_COUNTER


def file_error(filename, error, tb=""):
    """Add error to buffer."""
    STEP_COUNTER["failed"] += 1
    line = f"🚨 <b>{filename}</b> ERROR: {str(error)[:150]}"
    if tb:
        line += f"\n<code>{tb[:200]}</code>"
    LOG_BUFFER.append(line)
