"""B33_watermark_text.py — Sirf text watermark."""
from PIL import ImageDraw


def draw_text(img, text="SAWAJ STUDIO", font=None, pos="bottom-right", opacity=120):
    if not text or font is None:
        return
    try:
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        margin = 40
        if pos == "bottom-right":
            x, y = img.width - tw - margin, img.height - th - margin - 200
        elif pos == "bottom-left":
            x, y = margin, img.height - th - margin - 200
        elif pos == "top-right":
            x, y = img.width - tw - margin, margin
        else:
            x, y = margin, margin
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
    except Exception:
        pass
