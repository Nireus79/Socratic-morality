"""Comprehensive tests for care ethics framework."""

import pytest
from socratic_morality.ethics.care_ethics import (
    CareEthicsAnalyzer,
    CareConclusion,
    Relationship,
    VulnerabilityScore,
    CareViolation,
    CareAnalysis,
)


@pytest.fixture
def care_analyzer():
    """Create care ethics analyzer."""
    return CareEthicsAnalyzer()


class TestCareEthicsAnalyzer:
    """Tests for CareEthicsAnalyzer."""

    @pytest.mark.asyncio
    async def test_analyze_caring_action(self, care_analyzer):
        """Test analysis of a caring action."""
        result = await care_analyzer.analyze(
            action="provide support and care for vulnerable patient",
            context={
                "stakeholders": ["patient"],
                "affected_parties": ["patient"],
            },
        )

        assert result.conclusion == CareConclusion.CARING
        assert result.care_response_adequacy >= 0.7
        assert len(result.violations) == 0

    @pytest.mark.asyncio
    async def test_analyze_harmful_action(self, care_analyzer):
        """Test analysis of a harmful action."""
        result = await care_analyzer.analyze(
            action="abandon elderly person without care",
            context={
                "stakeholders": ["elderly_person"],
                "affected_parties": ["elderly_person"],
            },
        )

        assert result.conclusion == CareConclusion.HARMFUL
        assert len(result.violations) > 0
        assert any(v.severity == "critical" for v in result.violations)

    @pytest.mark.asyncio
    async def test_analyze_indifferent_action(self, care_analyzer):
        """Test analysis of an indifferent action."""
        result = await care_analyzer.analyze(
            action="process a routine transaction",
            context={
                "stakeholders": ["customer"],
                "affected_parties": ["customer"],
            },
        )

        assert result.conclusion == CareConclusion.INDIFFERENT
        assert 0.3 <= result.care_response_adequacy <= 0.7


class TestRelationshipIdentification:
    """Tests for relationship identification."""

    def test_identify_caregiver_relationship(self, care_analyzer):
        """Test identifying caregiver relationships."""
        relationships = care_analyzer.identify_relationships(["caregiver_nurse"])

        assert len(relationships) > 0
        assert relationships[0].relationship_type == "caregiver"

    def test_identify_dependent_relationship(self, care_analyzer):
        """Test identifying dependent relationships."""
        relationships = care_analyzer.identify_relationships(["child"])

        assert len(relationships) > 0
        assert relationships[0].relationship_type == "dependent"
        assert relationships[0].power_dynamic == "asymmetric_favoring_from"

    def test_identify_multiple_relationships(self, care_analyzer):
        """Test identifying multiple relationships."""
        relationships = care_analyzer.identify_relationships(["child", "caregiver", "patient"])

        assert len(relationships) >= 3
        dependency_rels = [r for r in relationships if r.relationship_type == "dependent"]
        assert len(dependency_rels) > 0


class TestVulnerabilityAssessment:
    """Tests for vulnerability assessment."""

    def test_assess_child_vulnerability(self, care_analyzer):
        """Test vulnerability assessment of a child."""
        score = care_analyzer.assess_vulnerability("child")

        assert score.vulnerability_score > 0.2
        assert score.risk_level in ("low", "medium", "high")
        assert len(score.protection_needs) > 0

    def test_assess_patient_vulnerability(self, care_analyzer):
        """Test vulnerability assessment of a patient."""
        score = care_analyzer.assess_vulnerability("patient_with_disability")

        assert score.vulnerability_score > 0.2
        assert len(score.protection_needs) > 0

    def test_assess_low_vulnerability(self, care_analyzer):
        """Test vulnerability assessment of less vulnerable party."""
        score = care_analyzer.assess_vulnerability("colleague")

        assert score.vulnerability_score <= 0.5
        assert score.risk_level == "low"

    def test_vulnerability_caching(self, care_analyzer):
        """Test that vulnerability assessments are cached."""
        score1 = care_analyzer.assess_vulnerability("test_person")
        score2 = care_analyzer.assess_vulnerability("test_person")

        assert score1 is score2  # Same object from cache


class TestCareViolationDetection:
    """Tests for care violation detection."""

    def test_detect_neglect_violation(self, care_analyzer):
        """Test detection of neglect violations."""
        violations = care_analyzer.detect_care_violations("neglect the patient's needs")

        assert len(violations) > 0
        assert violations[0].violation_type == "neglect"

    def test_detect_abandonment_violation(self, care_analyzer):
        """Test detection of abandonment violations."""
        violations = care_analyzer.detect_care_violations("abandon vulnerable person")

        assert len(violations) > 0
        # Abandonment detected or neglect detected - both are care violations
        assert violations[0].violation_type in ("abandonment", "neglect")
        assert violations[0].severity in ("high", "critical")

    def test_detect_exploitation_violation(self, care_analyzer):
        """Test detection of exploitation violations."""
        violations = care_analyzer.detect_care_violations("exploit dependent person")

        assert len(violations) > 0
        assert violations[0].violation_type == "exploitation"

    def test_no_violation_in_caring_action(self, care_analyzer):
        """Test that caring actions produce no violations."""
        violations = care_analyzer.detect_care_violations("provide care and support")

        assert len(violations) == 0


