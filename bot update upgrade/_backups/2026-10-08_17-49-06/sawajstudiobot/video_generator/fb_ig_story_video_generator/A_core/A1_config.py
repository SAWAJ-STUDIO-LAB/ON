# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A1_config.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A1_config.py                       ║
# ║  🎯 PURPOSE:   Config matching existing secret names     ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
⚙️  CONFIG MODULE (Secret-Name Matched)
═══════════════════════════════════════

🎯 Purpose:
   Aapke GitHub Secrets ke existing naamon se match karta hai.
   Kuchh bhi rename nahi karna padega.

📋 Secret Fallback Strategy:
   Har env var ke liye MULTIPLE names try karta hai.
   Jo pehle mile, wahi use hota hai.

🔑 Examples:
   Facebook Meta Token:
     1. FACEBOOK_META_TOKEN         ← Preferred
     2. FACEBOOK_INSTAGRAM_META_TOKEN ← Aapka current name

   OpenRouter:
     1. OPENROUTER_API_KEY          ← Preferred
     2. OPENROUTER_API_KEY_AI       ← Aapka current name

   Groq:
     1. GROQ_API_KEY
     2. GROQ_API_KEY_AI

   Cerebras:
     1. CEREBRAS_API_KEY            ← Correct spelling
     2. CEREBRAS_API_KEY_AI
     3. CELEBRAS_API_KEY_AI         ← Aapka typo wala naam
