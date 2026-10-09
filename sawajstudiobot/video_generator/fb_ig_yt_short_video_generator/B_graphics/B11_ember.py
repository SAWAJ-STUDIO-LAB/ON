# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B11_ember.py                              ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B11_ember.py                   ║
# ║  🎯 PURPOSE:   Rising ember particles (warm fire)        ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔥 EMBER MODULE                                        ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Rising orange ember particles (warm feel)           ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_embers() → 15 particles                      ║
║                                                          ║
║   🎨 Effect:                                             ║
║      • Rising motion                                     ║
║      • Orange color (255, 140, 60)                       ║
║      • Random sizes                                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math
import random
from PIL import ImageDraw

def draw_embers(draw: ImageDraw.Draw, t: float, count: int = 15) -> None:
    """
    Draw rising orange ember particles.

    Args:
        draw (ImageDraw.Draw): The drawing context.
        t (float): The current time in seconds.
        count (int, optional): The number of ember particles to draw. Defaults to 15.
    """
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
