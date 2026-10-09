"""A24_tg_report.py — Send a full report to Telegram with optional extra sections.

This module is responsible for generating and sending a comprehensive report to Telegram.
It includes the current time, total execution time, and the content of the log buffer.

Functions:
- send_full_report: Sends the full report with optional extra sections and handles chunking for long messages.
"""

import logging
import time
from typing import List, Optional

from A_core.A13_tg_buffer import LOG_BUFFER, START_TIME, RUN_HEADER, now
from A_core.A15_tg_send_raw import send_raw

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_full_report(extra_sections: Optional[List[str]] = None, silent: bool = False) -> None:
    """Send the full report to Telegram with optional extra sections.

    Args:
        extra_sections (list of str, optional): Additional sections to include in the report. Defaults to None.
        silent (bool, optional): Whether to suppress the report in the console. Defaults to False.

    Returns:
        None
    """
    try:
        total_time = time.time() - (START_TIME[0] or time.time())
        head = (f"<b>{RUN_HEADER[0]} — FULL REPORT</b>\n"
                f"🕐 {now()}  |  ⏱️ {total_time:.1f}s\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n")
        body = "\n".join(LOG_BUFFER)
        extras = ""
        if extra_sections:
            extras = "\n\n" + "\n".join(extra_sections)
        full_report = head + body + extras

        # Split the report into chunks if it exceeds Telegram's message limit
        max_message_length = 4096  # Telegram's maximum message length
        chunks = []
        current_chunk = ""
        for line in full_report.split("\n"):
            if len(current_chunk) + len(line) + 1 > max_message_length:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += ("\n" if current_chunk else "") + line
        if current_chunk:
            chunks.append(current_chunk)

        # Send each chunk as a separate message
        for i, chunk in enumerate(chunks, 1):
            prefix = f"📄 <b>Report {i}/{len(chunks)}</b>\n" if len(chunks) > 1 else ""
            send_raw(prefix + chunk, silent=silent)
            logger.info(f"Sent report chunk {i}/{len(chunks)}")

    except Exception as e:
        logger.error(f"Error sending full report: {e}")
        raise
