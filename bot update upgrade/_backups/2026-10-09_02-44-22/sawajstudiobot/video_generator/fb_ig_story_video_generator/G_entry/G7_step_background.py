"""G7_step_background.py — Sirf background."""
from C_content.C34_bg_main import get


def run(base, voice_dur):
    return get(base, voice_dur + 4.5)
