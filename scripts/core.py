#!/usr/bin/env python3
"""
📄 FILE:      core.py
📁 PATH:      scripts/core.py
🎯 PURPOSE:   Core modules — Config, Logger, Telegram, Utils, Pipeline, Secrets, Fonts
"""

import os

ROOT = "Sawaj_studio"
CODE = {}

# ═══════════════════════════════════════════════════════════
# 📁 1_CONFIG
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/1_config/__init__.py"] = '"""Config Module"""\n'

CODE[f"{ROOT}/generator/1_config/1_env_loader.py"] = '''"""
🔧 Env Loader
"""
import os


def load_env(env_path=".env"):
    if not os.path.exists(env_path):
        return False
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
        return True
    except Exception:
        return False


def get_env(key, default=""):
    return os.environ.get(key, default).strip()
'''

CODE[f"{ROOT}/generator/1_config/2_secret_reader.py"] = '''"""
🔑 Secret Reader
"""
import os


def read_secret(*names, default=""):
    for name in names:
        val = os.environ.get(name, "").strip()
        if val and val.lower() not in ("none", "null", "undefined"):
            return val
    return default


def has_secret(*names):
    return bool(read_secret(*names))


def mask_secret(value):
    if not value:
        return "(empty)"
    if len(value) <= 8:
        return "***"
    return value[:4] + "***" + value[-4:]
'''

CODE[f"{ROOT}/generator/1_config/3_path_builder.py"] = '''"""
📁 Path Builder
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(_HERE))

GENERATOR_DIR = os.path.join(ROOT_DIR, "generator")
UPLOADER_DIR = os.path.join(ROOT_DIR, "uploader")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


def build_path(*parts):
    return os.path.join(*parts)


def ensure_path(path):
    os.makedirs(path, exist_ok=True)
    return path
'''

CODE[f"{ROOT}/generator/1_config/4_mode_decider.py"] = '''"""
🎯 Mode Decider
"""
import os


def get_mode():
    event = os.environ.get("GITHUB_EVENT_NAME", "").strip()
    mode = os.environ.get("UPLOAD_MODE", "offline").strip().lower()
    confirmed = os.environ.get("UPLOAD_CONFIRMED", "false").strip().lower() == "true"
    if event == "schedule":
        return "online"
    if mode == "online" and confirmed:
        return "online"
    return "offline"


def is_online():
    return get_mode() == "online"


def is_offline():
    return get_mode() == "offline"


def get_worker():
    return os.environ.get("WORKER", "story").strip().lower()
'''

CODE[f"{ROOT}/generator/1_config/5_folder_creator.py"] = '''"""
📁 Folder Creator
"""
import os


def create_all_folders():
    folders = ["output/story", "output/short", "output/long",
               "output/temp", "output/logs"]
    result = {}
    for f in folders:
        os.makedirs(f, exist_ok=True)
        result[f] = f
    return result


def create_worker_folders(worker):
    frames = {"story": "s_frames", "short": "p_frames", "long": "l_frames"}.get(worker, "s_frames")
    out = {"story": "output/story", "short": "output/short", "long": "output/long"}.get(worker, "output/story")
    os.makedirs(frames, exist_ok=True)
    os.makedirs(os.path.join(out, "final"), exist_ok=True)
    os.makedirs(os.path.join(out, "temp"), exist_ok=True)
    return {"frames": frames, "output": out}
