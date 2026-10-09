# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B5_badge.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/B_graphics║
# ║  🎯 PURPOSE:   Hadith number badge draw (top-left)       ║
# ╚══════════════════════════════════════════════════════════╝

"""
Hadith number badge drawing utility for top-left corner.

Example:
┌───────────────────────────┐
│ #341 · Sahih al-Bukhari   │
└───────────────────────────┘

Design:
- Gold border
- Dark background (200 alpha)
- Rounded corners
"""

from PIL.ImageDraw import ImageDraw
from B_graphics.B1_fonts import FontLoader

def draw_badge(draw: ImageDraw, text: str, y: int = 180) -> None:
    """
    Draw a gold badge with text at the top-left corner.

    Args:
        draw (ImageDraw): PIL ImageDraw object.
        text (str): Badge text (e.g., "#341 · Sahih al-Bukhari").
        y (int, optional): Vertical position. Defaults to 180.
    """
    if not text:
        return

    # Load font
    font = FontLoader.load(26, "latin", bold=True)

    # Calculate size
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    padding = 12

    # Corner coordinates
    x1, y1 = 60, y
    x2, y2 = x1 + width + 2 * padding, y1 + height + padding

    # Background (rounded rectangle)
    draw.rounded_rectangle(
        [x1, y1, x2, y2],
        radius=8,
        fill=(20, 15, 8, 200),
        outline=(212, 175, 55, 220),
        width=2
    )

    # Text
    draw.text(
        (x1 + padding, y1 + padding // 2),
        text,
        fill=(230, 200, 130, 255),
        font=font
    )
