# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      story_uploader.py                         ║
# ║  📁 PATH:      .../video_uploader/facebook/              ║
# ║                story_uploader.py                         ║
# ║  🎯 PURPOSE:   Upload Story to Facebook                  ║
# ║  📖 FOLDER:    facebook                                  ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📘 FACEBOOK STORY UPLOADER                             ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Story video ko Facebook Page pe upload karna        ║
║                                                          ║
║   📖 API:                                                ║
║      POST /{page_id}/video_stories                       ║
║                                                          ║
║   📖 Flow (3 phases):                                    ║
║      1. Start phase  → Get video_id + upload_url         ║
║      2. Upload phase → Send video bytes                  ║
║      3. Finish phase → Publish story                     ║
║                                                          ║
║   🔑 Credentials:                                         ║
║      • FACEBOOK_META_TOKEN                               ║
║      • FACEBOOK_PAGE_ID                                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import requests


# ═══════════════════════════════════════════════════════════
# 📘 FACEBOOK STORY UPLOADER CLASS
# ═══════════════════════════════════════════════════════════

class FacebookStoryUploader:
    """Upload video to Facebook Story."""

    def __init__(self, base=None):
        """Initialize uploader."""
        self.base = base
        self.session = requests.Session()

    # ─────────────────────────────────────────────────────
    # UPLOAD — main upload method
    # ─────────────────────────────────────────────────────
    def upload(self, video_path):
        """
        Upload video to Facebook Story.

        Args:
            video_path: path to video file

        Returns:
            True if successful, False otherwise
        """
        # ═══════════ Get credentials ═══════════
        token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

        if not token:
            print("❌ FB Story: META token missing")
            return False

        if not page_id:
            print("❌ FB Story: Page ID missing")
            return False

        try:
            f_size = os.path.getsize(video_path)
            print(f"→ FB Story: Uploading {f_size // 1024} KB")

            # ═══════════ Phase 1: Start ═══════════
            start = self.session.post(
                f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
                data={
                    "upload_phase": "start",
                    "file_size": f_size,
                    "access_token": token,
                },
                timeout=30).json()

            v_id = start.get("video_id")
            v_url = start.get("upload_url")

            if not v_id or not v_url:
                print(f"❌ FB Story start failed: {str(start)[:100]}")
                return False

            # ═══════════ Phase 2: Upload bytes ═══════════
            with open(video_path, "rb") as f:
                up_res = self.session.post(
                    v_url,
                    headers={
                        "Authorization": f"OAuth {token}",
                        "offset": "0",
                        "file_size": str(f_size),
                    },
                    data=f.read(),
                    timeout=180)

            if up_res.status_code not in (200, 201):
                print(f"❌ FB Story upload failed: HTTP {up_res.status_code}")
                return False

            # ═══════════ Phase 3: Finish ═══════════
            finish = self.session.post(
                f"https://graph.facebook.com/v21.0/{page_id}/video_stories",
                data={
                    "upload_phase": "finish",
                    "video_id": v_id,
                    "access_token": token,
                },
                timeout=30).json()

            if finish.get("success") or finish.get("post_id"):
                print("✅ FB Story: Upload successful!")
                return True

            print(f"❌ FB Story finish failed: {str(finish)[:100]}")
            return False

        except Exception as e:
            print(f"❌ FB Story error: {str(e)[:100]}")
            return False


# ═══════════════════════════════════════════════════════════
# 🧪 TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    uploader = FacebookStoryUploader()
    uploader.upload("test_video.mp4")
