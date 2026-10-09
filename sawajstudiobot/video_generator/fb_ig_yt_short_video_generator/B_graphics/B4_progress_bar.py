# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B4_progress_bar.py                        ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B4_progress_bar.py             ║
# ║  🎯 PURPOSE:   Gold progress bar at bottom               ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📊 PROGRESS BAR MODULE                                 ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Video timeline — gold bar at bottom                 ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_progress() → Bar at y=1820                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""


def draw_progress(draw, current, total, y=1820):
    """Draw gold progress bar at bottom."""
    bar_x, bar_w, bar_h = 80, 920, 8

    # Track
    draw.rectangle([bar_x, y, bar_x + bar_w, y + bar_h],
                   fill=(0, 0, 0, 150))

    # Fill
    pct = min(1.0, current / max(total, 1))
    fill_w = int(bar_w * pct)
    draw.rectangle([bar_x, y, bar_x + fill_w, y + bar_h],
                   fill=(212, 175, 55, 255))

    # Glow dot at end
    if fill_w > 0:
        gx = bar_x + fill_w
        draw.ellipse([gx - 8, y - 4, gx + 8, y + 12],
                     fill=(255, 220, 120, 220))
