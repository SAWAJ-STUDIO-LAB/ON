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
from PIL.ImageDraw import ImageDraw

# ═══════════════════════════════════════════════════════════
# ✨ DRAW SPARKLES
# ═══════════════════════════════════════════════════════════

def draw_sparkles(draw: ImageDraw, t: float, count: int = 12) -> None:
    """
    Draw floating sparkles with random positions and pulsing opacity.

    Args:
        draw (ImageDraw): PIL ImageDraw object to draw on
        t (float): Current time in seconds (used for animation)
        count (int): Number of sparkles to draw (default 12)
    """
    # Fixed seed per 0.1s for consistent animation
    rng = random.Random(int(t * 10))

    for _ in range(count):
        # Random position within typical video dimensions
        x = rng.randint(80, 1000)
        y = rng.randint(200, 1800)

        # Random size for variety
        size = rng.randint(3, 9)

        # Sine wave based opacity for pulsing effect
        alpha = int(120 + 100 * math.sin(t * 3 + x))
        alpha = max(50, min(255, alpha))

        # Draw golden sparkle with calculated opacity
        draw.ellipse(
            [x - size, y - size, x + size, y + size],
            fill=(255, 240, 180, alpha)
        )
