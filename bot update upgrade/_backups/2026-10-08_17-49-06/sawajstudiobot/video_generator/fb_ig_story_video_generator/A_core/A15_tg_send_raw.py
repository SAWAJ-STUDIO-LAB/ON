"""A15_tg_send_raw.py — Sirf raw send."""
from A_core.A12_tg_session import session
from A_core.A14_tg_creds import get_creds


def send_raw(msg, silent=False):
    token, chat_id = get_creds()
    if token and chat_id:
        try:
            session.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": msg[:4000],
                      "parse_mode": "HTML",
                      "disable_web_page_preview": True,
                      "disable_notification": silent},
                timeout=15)
        except Exception:
            pass
    print(msg, flush=True)
