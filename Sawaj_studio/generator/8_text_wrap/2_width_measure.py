"""
📐 Width Measure
"""


def measure_text(draw, text, font):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        return 0, 0


def measure_height(draw, text, font):
    _, h = measure_text(draw, text, font)
    return h
