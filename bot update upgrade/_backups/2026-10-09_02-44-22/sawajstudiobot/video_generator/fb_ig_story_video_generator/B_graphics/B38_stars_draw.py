"""B38_stars_draw.py — Sirf stars."""
import math
import random


def draw_stars(draw, t, count=40):
    rng = random.Random(42)
    for _ in range(count):
        x = rng.randint(0, 1080)
        y = rng.randint(0, 1920)
        size = rng.randint(1, 3)
        twinkle = abs(math.sin(t * 2 + x * 0.01))
        alpha = int(100 + 155 * twinkle)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255, alpha))
