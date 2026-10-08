# ═══════════════════════════════════════════════════════════
# 📄 FILE:      B4_log_levels.py
# 🎯 PURPOSE:   Log levels constants
# ═══════════════════════════════════════════════════════════

"""
📊 LOG LEVELS
══════════════

🎯 Purpose:
   Log levels ki constants.
"""

# ═══════════════════════════════════════════════════════════
# ① LEVELS
# ═══════════════════════════════════════════════════════════

DEBUG = "DEBUG"
INFO = "INFO"
OK = "OK"
WARN = "WARN"
ERROR = "ERROR"
STEP = "STEP"
API = "API"


# ═══════════════════════════════════════════════════════════
# ② ICONS
# ═══════════════════════════════════════════════════════════

ICONS = {
    DEBUG: "🔍",
    INFO: "ℹ️",
    OK: "✅",
    WARN: "⚠️",
    ERROR: "❌",
    STEP: "🔹",
    API: "🌐",
}


# ═══════════════════════════════════════════════════════════
# ③ PRIORITY
# ═══════════════════════════════════════════════════════════

PRIORITY = {
    DEBUG: 10,
    INFO: 20,
    STEP: 25,
    OK: 30,
    API: 35,
    WARN: 40,
    ERROR: 50,
}


def get_icon(level: str) -> str:
    """Get icon for level."""
    return ICONS.get(level.upper(), "•")


def get_priority(level: str) -> int:
    """Get priority for level."""
    return PRIORITY.get(level.upper(), 0)# -*- coding: utf-8 -*-
