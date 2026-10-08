"""
🔐 Instagram Auth
"""
import os


def get_ig_credentials():
    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    return token, ig_id


def has_ig_credentials():
    token, ig_id = get_ig_credentials()
    return bool(token and ig_id)
