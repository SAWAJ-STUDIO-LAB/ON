"""
🖼️ Frame Generator
"""
import os
from PIL import Image, ImageDraw


def generate_frames(voice_dur, has_logo, sections,
                    hadith_label, out_dir="l_frames"):
    os.makedirs(out_dir, exist_ok=True)
    fps = 25
    total = 3.0 + voice_dur + 3.0
    frames_count = int(total * fps)
    for fi in range(frames_count):
        img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        img.save(out_dir + "/frame_" + str(fi).zfill(5) + ".png")
    return total
