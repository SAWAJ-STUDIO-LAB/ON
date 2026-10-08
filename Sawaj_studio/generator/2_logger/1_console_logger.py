"""
📺 Console Logger
"""
from datetime import datetime
ICONS = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERROR": "❌", "STEP": "🔹"}


def console_log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    icon = ICONS.get(level.upper(), "•")
    print("[" + ts + "] " + icon + " " + msg, flush=True)


def info(msg): console_log(msg, "INFO")
def ok(msg): console_log(msg, "OK")
def warn(msg): console_log(msg, "WARN")
def error(msg): console_log(msg, "ERROR")
def step(msg): console_log(msg, "STEP")
