"""A22_tg_header.py — Generates a header for Telegram messages with rich formatting.

This module is responsible for creating a visually appealing header for Telegram messages.
It appends a formatted string with the specified title to the LOG_BUFFER.

Functions:
- header(title: str) -> None: Generates and appends a header to the LOG_BUFFER.

Example:
    >>> from A_core.A22_tg_header import header
    >>> header("My Title")
    >>> print(LOG_BUFFER)
    ['<b>━━━ My Title ━━━</b>']
"""

from A_core.A13_tg_buffer import LOG_BUFFER

def header(title: str) -> None:
    """
    Generates a header with the given title and appends it to the LOG_BUFFER.

    Args:
        title (str): The title to be displayed in the header.

    Returns:
        None

    Example:
        >>> header("Header Example")
        >>> print(LOG_BUFFER)
        ['<b>━━━ Header Example ━━━</b>']
    """
    try:
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        if not title:
            raise ValueError("Title cannot be empty.")

        formatted_header = f"\n<b>━━━ {title} ━━━</b>"
        LOG_BUFFER.append(formatted_header)

    except TypeError as te:
        print(f"TypeError: {te}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
