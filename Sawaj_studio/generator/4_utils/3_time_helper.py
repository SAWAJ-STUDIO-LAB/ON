"""
⏱️ Time Helper
"""
import time
from datetime import datetime


def timer_start():
    return time.time()


def timer_elapsed(start):
    return time.time() - start


def format_duration(seconds):
    if seconds < 60:
        return str(round(seconds, 1)) + "s"
    m = int(seconds // 60)
    s = int(seconds % 60)
    return str(m) + "m " + str(s) + "s"


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
