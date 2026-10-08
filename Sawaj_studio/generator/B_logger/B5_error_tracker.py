# ═══════════════════════════════════════════════════════════
# 📄 FILE:      B5_error_tracker.py
# 🎯 PURPOSE:   Errors track karna
# ═══════════════════════════════════════════════════════════

"""
🚨 ERROR TRACKER
═════════════════

🎯 Purpose:
   Saare errors collect karke rakhna.
"""

import traceback
from datetime import datetime


# ═══════════════════════════════════════════════════════════
# ① ERROR STORAGE
# ═══════════════════════════════════════════════════════════

ERRORS = []


# ═══════════════════════════════════════════════════════════
# ② TRACK ERROR
# ═══════════════════════════════════════════════════════════

def track_error(module: str, error: Exception, include_traceback: bool = False):
    """
    Track an error.

    Args:
        module:  module name
        error:   exception
        include_traceback: include full traceback?
    """
    entry = {
        "module": module,
        "error": str(error)[:500],
        "type": type(error).__name__,
        "time": datetime.now().strftime("%H:%M:%S"),
    }

    if include_traceback:
        entry["traceback"] = traceback.format_exc()[:2000]

    ERRORS.append(entry)


# ═══════════════════════════════════════════════════════════
# ③ GET ERRORS
# ═══════════════════════════════════════════════════════════

def get_errors() -> list:
    """Get all tracked errors."""
    return ERRORS.copy()


def get_error_count() -> int:
    """Get total error count."""
    return len(ERRORS)


def clear_errors():
    """Clear error list."""
    ERRORS.clear()


# ═══════════════════════════════════════════════════════════
# ④ SUMMARY
# ═══════════════════════════════════════════════════════════

def summary() -> str:
    """Get error summary."""
    if not ERRORS:
        return "✅ No errors"

    lines = [f"❌ {len(ERRORS)} error(s):"]
    for e in ERRORS[-5:]:
        lines.append(f"   • [{e['time']}] {e['module']}: {e['error'][:80]}")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# ⑤ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚨 Error Tracker Self-Test")
    print("=" * 50)
    try:
        1 / 0
    except Exception as e:
        track_error("test", e, include_traceback=True)
    print(f"  Errors: {get_error_count()}")
    print(summary())
    print("✅ Done")# -*- coding: utf-8 -*-
