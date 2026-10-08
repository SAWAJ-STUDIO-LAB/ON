"""A10_log_api.py — Sirf API log."""
from A_core.A6_print_logger import log


def log_api(name, api, status, detail=""):
    log(f"  ★ {name} :: {api} → {status}")
    try:
        from A_core.A20_tg_api_call import api_call
        api_call(name, api, status, detail)
    except Exception:
        pass
