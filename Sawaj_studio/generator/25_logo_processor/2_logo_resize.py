"""
📐 Logo Resize
"""
from PIL import Image


def resize_logo(path, max_width=400):
    img = Image.open(path).convert("RGBA")
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)),
                         Image.Resampling.LANCZOS)
    return img
