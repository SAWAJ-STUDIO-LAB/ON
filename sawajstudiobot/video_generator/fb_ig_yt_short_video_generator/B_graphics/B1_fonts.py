# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B1_fonts.py                               ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B1_fonts.py                    ║
# ║  🎯 PURPOSE:   Font loader for all scripts               ║
# ║  ✅ FIXED:     Robust paths (system + ~/.fonts)          ║
# ╚══════════════════════════════════════════════════════════╝

import os
from PIL import ImageFont


class FontLoader:
    """
    Load fonts from system + ~/.fonts/ with fallback.

    Supports 3 scripts:
      - devanagari → Hindi
      - arabic     → Urdu/Arabic
      - latin      → English (default)
    """

    _cache = {}

    PATHS = {
        "devanagari": [
            "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
            "~/.fonts/NotoSansDevanagari-Bold.ttf",
            "~/.fonts/NotoSansDevanagari-Regular.ttf",
        ],
        "arabic": [
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
            "~/.fonts/NotoNaskhArabic-Bold.ttf",
            "~/.fonts/NotoNaskhArabic-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
        ],
        "latin": [
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "~/.fonts/NotoSans-Bold.ttf",
            "~/.fonts/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
    }

    @staticmethod
    def load(size, script="latin", bold=True):
        """
        Load font for given script.

        Args:
            size:   font size in pixels
            script: devanagari / arabic / latin
            bold:   True for bold, False for regular (kept for compat)

        Returns:
            PIL ImageFont object
        """
        cache_key = (size, script, bold)
        if cache_key in FontLoader._cache:
            return FontLoader._cache[cache_key]

        paths = FontLoader.PATHS.get(script, FontLoader.PATHS["latin"])

        for p in paths:
            expanded = os.path.expanduser(p)
            if bold and "Regular" in expanded:
                continue
            if not bold and "Bold" in expanded:
                continue
            if os.path.exists(expanded):
                try:
                    fnt = ImageFont.truetype(expanded, size)
                    FontLoader._cache[cache_key] = fnt
                    return fnt
                except Exception:
                    continue

        for p in paths:
            expanded = os.path.expanduser(p)
            if os.path.exists(expanded):
                try:
                    fnt = ImageFont.truetype(expanded, size)
                    FontLoader._cache[cache_key] = fnt
                    return fnt
                except Exception:
                    continue

        return ImageFont.load_default()
