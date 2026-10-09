# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B8_arabesque.py                           ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
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
║   📖 Design:                                             ║
║      • 8 dots in circle                                  ║
║      • Rotating slowly                                   ║
║      • Gold color (30% opacity)                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math


# ═══════════════════════════════════════════════════════════
# 🕌 DRAW ARABESQUE
# ═══════════════════════════════════════════════════════════

def draw_arabesque(draw, t, opacity=30):
    """
    Draw faint arabesque-style pattern (rotating).

    Args:
        draw:    PIL ImageDraw object
        t:       current time (seconds)
        opacity: dot opacity (0-255)
    """
    cx, cy = 540, 960       # Center of frame
    r_base = 200 + int(20 * math.sin(t * 0.5))   # Pulsing radius

    # ───────── 8 dots in circle ─────────
    for i in range(8):
        angle = (i * math.pi / 4) + t * 0.1

        x = cx + int(r_base * math.cos(angle))
        y = cy + int(r_base * math.sin(angle))

        # Draw dot
        draw.ellipse(
            [x - 4, y - 4, x + 4, y + 4],
            fill=(212, 175, 55, opacity)
        )
