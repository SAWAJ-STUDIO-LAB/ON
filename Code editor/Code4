"""
Code4 — Uploader code transfer.
"""
import os

BASE = "sawajstudiobot/video_uploader"

FILES = {
    "__init__.py": '"""Uploader package."""\n',

    # ═══ Facebook ═══
    "facebook/__init__.py": '"""FB uploader."""\n',
    "facebook/fb_story_start.py": '''"""fb_story_start.py"""
import requests


def start(page_id, token, file_size):
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
        data={"upload_phase": "start", "file_size": file_size,
              "access_token": token}, timeout=30).json()
    return r.get("video_id"), r.get("upload_url")
''',
    "facebook/fb_story_upload.py": '''"""fb_story_upload.py"""
import requests


def upload_bytes(upload_url, token, file_size, video_path):
    with open(video_path, "rb") as f:
        return requests.post(upload_url,
                             headers={"Authorization": f"OAuth {token}",
                                      "offset": "0",
                                      "file_size": str(file_size)},
                             data=f.read(), timeout=180)
''',
    "facebook/fb_story_finish.py": '''"""fb_story_finish.py"""
import requests


def finish(page_id, token, video_id):
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
        data={"upload_phase": "finish", "video_id": video_id,
              "access_token": token}, timeout=30).json()
    return bool(r.get("success") or r.get("post_id"))
''',
    "facebook/fb_story_main.py": '''"""fb_story_main.py"""
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
''',

    "facebook/fb_short_upload.py": '''"""fb_short_upload.py"""
import os
import requests


def upload(video_path, caption=""):
    token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    if not token or not page_id:
        return False
    with open(video_path, "rb") as f:
        r = requests.post(
            f"https://graph.facebook.com/v21.0/{page_id}/videos",
            data={"access_token": token, "description": caption,
                  "published": "true"},
            files={"source": f}, timeout=1800).json()
    return bool(r.get("id"))
''',
    "facebook/fb_short_main.py": '''"""fb_short_main.py"""
from sawajstudiobot.video_uploader.facebook.fb_short_upload import upload


def run(video_path, caption=""):
    return upload(video_path, caption)
''',

    "facebook/fb_long_upload.py": '''"""fb_long_upload.py"""
import os
import requests


def upload(video_path, caption=""):
    token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    if not token or not page_id:
        return False
    with open(video_path, "rb") as f:
        r = requests.post(
            f"https://graph.facebook.com/v21.0/{page_id}/videos",
            data={"access_token": token, "description": caption,
                  "published": "true"},
            files={"source": f}, timeout=3600).json()
    return bool(r.get("id"))
''',
    "facebook/fb_long_main.py": '''"""fb_long_main.py"""
from sawajstudiobot.video_uploader.facebook.fb_long_upload import upload


def run(video_path, caption=""):
    return upload(video_path, caption)
''',

    # ═══ Instagram ═══
    "instagram/__init__.py": '"""IG uploader."""\n',
    "instagram/ig_story_container.py": '''"""ig_story_container.py"""
import requests


def create(ig_id, token):
    return requests.post(
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        data={"media_type": "STORIES", "upload_type": "resumable",
              "access_token": token}, timeout=40).json()
''',
    "instagram/ig_story_upload.py": '''"""ig_story_upload.py"""
import requests


def upload_bytes(container_id, token, file_size, video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    url = f"https://rupload.facebook.com/ig-api-upload/v21.0/{container_id}"
    return requests.post(url,
                         headers={"Authorization": f"OAuth {token}",
                                  "offset": "0", "file_size": str(file_size),
                                  "Content-Type": "application/octet-stream"},
                         data=data, timeout=180)
''',
    "instagram/ig_story_poll.py": '''"""ig_story_poll.py"""
import time
import requests


def wait(container_id, token, max_tries=40):
    for _ in range(max_tries):
        time.sleep(5)
        r = requests.get(
            f"https://graph.facebook.com/v21.0/{container_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=15).json()
        if r.get("status_code") == "FINISHED":
            return True
        if r.get("status_code") == "ERROR":
            return False
    return False
''',
    "instagram/ig_story_publish.py": '''"""ig_story_publish.py"""
import requests


def publish(ig_id, token, container_id):
    r = requests.post(
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        data={"creation_id": container_id, "access_token": token},
        timeout=20).json()
    return bool(r.get("id"))
''',
    "instagram/ig_story_main.py": '''"""ig_story_main.py"""
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
''',

    "instagram/ig_short_container.py": '"""ig_short_container.py"""\n# Reels container\nimport requests\n\n\ndef create(ig_id, token, video_url, caption=""):\n    return requests.post(\n        f"https://graph.facebook.com/v21.0/{ig_id}/media",\n        data={"media_type": "REELS", "video_url": video_url,\n              "caption": caption, "access_token": token},\n        timeout=30).json()\n',
    "instagram/ig_short_upload.py": '"""ig_short_upload.py"""\n# Reels uses URL, no byte upload\n',
    "instagram/ig_short_poll.py": '"""ig_short_poll.py"""\nimport time\nimport requests\n\n\ndef wait(cid, token, max_tries=45):\n    for _ in range(max_tries):\n        time.sleep(6)\n        r = requests.get(\n            f"https://graph.facebook.com/v21.0/{cid}",\n            params={"fields": "status_code", "access_token": token},\n            timeout=12).json()\n        if r.get("status_code") == "FINISHED":\n            return True\n        if r.get("status_code") == "ERROR":\n            return False\n    return False\n',
    "instagram/ig_short_publish.py": '"""ig_short_publish.py"""\nimport requests\n\n\ndef publish(ig_id, token, cid):\n    r = requests.post(\n        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",\n        data={"creation_id": cid, "access_token": token},\n        timeout=18).json()\n    return bool(r.get("id"))\n',
    "instagram/ig_short_main.py": '"""ig_short_main.py"""\nimport os\nfrom sawajstudiobot.video_uploader.instagram.ig_short_container import create\nfrom sawajstudiobot.video_uploader.instagram.ig_short_poll import wait\nfrom sawajstudiobot.video_uploader.instagram.ig_short_publish import publish\n\n\ndef upload(video_path, caption="", direct_url=None):\n    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()\n    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()\n    if not token or not ig_id or not direct_url:\n        return False\n    cont = create(ig_id, token, direct_url, caption)\n    cid = cont.get("id")\n    if not cid:\n        return False\n    if not wait(cid, token):\n        return False\n    return publish(ig_id, token, cid)\n',

    # ═══ YouTube ═══
    "youtube/__init__.py": '"""YouTube uploader."""\n',
    "youtube/yt_auth.py": '''"""yt_auth.py"""
import os


def get_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    creds = Credentials(
        None,
        refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
        client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
        client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token")
    return build("youtube", "v3", credentials=creds, cache_discovery=False)
''',
    "youtube/yt_short_upload.py": '''"""yt_short_upload.py"""
from googleapiclient.http import MediaFileUpload


def upload_video(yt, video_path, title, description, tags):
    body = {"snippet": {"title": title[:100], "description": description,
                        "tags": tags or ["Shorts", "Hadith"], "categoryId": "22"},
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
''',
    "youtube/yt_short_playlist.py": '''"""yt_short_playlist.py"""


def add(yt, video_id, playlist_id):
    try:
        yt.playlistItems().insert(
            part="snippet",
            body={"snippet": {"playlistId": playlist_id.strip(),
                              "resourceId": {"kind": "youtube#video",
                                             "videoId": video_id}}}).execute()
        return True
    except Exception:
        return False
''',
    "youtube/yt_short_main.py": '''"""yt_short_main.py"""
import os
from sawajstudiobot.video_uploader.youtube.yt_auth import get_service
from sawajstudiobot.video_uploader.youtube.yt_short_upload import upload_video
from sawajstudiobot.video_uploader.youtube.yt_short_playlist import add


def upload(video_path, title="", description="", tags=None):
    yt = get_service()
    vid = upload_video(yt, video_path, title, description, tags)
    if vid:
        pl = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID")
        if pl:
            add(yt, vid, pl)
        return True
    return False
''',

    "youtube/yt_long_upload.py": '"""yt_long_upload.py"""\nfrom googleapiclient.http import MediaFileUpload\n\n\ndef upload_video(yt, video_path, title, description, tags):\n    body = {"snippet": {"title": title[:100], "description": description,\n                        "tags": tags or ["Hadith"], "categoryId": "22"},\n            "status": {"privacyStatus": "public",\n                       "selfDeclaredMadeForKids": False}}\n    req = yt.videos().insert(part="snippet,status", body=body,\n                             media_body=MediaFileUpload(video_path, chunksize=-1,\n                                                        resumable=True,\n                                                        mimetype="video/mp4"))\n    response = None\n    while response is None:\n        _, response = req.next_chunk()\n    return response.get("id")\n',
    "youtube/yt_long_playlist.py": '"""yt_long_playlist.py"""\n\n\ndef add(yt, video_id, playlist_id):\n    try:\n        yt.playlistItems().insert(\n            part="snippet",\n            body={"snippet": {"playlistId": playlist_id.strip(),\n                              "resourceId": {"kind": "youtube#video",\n                                             "videoId": video_id}}}).execute()\n        return True\n    except Exception:\n        return False\n',
    "youtube/yt_long_chapters.py": '"""yt_long_chapters.py"""\n\n\ndef format_chapters(chapters):\n    if not chapters:\n        return ""\n    lines = ["\\n\\n⏱️ Timestamps:"]\n    for c in chapters:\n        lines.append(f"{c} " if isinstance(c, str) else str(c))\n    return "\\n".join(lines)\n',
    "youtube/yt_long_main.py": '"""yt_long_main.py"""\nimport os\nfrom sawajstudiobot.video_uploader.youtube.yt_auth import get_service\nfrom sawajstudiobot.video_uploader.youtube.yt_long_upload import upload_video\nfrom sawajstudiobot.video_uploader.youtube.yt_long_playlist import add\nfrom sawajstudiobot.video_uploader.youtube.yt_long_chapters import format_chapters\n\n\ndef upload(video_path, title="", description="", tags=None, chapters=None):\n    if chapters:\n        description += format_chapters(chapters)\n    yt = get_service()\n    vid = upload_video(yt, video_path, title, description, tags)\n    if vid:\n        pl = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID")\n        if pl:\n            add(yt, vid, pl)\n        return True\n    return False\n',
}


def main():
    total = 0
    for rel_path, content in FILES.items():
        full = os.path.join(BASE, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        total += 1
    print(f"🎉 Uploader: {total} files written!")


if __name__ == "__main__":
    main()
