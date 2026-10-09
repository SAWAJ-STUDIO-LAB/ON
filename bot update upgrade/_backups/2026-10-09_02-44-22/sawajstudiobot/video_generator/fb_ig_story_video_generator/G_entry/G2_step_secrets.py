"""G2_step_secrets.py — Sirf secrets."""
from A_core.A9_log_step import log_step
from A_core.A45_secrets_verify import verify


def run(base):
    report = verify()
    s = report["summary"]
    log_step("G2_step_secrets.py", "Verified", "ok",
             f"{s['working_secrets']}/{s['total_secrets']}")
    return report
