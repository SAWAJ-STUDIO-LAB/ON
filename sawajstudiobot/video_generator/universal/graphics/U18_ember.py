"""
U18_ember.py — Universal rising embers
=======================================
Both function (draw) and image composite variants.
"""

import math
import random
from PIL import Image, ImageDraw


def draw_embers(draw, t, count=15):
    """Draw rising orange ember particles using ImageDraw."""
    W, H = draw.im.size
    rng = random.Random(int(t * 5))
    for _ in range(count):
        x = rng.randint(int(W * 0.05), int(W * 0.95))
        base_y = rng.randint(0, H)
        y = (base_y - int(t * 40)) % H
        size = rng.randint(2, 5)
        alpha = int(150 + 100 * math.sin(t * 4 + x))
        alpha = max(80, min(255, alpha))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 140, 60, alpha))


def draw_ember_particles(image: Image.Image,
                         ember_count=25, seed=100):
    """
    Apply rising embers via alpha composite.

    Returns new PIL Image.
    """
    rng = random.Random(seed)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    W, H = image.size

    for _ in range(ember_count):
        x = rng.randint(int(W * 0.02), int(W * 0.98))
        y = rng.randint(int(H * 0.02), int(H * 0.98))
        r = rng.randint(2, 5)
        a = rng.randint(40, 140)
        color = rng.choice([
            (255, 200, 100, a),
            (255, 160, 60, a),
            (240, 210, 130, a),
        ])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

    return Image.alpha_composite(image.convert("RGBA"), overlay)
