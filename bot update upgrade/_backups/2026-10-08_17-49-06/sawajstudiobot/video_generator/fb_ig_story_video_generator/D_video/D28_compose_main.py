"""D28_compose_main.py — Sirf compose."""
import os
import subprocess
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error


def compose(base, bg, frames_dir, voice, total,
            outfile="output/final/Final_Story.mp4"):
    log_step("D28_compose_main.py", f"compose({total:.1f}s)", "ok")
    if not os.path.exists(bg):
        raise FileNotFoundError(f"BG not found: {bg}")
    if not os.path.exists(voice):
        raise FileNotFoundError(f"Voice not found: {voice}")
    if not os.path.isdir(frames_dir):
        raise FileNotFoundError(f"Frames not found: {frames_dir}")
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    cmd = (f'ffmpeg -y -i "{bg}" -framerate 25 -i "{frames_dir}/frame_%05d.png" '
           f'-i "{voice}" -filter_complex '
           f'"[0:v][1:v]overlay=0:0:shortest=1,'
           f'eq=contrast=1.08:brightness=0.02:saturation=1.12,'
           f'vignette=PI/6,format=yuv420p[outv]" '
           f'-map "[outv]" -map 2:a '
           f'-c:v libx264 -preset veryfast -crf 20 -b:v 4M '
           f'-c:a aac -b:a 192k -t {total:.2f} '
           f'-movflags +faststart "{outfile}"')
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True,
                       text=True, timeout=1800)
    except subprocess.CalledProcessError as e:
        log_error("D28_compose_main.py", f"FFmpeg: {e.stderr[:200]}")
        raise
    size_mb = os.path.getsize(outfile) / 1024 / 1024
    log_step("D28_compose_main.py", "Video ready", "ok", f"{size_mb:.1f} MB")
    return outfile
