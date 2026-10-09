# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C7_logo_processor.py                      ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C7_logo_processor.py            ║
# ║  🎯 PURPOSE:   Process logo → avatar with border + glow  ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🖼️  LOGO PROCESSOR MODULE                              ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Logo.png ko avatar.png mein convert karna           ║
║      (gold border + glow + bottom strip)                 ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Try logo.png from various locations              ║
║      2. Resize to 400px width                            ║
║      3. Add gold border (12px)                           ║
║      4. Add bottom strip (26px)                          ║
║      5. Add glow effect                                  ║
║      6. Save as avatar.png                               ║
║                                                          ║
║   📁 Logo locations (in order):                          ║
║      • ./logo.png                                        ║
║      • ./assets/logo.png                                 ║
║      • ../../video_requirement/logo.png                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image, ImageDraw, ImageFilter
from A_core.A2_logger import log_file_start, log_file_end, log_step


# ═══════════════════════════════════════════════════════════
# 🖼️  LOGO PROCESSOR CLASS
# ═══════════════════════════════════════════════════════════

class LogoProcessor:
    """Load logo.png and add gold border + glow."""

    # ─────────────────────────────────────────────────────
    # ① INIT
    # ─────────────────────────────────────────────────────
    def __init__(self):
        log_file_start("C7_logo_processor.py", "Logo processing")
        log_file_end("C7_logo_processor.py", "success", "Ready")

    # ─────────────────────────────────────────────────────
    # ② MAKE — process logo → avatar
    # ─────────────────────────────────────────────────────
    def make(self, outfile="avatar.png"):
        """
        Load logo and add gold border + glow.

        Args:
            outfile: output path (default avatar.png)

        Returns:
            True if successful, False otherwise
        """
        log_step("C7_logo_processor.py", "make() starting", "ok")

        # ═══════════ Try user logo files ═══════════
        for src in ["logo.png", "logo.jpg",
                    "assets/logo.png", "assets/logo.jpg",
                    "../../video_requirement/logo.png"]:
            if os.path.exists(src):
                try:
                    log_step("C7_logo_processor.py", f"Found {src}", "ok")
                    img = Image.open(src).convert("RGBA")

                    # ───────── Resize if too big ─────────
                    if img.width > 400:
                        ratio = 400 / img.width
                        img = img.resize(
                            (400, int(img.height * ratio)),
                            Image.Resampling.LANCZOS)

                    # ───────── Add border + strip ─────────
                    border, bottom = 12, 26
                    nw = img.width + border * 2
                    nh = img.height + border + bottom
                    canvas = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(canvas)

                    # Gold outer border
                    draw.rectangle([0, 0, nw - 1, nh - 1],
                                   outline=(212, 175, 55, 255), width=border)

                    # Inner thin gold line
                    draw.rectangle([border, border,
                                    nw - border - 1, nh - bottom - 1],
                                   outline=(255, 215, 100, 200), width=2)

                    # Bottom dark strip
                    draw.rectangle([0, nh - bottom, nw - 1, nh - 1],
                                   fill=(20, 15, 8, 245))

                    # Paste logo
                    canvas.paste(img, (border, border), img)

                    # Glow effect
                    glow = canvas.filter(ImageFilter.GaussianBlur(6))
                    final = Image.alpha_composite(glow, canvas)
                    final.save(outfile)
                    log_step("C7_logo_processor.py", f"Saved {outfile}", "ok")
                    return True
                except Exception as e:
                    log_step("C7_logo_processor.py", f"Err {src}", "fail", str(e)[:60])

        # ═══════════ Fallback: no logo found ═══════════
        log_step("C7_logo_processor.py", "No logo found", "fail")
        return False
