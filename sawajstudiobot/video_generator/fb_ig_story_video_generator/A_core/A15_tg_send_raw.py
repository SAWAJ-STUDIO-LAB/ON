from A_core.A12_tg_session import session
from A_core.A14_tg_creds import get_creds


def send_raw(msg, silent=False):
    """
    Send a raw message to Telegram.

    Args:
        msg (str): The message to send.
        silent (bool, optional): Whether to disable notification. Defaults to False.
    """
    token, chat_id = get_creds()
    if token and chat_id:
        try:
            session.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": msg[:4000],
                      "parse_mode": "HTML",
                      "disable_web_page_preview": True,
                      "disable_notification": silent},
                timeout=15
            )
        except (TimeoutError, requests.RequestException) as e:
            log(f"Failed to send message to Telegram: {str(e)}")
    print(msg, flush=True)
