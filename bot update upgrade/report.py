"""
report.py
Telegram pe upgrade report bheje.
"""
import os
import json


WORK_DIR = "bot update upgrade/_work"


def send_telegram(msg):
    """Send message to Telegram."""
    import requests
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat:
        print("⚠️ Telegram not configured")
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat,
                "text": msg[:4000],
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=15
        )
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False


def load_report():
    """Load report from _work/report.json."""
    path = f"{WORK_DIR}/report.json"
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def build_message(data):
    """Build Telegram message."""
    if not data:
        return (
            "⚠️ <b>BOT UPGRADE FAILED</b>\n"
            "━━━━━━━━━━━━━━━\n"
            "No report found.\n"
            "Please check GitHub Actions logs."
        )

    files = data.get("files", 0)
    upgraded = data.get("upgraded", 0)
    ai = data.get("best_ai", "unknown")
    ts = data.get("time", "")

    return (
        "✅ <b>BOT UPGRADE COMPLETE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📁 Files scanned: <b>{files}</b>\n"
        f"⬆️ Files upgraded: <b>{upgraded}</b>\n"
        f"🏆 Best AI: <b>{ai}</b>\n"
        f"🕐 Time: <code>{ts}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎉 <b>Bot is now World #1</b>"
    )


def run():
    """Send report."""
    print("═" * 50)
    print("📱 SENDING REPORT")
    print("═" * 50)

    data = load_report()
    msg = build_message(data)

    ok = send_telegram(msg)
    if ok:
        print("✅ Report sent")
    else:
        print("❌ Report failed")

    return ok


if __name__ == "__main__":
    run()
