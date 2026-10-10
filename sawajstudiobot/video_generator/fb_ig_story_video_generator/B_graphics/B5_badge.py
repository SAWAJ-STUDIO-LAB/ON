# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B5_badge.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B5_badge.py                    ║
# ║  🎯 PURPOSE:   Hadith number badge draw (top-left)       ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🏷️  HADITH BADGE MODULE                                ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Top-left corner mein hadith number badge           ║
║                                                          ║
║   📖 Example:                                            ║
║      ┌───────────────────────────┐                       ║
║      │ #341 · Sahih al-Bukhari   │                       ║
║      └───────────────────────────┘                       ║
║                                                          ║
║   🎨 Design:                                             ║
║      • Gold border                                       ║
║      • Dark background (200 alpha)                       ║
║      • Rounded corners                                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from B_graphics.B1_fonts import FontLoader


# ═══════════════════════════════════════════════════════════
# 🏷️  DRAW BADGE
# ═══════════════════════════════════════════════════════════

def draw_badge(draw, text, y=180):
    """
    Draw gold badge with text at top-left.

    Args:
        draw: PIL ImageDraw object
        text: badge text (e.g. "#341 · Sahih al-Bukhari")
        y:    vertical position (default 180)
    """
    if not text:
        return

    # ───────── Load font ─────────
    fnt = FontLoader.load(26, "latin", bold=True)

    # ───────── Calculate size ─────────
    bbox = draw.textbbox((0, 0), text, font=fnt)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    pad = 12

    # ───────── Corner coordinates ─────────
    x1, y1 = 60, y
    x2, y2 = x1 + w + pad * 2, y1 + h + pad

    # ───────── Background (rounded rect) ─────────
    draw.rounded_rectangle(
        [x1, y1, x2, y2],
        radius=8,
        fill=(20, 15, 8, 200),
        outline=(212, 175, 55, 220),
        width=2
    )

    # ───────── Text ─────────
    draw.text(
        (x1 + pad, y1 + pad // 2),
        text,
        fill=(230, 200, 130, 255),
        font=fnt
    )
