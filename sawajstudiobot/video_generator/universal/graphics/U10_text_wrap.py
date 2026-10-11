"""
U10_text_wrap.py — Wrap + centered draw
========================================
Auto-detects canvas width — works for portrait & landscape.
"""


def wrap_text(draw, text, font, max_width=950):
    """Wrap text into lines fitting max_width."""
    if not text:
        return []
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, text, y, font, fill, W=1080, shadow=True):
    """
    Draw text centered horizontally.

    Args:
        draw:   PIL ImageDraw object
        text:   text to draw
        y:      vertical position
        font:   PIL font
        fill:   RGBA tuple
        W:      canvas width (default 1080 for portrait)
        shadow: black shadow offset
    """
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    if shadow:
        draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 220), font=font)
    draw.text((x, y), text, fill=fill, font=font)


# Also provide wrap_text compatible with new signature (text, font, max_width)
def wrap_lines(draw, text, font, max_width=950):
    """Same as wrap_text — kept for backward compat."""
    return wrap_text(draw, text, font, max_width)
