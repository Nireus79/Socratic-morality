"""Comprehensive tests for ethical deliberation engine."""

import pytest
from socratic_morality.ethics.deliberation import EthicalDeliberationEngine


@pytest.fixture
def deliberation_engine():
    """Create ethical deliberation engine."""
    return EthicalDeliberationEngine(llm_provider="anthropic")


class TestKantianAnalysis:
    """Tests for Kantian ethical analysis."""

    @pytest.mark.asyncio
    async def test_kantian_allows_honest_action(self, deliberation_engine):
        """Test that Kantian analysis allows honest actions."""
        result = await deliberation_engine.analyze(
            action="provide truthful information",
            purpose="help user make decision",
            actor="assistant",
            context={},
        )
        assert result["frameworks"]["kantian"]["allowed"] is True

    @pytest.mark.asyncio
    async def test_kantian_denies_manipulation(self, deliberation_engine):
        """Test that Kantian analysis denies manipulation."""
        result = await deliberation_engine.analyze(
            action="manipulate user", purpose="achieve goal", actor="assistant", context={}
        )
        assert result["frameworks"]["kantian"]["allowed"] is False


class TestRightsBasedAnalysis:
    """Tests for rights-based ethical analysis."""

    @pytest.mark.asyncio
    async def test_rights_denies_without_consent(self, deliberation_engine):
        """Test rights-based analysis denies actions without consent."""
        result = await deliberation_engine.analyze(
            action="access data without consent",
            purpose="improve system",
            actor="assistant",
            context={},
        )
        assert result["frameworks"]["rights_based"]["allowed"] is False


class TestSynthesizedAnalysis:
    """Tests for synthesized multi-framework analysis."""

    @pytest.mark.asyncio
    async def test_all_frameworks_included(self, deliberation_engine):
        """Test that all frameworks are analyzed."""
        result = await deliberation_engine.analyze(
            action="provide helpful information",
            purpose="assist user",
            actor="assistant",
            context={"user_id": "user123"},
        )

        assert "kantian" in result["frameworks"]
        assert "utilitarian" in result["frameworks"]
        assert "virtue_ethics" in result["frameworks"]
        assert "rights_based" in result["frameworks"]

    @pytest.mark.asyncio
    async def test_overall_denied_when_any_denies(self, deliberation_engine):
        """Test overall decision is denied when any framework denies."""
        result = await deliberation_engine.analyze(
            action="manipulate user without consent",
            purpose="achieve goal",
            actor="assistant",
            context={},
        )
        assert result["allowed"] is False

    @pytest.mark.asyncio
    async def test_confidence_property(self, deliberation_engine):
        """Test confidence is calculated across frameworks."""
        result = await deliberation_engine.analyze(
            action="process data", purpose="assist", actor="assistant", context={}
        )
        assert 0 <= result["confidence"] <= 1.0
