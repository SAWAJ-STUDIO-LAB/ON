"""
🚨 Error Tracker
"""
import traceback
from datetime import datetime
ERRORS = []


def track_error(module, error, include_traceback=False):
    entry = {
        "module": module, "error": str(error)[:500],
        "type": type(error).__name__,
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    if include_traceback:
        entry["traceback"] = traceback.format_exc()[:2000]
    ERRORS.append(entry)


def get_errors():
    return ERRORS.copy()


def get_error_count():
    return len(ERRORS)


def clear_errors():
    ERRORS.clear()
