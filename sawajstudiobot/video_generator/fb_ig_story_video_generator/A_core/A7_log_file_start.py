"""A7_log_file_start.py — Logs the start of a file execution with optional purpose.

This module is designed to log the initiation of a file's execution, providing a clear indication of when a specific file begins its operation.
It also allows for an optional purpose parameter to provide additional context.

Functions:
- log_file_start(name: str, purpose: str = "") -> None: Logs the start of a file execution with an optional purpose.

Usage:
    from A_core.A7_log_file_start import log_file_start

    # Log the start of 'my_script.py' with a purpose
    log_file_start("my_script.py", "Generating weekly reports")
"""

from A_core.A6_print_logger import log
from typing import Optional

def log_file_start(name: str, purpose: Optional[str] = "") -> None:
    """Logs the start of a file execution with an optional purpose.

    Args:
        name (str): The name of the file.
        purpose (str, optional): Additional context or purpose of the file execution. Defaults to an empty string.

    Returns:
        None
    """
    log(f"→ START {name}")
    try:
        from A_core.A17_tg_file_start import file_start
        file_start(name, purpose)
    except Exception as e:
        log(f"Error sending file start log: {e}")
