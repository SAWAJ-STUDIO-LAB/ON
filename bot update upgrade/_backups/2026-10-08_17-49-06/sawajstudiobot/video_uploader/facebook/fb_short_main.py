"""fb_short_main.py"""
from sawajstudiobot.video_uploader.facebook.fb_short_upload import upload


def run(video_path, caption=""):
    return upload(video_path, caption)
