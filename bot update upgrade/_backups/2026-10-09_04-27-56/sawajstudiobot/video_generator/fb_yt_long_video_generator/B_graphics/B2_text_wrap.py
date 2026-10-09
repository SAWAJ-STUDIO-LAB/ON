# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B2_text_wrap.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B2_text_wrap.py                ║
# ║  🎯 PURPOSE:   Multi-lingual line wrapping for Canvas    ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📏 TEXT WRAPPING MODULE                                ║
║   ══════════════════════                                 ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Long texts (Hindi, Arabic, English) ko max pixel    ║
║      width ke hisab se multiple lines mein todna.        ║
╚══════════════════════════════════════════════════════════╝
"""

from PIL import ImageFont


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
    """Wraps text into multiple lines fitting inside max_width pixels."""
    if not text:
        return []

    words = text.split(" ")
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        # Use getbbox for modern Pillow versions
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                # Word itself is wider than max_width
                lines.append(word)
                current_line = []

    if current_line:
        lines.append(" ".join(current_line))

    return lines
