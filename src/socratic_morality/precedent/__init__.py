"""Precedent - Moral case storage and similarity search."""

from .engine import MoralPrecedentEngine, PrecedentCase
from .embeddings import SemanticEmbeddings

__all__ = ["MoralPrecedentEngine", "PrecedentCase", "SemanticEmbeddings"]
