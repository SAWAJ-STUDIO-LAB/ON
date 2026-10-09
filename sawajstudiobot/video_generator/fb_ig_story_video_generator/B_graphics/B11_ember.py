# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B11_ember.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
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
from PIL.ImageDraw import ImageDraw

# ═══════════════════════════════════════════════════════════
# 🔥 DRAW EMBERS
# ═══════════════════════════════════════════════════════════

def draw_embers(draw: ImageDraw, t: float, count: int = 15) -> None:
    """
    Draw rising orange ember particles.

    Args:
        draw (ImageDraw): PIL ImageDraw object to draw on.
        t (float): Current time in seconds, used for animation.
        count (int, optional): Number of ember particles to draw. Defaults to 15.
    """
    # Seed changes with time — particles move
    rng = random.Random(int(t * 5))

    for _ in range(count):
        # Random position
        x = rng.randint(50, 1030)
        base_y = rng.randint(0, 1920)

        # Rising motion (wraps around)
        y = (base_y - int(t * 40)) % 1920

        # Random size
        size = rng.randint(2, 5)

        # Pulsing alpha
        alpha = int(150 + 100 * math.sin(t * 4 + x))
        alpha = max(80, min(255, alpha))

        # Orange ember
        draw.ellipse(
            [x - size, y - size, x + size, y + size],
            fill=(255, 140, 60, alpha)
        )
