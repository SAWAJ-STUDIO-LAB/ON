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


# ═══════════════════════════════════════════════════════════
# ① BASIC PRINT LOGGER
# ═══════════════════════════════════════════════════════════

def log(msg, level="INFO"):
    """
    Print message with timestamp.

    Args:
        msg: message to log
        level: INFO / WARNING / ERROR
    """
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


# ═══════════════════════════════════════════════════════════
# ② FILE START — called at beginning of module
# ═══════════════════════════════════════════════════════════

def log_file_start(name, purpose=""):
    """Log start of a module."""
    log(f"→ START {name}")
    from A_core.A3_telegram import file_start
    file_start(name, purpose)


# ═══════════════════════════════════════════════════════════
# ③ FILE END — called at end of module
# ═══════════════════════════════════════════════════════════

def log_file_end(name, status="success", note=""):
    """Log end of a module."""
    log(f"← END {name} ({status})")
    from A_core.A3_telegram import file_end
    file_end(name, status, note)


# ═══════════════════════════════════════════════════════════
# ④ STEP — called for each step inside module
# ═══════════════════════════════════════════════════════════

def log_step(name, action, result="ok", detail=""):
    """
    Log a specific step.

    Args:
        name:   module name
        action: what happened
        result: ok / fail / skip / warn / info
        detail: optional details
    """
    log(f"  • {name} :: {action} → {result} {detail}")
    from A_core.A3_telegram import step
    step(name, action, result, detail)


# ═══════════════════════════════════════════════════════════
# ⑤ API CALL — called for each external API call
# ═══════════════════════════════════════════════════════════

def log_api(name, api, status, detail=""):
    """
    Log an API call result.

    Args:
        name:   module name
        api:    API name
        status: success / failed / fallback / skipped
        detail: optional details
    """
    log(f"  ★ {name} :: {api} → {status}")
    from A_core.A3_telegram import api_call
    api_call(name, api, status, detail)


# ═══════════════════════════════════════════════════════════
# ⑥ ERROR — called when an error occurs
# ═══════════════════════════════════════════════════════════

def log_error(name, error, tb=""):
    """
    Log an error with optional traceback.

    Args:
        name:  module name
        error: error message
        tb:    optional traceback string
    """
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    from A_core.A3_telegram import file_error
    file_error(name, error, tb)
