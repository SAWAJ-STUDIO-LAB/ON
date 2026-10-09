"""C45_thumb_wrap.py — Sirf wrap."""


def wrap(draw_obj, text, font, max_width):
    if not text:
        return []
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip() if current else w
        bbox = draw_obj.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines
