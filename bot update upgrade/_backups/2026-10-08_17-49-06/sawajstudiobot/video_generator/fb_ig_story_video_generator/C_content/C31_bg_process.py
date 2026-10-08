"""C31_bg_process.py — Sirf bg process."""
import os
from C_content.C28_bg_scale_filter import build


def process(base, infile, outfile, duration):
    cmd = (f'ffmpeg -y -stream_loop -1 -i "{infile}" '
           f'-vf "{build()}" -t {duration:.2f} -an '
           f'-c:v libx264 -preset veryfast -crf 20 "{outfile}"')
    base.run_cmd(cmd)
    try:
        if os.path.exists(infile):
            os.remove(infile)
    except Exception:
        pass
