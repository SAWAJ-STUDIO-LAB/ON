import time
from typing import Union

from A_core.A13_tg_buffer import LOG_BUFFER, FILE_TIMERS, STEP_COUNTER


def file_end(filename: str, status: str = "success", note: Union[str, None] = None) -> None:
    """
    Log the completion of a file processing step with an optional status and note.

    Args:
        filename (str): The name of the file being processed.
        status (str, optional): The status of the operation. Defaults to "success".
        note (str or None, optional): Additional information about the operation. Defaults to None.

    Returns:
        None
    """
    try:
        start_time = FILE_TIMERS.get(filename, time.time())
        elapsed_time = time.time() - start_time

        if status == "success":
            STEP_COUNTER["success"] += 1
            icon = "✅"
        else:
            STEP_COUNTER["failed"] += 1
            icon = "❌"

        log_message = f"{icon} <b>{filename}</b> completed in {elapsed_time:.2f} seconds"
        if note:
            log_message += f" — {note}"

        LOG_BUFFER.append(log_message)
        print(log_message)  # Print the log message for immediate feedback

    except KeyError as e:
        print(f"Error: {e}. File '{filename}' not found in FILE_TIMERS.")
    except Exception as e:
        print(f"An error occurred: {e}")
