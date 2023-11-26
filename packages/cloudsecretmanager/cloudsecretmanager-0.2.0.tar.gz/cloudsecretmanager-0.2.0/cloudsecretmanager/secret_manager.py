from abc import ABC, abstractmethod
from typing import Optional


class SecretManager(ABC):
    """
    Abstract base class for a secret manager. Defines the contract for secret
    management operations.
    """

    @abstractmethod
    def create(self, *, secret_id: str, payload: str) -> None:
        """Create a new secret or a new version of an existing secret."""
        pass

    @abstractmethod
    def get(self, *, secret_id: str, version_id: str = "latest") -> Optional[str]:
        """Retrieve a specific version of a secret."""
        pass
