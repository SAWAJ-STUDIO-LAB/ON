"""
A22_tg_header.py
Sirf header.
"""
from A_core.A13_tg_buffer import LOG_BUFFER


def header(title):
    """Add header to buffer."""
    LOG_BUFFER.append(f"\n<b>━━━ {title} ━━━</b>")
