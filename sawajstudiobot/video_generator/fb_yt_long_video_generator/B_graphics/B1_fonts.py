# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B1_fonts.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B1_fonts.py                    ║
# ║  ✅ FIXED:     Robust font paths (system + ~/.fonts)     ║
# ╚══════════════════════════════════════════════════════════╝

import os
from PIL import ImageFont
from A_core.A2_logger import log_step


class FontManager:
    """Manages multi-lingual font selection for Long (16:9) videos."""

    SYSTEM_FONT_PATHS = [
        # Devanagari (Hindi)
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
        "~/.fonts/NotoSansDevanagari-Bold.ttf",
        "~/.fonts/NotoSansDevanagari-Regular.ttf",
        # Arabic (Urdu)
        "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
        "~/.fonts/NotoNaskhArabic-Bold.ttf",
        "~/.fonts/NotoNaskhArabic-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
        # Latin
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "~/.fonts/NotoSans-Bold.ttf",
        "~/.fonts/NotoSans-Regular.ttf",
        # DejaVu fallback
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    _cache = {}

    @staticmethod
    def get_font(font_path_or_name, size):
        """Load specific font or fallback to system."""
        cache_key = (font_path_or_name, size)
        if cache_key in FontManager._cache:
            return FontManager._cache[cache_key]

        # Try specific path first
        if font_path_or_name:
            expanded = os.path.expanduser(font_path_or_name)
            if os.path.exists(expanded):
                try:
                    f = ImageFont.truetype(expanded, size)
                    FontManager._cache[cache_key] = f
                    return f
                except Exception:
                    pass

        # Try system fallbacks
        for sys_path in FontManager.SYSTEM_FONT_PATHS:
            expanded = os.path.expanduser(sys_path)
            if os.path.exists(expanded):
                try:
                    f = ImageFont.truetype(expanded, size)
                    FontManager._cache[cache_key] = f
                    return f
                except Exception:
                    continue

        # Ultimate fallback
        log_step("B1_fonts.py", f"Fallback default font @ size={size}", "warn")
        return ImageFont.load_default()

    @staticmethod
    def load_bundle(base_path, sizes):
        """Load dict of fonts."""
        fonts = {}
        for key, size in sizes.items():
            path = os.path.join(base_path, f"{key}.ttf") if base_path else None
            fonts[key] = FontManager.get_font(path, size)
        return fonts
