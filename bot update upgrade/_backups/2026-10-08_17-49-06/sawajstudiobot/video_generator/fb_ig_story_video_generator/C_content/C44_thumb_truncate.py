"""C44_thumb_truncate.py — Sirf truncate."""


def truncate(draw_obj, text, font, max_width):
    if not text:
        return ""
    bbox = draw_obj.textbbox((0, 0), text, font=font)
    if bbox[2] - bbox[0] <= max_width:
        return text
    for length in range(len(text), 0, -1):
        s = text[:length] + "..."
        bbox = draw_obj.textbbox((0, 0), s, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return s
    return text[:20] + "..."
