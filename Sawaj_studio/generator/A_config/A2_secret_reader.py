# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A2_secret_reader.py
# 🎯 PURPOSE:   Secrets read karna — multi-fallback
# ═══════════════════════════════════════════════════════════

"""
🔑 SECRET READER
════════════════

🎯 Purpose:
   Multiple names try karke secret dhundhna.

📖 Example:
   read_secret("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
"""

import os


# ═══════════════════════════════════════════════════════════
# ① READ SECRET — try multiple names
# ═══════════════════════════════════════════════════════════

def read_secret(*names: str, default: str = "") -> str:
    """
    Return first non-empty env value from given names.

    Args:
        *names: Multiple env var names
        default: Fallback

    Returns:
        First found value or default
    """
    for name in names:
        val = os.environ.get(name, "").strip()
        if val and val.lower() not in ("none", "null", "undefined"):
            return val
    return default


# ═══════════════════════════════════════════════════════════
# ② CHECK SECRET EXISTS
# ═══════════════════════════════════════════════════════════

def has_secret(*names: str) -> bool:
    """Check if any secret exists."""
    return bool(read_secret(*names))


# ═══════════════════════════════════════════════════════════
# ③ MASK SECRET — for logs
# ═══════════════════════════════════════════════════════════

def mask_secret(value: str) -> str:
    """Mask secret for logging."""
    if not value:
        return "(empty)"
    if len(value) <= 8:
        return "***"
    return value[:4] + "***" + value[-4:]


# ═══════════════════════════════════════════════════════════
# ④ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🔑 Secret Reader Self-Test")
    print("=" * 50)
    key = read_secret("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI")
    print(f"  OpenRouter: {mask_secret(key)}")
    print("✅ Done")
