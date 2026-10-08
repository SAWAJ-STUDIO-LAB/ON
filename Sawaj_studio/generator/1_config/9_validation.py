"""
✅ Validation
"""
from .2_secret_reader import has_secret
from .8_worker_selector import list_workers


def validate_secrets(worker="story"):
    critical = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
    missing = [k for k in critical if not has_secret(k)]
    return {"valid": len(missing) == 0, "missing": missing}


def validate_worker(name):
    return name in list_workers()
