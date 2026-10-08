"""
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
        f"<b>{RUN_HEADER[0]} — FULL REPORT</b>\n"
        f"🕐 {now()}  |  ⏱️ {total_time:.1f}s\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    )
    body = "\n".join(LOG_BUFFER)
    extras = ""
    if extra_sections:
        extras = "\n\n" + "\n".join(extra_sections)
    full = head + body + extras

    chunks = []
    current = ""
    for line in full.split("\n"):
        if len(current) + len(line) + 1 > 3800:
            chunks.append(current)
            current = line
        else:
            current += ("\n" if current else "") + line
    if current:
        chunks.append(current)

    for i, chunk in enumerate(chunks, 1):
        prefix = f"📄 <b>Report {i}/{len(chunks)}</b>\n" if len(chunks) > 1 else ""
        send_raw(prefix + chunk, silent=silent)
