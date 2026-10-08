"""A16_tg_run_start.py — Sirf run start."""
from A_core.A13_tg_buffer import reset, now, RUN_HEADER
from A_core.A15_tg_send_raw import send_raw


def run_start(title="📖 STORY VIDEO RUN"):
    reset()
    RUN_HEADER[0] = title
    send_raw(f"▶️ <b>{title} STARTED</b>\n🕐 {now()}", silent=True)
