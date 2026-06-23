"""Governor decision module."""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from enum import Enum


class DecisionType(str, Enum):
    """Types of decisions the Governor can make."""

    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"
    BLOCK = "block"


@dataclass
class ConstitutionalViolation:
    """Represents a violation of a constitutional principle."""

    principle: str
    description: str = ""


@dataclass
class GovernorDecision:
    """Decision made by the Governor."""

    allowed: bool
    decision_type: DecisionType
    action: str
    purpose: str = ""
    actor: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    high_impact: bool = False
    violations: List[ConstitutionalViolation] = field(default_factory=list)
    reasoning: str = ""
    decision_id: str = ""
    timestamp: str = ""

    def requires_escalation(self) -> bool:
        """Check if decision requires escalation."""
        return self.decision_type == DecisionType.ESCALATE or self.high_impact
