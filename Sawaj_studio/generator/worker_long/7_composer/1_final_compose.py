"""
🎞️ Final Compose
"""
import os
import subprocess


def compose(bg, frames_dir, voice, total,
            outfile="output/long/final/Final_Long.mp4"):
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    cmd = ('ffmpeg -y -i ' + bg + ' -framerate 25 '
           '-i ' + frames_dir + '/frame_%05d.png '
           '-i ' + voice + ' '
           '-filter_complex "[0:v]scale=1920:1080,setsar=1[bgv];'
           '[bgv][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]" '
           '-map "[outv]" -map 2:a '
           '-c:v libx264 -preset medium -crf 20 -b:v 4M '
           '-c:a aac -b:a 192k -t ' + str(total) + ' '
           '-movflags +faststart ' + outfile)
    subprocess.run(cmd, shell=True, check=True, timeout=2400)
    return outfile
