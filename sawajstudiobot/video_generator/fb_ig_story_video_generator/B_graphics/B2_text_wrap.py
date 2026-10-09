# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B2_text_wrap.py                           ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B2_text_wrap.py                ║
# ║  🎯 PURPOSE:   Text wrap + center align helpers          ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📝 TEXT WRAP MODULE                                    ║
║   ═════════════════════                                  ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Text ko lines mein wrap karna + align karna        ║
║                                                          ║
║   📖 Functions:                                          ║
║      • wrap_text()      → Break long text into lines     ║
║      • draw_centered()  → Draw text centered             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from PIL import ImageDraw


# ═══════════════════════════════════════════════════════════
# ① WRAP TEXT — split text into lines
# ═══════════════════════════════════════════════════════════

def wrap_text(draw, text, font, max_width=950):
    """
    Wrap text into lines that fit max_width.

    Args:
        draw:      PIL ImageDraw object
        text:      text to wrap
        font:      PIL font object
        max_width: maximum width per line (default 950)

    Returns:
        list of lines
    """
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


# ═══════════════════════════════════════════════════════════
# ② DRAW CENTERED — draw text at center
# ═══════════════════════════════════════════════════════════

def draw_centered(draw, text, y, font, fill, shadow=True):
    """
    Draw text centered at given y.

    Args:
        draw:   PIL ImageDraw object
        text:   text to draw
        y:      vertical position
        font:   PIL font
        fill:   text color (RGBA)
        shadow: True for black shadow
    """
    if not text:
        return

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (1080 - w) // 2

    # Shadow
    if shadow:
        draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 220), font=font)

    # Main text
    draw.text((x, y), text, fill=fill, font=font)
