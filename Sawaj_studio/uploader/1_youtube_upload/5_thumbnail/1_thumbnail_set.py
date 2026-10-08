"""
🖼️ YouTube Thumbnail Set
"""


def set_thumbnail(video_id, image_path):
    try:
        from ..2_client.1_client_builder import build_client
        yt = build_client()
        if not yt:
            return False
        yt.thumbnails().set(videoId=video_id,
                            media_body=image_path).execute()
        return True
    except Exception:
        return False
