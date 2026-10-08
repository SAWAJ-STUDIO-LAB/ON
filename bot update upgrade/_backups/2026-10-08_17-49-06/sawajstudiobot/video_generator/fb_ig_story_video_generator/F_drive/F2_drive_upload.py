"""F2_drive_upload.py — Sirf upload."""
import os
import time
from A_core.A10_log_api import log_api


def upload(base, path, prefix="Story"):
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = Credentials(
            None,
            refresh_token=os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN"),
            client_id=os.environ.get("GOOGLE_DRIVE_CLIENT_ID"),
            client_secret=os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET"),
            token_uri="https://oauth2.googleapis.com/token")
        service = build("drive", "v3", credentials=creds, cache_discovery=False)
        meta = {"name": f"{prefix}_{int(time.time())}.mp4"}
        folder_id = os.environ.get("GDRIVE_STORY_VIDEO_FOLDER_ID")
        if folder_id:
            meta["parents"] = [folder_id]
        up = service.files().create(
            body=meta,
            media_body=MediaFileUpload(path, mimetype="video/mp4", resumable=True),
            fields="id").execute()
        did = up.get("id")
        log_api("F2_drive_upload.py", "Drive", "success", did)
        return did
    except Exception as e:
        log_api("F2_drive_upload.py", "Drive", "failed", str(e)[:100])
        return None
