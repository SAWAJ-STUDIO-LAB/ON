# Re-export universal Telegram + Story-specific header default
from universal.U2_telegram import *                              # noqa
from universal.U2_telegram import (
    set_header, run_start as _run_start,
    send_full_report, send_summary,
)

# Set Story header once at import time
set_header("📖 STORY VIDEO RUN")


def run_start(title=None):
    _run_start(title or "📖 STORY VIDEO RUN")
