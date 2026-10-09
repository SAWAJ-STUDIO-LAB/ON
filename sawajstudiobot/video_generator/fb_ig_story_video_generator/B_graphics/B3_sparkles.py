# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B3_sparkles.py                            ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
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
║      Golden sparkles (floating particles) draw karna     ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_sparkles() → 12 particles per frame          ║
║                                                          ║
║   🎨 Effect:                                             ║
║      Random positions + sine wave opacity                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math
import random


# ═══════════════════════════════════════════════════════════
# ✨ DRAW SPARKLES
# ═══════════════════════════════════════════════════════════

def draw_sparkles(draw, t, count=12):
    """
    Draw floating sparkles.

    Args:
        draw:  PIL ImageDraw object
        t:     current time (seconds)
        count: number of sparkles (default 12)
    """
    # Fixed seed per 0.1s for stability
    rng = random.Random(int(t * 10))

    for _ in range(count):
        # Random position
        x = rng.randint(80, 1000)
        y = rng.randint(200, 1800)

        # Random size
        size = rng.randint(3, 9)

        # Pulsing alpha
        alpha = int(120 + 100 * math.sin(t * 3 + x))
        alpha = max(50, min(255, alpha))

        # Golden sparkle
        draw.ellipse(
            [x - size, y - size, x + size, y + size],
            fill=(255, 240, 180, alpha)
        )
