"""B43_vignette_radial.py — Sirf radial."""
import math
from PIL import Image


def apply_radial_vignette(img, t=0.0, intensity=0.6):
    pulse = 0.1 * math.sin(t * 0.8)
    ai = max(0.0, min(1.0, intensity + pulse))
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    px = mask.load()
    cx, cy = w / 2, h / 2
    md = math.sqrt(cx**2 + cy**2)
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2) / md
            if dist < 0.4:
                v = 0
            elif dist > 0.9:
                v = int(255 * ai)
            else:
                tn = (dist - 0.4) / 0.5
                ts = tn * tn * (3 - 2 * tn)
                v = int(255 * ai * ts)
            for dy in range(4):
                for dx in range(4):
                    if y + dy < h and x + dx < w:
                        px[x + dx, y + dy] = v
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    black.putalpha(mask)
    return Image.alpha_composite(img.convert("RGBA"), black)
