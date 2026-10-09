"""C32_bg_gradient.py — Sirf gradient."""
import random
from C_content.C28_bg_scale_filter import TARGET_W, TARGET_H


def generate(base, duration, outfile):
    c0 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
    c1 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
    cmd = (f'ffmpeg -y -f lavfi -i "gradients=s={TARGET_W}x{TARGET_H}:'
           f'c0=0x{c0}:c1=0x{c1}:speed=0.006" '
           f'-t {duration:.2f} -c:v libx264 -preset veryfast -crf 20 "{outfile}"')
    base.run_cmd(cmd)
