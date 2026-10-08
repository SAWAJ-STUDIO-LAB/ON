"""
🎯 Mode Decider
"""
import os


def get_mode():
    event = os.environ.get("GITHUB_EVENT_NAME", "").strip()
    mode = os.environ.get("UPLOAD_MODE", "offline").strip().lower()
    confirmed = os.environ.get("UPLOAD_CONFIRMED", "false").strip().lower() == "true"
    if event == "schedule":
        return "online"
    if mode == "online" and confirmed:
        return "online"
    return "offline"


def is_online():
    return get_mode() == "online"


def is_offline():
    return get_mode() == "offline"


def get_worker():
    return os.environ.get("WORKER", "story").strip().lower()
