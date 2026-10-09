import time
import logging
from typing import Dict, List
from A_core.A13_tg_buffer import LOG_BUFFER, FILE_TIMERS, STEP_COUNTER


def file_start(filename: str, purpose: str = "") -> None:
    """
    Log the start of a file processing step.

    Args:
        filename (str): The name of the file being processed.
        purpose (str, optional): Additional information about the purpose of this step. Defaults to an empty string.

    Returns:
        None

    Raises:
        TypeError: If 'filename' is not a string.
        ValueError: If 'filename' is empty.

    """
    try:
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        if not filename:
            raise ValueError("Filename cannot be empty.")

        FILE_TIMERS[filename] = time.time()
        STEP_COUNTER["total"] += 1
        log_message = f"📂 <b>{filename}</b>"
        if purpose:
            log_message += f" — <i>{purpose}</i>"
        LOG_BUFFER.append(log_message)
        logging.info(log_message)

    except (TypeError, ValueError) as e:
        logging.error(f"Error in file_start: {e}")
        raise

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
