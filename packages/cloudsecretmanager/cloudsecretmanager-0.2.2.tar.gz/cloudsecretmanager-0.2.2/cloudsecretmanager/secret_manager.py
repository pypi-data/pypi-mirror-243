from typing import Optional, Protocol


class SecretManager(Protocol):
    """
    Protocol for a secret manager. Defines the contract for secret
    management operations.
    """

    def create(self, *, secret_id: str, payload: str) -> None:
        """Create a new secret or a new version of an existing secret."""
        pass

    def get(self, *, secret_id: str) -> Optional[str]:
        """Retrieve a specific version of a secret."""
        pass
