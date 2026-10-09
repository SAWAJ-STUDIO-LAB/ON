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


def log(msg, level="INFO"):
    """Print with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)


def log_file_start(name, purpose=""):
    """Module start logging."""
    log(f"→ START {name}")
    from A_core.A3_telegram import file_start
    file_start(name, purpose)


def log_file_end(name, status="success", note=""):
    """Module end logging."""
    log(f"← END {name} ({status})")
    from A_core.A3_telegram import file_end
    file_end(name, status, note)


def log_step(name, action, result="ok", detail=""):
    """Step logging."""
    log(f"  • {name} :: {action} → {result} {detail}")
    from A_core.A3_telegram import step
    step(name, action, result, detail)


def log_api(name, api, status, detail=""):
    """API call logging."""
    log(f"  ★ {name} :: {api} → {status}")
    from A_core.A3_telegram import api_call
    api_call(name, api, status, detail)


def log_error(name, error, tb=""):
    """Error logging."""
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    from A_core.A3_telegram import file_error
    file_error(name, error, tb)
