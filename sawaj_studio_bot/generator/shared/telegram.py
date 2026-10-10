"""Telegram notifier"""
import requests

def send_tg(msg, token=None, chat_id=None):
    if not token or not chat_id:
        import os
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat_id:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML",
                      "disable_web_page_preview": True},
                timeout=12
            )
        except: pass
    print(msg)

def report_api_status(api_status):
    lines = ["📊 <b>API STATUS REPORT</b>\n"]
    for section, status in api_status.items():
        if not status: continue
        lines.append(f"<b>{section}:</b>")
        for name, result in status.items():
            icon = "✅" if result == "success" else "❌" if "failed" in str(result) else "⏸️"
            lines.append(f"  {icon} {name} → {result}")
    send_tg("\n".join(lines))
