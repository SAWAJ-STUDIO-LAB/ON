"""
📝 Text Watermark
"""
from PIL import ImageDraw


def draw_text_watermark(img, text="SAWAJ STUDIO", font=None,
                        pos="bottom-right", opacity=120):
    if not text or font is None:
        return
    try:
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        margin = 40
        if pos == "bottom-right":
            x = img.width - tw - margin
            y = img.height - th - margin - 200
        else:
            x = margin
            y = img.height - th - margin - 200
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
    except Exception:
        pass
