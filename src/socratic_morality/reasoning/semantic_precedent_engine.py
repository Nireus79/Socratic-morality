"""Semantic Precedent Matching Engine using embeddings."""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import math


@dataclass
class SimilarPrecedent:
    """A precedent similar to a query action."""

    precedent_data: Dict[str, Any]
    semantic_similarity: float  # 0-1
    semantic_distance: float  # Euclidean distance
    relevance_score: float  # Combined score 0-1
    matching_principles: List[str] = field(default_factory=list)


@dataclass
class PrecedentMatch:
    """A precedent matched by semantic distance."""

    case_id: str
    action: str
    decision: str  # allowed/denied
    semantic_distance: float
    similarity_score: float
    matching_principles: List[str] = field(default_factory=list)
    confidence: float = 0.5


class SemanticPrecedentEngine:
    """Semantic search engine for moral precedents using embeddings."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the semantic precedent engine.

        Args:
            model_name: Name of the sentence-transformers model to use.
        """
        self.model_name = model_name
        self.embeddings = None
        self.precedent_cases: List[Dict[str, Any]] = []
        self.embedding_cache: Dict[str, List[float]] = {}
        self._initialize_embeddings()

    def _initialize_embeddings(self) -> None:
        """Initialize semantic embeddings if available."""
        try:
            from socratic_morality.precedent.embeddings import SemanticEmbeddings

            self.embeddings = SemanticEmbeddings(self.model_name)
        except ImportError:
            self.embeddings = None

    def compute_embedding(self, text: str) -> Optional[List[float]]:
        """Get text embedding.

        Args:
            text: Text to embed.

        Returns:
            Embedding as list of floats, or None if unavailable.
        """
        if not self.embeddings:
            return None

        return self.embeddings.embed(text)

    def find_semantically_similar_precedents(
        self, action: str, top_k: int = 5, threshold: float = 0.3
    ) -> List[SimilarPrecedent]:
        """Find semantically similar precedents.

        Args:
            action: Action to find similar cases for.
            top_k: Maximum number of results.
            threshold: Minimum similarity threshold (0-1).

        Returns:
            List of SimilarPrecedent objects sorted by relevance.
        """
        if not self.embeddings or not self.precedent_cases:
            return []

        action_embedding = self.compute_embedding(action)
        if not action_embedding:
            return []

        similar_cases = []

        for case in self.precedent_cases:
            case_action = case.get("action", "")
            case_embedding = self.compute_embedding(case_action)

            if not case_embedding:
                continue

            # Compute similarity
            similarity = self._cosine_similarity(action_embedding, case_embedding)
            distance = self._euclidean_distance(action_embedding, case_embedding)

            if similarity >= threshold:
                # Compute relevance score (weighted combination)
                relevance = self._compute_relevance_score(similarity, case, action)

                matching_principles = self._find_matching_principles(case, action)

                similar_cases.append(
                    SimilarPrecedent(
                        precedent_data=case,
                        semantic_similarity=similarity,
                        semantic_distance=distance,
                        relevance_score=relevance,
                        matching_principles=matching_principles,
                    )
                )

        # Sort by relevance and return top-k
        similar_cases.sort(key=lambda x: x.relevance_score, reverse=True)
        return similar_cases[:top_k]

    def compute_semantic_similarity(self, action1: str, action2: str) -> float:
        """Compare semantic similarity between two actions.

        Args:
            action1: First action.
            action2: Second action.

        Returns:
            Similarity score (0-1).
        """
        if not self.embeddings:
            return 0.0

        embedding1 = self.compute_embedding(action1)
        embedding2 = self.compute_embedding(action2)

        if not embedding1 or not embedding2:
            return 0.0

        return self._cosine_similarity(embedding1, embedding2)

    def cluster_precedents(self) -> Dict[str, List[Dict[str, Any]]]:
        """Group related precedents using semantic similarity.

        Returns:
            Dictionary mapping cluster names to precedent lists.
        """
        if not self.precedent_cases:
            return {}

        clusters = {}
        used_indices = set()

        # Simple clustering: find a seed and group similar cases around it
        for i, seed_case in enumerate(self.precedent_cases):
            if i in used_indices:
                continue

            seed_action = seed_case.get("action", "")
            cluster_id = seed_case.get("id", f"cluster_{i}")
            cluster = [seed_case]
            used_indices.add(i)

            # Find similar cases for this seed
            for j, compare_case in enumerate(self.precedent_cases):
                if j in used_indices or i == j:
                    continue

                similarity = self.compute_semantic_similarity(
                    seed_action, compare_case.get("action", "")
                )

                if similarity >= 0.5:  # Clustering threshold
                    cluster.append(compare_case)
                    used_indices.add(j)

            clusters[cluster_id] = cluster

        return clusters

    def get_precedent_by_semantic_distance(self, action: str, limit: int = 10) -> List[PrecedentMatch]:
        """Get precedents ranked by semantic distance.

        Args:
            action: Action to match.
            limit: Maximum number to return.

        Returns:
            List of PrecedentMatch objects sorted by distance (closest first).
        """
        if not self.embeddings or not self.precedent_cases:
            return []

        action_embedding = self.compute_embedding(action)
        if not action_embedding:
            return []

        matches = []

        for case in self.precedent_cases:
            case_action = case.get("action", "")
            case_embedding = self.compute_embedding(case_action)

            if not case_embedding:
                continue

            distance = self._euclidean_distance(action_embedding, case_embedding)
            similarity = self._cosine_similarity(action_embedding, case_embedding)

            matching_principles = self._find_matching_principles(case, action)
            decision = "allowed" if case.get("allowed", False) else "denied"

            # Convert distance to confidence (closer = more confident)
            confidence = max(0.0, 1.0 - (distance / 10.0))

            matches.append(
                PrecedentMatch(
                    case_id=case.get("id", "unknown"),
                    action=case_action,
                    decision=decision,
                    semantic_distance=distance,
                    similarity_score=similarity,
                    matching_principles=matching_principles,
                    confidence=confidence,
                )
            )

        # Sort by distance (closest first)
        matches.sort(key=lambda x: x.semantic_distance)
        return matches[:limit]

    def add_precedent_case(self, case: Dict[str, Any]) -> str:
        """Add a precedent case to the engine.

        Args:
            case: Case dictionary with action, decision, principles, etc.

        Returns:
            Case ID.
        """
        if "id" not in case:
            case["id"] = f"case_{len(self.precedent_cases)}"

        self.precedent_cases.append(case)
        return case["id"]

    def add_precedent_cases(self, cases: List[Dict[str, Any]]) -> List[str]:
        """Add multiple precedent cases.

        Args:
            cases: List of case dictionaries.

        Returns:
            List of case IDs.
        """
        case_ids = []
        for case in cases:
            case_id = self.add_precedent_case(case)
            case_ids.append(case_id)
        return case_ids

    def get_all_precedents(self) -> List[Dict[str, Any]]:
        """Get all stored precedents.

        Returns:
            List of precedent cases.
        """
        return self.precedent_cases.copy()

    def clear_precedents(self) -> None:
        """Clear all precedent cases."""
        self.precedent_cases.clear()
        self.embedding_cache.clear()

    def get_embedding_cache_stats(self) -> Dict[str, int]:
        """Get statistics about embedding cache.

        Returns:
            Dictionary with cache statistics.
        """
        return {
            "cached_embeddings": len(self.embedding_cache),
            "total_precedents": len(self.precedent_cases),
            "embeddings_available": self.embeddings is not None,
        }

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Compute cosine similarity between two vectors.

        Args:
            vec1: First vector.
            vec2: Second vector.

        Returns:
            Cosine similarity (0-1).
        """
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    @staticmethod
    def _euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
        """Compute Euclidean distance between two vectors.

        Args:
            vec1: First vector.
            vec2: Second vector.

        Returns:
            Euclidean distance.
        """
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return float("inf")

        sum_squares = sum((a - b) ** 2 for a, b in zip(vec1, vec2))
        return math.sqrt(sum_squares)

    def _compute_relevance_score(self, similarity: float, case: Dict[str, Any], action: str) -> float:
        """Compute combined relevance score.

        Args:
            similarity: Semantic similarity (0-1).
            case: The precedent case.
            action: The query action.

        Returns:
            Relevance score (0-1).
        """
        # Start with semantic similarity (60% weight)
        score = similarity * 0.6

        # Add principle matching boost (20% weight)
        matching_principles = self._find_matching_principles(case, action)
        principle_bonus = min(0.2, len(matching_principles) * 0.05)
        score += principle_bonus

        # Add recency bonus if available (20% weight)
        if "timestamp" in case:
            # Recent cases get slight boost
            score += 0.05

        return min(1.0, score)

    @staticmethod
    def _find_matching_principles(case: Dict[str, Any], action: str) -> List[str]:
        """Find principles matching between case and action.

        Args:
            case: The precedent case.
            action: The query action.

        Returns:
            List of matching principle names.
        """
        matching = []
        case_principles = set(case.get("principles_cited", []))
        action_lower = action.lower()

        # Check if action mentions any of the case's principles
        for principle in case_principles:
            if principle.lower() in action_lower:
                matching.append(principle)

        return matching
