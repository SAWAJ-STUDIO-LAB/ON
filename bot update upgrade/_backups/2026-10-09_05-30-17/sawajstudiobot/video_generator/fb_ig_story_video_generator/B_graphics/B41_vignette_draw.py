"""B41_vignette_draw.py — Sirf vignette."""
import math
from B_graphics.B42_vignette_ring import draw_ring_band

RING_COUNT, PULSE_AMOUNT = 12, 12


def draw_vignette(draw, t, intensity=60, canvas_w=1080, canvas_h=1920):
    pulse = int(PULSE_AMOUNT * math.sin(t * 0.8))
    base = max(20, min(100, intensity + pulse))
    max_dist = int(math.sqrt(canvas_w**2 + canvas_h**2) / 2)
    for i in range(RING_COUNT):
        ratio = 1.0 - (i / RING_COUNT)
        curve = ratio ** 2.5
        alpha = int(base * curve)
        if alpha < 2:
            continue
        margin = int((1 - ratio) * max_dist * 0.5)
        draw_ring_band(draw, canvas_w, canvas_h, margin, alpha)
