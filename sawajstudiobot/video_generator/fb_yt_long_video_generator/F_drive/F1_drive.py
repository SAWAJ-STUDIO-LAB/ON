# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      F1_drive.py                               ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                F_drive/F1_drive.py                       ║
# ║  ✅ FIXED:     Retry + larger chunks (10MB) for long     ║
# ╚══════════════════════════════════════════════════════════╝

import os
import time
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


class Drive:
    """Upload video to Google Drive (Long — bigger files)."""

    def __init__(self, base):
        log_file_start("F1_drive.py", "Google Drive upload (Long)")
        self.base = base
        log_file_end("F1_drive.py", "success", "Ready")

    def upload(self, path, prefix="Long", max_retries=3):
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
            folder_id = os.environ.get("GDRIVE_LONG_VIDEO_FOLDER_ID")
            if folder_id:
                meta["parents"] = [folder_id]

            # ✅ Long: 10 MB chunks for faster upload
            media = MediaFileUpload(
                path,
                mimetype="video/mp4",
                resumable=True,
                chunksize=10 * 1024 * 1024)

            request = service.files().create(
                body=meta, media_body=media, fields="id")

            response = None
            last_pct = -1
            while response is None:
                status, response = request.next_chunk()
                if status:
                    pct = int(status.progress() * 100)
                    if pct >= last_pct + 20:
                        log_step("F1_drive.py",
                                 f"Upload {pct}%", "info")
                        last_pct = pct

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
            log_api("F1_drive.py", "Google Drive", "failed",
                    str(e)[:150])
            return None, None
