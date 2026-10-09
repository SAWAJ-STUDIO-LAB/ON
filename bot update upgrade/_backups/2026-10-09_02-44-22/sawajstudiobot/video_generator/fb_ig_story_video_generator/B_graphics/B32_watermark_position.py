"""B32_watermark_position.py — Sirf position."""


def calc_position(img, size, pos="top-right", margin=30):
    w, h = size
    if pos == "top-right":
        return (img.width - w - margin, 180)
    if pos == "top-left":
        return (margin, 180)
    if pos == "bottom-right":
        return (img.width - w - margin, img.height - h - 250)
    return (margin, img.height - h - 250)
