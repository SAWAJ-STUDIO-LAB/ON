"""
🖼️ Thumb Draw
"""
from PIL import Image, ImageDraw


def create_thumbnail(hindi, arabic, english, hadith_label, outfile):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), (18, 14, 8))
    draw = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        r = int(18 + 30 * (y / H))
        g = int(14 + 20 * (y / H))
        b = int(8 + 15 * (y / H))
        draw.rectangle([0, y, W, y + 4], fill=(r, g, b))
    draw.rectangle([20, 20, W - 20, H - 20],
                   outline=(212, 175, 55), width=6)
    draw.rectangle([30, 30, W - 30, H - 30],
                   outline=(255, 215, 100), width=2)
    img.save(outfile, "JPEG", quality=92)
    return outfile
