# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C8_thumbnail.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                C_content/C8_thumbnail.py                 ║
# ║  🎯 PURPOSE:   Auto thumbnail generator                  ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🖼️  THUMBNAIL MODULE                                   ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Video ke liye thumbnail JPG banana                  ║
║                                                          ║
║   📐 Size:                                                ║
║      1080 x 1920 (9:16 vertical)                         ║
║                                                          ║
║   🎨 Elements:                                            ║
║      • Gradient background                               ║
║      • Gold border (outer + inner)                       ║
║      • Hadith label (top)                                ║
║      • "HADITH" (big title)                              ║
║      • "SHORTS" (subtitle — Short specific)              ║
║      • 3-language bullets                                ║
║      • Follow @sawajstudio (bottom)                      ║
║      • Avatar/logo (bottom center)                       ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      Subtitle: "SHORTS" (Story: "OF THE DAY")            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image, ImageDraw
from A_core.A2_logger import log_file_start, log_file_end, log_step
from B_graphics.B1_fonts import FontLoader


class Thumbnail:
    """Generate thumbnail JPG (Short version)."""

    def __init__(self, base):
        log_file_start("C8_thumbnail.py", "Thumbnail generator")
        self.base = base
        log_file_end("C8_thumbnail.py", "success", "Ready")

    def make(self, hindi, urdu, english, hadith_label,
             outfile="output/final/thumbnail.jpg"):
        """Generate thumbnail JPG."""
        log_step("C8_thumbnail.py", "make() starting", "ok")
        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        W, H = 1080, 1920
        img = Image.new("RGB", (W, H), (18, 14, 8))
        draw = ImageDraw.Draw(img)

        # ═══════════ Gradient background ═══════════
        for y in range(0, H, 4):
            r = int(18 + 30 * (y / H))
            g = int(14 + 20 * (y / H))
            b = int(8 + 15 * (y / H))
            draw.rectangle([0, y, W, y + 4], fill=(r, g, b))

        # ═══════════ Gold borders ═══════════
        draw.rectangle([20, 20, W - 20, H - 20],
                       outline=(212, 175, 55), width=6)
        draw.rectangle([30, 30, W - 30, H - 30],
                       outline=(255, 215, 100), width=2)

        # ═══════════ Hadith label (top) ═══════════
        if hadith_label:
            fnt = FontLoader.load(36, "latin", bold=True)
            bbox = draw.textbbox((0, 0), hadith_label, font=fnt)
            w = bbox[2] - bbox[0]
            draw.text(((W - w) // 2, 100), hadith_label,
                      fill=(230, 200, 130), font=fnt)

        # ═══════════ Big title ═══════════
        font_big = FontLoader.load(84, "latin", bold=True)
        title = "HADITH"
        bbox = draw.textbbox((0, 0), title, font=font_big)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) // 2, 300), title,
                  fill=(255, 240, 200), font=font_big)

        # ═══════════ Subtitle (SHORTS) ═══════════
        font_sub = FontLoader.load(56, "latin", bold=True)
        title2 = "SHORTS"
        bbox = draw.textbbox((0, 0), title2, font=font_sub)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) // 2, 420), title2,
                  fill=(230, 200, 130), font=font_sub)

        # ═══════════ 3-Language bullets ═══════════
        y = 780
        gap = 130

        # ───────── Hindi ─────────
        if hindi:
            fnt = FontLoader.load(48, "devanagari", bold=True)
            draw.ellipse([100, y + 20, 130, y + 50], fill=(240, 130, 200))
            draw.text((160, y), hindi[:30],
                      fill=(255, 255, 255), font=fnt)
            y += gap

        # ───────── Urdu ─────────
        if urdu:
            fnt = FontLoader.load(48, "arabic", bold=True)
            draw.ellipse([100, y + 20, 130, y + 50], fill=(90, 170, 255))
            draw.text((160, y), urdu[:30],
                      fill=(255, 255, 255), font=fnt)
            y += gap

        # ───────── English ─────────
        if english:
            fnt = FontLoader.load(44, "latin", bold=True)
            draw.ellipse([100, y + 20, 130, y + 50], fill=(255, 110, 110))
            words = english.split()
            lines = []
            cur = ""
            for w in words:
                test = (cur + " " + w).strip()
                bb = draw.textbbox((0, 0), test, font=fnt)
                if bb[2] - bb[0] < 850:
                    cur = test
                else:
                    if cur:
                        lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)
            for i, line in enumerate(lines[:3]):
                draw.text((160, y + i * 60), line,
                          fill=(255, 255, 255), font=fnt)

        # ═══════════ Bottom CTA ═══════════
        font_cta = FontLoader.load(40, "latin", bold=True)
        cta = "Follow @sawajstudio"
        bbox = draw.textbbox((0, 0), cta, font=font_cta)
        w = bbox[2] - bbox[0]
        draw.text(((W - w) // 2, 1780), cta,
                  fill=(255, 230, 180), font=font_cta)

        # ═══════════ Logo overlay ═══════════
        if os.path.exists("avatar.png"):
            try:
                logo = Image.open("avatar.png").convert("RGBA").resize(
                    (260, 110), Image.Resampling.LANCZOS)
                img.paste(logo, ((W - 260) // 2, 1580), logo)
            except Exception:
                pass

        # ═══════════ Save ═══════════
        img.save(outfile, "JPEG", quality=92)
        log_step("C8_thumbnail.py", f"Saved {outfile}", "ok",
                 f"{os.path.getsize(outfile)//1024} KB")
        return outfile
