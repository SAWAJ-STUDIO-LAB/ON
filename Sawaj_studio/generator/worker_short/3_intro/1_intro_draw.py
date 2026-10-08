"""
🎬 Intro Draw
"""


def draw_intro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.5)
    p = t / duration if duration > 0 else 0
    if p > 0.5:
        draw.text((400, 980), "Islamic Shorts",
                  fill=(230, 200, 130, int(255 * alpha)))
