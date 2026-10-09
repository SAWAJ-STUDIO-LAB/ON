"""B28_bullet_circle.py — Sirf circle."""
BULLET_X, BULLET_SIZE = 130, 40


def draw_circle(draw, y, color, alpha):
    a = int(255 * max(alpha, 0.6))
    cy = y + BULLET_SIZE // 2 + 10
    cx = BULLET_X + BULLET_SIZE // 2
    draw.ellipse([cx - BULLET_SIZE//2 - 4, cy - BULLET_SIZE//2 - 4,
                  cx + BULLET_SIZE//2 + 4, cy + BULLET_SIZE//2 + 4],
                 fill=(*color, a // 3))
    draw.ellipse([cx - BULLET_SIZE//2, cy - BULLET_SIZE//2,
                  cx + BULLET_SIZE//2, cy + BULLET_SIZE//2],
                 fill=(*color, a), outline=(255, 255, 255, a), width=2)
