# ═══════════════════════════════════════════════════════════
# 📄 FILE:      B1_console_logger.py
# 📁 PATH:      generator/B_logger/B1_console_logger.py
# 🎯 PURPOSE:   Console pe log print karna
# ═══════════════════════════════════════════════════════════

"""
📺 CONSOLE LOGGER
══════════════════

🎯 Purpose:
   Console pe colored logs print karna.

📖 Levels:
   • INFO  → ℹ️ Normal info
   • OK    → ✅ Success
   • WARN  → ⚠️ Warning
   • ERROR → ❌ Error
   • STEP  → 🔹 Step
   • API   → 🌐 API call
"""

from datetime import datetime


# ═══════════════════════════════════════════════════════════
# ① LEVEL ICONS
# ═══════════════════════════════════════════════════════════

LEVEL_ICONS = {
    "INFO": "ℹ️",
    "OK": "✅",
    "WARN": "⚠️",
    "ERROR": "❌",
    "STEP": "🔹",
    "API": "🌐",
    "DEBUG": "🔍",
}


# ═══════════════════════════════════════════════════════════
# ② CONSOLE LOG
# ═══════════════════════════════════════════════════════════

def console_log(msg: str, level: str = "INFO"):
    """
    Print message with timestamp + level icon.

    Args:
        msg:   message
        level: INFO/OK/WARN/ERROR/STEP/API/DEBUG
    """
    ts = datetime.now().strftime("%H:%M:%S")
    icon = LEVEL_ICONS.get(level.upper(), "•")
    print(f"[{ts}] {icon} {msg}", flush=True)


# ═══════════════════════════════════════════════════════════
# ③ SHORTCUTS
# ═══════════════════════════════════════════════════════════

def info(msg: str):    console_log(msg, "INFO")
def ok(msg: str):      console_log(msg, "OK")
def warn(msg: str):    console_log(msg, "WARN")
def error(msg: str):   console_log(msg, "ERROR")
def step(msg: str):    console_log(msg, "STEP")
def api(msg: str):     console_log(msg, "API")
def debug(msg: str):   console_log(msg, "DEBUG")


# ═══════════════════════════════════════════════════════════
# ④ BANNER
# ═══════════════════════════════════════════════════════════

def banner(title: str):
    """Print banner."""
    line = "═" * 60
    print(f"\n{line}\n  🟣 {title}\n{line}\n", flush=True)


# ═══════════════════════════════════════════════════════════
# ⑤ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("📺 Console Logger Self-Test")
    print("=" * 50)
    banner("SAWAJ STUDIO TEST")
    info("This is info")
    ok("This is success")
    warn("This is warning")
    error("This is error")
    step("This is step")
    api("This is api")
    debug("This is debug")
    print("✅ Done")# -*- coding: utf-8 -*-
