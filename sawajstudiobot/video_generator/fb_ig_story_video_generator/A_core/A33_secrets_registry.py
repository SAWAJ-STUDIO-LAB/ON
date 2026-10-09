"""
Secrets Registry Module
=======================
Centralized management of sensitive configuration values with encryption support.
"""

import os
import logging
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
import base64
import hashlib
from cryptography.fernet import Fernet
import json
from pathlib import Path
import warnings

logger = logging.getLogger(__name__)

@dataclass
class SecretsRegistry:
    """
    Central registry for managing sensitive configuration values with encryption.
    Supports both encrypted storage and direct environment variable access.
    """

    config_path: Path = Path("secrets.json")
    encryption_key: Optional[str] = None
    _cipher: Optional[Fernet] = None
    _loaded: bool = False

    def __post_init__(self):
        """Initialize the secrets registry."""
        if not self.encryption_key:
            self._generate_encryption_key()

        try:
            self._cipher = Fernet(self.encryption_key.encode())
            self._load_secrets()
            self._loaded = True
            logger.info("Secrets registry initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize secrets registry: {str(e)}")
            raise

    def _generate_encryption_key(self) -> None:
        """Generate a new encryption key if none exists."""
        if not self.encryption_key:
            self.encryption_key = self._generate_key()
            logger.warning("No encryption key found. Generated new one. "
                          "Consider backing up this key securely.")

    @staticmethod
    def _generate_key() -> str:
        """Generate a secure encryption key."""
        return base64.urlsafe_b64encode(
            hashlib.sha256(os.urandom(60)).digest()
        ).decode()

    def _load_secrets(self) -> None:
        """Load secrets from JSON file if exists."""
        if not self.config_path.exists():
            return

        try:
            with open(self.config_path) as f:
                secrets_data = json.load(f)

            self._decrypt_secrets(secrets_data)
        except Exception as e:
            logger.warning(f"Failed to load encrypted secrets: {str(e)}")
            # Fallback to unencrypted if encryption fails
            try:
                with open(self.config_path) as f:
                    self._secrets = json.load(f)
                logger.info("Loaded secrets without decryption (fallback)")
            except Exception as e:
                logger.error(f"Failed to load secrets: {str(e)}")
                raise

    def _decrypt_secrets(self, secrets_data: Dict[str, Any]) -> None:
        """Decrypt secrets if they were encrypted."""
        decrypted = {}
        for key, value in secrets_data.items():
            if isinstance(value, str) and value.startswith("encrypted:"):
                try:
                    decrypted[key] = self._cipher.decrypt(value[10:].encode()).decode()
                except:
                    decrypted[key] = value
            else:
                decrypted[key] = value
        self._secrets = decrypted

    def _encrypt_value(self, value: str) -> str:
        """Encrypt a sensitive value."""
        if not self._cipher:
            raise ValueError("Encryption not initialized")
        return f"encrypted:{base64.urlsafe_b64encode(self._cipher.encrypt(value.encode())).decode()}"

    def _should_encrypt(self, value: str) -> bool:
        """Determine if a value should be encrypted."""
        return bool(value.strip()) and not any(
            x in value.lower() for x in ["key:", "token:", "secret:", "password:", "api_key:"]
        )

    def save(self) -> None:
        """Save current secrets to file with encryption."""
        if not self._secrets:
            return

        try:
            encrypted_secrets = {}
            for key, value in self._secrets.items():
                if self._should_encrypt(value):
                    encrypted_secrets[key] = self._encrypt_value(value)
                else:
                    encrypted_secrets[key] = value

            with open(self.config_path, 'w') as f:
                json.dump(encrypted_secrets, f, indent=2)

            logger.info(f"Secrets saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save secrets: {str(e)}")
            raise

    def get(self, key: str, default: Optional[str] = None) -> str:
        """
        Get a secret value by key.

        Args:
            key: Secret key to retrieve
            default: Default value if key not found

        Returns:
            Secret value or default if not found
        """
        if not self._loaded:
            self._load_secrets()

        return self._secrets.get(key, default)

    def set(self, key: str, value: str) -> None:
        """
        Set a secret value.

        Args:
            key: Secret key to set
            value: Secret value to store
        """
        if not self._loaded:
            self._load_secrets()

        self._secrets[key] = value
        self.save()

    def has(self, key: str) -> bool:
        """Check if a secret key exists."""
        if not self._loaded:
            self._load_secrets()

        return key in self._secrets

    def clear(self) -> None:
        """Clear all secrets."""
        self._secrets = {}
        self.save()

    def __contains__(self, key: str) -> bool:
        """Check if key exists in secrets."""
        return self.has(key)

    def __getitem__(self, key: str) -> str:
        """Get secret value using dict-style access."""
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> None:
        """Set secret value using dict-style access."""
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        """Delete secret value."""
        if self.has(key):
            del self._secrets[key]
            self.save()

    def keys(self) -> list:
        """Get all secret keys."""
        if not self._loaded:
            self._load_secrets()
        return list(self._secrets.keys())

    def items(self) -> list:
        """Get all secret key-value pairs."""
        if not self._loaded:
            self._load_secrets()
        return list(self._secrets.items())

    def __len__(self) -> int:
        """Get number of secrets stored."""
        if not self._loaded:
            self._load_secrets()
        return len(self._secrets)

    def export_environment(self) -> Dict[str, str]:
        """
        Export secrets to environment variables dictionary.

        Returns:
            Dictionary of environment variable names and values
        """
        env_vars = {}
        for key, value in self._secrets.items():
            # Convert secret key to environment variable name
            env_name = key.upper().replace("_", "_")
            env_vars[env_name] = value
        return env_vars

    def import_from_environment(self, env_vars: Dict[str, str]) -> None:
        """
        Import secrets from environment variables.

        Args:
            env_vars: Dictionary of environment variable names and values
        """
        for env_name, value in env_vars.items():
            # Convert environment variable name to secret key
            key = env_name.lower().replace("_", "_")
            self.set(key, value)

    def generate_encryption_key(self) -> str:
        """Generate and return a new encryption key."""
        key = self._generate_key()
        logger.warning(f"Generated new encryption key: {key[:8]}... (keep this secure)")
        return key

    def verify_encryption(self) -> bool:
        """
        Verify encryption is working properly.

        Returns:
            True if encryption verification passed, False otherwise
        """
        if not self._cipher:
            return False

        try:
            test_value = "test_encryption_value"
            encrypted = self._encrypt_value(test_value)
            decrypted = self._cipher.decrypt(encrypted[10:].encode()).decode()
            return decrypted == test_value
        except:
            return False

# Initialize global secrets registry
secrets_registry = SecretsRegistry()

if __name__ == "__main__":
    try:
        # Test basic functionality
        secrets_registry.set("test_secret", "test_value")
        print(f"Set test_secret: {secrets_registry.get('test_secret')}")

        # Test encryption
        secrets_registry.set("encrypted_test", "this should be encrypted")
        print(f"Encrypted test exists: {secrets_registry.has('encrypted_test')}")

        # Test environment export
        env_vars = secrets_registry.export_environment()
        print(f"Exported {len(env_vars)} environment variables")

        # Test verification
        print(f"Encryption working: {secrets_registry.verify_encryption()}")

    except Exception as e:
        print(f"Test failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
