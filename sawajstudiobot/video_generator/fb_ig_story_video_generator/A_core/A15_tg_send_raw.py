from A_core.A12_tg_session import session
from A_core.A14_tg_creds import get_creds
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_raw(msg: str, silent: bool = False) -> None:
    """
    Send a raw message to Telegram.

    Args:
        msg (str): The message to send.
        silent (bool, optional): Whether to disable notification. Defaults to False.

    Returns:
        None
    """
    token, chat_id = get_creds()

    if token and chat_id:
        try:
            response = session.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": msg[:4000],
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "disable_notification": silent
                },
                timeout=15
            )
            response.raise_for_status()  # Raise an exception for non-2xx status codes
        except (TimeoutError, requests.RequestException) as e:
            logger.error(f"Failed to send message to Telegram: {str(e)}")
        else:
            logger.info(f"Message sent successfully: {msg[:50]}...")
    else:
        logger.warning("Token or chat ID not available. Unable to send message.")

    # Print the message to the console
    print(msg, flush=True)
