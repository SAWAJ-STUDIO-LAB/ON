"""
Universal Shared Modules — SawajStudioBot
==========================================

यह folder तीनों generators (Story, Short, Long) के common modules रखता है।
हर generator की existing file एक thin re-export wrapper है।

Files:
  U1_logger.py         → Print + Telegram logging
  U2_telegram.py       → Combined Telegram report
  U3_utils.py          → Sanitize helpers
  U4_base_pipeline.py  → HTTP session + trackers
  U5_fonts.py          → Multi-script font loader
  U6_ai_provider.py    → 10-provider AI fallback
  U7_tts.py            → 4-engine TTS fallback
  U8_drive.py          → Google Drive upload
  U9_mastering.py      → Voice mastering (tempo-configurable)
"""

__version__ = "2.0.0"
__all__ = [
    "U1_logger", "U2_telegram", "U3_utils", "U4_base_pipeline",
    "U5_fonts", "U6_ai_provider", "U7_tts", "U8_drive", "U9_mastering",
]
