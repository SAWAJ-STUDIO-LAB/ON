"""
💫 Glow Effect
"""
from PIL import Image, ImageFilter


def add_glow(canvas):
    glow = canvas.filter(ImageFilter.GaussianBlur(6))
    return Image.alpha_composite(glow, canvas)
