# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A7_platform_config.py
# 🎯 PURPOSE:   Platform-specific config
# ═══════════════════════════════════════════════════════════

"""
📤 PLATFORM CONFIG
═══════════════════

🎯 Purpose:
   Har platform ka config.
"""

# ═══════════════════════════════════════════════════════════
# ① PLATFORM CONFIGS
# ═══════════════════════════════════════════════════════════

PLATFORMS = {
    "youtube": {
        "api_version": "v3",
        "category_id": "22",
        "privacy": "public",
        "max_title": 100,
        "max_desc": 5000,
        "max_tags": 500,
    },
    "facebook": {
        "api_version": "v21.0",
        "privacy": "public",
        "max_desc": 5000,
    },
    "instagram": {
        "api_version": "v21.0",
        "media_type_reel": "REELS",
        "media_type_story": "STORIES",
        "max_caption": 2200,
    },
}

# ═══════════════════════════════════════════════════════════
# ② WORKER-PLATFORM MAP
# ═══════════════════════════════════════════════════════════

WORKER_PLATFORMS = {
    "story": ["facebook", "instagram"],
    "short": ["facebook", "instagram", "youtube"],
    "long": ["facebook", "youtube"],
}

# ═══════════════════════════════════════════════════════════
# ③ HELPER
# ═══════════════════════════════════════════════════════════

def get_platform_config(name: str) -> dict:
    """Get platform config."""
    return PLATFORMS.get(name, {})


def get_worker_platforms(worker: str) -> list:
    """Get platforms for worker."""
    return WORKER_PLATFORMS.get(worker, [])# -*- coding: utf-8 -*-
