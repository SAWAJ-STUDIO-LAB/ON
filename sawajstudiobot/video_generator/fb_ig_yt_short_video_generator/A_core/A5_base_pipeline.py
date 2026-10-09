# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A5_base_pipeline.py                       ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                A_core/A5_base_pipeline.py                ║
# ║  🎯 PURPOSE:   HTTP session + download + cleanup         ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔧 BASE PIPELINE MODULE                                ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Shared helpers for short video pipeline             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import subprocess
import shutil
from typing import List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_error


class BasePipeline:
    """
    Base class for video generation pipelines. Provides common utilities like
    HTTP session management, command execution, file download, and cleanup.
    """

    def __init__(self) -> None:
        """
        Initializes the BasePipeline with a requests session and API status tracker.
        """
        log_file_start("A5_base_pipeline.py", "Setup session + tracker")
        self.cfg = Config()
        self.session = requests.Session()
        retry = Retry(total=5, backoff_factor=1.5,
                      status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

        self.api_status: dict = {
            "AI": {}, "TTS": {}, "Music": {}, "Background": {},
            "Translation": {}, "Hadith": {}, "Drive": {},
            "Facebook": {}, "Instagram": {}, "YouTube": {},
        }
        log_file_end("A5_base_pipeline.py", "success", "Session ready")

    def run_cmd(self, cmd: str) -> None:
        """
        Runs a shell command and logs the result.

        Args:
            cmd (str): The command to execute.

        Raises:
            subprocess.CalledProcessError: If the command fails.
        """
        log_step("A5_base_pipeline.py", f"CMD: {cmd[:80]}", "ok")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            log_error("A5_base_pipeline.py", f"CMD failed: {str(e)[:120]}")
            raise

    def download(self, url: str, path: str, min_size: int = 12000) -> bool:
        """
        Downloads a file from a URL and saves it to the specified path.

        Args:
            url (str): The URL to download from.
            path (str): The path to save the file to.
            min_size (int, optional): Minimum file size in bytes. Defaults to 12000.

        Returns:
            bool: True if the download was successful, False otherwise.
        """
        try:
            response = self.session.get(url, timeout=35)
            if response.status_code == 200 and len(response.content) > min_size:
                with open(path, "wb") as file:
                    file.write(response.content)
                log_step("A5_base_pipeline.py", f"Download OK: {path}", "ok",
                         f"{len(response.content) // 1024} KB")
                return True
        except Exception as e:
            log_step("A5_base_pipeline.py", f"Download err", "fail", str(e)[:60])
        return False

    def cleanup(self, files: List[str], folder: Optional[str] = None) -> None:
        """
        Cleans up files and optionally a folder.

        Args:
            files (List[str]): List of file paths to delete.
            folder (Optional[str], optional): Folder path to delete. Defaults to None.
        """
        log_step("A5_base_pipeline.py", "Cleanup starting", "ok")
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)
        if folder and os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
        log_step("A5_base_pipeline.py", "Cleanup done", "ok")
