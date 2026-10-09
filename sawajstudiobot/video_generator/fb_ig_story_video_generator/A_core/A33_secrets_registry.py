"""
Secrets Registry Module
=======================
Centralized management of sensitive configuration values with encryption support.

This module provides a secure way to manage and store sensitive configuration values,
such as API keys, passwords, or any other secrets required by the application. It uses
encryption to protect the data and supports both encrypted storage and direct environment
variable access.
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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SecretsRegistry:
    """
    Central registry for managing sensitive configuration values with encryption.

    This class provides a secure way to store and retrieve sensitive configuration values.
    It supports encryption using Fernet symmetric encryption and can also load secrets
    directly from environment variables.

    Attributes:
        config_path (Path): Path to the JSON file where secrets are stored.
        encryption_key (Optional[str]): Encryption key used for Fernet encryption.
        _cipher (Optional[Fernet]): Fernet cipher object for encryption/decryption.
        _loaded (bool): Flag indicating if the secrets have been loaded.

    Methods:
        __post_init__(): Initializes the secrets registry and sets up encryption.
        _generate_encryption_key(): Generates a new encryption key if none is provided.
        _generate_key(): Generates a secure encryption key.
        _load_secrets(): Loads secrets from the JSON file.
        _decrypt_secrets(): Decrypts the loaded secrets.
        _encrypt_value(): Encrypts a sensitive value.
        _should_encrypt(): Checks if a value should be encrypted.
        save(): Saves the current secrets to the JSON file with encryption.
        get(key, default): Retrieves a secret value by key.
        set(key, value): Sets a secret value.
        has(key): Checks if a secret key exists.
        clear(): Clears all secrets.
        __contains__(key): Checks if a key exists in the secrets.
        __getitem__(key): Retrieves a secret value using dict-style access.
        __setitem__(key, value): Sets a secret value using dict-style access.
        __delitem__(key): Deletes a secret value.
        keys(): Returns all secret keys.
        items(): Returns all secret key-value pairs.
        __len__(): Returns the number of secrets stored.
        export_environment(): Exports secrets to environment variables dictionary.
        import_from_environment(env_vars): Imports secrets from environment variables.
        generate_encryption_key(): Generates and returns a new encryption key.
        verify_encryption(): Verifies that encryption is working properly.
    """

    config_path: Path = Path("secrets.json")
    encryption_key: Optional[str] = None
    _cipher: Optional[Fernet] = None
    _loaded: bool = False

    def __post_init__(self):
        """Initialize the secrets registry and set up encryption."""
        try:
            # Generate encryption key if not provided
            if not self.encryption_key:
                self._generate_encryption_key()

            # Initialize Fernet cipher with the encryption key
            self._cipher = Fernet(self.encryption_key.encode())
            self._loaded = True
            logger.info("Secrets registry initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize secrets registry: {e}")
            raise

    def _generate_encryption_key(self) -> None:
        """Generate a new encryption key if none exists."""
        if not self.encryption_key:
            self.encryption_key = self._generate_key()
            logger.warning("No encryption key found. Generated a new one. "
                          "Please back up this key securely.")

    @staticmethod
    def _generate_key() -> str:
        """Generate a secure encryption key using random data and SHA-256 hashing."""
        random_data = os.urandom(60)
        hashed_data = hashlib.sha256(random_data).digest()
        encoded_key = base64.urlsafe_b64encode(hashed_data).decode()
        return encoded_key

    def _load_secrets(self) -> None:
        """Load secrets from the JSON file if it exists."""
        if not self.config_path.exists():
            logger.warning(f"Secrets file '{self.config_path}' does not exist.")
            return

        try:
            with open(self.config_path, "r") as f:
                secrets_data = json.load(f)

            # Attempt to decrypt the loaded secrets
            self._decrypt_secrets(secrets_data)
        except FileNotFoundError:
            logger.error(f"Secrets file '{self.config_path}' not found.")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse secrets file '{self.config_path}': {e}")
        except Exception as e:
            logger.error(f"Failed to load secrets from '{self.config_path}': {e}")
            raise

    def _decrypt_secrets(self, secrets_data: Dict[str, Any]) -> None:
        """Decrypt the loaded secrets data."""
        decrypted_secrets = {}
        for key, value in secrets_data.items():
            try:
                # Attempt to decrypt the value
                decrypted_value = self._cipher.decrypt(value.encode()).decode()
            except Exception as e:
                logger.warning(f"Failed to decrypt value for key '{key}': {e}")
                decrypted_value = value

            decrypted_secrets[key] = decrypted_value

        self._secrets = decrypted_secrets

    def _encrypt_value(self, value: str) -> str:
        """Encrypt a sensitive value using Fernet encryption."""
        if not self._cipher:
            raise ValueError("Encryption not initialized. Please ensure an encryption key is set.")

        encrypted_value = self._cipher.encrypt(value.encode()).decode()
        return encrypted_value

    def _should_encrypt(self, value: str) -> bool:
        """Determine if a value should be encrypted based on its content."""
        return bool(value.strip()) and not any(
            sensitive_word in value.lower()
            for sensitive_word in ["key:", "token:", "secret:", "password:", "api_key:"]
        )

    def save(self) -> None:
        """Save the current secrets to the JSON file with encryption."""
        if not self._secrets:
            logger.warning("No secrets to save.")
            return

        try:
            encrypted_secrets = {}
            for key, value in self._secrets.items():
                if self._should_encrypt(value):
                    encrypted_secrets[key] = self._encrypt_value(value)
                else:
                    encrypted_secrets[key] = value

            with open(self.config_path, "w") as f:
                json.dump(encrypted_secrets, f, indent=2)

            logger.info(f"Secrets saved to {self.config_path}")
        except FileNotFoundError:
            logger.error(f"Failed to save secrets. File '{self.config_path}' not found.")
        except Exception as e:
            logger.error(f"Failed to save secrets to '{self.config_path}': {e}")
            raise

    def get(self, key: str, default: Optional[str] = None) -> str:
        """
        Get a secret value by key.

        Args:
            key (str): Secret key to retrieve.
            default (Optional[str]): Default value to return if the key is not found.

        Returns:
            str: Secret value or the default value if not found.
        """
        if not self._loaded:
            self._load_secrets()

        return self._secrets.get(key, default)

    def set(self, key: str, value: str) -> None:
        """
        Set a secret value.

        Args:
            key (str): Secret key to set.
            value (str): Secret value to store.
        """
        if not self._loaded:
            self._load_secrets()

        self._secrets[key] = value
        self.save()

    def has(self, key: str) -> bool:
        """
        Check if a secret key exists.

        Args:
            key (str): Secret key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        if not self._loaded:
            self._load_secrets()

        return key in self._secrets

    def clear(self) -> None:
        """Clear all secrets."""
        self._secrets = {}
        self.save()

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the secrets."""
        return self.has(key)

    def __getitem__(self, key: str) -> str:
        """Get secret value using dict-style access."""
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> None:
        """Set secret value using dict-style access."""
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        """Delete a secret value."""
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
        """Get the number of secrets stored."""
        if not self._loaded:
            self._load_secrets()
        return len(self._secrets)

    def export_environment(self) -> Dict[str, str]:
        """
        Export secrets to environment variables dictionary.

        Returns:
            Dict[str, str]: Dictionary of environment variable names and values.
        """
        env_vars = {}
        for key, value in self._secrets.items():
            env_name = key.upper().replace("_", "_").replace("-", "_")
            env_vars[env_name] = value
        return env_vars

    def import_from_environment(self, env_vars: Dict[str, str]) -> None:
        """
        Import secrets from environment variables.

        Args:
            env_vars (Dict[str, str]): Dictionary of environment variable names and values.
        """
        for env_name, value in env_vars.items():
            key = env_name.lower().replace("_", "_").replace("-", "_")
            self.set(key, value)

    def generate_encryption_key(self) -> str:
        """
        Generate and return a new encryption key.

        Returns:
            str: New encryption key.
        """
        new_key = self._generate_key()
        logger.warning(f"Generated new encryption key: {new_key[:8]}... (keep this secure)")
        return new_key

    def verify_encryption(self) -> bool:
        """
        Verify that encryption is working properly.

        Returns:
            bool: True if encryption verification passed, False otherwise.
        """
        if not self._cipher:
            return False

        try:
            test_value = "test_encryption"
            encrypted_value = self._encrypt_value(test_value)
            decrypted_value = self._cipher.decrypt(encrypted_value.encode()).decode()
            return decrypted_value == test_value
        except Exception as e:
            logger.error(f"Encryption verification failed: {e}")
            return False

# Initialize the global secrets registry
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
        logger.error(f"Test failed: {e}")
