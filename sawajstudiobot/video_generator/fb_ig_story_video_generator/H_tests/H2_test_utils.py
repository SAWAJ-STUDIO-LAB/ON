import logging
from typing import Any, Dict, Optional, Callable, TypeVar
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
import os

logger = logging.getLogger('TestUtilsLogger')

T = TypeVar('T')

class TestUtils:
    """Utility functions for comprehensive testing."""

    @staticmethod
    def load_test_config(config_path: str = None) -> Dict[str, Any]:
        """Load test configuration with fallback to default."""
        try:
            if not config_path:
                config_path = Path(__file__).parent.parent / 'A_core' / 'A1_config.py'

            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Successfully loaded test config from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Failed to load test config: {str(e)}")
            return {}

    @staticmethod
    def mock_api_call(api_func: Callable, mock_response: Any) -> Any:
        """Mock API call for testing."""
        with patch(api_func.__module__ + '.' + api_func.__name__) as mock:
            mock.return_value = mock_response
            return mock

    @staticmethod
    def validate_config_structure(config: Dict[str, Any]) -> bool:
        """Validate config structure against expected schema."""
        required_sections = {
            'platform': str,
            'version': str,
            'api_keys': dict,
            'secrets': dict,
            'settings': dict
        }

        for section, expected_type in required_sections.items():
            if section not in config:
                logger.error(f"Missing required config section: {section}")
                return False

            if not isinstance(config[section], expected_type):
                logger.error(f"Invalid type for {section}: expected {expected_type}, got {type(config[section])}")
                return False

        return True

    @staticmethod
    def create_temp_dir() -> Path:
        """Create temporary directory for testing."""
        try:
            temp_dir = Path(os.getenv('TEMP', '/tmp')) / 'sawaj_test'
            temp_dir.mkdir(exist_ok=True)
            logger.info(f"Created temp directory: {temp_dir}")
            return temp_dir
        except Exception as e:
            logger.error(f"Failed to create temp directory: {str(e)}")
            return Path('/')

    @staticmethod
    def cleanup_temp_dir(temp_dir: Path) -> None:
        """Clean up temporary directory."""
        try:
            for item in temp_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    import shutil
                    shutil.rmtree(item)
            logger.info(f"Cleaned up temp directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Failed to clean up temp directory: {str(e)}")

    @staticmethod
    def patch_all_dependencies(func: Callable) -> Callable:
        """Decorator to patch all dependencies of a function."""
        def wrapper(*args, **kwargs):
            try:
                # Get all imported modules in the function
                import inspect
                source = inspect.getsource(func)
                imports = [line for line in source.split('\n') if line.strip().startswith(('import ', 'from '))]

                for imp in imports:
                    if 'import ' in imp:
                        module = imp.split('import ')[1].split(',')[0].strip()
                        TestUtils.mock_api_call(getattr(__import__(module, fromlist=[True]), module)
                    else:
                        parts = imp.split('from ')[1].split(' import ')
                        module = parts[0].strip()
                        attr = parts[1].split(',')[0].strip()
                        TestUtils.mock_api_call(getattr(__import__(module, fromlist=[True]), attr)

                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Dependency patching failed: {str(e)}")
                raise
        return wrapper
