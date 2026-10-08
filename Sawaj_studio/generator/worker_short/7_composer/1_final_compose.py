"""
🎞️ Final Compose
"""
import os
import subprocess


def compose(bg, frames_dir, voice, total,
            outfile="output/short/final/Final_Short.mp4"):
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    cmd = ('ffmpeg -y -i ' + bg + ' -framerate 25 '
           '-i ' + frames_dir + '/frame_%05d.png '
           '-i ' + voice + ' '
           '-filter_complex "[0:v][1:v]overlay=0:0:shortest=1,'
           'format=yuv420p[outv]" '
           '-map "[outv]" -map 2:a '
           '-c:v libx264 -preset veryfast -crf 18 -b:v 6M '
           '-c:a aac -b:a 192k -t ' + str(total) + ' '
           '-movflags +faststart ' + outfile)
    subprocess.run(cmd, shell=True, check=True, timeout=1800)
    return outfile
