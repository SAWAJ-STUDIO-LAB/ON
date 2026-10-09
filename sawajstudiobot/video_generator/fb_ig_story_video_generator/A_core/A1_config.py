# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      A1_config.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                A_core/A1_config.py                       ║
# ║  🎯 PURPOSE:   Config — offline/online mode (STORY)      ║
# ║  📖 FOLDER:    A_core                                    ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   ⚙️  CONFIG MODULE (STORY)                              ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Upload Modes:                                       ║
║      • offline → Sirf Google Drive                       ║
║      • online  → Google Drive + Social Media             ║
║                                                          ║
║   🔐 Safety:                                             ║
║      • online mode → confirm_upload checkbox zaroori     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os


class Config:
    """Config — offline/online upload system (Story)."""

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
    YT_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
    YT_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
    YT_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    YT_PLAYLIST_ID = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID")

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
    HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

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
    EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME", "")
    UPLOAD_MODE = os.environ.get("UPLOAD_MODE", "offline").strip().lower()
    UPLOAD_CONFIRMED = str(
        os.environ.get("UPLOAD_CONFIRMED", "false")
    ).lower() == "true"

    # ═══════════════════════════════════════════════════════
    # LOGIC
    # ═══════════════════════════════════════════════════════

    @property
    def is_scheduled(self):
        """Cron-triggered?"""
        return self.EVENT_NAME == "schedule"

    @property
    def should_upload_drive(self):
        """Drive upload — always (both modes)."""
        return True

    @property
    def should_post_social(self):
        """
        • Schedule → always TRUE
        • Manual online + confirmed → TRUE
        • Manual online + NOT confirmed → FALSE
        • Manual offline → FALSE
        """
        if self.is_scheduled:
            return True
        if self.UPLOAD_MODE == "online":
            return self.UPLOAD_CONFIRMED
        return False

    def available_platforms(self):
        """Which platforms have credentials? (Story: FB + IG)"""
        available = []
        if self.META_TOKEN and self.PAGE_ID:
            available.append("facebook")
        if self.IG_TOKEN and self.IG_BUSINESS_ID:
            available.append("instagram")
        return available
