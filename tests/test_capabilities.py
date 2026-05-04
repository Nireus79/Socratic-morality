"""Tests for capability-based access control."""

import pytest
from socratic_morality.security.capabilities import CapabilityToken, CapabilityValidator


class TestCapabilityToken:
    """Tests for CapabilityToken."""

    def test_create_token(self):
        """Test creating a capability token."""
        token = CapabilityToken("agent_1", {"read", "write"})
        assert token.agent_id == "agent_1"
        assert len(token.capabilities) == 2

    def test_has_capability(self):
        """Test checking for a capability."""
        token = CapabilityToken("agent_1", {"read", "write"})
        assert token.has_capability("read") is True
        assert token.has_capability("delete") is False

    def test_add_capability(self):
        """Test adding a capability."""
        token = CapabilityToken("agent_1", {"read"})
        assert token.has_capability("write") is False
        token.add_capability("write")
        assert token.has_capability("write") is True

    def test_remove_capability(self):
        """Test removing a capability."""
        token = CapabilityToken("agent_1", {"read", "write"})
        assert token.has_capability("write") is True
        token.remove_capability("write")
        assert token.has_capability("write") is False

    def test_remove_nonexistent_capability(self):
        """Test removing a capability that doesn't exist."""
        token = CapabilityToken("agent_1", {"read"})
        # Should not raise error
        token.remove_capability("delete")
        assert token.has_capability("read") is True

    def test_has_all_capabilities(self):
        """Test checking if agent has all required capabilities."""
        token = CapabilityToken("agent_1", {"read", "write", "delete"})
        assert token.has_all_capabilities(["read", "write"]) is True
        assert token.has_all_capabilities(["read", "execute"]) is False

    def test_has_any_capability(self):
        """Test checking if agent has any required capability."""
        token = CapabilityToken("agent_1", {"read", "write"})
        assert token.has_any_capability(["read", "delete"]) is True
        assert token.has_any_capability(["execute", "delete"]) is False


class TestCapabilityValidator:
    """Tests for CapabilityValidator."""

    def test_register_agent(self):
        """Test registering an agent."""
        validator = CapabilityValidator()
        token = validator.register_agent("agent_1", ["read", "write"])
        assert token.agent_id == "agent_1"
        assert "agent_1" in validator.tokens

    def test_validate_single_capability(self):
        """Test validating a single capability."""
        validator = CapabilityValidator()
        validator.register_agent("agent_1", ["read", "write"])
        assert validator.validate("agent_1", "read") is True
        assert validator.validate("agent_1", "delete") is False

    def test_validate_nonexistent_agent(self):
        """Test validating a nonexistent agent."""
        validator = CapabilityValidator()
        assert validator.validate("agent_2", "read") is False

    def test_validate_all_capabilities(self):
        """Test validating all required capabilities."""
        validator = CapabilityValidator()
        validator.register_agent("agent_1", ["read", "write", "delete"])
        assert validator.validate_all("agent_1", ["read", "write"]) is True
        assert validator.validate_all("agent_1", ["read", "execute"]) is False

    def test_validate_any_capability(self):
        """Test validating any required capability."""
        validator = CapabilityValidator()
        validator.register_agent("agent_1", ["read", "write"])
        assert validator.validate_any("agent_1", ["read", "delete"]) is True
        assert validator.validate_any("agent_1", ["execute", "delete"]) is False

    def test_revoke_capability(self):
        """Test revoking a capability."""
        validator = CapabilityValidator()
        validator.register_agent("agent_1", ["read", "write"])
        assert validator.revoke_capability("agent_1", "write") is True
        assert validator.validate("agent_1", "write") is False
        assert validator.validate("agent_1", "read") is True

    def test_revoke_nonexistent_agent_capability(self):
        """Test revoking capability from nonexistent agent."""
        validator = CapabilityValidator()
        assert validator.revoke_capability("agent_2", "read") is False

    def test_get_agent_capabilities(self):
        """Test getting all agent capabilities."""
        validator = CapabilityValidator()
        validator.register_agent("agent_1", ["read", "write", "delete"])
        capabilities = validator.get_agent_capabilities("agent_1")
        assert capabilities == {"read", "write", "delete"}

    def test_get_nonexistent_agent_capabilities(self):
        """Test getting capabilities for nonexistent agent."""
        validator = CapabilityValidator()
        capabilities = validator.get_agent_capabilities("agent_2")
        assert capabilities == set()

    def test_unregister_agent(self):
        """Test unregistering an agent."""
        validator = CapabilityValidator()
        validator.register_agent("agent_1", ["read"])
        assert "agent_1" in validator.tokens
        assert validator.unregister_agent("agent_1") is True
        assert "agent_1" not in validator.tokens

    def test_unregister_nonexistent_agent(self):
        """Test unregistering a nonexistent agent."""
        validator = CapabilityValidator()
        assert validator.unregister_agent("agent_2") is False
