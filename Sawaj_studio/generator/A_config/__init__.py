# ═══════════════════════════════════════════════════════════
# 📄 FILE:      __init__.py
# 🎯 PURPOSE:   A_config package marker
# ═══════════════════════════════════════════════════════════

"""
⚙️ A_CONFIG PACKAGE
════════════════════

📦 Exports:
   • load_env, get_env
   • read_secret, has_secret, mask_secret
   • ROOT_DIR, GENERATOR_DIR, etc.
   • get_mode, is_online, is_offline
   • create_all_folders, create_worker_folders
   • VIDEO_WIDTH, VIDEO_HEIGHT, etc.
   • PLATFORMS, WORKER_PLATFORMS
   • select_worker, list_workers
   • run_validation
"""

from .A1_env_loader import load_env, get_env
from .A2_secret_reader import read_secret, has_secret, mask_secret
from .A3_path_builder import (
    ROOT_DIR, GENERATOR_DIR, UPLOADER_DIR, ASSETS_DIR,
    DOCS_DIR, OUTPUT_DIR, TEMP_DIR, LOGS_DIR,
    STORY_OUTPUT_DIR, SHORT_OUTPUT_DIR, LONG_OUTPUT_DIR,
    EMOJI_DIR, PHOTO_DIR, ICON_DIR, STICKER_DIR,
    EFFECT_DIR, SOUND_DIR, FONT_DIR, LOGO_DIR,
    build_path, ensure_path,
)
from .A4_mode_decider import get_mode, is_online, is_offline, get_worker
from .A5_folder_creator import create_all_folders, create_worker_folders
from .A7_platform_config import PLATFORMS, WORKER_PLATFORMS, get_platform_config, get_worker_platforms
from .A8_worker_selector import WORKERS, select_worker, list_workers
from .A9_validation import validate_secrets, validate_worker, run_validation

__all__ = [
    "load_env", "get_env",
    "read_secret", "has_secret", "mask_secret",
    "ROOT_DIR", "GENERATOR_DIR", "UPLOADER_DIR", "ASSETS_DIR",
    "DOCS_DIR", "OUTPUT_DIR", "TEMP_DIR", "LOGS_DIR",
    "STORY_OUTPUT_DIR", "SHORT_OUTPUT_DIR", "LONG_OUTPUT_DIR",
    "EMOJI_DIR", "PHOTO_DIR", "ICON_DIR", "STICKER_DIR",
    "EFFECT_DIR", "SOUND_DIR", "FONT_DIR", "LOGO_DIR",
    "build_path", "ensure_path",
    "get_mode", "is_online", "is_offline", "get_worker",
    "create_all_folders", "create_worker_folders",
    "PLATFORMS", "WORKER_PLATFORMS", "get_platform_config", "get_worker_platforms",
    "WORKERS", "select_worker", "list_workers",
    "validate_secrets", "validate_worker", "run_validation",
]# -*- coding: utf-8 -*-
