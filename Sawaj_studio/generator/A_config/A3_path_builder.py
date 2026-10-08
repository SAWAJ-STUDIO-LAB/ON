# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A3_path_builder.py
# 🎯 PURPOSE:   Saare paths banana
# ═══════════════════════════════════════════════════════════

"""
📁 PATH BUILDER
═══════════════

🎯 Purpose:
   Project ke saare paths ek jagah.

📖 Paths:
   • ROOT_DIR        → Project root
   • GENERATOR_DIR   → generator/
   • UPLOADER_DIR    → uploader/
   • ASSETS_DIR      → assets/
   • OUTPUT_DIR      → output/
   • LOGS_DIR        → logs/
   • TEMP_DIR        → temp/
"""

import os


# ═══════════════════════════════════════════════════════════
# ① BASE PATHS
# ═══════════════════════════════════════════════════════════

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(_HERE))


# ═══════════════════════════════════════════════════════════
# ② MAIN DIRECTORIES
# ═══════════════════════════════════════════════════════════

GENERATOR_DIR = os.path.join(ROOT_DIR, "generator")
UPLOADER_DIR = os.path.join(ROOT_DIR, "uploader")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


# ═══════════════════════════════════════════════════════════
# ③ OUTPUT SUB-FOLDERS
# ═══════════════════════════════════════════════════════════

STORY_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "story")
SHORT_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "short")
LONG_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "long")
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")
LOGS_DIR = os.path.join(OUTPUT_DIR, "logs")


# ═══════════════════════════════════════════════════════════
# ④ ASSET SUB-FOLDERS
# ═══════════════════════════════════════════════════════════

EMOJI_DIR = os.path.join(ASSETS_DIR, "emoji")
PHOTO_DIR = os.path.join(ASSETS_DIR, "photo")
ICON_DIR = os.path.join(ASSETS_DIR, "icon")
STICKER_DIR = os.path.join(ASSETS_DIR, "sticker")
EFFECT_DIR = os.path.join(ASSETS_DIR, "effect")
SOUND_DIR = os.path.join(ASSETS_DIR, "sound")
FONT_DIR = os.path.join(ASSETS_DIR, "font")
LOGO_DIR = os.path.join(ASSETS_DIR, "logo")


# ═══════════════════════════════════════════════════════════
# ⑤ HELPER
# ═══════════════════════════════════════════════════════════

def build_path(*parts: str) -> str:
    """Build path from parts."""
    return os.path.join(*parts)


def ensure_path(path: str) -> str:
    """Create folder if missing."""
    os.makedirs(path, exist_ok=True)
    return path


# ═══════════════════════════════════════════════════════════
# ⑥ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("📁 Path Builder Self-Test")
    print("=" * 50)
    print(f"  ROOT_DIR:      {ROOT_DIR}")
    print(f"  GENERATOR_DIR: {GENERATOR_DIR}")
    print(f"  UPLOADER_DIR:  {UPLOADER_DIR}")
    print(f"  ASSETS_DIR:    {ASSETS_DIR}")
    print(f"  OUTPUT_DIR:    {OUTPUT_DIR}")
    print("✅ Done")# -*- coding: utf-8 -*-
