"""Tests for framework adapters."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from socratic_morality.adapters.langchain_adapter import LangChainAdapter
from socratic_morality.adapters.autogen_adapter import AutoGenAdapter
from socratic_morality.adapters.crewai_adapter import CrewAIAdapter
from socratic_morality.governor.decision import DecisionType


@pytest.fixture
def mock_governor():
    """Create a mock Governor."""
    governor = AsyncMock()
    governor.evaluate = AsyncMock()
    return governor


@pytest.fixture
def langchain_adapter(mock_governor):
    """Create LangChain adapter."""
    return LangChainAdapter(mock_governor)


@pytest.fixture
def autogen_adapter(mock_governor):
    """Create AutoGen adapter."""
    return AutoGenAdapter(mock_governor)


@pytest.fixture
def crewai_adapter(mock_governor):
    """Create CrewAI adapter."""
    return CrewAIAdapter(mock_governor)


class TestLangChainAdapter:
    """Tests for LangChain adapter."""

    @pytest.mark.asyncio
    async def test_langchain_wrap_agent(self, langchain_adapter, mock_governor):
        """Test wrapping a LangChain agent."""
        mock_agent = MagicMock()
        mock_agent.name = "test_agent"
        mock_agent.invoke = MagicMock(return_value="result")

        mock_decision = MagicMock()
        mock_decision.allowed = True
        mock_decision.decision_type = DecisionType.ALLOW
        mock_decision.reasoning = "Action allowed"
        mock_decision.violations = []
        mock_decision.requires_escalation = MagicMock(return_value=False)

        mock_governor.evaluate.return_value = mock_decision

        wrapped_agent = await langchain_adapter.wrap_agent(mock_agent)
        assert hasattr(wrapped_agent, "governed_invoke")

    @pytest.mark.asyncio
    async def test_langchain_intercept_allowed(self, langchain_adapter, mock_governor):
        """Test intercepting an allowed action."""
        mock_decision = MagicMock()
        mock_decision.allowed = True
        mock_decision.decision_type = DecisionType.ALLOW
        mock_decision.reasoning = "Action allowed"
        mock_decision.violations = []
        mock_decision.requires_escalation = MagicMock(return_value=False)

        mock_governor.evaluate.return_value = mock_decision

        result = await langchain_adapter.intercept_action(
            action="test action", agent_name="test_agent"
        )

        assert result["allowed"] is True
        assert result["decision_type"] == DecisionType.ALLOW


class TestAutoGenAdapter:
    """Tests for AutoGen adapter."""

    @pytest.mark.asyncio
    async def test_autogen_wrap_agent(self, autogen_adapter, mock_governor):
        """Test wrapping an AutoGen agent."""
        mock_agent = MagicMock()
        mock_agent.name = "autogen_test"
        mock_agent.generate_reply = AsyncMock(return_value="reply")

        mock_decision = MagicMock()
        mock_decision.allowed = True
        mock_decision.decision_type = DecisionType.ALLOW
        mock_decision.reasoning = "Action allowed"
        mock_decision.violations = []
        mock_decision.requires_escalation = MagicMock(return_value=False)

        mock_governor.evaluate.return_value = mock_decision

        wrapped_agent = await autogen_adapter.wrap_agent(mock_agent)
        assert hasattr(wrapped_agent, "governed_generate_reply")

    @pytest.mark.asyncio
    async def test_autogen_intercept(self, autogen_adapter, mock_governor):
        """Test intercepting an AutoGen action."""
        mock_decision = MagicMock()
        mock_decision.allowed = True
        mock_decision.decision_type = DecisionType.ALLOW
        mock_decision.reasoning = "Action allowed"
        mock_decision.violations = []
        mock_decision.requires_escalation = MagicMock(return_value=False)

        mock_governor.evaluate.return_value = mock_decision

        result = await autogen_adapter.intercept_action(
            action="reply to message", agent_name="autogen_agent"
        )

        assert result["allowed"] is True


class TestCrewAIAdapter:
    """Tests for CrewAI adapter."""

    @pytest.mark.asyncio
    async def test_crewai_wrap_agent(self, crewai_adapter, mock_governor):
        """Test wrapping a CrewAI agent."""
        mock_agent = MagicMock()
        mock_agent.role = "researcher"
        mock_agent.goal = "Find information"
        mock_agent.execute_task = AsyncMock(return_value="task result")

        mock_decision = MagicMock()
        mock_decision.allowed = True
        mock_decision.decision_type = DecisionType.ALLOW
        mock_decision.reasoning = "Action allowed"
        mock_decision.violations = []
        mock_decision.requires_escalation = MagicMock(return_value=False)

        mock_governor.evaluate.return_value = mock_decision

        wrapped_agent = await crewai_adapter.wrap_agent(mock_agent)
        assert hasattr(wrapped_agent, "governed_execute_task")

    @pytest.mark.asyncio
    async def test_crewai_intercept(self, crewai_adapter, mock_governor):
        """Test intercepting a CrewAI action."""
        mock_decision = MagicMock()
        mock_decision.allowed = True
        mock_decision.decision_type = DecisionType.ALLOW
        mock_decision.reasoning = "Action allowed"
        mock_decision.violations = []
        mock_decision.requires_escalation = MagicMock(return_value=False)

        mock_governor.evaluate.return_value = mock_decision

        result = await crewai_adapter.intercept_action(
            action="execute research task", agent_name="researcher"
        )

        assert result["allowed"] is True
