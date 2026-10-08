# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A1_env_loader.py
# 📁 PATH:      generator/A_config/A1_env_loader.py
# 🎯 PURPOSE:   Environment variables load karna
# ═══════════════════════════════════════════════════════════

"""
🔧 ENV LOADER
═════════════

🎯 Purpose:
   .env file ya system env se variables load karna.

📖 Kaam:
   • .env file padhna
   • Key=Value parse karna
   • os.environ mein set karna
   • Duplicate avoid karna

🔑 Usage:
   from A_config.A1_env_loader import load_env
   load_env()
"""

import os


# ═══════════════════════════════════════════════════════════
# ① LOAD ENV FILE
# ═══════════════════════════════════════════════════════════

def load_env(env_path: str = ".env") -> bool:
    """
    Load .env file into os.environ.

    Args:
        env_path: path to .env file

    Returns:
        True if loaded, False otherwise
    """
    if not os.path.exists(env_path):
        return False

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue

                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")

                if key and key not in os.environ:
                    os.environ[key] = val

        return True
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════
# ② GET ENV
# ═══════════════════════════════════════════════════════════

def get_env(key: str, default: str = "") -> str:
    """Get env variable with default."""
    return os.environ.get(key, default).strip()


# ═══════════════════════════════════════════════════════════
# ③ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🔧 Env Loader Self-Test")
    print("=" * 50)
    print(f"  Loaded: {load_env()}")
    print(f"  TELEGRAM_BOT_TOKEN: {get_env('TELEGRAM_BOT_TOKEN')[:10]}...")
    print("✅ Done")
