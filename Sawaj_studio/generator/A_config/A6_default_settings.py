# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A6_default_settings.py
# 🎯 PURPOSE:   Saare default settings ek jagah
# ═══════════════════════════════════════════════════════════

"""
⚙️ DEFAULT SETTINGS
════════════════════

🎯 Purpose:
   Saare constants yahan.
"""

# ═══════════════════════════════════════════════════════════
# ① VIDEO
# ═══════════════════════════════════════════════════════════

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 25
VIDEO_CODEC = "libx264"
VIDEO_CRF = 20
VIDEO_PRESET = "veryfast"

LONG_VIDEO_WIDTH = 1920
LONG_VIDEO_HEIGHT = 1080

# ═══════════════════════════════════════════════════════════
# ② AUDIO
# ═══════════════════════════════════════════════════════════

AUDIO_VOICE = "hi-IN-MadhurNeural"
AUDIO_RATE = "-7%"
AUDIO_PITCH = "-2Hz"
AUDIO_VOLUME = "+8%"

MUSIC_VOL_STORY = 0.20
MUSIC_VOL_SHORT = 0.22
MUSIC_VOL_LONG = 0.18

# ═══════════════════════════════════════════════════════════
# ③ DURATION
# ═══════════════════════════════════════════════════════════

STORY_INTRO_DUR = 2.0
STORY_OUTRO_DUR = 2.0

SHORT_INTRO_DUR = 2.0
SHORT_OUTRO_DUR = 2.0

LONG_INTRO_DUR = 3.0
LONG_OUTRO_DUR = 3.0

# ═══════════════════════════════════════════════════════════
# ④ HADITH WORDS
# ═══════════════════════════════════════════════════════════

STORY_WORDS_MIN = 50
STORY_WORDS_MAX = 100

SHORT_WORDS_MIN = 150
SHORT_WORDS_MAX = 400

LONG_WORDS_MIN = 400
LONG_WORDS_MAX = 1800

# ═══════════════════════════════════════════════════════════
# ⑤ MUSIC DURATION
# ═══════════════════════════════════════════════════════════

STORY_MUSIC_DUR = 60
SHORT_MUSIC_DUR = 200
LONG_MUSIC_DUR = 900

# ═══════════════════════════════════════════════════════════
# ⑥ TIMEOUTS
# ═══════════════════════════════════════════════════════════

HTTP_TIMEOUT = 30
TTS_TIMEOUT = 120
UPLOAD_TIMEOUT = 3600
FFMPEG_TIMEOUT = 1800

# ═══════════════════════════════════════════════════════════
# ⑦ RETRY
# ═══════════════════════════════════════════════════════════

MAX_RETRIES = 5
BACKOFF_FACTOR = 1.5
