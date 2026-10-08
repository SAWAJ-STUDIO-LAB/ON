"""
📺 YouTube Short Uploader
"""


def upload_short(video_path, title="", description="", tags=None):
    try:
        from googleapiclient.http import MediaFileUpload
        from ..2_client.1_client_builder import build_client
        yt = build_client()
        if not yt:
            return False
        body = {
            "snippet": {
                "title": title[:100], "description": description,
                "tags": tags or ["Shorts", "Hadith", "Islamic"],
                "categoryId": "22",
            },
            "status": {"privacyStatus": "public",
                       "selfDeclaredMadeForKids": False},
        }
        req = yt.videos().insert(
            part="snippet,status", body=body,
            media_body=MediaFileUpload(video_path, chunksize=-1,
                                       resumable=True,
                                       mimetype="video/mp4"))
        response = None
        while response is None:
            _, response = req.next_chunk()
        return bool(response.get("id"))
    except Exception:
        return False
