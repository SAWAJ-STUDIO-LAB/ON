# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      short_uploader.py                         ║
# ║  📁 PATH:      .../video_uploader/facebook/              ║
# ║  ✅ FIXED:     Streaming upload (no RAM overload)        ║
# ╚══════════════════════════════════════════════════════════╝

import os
import requests


class FacebookShortUploader:
    """Upload Short video to Facebook Page (streaming-safe)."""

    def __init__(self, base=None):
        self.base = base
        self.session = requests.Session()

    def upload(self, video_path, caption=""):
        token = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
        page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

        if not token:
            print("❌ FB Short: META token missing")
            return False
        if not page_id:
            print("❌ FB Short: Page ID missing")
            return False
        if not os.path.exists(video_path):
            print(f"❌ FB Short: File not found: {video_path}")
            return False

        try:
            f_size = os.path.getsize(video_path)
            print(f"→ FB Short: Uploading {f_size // 1024} KB")

            # ✅ streaming — no f.read() into memory
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
            print(f"❌ FB Short: {err.get('code', '?')} — "
                  f"{err.get('message', '')[:150]}")
            return False

        except Exception as e:
            print(f"❌ FB Short error: {str(e)[:200]}")
            return False


if __name__ == "__main__":
    FacebookShortUploader().upload("test_video.mp4", "Test caption")
