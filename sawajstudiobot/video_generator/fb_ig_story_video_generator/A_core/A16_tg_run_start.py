from A_core.A13_tg_buffer import reset, now, RUN_HEADER
from A_core.A15_tg_send_raw import send_raw
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_start(title: str = "📖 STORY VIDEO RUN") -> None:
    """
    Initiate the run by resetting the buffer and signaling the start.

    Args:
        title (str, optional): The title of the run. Defaults to "📖 STORY VIDEO RUN".

    Returns:
        None
    """
    try:
        # Reset the buffer
        reset()

        # Update the RUN_HEADER with the provided title
        RUN_HEADER[0] = title

        # Send a message to indicate the start of the run
        send_raw(f"▶️ <b>{title} STARTED</b>\n🕐 {now()}", silent=True)
        logger.info(f"Run started: {title}")

    except Exception as e:
        logger.error(f"Error during run start: {e}")
        raise
