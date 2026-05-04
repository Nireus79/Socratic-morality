"""SQLite storage backend for precedent and audit logs."""

import sqlite3
import json
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
from threading import Lock
from socratic_morality.storage.base import StorageBackend


class SQLiteStorage(StorageBackend):
    """SQLite storage backend for development and production."""

    def __init__(self, database_path: str = "socratic_morality.db"):
        """Initialize SQLite storage.

        Args:
            database_path: Path to SQLite database file
        """
        self.database_path = Path(database_path)
        self.db_conn: Optional[sqlite3.Connection] = None
        self._lock = Lock()
        self._initialized = False

    async def _ensure_connected(self) -> None:
        """Ensure database connection is established."""
        if not self._initialized:
            await self._initialize_db()
            self._initialized = True

    async def _initialize_db(self) -> None:
        """Initialize database schema."""

        def _init():
            with self._lock:
                self.db_conn = sqlite3.connect(str(self.database_path), check_same_thread=False)
                self.db_conn.row_factory = sqlite3.Row
                cursor = self.db_conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS records (
                        id TEXT PRIMARY KEY,
                        key TEXT NOT NULL,
                        data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_key ON records(key)
                """)

                self.db_conn.commit()

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _init)

    async def store(self, key: str, value: Dict[str, Any]) -> str:
        """Store a record and return its ID."""
        await self._ensure_connected()

        import uuid

        record_id = str(uuid.uuid4())
        data_json = json.dumps(value)

        def _store():
            with self._lock:
                cursor = self.db_conn.cursor()
                cursor.execute(
                    "INSERT INTO records (id, key, data) VALUES (?, ?, ?)",
                    (record_id, key, data_json),
                )
                self.db_conn.commit()

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _store)
        return record_id

    async def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a record by key."""
        await self._ensure_connected()

        def _retrieve():
            with self._lock:
                cursor = self.db_conn.cursor()
                cursor.execute("SELECT data FROM records WHERE key = ? LIMIT 1", (key,))
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return None

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _retrieve)

    async def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for records matching query."""
        await self._ensure_connected()

        def _search():
            with self._lock:
                cursor = self.db_conn.cursor()
                cursor.execute("SELECT data FROM records")
                rows = cursor.fetchall()

                results = []
                for row in rows:
                    record = json.loads(row[0])

                    # Check if all query fields match
                    match = True
                    for field, value in query.items():
                        if record.get(field) != value:
                            match = False
                            break

                    if match:
                        results.append(record)

                return results

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _search)

    async def delete(self, key: str) -> bool:
        """Delete a record by key."""
        await self._ensure_connected()

        def _delete():
            with self._lock:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM records WHERE key = ?", (key,))
                self.db_conn.commit()
                return cursor.rowcount > 0

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _delete)

    async def list_all(self) -> List[Dict[str, Any]]:
        """List all records."""
        await self._ensure_connected()

        def _list_all():
            with self._lock:
                cursor = self.db_conn.cursor()
                cursor.execute("SELECT data FROM records ORDER BY created_at DESC")
                rows = cursor.fetchall()
                return [json.loads(row[0]) for row in rows]

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _list_all)

    async def close(self) -> None:
        """Close database connection."""
        if self.db_conn:
            with self._lock:
                self.db_conn.close()
            self._initialized = False
