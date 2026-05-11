"""Ethics - Multi-framework ethical analysis."""

from .deliberation import EthicalDeliberationEngine
from .explanations import ExplanationGenerator
from .care_ethics import (
    CareEthicsAnalyzer,
    CareEthicsResult,
    CareConclusion,
    Relationship,
    VulnerabilityScore,
    CareViolation,
    CareAnalysis,
)

__all__ = [
    "EthicalDeliberationEngine",
    "ExplanationGenerator",
    "CareEthicsAnalyzer",
    "CareEthicsResult",
    "CareConclusion",
    "Relationship",
    "VulnerabilityScore",
    "CareViolation",
    "CareAnalysis",
]