'''

CODE[f"{ROOT}/generator/1_config/6_default_settings.py"] = '''"""
⚙️ Default Settings
"""
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 25
VIDEO_CRF = 20
LONG_VIDEO_WIDTH = 1920
LONG_VIDEO_HEIGHT = 1080
AUDIO_VOICE = "hi-IN-MadhurNeural"
AUDIO_RATE = "-7%"
AUDIO_PITCH = "-2Hz"
AUDIO_VOLUME = "+8%"
MUSIC_VOL_STORY = 0.20
MUSIC_VOL_SHORT = 0.22
MUSIC_VOL_LONG = 0.18
STORY_WORDS_MIN = 50
STORY_WORDS_MAX = 100
SHORT_WORDS_MIN = 150
SHORT_WORDS_MAX = 400
LONG_WORDS_MIN = 400
LONG_WORDS_MAX = 1800
HTTP_TIMEOUT = 30
TTS_TIMEOUT = 120
UPLOAD_TIMEOUT = 3600
'''

CODE[f"{ROOT}/generator/1_config/7_platform_config.py"] = '''"""
📤 Platform Config
"""
PLATFORMS = {
    "youtube": {"api_version": "v3", "category_id": "22"},
    "facebook": {"api_version": "v21.0"},
    "instagram": {"api_version": "v21.0"},
}
WORKER_PLATFORMS = {
    "story": ["facebook", "instagram"],
    "short": ["facebook", "instagram", "youtube"],
    "long": ["facebook", "youtube"],
}


def get_platform_config(name):
    return PLATFORMS.get(name, {})


def get_worker_platforms(worker):
    return WORKER_PLATFORMS.get(worker, [])
'''

CODE[f"{ROOT}/generator/1_config/8_worker_selector.py"] = '''"""
👷 Worker Selector
"""
import os
WORKERS = {
    "story": {"duration": "50-60s", "words": "50-100", "music_dur": 60},
    "short": {"duration": "1-3 min", "words": "150-400", "music_dur": 200},
    "long": {"duration": "5-15 min", "words": "400-1800", "music_dur": 900},
}


def select_worker(name=None):
    if not name:
        name = os.environ.get("WORKER", "story").strip().lower()
    if name not in WORKERS:
        raise ValueError("Unknown worker: " + name)
    cfg = WORKERS[name].copy()
    cfg["key"] = name
    return cfg


def list_workers():
    return list(WORKERS.keys())
'''

CODE[f"{ROOT}/generator/1_config/9_validation.py"] = '''"""
✅ Validation
"""
from .2_secret_reader import has_secret
from .8_worker_selector import list_workers


def validate_secrets(worker="story"):
    critical = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
    missing = [k for k in critical if not has_secret(k)]
    return {"valid": len(missing) == 0, "missing": missing}


def validate_worker(name):
    return name in list_workers()
'''

# ═══════════════════════════════════════════════════════════
# 📝 2_LOGGER
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/2_logger/__init__.py"] = '"""Logger Module"""\n'

CODE[f"{ROOT}/generator/2_logger/1_console_logger.py"] = '''"""
📺 Console Logger
"""
from datetime import datetime
ICONS = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERROR": "❌", "STEP": "🔹"}


def console_log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    icon = ICONS.get(level.upper(), "•")
    print("[" + ts + "] " + icon + " " + msg, flush=True)


def info(msg): console_log(msg, "INFO")
def ok(msg): console_log(msg, "OK")
def warn(msg): console_log(msg, "WARN")
def error(msg): console_log(msg, "ERROR")
def step(msg): console_log(msg, "STEP")
'''

CODE[f"{ROOT}/generator/2_logger/2_file_logger.py"] = '''"""
📁 File Logger
"""
import os
from datetime import datetime
LOG_DIR = "output/logs"


def _log_file():
    os.makedirs(LOG_DIR, exist_ok=True)
    d = datetime.now().strftime("%Y%m%d")
    return os.path.join(LOG_DIR, "sawaj_" + d + ".log")


def file_log(msg, level="INFO"):
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(_log_file(), "a", encoding="utf-8") as f:
            f.write("[" + ts + "] [" + level.upper() + "] " + msg + "\\n")
    except Exception:
        pass


def read_log_file(lines=100):
    p = _log_file()
    if not os.path.exists(p):
        return ""
    with open(p, encoding="utf-8") as f:
        return "".join(f.readlines()[-lines:])
