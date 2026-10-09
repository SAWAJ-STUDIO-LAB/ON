import sys
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from unittest import TestCase
from importlib import import_module
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_config.log', mode='w')
    ]
)
logger = logging.getLogger('TestConfigLogger')

class ConfigTestCase(TestCase):
    """Comprehensive test case for Config class with deep validation and error handling."""

    @contextmanager
    def _safe_import(self, module_name: str) -> Optional[Any]:
        """Safe import context manager with error handling."""
        try:
            module = import_module(module_name)
            logger.info(f"Successfully imported module: {module_name}")
            yield module
        except ImportError as e:
            logger.error(f"ImportError in {module_name}: {str(e)}")
            yield None
        except Exception as e:
            logger.error(f"Unexpected error importing {module_name}: {str(e)}", exc_info=True)
            yield None

    def _validate_config_class(self, config_class: Any) -> bool:
        """Validate Config class structure and attributes."""
        if not config_class:
            return False

        required_attrs = {
            'config': dict,
            'platform': str,
            'version': str,
            'api_keys': dict,
            'secrets': dict,
            'settings': dict,
            'validate': bool,
            'load': callable,
            'save': callable,
            'get': callable,
            'set': callable
        }

        for attr, expected_type in required_attrs.items():
            if not hasattr(config_class, attr):
                logger.error(f"Missing required attribute: {attr}")
                return False

            attr_value = getattr(config_class, attr)
            if not isinstance(attr_value, expected_type):
                logger.error(f"Invalid type for {attr}: expected {expected_type}, got {type(attr_value)}")
                return False

        return True

    def test_config_import(self) -> None:
        """Test Config class import with comprehensive validation."""
        try:
            # Test import with path resolution
            config_path = Path(__file__).parent.parent / 'A_core' / 'A3_config_class.py'
            module_name = f"video_generator.fb_ig_story_video_generator.A_core.A3_config_class"

            with self._safe_import(module_name) as config_module:
                if not config_module:
                    raise ImportError("Config module import failed")

                Config = config_module.Config
                self.assertIsNotNone(Config, "Config class not found in module")

                # Validate Config class structure
                if not self._validate_config_class(Config):
                    raise AssertionError("Config class validation failed")

                # Test basic functionality
                config = Config()
                self.assertIsInstance(config.config, dict, "Config initialization failed")
                self.assertTrue(config.validate(), "Config validation failed")

                logger.info("All Config tests passed successfully")
                self.assertTrue(True, "Config import and validation successful")

        except Exception as e:
            logger.error(f"Test failed: {str(e)}", exc_info=True)
            self.fail(f"Config test failed: {str(e)}")

    def test_config_environment_validation(self) -> None:
        """Test environment variable validation."""
        try:
            from A_core.A34_secrets_env_check import check_environment
            from A_core.A33_secrets_registry import SecretsRegistry

            # Test environment check
            env_status = check_environment()
            self.assertTrue(env_status, "Environment validation failed")

            # Test secrets registry
            secrets = SecretsRegistry()
            self.assertIsInstance(secrets.get('FB_ACCESS_TOKEN'), str, "Secrets registry test failed")

        except Exception as e:
            logger.error(f"Environment validation test failed: {str(e)}", exc_info=True)
            self.fail(f"Environment validation test failed: {str(e)}")

if __name__ == '__main__':
    # Run tests with comprehensive logging
    logger.info("Starting Config Test Suite")
    test_suite = ConfigTestCase('ConfigTestSuite')
    test_suite.test_config_import()
    test_suite.test_config_environment_validation()
    logger.info("Config Test Suite completed")
