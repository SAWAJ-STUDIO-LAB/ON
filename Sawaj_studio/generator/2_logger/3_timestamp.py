"""
⏰ Timestamp
"""
from datetime import datetime, timezone


def now_hms():
    return datetime.now().strftime("%H:%M:%S")


def now_ymd():
    return datetime.now().strftime("%Y%m%d")


def now_ymdhms():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def elapsed_str(seconds):
    if seconds < 60:
        return str(round(seconds, 1)) + "s"
    return str(int(seconds // 60)) + "m " + str(int(seconds % 60)) + "s"
