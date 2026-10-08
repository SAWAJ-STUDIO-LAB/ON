import os


def get_creds():
    """
    Retrieve Telegram credentials from environment variables.

    Returns:
        tuple: A tuple containing the Telegram Bot Token and Chat ID.
    """
    return (os.environ.get("TELEGRAM_BOT_TOKEN", "").strip(),
            os.environ.get("TELEGRAM_CHAT_ID", "").strip())
