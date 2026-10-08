"""
🎵 Generated Sine
"""
import subprocess


def generate_sine(outfile, duration=60):
    try:
        cmd = ('ffmpeg -y -f lavfi -i "sine=frequency=110:duration=' + str(duration) + '" '
               '-f lavfi -i "sine=frequency=165:duration=' + str(duration) + '" '
               '-filter_complex "[0:a][1:a]amix=inputs=2:duration=longest,'
               'volume=0.12,afade=t=in:st=0:d=2.5,'
               'afade=t=out:st=' + str(duration - 10) + ':d=6" ' + outfile)
        subprocess.run(cmd, shell=True, check=True, timeout=120)
        return True
    except Exception:
        return False
