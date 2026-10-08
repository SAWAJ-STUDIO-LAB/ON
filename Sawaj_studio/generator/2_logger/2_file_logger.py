"""
📁 File Logger
"""
import os
from datetime import datetime
LOG_DIR = "output/logs"


def _log_file():
    os.makedirs(LOG_DIR, exist_ok=True)
    d = datetime.now().strftime("%Y%m%d")
    return os.path.join(LOG_DIR, "sawaj_" + d + ".log")


def file_log(msg, level="INFO"):
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(_log_file(), "a", encoding="utf-8") as f:
            f.write("[" + ts + "] [" + level.upper() + "] " + msg + "\n")
    except Exception:
        pass


def read_log_file(lines=100):
    p = _log_file()
    if not os.path.exists(p):
        return ""
    with open(p, encoding="utf-8") as f:
        return "".join(f.readlines()[-lines:])
