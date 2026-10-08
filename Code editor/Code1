
"""
Code1 — Story Generator code transfer.
"""
import os

BASE = "sawajstudiobot/video_generator/fb_ig_story_video_generator"

FILES = {

    # ═══════════════════════════════════════════════════
    # A_core (45 files)
    # ═══════════════════════════════════════════════════
    "A_core/A1_env_loader.py": '''"""A1_env_loader.py — Sirf env var load."""
import os


def get_env(name, default=""):
    return os.environ.get(name, default).strip()
''',

    "A_core/A2_env_fallback.py": '''"""A2_env_fallback.py — Sirf multi-name fallback."""
import os


def get_env_fallback(*names, default=""):
    for name in names:
        val = os.environ.get(name, "").strip()
        if val:
            return val
    return default
''',

    "A_core/A3_config_class.py": '''"""A3_config_class.py — Sirf Config class."""
from A_core.A1_env_loader import get_env
from A_core.A2_env_fallback import get_env_fallback


class Config:
    TG_TOKEN = get_env("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = get_env("TELEGRAM_CHAT_ID")
    META_TOKEN = get_env_fallback("FACEBOOK_META_TOKEN", "FACEBOOK_INSTAGRAM_META_TOKEN")
    PAGE_ID = get_env("FACEBOOK_PAGE_ID")
    IG_TOKEN = get_env_fallback("FACEBOOK_INSTAGRAM_META_TOKEN", "FACEBOOK_META_TOKEN")
    IG_BUSINESS_ID = get_env("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    YT_CLIENT_ID = get_env("YOUTUBE_CLIENT_ID")
    YT_CLIENT_SECRET = get_env("YOUTUBE_CLIENT_SECRET")
    YT_REFRESH_TOKEN = get_env("YOUTUBE_REFRESH_TOKEN")
    YT_PLAYLIST_ID = get_env("DAILY_HADEES_YT_PLAYLIST_ID")
    DRIVE_CLIENT_ID = get_env("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = get_env("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = get_env("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_STORY_FOLDER_ID = get_env_fallback("GDRIVE_STORY_VIDEO_FOLDER_ID", "GDRIVE_SHORT_VIDEO_FOLDER_ID")
    OPENROUTER_API_KEY = get_env_fallback("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
    GROQ_API_KEY = get_env_fallback("GROQ_API_KEY", "GROQ_API_KEY_AI")
    GEMINI_API_KEY = get_env_fallback("GEMINI_API_KEY", "GEMINI_API_KEY_AI")
    MISTRAL_API_KEY = get_env_fallback("MISTRAL_API_KEY", "MISTRAL_API_KEY_AI")
    CEREBRAS_API_KEY = get_env_fallback("CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI")
    COHERE_API_KEY = get_env_fallback("COHERE_API_KEY", "COHERE_API_KEY_AI")
    ELEVENLABS_API_KEY = get_env("ELEVENLABS_API_KEY")
    DEEPL_API_KEY = get_env("DEEPL_API_KEY")
    PEXELS_API_KEY = get_env("PEXELS_API_KEY")
    PIXABAY_API_KEY = get_env("PIXABAY_API_KEY")
    FREESOUND_API_KEY = get_env("FREESOUND_API_KEY")
    HADITH_API_URL = get_env("HADITH_API_URL")
    EVENT_NAME = get_env("GITHUB_EVENT_NAME")
    UPLOAD_TARGET = get_env("UPLOAD_TARGET", default="drive_only").lower()
    CONFIRM_UPLOAD = get_env("CONFIRM_UPLOAD", default="false").lower() == "true"
''',

    "A_core/A4_upload_decider.py": '''"""A4_upload_decider.py — Sirf upload decisions."""
from A_core.A3_config_class import Config


def decide(cfg=None):
    if cfg is None:
        cfg = Config()
    is_scheduled = cfg.EVENT_NAME == "schedule"
    is_confirmed = True if is_scheduled else cfg.CONFIRM_UPLOAD
    return {
        "drive": True,
        "facebook": (is_scheduled or is_confirmed) and cfg.UPLOAD_TARGET in ("fb_ig", "all"),
        "instagram": (is_scheduled or is_confirmed) and cfg.UPLOAD_TARGET in ("fb_ig", "all"),
        "youtube": (not is_scheduled) and is_confirmed and cfg.UPLOAD_TARGET in ("youtube", "all"),
    }
''',

    "A_core/A5_platform_checker.py": '''"""A5_platform_checker.py — Sirf platforms check."""
from A_core.A3_config_class import Config


def available_platforms(cfg=None):
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

    "A_core/A6_print_logger.py": '''"""A6_print_logger.py — Sirf print."""
from datetime import datetime


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}", flush=True)
''',

    "A_core/A7_log_file_start.py": '''"""A7_log_file_start.py — Sirf file start log."""
from A_core.A6_print_logger import log


def log_file_start(name, purpose=""):
    log(f"→ START {name}")
    try:
        from A_core.A17_tg_file_start import file_start
        file_start(name, purpose)
    except Exception:
        pass
''',

    "A_core/A8_log_file_end.py": '''"""A8_log_file_end.py — Sirf file end log."""
from A_core.A6_print_logger import log


def log_file_end(name, status="success", note=""):
    log(f"← END {name} ({status})")
    try:
        from A_core.A18_tg_file_end import file_end
        file_end(name, status, note)
    except Exception:
        pass
''',

    "A_core/A9_log_step.py": '''"""A9_log_step.py — Sirf step log."""
from A_core.A6_print_logger import log


def log_step(name, action, result="ok", detail=""):
    log(f"  • {name} :: {action} → {result} {detail}")
    try:
        from A_core.A19_tg_step import step
        step(name, action, result, detail)
    except Exception:
        pass
''',

    "A_core/A10_log_api.py": '''"""A10_log_api.py — Sirf API log."""
from A_core.A6_print_logger import log


def log_api(name, api, status, detail=""):
    log(f"  ★ {name} :: {api} → {status}")
    try:
        from A_core.A20_tg_api_call import api_call
        api_call(name, api, status, detail)
    except Exception:
        pass
''',

    "A_core/A11_log_error.py": '''"""A11_log_error.py — Sirf error log."""
from A_core.A6_print_logger import log


def log_error(name, error, tb=""):
    log(f"  ✗ {name} :: ERROR → {error}", level="ERROR")
    try:
        from A_core.A21_tg_file_error import file_error
        file_error(name, error, tb)
    except Exception:
        pass
''',

    "A_core/A12_tg_session.py": '''"""A12_tg_session.py — Sirf session."""
import requests

session = requests.Session()
''',

    "A_core/A13_tg_buffer.py": '''"""A13_tg_buffer.py — Sirf buffer."""
import time
from datetime import datetime

LOG_BUFFER = []
FILE_TIMERS = {}
STEP_COUNTER = {"total": 0, "success": 0, "failed": 0}
START_TIME = [None]
RUN_HEADER = ["📖 STORY VIDEO RUN"]


def now():
    return datetime.now().strftime("%H:%M:%S")


def reset():
    LOG_BUFFER.clear()
    FILE_TIMERS.clear()
    STEP_COUNTER.update({"total": 0, "success": 0, "failed": 0})
    START_TIME[0] = time.time()
''',

    "A_core/A14_tg_creds.py": '''"""A14_tg_creds.py — Sirf TG creds."""
import os


def get_creds():
    return (os.environ.get("TELEGRAM_BOT_TOKEN", "").strip(),
            os.environ.get("TELEGRAM_CHAT_ID", "").strip())
''',

    "A_core/A15_tg_send_raw.py": '''"""A15_tg_send_raw.py — Sirf raw send."""
from A_core.A12_tg_session import session
from A_core.A14_tg_creds import get_creds


def send_raw(msg, silent=False):
    token, chat_id = get_creds()
    if token and chat_id:
        try:
            session.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": msg[:4000],
                      "parse_mode": "HTML",
                      "disable_web_page_preview": True,
                      "disable_notification": silent},
                timeout=15)
        except Exception:
            pass
    print(msg, flush=True)
''',

    "A_core/A16_tg_run_start.py": '''"""A16_tg_run_start.py — Sirf run start."""
from A_core.A13_tg_buffer import reset, now, RUN_HEADER
from A_core.A15_tg_send_raw import send_raw


def run_start(title="📖 STORY VIDEO RUN"):
    reset()
    RUN_HEADER[0] = title
    send_raw(f"▶️ <b>{title} STARTED</b>\\n🕐 {now()}", silent=True)
''',

    "A_core/A17_tg_file_start.py": '''"""A17_tg_file_start.py — Sirf file_start."""
import time
from A_core.A13_tg_buffer import LOG_BUFFER, FILE_TIMERS, STEP_COUNTER


def file_start(filename, purpose=""):
    FILE_TIMERS[filename] = time.time()
    STEP_COUNTER["total"] += 1
    line = f"📂 <b>{filename}</b>"
    if purpose:
        line += f" — <i>{purpose}</i>"
    LOG_BUFFER.append(line)
''',

    "A_core/A18_tg_file_end.py": '''"""A18_tg_file_end.py — Sirf file_end."""
import time
from A_core.A13_tg_buffer import LOG_BUFFER, FILE_TIMERS, STEP_COUNTER


def file_end(filename, status="success", note=""):
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

    "A_core/A19_tg_step.py": '''"""A19_tg_step.py — Sirf step."""
from A_core.A13_tg_buffer import LOG_BUFFER


def step(filename, action, result="ok", detail=""):
    icon = {"ok": "✅", "fail": "❌", "skip": "⏭️",
            "warn": "⚠️", "info": "ℹ️"}.get(result, "ℹ️")
    line = f"{icon} <b>{filename}</b> → {action}"
    if detail:
        line += f" ({detail})"
    LOG_BUFFER.append(line)
''',

    "A_core/A20_tg_api_call.py": '''"""A20_tg_api_call.py — Sirf api_call."""
from A_core.A13_tg_buffer import LOG_BUFFER


def api_call(filename, api_name, status, detail=""):
    icon = {"success": "🟢", "failed": "🔴",
            "fallback": "🟡", "skipped": "⚪"}.get(status, "⚫")
    line = f"{icon} <b>{api_name}</b> [{status.upper()}]"
    if detail:
        line += f" — {detail}"
    LOG_BUFFER.append(line)
''',

    "A_core/A21_tg_file_error.py": '''"""A21_tg_file_error.py — Sirf file_error."""
from A_core.A13_tg_buffer import LOG_BUFFER, STEP_COUNTER


def file_error(filename, error, tb=""):
    STEP_COUNTER["failed"] += 1
    line = f"🚨 <b>{filename}</b> ERROR: {str(error)[:150]}"
    if tb:
        line += f"\\n<code>{tb[:200]}</code>"
    LOG_BUFFER.append(line)
''',

    "A_core/A22_tg_header.py": '''"""A22_tg_header.py — Sirf header."""
from A_core.A13_tg_buffer import LOG_BUFFER


def header(title):
    LOG_BUFFER.append(f"\\n<b>━━━ {title} ━━━</b>")
''',

    "A_core/A23_tg_send.py": '''"""A23_tg_send.py — Sirf send_tg."""
from A_core.A15_tg_send_raw import send_raw


def send_tg(msg, silent=False):
    send_raw(msg, silent=silent)
''',

    "A_core/A24_tg_report.py": '''"""A24_tg_report.py — Sirf full report."""
import time
from A_core.A13_tg_buffer import LOG_BUFFER, START_TIME, RUN_HEADER, now
from A_core.A15_tg_send_raw import send_raw


def send_full_report(extra_sections=None, silent=False):
    total_time = time.time() - (START_TIME[0] or time.time())
    head = (f"<b>{RUN_HEADER[0]} — FULL REPORT</b>\\n"
            f"🕐 {now()}  |  ⏱️ {total_time:.1f}s\\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\\n")
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

    "A_core/A25_tg_summary.py": '''"""A25_tg_summary.py — Sirf summary."""
import time
from A_core.A13_tg_buffer import STEP_COUNTER, START_TIME, now
from A_core.A15_tg_send_raw import send_raw


def send_summary(silent=False):
    total = STEP_COUNTER["total"]
    ok = STEP_COUNTER["success"]
    fail = STEP_COUNTER["failed"]
    total_time = time.time() - (START_TIME[0] or time.time())
    icon = "🎉" if fail == 0 else "⚠️"
    msg = (f"{icon} <b>RUN COMPLETE</b>\\n"
           f"━━━━━━━━━━━━━━━━━━━━━━━\\n"
           f"📁 Files: <b>{total}</b>\\n"
           f"✅ Success: <b>{ok}</b>\\n"
           f"❌ Failed: <b>{fail}</b>\\n"
           f"⏱️ Time: <b>{total_time:.1f}s</b>\\n"
           f"🕐 Finished: <b>{now()}</b>")
    send_raw(msg, silent=silent)
''',

    "A_core/A26_sanitize.py": '''"""A26_sanitize.py — Sirf sanitize."""
import re


def sanitize(t):
    if not t:
        return ""
    t = re.sub(r'[\\u200b-\\u200f\\ufeff\\u202a-\\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\\n', ' ').strip()
''',

    "A_core/A27_ensure_dir.py": '''"""A27_ensure_dir.py — Sirf ensure_dir."""
import os


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path
''',

    "A_core/A28_http_session.py": '''"""A28_http_session.py — Sirf HTTP session."""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1.5,
                  status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session
''',

    "A_core/A29_http_download.py": '''"""A29_http_download.py — Sirf download."""
from A_core.A9_log_step import log_step


def download(session, url, path, min_size=12000):
    try:
        r = session.get(url, timeout=35)
        if r.status_code == 200 and len(r.content) > min_size:
            with open(path, "wb") as f:
                f.write(r.content)
            log_step("A29_http_download.py", f"OK: {path}", "ok", f"{len(r.content)//1024} KB")
            return True
    except Exception as e:
        log_step("A29_http_download.py", "err", "fail", str(e)[:60])
    return False
''',

    "A_core/A30_cmd_runner.py": '''"""A30_cmd_runner.py — Sirf cmd runner."""
import subprocess
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error


def run_cmd(cmd):
    log_step("A30_cmd_runner.py", f"CMD: {cmd[:80]}", "ok")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_error("A30_cmd_runner.py", f"CMD failed: {str(e)[:120]}")
        raise
''',

    "A_core/A31_cleanup.py": '''"""A31_cleanup.py — Sirf cleanup."""
import os
import shutil
from A_core.A9_log_step import log_step


def cleanup(files, folder=None):
    log_step("A31_cleanup.py", "Cleanup", "ok")
    for f in files:
        if os.path.exists(f):
            os.remove(f)
    if folder:
        shutil.rmtree(folder, ignore_errors=True)
    log_step("A31_cleanup.py", "Done", "ok")
''',

    "A_core/A32_api_tracker.py": '''"""A32_api_tracker.py — Sirf tracker."""


def create_tracker():
    return {"AI": {}, "TTS": {}, "Music": {}, "Background": {},
            "Translation": {}, "Hadith": {}, "Drive": {},
            "Facebook": {}, "Instagram": {}, "YouTube": {}}
