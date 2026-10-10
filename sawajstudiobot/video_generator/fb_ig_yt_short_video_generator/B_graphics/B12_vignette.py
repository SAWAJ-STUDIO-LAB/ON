# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B12_vignette.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
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
║      Soft dark edges (breathing pulse)                   ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_vignette() → Darken all 4 edges              ║
║                                                          ║
║   🎨 Effect:                                             ║
║      • Top / Bottom / Left / Right edges                 ║
║      • Breathing intensity (60 ± 20)                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math


def draw_vignette(draw, t, intensity=60):
    """Draw vignette (breathing effect)."""
    pulse = int(intensity + 20 * math.sin(t * 0.8))
    pulse = max(20, min(100, pulse))

    edges = [
        (0, 0, 1080, 200),        # Top
        (0, 1720, 1080, 1920),    # Bottom
        (0, 0, 150, 1920),        # Left
        (930, 0, 1080, 1920),     # Right
    ]
    for (x1, y1, x2, y2) in edges:
        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, pulse))
