"""
📱 Telegram Bot Sender
"""
import os
import requests


def send_message(text, parse_mode="HTML"):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat:
        return False
    try:
        r = requests.post(
            "https://api.telegram.org/bot" + token + "/sendMessage",
            json={"chat_id": chat, "text": text[:4000], "parse_mode": parse_mode},
            timeout=15)
        return r.status_code == 200
    except Exception:
        return False


def send_document(path, caption=""):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat or not os.path.exists(path):
        return False
    try:
        with open(path, "rb") as f:
            r = requests.post(
                "https://api.telegram.org/bot" + token + "/sendDocument",
                data={"chat_id": chat, "caption": caption, "parse_mode": "HTML"},
                files={"document": f}, timeout=60)
        return r.status_code == 200
    except Exception:
        return False
