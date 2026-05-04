"""Tests for Governor class."""

import pytest
from socratic_morality.governor.core import Governor
from socratic_morality.constitution.models import Constitution


@pytest.mark.asyncio
async def test_governor_creation():
    """Test Governor can be created with a dict constitution."""
    constitution = {
        "metadata": {"name": "Test Constitution"},
        "supreme_principle": "Test principle",
        "principles": {},
        "rules": [],
    }
    gov = Governor(constitution=constitution)
    assert gov.llm_provider == "anthropic"
    assert gov.constitution is not None


@pytest.mark.asyncio
async def test_governor_evaluate():
    """Test Governor.evaluate() returns a decision."""
    constitution = {"metadata": {"name": "Test"}, "principles": {}, "rules": []}
    gov = Governor(constitution=constitution)

    decision = await gov.evaluate(
        action="Test action", purpose="Testing", actor="test_agent", context={"user_id": "user_123"}
    )

    assert decision is not None
    assert decision.action == "Test action"
    assert decision.allowed == True
    assert decision.decision_id.startswith("decision_")


@pytest.mark.asyncio
async def test_governor_tracking():
    """Test Governor tracks decisions."""
    constitution = {"metadata": {}, "principles": {}, "rules": []}
    gov = Governor(constitution=constitution)

    decision1 = await gov.evaluate(action="Action 1")
    decision2 = await gov.evaluate(action="Action 2")

    assert decision1.decision_id == "decision_1"
    assert decision2.decision_id == "decision_2"
