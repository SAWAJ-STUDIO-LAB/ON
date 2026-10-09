"""A26_sanitize.py — Sanitize text by removing special characters and whitespace.

This module provides a function to sanitize text, making it suitable for further processing or display.
It removes Unicode control characters, quotation marks, and newlines, and strips leading/trailing spaces.

Functions:
- sanitize(t: str) -> str: Sanitize the input text and return the cleaned version.
"""

import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sanitize(t: str) -> str:
    """Sanitize the input text by removing special characters and whitespace.

    Args:
        t (str): The input text to be sanitized.

    Returns:
        str: Sanitized text with special characters and whitespace removed.
    """
    try:
        if not t:
            return ""
        # Remove Unicode control characters and other special characters
        t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
        # Replace quotation marks and newlines with spaces, then strip spaces
        t = t.replace('"', ' ').replace("'", ' ').replace('\n', ' ').strip()
        return t
    except Exception as e:
        logger.error(f"Error sanitizing text: {e}")
        raise e
