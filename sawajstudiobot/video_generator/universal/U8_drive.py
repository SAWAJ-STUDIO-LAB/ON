"""
U8_drive.py — Universal Google Drive Upload
============================================
Parametrized via folder_env_var + chunk_mb.
"""

import os
import time
from universal.U1_logger import log_file_start, log_file_end, log_step, log_api


class Drive:

    def __init__(self, base, folder_env_var, chunk_mb=5):
        """
        Args:
            base:            BasePipeline instance
            folder_env_var:  e.g. "GDRIVE_STORY_VIDEO_FOLDER_ID"
            chunk_mb:        upload chunk size (5 for small, 10 for long)
        """
        log_file_start("F1_drive.py", "Google Drive upload")
        self.base = base
        self.folder_env_var = folder_env_var
        self.chunk_bytes = chunk_mb * 1024 * 1024
        log_file_end("F1_drive.py", "success", "Ready")

    def upload(self, path, prefix="Video", max_retries=3):
        log_step("F1_drive.py", f"upload({path})", "ok")
        if not path or not os.path.exists(path):
            log_api("F1_drive.py", "Drive", "failed", "file not found")
            return None, None

        size_mb = os.path.getsize(path) / 1024 / 1024
        if size_mb < 0.01:
            log_api("F1_drive.py", "Drive", "failed",
                    f"file too small ({size_mb:.3f} MB)")
            return None, None
        log_step("F1_drive.py", f"File size {size_mb:.1f} MB", "info")

        for attempt in range(1, max_retries + 1):
            try:
                result = self._do_upload(path, prefix)
                if result[0]:
                    return result
                log_step("F1_drive.py",
                         f"Attempt {attempt}/{max_retries} failed", "warn")
            except Exception as e:
                log_step("F1_drive.py",
                         f"Attempt {attempt}/{max_retries} error",
                         "warn", str(e)[:80])
            if attempt < max_retries:
                time.sleep(2 ** attempt)

        log_api("F1_drive.py", "Drive", "failed",
                f"all {max_retries} attempts failed")
        return None, None

    def _do_upload(self, path, prefix):
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
            service = build("drive", "v3", credentials=creds,
                            cache_discovery=False)

            meta = {"name": f"{prefix}_{int(time.time())}.mp4"}
            folder_id = os.environ.get(self.folder_env_var)
            if folder_id:
                meta["parents"] = [folder_id]

            media = MediaFileUpload(
                path, mimetype="video/mp4",
                resumable=True, chunksize=self.chunk_bytes)

            request = service.files().create(
                body=meta, media_body=media, fields="id")

            response = None
            while response is None:
                _, response = request.next_chunk()

            did = response.get("id")
            if not did:
                return None, None

            try:
                service.permissions().create(
                    fileId=did,
                    body={"type": "anyone", "role": "reader"}).execute()
            except Exception as e:
                log_step("F1_drive.py", "Permission failed (ignored)",
                         "warn", str(e)[:60])

            link = f"https://drive.google.com/file/d/{did}/view"
            direct = f"https://drive.google.com/uc?export=download&id={did}"

            self.base.api_status["Drive"]["Google Drive"] = "success"
            log_api("F1_drive.py", "Google Drive", "success", did)
            return link, direct

        except Exception as e:
            self.base.api_status["Drive"]["Google Drive"] = \
                f"failed ({str(e)[:50]})"
            log_api("F1_drive.py", "Google Drive", "failed", str(e)[:150])
            return None, None
