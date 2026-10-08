# ═══════════════════════════════════════════════════════════
# 📄 FILE:      B2_file_logger.py
# 🎯 PURPOSE:   File mein log save karna
# ═══════════════════════════════════════════════════════════

"""
📁 FILE LOGGER
══════════════

🎯 Purpose:
   Logs ko file mein save karna.

📖 File:
   output/logs/sawaj_YYYYMMDD.log
"""

import os
from datetime import datetime

from A_config.A3_path_builder import LOGS_DIR, ensure_path


# ═══════════════════════════════════════════════════════════
# ① LOG FILE PATH
# ═══════════════════════════════════════════════════════════

def get_log_file() -> str:
    """Return today's log file path."""
    ensure_path(LOGS_DIR)
    date = datetime.now().strftime("%Y%m%d")
    return os.path.join(LOGS_DIR, f"sawaj_{date}.log")


# ═══════════════════════════════════════════════════════════
# ② WRITE TO FILE
# ═══════════════════════════════════════════════════════════

def file_log(msg: str, level: str = "INFO"):
    """
    Write log to file.

    Args:
        msg:   message
        level: log level
    """
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] [{level.upper()}] {msg}\n"

        with open(get_log_file(), "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════
# ③ READ LOG FILE
# ═══════════════════════════════════════════════════════════

def read_log_file(lines: int = 100) -> str:
    """Read last N lines from log file."""
    path = get_log_file()
    if not os.path.exists(path):
        return ""

    try:
        with open(path, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
        return "".join(all_lines[-lines:])
    except Exception:
        return ""


# ═══════════════════════════════════════════════════════════
# ④ CLEAR LOG FILE
# ═══════════════════════════════════════════════════════════

def clear_log_file():
    """Clear today's log file."""
    path = get_log_file()
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════
# ⑤ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("📁 File Logger Self-Test")
    print("=" * 50)
    file_log("Test info", "INFO")
    file_log("Test error", "ERROR")
    print(f"  Log file: {get_log_file()}")
    print(f"  Last 2 lines:\n{read_log_file(2)}")
    print("✅ Done")# -*- coding: utf-8 -*-
