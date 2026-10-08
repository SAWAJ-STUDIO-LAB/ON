"""
🔐 Facebook Auth
"""
import os


def get_fb_credentials():
    token = (os.environ.get("FACEBOOK_META_TOKEN", "").strip() or
             os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip())
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    return token, page_id


def has_fb_credentials():
    token, page_id = get_fb_credentials()
    return bool(token and page_id)
