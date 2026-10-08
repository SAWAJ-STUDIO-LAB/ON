"""
Sawaj Studio Module
"""
"""
📝 2_logger — Saare logger modules ka code
"""
import os

ROOT = "Sawaj_studio"
CODE = {}

# ═══════════════════════════════════════════════════════════
# 1_console_logger.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 2_file_logger.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 3_timestamp.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 4_log_levels.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 5_error_tracker.py
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/2_logger/5_error_tracker.py"] = '''"""
🚨 Error Tracker
"""
import traceback
from datetime import datetime

ERRORS = []


def track_error(module, error, include_traceback=False):
    entry = {
        "module": module,
        "error": str(error)[:500],
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

# ═══════════════════════════════════════════════════════════
# 6_step_logger.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 7_api_logger.py
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/2_logger/7_api_logger.py"] = '''"""
🌐 API Logger
"""
from datetime import datetime

API_LOGS = []


def log_api(name, status, detail="", code=None):
    API_LOGS.append({
        "name": name,
        "status": status.lower(),
        "detail": detail[:200],
        "code": code,
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

# ═══════════════════════════════════════════════════════════
# 8_buffer.py
# ═══════════════════════════════════════════════════════════
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
# __init__.py
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/2_logger/__init__.py"] = '''"""Logger Module"""
'''


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
