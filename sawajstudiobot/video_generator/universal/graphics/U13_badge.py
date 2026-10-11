"""
U13_badge.py — Universal hadith badge (top-left)
=================================================
Uses universal FontManager for Latin text.
"""

from universal.U5_fonts import FontManager


def draw_badge(draw, text, y=None):
    """Draw gold badge with hadith reference at top-left."""
    if not text:
        return

    W, H = draw.im.size

    # Auto y (60 for landscape, 180 for portrait)
    if y is None:
        y = 60 if W > H else 180

    # Adaptive font size
    font_size = 32 if W > H else 26
    fnt = FontManager.get_font(None, font_size, script="latin")

    bbox = draw.textbbox((0, 0), text, font=fnt)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    pad_x, pad_y = 16, 10

    # Left margin
    left = 80 if W > H else 60
    x1, y1 = left, y
    x2, y2 = x1 + w + pad_x * 2, y1 + h + pad_y * 2

    # Rounded rect
    draw.rounded_rectangle(
        [x1, y1, x2, y2],
        radius=10,
        fill=(20, 15, 8, 200),
        outline=(212, 175, 55, 220),
        width=2)

    # Text
    draw.text((x1 + pad_x, y1 + pad_y - bbox[1]),
              text,
              fill=(230, 200, 130, 255),
              font=fnt)
