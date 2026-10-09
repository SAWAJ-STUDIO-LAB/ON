# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D3_outro.py                               ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                D_video/D3_outro.py                       ║
# ║  🎯 PURPOSE:   Outro frames (JazakAllah + CTA)           ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 OUTRO MODULE (SHORT)                                ║
║   ═══════════════════                                    ║
║                                                          ║
║   ⏱️  Duration: 2 seconds                                 ║
║                                                          ║
║   🎨 Elements:                                            ║
║      • "JazakAllah Khair" (big gold)                     ║
║      • LIKE / SUBSCRIBE / SHARE buttons                  ║
║      • "Follow @sawajstudio"                             ║
║      • Logo (center)                                     ║
║      • Sparkles                                          ║
║                                                          ║
║   📝 Note:                                                ║
║      Same as Story — same code                           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image
from B_graphics.B1_fonts import FontLoader
from B_graphics.B2_text_wrap import draw_centered
from B_graphics.B3_sparkles import draw_sparkles


def draw_outro(img, draw, t, outro_dur, has_logo):
    """Draw outro frame at time t."""
    alpha = min(1.0, t / 0.5)

    # ═══════════ Load fonts ═══════════
    font_outro = FontLoader.load(72, "latin", bold=True)
    font_cta = FontLoader.load(36, "latin", bold=True)
    font_follow = FontLoader.load(44, "latin", bold=True)

    C_GOLD = (230, 200, 130)

    # ═══════════ JazakAllah (big text) ═══════════
    draw_centered(draw, "JazakAllah Khair", 780, font_outro,
                  (*C_GOLD, int(255 * alpha)))

    # ═══════════ CTA row ═══════════
    if alpha > 0.4:
        cta_y = 960
        cta_items = [
            ("LIKE", 200),
            ("SUBSCRIBE", 460),
            ("SHARE", 760),
        ]
        for label, x in cta_items:
            draw.text((x, cta_y), label,
                      fill=(255, 240, 200, int(255 * alpha)),
                      font=font_cta)

    # ═══════════ Follow text ═══════════
    if alpha > 0.6:
        draw_centered(draw, "Follow @sawajstudio", 1120, font_follow,
                      (220, 190, 130, int(255 * alpha)))

    # ═══════════ Logo (center) ═══════════
    if has_logo:
        try:
            logo = Image.open("avatar.png").convert("RGBA").resize(
                (260, 110), Image.Resampling.LANCZOS)
            img.paste(logo, ((1080 - 260) // 2, 1260), logo)
        except Exception:
            pass

    # ═══════════ Sparkles ═══════════
    draw_sparkles(draw, t)
