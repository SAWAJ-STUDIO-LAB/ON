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
from typing import List, Tuple


# ═══════════════════════════════════════════════════════════
# ① WRAP TEXT — split text into lines
# ═══════════════════════════════════════════════════════════

def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int = 950) -> List[str]:
    """
    Wrap text into lines that fit max_width.

    Args:
        draw (ImageDraw.ImageDraw): PIL ImageDraw object
        text (str): Text to wrap
        font: PIL font object
        max_width (int): Maximum width per line (default 950)

    Returns:
        List[str]: List of wrapped lines
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

def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, font, fill: Tuple[int, int, int, int], shadow: bool = True) -> None:
    """
    Draw text centered at given y position.

    Args:
        draw (ImageDraw.ImageDraw): PIL ImageDraw object
        text (str): Text to draw
        y (int): Vertical position
        font: PIL font object
        fill (Tuple[int, int, int, int]): Text color (RGBA)
        shadow (bool): True for black shadow (default True)
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
