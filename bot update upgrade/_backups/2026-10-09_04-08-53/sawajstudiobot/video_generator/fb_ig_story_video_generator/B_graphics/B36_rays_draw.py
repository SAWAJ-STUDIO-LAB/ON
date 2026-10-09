"""B36_rays_draw.py — Sirf rays draw."""
import math

RAY_COUNT, RAY_SPREAD = 7, 0.18
RAY_LENGTH, RAY_WIDTH_TOP, RAY_WIDTH_BOTTOM = 1200, 30, 120
BASE_COLOR = (255, 240, 180)


def draw_god_rays(draw, t, opacity=35, canvas_w=1080, canvas_h=1920):
    cx = canvas_w // 2
    rotation = 0.04 * math.sin(t * 0.3)
    for i in range(RAY_COUNT):
        offset = (i - (RAY_COUNT - 1) / 2) * RAY_SPREAD
        angle = -math.pi / 2 + offset + rotation
        dist = abs(i - (RAY_COUNT - 1) / 2) / ((RAY_COUNT - 1) / 2)
        a = int(opacity * (1 - dist * 0.7))
        pulse = 0.7 + 0.3 * math.sin(t * 1.2 + i * 0.9)
        a = int(a * pulse)
        if a < 3:
            continue
        xe = cx + int(RAY_LENGTH * math.cos(angle))
        ye = int(RAY_LENGTH * math.sin(angle))
        px = int(math.sin(angle) * RAY_WIDTH_BOTTOM / 2)
        py = int(-math.cos(angle) * RAY_WIDTH_BOTTOM / 2)
        draw.polygon([(cx - RAY_WIDTH_TOP//2, 0),
                      (cx + RAY_WIDTH_TOP//2, 0),
                      (xe + px, ye + py),
                      (xe - px, ye - py)],
                     fill=(*BASE_COLOR, a))
