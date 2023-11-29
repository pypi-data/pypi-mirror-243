import logging
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

from cloudsecretmanager.secret_manager import SecretManager

logger = logging.getLogger("AzureSecretManager")

class AzureKeyVaultManager:
    """
    Implementation of the SecretManager protocol using Azure Key Vault.
    """

    def __init__(self, vault_url: str):
        self.vault_url = vault_url
        self.client = self._initialize_client()

    def _initialize_client(self):
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=self.vault_url, credential=credential)  # type: ignore
        try:
            # Attempt to retrieve a non-existing secret to check vault existence
            client.get_secret("non-existing-secret")  # type: ignore
        except ResourceNotFoundError:
            # Vault exists but the specific secret does not
            logger.info(f"Initialized Azure Key Vault client for {self.vault_url}")
            return client
        except Exception as e:
            # Vault does not exist or other error occurred
            raise ConnectionError(
                f"Failed to connect to Azure Key Vault at {self.vault_url}: {e}"
            )

    def create(self, *, secret_id: str, payload: str) -> None:
        if not secret_id:
            raise ValueError("`secret_id` cannot be empty")
        self.client.set_secret(secret_id, payload)

    def get(self, *, secret_id: str) -> Optional[str]:
        if not secret_id:
            raise ValueError("`secret_id` cannot be empty")
        try:
            # Retrieve the latest version of the secret
            secret = self.client.get_secret(secret_id)
            return secret.value
        except Exception as e:
            logger.error(f"Error accessing secret {secret_id}: {e}")
            return None
