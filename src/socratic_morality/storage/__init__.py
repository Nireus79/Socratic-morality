"""Storage backends for precedent and audit logs."""

from socratic_morality.storage.base import StorageBackend
from socratic_morality.storage.sqlite import SQLiteStorage

try:
    from socratic_morality.storage.postgres import PostgreSQLStorage
except ImportError:
    PostgreSQLStorage = None

__all__ = ["StorageBackend", "SQLiteStorage", "PostgreSQLStorage"]
