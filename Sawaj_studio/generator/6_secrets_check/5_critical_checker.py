"""
🚨 Critical Checker
"""
CRITICAL = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]


def check_critical(env_dict):
    return [k for k in CRITICAL if not env_dict.get(k)]


def is_all_critical_present(env_dict):
    return len(check_critical(env_dict)) == 0
