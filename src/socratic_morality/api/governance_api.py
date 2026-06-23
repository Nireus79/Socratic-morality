"""Unified Governance API for decision evaluation."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
from uuid import uuid4
from enum import Enum

from socratic_morality.governor.core import Governor
from socratic_morality.governance.constitutional_enforcer import (
    ConstitutionalEnforcer,
    ConstitutionalCheck,
)
from socratic_morality.constitution.models import Constitution
from socratic_morality.precedent.engine import MoralPrecedentEngine
from socratic_morality.ethics.deliberation import EthicalDeliberationEngine


class DecisionCategory(str, Enum):
    """Categories of governance decisions."""

    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    ESCALATE = "ESCALATE"
    CONDITIONAL = "CONDITIONAL"


@dataclass
class ThreatAnalysis:
    """Analysis of potential threats from an action."""

    threat_level: str  # low, medium, high, critical
    threats_identified: List[str] = field(default_factory=list)
    mitigation_strategies: List[str] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class PrecedentAnalysis:
    """Analysis of relevant precedents."""

    similar_precedents: List[Dict[str, Any]] = field(default_factory=list)
    precedent_consistency: float = 0.5  # 0.0-1.0
    conflicting_precedents: List[Dict[str, Any]] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class ExplanationReport:
    """Detailed explanation of a governance decision."""

    decision_id: str
    action: str
    headline: str
    constitutional_analysis: str
    precedent_references: str
    ethical_considerations: str
    alternatives_considered: List[str] = field(default_factory=list)
    confidence_statement: str = ""
    recommendations: List[str] = field(default_factory=list)


@dataclass
class GovernanceDecision:
    """Comprehensive governance decision with full reasoning trace."""

    decision_id: str
    action: str
    allowed: bool
    decision_type: str  # ALLOWED, BLOCKED, ESCALATE, CONDITIONAL
    confidence: float
    constitutional_check: ConstitutionalCheck
    actor: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    deliberation: Optional[Dict[str, Any]] = None
    precedent_analysis: Optional[PrecedentAnalysis] = None
    threat_analysis: Optional[ThreatAnalysis] = None
    dialogue_transcript: Optional[List[Dict[str, str]]] = None
    reasoning_trace: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    explanation: Optional[ExplanationReport] = None

    def requires_escalation(self) -> bool:
        """Check if decision requires escalation."""
        return self.decision_type == DecisionCategory.ESCALATE


class GovernanceAPI:
    """Unified API for governance decisions with comprehensive analysis."""

    def __init__(
        self,
        constitution: Optional[Constitution] = None,
        constitution_path: Optional[str] = None,
        llm_provider: str = "anthropic",
        enable_precedent: bool = True,
        enable_deliberation: bool = True,
        enable_dialogue: bool = True,
    ):
        """Initialize the Governance API.

        Args:
            constitution: Constitution object or path to YAML file.
            constitution_path: Path to constitution YAML file (alternative to constitution param).
            llm_provider: LLM provider to use ("anthropic" or "openai").
            enable_precedent: Enable precedent analysis.
            enable_deliberation: Enable ethical deliberation.
            enable_dialogue: Enable Socratic dialogue features.
        """
        # Initialize constitution
        if isinstance(constitution, str):
            constitution_path = constitution
        if constitution_path:
            self.constitution = Constitution.load_from_file(constitution_path)
        elif constitution:
            self.constitution = constitution
        else:
            self.constitution = Constitution()

        self.llm_provider = llm_provider
        self.enable_precedent = enable_precedent
        self.enable_deliberation = enable_deliberation
        self.enable_dialogue = enable_dialogue

        # Initialize components
        self.governor = Governor(constitution=self.constitution, llm_provider=llm_provider)
        self.enforcer = ConstitutionalEnforcer()
        self.enforcer.constitution = self.constitution

        self.precedent_engine = (
            MoralPrecedentEngine(constitution=self.constitution) if enable_precedent else None
        )
        self.deliberation_engine = (
            EthicalDeliberationEngine(llm_provider=llm_provider) if enable_deliberation else None
        )

        # Decision history
        self._decision_history: List[GovernanceDecision] = []
        self._max_history = 100

    async def evaluate(
        self,
        action: str,
        context: Optional[Dict[str, Any]] = None,
        actor: Optional[str] = None,
        high_impact: bool = False,
    ) -> GovernanceDecision:
        """Main entry point for evaluating an action.

        Args:
            action: Description of the action to evaluate.
            context: Context information about the action.
            actor: Actor performing the action.
            high_impact: Whether this is a high-impact decision.

        Returns:
            GovernanceDecision with comprehensive analysis.
        """
        context = context or {}
        decision_id = str(uuid4())

        # Step 1: Constitutional check
        constitutional_check = self.enforcer.check_principles(action)

        # Step 2: Get Governor decision
        governor_decision = await self.governor.evaluate(
            action=action,
            purpose=context.get("purpose", ""),
            actor=actor or "",
            context=context,
            high_impact=high_impact,
        )

        # Step 3: Determine decision type
        decision_type = self._determine_decision_type(constitutional_check, high_impact)
        allowed = constitutional_check.allowed and governor_decision.allowed

        # Step 4: Build reasoning trace
        reasoning_trace = {
            "constitutional_check": {
                "allowed": constitutional_check.allowed,
                "violations_count": len(constitutional_check.violations),
                "confidence": constitutional_check.confidence,
            },
            "governor_decision": {
                "allowed": governor_decision.allowed,
                "decision_type": str(governor_decision.decision_type),
            },
        }

        # Step 5: Optional analyses
        precedent_analysis = None
        if self.enable_precedent and self.precedent_engine:
            precedent_analysis = await self._analyze_precedents(action)

        deliberation = None
        if self.enable_deliberation and self.deliberation_engine:
            deliberation = await self._deliberate(
                action, context, actor, constitutional_check.violations
            )

        threat_analysis = self._analyze_threats(action, context)

        # Calculate overall confidence
        confidence = (constitutional_check.confidence + governor_decision.allowed) / 2

        # Create decision
        decision = GovernanceDecision(
            decision_id=decision_id,
            action=action,
            allowed=allowed,
            decision_type=decision_type,
            confidence=confidence,
            constitutional_check=constitutional_check,
            actor=actor,
            context=context,
            deliberation=deliberation,
            precedent_analysis=precedent_analysis,
            threat_analysis=threat_analysis,
            reasoning_trace=reasoning_trace,
            timestamp=datetime.utcnow(),
        )

        # Store in history
        self._decision_history.append(decision)
        if len(self._decision_history) > self._max_history:
            self._decision_history.pop(0)

        return decision

    async def evaluate_with_dialogue(
        self,
        action: str,
        context: Optional[Dict[str, Any]] = None,
        actor: Optional[str] = None,
        interactive: bool = True,
        user_input_fn: Optional[Callable[[str], str]] = None,
    ) -> GovernanceDecision:
        """Evaluate action with optional interactive dialogue.

        Args:
            action: Description of the action to evaluate.
            context: Context information.
            actor: Actor performing the action.
            interactive: Whether to enable interactive dialogue.
            user_input_fn: Optional function to get user input.

        Returns:
            GovernanceDecision with dialogue transcript.
        """
        decision = await self.evaluate(action, context, actor)

        if interactive and self.enable_dialogue:
            dialogue_transcript = await self._conduct_dialogue(
                action, context, decision, user_input_fn
            )
            decision.dialogue_transcript = dialogue_transcript

        return decision

    async def batch_evaluate(self, actions: List[Dict[str, Any]]) -> List[GovernanceDecision]:
        """Evaluate multiple actions.

        Args:
            actions: List of action dictionaries with keys: action, context, actor.

        Returns:
            List of GovernanceDecision objects.
        """
        decisions = []
        for action_dict in actions:
            decision = await self.evaluate(
                action=action_dict.get("action", ""),
                context=action_dict.get("context", {}),
                actor=action_dict.get("actor"),
                high_impact=action_dict.get("high_impact", False),
            )
            decisions.append(decision)
        return decisions

    def get_evaluation_history(self, limit: int = 10) -> List[GovernanceDecision]:
        """Get recent decisions from history.

        Args:
            limit: Maximum number of decisions to return.

        Returns:
            List of recent GovernanceDecision objects.
        """
        return self._decision_history[-limit:]

    def explain_decision(self, decision_id: str) -> Optional[ExplanationReport]:
        """Get detailed explanation for a decision.

        Args:
            decision_id: ID of the decision to explain.

        Returns:
            ExplanationReport with detailed reasoning.
        """
        # Find decision in history
        decision = None
        for d in self._decision_history:
            if d.decision_id == decision_id:
                decision = d
                break

        if not decision:
            return None

        # Generate explanation
        return ExplanationReport(
            decision_id=decision_id,
            action=decision.action,
            headline=self._generate_headline(decision.allowed, decision.confidence),
            constitutional_analysis=decision.constitutional_check.reasoning,
            precedent_references=self._format_precedent_explanation(decision.precedent_analysis),
            ethical_considerations=self._format_deliberation_explanation(decision.deliberation),
            confidence_statement=self._generate_confidence_statement(decision.confidence),
            recommendations=self._generate_recommendations(decision),
        )

    async def _analyze_precedents(self, action: str) -> PrecedentAnalysis:
        """Analyze relevant precedents.

        Args:
            action: Action to analyze.

        Returns:
            PrecedentAnalysis with similar cases and consistency.
        """
        if not self.precedent_engine:
            return PrecedentAnalysis()

        similar = await self.precedent_engine.find_similar_cases_semantic(action, limit=5)

        return PrecedentAnalysis(
            similar_precedents=similar,
            precedent_consistency=0.7 if similar else 0.5,
            reasoning=(
                "Based on semantic similarity to previous cases."
                if similar
                else "No similar precedents found."
            ),
        )

    async def _deliberate(
        self, action: str, context: Dict[str, Any], actor: Optional[str], violations: List[Any]
    ) -> Dict[str, Any]:
        """Perform ethical deliberation.

        Args:
            action: Action to deliberate.
            context: Context information.
            actor: Actor performing action.
            violations: Constitutional violations found.

        Returns:
            Deliberation result dictionary.
        """
        if not self.deliberation_engine:
            return {}

        result = await self.deliberation_engine.analyze(
            action=action,
            purpose=context.get("purpose", ""),
            actor=actor or "unknown",
            context=context,
            violations=violations,
        )

        return result

    def _analyze_threats(self, action: str, context: Dict[str, Any]) -> ThreatAnalysis:
        """Analyze potential threats from an action.

        Args:
            action: Action to analyze.
            context: Context information.

        Returns:
            ThreatAnalysis with threat level and mitigation.
        """
        action_lower = action.lower()
        threats = []
        threat_level = "low"

        # Simple threat detection
        critical_keywords = ["delete", "destroy", "disable", "terminate", "remove"]
        high_keywords = ["modify", "access", "change", "update", "override"]

        for keyword in critical_keywords:
            if keyword in action_lower:
                threats.append(f"Critical action: {keyword}")
                threat_level = "critical"

        for keyword in high_keywords:
            if keyword in action_lower and threat_level == "low":
                threats.append(f"Significant action: {keyword}")
                threat_level = "high"

        mitigation = []
        if threat_level == "critical":
            mitigation.append("Requires human approval and verification")
            mitigation.append("Implement audit logging")
        elif threat_level == "high":
            mitigation.append("Implement enhanced monitoring")

        return ThreatAnalysis(
            threat_level=threat_level,
            threats_identified=threats,
            mitigation_strategies=mitigation,
            reasoning="Threat assessment based on action keywords and context.",
        )

    async def _conduct_dialogue(
        self,
        action: str,
        context: Dict[str, Any],
        decision: GovernanceDecision,
        user_input_fn: Optional[Callable[[str], str]],
    ) -> List[Dict[str, str]]:
        """Conduct interactive dialogue.

        Args:
            action: Action being evaluated.
            context: Context information.
            decision: Initial decision.
            user_input_fn: Function to get user input.

        Returns:
            List of dialogue exchanges.
        """
        transcript = []

        # Initial question
        initial_question = (
            f"Regarding the action: '{action}' - Do you have any concerns about this action?"
        )
        transcript.append({"role": "system", "message": initial_question})

        if user_input_fn:
            user_response = user_input_fn(initial_question)
            transcript.append({"role": "user", "message": user_response})

            # Follow-up question
            followup = "Based on your concerns, what safeguards would you recommend?"
            transcript.append({"role": "system", "message": followup})
            user_followup = user_input_fn(followup)
            transcript.append({"role": "user", "message": user_followup})

        return transcript

    def _determine_decision_type(
        self, constitutional_check: ConstitutionalCheck, high_impact: bool
    ) -> str:
        """Determine the type of decision.

        Args:
            constitutional_check: Constitutional check result.
            high_impact: Whether decision is high impact.

        Returns:
            Decision type string.
        """
        if high_impact and not constitutional_check.allowed:
            return DecisionCategory.ESCALATE

        if constitutional_check.allowed:
            if len(constitutional_check.violations) > 0:
                return DecisionCategory.CONDITIONAL
            return DecisionCategory.ALLOWED

        return DecisionCategory.BLOCKED

    @staticmethod
    def _generate_headline(allowed: bool, confidence: float) -> str:
        """Generate decision headline."""
        if allowed:
            if confidence >= 0.9:
                return "APPROVED with high confidence"
            elif confidence >= 0.7:
                return "APPROVED with moderate confidence"
            else:
                return "APPROVED with low confidence"
        else:
            if confidence >= 0.9:
                return "DENIED with high confidence"
            elif confidence >= 0.7:
                return "DENIED with moderate confidence"
            else:
                return "DENIED with low confidence"

    @staticmethod
    def _generate_confidence_statement(confidence: float) -> str:
        """Generate confidence statement."""
        pct = int(confidence * 100)
        if confidence >= 0.9:
            return f"Confidence: {pct}% (Very High)"
        elif confidence >= 0.7:
            return f"Confidence: {pct}% (High)"
        elif confidence >= 0.5:
            return f"Confidence: {pct}% (Moderate)"
        else:
            return f"Confidence: {pct}% (Low)"

    @staticmethod
    def _format_precedent_explanation(precedent_analysis: Optional[PrecedentAnalysis]) -> str:
        """Format precedent analysis for explanation."""
        if not precedent_analysis or not precedent_analysis.similar_precedents:
            return "No similar precedents found."

        lines = [f"Found {len(precedent_analysis.similar_precedents)} similar precedent(s):"]
        for i, p in enumerate(precedent_analysis.similar_precedents[:3], 1):
            action = str(p.get("action", ""))[:50]
            decision = "allowed" if p.get("allowed") else "denied"
            lines.append(f"  {i}. {action}... - {decision}")

        return "\n".join(lines)

    @staticmethod
    def _format_deliberation_explanation(deliberation: Optional[Dict[str, Any]]) -> str:
        """Format deliberation for explanation."""
        if not deliberation:
            return "No ethical deliberation available."

        concerns = deliberation.get("concerns", "No major concerns")
        return f"Ethical Analysis: {concerns}"

    @staticmethod
    def _generate_recommendations(decision: GovernanceDecision) -> List[str]:
        """Generate recommendations based on decision."""
        recommendations = []

        if not decision.allowed:
            recommendations.append("Consider modifying the action to comply with principles")
            recommendations.append("Request human review for potential exceptions")

        if decision.threat_analysis and decision.threat_analysis.threat_level in [
            "high",
            "critical",
        ]:
            recommendations.extend(decision.threat_analysis.mitigation_strategies)

        if decision.requires_escalation():
            recommendations.append("Escalate to human decision-maker")

        return recommendations
