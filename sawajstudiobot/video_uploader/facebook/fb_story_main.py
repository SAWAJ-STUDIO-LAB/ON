"""fb_story_main.py"""
import os
from sawajstudiobot.video_uploader.facebook.fb_story_start import start
from sawajstudiobot.video_uploader.facebook.fb_story_upload import upload_bytes
from sawajstudiobot.video_uploader.facebook.fb_story_finish import finish


def upload(video_path):
    token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    if not token or not page_id:
        return False
    size = os.path.getsize(video_path)
    v_id, v_url = start(page_id, token, size)
    if not v_id or not v_url:
        return False
    up = upload_bytes(v_url, token, size, video_path)
    if up.status_code not in (200, 201):
        return False
    return finish(page_id, token, v_id)
