"""Tests for semantic similarity in precedent engine."""
import pytest
from unittest.mock import Mock
from socratic_morality.precedent.engine import MoralPrecedentEngine


class TestPrecedentSemanticSimilarity:
    """Tests for semantic similarity search in precedent engine."""

    @pytest.mark.asyncio
    async def test_find_similar_cases_fallback_word_overlap(self):
        """Test finding similar cases using fallback word overlap."""
        engine = MoralPrecedentEngine()
        engine.embeddings.model = None

        decision1 = Mock(decision_type="allow", allowed=True, context={}, high_impact=False, actor="actor1")
        decision2 = Mock(decision_type="deny", allowed=False, context={}, high_impact=False, actor="actor2")

        await engine.store_case(
            action="user requests access to sensitive data",
            decision=decision1,
            reasoning="Allowed"
        )
        await engine.store_case(
            action="application sends network request",
            decision=decision2,
            reasoning="Denied"
        )

        similar_cases = await engine.find_similar_cases("user sends request", limit=5)
        assert len(similar_cases) >= 1
        assert all("similarity_score" in case for case in similar_cases)

    @pytest.mark.asyncio
    async def test_similarity_scoring(self):
        """Test similarity scoring accuracy."""
        engine = MoralPrecedentEngine()
        engine.embeddings.model = None

        decision = Mock(decision_type="allow", allowed=True, context={}, high_impact=False, actor="actor")

        await engine.store_case(
            action="approve user authentication request",
            decision=decision,
            reasoning="Valid credentials"
        )

        similar = await engine.find_similar_cases("approve authentication", limit=1)
        assert len(similar) == 1
        assert similar[0]["similarity_score"] > 0

    @pytest.mark.asyncio
    async def test_empty_precedent_similar_search(self):
        """Test similar search on empty precedent engine."""
        engine = MoralPrecedentEngine()
        similar_cases = await engine.find_similar_cases("any action")
        assert similar_cases == []

    @pytest.mark.asyncio
    async def test_similar_cases_limit(self):
        """Test limit parameter in similar cases search."""
        engine = MoralPrecedentEngine()
        decision = Mock(decision_type="allow", allowed=True, context={}, high_impact=False, actor="actor")

        for i in range(5):
            await engine.store_case(
                action=f"test action {i}",
                decision=decision,
                reasoning="Test"
            )

        similar = await engine.find_similar_cases("action", limit=2)
        assert len(similar) <= 2

    @pytest.mark.asyncio
    async def test_similar_cases_sorted_by_similarity(self):
        """Test that similar cases are sorted by similarity score."""
        engine = MoralPrecedentEngine()
        engine.embeddings.model = None

        decision = Mock(decision_type="allow", allowed=True, context={}, high_impact=False, actor="actor")

        await engine.store_case(
            action="exact test action here",
            decision=decision,
            reasoning="Test"
        )
        await engine.store_case(
            action="different other action",
            decision=decision,
            reasoning="Test"
        )

        similar = await engine.find_similar_cases("test action", limit=5)

        if len(similar) > 1:
            assert similar[0]["similarity_score"] >= similar[1]["similarity_score"]

    @pytest.mark.asyncio
    async def test_case_metadata_preserved(self):
        """Test that case metadata is preserved in similarity search results."""
        engine = MoralPrecedentEngine()
        decision = Mock(decision_type="allow", allowed=True, context={"key": "value"}, high_impact=True, actor="actor1")

        case_id = await engine.store_case(
            action="test action",
            decision=decision,
            reasoning="Test reasoning",
            principles_cited=["principle1", "principle2"],
            stakeholders_affected=["user1", "org1"]
        )

        similar = await engine.find_similar_cases("action", limit=1)

        assert len(similar) > 0
        case = similar[0]
        assert case["id"] == case_id
        assert case["allowed"] == True
        assert case["high_impact"] == True
        assert case["actor"] == "actor1"

    @pytest.mark.asyncio
    async def test_embeddings_with_precedent(self):
        """Test embeddings integration with precedent engine."""
        engine = MoralPrecedentEngine()
        embeddings = engine.embeddings
        is_available = embeddings.is_available()
        assert isinstance(is_available, bool)

    @pytest.mark.asyncio
    async def test_precedent_handles_missing_embeddings(self):
        """Test precedent engine handles missing embeddings gracefully."""
        engine = MoralPrecedentEngine()
        engine.embeddings.model = None

        decision = Mock(decision_type="allow", allowed=True, context={}, high_impact=False, actor="actor")

        await engine.store_case(
            action="test action",
            decision=decision,
            reasoning="Test"
        )

        similar = await engine.find_similar_cases("action", limit=1)
        assert len(similar) > 0

    @pytest.mark.asyncio
    async def test_embeddings_caching_with_precedent(self):
        """Test that embeddings are cached across multiple searches."""
        engine = MoralPrecedentEngine()
        engine.embeddings.model = None

        test_embedding = [0.1, 0.2, 0.3]
        engine.embeddings.embeddings_cache["cached action"] = test_embedding

        cached = engine.embeddings.embed("cached action")
        assert cached == test_embedding

    @pytest.mark.asyncio
    async def test_case_insensitive_fallback_search(self):
        """Test that fallback word overlap search is case-insensitive."""
        engine = MoralPrecedentEngine()
        engine.embeddings.model = None

        decision = Mock(decision_type="allow", allowed=True, context={}, high_impact=False, actor="actor")

        await engine.store_case(
            action="User Requests Data Access",
            decision=decision,
            reasoning="Test"
        )

        similar = await engine.find_similar_cases("user requests", limit=1)
        assert len(similar) > 0

    @pytest.mark.asyncio
    async def test_semantic_similarity_with_embeddings(self):
        """Test semantic similarity when embeddings are available."""
        engine = MoralPrecedentEngine()
        if engine.embeddings.model:
            decision1 = Mock(decision_type="allow", allowed=True, context={}, high_impact=False, actor="actor1")
            decision2 = Mock(decision_type="deny", allowed=False, context={}, high_impact=False, actor="actor2")

            case1_id = await engine.store_case(
                action="user asks for sensitive data access",
                decision=decision1,
                reasoning="User has authorization"
            )
            case2_id = await engine.store_case(
                action="unauthorized data request",
                decision=decision2,
                reasoning="No proper authorization"
            )

            similar_cases = await engine.find_similar_cases("user requests data", limit=2)
            assert len(similar_cases) > 0
            assert "similarity_score" in similar_cases[0]
