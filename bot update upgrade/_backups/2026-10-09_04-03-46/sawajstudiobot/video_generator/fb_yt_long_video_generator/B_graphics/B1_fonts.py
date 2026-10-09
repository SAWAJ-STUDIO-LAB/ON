# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B1_fonts.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B1_fonts.py                    ║
# ║  🎯 PURPOSE:   System & custom font loader with fallbacks║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔤 FONT MANAGER MODULE                                 ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Arabic, Hindi, English, and Decorative fonts load    ║
║      karna fallback options ke saath.                    ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import ImageFont
from A_core.A2_logger import log_step


class FontManager:
    """Manages multi-lingual font selection and loading for Pillow rendering."""

    SYSTEM_FONT_PATHS = [
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    @staticmethod
    def get_font(font_path_or_name: str, size: int) -> ImageFont.FreeTypeFont:
        """Loads specific font or safely falls back to default if not found."""
        if font_path_or_name and os.path.exists(font_path_or_name):
            try:
                return ImageFont.truetype(font_path_or_name, size)
            except Exception:
                pass

        # Try system fallbacks
        for sys_path in FontManager.SYSTEM_FONT_PATHS:
            if os.path.exists(sys_path):
                try:
                    return ImageFont.truetype(sys_path, size)
                except Exception:
                    continue

        # Ultimate fallback
        log_step("B1_fonts.py", f"Fallback to default font for {font_path_or_name}", "warn")
        return ImageFont.load_default()

    @staticmethod
    def load_bundle(base_path: str, sizes: dict) -> dict:
        """Loads a dict of fonts for Arabic, Hindi, English, and Titles."""
        fonts = {}
        for key, size in sizes.items():
            path = os.path.join(base_path, f"{key}.ttf") if base_path else ""
            fonts[key] = FontManager.get_font(path, size)
        return fonts
      
