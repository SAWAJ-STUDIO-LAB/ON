"""B19_badge_fit_font.py — Sirf font fit."""
from B_graphics.B2_font_load import load


def fit_font(draw, text, max_width):
    for size in (28, 26, 24, 22, 20, 18, 16):
        font = load(size, "latin", True)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
    return load(16, "latin", True)
