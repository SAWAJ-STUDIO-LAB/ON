"""C35_logo_make.py — Sirf logo make."""
import os
from PIL import Image, ImageDraw, ImageFilter
from A_core.A9_log_step import log_step


def make(outfile="avatar.png"):
    log_step("C35_logo_make.py", "make()", "ok")
    for src in ["logo.png", "logo.jpg", "assets/logo.png", "assets/logo.jpg",
                "../../video_requirement/logo.png"]:
        if os.path.exists(src):
            try:
                img = Image.open(src).convert("RGBA")
                if img.width > 400:
                    ratio = 400 / img.width
                    img = img.resize((400, int(img.height * ratio)),
                                     Image.Resampling.LANCZOS)
                border, bottom = 12, 26
                nw = img.width + border * 2
                nh = img.height + border + bottom
                canvas = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
                draw = ImageDraw.Draw(canvas)
                draw.rectangle([0, 0, nw-1, nh-1], outline=(212, 175, 55, 255), width=border)
                draw.rectangle([border, border, nw-border-1, nh-bottom-1],
                               outline=(255, 215, 100, 200), width=2)
                draw.rectangle([0, nh-bottom, nw-1, nh-1], fill=(20, 15, 8, 245))
                canvas.paste(img, (border, border), img)
                glow = canvas.filter(ImageFilter.GaussianBlur(6))
                final = Image.alpha_composite(glow, canvas)
                final.save(outfile)
                log_step("C35_logo_make.py", f"Saved {outfile}", "ok")
                return True
            except Exception as e:
                log_step("C35_logo_make.py", f"err {src}", "fail", str(e)[:50])
    log_step("C35_logo_make.py", "No logo", "fail")
    return False