"""

import os


# ═══════════════════════════════════════════════════════════
# 🔧 HELPER — Get first non-empty env var
# ═══════════════════════════════════════════════════════════

def _env(*names, default=""):
    """
    Return first non-empty env value from given names.
    
    Args:
        *names: Multiple env var names to try
        default: Fallback if none found
    
    Returns:
        First non-empty value, or default
    """
    for name in names:
        val = os.environ.get(name, "").strip()
        if val:
            return val
    return default


# ═══════════════════════════════════════════════════════════
# ⚙️  CONFIG CLASS
# ═══════════════════════════════════════════════════════════

class Config:
    """Config — multi-mode upload system (Story) with fallback names."""
    
    # ─── TELEGRAM ───
    TG_TOKEN = _env("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = _env("TELEGRAM_CHAT_ID")
    
    # ─── FACEBOOK ───
    # Try both names (aapke paas FACEBOOK_INSTAGRAM_META_TOKEN hai)
    META_TOKEN = _env(
        "FACEBOOK_META_TOKEN",
        "FACEBOOK_INSTAGRAM_META_TOKEN",
    )
    PAGE_ID = _env("FACEBOOK_PAGE_ID")
    
    # ─── INSTAGRAM ───
    # Try both names
    IG_TOKEN = _env(
        "FACEBOOK_INSTAGRAM_META_TOKEN",
        "FACEBOOK_META_TOKEN",
    )
    IG_BUSINESS_ID = _env("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    
    # ─── YOUTUBE ───
    YT_CLIENT_ID = _env("YOUTUBE_CLIENT_ID")
    YT_CLIENT_SECRET = _env("YOUTUBE_CLIENT_SECRET")
    YT_REFRESH_TOKEN = _env("YOUTUBE_REFRESH_TOKEN")
    YT_PLAYLIST_ID = _env("DAILY_HADEES_YT_PLAYLIST_ID")
    
    # ─── DRIVE ───
    DRIVE_CLIENT_ID = _env("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = _env("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = _env("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_STORY_FOLDER_ID = _env(
        "GDRIVE_STORY_VIDEO_FOLDER_ID",
        "GDRIVE_SHORT_VIDEO_FOLDER_ID",  # Fallback
    )
    
    # ─── AI PROVIDERS (with _AI suffix support) ───
    OPENROUTER_API_KEY = _env(
        "OPENROUTER_API_KEY",
        "OPENROUTER_API_KEY_AI",
    )
    GROQ_API_KEY = _env(
        "GROQ_API_KEY",
        "GROQ_API_KEY_AI",
    )
    GEMINI_API_KEY = _env(
        "GEMINI_API_KEY",
        "GEMINI_API_KEY_AI",
    )
    MISTRAL_API_KEY = _env(
        "MISTRAL_API_KEY",
        "MISTRAL_API_KEY_AI",
    )
    CEREBRAS_API_KEY = _env(
        "CEREBRAS_API_KEY",           # Correct spelling
        "CEREBRAS_API_KEY_AI",        # Correct + _AI
        "CELEBRAS_API_KEY_AI",        # Aapka typo wala
    )
    COHERE_API_KEY = _env(
        "COHERE_API_KEY",
        "COHERE_API_KEY_AI",
    )
    HUGGINGFACE_API_KEY = _env(
        "HUGGINGFACE_API_KEY",
        "HUGGINGFACE_API_KEY_AI",
    )
    
    # ─── TTS / TRANSLATION ───
    ELEVENLABS_API_KEY = _env("ELEVENLABS_API_KEY")
    DEEPL_API_KEY = _env("DEEPL_API_KEY")
    
    # ─── MEDIA APIS ───
    PEXELS_API_KEY = _env("PEXELS_API_KEY")
    PIXABAY_API_KEY = _env("PIXABAY_API_KEY")
    FREESOUND_API_KEY = _env("FREESOUND_API_KEY")
    
    # ─── HADITH ───
    HADITH_API_URL = _env("HADITH_API_URL")
    
    # ─── RUNTIME ───
    EVENT_NAME = _env("GITHUB_EVENT_NAME")
    UPLOAD_TARGET = _env("UPLOAD_TARGET", default="drive_only").lower()
    CONFIRM_UPLOAD = _env("CONFIRM_UPLOAD", default="false").lower() == "true"
    
    # ═══════════════════════════════════════════════════════
    # 🎯 UPLOAD LOGIC PROPERTIES
    # ═══════════════════════════════════════════════════════
    
    @property
    def is_scheduled(self) -> bool:
        """Cron-triggered?"""
        return self.EVENT_NAME == "schedule"
    
    @property
    def is_manual(self) -> bool:
        """Manual workflow_dispatch?"""
        return self.EVENT_NAME == "workflow_dispatch"
    
    @property
    def is_confirmed(self) -> bool:
        """Manual mode mein tick mark lagaya?"""
        if self.is_scheduled:
            return True
        return self.CONFIRM_UPLOAD
    
    # ─────────────────────────────────────────────────────
    # 🎯 UPLOAD DECISIONS
    # ─────────────────────────────────────────────────────
    
    @property
    def should_upload_drive(self) -> bool:
        """Google Drive upload — always True (backup)."""
        return True
    
    @property
    def should_upload_facebook(self) -> bool:
        """Facebook Story upload?"""
        if self.is_scheduled:
            return True
        if not self.is_confirmed:
            return False
        return self.UPLOAD_TARGET in ("fb_ig", "all")
    
    @property
    def should_upload_instagram(self) -> bool:
        """Instagram Story upload?"""
        if self.is_scheduled:
            return True
        if not self.is_confirmed:
            return False
        return self.UPLOAD_TARGET in ("fb_ig", "all")
    
    @property
    def should_upload_youtube(self) -> bool:
        """YouTube Shorts upload?"""
        if self.is_scheduled:
            return False
        if not self.is_confirmed:
            return False
        return self.UPLOAD_TARGET in ("youtube", "all")
    
    # ─────────────────────────────────────────────────────
    # 🎯 AVAILABLE PLATFORMS
    # ─────────────────────────────────────────────────────
    
    def available_platforms(self) -> list:
        """Which platforms have valid credentials?"""
        platforms = []
        
        # ───── Facebook ─────
        if self.META_TOKEN and self.PAGE_ID:
            platforms.append("facebook")
        
        # ───── Instagram ─────
        if self.IG_TOKEN and self.IG_BUSINESS_ID:
            platforms.append("instagram")
        
        # ───── YouTube ─────
        if all([self.YT_CLIENT_ID, self.YT_CLIENT_SECRET, self.YT_REFRESH_TOKEN]):
            platforms.append("youtube")
        
        return platforms
    
    # ─────────────────────────────────────────────────────
    # 🎯 RUN CONTEXT
    # ─────────────────────────────────────────────────────
    
    def describe(self) -> str:
        """Human-readable description of current run mode."""
        if self.is_scheduled:
            return "🤖 AUTO (scheduled) → Drive + FB + IG"
        
        if not self.is_confirmed:
            return "⚠️  MANUAL unconfirmed → Drive only"
        
        targets = {
            "drive_only": "📁 Drive Only",
            "fb_ig": "📘📸 FB + IG Story",
            "youtube": "📺 YouTube Shorts",
            "all": "🌟 All platforms",
        }
        
        return f"🎯 MANUAL → {targets.get(self.UPLOAD_TARGET, '?')}"
    
    def summary(self) -> dict:
        """Full config summary."""
        return {
            "event": self.EVENT_NAME or "local",
            "mode": "auto" if self.is_scheduled else "manual",
            "target": self.UPLOAD_TARGET,
            "confirmed": self.CONFIRM_UPLOAD,
            "should_upload": {
                "drive": self.should_upload_drive,
                "facebook": self.should_upload_facebook,
                "instagram": self.should_upload_instagram,
                "youtube": self.should_upload_youtube,
            },
            "available": self.available_platforms(),
        }


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("⚙️  Config Self-Test")
    print("=" * 50)
    
    cfg = Config()
    
    print(f"\n📍 Run Context:")
    print(f"   Event:     {cfg.EVENT_NAME or 'local'}")
    print(f"   Mode:      {'auto' if cfg.is_scheduled else 'manual'}")
    print(f"   Target:    {cfg.UPLOAD_TARGET}")
    print(f"   Confirmed: {cfg.CONFIRM_UPLOAD}")
    
    print(f"\n🔑 Key Secrets Detected:")
    checks = [
        ("Telegram Bot", cfg.TG_TOKEN),
        ("Telegram Chat", cfg.TG_CHAT_ID),
        ("Facebook Meta", cfg.META_TOKEN),
        ("Facebook Page", cfg.PAGE_ID),
        ("Instagram Token", cfg.IG_TOKEN),
        ("Instagram ID", cfg.IG_BUSINESS_ID),
        ("YouTube Client", cfg.YT_CLIENT_ID),
        ("Drive Client", cfg.DRIVE_CLIENT_ID),
        ("Drive Folder", cfg.DRIVE_STORY_FOLDER_ID),
        ("OpenRouter", cfg.OPENROUTER_API_KEY),
        ("Groq", cfg.GROQ_API_KEY),
        ("Gemini", cfg.GEMINI_API_KEY),
        ("Mistral", cfg.MISTRAL_API_KEY),
        ("Cerebras", cfg.CEREBRAS_API_KEY),
        ("Cohere", cfg.COHERE_API_KEY),
        ("DeepL", cfg.DEEPL_API_KEY),
        ("ElevenLabs", cfg.ELEVENLABS_API_KEY),
        ("Pexels", cfg.PEXELS_API_KEY),
    ]
    
    for label, value in checks:
        icon = "✅" if value else "❌"
        length = f"({len(value)} chars)" if value else ""
        print(f"   {icon} {label:20} {length}")
    
    print(f"\n🌐 Available Platforms:")
    for p in cfg.available_platforms():
        print(f"   ✅ {p}")
    
    print(f"\n📖 Description: {cfg.describe()}")
