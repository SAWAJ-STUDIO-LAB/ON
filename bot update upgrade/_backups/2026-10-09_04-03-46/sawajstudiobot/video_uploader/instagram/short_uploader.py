# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      short_uploader.py                         ║
# ║  📁 PATH:      .../video_uploader/instagram/             ║
# ║                short_uploader.py                         ║
# ║  🎯 PURPOSE:   Upload Reel to Instagram                  ║
# ║  📖 FOLDER:    instagram                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📸 INSTAGRAM REELS UPLOADER                            ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Short video (Reel) ko Instagram pe upload karna     ║
║                                                          ║
║   📖 API:                                                ║
║      POST /{ig_id}/media  (media_type=REELS)             ║
║      POST /{ig_id}/media_publish                         ║
║                                                          ║
║   📖 Flow (4 phases):                                    ║
║      1. Create REELS container with video URL            ║
║      2. Poll status → wait for FINISHED                  ║
║      3. Publish → media_publish                          ║
║                                                          ║
║   🔑 Credentials:                                         ║
║      • FACEBOOK_INSTAGRAM_META_TOKEN                     ║
║      • INSTAGRAM_BUSINESS_ACCOUNT_ID                     ║
║                                                          ║
║   📝 Note:                                                ║
║      video_url (Google Drive direct link) chahiye        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import time
import requests


# ═══════════════════════════════════════════════════════════
# 📸 INSTAGRAM REELS UPLOADER CLASS
# ═══════════════════════════════════════════════════════════

class InstagramShortUploader:
    """Upload Reel to Instagram."""

    def __init__(self, base=None):
        """Initialize uploader."""
        self.base = base
        self.session = requests.Session()

    # ─────────────────────────────────────────────────────
    # UPLOAD — main upload method
    # ─────────────────────────────────────────────────────
    def upload(self, video_path, caption="", direct_url=None):
        """
        Upload Reel to Instagram.

        Args:
            video_path: path to video file (not used, for logging)
            caption:    post caption
            direct_url: public video URL (required)

        Returns:
            True if successful, False otherwise
        """
        # ═══════════ Get credentials ═══════════
        token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
        ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()

        if not token:
            print("❌ IG Reel: META token missing")
            return False

        if not ig_id:
            print("❌ IG Reel: IG Business ID missing")
            return False

        if not direct_url:
            print("❌ IG Reel: video URL missing")
            return False

        try:
            print(f"→ IG Reel: Uploading via {direct_url[:60]}...")

            # ═══════════ Phase 1: Create container ═══════════
            cont = self.session.post(
                f"https://graph.facebook.com/v21.0/{ig_id}/media",
                data={
                    "media_type": "REELS",
                    "video_url": direct_url,
                    "caption": caption,
                    "access_token": token,
                },
                timeout=30).json()

            cid = cont.get("id")
            if not cid:
                print(f"❌ IG Reel container failed: {str(cont)[:100]}")
                return False

            print(f"  ℹ️ Container ID: {cid}")

            # ═══════════ Phase 2: Poll status ═══════════
            print("  ℹ️ Polling status...")
            for _ in range(45):
                time.sleep(6)
                st = self.session.get(
                    f"https://graph.facebook.com/v21.0/{cid}",
                    params={"fields": "status_code", "access_token": token},
                    timeout=12).json()

                if st.get("status_code") == "FINISHED":
                    break
                if st.get("status_code") == "ERROR":
                    print("❌ IG Reel processing error")
                    return False

            # ═══════════ Phase 3: Publish ═══════════
            pub = self.session.post(
                f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
                data={
                    "creation_id": cid,
                    "access_token": token,
                },
                timeout=18).json()

            if pub.get("id"):
                print(f"✅ IG Reel: Upload successful! ID: {pub['id']}")
                return True

            print(f"❌ IG Reel publish failed: {str(pub)[:100]}")
            return False

        except Exception as e:
            print(f"❌ IG Reel error: {str(e)[:100]}")
            return False


# ═══════════════════════════════════════════════════════════
# 🧪 TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    uploader = InstagramShortUploader()
    uploader.upload("test_video.mp4", "Test caption",
                    "https://drive.google.com/uc?id=xxx")
