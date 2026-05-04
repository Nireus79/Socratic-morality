"""Tests for storage backends."""

import pytest
import asyncio
from pathlib import Path
from socratic_morality.storage.base import StorageBackend
from socratic_morality.storage.sqlite import SQLiteStorage


@pytest.fixture
async def sqlite_storage(tmp_path):
    """Create SQLite storage for tests."""
    db_path = str(tmp_path / "test.db")
    storage = SQLiteStorage(db_path)
    await storage._ensure_connected()
    yield storage
    await storage.close()


class TestSQLiteStorage:
    """Tests for SQLite storage backend."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve(self, sqlite_storage):
        """Test storing and retrieving records."""
        test_data = {"action": "test_action", "allowed": True}

        record_id = await sqlite_storage.store("test_key", test_data)
        assert record_id is not None

        retrieved = await sqlite_storage.retrieve("test_key")
        assert retrieved is not None
        assert retrieved["action"] == "test_action"
        assert retrieved["allowed"] is True

    @pytest.mark.asyncio
    async def test_search(self, sqlite_storage):
        """Test searching records."""
        await sqlite_storage.store("key1", {"action": "read", "allowed": True})
        await sqlite_storage.store("key2", {"action": "write", "allowed": False})
        await sqlite_storage.store("key3", {"action": "read", "allowed": True})

        results = await sqlite_storage.search({"action": "read"})
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_search_multiple_criteria(self, sqlite_storage):
        """Test searching with multiple criteria."""
        await sqlite_storage.store("key1", {"action": "read", "allowed": True})
        await sqlite_storage.store("key2", {"action": "read", "allowed": False})
        await sqlite_storage.store("key3", {"action": "write", "allowed": True})

        results = await sqlite_storage.search({"action": "read", "allowed": True})
        assert len(results) == 1
        assert results[0]["action"] == "read"

    @pytest.mark.asyncio
    async def test_delete(self, sqlite_storage):
        """Test deleting records."""
        await sqlite_storage.store("test_key", {"action": "test"})

        deleted = await sqlite_storage.delete("test_key")
        assert deleted is True

        retrieved = await sqlite_storage.retrieve("test_key")
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, sqlite_storage):
        """Test deleting nonexistent record."""
        deleted = await sqlite_storage.delete("nonexistent")
        assert deleted is False

    @pytest.mark.asyncio
    async def test_list_all(self, sqlite_storage):
        """Test listing all records."""
        await sqlite_storage.store("key1", {"action": "action1"})
        await sqlite_storage.store("key2", {"action": "action2"})
        await sqlite_storage.store("key3", {"action": "action3"})

        all_records = await sqlite_storage.list_all()
        assert len(all_records) == 3

    @pytest.mark.asyncio
    async def test_list_all_empty(self, sqlite_storage):
        """Test listing records when storage is empty."""
        all_records = await sqlite_storage.list_all()
        assert len(all_records) == 0

    @pytest.mark.asyncio
    async def test_concurrent_storage(self, sqlite_storage):
        """Test concurrent storage operations."""

        async def store_record(key, data):
            return await sqlite_storage.store(key, data)

        tasks = [store_record(f"key_{i}", {"action": f"action_{i}"}) for i in range(10)]

        results = await asyncio.gather(*tasks)
        assert len(results) == 10

        all_records = await sqlite_storage.list_all()
        assert len(all_records) == 10
