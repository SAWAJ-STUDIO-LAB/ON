# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      short_uploader.py                         ║
# ║  📁 PATH:      .../video_uploader/facebook/              ║
# ║                short_uploader.py                         ║
# ║  🎯 PURPOSE:   Upload Short video to Facebook            ║
# ║  📖 FOLDER:    facebook                                  ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📘 FACEBOOK SHORT UPLOADER                             ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Short video ko Facebook Page pe upload karna        ║
║                                                          ║
║   📖 API:                                                ║
║      POST /{page_id}/videos                              ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Upload video via multipart/form-data             ║
║      2. Facebook auto-publishes                          ║
║                                                          ║
║   🔑 Credentials:                                         ║
║      • FACEBOOK_META_TOKEN                               ║
║      • FACEBOOK_PAGE_ID                                  ║
║                                                          ║
║   📝 Note:                                                ║
║      Yeh endpoint 100MB tak handle karta hai             ║
║      Bade files ke liye resumable upload chahiye         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import requests


# ═══════════════════════════════════════════════════════════
# 📘 FACEBOOK SHORT UPLOADER CLASS
# ═══════════════════════════════════════════════════════════

class FacebookShortUploader:
    """Upload Short video to Facebook Page."""

    def __init__(self, base=None):
        """Initialize uploader."""
        self.base = base
        self.session = requests.Session()

    # ─────────────────────────────────────────────────────
    # UPLOAD — main upload method
    # ─────────────────────────────────────────────────────
    def upload(self, video_path, caption=""):
        """
        Upload Short video to Facebook Page.

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
            print("❌ FB Short: META token missing")
            return False

        if not page_id:
            print("❌ FB Short: Page ID missing")
            return False

        try:
            f_size = os.path.getsize(video_path)
            print(f"→ FB Short: Uploading {f_size // 1024} KB")

            with open(video_path, "rb") as f:
                res = self.session.post(
                    f"https://graph.facebook.com/v21.0/{page_id}/videos",
                    data={
                        "access_token": token,
                        "description": caption,
                        "published": "true",
                    },
                    files={"source": f},
                    timeout=1800).json()

            if res.get("id"):
                print(f"✅ FB Short: Upload successful! ID: {res['id']}")
                return True

            err = res.get("error", {})
            print(f"❌ FB Short: {err.get('code', '?')} — {err.get('message', '')[:80]}")
            return False

        except Exception as e:
            print(f"❌ FB Short error: {str(e)[:100]}")
            return False


# ═══════════════════════════════════════════════════════════
# 🧪 TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    uploader = FacebookShortUploader()
    uploader.upload("test_video.mp4", "Test caption")
