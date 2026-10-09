"""
A21_tg_file_error.py — Handles file-related errors and logs them with relevant details.

This module provides a function to process and log file errors, including the filename, error message, and optional traceback.

Functions:
- file_error(filename, error, tb=""): Logs file-related errors with optional traceback.
"""
from A_core.A13_tg_buffer import LOG_BUFFER, STEP_COUNTER
import traceback


def file_error(filename: str, error: Exception, tb: str = "") -> None:
    """
    Logs file-related errors with optional traceback.

    Args:
        filename (str): The name of the file where the error occurred.
        error (Exception): The error object raised.
        tb (str, optional): The traceback string. Defaults to an empty string.

    Returns:
        None
    """
    STEP_COUNTER["failed"] += 1
    error_message = f"🚨 <b>{filename}</b> ERROR: {str(error)[:150]}"
    if tb:
        error_message += f"\n<code>{tb[:200]}</code>"
    LOG_BUFFER.append(error_message)

# Example usage:
# try:
#     with open("nonexistent_file.txt", "r") as file:
#         content = file.read()
# except FileNotFoundError as e:
#     file_error("nonexistent_file.txt", e, traceback.format_exc())
