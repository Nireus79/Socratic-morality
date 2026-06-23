"""Care Ethics Framework for relational and context-aware moral analysis."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class CareConclusion(str, Enum):
    """Conclusions from care ethics analysis."""

    CARING = "caring"
    INDIFFERENT = "indifferent"
    HARMFUL = "harmful"


@dataclass
class Relationship:
    """Represents a relationship between parties."""

    from_party: str
    to_party: str
    relationship_type: str = "general"  # caregiver, dependent, peer, etc.
    power_dynamic: str = "equal"  # equal, asymmetric_favoring_from, asymmetric_favoring_to
    vulnerability_level: str = "low"  # low, medium, high
    care_history: str = ""  # previous care interactions


@dataclass
class VulnerabilityScore:
    """Assessment of a stakeholder's vulnerability."""

    stakeholder: str
    vulnerability_score: float  # 0-1, higher means more vulnerable
    vulnerability_factors: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    protection_needs: List[str] = field(default_factory=list)
    risk_level: str = "low"  # low, medium, high


@dataclass
class CareViolation:
    """Represents a violation of care ethics principles."""

    violation_type: str  # neglect, abandonment, harm, exploitation, misuse_of_power
    affected_party: str
    description: str
    severity: str = "medium"  # low, medium, high, critical
    harm_assessment: str = ""


@dataclass
class CareAnalysis:
    """Analysis of action's adequacy in care response."""

    action_description: str
    adequate: bool
    care_score: float  # 0-1, higher means more caring
    specific_concerns: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)
    alternative_actions: List[str] = field(default_factory=list)


@dataclass
class CareEthicsResult:
    """Complete care ethics analysis result."""

    action: str
    conclusion: CareConclusion
    vulnerability_concerns: List[str] = field(default_factory=list)
    relationship_analysis: List[Relationship] = field(default_factory=list)
    care_response_adequacy: float = 0.5  # 0-1
    violations: List[CareViolation] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    reasoning: str = ""
    confidence: float = 0.8


