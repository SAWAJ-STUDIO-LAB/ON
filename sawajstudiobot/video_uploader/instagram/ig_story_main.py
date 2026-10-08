"""ig_story_main.py"""
import os
from sawajstudiobot.video_uploader.instagram.ig_story_container import create
from sawajstudiobot.video_uploader.instagram.ig_story_upload import upload_bytes
from sawajstudiobot.video_uploader.instagram.ig_story_poll import wait
from sawajstudiobot.video_uploader.instagram.ig_story_publish import publish


def upload(video_path):
    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    if not token or not ig_id:
        return False
    cont = create(ig_id, token)
    c_id = cont.get("id")
    if not c_id:
        return False
    size = os.path.getsize(video_path)
    upload_bytes(c_id, token, size, video_path)
    if not wait(c_id, token):
        return False
    return publish(ig_id, token, c_id)
