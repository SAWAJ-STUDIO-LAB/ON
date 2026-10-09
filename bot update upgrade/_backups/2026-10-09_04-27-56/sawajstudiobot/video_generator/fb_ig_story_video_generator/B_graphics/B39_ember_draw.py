"""B39_ember_draw.py — Sirf embers."""
import math
import random
from B_graphics.B40_ember_single import draw_single

EMBER_COUNT = 20


def draw_embers(draw, t, count=EMBER_COUNT):
    rng = random.Random(4242)
    for _ in range(count):
        bx = rng.randint(40, 1040)
        by = rng.randint(0, 1920)
        size = rng.randint(2, 6)
        speed = rng.uniform(30, 80)
        phase = rng.uniform(0, 6.28)
        ab = rng.randint(150, 240)
        rise = (t * speed) % 1920
        y = (by - rise) % 1920
        x = bx + int(15 * math.sin(t * 0.8 + phase))
        pulse = math.sin(t * 3 + phase)
        a = max(80, min(255, int(ab * (0.7 + 0.3 * pulse))))
        draw_single(draw, x, y, size, a)
