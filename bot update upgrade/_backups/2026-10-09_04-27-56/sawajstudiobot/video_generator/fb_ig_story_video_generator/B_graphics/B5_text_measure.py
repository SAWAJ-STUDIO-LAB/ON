"""B5_text_measure.py — Sirf text measure."""


def measure(draw, text, font):
    if not text:
        return 0, 0, 0, 0
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox[0], bbox[1]
    except AttributeError:
        w, h = draw.textsize(text, font=font)
        return w, h, 0, 0
