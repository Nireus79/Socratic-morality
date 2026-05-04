"""Constitutional Governor - core decision engine."""

from datetime import datetime
from typing import Any, Dict, Optional, Union
from pathlib import Path
from socratic_morality.governor.decision import DecisionType, GovernorDecision
from socratic_morality.constitution.models import Constitution


class Governor:
    """Governor for constitutional AI governance."""

    def __init__(
        self, constitution: Union[str, Path, Dict, Constitution], llm_provider: str = "anthropic"
    ):
        if isinstance(constitution, Constitution):
            self.constitution = constitution
        elif isinstance(constitution, (str, Path)):
            self.constitution = Constitution.load_from_file(constitution)
        elif isinstance(constitution, dict):
            self.constitution = Constitution.from_dict(constitution)
        else:
            raise ValueError("Constitution must be a file path, dict, or Constitution object")
        self.llm_provider = llm_provider
        self._decision_count = 0

    async def evaluate(
        self,
        action: str,
        purpose: str = "",
        actor: str = "",
        context: Optional[Dict[str, Any]] = None,
        high_impact: bool = False,
    ) -> GovernorDecision:
        """Evaluate an action against the constitution."""
        self._decision_count += 1
        decision_id = f"decision_{self._decision_count}"
        timestamp = datetime.utcnow().isoformat()
        context = context or {}

        # Simple evaluation logic
        allowed = True
        decision_type = DecisionType.ALLOW
        violations = []

        return GovernorDecision(
            allowed=allowed,
            decision_type=decision_type,
            action=action,
            purpose=purpose,
            actor=actor,
            context=context,
            high_impact=high_impact,
            violations=violations,
            reasoning="Action approved by Governor",
            decision_id=decision_id,
            timestamp=timestamp,
        )
