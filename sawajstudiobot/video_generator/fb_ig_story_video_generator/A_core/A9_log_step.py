"""A9_log_step.py — Sirf step log."""
from A_core.A6_print_logger import log


def log_step(name, action, result="ok", detail=""):
    log(f"  • {name} :: {action} → {result} {detail}")
    try:
        from A_core.A19_tg_step import step
        step(name, action, result, detail)
    except Exception:
        pass
