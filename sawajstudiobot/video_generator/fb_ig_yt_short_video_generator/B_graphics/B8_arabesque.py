# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B8_arabesque.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B8_arabesque.py                ║
# ║  🎯 PURPOSE:   Islamic pattern overlay (faint)           ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🕌 ARABESQUE MODULE                                    ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Faint Islamic pattern — rotating dots               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math

DEFAULT_OPACITY = 30

def draw_arabesque(draw: any, t: float, opacity: int = DEFAULT_OPACITY) -> None:
    """
    Draw a faint arabesque-style pattern with rotating dots.

    Args:
        draw (ImageDraw): The ImageDraw instance to draw on.
        t (float): Time parameter for animation.
        opacity (int, optional): Opacity of the pattern. Defaults to DEFAULT_OPACITY.
    """
    cx, cy = 540, 960
    r_base = 200 + int(20 * math.sin(t * 0.5))
    for i in range(8):
        angle = (i * math.pi / 4) + t * 0.1
        x = cx + int(r_base * math.cos(angle))
        y = cy + int(r_base * math.sin(angle))
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(212, 175, 55, opacity))
