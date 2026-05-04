"""Capability-based access control for agents."""

from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class CapabilityToken:
    """Token representing agent capabilities."""
    agent_id: str
    capabilities: Set[str] = field(default_factory=set)

    def has_capability(self, capability: str) -> bool:
        """Check if agent has a specific capability."""
        return capability in self.capabilities

    def add_capability(self, capability: str) -> None:
        """Add a capability to the token."""
        self.capabilities.add(capability)

    def remove_capability(self, capability: str) -> None:
        """Remove a capability from the token."""
        self.capabilities.discard(capability)

    def has_all_capabilities(self, required: List[str]) -> bool:
        """Check if agent has all required capabilities."""
        return all(self.has_capability(cap) for cap in required)

    def has_any_capability(self, required: List[str]) -> bool:
        """Check if agent has any of the required capabilities."""
        return any(self.has_capability(cap) for cap in required)


class CapabilityValidator:
    """Validates agent capabilities against requirements."""

    def __init__(self):
        """Initialize capability validator."""
        self.tokens: dict[str, CapabilityToken] = {}

    def register_agent(
        self,
        agent_id: str,
        capabilities: List[str]
    ) -> CapabilityToken:
        """Register an agent with specific capabilities."""
        token = CapabilityToken(agent_id, set(capabilities))
        self.tokens[agent_id] = token
        return token

    def validate(
        self,
        agent_id: str,
        required_capability: str
    ) -> bool:
        """Validate that an agent has required capability."""
        if agent_id not in self.tokens:
            return False
        return self.tokens[agent_id].has_capability(required_capability)

    def validate_all(
        self,
        agent_id: str,
        required_capabilities: List[str]
    ) -> bool:
        """Validate that an agent has all required capabilities."""
        if agent_id not in self.tokens:
            return False
        return self.tokens[agent_id].has_all_capabilities(required_capabilities)

    def validate_any(
        self,
        agent_id: str,
        required_capabilities: List[str]
    ) -> bool:
        """Validate that an agent has any of the required capabilities."""
        if agent_id not in self.tokens:
            return False
        return self.tokens[agent_id].has_any_capability(required_capabilities)

    def revoke_capability(
        self,
        agent_id: str,
        capability: str
    ) -> bool:
        """Revoke a capability from an agent."""
        if agent_id not in self.tokens:
            return False
        self.tokens[agent_id].remove_capability(capability)
        return True

    def get_agent_capabilities(self, agent_id: str) -> Set[str]:
        """Get all capabilities for an agent."""
        if agent_id not in self.tokens:
            return set()
        return self.tokens[agent_id].capabilities.copy()

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent and remove all its capabilities."""
        if agent_id not in self.tokens:
            return False
        del self.tokens[agent_id]
        return True
