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

    Args:
        None

    Attributes:
        cfg (Config): Configuration object.
        session (requests.Session): HTTP session with retry.
        api_status (dict): API status tracker.

    Methods:
        __init__(self): Initializes the BasePipeline object.
        run_cmd(self, cmd): Runs a shell command with logging.
        download(self, url, path, min_size=12000): Downloads a file with minimum size check.
        cleanup(self, files, folder=None): Removes temporary files and folders.
    """

    # ─────────────────────────────────────────────────────
    # ① INIT — setup session + trackers
    # ─────────────────────────────────────────────────────
    def __init__(self):
        """
        Initializes the BasePipeline object. Sets up the HTTP session with retry,
        API status tracker, and configuration.
        """
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
    def run_cmd(self, cmd: str) -> None:
        """
        Runs a shell command with logging.

        Args:
            cmd (str): The shell command to execute.

        Returns:
            None
        """
        log_step("A5_base_pipeline.py", f"CMD: {cmd[:80]}", "ok")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            log_error("A5_base_pipeline.py", f"CMD failed: {str(e)[:120]}")
            raise

    # ─────────────────────────────────────────────────────
    # ③ DOWNLOAD
    # ─────────────────────────────────────────────────────
    def download(self, url: str, path: str, min_size: int = 12000) -> bool:
        """
        Downloads a file with a minimum size check.

        Args:
            url (str): URL to download.
            path (str): Local path to save the downloaded file.
            min_size (int, optional): Minimum file size in bytes. Defaults to 12000.

        Returns:
            bool: True if the download was successful and the file size is above the minimum, False otherwise.
        """
        try:
            response = self.session.get(url, timeout=35)
            if response.status_code == 200 and len(response.content) > min_size:
                with open(path, "wb") as file:
                    file.write(response.content)
                log_step("A5_base_pipeline.py", f"Download OK: {path}", "ok",
                         f"{len(response.content) // 1024} KB")
                return True
            log_step("A5_base_pipeline.py", f"Download small: {url[:50]}", "fail")
        except Exception as e:
            log_step("A5_base_pipeline.py", f"Download error", "fail", str(e)[:60])
        return False

    # ─────────────────────────────────────────────────────
    # ④ CLEANUP
    # ─────────────────────────────────────────────────────
    def cleanup(self, files: list, folder: str = None) -> None:
        """
        Removes temporary files and folders.

        Args:
            files (list): List of files to remove.
            folder (str, optional): Optional folder to remove. Defaults to None.

        Returns:
            None
        """
        log_step("A5_base_pipeline.py", "Cleanup starting", "ok")
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        if folder:
            shutil.rmtree(folder, ignore_errors=True)
        log_step("A5_base_pipeline.py", "Cleanup done", "ok")
