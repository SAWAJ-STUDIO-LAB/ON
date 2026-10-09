import re
from typing import Any, Dict, Optional
from jsonschema import validate, ValidationError
from jsonschema.exceptions import SchemaError

class ConfigValidator:
    """Schema validator for configuration files with fallback mechanisms"""

    _SCHEMA = {
        "type": "object",
        "properties": {
            "general": {
                "type": "object",
                "properties": {
                    "platform": {"type": "string", "enum": ["facebook", "instagram", "youtube"]},
                    "language": {"type": "string", "pattern": "^[a-z]{2}(?:_[A-Z]{2})?$"},
                    "output_dir": {"type": "string"},
                    "temp_dir": {"type": "string"},
                    "max_retries": {"type": "integer", "minimum": 0, "maximum": 10},
                    "timeout": {"type": "integer", "minimum": 1, "maximum": 300},
                    "debug": {"type": "boolean"},
                    "test_mode": {"type": "boolean"},
                    "api_keys": {
                        "type": "object",
                        "patternProperties": {
                            "^[A-Za-z0-9_]+$": {"type": "string"}
                        },
                        "additionalProperties": False
                    }
                },
                "required": ["platform", "language", "output_dir", "temp_dir"]
            },
            "content": {
                "type": "object",
                "properties": {
                    "hadith": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string"},
                            "count": {"type": "integer", "minimum": 1, "maximum": 50},
                            "fallback": {"type": "boolean"},
                            "books": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["source"]
                    },
                    "translation": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "provider": {"type": "string"},
                            "fallback": {"type": "boolean"}
                        }
                    },
                    "meaning": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "provider": {"type": "string"},
                            "fallback": {"type": "boolean"}
                        }
                    },
                    "tts": {
                        "type": "object",
                        "properties": {
                            "provider": {"type": "string"},
                            "voice": {"type": "string"},
                            "speed": {"type": "number", "minimum": 0.5, "maximum": 2.0},
                            "volume": {"type": "number", "minimum": 0.1, "maximum": 1.0}
                        },
                        "required": ["provider"]
                    },
                    "music": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "provider": {"type": "string"},
                            "style": {"type": "string"},
                            "duration": {"type": "integer", "minimum": 1, "maximum": 60}
                        }
                    },
                    "background": {
                        "type": "object",
                        "properties": {
                            "provider": {"type": "string"},
                            "style": {"type": "string"},
                            "color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                            "pattern": {"type": "string"}
                        }
                    }
                }
            },
            "graphics": {
                "type": "object",
                "properties": {
                    "logo": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "position": {"type": "string"},
                            "size": {"type": "number", "minimum": 10, "maximum": 200},
                            "opacity": {"type": "number", "minimum": 0.1, "maximum": 1.0}
                        }
                    },
                    "watermark": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "text": {"type": "string"},
                            "position": {"type": "string"},
                            "size": {"type": "number", "minimum": 10, "maximum": 100},
                            "color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"}
                        }
                    },
                    "bullets": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "style": {"type": "string"},
                            "color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                            "size": {"type": "number", "minimum": 10, "maximum": 50}
                        }
                    },
                    "progress": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "style": {"type": "string"},
                            "color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                            "thickness": {"type": "number", "minimum": 1, "maximum": 20}
                        }
                    }
                }
            },
            "video": {
                "type": "object",
                "properties": {
                    "fps": {"type": "integer", "minimum": 10, "maximum": 60},
                    "resolution": {
                        "type": "object",
                        "properties": {
                            "width": {"type": "integer", "minimum": 320, "maximum": 4096},
                            "height": {"type": "integer", "minimum": 320, "maximum": 4096}
                        },
                        "required": ["width", "height"]
                    },
                    "duration": {"type": "integer", "minimum": 1, "maximum": 60},
                    "transitions": {
                        "type": "object",
                        "properties": {
                            "style": {"type": "string"},
                            "duration": {"type": "integer", "minimum": 1, "maximum": 10}
                        }
                    },
                    "effects": {
                        "type": "object",
                        "properties": {
                            "sparkles": {"type": "boolean"},
                            "rays": {"type": "boolean"},
                            "vignette": {"type": "boolean"}
                        }
                    }
                },
                "required": ["fps", "resolution", "duration"]
            },
            "audio": {
                "type": "object",
                "properties": {
                    "volume": {"type": "number", "minimum": 0.1, "maximum": 1.0},
                    "balance": {"type": "number", "minimum": -1.0, "maximum": 1.0},
                    "effects": {
                        "type": "object",
                        "properties": {
                            "ducking": {"type": "boolean"},
                            "reverb": {"type": "boolean"}
                        }
                    }
                }
            },
            "upload": {
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean"},
                    "platform": {"type": "string"},
                    "schedule": {"type": "string"},
                    "caption": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "description": {"type": "string"}
                }
            }
        },
        "required": ["general", "content", "graphics", "video", "audio"]
    }

    @classmethod
    def validate_config(cls, config_data: Dict[str, Any], config_path: Optional[str] = None) -> Dict[str, Any]:
        """Validate configuration with comprehensive error handling"""
        try:
            validate(instance=config_data, schema=cls._SCHEMA)
            return cls._sanitize_config(config_data)
        except ValidationError as ve:
            error_msg = f"Configuration validation failed: {ve.message}"
            if config_path:
                error_msg += f"\nFile: {config_path}"
            raise ValueError(error_msg) from ve
        except SchemaError as se:
            raise ValueError(f"Invalid schema definition: {str(se)}") from se

    @classmethod
    def _sanitize_config(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize configuration values with fallback defaults"""
        sanitized = config.copy()

        # General section
        if "general" in sanitized:
            gen = sanitized["general"]
            if "max_retries" not in gen:
                gen["max_retries"] = 3
            if "timeout" not in gen:
                gen["timeout"] = 30
            if "debug" not in gen:
                gen["debug"] = False
            if "test_mode" not in gen:
                gen["test_mode"] = False

            # Ensure paths exist
            for path_key in ["output_dir", "temp_dir"]:
                if path_key in gen and not os.path.exists(gen[path_key]):
                    warnings.warn(f"Directory {gen[path_key]} doesn't exist. Creating...")
                    os.makedirs(gen[path_key], exist_ok=True)

        # Content section
        if "content" in sanitized:
            content = sanitized["content"]

            # Hadith defaults
            if "hadith" in content:
                hadith = content["hadith"]
                if "count" not in hadith:
                    hadith["count"] = 3
                if "fallback" not in hadith:
                    hadith["fallback"] = True
                if "books" not in hadith:
                    hadith["books"] = ["Sahih Bukhari", "Sahih Muslim"]

            # Translation defaults
            if "translation" not in content:
                content["translation"] = {"enabled": False, "provider": "deepl", "fallback": True}

            # Meaning defaults
            if "meaning" not in content:
                content["meaning"] = {"enabled": False, "provider": "openrouter", "fallback": True}

            # TTS defaults
            if "tts" in content:
                tts = content["tts"]
                if "speed" not in tts:
                    tts["speed"] = 1.0
                if "volume" not in tts:
                    tts["volume"] = 0.8

            # Music defaults
            if "music" in content:
                music = content["music"]
                if "style" not in music:
                    music["style"] = "islamic"
                if "duration" not in music:
                    music["duration"] = 15

        # Graphics section
        if "graphics" in sanitized:
            graphics = sanitized["graphics"]

            # Logo defaults
            if "logo" in graphics:
                logo = graphics["logo"]
                if "position" not in logo:
                    logo["position"] = "top_right"
                if "size" not in logo:
                    logo["size"] = 100
                if "opacity" not in logo:
                    logo["opacity"] = 0.9

            # Watermark defaults
            if "watermark" in graphics:
                watermark = graphics["watermark"]
                if "enabled" not in watermark:
                    watermark["enabled"] = True
                if "position" not in watermark:
                    watermark["position"] = "bottom_right"
                if "size" not in watermark:
                    watermark["size"] = 30
                if "color" not in watermark:
                    watermark["color"] = "#FFFFFF"

            # Bullets defaults
            if "bullets" in graphics:
                bullets = graphics["bullets"]
                if "enabled" not in bullets:
                    bullets["enabled"] = True
                if "style" not in bullets:
                    bullets["style"] = "arabic"
                if "color" not in bullets:
                    bullets["color"] = "#FFD700"
                if "size" not in bullets:
                    bullets["size"] = 20

            # Progress defaults
            if "progress" in graphics:
                progress = graphics["progress"]
                if "enabled" not in progress:
                    progress["enabled"] = True
                if "style" not in progress:
                    progress["style"] = "gradient"
                if "color" not in progress:
                    progress["color"] = "#FF0000"
                if "thickness" not in progress:
                    progress["thickness"] = 5

        # Video section
        if "video" in sanitized:
            video = sanitized["video"]

            # Resolution defaults
            if "resolution" in video:
                res = video["resolution"]
                if "width" not in res or "height" not in res:
                    # Default to 1080p for short videos
                    res["width"] = 1080
                    res["height"] = 1920

            # Duration defaults
            if "duration" not in video:
                video["duration"] = 15

            # Effects defaults
            if "effects" not in video:
                video["effects"] = {
                    "sparkles": True,
                    "rays": False,
                    "vignette": True
                }

        # Audio section
        if "audio" in sanitized:
            audio = sanitized["audio"]

            # Effects defaults
            if "effects" not in audio:
                audio["effects"] = {
                    "ducking": True,
                    "reverb": False
                }

        return sanitized

    @classmethod
    def load_config(cls, config_path: str) -> Dict[str, Any]:
        """Load and validate configuration from file with multiple format support"""
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        try:
            if config_path.suffix.lower() == '.json':
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            elif config_path.suffix.lower() in ('.yaml', '.yml'):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported config file format: {config_path.suffix}")

            return cls.validate_config(config_data, str(config_path))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {str(e)}") from e
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {str(e)}") from e
        except Exception as e:
            raise ValueError(f"Error loading config file: {str(e)}") from e

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """Return fully configured default settings"""
        return {
            "general": {
                "platform": "youtube",
                "language": "en_US",
                "output_dir": "./output",
                "temp_dir": "./temp",
                "max_retries": 3,
                "timeout": 30,
                "debug": False,
                "test_mode": False,
                "api_keys": {}
            },
            "content": {
                "hadith": {
                    "source": "sahih_bukhari",
                    "count": 3,
                    "fallback": True,
                    "books": ["Sahih Bukhari", "Sahih Muslim"]
                },
                "translation": {
                    "enabled": True,
                    "provider": "deepl",
                    "fallback": True
                },
                "meaning": {
                    "enabled": True,
                    "provider": "openrouter",
                    "fallback": True
                },
                "tts": {
                    "provider": "elevenlabs",
                    "voice": "Arabic Female",
                    "speed": 1.0,
                    "volume": 0.8
                },
                "music": {
                    "enabled": True,
                    "provider": "freesound",
                    "style": "islamic",
                    "duration": 15
                },
                "background": {
                    "provider": "pexels",
                    "style": "islamic",
                    "color": "#000000",
                    "pattern": None
                }
            },
            "graphics": {
                "logo": {
                    "path": "./assets/logo.png",
                    "position": "top_right",
                    "size": 100,
                    "opacity": 0.9
                },
                "watermark": {
                    "enabled": True,
                    "text": "© SawajStudioBot",
                    "position": "bottom_right",
                    "size": 30,
                    "color": "#FFFFFF"
                },
                "bullets": {
                    "enabled": True,
                    "style": "arabic",
                    "color": "#FFD700",
                    "size": 20
                },
                "progress": {
                    "enabled": True,
                    "style": "gradient",
                    "color": "#FF0000",
                    "thickness": 5
                }
            },
            "video": {
                "fps": 30,
                "resolution": {
                    "width": 1080,
                    "height": 1920
                },
                "duration": 15,
                "transitions": {
                    "style": "fade",
                    "duration": 2
                },
                "effects": {
                    "sparkles": True,
                    "rays": False,
                    "vignette": True
                }
            },
            "audio": {
                "volume": 0.8,
                "balance": 0.0,
                "effects": {
                    "ducking": True,
                    "reverb": False
                }
            },
            "upload": {
                "enabled": True,
                "platform": "youtube",
                "schedule": None,
                "caption": "Islamic Hadith with Meaning",
                "tags": ["Islam", "Hadith", "Quran", "IslamicTeachings"],
                "description": "Daily Islamic Hadith with translation and meaning for spiritual growth"
            }
        }
