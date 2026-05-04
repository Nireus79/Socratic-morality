"""Socratic Morality - Constitutional AI Governance Framework

A comprehensive framework for implementing constitutional AI with ethical reasoning,
governance decisions, and moral precedent learning.
"""

# Governor and decision making
from .governor import Governor, GovernorDecision, DecisionType

# Constitution and principles
from .constitution import Constitution

# Capabilities and access control
from .security import CapabilityToken, CapabilityValidator

# Precedent and learning
from .precedent import MoralPrecedentEngine, PrecedentCase

# Ethical analysis
from .ethics import EthicalDeliberationEngine, ExplanationGenerator

# Storage backends
from .storage import StorageBackend, SQLiteStorage

__version__ = "0.0.3"

__all__ = [
    # Governor and decisions
    "Governor",
    "GovernorDecision",
    "DecisionType",
    # Constitution
    "Constitution",
    # Security
    "CapabilityToken",
    "CapabilityValidator",
    # Precedent
    "MoralPrecedentEngine",
    "PrecedentCase",
    # Ethics
    "EthicalDeliberationEngine",
    "ExplanationGenerator",
    # Storage
    "StorageBackend",
    "SQLiteStorage",
]
