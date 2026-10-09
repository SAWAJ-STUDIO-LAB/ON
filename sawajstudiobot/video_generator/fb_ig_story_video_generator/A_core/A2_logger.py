# ╔══════════════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A2_logger.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A2_logger.py                       ║
# ║  🎯 PURPOSE:   Enhanced Print + Telegram logging          ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📝 ENHANCED LOGGER MODULE                              ║
║   ═══════════════════                                     ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Enhanced print and Telegram logging with           ║
║      error handling and type hints.                     ║
║                                                          ║
║   📖 Functions:                                          ║
║      • log()            → Enhanced print with timestamp  ║
║      • log_file_start() → Module start with details      ║
║      • log_file_end()   → Module end with status         ║
║      • log_step()       → Step logging with result        ║
║      • log_api()        → API call logging with status    ║
║      • log_error()      → Error logging with traceback   ║
║                                                          ║
║   ⚠️  Note:                                                ║
║      This module provides a robust logging mechanism     ║
║      with error handling and type hints for better       ║
║      code readability and maintainability.               ║
╚══════════════════════════════════════════════════════════╝
"""

import traceback
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════
# ① ENHANCED PRINT LOGGER WITH ERROR HANDLING
# ═══════════════════════════════════════════════════════════

def log(msg: str, level: str = "INFO") -> None:
    """
    Enhanced print message with timestamp and error handling.

    Args:
        msg (str): Message to log
        level (str, optional): Log level (INFO / WARNING / ERROR). Defaults to "INFO".

    Returns:
        None
    """
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] [{level}] {msg}", flush=True)
    except Exception as e:
        print(f"Logging error: {e}")
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════
# ② FILE START — called at the beginning of the module
# ═══════════════════════════════════════════════════════════

def log_file_start(name: str, purpose: str = "") -> None:
    """
    Log the start of a module with optional purpose.

    Args:
        name (str): Module name
        purpose (str, optional): Module purpose. Defaults to "".

    Returns:
        None
    """
    log(f"→ START {name} - {purpose}")
    try:
        from A_core.A3_telegram import file_start
        file_start(name, purpose)
    except ImportError as e:
        log(f"ImportError: {e}")
    except Exception as e:
        log(f"Error in file_start: {e}")
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════
# ③ FILE END — called at the end of the module
# ═══════════════════════════════════════════════════════════

def log_file_end(name: str, status: str = "success", note: str = "") -> None:
    """
    Log the end of a module with status and optional note.

    Args:
        name (str): Module name
        status (str, optional): Status of the module (success / failed / skipped). Defaults to "success".
        note (str, optional): Additional notes. Defaults to "".

    Returns:
        None
    """
    log(f"← END {name} ({status}) - {note}")
    try:
        from A_core.A3_telegram import file_end
        file_end(name, status, note)
    except ImportError as e:
        log(f"ImportError: {e}")
    except Exception as e:
        log(f"Error in file_end: {e}")
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════
# ④ STEP — called for each step inside the module
# ═══════════════════════════════════════════════════════════

def log_step(name: str, action: str, result: str = "ok", detail: Optional[str] = None) -> None:
    """
    Log a specific step with result and optional details.

    Args:
        name (str): Module name
        action (str): Action performed
        result (str, optional): Result of the action (ok / fail / skip / warn / info). Defaults to "ok".
        detail (str, optional): Additional details. Defaults to None.

    Returns:
        None
    """
    log(f"  • {name} :: {action} → {result} {detail if detail else ''}")
    try:
        from A_core.A3_telegram import step
        step(name, action, result, detail if detail else '')
    except ImportError as e:
        log(f"ImportError: {e}")
    except Exception as e:
        log(f"Error in step: {e}")
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════
# ⑤ API CALL — called for each external API call
# ═══════════════════════════════════════════════════════════

def log_api(name: str, api: str, status: str, detail: Optional[str] = None) -> None:
    """
    Log an API call with status and optional details.

    Args:
        name (str): Module name
        api (str): API name
        status (str): Status of the API call (success / failed / fallback / skipped)
        detail (str, optional): Additional details. Defaults to None.

    Returns:
        None
    """
    log(f"  ★ {name} :: {api} → {status} {detail if detail else ''}")
    try:
        from A_core.A3_telegram import api_call
        api_call(name, api, status, detail if detail else '')
    except ImportError as e:
        log(f"ImportError: {e}")
    except Exception as e:
        log(f"Error in api_call: {e}")
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════
# ⑥ ERROR — called when an error occurs
# ═══════════════════════════════════════════════════════════

def log_error(name: str, error: str, tb: Optional[str] = None) -> None:
    """
    Log an error with optional traceback.

    Args:
        name (str): Module name
        error (str): Error message
        tb (str, optional): Optional traceback string. Defaults to None.

    Returns:
        None
    """
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    try:
        from A_core.A3_telegram import file_error
        file_error(name, error, tb)
    except ImportError as e:
        log(f"ImportError: {e}")
    except Exception as e:
        log(f"Error in file_error: {e}")
        traceback.print_exc()
