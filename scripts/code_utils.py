"""
Sawaj Studio Module
"""
"""
🧰 4_utils — Saare utils modules ka code
"""
import os

ROOT = "Sawaj_studio"
CODE = {}

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


def remove_emoji(text):
    if not text:
        return ""
    emoji_pattern = re.compile(
        "["
        "\\U0001F600-\\U0001F64F"
        "\\U0001F300-\\U0001F5FF"
        "\\U0001F680-\\U0001F6FF"
        "\\U0001F1E0-\\U0001F1FF"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub("", text)
'''

CODE[f"{ROOT}/generator/4_utils/__init__.py"] = '''"""Utils Module"""
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
    return written
