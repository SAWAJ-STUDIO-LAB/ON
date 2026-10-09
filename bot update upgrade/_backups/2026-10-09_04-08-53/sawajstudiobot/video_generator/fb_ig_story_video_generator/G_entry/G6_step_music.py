"""G6_step_music.py — Sirf music."""
from C_content.C27_music_main import get
from E_audio.E1_duck_mix import mix


def run(base, voice_dur):
    get(base, "music_soft.mp3")
    mix(base, "s_v.mp3", "music_soft.mp3", "s_voice.mp3", voice_dur)
    return "s_voice.mp3"
