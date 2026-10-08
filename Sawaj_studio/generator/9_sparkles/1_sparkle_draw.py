"""
✨ Sparkle Draw
"""
import math
import random


def draw_sparkles(draw, t, count=15):
    rng = random.Random(1337)
    for _ in range(count):
        base_x = rng.randint(80, 1000)
        base_y = rng.randint(200, 1800)
        size = rng.randint(3, 9)
        phase = rng.uniform(0, 6.28)
        drift_x = int(8 * math.sin(t + phase))
        drift_y = int(6 * math.cos(t * 0.7 + phase))
        x = base_x + drift_x
        y = base_y + drift_y
        pulse = math.sin(t * 2.5 + phase)
        alpha = int(150 + 100 * pulse)
        alpha = max(60, min(255, alpha))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 240, 180, alpha))
