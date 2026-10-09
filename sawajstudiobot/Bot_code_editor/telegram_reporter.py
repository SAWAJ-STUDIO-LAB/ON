"""
Telegram Reporter — All Telegram messages
"""
import os
import time
import requests
from datetime import datetime
from typing import Dict


# ═══════════════════════════════════════════════════════════
# TELEGRAM SEND
# ═══════════════════════════════════════════════════════════
def tg(msg: str, silent: bool = False) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return
    chunks = [msg[i:i+3800] for i in range(0, len(msg), 3800)]
    for chunk in chunks:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": chunk,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "disable_notification": silent,
                },
                timeout=15)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════
# START REPORT
# ═══════════════════════════════════════════════════════════
def report_start() -> None:
    tg(f"👑 <b>Sawaj AI Developer Started</b>\n"
       f"📂 Folder-by-folder mode\n"
       f"🕐 {datetime.now().strftime('%H:%M:%S')}", silent=True)


# ═══════════════════════════════════════════════════════════
# SCAN REPORT
# ═══════════════════════════════════════════════════════════
def report_scan(bot_count: int, wf_count: int,
                 total: int, folders: int) -> None:
    tg(f"""📊 <b>Scan Complete</b>

📁 sawajstudiobot/ — <b>{bot_count}</b> files
📁 .github/workflows/ — <b>{wf_count}</b> files

📦 <b>Total: {total} files</b>
📂 <b>Total Folders: {folders}</b>
🎯 Mode: <b>Folder-by-Folder</b>""")


# ═══════════════════════════════════════════════════════════
# BATCH REPORT
# ═══════════════════════════════════════════════════════════
def report_batch(bnum: int, btotal: int, folder_name: str,
                  file_count: int, ops: Dict, used_ai: str) -> None:
    tg(f"""✅ <b>Batch {bnum}/{btotal}</b>

📂 <b>Folder:</b> {folder_name}/
📄 <b>Files:</b> {file_count}
💾 <b>Updated:</b> {len(ops['updates'])}
➕ <b>Created:</b> {len(ops['creates'])}
📁 <b>Folders:</b> {len(ops['folders'])}
🗑️ <b>Deleted:</b> {len(ops['deletes'])}
✂️ <b>Splits:</b> {len(ops['splits'])}
🤖 <b>AI:</b> {used_ai}""", silent=True)


# ═══════════════════════════════════════════════════════════
# COMPLETE REPORT
# ═══════════════════════════════════════════════════════════
def report_complete(stats: Dict, total_folders: int,
                     failed_batches: list,
                     ai_used: Dict, elapsed: float) -> None:
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)

    ai_summary = "\n".join(
        f"   • {ai}: {cnt} folders"
        for ai, cnt in sorted(ai_used.items(), key=lambda x: -x[1]))

    tg(f"""🏁 <b>Sawaj AI Developer Complete</b>

═══════════════════════════════════════════
📊 <b>RESULTS</b>
═══════════════════════════════════════════
📂 <b>Total Folders:</b> {total_folders}
💾 <b>Files Updated:</b> {stats['updated']}
⏭️ <b>Cancelled (not better):</b> {stats['cancelled']}
❌ <b>Invalid syntax:</b> {stats['invalid']}
➕ <b>New Files Created:</b> {stats['created_files']}
📁 <b>New Folders:</b> {stats['created_folders']}
🗑️ <b>Files Deleted:</b> {stats['deleted']}
✂️ <b>Files Split:</b> {stats['splits']}
⚠️ <b>Failed Folders:</b> {len(failed_batches)}
⏱️ <b>Time:</b> {mins}m {secs}s

═══════════════════════════════════════════
🤖 <b>AI USAGE</b>
═══════════════════════════════════════════
{ai_summary}""")
