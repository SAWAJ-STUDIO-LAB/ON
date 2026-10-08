"""
A23_tg_send.py
Sirf send_tg.
"""
from A_core.A15_tg_send_raw import send_raw


def send_tg(msg, silent=False):
    """Send message to Telegram immediately."""
    send_raw(msg, silent=silent)
