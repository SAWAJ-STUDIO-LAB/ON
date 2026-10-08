"""
A20_tg_api_call.py
Sirf api_call.
"""
from A_core.A13_tg_buffer import LOG_BUFFER


def api_call(filename, api_name, status, detail=""):
    """Add API call to buffer."""
    icon = {"success": "🟢", "failed": "🔴",
            "fallback": "🟡", "skipped": "⚪"}.get(status, "⚫")
    line = f"{icon} <b>{api_name}</b> [{status.upper()}]"
    if detail:
        line += f" — {detail}"
    LOG_BUFFER.append(line)
