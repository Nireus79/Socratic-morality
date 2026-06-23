"""Remediation Engine for addressing constraint violations and decision reversals."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime
from socratic_morality.governor.decision import GovernorDecision


class RemediationType(str, Enum):
    """Types of remediation strategies."""

    MODIFY_ACTION = "modify_action"
    ADD_SAFEGUARDS = "add_safeguards"
    REJECT_AND_PROPOSE_ALTERNATIVE = "reject_and_propose_alternative"
    ESCALATE_WITH_CONSTRAINTS = "escalate_with_constraints"
    ROLLBACK = "rollback"


class RiskLevel(str, Enum):
    """Risk levels for remediation approaches."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class RemediationSuggestion:
    """Suggested remediation for a constraint violation."""

    remediation_type: RemediationType
    description: str
    required_changes: List[str] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    implementation_steps: List[str] = field(default_factory=list)
    estimated_impact: Dict[str, Any] = field(default_factory=dict)
    reversibility: str = "reversible"  # reversible or irreversible
    estimated_effort: str = "medium"  # low, medium, high


@dataclass
class SafeguardPlan:
    """Plan for implementing protective measures."""

    action_description: str
    safeguards: List[str] = field(default_factory=list)
    monitoring_requirements: List[str] = field(default_factory=list)
    fallback_procedures: List[str] = field(default_factory=list)
    escalation_triggers: List[str] = field(default_factory=list)
    estimated_effectiveness: float = 0.8  # 0-1


