"""
U17_star_field.py — Universal twinkling stars
==============================================
Works as class method (PIL overlay) or function (ImageDraw).
"""

import math
import random
from PIL import Image, ImageDraw


def draw_stars(draw, t, count=40):
    """
    Draw twinkling stars using existing ImageDraw.

    Args:
        draw:  PIL ImageDraw
        t:     time (sec)
        count: number of stars
    """
    W, H = draw.im.size
    rng = random.Random(42)   # stable positions
    for _ in range(count):
        x = rng.randint(0, W)
        y = rng.randint(0, H)
        base_size = rng.randint(1, 3)
        twinkle = abs(math.sin(t * 2 + x * 0.01))
        alpha = int(100 + 155 * twinkle)
        draw.ellipse([x - base_size, y - base_size,
                      x + base_size, y + base_size],
                     fill=(255, 255, 255, alpha))


def draw_star_field(image: Image.Image, star_count=60, seed=42):
    """
    Apply stars via alpha composite (for PIL Image input).

    Returns new PIL Image.
    """
    rng = random.Random(seed)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    W, H = image.size

    for _ in range(star_count):
        x = rng.randint(10, W - 10)
        y = rng.randint(10, H - 10)
        r = rng.choice([1, 1, 2])
        a = rng.randint(60, 180)
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=(255, 255, 255, a))

    return Image.alpha_composite(image.convert("RGBA"), overlay)
