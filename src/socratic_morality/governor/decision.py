# Governor decision module
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum

class DecisionType(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"
    BLOCK = "block"

@dataclass
class ConstitutionalViolation:
    principle: str

@dataclass
class GovernorDecision:
    allowed: bool
    decision_type: DecisionType
    action: str
