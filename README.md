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

## Status

**Phase 1 & 2**: Complete ✅ (v0.0.3)
- Published to PyPI: `pip install socratic-morality==0.0.3`
- Used by: socratic-agents (governance integration)

## License

MIT License - See [LICENSE](LICENSE) for details
