import logging
from typing import Optional

from cloudsecretmanager.secret_manager import SecretManager
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger("AzureSecretManager")


class AzureKeyVaultManager(SecretManager):
    """
    Concrete implementation of a secret manager using Azure Key Vault.
    """

    def __init__(self, vault_url: str):
        self.client = SecretClient(
            vault_url=vault_url, credential=DefaultAzureCredential()
        )
        self.vault_url = vault_url

    def create(self, *, secret_id: str, payload: str) -> None:
        if not secret_id:
            raise ValueError("`secret_id` cannot be empty")
        # Create a new secret or update an existing one
        self.client.set_secret(secret_id, payload)

    def get(self, *, secret_id: str, version_id: str = "latest") -> Optional[str]:
        if not secret_id:
            raise ValueError("`secret_id` cannot be empty")
        try:
            secret = self.client.get_secret(secret_id)
            return secret.value
        except Exception as e:
            logger.error(f"Error accessing secret {secret_id}: {e}")
            return None
