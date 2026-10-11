"""
U4_base_pipeline.py — Universal Base Pipeline
==============================================
Parametrized via constructor — each generator passes its own api_status keys.

Fixes:
  • run_cmd logs stderr (FFmpeg diagnostics)
  • download() retries (2x)
  • Session with User-Agent + retry adapter
  • cleanup() counter
"""

import os
import subprocess
import shutil
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from A_core.A1_config import Config
from universal.U1_logger import (log_file_start, log_file_end,
                                  log_step, log_error)


class BasePipeline:

    DEFAULT_STATUS_KEYS = [
        "AI", "TTS", "Music", "Background",
        "Translation", "Hadith", "Drive",
        "Facebook", "Instagram", "YouTube",
    ]

    def __init__(self, extra_status_keys=None):
        log_file_start("A5_base_pipeline.py", "Setup session + tracker")
        self.cfg = Config()
        self.session = requests.Session()

        retry = Retry(total=5, backoff_factor=1.5,
                      status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.headers.update({
            "User-Agent": "SawajStudioBot/2.0 (+github.com/SAWAJ-STUDIO-LAB)"
        })

        keys = list(self.DEFAULT_STATUS_KEYS)
        if extra_status_keys:
            keys += extra_status_keys
        self.api_status = {k: {} for k in keys}

        log_file_end("A5_base_pipeline.py", "success", "Session ready")

    def run_cmd(self, cmd):
        log_step("A5_base_pipeline.py", f"CMD: {cmd[:80]}", "ok")
        try:
            result = subprocess.run(
                cmd, shell=True, check=True,
                capture_output=True, text=True)
            if result.stderr:
                last_lines = result.stderr.strip().split("\n")[-3:]
                log_step("A5_base_pipeline.py",
                         "cmd output", "info",
                         " | ".join(last_lines)[:200])
        except subprocess.CalledProcessError as e:
            err_msg = (e.stderr or "")[:200]
            log_error("A5_base_pipeline.py",
                      f"CMD failed: {str(e)[:120]} | {err_msg}")
            raise

    def download(self, url, path, min_size=12000, retries=2):
        for attempt in range(1, retries + 1):
            try:
                r = self.session.get(url, timeout=35)
                if r.status_code == 200 and len(r.content) > min_size:
                    with open(path, "wb") as f:
                        f.write(r.content)
                    log_step("A5_base_pipeline.py",
                             f"Download OK: {path}", "ok",
                             f"{len(r.content)//1024} KB")
                    return True
                log_step("A5_base_pipeline.py",
                         f"Download small ({attempt}/{retries})", "warn")
            except Exception as e:
                log_step("A5_base_pipeline.py",
                         f"Download err ({attempt}/{retries})", "warn",
                         str(e)[:60])
        return False

    def cleanup(self, files, folder=None):
        log_step("A5_base_pipeline.py", "Cleanup starting", "ok")
        removed = 0
        for f in files:
            if os.path.exists(f):
                try:
                    os.remove(f)
                    removed += 1
                except Exception:
                    pass
        if folder and os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
        log_step("A5_base_pipeline.py", "Cleanup done", "ok",
                 f"{removed} files removed")
