# Re-export universal text wrap (portrait W=1080)
from universal.graphics.U10_text_wrap import (
    wrap_text, wrap_lines, draw_centered as _dc,
)


def draw_centered(draw, text, y, font, fill, shadow=True):
    """Portrait variant — hardcodes W=1080."""
    return _dc(draw, text, y, font, fill, W=1080, shadow=shadow)


__all__ = ["wrap_text", "wrap_lines", "draw_centered"]
