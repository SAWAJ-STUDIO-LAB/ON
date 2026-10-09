from A_core.A13_tg_buffer import LOG_BUFFER
from typing import Union

def step(filename: str, action: str, result: str = "ok", detail: Union[str, None] = None) -> None:
    """
    Log a specific step in the process with an optional detail message.

    :param filename: The name of the file associated with the step.
    :param action: The action being performed.
    :param result: The result of the step (ok, fail, skip, warn, info).
    :param detail: Optional detail message to provide additional context.
    """
    # Define a dictionary to map result codes to icons
    result_icons = {
        "ok": "✅",
        "fail": "❌",
        "skip": "⏭️",
        "warn": "⚠️",
        "info": "ℹ️"
    }

    # Get the icon based on the result, defaulting to 'ℹ️' if not found
    icon = result_icons.get(result, "ℹ️")

    # Construct the log message
    line = f"{icon} <b>{filename}</b> → {action}"

    # Append the detail if provided
    if detail:
        line += f" ({detail})"

    # Append the log message to the buffer
    LOG_BUFFER.append(line)

# Example usage
step("video.mp4", "Processing", "ok", "Resizing and adding effects")
