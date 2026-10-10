# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C6_background.py                          ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C6_background.py                ║
# ║  🎯 PURPOSE:   Stock Background Video / Image Fetcher    ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🖼️ BACKGROUND MEDIA MODULE                              ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Pexels / Pixabay API se high quality 16:9 4K landscape║
║      nature & Islamic background video clips load karna.  ║
╚══════════════════════════════════════════════════════════╝
"""

import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_api, log_step


class BackgroundFetcher:
    """Fetches high-resolution landscape background videos/images for 16:9 Long Videos."""

    def __init__(self, session=None):
        log_file_start("C6_background.py", "Init Background Fetcher")
        self.cfg = Config()
        self.session = session or requests.Session()
        log_file_end("C6_background.py", "success")

    def fetch_video(self, query: str, output_path: str) -> bool:
        """Fetches HD video from Pexels."""
        if not self.cfg.PEXELS_API_KEY:
            return False

        try:
            headers = {"Authorization": self.cfg.PEXELS_API_KEY}
            url = f"https://api.pexels.com/videos/search?query={query}&orientation=landscape&per_page=5"
            r = self.session.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                videos = r.json().get("videos", [])
                if videos:
                    video_files = videos[0].get("video_files", [])
                    # Pick 1080p landscape video file
                    for vf in video_files:
                        if vf.get("width", 0) >= 1280:
                            video_url = vf.get("link")
                            vr = self.session.get(video_url, timeout=60)
                            if vr.status_code == 200:
                                with open(output_path, "wb") as f:
                                    f.write(vr.content)
                                log_api("C6_background.py", "Pexels Video API", "success")
                                return True
        except Exception as e:
            log_api("C6_background.py", "Pexels Video API", "failed", str(e)[:50])

        return False
                          