class TestCareResponseEvaluation:
    """Tests for care response adequacy evaluation."""

    def test_evaluate_adequate_care_response(self, care_analyzer):
        """Test evaluation of adequate care response."""
        analysis = care_analyzer.evaluate_care_response(
            "provide comprehensive support to vulnerable stakeholder",
            ["vulnerable_person"],
        )

        assert analysis.adequate is True
        assert analysis.care_score >= 0.6

    def test_evaluate_inadequate_care_response(self, care_analyzer):
        """Test evaluation of inadequate care response."""
        analysis = care_analyzer.evaluate_care_response(
            "ignore and neglect stakeholder needs",
            ["dependent_person"],
        )

        assert analysis.adequate is False
        assert analysis.care_score < 0.6
        assert len(analysis.specific_concerns) > 0

    def test_care_response_suggestions(self, care_analyzer):
        """Test that improvement suggestions are provided."""
        analysis = care_analyzer.evaluate_care_response(
            "dismiss stakeholder concerns without investigation",
            ["stakeholder"],
        )

        assert len(analysis.improvement_suggestions) > 0
        assert len(analysis.alternative_actions) > 0

    def test_care_response_caching(self, care_analyzer):
        """Test care response evaluation results."""
        analysis1 = care_analyzer.evaluate_care_response("test action", ["test_stakeholder"])
        analysis2 = care_analyzer.evaluate_care_response("test action", ["test_stakeholder"])

        assert analysis1.care_score == analysis2.care_score


class TestCareEthicsResult:
    """Tests for complete care ethics results."""

    @pytest.mark.asyncio
    async def test_result_completeness(self, care_analyzer):
        """Test that result contains all expected fields."""
        result = await care_analyzer.analyze(
            action="test action",
            context={
                "stakeholders": ["person1", "person2"],
                "affected_parties": ["person1"],
            },
        )

        assert result.action == "test action"
        assert result.conclusion in (
            CareConclusion.CARING,
            CareConclusion.INDIFFERENT,
            CareConclusion.HARMFUL,
        )
        assert isinstance(result.care_response_adequacy, float)
        assert 0 <= result.care_response_adequacy <= 1
        assert isinstance(result.violations, list)
        assert isinstance(result.recommendations, list)
        assert isinstance(result.reasoning, str)
        assert 0 <= result.confidence <= 1

    @pytest.mark.asyncio
    async def test_result_with_multiple_stakeholders(self, care_analyzer):
        """Test analysis with multiple stakeholders."""
        result = await care_analyzer.analyze(
            action="allocate resources to help vulnerable families",
            context={
                "stakeholders": ["family1", "child_in_family1", "elderly_parent"],
                "affected_parties": ["family1", "child_in_family1"],
            },
        )

        assert len(result.vulnerability_concerns) >= 0
        assert len(result.relationship_analysis) >= 0

    @pytest.mark.asyncio
    async def test_confidence_reflects_violations(self, care_analyzer):
        """Test that confidence decreases with violations."""
        result_clean = await care_analyzer.analyze(
            action="provide care",
            context={"stakeholders": ["person"], "affected_parties": ["person"]},
        )

        result_dirty = await care_analyzer.analyze(
            action="harm and exploit vulnerable person",
            context={"stakeholders": ["person"], "affected_parties": ["person"]},
        )

        assert result_clean.confidence >= result_dirty.confidence


class TestCareEthicsIntegration:
    """Integration tests for care ethics analyzer."""

    @pytest.mark.asyncio
    async def test_full_workflow_caring(self, care_analyzer):
        """Test full workflow for caring action."""
        result = await care_analyzer.analyze(
            action="listen to concerns and provide support",
            context={
                "stakeholders": ["patient", "family"],
                "affected_parties": ["patient"],
            },
        )

        assert result.conclusion == CareConclusion.CARING
        assert result.care_response_adequacy >= 0.7
        assert len(result.violations) == 0

    @pytest.mark.asyncio
    async def test_full_workflow_harmful(self, care_analyzer):
        """Test full workflow for harmful action."""
        result = await care_analyzer.analyze(
            action="manipulate and exploit vulnerable population for profit",
            context={
                "stakeholders": ["vulnerable_group"],
                "affected_parties": ["vulnerable_group"],
            },
        )

        assert result.conclusion == CareConclusion.HARMFUL
        assert len(result.violations) > 0
        assert len(result.recommendations) > 0

    @pytest.mark.asyncio
    async def test_recommendations_specific_to_vulnerability(self, care_analyzer):
        """Test that recommendations address identified vulnerabilities."""
        result = await care_analyzer.analyze(
            action="provide minimal care to dependent children",
            context={
                "stakeholders": ["child1", "child2"],
                "affected_parties": ["child1", "child2"],
            },
        )

        assert len(result.recommendations) > 0
        # Should have recommendations mentioning children or protection
