"""G14_step_cleanup.py — Sirf cleanup."""
from A_core.A31_cleanup import cleanup


def run():
    cleanup(
        ["s_raw.mp3", "s_v.mp3", "s_voice.mp3", "tmp.mp4",
         "tmp_bg.mp4", "music_raw.mp3", "music_soft.mp3"],
        folder="s_frames")
