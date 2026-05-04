"""Comprehensive tests for moral precedent engine."""
import pytest
from socratic_morality.precedent.engine import MoralPrecedentEngine


@pytest.fixture
async def precedent_engine():
    """Create moral precedent engine."""
    return MoralPrecedentEngine(storage_type="memory")


class TestPrecedentStorage:
    """Tests for precedent case storage."""

    @pytest.mark.asyncio
    async def test_store_case(self, precedent_engine):
        """Test storing a precedent case."""
        case_id = await precedent_engine.store_case(
            action="allow user access",
            decision=type('Decision', (), {
                'decision_type': 'ALLOW',
                'allowed': True,
                'context': {'user_id': 'user1'},
                'high_impact': False,
                'actor': 'system'
            })(),
            reasoning="User authenticated and authorized",
            principles_cited=["transparency", "autonomy"],
            stakeholders_affected=["user"]
        )

        assert case_id is not None
        assert case_id.startswith("case_")

    @pytest.mark.asyncio
    async def test_retrieve_case(self, precedent_engine):
        """Test retrieving a stored case."""
        case_id = await precedent_engine.store_case(
            action="test action",
            decision=type('Decision', (), {
                'decision_type': 'ALLOW',
                'allowed': True,
                'context': {},
                'high_impact': False,
                'actor': 'test_actor'
            })(),
            reasoning="test reasoning",
            principles_cited=["test_principle"]
        )

        case = await precedent_engine.get_case(case_id)
        assert case is not None
        assert case["action"] == "test action"
        assert case["reasoning"] == "test reasoning"

    @pytest.mark.asyncio
    async def test_store_multiple_cases(self, precedent_engine):
        """Test storing multiple cases."""
        for i in range(5):
            await precedent_engine.store_case(
                action=f"action_{i}",
                decision=type('Decision', (), {
                    'decision_type': 'ALLOW' if i % 2 == 0 else 'DENY',
                    'allowed': i % 2 == 0,
                    'context': {},
                    'high_impact': False,
                    'actor': f'actor_{i}'
                })(),
                reasoning=f"reasoning_{i}"
            )

        all_cases = await precedent_engine.get_all_cases()
        assert len(all_cases) == 5


class TestSimilaritySearch:
    """Tests for case similarity search."""

    @pytest.mark.asyncio
    async def test_find_similar_cases(self, precedent_engine):
        """Test finding similar cases."""
        await precedent_engine.store_case(
            action="read file from disk",
            decision=type('Decision', (), {
                'decision_type': 'ALLOW',
                'allowed': True,
                'context': {},
                'high_impact': False,
                'actor': 'system'
            })(),
            reasoning="Standard read operation"
        )

        await precedent_engine.store_case(
            action="read data from database",
            decision=type('Decision', (), {
                'decision_type': 'ALLOW',
                'allowed': True,
                'context': {},
                'high_impact': False,
                'actor': 'system'
            })(),
            reasoning="Database query"
        )

        similar = await precedent_engine.find_similar_cases("read file")
        assert len(similar) > 0

    @pytest.mark.asyncio
    async def test_similarity_scoring(self, precedent_engine):
        """Test that similarity scores are calculated."""
        await precedent_engine.store_case(
            action="user login with password",
            decision=type('Decision', (), {
                'decision_type': 'ALLOW',
                'allowed': True,
                'context': {},
                'high_impact': False,
                'actor': 'auth'
            })(),
            reasoning="Authentication"
        )

        similar = await precedent_engine.find_similar_cases("user login")
        assert len(similar) > 0
        assert "similarity_score" in similar[0]
        assert 0 <= similar[0]["similarity_score"] <= 1.0


class TestPrincipleSearch:
    """Tests for searching by principle."""

    @pytest.mark.asyncio
    async def test_search_by_principle(self, precedent_engine):
        """Test searching cases by principle."""
        await precedent_engine.store_case(
            action="grant user access",
            decision=type('Decision', (), {
                'decision_type': 'ALLOW',
                'allowed': True,
                'context': {},
                'high_impact': False,
                'actor': 'system'
            })(),
            reasoning="User authorized",
            principles_cited=["autonomy", "transparency"]
        )

        autonomy_cases = await precedent_engine.search_by_principle("autonomy")
        assert len(autonomy_cases) >= 1


class TestStatistics:
    """Tests for precedent statistics."""

    @pytest.mark.asyncio
    async def test_get_statistics(self, precedent_engine):
        """Test getting case statistics."""
        for i in range(3):
            await precedent_engine.store_case(
                action=f"action_{i}",
                decision=type('Decision', (), {
                    'decision_type': 'ALLOW',
                    'allowed': True,
                    'context': {},
                    'high_impact': False,
                    'actor': 'system'
                })(),
                reasoning="allowed"
            )

        for i in range(2):
            await precedent_engine.store_case(
                action=f"denied_action_{i}",
                decision=type('Decision', (), {
                    'decision_type': 'DENY',
                    'allowed': False,
                    'context': {},
                    'high_impact': False,
                    'actor': 'system'
                })(),
                reasoning="denied"
            )

        stats = await precedent_engine.get_statistics()
        assert stats["total_cases"] == 5
        assert stats["allowed_decisions"] == 3
        assert stats["denied_decisions"] == 2
        assert stats["decision_rate"] == 0.6

    @pytest.mark.asyncio
    async def test_statistics_empty_engine(self, precedent_engine):
        """Test statistics on empty engine."""
        stats = await precedent_engine.get_statistics()
        assert stats["total_cases"] == 0
        assert stats["allowed_decisions"] == 0
        assert stats["denied_decisions"] == 0
