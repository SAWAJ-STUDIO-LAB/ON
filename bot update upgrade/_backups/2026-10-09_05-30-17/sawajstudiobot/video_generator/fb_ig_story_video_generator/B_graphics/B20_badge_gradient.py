"""B20_badge_gradient.py — Sirf gradient."""
C_TOP, C_BOT = (25, 18, 8, 220), (15, 10, 5, 240)


def draw_gradient(draw, x1, y1, x2, y2):
    h = y2 - y1
    if h <= 0:
        return
    steps = min(h, 40)
    strip_h = h / steps
    for i in range(steps):
        t = i / max(steps - 1, 1)
        r = int(C_TOP[0] * (1 - t) + C_BOT[0] * t)
        g = int(C_TOP[1] * (1 - t) + C_BOT[1] * t)
        b = int(C_TOP[2] * (1 - t) + C_BOT[2] * t)
        a = int(C_TOP[3] * (1 - t) + C_BOT[3] * t)
        sy = y1 + int(i * strip_h)
        ey = y1 + int((i + 1) * strip_h) + 1
        draw.rectangle([x1 + 4, sy, x2 - 4, ey], fill=(r, g, b, a))
