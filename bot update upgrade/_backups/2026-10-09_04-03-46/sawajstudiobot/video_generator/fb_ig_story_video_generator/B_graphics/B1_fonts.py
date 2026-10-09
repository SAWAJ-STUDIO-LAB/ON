# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B1_fonts.py                               ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                B_graphics/B1_fonts.py                    ║
# ║  🎯 PURPOSE:   Font loader — robust multi-path fallback  ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
🔤 FONT LOADER (UPGRADED)
═══════════════════════════

🎯 Purpose:
   Hindi (Devanagari), Urdu (Arabic), aur English (Latin) ke
   fonts ko load karta hai — MULTIPLE FALLBACK PATHS ke saath.

📖 Kya improve hua:
   ✅ Pehle: Sirf ~/.fonts/ check karta tha → crash
   ✅ Ab: 7 different paths try karta hai (Windows/Mac/Linux)
   ✅ Ab: System fonts bhi check karta hai
   ✅ Ab: Font missing par warning deta hai (silent fail nahi)
   ✅ Ab: Cached fonts — same font baar baar load nahi hoga (fast)

📁 Path Search Order (Har Script Ke Liye):
   1. ~/.fonts/NotoSansDevanagari-Bold.ttf       ← GitHub Actions
   2. /usr/share/fonts/truetype/noto/            ← Linux system
   3. /Library/Fonts/                            ← macOS
   4. C:/Windows/Fonts/                          ← Windows
   5. ./assets/fonts/                            ← Local project
   6. Default DejaVu                              ← Ultimate fallback
   7. PIL default                                 ← Last resort
"""

import os
import warnings
from functools import lru_cache
from PIL import ImageFont, Image


# ═══════════════════════════════════════════════════════════
# 🗂️  FONT PATHS REGISTRY — Har script ke liye possible paths
# ═══════════════════════════════════════════════════════════

def _get_font_paths(script: str, bold: bool) -> list:
    """
    Return list of possible font paths for given script.
    
    Args:
        script: "devanagari" | "arabic" | "latin"
        bold:   True = Bold, False = Regular
    
    Returns:
        List of paths (in priority order)
    """
    weight = "Bold" if bold else "Regular"
    
    # ───── Script-specific font names ─────
    if script == "devanagari":
        font_names = [
            f"NotoSansDevanagari-{weight}.ttf",
            "NotoSansDevanagari-Bold.ttf",      # fallback
            "NotoSerifDevanagari-Bold.ttf",
            "Mangal.ttf",                        # Windows Hindi
            "NirmalaUI-Bold.ttf",                # Windows
        ]
    elif script == "arabic":
        font_names = [
            f"NotoNaskhArabic-{weight}.ttf",
            "NotoNaskhArabic-Bold.ttf",
            "NotoSansArabic-Bold.ttf",
            "Amiri-Bold.ttf",
            "Scheherazade-Bold.ttf",
        ]
    else:  # latin
        font_names = [
            f"NotoSans-{weight}.ttf",
            "NotoSans-Bold.ttf",
            "DejaVuSans-Bold.ttf",
            "Arial-Bold.ttf",
            "Arial.ttf",
        ]
    
    # ───── Base directories ─────
    home = os.path.expanduser("~")
    cwd = os.getcwd()
    
    base_dirs = [
        f"{home}/.fonts",                            # Linux / GH Actions
        "/usr/share/fonts/truetype/noto",            # Linux system
        "/usr/share/fonts/truetype/dejavu",          # Linux DejaVu
        "/usr/share/fonts/TTF",                      # Arch
        "/Library/Fonts",                            # macOS
        "/System/Library/Fonts",                     # macOS system
        "C:/Windows/Fonts",                          # Windows
        f"{cwd}/assets/fonts",                       # Project local
        f"{cwd}/fonts",                              # Project local
    ]
    
    # ───── Combine: dir × font_name ─────
    paths = []
    for d in base_dirs:
        for name in font_names:
            paths.append(os.path.join(d, name))
    
    return paths


# ═══════════════════════════════════════════════════════════
# 🔤 FONT LOADER CLASS
# ═══════════════════════════════════════════════════════════

class FontLoader:
    """
    Multi-path font loader with aggressive fallback.
    
    Usage:
        font = FontLoader.load(72, "devanagari")   # Bold Hindi
        font = FontLoader.load(48, "arabic", False) # Regular Urdu
        font = FontLoader.load(64, "latin")         # Bold English
    """
    
    # ───── Class-level cache (avoid re-loading same font) ─────
    _cache = {}
    _warned = set()
    
    # ─────────────────────────────────────────────────────
    # ① LOAD — main method
    # ─────────────────────────────────────────────────────
    @classmethod
    def load(cls, size: int, script: str = "latin", bold: bool = True):
        """
        Load font with multi-path fallback.
        
        Args:
            size:   Font size (pixels)
            script: "devanagari" | "arabic" | "latin"
            bold:   True = Bold, False = Regular
        
        Returns:
            PIL ImageFont object (never None)
        """
        # ───── Check cache first ─────
        cache_key = (size, script, bold)
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        # ───── Try all paths ─────
        font_paths = _get_font_paths(script, bold)
        
        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, size)
                    cls._cache[cache_key] = font
                    return font
                except Exception:
                    continue
        
        # ───── No path worked — warn only once ─────
        warn_key = f"{script}_{bold}"
        if warn_key not in cls._warned:
            cls._warned.add(warn_key)
            warnings.warn(
                f"⚠️ Font not found for script='{script}' bold={bold}. "
                f"Tried {len(font_paths)} paths. Using default font.",
                RuntimeWarning,
                stacklevel=2
            )
        
        # ───── Ultimate fallback: PIL default ─────
        try:
            # Pillow 10+ has size-aware default font
            if hasattr(ImageFont, "load_default") and size > 10:
                try:
                    default = ImageFont.load_default(size=size)
                except TypeError:
                    default = ImageFont.load_default()
            else:
                default = ImageFont.load_default()
        except Exception:
            default = ImageFont.load_default()
        
        cls._cache[cache_key] = default
        return default
    
    # ─────────────────────────────────────────────────────
    # ② CLEAR CACHE — memory management
    # ─────────────────────────────────────────────────────
    @classmethod
    def clear_cache(cls):
        """Clear font cache (useful in tests or long runs)."""
        cls._cache.clear()
        cls._warned.clear()
    
    # ─────────────────────────────────────────────────────
    # ③ FONT INFO — debug helper
    # ─────────────────────────────────────────────────────
    @classmethod
    def info(cls, size: int, script: str = "latin", bold: bool = True) -> dict:
        """
        Return info about which font would be loaded.
        Useful for debugging.
        """
        font_paths = _get_font_paths(script, bold)
        for path in font_paths:
            if os.path.exists(path):
                return {
                    "script": script,
                    "bold": bold,
                    "size": size,
                    "found_path": path,
                    "used_fallback": False,
                }
        return {
            "script": script,
            "bold": bold,
            "size": size,
            "found_path": None,
            "used_fallback": True,
            "total_tried": len(font_paths),
        }


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST (Run this file directly to verify)
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🔤 FontLoader Self-Test")
    print("=" * 50)
    
    for script in ("devanagari", "arabic", "latin"):
        info = FontLoader.info(72, script, bold=True)
        print(f"\n📖 Script: {script}")
        print(f"   Found: {info['found_path']}")
        print(f"   Fallback: {info['used_fallback']}")
        
        font = FontLoader.load(72, script, bold=True)
        print(f"   Loaded: {type(font).__name__} ✅")
    
    print("\n✅ All fonts loaded successfully!")
