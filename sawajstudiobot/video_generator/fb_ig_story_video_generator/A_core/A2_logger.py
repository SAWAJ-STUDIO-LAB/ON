# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A2_logger.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
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
║   ⚠️  Note:                                                ║
║      Telegram imports lazy hain — circular avoid         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════
# ① BASIC PRINT LOGGER
# ═══════════════════════════════════════════════════════════

def log(msg: str, level: str = "INFO") -> None:
    """
    Print message with timestamp.

    Args:
        msg (str): Message to log.
        level (str): Log level (INFO, WARNING, ERROR). Defaults to "INFO".
    """
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


# ═══════════════════════════════════════════════════════════
# ② FILE START — called at beginning of module
# ═══════════════════════════════════════════════════════════

def log_file_start(name: str, purpose: str = "") -> None:
    """
    Log start of a module.

    Args:
        name (str): Module name.
        purpose (str, optional): Module purpose. Defaults to "".
    """
    log(f"→ START {name}")
    from A_core.A3_telegram import file_start
    file_start(name, purpose)


# ═══════════════════════════════════════════════════════════
# ③ FILE END — called at end of module
# ═══════════════════════════════════════════════════════════

def log_file_end(name: str, status: str = "success", note: str = "") -> None:
    """
    Log end of a module.

    Args:
        name (str): Module name.
        status (str, optional): Module status. Defaults to "success".
        note (str, optional): Additional note. Defaults to "".
    """
    log(f"← END {name} ({status})")
    from A_core.A3_telegram import file_end
    file_end(name, status, note)


# ═══════════════════════════════════════════════════════════
# ④ STEP — called for each step inside module
# ═══════════════════════════════════════════════════════════

def log_step(name: str, action: str, result: str = "ok", detail: str = "") -> None:
    """
    Log a specific step.

    Args:
        name (str): Module name.
        action (str): Action performed.
        result (str, optional): Result of the action. Defaults to "ok".
        detail (str, optional): Additional details. Defaults to "".
    """
    log(f"  • {name} :: {action} → {result} {detail}")
    from A_core.A3_telegram import step
    step(name, action, result, detail)


# ═══════════════════════════════════════════════════════════
# ⑤ API CALL — called for each external API call
# ═══════════════════════════════════════════════════════════

def log_api(name: str, api: str, status: str, detail: str = "") -> None:
    """
    Log an API call result.

    Args:
        name (str): Module name.
        api (str): API name.
        status (str): API call status.
        detail (str, optional): Additional details. Defaults to "".
    """
    log(f"  ★ {name} :: {api} → {status}")
    from A_core.A3_telegram import api_call
    api_call(name, api, status, detail)


# ═══════════════════════════════════════════════════════════
# ⑥ ERROR — called when an error occurs
# ═══════════════════════════════════════════════════════════

def log_error(name: str, error: str, tb: str = "") -> None:
    """
    Log an error with optional traceback.

    Args:
        name (str): Module name.
        error (str): Error message.
        tb (str, optional): Traceback string. Defaults to "".
    """
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    from A_core.A3_telegram import file_error
    file_error(name, error, tb)
