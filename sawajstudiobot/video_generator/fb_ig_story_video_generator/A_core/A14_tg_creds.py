import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_creds() -> tuple:
    """
    Retrieve Telegram credentials from environment variables.

    This function reads the Telegram Bot Token and Chat ID from the environment variables.
    It ensures that the values are not empty and returns them as a tuple.

    Returns:
        tuple: A tuple containing the Telegram Bot Token and Chat ID. If either value is missing or empty,
              it will log a warning and return an empty string for that value.
    """
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if not bot_token:
        logger.warning("Telegram Bot Token is not set or empty.")

    if not chat_id:
        logger.warning("Telegram Chat ID is not set or empty.")

    return bot_token, chat_id
