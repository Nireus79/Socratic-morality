"""Tests for Constitution framework."""

from socratic_morality.constitution.models import Constitution, Principle, Rule


def test_constitution_from_dict():
    """Test creating Constitution from dictionary."""
    data = {
        "metadata": {"name": "Test"},
        "supreme_principle": "Never do evil",
        "principles": {
            "honesty": {
                "category": "virtue",
                "severity": "critical",
                "description": "Always be truthful",
            }
        },
        "rules": [
            {
                "name": "No Lying",
                "principle": "honesty",
                "condition": "agent tells falsehood",
                "action": "block",
            }
        ],
    }

    constitution = Constitution.from_dict(data)

    assert constitution.supreme_principle == "Never do evil"
    assert "honesty" in constitution.principles
    assert len(constitution.rules) == 1
    assert constitution.rules[0].name == "No Lying"


def test_principle_creation():
    """Test Principle dataclass."""
    principle = Principle(
        name="honesty", category="virtue", severity="critical", description="Be truthful"
    )

    assert principle.name == "honesty"
    assert principle.severity == "critical"


def test_rule_creation():
    """Test Rule dataclass."""
    rule = Rule(
        name="No Deception", principle="honesty", condition="agent deceives", action="block"
    )

    assert rule.name == "No Deception"
    assert rule.action == "block"
