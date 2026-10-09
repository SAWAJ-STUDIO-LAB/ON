"""C25_music_process.py — Sirf processing."""
import os
from C_content.C21_music_constants import MUSIC_VOL, MUSIC_DUR


def process(base, infile, outfile):
    fade_out_start = MUSIC_DUR - 5
    cmd = (f'ffmpeg -y -stream_loop -1 -i "{infile}" '
           f'-af "volume={MUSIC_VOL},'
           f'afade=t=in:st=0:d=2,'
           f'afade=t=out:st={fade_out_start}:d=5" '
           f'-t {MUSIC_DUR} "{outfile}"')
    base.run_cmd(cmd)
    try:
        if os.path.exists(infile) and infile != outfile:
            os.remove(infile)
    except Exception:
        pass
