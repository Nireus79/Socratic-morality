"""Ethical Deliberation Engine with multi-framework analysis."""
from typing import Any, Dict, List, Optional
import json


class EthicalDeliberationEngine:
    """Multi-framework ethical analysis engine."""

    def __init__(self, llm_provider: str = "anthropic", constitution: Optional[Any] = None):
        self.llm_provider = llm_provider
        self.constitution = constitution
        self.frameworks = ["kantian", "utilitarian", "virtue_ethics", "rights_based"]

    async def analyze(
        self,
        action: str,
        purpose: str,
        actor: str,
        context: Dict[str, Any],
        violations: List[Any] = None
    ) -> Dict[str, Any]:
        """Perform comprehensive ethical analysis."""
        violations = violations or []

        # Step 1: Identify stakeholders
        stakeholders = self._identify_stakeholders(context)

        # Step 2: Analyze rights and duties
        rights_analysis = self._analyze_rights_and_duties(action, stakeholders)

        # Step 3: Run framework analyses
        frameworks_analysis = {}
        for framework in self.frameworks:
            frameworks_analysis[framework] = await self._analyze_framework(
                framework, action, purpose, stakeholders, context
            )

        # Step 4: Synthesize results
        all_allowed = all(f.get('allowed', True) for f in frameworks_analysis.values())
        min_confidence = min(f.get('confidence', 0.8) for f in frameworks_analysis.values())

        # Collect concerns
        concerns = []
        for name, analysis in frameworks_analysis.items():
            if analysis.get('concerns'):
                concerns.append(f"{name}: {analysis['concerns']}")

        return {
            'allowed': all_allowed and len(violations) == 0,
            'confidence': min_confidence,
            'concerns': '; '.join(concerns) if concerns else None,
            'stakeholders': stakeholders,
            'rights_analysis': rights_analysis,
            'frameworks': frameworks_analysis,
        }

    def _identify_stakeholders(self, context: Dict[str, Any]) -> List[str]:
        """Identify who is affected by this action."""
        stakeholders = []
        if 'user_id' in context:
            stakeholders.append(f"user:{context['user_id']}")
        if 'organization_id' in context:
            stakeholders.append(f"org:{context['organization_id']}")
        if 'team_id' in context:
            stakeholders.append(f"team:{context['team_id']}")
        return stakeholders

    def _analyze_rights_and_duties(
        self,
        action: str,
        stakeholders: List[str]
    ) -> Dict[str, Any]:
        """Analyze legal and moral rights/duties."""
        return {
            'rights_affected': [],
            'duties_implicated': [],
            'conflicts': [],
            'human_rights_relevant': any('user:' in s for s in stakeholders)
        }

    async def _analyze_framework(
        self,
        framework: str,
        action: str,
        purpose: str,
        stakeholders: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze action through a specific ethical framework."""
        if framework == "kantian":
            return self._kantian_analysis(action, stakeholders)
        elif framework == "utilitarian":
            return self._utilitarian_analysis(action, context)
        elif framework == "virtue_ethics":
            return self._virtue_ethics_analysis(action)
        elif framework == "rights_based":
            return self._rights_based_analysis(action, stakeholders)
        return {'allowed': True, 'confidence': 0.5}

    def _kantian_analysis(
        self,
        action: str,
        stakeholders: List[str]
    ) -> Dict[str, Any]:
        """Kantian ethics: Dignity, categorical imperative, never treat people as mere means."""
        action_lower = action.lower()
        concerns = None
        allowed = True

        # Check for treating people as ends in themselves
        violation_keywords = [
            'manipulate', 'deceive', 'coerce', 'exploit',
            'use without consent', 'treat as mere means'
        ]

        for keyword in violation_keywords:
            if keyword in action_lower:
                concerns = f"Violates duty to treat people as ends in themselves: {keyword}"
                allowed = False
                break

        return {
            'allowed': allowed,
            'confidence': 0.85,
            'concerns': concerns,
            'principle': 'Categorical Imperative',
            'stakeholders_affected': len(stakeholders),
            'reasoning': 'Can this action be universalized without contradiction?'
        }

    def _utilitarian_analysis(
        self,
        action: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Utilitarian ethics: Maximize wellbeing, minimize harm."""
        return {
            'allowed': True,
            'confidence': 0.75,
            'concerns': None,
            'principle': 'Greatest Good for Greatest Number',
            'harm_assessment': 'Requires context-specific evaluation',
            'reasoning': 'Does this action maximize overall wellbeing?'
        }

    def _virtue_ethics_analysis(self, action: str) -> Dict[str, Any]:
        """Virtue ethics: What character does this action reflect?"""
        action_lower = action.lower()
        concerns = None
        allowed = True

        # Check if action reflects vice
        vice_keywords = [
            'hide', 'deception', 'cowardice', 'avarice',
            'injustice', 'intemperance', 'dishonesty'
        ]

        for keyword in vice_keywords:
            if keyword in action_lower:
                concerns = f"Action may cultivate vice: {keyword}"
                allowed = False
                break

        return {
            'allowed': allowed,
            'confidence': 0.78,
            'concerns': concerns,
            'principle': 'Virtue and Practical Wisdom',
            'character_assessment': 'Reflects practical wisdom?',
            'reasoning': 'What kind of agent does this make us?'
        }

    def _rights_based_analysis(
        self,
        action: str,
        stakeholders: List[str]
    ) -> Dict[str, Any]:
        """Rights-based ethics: Respect autonomy and human rights."""
        action_lower = action.lower()
        concerns = None
        allowed = True

        # Check for violations of autonomy and consent
        autonomy_keywords = [
            'without consent', 'override', 'force', 'coerce',
            'prevent choice', 'remove agency'
        ]

        for keyword in autonomy_keywords:
            if keyword in action_lower:
                concerns = f"Violates right to autonomous decision-making: {keyword}"
                allowed = False
                break

        return {
            'allowed': allowed,
            'confidence': 0.82,
            'concerns': concerns,
            'principle': 'Human Agency and Autonomy',
            'consent_required': 'Evaluate whether informed consent is present',
            'reasoning': 'Does this respect stakeholder autonomy?',
            'stakeholders_affected': len(stakeholders)
        }
