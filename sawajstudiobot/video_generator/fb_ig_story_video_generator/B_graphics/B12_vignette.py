# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B12_vignette.py                           ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B12_vignette.py                ║
# ║  🎯 PURPOSE:   Vignette (soft dark edges with pulse)     ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🌑 VIGNETTE MODULE                                     ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Soft dark edges with a breathing pulse effect.      ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_vignette() → Darken all 4 edges with pulse   ║
║                                                          ║
║   🎨 Effect:                                             ║
║      • Top / Bottom / Left / Right edges                 ║
║      • Breathing intensity (60 ± 20)                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math
from PIL import ImageDraw

# ═══════════════════════════════════════════════════════════
# 🌑 DRAW VIGNETTE
# ═══════════════════════════════════════════════════════════

def draw_vignette(draw: ImageDraw.Draw, t: float, intensity: int = 60) -> None:
    """
    Draw a vignette effect with a breathing pulse on the image.

    Args:
        draw (ImageDraw.Draw): PIL ImageDraw object to draw on.
        t (float): Current time in seconds, used for the breathing effect.
        intensity (int, optional): Base intensity of the vignette (0-100). Defaults to 60.
    """
    # ───────── Breathing pulse calculation ─────────
    pulse = int(intensity + 20 * math.sin(t * 0.8))
    pulse = max(20, min(100, pulse))  # Clamp pulse between 20 and 100

    # ───────── Define the 4 edges ─────────
    edges = [
        (0, 0, 1080, 200),        # Top
        (0, 1720, 1080, 1920),    # Bottom
        (0, 0, 150, 1920),        # Left
        (930, 0, 1080, 1920),     # Right
    ]

    # ───────── Draw each edge with the calculated pulse ─────────
    for (x1, y1, x2, y2) in edges:
        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, pulse))
