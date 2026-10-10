
# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B1_fonts.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B1_fonts.py                    ║
# ║  🎯 PURPOSE:   Font loader for all scripts               ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

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
    def load(size, script="latin", bold=True):
        """
        Load font for given script.

        Args:
            size:   font size in pixels
            script: devanagari / arabic / latin
            bold:   True for bold, False for regular

        Returns:
            PIL ImageFont object
        """
        # ───────── Devanagari (Hindi) ─────────
        if script == "devanagari":
            paths = [
                "~/.fonts/NotoSansDevanagari-Bold.ttf" if bold
                else "~/.fonts/NotoSansDevanagari-Regular.ttf",
            ]

        # ───────── Arabic (Urdu) ─────────
        elif script == "arabic":
            paths = [
                "~/.fonts/NotoNaskhArabic-Bold.ttf" if bold
                else "~/.fonts/NotoNaskhArabic-Regular.ttf",
            ]

        # ───────── Latin (English) ─────────
        else:
            paths = [
                "~/.fonts/NotoSans-Bold.ttf" if bold
                else "~/.fonts/NotoSans-Regular.ttf",
            ]

        # ───────── Try each path ─────────
        for p in paths:
            try:
                return ImageFont.truetype(os.path.expanduser(p), size)
            except Exception:
                continue

        # ───────── Fallback ─────────
        return ImageFont.load_default()
