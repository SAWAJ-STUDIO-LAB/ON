"""
🎵 Volume Mixer
"""
import subprocess


def apply_volume_and_fade(infile, outfile, duration=60,
                          volume=0.20, fade_in=2, fade_out=5):
    try:
        fade_out_start = duration - fade_out
        cmd = ('ffmpeg -y -stream_loop -1 -i "' + infile + '" -af '
               '"volume=' + str(volume) + ','
               'afade=t=in:st=0:d=' + str(fade_in) + ','
               'afade=t=out:st=' + str(fade_out_start) + ':d=' + str(fade_out) + '" '
               '-t ' + str(duration) + ' "' + outfile + '"')
        subprocess.run(cmd, shell=True, check=True, timeout=180)
        return True
    except Exception:
        return False
