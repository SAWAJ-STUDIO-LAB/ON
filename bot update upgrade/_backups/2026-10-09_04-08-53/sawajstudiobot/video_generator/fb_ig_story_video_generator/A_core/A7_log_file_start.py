"""A7_log_file_start.py — Sirf file start log."""
from A_core.A6_print_logger import log


def log_file_start(name, purpose=""):
    log(f"→ START {name}")
    try:
        from A_core.A17_tg_file_start import file_start
        file_start(name, purpose)
    except Exception:
        pass
