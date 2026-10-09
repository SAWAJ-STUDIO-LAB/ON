"""A8_log_file_end.py — Logs the end of a file execution with status and optional notes.

This module is designed to provide a simple way to log the completion of a file's execution,
along with its status and any additional notes. It is particularly useful for tracking the progress
of long-running tasks or for debugging purposes.

Functions:
- log_file_end(name, status, note): Logs the end of a file execution with the given name, status, and note.

Arguments:
- name (str): The name of the file or process being logged.
- status (str, optional): The status of the file execution. Defaults to "success".
- note (str, optional): Additional notes or details about the file execution. Defaults to an empty string.

Usage:
- Call log_file_end() at the end of a file to log its completion.
- The function will print a log message and attempt to send a notification to Telegram.
- If sending to Telegram fails, the function will gracefully handle the exception.

Example:
>>> log_file_end("my_script.py", "completed", "All tasks finished successfully.")
← END my_script.py (completed)

Dependencies:
- A_core.A6_print_logger: For logging messages.
- A_core.A18_tg_file_end: For sending file end notifications to Telegram (optional).
"""

from A_core.A6_print_logger import log
from typing import Optional

def log_file_end(name: str, status: Optional[str] = "success", note: Optional[str] = "") -> None:
    """Logs the end of a file execution with the given name, status, and note.

    Args:
        name (str): The name of the file or process.
        status (str, optional): The status of the file execution. Defaults to "success".
        note (str, optional): Additional notes about the file execution. Defaults to "".

    Returns:
        None
    """
    log_message = f"← END {name} ({status})"
    if note:
        log_message += f" - {note}"
    log(log_message)

    try:
        from A_core.A18_tg_file_end import file_end
        file_end(name, status, note)
    except Exception as e:
        log(f"Failed to send file end notification to Telegram: {e}")
