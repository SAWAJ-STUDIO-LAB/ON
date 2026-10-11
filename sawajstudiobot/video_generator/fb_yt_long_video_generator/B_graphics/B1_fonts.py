# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B1_fonts.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B1_fonts.py                    ║
# ║  ✅ FIXED:     Added script parameter (arabic/hindi/latin)║
# ╚══════════════════════════════════════════════════════════╝

import os
from PIL import ImageFont
from A_core.A2_logger import log_step


class FontManager:
    """Multi-lingual font loader for Long (16:9) videos with script support."""

    _FONTS = {
        "arabic": [
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "~/.fonts/NotoNaskhArabic-Bold.ttf",
        ],
        "devanagari": [
            "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
            "~/.fonts/NotoSansDevanagari-Bold.ttf",
        ],
        "latin": [
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "~/.fonts/NotoSans-Bold.ttf",
        ],
    }

    _cache = {}

    @staticmethod
    def get_font(font_path_or_name, size, script="latin"):
        """
        Load font for a specific script.

        Args:
            font_path_or_name: explicit .ttf path (optional)
            size:              pixel size
            script:            "arabic" | "devanagari" | "latin"
        """
        cache_key = (font_path_or_name, size, script)
        if cache_key in FontManager._cache:
            return FontManager._cache[cache_key]

        # Try explicit path first
        if font_path_or_name:
            expanded = os.path.expanduser(font_path_or_name)
            if os.path.exists(expanded):
                try:
                    f = ImageFont.truetype(expanded, size)
                    FontManager._cache[cache_key] = f
                    return f
                except Exception:
                    pass

        # Try script-specific paths
        paths = FontManager._FONTS.get(script, FontManager._FONTS["latin"])
        for p in paths:
            expanded = os.path.expanduser(p)
            if os.path.exists(expanded):
                try:
                    f = ImageFont.truetype(expanded, size)
                    FontManager._cache[cache_key] = f
                    return f
                except Exception:
                    continue

        # Fallback: any available font
        for font_list in FontManager._FONTS.values():
            for p in font_list:
                expanded = os.path.expanduser(p)
                if os.path.exists(expanded):
                    try:
                        f = ImageFont.truetype(expanded, size)
                        FontManager._cache[cache_key] = f
                        return f
                    except Exception:
                        continue

        log_step("B1_fonts.py", f"Fallback default @ size={size} script={script}", "warn")
        return ImageFont.load_default()

    @staticmethod
    def load_bundle(base_path, sizes):
        fonts = {}
        for key, size in sizes.items():
            fonts[key] = FontManager.get_font(None, size, script=key)
        return fonts
