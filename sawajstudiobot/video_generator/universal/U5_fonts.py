"""
U5_fonts.py — Universal Multi-Script Font Loader
=================================================
Handles Devanagari (Hindi) + Arabic (Urdu) + Latin (English).
Cached. System paths + user fonts.
"""

import os
from PIL import ImageFont


class FontManager:
    """Multi-lingual font loader with script support + caching."""

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
        cache_key = (font_path_or_name, size, script)
        if cache_key in FontManager._cache:
            return FontManager._cache[cache_key]

        if font_path_or_name:
            expanded = os.path.expanduser(font_path_or_name)
            if os.path.exists(expanded):
                try:
                    f = ImageFont.truetype(expanded, size)
                    FontManager._cache[cache_key] = f
                    return f
                except Exception:
                    pass

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

        return ImageFont.load_default()


# ─── Backward-compat: FontLoader (Story/Short use this class) ───

class FontLoader:
    """Compat wrapper for existing B1_fonts.py callers."""

    @staticmethod
    def load(size, script="latin", bold=True):
        return FontManager.get_font(None, size, script=script)
