# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B9_god_rays.py                            ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/B_graphics/║
# ║                B9_god_rays.py                            ║
# ║  🎯 PURPOSE:   Soft light rays from top (god rays)       ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🌤️  GOD RAYS MODULE                                    ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Top se light beams — cinematic feel                 ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_god_rays() → 5 beams from top                ║
║                                                          ║
║   🎨 Effect:                                             ║
║      • Warm golden color                                 ║
║      • Slow wave motion                                  ║
║      • 25% opacity                                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math
from PIL import ImageDraw

# ═══════════════════════════════════════════════════════════
# 🌤️  DRAW GOD RAYS
# ═══════════════════════════════════════════════════════════

def draw_god_rays(draw: ImageDraw.Draw, t: float, opacity: int = 25) -> None:
    """
    Draw soft light beams from top center.

    Args:
        draw (ImageDraw.Draw): PIL ImageDraw object
        t (float): Current time in seconds
        opacity (int, optional): Beam opacity (0-255). Defaults to 25.
    """
    cx = 540  # Center X

    # ───────── 5 beams ─────────
    for i in range(5):
        # Angle: spread from -2 to +2
        angle = -math.pi / 2 + (i - 2) * 0.15 + 0.02 * math.sin(t)

        # Beam length
        length = 800
        x2 = cx + int(length * math.cos(angle))
        y2 = int(length * math.sin(angle))

        # Draw beam
        draw.line(
            [(cx, 0), (x2, y2)],
            fill=(255, 240, 180, opacity),
            width=40
        )
