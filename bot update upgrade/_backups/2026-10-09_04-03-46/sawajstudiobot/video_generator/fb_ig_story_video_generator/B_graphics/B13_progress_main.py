"""B13_progress_main.py — Sirf progress main."""
from B_graphics.B14_progress_track import draw_track
from B_graphics.B15_progress_fill import draw_fill
from B_graphics.B16_progress_glow import draw_glow

BAR_X, BAR_W, BAR_H, BAR_Y = 80, 920, 12, 1815


def draw_progress(draw, current, total, y=BAR_Y):
    pct = 0.0 if total <= 0 else min(1.0, max(0.0, current / total))
    draw_track(draw, y)
    if pct > 0:
        fill_w = int(BAR_W * pct)
        draw_fill(draw, y, fill_w)
        draw_glow(draw, y, BAR_X + fill_w)
