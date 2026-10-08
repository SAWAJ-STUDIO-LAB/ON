"""
A33_secrets_registry.py
Sirf secrets registry dict.
"""

SECRETS_REGISTRY = {
    "telegram": {
        "label": "📱 Telegram", "required": True,
        "secrets": {
            "TELEGRAM_BOT_TOKEN": {"label": "Bot Token", "names": ["TELEGRAM_BOT_TOKEN"]},
            "TELEGRAM_CHAT_ID": {"label": "Chat ID", "names": ["TELEGRAM_CHAT_ID"]},
        },
    },
    "facebook": {
        "label": "📘 Facebook", "required": True,
        "secrets": {
            "FACEBOOK_META_TOKEN": {"label": "Meta Token",
                "names": ["FACEBOOK_META_TOKEN", "FACEBOOK_INSTAGRAM_META_TOKEN"]},
            "FACEBOOK_PAGE_ID": {"label": "Page ID", "names": ["FACEBOOK_PAGE_ID"]},
        },
    },
    "instagram": {
        "label": "📸 Instagram", "required": True,
        "secrets": {
            "FACEBOOK_INSTAGRAM_META_TOKEN": {"label": "IG Token",
                "names": ["FACEBOOK_INSTAGRAM_META_TOKEN", "FACEBOOK_META_TOKEN"]},
            "INSTAGRAM_BUSINESS_ACCOUNT_ID": {"label": "IG Business ID",
                "names": ["INSTAGRAM_BUSINESS_ACCOUNT_ID"]},
        },
    },
    "youtube": {
        "label": "📺 YouTube", "required": False,
        "secrets": {
            "YOUTUBE_CLIENT_ID": {"label": "Client ID", "names": ["YOUTUBE_CLIENT_ID"]},
            "YOUTUBE_CLIENT_SECRET": {"label": "Client Secret", "names": ["YOUTUBE_CLIENT_SECRET"]},
            "YOUTUBE_REFRESH_TOKEN": {"label": "Refresh Token", "names": ["YOUTUBE_REFRESH_TOKEN"]},
        },
    },
    "drive": {
        "label": "☁️ Google Drive", "required": True,
        "secrets": {
            "GOOGLE_DRIVE_CLIENT_ID": {"label": "Client ID", "names": ["GOOGLE_DRIVE_CLIENT_ID"]},
            "GOOGLE_DRIVE_CLIENT_SECRET": {"label": "Client Secret", "names": ["GOOGLE_DRIVE_CLIENT_SECRET"]},
            "GOOGLE_DRIVE_REFRESH_TOKEN": {"label": "Refresh Token", "names": ["GOOGLE_DRIVE_REFRESH_TOKEN"]},
            "GDRIVE_STORY_VIDEO_FOLDER_ID": {"label": "Folder ID",
                "names": ["GDRIVE_STORY_VIDEO_FOLDER_ID", "GDRIVE_SHORT_VIDEO_FOLDER_ID"]},
        },
    },
    "ai_providers": {
        "label": "🤖 AI", "required": False, "min_required": 1,
        "secrets": {
            "OPENROUTER_API_KEY": {"label": "OpenRouter",
                "names": ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_AI"]},
            "GROQ_API_KEY": {"label": "Groq", "names": ["GROQ_API_KEY", "GROQ_API_KEY_AI"]},
            "GEMINI_API_KEY": {"label": "Gemini", "names": ["GEMINI_API_KEY", "GEMINI_API_KEY_AI"]},
            "MISTRAL_API_KEY": {"label": "Mistral", "names": ["MISTRAL_API_KEY", "MISTRAL_API_KEY_AI"]},
            "CEREBRAS_API_KEY": {"label": "Cerebras",
                "names": ["CEREBRAS_API_KEY", "CEREBRAS_API_KEY_AI", "CELEBRAS_API_KEY_AI"]},
            "COHERE_API_KEY": {"label": "Cohere", "names": ["COHERE_API_KEY", "COHERE_API_KEY_AI"]},
        },
    },
    "media": {
        "label": "🎬 Media", "required": False, "min_required": 1,
        "secrets": {
            "PEXELS_API_KEY": {"label": "Pexels", "names": ["PEXELS_API_KEY"]},
            "PIXABAY_API_KEY": {"label": "Pixabay", "names": ["PIXABAY_API_KEY"]},
            "FREESOUND_API_KEY": {"label": "Freesound", "names": ["FREESOUND_API_KEY"]},
        },
    },
    "tts": {
        "label": "🎙️ TTS", "required": False,
        "secrets": {
            "ELEVENLABS_API_KEY": {"label": "ElevenLabs", "names": ["ELEVENLABS_API_KEY"]},
            "DEEPL_API_KEY": {"label": "DeepL", "names": ["DEEPL_API_KEY"]},
        },
    },
}
