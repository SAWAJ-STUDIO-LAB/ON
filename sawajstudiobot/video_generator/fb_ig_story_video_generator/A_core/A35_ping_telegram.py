"""A35_ping_telegram.py — Module to ping the Telegram bot and check its status.

This module sends a request to the Telegram API to retrieve bot information and determine its status.

Functions:
- ping(): Sends a GET request to the Telegram API to fetch bot details and returns a dictionary with status and related information.
"""

import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ping() -> dict:
    """
    Ping the Telegram bot and return its status.

    Returns a dictionary with the following keys:
    - status: Indicates the status of the bot (working, failed, error, or skipped).
    - bot_name: The username of the bot, if available.
    - code: HTTP status code of the response.
    - reason: Additional information in case of an error.

    Raises:
    - Exception: If an unexpected error occurs during the request.
    """
    try:
        # Get the Telegram bot token from environment variables
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()

        if not token:
            logger.warning("Telegram bot token not found. Skipping ping.")
            return {"status": "skipped", "reason": "No token provided."}

        # Construct the API endpoint URL
        api_endpoint = f"https://api.telegram.org/bot{token}/getMe"

        # Send a GET request to the Telegram API
        response = requests.get(api_endpoint, timeout=8)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()

            if response_data.get("ok"):
                bot_info = response_data.get("result", {})
                bot_name = bot_info.get("username", "?")
                logger.info("Telegram bot is working. Bot name: %s", bot_name)
                return {"status": "working", "bot_name": bot_name, "code": 200}
            else:
                error_message = response_data.get("description", "Unknown error")
                logger.error("Telegram API error: %s", error_message)
                return {"status": "failed", "code": response.status_code, "reason": error_message}
        else:
            logger.error("Failed to ping Telegram bot. HTTP status code: %d", response.status_code)
            return {"status": "failed", "code": response.status_code}

    except requests.RequestException as e:
        logger.error("Request to Telegram API failed: %s", str(e))
        return {"status": "error", "reason": str(e)[:60]}
    except Exception as e:
        logger.exception("Unexpected error occurred: %s", str(e))
        return {"status": "error", "reason": str(e)[:60]}
