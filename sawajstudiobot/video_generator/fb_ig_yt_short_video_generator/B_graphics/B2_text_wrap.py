# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B2_text_wrap.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
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
║      Text wrap + align karna                             ║
║      (Yeh Short ke liye bhi same hai)                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from PIL import ImageDraw
from typing import List


def wrap_text(draw: ImageDraw.Draw, text: str, font: ImageDraw.ImageFont, *, max_width: int = 950) -> List[str]:
    """
    Wrap text into lines based on maximum width.

    Args:
        draw (ImageDraw.Draw): PIL ImageDraw instance.
        text (str): Text to wrap.
        font (ImageDraw.ImageFont): Font to use for text measurement.
        max_width (int, optional): Maximum width of the text. Defaults to 950.

    Returns:
        List[str]: List of wrapped lines.
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


def draw_centered(draw: ImageDraw.Draw, text: str, y: int, font: ImageDraw.ImageFont, fill: tuple, *, shadow: bool = True) -> None:
    """
    Draw text centered on the image.

    Args:
        draw (ImageDraw.Draw): PIL ImageDraw instance.
        text (str): Text to draw.
        y (int): Y-coordinate for the text.
        font (ImageDraw.ImageFont): Font to use for the text.
        fill (tuple): Color fill for the text.
        shadow (bool, optional): Whether to draw a shadow. Defaults to True.
    """
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (1080 - w) // 2
    if shadow:
        draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 220), font=font)
    draw.text((x, y), text, fill=fill, font=font)
