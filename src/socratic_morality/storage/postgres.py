"""PostgreSQL storage backend for precedent and audit logs."""

import json
from typing import Any, Dict, List, Optional
from socratic_morality.storage.base import StorageBackend


class PostgreSQLStorage(StorageBackend):
    """PostgreSQL storage backend for production deployments."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "socratic_morality",
        user: str = "postgres",
        password: str = "",
    ):
        """Initialize PostgreSQL storage.

        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            database: Database name
            user: Database user
            password: Database password
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self._initialized = False

    async def _ensure_connected(self) -> None:
        """Ensure database connection is established."""
        if not self._initialized:
            await self._initialize_db()
            self._initialized = True

    async def _initialize_db(self) -> None:
        """Initialize database schema."""
        try:
            import asyncpg

            self.conn = await asyncpg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password if self.password else None,
            )

            await self.conn.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    key TEXT NOT NULL,
                    data JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            await self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_key ON records(key)
            """)

        except ImportError:
            raise ImportError(
                "asyncpg is required for PostgreSQL storage. "
                "Install with: pip install socratic-morality[postgres]"
            )

    async def store(self, key: str, value: Dict[str, Any]) -> str:
        """Store a record and return its ID."""
        await self._ensure_connected()

        result = await self.conn.fetchval(
            "INSERT INTO records (key, data) VALUES ($1, $2) RETURNING id::TEXT",
            key,
            json.dumps(value),
        )
        return result

    async def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a record by key."""
        await self._ensure_connected()

        result = await self.conn.fetchval("SELECT data FROM records WHERE key = $1 LIMIT 1", key)

        if result:
            return json.loads(result)
        return None

    async def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for records matching query."""
        await self._ensure_connected()

        # Build WHERE clause dynamically for all query fields
        where_clauses = []
        params = []

        for i, (field, value) in enumerate(query.items(), 1):
            where_clauses.append(f"data->>'{field}' = ${i}")
            params.append(value)

        where_clause = " AND ".join(where_clauses) if where_clauses else "TRUE"

        query_str = f"SELECT data FROM records WHERE {where_clause}"
        rows = await self.conn.fetch(query_str, *params)

        return [json.loads(row["data"]) for row in rows]

    async def delete(self, key: str) -> bool:
        """Delete a record by key."""
        await self._ensure_connected()

        result = await self.conn.execute("DELETE FROM records WHERE key = $1", key)

        # Parse the result string to get the number of deleted rows
        return int(result.split()[-1]) > 0

    async def list_all(self) -> List[Dict[str, Any]]:
        """List all records."""
        await self._ensure_connected()

        rows = await self.conn.fetch("SELECT data FROM records ORDER BY created_at DESC")

        return [json.loads(row["data"]) for row in rows]

    async def close(self) -> None:
        """Close database connection."""
        if self.conn:
            await self.conn.close()
            self._initialized = False
