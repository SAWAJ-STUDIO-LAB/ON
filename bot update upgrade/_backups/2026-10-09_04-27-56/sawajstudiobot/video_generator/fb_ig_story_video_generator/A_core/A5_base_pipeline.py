# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A5_base_pipeline.py                       ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A5_base_pipeline.py                ║
# ║  🎯 PURPOSE:   HTTP session + download + cleanup         ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔧 BASE PIPELINE MODULE                                ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Shared helpers for all pipelines                    ║
║                                                          ║
║   📖 Provides:                                           ║
║      • HTTP session with retry                           ║
║      • API status tracker                                ║
║      • Download helper                                   ║
║      • Cleanup helper                                    ║
║      • Command runner                                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import subprocess
import shutil
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_error


# ═══════════════════════════════════════════════════════════
# 🎯 BASE PIPELINE CLASS
# ═══════════════════════════════════════════════════════════

class BasePipeline:
    """
    Base class — shared helpers for all pipelines.

    Provides:
      - HTTP session with retry
      - API status tracker
      - Download helper
      - Cleanup helper
      - Command runner
    """

    # ─────────────────────────────────────────────────────
    # ① INIT — setup session + trackers
    # ─────────────────────────────────────────────────────
    def __init__(self):
        log_file_start("A5_base_pipeline.py", "Setup session + tracker")
        self.cfg = Config()
        self.session = requests.Session()

        # Retry strategy
        retry = Retry(
            total=5,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

        # API status tracker
        self.api_status = {
            "AI": {}, "TTS": {}, "Music": {}, "Background": {},
            "Translation": {}, "Hadith": {}, "Drive": {},
            "Facebook": {}, "Instagram": {},
        }
        log_file_end("A5_base_pipeline.py", "success", "Session ready")

    # ─────────────────────────────────────────────────────
    # ② RUN COMMAND
    # ─────────────────────────────────────────────────────
    def run_cmd(self, cmd):
        """Run shell command with logging."""
        log_step("A5_base_pipeline.py", f"CMD: {cmd[:80]}", "ok")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            log_error("A5_base_pipeline.py", f"CMD failed: {str(e)[:120]}")
            raise

    # ─────────────────────────────────────────────────────
    # ③ DOWNLOAD
    # ─────────────────────────────────────────────────────
    def download(self, url, path, min_size=12000):
        """
        Download file with minimum size check.

        Args:
            url:      URL to download
            path:     local path to save
            min_size: minimum bytes (default 12000)

        Returns:
            True if downloaded, False otherwise
        """
        try:
            r = self.session.get(url, timeout=35)
            if r.status_code == 200 and len(r.content) > min_size:
                with open(path, "wb") as f:
                    f.write(r.content)
                log_step("A5_base_pipeline.py", f"Download OK: {path}", "ok",
                         f"{len(r.content) // 1024} KB")
                return True
            log_step("A5_base_pipeline.py", f"Download small: {url[:50]}", "fail")
        except Exception as e:
            log_step("A5_base_pipeline.py", f"Download err", "fail", str(e)[:60])
        return False

    # ─────────────────────────────────────────────────────
    # ④ CLEANUP
    # ─────────────────────────────────────────────────────
    def cleanup(self, files, folder=None):
        """
        Remove temp files + folders.

        Args:
            files:  list of files to remove
            folder: optional folder to remove
        """
        log_step("A5_base_pipeline.py", "Cleanup starting", "ok")
        for f in files:
            if os.path.exists(f):
                os.remove(f)
        if folder:
            shutil.rmtree(folder, ignore_errors=True)
        log_step("A5_base_pipeline.py", "Cleanup done", "ok")
