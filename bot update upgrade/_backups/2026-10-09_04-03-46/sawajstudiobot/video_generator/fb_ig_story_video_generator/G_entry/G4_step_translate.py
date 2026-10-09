"""G4_step_translate.py — Sirf translate."""
from A_core.A9_log_step import log_step
from C_content.C15_translate_main import to_hindi


def run(base, english):
    hindi = to_hindi(base.session, english)
    log_step("G4_step_translate.py", "Done", "ok")
    return hindi
