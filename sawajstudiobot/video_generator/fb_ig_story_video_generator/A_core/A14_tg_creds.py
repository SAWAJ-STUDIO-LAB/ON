"""
A14_tg_creds.py
Sirf Telegram credentials.
"""
import os


def get_creds():
    """Return (token, chat_id)."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    return token, chat_id
