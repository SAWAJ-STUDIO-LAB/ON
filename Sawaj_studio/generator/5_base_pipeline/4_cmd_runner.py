"""
▶️ Command Runner
"""
import subprocess


def run_cmd(cmd, timeout=1800):
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                                capture_output=True, text=True, timeout=timeout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, str(e)[:200]
    except subprocess.TimeoutExpired:
        return False, "Timeout"


def run_cmd_silent(cmd, timeout=1800):
    try:
        subprocess.run(cmd, shell=True, check=True,
                       capture_output=True, timeout=timeout)
        return True
    except Exception:
        return False
