# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C7_logo_processor.py                      ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C7_logo_processor.py            ║
# ║  ✅ FIXED:     Robust logo path search (all levels)      ║
# ╚══════════════════════════════════════════════════════════╝

import os
from PIL import Image, ImageDraw, ImageFilter
from A_core.A2_logger import log_file_start, log_file_end, log_step


class LogoProcessor:
    """Load logo.png and add gold border + glow."""

    # Search order — most specific to least
    LOGO_CANDIDATES = [
        "logo.png",
        "logo.jpg",
        "assets/logo.png",
        "assets/logo.jpg",
        "../logo.png",
        "../assets/logo.png",
        "../../logo.png",
        "../../assets/logo.png",
        "../../video_requirement/logo.png",
        "../../../video_requirement/logo.png",
        "../../../../video_requirement/logo.png",
        os.path.expanduser("~/logo.png"),
    ]

    def __init__(self):
        log_file_start("C7_logo_processor.py", "Logo processing")
        log_file_end("C7_logo_processor.py", "success", "Ready")

    def _find_logo(self):
        """Search all candidates and return the first one that exists."""
        for src in self.LOGO_CANDIDATES:
            if os.path.exists(src):
                return src
        return None

    def make(self, outfile="avatar.png"):
        """Load logo and add gold border + glow."""
        log_step("C7_logo_processor.py", "make() starting", "ok")

        src = self._find_logo()
        if not src:
            log_step("C7_logo_processor.py",
                     "No logo found anywhere", "fail")
            return False

        try:
            log_step("C7_logo_processor.py", f"Found {src}", "ok")
            img = Image.open(src).convert("RGBA")

            # Resize if too big
            if img.width > 400:
                ratio = 400 / img.width
                img = img.resize(
                    (400, int(img.height * ratio)),
                    Image.Resampling.LANCZOS)

            # Add border + strip
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
            log_step("C7_logo_processor.py", f"Err {src}", "fail",
                     str(e)[:80])
            return False
