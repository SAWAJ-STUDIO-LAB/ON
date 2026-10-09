"""A30_cmd_runner.py — Execute commands and handle errors.

This module provides a function to run shell commands and log the execution. It also includes error handling to capture and report any command execution failures.

Functions:
- run_cmd(cmd: str) -> None: Executes the given command and logs the result. Handles errors gracefully.
"""

import subprocess
from typing import NoReturn
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error


def run_cmd(cmd: str) -> NoReturn:
    """Execute the given command and log the result.

    Args:
        cmd (str): The command to be executed.

    Returns:
        None: The function does not return any value.

    Raises:
        subprocess.CalledProcessError: If the command execution fails. This error is logged and re-raised.
    """
    log_step("A30_cmd_runner.py", f"Executing command: {cmd[:80]}", "info")
    try:
        subprocess.run(cmd, shell=True, check=True)
        log_step("A30_cmd_runner.py", "Command executed successfully", "ok")
    except subprocess.CalledProcessError as e:
        error_msg = f"Command execution failed: {str(e)[:120]}"
        log_error("A30_cmd_runner.py", error_msg)
        raise subprocess.CalledProcessError(error_msg) from e
