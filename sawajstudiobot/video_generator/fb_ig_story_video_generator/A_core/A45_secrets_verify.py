"""
A45_secrets_verify.py
Sirf main verify function.
"""
from datetime import datetime
from A_core.A33_secrets_registry import SECRETS_REGISTRY
from A_core.A34_secrets_env_check import check_env
from A_core.A35_ping_telegram import ping as ping_telegram
from A_core.A36_ping_facebook import ping as ping_facebook
from A_core.A37_ping_instagram import ping as ping_instagram
from A_core.A38_ping_drive import ping as ping_drive
from A_core.A39_ping_openrouter import ping as ping_openrouter
from A_core.A40_ping_groq import ping as ping_groq
from A_core.A41_ping_pexels import ping as ping_pexels
from A_core.A42_secrets_summary import build as build_summary


def verify():
    """Run full verification."""
    secrets_report = {}
    for cat_key, meta in SECRETS_REGISTRY.items():
        cat_report = {
            "label": meta["label"],
            "required": meta["required"],
            "min_required": meta.get("min_required", 0),
            "secrets": {}, "set_count": 0, "missing_count": 0,
            "total": len(meta["secrets"]),
        }
        for sk, sm in meta["secrets"].items():
            found, actual, length = check_env(*sm["names"])
            cat_report["secrets"][sk] = {
                "label": sm["label"], "is_set": found,
                "actual_name": actual if found else "", "length": length,
            }
            if found:
                cat_report["set_count"] += 1
            else:
                cat_report["missing_count"] += 1

        if cat_report["missing_count"] == 0:
            cat_report["status"] = "complete"
        elif cat_report["set_count"] >= cat_report["min_required"]:
            cat_report["status"] = "partial"
        elif cat_report["required"]:
            cat_report["status"] = "critical"
        else:
            cat_report["status"] = "optional_missing"

        secrets_report[cat_key] = cat_report

    api_report = {
        "telegram": ping_telegram(),
        "facebook": ping_facebook(),
        "instagram": ping_instagram(),
        "google_drive": ping_drive(),
        "openrouter": ping_openrouter(),
        "groq": ping_groq(),
        "pexels": ping_pexels(),
    }

    return {
        "secrets": secrets_report,
        "api_health": api_report,
        "summary": build_summary(secrets_report, api_report),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
