"""B17_progress_markers.py — Sirf markers."""
BAR_X, BAR_W, BAR_H = 80, 920, 12


def draw_markers(draw, markers, y):
    if not markers:
        return
    cy = y + BAR_H // 2
    for pct in markers:
        pct = max(0.0, min(1.0, pct))
        mx = BAR_X + int(BAR_W * pct)
        draw.ellipse([mx - 3, cy - 3, mx + 3, cy + 3],
                     fill=(255, 250, 200, 220),
                     outline=(180, 140, 40, 255), width=1)
