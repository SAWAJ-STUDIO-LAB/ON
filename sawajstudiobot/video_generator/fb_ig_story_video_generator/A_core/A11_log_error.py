"""A11_log_error.py — Sirf error log."""
from A_core.A6_print_logger import log


def log_error(name, error, tb=""):
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    try:
        from A_core.A21_tg_file_error import file_error
        file_error(name, error, tb)
    except Exception:
        pass
