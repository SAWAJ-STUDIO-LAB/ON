"""
🔲 Border Add
"""
from PIL import Image, ImageDraw


def add_border(img, border=12, bottom=26):
    w = img.width + border * 2
    h = img.height + border + bottom
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, w - 1, h - 1],
                   outline=(212, 175, 55, 255), width=border)
    draw.rectangle([border, border, w - border - 1, h - bottom - 1],
                   outline=(255, 215, 100, 200), width=2)
    draw.rectangle([0, h - bottom, w - 1, h - 1], fill=(20, 15, 8, 245))
    canvas.paste(img, (border, border), img)
    return canvas
