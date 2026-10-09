"""A35_ping_telegram.py — Sirf TG ping."""
import os, requests


def ping():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return {"status": "skipped", "reason": "no token"}
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=8)
        if r.status_code == 200 and r.json().get("ok"):
            bot = r.json().get("result", {})
            return {"status": "working", "bot_name": bot.get("username", "?"), "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
