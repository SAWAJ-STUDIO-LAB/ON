"""
🎨 Gradient Fallback
"""
import random
import subprocess


def generate_gradient(outfile, duration=60, width=1080, height=1920):
    try:
        c0 = "%02x%02x%02x" % (random.randint(10,30), random.randint(8,25), random.randint(25,55))
        c1 = "%02x%02x%02x" % (random.randint(10,30), random.randint(8,25), random.randint(25,55))
        cmd = ('ffmpeg -y -f lavfi -i "gradients=s=' + str(width) + 'x' + str(height) + ':'
               'c0=0x' + c0 + ':c1=0x' + c1 + ':speed=0.006" '
               '-t ' + str(duration) + ' -c:v libx264 -preset veryfast "' + outfile + '"')
        subprocess.run(cmd, shell=True, check=True, timeout=180)
        return True
    except Exception:
        return False
