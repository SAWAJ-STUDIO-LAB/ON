"""yt_long_upload.py"""
from googleapiclient.http import MediaFileUpload


def upload_video(yt, video_path, title, description, tags):
    body = {"snippet": {"title": title[:100], "description": description,
                        "tags": tags or ["Hadith"], "categoryId": "22"},
            "status": {"privacyStatus": "public",
                       "selfDeclaredMadeForKids": False}}
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(video_path, chunksize=-1,
                                                        resumable=True,
                                                        mimetype="video/mp4"))
    response = None
    while response is None:
        _, response = req.next_chunk()
    return response.get("id")
