# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      F1_drive.py                               ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                F_drive/F1_drive.py                       ║
# ║  🎯 PURPOSE:   Google Drive upload (video backup)        ║
# ║  📖 FOLDER:    F_drive                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   ☁️  DRIVE UPLOAD MODULE (SHORT)                        ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Final video ko Google Drive pe upload karna         ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Authenticate (OAuth refresh token)               ║
║      2. Create file metadata                             ║
║      3. Upload video (resumable)                         ║
║      4. Make public                                      ║
║      5. Return view + direct links                       ║
║                                                          ║
║   🔑 Credentials:                                         ║
║      • GOOGLE_DRIVE_CLIENT_ID                            ║
║      • GOOGLE_DRIVE_CLIENT_SECRET                        ║
║      • GOOGLE_DRIVE_REFRESH_TOKEN                        ║
║      • GDRIVE_SHORT_VIDEO_FOLDER_ID (target folder)      ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      Target folder: Short video folder                   ║
║      prefix: "Short" (Story: "Story")                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import time
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class Drive:
    """Upload video to Google Drive (Short version)."""

    def __init__(self, base):
        log_file_start("F1_drive.py", "Google Drive upload")
        self.base = base
        log_file_end("F1_drive.py", "success", "Ready")

    def upload(self, path, prefix="Short"):
        """
        Upload video to Google Drive.

        Args:
            path:   video path
            prefix: file name prefix (default "Short")

        Returns:
            (link, direct) tuple
        """
        log_step("F1_drive.py", f"upload({path})", "ok")

        try:
            # ═══════════ Import Google libs ═══════════
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            # ═══════════ Authenticate ═══════════
            creds = Credentials(
                None,
                refresh_token=os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN"),
                client_id=os.environ.get("GOOGLE_DRIVE_CLIENT_ID"),
                client_secret=os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET"),
                token_uri="https://oauth2.googleapis.com/token")
            service = build("drive", "v3", credentials=creds, cache_discovery=False)

            # ═══════════ Prepare metadata ═══════════
            meta = {"name": f"{prefix}_{int(time.time())}.mp4"}
            folder_id = os.environ.get("GDRIVE_SHORT_VIDEO_FOLDER_ID")
            if folder_id:
                meta["parents"] = [folder_id]

            # ═══════════ Upload ═══════════
            up = service.files().create(
                body=meta,
                media_body=MediaFileUpload(path, mimetype="video/mp4", resumable=True),
                fields="id").execute()
            did = up.get("id")

            # ═══════════ Make public ═══════════
            service.permissions().create(
                fileId=did,
                body={"type": "anyone", "role": "reader"}).execute()

            # ═══════════ Build links ═══════════
            link = f"https://drive.google.com/file/d/{did}/view"
            direct = f"https://drive.google.com/uc?export=download&id={did}"

            self.base.api_status["Drive"]["Google Drive"] = "success"
            log_api("F1_drive.py", "Google Drive", "success", did)
            return link, direct

        except Exception as e:
            self.base.api_status["Drive"]["Google Drive"] = f"failed ({str(e)[:50]})"
            log_api("F1_drive.py", "Google Drive", "failed", str(e)[:100])
            return None, None
