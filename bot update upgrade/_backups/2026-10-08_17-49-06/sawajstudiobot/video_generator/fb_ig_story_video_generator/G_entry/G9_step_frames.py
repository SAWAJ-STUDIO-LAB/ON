"""G9_step_frames.py — Sirf frames."""
from D_video.D15_frames_generate import generate


def run(voice_dur, has_logo, hindi, urdu, english, hadith_label):
    return generate(voice_dur, has_logo, hindi, urdu, english,
                    hadith_label, "s_frames")
