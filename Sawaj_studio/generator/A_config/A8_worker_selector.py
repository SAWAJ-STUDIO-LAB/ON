# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A8_worker_selector.py
# 🎯 PURPOSE:   Worker select karna
# ═══════════════════════════════════════════════════════════

"""
👷 WORKER SELECTOR
═══════════════════

🎯 Purpose:
   Kaunsa worker chalega, woh decide karna.

📖 Workers:
   • story  → 50-100 words, 60s
   • short  → 150-400 words, 200s
   • long   → 400-1800 words, 900s
"""

import os


# ═══════════════════════════════════════════════════════════
# ① AVAILABLE WORKERS
# ═══════════════════════════════════════════════════════════

WORKERS = {
    "story": {
        "name": "Story Video",
        "duration": "50-60s",
        "words": "50-100",
        "music_dur": 60,
        "platforms": ["facebook", "instagram"],
    },
    "short": {
        "name": "Short Video",
        "duration": "1-3 min",
        "words": "150-400",
        "music_dur": 200,
        "platforms": ["facebook", "instagram", "youtube"],
    },
    "long": {
        "name": "Long Video",
        "duration": "5-15 min",
        "words": "400-1800",
        "music_dur": 900,
        "platforms": ["facebook", "youtube"],
    },
}


# ═══════════════════════════════════════════════════════════
# ② SELECT WORKER
# ═══════════════════════════════════════════════════════════

def select_worker(name: str = None) -> dict:
    """
    Select worker by name.

    Args:
        name: worker name (story/short/long)

    Returns:
        worker config dict
    """
    if not name:
        name = os.environ.get("WORKER", "story").strip().lower()

    if name not in WORKERS:
        raise ValueError(f"Unknown worker: {name}. Use: {list(WORKERS.keys())}")

    config = WORKERS[name].copy()
    config["key"] = name
    return config


def list_workers() -> list:
    """List all worker names."""
    return list(WORKERS.keys())


# ═══════════════════════════════════════════════════════════
# ③ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("👷 Worker Selector Self-Test")
    print("=" * 50)
    print(f"  Available: {list_workers()}")
    for w in list_workers():
        cfg = select_worker(w)
        print(f"  ✅ {w}: {cfg['name']} ({cfg['duration']})")
    print("✅ Done")# -*- coding: utf-8 -*-
