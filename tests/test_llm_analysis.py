"""Tests for LLM-based ethical analysis."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from socratic_morality.ethics.llm_analysis import LLMEthicalAnalyzer

@pytest.fixture
def mock_llm_client():
    client = AsyncMock()
    return client

@pytest.fixture
def llm_analyzer(mock_llm_client):
    return LLMEthicalAnalyzer(llm_client=mock_llm_client)

@pytest.fixture
def llm_analyzer_no_client():
    return LLMEthicalAnalyzer(llm_client=None)

class TestKantianAnalysis:
    @pytest.mark.asyncio
    async def test_kantian_with_llm(self, llm_analyzer, mock_llm_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"allowed": false}')]
        mock_llm_client.messages.create.return_value = mock_response
        result = await llm_analyzer.analyze_kantian("manipulate user", ["user"], {})
        assert result['allowed'] is False

    @pytest.mark.asyncio
    async def test_kantian_fallback_violation(self, llm_analyzer_no_client):
        result = await llm_analyzer_no_client.analyze_kantian("manipulate user", ["user"], {})
        assert result['allowed'] is False

    @pytest.mark.asyncio
    async def test_kantian_fallback_allow(self, llm_analyzer_no_client):
        result = await llm_analyzer_no_client.analyze_kantian("provide information", ["user"], {})
        assert result['allowed'] is True

class TestUtilitarianAnalysis:
    @pytest.mark.asyncio
    async def test_utilitarian_with_llm(self, llm_analyzer, mock_llm_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"allowed": true}')]
        mock_llm_client.messages.create.return_value = mock_response
        result = await llm_analyzer.analyze_utilitarian("help user", {})
        assert result['allowed'] is True

    @pytest.mark.asyncio
    async def test_utilitarian_fallback(self, llm_analyzer_no_client):
        result = await llm_analyzer_no_client.analyze_utilitarian("help user", {})
        assert result['allowed'] is True

class TestVirtueEthicsAnalysis:
    @pytest.mark.asyncio
    async def test_virtue_with_llm(self, llm_analyzer, mock_llm_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"allowed": false}')]
        mock_llm_client.messages.create.return_value = mock_response
        result = await llm_analyzer.analyze_virtue_ethics("deceive user", "agent", {})
        assert result['allowed'] is False

    @pytest.mark.asyncio
    async def test_virtue_fallback(self, llm_analyzer_no_client):
        result = await llm_analyzer_no_client.analyze_virtue_ethics("process data", "agent", {})
        assert result['allowed'] is True

class TestRightsBasedAnalysis:
    @pytest.mark.asyncio
    async def test_rights_with_llm(self, llm_analyzer, mock_llm_client):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"allowed": false}')]
        mock_llm_client.messages.create.return_value = mock_response
        result = await llm_analyzer.analyze_rights_based("override decision", {})
        assert result['allowed'] is False

    @pytest.mark.asyncio
    async def test_rights_fallback(self, llm_analyzer_no_client):
        result = await llm_analyzer_no_client.analyze_rights_based("process data", {})
        assert result['allowed'] is True

class TestJSONExtraction:
    def test_extract_valid_json(self):
        analyzer = LLMEthicalAnalyzer()
        text = 'Some text {"allowed": true} more text'
        result = analyzer._extract_json(text)
        assert result is not None

    def test_extract_invalid_json(self):
        analyzer = LLMEthicalAnalyzer()
        text = 'No json here'
        result = analyzer._extract_json(text)
        assert result is None

class TestFrameworkResults:
    @pytest.mark.asyncio
    async def test_all_frameworks_have_required_fields(self, llm_analyzer_no_client):
        k = await llm_analyzer_no_client.analyze_kantian("test", [], {})
        u = await llm_analyzer_no_client.analyze_utilitarian("test", {})
        v = await llm_analyzer_no_client.analyze_virtue_ethics("test", "agent", {})
        r = await llm_analyzer_no_client.analyze_rights_based("test", {})
        
        for result in [k, u, v, r]:
            assert 'allowed' in result
            assert 'confidence' in result
            assert 0 <= result['confidence'] <= 1.0
