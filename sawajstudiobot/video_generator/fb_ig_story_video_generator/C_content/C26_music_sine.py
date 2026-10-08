"""C26_music_sine.py — Sirf sine."""
from C_content.C21_music_constants import MUSIC_DUR


def generate(base, outfile):
    cmd = (f'ffmpeg -y '
           f'-f lavfi -i "sine=frequency=110:duration={MUSIC_DUR}" '
           f'-f lavfi -i "sine=frequency=165:duration={MUSIC_DUR}" '
           f'-filter_complex "[0:a][1:a]amix=inputs=2:duration=longest,'
           f'volume=0.12,afade=t=in:st=0:d=2.5,'
           f'afade=t=out:st={MUSIC_DUR-10}:d=6" '
           f'"{outfile}"')
    base.run_cmd(cmd)
