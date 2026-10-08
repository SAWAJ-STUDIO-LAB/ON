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


def draw_sparkles(draw, t, count=12):
    """Draw floating sparkles."""
    rng = random.Random(int(t * 10))
    for _ in range(count):
        x = rng.randint(80, 1000)
        y = rng.randint(200, 1800)
        size = rng.randint(3, 9)
        alpha = int(120 + 100 * math.sin(t * 3 + x))
        alpha = max(50, min(255, alpha))
        draw.ellipse([x - size, y - size, x + size, y + size],
                     fill=(255, 240, 180, alpha))
