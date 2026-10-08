"""
1send code.py
A_core module ki saari files mein code daalta hai.
"""
import os

BASE = "sawajstudiobot/video_generator/fb_ig_story_video_generator/A_core"

FILES = {

    "A1_env_loader.py": '''"""
A1_env_loader.py
Sirf env var load karna.
"""
import os


def get_env(name, default=""):
    """Get env var and strip whitespace."""
    return os.environ.get(name, default).strip()
''',

    "A2_env_fallback.py": '''"""
A2_env_fallback.py
Sirf multi-name fallback.
"""
import os


def get_env_fallback(*names, default=""):
    """Try multiple env names, return first non-empty."""
    for name in names:
        val = os.environ.get(name, "").strip()
        if val:
            return val
    return default
''',

    "A3_config_class.py": '''"""
A3_config_class.py
Sirf Config class.
"""
from A_core.A1_env_loader import get_env
from A_core.A2_env_fallback import get_env_fallback


class Config:
    """Story generator config — offline/online upload system."""

    # ─── Telegram ───
    TG_TOKEN = get_env("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = get_env("TELEGRAM_CHAT_ID")

    # ─── Facebook ───
    META_TOKEN = get_env_fallback(
        "FACEBOOK_META_TOKEN",
        "FACEBOOK_INSTAGRAM_META_TOKEN",
    )
    PAGE_ID = get_env("FACEBOOK_PAGE_ID")

    # ─── Instagram ───
    IG_TOKEN = get_env_fallback(
        "FACEBOOK_INSTAGRAM_META_TOKEN",
        "FACEBOOK_META_TOKEN",
    )
    IG_BUSINESS_ID = get_env("INSTAGRAM_BUSINESS_ACCOUNT_ID")

    # ─── YouTube ───
    YT_CLIENT_ID = get_env("YOUTUBE_CLIENT_ID")
    YT_CLIENT_SECRET = get_env("YOUTUBE_CLIENT_SECRET")
    YT_REFRESH_TOKEN = get_env("YOUTUBE_REFRESH_TOKEN")
    YT_PLAYLIST_ID = get_env("DAILY_HADEES_YT_PLAYLIST_ID")

    # ─── Drive ───
    DRIVE_CLIENT_ID = get_env("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = get_env("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = get_env("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_STORY_FOLDER_ID = get_env_fallback(
        "GDRIVE_STORY_VIDEO_FOLDER_ID",
        "GDRIVE_SHORT_VIDEO_FOLDER_ID",
    )

    # ─── AI Providers ───
    OPENROUTER_API_KEY = get_env_fallback(
        "OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
    GROQ_API_KEY = get_env_fallback(
        "GROQ_API_KEY", "GROQ_API_KEY_AI")
    GEMINI_API_KEY = get_env_fallback(
        "GEMINI_API_KEY", "GEMINI_API_KEY_AI")
    MISTRAL_API_KEY = get_env_fallback(
        "MISTRAL_API_KEY", "MISTRAL_API_KEY_AI")
    CEREBRAS_API_KEY = get_env_fallback(
        "CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI")
    COHERE_API_KEY = get_env_fallback(
        "COHERE_API_KEY", "COHERE_API_KEY_AI")
    HUGGINGFACE_API_KEY = get_env_fallback(
        "HUGGINGFACE_API_KEY", "HUGGINGFACE_API_KEY_AI")

    # ─── TTS / Translation ───
    ELEVENLABS_API_KEY = get_env("ELEVENLABS_API_KEY")
    DEEPL_API_KEY = get_env("DEEPL_API_KEY")

    # ─── Media ───
    PEXELS_API_KEY = get_env("PEXELS_API_KEY")
    PIXABAY_API_KEY = get_env("PIXABAY_API_KEY")
    FREESOUND_API_KEY = get_env("FREESOUND_API_KEY")

    # ─── Hadith ───
    HADITH_API_URL = get_env("HADITH_API_URL")

    # ─── Runtime ───
    EVENT_NAME = get_env("GITHUB_EVENT_NAME")
    UPLOAD_TARGET = get_env("UPLOAD_TARGET", default="drive_only").lower()
    CONFIRM_UPLOAD = get_env("CONFIRM_UPLOAD", default="false").lower() == "true"
''',

    "A4_upload_decider.py": '''"""
A4_upload_decider.py
Sirf upload decisions.
"""
from A_core.A3_config_class import Config


def decide(cfg: Config = None) -> dict:
    """Return which platforms to upload to."""
    if cfg is None:
        cfg = Config()

    is_scheduled = cfg.EVENT_NAME == "schedule"
    is_confirmed = True if is_scheduled else cfg.CONFIRM_UPLOAD

    return {
        "drive": True,
        "facebook": (is_scheduled or is_confirmed) and
                    cfg.UPLOAD_TARGET in ("fb_ig", "all"),
        "instagram": (is_scheduled or is_confirmed) and
                     cfg.UPLOAD_TARGET in ("fb_ig", "all"),
        "youtube": (not is_scheduled) and is_confirmed and
                   cfg.UPLOAD_TARGET in ("youtube", "all"),
    }
''',

    "A5_platform_checker.py": '''"""
A5_platform_checker.py
Sirf available platforms check.
"""
from A_core.A3_config_class import Config


def available_platforms(cfg: Config = None) -> list:
    """Return platforms with valid credentials."""
    if cfg is None:
        cfg = Config()

    platforms = []
    if cfg.META_TOKEN and cfg.PAGE_ID:
        platforms.append("facebook")
    if cfg.IG_TOKEN and cfg.IG_BUSINESS_ID:
        platforms.append("instagram")
    if all([cfg.YT_CLIENT_ID, cfg.YT_CLIENT_SECRET, cfg.YT_REFRESH_TOKEN]):
        platforms.append("youtube")
    return platforms
''',

    "A6_print_logger.py": '''"""
A6_print_logger.py
Sirf print karna.
"""
from datetime import datetime


def log(msg, level="INFO"):
    """Print with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)
''',

    "A7_log_file_start.py": '''"""
A7_log_file_start.py
Sirf module start logging.
"""
from A_core.A6_print_logger import log


def log_file_start(name, purpose=""):
    """Log start of a module."""
    log(f"→ START {name}")
    try:
        from A_core.A17_tg_file_start import file_start
        file_start(name, purpose)
    except Exception:
        pass
''',

    "A8_log_file_end.py": '''"""
A8_log_file_end.py
Sirf module end logging.
"""
from A_core.A6_print_logger import log


def log_file_end(name, status="success", note=""):
    """Log end of a module."""
    log(f"← END {name} ({status})")
    try:
        from A_core.A18_tg_file_end import file_end
        file_end(name, status, note)
    except Exception:
        pass
''',

    "A9_log_step.py": '''"""
A9_log_step.py
Sirf step logging.
"""
from A_core.A6_print_logger import log


def log_step(name, action, result="ok", detail=""):
    """Log a specific step."""
    log(f"  • {name} :: {action} → {result} {detail}")
    try:
        from A_core.A19_tg_step import step
        step(name, action, result, detail)
    except Exception:
        pass
''',

    "A10_log_api.py": '''"""
A10_log_api.py
Sirf API call logging.
"""
from A_core.A6_print_logger import log


def log_api(name, api, status, detail=""):
    """Log API call."""
    log(f"  ★ {name} :: {api} → {status}")
    try:
        from A_core.A20_tg_api_call import api_call
        api_call(name, api, status, detail)
    except Exception:
        pass
''',

    "A11_log_error.py": '''"""
A11_log_error.py
Sirf error logging.
"""
from A_core.A6_print_logger import log


def log_error(name, error, tb=""):
    """Log error."""
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    try:
        from A_core.A21_tg_file_error import file_error
        file_error(name, error, tb)
    except Exception:
        pass
''',

    "A12_tg_session.py": '''"""
A12_tg_session.py
Sirf requests session.
"""
import requests

session = requests.Session()
''',

    "A13_tg_buffer.py": '''"""
A13_tg_buffer.py
Sirf log buffer + counters.
"""
import time

LOG_BUFFER = []
FILE_TIMERS = {}
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}
START_TIME = [None]
RUN_HEADER = ["📖 STORY VIDEO RUN"]


def now():
    """Current time HH:MM:SS."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")


def reset():
    """Reset all buffers."""
    global LOG_BUFFER
    LOG_BUFFER.clear()
    FILE_TIMERS.clear()
    STEP_COUNTER.update({"total": 0, "success": 0, "failed": 0})
    START_TIME[0] = time.time()
''',

    "A14_tg_creds.py": '''"""
A14_tg_creds.py
Sirf Telegram credentials.
"""
import os


def get_creds():
    """Return (token, chat_id)."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    return token, chat_id
''',

    "A15_tg_send_raw.py": '''"""
A15_tg_send_raw.py
Sirf raw message send.
"""
from A_core.A12_tg_session import session
from A_core.A14_tg_creds import get_creds


def send_raw(msg, silent=False):
    """Send raw message to Telegram."""
    token, chat_id = get_creds()
    if token and chat_id:
        try:
            session.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": msg[:4000],
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "disable_notification": silent,
                },
                timeout=15,
            )
        except Exception:
            pass
    print(msg, flush=True)
''',

    "A16_tg_run_start.py": '''"""
A16_tg_run_start.py
Sirf run start.
"""
from A_core.A13_tg_buffer import reset, now, RUN_HEADER
from A_core.A15_tg_send_raw import send_raw


def run_start(title="📖 STORY VIDEO RUN"):
    """Initialize run."""
    reset()
    RUN_HEADER[0] = title
    send_raw(f"▶️ <b>{title} STARTED</b>\\n🕐 {now()}", silent=True)
''',

    "A17_tg_file_start.py": '''"""
A17_tg_file_start.py
Sirf file_start.
"""
import time
from A_core.A13_tg_buffer import LOG_BUFFER, FILE_TIMERS, STEP_COUNTER


def file_start(filename, purpose=""):
    """Add file start to buffer."""
    FILE_TIMERS[filename] = time.time()
    STEP_COUNTER["total"] += 1
    line = f"📂 <b>{filename}</b>"
    if purpose:
        line += f" — <i>{purpose}</i>"
    LOG_BUFFER.append(line)
''',

    "A18_tg_file_end.py": '''"""
A18_tg_file_end.py
Sirf file_end.
"""
import time
from A_core.A13_tg_buffer import LOG_BUFFER, FILE_TIMERS, STEP_COUNTER


def file_end(filename, status="success", note=""):
    """Add file end to buffer."""
    elapsed = time.time() - FILE_TIMERS.get(filename, time.time())
    if status == "success":
        STEP_COUNTER["success"] += 1
        icon = "✅"
    else:
        STEP_COUNTER["failed"] += 1
        icon = "❌"
    line = f"{icon} <b>{filename}</b> done in {elapsed:.2f}s"
    if note:
        line += f" — {note}"
    LOG_BUFFER.append(line)
''',

    "A19_tg_step.py": '''"""
A19_tg_step.py
Sirf step.
"""
from A_core.A13_tg_buffer import LOG_BUFFER


def step(filename, action, result="ok", detail=""):
    """Add step to buffer."""
    icon = {
        "ok": "✅", "fail": "❌", "skip": "⏭️",
        "warn": "⚠️", "info": "ℹ️",
    }.get(result, "ℹ️")
    line = f"{icon} <b>{filename}</b> → {action}"
    if detail:
        line += f" ({detail})"
    LOG_BUFFER.append(line)
''',

    "A20_tg_api_call.py": '''"""
A20_tg_api_call.py
Sirf api_call.
"""
from A_core.A13_tg_buffer import LOG_BUFFER


def api_call(filename, api_name, status, detail=""):
    """Add API call to buffer."""
    icon = {
        "success": "🟢", "failed": "🔴",
        "fallback": "🟡", "skipped": "⚪",
    }.get(status, "⚫")
    line = f"{icon} <b>{api_name}</b> [{status.upper()}]"
    if detail:
        line += f" — {detail}"
    LOG_BUFFER.append(line)
''',

    "A21_tg_file_error.py": '''"""
A21_tg_file_error.py
Sirf file_error.
"""
from A_core.A13_tg_buffer import LOG_BUFFER, STEP_COUNTER


def file_error(filename, error, tb=""):
    """Add error to buffer."""
    STEP_COUNTER["failed"] += 1
    line = f"🚨 <b>{filename}</b> ERROR: {str(error)[:150]}"
    if tb:
        line += f"\\n<code>{tb[:200]}</code>"
    LOG_BUFFER.append(line)
''',

    "A22_tg_header.py": '''"""
A22_tg_header.py
Sirf header.
"""
from A_core.A13_tg_buffer import LOG_BUFFER


def header(title):
    """Add header to buffer."""
    LOG_BUFFER.append(f"\\n<b>━━━ {title} ━━━</b>")
''',

    "A23_tg_send.py": '''"""
A23_tg_send.py
Sirf send_tg.
"""
from A_core.A15_tg_send_raw import send_raw


def send_tg(msg, silent=False):
    """Send message to Telegram immediately."""
    send_raw(msg, silent=silent)
''',

    "A24_tg_report.py": '''"""
A24_tg_report.py
Sirf full report.
"""
import time
from A_core.A13_tg_buffer import LOG_BUFFER, START_TIME, RUN_HEADER, now
from A_core.A15_tg_send_raw import send_raw


def send_full_report(extra_sections=None, silent=False):
    """Send all buffered logs (auto-split at 3800)."""
    total_time = time.time() - (START_TIME[0] or time.time())
    head = (
        f"<b>{RUN_HEADER[0]} — FULL REPORT</b>\\n"
        f"🕐 {now()}  |  ⏱️ {total_time:.1f}s\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\\n"
    )
    body = "\\n".join(LOG_BUFFER)
    extras = ""
    if extra_sections:
        extras = "\\n\\n" + "\\n".join(extra_sections)
    full = head + body + extras

    chunks = []
    current = ""
    for line in full.split("\\n"):
        if len(current) + len(line) + 1 > 3800:
            chunks.append(current)
            current = line
        else:
            current += ("\\n" if current else "") + line
    if current:
        chunks.append(current)

    for i, chunk in enumerate(chunks, 1):
        prefix = f"📄 <b>Report {i}/{len(chunks)}</b>\\n" if len(chunks) > 1 else ""
        send_raw(prefix + chunk, silent=silent)
''',

    "A25_tg_summary.py": '''"""
A25_tg_summary.py
Sirf summary.
"""
import time
from A_core.A13_tg_buffer import STEP_COUNTER, START_TIME, now
from A_core.A15_tg_send_raw import send_raw


def send_summary(silent=False):
    """Send final summary."""
    total = STEP_COUNTER["total"]
    ok = STEP_COUNTER["success"]
    fail = STEP_COUNTER["failed"]
    total_time = time.time() - (START_TIME[0] or time.time())
    icon = "🎉" if fail == 0 else "⚠️"
    msg = (
        f"{icon} <b>RUN COMPLETE</b>\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\\n"
        f"📁 Files: <b>{total}</b>\\n"
        f"✅ Success: <b>{ok}</b>\\n"
        f"❌ Failed: <b>{fail}</b>\\n"
        f"⏱️ Time: <b>{total_time:.1f}s</b>\\n"
        f"🕐 Finished: <b>{now()}</b>"
    )
    send_raw(msg, silent=silent)
''',

    "A26_sanitize.py": '''"""
A26_sanitize.py
Sirf text sanitize.
"""
import re


def sanitize(t):
    """Clean text — remove unicode, quotes, newlines."""
    if not t:
        return ""
    t = re.sub(r'[\\u200b-\\u200f\\ufeff\\u202a-\\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\\n', ' ').strip()
''',

    "A27_ensure_dir.py": '''"""
A27_ensure_dir.py
Sirf directory ensure.
"""
import os


def ensure_dir(path):
    """Create folder if missing."""
    os.makedirs(path, exist_ok=True)
    return path
''',

    "A28_http_session.py": '''"""
A28_http_session.py
Sirf HTTP session with retry.
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    """Create HTTP session with retry."""
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session
''',

    "A29_http_download.py": '''"""
A29_http_download.py
Sirf file download.
"""
import os
from A_core.A9_log_step import log_step


def download(session, url, path, min_size=12000):
    """Download file with minimum size check."""
    try:
        r = session.get(url, timeout=35)
        if r.status_code == 200 and len(r.content) > min_size:
            with open(path, "wb") as f:
                f.write(r.content)
            log_step("A29_http_download.py", f"Download OK: {path}", "ok",
                     f"{len(r.content) // 1024} KB")
            return True
        log_step("A29_http_download.py", f"Download small: {url[:50]}", "fail")
    except Exception as e:
        log_step("A29_http_download.py", "Download err", "fail", str(e)[:60])
    return False
''',

    "A30_cmd_runner.py": '''"""
A30_cmd_runner.py
Sirf shell command run karna.
"""
import subprocess
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error


def run_cmd(cmd):
    """Run shell command with logging."""
    log_step("A30_cmd_runner.py", f"CMD: {cmd[:80]}", "ok")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_error("A30_cmd_runner.py", f"CMD failed: {str(e)[:120]}")
        raise
''',

    "A31_cleanup.py": '''"""
A31_cleanup.py
Sirf cleanup.
"""
import os
import shutil
from A_core.A9_log_step import log_step


def cleanup(files, folder=None):
    """Remove temp files + folders."""
    log_step("A31_cleanup.py", "Cleanup starting", "ok")
    for f in files:
        if os.path.exists(f):
            os.remove(f)
    if folder:
        shutil.rmtree(folder, ignore_errors=True)
    log_step("A31_cleanup.py", "Cleanup done", "ok")
''',

    "A32_api_tracker.py": '''"""
A32_api_tracker.py
Sirf API status dict.
"""


def create_tracker():
    """Return empty API status dict."""
    return {
        "AI": {}, "TTS": {}, "Music": {}, "Background": {},
        "Translation": {}, "Hadith": {}, "Drive": {},
        "Facebook": {}, "Instagram": {}, "YouTube": {},
    }
''',

    "A33_secrets_registry.py": '''"""
A33_secrets_registry.py
Sirf secrets registry dict.
"""

SECRETS_REGISTRY = {
    "telegram": {
        "label": "📱 Telegram",
        "required": True,
        "secrets": {
            "TELEGRAM_BOT_TOKEN": {
                "label": "Bot Token",
                "names": ["TELEGRAM_BOT_TOKEN"],
            },
            "TELEGRAM_CHAT_ID": {
                "label": "Chat ID",
                "names": ["TELEGRAM_CHAT_ID"],
            },
        },
    },
    "facebook": {
        "label": "📘 Facebook",
        "required": True,
        "secrets": {
            "FACEBOOK_META_TOKEN": {
                "label": "Meta Token",
                "names": ["FACEBOOK_META_TOKEN", "FACEBOOK_INSTAGRAM_META_TOKEN"],
            },
            "FACEBOOK_PAGE_ID": {
                "label": "Page ID",
                "names": ["FACEBOOK_PAGE_ID"],
            },
        },
    },
    "instagram": {
        "label": "📸 Instagram",
        "required": True,
        "secrets": {
            "FACEBOOK_INSTAGRAM_META_TOKEN": {
                "label": "IG Token",
                "names": ["FACEBOOK_INSTAGRAM_META_TOKEN", "FACEBOOK_META_TOKEN"],
            },
            "INSTAGRAM_BUSINESS_ACCOUNT_ID": {
                "label": "IG Business ID",
                "names": ["INSTAGRAM_BUSINESS_ACCOUNT_ID"],
            },
        },
    },
    "youtube": {
        "label": "📺 YouTube",
        "required": False,
        "secrets": {
            "YOUTUBE_CLIENT_ID": {"label": "Client ID", "names": ["YOUTUBE_CLIENT_ID"]},
            "YOUTUBE_CLIENT_SECRET": {"label": "Client Secret", "names": ["YOUTUBE_CLIENT_SECRET"]},
            "YOUTUBE_REFRESH_TOKEN": {"label": "Refresh Token", "names": ["YOUTUBE_REFRESH_TOKEN"]},
        },
    },
    "drive": {
        "label": "☁️ Google Drive",
        "required": True,
        "secrets": {
            "GOOGLE_DRIVE_CLIENT_ID": {"label": "Client ID", "names": ["GOOGLE_DRIVE_CLIENT_ID"]},
            "GOOGLE_DRIVE_CLIENT_SECRET": {"label": "Client Secret", "names": ["GOOGLE_DRIVE_CLIENT_SECRET"]},
            "GOOGLE_DRIVE_REFRESH_TOKEN": {"label": "Refresh Token", "names": ["GOOGLE_DRIVE_REFRESH_TOKEN"]},
            "GDRIVE_STORY_VIDEO_FOLDER_ID": {"label": "Folder ID", "names": ["GDRIVE_STORY_VIDEO_FOLDER_ID", "GDRIVE_SHORT_VIDEO_FOLDER_ID"]},
        },
    },
    "ai_providers": {
        "label": "🤖 AI",
        "required": False,
        "min_required": 1,
        "secrets": {
            "OPENROUTER_API_KEY": {"label": "OpenRouter", "names": ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI"]},
            "GROQ_API_KEY": {"label": "Groq", "names": ["GROQ_API_KEY", "GROQ_API_KEY_AI"]},
            "GEMINI_API_KEY": {"label": "Gemini", "names": ["GEMINI_API_KEY", "GEMINI_API_KEY_AI"]},
            "MISTRAL_API_KEY": {"label": "Mistral", "names": ["MISTRAL_API_KEY", "MISTRAL_API_KEY_AI"]},
            "CEREBRAS_API_KEY": {"label": "Cerebras", "names": ["CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI"]},
            "COHERE_API_KEY": {"label": "Cohere", "names": ["COHERE_API_KEY", "COHERE_API_KEY_AI"]},
        },
    },
    "media": {
        "label": "🎬 Media",
        "required": False,
        "min_required": 1,
        "secrets": {
            "PEXELS_API_KEY": {"label": "Pexels", "names": ["PEXELS_API_KEY"]},
            "PIXABAY_API_KEY": {"label": "Pixabay", "names": ["PIXABAY_API_KEY"]},
            "FREESOUND_API_KEY": {"label": "Freesound", "names": ["FREESOUND_API_KEY"]},
        },
    },
    "tts": {
        "label": "🎙️ TTS",
        "required": False,
        "secrets": {
            "ELEVENLABS_API_KEY": {"label": "ElevenLabs", "names": ["ELEVENLABS_API_KEY"]},
            "DEEPL_API_KEY": {"label": "DeepL", "names": ["DEEPL_API_KEY"]},
        },
    },
}
''',

    "A34_secrets_env_check.py": '''"""
A34_secrets_env_check.py
Sirf env var check.
"""
import os


def check_env(*names) -> tuple:
    """Check multiple env var names, return first found."""
    for name in names:
        val = os.environ.get(name, "").strip()
        if val and val not in ("your_token_here", "undefined"):
            return (True, name, len(val))
    return (False, names[0] if names else "", 0)
''',

    "A35_ping_telegram.py": '''"""
A35_ping_telegram.py
Sirf Telegram ping.
"""
import os
import requests


def ping() -> dict:
    """Ping Telegram API."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return {"status": "skipped", "reason": "no token"}
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{token}/getMe", timeout=8)
        if r.status_code == 200 and r.json().get("ok"):
            bot = r.json().get("result", {})
            return {"status": "working", "bot_name": bot.get("username", "?"), "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A36_ping_facebook.py": '''"""
A36_ping_facebook.py
Sirf Facebook ping.
"""
import os
import requests


def ping() -> dict:
    """Ping Facebook Graph API."""
    token = (os.environ.get("FACEBOOK_META_TOKEN", "").strip()
             or os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip())
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    if not token or not page_id:
        return {"status": "skipped", "reason": "no creds"}
    try:
        r = requests.get(
            f"https://graph.facebook.com/v21.0/{page_id}",
            params={"access_token": token, "fields": "name"},
            timeout=10)
        if r.status_code == 200:
            return {"status": "working", "page_name": r.json().get("name", "?"), "code": 200}
        err = r.json().get("error", {}).get("message", "")
        return {"status": "failed", "code": r.status_code, "error": err[:80]}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A37_ping_instagram.py": '''"""
A37_ping_instagram.py
Sirf Instagram ping.
"""
import os
import requests


def ping() -> dict:
    """Ping Instagram Graph API."""
    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    if not token or not ig_id:
        return {"status": "skipped", "reason": "no creds"}
    try:
        r = requests.get(
            f"https://graph.facebook.com/v21.0/{ig_id}",
            params={"access_token": token, "fields": "username"},
            timeout=10)
        if r.status_code == 200:
            return {"status": "working", "username": r.json().get("username", "?"), "code": 200}
        err = r.json().get("error", {}).get("message", "")
        return {"status": "failed", "code": r.status_code, "error": err[:80]}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A38_ping_drive.py": '''"""
A38_ping_drive.py
Sirf Google Drive ping.
"""
import os
import requests


def ping() -> dict:
    """Ping Google Drive OAuth."""
    cid = os.environ.get("GOOGLE_DRIVE_CLIENT_ID", "").strip()
    csec = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET", "").strip()
    rt = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN", "").strip()
    if not all([cid, csec, rt]):
        return {"status": "skipped", "reason": "missing creds"}
    try:
        r = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": cid, "client_secret": csec,
                "refresh_token": rt, "grant_type": "refresh_token",
            }, timeout=10)
        if r.status_code == 200 and "access_token" in r.json():
            return {"status": "working", "code": 200}
        return {"status": "failed", "code": r.status_code,
                "error": r.json().get("error", "")[:80]}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A39_ping_openrouter.py": '''"""
A39_ping_openrouter.py
Sirf OpenRouter ping.
"""
import os
import requests


def ping() -> dict:
    """Ping OpenRouter."""
    key = (os.environ.get("OPENROUTER_API_KEY", "").strip()
           or os.environ.get("OPENROUTER_API_KEY_AI", "").strip())
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if r.status_code == 200:
            return {"status": "working", "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A40_ping_groq.py": '''"""
A40_ping_groq.py
Sirf Groq ping.
"""
import os
import requests


def ping() -> dict:
    """Ping Groq."""
    key = (os.environ.get("GROQ_API_KEY", "").strip()
           or os.environ.get("GROQ_API_KEY_AI", "").strip())
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if r.status_code == 200:
            return {"status": "working", "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A41_ping_pexels.py": '''"""
A41_ping_pexels.py
Sirf Pexels ping.
"""
import os
import requests


def ping() -> dict:
    """Ping Pexels."""
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get(
            "https://api.pexels.com/videos/search",
            params={"query": "test", "per_page": 1},
            headers={"Authorization": key}, timeout=10)
        if r.status_code == 200:
            return {"status": "working", "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A42_secrets_summary.py": '''"""
A42_secrets_summary.py
Sirf secrets summary banani.
"""


def build(secrets_report, api_report) -> dict:
    """Build summary dict."""
    total_secrets = 0
    working_secrets = 0
    for cat in secrets_report.values():
        total_secrets += cat["total"]
        working_secrets += cat["set_count"]

    checked = 0
    working = 0
    failed = 0
    skipped = 0

    for api in api_report.values():
        st = api.get("status", "")
        if st == "skipped":
            skipped += 1
        else:
            checked += 1
            if st == "working":
                working += 1
            else:
                failed += 1

    return {
        "total_secrets": total_secrets,
        "working_secrets": working_secrets,
        "missing_secrets": total_secrets - working_secrets,
        "checked_apis": checked,
        "working_apis": working,
        "failed_apis": failed,
        "skipped_apis": skipped,
        "health_pct": int(100 * working / max(checked, 1)),
    }
''',

    "A43_secrets_report.py": '''"""
A43_secrets_report.py
Sirf report format karna.
"""


def format_report(report: dict) -> str:
    """Format report as Telegram HTML."""
    lines = []
    s = report["summary"]

    lines.append("<b>🔐 SECRETS &amp; API VERIFICATION</b>")
    lines.append(f"🕐 {report['timestamp']}")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("<b>📊 SUMMARY</b>")
    lines.append(f"🔑 Secrets: <b>{s['working_secrets']}/{s['total_secrets']}</b>")
    lines.append(f"🌐 APIs: <b>{s['working_apis']}/{s['checked_apis']}</b> ({s['health_pct']}%)")
    if s["failed_apis"] > 0:
        lines.append(f"❌ Failed: <b>{s['failed_apis']}</b>")

    return "\\n".join(lines)
''',

    "A44_msg_splitter.py": '''"""
A44_msg_splitter.py
Sirf message split karna.
"""


def split(msg: str, max_len: int = 3800) -> list:
    """Split long message into chunks."""
    if len(msg) <= max_len:
        return [msg]
    chunks = []
    current = ""
    for line in msg.split("\\n"):
        if len(current) + len(line) + 1 > max_len:
            chunks.append(current)
            current = line
        else:
            current += ("\\n" if current else "") + line
    if current:
        chunks.append(current)
    return chunks
''',

    "A45_secrets_verify.py": '''"""
A45_secrets_verify.py
Sirf main verify function.
"""
from datetime import datetime
from A_core.A33_secrets_registry import SECRETS_REGISTRY
from A_core.A34_secrets_env_check import check_env
from A_core.A35_ping_telegram import ping as ping_telegram
from A_core.A36_ping_facebook import ping as ping_facebook
from A_core.A37_ping_instagram import ping as ping_instagram
from A_core.A38_ping_drive import ping as ping_drive
from A_core.A39_ping_openrouter import ping as ping_openrouter
from A_core.A40_ping_groq import ping as ping_groq
from A_core.A41_ping_pexels import ping as ping_pexels
from A_core.A42_secrets_summary import build as build_summary


def verify():
    """Run full verification."""
    secrets_report = {}
    for cat_key, meta in SECRETS_REGISTRY.items():
        cat_report = {
            "label": meta["label"],
            "required": meta["required"],
            "min_required": meta.get("min_required", 0),
            "secrets": {},
            "set_count": 0,
            "missing_count": 0,
            "total": len(meta["secrets"]),
        }
        for sk, sm in meta["secrets"].items():
            found, actual, length = check_env(*sm["names"])
            cat_report["secrets"][sk] = {
                "label": sm["label"],
                "is_set": found,
                "actual_name": actual if found else "",
                "length": length,
            }
            if found:
                cat_report["set_count"] += 1
            else:
                cat_report["missing_count"] += 1

        if cat_report["missing_count"] == 0:
            cat_report["status"] = "complete"
        elif cat_report["set_count"] >= cat_report["min_required"]:
            cat_report["status"] = "partial"
        elif cat_report["required"]:
            cat_report["status"] = "critical"
        else:
            cat_report["status"] = "optional_missing"

        secrets_report[cat_key] = cat_report

    api_report = {
        "telegram": ping_telegram(),
        "facebook": ping_facebook(),
        "instagram": ping_instagram(),
        "google_drive": ping_drive(),
        "openrouter": ping_openrouter(),
        "groq": ping_groq(),
        "pexels": ping_pexels(),
    }

    return {
        "secrets": secrets_report,
        "api_health": api_report,
        "summary": build_summary(secrets_report, api_report),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
''',

    "__init__.py": '''"""
A_core package — Story generator core modules.
"""
''',
}


def main():
    """Write all files."""
    base = BASE
    os.makedirs(base, exist_ok=True)
    total = 0

    for filename, content in FILES.items():
        path = os.path.join(base, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        total += 1
        print(f"  ✅ {path}")

    print(f"\\n🎉 A_core: {total} files written!")


if __name__ == "__main__":
    main()
