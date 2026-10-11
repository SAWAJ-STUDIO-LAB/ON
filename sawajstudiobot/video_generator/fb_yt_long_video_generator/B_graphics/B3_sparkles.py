# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B3_sparkles.py                            ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B3_sparkles.py                 ║
# ║  ✅ FIXED:     draw_sparkles(draw, t, count) — matches   ║
# ║                D_video API (16:9 landscape)              ║
# ╚══════════════════════════════════════════════════════════╝

import math
import random


def draw_sparkles(draw, t, count=20):
    """Draw floating golden sparkles (1920x1080 landscape)."""
    rng = random.Random(int(t * 10))

    for _ in range(count):
        x = rng.randint(100, 1820)
        y = rng.randint(100, 980)
        size = rng.randint(3, 9)

        alpha = int(120 + 100 * math.sin(t * 3 + x))
        alpha = max(60, min(255, alpha))

        draw.ellipse(
            [x - size, y - size, x + size, y + size],
            fill=(255, 240, 180, alpha)
        )
