"""E1_duck_mix.py — Sirf mix."""
from A_core.A9_log_step import log_step


def mix(base, voice_file, music_file, out_file, voice_dur, music_vol=0.20):
    log_step("E1_duck_mix.py", "mix()", "ok")
    fade = max(voice_dur - 3.0, 1.0)
    base.run_cmd(
        f'ffmpeg -y -i {voice_file} -i {music_file} '
        f'-filter_complex '
        f'"[1:a]volume={music_vol},afade=t=in:st=0:d=2,'
        f'afade=t=out:st={fade:.2f}:d=3[bg];'
        f'[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]" '
        f'-map "[aout]" -c:a libmp3lame -b:a 192k {out_file}')
    return out_file
