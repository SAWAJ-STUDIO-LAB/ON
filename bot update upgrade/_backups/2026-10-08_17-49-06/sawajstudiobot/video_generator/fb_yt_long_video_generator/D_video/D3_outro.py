# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D3_outro.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                D_video/D3_outro.py                       ║
# ║  🎯 PURPOSE:   Outro frames (JazakAllah + CTA)           ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 OUTRO MODULE (LONG)                                 ║
║   ═══════════════════════                                ║
║                                                          ║
║   ⏱️  Duration: 3 seconds                                 ║
║                                                          ║
║   🎨 Elements (16:9 landscape 1920x1080):                ║
║      • "JazakAllah Khair" big gold                       ║
║      • LIKE / SUBSCRIBE / SHARE buttons                  ║
║      • "Follow @sawajstudio"                             ║
║      • Logo center                                       ║
║      • Sparkles                                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image
from B_graphics.B1_fonts import FontManager
from B_graphics.B3_sparkles import draw_sparkles


def _draw_centered(draw, text, y, font, fill, W=1920, shadow=True):
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    if shadow:
        draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 220), font=font)
    draw.text((x, y), text, fill=fill, font=font)


def draw_outro(img, draw, t, outro_dur, has_logo):
    """Draw outro frame (16:9 landscape)."""
    alpha = min(1.0, t / 0.7)
    W, H = 1920, 1080
    C_GOLD = (230, 200, 130)

    font_outro = FontManager.get_font(None, 96)
    font_cta = FontManager.get_font(None, 44)
    font_follow = FontManager.get_font(None, 56)

    # ═══════════ JazakAllah big ═══════════
    _draw_centered(draw, "JazakAllah Khair", 300, font_outro,
                   (*C_GOLD, int(255 * alpha)), W)

    # ═══════════ CTA buttons ═══════════
    if alpha > 0.4:
        cta_y = 520
        cta_items = [("LIKE", 500), ("SUBSCRIBE", 850), ("SHARE", 1250)]
        for label, x in cta_items:
            draw.text((x, cta_y), label,
                      fill=(255, 240, 200, int(255 * alpha)),
                      font=font_cta)

    # ═══════════ Follow ═══════════
    if alpha > 0.6:
        _draw_centered(draw, "Follow @sawajstudio", 680, font_follow,
                       (220, 190, 130, int(255 * alpha)), W)

    # ═══════════ Logo center ═══════════
    if has_logo:
        try:
            logo = Image.open("avatar.png").convert("RGBA")
            logo.thumbnail((340, 340))
            lx = (W - logo.width) // 2
            img.paste(logo, (lx, 780), logo)
        except Exception:
            pass

    # ═══════════ Sparkles ═══════════
    draw_sparkles(draw, t)
