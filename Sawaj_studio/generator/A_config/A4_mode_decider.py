# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A4_mode_decider.py
# 🎯 PURPOSE:   Offline / Online mode decide karna
# ═══════════════════════════════════════════════════════════

"""
🎯 MODE DECIDER
════════════════

🎯 Purpose:
   Decide karna kaunsa mode chalega.

📖 Modes:
   • offline  → Sirf Google Drive
   • online   → Drive + Social upload
   • auto     → Schedule se auto decide

📖 Logic:
   • GITHUB_EVENT_NAME == "schedule" → auto online
   • UPLOAD_MODE = "online" + UPLOAD_CONFIRMED = true → online
   • Warna → offline
"""

import os


# ═══════════════════════════════════════════════════════════
# ① GET MODE
# ═══════════════════════════════════════════════════════════

def get_mode() -> str:
    """
    Return current mode.

    Returns:
        "offline" | "online"
    """
    event = os.environ.get("GITHUB_EVENT_NAME", "").strip()
    mode = os.environ.get("UPLOAD_MODE", "offline").strip().lower()
    confirmed = os.environ.get("UPLOAD_CONFIRMED", "false").strip().lower() == "true"

    # Scheduled → auto online
    if event == "schedule":
        return "online"

    # Manual online with confirm
    if mode == "online" and confirmed:
        return "online"

    return "offline"


# ═══════════════════════════════════════════════════════════
# ② IS ONLINE
# ═══════════════════════════════════════════════════════════

def is_online() -> bool:
    """Check if online mode."""
    return get_mode() == "online"


def is_offline() -> bool:
    """Check if offline mode."""
    return get_mode() == "offline"


# ═══════════════════════════════════════════════════════════
# ③ GET WORKER
# ═══════════════════════════════════════════════════════════

def get_worker() -> str:
    """
    Return which worker to run.

    Returns:
        "story" | "short" | "long"
    """
    return os.environ.get("WORKER", "story").strip().lower()


# ═══════════════════════════════════════════════════════════
# ④ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎯 Mode Decider Self-Test")
    print("=" * 50)
    print(f"  Mode:   {get_mode()}")
    print(f"  Online: {is_online()}")
    print(f"  Worker: {get_worker()}")
    print("✅ Done")# -*- coding: utf-8 -*-
