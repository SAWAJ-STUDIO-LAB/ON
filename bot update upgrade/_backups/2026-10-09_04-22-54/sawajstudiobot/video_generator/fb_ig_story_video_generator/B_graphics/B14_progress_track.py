"""B14_progress_track.py — Sirf track."""
BAR_X, BAR_W, BAR_H = 80, 920, 12


def draw_track(draw, y):
    draw.rounded_rectangle([BAR_X, y, BAR_X + BAR_W, y + BAR_H],
                           radius=BAR_H // 2,
                           fill=(0, 0, 0, 180),
                           outline=(60, 45, 20, 200), width=1)
