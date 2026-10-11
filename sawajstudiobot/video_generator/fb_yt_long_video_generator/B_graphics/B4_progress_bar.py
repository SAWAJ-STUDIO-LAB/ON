# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B4_progress_bar.py                        ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B4_progress_bar.py             ║
# ║  ✅ FIXED:     draw_progress(draw, current, total, y)    ║
# ╚══════════════════════════════════════════════════════════╝


def draw_progress(draw, current, total, y=1040):
    """Draw gold progress bar at bottom of 1920x1080 frame."""
    bar_x, bar_w, bar_h = 160, 1600, 6

    # Track
    draw.rectangle(
        [bar_x, y, bar_x + bar_w, y + bar_h],
        fill=(0, 0, 0, 150)
    )

    # Progress fill
    pct = min(1.0, current / max(total, 1))
    fill_w = int(bar_w * pct)

    if fill_w > 0:
        draw.rectangle(
            [bar_x, y, bar_x + fill_w, y + bar_h],
            fill=(212, 175, 55, 255)
        )
        # Glow dot at end
        gx = bar_x + fill_w
        draw.ellipse(
            [gx - 8, y - 4, gx + 8, y + 10],
            fill=(255, 220, 120, 220)
        )
