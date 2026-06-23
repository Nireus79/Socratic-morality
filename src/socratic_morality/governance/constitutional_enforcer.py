"""Constitutional Enforcer - Principle verification and capability checking."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from socratic_morality.constitution.models import Constitution, Principle


@dataclass
class PrincipleViolation:
    """Represents a violation of a constitutional principle."""

    principle_name: str
    severity: str = "medium"
    description: str = ""
    violated_aspect: str = ""


@dataclass
class ConstitutionalCheck:
    """Result of checking an action against constitutional principles."""

    allowed: bool
    violations: List[PrincipleViolation] = field(default_factory=list)
    applicable_principles: List[Principle] = field(default_factory=list)
    reasoning: str = ""
    confidence: float = 1.0


class ConstitutionalEnforcer:
    """Enforces constitutional principles and validates actions."""

    def __init__(self, constitution_path: Optional[Union[str, Path]] = None):
        """Initialize enforcer with optional constitution file.

        Args:
            constitution_path: Path to constitution.yaml file or None for empty constitution.
        """
        if constitution_path:
            self.constitution = Constitution.load_from_file(constitution_path)
        else:
            self.constitution = Constitution()
        self._violation_cache: Dict[str, List[PrincipleViolation]] = {}

    def check_principles(self, action_description: str) -> ConstitutionalCheck:
        """Verify action against all constitutional principles.

        Args:
            action_description: Description of the action to check.

        Returns:
            ConstitutionalCheck with decision and reasoning.
        """
        violations = self.get_violations(action_description)
        applicable_principles = self.get_applicable_principles("general")

        # Determine if action is allowed based on violations
        critical_violations = [v for v in violations if v.severity == "critical"]
        allowed = len(critical_violations) == 0

        # Calculate confidence based on violation severity
        confidence = 1.0
        for violation in violations:
            if violation.severity == "critical":
                confidence -= 0.5
            elif violation.severity == "high":
                confidence -= 0.3
            elif violation.severity == "medium":
                confidence -= 0.1

        confidence = max(0.0, min(1.0, confidence))

        # Generate reasoning
        if allowed:
            reasoning = "Action complies with all constitutional principles."
            if violations:
                reasoning += f" {len(violations)} minor concerns noted."
        else:
            reasoning = f"Action violates {len(critical_violations)} critical principle(s)."

        return ConstitutionalCheck(
            allowed=allowed,
            violations=violations,
            applicable_principles=applicable_principles,
            reasoning=reasoning,
            confidence=confidence,
        )

    def get_violations(self, action_description: str) -> List[PrincipleViolation]:
        """Get principle violations for an action.

        Args:
            action_description: Description of the action to check.

        Returns:
            List of principle violations found.
        """
        # Check cache
        if action_description in self._violation_cache:
            return self._violation_cache[action_description]

        violations = []
        action_lower = action_description.lower()

        # Check each principle against the action
        for principle_name, principle in self.constitution.principles.items():
            violation = self._check_principle_violation(principle, action_lower)
            if violation:
                violations.append(violation)

        # Cache result
        self._violation_cache[action_description] = violations
        return violations

    def _check_principle_violation(
        self, principle: Principle, action_lower: str
    ) -> Optional[PrincipleViolation]:
        """Check if an action violates a specific principle.

        Args:
            principle: The principle to check.
            action_lower: Lowercase action description.

        Returns:
            PrincipleViolation if principle is violated, None otherwise.
        """
        principle_name_lower = principle.name.lower()

        # Define violation keywords for common principles
        violation_patterns = {
            "transparency": ["hide", "conceal", "secret", "undisclosed", "opaque"],
            "autonomy": [
                "force",
                "coerce",
                "override",
                "without consent",
                "deny choice",
                "remove agency",
            ],
            "honesty": ["deceive", "manipulate", "lie", "misrepresent", "fraud"],
            "safety": ["harm", "endanger", "risk", "compromise safety", "dangerous"],
            "fairness": ["discriminate", "bias", "unfair", "prejudice", "unjust"],
            "privacy": ["spy", "surveil", "invade privacy", "without permission"],
            "consent": ["without consent", "unconsented", "non-consensual"],
        }

        # Check if principle matches any violation patterns
        for principle_key, keywords in violation_patterns.items():
            if principle_key in principle_name_lower:
                for keyword in keywords:
                    if keyword in action_lower:
                        return PrincipleViolation(
                            principle_name=principle.name,
                            severity=principle.severity,
                            description=principle.description,
                            violated_aspect=keyword,
                        )

        return None

    def get_applicable_principles(self, action_type: str) -> List[Principle]:
        """Get principles applicable to an action type.

        Args:
            action_type: Type of action (e.g., "data_access", "communication").

        Returns:
            List of applicable principles.
        """
        applicable = []
        action_type_lower = action_type.lower()

        for principle_name, principle in self.constitution.principles.items():
            # All principles are applicable to general actions
            if action_type_lower == "general":
                applicable.append(principle)
            # Check category matches for specific action types
            elif principle.category and action_type_lower in principle.category.lower():
                applicable.append(principle)

        return applicable if applicable else list(self.constitution.principles.values())

    def evaluate_agent_capabilities(self, agent_name: str, requested_access: List[str]) -> bool:
        """Check if agent has required capabilities.

        Args:
            agent_name: Name of the agent requesting access.
            requested_access: List of capabilities/permissions requested.

        Returns:
            True if agent has all requested capabilities, False otherwise.
        """
        agent_capabilities = self.constitution.capabilities.get(agent_name, {})

        if not agent_capabilities:
            return False

        allowed_capabilities = agent_capabilities.get("allowed_actions", [])
        restrictions = agent_capabilities.get("restrictions", [])

        # Check if all requested access are in allowed list
        for access in requested_access:
            if access not in allowed_capabilities:
                return False
            # Check restrictions
            if access in restrictions:
                return False

        return True

    def load_constitution(self, path: Union[str, Path]) -> None:
        """Load a new constitution from file.

        Args:
            path: Path to constitution file.
        """
        self.constitution = Constitution.load_from_file(path)
        self._violation_cache.clear()

    def get_constitution_summary(self) -> Dict[str, Any]:
        """Get a summary of the current constitution.

        Returns:
            Dictionary with constitution metadata and structure.
        """
        return {
            "metadata": self.constitution.metadata,
            "supreme_principle": self.constitution.supreme_principle,
            "num_principles": len(self.constitution.principles),
            "num_rules": len(self.constitution.rules),
            "principles": list(self.constitution.principles.keys()),
            "axioms": self.constitution.axioms,
            "agents": list(self.constitution.capabilities.keys()),
        }
