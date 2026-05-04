"""Real framework adapter integration tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from socratic_morality.adapters.langchain_adapter import LangChainAdapter
from socratic_morality.adapters.autogen_adapter import AutoGenAdapter
from socratic_morality.adapters.crewai_adapter import CrewAIAdapter
from socratic_morality.governor.decision import DecisionType


@pytest.fixture
def mock_governor():
    """Create mock Governor."""
    governor = AsyncMock()
    decision = MagicMock()
    decision.allowed = True
    decision.decision_type = DecisionType.ALLOW
    decision.reasoning = "Allowed"
    decision.violations = []
    decision.requires_escalation = MagicMock(return_value=False)
    governor.evaluate.return_value = decision
    return governor


class TestLangChainIntegration:
    """Tests for LangChain framework integration."""

    @pytest.mark.asyncio
    async def test_langchain_agent_wrapping(self, mock_governor):
        """Test wrapping a LangChain agent."""
        adapter = LangChainAdapter(mock_governor)
        mock_agent = MagicMock()
        mock_agent.name = "test_agent"
        wrapped_agent = await adapter.wrap_agent(mock_agent)
        assert hasattr(wrapped_agent, "governed_invoke")

    @pytest.mark.asyncio
    async def test_langchain_action_interception(self, mock_governor):
        """Test intercepting LangChain action."""
        adapter = LangChainAdapter(mock_governor)
        result = await adapter.intercept_action(action="test", agent_name="agent")
        assert result["allowed"] is True
        mock_governor.evaluate.assert_called()


class TestAutoGenIntegration:
    """Tests for AutoGen framework integration."""

    @pytest.mark.asyncio
    async def test_autogen_agent_wrapping(self, mock_governor):
        """Test wrapping an AutoGen agent."""
        adapter = AutoGenAdapter(mock_governor)
        mock_agent = MagicMock()
        mock_agent.name = "autogen_agent"
        wrapped_agent = await adapter.wrap_agent(mock_agent)
        assert hasattr(wrapped_agent, "governed_generate_reply")

    @pytest.mark.asyncio
    async def test_autogen_action_interception(self, mock_governor):
        """Test intercepting AutoGen action."""
        adapter = AutoGenAdapter(mock_governor)
        result = await adapter.intercept_action(action="test", agent_name="agent")
        assert result["allowed"] is True


class TestCrewAIIntegration:
    """Tests for CrewAI framework integration."""

    @pytest.mark.asyncio
    async def test_crewai_agent_wrapping(self, mock_governor):
        """Test wrapping a CrewAI agent."""
        adapter = CrewAIAdapter(mock_governor)
        mock_agent = MagicMock()
        mock_agent.role = "researcher"
        wrapped_agent = await adapter.wrap_agent(mock_agent)
        assert hasattr(wrapped_agent, "governed_execute_task")

    @pytest.mark.asyncio
    async def test_crewai_action_interception(self, mock_governor):
        """Test intercepting CrewAI action."""
        adapter = CrewAIAdapter(mock_governor)
        result = await adapter.intercept_action(action="test", agent_name="agent")
        assert result["allowed"] is True
