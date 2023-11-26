import logging
from google.cloud import secretmanager_v1 as secretmanager  # type: ignore
from typing import Optional
from google.api_core.exceptions import NotFound
from cloudsecretmanager.secret_manager import SecretManager

logger = logging.getLogger("GCPSecretManager")


class GCPSecretManager(SecretManager):
    """
    Concrete implementation of a secret manager using GCP Secret Manager.
    """

    def __init__(self, project_id: str):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id
        self.parent = f"projects/{project_id}"

    def create(self, *, secret_id: str, payload: str) -> None:
        if not secret_id:
            raise ValueError("`secret_id` cannot be empty")

        try:
            secret_path = f"{self.parent}/secrets/{secret_id}"
            # Check if the secret already exists
            self.client.get_secret(request={"name": secret_path})
            logger.info(f"Secret {secret_id} already exists.")
        except NotFound:
            # Create the secret if it does not exist
            self.client.create_secret(
                request={
                    "parent": self.parent,
                    "secret_id": secret_id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )

        # Add a new version of the secret
        self.client.add_secret_version(
            request={
                "parent": secret_path,
                "payload": {"data": payload.encode("UTF-8")},
            }
        )

    def get(self, *, secret_id: str, version_id: str = "latest") -> Optional[str]:
        if not secret_id:
            raise ValueError("`secret_id` cannot be empty")

        try:
            name = f"{self.parent}/secrets/{secret_id}/versions/{version_id}"
            response = self.client.access_secret_version(request={"name": name})
            return (
                response.payload.data.decode("UTF-8") if response.payload.data else ""
            )
        except NotFound:
            logger.error(f"Secret {secret_id} version {version_id} not found.")
            return None
        except Exception as e:
            logger.error(
                f"Error accessing secret {secret_id}, version {version_id}: {e}"
            )
            raise
