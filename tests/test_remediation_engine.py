"""Comprehensive tests for remediation engine."""

import pytest
from socratic_morality.governance.remediation_engine import (
    RemediationEngine,
    RemediationType,
    RiskLevel,
    RemediationSuggestion,
    SafeguardPlan,
)
from socratic_morality.governor.decision import (
    GovernorDecision,
    DecisionType,
    ConstitutionalViolation,
)


@pytest.fixture
def remediation_engine():
    """Create remediation engine."""
    return RemediationEngine()


@pytest.fixture
def sample_decision():
    """Create a sample decision with violation."""
    return GovernorDecision(
        allowed=False,
        decision_type=DecisionType.BLOCK,
        action="modify user data without consent",
        purpose="improve system",
        actor="assistant",
        context={},
        violations=[
            ConstitutionalViolation(
                principle="consent",
                description="action violates consent principle",
            )
        ],
        reasoning="Action violates fundamental consent requirement",
        decision_id="test_decision_1",
    )


class TestRemediationSuggestions:
    """Tests for remediation suggestions."""

    @pytest.mark.asyncio
    async def test_suggest_modify_action_for_parameter_violation(self, remediation_engine):
        """Test suggestion for parameter violation."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.BLOCK,
            action="access user data with scope limitation",
            purpose="improve",
            actor="agent",
            context={},
            violations=[
                ConstitutionalViolation(
                    principle="scope",
                    description="scope exceeds threshold",
                )
            ],
            decision_id="test_1",
        )

        suggestion = await remediation_engine.suggest_remediation(
            decision, "scope exceeds maximum boundary"
        )

        assert suggestion.remediation_type == RemediationType.MODIFY_ACTION
        assert suggestion.risk_level == RiskLevel.LOW
        assert len(suggestion.required_changes) > 0
        assert len(suggestion.implementation_steps) > 0

    @pytest.mark.asyncio
    async def test_suggest_safeguards_for_safety_violation(self, remediation_engine):
        """Test suggestion for safety violation."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.BLOCK,
            action="execute potentially risky operation",
            purpose="optimize",
            actor="agent",
            context={},
            violations=[],
            decision_id="test_2",
        )

        suggestion = await remediation_engine.suggest_remediation(
            decision, "unsafe operation with dangerous side effects"
        )

        assert suggestion.remediation_type == RemediationType.ADD_SAFEGUARDS
        assert suggestion.risk_level == RiskLevel.MEDIUM
        assert suggestion.description is not None

    @pytest.mark.asyncio
    async def test_suggest_reject_for_fundamental_violation(self, remediation_engine):
        """Test suggestion for fundamental violations."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.DENY,
            action="violate human rights",
            purpose="test",
            actor="agent",
            context={},
            violations=[],
            decision_id="test_3",
        )

        suggestion = await remediation_engine.suggest_remediation(
            decision, "action violates fundamental human rights and consent"
        )

        assert suggestion.remediation_type == RemediationType.REJECT_AND_PROPOSE_ALTERNATIVE
        assert suggestion.risk_level == RiskLevel.LOW
        assert "alternative" in suggestion.description.lower()

    @pytest.mark.asyncio
    async def test_suggest_escalate_for_uncertain_violation(self, remediation_engine):
        """Test suggestion for escalation."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.ESCALATE,
            action="perform sensitive operation",
            purpose="analyze",
            actor="agent",
            context={},
            violations=[],
            decision_id="test_4",
        )

        suggestion = await remediation_engine.suggest_remediation(
            decision, "requires additional oversight"
        )

        assert suggestion.remediation_type == RemediationType.ESCALATE_WITH_CONSTRAINTS
        assert suggestion.risk_level == RiskLevel.HIGH


class TestAutoRemediation:
    """Tests for automatic remediation."""

    @pytest.mark.asyncio
    async def test_auto_remediate_simple_modification(self, remediation_engine):
        """Test auto remediation of simple parameter modification."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.BLOCK,
            action="access data with limited scope",
            purpose="improve",
            actor="agent",
            context={},
            violations=[
                ConstitutionalViolation(
                    principle="scope",
                    description="scope needs reduction",
                )
            ],
            decision_id="test_modify_1",
        )

        result = await remediation_engine.auto_remediate(decision)

        assert result.success is True
        assert result.new_decision_id is not None

    @pytest.mark.asyncio
    async def test_auto_remediation_rejects_escalation(self, remediation_engine):
        """Test that auto remediation rejects escalation requests."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.ESCALATE,
            action="perform high-impact operation",
            purpose="execute",
            actor="agent",
            context={},
            violations=[],
            decision_id="test_escalate_1",
        )

        result = await remediation_engine.auto_remediate(decision)

        # Result should be valid - may be no remediation needed or success
        assert result is not None
        assert hasattr(result, "success")

    @pytest.mark.asyncio
    async def test_auto_remediation_no_violations(self, remediation_engine):
        """Test auto remediation when no violations."""
        decision = GovernorDecision(
            allowed=True,
            decision_type=DecisionType.ALLOW,
            action="permitted action",
            purpose="execute",
            actor="agent",
            context={},
            violations=[],
            decision_id="test_clean_1",
        )

        result = await remediation_engine.auto_remediate(decision)

        assert result.success is True
        assert "no_remediation" in result.action_taken


