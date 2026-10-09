# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C8_thumbnail.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C8_thumbnail.py                 ║
# ║  🎯 PURPOSE:   YouTube thumbnail generator (1280x720)    ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🖼️  THUMBNAIL MODULE (LONG)                            ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      YouTube 16:9 thumbnail generator                    ║
║                                                          ║
║   📐 Size:                                                ║
║      1280 x 720 (YouTube standard 16:9)                  ║
║                                                          ║
║   🎨 Elements:                                            ║
║      • Gradient background (dark Islamic tone)           ║
║      • Gold frame border                                 ║
║      • Hadith reference (top-left)                       ║
║      • "HADITH" big title                                ║
║      • Hindi subtitle highlight                          ║
║      • "SAWAJ STUDIO" branding bottom                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image, ImageDraw
from A_core.A2_logger import log_file_start, log_file_end, log_step
from B_graphics.B1_fonts import FontManager


class Thumbnail:
    """Generate YouTube landscape thumbnail."""

    def __init__(self, base):
        log_file_start("C8_thumbnail.py", "Thumbnail generator")
        self.base = base
        log_file_end("C8_thumbnail.py", "success", "Ready")

    def make(self, hindi, urdu, english, hadith_label,
             outfile="output/final/thumbnail.jpg"):
        """Generate YouTube 1280x720 thumbnail."""
        log_step("C8_thumbnail.py", "make() starting", "ok")
        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        W, H = 1280, 720
        img = Image.new("RGB", (W, H), (18, 14, 8))
        draw = ImageDraw.Draw(img)

        # ═══════════ Gradient background ═══════════
        for y in range(0, H, 4):
            r = int(20 + 35 * (y / H))
            g = int(15 + 22 * (y / H))
            b = int(10 + 20 * (y / H))
            draw.rectangle([0, y, W, y + 4], fill=(r, g, b))

        # ═══════════ Gold frame ═══════════
        draw.rectangle([20, 20, W - 20, H - 20],
                       outline=(212, 175, 55), width=6)
        draw.rectangle([32, 32, W - 32, H - 32],
                       outline=(255, 215, 100), width=2)

        # ═══════════ Hadith label (top) ═══════════
        if hadith_label:
            fnt = FontManager.get_font(None, 28)
            bbox = draw.textbbox((0, 0), hadith_label, font=fnt)
            w = bbox[2] - bbox[0]
            draw.text(((W - w) // 2, 60), hadith_label,
                      fill=(230, 200, 130), font=fnt)

        # ═══════════ Big title "HADITH" ═══════════
        font_big = FontManager.get_font(None, 110)
        title = "HADITH"
        bbox = draw.textbbox((0, 0), title, font=font_big)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) // 2, 140), title,
                  fill=(255, 240, 200), font=font_big)

        # ═══════════ Hindi subtitle (highlight) ═══════════
        font_sub = FontManager.get_font(None, 44)
        if hindi:
            sub = hindi.split("।")[0][:60]
            bbox = draw.textbbox((0, 0), sub, font=font_sub)
            w = bbox[2] - bbox[0]
            draw.text(((W - w) // 2, 300), sub,
                      fill=(240, 200, 120), font=font_sub)

        # ═══════════ English first line ═══════════
        if english:
            font_en = FontManager.get_font(None, 30)
            line = english.split(".")[0][:80]
            bbox = draw.textbbox((0, 0), line, font=font_en)
            w = bbox[2] - bbox[0]
            draw.text(((W - w) // 2, 400), line,
                      fill=(200, 200, 200), font=font_en)

        # ═══════════ Bottom CTA ═══════════
        font_cta = FontManager.get_font(None, 32)
        cta = "SAWAJ STUDIO  •  @sawajstudio"
        bbox = draw.textbbox((0, 0), cta, font=font_cta)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) // 2, 620), cta,
                  fill=(255, 230, 180), font=font_cta)

        # ═══════════ Logo overlay ═══════════
        if os.path.exists("avatar.png"):
            try:
                logo = Image.open("avatar.png").convert("RGBA")
                logo.thumbnail((240, 240))
                img.paste(logo, (W - logo.width - 50, 100), logo)
            except Exception:
                pass

        img.save(outfile, "JPEG", quality=92)
        log_step("C8_thumbnail.py", f"Saved {outfile}", "ok",
                 f"{os.path.getsize(outfile)//1024} KB")
        return outfile
