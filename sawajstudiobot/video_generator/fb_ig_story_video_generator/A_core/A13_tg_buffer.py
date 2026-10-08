"""
A13_tg_buffer.py
Sirf log buffer + counters.
"""
import time
from datetime import datetime

LOG_BUFFER = []
FILE_TIMERS = {}
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}
START_TIME = [None]
RUN_HEADER = ["📖 STORY VIDEO RUN"]


def now():
    """Current time HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")


def reset():
    """Reset all buffers."""
    LOG_BUFFER.clear()
    FILE_TIMERS.clear()
    STEP_COUNTER.update({"total": 0, "success": 0, "failed": 0})
    START_TIME[0] = time.time()
