# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      long_uploader.py                          ║
# ║  📁 PATH:      .../video_uploader/facebook/              ║
# ║                long_uploader.py                          ║
# ║  🎯 PURPOSE:   Upload Long video to Facebook             ║
# ║  📖 FOLDER:    facebook                                  ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📘 FACEBOOK LONG UPLOADER                              ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Long video ko Facebook Page pe upload karna         ║
║                                                          ║
║   📖 API:                                                ║
║      POST /{page_id}/videos                              ║
║                                                          ║
║   📝 Difference:                                          ║
║      • Timeout: 3600s (1 hour) for large files           ║
║      • Same API as Short                                 ║
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
# 📘 FACEBOOK LONG UPLOADER CLASS
# ═══════════════════════════════════════════════════════════

class FacebookLongUploader:
    """Upload Long video to Facebook Page."""

    def __init__(self, base=None):
        """Initialize uploader."""
        self.base = base
        self.session = requests.Session()

    # ─────────────────────────────────────────────────────
    # UPLOAD — main upload method
    # ─────────────────────────────────────────────────────
    def upload(self, video_path, caption=""):
        """
        Upload Long video to Facebook Page.

        Args:
            video_path: path to video file
            caption:    description text

        Returns:
            True if successful, False otherwise
        """
        # ═══════════ Get credentials ═══════════
        token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

        if not token:
            print("❌ FB Long: META token missing")
            return False

        if not page_id:
            print("❌ FB Long: Page ID missing")
            return False

        try:
            f_size = os.path.getsize(video_path)
            print(f"→ FB Long: Uploading {f_size // 1024} KB")

            with open(video_path, "rb") as f:
                res = self.session.post(
                    f"https://graph.facebook.com/v21.0/{page_id}/videos",
                    data={
                        "access_token": token,
                        "description": caption,
                        "published": "true",
                    },
                    files={"source": f},
                    timeout=3600).json()

            if res.get("id"):
                print(f"✅ FB Long: Upload successful! ID: {res['id']}")
                return True

            err = res.get("error", {})
            print(f"❌ FB Long: {err.get('code', '?')} — {err.get('message', '')[:80]}")
            return False

        except Exception as e:
            print(f"❌ FB Long error: {str(e)[:100]}")
            return False


# ═══════════════════════════════════════════════════════════
# 🧪 TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    uploader = FacebookLongUploader()
    uploader.upload("test_video.mp4", "Test caption")
