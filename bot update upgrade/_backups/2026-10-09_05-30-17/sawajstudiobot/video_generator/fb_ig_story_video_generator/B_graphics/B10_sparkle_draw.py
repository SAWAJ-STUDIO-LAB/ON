"""B10_sparkle_draw.py — Sirf sparkles."""
import math
import random
from B_graphics.B11_sparkle_star import draw_star

SPARKLE_COUNT = 15
GOLD = (255, 240, 180)
WHITE = (255, 255, 255)


def draw_sparkles(draw, t, count=SPARKLE_COUNT):
    rng = random.Random(1337)
    for _ in range(count):
        bx = rng.randint(80, 1000)
        by = rng.randint(200, 1800)
        size = rng.randint(3, 9)
        phase = rng.uniform(0, 6.28)
        speed = rng.uniform(0.5, 1.5)
        dx = int(8 * math.sin(t * speed + phase))
        dy = int(6 * math.cos(t * speed * 0.7 + phase))
        pulse = math.sin(t * 2.5 * speed + phase)
        alpha = max(60, min(255, int(150 + 100 * pulse)))
        draw_star(draw, bx + dx, by + dy, size, alpha)
