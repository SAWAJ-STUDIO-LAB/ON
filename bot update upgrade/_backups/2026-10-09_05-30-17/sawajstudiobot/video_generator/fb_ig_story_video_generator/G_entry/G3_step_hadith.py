"""G3_step_hadith.py — Sirf hadith."""
from A_core.A9_log_step import log_step
from C_content.C5_hadith_main import fetch


def run(base):
    h = fetch(base.session)
    log_step("G3_step_hadith.py", "Fetched", "ok",
             f"{h['collection']} #{h['number']}")
    return h
