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
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_error


class BasePipeline:

    def __init__(self):
        log_file_start("A5_base_pipeline.py", "Setup session + tracker")
        self.cfg = Config()
        self.session = requests.Session()
        retry = Retry(total=5, backoff_factor=1.5,
                      status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

        self.api_status = {
            "AI": {}, "TTS": {}, "Music": {}, "Background": {},
            "Translation": {}, "Hadith": {}, "Drive": {},
            "Facebook": {}, "Instagram": {}, "YouTube": {},
        }
        log_file_end("A5_base_pipeline.py", "success", "Session ready")

    def run_cmd(self, cmd):
        log_step("A5_base_pipeline.py", f"CMD: {cmd[:80]}", "ok")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            log_error("A5_base_pipeline.py", f"CMD failed: {str(e)[:120]}")
            raise

    def download(self, url, path, min_size=12000):
        try:
            r = self.session.get(url, timeout=35)
            if r.status_code == 200 and len(r.content) > min_size:
                with open(path, "wb") as f:
                    f.write(r.content)
                log_step("A5_base_pipeline.py", f"Download OK: {path}", "ok",
                         f"{len(r.content) // 1024} KB")
                return True
        except Exception as e:
            log_step("A5_base_pipeline.py", f"Download err", "fail", str(e)[:60])
        return False

    def cleanup(self, files, folder=None):
        log_step("A5_base_pipeline.py", "Cleanup starting", "ok")
        for f in files:
            if os.path.exists(f):
                os.remove(f)
        if folder:
            shutil.rmtree(folder, ignore_errors=True)
        log_step("A5_base_pipeline.py", "Cleanup done", "ok")
