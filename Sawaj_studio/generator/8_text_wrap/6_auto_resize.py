"""
🔍 Auto Resize
"""
from PIL import ImageFont


def fit_font_size(draw, text, max_width, font_path,
                  start_size=72, min_size=16):
    from .2_width_measure import measure_text
    for size in range(start_size, min_size - 1, -2):
        try:
            font = ImageFont.truetype(font_path, size)
            w, _ = measure_text(draw, text, font)
            if w <= max_width:
                return font
        except Exception:
            continue
    return None
