# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A9_validation.py
# 🎯 PURPOSE:   Config validation
# ═══════════════════════════════════════════════════════════

"""
✅ CONFIG VALIDATION
═════════════════════

🎯 Purpose:
   Config sahi hai ya nahi, check karna.
"""

from A_config.A2_secret_reader import has_secret
from A_config.A8_worker_selector import list_workers


# ═══════════════════════════════════════════════════════════
# ① VALIDATE SECRETS
# ═══════════════════════════════════════════════════════════

def validate_secrets(worker: str) -> dict:
    """
    Validate required secrets for worker.

    Args:
        worker: story/short/long

    Returns:
        {
          "valid": bool,
          "critical_missing": [...],
          "optional_missing": [...],
        }
    """
    # Critical (hamesha chahiye)
    critical = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]

    # Optional (fallback hain)
    optional = [
        ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI"),
        ("GROQ_API_KEY", "GROQ_API_KEY_AI"),
        ("GEMINI_API_KEY", "GEMINI_API_KEY_AI"),
        ("PEXELS_API_KEY",),
        ("HADITH_API_URL",),
    ]

    missing_critical = [k for k in critical if not has_secret(k)]
    missing_optional = [
        names[0] for names in optional if not has_secret(*names)
    ]

    return {
        "valid": len(missing_critical) == 0,
        "critical_missing": missing_critical,
        "optional_missing": missing_optional,
    }


# ═══════════════════════════════════════════════════════════
# ② VALIDATE WORKER
# ═══════════════════════════════════════════════════════════

def validate_worker(name: str) -> bool:
    """Check if worker name is valid."""
    return name in list_workers()


# ═══════════════════════════════════════════════════════════
# ③ RUN FULL VALIDATION
# ═══════════════════════════════════════════════════════════

def run_validation(worker: str = "story") -> dict:
    """Run full validation."""
    result = {
        "worker_valid": validate_worker(worker),
        "secrets": validate_secrets(worker),
    }
    result["all_valid"] = (
        result["worker_valid"] and result["secrets"]["valid"]
    )
    return result


# ═══════════════════════════════════════════════════════════
# ④ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("✅ Config Validation Self-Test")
    print("=" * 50)
    result = run_validation("story")
    print(f"  Worker valid: {result['worker_valid']}")
    print(f"  Secrets valid: {result['secrets']['valid']}")
    print(f"  Critical missing: {result['secrets']['critical_missing']}")
    print(f"  Optional missing: {result['secrets']['optional_missing']}")
    print("✅ Done")# -*- coding: utf-8 -*-
