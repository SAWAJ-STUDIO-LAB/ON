from A_core.A13_tg_buffer import LOG_BUFFER


def step(filename, action, result="ok", detail=""):
    """Log a specific step in the process."""
    icon = {
        "ok": "✅", "fail": "❌", "skip": "⏭️",
        "warn": "⚠️", "info": "ℹ️"
    }.get(result, "ℹ️")
    line = f"{icon} <b>{filename}</b> → {action}"
    if detail:
        line += f" ({detail})"
    LOG_BUFFER.append(line)
