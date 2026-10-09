"""E2_sfx_whoosh.py — Sirf whoosh."""


def whoosh_cmd(outfile="whoosh.mp3"):
    return (f'ffmpeg -y -f lavfi -i "anoisesrc=d=0.5:c=pink:a=0.5" '
            f'-af "afade=t=in:d=0.1,afade=t=out:st=0.3:d=0.2,volume=0.3" '
            f'{outfile}')
