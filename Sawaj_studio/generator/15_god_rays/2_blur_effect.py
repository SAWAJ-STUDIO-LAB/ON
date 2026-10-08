"""
🌫️ Blur Effect
"""
from PIL import ImageFilter


def apply_blur(image, radius=12):
    return image.filter(ImageFilter.GaussianBlur(radius))


def blur_overlay(base, overlay, radius=12):
    from PIL import Image
    blurred = overlay.filter(ImageFilter.GaussianBlur(radius))
    return Image.alpha_composite(base.convert("RGBA"), blurred)
