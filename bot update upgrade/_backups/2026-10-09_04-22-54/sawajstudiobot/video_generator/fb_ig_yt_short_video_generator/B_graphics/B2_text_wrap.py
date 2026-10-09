# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B2_text_wrap.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B2_text_wrap.py                ║
# ║  🎯 PURPOSE:   Text wrap + center align helpers          ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📝 TEXT WRAP MODULE                                    ║
║   ═════════════════════                                  ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Text wrap + align karna                             ║
║      (Yeh Short ke liye bhi same hai)                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from PIL import ImageDraw


def wrap_text(draw, text, font, max_width=950):
    """Wrap text into lines."""
    if not text:
        return []
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
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


def draw_centered(draw, text, y, font, fill, shadow=True):
    """Draw text centered."""
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (1080 - w) // 2
    if shadow:
        draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 220), font=font)
    draw.text((x, y), text, fill=fill, font=font)
