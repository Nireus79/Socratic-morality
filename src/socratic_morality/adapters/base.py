"""Base adapter for wrapping agents with Governor."""

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """Abstract base class for framework adapters."""

    def __init__(self, governor: Any):
        """Initialize adapter with a Governor instance."""
        self.governor = governor

    @abstractmethod
    async def wrap_agent(self, agent: Any) -> Any:
        """Wrap an agent with Governor governance."""
        pass

    @abstractmethod
    async def intercept_action(
        self, action: str, agent_name: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Intercept and evaluate an agent action."""
        pass

    async def _evaluate_action(
        self, action: str, actor: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Common evaluation logic for all adapters."""
        context = context or {}
        decision = await self.governor.evaluate(action=action, actor=actor, context=context)

        return {
            "allowed": decision.allowed,
            "decision_type": decision.decision_type,
            "reasoning": decision.reasoning,
            "violations": [
                {"principle": v.principle, "description": v.description}
                for v in decision.violations
            ],
            "requires_escalation": decision.requires_escalation(),
        }
