import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOG_BUFFER = []
FILE_TIMERS = {}
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}
START_TIME = [None]
RUN_HEADER = ["📖 STORY VIDEO RUN"]


def now() -> str:
    """
    Returns the current time as a formatted string.

    Returns:
        str: Current time in HH:MM:SS format.
    """
    return datetime.now().strftime("%H:%M:%S")


def reset() -> None:
    """
    Resets the logging buffer and counters for a new run.

    This function clears the log buffer, file timers, and step counters, and sets the start time for a new run.
    """
    LOG_BUFFER.clear()
    FILE_TIMERS.clear()
    STEP_COUNTER.update({"total": 0, "success": 0, "failed": 0})
    START_TIME[0] = time.time()

    log_message = "Log buffer and state reset for a new run."
    log(log_message, level="INFO")


def log(message: str, level: str = "INFO") -> None:
    """
    Logs a message with the current time and specified level.

    Args:
        message (str): The message to be logged.
        level (str, optional): The log level. Defaults to "INFO". Other options include "DEBUG", "WARNING", "ERROR".

    Returns:
        None
    """
    current_time = now()
    formatted_message = f"[{current_time}] {level.upper()}: {message}"
    LOG_BUFFER.append(formatted_message)
    logger.log(getattr(logging, level.upper()), message)


# Example usage
reset()
log("Starting the video generation process.")
log("Downloading assets from the internet.", level="DEBUG")
log("Asset download completed.", level="INFO")
