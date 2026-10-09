# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B3_sparkles.py                            ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B3_sparkles.py                 ║
# ║  🎯 PURPOSE:   Sparkle particles draw                    ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   ✨ SPARKLES MODULE                                     ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Golden sparkles draw karna                          ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_sparkles() → 12 particles per frame          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math
import random
from PIL import ImageDraw

def draw_sparkles(draw: ImageDraw.Draw, t: float, count: int = 12) -> None:
    """
    Draw floating sparkles on the image.

    Args:
        draw (ImageDraw.Draw): PIL ImageDraw instance to draw on.
        t (float): Time in seconds, used for animation.
        count (int, optional): Number of sparkles to draw. Defaults to 12.
    """
    rng = random.Random(int(t * 10))
    for _ in range(count):
        x = rng.randint(80, 1000)
        y = rng.randint(200, 1800)
        size = rng.randint(3, 9)
        alpha = int(120 + 100 * math.sin(t * 3 + x))
        alpha = max(50, min(255, alpha))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 240, 180, alpha))
