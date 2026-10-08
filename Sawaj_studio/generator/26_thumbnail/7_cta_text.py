"""
📢 CTA Text
"""


def draw_cta(draw, w, cta="Follow @sawajstudio", y=1780):
    draw.text(((w - 300) // 2, y), cta, fill=(255, 230, 180))
