from typing import Optional
from PIL import ImageDraw
from B_graphics.B1_fonts import FontLoader

def draw_badge(draw: ImageDraw.Draw, text: str, y: int = 180) -> None:
    """
    Draw a gold badge with the given text at the top-left corner of the image.

    Args:
        draw (ImageDraw.Draw): The ImageDraw instance to draw on.
        text (str): The text to display inside the badge.
        y (int, optional): The vertical position of the badge. Defaults to 180.
    """
    if not text:
        return
    
    fnt = FontLoader.load(26, "latin", bold=True)
    bbox = draw.textbbox((0, 0), text, font=fnt)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    pad = 12
    x1, y1 = 60, y
    x2, y2 = x1 + w + pad * 2, y1 + h + pad
    
    draw.rounded_rectangle([x1, y1, x2, y2], radius=8,
                           fill=(20, 15, 8, 200),
                           outline=(212, 175, 55, 220), width=2)
    draw.text((x1 + pad, y1 + pad // 2), text,
              fill=(230, 200, 130, 255), font=fnt)
