"""B16_progress_glow.py — Sirf glow."""
BAR_H = 12


def draw_glow(draw, y, glow_x):
    cy = y + BAR_H // 2
    draw.ellipse([glow_x - 14, cy - 14, glow_x + 14, cy + 14], fill=(212, 175, 55, 80))
    draw.ellipse([glow_x - 9, cy - 9, glow_x + 9, cy + 9], fill=(255, 220, 120, 180))
    draw.ellipse([glow_x - 5, cy - 5, glow_x + 5, cy + 5], fill=(255, 240, 180, 255))
