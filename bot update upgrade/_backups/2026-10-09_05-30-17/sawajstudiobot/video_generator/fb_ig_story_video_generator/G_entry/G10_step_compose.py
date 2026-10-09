"""G10_step_compose.py — Sirf compose."""
from D_video.D28_compose_main import compose


def run(base, bg_file, total):
    return compose(base, bg_file, "s_frames", "s_voice.mp3", total,
                   "output/final/Final_Story.mp4")
