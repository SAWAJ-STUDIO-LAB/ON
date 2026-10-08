"""ig_short_main.py"""
import os
from sawajstudiobot.video_uploader.instagram.ig_short_container import create
from sawajstudiobot.video_uploader.instagram.ig_short_poll import wait
from sawajstudiobot.video_uploader.instagram.ig_short_publish import publish


def upload(video_path, caption="", direct_url=None):
    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    if not token or not ig_id or not direct_url:
        return False
    cont = create(ig_id, token, direct_url, caption)
    cid = cont.get("id")
    if not cid:
        return False
    if not wait(cid, token):
        return False
    return publish(ig_id, token, cid)
