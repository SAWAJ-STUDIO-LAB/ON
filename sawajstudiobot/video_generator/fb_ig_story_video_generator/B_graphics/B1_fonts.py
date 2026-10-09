"""
╔══════════════════════════════════════════════════════════╗
║   🔤 FONT LOADER MODULE                                  ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      3 languages ke fonts load karna:                    ║
║        • Devanagari (Hindi)                              ║
║        • Arabic (Urdu)                                   ║
║        • Latin (English)                                 ║
║                                                          ║
║   📖 Usage:                                              ║
║      from B_graphics.B1_fonts import FontLoader          ║
║      font = FontLoader.load(72, "devanagari")            ║
║                                                          ║
║   🔗 Font Sources:                                       ║
║      ~/.fonts/NotoSansDevanagari-Bold.ttf                ║
║      ~/.fonts/NotoNaskhArabic-Bold.ttf                   ║
║      ~/.fonts/NotoSans-Bold.ttf                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from typing import List
from PIL import ImageFont

# ═══════════════════════════════════════════════════════════
# 🔤 FONT LOADER CLASS
# ═══════════════════════════════════════════════════════════

class FontLoader:
    """
    Load fonts from ~/.fonts/ with fallback.

    Supports 3 scripts:
      - devanagari → Hindi
      - arabic     → Urdu/Arabic
      - latin      → English (default)
    """

    # ─────────────────────────────────────────────────────
    # ① LOAD — load font by size + script
    # ─────────────────────────────────────────────────────
    @staticmethod
    def load(size: int, script: str = "latin", bold: bool = True) -> ImageFont.FreeTypeFont:
        """
        Load font for given script.

        Args:
            size (int): Font size in pixels.
            script (str): devanagari / arabic / latin.
            bold (bool): True for bold, False for regular.

        Returns:
            ImageFont.FreeTypeFont: PIL ImageFont object.
        """
        # ───────── Devanagari (Hindi) ─────────
        if script == "devanagari":
            paths: List[str] = [
                os.path.expanduser("~/.fonts/NotoSansDevanagari-Bold.ttf") if bold else 
                os.path.expanduser("~/.fonts/NotoSansDevanagari-Regular.ttf"),
            ]

        # ───────── Arabic (Urdu) ─────────
        elif script == "arabic":
            paths: List[str] = [
                os.path.expanduser("~/.fonts/NotoNaskhArabic-Bold.ttf") if bold else 
                os.path.expanduser("~/.fonts/NotoNaskhArabic-Regular.ttf"),
            ]

        # ───────── Latin (English) ─────────
        else:
            paths: List[str] = [
                os.path.expanduser("~/.fonts/NotoSans-Bold.ttf") if bold else 
                os.path.expanduser("~/.fonts/NotoSans-Regular.ttf"),
            ]

        # ───────── Try each path ─────────
        for path in paths:
            try:
                return ImageFont.truetype(path, size)
            except (FileNotFoundError, IOError):
                continue

        # ───────── Fallback ─────────
        return ImageFont.load_default()
