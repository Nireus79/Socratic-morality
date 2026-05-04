"""Base storage interface for precedent and audit logs."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    async def store(self, key: str, value: Dict[str, Any]) -> str:
        """Store a record and return its ID."""
        pass

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a record by key."""
        pass

    @abstractmethod
    async def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for records matching query."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a record."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Dict[str, Any]]:
        """List all records."""
        pass