''',

    "A_core/A33_secrets_registry.py": '''"""A33_secrets_registry.py — Sirf registry."""
SECRETS_REGISTRY = {
    "telegram": {"label": "📱 Telegram", "required": True, "secrets": {
        "TELEGRAM_BOT_TOKEN": {"label": "Bot", "names": ["TELEGRAM_BOT_TOKEN"]},
        "TELEGRAM_CHAT_ID": {"label": "Chat", "names": ["TELEGRAM_CHAT_ID"]}}},
    "facebook": {"label": "📘 Facebook", "required": True, "secrets": {
        "FACEBOOK_META_TOKEN": {"label": "Meta", "names": ["FACEBOOK_META_TOKEN", "FACEBOOK_INSTAGRAM_META_TOKEN"]},
        "FACEBOOK_PAGE_ID": {"label": "Page", "names": ["FACEBOOK_PAGE_ID"]}}},
    "instagram": {"label": "📸 Instagram", "required": True, "secrets": {
        "FACEBOOK_INSTAGRAM_META_TOKEN": {"label": "IG", "names": ["FACEBOOK_INSTAGRAM_META_TOKEN", "FACEBOOK_META_TOKEN"]},
        "INSTAGRAM_BUSINESS_ACCOUNT_ID": {"label": "IG ID", "names": ["INSTAGRAM_BUSINESS_ACCOUNT_ID"]}}},
    "youtube": {"label": "📺 YouTube", "required": False, "secrets": {
        "YOUTUBE_CLIENT_ID": {"label": "ID", "names": ["YOUTUBE_CLIENT_ID"]},
        "YOUTUBE_CLIENT_SECRET": {"label": "Secret", "names": ["YOUTUBE_CLIENT_SECRET"]},
        "YOUTUBE_REFRESH_TOKEN": {"label": "Token", "names": ["YOUTUBE_REFRESH_TOKEN"]}}},
    "drive": {"label": "☁️ Drive", "required": True, "secrets": {
        "GOOGLE_DRIVE_CLIENT_ID": {"label": "ID", "names": ["GOOGLE_DRIVE_CLIENT_ID"]},
        "GOOGLE_DRIVE_CLIENT_SECRET": {"label": "Secret", "names": ["GOOGLE_DRIVE_CLIENT_SECRET"]},
        "GOOGLE_DRIVE_REFRESH_TOKEN": {"label": "Token", "names": ["GOOGLE_DRIVE_REFRESH_TOKEN"]},
        "GDRIVE_STORY_VIDEO_FOLDER_ID": {"label": "Folder", "names": ["GDRIVE_STORY_VIDEO_FOLDER_ID", "GDRIVE_SHORT_VIDEO_FOLDER_ID"]}}},
    "ai_providers": {"label": "🤖 AI", "required": False, "min_required": 1, "secrets": {
        "OPENROUTER_API_KEY": {"label": "OR", "names": ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI"]},
        "GROQ_API_KEY": {"label": "Groq", "names": ["GROQ_API_KEY", "GROQ_API_KEY_AI"]},
        "GEMINI_API_KEY": {"label": "Gemini", "names": ["GEMINI_API_KEY", "GEMINI_API_KEY_AI"]},
        "MISTRAL_API_KEY": {"label": "Mistral", "names": ["MISTRAL_API_KEY", "MISTRAL_API_KEY_AI"]},
        "CEREBRAS_API_KEY": {"label": "Cerebras", "names": ["CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI"]},
        "COHERE_API_KEY": {"label": "Cohere", "names": ["COHERE_API_KEY", "COHERE_API_KEY_AI"]}}},
    "media": {"label": "🎬 Media", "required": False, "min_required": 1, "secrets": {
        "PEXELS_API_KEY": {"label": "Pexels", "names": ["PEXELS_API_KEY"]},
        "PIXABAY_API_KEY": {"label": "Pixabay", "names": ["PIXABAY_API_KEY"]},
        "FREESOUND_API_KEY": {"label": "FS", "names": ["FREESOUND_API_KEY"]}}},
    "tts": {"label": "🎙️ TTS", "required": False, "secrets": {
        "ELEVENLABS_API_KEY": {"label": "11L", "names": ["ELEVENLABS_API_KEY"]},
        "DEEPL_API_KEY": {"label": "DeepL", "names": ["DEEPL_API_KEY"]}}},
}
''',

    "A_core/A34_secrets_env_check.py": '''"""A34_secrets_env_check.py — Sirf env check."""
import os


def check_env(*names):
    for name in names:
        val = os.environ.get(name, "").strip()
        if val and val not in ("your_token_here", "undefined"):
            return (True, name, len(val))
    return (False, names[0] if names else "", 0)
''',

    "A_core/A35_ping_telegram.py": '''"""A35_ping_telegram.py — Sirf TG ping."""
import os, requests


def ping():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return {"status": "skipped", "reason": "no token"}
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=8)
        if r.status_code == 200 and r.json().get("ok"):
            bot = r.json().get("result", {})
            return {"status": "working", "bot_name": bot.get("username", "?"), "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A_core/A36_ping_facebook.py": '''"""A36_ping_facebook.py — Sirf FB ping."""
import os, requests


def ping():
    token = (os.environ.get("FACEBOOK_META_TOKEN", "").strip()
             or os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip())
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    if not token or not page_id:
        return {"status": "skipped", "reason": "no creds"}
    try:
        r = requests.get(f"https://graph.facebook.com/v21.0/{page_id}",
                         params={"access_token": token, "fields": "name"}, timeout=10)
        if r.status_code == 200:
            return {"status": "working", "page_name": r.json().get("name", "?"), "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A_core/A37_ping_instagram.py": '''"""A37_ping_instagram.py — Sirf IG ping."""
import os, requests


def ping():
    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    if not token or not ig_id:
        return {"status": "skipped", "reason": "no creds"}
    try:
        r = requests.get(f"https://graph.facebook.com/v21.0/{ig_id}",
                         params={"access_token": token, "fields": "username"}, timeout=10)
        if r.status_code == 200:
            return {"status": "working", "username": r.json().get("username", "?"), "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A_core/A38_ping_drive.py": '''"""A38_ping_drive.py — Sirf Drive ping."""
import os, requests


def ping():
    cid = os.environ.get("GOOGLE_DRIVE_CLIENT_ID", "").strip()
    csec = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET", "").strip()
    rt = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN", "").strip()
    if not all([cid, csec, rt]):
        return {"status": "skipped", "reason": "missing creds"}
    try:
        r = requests.post("https://oauth2.googleapis.com/token",
                          data={"client_id": cid, "client_secret": csec,
                                "refresh_token": rt, "grant_type": "refresh_token"}, timeout=10)
        if r.status_code == 200 and "access_token" in r.json():
            return {"status": "working", "code": 200}
        return {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A_core/A39_ping_openrouter.py": '''"""A39_ping_openrouter.py — Sirf OR ping."""
import os, requests


def ping():
    key = (os.environ.get("OPENROUTER_API_KEY", "").strip()
           or os.environ.get("OPENROUTER_API_KEY_AI", "").strip())
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get("https://openrouter.ai/api/v1/models",
                         headers={"Authorization": f"Bearer {key}"}, timeout=10)
        return {"status": "working", "code": 200} if r.status_code == 200 else {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A_core/A40_ping_groq.py": '''"""A40_ping_groq.py — Sirf Groq ping."""
import os, requests


def ping():
    key = (os.environ.get("GROQ_API_KEY", "").strip()
           or os.environ.get("GROQ_API_KEY_AI", "").strip())
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get("https://api.groq.com/openai/v1/models",
                         headers={"Authorization": f"Bearer {key}"}, timeout=10)
        return {"status": "working", "code": 200} if r.status_code == 200 else {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A_core/A41_ping_pexels.py": '''"""A41_ping_pexels.py — Sirf Pexels ping."""
import os, requests


def ping():
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        return {"status": "skipped", "reason": "no key"}
    try:
        r = requests.get("https://api.pexels.com/videos/search",
                         params={"query": "test", "per_page": 1},
                         headers={"Authorization": key}, timeout=10)
        return {"status": "working", "code": 200} if r.status_code == 200 else {"status": "failed", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:60]}
''',

    "A_core/A42_secrets_summary.py": '''"""A42_secrets_summary.py — Sirf summary."""


def build(secrets_report, api_report):
    total = sum(c["total"] for c in secrets_report.values())
    working = sum(c["set_count"] for c in secrets_report.values())
    checked = working_api = failed = skipped = 0
    for api in api_report.values():
        st = api.get("status", "")
        if st == "skipped":
            skipped += 1
        else:
            checked += 1
            if st == "working":
                working_api += 1
            else:
                failed += 1
    return {"total_secrets": total, "working_secrets": working,
            "missing_secrets": total - working, "checked_apis": checked,
            "working_apis": working_api, "failed_apis": failed,
            "skipped_apis": skipped,
            "health_pct": int(100 * working_api / max(checked, 1))}
''',

    "A_core/A43_secrets_report.py": '''"""A43_secrets_report.py — Sirf report."""


def format_report(report):
    s = report["summary"]
    lines = ["<b>🔐 SECRETS & API VERIFICATION</b>",
             f"🕐 {report['timestamp']}",
             "━━━━━━━━━━━━━━━━━━━━━", "",
             "<b>📊 SUMMARY</b>",
             f"🔑 Secrets: <b>{s['working_secrets']}/{s['total_secrets']}</b>",
             f"🌐 APIs: <b>{s['working_apis']}/{s['checked_apis']}</b> ({s['health_pct']}%)"]
    if s["failed_apis"] > 0:
        lines.append(f"❌ Failed: <b>{s['failed_apis']}</b>")
    return "\\n".join(lines)
''',

    "A_core/A44_msg_splitter.py": '''"""A44_msg_splitter.py — Sirf split."""


def split(msg, max_len=3800):
    if len(msg) <= max_len:
        return [msg]
    chunks, current = [], ""
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

    "A_core/A45_secrets_verify.py": '''"""A45_secrets_verify.py — Sirf verify."""
from datetime import datetime
from A_core.A33_secrets_registry import SECRETS_REGISTRY
from A_core.A34_secrets_env_check import check_env
from A_core.A35_ping_telegram import ping as p_tg
from A_core.A36_ping_facebook import ping as p_fb
from A_core.A37_ping_instagram import ping as p_ig
from A_core.A38_ping_drive import ping as p_dr
from A_core.A39_ping_openrouter import ping as p_or
from A_core.A40_ping_groq import ping as p_gq
from A_core.A41_ping_pexels import ping as p_px
from A_core.A42_secrets_summary import build as b_sum


def verify():
    sr = {}
    for ck, meta in SECRETS_REGISTRY.items():
        cr = {"label": meta["label"], "required": meta["required"],
              "min_required": meta.get("min_required", 0),
              "secrets": {}, "set_count": 0, "missing_count": 0,
              "total": len(meta["secrets"])}
        for sk, sm in meta["secrets"].items():
            found, actual, length = check_env(*sm["names"])
            cr["secrets"][sk] = {"label": sm["label"], "is_set": found,
                                 "actual_name": actual if found else "", "length": length}
            if found:
                cr["set_count"] += 1
            else:
                cr["missing_count"] += 1
        if cr["missing_count"] == 0:
            cr["status"] = "complete"
        elif cr["set_count"] >= cr["min_required"]:
            cr["status"] = "partial"
        elif cr["required"]:
            cr["status"] = "critical"
        else:
            cr["status"] = "optional_missing"
        sr[ck] = cr
    ar = {"telegram": p_tg(), "facebook": p_fb(), "instagram": p_ig(),
          "google_drive": p_dr(), "openrouter": p_or(), "groq": p_gq(), "pexels": p_px()}
    return {"secrets": sr, "api_health": ar,
            "summary": b_sum(sr, ar),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
''',

    # ═══════════════════════════════════════════════════
    # B_graphics (43 files)
    # ═══════════════════════════════════════════════════
    "B_graphics/B1_font_paths.py": '''"""B1_font_paths.py — Sirf font paths."""
import os


def get_paths(script="latin", bold=True):
    weight = "Bold" if bold else "Regular"
    names = {
        "devanagari": [f"NotoSansDevanagari-{weight}.ttf", "NotoSansDevanagari-Bold.ttf"],
        "arabic": [f"NotoNaskhArabic-{weight}.ttf", "NotoNaskhArabic-Bold.ttf"],
        "latin": [f"NotoSans-{weight}.ttf", "NotoSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
    }.get(script, ["NotoSans-Bold.ttf"])
    home = os.path.expanduser("~")
    cwd = os.getcwd()
    dirs = [f"{home}/.fonts", "/usr/share/fonts/truetype/noto",
            "/usr/share/fonts/truetype/dejavu", "/Library/Fonts",
            "C:/Windows/Fonts", f"{cwd}/assets/fonts"]
    return [os.path.join(d, n) for d in dirs for n in names]
''',

    "B_graphics/B2_font_load.py": '''"""B2_font_load.py — Sirf font load."""
import os
from PIL import ImageFont
from B_graphics.B1_font_paths import get_paths


def load(size, script="latin", bold=True):
    for path in get_paths(script, bold):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()
''',

    "B_graphics/B3_font_cache.py": '''"""B3_font_cache.py — Sirf cache."""

CACHE = {}


def get(key):
    return CACHE.get(key)


def set_(key, value):
    CACHE[key] = value
''',

    "B_graphics/B4_font_info.py": '''"""B4_font_info.py — Sirf font info."""
import os
from B_graphics.B1_font_paths import get_paths


def info(script="latin", bold=True):
    for p in get_paths(script, bold):
        if os.path.exists(p):
            return {"script": script, "bold": bold, "found": p, "fallback": False}
    return {"script": script, "bold": bold, "found": None, "fallback": True}
''',

    "B_graphics/B5_text_measure.py": '''"""B5_text_measure.py — Sirf text measure."""


def measure(draw, text, font):
    if not text:
        return 0, 0, 0, 0
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox[0], bbox[1]
    except AttributeError:
        w, h = draw.textsize(text, font=font)
        return w, h, 0, 0
''',

    "B_graphics/B6_text_wrap.py": '''"""B6_text_wrap.py — Sirf text wrap."""


def wrap(draw, text, font, max_width=950):
    if not text:
        return []
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip() if current else w
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines
''',

    "B_graphics/B7_text_draw_center.py": '''"""B7_text_draw_center.py — Sirf center draw."""


def draw_centered(draw, text, y, font, fill, shadow=True,
                  offset=3, canvas_width=1080):
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (canvas_width - w) // 2 - bbox[0]
    if shadow:
        draw.text((x + offset, y + offset - bbox[1]), text, font=font, fill=(0, 0, 0, 200))
    draw.text((x, y - bbox[1]), text, font=font, fill=fill)
''',

    "B_graphics/B8_text_draw_multi.py": '''"""B8_text_draw_multi.py — Sirf multi-line draw."""
from B_graphics.B7_text_draw_center import draw_centered


def draw_multi(draw, lines, start_y, font, fill, line_spacing=12, canvas_width=1080):
    y = start_y
    for line in lines:
        if not line:
            continue
        draw_centered(draw, line, y, font, fill, canvas_width=canvas_width)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y
''',

    "B_graphics/B9_text_draw_at.py": '''"""B9_text_draw_at.py — Sirf at position draw."""


def draw_at(draw, text, x, y, font, fill, shadow=True, offset=3):
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    dx, dy = x - bbox[0], y - bbox[1]
    if shadow:
        draw.text((dx + offset, dy + offset), text, font=font, fill=(0, 0, 0, 200))
    draw.text((dx, dy), text, font=font, fill=fill)
''',

    "B_graphics/B10_sparkle_draw.py": '''"""B10_sparkle_draw.py — Sirf sparkles."""
import math
import random
from B_graphics.B11_sparkle_star import draw_star

SPARKLE_COUNT = 15
GOLD = (255, 240, 180)
WHITE = (255, 255, 255)


def draw_sparkles(draw, t, count=SPARKLE_COUNT):
    rng = random.Random(1337)
    for _ in range(count):
        bx = rng.randint(80, 1000)
        by = rng.randint(200, 1800)
        size = rng.randint(3, 9)
        phase = rng.uniform(0, 6.28)
        speed = rng.uniform(0.5, 1.5)
        dx = int(8 * math.sin(t * speed + phase))
        dy = int(6 * math.cos(t * speed * 0.7 + phase))
        pulse = math.sin(t * 2.5 * speed + phase)
        alpha = max(60, min(255, int(150 + 100 * pulse)))
        draw_star(draw, bx + dx, by + dy, size, alpha)
''',

    "B_graphics/B11_sparkle_star.py": '''"""B11_sparkle_star.py — Sirf star draw."""
GOLD = (255, 240, 180)
WHITE = (255, 255, 255)


def draw_star(draw, x, y, size, alpha):
    color = (*GOLD, alpha)
    draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
    draw.line([(x, y - size), (x, y + size)], fill=color, width=1)
    d = max(1, size // 2)
    da = int(alpha * 0.6)
    dc = (*GOLD, da)
    draw.line([(x - d, y - d), (x + d, y + d)], fill=dc, width=1)
    draw.line([(x - d, y + d), (x + d, y - d)], fill=dc, width=1)
    dot = max(1, size // 4)
    draw.ellipse([x - dot, y - dot, x + dot, y + dot],
                 fill=(*WHITE, min(255, alpha + 40)))
''',

    "B_graphics/B12_sparkle_burst.py": '''"""B12_sparkle_burst.py — Sirf burst."""
import math
from B_graphics.B11_sparkle_star import draw_star


def burst(draw, cx, cy, t, duration=1.0):
    if t < 0 or t > duration:
        return
    progress = t / duration
    count = 12
    for i in range(count):
        angle = (i / count) * 6.28
        distance = 100 * progress
        alpha = int(255 * (1 - progress))
        if alpha < 20:
            continue
        x = cx + int(distance * math.cos(angle))
        y = cy + int(distance * math.sin(angle))
        size = int(6 * (1 - progress * 0.5))
        draw_star(draw, x, y, size, alpha)
''',

    "B_graphics/B13_progress_main.py": '''"""B13_progress_main.py — Sirf progress main."""
from B_graphics.B14_progress_track import draw_track
from B_graphics.B15_progress_fill import draw_fill
from B_graphics.B16_progress_glow import draw_glow

BAR_X, BAR_W, BAR_H, BAR_Y = 80, 920, 12, 1815


def draw_progress(draw, current, total, y=BAR_Y):
    pct = 0.0 if total <= 0 else min(1.0, max(0.0, current / total))
    draw_track(draw, y)
    if pct > 0:
        fill_w = int(BAR_W * pct)
        draw_fill(draw, y, fill_w)
        draw_glow(draw, y, BAR_X + fill_w)
''',

    "B_graphics/B14_progress_track.py": '''"""B14_progress_track.py — Sirf track."""
BAR_X, BAR_W, BAR_H = 80, 920, 12


def draw_track(draw, y):
    draw.rounded_rectangle([BAR_X, y, BAR_X + BAR_W, y + BAR_H],
                           radius=BAR_H // 2,
                           fill=(0, 0, 0, 180),
                           outline=(60, 45, 20, 200), width=1)
''',

    "B_graphics/B15_progress_fill.py": '''"""B15_progress_fill.py — Sirf fill."""
BAR_X, BAR_W, BAR_H = 80, 920, 12


def draw_fill(draw, y, fill_w):
    if fill_w < BAR_H:
        fill_w = BAR_H
    draw.rounded_rectangle([BAR_X, y, BAR_X + fill_w, y + BAR_H],
                           radius=BAR_H // 2, fill=(255, 220, 120))
    if fill_w > 4:
        draw.rounded_rectangle([BAR_X + 2, y + 2, BAR_X + fill_w - 2, y + BAR_H // 2],
                               radius=BAR_H // 4, fill=(255, 245, 200, 120))
''',

    "B_graphics/B16_progress_glow.py": '''"""B16_progress_glow.py — Sirf glow."""
BAR_H = 12


def draw_glow(draw, y, glow_x):
    cy = y + BAR_H // 2
    draw.ellipse([glow_x - 14, cy - 14, glow_x + 14, cy + 14], fill=(212, 175, 55, 80))
    draw.ellipse([glow_x - 9, cy - 9, glow_x + 9, cy + 9], fill=(255, 220, 120, 180))
    draw.ellipse([glow_x - 5, cy - 5, glow_x + 5, cy + 5], fill=(255, 240, 180, 255))
''',

    "B_graphics/B17_progress_markers.py": '''"""B17_progress_markers.py — Sirf markers."""
BAR_X, BAR_W, BAR_H = 80, 920, 12


def draw_markers(draw, markers, y):
    if not markers:
        return
    cy = y + BAR_H // 2
    for pct in markers:
        pct = max(0.0, min(1.0, pct))
        mx = BAR_X + int(BAR_W * pct)
        draw.ellipse([mx - 3, cy - 3, mx + 3, cy + 3],
                     fill=(255, 250, 200, 220),
                     outline=(180, 140, 40, 255), width=1)
''',

    "B_graphics/B18_badge_main.py": '''"""B18_badge_main.py — Sirf badge."""
from B_graphics.B19_badge_fit_font import fit_font
from B_graphics.B20_badge_gradient import draw_gradient
from B_graphics.B21_badge_corners import draw_corners

BADGE_X, BADGE_Y, MAX_W = 60, 180, 700
PAD_X, PAD_Y, RADIUS = 18, 12, 10
C_BORDER = (212, 175, 55, 255)
C_BORDER_IN = (255, 215, 100, 180)
C_TEXT = (235, 210, 150, 255)


def draw_badge(draw, text, y=BADGE_Y, x=BADGE_X):
    if not text:
        return (x, y)
    font = fit_font(draw, text, MAX_W - 2 * PAD_X)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    bw, bh = tw + 2 * PAD_X, th + 2 * PAD_Y
    x1, y1, x2, y2 = x, y, x + bw, y + bh
    draw_gradient(draw, x1, y1, x2, y2)
    draw.rounded_rectangle([x1, y1, x2, y2], radius=RADIUS, outline=C_BORDER, width=2)
    draw.rounded_rectangle([x1+4, y1+4, x2-4, y2-4], radius=RADIUS-2, outline=C_BORDER_IN, width=1)
    draw_corners(draw, x1, y1, x2, y2)
    tx, ty = x1 + PAD_X, y1 + PAD_Y - bbox[1]
    draw.text((tx + 1, ty + 1), text, font=font, fill=(0, 0, 0, 200))
    draw.text((tx, ty), text, font=font, fill=C_TEXT)
    return (x2, y2)
''',

    "B_graphics/B19_badge_fit_font.py": '''"""B19_badge_fit_font.py — Sirf font fit."""
from B_graphics.B2_font_load import load


def fit_font(draw, text, max_width):
    for size in (28, 26, 24, 22, 20, 18, 16):
        font = load(size, "latin", True)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
    return load(16, "latin", True)
''',

    "B_graphics/B20_badge_gradient.py": '''"""B20_badge_gradient.py — Sirf gradient."""
C_TOP, C_BOT = (25, 18, 8, 220), (15, 10, 5, 240)


def draw_gradient(draw, x1, y1, x2, y2):
    h = y2 - y1
    if h <= 0:
        return
    steps = min(h, 40)
    strip_h = h / steps
    for i in range(steps):
        t = i / max(steps - 1, 1)
        r = int(C_TOP[0] * (1 - t) + C_BOT[0] * t)
        g = int(C_TOP[1] * (1 - t) + C_BOT[1] * t)
        b = int(C_TOP[2] * (1 - t) + C_BOT[2] * t)
        a = int(C_TOP[3] * (1 - t) + C_BOT[3] * t)
        sy = y1 + int(i * strip_h)
        ey = y1 + int((i + 1) * strip_h) + 1
        draw.rectangle([x1 + 4, sy, x2 - 4, ey], fill=(r, g, b, a))
''',

    "B_graphics/B21_badge_corners.py": '''"""B21_badge_corners.py — Sirf corners."""
C_ACCENT = (255, 220, 120, 255)


def draw_corners(draw, x1, y1, x2, y2):
    d = 4
    corners = [(x1+6, y1+6), (x2-6, y1+6), (x1+6, y2-6), (x2-6, y2-6)]
    for cx, cy in corners:
        draw.polygon([(cx, cy-d), (cx+d, cy), (cx, cy+d), (cx-d, cy)], fill=C_ACCENT)
''',

    "B_graphics/B22_word_state.py": '''"""B22_word_state.py — Sirf word state."""
from B_graphics.B23_word_empty import empty
from B_graphics.B24_word_alphas import calc

FADE_IN_END, FADE_OUT_START = 0.30, 0.70


def get_state(text, elapsed, total_dur):
    if not text:
        return empty()
    words = text.split()
    if not words:
        return empty()
    n = len(words)
    if total_dur <= 0:
        total_dur = 1.0
    wd = total_dur / n
    idx_f = elapsed / wd
    idx = int(idx_f)
    if idx < 0:
        idx, progress = 0, 0.0
    elif idx >= n:
        idx, progress = n - 1, 1.0
    else:
        progress = idx_f - idx
    current = words[idx]
    prev_w = words[idx-1] if idx > 0 else None
    next_w = words[idx+1] if idx < n-1 else None
    ca, pa, na = calc(progress)
    return {"word": current, "prev_word": prev_w, "next_word": next_w,
            "alpha": ca, "prev_alpha": pa, "next_alpha": na,
            "progress": progress, "idx": idx, "total": n}
''',

    "B_graphics/B23_word_empty.py": '''"""B23_word_empty.py — Sirf empty."""


def empty():
    return {"word": "", "prev_word": None, "next_word": None,
            "alpha": 0.0, "prev_alpha": 0.0, "next_alpha": 0.0,
            "progress": 0.0, "idx": -1, "total": 0}
''',

    "B_graphics/B24_word_alphas.py": '''"""B24_word_alphas.py — Sirf alphas."""
from B_graphics.B25_word_smooth import smooth

FADE_IN_END, FADE_OUT_START = 0.30, 0.70


def calc(progress):
    if progress < FADE_IN_END:
        p = progress / FADE_IN_END
        ca = smooth(p)
        pa = 1.0 - p
        na = 0.0
    elif progress > FADE_OUT_START:
        p = (progress - FADE_OUT_START) / (1.0 - FADE_OUT_START)
        ca = 1.0 - smooth(p)
        pa = 0.0
        na = smooth(p)
    else:
        ca, pa, na = 1.0, 0.0, 0.0
    return (max(0.0, min(1.0, ca)), max(0.0, min(1.0, pa)), max(0.0, min(1.0, na)))
''',

    "B_graphics/B25_word_smooth.py": '''"""B25_word_smooth.py — Sirf smooth."""


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)
''',

    "B_graphics/B26_bullet_lang_row.py": '''"""B26_bullet_lang_row.py — Sirf lang row."""
from B_graphics.B27_bullet_word_draw import draw_word
from B_graphics.B28_bullet_circle import draw_circle

BULLET_X, BULLET_SIZE, TEXT_X = 130, 40, 196


def draw_lang_row(draw, state, y, font, color, global_alpha):
    word = state["word"]
    if not word:
        return
    ca = state["alpha"] * global_alpha
    pa = state["prev_alpha"] * global_alpha
    na = state["next_alpha"] * global_alpha
    if state["prev_word"] and pa > 0.05:
        draw_word(draw, state["prev_word"], y, font, color, pa * 0.4, -60)
    if state["next_word"] and na > 0.05:
        draw_word(draw, state["next_word"], y, font, color, na * 0.4, 60)
    if ca > 0.05:
        draw_word(draw, word, y, font, color, ca, 0)
    draw_circle(draw, y, color, ca)
''',

    "B_graphics/B27_bullet_word_draw.py": '''"""B27_bullet_word_draw.py — Sirf word draw."""
TEXT_X = 196


def draw_word(draw, word, y, font, color, alpha, x_offset=0):
    if not word:
        return
    a = int(255 * alpha)
    if a <= 5:
        return
    x = TEXT_X + x_offset
    sa = int(a * 0.85)
    draw.text((x + 3, y + 4), word, font=font, fill=(0, 0, 0, sa))
    draw.text((x, y), word, font=font, fill=(*color, a))
''',

    "B_graphics/B28_bullet_circle.py": '''"""B28_bullet_circle.py — Sirf circle."""
BULLET_X, BULLET_SIZE = 130, 40


def draw_circle(draw, y, color, alpha):
    a = int(255 * max(alpha, 0.6))
    cy = y + BULLET_SIZE // 2 + 10
    cx = BULLET_X + BULLET_SIZE // 2
    draw.ellipse([cx - BULLET_SIZE//2 - 4, cy - BULLET_SIZE//2 - 4,
                  cx + BULLET_SIZE//2 + 4, cy + BULLET_SIZE//2 + 4],
                 fill=(*color, a // 3))
    draw.ellipse([cx - BULLET_SIZE//2, cy - BULLET_SIZE//2,
                  cx + BULLET_SIZE//2, cy + BULLET_SIZE//2],
                 fill=(*color, a), outline=(255, 255, 255, a), width=2)
''',

    "B_graphics/B29_bullets_main.py": '''"""B29_bullets_main.py — Sirf bullets main."""
from B_graphics.B2_font_load import load
from B_graphics.B22_word_state import get_state
from B_graphics.B26_bullet_lang_row import draw_lang_row

C_HINDI = (240, 130, 200)
C_URDU = (90, 170, 255)
C_ENGLISH = (255, 110, 110)
FONT_SIZE = 72
GAP = 180
Y_START = 780


def draw_bullets(draw, hindi, urdu, english, elapsed, voice_dur, y_start=Y_START, alpha=1.0):
    fh = load(FONT_SIZE, "devanagari", True)
    fa = load(FONT_SIZE, "arabic", True)
    fl = load(FONT_SIZE, "latin", True)
    hi = get_state(hindi, elapsed, voice_dur)
    ur = get_state(urdu, elapsed, voice_dur)
    en = get_state(english, elapsed, voice_dur)
    y = y_start
    draw_lang_row(draw, hi, y, fh, C_HINDI, alpha)
    y += GAP
    draw_lang_row(draw, ur, y, fa, C_URDU, alpha)
    y += GAP
    draw_lang_row(draw, en, y, fl, C_ENGLISH, alpha)
''',

    "B_graphics/B30_bullets_sync.py": '''"""B30_bullets_sync.py — Sirf sync info."""
from B_graphics.B22_word_state import get_state


def get_info(hindi, urdu, english, elapsed, voice_dur):
    return {
        "elapsed": round(elapsed, 2), "voice_dur": round(voice_dur, 2),
        "progress_pct": round(100 * elapsed / max(voice_dur, 0.01), 1),
        "hindi": {"word_count": len(hindi.split()) if hindi else 0,
                  "current_idx": get_state(hindi, elapsed, voice_dur)["idx"]},
        "urdu": {"word_count": len(urdu.split()) if urdu else 0,
                 "current_idx": get_state(urdu, elapsed, voice_dur)["idx"]},
        "english": {"word_count": len(english.split()) if english else 0,
                    "current_idx": get_state(english, elapsed, voice_dur)["idx"]},
    }
''',

    "B_graphics/B31_watermark_main.py": '''"""B31_watermark_main.py — Sirf watermark."""
import os
from PIL import Image
from B_graphics.B32_watermark_position import calc_position


def draw_watermark(img, logo_path="avatar.png", size=(160, 68),
                   pos="top-right", opacity=0.55):
    if not os.path.exists(logo_path):
        return
    try:
        wm = Image.open(logo_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        alpha = wm.split()[3].point(lambda v: int(v * opacity))
        wm.putalpha(alpha)
        x, y = calc_position(img, size, pos)
        img.paste(wm, (x, y), wm)
    except Exception:
        pass
''',

    "B_graphics/B32_watermark_position.py": '''"""B32_watermark_position.py — Sirf position."""


def calc_position(img, size, pos="top-right", margin=30):
    w, h = size
    if pos == "top-right":
        return (img.width - w - margin, 180)
    if pos == "top-left":
        return (margin, 180)
    if pos == "bottom-right":
        return (img.width - w - margin, img.height - h - 250)
    return (margin, img.height - h - 250)
''',

    "B_graphics/B33_watermark_text.py": '''"""B33_watermark_text.py — Sirf text watermark."""
from PIL import ImageDraw


def draw_text(img, text="SAWAJ STUDIO", font=None, pos="bottom-right", opacity=120):
    if not text or font is None:
        return
    try:
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        margin = 40
        if pos == "bottom-right":
            x, y = img.width - tw - margin, img.height - th - margin - 200
        elif pos == "bottom-left":
            x, y = margin, img.height - th - margin - 200
        elif pos == "top-right":
            x, y = img.width - tw - margin, margin
        else:
            x, y = margin, margin
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
    except Exception:
        pass
''',

    "B_graphics/B34_logo_float.py": '''"""B34_logo_float.py — Sirf floating logo."""
import os
import math
from PIL import Image


def draw_floating_logo(img, t, logo_path="avatar.png", size=(240, 100)):
    if not os.path.exists(logo_path):
        return
    try:
        logo = Image.open(logo_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        bx, by = 80, 1480
        dx = int(25 * math.sin(t * 0.7))
        dy = int(18 * math.sin(t * 1.1))
        x = max(10, min(bx + dx, img.width - size[0] - 10))
        y = max(10, min(by + dy, img.height - size[1] - 250))
        img.paste(logo, (x, y), logo)
    except Exception:
        pass
''',

    "B_graphics/B35_arabesque_main.py": '''"""B35_arabesque_main.py — Sirf arabesque."""
import math


def draw_arabesque(draw, t, opacity=30):
    cx, cy = 540, 960
    r = 200 + int(20 * math.sin(t * 0.5))
    for i in range(8):
        angle = (i * math.pi / 4) + t * 0.1
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle))
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(212, 175, 55, opacity))
''',

    "B_graphics/B36_rays_draw.py": '''"""B36_rays_draw.py — Sirf rays draw."""
import math

RAY_COUNT, RAY_SPREAD = 7, 0.18
RAY_LENGTH, RAY_WIDTH_TOP, RAY_WIDTH_BOTTOM = 1200, 30, 120
BASE_COLOR = (255, 240, 180)


def draw_god_rays(draw, t, opacity=35, canvas_w=1080, canvas_h=1920):
    cx = canvas_w // 2
    rotation = 0.04 * math.sin(t * 0.3)
    for i in range(RAY_COUNT):
        offset = (i - (RAY_COUNT - 1) / 2) * RAY_SPREAD
        angle = -math.pi / 2 + offset + rotation
        dist = abs(i - (RAY_COUNT - 1) / 2) / ((RAY_COUNT - 1) / 2)
        a = int(opacity * (1 - dist * 0.7))
        pulse = 0.7 + 0.3 * math.sin(t * 1.2 + i * 0.9)
        a = int(a * pulse)
        if a < 3:
            continue
        xe = cx + int(RAY_LENGTH * math.cos(angle))
        ye = int(RAY_LENGTH * math.sin(angle))
        px = int(math.sin(angle) * RAY_WIDTH_BOTTOM / 2)
        py = int(-math.cos(angle) * RAY_WIDTH_BOTTOM / 2)
        draw.polygon([(cx - RAY_WIDTH_TOP//2, 0),
                      (cx + RAY_WIDTH_TOP//2, 0),
                      (xe + px, ye + py),
                      (xe - px, ye - py)],
                     fill=(*BASE_COLOR, a))
''',

    "B_graphics/B37_rays_apply.py": '''"""B37_rays_apply.py — Sirf rays apply."""
from PIL import Image, ImageDraw, ImageFilter
from B_graphics.B36_rays_draw import draw_god_rays

BLUR_RADIUS = 12


def apply_god_rays(img, t, opacity=35):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay)
    draw_god_rays(ov, t, opacity, img.width, img.height)
    overlay = overlay.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
    return Image.alpha_composite(img.convert("RGBA"), overlay)
''',

    "B_graphics/B38_stars_draw.py": '''"""B38_stars_draw.py — Sirf stars."""
import math
import random


def draw_stars(draw, t, count=40):
    rng = random.Random(42)
    for _ in range(count):
        x = rng.randint(0, 1080)
        y = rng.randint(0, 1920)
        size = rng.randint(1, 3)
        twinkle = abs(math.sin(t * 2 + x * 0.01))
        alpha = int(100 + 155 * twinkle)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255, alpha))
''',

    "B_graphics/B39_ember_draw.py": '''"""B39_ember_draw.py — Sirf embers."""
import math
import random
from B_graphics.B40_ember_single import draw_single

EMBER_COUNT = 20


def draw_embers(draw, t, count=EMBER_COUNT):
    rng = random.Random(4242)
    for _ in range(count):
        bx = rng.randint(40, 1040)
        by = rng.randint(0, 1920)
        size = rng.randint(2, 6)
        speed = rng.uniform(30, 80)
        phase = rng.uniform(0, 6.28)
        ab = rng.randint(150, 240)
        rise = (t * speed) % 1920
        y = (by - rise) % 1920
        x = bx + int(15 * math.sin(t * 0.8 + phase))
        pulse = math.sin(t * 3 + phase)
        a = max(80, min(255, int(ab * (0.7 + 0.3 * pulse))))
        draw_single(draw, x, y, size, a)
''',

    "B_graphics/B40_ember_single.py": '''"""B40_ember_single.py — Sirf single ember."""
BASE_COLOR = (255, 140, 60)
GLOW_COLOR = (255, 180, 100)


def draw_single(draw, x, y, size, alpha):
    gs = size * 3
    ga = alpha // 4
    draw.ellipse([x-gs, y-gs, x+gs, y+gs], fill=(*GLOW_COLOR, ga))
    ms = size * 2
    ma = alpha // 2
    draw.ellipse([x-ms, y-ms, x+ms, y+ms], fill=(*GLOW_COLOR, ma))
    draw.ellipse([x-size, y-size, x+size, y+size], fill=(*BASE_COLOR, alpha))
''',

    "B_graphics/B41_vignette_draw.py": '''"""B41_vignette_draw.py — Sirf vignette."""
import math
from B_graphics.B42_vignette_ring import draw_ring_band

RING_COUNT, PULSE_AMOUNT = 12, 12


def draw_vignette(draw, t, intensity=60, canvas_w=1080, canvas_h=1920):
    pulse = int(PULSE_AMOUNT * math.sin(t * 0.8))
    base = max(20, min(100, intensity + pulse))
    max_dist = int(math.sqrt(canvas_w**2 + canvas_h**2) / 2)
    for i in range(RING_COUNT):
        ratio = 1.0 - (i / RING_COUNT)
        curve = ratio ** 2.5
        alpha = int(base * curve)
        if alpha < 2:
            continue
        margin = int((1 - ratio) * max_dist * 0.5)
        draw_ring_band(draw, canvas_w, canvas_h, margin, alpha)
''',

    "B_graphics/B42_vignette_ring.py": '''"""B42_vignette_ring.py — Sirf ring band."""


def draw_ring_band(draw, w, h, margin, alpha):
    color = (0, 0, 0, alpha)
    draw.rectangle([0, 0, w, margin], fill=color)
    draw.rectangle([0, h - margin, w, h], fill=color)
    draw.rectangle([0, margin, margin, h - margin], fill=color)
    draw.rectangle([w - margin, margin, w, h - margin], fill=color)
''',

    "B_graphics/B43_vignette_radial.py": '''"""B43_vignette_radial.py — Sirf radial."""
import math
from PIL import Image


def apply_radial_vignette(img, t=0.0, intensity=0.6):
    pulse = 0.1 * math.sin(t * 0.8)
    ai = max(0.0, min(1.0, intensity + pulse))
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    px = mask.load()
    cx, cy = w / 2, h / 2
    md = math.sqrt(cx**2 + cy**2)
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2) / md
            if dist < 0.4:
                v = 0
            elif dist > 0.9:
                v = int(255 * ai)
            else:
                tn = (dist - 0.4) / 0.5
                ts = tn * tn * (3 - 2 * tn)
                v = int(255 * ai * ts)
            for dy in range(4):
                for dx in range(4):
                    if y + dy < h and x + dx < w:
                        px[x + dx, y + dy] = v
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    black.putalpha(mask)
    return Image.alpha_composite(img.convert("RGBA"), black)
''',

    # ═══════════════════════════════════════════════════
    # C_content (46 files)
    # ═══════════════════════════════════════════════════
    "C_content/C1_hadith_fallback.py": '''"""C1_hadith_fallback.py — Sirf fallback."""
FALLBACK = {
    "collection": "Sahih al-Bukhari",
    "number": "1",
    "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.",
    "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
}
''',

    "C_content/C2_hadith_count.py": '''"""C2_hadith_count.py — Sirf count."""


def count(text):
    return len(text.split()) if text else 0
''',

    "C_content/C3_hadith_fetch_one.py": '''"""C3_hadith_fetch_one.py — Sirf fetch one."""
from A_core.A26_sanitize import sanitize
from C_content.C2_hadith_count import count


def fetch_one(session, base_url, book, num):
    try:
        url = f"{base_url}/editions/{book['eng']}/{num}.json"
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            return None
        hs = r.json().get("hadiths", [])
        if not hs:
            return None
        eng = sanitize(hs[0].get("text", ""))
        if len(eng) < 30:
            return None
        ara = ""
        try:
            ar = session.get(url.replace(book["eng"], book["ara"]), timeout=10)
            if ar.status_code == 200:
                ad = ar.json().get("hadiths", [])
                if ad:
                    ara = sanitize(ad[0].get("text", ""))
        except Exception:
            pass
        return {"collection": book["name"], "number": str(hs[0].get("hadithnumber") or num),
                "english": eng, "arabic": ara, "word_count": count(eng)}
    except Exception:
        return None
''',

    "C_content/C4_hadith_books.py": '''"""C4_hadith_books.py — Sirf books."""
BOOKS = [
    {"eng": "eng-bukhari", "ara": "ara-bukhari", "name": "Sahih al-Bukhari", "max": 7000},
    {"eng": "eng-muslim", "ara": "ara-muslim", "name": "Sahih Muslim", "max": 5000},
    {"eng": "eng-abudawud", "ara": "ara-abudawud", "name": "Sunan Abu Dawud", "max": 4000},
    {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi", "name": "Jami at-Tirmidhi", "max": 3500},
]
''',

    "C_content/C5_hadith_main.py": '''"""C5_hadith_main.py — Sirf main fetch."""
import os
import random
from A_core.A9_log_step import log_step
from A_core.A10_log_api import log_api
from C_content.C1_hadith_fallback import FALLBACK
from C_content.C3_hadith_fetch_one import fetch_one
from C_content.C4_hadith_books import BOOKS

TARGET_MIN, TARGET_MAX = 50, 100
FALLBACK_MIN, FALLBACK_MAX = 30, 150


def fetch(session):
    bases = []
    if os.environ.get("HADITH_API_URL"):
        bases.append(os.environ["HADITH_API_URL"].rstrip("/"))
    bases += ["https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
              "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1"]

    log_step("C5_hadith_main.py", f"Phase 1: {TARGET_MIN}-{TARGET_MAX}", "info")
    for _ in range(25):
        book = random.choice(BOOKS)
        num = random.randint(1, book["max"])
        for base in bases:
            h = fetch_one(session, base, book, num)
            if h and TARGET_MIN <= h["word_count"] <= TARGET_MAX:
                log_api("C5_hadith_main.py", "Found", "success", f"{h['word_count']}w")
                return {k: v for k, v in h.items() if k != "word_count"}

    log_step("C5_hadith_main.py", f"Phase 2: {FALLBACK_MIN}-{FALLBACK_MAX}", "warn")
    for _ in range(25):
        book = random.choice(BOOKS)
        num = random.randint(1, book["max"])
        for base in bases:
            h = fetch_one(session, base, book, num)
            if h and FALLBACK_MIN <= h["word_count"] <= FALLBACK_MAX:
                log_api("C5_hadith_main.py", "Fallback", "fallback", f"{h['word_count']}w")
                return {k: v for k, v in h.items() if k != "word_count"}

    log_step("C5_hadith_main.py", "Phase 3: any", "warn")
    for _ in range(10):
        book = random.choice(BOOKS)
        num = random.randint(1, book["max"])
        for base in bases:
            h = fetch_one(session, base, book, num)
            if h:
                log_api("C5_hadith_main.py", "Any", "fallback", f"{h['word_count']}w")
                return {k: v for k, v in h.items() if k != "word_count"}

    log_api("C5_hadith_main.py", "Hardcoded", "fallback")
    return FALLBACK
''',

    "C_content/C6_ai_get_key.py": '''"""C6_ai_get_key.py — Sirf key lena."""
import os


def get_key(*names):
    for name in names:
        val = os.environ.get(name, "").strip()
        if val:
            return val
    return ""
''',

    "C_content/C7_ai_openrouter.py": '''"""C7_ai_openrouter.py — Sirf OpenRouter."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "openai/gpt-4o-mini",
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.7, "max_tokens": max_tokens}, timeout=40)
        if r.status_code == 200:
            log_api("C7_ai_openrouter.py", "OpenRouter", "success")
            return r.json()["choices"][0]["message"]["content"].strip()
        log_api("C7_ai_openrouter.py", "OpenRouter", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C7_ai_openrouter.py", "OpenRouter", "failed", str(e)[:60])
    return None
''',

    "C_content/C8_ai_groq.py": '''"""C8_ai_groq.py — Sirf Groq."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("GROQ_API_KEY", "GROQ_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "llama-3.3-70b-versatile",
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.7, "max_tokens": max_tokens}, timeout=40)
        if r.status_code == 200:
            log_api("C8_ai_groq.py", "Groq", "success")
            return r.json()["choices"][0]["message"]["content"].strip()
        log_api("C8_ai_groq.py", "Groq", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C8_ai_groq.py", "Groq", "failed", str(e)[:60])
    return None
''',

    "C_content/C9_ai_gemini.py": '''"""C9_ai_gemini.py — Sirf Gemini."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("GEMINI_API_KEY", "GEMINI_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={key}",
            json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=40)
        if r.status_code == 200:
            log_api("C9_ai_gemini.py", "Gemini", "success")
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        log_api("C9_ai_gemini.py", "Gemini", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C9_ai_gemini.py", "Gemini", "failed", str(e)[:60])
    return None
''',

    "C_content/C10_ai_mistral.py": '''"""C10_ai_mistral.py — Sirf Mistral."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("MISTRAL_API_KEY", "MISTRAL_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "mistral-small-latest",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens}, timeout=40)
        if r.status_code == 200:
            log_api("C10_ai_mistral.py", "Mistral", "success")
            return r.json()["choices"][0]["message"]["content"].strip()
        log_api("C10_ai_mistral.py", "Mistral", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C10_ai_mistral.py", "Mistral", "failed", str(e)[:60])
    return None
''',

    "C_content/C11_ai_cerebras.py": '''"""C11_ai_cerebras.py — Sirf Cerebras."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://api.cerebras.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "llama3.1-8b",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens}, timeout=40)
        if r.status_code == 200:
            log_api("C11_ai_cerebras.py", "Cerebras", "success")
            return r.json()["choices"][0]["message"]["content"].strip()
        log_api("C11_ai_cerebras.py", "Cerebras", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C11_ai_cerebras.py", "Cerebras", "failed", str(e)[:60])
    return None
''',

    "C_content/C12_ai_cohere.py": '''"""C12_ai_cohere.py — Sirf Cohere."""
from A_core.A10_log_api import log_api
from C_content.C6_ai_get_key import get_key


def call(session, prompt, max_tokens):
    key = get_key("COHERE_API_KEY", "COHERE_API_KEY_AI")
    if not key:
        return None
    try:
        r = session.post(
            "https://api.cohere.com/v1/chat",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "command-r-plus", "message": prompt}, timeout=40)
        if r.status_code == 200:
            log_api("C12_ai_cohere.py", "Cohere", "success")
            return r.json()["text"].strip()
        log_api("C12_ai_cohere.py", "Cohere", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C12_ai_cohere.py", "Cohere", "failed", str(e)[:60])
    return None
''',

    "C_content/C13_ai_main.py": '''"""C13_ai_main.py — Sirf AI main call."""
from A_core.A9_log_step import log_step
from C_content.C7_ai_openrouter import call as or_call
from C_content.C8_ai_groq import call as gq_call
from C_content.C9_ai_gemini import call as gm_call
from C_content.C10_ai_mistral import call as ms_call
from C_content.C11_ai_cerebras import call as cb_call
from C_content.C12_ai_cohere import call as ch_call


def call(session, prompt, max_tokens=400, task="general"):
    log_step("C13_ai_main.py", f"call({task})", "ok")
    for name, fn in [("OpenRouter", or_call), ("Groq", gq_call),
                     ("Gemini", gm_call), ("Mistral", ms_call),
                     ("Cerebras", cb_call), ("Cohere", ch_call)]:
        log_step("C13_ai_main.py", f"Trying {name}", "info")
        res = fn(session, prompt, max_tokens)
        if res:
            return res
    log_step("C13_ai_main.py", "All failed", "fail")
    return None
''',

    "C_content/C14_translate_deepl.py": '''"""C14_translate_deepl.py — Sirf DeepL."""
import os
from A_core.A10_log_api import log_api


def translate(session, text):
    key = os.environ.get("DEEPL_API_KEY")
    if not key:
        log_api("C14_translate_deepl.py", "DeepL", "skipped")
        return None
    try:
        r = session.post(
            "https://api-free.deepl.com/v2/translate",
            headers={"Authorization": f"DeepL-Auth-Key {key}"},
            data={"text": text, "target_lang": "HI"}, timeout=25)
        if r.status_code == 200:
            log_api("C14_translate_deepl.py", "DeepL", "success")
            return r.json()["translations"][0]["text"]
        log_api("C14_translate_deepl.py", "DeepL", "failed", f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C14_translate_deepl.py", "DeepL", "failed", str(e)[:60])
    return None
''',

    "C_content/C15_translate_main.py": '''"""C15_translate_main.py — Sirf Hindi main."""
from A_core.A9_log_step import log_step
from C_content.C13_ai_main import call as ai_call
from C_content.C14_translate_deepl import translate as deepl


def to_hindi(session, english):
    log_step("C15_translate_main.py", "to_hindi", "ok")
    h = deepl(session, english)
    if h:
        return h
    log_step("C15_translate_main.py", "DeepL fail → AI", "warn")
    res = ai_call(session,
                  f"Is English Hadith ka soft accurate Hindi tarjuma likho. "
                  f"Sirf tarjuma. Kuch mat chhodo.\\n\\n{english}",
                  task="hindi")
    if res:
        return res
    log_step("C15_translate_main.py", "Hardcoded", "warn")
    return "अमल का दारोमदार नीयतों पर है।"
''',

    "C_content/C16_tts_constants.py": '''"""C16_tts_constants.py — Sirf constants."""
DEFAULT_VOICE = "hi-IN-MadhurNeural"
DEFAULT_RATE = "-7%"
DEFAULT_PITCH = "-2Hz"
DEFAULT_VOLUME = "+8%"
MIN_AUDIO_SIZE = 1000
ELEVEN_TIMEOUT = 90
EDGE_TIMEOUT = 120
''',

    "C_content/C17_tts_elevenlabs.py": '''"""C17_tts_elevenlabs.py — Sirf ElevenLabs."""
import os
from A_core.A10_log_api import log_api
from C_content.C16_tts_constants import MIN_AUDIO_SIZE, ELEVEN_TIMEOUT


def generate(session, text, outfile):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return False
    try:
        r = session.post(
            "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
            headers={"Accept": "audio/mpeg",
                     "Content-Type": "application/json",
                     "xi-api-key": key},
            json={"text": text, "model_id": "eleven_multilingual_v2",
                  "voice_settings": {"stability": 0.42, "similarity_boost": 0.82,
                                     "style": 0.35, "use_speaker_boost": True}},
            timeout=ELEVEN_TIMEOUT)
        if r.status_code == 200 and len(r.content) > MIN_AUDIO_SIZE:
            with open(outfile, "wb") as f:
                f.write(r.content)
            log_api("C17_tts_elevenlabs.py", "ElevenLabs", "success",
                    f"{len(r.content)//1024} KB")
            return True
        log_api("C17_tts_elevenlabs.py", "ElevenLabs", "failed",
                f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C17_tts_elevenlabs.py", "ElevenLabs", "failed", str(e)[:60])
    return False
''',

    "C_content/C18_tts_edge.py": '''"""C18_tts_edge.py — Sirf Edge-TTS."""
import os
import asyncio
from A_core.A10_log_api import log_api
from C_content.C16_tts_constants import (
    DEFAULT_VOICE, DEFAULT_PITCH, DEFAULT_VOLUME,
    MIN_AUDIO_SIZE, EDGE_TIMEOUT)


def generate(text, outfile, rate="-7%"):
    try:
        import edge_tts
    except ImportError:
        log_api("C18_tts_edge.py", "edge-tts", "failed", "not installed")
        return False

    async def _run():
        c = edge_tts.Communicate(text, DEFAULT_VOICE, rate=rate,
                                 pitch=DEFAULT_PITCH, volume=DEFAULT_VOLUME)
        await c.save(outfile)

    try:
        asyncio.run(asyncio.wait_for(_run(), timeout=EDGE_TIMEOUT))
    except asyncio.TimeoutError:
        log_api("C18_tts_edge.py", "edge-tts", "failed", "timeout")
        return False
    except Exception as e:
        log_api("C18_tts_edge.py", "edge-tts", "failed", str(e)[:60])
        return False

    if not os.path.exists(outfile) or os.path.getsize(outfile) < MIN_AUDIO_SIZE:
        return False
    log_api("C18_tts_edge.py", "edge-tts", "success",
            f"{os.path.getsize(outfile)//1024} KB")
    return True
''',

    "C_content/C19_tts_gtts.py": '''"""C19_tts_gtts.py — Sirf gTTS."""
import os
from A_core.A10_log_api import log_api
from C_content.C16_tts_constants import MIN_AUDIO_SIZE


def generate(text, outfile):
    try:
        from gtts import gTTS
    except ImportError:
        log_api("C19_tts_gtts.py", "gTTS", "failed", "not installed")
        return False
    try:
        gTTS(text=text, lang="hi", slow=False).save(outfile)
        if os.path.getsize(outfile) < MIN_AUDIO_SIZE:
            return False
        log_api("C19_tts_gtts.py", "gTTS", "success")
        return True
    except Exception as e:
        log_api("C19_tts_gtts.py", "gTTS", "failed", str(e)[:60])
        return False
''',

    "C_content/C20_tts_main.py": '''"""C20_tts_main.py — Sirf TTS main."""
import os
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error
from C_content.C17_tts_elevenlabs import generate as el_gen
from C_content.C18_tts_edge import generate as edge_gen
from C_content.C19_tts_gtts import generate as gtts_gen


def generate(session, text, outfile, rate=None):
    if rate is None:
        rate = "-7%"
    if not text or len(text) < 2:
        log_error("C20_tts_main.py", "Text empty")
        return False

    log_step("C20_tts_main.py", f"generate({os.path.basename(outfile)})", "ok")
    if os.environ.get("ELEVENLABS_API_KEY") and el_gen(session, text, outfile):
        return True
    if edge_gen(text, outfile, rate):
        return True
    if gtts_gen(text, outfile):
        return True
    log_error("C20_tts_main.py", "All TTS failed")
    return False
''',

    "C_content/C21_music_constants.py": '''"""C21_music_constants.py — Sirf constants."""
MUSIC_VOL = 0.22
MUSIC_DUR = 60
MIN_MUSIC_SIZE = 100 * 1024
''',

    "C_content/C22_music_freesound.py": '''"""C22_music_freesound.py — Sirf Freesound."""
import os
import random
from A_core.A10_log_api import log_api


def fetch(base, outfile):
    key = os.environ.get("FREESOUND_API_KEY")
    if not key:
        return False
    try:
        r = base.session.get(
            "https://freesound.org/apiv2/search/text/",
            params={"query": "soft ambient meditation islamic peaceful",
                    "filter": "duration:[30 TO 180]",
                    "fields": "id,name,previews",
                    "page_size": 10, "token": key}, timeout=14)
        if r.status_code != 200:
            return False
        results = r.json().get("results", [])
        if not results:
            return False
        track = random.choice(results)
        url = track.get("previews", {}).get("preview-hq-mp3") or \\
              track.get("previews", {}).get("preview-lq-mp3")
        if not url:
            return False
        if not base.download(url, "music_raw.mp3"):
            return False
        log_api("C22_music_freesound.py", "Freesound", "success")
        return True
    except Exception as e:
        log_api("C22_music_freesound.py", "Freesound", "failed", str(e)[:60])
        return False
''',

    "C_content/C23_music_pixabay.py": '''"""C23_music_pixabay.py — Sirf Pixabay."""
from A_core.A10_log_api import log_api


def fetch(base):
    urls = [
        "https://cdn.pixabay.com/download/audio/2022/03/10/audio_2ba9c69e71.mp3?filename=meditation-relax-music-115480.mp3",
        "https://cdn.pixabay.com/download/audio/2022/08/02/audio_b6f7c5e8c4.mp3?filename=ambient-piano-amp-strings-10711.mp3",
        "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
    ]
    for i, u in enumerate(urls, 1):
        if base.download(u, "music_raw.mp3"):
            log_api("C23_music_pixabay.py", f"Pixabay #{i}", "success")
            return True
    return False
''',

    "C_content/C24_music_bensound.py": '''"""C24_music_bensound.py — Sirf Bensound."""
from A_core.A10_log_api import log_api


def fetch(base):
    urls = [
        "https://www.bensound.com/bensound-music/bensound-relaxing.mp3",
        "https://www.bensound.com/bensound-music/bensound-slowmotion.mp3",
    ]
    for i, u in enumerate(urls, 1):
        if base.download(u, "music_raw.mp3"):
            log_api("C24_music_bensound.py", f"Bensound #{i}", "success")
            return True
    return False
''',

    "C_content/C25_music_process.py": '''"""C25_music_process.py — Sirf processing."""
import os
from C_content.C21_music_constants import MUSIC_VOL, MUSIC_DUR


def process(base, infile, outfile):
    fade_out_start = MUSIC_DUR - 5
    cmd = (f'ffmpeg -y -stream_loop -1 -i "{infile}" '
           f'-af "volume={MUSIC_VOL},'
           f'afade=t=in:st=0:d=2,'
           f'afade=t=out:st={fade_out_start}:d=5" '
           f'-t {MUSIC_DUR} "{outfile}"')
    base.run_cmd(cmd)
    try:
        if os.path.exists(infile) and infile != outfile:
            os.remove(infile)
    except Exception:
        pass
''',

    "C_content/C26_music_sine.py": '''"""C26_music_sine.py — Sirf sine."""
from C_content.C21_music_constants import MUSIC_DUR


def generate(base, outfile):
    cmd = (f'ffmpeg -y '
           f'-f lavfi -i "sine=frequency=110:duration={MUSIC_DUR}" '
           f'-f lavfi -i "sine=frequency=165:duration={MUSIC_DUR}" '
           f'-filter_complex "[0:a][1:a]amix=inputs=2:duration=longest,'
           f'volume=0.12,afade=t=in:st=0:d=2.5,'
           f'afade=t=out:st={MUSIC_DUR-10}:d=6" '
           f'"{outfile}"')
    base.run_cmd(cmd)
''',

    "C_content/C27_music_main.py": '''"""C27_music_main.py — Sirf music main."""
import os
from A_core.A9_log_step import log_step
from C_content.C22_music_freesound import fetch as fs_fetch
from C_content.C23_music_pixabay import fetch as px_fetch
from C_content.C24_music_bensound import fetch as bs_fetch
from C_content.C25_music_process import process
from C_content.C26_music_sine import generate


def get(base, outfile="music_soft.mp3"):
    log_step("C27_music_main.py", "get()", "ok")
    if os.environ.get("FREESOUND_API_KEY") and fs_fetch(base, outfile):
        process(base, "music_raw.mp3", outfile)
        return outfile
    if px_fetch(base):
        process(base, "music_raw.mp3", outfile)
        return outfile
    if bs_fetch(base):
        process(base, "music_raw.mp3", outfile)
        return outfile
    generate(base, outfile)
    return outfile
''',

    "C_content/C28_bg_scale_filter.py": '''"""C28_bg_scale_filter.py — Sirf scale filter."""
TARGET_W, TARGET_H = 1080, 1920
DARKEN_FILTER = ("eq=contrast=1.10:brightness=0.02:saturation=1.12,"
                 "vignette=PI/5")


def build():
    return (f"scale=1200:2140:force_original_aspect_ratio=increase,"
            f"crop={TARGET_W}:{TARGET_H},"
            f"zoompan=z='min(zoom+0.0004,1.06)':d=1:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={TARGET_W}x{TARGET_H},"
            f"setsar=1,{DARKEN_FILTER}")
''',

    "C_content/C29_bg_pexels.py": '''"""C29_bg_pexels.py — Sirf Pexels."""
import os
import random
from A_core.A10_log_api import log_api


def fetch(base, total_dur, outfile):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return False
    queries = ["islamic architecture night", "mosque night",
               "night sky stars", "desert night", "kaaba night"]
    for q in random.sample(queries, min(4, len(queries))):
        try:
            r = base.session.get(
                "https://api.pexels.com/videos/search",
                params={"query": q, "orientation": "portrait",
                        "per_page": 6, "size": "medium"},
                headers={"Authorization": key}, timeout=14)
            if r.status_code != 200:
                continue
            vids = r.json().get("videos", [])
            if not vids:
                continue
            video = random.choice(vids)
            files = sorted(video.get("video_files", []),
                           key=lambda x: x.get("width", 0), reverse=True)
            if not files:
                continue
            if base.download(files[0].get("link"), "tmp_bg.mp4", 50000):
                log_api("C29_bg_pexels.py", "Pexels", "success", q)
                return True
        except Exception as e:
            log_api("C29_bg_pexels.py", "Pexels", "failed", str(e)[:50])
    return False
''',

    "C_content/C30_bg_pixabay.py": '''"""C30_bg_pixabay.py — Sirf Pixabay."""
import os
import random
from A_core.A10_log_api import log_api


def fetch(base):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        return False
    try:
        r = base.session.get(
            "https://pixabay.com/api/videos/",
            params={"key": key, "q": "mosque night",
                    "orientation": "vertical", "per_page": 10,
                    "safesearch": "true"}, timeout=14)
        if r.status_code != 200:
            return False
        hits = r.json().get("hits", [])
        if not hits:
            return False
        hit = random.choice(hits)
        v = hit.get("videos", {})
        url = (v.get("large", {}).get("url") or
               v.get("medium", {}).get("url") or
               v.get("small", {}).get("url"))
        if not url:
            return False
        if base.download(url, "tmp_bg.mp4", 50000):
            log_api("C30_bg_pixabay.py", "Pixabay", "success")
            return True
    except Exception as e:
        log_api("C30_bg_pixabay.py", "Pixabay", "failed", str(e)[:60])
    return False
''',

    "C_content/C31_bg_process.py": '''"""C31_bg_process.py — Sirf bg process."""
import os
from C_content.C28_bg_scale_filter import build


def process(base, infile, outfile, duration):
    cmd = (f'ffmpeg -y -stream_loop -1 -i "{infile}" '
           f'-vf "{build()}" -t {duration:.2f} -an '
           f'-c:v libx264 -preset veryfast -crf 20 "{outfile}"')
    base.run_cmd(cmd)
    try:
        if os.path.exists(infile):
            os.remove(infile)
    except Exception:
        pass
''',

    "C_content/C32_bg_gradient.py": '''"""C32_bg_gradient.py — Sirf gradient."""
import random
from C_content.C28_bg_scale_filter import TARGET_W, TARGET_H


def generate(base, duration, outfile):
    c0 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
    c1 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
    cmd = (f'ffmpeg -y -f lavfi -i "gradients=s={TARGET_W}x{TARGET_H}:'
           f'c0=0x{c0}:c1=0x{c1}:speed=0.006" '
           f'-t {duration:.2f} -c:v libx264 -preset veryfast -crf 20 "{outfile}"')
    base.run_cmd(cmd)
''',

    "C_content/C33_bg_random_hex.py": '''"""C33_bg_random_hex.py — Sirf hex."""
import random


def get():
    return (f"{random.randint(10,30):02x}"
            f"{random.randint(8,25):02x}"
            f"{random.randint(25,55):02x}")
''',

    "C_content/C34_bg_main.py": '''"""C34_bg_main.py — Sirf bg main."""
from A_core.A9_log_step import log_step
from C_content.C29_bg_pexels import fetch as px_fetch
from C34_imports_patch import *  # noqa
''',

    "C_content/C35_logo_make.py": '''"""C35_logo_make.py — Sirf logo make."""
import os
from PIL import Image, ImageDraw, ImageFilter
from A_core.A9_log_step import log_step


def make(outfile="avatar.png"):
    log_step("C35_logo_make.py", "make()", "ok")
    for src in ["logo.png", "logo.jpg", "assets/logo.png", "assets/logo.jpg",
                "../../video_requirement/logo.png"]:
        if os.path.exists(src):
            try:
                img = Image.open(src).convert("RGBA")
                if img.width > 400:
                    ratio = 400 / img.width
                    img = img.resize((400, int(img.height * ratio)),
                                     Image.Resampling.LANCZOS)
                border, bottom = 12, 26
                nw = img.width + border * 2
                nh = img.height + border + bottom
                canvas = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
                draw = ImageDraw.Draw(canvas)
                draw.rectangle([0, 0, nw-1, nh-1], outline=(212, 175, 55, 255), width=border)
                draw.rectangle([border, border, nw-border-1, nh-bottom-1],
                               outline=(255, 215, 100, 200), width=2)
                draw.rectangle([0, nh-bottom, nw-1, nh-1], fill=(20, 15, 8, 245))
                canvas.paste(img, (border, border), img)
                glow = canvas.filter(ImageFilter.GaussianBlur(6))
                final = Image.alpha_composite(glow, canvas)
                final.save(outfile)
                log_step("C35_logo_make.py", f"Saved {outfile}", "ok")
                return True
            except Exception as e:
                log_step("C35_logo_make.py", f"err {src}", "fail", str(e)[:50])
    log_step("C35_logo_make.py", "No logo", "fail")
    return False
''',

    "C_content/C36_thumb_constants.py": '''"""C36_thumb_constants.py — Sirf constants."""
W, H = 1080, 1920
C_BG_DARK = (18, 14, 8)
C_BG_GRAD_TOP = (18, 14, 8)
C_BG_GRAD_BOTTOM = (48, 34, 23)
C_GOLD = (212, 175, 55)
C_GOLD_BRIGHT = (255, 215, 100)
C_TEXT_GOLD = (230, 200, 130)
C_TEXT_BRIGHT = (255, 240, 200)
C_WHITE = (255, 255, 255)
C_HINDI = (240, 130, 200)
C_URDU = (90, 170, 255)
C_ENGLISH = (255, 110, 110)
''',

    "C_content/C37_thumb_gradient.py": '''"""C37_thumb_gradient.py — Sirf gradient."""
from C_content.C36_thumb_constants import (W, H, C_BG_GRAD_TOP, C_BG_GRAD_BOTTOM)


def draw(draw_obj):
    for y in range(0, H, 4):
        t = y / H
        r = int(C_BG_GRAD_TOP[0] * (1 - t) + C_BG_GRAD_BOTTOM[0] * t)
        g = int(C_BG_GRAD_TOP[1] * (1 - t) + C_BG_GRAD_BOTTOM[1] * t)
        b = int(C_BG_GRAD_TOP[2] * (1 - t) + C_BG_GRAD_BOTTOM[2] * t)
        draw_obj.rectangle([0, y, W, y + 4], fill=(r, g, b))
''',

    "C_content/C38_thumb_borders.py": '''"""C38_thumb_borders.py — Sirf borders."""
from C_content.C36_thumb_constants import W, H, C_GOLD, C_GOLD_BRIGHT


def draw(draw_obj):
    draw_obj.rectangle([20, 20, W - 20, H - 20], outline=C_GOLD, width=6)
    draw_obj.rectangle([30, 30, W - 30, H - 30], outline=C_GOLD_BRIGHT, width=2)
''',

    "C_content/C39_thumb_label.py": '''"""C39_thumb_label.py — Sirf label."""
from B_graphics.B2_font_load import load
from C_content.C36_thumb_constants import W, C_TEXT_GOLD


def draw(draw_obj, label):
    if not label:
        return
    font = load(36, "latin", True)
    bbox = draw_obj.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw_obj.text((x + 2, 102), label, font=font, fill=(0, 0, 0))
    draw_obj.text((x, 100), label, font=font, fill=C_TEXT_GOLD)
''',

    "C_content/C40_thumb_title.py": '''"""C40_thumb_title.py — Sirf title."""
from B_graphics.B2_font_load import load
from C_content.C36_thumb_constants import W, C_TEXT_BRIGHT, C_TEXT_GOLD


def draw(draw_obj):
    fb = load(84, "latin", True)
    for text, y, color in [("HADITH", 280, C_TEXT_BRIGHT),
                            ("OF THE DAY", 420, C_TEXT_GOLD)]:
        font = fb if text == "HADITH" else load(56, "latin", True)
        bbox = draw_obj.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw_obj.text((x + 4, y + 4), text, font=font, fill=(0, 0, 0, 220))
        draw_obj.text((x, y), text, font=font, fill=color)
''',

    "C_content/C41_thumb_lang.py": '''"""C41_thumb_lang.py — Sirf lang lines."""
from B_graphics.B2_font_load import load
from C_content.C36_thumb_constants import W, C_WHITE, C_HINDI, C_URDU, C_ENGLISH


def draw(draw_obj, hindi, urdu, english):
    y = 780
    gap = 130
    if hindi:
        font = load(48, "devanagari", True)
        draw_obj.ellipse([100, y+20, 130, y+50], fill=C_HINDI, outline=C_WHITE, width=1)
        draw_obj.text((160, y), hindi[:30], font=font, fill=C_WHITE)
        y += gap
    if urdu:
        font = load(48, "arabic", True)
        draw_obj.ellipse([100, y+20, 130, y+50], fill=C_URDU, outline=C_WHITE, width=1)
        draw_obj.text((160, y), urdu[:30], font=font, fill=C_WHITE)
        y += gap
    if english:
        font = load(44, "latin", True)
        draw_obj.ellipse([100, y+20, 130, y+50], fill=C_ENGLISH, outline=C_WHITE, width=1)
        draw_obj.text((160, y), english[:60], font=font, fill=C_WHITE)
''',

    "C_content/C42_thumb_cta.py": '''"""C42_thumb_cta.py — Sirf CTA."""
from B_graphics.B2_font_load import load
from C_content.C36_thumb_constants import W


def draw(draw_obj):
    font = load(40, "latin", True)
    cta = "Follow @sawajstudio"
    bbox = draw_obj.textbbox((0, 0), cta, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw_obj.text((x + 2, 1782), cta, font=font, fill=(0, 0, 0))
    draw_obj.text((x, 1780), cta, font=font, fill=(255, 230, 180))
''',

    "C_content/C43_thumb_logo.py": '''"""C43_thumb_logo.py — Sirf logo."""
import os
from PIL import Image
from C_content.C36_thumb_constants import W


def draw(img):
    if not os.path.exists("avatar.png"):
        return
    try:
        logo = Image.open("avatar.png").convert("RGBA").resize(
            (260, 110), Image.Resampling.LANCZOS)
        img.paste(logo, ((W - 260) // 2, 1580), logo)
    except Exception:
        pass
''',

    "C_content/C44_thumb_truncate.py": '''"""C44_thumb_truncate.py — Sirf truncate."""


def truncate(draw_obj, text, font, max_width):
    if not text:
        return ""
    bbox = draw_obj.textbbox((0, 0), text, font=font)
    if bbox[2] - bbox[0] <= max_width:
        return text
    for length in range(len(text), 0, -1):
        s = text[:length] + "..."
        bbox = draw_obj.textbbox((0, 0), s, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return s
    return text[:20] + "..."
''',

    "C_content/C45_thumb_wrap.py": '''"""C45_thumb_wrap.py — Sirf wrap."""


def wrap(draw_obj, text, font, max_width):
    if not text:
        return []
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip() if current else w
        bbox = draw_obj.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines
''',

    "C_content/C46_thumb_main.py": '''"""C46_thumb_main.py — Sirf thumbnail main."""
import os
from PIL import Image, ImageDraw
from A_core.A9_log_step import log_step
from C_content.C37_thumb_gradient import draw as grad
from C_content.C38_thumb_borders import draw as borders
from C_content.C39_thumb_label import draw as label
from C_content.C40_thumb_title import draw as title
from C_content.C41_thumb_lang import draw as lang
from C_content.C42_thumb_cta import draw as cta
from C_content.C43_thumb_logo import draw as logo
from C_content.C36_thumb_constants import W, H, C_BG_DARK


def make(hindi, urdu, english, hadith_label,
         outfile="output/final/thumbnail.jpg"):
    log_step("C46_thumb_main.py", "make()", "ok")
    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)
    img = Image.new("RGB", (W, H), C_BG_DARK)
    draw_obj = ImageDraw.Draw(img)
    grad(draw_obj)
    borders(draw_obj)
    label(draw_obj, hadith_label)
    title(draw_obj)
    lang(draw_obj, hindi, urdu, english)
    logo(img)
    cta(draw_obj)
    img.save(outfile, "JPEG", quality=92, optimize=True)
    log_step("C46_thumb_main.py", f"Saved {outfile}", "ok")
    return outfile
''',

    # ═══════════════════════════════════════════════════
    # D_video (29 files)
    # ═══════════════════════════════════════════════════
    "D_video/D1_intro_goldline.py": '''"""D1_intro_goldline.py — Sirf gold line."""
import math


def draw_gold_line(draw, p, t):
    line_y = 320
    progress = max(0.0, min(1.0, (p - 0.2) / 0.4))
    if progress <= 0:
        return
    lw = int(600 * progress)
    lx = (1080 - lw) // 2
    shimmer = 0.85 + 0.15 * math.sin(t * 8)
    a = int(255 * progress * shimmer)
    draw.rectangle([lx, line_y, lx + lw, line_y + 3], fill=(230, 200, 130, a))
    if progress > 0.7:
        da = int(255 * (progress - 0.7) / 0.3)
        draw.ellipse([lx-4, line_y-3, lx+4, line_y+6], fill=(255, 240, 180, da))
        draw.ellipse([lx+lw-4, line_y-3, lx+lw+4, line_y+6], fill=(255, 240, 180, da))
''',

    "D_video/D2_intro_logo.py": '''"""D2_intro_logo.py — Sirf logo draw."""
import os
from PIL import Image


def draw_logo(img, p):
    if not os.path.exists("avatar.png"):
        return
    logo_p = max(0.0, min(1.0, (p - 0.3) / 0.4))
    if logo_p <= 0:
        return
    try:
        base = Image.open("avatar.png").convert("RGBA")
        scale = 0.6 + 0.4 * (1 - (1 - logo_p) ** 2)
        sw = int(240 * scale)
        sh = int(base.height * (sw / base.width))
        logo = base.resize((sw, sh), Image.Resampling.LANCZOS)
        mask = logo.split()[3].point(lambda v: int(v * logo_p))
        logo.putalpha(mask)
        lx = (1080 - sw) // 2
        ly = 720 - sh // 2 + 50
        img.paste(logo, (lx, ly), logo)
    except Exception:
        pass
''',

    "D_video/D3_intro_main.py": '''"""D3_intro_main.py — Sirf intro main."""
from B_graphics.B2_font_load import load
from B_graphics.B7_text_draw_center import draw_centered
from B_graphics.B10_sparkle_draw import draw_sparkles
from D_video.D1_intro_goldline import draw_gold_line
from D_video.D2_intro_logo import draw_logo

C_GOLD = (230, 200, 130)


def draw_intro(img, draw, t, intro_dur, has_logo):
    p = t / intro_dur if intro_dur > 0 else 0
    p = max(0.0, min(1.0, p))
    font_arabic = load(56, "arabic", True)
    font_title = load(76, "latin", True)
    font_sub = load(40, "latin", False)
    alpha = min(1.0, t / 0.5)

    draw_centered(draw, "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ",
                  200, font_arabic, (*C_GOLD, int(255 * alpha)))
    draw_gold_line(draw, p, t)
    if has_logo and p > 0.3:
        draw_logo(img, p)
    title_p = max(0.0, min(1.0, (p - 0.5) / 0.4))
    if title_p > 0:
        draw_centered(draw, "HADITH OF THE DAY", 980, font_title,
                      (*C_GOLD, int(255 * title_p)))
        if title_p > 0.5:
            sa = (title_p - 0.5) / 0.5
            draw_centered(draw, "SAWAJ STUDIO Presents", 1080, font_sub,
                          (180, 160, 130, int(200 * sa)))
    draw_sparkles(draw, t)
''',

    "D_video/D4_main_alpha.py": '''"""D4_main_alpha.py — Sirf alpha."""


def get_alpha(mt):
    return min(1.0, mt / 0.5) if mt > 0 else 0.0
''',

    "D_video/D5_main_badge.py": '''"""D5_main_badge.py — Sirf badge."""
from B_graphics.B18_badge_main import draw_badge

BADGE_Y = 180


def draw(draw, hadith_label):
    if hadith_label:
        draw_badge(draw, hadith_label, y=BADGE_Y)
''',

    "D_video/D6_main_watermark.py": '''"""D6_main_watermark.py — Sirf watermark."""
from B_graphics.B31_watermark_main import draw_watermark
from B_graphics.B34_logo_float import draw_floating_logo


def draw(img, mt, has_logo):
    if has_logo:
        draw_watermark(img, "avatar.png", size=(160, 68),
                       pos="top-right", opacity=0.55)
        draw_floating_logo(img, mt, "avatar.png", size=(240, 100))
''',

    "D_video/D7_main_bullets.py": '''"""D7_main_bullets.py — Sirf bullets."""
from B_graphics.B29_bullets_main import draw_bullets

BULLETS_Y = 780


def draw(draw, hindi, urdu, english, mt, voice_dur, alpha):
    draw_bullets(draw, hindi, urdu, english, mt, voice_dur,
                 y_start=BULLETS_Y, alpha=alpha)
''',

    "D_video/D8_main_progress.py": '''"""D8_main_progress.py — Sirf progress."""
from B_graphics.B13_progress_main import draw_progress


def draw(draw, mt, voice_dur):
    draw_progress(draw, mt, voice_dur)
''',

    "D_video/D9_main_sparkles.py": '''"""D9_main_sparkles.py — Sirf sparkles."""
from B_graphics.B10_sparkle_draw import draw_sparkles


def draw(draw, mt):
    draw_sparkles(draw, mt)
''',

    "D_video/D10_main_bg_layers.py": '''"""D10_main_bg_layers.py — Sirf bg layers."""
from B_graphics.B35_arabesque_main import draw_arabesque
from B_graphics.B36_rays_draw import draw_god_rays
from B_graphics.B39_ember_draw import draw_embers

ENABLE_GOD_RAYS = True
ENABLE_ARABESQUE = True
ENABLE_EMBERS = True


def draw(draw, mt, alpha):
    if ENABLE_GOD_RAYS:
        draw_god_rays(draw, mt, opacity=int(25 * alpha))
    if ENABLE_ARABESQUE:
        draw_arabesque(draw, mt, opacity=int(30 * alpha))
    if ENABLE_EMBERS:
        draw_embers(draw, mt, count=12)
''',

    "D_video/D11_main_draw.py": '''"""D11_main_draw.py — Sirf main draw."""
from D_video.D4_main_alpha import get_alpha
from D_video.D5_main_badge import draw as badge
from D_video.D6_main_watermark import draw as wm
from D_video.D7_main_bullets import draw as bullets
from D_video.D8_main_progress import draw as progress
from D_video.D9_main_sparkles import draw as sparkles
from D_video.D10_main_bg_layers import draw as bg_layers


def draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
              hadith_label, has_logo):
    alpha = get_alpha(mt)
    bg_layers(draw, mt, alpha)
    badge(draw, hadith_label)
    wm(img, mt, has_logo)
    bullets(draw, hindi, urdu, english, mt, voice_dur, alpha)
    progress(draw, mt, voice_dur)
    sparkles(draw, mt)
''',

    "D_video/D12_outro_cta.py": '''"""D12_outro_cta.py — Sirf CTA."""


def draw_cta(draw, alpha, font):
    a = int(255 * alpha)
    if a < 5:
        return
    buttons = [("LIKE", 140), ("SUBSCRIBE", 420), ("SHARE", 780)]
    cy = 960
    btn_h = 60
    pad_x = 24
    for label, x_start in buttons:
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        btn_w = tw + pad_x * 2
        x1 = x_start
        y1 = cy - btn_h // 2
        x2 = x_start + btn_w
        y2 = cy + btn_h // 2
        draw.rounded_rectangle([x1, y1, x2, y2], radius=btn_h // 2,
                               fill=(255, 240, 200, int(a * 0.25)),
                               outline=(255, 220, 130, a), width=2)
        tx = x1 + pad_x
        ty = cy - th // 2 - bbox[1]
        draw.text((tx, ty), label, font=font, fill=(255, 240, 200, a))
''',

    "D_video/D13_outro_logo.py": '''"""D13_outro_logo.py — Sirf outro logo."""
import os
from PIL import Image


def draw_logo(img, t, amin=0.8, amax=1.2):
    if not os.path.exists("avatar.png"):
        return
    try:
        logo = Image.open("avatar.png").convert("RGBA").resize(
            (260, 110), Image.Resampling.LANCZOS)
        if t < amax:
            progress = max(0.0, min(1.0, (t - amin) / (amax - amin)))
            mask = logo.split()[3].point(lambda v: int(v * progress))
            logo.putalpha(mask)
        lx = (1080 - 260) // 2
        ly = 1260
        img.paste(logo, (lx, ly), logo)
    except Exception:
        pass
''',

    "D_video/D14_outro_main.py": '''"""D14_outro_main.py — Sirf outro main."""
from B_graphics.B2_font_load import load
from B_graphics.B7_text_draw_center import draw_centered
from B_graphics.B10_sparkle_draw import draw_sparkles
from D_video.D12_outro_cta import draw_cta
from D_video.D13_outro_logo import draw_logo

C_GOLD = (230, 200, 130)


def draw_outro(img, draw, t, outro_dur, has_logo):
    font_outro = load(72, "latin", True)
    font_cta = load(36, "latin", True)
    font_follow = load(44, "latin", True)
    alpha_j = min(1.0, t / 0.5)

    draw_centered(draw, "JazakAllah Khair", 780, font_outro,
                  (*C_GOLD, int(255 * alpha_j)))
    if t > 0.4:
        ac = min(1.0, (t - 0.4) / 0.5)
        draw_cta(draw, ac, font_cta)
    if t > 0.6:
        af = min(1.0, (t - 0.6) / 0.4)
        draw_centered(draw, "Follow @sawajstudio", 1120, font_follow,
                      (220, 190, 130, int(255 * af)))
    if has_logo and t > 0.8:
        draw_logo(img, t)
    draw_sparkles(draw, t)
''',

    "D_video/D15_frames_generate.py": '''"""D15_frames_generate.py — Sirf frames."""
import os
import gc
import time
from PIL import Image, ImageDraw
from A_core.A9_log_step import log_step
from D_video.D3_intro_main import draw_intro
from D_video.D11_main_draw import draw_main
from D_video.D14_outro_main import draw_outro


def generate(voice_dur, has_logo, hindi, urdu, english,
             hadith_label="", out_dir="s_frames",
             intro_dur=2.0, outro_dur=2.0):
    fps = 25
    os.makedirs(out_dir, exist_ok=True)
    total = intro_dur + voice_dur + outro_dur
    count = int(total * fps)
    log_step("D15_frames_generate.py", f"Total {total:.1f}s ({count} frames)", "ok")
    canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    start = time.time()
    try:
        for fi in range(count):
            t = fi / fps
            canvas.paste((0, 0, 0, 0), (0, 0, 1080, 1920))
            draw = ImageDraw.Draw(canvas)
            if t < intro_dur:
                draw_intro(canvas, draw, t, intro_dur, has_logo)
            elif t < intro_dur + voice_dur:
                mt = t - intro_dur
                draw_main(canvas, draw, mt, voice_dur, hindi, urdu,
                          english, hadith_label, has_logo)
            else:
                ot = t - (intro_dur + voice_dur)
                draw_outro(canvas, draw, ot, outro_dur, has_logo)
            canvas.convert("RGB").save(
                os.path.join(out_dir, f"frame_{fi:05d}.png"), "PNG")
            if fi > 0 and fi % 100 == 0:
                el = time.time() - start
                rate = fi / el if el > 0 else 0
                log_step("D15_frames_generate.py",
                         f"{fi}/{count}", "info", f"{rate:.1f} fps")
            if fi % 500 == 0:
                gc.collect()
    finally:
        try:
            canvas.close()
        except Exception:
            pass
        gc.collect()
    return total
''',

    "D_video/D16_frames_cleanup.py": '''"""D16_frames_cleanup.py — Sirf cleanup."""
import os
import shutil


def cleanup(folder="s_frames"):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
''',

    "D_video/D17_ease_crossfade.py": '''"""D17_ease_crossfade.py — Sirf crossfade."""


def crossfade_alpha(current_t, start, duration):
    if duration <= 0:
        return 1.0 if current_t >= start else 0.0
    if current_t < start:
        return 0.0
    if current_t > start + duration:
        return 1.0
    return (current_t - start) / duration
''',

    "D_video/D18_ease_inout.py": '''"""D18_ease_inout.py — Sirf ease_in_out."""


def ease_in_out(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)
''',

    "D_video/D19_ease_fadeio.py": '''"""D19_ease_fadeio.py — Sirf fade_in_out."""


def fade_in_out(t, start, fade_in, fade_out, end):
    if t < start or t > end:
        return 0.0
    if t < start + fade_in:
        return (t - start) / fade_in if fade_in > 0 else 1.0
    if t > end - fade_out:
        return (end - t) / fade_out if fade_out > 0 else 1.0
    return 1.0
''',

    "D_video/D20_ease_linear.py": '''"""D20_ease_linear.py — Sirf linear."""


def ease_linear(x):
    return max(0.0, min(1.0, x))
''',

    "D_video/D21_ease_in.py": '''"""D21_ease_in.py — Sirf ease_in."""


def ease_in(x):
    x = max(0.0, min(1.0, x))
    return x * x
''',

    "D_video/D22_ease_out.py": '''"""D22_ease_out.py — Sirf ease_out."""


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) * (1 - x)
''',

    "D_video/D23_ease_bounce.py": '''"""D23_ease_bounce.py — Sirf bounce."""


def ease_bounce(x):
    x = max(0.0, min(1.0, x))
    if x < 0.8:
        return x * 1.35
    return 1.08 - (x - 0.8) * 0.4
''',

    "D_video/D24_ease_cubic.py": '''"""D24_ease_cubic.py — Sirf cubic."""


def ease_cubic(x):
    x = max(0.0, min(1.0, x))
    if x < 0.5:
        return 4 * x * x * x
    return 1 - pow(-2 * x + 2, 3) / 2
''',

    "D_video/D25_ease_smoothstep.py": '''"""D25_ease_smoothstep.py — Sirf smoothstep."""


def smoothstep(edge0, edge1, x):
    if edge0 == edge1:
        return 0.0 if x < edge0 else 1.0
    t = (x - edge0) / (edge1 - edge0)
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)
''',

    "D_video/D26_ease_scene.py": '''"""D26_ease_scene.py — Sirf scene."""


def scene_progress(current_t, scene_start, scene_duration):
    if scene_duration <= 0:
        return 1.0
    p = (current_t - scene_start) / scene_duration
    return max(0.0, min(1.0, p))
''',

    "D_video/D27_ease_pulse.py": '''"""D27_ease_pulse.py — Sirf pulse."""
import math


def pulse(t, speed=1.0, min_val=0.0, max_val=1.0):
    mid = (min_val + max_val) / 2
    amp = (max_val - min_val) / 2
    return mid + amp * math.sin(t * speed)
''',

    "D_video/D28_compose_main.py": '''"""D28_compose_main.py — Sirf compose."""
import os
import subprocess
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error


def compose(base, bg, frames_dir, voice, total,
            outfile="output/final/Final_Story.mp4"):
    log_step("D28_compose_main.py", f"compose({total:.1f}s)", "ok")
    if not os.path.exists(bg):
        raise FileNotFoundError(f"BG not found: {bg}")
    if not os.path.exists(voice):
        raise FileNotFoundError(f"Voice not found: {voice}")
    if not os.path.isdir(frames_dir):
        raise FileNotFoundError(f"Frames not found: {frames_dir}")
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    cmd = (f'ffmpeg -y -i "{bg}" -framerate 25 -i "{frames_dir}/frame_%05d.png" '
           f'-i "{voice}" -filter_complex '
           f'"[0:v][1:v]overlay=0:0:shortest=1,'
           f'eq=contrast=1.08:brightness=0.02:saturation=1.12,'
           f'vignette=PI/6,format=yuv420p[outv]" '
           f'-map "[outv]" -map 2:a '
           f'-c:v libx264 -preset veryfast -crf 20 -b:v 4M '
           f'-c:a aac -b:a 192k -t {total:.2f} '
           f'-movflags +faststart "{outfile}"')
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True,
                       text=True, timeout=1800)
    except subprocess.CalledProcessError as e:
        log_error("D28_compose_main.py", f"FFmpeg: {e.stderr[:200]}")
        raise
    size_mb = os.path.getsize(outfile) / 1024 / 1024
    log_step("D28_compose_main.py", "Video ready", "ok", f"{size_mb:.1f} MB")
    return outfile
''',

    "D_video/D29_compose_verify.py": '''"""D29_compose_verify.py — Sirf verify."""
import json
import subprocess


def verify(video_path):
    try:
        result = subprocess.run(
            f'ffprobe -v error -show_entries format=duration,size -of json "{video_path}"',
            shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"error": "ffprobe failed"}
        data = json.loads(result.stdout)
        fmt = data.get("format", {})
        return {"duration": float(fmt.get("duration", 0)),
                "size": int(fmt.get("size", 0)),
                "size_mb": int(fmt.get("size", 0)) / 1024 / 1024}
    except Exception as e:
        return {"error": str(e)[:100]}
''',

    # ═══════════════════════════════════════════════════
    # E_audio (4 files)
    # ═══════════════════════════════════════════════════
    "E_audio/E1_duck_mix.py": '''"""E1_duck_mix.py — Sirf mix."""
from A_core.A9_log_step import log_step


def mix(base, voice_file, music_file, out_file, voice_dur, music_vol=0.20):
    log_step("E1_duck_mix.py", "mix()", "ok")
    fade = max(voice_dur - 3.0, 1.0)
    base.run_cmd(
        f'ffmpeg -y -i {voice_file} -i {music_file} '
        f'-filter_complex '
        f'"[1:a]volume={music_vol},afade=t=in:st=0:d=2,'
        f'afade=t=out:st={fade:.2f}:d=3[bg];'
        f'[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]" '
        f'-map "[aout]" -c:a libmp3lame -b:a 192k {out_file}')
    return out_file
''',

    "E_audio/E2_sfx_whoosh.py": '''"""E2_sfx_whoosh.py — Sirf whoosh."""


def whoosh_cmd(outfile="whoosh.mp3"):
    return (f'ffmpeg -y -f lavfi -i "anoisesrc=d=0.5:c=pink:a=0.5" '
            f'-af "afade=t=in:d=0.1,afade=t=out:st=0.3:d=0.2,volume=0.3" '
            f'{outfile}')
''',

    "E_audio/E3_sfx_ding.py": '''"""E3_sfx_ding.py — Sirf ding."""


def ding_cmd(outfile="ding.mp3"):
    return (f'ffmpeg -y -f lavfi -i "sine=frequency=880:duration=0.5" '
            f'-af "afade=t=out:st=0.2:d=0.3,volume=0.4" {outfile}')
''',

    "E_audio/E4_master_voice.py": '''"""E4_master_voice.py — Sirf mastering."""
from A_core.A9_log_step import log_step


def master(base, in_file, out_file):
    log_step("E4_master_voice.py", "master()", "ok")
    base.run_cmd(
        f'ffmpeg -y -i {in_file} -af '
        f'"atempo=0.88,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.35" '
        f'{out_file}')
    return out_file
''',

    # ═══════════════════════════════════════════════════
    # F_drive (4 files)
    # ═══════════════════════════════════════════════════
    "F_drive/F1_drive_auth.py": '''"""F1_drive_auth.py — Sirf auth."""
import os


def get_creds():
    return {
        "client_id": os.environ.get("GOOGLE_DRIVE_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET"),
        "refresh_token": os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN"),
    }
''',

    "F_drive/F2_drive_upload.py": '''"""F2_drive_upload.py — Sirf upload."""
import os
import time
from A_core.A10_log_api import log_api


def upload(base, path, prefix="Story"):
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = Credentials(
            None,
            refresh_token=os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN"),
            client_id=os.environ.get("GOOGLE_DRIVE_CLIENT_ID"),
            client_secret=os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET"),
            token_uri="https://oauth2.googleapis.com/token")
        service = build("drive", "v3", credentials=creds, cache_discovery=False)
        meta = {"name": f"{prefix}_{int(time.time())}.mp4"}
        folder_id = os.environ.get("GDRIVE_STORY_VIDEO_FOLDER_ID")
        if folder_id:
            meta["parents"] = [folder_id]
        up = service.files().create(
            body=meta,
            media_body=MediaFileUpload(path, mimetype="video/mp4", resumable=True),
            fields="id").execute()
        did = up.get("id")
        log_api("F2_drive_upload.py", "Drive", "success", did)
        return did
    except Exception as e:
        log_api("F2_drive_upload.py", "Drive", "failed", str(e)[:100])
        return None
''',

    "F_drive/F3_drive_public.py": '''"""F3_drive_public.py — Sirf public."""
def make_public(service, file_id):
    try:
        service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"}).execute()
        return True
    except Exception:
        return False
''',

    "F_drive/F4_drive_links.py": '''"""F4_drive_links.py — Sirf links."""


def build_links(did):
    return (f"https://drive.google.com/file/d/{did}/view",
            f"https://drive.google.com/uc?export=download&id={did}")
''',

    # ═══════════════════════════════════════════════════
    # G_entry (16 files)
    # ═══════════════════════════════════════════════════
    "G_entry/G1_step_init.py": '''"""G1_step_init.py — Sirf init."""
from A_core.A9_log_step import log_step


def run(base):
    log_step("G1_step_init.py", "Init", "ok")
    return True
''',

    "G_entry/G2_step_secrets.py": '''"""G2_step_secrets.py — Sirf secrets."""
from A_core.A9_log_step import log_step
from A_core.A45_secrets_verify import verify


def run(base):
    report = verify()
    s = report["summary"]
    log_step("G2_step_secrets.py", "Verified", "ok",
             f"{s['working_secrets']}/{s['total_secrets']}")
    return report
''',

    "G_entry/G3_step_hadith.py": '''"""G3_step_hadith.py — Sirf hadith."""
from A_core.A9_log_step import log_step
from C_content.C5_hadith_main import fetch


def run(base):
    h = fetch(base.session)
    log_step("G3_step_hadith.py", "Fetched", "ok",
             f"{h['collection']} #{h['number']}")
    return h
''',

    "G_entry/G4_step_translate.py": '''"""G4_step_translate.py — Sirf translate."""
from A_core.A9_log_step import log_step
from C_content.C15_translate_main import to_hindi


def run(base, english):
    hindi = to_hindi(base.session, english)
    log_step("G4_step_translate.py", "Done", "ok")
    return hindi
''',

    "G_entry/G5_step_tts.py": '''"""G5_step_tts.py — Sirf tts."""
from A_core.A9_log_step import log_step
from C_content.C20_tts_main import generate
from E_audio.E4_master_voice import master


def run(base, hindi):
    generate(base.session, f"हदीस शरीफ। {hindi}", "s_raw.mp3")
    master(base, "s_raw.mp3", "s_v.mp3")
    from mutagen.mp3 import MP3
    d = MP3("s_v.mp3").info.length
    log_step("G5_step_tts.py", "Voice ready", "ok", f"{d:.1f}s")
    return d
''',

    "G_entry/G6_step_music.py": '''"""G6_step_music.py — Sirf music."""
from C_content.C27_music_main import get
from E_audio.E1_duck_mix import mix


def run(base, voice_dur):
    get(base, "music_soft.mp3")
    mix(base, "s_v.mp3", "music_soft.mp3", "s_voice.mp3", voice_dur)
    return "s_voice.mp3"
''',

    "G_entry/G7_step_background.py": '''"""G7_step_background.py — Sirf background."""
from C_content.C34_bg_main import get


def run(base, voice_dur):
    return get(base, voice_dur + 4.5)
''',

    "G_entry/G8_step_logo.py": '''"""G8_step_logo.py — Sirf logo."""
from C_content.C35_logo_make import make


def run():
    return make("avatar.png")
''',

    "G_entry/G9_step_frames.py": '''"""G9_step_frames.py — Sirf frames."""
from D_video.D15_frames_generate import generate


def run(voice_dur, has_logo, hindi, urdu, english, hadith_label):
    return generate(voice_dur, has_logo, hindi, urdu, english,
                    hadith_label, "s_frames")
''',

    "G_entry/G10_step_compose.py": '''"""G10_step_compose.py — Sirf compose."""
from D_video.D28_compose_main import compose


def run(base, bg_file, total):
    return compose(base, bg_file, "s_frames", "s_voice.mp3", total,
                   "output/final/Final_Story.mp4")
''',

    "G_entry/G11_step_thumbnail.py": '''"""G11_step_thumbnail.py — Sirf thumb."""
from C_content.C46_thumb_main import make


def run(hindi, arabic, english, label):
    return make(hindi, arabic, english, label, "output/final/thumbnail.jpg")
''',

    "G_entry/G12_step_drive.py": '''"""G12_step_drive.py — Sirf drive."""
from F_drive.F2_drive_upload import upload


def run(base, video_path):
    return upload(base, video_path, "Story")
''',

    "G_entry/G13_step_socials.py": '''"""G13_step_socials.py — Sirf socials."""
import os
import sys


def run(video_path, hindi, hadith):
    results = {}
    cfg_target = os.environ.get("UPLOAD_TARGET", "drive_only").lower()
    sys.path.insert(0, os.path.abspath("../../../.."))

    if cfg_target in ("fb_ig", "all") and os.environ.get("FACEBOOK_META_TOKEN"):
        try:
            from sawajstudiobot.video_uploader.facebook.fb_story_main import upload as fb_up
            results["facebook"] = fb_up(video_path)
        except Exception as e:
            results["facebook"] = str(e)[:60]

    if cfg_target in ("fb_ig", "all") and os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN"):
        try:
            from sawajstudiobot.video_uploader.instagram.ig_story_main import upload as ig_up
            results["instagram"] = ig_up(video_path)
        except Exception as e:
            results["instagram"] = str(e)[:60]
    return results
''',

    "G_entry/G14_step_cleanup.py": '''"""G14_step_cleanup.py — Sirf cleanup."""
from A_core.A31_cleanup import cleanup


def run():
    cleanup(
        ["s_raw.mp3", "s_v.mp3", "s_voice.mp3", "tmp.mp4",
         "tmp_bg.mp4", "music_raw.mp3", "music_soft.mp3"],
        folder="s_frames")
''',

    "G_entry/G15_pipeline_run.py": '''"""G15_pipeline_run.py — Sirf pipeline."""
import traceback
from A_core.A5_platform_checker import available_platforms
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error
from G_entry.G1_step_init import run as s_init
from G_entry.G2_step_secrets import run as s_sec
from G_entry.G3_step_hadith import run as s_had
from G_entry.G4_step_translate import run as s_tr
from G_entry.G5_step_tts import run as s_tts
from G_entry.G6_step_music import run as s_mus
from G_entry.G7_step_background import run as s_bg
from G_entry.G8_step_logo import run as s_logo
from G_entry.G9_step_frames import run as s_frames
from G_entry.G10_step_compose import run as s_comp
from G_entry.G11_step_thumbnail import run as s_thumb
from G_entry.G12_step_drive import run as s_drive
from G_entry.G13_step_socials import run as s_soc
from G_entry.G14_step_cleanup import run as s_clean


def run_pipeline(base):
    try:
        s_init(base)
        s_sec(base)
        h = s_had(base)
        hindi = s_tr(base, h["english"])
        voice_dur = s_tts(base, hindi)
        s_mus(base, voice_dur)
        bg_file = s_bg(base, voice_dur)
        has_logo = s_logo()
        label = f"#{h['number']} · {h['collection']}"
        total = s_frames(voice_dur, has_logo, hindi, h.get("arabic", ""),
                         h["english"], label)
        final = s_comp(base, bg_file, total)
        s_thumb(hindi, h.get("arabic", ""), h["english"], label)
        s_drive(base, final)
        s_soc(final, hindi, h)
        s_clean()
        log_step("G15_pipeline_run.py", "Pipeline complete", "ok")
        return True
    except Exception as e:
        log_error("G15_pipeline_run.py", str(e), traceback.format_exc())
        raise
''',

    "G_entry/G16_main.py": '''"""G16_main.py — Sirf main entry."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from A_core.A5_platform_checker import available_platforms
from A_core.A16_tg_run_start import run_start
from A_core.A24_tg_report import send_full_report
from A_core.A25_tg_summary import send_summary
from A_core.A28_http_session import create_session
from A_core.A32_api_tracker import create_tracker
from G_entry.G15_pipeline_run import run_pipeline


class BasePipeline:
    def __init__(self):
        self.session = create_session()
        self.api_status = create_tracker()


def main():
    run_start("📖 STORY VIDEO RUN")
    base = BasePipeline()
    try:
        run_pipeline(base)
        send_full_report()
        send_summary()
        sys.exit(0)
    except Exception:
        send_full_report()
        send_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()
''',

    # ═══════════════════════════════════════════════════
    # H_tests (5 files)
    # ═══════════════════════════════════════════════════
    "H_tests/H1_conftest.py": '''"""H1_conftest.py — Sirf path setup."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)
''',

    "H_tests/H2_test_config.py": '''"""H2_test_config.py — Sirf config test."""
from A_core.A3_config_class import Config


def test_config_import():
    assert Config is not None
''',

    "H_tests/H3_test_utils.py": '''"""H3_test_utils.py — Sirf utils test."""
from A_core.A26_sanitize import sanitize


def test_sanitize_basic():
    assert sanitize("  hello\\nworld  ") == "hello world"


def test_sanitize_empty():
    assert sanitize("") == ""
    assert sanitize(None) == ""
''',

    "H_tests/H4_test_media.py": '''"""H4_test_media.py — Sirf media test."""
from C_content.C5_hadith_main import fetch
from C_content.C20_tts_main import generate


def test_hadith_import():
    assert fetch is not None


def test_tts_import():
    assert generate is not None
''',

    "H_tests/H5_test_render.py": '''"""H5_test_render.py — Sirf render test."""
from D_video.D15_frames_generate import generate
from B_graphics.B2_font_load import load


def test_frames_import():
    assert generate is not None


def test_font_import():
    assert load is not None
''',

    # ═══════════════════════════════════════════════════
    # __init__ files
    # ═══════════════════════════════════════════════════
    "A_core/__init__.py": '"""A_core package."""\n',
    "B_graphics/__init__.py": '"""B_graphics package."""\n',
    "C_content/__init__.py": '"""C_content package."""\n',
    "D_video/__init__.py": '"""D_video package."""\n',
    "E_audio/__init__.py": '"""E_audio package."""\n',
    "F_drive/__init__.py": '"""F_drive package."""\n',
    "G_entry/__init__.py": '"""G_entry package."""\n',
    "H_tests/__init__.py": '"""H_tests package."""\n',
    "__init__.py": '"""Story generator package."""\n',
}


def main():
    total = 0
    for rel_path, content in FILES.items():
        full = os.path.join(BASE, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        total += 1
        print(f"  ✅ {rel_path}")
    print(f"\\n🎉 Story generator: {total} files written!")


if __name__ == "__main__":
    main()
