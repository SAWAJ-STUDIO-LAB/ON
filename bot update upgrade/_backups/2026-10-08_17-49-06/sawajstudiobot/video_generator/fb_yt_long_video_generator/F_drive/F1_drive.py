# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      F1_drive.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                F_drive/F1_drive.py                       ║
# ║  🎯 PURPOSE:   Google Drive upload (video backup)        ║
# ║  📖 FOLDER:    F_drive                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   ☁️  DRIVE UPLOAD MODULE (LONG)                         ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Long video ko Google Drive pe upload karna          ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Authenticate (OAuth refresh token)               ║
║      2. Upload video (resumable — long files ke liye)    ║
║      3. Make public                                      ║
║      4. Return view + direct links                       ║
║                                                          ║
║   🔑 Credentials:                                         ║
║      • GOOGLE_DRIVE_CLIENT_ID                            ║
║      • GOOGLE_DRIVE_CLIENT_SECRET                        ║
║      • GOOGLE_DRIVE_REFRESH_TOKEN                        ║
║      • GDRIVE_LONG_VIDEO_FOLDER_ID                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import time
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class Drive:
    """Upload long video to Google Drive."""

    def __init__(self, base):
        log_file_start("F1_drive.py", "Google Drive upload (Long)")
        self.base = base
        log_file_end("F1_drive.py", "success", "Ready")

    def upload(self, path, prefix="Long"):
        """
        Upload video to Google Drive.

        Args:
            path:   video path
            prefix: file name prefix (default "Long")

        Returns:
            (link, direct) tuple
        """
        log_step("F1_drive.py", f"upload({path})", "ok")

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
            folder_id = os.environ.get("GDRIVE_LONG_VIDEO_FOLDER_ID")
            if folder_id:
                meta["parents"] = [folder_id]

            # Long files — chunked resumable upload
            up = service.files().create(
                body=meta,
                media_body=MediaFileUpload(
                    path, mimetype="video/mp4",
                    resumable=True, chunksize=10 * 1024 * 1024),
                fields="id").execute()
            did = up.get("id")

            service.permissions().create(
                fileId=did,
                body={"type": "anyone", "role": "reader"}).execute()

            link = f"https://drive.google.com/file/d/{did}/view"
            direct = f"https://drive.google.com/uc?export=download&id={did}"

            self.base.api_status["Drive"]["Google Drive"] = "success"
            log_api("F1_drive.py", "Google Drive", "success", did)
            return link, direct

        except Exception as e:
            self.base.api_status["Drive"]["Google Drive"] = f"failed ({str(e)[:50]})"
            log_api("F1_drive.py", "Google Drive", "failed", str(e)[:100])
            return None, None
