"""fb_long_main.py"""
from sawajstudiobot.video_uploader.facebook.fb_long_upload import upload


def run(video_path, caption=""):
    return upload(video_path, caption)
