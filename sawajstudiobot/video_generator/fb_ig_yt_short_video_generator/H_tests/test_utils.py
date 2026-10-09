import logging
from typing import Any, Dict, Optional, Tuple, Callable
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import json
from datetime import datetime
from video_generator.fb_ig_yt_short_video_generator.A_core import A2_logger, A6_print_logger

class TestConfigUtils:
    """Utility class for test configuration management"""

    @staticmethod
    def create_mock_config() -> Dict[str, Any]:
        """Create standardized mock configuration for testing"""
        return {
            "general": {
                "platform": "yt_short",
                "test_mode": True,
                "log_level": "DEBUG",
                "temp_dir": "/tmp/test_short_video",
                "output_dir": "/tmp/test_output_short",
                "api_keys": {
                    "hadith_api": "mock_api_key",
                    "tts_api": "mock_tts_key",
                    "ai_api": "mock_ai_key"
                },
                "media": {
                    "width": 1080,
                    "height": 1920,
                    "fps": 30,
                    "bitrate": "8M"
                },
                "audio": {
                    "volume": 0.8,
                    "ducking": True,
                    "sfx": {
                        "whoosh": "path/to/whoosh.wav",
                        "ding": "path/to/ding.wav"
                    }
                },
                "content": {
                    "hadith_count": 3,
                    "meaning_count": 2,
                    "bullet_style": "simple",
                    "font": "Noto Naskh Arabic",
                    "colors": {
                        "primary": "#FF5722",
                        "secondary": "#3F51B5",
                        "text": "#FFFFFF",
                        "bg": "#000000"
                    }
                },
                "upload": {
                    "auto_upload": False,
                    "platforms": ["youtube"]
                }
            },
            "pipeline": {
                "steps": [
                    "init",
                    "hadith",
                    "translate",
                    "meaning",
                    "tts",
                    "music",
                    "background",
                    "logo",
                    "frames",
                    "compose",
                    "thumbnail",
                    "drive",
                    "socials"
                ],
                "skip_steps": []
            },
            "testing": {
                "mock_hadiths": True,
                "mock_tts": True,
                "mock_ai": True,
                "mock_media": True,
                "test_duration": 15,
                "test_frames": 450
            }
        }

    @staticmethod
    def setup_test_environment(config: Dict[str, Any]) -> Tuple[Path, Path]:
        """Create temporary directories for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_path = temp_path / "output"

            # Create output directory
            output_path.mkdir(exist_ok=True)

            # Configure paths in config
            config["general"]["temp_dir"] = str(temp_path)
            config["general"]["output_dir"] = str(output_path)

            # Ensure directories exist
            A27_ensure_dir.ensure_dir_exists(temp_path)
            A27_ensure_dir.ensure_dir_exists(output_path)

            return temp_path, output_path

    @staticmethod
    def restore_original_env():
        """Restore environment variables after testing"""
        os.environ.pop("TEST_MODE", None)
        os.environ.pop("API_KEY_HADITH", None)
        os.environ.pop("API_KEY_TTS", None)
        os.environ.pop("API_KEY_AI", None)

    @staticmethod
    def mock_api_calls(api_tracker: A32_api_tracker.APITracker):
        """Mock API calls for testing"""
        with patch.object(api_tracker, 'track_api_call') as mock_track:
            mock_track.return_value = True
            return mock_track

    @staticmethod
    def setup_test_logging(config: Dict[str, Any]) -> logging.Logger:
        """Configure test logging"""
        log_level = getattr(logging, config["general"]["log_level"].upper())
        logger = A2_logger.get_logger(__name__)
        logger.setLevel(log_level)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add ch to logger
        logger.addHandler(ch)

        return logger

    @staticmethod
    def validate_config_structure(config: Dict[str, Any]) -> bool:
        """Validate test configuration structure"""
        required_sections = {
            "general", "pipeline", "testing",
            "content", "audio", "media", "upload"
        }

        if not all(section in config for section in required_sections):
            return False

        # Validate general section
        general_req = {"platform", "test_mode", "log_level", "temp_dir", "output_dir", "api_keys"}
        if not all(item in config["general"] for item in general_req):
            return False

        # Validate media section
        media_req = {"width", "height", "fps", "bitrate"}
        if not all(item in config["general"]["media"] for item in media_req):
            return False

        return True

    @staticmethod
    def generate_test_hadiths(count: int = 3) -> List[Dict[str, Any]]:
        """Generate mock hadith data for testing"""
        return [
            {
                "id": f"H{idx}",
                "arabic": f"الْحَدِيثُ {idx} في اللغة العربية",
                "english": f"This is hadith number {idx} in English",
                "source": f"Book {idx}",
                "reference": f"Chapter {idx}, Verse {idx}"
            }
            for idx in range(1, count+1)
        ]

    @staticmethod
    def generate_test_meanings(count: int = 2) -> List[Dict[str, Any]]:
        """Generate mock meaning translations for testing"""
        return [
            {
                "id": f"M{idx}",
                "arabic": f"التفسير {idx}",
                "english": f"Explanation {idx} in English",
                "hindi": f"व्याख्या {idx} में हिंदी"
            }
            for idx in range(1, count+1)
        ]

    @staticmethod
    def mock_file_system(config: Dict[str, Any]) -> None:
        """Mock file system operations for testing"""
        temp_dir = Path(config["general"]["temp_dir"])
        output_dir = Path(config["general"]["output_dir"])

        # Create test files
        (temp_dir / "test_hadith.json").write_text(json.dumps([]))
        (temp_dir / "test_meaning.json").write_text(json.dumps([]))
        (output_dir / "test_video.mp4").touch()
        (output_dir / "test_thumbnail.jpg").touch()
        (output_dir / "test_audio.mp3").touch()
