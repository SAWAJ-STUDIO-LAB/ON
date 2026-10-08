"""
🔆 Opacity Control
"""
from PIL import Image


def apply_opacity(image, opacity=0.5):
    if opacity >= 1.0:
        return image
    alpha = image.split()[3].point(lambda v: int(v * opacity))
    image.putalpha(alpha)
    return image


def blend_images(base, overlay, alpha=0.5):
    return Image.blend(base.convert("RGBA"),
                       overlay.convert("RGBA"), alpha)
