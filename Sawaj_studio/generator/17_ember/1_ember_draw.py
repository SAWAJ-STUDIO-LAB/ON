"""
🔥 Ember Draw
"""
import math
import random


def draw_embers(draw, t, count=15):
    rng = random.Random(int(t * 5))
    for _ in range(count):
        x = rng.randint(50, 1030)
        base_y = rng.randint(0, 1920)
        y = (base_y - int(t * 40)) % 1920
        size = rng.randint(2, 5)
        alpha = int(150 + 100 * math.sin(t * 4 + x))
        alpha = max(80, min(255, alpha))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 140, 60, alpha))
