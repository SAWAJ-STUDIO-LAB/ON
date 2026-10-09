"""A9_log_step.py — Log step with detailed information.

This module provides a function to log a step with a name, action, result, and optional details.
It also sends the step information to Telegram for remote monitoring.

Example:
    >>> log_step("Video Generation", "Started", "pending", "Initiating video creation process.")

Attributes:
    log (function): Logging function imported from A_core.A6_print_logger.

Functions:
    log_step(name, action, result="ok", detail=""):
        Logs the step information and sends it to Telegram.
"""

from A_core.A6_print_logger import log
from A_core.A19_tg_step import step  # Import the step function for Telegram reporting

def log_step(name: str, action: str, result: str = "ok", detail: str = "") -> None:
    """
    Log a step with name, action, result, and optional details.

    Args:
        name (str): Step name.
        action (str): Action performed.
        result (str, optional): Result of the action. Defaults to "ok".
        detail (str, optional): Additional details about the step. Defaults to an empty string.

    Returns:
        None
    """
    log_message = f"  • {name} :: {action} → {result} {detail}"
    log(log_message)  # Log the step information

    try:
        step(name, action, result, detail)  # Send step info to Telegram
    except Exception as e:
        error_message = f"Error sending step info to Telegram: {e}"
        log(error_message)  # Log the error
