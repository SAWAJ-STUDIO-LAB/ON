# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C7_logo_processor.py                      ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C7_logo_processor.py            ║
# ║  🎯 PURPOSE:   Process logo → avatar with border + glow  ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🖼️  LOGO PROCESSOR MODULE (LONG)                       ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Logo.png → avatar.png (gold border + glow)          ║
║      Landscape optimized for 16:9 long video.            ║
║                                                          ║
║   📁 Logo locations (in order):                          ║
║      • ./logo.png                                        ║
║      • ./assets/logo.png                                 ║
║      • ../../video_requirement/logo.png                  ║
║      • ../../../video_requirement/logo.png               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from PIL import Image, ImageDraw, ImageFilter
from A_core.A2_logger import log_file_start, log_file_end, log_step


class LogoProcessor:
    """Load logo.png and add gold border + glow (Long version)."""

    def __init__(self):
        log_file_start("C7_logo_processor.py", "Logo processing")
        log_file_end("C7_logo_processor.py", "success", "Ready")

    def make(self, outfile="avatar.png"):
        """Load logo and add gold border + glow."""
        log_step("C7_logo_processor.py", "make() starting", "ok")

        for src in ["logo.png", "logo.jpg",
                    "assets/logo.png", "assets/logo.jpg",
                    "../../video_requirement/logo.png",
                    "../../../video_requirement/logo.png"]:
            if os.path.exists(src):
                try:
                    log_step("C7_logo_processor.py", f"Found {src}", "ok")
                    img = Image.open(src).convert("RGBA")

                    # Landscape: wider max width
                    if img.width > 600:
                        ratio = 600 / img.width
                        img = img.resize(
                            (600, int(img.height * ratio)),
                            Image.Resampling.LANCZOS)

                    border, bottom = 14, 30
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

                    canvas.paste(img, (border, border), img)

                    # Glow
                    glow = canvas.filter(ImageFilter.GaussianBlur(6))
                    final = Image.alpha_composite(glow, canvas)
                    final.save(outfile)
                    log_step("C7_logo_processor.py", f"Saved {outfile}", "ok")
                    return True
                except Exception as e:
                    log_step("C7_logo_processor.py", f"Err {src}", "fail", str(e)[:60])

        log_step("C7_logo_processor.py", "No logo found", "fail")
        return False