class CareEthicsAnalyzer:
    """Analyzes actions through care ethics lens.

    Care ethics is a framework emphasizing:
    - Relationships and interdependence matter
    - Vulnerability requires attention and protection
    - Care is a moral priority
    - Context-specific judgment is essential
    - Relational morality (not just individual rights)
    """

    def __init__(self):
        """Initialize care ethics analyzer."""
        self.relationships: Dict[str, List[Relationship]] = {}
        self.vulnerability_assessments: Dict[str, VulnerabilityScore] = {}
        self.care_violation_history: List[CareViolation] = []

    async def analyze(self, action: str, context: Dict[str, Any]) -> CareEthicsResult:
        """Analyze action through care ethics lens.

        Args:
            action: Description of the action to analyze
            context: Contextual information (stakeholders, relationships, etc.)

        Returns:
            CareEthicsResult with comprehensive care ethics analysis
        """
        # Identify all stakeholders affected
        stakeholders = context.get("stakeholders", [])
        if isinstance(stakeholders, str):
            stakeholders = [stakeholders]

        # Step 1: Identify relationships
        relationships = self.identify_relationships(stakeholders)

        # Step 2: Assess vulnerability of each stakeholder
        vulnerability_concerns = []
        vulnerability_assessments = []
        for stakeholder in stakeholders:
            vuln_score = self.assess_vulnerability(stakeholder)
            vulnerability_assessments.append(vuln_score)
            if vuln_score.vulnerability_score >= 0.6:
                vulnerability_concerns.append(
                    f"{stakeholder}: {vuln_score.risk_level.upper()} vulnerability "
                    f"({vuln_score.vulnerability_factors})"
                )

        # Step 3: Evaluate care response adequacy
        affected_parties = context.get("affected_parties", stakeholders)
        care_analysis = self.evaluate_care_response(action, affected_parties)

        # Step 4: Detect care violations
        violations = self.detect_care_violations(action)

        # Step 5: Determine conclusion
        conclusion = self._determine_conclusion(
            care_analysis, violations, vulnerability_assessments
        )

        # Step 6: Generate recommendations
        recommendations = self._generate_recommendations(
            action, vulnerability_assessments, violations
        )

        # Calculate confidence based on evidence
        confidence = 0.8 - (len(violations) * 0.1)
        confidence = max(0.3, min(1.0, confidence))

        return CareEthicsResult(
            action=action,
            conclusion=conclusion,
            vulnerability_concerns=vulnerability_concerns,
            relationship_analysis=relationships,
            care_response_adequacy=care_analysis.care_score,
            violations=violations,
            recommendations=recommendations,
            reasoning=self._generate_reasoning(
                conclusion, violations, care_analysis, vulnerability_assessments
            ),
            confidence=confidence,
        )

    def identify_relationships(self, stakeholders: List[str]) -> List[Relationship]:
        """Map relationships between stakeholders.

        Args:
            stakeholders: List of affected parties

        Returns:
            List of identified relationships
        """
        relationships = []

        # Identify key relationship patterns
        action_keywords = {
            "caregiver": ["care", "support", "help", "protect", "facilitate"],
            "dependent": ["child", "elderly", "vulnerable", "patient", "client"],
            "peer": ["colleague", "friend", "partner", "equal", "team"],
        }

        for stakeholder in stakeholders:
            stakeholder_lower = stakeholder.lower()

            for rel_type, keywords in action_keywords.items():
                if any(kw in stakeholder_lower for kw in keywords):
                    # Determine power dynamic
                    power_dynamic = "equal"
                    if rel_type == "dependent":
                        power_dynamic = "asymmetric_favoring_from"
                    elif rel_type == "caregiver":
                        power_dynamic = "asymmetric_favoring_to"

                    relationships.append(
                        Relationship(
                            from_party="agent",
                            to_party=stakeholder,
                            relationship_type=rel_type,
                            power_dynamic=power_dynamic,
                            vulnerability_level="medium" if rel_type == "dependent" else "low",
                        )
                    )
                    break

        # Cache relationships
        for stakeholder in stakeholders:
            if stakeholder not in self.relationships:
                self.relationships[stakeholder] = relationships

        return relationships

    def assess_vulnerability(self, stakeholder: str) -> VulnerabilityScore:
        """Identify and assess vulnerability of a stakeholder.

        Args:
            stakeholder: Name or description of stakeholder

        Returns:
            VulnerabilityScore with assessment details
        """
        # Check cache first
        if stakeholder in self.vulnerability_assessments:
            return self.vulnerability_assessments[stakeholder]

        stakeholder_lower = stakeholder.lower()
        vulnerability_factors = []
        dependencies = []
        protection_needs = []
        risk_level = "low"
        vulnerability_score = 0.0

        # Identify vulnerability factors
        vulnerability_keywords = {
            "age_vulnerable": ["child", "elderly", "infant", "minor", "senior"],
            "health_vulnerable": ["patient", "sick", "disabled", "injured", "ill"],
            "social_vulnerable": ["homeless", "refugee", "marginalized", "isolated"],
            "economic_vulnerable": ["poor", "unemployed", "dependent", "low_income"],
            "information_vulnerable": ["uneducated", "illiterate", "unaware"],
        }

        for factor_type, keywords in vulnerability_keywords.items():
            if any(kw in stakeholder_lower for kw in keywords):
                vulnerability_factors.append(factor_type)
                vulnerability_score += 0.25

        # Identify dependencies
        if "child" in stakeholder_lower or "dependent" in stakeholder_lower:
            dependencies.append("needs_care_and_protection")
            protection_needs.append("physical_safety")
            protection_needs.append("emotional_wellbeing")

        if "patient" in stakeholder_lower or "health" in stakeholder_lower:
            dependencies.append("needs_medical_care")
            protection_needs.append("health_protection")

        if "isolated" in stakeholder_lower:
            dependencies.append("needs_connection")
            protection_needs.append("social_support")

        # Determine risk level
        vulnerability_score = min(1.0, vulnerability_score)
        if vulnerability_score >= 0.75:
            risk_level = "high"
        elif vulnerability_score >= 0.5:
            risk_level = "medium"
        else:
            risk_level = "low"

        score = VulnerabilityScore(
            stakeholder=stakeholder,
            vulnerability_score=vulnerability_score,
            vulnerability_factors=vulnerability_factors,
            dependencies=dependencies,
            protection_needs=protection_needs,
            risk_level=risk_level,
        )

        # Cache assessment
        self.vulnerability_assessments[stakeholder] = score
        return score

    def evaluate_care_response(self, action: str, affected_parties: List[str]) -> CareAnalysis:
        """Check if action adequately responds to care needs.

        Args:
            action: Description of the action
            affected_parties: List of parties affected

        Returns:
            CareAnalysis with care adequacy assessment
        """
        action_lower = action.lower()
        care_score = 0.5
        specific_concerns = []
        improvement_suggestions = []
        alternative_actions = []
        adequate = True

        # Check for care-positive actions
        care_positive_keywords = [
            "support",
            "help",
            "protect",
            "care",
            "assist",
            "facilitate",
            "enable",
            "empower",
            "listen",
            "respond",
        ]

        care_count = sum(1 for kw in care_positive_keywords if kw in action_lower)
        if care_count > 0:
            care_score += 0.1 * care_count

        # Check for care-negative actions
        care_negative_keywords = [
            "ignore",
            "neglect",
            "abandon",
            "exploit",
            "manipulate",
            "coerce",
            "dismiss",
            "harm",
            "endanger",
        ]

        violation_count = sum(1 for kw in care_negative_keywords if kw in action_lower)
        if violation_count > 0:
            care_score -= 0.2 * violation_count
            adequate = False
            for party in affected_parties:
                specific_concerns.append(f"Action may harm or neglect {party}")

        # Assess relationship impact
        if "relationship" in action_lower or "trust" in action_lower:
            care_score += 0.1
        elif "disconnect" in action_lower or "isolate" in action_lower:
            care_score -= 0.15
            adequate = False

        # Generate suggestions
        if not adequate:
            improvement_suggestions.append(
                "Consider how this action preserves and strengthens relationships"
            )
            improvement_suggestions.append("Evaluate impact on most vulnerable stakeholders")
            improvement_suggestions.append("Ensure consent and communication with affected parties")

        # Generate alternatives
        if violation_count > 0:
            alternative_actions.append("Provide support instead of dismissal")
            alternative_actions.append("Seek input from affected parties")
            alternative_actions.append("Implement protective measures")

        care_score = max(0.0, min(1.0, care_score))

        return CareAnalysis(
            action_description=action,
            adequate=adequate,
            care_score=care_score,
            specific_concerns=specific_concerns,
            improvement_suggestions=improvement_suggestions,
            alternative_actions=alternative_actions,
        )

    def detect_care_violations(self, action: str) -> List[CareViolation]:
        """Detect violations of care ethics principles.

        Args:
            action: Description of the action

        Returns:
            List of detected care ethics violations
        """
        violations = []
        action_lower = action.lower()

        # Define violation patterns
        violation_patterns = {
            "neglect": {
                "keywords": ["ignore", "neglect", "abandon", "dismiss"],
                "severity": "high",
            },
            "abandonment": {
                "keywords": ["abandon", "leave", "discard", "desert"],
                "severity": "critical",
            },
            "harm": {
                "keywords": ["harm", "hurt", "endanger", "damage"],
                "severity": "high",
            },
            "exploitation": {
                "keywords": ["exploit", "use without consent", "abuse", "misuse"],
                "severity": "critical",
            },
            "misuse_of_power": {
                "keywords": ["coerce", "force", "manipulate", "control"],
                "severity": "high",
            },
        }

        for violation_type, pattern in violation_patterns.items():
            for keyword in pattern["keywords"]:
                if keyword in action_lower:
                    violation = CareViolation(
                        violation_type=violation_type,
                        affected_party="unspecified_stakeholder",
                        description=f"Action contains '{keyword}' which suggests {violation_type}",
                        severity=pattern["severity"],
                        harm_assessment=f"Potential {violation_type} affecting dependent parties",
                    )
                    violations.append(violation)
                    self.care_violation_history.append(violation)
                    break  # Only add one violation per type

        return violations

    def _determine_conclusion(
        self,
        care_analysis: CareAnalysis,
        violations: List[CareViolation],
        vulnerability_assessments: List[VulnerabilityScore],
    ) -> CareConclusion:
        """Determine overall care ethics conclusion.

        Args:
            care_analysis: Care response analysis
            violations: Detected violations
            vulnerability_assessments: Vulnerability assessments

        Returns:
            CareConclusion (CARING, INDIFFERENT, or HARMFUL)
        """
        if violations:
            critical_violations = [v for v in violations if v.severity == "critical"]
            if critical_violations:
                return CareConclusion.HARMFUL

        if care_analysis.care_score >= 0.7:
            return CareConclusion.CARING
        elif care_analysis.care_score >= 0.4:
            return CareConclusion.INDIFFERENT
        else:
            return CareConclusion.HARMFUL

    def _generate_recommendations(
        self,
        action: str,
        vulnerability_assessments: List[VulnerabilityScore],
        violations: List[CareViolation],
    ) -> List[str]:
        """Generate care ethics recommendations.

        Args:
            action: The action being analyzed
            vulnerability_assessments: Vulnerability assessments
            violations: Detected violations

        Returns:
            List of recommendations
        """
        recommendations = []

        # Add vulnerability-based recommendations
        for assessment in vulnerability_assessments:
            if assessment.risk_level in ("high", "medium"):
                for need in assessment.protection_needs:
                    recommendations.append(
                        f"Prioritize {need} for vulnerable stakeholder: {assessment.stakeholder}"
                    )

        # Add violation-based recommendations
        if violations:
            recommendations.append("Address identified care ethics violations before proceeding")
            for violation in violations:
                if violation.severity == "critical":
                    recommendations.append(
                        f"Reject action due to critical {violation.violation_type}"
                    )

        # Add general care recommendations
        recommendations.append("Maintain and strengthen relationships with affected parties")
        recommendations.append("Ensure ongoing communication and feedback")
        recommendations.append("Monitor for unintended negative impacts on vulnerable parties")

        return recommendations

    def _generate_reasoning(
        self,
        conclusion: CareConclusion,
        violations: List[CareViolation],
        care_analysis: CareAnalysis,
        vulnerability_assessments: List[VulnerabilityScore],
    ) -> str:
        """Generate reasoning for care ethics conclusion.

        Args:
            conclusion: The determined conclusion
            violations: Detected violations
            care_analysis: Care response analysis
            vulnerability_assessments: Vulnerability assessments

        Returns:
            Reasoning string
        """
        parts = []

        if conclusion == CareConclusion.CARING:
            parts.append("Action demonstrates adequate care and attention to relationships.")
        elif conclusion == CareConclusion.INDIFFERENT:
            parts.append("Action shows mixed or moderate care response. Improvement possible.")
        else:
            parts.append("Action fails to provide adequate care. Significant concerns identified.")

        if violations:
            parts.append(f"Detected {len(violations)} care ethics violation(s).")

        vulnerable = [a for a in vulnerability_assessments if a.risk_level in ("high", "medium")]
        if vulnerable:
            parts.append(
                f"Multiple vulnerable parties identified ({len(vulnerable)}). "
                "Special attention required."
            )

        parts.append(
            f"Care response adequacy: {care_analysis.care_score:.1%}. "
            f"{'Adequate' if care_analysis.adequate else 'Inadequate'}."
        )

        return " ".join(parts)
