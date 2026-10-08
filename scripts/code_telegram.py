"""
Sawaj Studio Module
"""
"""
📱 3_telegram — Saare telegram modules ka code
"""
import os

ROOT = "Sawaj_studio"
CODE = {}

# ═══════════════════════════════════════════════════════════
# 1_bot_sender.py
# ═══════════════════════════════════════════════════════════
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
                files={"document": f},
                timeout=60)
        return r.status_code == 200
    except Exception:
        return False
'''

# ═══════════════════════════════════════════════════════════
# 2_message_builder.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 3_html_formatter.py
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/3_telegram/3_html_formatter.py"] = '''"""
🎨 HTML Formatter
"""


def bold(text):
    return "<b>" + str(text) + "</b>"


def italic(text):
    return "<i>" + str(text) + "</i>"


def code(text):
    return "<code>" + str(text) + "</code>"


def link(url, text):
    return "<a href='" + url + "'>" + text + "</a>"
'''

# ═══════════════════════════════════════════════════════════
# 4_document_sender.py
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/3_telegram/4_document_sender.py"] = '''"""
📄 Document Sender
"""
from .1_bot_sender import send_document


def send_report(path, caption="Report"):
    return send_document(path, caption)


def send_log_file(path):
    return send_document(path, "📋 Log File")
'''

# ═══════════════════════════════════════════════════════════
# 5_error_report.py
# ═══════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════
# 6_summary_sender.py
# ═══════════════════════════════════════════════════════════
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
        lines.append(f"• {k}: <b>{v}</b>")
    return send_message("\\n".join(lines))
'''

# ═══════════════════════════════════════════════════════════
# 7_chunk_splitter.py
# ═══════════════════════════════════════════════════════════
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
# __init__.py
# ═══════════════════════════════════════════════════════════
CODE[f"{ROOT}/generator/3_telegram/__init__.py"] = '''"""Telegram Module"""
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
