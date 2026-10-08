"""B42_vignette_ring.py — Sirf ring band."""


def draw_ring_band(draw, w, h, margin, alpha):
    color = (0, 0, 0, alpha)
    draw.rectangle([0, 0, w, margin], fill=color)
    draw.rectangle([0, h - margin, w, h], fill=color)
    draw.rectangle([0, margin, margin, h - margin], fill=color)
    draw.rectangle([w - margin, margin, w, h - margin], fill=color)
