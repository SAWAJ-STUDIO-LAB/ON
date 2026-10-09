# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B10_star_field.py                         ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B10_star_field.py              ║
# ║  🎯 PURPOSE:   Twinkling stars background                ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   ⭐ STAR FIELD MODULE                                   ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Twinkling stars — night sky feel                    ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_stars() → 40 stars                           ║
║                                                          ║
║   🎨 Effect:                                             ║
║      • Fixed seed (stable positions)                     ║
║      • Sine wave twinkle                                 ║
║      • White dots                                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math
import random
from PIL.ImageDraw import ImageDraw

def draw_stars(draw: ImageDraw, t: float, count: int = 40) -> None:
    """
    Draw twinkling stars with a fixed seed for consistent positions.

    Args:
        draw (ImageDraw): PIL ImageDraw instance to draw on.
        t (float): Time value for animation effect.
        count (int): Number of stars to draw (default 40).
    """
    rng = random.Random(42)  # Fixed seed for consistent star positions
    for _ in range(count):
        x = rng.randint(0, 1080)
        y = rng.randint(0, 1920)
        base_size = rng.randint(1, 3)
        twinkle = abs(math.sin(t * 2 + x * 0.01))
        alpha = int(100 + 155 * twinkle)
        draw.ellipse([x - base_size, y - base_size, x + base_size, y + base_size],
                     fill=(255, 255, 255, alpha))
