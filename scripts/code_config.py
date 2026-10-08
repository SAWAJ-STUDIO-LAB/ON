"""
Sawaj Studio Module
"""
"""
📁 1_config — Saare config modules ka code
"""
import os

ROOT = "Sawaj_studio"
CODE = {}

# ═══════════════════════════════════════════════════════════
# 1_env_loader.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 2_secret_reader.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 3_path_builder.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 4_mode_decider.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 5_folder_creator.py
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/1_config/5_folder_creator.py"] = '''"""
📁 Folder Creator
"""
import os


def create_all_folders():
    folders = [
        "output/story", "output/short", "output/long",
        "output/temp", "output/logs",
    ]
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

# ═══════════════════════════════════════════════════════════
# 6_default_settings.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 7_platform_config.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 8_worker_selector.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 9_validation.py
# ═══════════════════════════════════════════════════════════
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
# __init__.py
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/1_config/__init__.py"] = '''"""Config Module"""
'''


# ═══════════════════════════════════════════════════════════
# WRITE ALL
# ═══════════════════════════════════════════════════════════
def write_all():
    written = 0
    for path, code in CODE.items():
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        written += 1
        print(f"   📄 {path}")
    return written
