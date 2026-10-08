"""
🎬 Intro Draw
"""


def draw_intro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.7)
    p = t / duration if duration > 0 else 0
    if p > 0.5:
        draw.text((700, 720), "HADITH OF THE DAY",
                  fill=(230, 200, 130, int(255 * alpha)))
