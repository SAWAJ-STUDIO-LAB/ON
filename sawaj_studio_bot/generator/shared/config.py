"""Configuration constants"""
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
META_TOKEN = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()

FPS = 25
INTRO_DUR = 1.5
OUTRO_DUR = 1.7
MUSIC_VOL = 0.20
VIDEO_W = 1080
VIDEO_H = 1920
