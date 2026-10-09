# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A2_logger.py                              ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                A_core/A2_logger.py                       ║
# ║  🎯 PURPOSE:   Print + Telegram logging                  ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📝 LOGGER MODULE                                       ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Print + Telegram ko log bhejna                     ║
║                                                          ║
║   📖 Functions:                                          ║
║      • log()            → Simple print                   ║
║      • log_file_start() → Module start                   ║
║      • log_file_end()   → Module end                     ║
║      • log_step()       → Step logging                   ║
║      • log_api()        → API call logging               ║
║      • log_error()      → Error logging                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from datetime import datetime
from A_core.A3_telegram import file_start, file_end, step, api_call, file_error

def log(msg: str, level: str = "INFO") -> None:
    """
    Print message with timestamp.

    Args:
        msg (str): Message to log.
        level (str): Log level (default: "INFO").
    """
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")

def log_file_start(name: str, purpose: str = "") -> None:
    """
    Log module start.

    Args:
        name (str): Module name.
        purpose (str): Module purpose (default: "").
    """
    log(f"→ START {name}")
    file_start(name, purpose)

def log_file_end(name: str, status: str = "success", note: str = "") -> None:
    """
    Log module end.

    Args:
        name (str): Module name.
        status (str): Completion status (default: "success").
        note (str): Additional note (default: "").
    """
    log(f"← END {name} ({status})")
    file_end(name, status, note)

def log_step(name: str, action: str, result: str = "ok", detail: str = "") -> None:
    """
    Log step execution.

    Args:
        name (str): Step name.
        action (str): Action performed.
        result (str): Result of the action (default: "ok").
        detail (str): Additional details (default: "").
    """
    log(f"  • {name} :: {action} → {result} {detail}")
    step(name, action, result, detail)

def log_api(name: str, api: str, status: str, detail: str = "") -> None:
    """
    Log API call.

    Args:
        name (str): API name.
        api (str): API endpoint.
        status (str): Call status.
        detail (str): Additional details (default: "").
    """
    log(f"  ★ {name} :: {api} → {status}")
    api_call(name, api, status, detail)

def log_error(name: str, error: str, tb: str = "") -> None:
    """
    Log error.

    Args:
        name (str): Error source.
        error (str): Error message.
        tb (str): Traceback (default: "").
    """
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    file_error(name, error, tb)
