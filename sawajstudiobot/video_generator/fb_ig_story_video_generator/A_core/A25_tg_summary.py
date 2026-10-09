"""A25_tg_summary.py — Send a summary message to Telegram at the end of the run.

This module is responsible for sending a summary message to Telegram, providing an overview of the run's performance.
It calculates the total number of files processed, the success and failure counts, the total time taken, and the current time.

Functions:
- send_summary(silent=False): Sends the summary message to Telegram.
  - silent (bool): Optional. If True, sends the message silently without notification. Default is False.

Dependencies:
- A_core.A13_tg_buffer: For accessing step counters and start time.
- A_core.A15_tg_send_raw: For sending raw messages to Telegram.
"""

import logging
import time
from typing import Optional

from A_core.A13_tg_buffer import STEP_COUNTER, START_TIME, now
from A_core.A15_tg_send_raw import send_raw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_summary(silent: Optional[bool] = False) -> None:
    """Send a summary message to Telegram.

    Args:
        silent (bool, optional): Whether to send the message silently without notification. Defaults to False.

    Returns:
        None
    """
    try:
        total = STEP_COUNTER["total"]
        ok = STEP_COUNTER["success"]
        fail = STEP_COUNTER["failed"]
        total_time = time.time() - (START_TIME[0] or time.time())
        icon = "🎉" if fail == 0 else "⚠️"
        msg = (f"{icon} <b>RUN COMPLETE</b>\n"
               f"━━━━━━━━━━━━━━━━━━━━━━━\n"
               f"📁 Files: <b>{total}</b>\n"
               f"✅ Success: <b>{ok}</b>\n"
               f"❌ Failed: <b>{fail}</b>\n"
               f"⏱️ Time: <b>{total_time:.1f}s</b>\n"
               f"🕐 Finished: <b>{now()}</b>")

        send_raw(msg, silent=silent)
        logger.info("Summary message sent to Telegram.")

    except Exception as e:
        logger.error(f"Error sending summary: {e}")
        raise
