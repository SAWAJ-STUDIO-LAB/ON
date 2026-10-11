"""
U12_progress_bar.py — Universal progress bar
=============================================
Auto-places at bottom of canvas.
"""


def draw_progress(draw, current, total, y=None):
    """
    Draw gold progress bar at bottom.

    Args:
        draw:    PIL ImageDraw
        current: elapsed seconds
        total:   total seconds
        y:       vertical pos (None = auto)
    """
    W, H = draw.im.size

    # Auto-position (leave 60 px margin from bottom)
    if y is None:
        y = H - 60

    # Bar dims (adaptive)
    margin_x = int(W * 0.07)
    bar_x = margin_x
    bar_w = W - (margin_x * 2)
    bar_h = max(6, int(H * 0.004))

    # Track
    draw.rectangle([bar_x, y, bar_x + bar_w, y + bar_h],
                   fill=(0, 0, 0, 150))

    # Progress fill
    pct = min(1.0, current / max(total, 1))
    fill_w = int(bar_w * pct)
    if fill_w > 0:
        draw.rectangle([bar_x, y, bar_x + fill_w, y + bar_h],
                       fill=(212, 175, 55, 255))

        # Glow dot
        gx = bar_x + fill_w
        r = bar_h + 2
        draw.ellipse([gx - r, y - r // 2, gx + r, y + r + r // 2],
                     fill=(255, 220, 120, 220))
