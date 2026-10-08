"""A6_print_logger.py — Sirf print."""
from datetime import datetime


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)
