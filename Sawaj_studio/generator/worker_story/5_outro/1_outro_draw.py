"""
🎬 Outro Draw
"""


def draw_outro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.5)
    draw.text((350, 780), "JazakAllah Khair",
              fill=(230, 200, 130, int(255 * alpha)))
