# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      story_uploader.py                         ║
# ║  📁 PATH:      .../video_uploader/instagram/             ║
# ║                story_uploader.py                         ║
# ║  🎯 PURPOSE:   Upload Story to Instagram                 ║
# ║  📖 FOLDER:    instagram                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📸 INSTAGRAM STORY UPLOADER                            ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Story video ko Instagram pe upload karna            ║
║                                                          ║
║   📖 API:                                                ║
║      POST /{ig_id}/media  (media_type=STORIES)           ║
║      POST /{ig_id}/media_publish                         ║
║                                                          ║
║   📖 Flow (4 phases):                                    ║
║      1. Create container → Get container_id              ║
║      2. Upload bytes → resumable upload                  ║
║      3. Poll status → wait for FINISHED                  ║
║      4. Publish → media_publish                          ║
║                                                          ║
║   🔑 Credentials:                                         ║
║      • FACEBOOK_INSTAGRAM_META_TOKEN                     ║
║      • INSTAGRAM_BUSINESS_ACCOUNT_ID                     ║
║                                                          ║
║   ⏱️  Duration: 60s max (our video: 50-60s)               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import time
import requests


# ═══════════════════════════════════════════════════════════
# 📸 INSTAGRAM STORY UPLOADER CLASS
# ═══════════════════════════════════════════════════════════

class InstagramStoryUploader:
    """Upload video to Instagram Story."""

    def __init__(self, base=None):
        """Initialize uploader."""
        self.base = base
        self.session = requests.Session()

    # ─────────────────────────────────────────────────────
    # UPLOAD — main upload method
    # ─────────────────────────────────────────────────────
    def upload(self, video_path):
        """
        Upload video to Instagram Story.

        Args:
            video_path: path to video file

        Returns:
            True if successful, False otherwise
        """
        # ═══════════ Get credentials ═══════════
        token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
        ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()

        if not token:
            print("❌ IG Story: META token missing")
            return False

        if not ig_id:
            print("❌ IG Story: IG Business ID missing")
            return False

        try:
            f_size = os.path.getsize(video_path)
            print(f"→ IG Story: Uploading {f_size // 1024} KB")

            # ═══════════ Phase 1: Create container ═══════════
            cont = self.session.post(
                f"https://graph.facebook.com/v21.0/{ig_id}/media",
                data={
                    "media_type": "STORIES",
                    "upload_type": "resumable",
                    "access_token": token,
                },
                timeout=40).json()

            c_id = cont.get("id")
            if not c_id:
                print(f"❌ IG Story container failed: {str(cont)[:100]}")
                return False

            print(f"  ℹ️ Container ID: {c_id}")

            # ═══════════ Phase 2: Upload bytes ═══════════
            upload_url = (cont.get("uri")
                         or f"https://rupload.facebook.com/ig-api-upload/v21.0/{c_id}")

            with open(video_path, "rb") as f:
                video_bytes = f.read()

            headers = {
                "Authorization": f"OAuth {token}",
                "offset": "0",
                "file_size": str(f_size),
                "Content-Type": "application/octet-stream",
            }
            self.session.post(upload_url, headers=headers,
                              data=video_bytes, timeout=180)

            # ═══════════ Phase 3: Poll status ═══════════
            print("  ℹ️ Polling status...")
            for _ in range(40):
                time.sleep(5)
                st = self.session.get(
                    f"https://graph.facebook.com/v21.0/{c_id}",
                    params={"fields": "status_code", "access_token": token},
                    timeout=15).json()

                if st.get("status_code") == "FINISHED":
                    break
                if st.get("status_code") == "ERROR":
                    print("❌ IG Story processing error")
                    return False

            # ═══════════ Phase 4: Publish ═══════════
            pub = self.session.post(
                f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
                data={
                    "creation_id": c_id,
                    "access_token": token,
                },
                timeout=20).json()

            if pub.get("id"):
                print(f"✅ IG Story: Upload successful! ID: {pub['id']}")
                return True

            print(f"❌ IG Story publish failed: {str(pub)[:100]}")
            return False

        except Exception as e:
            print(f"❌ IG Story error: {str(e)[:100]}")
            return False


# ═══════════════════════════════════════════════════════════
# 🧪 TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    uploader = InstagramStoryUploader()
    uploader.upload("test_video.mp4")