'''

CODE[f"{ROOT}/generator/2_logger/3_timestamp.py"] = '''"""
⏰ Timestamp
"""
from datetime import datetime, timezone


def now_hms():
    return datetime.now().strftime("%H:%M:%S")


def now_ymd():
    return datetime.now().strftime("%Y%m%d")


def now_ymdhms():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def elapsed_str(seconds):
    if seconds < 60:
        return str(round(seconds, 1)) + "s"
    return str(int(seconds // 60)) + "m " + str(int(seconds % 60)) + "s"
'''

CODE[f"{ROOT}/generator/2_logger/4_log_levels.py"] = '''"""
📊 Log Levels
"""
DEBUG = "DEBUG"
INFO = "INFO"
OK = "OK"
WARN = "WARN"
ERROR = "ERROR"
STEP = "STEP"
API = "API"
'''

CODE[f"{ROOT}/generator/2_logger/5_error_tracker.py"] = '''"""
🚨 Error Tracker
"""
import traceback
from datetime import datetime
ERRORS = []


def track_error(module, error, include_traceback=False):
    entry = {
        "module": module, "error": str(error)[:500],
        "type": type(error).__name__,
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    if include_traceback:
        entry["traceback"] = traceback.format_exc()[:2000]
    ERRORS.append(entry)


def get_errors():
    return ERRORS.copy()


def get_error_count():
    return len(ERRORS)


def clear_errors():
    ERRORS.clear()
'''

CODE[f"{ROOT}/generator/2_logger/6_step_logger.py"] = '''"""
🔹 Step Logger
"""
import time
STEPS = []
TIMES = {}


def step_start(name):
    TIMES[name] = time.time()
    print("🔹 START: " + name, flush=True)


def step_end(name, success=True, note=""):
    elapsed = time.time() - TIMES.get(name, time.time())
    STEPS.append({"name": name, "success": success, "elapsed": elapsed, "note": note})
    icon = "✅" if success else "❌"
    print(icon + " END: " + name + " (" + str(round(elapsed, 1)) + "s) " + note, flush=True)


def get_steps():
    return STEPS.copy()


def get_step_summary():
    total = len(STEPS)
    success = sum(1 for s in STEPS if s["success"])
    return {"total": total, "success": success, "failed": total - success}
'''

CODE[f"{ROOT}/generator/2_logger/7_api_logger.py"] = '''"""
🌐 API Logger
"""
from datetime import datetime
API_LOGS = []


def log_api(name, status, detail="", code=None):
    API_LOGS.append({
        "name": name, "status": status.lower(),
        "detail": detail[:200], "code": code,
        "time": datetime.now().strftime("%H:%M:%S"),
    })


def get_api_logs():
    return API_LOGS.copy()


def get_api_summary():
    summary = {"success": 0, "failed": 0, "fallback": 0, "skipped": 0}
    for e in API_LOGS:
        if e["status"] in summary:
            summary[e["status"]] += 1
    summary["total"] = len(API_LOGS)
    return summary
'''

CODE[f"{ROOT}/generator/2_logger/8_buffer.py"] = '''"""
📦 Buffer
"""
BUFFER = []


def add(line):
    if line:
        BUFFER.append(line)


def add_many(lines):
    BUFFER.extend(lines)


def get_text():
    return "\\n".join(BUFFER)


def get_chunks(max_len=3800):
    chunks = []
    current = ""
    for line in BUFFER:
        if len(current) + len(line) + 1 > max_len:
            if current:
                chunks.append(current)
            current = line
        else:
            current += ("\\n" if current else "") + line
    if current:
        chunks.append(current)
    return chunks


def clear():
    BUFFER.clear()


def size():
    return len(BUFFER)
'''

# ═══════════════════════════════════════════════════════════
# 📱 3_TELEGRAM
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/3_telegram/__init__.py"] = '"""Telegram Module"""\n'

CODE[f"{ROOT}/generator/3_telegram/1_bot_sender.py"] = '''"""
📱 Telegram Bot Sender
"""
import os
import requests


def send_message(text, parse_mode="HTML"):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat:
        return False
    try:
        r = requests.post(
            "https://api.telegram.org/bot" + token + "/sendMessage",
            json={"chat_id": chat, "text": text[:4000], "parse_mode": parse_mode},
            timeout=15)
        return r.status_code == 200
    except Exception:
        return False


def send_document(path, caption=""):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat or not os.path.exists(path):
        return False
    try:
        with open(path, "rb") as f:
            r = requests.post(
                "https://api.telegram.org/bot" + token + "/sendDocument",
                data={"chat_id": chat, "caption": caption, "parse_mode": "HTML"},
                files={"document": f}, timeout=60)
        return r.status_code == 200
    except Exception:
        return False
'''

CODE[f"{ROOT}/generator/3_telegram/2_message_builder.py"] = '''"""
📝 Message Builder
"""


def build_status(title, lines):
    msg = "<b>" + title + "</b>\\n"
    msg += "━━━━━━━━━━━━━━━━━━━\\n"
    for line in lines:
        msg += line + "\\n"
    return msg


def build_simple(title, message):
    return "<b>" + title + "</b>\\n\\n" + message
'''

CODE[f"{ROOT}/generator/3_telegram/3_html_formatter.py"] = '''"""
🎨 HTML Formatter
"""


def bold(text): return "<b>" + str(text) + "</b>"
def italic(text): return "<i>" + str(text) + "</i>"
def code(text): return "<code>" + str(text) + "</code>"
def link(url, text): return "<a href='" + url + "'>" + text + "</a>"
'''

CODE[f"{ROOT}/generator/3_telegram/4_document_sender.py"] = '''"""
📄 Document Sender
"""
from .1_bot_sender import send_document


def send_report(path, caption="Report"):
    return send_document(path, caption)


def send_log_file(path):
    return send_document(path, "📋 Log File")
'''

CODE[f"{ROOT}/generator/3_telegram/5_error_report.py"] = '''"""
🚨 Error Report
"""
from .1_bot_sender import send_message


def report_error(module, error):
    msg = "❌ <b>ERROR</b>\\n\\n<b>Module:</b> " + str(module)
    msg += "\\n<b>Error:</b> " + str(error)[:200]
    return send_message(msg)


def report_warning(module, warning):
    msg = "⚠️ <b>WARNING</b>\\n\\n<b>Module:</b> " + str(module)
    msg += "\\n<b>Message:</b> " + str(warning)[:200]
    return send_message(msg)
'''

CODE[f"{ROOT}/generator/3_telegram/6_summary_sender.py"] = '''"""
📊 Summary Sender
"""
from .1_bot_sender import send_message


def send_summary(success, failed, total_time):
    icon = "🎉" if failed == 0 else "⚠️"
    msg = icon + " <b>RUN COMPLETE</b>\\n"
    msg += "━━━━━━━━━━━━━━━━━━━\\n"
    msg += "✅ Success: <b>" + str(success) + "</b>\\n"
    msg += "❌ Failed: <b>" + str(failed) + "</b>\\n"
    msg += "⏱️ Time: <b>" + str(round(total_time, 1)) + "s</b>"
    return send_message(msg)


def send_detailed_summary(stats):
    lines = ["📊 <b>DETAILED SUMMARY</b>", "━━━━━━━━━━━━━━━━━━━"]
    for k, v in stats.items():
        lines.append("• " + str(k) + ": <b>" + str(v) + "</b>")
    return send_message("\\n".join(lines))
'''

CODE[f"{ROOT}/generator/3_telegram/7_chunk_splitter.py"] = '''"""
✂️ Chunk Splitter
"""


def split_message(text, max_len=3800):
    chunks = []
    current = ""
    for line in text.split("\\n"):
        if len(current) + len(line) + 1 > max_len:
            chunks.append(current)
            current = line
        else:
            current += ("\\n" if current else "") + line
    if current:
        chunks.append(current)
    return chunks


def send_long_message(send_func, text):
    for chunk in split_message(text):
        send_func(chunk)
'''

# ═══════════════════════════════════════════════════════════
# 🧰 4_UTILS
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/4_utils/__init__.py"] = '"""Utils Module"""\n'

CODE[f"{ROOT}/generator/4_utils/1_sanitizer.py"] = '''"""
🧹 Sanitizer
"""
import re


def sanitize(text):
    if not text:
        return ""
    text = re.sub(r"[\\u200b-\\u200f\\ufeff\\u202a-\\u202e]", "", str(text))
    return text.replace(chr(34), "").replace(chr(39), "").replace("\\n", " ").strip()


def remove_quotes(text):
    if not text:
        return ""
    return str(text).replace('"', "").replace("'", "").strip()
'''

CODE[f"{ROOT}/generator/4_utils/2_file_helper.py"] = '''"""
📁 File Helper
"""
import os
import shutil


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def file_size_mb(path):
    if not os.path.exists(path):
        return 0
    return os.path.getsize(path) / 1024 / 1024


def file_exists(path):
    return os.path.exists(path)
'''

CODE[f"{ROOT}/generator/4_utils/3_time_helper.py"] = '''"""
⏱️ Time Helper
"""
import time
from datetime import datetime


def timer_start():
    return time.time()


def timer_elapsed(start):
    return time.time() - start


def format_duration(seconds):
    if seconds < 60:
        return str(round(seconds, 1)) + "s"
    m = int(seconds // 60)
    s = int(seconds % 60)
    return str(m) + "m " + str(s) + "s"


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
'''

CODE[f"{ROOT}/generator/4_utils/4_random_helper.py"] = '''"""
🎲 Random Helper
"""
import random
import string


def random_string(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def random_choice(items):
    return random.choice(items) if items else None


def random_int(min_val, max_val):
    return random.randint(min_val, max_val)


def shuffle_list(items):
    items = list(items)
    random.shuffle(items)
    return items
'''

CODE[f"{ROOT}/generator/4_utils/5_json_helper.py"] = '''"""
📋 JSON Helper
"""
import json


def read_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def json_to_string(data):
    try:
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        return "{}"
'''

CODE[f"{ROOT}/generator/4_utils/6_hash_helper.py"] = '''"""
🔐 Hash Helper
"""
import hashlib


def md5(text):
    return hashlib.md5(str(text).encode()).hexdigest()


def sha256(text):
    return hashlib.sha256(str(text).encode()).hexdigest()


def short_hash(text, length=8):
    return sha256(text)[:length]
'''

CODE[f"{ROOT}/generator/4_utils/7_text_cleaner.py"] = '''"""
🧼 Text Cleaner
"""
import re


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\\s+", " ", text)
    return text.strip()


def truncate(text, max_len=100):
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
'''

# ═══════════════════════════════════════════════════════════
# 🌐 5_BASE_PIPELINE
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/5_base_pipeline/__init__.py"] = '"""Pipeline Module"""\n'

CODE[f"{ROOT}/generator/5_base_pipeline/1_http_session.py"] = '''"""
🌐 HTTP Session
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_session():
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1.5,
                  status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_headers(content_type="application/json"):
    return {"Content-Type": content_type}
'''

CODE[f"{ROOT}/generator/5_base_pipeline/2_downloader.py"] = '''"""
⬇️ Downloader
"""
import requests


def download(url, path, min_size=12000, timeout=35):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200 and len(r.content) > min_size:
            with open(path, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False


def download_with_session(session, url, path, min_size=12000):
    try:
        r = session.get(url, timeout=35)
        if r.status_code == 200 and len(r.content) > min_size:
            with open(path, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False
'''

CODE[f"{ROOT}/generator/5_base_pipeline/3_cleanup.py"] = '''"""
🧹 Cleanup
"""
import os
import shutil


def cleanup_files(files):
    for f in files:
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass


def cleanup_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
'''

CODE[f"{ROOT}/generator/5_base_pipeline/4_cmd_runner.py"] = '''"""
▶️ Command Runner
"""
import subprocess


def run_cmd(cmd, timeout=1800):
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                                capture_output=True, text=True, timeout=timeout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, str(e)[:200]
    except subprocess.TimeoutExpired:
        return False, "Timeout"


def run_cmd_silent(cmd, timeout=1800):
    try:
        subprocess.run(cmd, shell=True, check=True,
                       capture_output=True, timeout=timeout)
        return True
    except Exception:
        return False
'''

CODE[f"{ROOT}/generator/5_base_pipeline/5_retry_handler.py"] = '''"""
🔄 Retry Handler
"""
import time
from functools import wraps


def retry(max_attempts=3, delay=2, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator
'''

CODE[f"{ROOT}/generator/5_base_pipeline/6_progress_tracker.py"] = '''"""
📊 Progress Tracker
"""
PROGRESS = {"current": 0, "total": 100}


def set_total(n):
    PROGRESS["total"] = n
    PROGRESS["current"] = 0


def update(n=1):
    PROGRESS["current"] += n


def get_percent():
    total = PROGRESS.get("total", 100)
    if total == 0:
        return 0
    return int(100 * PROGRESS["current"] / total)


def reset():
    PROGRESS["current"] = 0
    PROGRESS["total"] = 100
'''

# ═══════════════════════════════════════════════════════════
# 🔐 6_SECRETS_CHECK
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/6_secrets_check/__init__.py"] = '"""Secrets Module"""\n'

CODE[f"{ROOT}/generator/6_secrets_check/1_env_checker.py"] = '''"""
🔐 Env Checker
"""
import os


def check_env(*keys):
    missing = [k for k in keys if not os.environ.get(k, "").strip()]
    return {"valid": len(missing) == 0, "missing": missing}


def check_any(*keys):
    for k in keys:
        if os.environ.get(k, "").strip():
            return True
    return False


def get_all_env():
    return {k: v for k, v in os.environ.items() if "API" in k or "TOKEN" in k}
'''

CODE[f"{ROOT}/generator/6_secrets_check/2_api_tester.py"] = '''"""
🌐 API Tester
"""
import requests


def test_url(url, headers=None, timeout=10):
    try:
        r = requests.get(url, headers=headers or {}, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False


def test_post(url, headers=None, data=None, timeout=10):
    try:
        r = requests.post(url, headers=headers or {}, json=data or {}, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False
'''

CODE[f"{ROOT}/generator/6_secrets_check/3_fallback_checker.py"] = '''"""
🔄 Fallback Checker
"""


def check_fallback(providers):
    return [p for p in providers if p]


def count_working(providers):
    return sum(1 for p in providers if p)


def has_any(providers):
    return any(providers)
'''

CODE[f"{ROOT}/generator/6_secrets_check/4_health_report.py"] = '''"""
💚 Health Report
"""


def build_health(checks):
    ok = sum(1 for v in checks.values() if v)
    total = len(checks)
    percent = int(100 * ok / total) if total else 0
    return {"ok": ok, "total": total, "percent": percent}


def format_health(report):
    return f"{report['ok']}/{report['total']} ({report['percent']}%)"
'''

CODE[f"{ROOT}/generator/6_secrets_check/5_critical_checker.py"] = '''"""
🚨 Critical Checker
"""
CRITICAL = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]


def check_critical(env_dict):
    return [k for k in CRITICAL if not env_dict.get(k)]


def is_all_critical_present(env_dict):
    return len(check_critical(env_dict)) == 0
'''

# ═══════════════════════════════════════════════════════════
# 🔤 7_FONTS
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/7_fonts/__init__.py"] = '"""Fonts Module"""\n'

CODE[f"{ROOT}/generator/7_fonts/1_font_loader.py"] = '''"""
🔤 Font Loader
"""
import os
from PIL import ImageFont


def load_font(path, size):
    try:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    except Exception:
        pass
    return ImageFont.load_default()


def load_font_safe(path, size, fallback=None):
    font = load_font(path, size)
    if font is None and fallback:
        return load_font(fallback, size)
    return font
'''

CODE[f"{ROOT}/generator/7_fonts/2_font_cache.py"] = '''"""
💾 Font Cache
"""
_CACHE = {}


def get_cached(path, size):
    return _CACHE.get((path, size))


def set_cached(path, size, font):
    _CACHE[(path, size)] = font


def clear_cache():
    _CACHE.clear()


def cache_size():
    return len(_CACHE)
'''

CODE[f"{ROOT}/generator/7_fonts/3_path_finder.py"] = '''"""
🔍 Path Finder
"""
import os

BASE_DIRS = [
    os.path.expanduser("~/.fonts"),
    "/usr/share/fonts/truetype/noto",
    "/usr/share/fonts/truetype/dejavu",
    "/Library/Fonts",
    "C:/Windows/Fonts",
]


def find_font(name):
    for d in BASE_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


def find_first(names):
    for n in names:
        p = find_font(n)
        if p:
            return p
    return None
'''

CODE[f"{ROOT}/generator/7_fonts/4_fallback_font.py"] = '''"""
🔄 Fallback Font
"""
from .3_path_finder import find_font

FALLBACKS = ["DejaVuSans.ttf", "Arial.ttf", "NotoSans-Regular.ttf"]


def get_fallback():
    for f in FALLBACKS:
        p = find_font(f)
        if p:
            return p
    return None
'''

CODE[f"{ROOT}/generator/7_fonts/5_hindi_font.py"] = '''"""
🇮🇳 Hindi Font
"""
from .3_path_finder import find_font

FONTS = ["NotoSansDevanagari-Bold.ttf", "NotoSansDevanagari-Regular.ttf"]


def get_hindi_font():
    for f in FONTS:
        p = find_font(f)
        if p:
            return p
    return None
'''

CODE[f"{ROOT}/generator/7_fonts/6_arabic_font.py"] = '''"""
🇸🇦 Arabic Font
"""
from .3_path_finder import find_font

FONTS = ["NotoNaskhArabic-Bold.ttf", "NotoNaskhArabic-Regular.ttf"]


def get_arabic_font():
    for f in FONTS:
        p = find_font(f)
        if p:
            return p
    return None
'''

CODE[f"{ROOT}/generator/7_fonts/7_english_font.py"] = '''"""
🇬🇧 English Font
"""
from .3_path_finder import find_font

FONTS = ["NotoSans-Bold.ttf", "NotoSans-Regular.ttf", "DejaVuSans-Bold.ttf"]


def get_english_font():
    for f in FONTS:
        p = find_font(f)
        if p:
            return p
    return None
'''

# ═══════════════════════════════════════════════════════════
# 🏗️ WRITE ALL
# ═══════════════════════════════════════════════════════════

def write_all():
    written = 0
    skipped = 0
    for path, code in CODE.items():
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if os.path.exists(path):
            try:
                size = os.path.getsize(path)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if size > 100 and "Sawaj Studio Module" not in content:
                    skipped += 1
                    continue
            except Exception:
                pass
        with open(path, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        written += 1
    print("=" * 60)
    print(f"💻 core.py — Written: {written} | Skipped: {skipped}")
    print("=" * 60)
    return written, skipped


if __name__ == "__main__":
    print("=" * 60)
    print("🏗️  SAWAJ STUDIO — CORE")
    print("=" * 60)
    write_all()
    print("🎉 CORE COMPLETE")
