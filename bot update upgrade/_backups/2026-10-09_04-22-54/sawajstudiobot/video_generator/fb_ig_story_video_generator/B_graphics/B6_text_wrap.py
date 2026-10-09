"""B6_text_wrap.py — Sirf text wrap."""


def wrap(draw, text, font, max_width=950):
    if not text:
        return []
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip() if current else w
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines
