import time
from datetime import datetime

LOG_BUFFER = []
FILE_TIMERS = {}
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}
START_TIME = [None]
RUN_HEADER = ["📖 STORY VIDEO RUN"]


def now():
    """Returns the current time as a formatted string."""
    return datetime.now().strftime("%H:%M:%S")


def reset():
    """Resets the logging buffer and counters for a new run."""
    LOG_BUFFER.clear()
    FILE_TIMERS.clear()
    STEP_COUNTER.update({"total": 0, "success": 0, "failed": 0})
    START_TIME[0] = time.time()

    log("Log buffer and state reset for a new run.", level="INFO")
