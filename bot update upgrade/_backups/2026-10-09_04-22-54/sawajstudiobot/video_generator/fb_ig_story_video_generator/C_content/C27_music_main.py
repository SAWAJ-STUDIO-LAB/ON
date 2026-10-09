"""C27_music_main.py — Sirf music main."""
import os
from A_core.A9_log_step import log_step
from C_content.C22_music_freesound import fetch as fs_fetch
from C_content.C23_music_pixabay import fetch as px_fetch
from C_content.C24_music_bensound import fetch as bs_fetch
from C_content.C25_music_process import process
from C_content.C26_music_sine import generate


def get(base, outfile="music_soft.mp3"):
    log_step("C27_music_main.py", "get()", "ok")
    if os.environ.get("FREESOUND_API_KEY") and fs_fetch(base, outfile):
        process(base, "music_raw.mp3", outfile)
        return outfile
    if px_fetch(base):
        process(base, "music_raw.mp3", outfile)
        return outfile
    if bs_fetch(base):
        process(base, "music_raw.mp3", outfile)
        return outfile
    generate(base, outfile)
    return outfile
