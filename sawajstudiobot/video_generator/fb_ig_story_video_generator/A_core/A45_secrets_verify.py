"""A45_secrets_verify.py — Sirf verify."""
from datetime import datetime
from A_core.A33_secrets_registry import SECRETS_REGISTRY
from A_core.A34_secrets_env_check import check_env
from A_core.A35_ping_telegram import ping as p_tg
from A_core.A36_ping_facebook import ping as p_fb
from A_core.A37_ping_instagram import ping as p_ig
from A_core.A38_ping_drive import ping as p_dr
from A_core.A39_ping_openrouter import ping as p_or
from A_core.A40_ping_groq import ping as p_gq
from A_core.A41_ping_pexels import ping as p_px
from A_core.A42_secrets_summary import build as b_sum


def verify():
    sr = {}
    for ck, meta in SECRETS_REGISTRY.items():
        cr = {"label": meta["label"], "required": meta["required"],
              "min_required": meta.get("min_required", 0),
              "secrets": {}, "set_count": 0, "missing_count": 0,
              "total": len(meta["secrets"])}
        for sk, sm in meta["secrets"].items():
            found, actual, length = check_env(*sm["names"])
            cr["secrets"][sk] = {"label": sm["label"], "is_set": found,
                                 "actual_name": actual if found else "", "length": length}
            if found:
                cr["set_count"] += 1
            else:
                cr["missing_count"] += 1
        if cr["missing_count"] == 0:
            cr["status"] = "complete"
        elif cr["set_count"] >= cr["min_required"]:
            cr["status"] = "partial"
        elif cr["required"]:
            cr["status"] = "critical"
        else:
            cr["status"] = "optional_missing"
        sr[ck] = cr
    ar = {"telegram": p_tg(), "facebook": p_fb(), "instagram": p_ig(),
          "google_drive": p_dr(), "openrouter": p_or(), "groq": p_gq(), "pexels": p_px()}
    return {"secrets": sr, "api_health": ar,
            "summary": b_sum(sr, ar),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
