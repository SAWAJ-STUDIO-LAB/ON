# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A1_config.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A1_config.py                       ║
# ║  🎯 PURPOSE:   Config with YouTube + upload modes        ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
⚙️  CONFIG MODULE (UPGRADED)
═══════════════════════════

🎯 Purpose:
   Environment variables load + upload modes decide karna.

🔴 PEHLE KYA THA:
   • Sirf 2 modes: offline / online
   • YouTube support nahi
   • Manual confirmation sirf bool

✅ AB KYA HAI:
   • 4 Manual upload modes:
       1. drive_only  → Sirf Google Drive
       2. fb_ig       → Facebook Story + Instagram Story
       3. youtube     → YouTube Shorts
       4. all         → Sab kuch (Drive + FB + IG + YT)
   
   • Auto (schedule):
       → Drive + FB Story + IG Story (YouTube skip by default)

📋 Environment Variables:
   • GITHUB_EVENT_NAME  → "schedule" or "workflow_dispatch"
   • UPLOAD_TARGET      → "drive_only" | "fb_ig" | "youtube" | "all"
   • CONFIRM_UPLOAD     → "true" | "false" (tick mark)

🔐 Safety:
   • Manual mode mein CONFIRM_UPLOAD=true zaroori
   • Auto mode mein always allowed
"""

import os


# ═══════════════════════════════════════════════════════════
# ⚙️  CONFIG CLASS
# ═══════════════════════════════════════════════════════════

class Config:
    """Config — multi-mode upload system (Story)."""
    
    # ─── TELEGRAM ───
    TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    
    # ─── FACEBOOK ───
    META_TOKEN = os.environ.get("FACEBOOK_META_TOKEN", "").strip()
    PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    
    # ─── INSTAGRAM ───
    IG_TOKEN = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    IG_BUSINESS_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    
    # ─── YOUTUBE ───
    YT_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID", "").strip()
    YT_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET", "").strip()
    YT_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN", "").strip()
    YT_PLAYLIST_ID = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID", "").strip()
    
    # ─── DRIVE ───
    DRIVE_CLIENT_ID = os.environ.get("GOOGLE_DRIVE_CLIENT_ID")
    DRIVE_CLIENT_SECRET = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET")
    DRIVE_REFRESH_TOKEN = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN")
    DRIVE_STORY_FOLDER_ID = os.environ.get("GDRIVE_STORY_VIDEO_FOLDER_ID")
    
    # ─── AI PROVIDERS ───
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
    CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY")
    COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
    
    # ─── TTS / TRANSLATION ───
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")
    
    # ─── MEDIA APIS ───
    PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
    PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY")
    FREESOUND_API_KEY = os.environ.get("FREESOUND_API_KEY")
    
    # ─── HADITH ───
    HADITH_API_URL = os.environ.get("HADITH_API_URL")
    
    # ─── RUNTIME ───
    EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME", "").strip()
    UPLOAD_TARGET = os.environ.get("UPLOAD_TARGET", "drive_only").strip().lower()
    CONFIRM_UPLOAD = str(
        os.environ.get("CONFIRM_UPLOAD", "false")
    ).lower() == "true"
    
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
        """
        Manual mode mein tick mark lagaya?
        Auto mode mein always True.
        """
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
        """
        Facebook Story upload?
        
        Auto:     Always True
        Manual:   Only if confirmed AND target in (fb_ig, all)
        """
        if self.is_scheduled:
            return True
        if not self.is_confirmed:
            return False
        return self.UPLOAD_TARGET in ("fb_ig", "all")
    
    @property
    def should_upload_instagram(self) -> bool:
        """
        Instagram Story upload?
        
        Auto:     Always True
        Manual:   Only if confirmed AND target in (fb_ig, all)
        """
        if self.is_scheduled:
            return True
        if not self.is_confirmed:
            return False
        return self.UPLOAD_TARGET in ("fb_ig", "all")
    
    @property
    def should_upload_youtube(self) -> bool:
        """
        YouTube Shorts upload?
        
        Auto:     False (schedule mein skip — kyunki Story format hai)
        Manual:   Only if confirmed AND target in (youtube, all)
        """
        if self.is_scheduled:
            return False        # Auto mein YouTube skip
        if not self.is_confirmed:
            return False
        return self.UPLOAD_TARGET in ("youtube", "all")
    
    # ─────────────────────────────────────────────────────
    # 🎯 AVAILABLE PLATFORMS
    # ─────────────────────────────────────────────────────
    
    def available_platforms(self) -> list:
        """
        Which platforms have valid credentials?
        
        Returns:
            List like ["facebook", "instagram", "youtube"]
        """
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
    # 🎯 RUN CONTEXT — for logging
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
        """Full config summary — for logs/telegram."""
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
    summary = cfg.summary()
    
    print(f"\n📍 Run Context:")
    print(f"   Event:     {summary['event']}")
    print(f"   Mode:      {summary['mode']}")
    print(f"   Target:    {summary['target']}")
    print(f"   Confirmed: {summary['confirmed']}")
    
    print(f"\n🎯 Upload Decisions:")
    for platform, should in summary["should_upload"].items():
        icon = "✅" if should else "⏭️"
        print(f"   {icon} {platform}")
    
    print(f"\n🌐 Available Platforms:")
    for p in summary["available"]:
        print(f"   ✓ {p}")
    
    print(f"\n📖 Description: {cfg.describe()}")
