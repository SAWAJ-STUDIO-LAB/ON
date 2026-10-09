"""A6_print_logger.py - A simple logging module with print functionality.

This module provides a basic logging mechanism using Python's built-in print function. It includes a log function
that formats messages with a timestamp and log level.

Functions:
- log(msg, level="INFO"): Logs a message with a timestamp and specified log level.

Usage:
    from A6_print_logger import log

    log("Starting video generation process.")
    log("Error occurred while connecting to the database.", level="ERROR")
"""

import sys
from datetime import datetime

# Global variable to store the log level
LOG_LEVEL = "INFO"


def set_log_level(level):
    """
    Sets the global log level.

    Args:
        level (str): The desired log level (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    """
    global LOG_LEVEL
    LOG_LEVEL = level


def log(msg, level="INFO"):
    """
    Logs a message with a timestamp and specified log level.

    Args:
        msg (str): The message to be logged.
        level (str, optional): The log level for the message. Defaults to "INFO".

    Returns:
        None
    """
    try:
        # Validate and format the log level
        if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid log level. Choose from DEBUG, INFO, WARNING, ERROR, CRITICAL.")

        # Get current timestamp
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format the log message
        formatted_msg = f"[{ts}] [{level}] {msg}"

        # Print the message to the specified stream
        if level in ["ERROR", "CRITICAL"]:
            print(formatted_msg, file=sys.stderr, flush=True)
        else:
            print(formatted_msg, flush=True)

    except Exception as e:
        # Handle any exceptions during logging
        print(f"Error in logging: {e}", file=sys.stderr, flush=True)
        raise
