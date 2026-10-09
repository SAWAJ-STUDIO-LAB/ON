"""A44_msg_splitter.py — Splits a message into chunks of a specified maximum length.

This module provides a function to split a message into multiple parts if it exceeds a certain length.
It is useful for handling long messages that need to be sent in smaller chunks.

Functions:
- split(msg, max_len=3800): Splits the input message into a list of chunks, ensuring each chunk's length is within the specified limit.

Usage:
    from A44_msg_splitter import split

    message = "This is a very long message that needs to be split into smaller chunks for processing."
    chunks = split(message, max_len=1000)
    print(chunks)
    # Output: ['This is a very long message that needs to be split into smaller chunks for processing.']
"""


def split(msg: str, max_len: int = 3800) -> list:
    """
    Splits the input message into a list of chunks, each with a length less than or equal to max_len.

    Args:
        msg (str): The message to be split.
        max_len (int, optional): The maximum length of each chunk. Defaults to 3800.

    Returns:
        list: A list of message chunks.

    Raises:
        TypeError: If msg is not a string.
        ValueError: If max_len is not a positive integer.
    """
    try:
        if not isinstance(msg, str):
            raise TypeError("Message must be a string.")
        if not isinstance(max_len, int) or max_len <= 0:
            raise ValueError("Max length must be a positive integer.")

        if len(msg) <= max_len:
            return [msg]

        chunks = []
        current_chunk = ""
        for line in msg.split("\n"):
            if len(current_chunk) + len(line) + 1 > max_len:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += ("\n" if current_chunk else "") + line
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    except Exception as e:
        # Log the error and re-raise it
        import logging
        logging.error(f"Error occurred while splitting message: {e}")
        raise
