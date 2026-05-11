"""Socratic Dialogue Engine for ethical reasoning through questioning."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from enum import Enum


class SocraticApproach(str, Enum):
    """Different Socratic questioning techniques."""

    EXPOSING_CONTRADICTION = "exposing_contradiction"
    TESTING_UNIVERSALITY = "testing_universality"
    REVEALING_ASSUMPTIONS = "revealing_assumptions"
    EXPLORING_CONSEQUENCES = "exploring_consequences"
    CLARIFYING_CONCEPTS = "clarifying_concepts"
    IDENTIFYING_STAKEHOLDERS = "identifying_stakeholders"
    MORAL_REASONING = "moral_reasoning"
    PRACTICAL_WISDOM = "practical_wisdom"


class QuestionCategory(str, Enum):
    """Categories of Socratic questions."""

    STAKEHOLDER = "stakeholder"
    CONSEQUENCE = "consequence"
    PRINCIPLE = "principle"
    ALTERNATIVE = "alternative"
    ASSUMPTION = "assumption"
    PRECEDENT = "precedent"
    CONSISTENCY = "consistency"


@dataclass
class Question:
    """A Socratic question for dialogue."""

    text: str
    category: str  # From QuestionCategory
    socratic_approach: str  # From SocraticApproach
    expected_insights: List[str] = field(default_factory=list)
    depth_level: int = 1  # 1-5, deeper questions need context
    follow_up_questions: List[str] = field(default_factory=list)


@dataclass
class Alternative:
    """An alternative approach to an action."""

    description: str
    advantages: List[str] = field(default_factory=list)
    disadvantages: List[str] = field(default_factory=list)
    stakeholder_impact: Dict[str, str] = field(default_factory=dict)
    feasibility: float = 0.5  # 0-1, how feasible is this alternative
    preserves_principles: List[str] = field(default_factory=list)


@dataclass
class Exchange:
    """A single question-answer exchange in dialogue."""

    question: Question
    answer: Optional[str] = None
    insights: List[str] = field(default_factory=list)
    follow_up_needed: bool = False
    turn_number: int = 0


@dataclass
class DialogueSynthesis:
    """Synthesis of dialogue insights."""

    key_insights: List[str] = field(default_factory=list)
    tensions_identified: List[str] = field(default_factory=list)
    stakeholder_concerns: Dict[str, List[str]] = field(default_factory=dict)
    principle_conflicts: List[Dict[str, Any]] = field(default_factory=list)
    modified_action: Optional[str] = None
    new_considerations: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class DialogueResult:
    """Complete result of a Socratic dialogue."""

    action: str
    exchanges: List[Exchange] = field(default_factory=list)
    insights_gained: List[str] = field(default_factory=list)
    new_considerations: List[str] = field(default_factory=list)
    modified_analysis: Optional[Dict[str, Any]] = None
    synthesis: Optional[DialogueSynthesis] = None
    dialogue_duration: int = 0  # seconds
    num_exchanges: int = 0


class SocraticDialogueEngine:
    """Engine for conducting Socratic dialogues on ethical decisions."""

    def __init__(self, llm_provider: str = "anthropic", interactive: bool = True):
        """Initialize the Socratic Dialogue Engine.

        Args:
            llm_provider: LLM provider for generating questions.
            interactive: Whether to enable interactive dialogue.
        """
        self.llm_provider = llm_provider
        self.interactive = interactive
        self._question_history: List[Question] = []
        self._dialogue_history: List[DialogueResult] = []

    def question_stakeholders(self, stakeholder_analysis: Dict[str, Any]) -> List[Question]:
        """Generate Socratic questions about stakeholders.

        Args:
            stakeholder_analysis: Dictionary with stakeholder information.

        Returns:
            List of Socratic questions about stakeholders.
        """
        questions = []

        stakeholders = stakeholder_analysis.get("stakeholders", [])
        affected_groups = stakeholder_analysis.get("affected_groups", [])

        # Question 1: Stakeholder perspective
        questions.append(
            Question(
                text="Would you accept if this same action were taken against you?",
                category=QuestionCategory.STAKEHOLDER,
                socratic_approach=SocraticApproach.EXPOSING_CONTRADICTION,
                expected_insights=[
                    "Reveals assumption about fairness",
                    "Tests universalizability of action",
                    "Identifies asymmetries in impact",
                ],
                follow_up_questions=[
                    "Why or why not?",
                    "What would make it acceptable to you?",
                ],
            )
        )

        # Question 2: Whose interests matter?
        questions.append(
            Question(
                text="Who are all the stakeholders affected by this action, and whose interests might be overlooked?",
                category=QuestionCategory.STAKEHOLDER,
                socratic_approach=SocraticApproach.IDENTIFYING_STAKEHOLDERS,
                expected_insights=[
                    "Comprehensive stakeholder mapping",
                    "Identification of vulnerable parties",
                    "Recognition of indirect impacts",
                ],
            )
        )

        # Question 3: Stakeholder voices
        questions.append(
            Question(
                text="If we could ask each stakeholder directly, what concerns would they raise?",
                category=QuestionCategory.STAKEHOLDER,
                socratic_approach=SocraticApproach.REVEALING_ASSUMPTIONS,
                expected_insights=[
                    "Empathy for affected parties",
                    "Exposure of assumptions about preferences",
                    "Recognition of diverse perspectives",
                ],
            )
        )

        # Question 4: Power dynamics
        questions.append(
            Question(
                text="What power imbalances exist between the actor and the stakeholders?",
                category=QuestionCategory.STAKEHOLDER,
                socratic_approach=SocraticApproach.MORAL_REASONING,
                expected_insights=[
                    "Recognition of vulnerability",
                    "Identification of consent issues",
                    "Understanding of coercion risks",
                ],
                depth_level=2,
            )
        )

        return questions

    def question_consequences(self, consequence_analysis: Dict[str, Any]) -> List[Question]:
        """Generate Socratic questions about consequences.

        Args:
            consequence_analysis: Dictionary with consequence information.

        Returns:
            List of Socratic questions about outcomes.
        """
        questions = []

        # Question 1: Unforeseen consequences
        questions.append(
            Question(
                text="What are the potential unforeseen consequences of this action, especially indirect or delayed effects?",
                category=QuestionCategory.CONSEQUENCE,
                socratic_approach=SocraticApproach.EXPLORING_CONSEQUENCES,
                expected_insights=[
                    "Recognition of complexity",
                    "Identification of second-order effects",
                    "Consideration of long-term impact",
                ],
            )
        )

        # Question 2: Worst case scenario
        questions.append(
            Question(
                text="What is the worst-case scenario if this action goes wrong, and how likely is it?",
                category=QuestionCategory.CONSEQUENCE,
                socratic_approach=SocraticApproach.EXPLORING_CONSEQUENCES,
                expected_insights=[
                    "Risk awareness",
                    "Contingency planning",
                    "Failure mode analysis",
                ],
                depth_level=2,
            )
        )

        # Question 3: Systemic effects
        questions.append(
            Question(
                text="How would repeated similar actions shape institutions, norms, or future decisions?",
                category=QuestionCategory.CONSEQUENCE,
                socratic_approach=SocraticApproach.TESTING_UNIVERSALITY,
                expected_insights=[
                    "Systemic thinking",
                    "Recognition of precedent-setting",
                    "Long-term cultural impact",
                ],
                depth_level=3,
            )
        )

        return questions

    def question_principles(self, framework_results: Dict[str, Any]) -> List[Question]:
        """Generate Socratic questions challenging logical consistency.

        Args:
            framework_results: Dictionary with ethical framework analysis.

        Returns:
            List of Socratic questions about principles.
        """
        questions = []

        frameworks = framework_results.get("frameworks", {})

        # Question 1: Principle conflict
        questions.append(
            Question(
                text="Are there conflicting principles or values at play here? Which should take precedence?",
                category=QuestionCategory.PRINCIPLE,
                socratic_approach=SocraticApproach.EXPOSING_CONTRADICTION,
                expected_insights=[
                    "Identification of value conflicts",
                    "Clarification of priorities",
                    "Recognition of tradeoffs",
                ],
                depth_level=2,
            )
        )

        # Question 2: Universal principle test
        questions.append(
            Question(
                text="Can you articulate a universal principle that would justify this action in all similar circumstances?",
                category=QuestionCategory.PRINCIPLE,
                socratic_approach=SocraticApproach.TESTING_UNIVERSALITY,
                expected_insights=[
                    "Testing categorical imperative",
                    "Exposure of special pleading",
                    "Clarification of reasoning",
                ],
                depth_level=3,
            )
        )

        # Question 3: Dignity and respect
        questions.append(
            Question(
                text="Does this action treat all affected parties as ends in themselves, or does it treat anyone as merely a means?",
                category=QuestionCategory.PRINCIPLE,
                socratic_approach=SocraticApproach.MORAL_REASONING,
                expected_insights=[
                    "Respect for autonomy",
                    "Recognition of human dignity",
                    "Identification of instrumentalization",
                ],
                depth_level=3,
            )
        )

        # Question 4: Virtue examination
        questions.append(
            Question(
                text="What character traits or virtues does this action reflect or cultivate?",
                category=QuestionCategory.PRINCIPLE,
                socratic_approach=SocraticApproach.REVEALING_ASSUMPTIONS,
                expected_insights=[
                    "Character assessment",
                    "Recognition of virtue/vice",
                    "Moral development awareness",
                ],
            )
        )

        return questions

    def question_alternatives(self, action: str, concerns: List[str]) -> List[Alternative]:
        """Propose alternative approaches to address concerns.

        Args:
            action: The original action being evaluated.
            concerns: List of concerns or objections raised.

        Returns:
            List of Alternative approaches.
        """
        alternatives = []

        # Alternative 1: Seek consent
        alternatives.append(
            Alternative(
                description="Seek informed consent from all affected stakeholders before proceeding",
                advantages=[
                    "Respects autonomy",
                    "Reduces coercion risks",
                    "Improves buy-in",
                    "Builds trust",
                ],
                disadvantages=[
                    "May be time-consuming",
                    "Stakeholders may refuse",
                    "May reveal objections",
                ],
                feasibility=0.8,
                preserves_principles=["autonomy", "respect", "transparency"],
            )
        )

        # Alternative 2: Graduated implementation
        alternatives.append(
            Alternative(
                description="Implement action in phases with safeguards and monitoring at each step",
                advantages=[
                    "Reduces risk exposure",
                    "Allows course correction",
                    "Provides early warning system",
                    "Demonstrates caution",
                ],
                disadvantages=[
                    "Takes longer",
                    "May miss critical timing",
                    "Increases complexity",
                ],
                feasibility=0.75,
                preserves_principles=["safety", "prudence", "accountability"],
            )
        )

        # Alternative 3: Selective application
        alternatives.append(
            Alternative(
                description="Limit action to lower-risk cases or stakeholder groups first",
                advantages=[
                    "Reduces overall harm",
                    "Protects vulnerable parties",
                    "Tests assumptions",
                    "Allows learning",
                ],
                disadvantages=[
                    "May create inequity",
                    "Delays benefits",
                    "Could appear discriminatory",
                ],
                feasibility=0.7,
                preserves_principles=["fairness", "safety", "justice"],
            )
        )

        # Alternative 4: Enhanced transparency
        alternatives.append(
            Alternative(
                description="Add full disclosure, audit logging, and public reporting of all actions and outcomes",
                advantages=[
                    "Increases accountability",
                    "Enables oversight",
                    "Builds public trust",
                    "Creates learning records",
                ],
                disadvantages=[
                    "May reveal sensitive information",
                    "Could enable gaming the system",
                    "Adds administrative burden",
                ],
                feasibility=0.85,
                preserves_principles=["transparency", "accountability", "honesty"],
            )
        )

        # Alternative 5: Human oversight
        alternatives.append(
            Alternative(
                description="Require human approval or real-time monitoring for critical decision points",
                advantages=[
                    "Adds human judgment",
                    "Catches errors",
                    "Provides accountability",
                    "Respects human oversight",
                ],
                disadvantages=[
                    "Slows decisions",
                    "Humans may miss details",
                    "Creates bottlenecks",
                ],
                feasibility=0.9,
                preserves_principles=["accountability", "human agency", "safety"],
            )
        )

        return alternatives

    async def run_dialogue(
        self,
        action: str,
        context: Dict[str, Any],
        user: Optional[Callable[[str], str]] = None,
    ) -> DialogueResult:
        """Run an interactive Socratic dialogue.

        Args:
            action: Action to dialogue about.
            context: Context information.
            user: Optional function to get user input.

        Returns:
            DialogueResult with exchanges and synthesis.
        """
        dialogue_result = DialogueResult(action=action)
        exchanges = []
        turn_number = 0
        insights_gained = set()

        # Generate questions based on context
        stakeholder_analysis = context.get("stakeholder_analysis", {})
        consequence_analysis = context.get("consequence_analysis", {})
        framework_results = context.get("framework_results", {})

        all_questions = []
        all_questions.extend(self.question_stakeholders(stakeholder_analysis))
        all_questions.extend(self.question_consequences(consequence_analysis))
        all_questions.extend(self.question_principles(framework_results))

        # Conduct dialogue
        for question in all_questions[:5]:  # Limit to 5 questions for reasonable dialogue length
            turn_number += 1
            exchange = Exchange(question=question, turn_number=turn_number)

            if user and self.interactive:
                # Get user input
                answer = user(question.text)
                exchange.answer = answer

                # Extract insights from answer
                exchange.insights = question.expected_insights
                insights_gained.update(question.expected_insights)

                exchange.follow_up_needed = len(answer) < 10 or "?" in answer

            exchanges.append(exchange)

        # Synthesize dialogue
        dialogue_result.exchanges = exchanges
        dialogue_result.insights_gained = list(insights_gained)
        dialogue_result.num_exchanges = len(exchanges)
        dialogue_result.synthesis = self._synthesize_dialogue(exchanges, action)

        # Store in history
        self._dialogue_history.append(dialogue_result)

        return dialogue_result

    def synthesize_dialogue(self, dialogue: List[Exchange]) -> DialogueSynthesis:
        """Extract insights and recommendations from dialogue.

        Args:
            dialogue: List of exchanges from dialogue.

        Returns:
            DialogueSynthesis with key insights and recommendations.
        """
        return self._synthesize_dialogue(dialogue, "Unknown action")

    def _synthesize_dialogue(self, exchanges: List[Exchange], action: str) -> DialogueSynthesis:
        """Internal method to synthesize dialogue.

        Args:
            exchanges: List of exchanges.
            action: The original action.

        Returns:
            DialogueSynthesis.
        """
        synthesis = DialogueSynthesis()

        # Collect insights from all exchanges
        all_insights = set()
        for exchange in exchanges:
            all_insights.update(exchange.insights)
            if exchange.answer:
                # Detect concerns in answers
                answer_lower = exchange.answer.lower()
                if any(word in answer_lower for word in ["concern", "worry", "risk", "problem", "danger"]):
                    synthesis.tensions_identified.append(f"Concern raised in response to: {exchange.question.text}")

        synthesis.key_insights = list(all_insights)

        # Identify new considerations
        synthesis.new_considerations = [
            "All affected stakeholders should be heard",
            "Unintended consequences may emerge",
            "Multiple principles may conflict",
            "Alternatives exist to the proposed action",
            "Long-term systemic effects matter",
        ]

        # Generate recommendations
        synthesis.recommendations = [
            "Seek broader stakeholder input",
            "Implement safeguards and monitoring",
            "Prepare contingency plans",
            "Consider alternatives",
            "Document decision rationale",
        ]

        return synthesis

    def get_dialogue_history(self, limit: int = 10) -> List[DialogueResult]:
        """Get recent dialogues.

        Args:
            limit: Maximum number to return.

        Returns:
            List of recent DialogueResult objects.
        """
        return self._dialogue_history[-limit:]

    def clear_history(self) -> None:
        """Clear dialogue history."""
        self._dialogue_history.clear()
