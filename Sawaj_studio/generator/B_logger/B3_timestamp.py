# ═══════════════════════════════════════════════════════════
# 📄 FILE:      B3_timestamp.py
# 🎯 PURPOSE:   Timestamp helpers
# ═══════════════════════════════════════════════════════════

"""
⏰ TIMESTAMP
═════════════

🎯 Purpose:
   Different timestamp formats.
"""

from datetime import datetime, timezone


# ═══════════════════════════════════════════════════════════
# ① FORMATS
# ═══════════════════════════════════════════════════════════

def now_hms() -> str:
    """HH:MM:SS — for console logs."""
    return datetime.now().strftime("%H:%M:%S")


def now_ymd() -> str:
    """YYYYMMDD — for filenames."""
    return datetime.now().strftime("%Y%m%d")


def now_ymdhms() -> str:
    """YYYY-MM-DD HH:MM:SS — for file logs."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_iso() -> str:
    """ISO format — for APIs."""
    return datetime.now(timezone.utc).isoformat()


def now_utc() -> str:
    """UTC time string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# ═══════════════════════════════════════════════════════════
# ② ELAPSED
# ═══════════════════════════════════════════════════════════

def elapsed_str(seconds: float) -> str:
    """Convert seconds to readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}m {s}s"


# ═══════════════════════════════════════════════════════════
# ③ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("⏰ Timestamp Self-Test")
    print("=" * 50)
    print(f"  HMS:    {now_hms()}")
    print(f"  YMD:    {now_ymd()}")
    print(f"  YMDHMS: {now_ymdhms()}")
    print(f"  ISO:    {now_iso()}")
    print(f"  UTC:    {now_utc()}")
    print(f"  Elapsed: {elapsed_str(125.5)}")
    print("✅ Done")# -*- coding: utf-8 -*-
