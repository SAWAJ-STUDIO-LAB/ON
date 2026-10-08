"""A14_tg_creds.py — Sirf TG creds."""
import os


def get_creds():
    return (os.environ.get("TELEGRAM_BOT_TOKEN", "").strip(),
            os.environ.get("TELEGRAM_CHAT_ID", "").strip())