@dataclass
class RemediationResult:
    """Result of remediation attempt."""

    success: bool
    action_taken: str
    changes_made: List[str] = field(default_factory=list)
    new_decision_id: Optional[str] = None
    risks_eliminated: List[str] = field(default_factory=list)
    residual_risks: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class RollbackResult:
    """Result of rolling back a decision."""

    success: bool
    rolled_back_decision_id: str
    original_state_restored: bool
    side_effects: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class RemediationRecord:
    """Record of a remediation action."""

    record_id: str
    decision_id: str
    constraint_violated: str
    remediation_type: RemediationType
    remediation_details: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class RemediationEngine:
    """Engine for suggesting and executing remediations for constraint violations."""

    def __init__(self):
        """Initialize remediation engine."""
        self.remediation_history: List[RemediationRecord] = []
        self.active_remediations: Dict[str, RemediationResult] = {}
        self._record_counter = 0

    async def suggest_remediation(
        self, decision: GovernorDecision, constraint_violated: str
    ) -> RemediationSuggestion:
        """Suggest remediation for a constraint violation.

        Args:
            decision: The decision that violated a constraint
            constraint_violated: Description of the constraint violated

        Returns:
            RemediationSuggestion with proposed fix
        """
        action_lower = decision.action.lower()

        # Determine best remediation type based on violation
        if self._is_parameter_violation(constraint_violated):
            return self._suggest_modify_action(decision, constraint_violated)
        elif self._is_safety_violation(constraint_violated):
            return self._suggest_add_safeguards(decision, constraint_violated)
        elif self._is_fundamental_violation(constraint_violated):
            return self._suggest_reject_and_propose(decision, constraint_violated)
        else:
            return self._suggest_escalate_with_constraints(decision, constraint_violated)

    def _is_parameter_violation(self, constraint: str) -> bool:
        """Check if violation is fixable by parameter modification."""
        parameter_keywords = [
            "scope",
            "threshold",
            "limit",
            "boundary",
            "range",
            "duration",
            "frequency",
        ]
        return any(kw in constraint.lower() for kw in parameter_keywords)

    def _is_safety_violation(self, constraint: str) -> bool:
        """Check if violation is a safety issue requiring safeguards."""
        safety_keywords = ["risk", "dangerous", "unsafe", "hazard", "exposure"]
        return any(kw in constraint.lower() for kw in safety_keywords)

    def _is_fundamental_violation(self, constraint: str) -> bool:
        """Check if violation is fundamental, requiring rejection."""
        fundamental_keywords = [
            "harm",
            "illegal",
            "unethical",
            "violation",
            "breach",
            "rights",
            "consent",
        ]
        return any(kw in constraint.lower() for kw in fundamental_keywords)

    def _suggest_modify_action(
        self, decision: GovernorDecision, constraint: str
    ) -> RemediationSuggestion:
        """Suggest modifying action parameters."""
        return RemediationSuggestion(
            remediation_type=RemediationType.MODIFY_ACTION,
            description="Modify action parameters to comply with constraint",
            required_changes=[
                "Adjust action scope to be more limited",
                "Reduce impact on affected parties",
                "Add explicitness and transparency",
            ],
            risk_level=RiskLevel.LOW,
            implementation_steps=[
                "1. Identify specific parameters causing violation",
                "2. Define modified parameters within acceptable range",
                "3. Re-evaluate modified action against constraints",
                "4. Verify compliance before execution",
            ],
            estimated_impact={
                "effectiveness": 0.85,
                "implementation_time": "low",
                "stakeholder_impact": "minimal",
            },
            reversibility="reversible",
            estimated_effort="low",
        )

    def _suggest_add_safeguards(
        self, decision: GovernorDecision, constraint: str
    ) -> RemediationSuggestion:
        """Suggest adding protective safeguards."""
        return RemediationSuggestion(
            remediation_type=RemediationType.ADD_SAFEGUARDS,
            description="Implement protective measures to mitigate identified risks",
            required_changes=[
                "Add monitoring mechanisms",
                "Implement rollback capability",
                "Establish escalation triggers",
                "Set up audit logging",
            ],
            risk_level=RiskLevel.MEDIUM,
            implementation_steps=[
                "1. Identify specific risks to mitigate",
                "2. Design monitoring approach",
                "3. Implement safeguard mechanisms",
                "4. Test safeguard effectiveness",
                "5. Deploy with monitoring active",
            ],
            estimated_impact={
                "effectiveness": 0.75,
                "implementation_time": "medium",
                "stakeholder_impact": "low",
                "performance_overhead": "5-10%",
            },
            reversibility="reversible",
            estimated_effort="medium",
        )

    def _suggest_reject_and_propose(
        self, decision: GovernorDecision, constraint: str
    ) -> RemediationSuggestion:
        """Suggest rejecting action and proposing alternative."""
        return RemediationSuggestion(
            remediation_type=RemediationType.REJECT_AND_PROPOSE_ALTERNATIVE,
            description="Reject current action and propose better alternative",
            required_changes=[
                "Block current action",
                "Analyze root need",
                "Identify alternative approach",
                "Verify alternative compliance",
            ],
            risk_level=RiskLevel.LOW,
            implementation_steps=[
                "1. Block execution of current action",
                "2. Communicate rejection to stakeholders",
                "3. Analyze what was trying to be achieved",
                "4. Propose alternative that achieves goal ethically",
                "5. Re-evaluate alternative against all constraints",
            ],
            estimated_impact={
                "effectiveness": 0.95,
                "implementation_time": "high",
                "stakeholder_impact": "moderate",
                "resolution_quality": "high",
            },
            reversibility="irreversible",
            estimated_effort="high",
        )

    def _suggest_escalate_with_constraints(
        self, decision: GovernorDecision, constraint: str
    ) -> RemediationSuggestion:
        """Suggest escalating with operational constraints."""
        return RemediationSuggestion(
            remediation_type=RemediationType.ESCALATE_WITH_CONSTRAINTS,
            description="Allow action with additional operational constraints and oversight",
            required_changes=[
                "Add human review requirement",
                "Implement strict logging",
                "Set time limits",
                "Establish approval process",
            ],
            risk_level=RiskLevel.HIGH,
            implementation_steps=[
                "1. Flag for human review",
                "2. Define operational constraints",
                "3. Set up approval workflow",
                "4. Implement enhanced logging",
                "5. Schedule follow-up evaluation",
            ],
            estimated_impact={
                "effectiveness": 0.65,
                "implementation_time": "medium",
                "stakeholder_impact": "high",
                "delay_introduced": "depends on review time",
            },
            reversibility="reversible",
            estimated_effort="medium",
        )

    async def auto_remediate(self, decision: GovernorDecision) -> RemediationResult:
        """Automatically execute safe remediation actions.

        Only applies MODIFY_ACTION remediations; others require human approval.

        Args:
            decision: The decision to remediate

        Returns:
            RemediationResult with outcome
        """
        # Only auto-remediate safe modifications
        if not decision.violations:
            return RemediationResult(
                success=True,
                action_taken="no_remediation_needed",
                new_decision_id=decision.decision_id,
            )

        # Suggest remediation
        constraint = decision.violations[0].description if decision.violations else "unknown"
        suggestion = await self.suggest_remediation(decision, constraint)

        if suggestion.remediation_type != RemediationType.MODIFY_ACTION:
            return RemediationResult(
                success=False,
                action_taken="remediation_requires_human_approval",
                residual_risks=["Remediation type requires human oversight"],
            )

        # Apply modification
        modified_action = self._apply_modifications(decision.action)

        # Create new decision
        new_decision_id = f"{decision.decision_id}_remediated"

        result = RemediationResult(
            success=True,
            action_taken="auto_modified_action",
            changes_made=suggestion.required_changes,
            new_decision_id=new_decision_id,
            risks_eliminated=["Original constraint violation addressed"],
        )

        self.active_remediations[new_decision_id] = result
        return result

    def _apply_modifications(self, action: str) -> str:
        """Apply parameter modifications to an action."""
        # Implementation would be domain-specific
        # For now, add qualification
        return f"{action} (with scope limitations and safeguards)"

    async def rollback_decision(self, decision_id: str) -> RollbackResult:
        """Rollback a previously made decision.

        Args:
            decision_id: ID of decision to rollback

        Returns:
            RollbackResult with outcome
        """
        if decision_id not in self.active_remediations:
            return RollbackResult(
                success=False,
                rolled_back_decision_id=decision_id,
                original_state_restored=False,
                side_effects=["Decision not found in remediation system"],
            )

        remediation = self.active_remediations[decision_id]

        # Attempt rollback
        side_effects = []

        # Check for irreversible changes
        if hasattr(remediation, "reversibility") and remediation.reversibility == "irreversible":
            side_effects.append("Note: Some changes may not be fully reversible")

        # Remove from active
        del self.active_remediations[decision_id]

        result = RollbackResult(
            success=True,
            rolled_back_decision_id=decision_id,
            original_state_restored=True,
            side_effects=side_effects,
        )

        # Record the rollback
        self._record_remediation(
            decision_id, "rollback", RemediationType.ROLLBACK, {"result": result}
        )

        return result

    async def implement_safeguards(self, action: str) -> SafeguardPlan:
        """Implement protective safeguards for an action.

        Args:
            action: Description of the action

        Returns:
            SafeguardPlan with protective measures
        """
        action_lower = action.lower()

        safeguards = [
            "Continuous monitoring of execution",
            "Real-time impact assessment",
            "Automated rollback capability",
            "Audit trail creation",
            "Performance metrics tracking",
        ]

        monitoring_requirements = [
            "Monitor stakeholder feedback",
            "Track performance metrics",
            "Detect anomalies",
            "Log all state changes",
        ]

        fallback_procedures = [
            "Immediate pause capability",
            "Restore to previous state procedure",
            "Manual override option",
            "Escalation to human review",
        ]

        escalation_triggers = [
            "Error rate exceeds threshold",
            "Stakeholder complaints received",
            "Performance degrades",
            "Unintended side effects detected",
        ]

        plan = SafeguardPlan(
            action_description=action,
            safeguards=safeguards,
            monitoring_requirements=monitoring_requirements,
            fallback_procedures=fallback_procedures,
            escalation_triggers=escalation_triggers,
            estimated_effectiveness=0.85,
        )

        return plan

    def get_remediation_history(self) -> List[RemediationRecord]:
        """Get complete remediation history.

        Returns:
            List of all remediation records
        """
        return self.remediation_history.copy()

    def _record_remediation(
        self,
        decision_id: str,
        constraint: str,
        remediation_type: RemediationType,
        details: Dict[str, Any],
    ) -> None:
        """Record a remediation action."""
        self._record_counter += 1
        record = RemediationRecord(
            record_id=f"remediation_{self._record_counter}",
            decision_id=decision_id,
            constraint_violated=constraint,
            remediation_type=remediation_type,
            remediation_details=details,
        )
        self.remediation_history.append(record)

    def get_active_remediations(self) -> Dict[str, RemediationResult]:
        """Get all active remediations.

        Returns:
            Dictionary of active remediation results
        """
        return self.active_remediations.copy()

    def clear_remediation_history(self) -> int:
        """Clear remediation history.

        Returns:
            Number of records cleared
        """
        count = len(self.remediation_history)
        self.remediation_history.clear()
        return count
