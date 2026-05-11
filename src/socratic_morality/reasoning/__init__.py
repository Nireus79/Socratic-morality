"""Reasoning module for Socratic dialogue and semantic precedent matching."""

from .socratic_dialogue_engine import (
    SocraticDialogueEngine,
    Question,
    Alternative,
    Exchange,
    DialogueResult,
    DialogueSynthesis,
    SocraticApproach,
    QuestionCategory,
)
from .semantic_precedent_engine import (
    SemanticPrecedentEngine,
    SimilarPrecedent,
    PrecedentMatch,
)

__all__ = [
    # Socratic Dialogue
    "SocraticDialogueEngine",
    "Question",
    "Alternative",
    "Exchange",
    "DialogueResult",
    "DialogueSynthesis",
    "SocraticApproach",
    "QuestionCategory",
    # Semantic Precedent
    "SemanticPrecedentEngine",
    "SimilarPrecedent",
    "PrecedentMatch",
]
