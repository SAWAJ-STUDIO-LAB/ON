"""A8_log_file_end.py — Sirf file end log."""
from A_core.A6_print_logger import log


def log_file_end(name, status="success", note=""):
    log(f"← END {name} ({status})")
    try:
        from A_core.A18_tg_file_end import file_end
        file_end(name, status, note)
    except Exception:
        pass