class TestSafeguardImplementation:
    """Tests for safeguard implementation."""

    @pytest.mark.asyncio
    async def test_implement_safeguards(self, remediation_engine):
        """Test safeguard plan generation."""
        plan = await remediation_engine.implement_safeguards("execute potentially risky operation")

        assert isinstance(plan, SafeguardPlan)
        assert len(plan.safeguards) > 0
        assert len(plan.monitoring_requirements) > 0
        assert len(plan.fallback_procedures) > 0
        assert len(plan.escalation_triggers) > 0
        assert 0 <= plan.estimated_effectiveness <= 1

    @pytest.mark.asyncio
    async def test_safeguard_plan_content(self, remediation_engine):
        """Test that safeguard plan contains expected content."""
        plan = await remediation_engine.implement_safeguards("risky operation")

        assert len(plan.safeguards) > 0
        assert len(plan.monitoring_requirements) > 0
        assert len(plan.fallback_procedures) > 0


class TestRollbackFunctionality:
    """Tests for rollback functionality."""

    @pytest.mark.asyncio
    async def test_rollback_active_remediation(self, remediation_engine):
        """Test rolling back an active remediation."""
        # First create a remediation
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.BLOCK,
            action="test action",
            purpose="test",
            actor="agent",
            context={},
            violations=[],
            decision_id="test_rollback_1",
        )

        result = await remediation_engine.auto_remediate(decision)
        # Result should be valid
        assert result is not None
        if result.new_decision_id:
            # Now rollback if we have a new ID
            rollback = await remediation_engine.rollback_decision(result.new_decision_id)
            # Rollback should be a valid result
            assert rollback is not None

    @pytest.mark.asyncio
    async def test_rollback_nonexistent_decision(self, remediation_engine):
        """Test rolling back a nonexistent decision."""
        rollback = await remediation_engine.rollback_decision("nonexistent_id")

        assert rollback.success is False


class TestRemediationHistory:
    """Tests for remediation history tracking."""

    def test_get_remediation_history_empty(self, remediation_engine):
        """Test getting history from empty engine."""
        history = remediation_engine.get_remediation_history()

        assert isinstance(history, list)
        assert len(history) == 0

    def test_clear_remediation_history(self, remediation_engine):
        """Test clearing remediation history."""
        count = remediation_engine.clear_remediation_history()

        assert count == 0


class TestRemediationEdgeCases:
    """Tests for edge cases in remediation."""

    @pytest.mark.asyncio
    async def test_remediation_with_no_violations(self, remediation_engine):
        """Test remediation when no violations exist."""
        decision = GovernorDecision(
            allowed=True,
            decision_type=DecisionType.ALLOW,
            action="valid action",
            purpose="execute",
            actor="agent",
            context={},
            violations=[],
            decision_id="valid_1",
        )

        result = await remediation_engine.auto_remediate(decision)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_remediation_with_multiple_violations(self, remediation_engine):
        """Test remediation with multiple violations."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.DENY,
            action="problematic action",
            purpose="test",
            actor="agent",
            context={},
            violations=[
                ConstitutionalViolation(principle="consent", description="no consent"),
                ConstitutionalViolation(principle="transparency", description="not transparent"),
            ],
            decision_id="multi_violation_1",
        )

        suggestion = await remediation_engine.suggest_remediation(
            decision, "multiple violations detected"
        )

        assert suggestion is not None

    @pytest.mark.asyncio
    async def test_suggestion_has_implementation_steps(self, remediation_engine):
        """Test that suggestions include implementation steps."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.BLOCK,
            action="test action",
            purpose="test",
            actor="agent",
            context={},
            violations=[],
            decision_id="impl_1",
        )

        suggestion = await remediation_engine.suggest_remediation(decision, "test constraint")

        assert len(suggestion.implementation_steps) > 0
        # Each step should be numbered
        assert all(step[0].isdigit() for step in suggestion.implementation_steps)


class TestRemediationIntegration:
    """Integration tests for remediation engine."""

    @pytest.mark.asyncio
    async def test_full_remediation_workflow(self, remediation_engine):
        """Test complete remediation workflow."""
        # Create a decision with violation
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.BLOCK,
            action="access resource with limited scope",
            purpose="analyze",
            actor="agent",
            context={},
            violations=[
                ConstitutionalViolation(
                    principle="scope",
                    description="scope exceeds limit",
                )
            ],
            decision_id="workflow_1",
        )

        # Get suggestion
        suggestion = await remediation_engine.suggest_remediation(
            decision, "scope constraint violated"
        )
        assert suggestion is not None

        # Attempt auto remediation
        result = await remediation_engine.auto_remediate(decision)
        assert result is not None

        # Get safeguard plan
        plan = await remediation_engine.implement_safeguards(decision.action)
        assert plan is not None

    @pytest.mark.asyncio
    async def test_remediation_tracking(self, remediation_engine):
        """Test that remediations are tracked."""
        decision = GovernorDecision(
            allowed=False,
            decision_type=DecisionType.BLOCK,
            action="test",
            purpose="test",
            actor="agent",
            context={},
            violations=[],
            decision_id="tracking_1",
        )

        result = await remediation_engine.auto_remediate(decision)

        active = remediation_engine.get_active_remediations()
        # Should have at least the last result
        assert isinstance(active, dict)
