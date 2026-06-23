"""Semantic embeddings for precedent similarity search."""

import math
from typing import Dict, List, Optional


class SemanticEmbeddings:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.embeddings_cache: Dict[str, List[float]] = {}
        self._load_model()

    def _load_model(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(self.model_name)
        except ImportError:
            self.model = None

    def embed(self, text: str) -> Optional[List[float]]:
        if not self.model:
            return None
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            embedding_list = embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
            self.embeddings_cache[text] = embedding_list
            return embedding_list
        except Exception:
            return None

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    def is_available(self) -> bool:
        return self.model is not None
