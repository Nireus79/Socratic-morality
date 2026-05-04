"""Storage - Persistence backends for governance data."""

from .base import StorageBackend
from .sqlite import SQLiteStorage

__all__ = ["StorageBackend", "SQLiteStorage"]
