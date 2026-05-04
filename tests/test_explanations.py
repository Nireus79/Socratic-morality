"""Tests for explanation generation."""

import pytest
from socratic_morality.ethics.explanations import ExplanationGenerator


@pytest.fixture
def gen():
    return ExplanationGenerator()


@pytest.fixture
def allowed_decision():
    return {
        "allowed": True,
        "confidence": 0.85,
        "concerns": None,
        "stakeholders": ["user:user123"],
        "frameworks": {
            "kantian": {"allowed": True, "principle": "Categorical Imperative"},
            "rights_based": {"allowed": True, "principle": "Human Agency"},
        },
    }


@pytest.fixture
def denied_decision():
    return {
        "allowed": False,
        "confidence": 0.9,
        "concerns": "kantian: Violates duty; rights_based: Violates consent",
        "stakeholders": ["user:user123", "org:org456"],
        "frameworks": {
            "kantian": {
                "allowed": False,
                "principle": "Categorical Imperative",
                "concerns": "Treats as means",
            },
            "rights_based": {
                "allowed": False,
                "principle": "Human Agency",
                "concerns": "Violates autonomy",
            },
        },
    }


class TestHeadlineGeneration:
    def test_allowed_high_confidence(self, gen):
        headline = gen._generate_headline(True, 0.95)
        assert "approved" in headline.lower() or "decision" in headline.lower()

    def test_denied_high_confidence(self, gen):
        headline = gen._generate_headline(False, 0.95)
        assert "denied" in headline.lower()


class TestFrameworksSummary:
    def test_frameworks_summary(self, gen):
        frameworks = {"kantian": {"allowed": True, "principle": "Categorical Imperative"}}
        summary = gen._generate_frameworks_summary(frameworks)
        assert "kantian" in summary.lower()

    def test_empty_frameworks(self, gen):
        summary = gen._generate_frameworks_summary({})
        assert summary == ""


class TestConcernsFormatting:
    def test_format_concerns(self, gen):
        concerns = "kantian: Violates dignity"
        formatted = gen._format_concerns(concerns)
        assert "concerns" in formatted.lower()

    def test_empty_concerns(self, gen):
        formatted = gen._format_concerns(None)
        assert formatted == ""


class TestPrecedentReferences:
    def test_precedent_references(self, gen):
        cases = [{"action": "Action", "allowed": True, "similarity_score": 0.85}]
        text = gen._generate_precedent_references(cases)
        assert "precedent" in text.lower() or "case" in text.lower()

    def test_empty_precedent(self, gen):
        text = gen._generate_precedent_references([])
        assert text == ""


class TestStakeholderAnalysis:
    def test_stakeholder_analysis(self, gen):
        stakeholders = ["user:user123"]
        text = gen._generate_stakeholder_analysis(stakeholders)
        assert "stakeholders" in text.lower()
        assert "user123" in text

    def test_empty_stakeholders(self, gen):
        text = gen._generate_stakeholder_analysis([])
        assert text == ""


class TestConfidenceStatement:
    def test_high_confidence(self, gen):
        text = gen._generate_confidence_statement(0.95)
        assert "95" in text

    def test_low_confidence(self, gen):
        text = gen._generate_confidence_statement(0.35)
        assert "35" in text
        assert "low" in text.lower()


class TestFullExplanation:
    def test_full_explanation_allowed(self, gen, allowed_decision):
        explanation = gen.generate_explanation(allowed_decision)
        assert "approved" in explanation.lower() or "decision" in explanation.lower()

    def test_full_explanation_denied(self, gen, denied_decision):
        explanation = gen.generate_explanation(denied_decision)
        assert "denied" in explanation.lower()


class TestCounterArguments:
    def test_counter_arguments(self, gen):
        decision = {"allowed": True, "confidence": 0.65, "frameworks": {}}
        counter = gen.generate_counter_arguments(decision)

    def test_no_counter_high_confidence(self, gen):
        decision = {"allowed": True, "confidence": 0.95, "frameworks": {}}
        counter = gen.generate_counter_arguments(decision)
        assert counter is None
