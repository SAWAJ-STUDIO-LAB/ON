"""A23_tg_send.py — Send messages to Telegram using the send_raw function.

This module provides a wrapper function, send_tg, which simplifies the process of sending messages to Telegram.
It handles error cases and provides a clean interface for sending messages.

Functions:
- send_tg: Sends a message to Telegram with error handling and optional silent mode.

Usage:
    from A_core.A23_tg_send import send_tg

    send_tg("Hello, Telegram!", silent=True)
"""

import logging
from typing import Union

from A_core.A15_tg_send_raw import send_raw

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_tg(msg: Union[str, bytes], silent: bool = False) -> None:
    """
    Send a message to Telegram with error handling.

    Args:
        msg (str or bytes): The message to be sent.
        silent (bool, optional): Whether to suppress output. Defaults to False.

    Returns:
        None

    Raises:
        TypeError: If msg is not a string or bytes-like object.
        Exception: For any other unexpected errors during sending.
    """
    try:
        # Check msg type
        if not isinstance(msg, (str, bytes)):
            raise TypeError("msg must be a string or bytes-like object.")

        # Send the message
        send_raw(msg, silent=silent)
        if not silent:
            logger.info("Message sent successfully.")

    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise
