"""
🔲 Border Draw
"""


def draw_arabesque_border(img_draw, w=1080, h=1920,
                          margin=25, color=(212, 175, 55, 180)):
    img_draw.rectangle([margin, margin, w - margin, h - margin],
                       outline=color, width=3)


def draw_double_arabesque_border(img_draw, w=1080, h=1920, margin=25):
    color = (212, 175, 55, 180)
    m2 = margin + 8
    img_draw.rectangle([margin, margin, w - margin, h - margin],
                       outline=color, width=3)
    img_draw.rectangle([m2, m2, w - m2, h - m2],
                       outline=color, width=1)
