"""
🛠️ YouTube Client Builder
"""
from ..1_auth.1_oauth import get_youtube_client


def build_client():
    try:
        return get_youtube_client()
    except Exception:
        return None
