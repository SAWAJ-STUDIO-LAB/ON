"""
🔐 Env Checker
"""
import os


def check_env(*keys):
    missing = [k for k in keys if not os.environ.get(k, "").strip()]
    return {"valid": len(missing) == 0, "missing": missing}


def check_any(*keys):
    for k in keys:
        if os.environ.get(k, "").strip():
            return True
    return False


def get_all_env():
    return {k: v for k, v in os.environ.items() if "API" in k or "TOKEN" in k}
