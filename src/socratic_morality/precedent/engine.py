"""Moral Precedent Engine with semantic similarity search."""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import math


@dataclass
class PrecedentCase:
    """A stored precedent case with metadata."""
    id: str
    action: str
    decision_type: str
    allowed: bool
    reasoning: str
    principles_cited: List[str]
    stakeholders_affected: List[str]
    actor: str
    context: Dict[str, Any]


class MoralPrecedentEngine:
    """Stores and retrieves past decisions as institutional memory."""

    def __init__(self, storage_type: str = "memory", constitution: Optional[Any] = None):
        self.storage_type = storage_type
        self.constitution = constitution
        self.cases: List[Dict[str, Any]] = []
        self._case_counter = 0

    async def store_case(
        self,
        action: str,
        decision: Any,
        reasoning: str,
        principles_cited: List[str] = None,
        stakeholders_affected: List[str] = None
    ) -> str:
        """Store a decision as a precedent case."""
        self._case_counter += 1
        case_id = f"case_{self._case_counter}"

        case = {
            'id': case_id,
            'action': action,
            'decision_type': getattr(decision, 'decision_type', 'unknown'),
            'allowed': getattr(decision, 'allowed', False),
            'reasoning': reasoning,
            'principles_cited': principles_cited or [],
            'stakeholders_affected': stakeholders_affected or [],
            'actor': getattr(decision, 'actor', ''),
            'context': getattr(decision, 'context', {}),
            'timestamp': getattr(decision, 'timestamp', ''),
        }

        self.cases.append(case)
        return case_id

    async def find_similar_cases(
        self,
        action: str,
        limit: int = 5,
        threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Find cases similar to the proposed action using string similarity.
        
        Returns cases with similarity scores above threshold.
        """
        if not self.cases:
            return []

        similar = []
        action_words = set(action.lower().split())

        for case in self.cases:
            case_action = case.get('action', '').lower()
            case_words = set(case_action.split())

            # Calculate Jaccard similarity
            if case_words or action_words:
                intersection = len(action_words & case_words)
                union = len(action_words | case_words)
                similarity = intersection / union if union > 0 else 0
            else:
                similarity = 0

            if similarity >= threshold:
                similar.append({
                    **case,
                    'similarity_score': similarity
                })

        # Sort by similarity and return top N
        similar.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar[:limit]

    async def search_by_principle(
        self,
        principle: str
    ) -> List[Dict[str, Any]]:
        """Search cases by constitutional principle."""
        return [
            case for case in self.cases
            if principle in case.get('principles_cited', [])
        ]

    async def search_by_actor(
        self,
        actor: str
    ) -> List[Dict[str, Any]]:
        """Search cases by actor."""
        return [
            case for case in self.cases
            if case.get('actor') == actor
        ]

    async def get_decision_rate_for_principle(
        self,
        principle: str
    ) -> Dict[str, Any]:
        """Get decision statistics for a principle."""
        principle_cases = await self.search_by_principle(principle)

        if not principle_cases:
            return {
                'principle': principle,
                'total_cases': 0,
                'allowed': 0,
                'denied': 0,
                'rate': 0
            }

        allowed = sum(1 for c in principle_cases if c.get('allowed', False))
        denied = len(principle_cases) - allowed

        return {
            'principle': principle,
            'total_cases': len(principle_cases),
            'allowed': allowed,
            'denied': denied,
            'rate': allowed / len(principle_cases) if principle_cases else 0
        }

    async def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored cases."""
        if not self.cases:
            return {
                'total_cases': 0,
                'allowed_decisions': 0,
                'denied_decisions': 0,
                'decision_rate': 0,
                'principles_cited': [],
                'actors': [],
            }

        allowed = sum(1 for c in self.cases if c.get('allowed', False))
        denied = len(self.cases) - allowed

        # Aggregate principles and actors
        all_principles = set()
        all_actors = set()
        for case in self.cases:
            all_principles.update(case.get('principles_cited', []))
            if case.get('actor'):
                all_actors.add(case['actor'])

        return {
            'total_cases': len(self.cases),
            'allowed_decisions': allowed,
            'denied_decisions': denied,
            'decision_rate': allowed / len(self.cases) if self.cases else 0,
            'principles_cited': list(all_principles),
            'actors': list(all_actors),
            'cases_per_principle': {
                p: sum(1 for c in self.cases if p in c.get('principles_cited', []))
                for p in all_principles
            }
        }

    async def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific case by ID."""
        for case in self.cases:
            if case['id'] == case_id:
                return case
        return None

    async def get_all_cases(self) -> List[Dict[str, Any]]:
        """Get all stored cases."""
        return self.cases.copy()
