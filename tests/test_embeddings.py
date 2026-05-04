"""Tests for semantic embeddings functionality."""
import pytest
from unittest.mock import Mock
from socratic_morality.precedent.embeddings import SemanticEmbeddings


class TestSemanticEmbeddingsInitialization:
    """Tests for SemanticEmbeddings initialization."""

    def test_initialization_with_default_model(self):
        """Test initialization with default model name."""
        embeddings = SemanticEmbeddings()
        assert embeddings.model_name == "all-MiniLM-L6-v2"
        assert isinstance(embeddings.embeddings_cache, dict)

    def test_initialization_with_custom_model(self):
        """Test initialization with custom model name."""
        embeddings = SemanticEmbeddings(model_name="all-mpnet-base-v2")
        assert embeddings.model_name == "all-mpnet-base-v2"


class TestEmbeddingGeneration:
    """Tests for embedding generation."""

    def test_embed_without_model(self):
        """Test embedding generation when model is not available."""
        embeddings = SemanticEmbeddings()
        embeddings.model = None
        result = embeddings.embed("test text")
        assert result is None

    def test_embed_caching(self):
        """Test that embeddings are cached."""
        embeddings = SemanticEmbeddings()
        embeddings.model = None
        embeddings.embeddings_cache["cached_text"] = [0.1, 0.2, 0.3]
        result = embeddings.embed("cached_text")
        assert result == [0.1, 0.2, 0.3]

    def test_embed_error_handling(self):
        """Test embedding generation with error handling."""
        embeddings = SemanticEmbeddings()
        if embeddings.model:
            embeddings.model.encode = Mock(side_effect=Exception("Model error"))
            result = embeddings.embed("test text")
            assert result is None


class TestCosineSimilarity:
    """Tests for cosine similarity calculation."""

    def test_cosine_similarity_identical_vectors(self):
        """Test cosine similarity of identical vectors."""
        vec = [1.0, 0.0, 0.0]
        similarity = SemanticEmbeddings.cosine_similarity(vec, vec)
        assert similarity == pytest.approx(1.0)

    def test_cosine_similarity_orthogonal_vectors(self):
        """Test cosine similarity of orthogonal vectors."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0]
        similarity = SemanticEmbeddings.cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(0.0)

    def test_cosine_similarity_opposite_vectors(self):
        """Test cosine similarity of opposite vectors."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [-1.0, 0.0, 0.0]
        similarity = SemanticEmbeddings.cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(-1.0)

    def test_cosine_similarity_partial_overlap(self):
        """Test cosine similarity with partial overlap."""
        vec1 = [1.0, 1.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        similarity = SemanticEmbeddings.cosine_similarity(vec1, vec2)
        assert 0 < similarity < 1

    def test_cosine_similarity_empty_vectors(self):
        """Test cosine similarity with empty vectors."""
        similarity = SemanticEmbeddings.cosine_similarity([], [])
        assert similarity == 0.0

    def test_cosine_similarity_different_length(self):
        """Test cosine similarity with different length vectors."""
        vec1 = [1.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        similarity = SemanticEmbeddings.cosine_similarity(vec1, vec2)
        assert similarity == 0.0

    def test_cosine_similarity_zero_magnitude(self):
        """Test cosine similarity when one vector has zero magnitude."""
        vec1 = [0.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        similarity = SemanticEmbeddings.cosine_similarity(vec1, vec2)
        assert similarity == 0.0

    def test_cosine_similarity_large_vectors(self):
        """Test cosine similarity with large dimension vectors."""
        vec1 = [float(i) for i in range(100)]
        vec2 = [float(i) for i in range(100)]
        similarity = SemanticEmbeddings.cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(1.0)


class TestIsAvailable:
    """Tests for availability checking."""

    def test_is_available_without_model(self):
        """Test is_available when model is None."""
        embeddings = SemanticEmbeddings()
        embeddings.model = None
        assert embeddings.is_available() is False

    def test_is_available_with_model(self):
        """Test is_available when model is present."""
        embeddings = SemanticEmbeddings()
        embeddings.model = Mock()
        assert embeddings.is_available() is True
