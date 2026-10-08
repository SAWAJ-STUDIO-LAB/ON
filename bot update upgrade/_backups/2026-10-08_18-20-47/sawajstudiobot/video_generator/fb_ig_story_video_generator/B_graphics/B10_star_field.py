# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B10_star_field.py                         ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
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


# ═══════════════════════════════════════════════════════════
# ⭐ DRAW STARS
# ═══════════════════════════════════════════════════════════

def draw_stars(draw, t, count=40):
    """
    Draw twinkling stars (fixed seed for stability).

    Args:
        draw:  PIL ImageDraw object
        t:     current time (seconds)
        count: number of stars (default 40)
    """
    # Fixed seed — positions stable
    rng = random.Random(42)

    for _ in range(count):
        # Random position
        x = rng.randint(0, 1080)
        y = rng.randint(0, 1920)

        # Random size
        base_size = rng.randint(1, 3)

        # Twinkle effect
        twinkle = abs(math.sin(t * 2 + x * 0.01))
        alpha = int(100 + 155 * twinkle)

        # White dot
        draw.ellipse(
            [x - base_size, y - base_size, x + base_size, y + base_size],
            fill=(255, 255, 255, alpha)
        )
