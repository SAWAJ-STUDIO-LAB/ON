"""yt_short_main.py"""
import os
from sawajstudiobot.video_uploader.youtube.yt_auth import get_service
from sawajstudiobot.video_uploader.youtube.yt_short_upload import upload_video
from sawajstudiobot.video_uploader.youtube.yt_short_playlist import add


def upload(video_path, title="", description="", tags=None):
    yt = get_service()
    vid = upload_video(yt, video_path, title, description, tags)
    if vid:
        pl = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID")
        if pl:
            add(yt, vid, pl)
        return True
    return False
