"""
A6_print_logger.py
Sirf print karna.
"""
from datetime import datetime


def log(msg, level="INFO"):
    """Print with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)
