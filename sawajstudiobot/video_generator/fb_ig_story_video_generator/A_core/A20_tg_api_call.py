"""A20_tg_api_call.py — Module for handling API calls and logging.

This module provides a function to log API call details with status and optional details.

Functions:
- api_call(filename, api_name, status, detail=""): Logs API call information with status and optional details.

Attributes:
- LOG_BUFFER (list): A buffer to store log messages.
"""
from A_core.A13_tg_buffer import LOG_BUFFER

def api_call(filename: str, api_name: str, status: str, detail: str = "") -> None:
    """Logs API call information with status and optional details.

    Args:
        filename (str): The name of the file related to the API call.
        api_name (str): The name of the API being called.
        status (str): The status of the API call (success, failed, fallback, skipped).
        detail (str, optional): Additional details about the API call. Defaults to an empty string.

    Returns:
        None
    """
    try:
        # Validate and process input parameters
        if not isinstance(filename, str) or not isinstance(api_name, str) or not isinstance(status, str):
            raise ValueError("Invalid input types. filename, api_name, and status must be strings.")
        if status not in ["success", "failed", "fallback", "skipped"]:
            raise ValueError("Invalid status. Allowed values are 'success', 'failed', 'fallback', 'skipped'.")

        # Get the icon based on the status
        icon = {"success": "🟢", "failed": "🔴", "fallback": "🟡", "skipped": "⚪"}.get(status, "⚫")

        # Construct the log message
        line = f"{icon} <b>{api_name}</b> [{status.upper()}]"
        if detail:
            line += f" — {detail}"

        # Append the log message to the buffer
        LOG_BUFFER.append(line)

    except ValueError as ve:
        # Handle value errors and log the exception
        error_message = f"ValueError: {ve}"
        LOG_BUFFER.append(f"⚠️ <b>ERROR</b> in api_call: {error_message}")
        raise

    except Exception as e:
        # Handle any other exceptions and log the exception
        error_message = str(e)
        LOG_BUFFER.append(f"⚠️ <b>ERROR</b> in api_call: {error_message}")
        raise
