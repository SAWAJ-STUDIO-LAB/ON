"""B40_ember_single.py — Sirf single ember."""
BASE_COLOR = (255, 140, 60)
GLOW_COLOR = (255, 180, 100)


def draw_single(draw, x, y, size, alpha):
    gs = size * 3
    ga = alpha // 4
    draw.ellipse([x-gs, y-gs, x+gs, y+gs], fill=(*GLOW_COLOR, ga))
    ms = size * 2
    ma = alpha // 2
    draw.ellipse([x-ms, y-ms, x+ms, y+ms], fill=(*GLOW_COLOR, ma))
    draw.ellipse([x-size, y-size, x+size, y+size], fill=(*BASE_COLOR, alpha))
