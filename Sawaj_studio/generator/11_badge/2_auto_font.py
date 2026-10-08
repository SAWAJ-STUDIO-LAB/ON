"""
🔤 Auto Font
"""
from PIL import ImageFont


def fit_badge_font(draw, text, max_width=350):
    for size in (28, 26, 24, 22, 20, 18, 16):
        try:
            font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                return size
        except Exception:
            continue
    return 16
