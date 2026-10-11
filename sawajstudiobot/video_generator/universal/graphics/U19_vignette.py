"""
U19_vignette.py — Universal vignette (PIL-only, no numpy)
==========================================================
Two flavours:
  • draw_vignette(draw, t)   → edge rectangles (works with ImageDraw)
  • apply_vignette(image)    → smooth radial (returns new Image)
"""

import math
from PIL import Image, ImageDraw, ImageFilter


def draw_vignette(draw, t, intensity=60):
    """
    Fast vignette: dark rectangles on 4 edges (breathing pulse).
    """
    W, H = draw.im.size
    pulse = int(intensity + 20 * math.sin(t * 0.8))
    pulse = max(20, min(100, pulse))

    pad_x = int(W * 0.14)
    pad_y = int(H * 0.10)

    edges = [
        (0, 0, W, pad_y),                    # Top
        (0, H - pad_y, W, H),                # Bottom
        (0, 0, pad_x, H),                    # Left
        (W - pad_x, 0, W, H),                # Right
    ]
    for (x1, y1, x2, y2) in edges:
        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, pulse))


def apply_vignette(image: Image.Image, amount=0.6):
    """Smooth radial vignette (slow, PIL-only)."""
    w, h = image.size
    rgba = image.convert("RGBA")

    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)

    cx, cy = w // 2, h // 2
    max_r = int(((w ** 2 + h ** 2) ** 0.5) / 2)

    steps = 60
    for i in range(steps, 0, -1):
        ratio = i / steps
        r = int(max_r * ratio)
        brightness = int(255 * (1 - ratio) ** 1.4)
        mask_draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r], fill=brightness)

    mask = mask.filter(
        ImageFilter.GaussianBlur(radius=max(w, h) // 40))
    mask = mask.point(lambda v: int(v * amount))

    dark = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    dark.putalpha(mask)

    return Image.alpha_composite(rgba, dark)
