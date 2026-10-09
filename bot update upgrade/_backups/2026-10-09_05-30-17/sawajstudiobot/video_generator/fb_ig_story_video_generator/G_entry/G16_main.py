"""G16_main.py — Sirf main entry."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from A_core.A5_platform_checker import available_platforms
from A_core.A16_tg_run_start import run_start
from A_core.A24_tg_report import send_full_report
from A_core.A25_tg_summary import send_summary
from A_core.A28_http_session import create_session
from A_core.A32_api_tracker import create_tracker
from G_entry.G15_pipeline_run import run_pipeline


class BasePipeline:
    def __init__(self):
        self.session = create_session()
        self.api_status = create_tracker()


def main():
    run_start("📖 STORY VIDEO RUN")
    base = BasePipeline()
    try:
        run_pipeline(base)
        send_full_report()
        send_summary()
        sys.exit(0)
    except Exception:
        send_full_report()
        send_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()
