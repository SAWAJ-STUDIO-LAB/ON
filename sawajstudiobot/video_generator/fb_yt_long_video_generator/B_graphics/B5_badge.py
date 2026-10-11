
# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B5_badge.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B5_badge.py                    ║
# ║  ✅ FIXED:     draw_badge(draw, text, y)                 ║
# ╚══════════════════════════════════════════════════════════╝

from B_graphics.B1_fonts import FontManager


def draw_badge(draw, text, y=60):
    """Draw gold hadith badge at top-left of frame."""
    if not text:
        return

    fnt = FontManager.get_font(None, 32)

    bbox = draw.textbbox((0, 0), text, font=fnt)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    pad = 16

    x1, y1 = 80, y
    x2, y2 = x1 + w + pad * 2, y1 + h + pad

    draw.rounded_rectangle(
        [x1, y1, x2, y2],
        radius=10,
        fill=(20, 15, 8, 200),
        outline=(212, 175, 55, 220),
        width=2
    )

    draw.text(
        (x1 + pad, y1 + pad // 2),
        text,
        fill=(230, 200, 130, 255),
        font=fnt
    )
