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


def draw_arabesque(draw, t, opacity=30):
    """Draw faint arabesque-style pattern."""
    cx, cy = 540, 960
    r_base = 200 + int(20 * math.sin(t * 0.5))
    for i in range(8):
        angle = (i * math.pi / 4) + t * 0.1
        x = cx + int(r_base * math.cos(angle))
        y = cy + int(r_base * math.sin(angle))
        draw.ellipse([x - 4, y - 4, x + 4, y + 4],
                     fill=(212, 175, 55, opacity))
