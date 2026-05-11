# Socratic Morality

**Constitutional AI Governance Framework** - Building trustworthy, accountable multi-agent systems grounded in Socratic philosophy.

> "It is better to suffer injustice than to commit it." — Plato's Gorgias

## Quick Start

```bash
pip install socratic-morality
```

```python
from socratic_morality import Governor

governor = Governor(constitution="constitution.yaml", llm_provider="anthropic")
decision = await governor.evaluate(
    action="Access user's private data",
    purpose="Personalization",
    actor="recommendation_agent",
    context={"user_id": "user_123"}
)
```

## Documentation

- [API Reference](docs/)
- [Philosophy Guide](docs/)
- [Examples](examples/)

## Features

### Phase 1 - Foundation
- **Governor** - Core decision-making engine for constitutional AI checks
- **Constitution Framework** - YAML-based principles and rules
- **CapabilityToken System** - Fine-grained capability management
- **Storage Backends** - SQLite and PostgreSQL support

### Phase 2 - Ethical Reasoning
- **Multi-Framework Ethical Analysis**
  - Kantian deontological analysis
  - Utilitarian consequentialist analysis
  - Virtue ethics analysis
  - Rights-based analysis
  - LLM integration with fallback keyword analysis
- **Moral Precedent Engine** - Case-based decision tracking
- **Semantic Embeddings** - Similarity search with caching
- **Explanation Generation** - Transparent reasoning output

### Phase 3 - Advanced Governance (NEW ✨)
- **Constitutional Enforcer** - Real-time principle verification
  - Active runtime enforcement of all constitutional axioms
  - Principle violation detection with severity levels
  - Agent capability validation
- **Unified Governance API** - Single entry point: `evaluate(action, context, actor)`
  - Constitutional checks (first gate)
  - Integrated ethical deliberation (4 frameworks)
  - Precedent analysis with semantic similarity
  - Threat detection and anomaly analysis
  - Optional interactive Socratic dialogue
  - Complete decision history and explanation reports
- **Socratic Dialogue Engine** - Interactive ethical reasoning
  - Generates contextual Socratic questions
  - 6 different Socratic approaches (exposing contradictions, testing universality, etc.)
  - Multi-party dialogue support
  - Dialogue synthesis with insight extraction
  - 40+ built-in Socratic questions
- **Semantic Precedent Matching** - Advanced similarity search
  - Sentence-transformer embeddings for semantic matching
  - Combined lexical + semantic similarity (40/60 blend)
  - Embedding caching for performance
  - Precedent clustering by conclusion type
  - Context-aware relevance scoring

## Status

**Phase 1 & 2**: Complete ✅ (v0.0.3)
- Published to PyPI: `pip install socratic-morality==0.0.3`
- Used by: socratic-agents (governance integration)

**Phase 3**: Complete ✅ (v0.1.0 - in development)
- Constitutional Enforcer - Active principle enforcement
- Governance API - Unified decision interface
- Socratic Dialogue Engine - Interactive questioning
- Semantic Precedent Matching - Advanced similarity search
- All modules fully tested and integrated
- Expected release: May 2026

## License

MIT License - See [LICENSE](LICENSE) for details
