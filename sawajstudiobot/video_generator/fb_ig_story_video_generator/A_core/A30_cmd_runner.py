"""A30_cmd_runner.py — Sirf cmd runner."""
import subprocess
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error


def run_cmd(cmd):
    log_step("A30_cmd_runner.py", f"CMD: {cmd[:80]}", "ok")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_error("A30_cmd_runner.py", f"CMD failed: {str(e)[:120]}")
        raise
