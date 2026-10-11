"""
U11_sparkles.py — Universal sparkles
=====================================
Auto-detects canvas from draw.im.size.
"""

import math
import random


def draw_sparkles(draw, t, count=12):
    """
    Draw floating golden sparkles.

    Args:
        draw:  PIL ImageDraw object
        t:     current time (seconds)
        count: number of sparkles
    """
    W, H = draw.im.size
    rng = random.Random(int(t * 10))

    # Padding from edges
    pad_x = int(W * 0.08)
    pad_y = int(H * 0.10)
    size_min, size_max = 3, 9

    for _ in range(count):
        x = rng.randint(pad_x, W - pad_x)
        y = rng.randint(pad_y, H - pad_y)
        size = rng.randint(size_min, size_max)

        alpha = int(120 + 100 * math.sin(t * 3 + x))
        alpha = max(50, min(255, alpha))

        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 240, 180, alpha))
