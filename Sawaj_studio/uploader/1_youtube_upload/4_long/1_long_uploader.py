"""
📺 YouTube Long Uploader
"""


def upload_long(video_path, title="", description="", tags=None,
                chapters=None):
    try:
        from googleapiclient.http import MediaFileUpload
        from ..2_client.1_client_builder import build_client
        yt = build_client()
        if not yt:
            return False
        if chapters:
            description += "\n\n⏱️ Timestamps:\n" + "\n".join(chapters)
        body = {
            "snippet": {
                "title": title[:100], "description": description,
                "tags": tags or ["Hadith", "Long Hadith", "Islamic"],
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
