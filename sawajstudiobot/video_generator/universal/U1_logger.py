"""
U1_logger.py — Universal Print + Telegram Logger
=================================================
Safe implementation — never crashes even if Telegram is down.
"""

from datetime import datetime


def _safe_telegram(func_name):
    """Import telegram helper safely — never crash logger."""
    try:
        import importlib
        tg = importlib.import_module("A_core.A3_telegram")
        return getattr(tg, func_name)
    except Exception:
        return None


def log(msg, level="INFO"):
    """Print with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


def log_file_start(name, purpose=""):
    log(f"→ START {name}")
    fn = _safe_telegram("file_start")
    if fn:
        try:
            fn(name, purpose)
        except Exception:
            pass


def log_file_end(name, status="success", note=""):
    log(f"← END {name} ({status})")
    fn = _safe_telegram("file_end")
    if fn:
        try:
            fn(name, status, note)
        except Exception:
            pass


def log_step(name, action, result="ok", detail=""):
    log(f"  • {name} :: {action} → {result} {detail}")
    fn = _safe_telegram("step")
    if fn:
        try:
            fn(name, action, result, detail)
        except Exception:
            pass


def log_api(name, api, status, detail=""):
    log(f"  ★ {name} :: {api} → {status}")
    fn = _safe_telegram("api_call")
    if fn:
        try:
            fn(name, api, status, detail)
        except Exception:
            pass


def log_error(name, error, tb=""):
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    fn = _safe_telegram("file_error")
    if fn:
        try:
            fn(name, error, tb)
        except Exception:
            pass


def log_debug(msg):
    import os
    if os.environ.get("SAWAJ_DEBUG"):
        log(msg, level="DEBUG")
