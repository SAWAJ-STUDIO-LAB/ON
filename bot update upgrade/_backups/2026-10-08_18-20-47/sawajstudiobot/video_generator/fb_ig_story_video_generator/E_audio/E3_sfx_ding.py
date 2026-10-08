"""E3_sfx_ding.py — Sirf ding."""


def ding_cmd(outfile="ding.mp3"):
    return (f'ffmpeg -y -f lavfi -i "sine=frequency=880:duration=0.5" '
            f'-af "afade=t=out:st=0.2:d=0.3,volume=0.4" {outfile}')
