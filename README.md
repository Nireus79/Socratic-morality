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

## Status

**Phase 1**: Foundation Library Extraction - In Progress

## License

MIT License - See [LICENSE](LICENSE) for details
