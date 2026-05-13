# Socratic Morality

[![PyPI](https://img.shields.io/pypi/v/socratic-morality.svg)](https://pypi.org/project/socratic-morality/)
[![Downloads](https://img.shields.io/pypi/dm/socratic-morality.svg)](https://pypi.org/project/socratic-morality/)
[![GitHub](https://img.shields.io/github/stars/Nireus79/Socratic-morality.svg?style=social)](https://github.com/Nireus79/Socratic-morality)
[![License](https://img.shields.io/github/license/Nireus79/Socratic-morality.svg)](LICENSE)


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

## Complete Module Architecture (7 Modules)

### Phase 1 - Foundation (3 modules)
1. **Governor** - Core decision-making engine
   - Constraint checking and validation
   - Decision tracking with audit trails
   - Multi-dimensional decision analysis

2. **Constitution Framework** - YAML-based governance
   - Supreme principles and axioms
   - Named principles with severity levels
   - Agent capabilities and permissions
   - Action policies and constraints
   - Escalation rules and approval workflows

3. **CapabilityToken System** - Fine-grained access control
   - Token-based permissions
   - Resource authorization
   - Capability validation
   - Storage backends (SQLite, PostgreSQL)

### Phase 2 - Ethical Reasoning (3 modules)
4. **Multi-Framework Ethical Analysis**
   - Kantian deontological analysis (duty, dignity, universality)
   - Utilitarian consequentialist analysis (benefit/harm, extremes)
   - Virtue ethics analysis (virtues, vices, flourishing)
   - Rights-based analysis (fundamental rights, consent)
   - LLM integration with keyword analysis fallback

5. **Moral Precedent Engine** - Case-based reasoning
   - Decision storage and retrieval
   - Similarity-based matching
   - Consistency analysis
   - Precedent clustering and history

6. **Explanation Generation** - Transparent reasoning
   - Reasoning artifact export
   - Decision justification
   - Explanation reports
   - Framework analysis summaries

### Phase 3 - Advanced Governance (4 modules - NEW ✨)
7. **Constitutional Enforcer** - Active principle enforcement
   - Real-time principle verification
   - Principle violation detection with severity levels
   - Agent capability validation
   - Constitutional reasoning generation

8. **Unified Governance API** - Single entry point for all decisions
   - `evaluate(action, context, actor)` - Main interface
   - Constitutional checks (first gate)
   - Integrated ethical deliberation (4 frameworks)
   - Precedent analysis with semantic similarity
   - Threat detection and anomaly analysis
   - Optional interactive Socratic dialogue
   - Complete decision history and explanation reports
   - Batch evaluation support

9. **Socratic Dialogue Engine** - Interactive ethical reasoning
   - 8 Socratic approaches (exposing contradictions, testing universality, examining assumptions, probing consequences, inviting counterarguments, clarifying definitions)
   - 7 question categories (stakeholder, consequence, principle, alternative, assumption, vulnerability, outcome)
   - 40+ built-in Socratic questions
   - Interactive dialogue with Claude LLM
   - Dialogue synthesis and insight extraction
   - Dialogue history tracking

10. **Semantic Precedent Matching** - Advanced similarity search
    - Sentence-transformer embeddings (semantic matching)
    - Combined lexical + semantic similarity (40/60 blend)
    - Embedding caching for performance
    - Precedent clustering by conclusion type
    - Context-aware relevance scoring

### Phase 3 Extensions (3 modules - NEW ✨)
11. **Care Ethics Framework** - Relational moral analysis
    - Relationship mapping and analysis
    - Vulnerability assessment
    - Care response adequacy evaluation
    - Care violation detection
    - Emphasis on interdependence and caring

12. **Remediation Engine** - Constraint violation handling
    - 5 remediation strategies:
      - MODIFY_ACTION: Adjust action parameters
      - ADD_SAFEGUARDS: Add protective measures
      - REJECT_AND_PROPOSE_ALTERNATIVE: Suggest better approach
      - ESCALATE_WITH_CONSTRAINTS: Allow with restrictions
      - ROLLBACK: Reverse decisions
    - Intelligent suggestion generation
    - Auto-remediation for safe violations
    - Decision rollback capability
    - Complete audit trail

13. **Resource Monitor** - Real-time resource enforcement
    - CPU, memory, file descriptor, process monitoring
    - Soft and hard limit enforcement
    - Violation detection and escalation
    - Comprehensive usage reporting
    - Session-based monitoring lifecycle
    - Integration with sandbox execution

## Release Status

**v0.0.5 - COMPLETE ✅ (May 2026)**

All 13 modules fully implemented, tested, and documented:
- Phase 1: 3 foundation modules ✅
- Phase 2: 3 ethical reasoning modules ✅
- Phase 3: 4 advanced governance modules ✅
- Phase 3 Extensions: 3 specialized modules ✅

**Available on PyPI:**
```bash
pip install socratic-morality==0.0.5
```

**Test Coverage**: 100% (71/71 tests passing)
**Code Quality**: All linting and type checks passing
**Documentation**: Complete API docs and examples included

## License

MIT License - See [LICENSE](LICENSE) for details


---

## Part of Socrates AI Ecosystem

This package is a component of [**Socrates AI**](https://github.com/Nireus79/Socrates), a production-ready platform for building intelligent multi-agent systems with constitutional governance.

### Use This Package Standalone:
```bash
pip install socratic-morality
```

### Or As Part of Socrates Platform:
```bash
pip install socrates-ai  # Includes 37+ modules + all 11 packages
```

### Integration Example:

See the [**Socrates ECOSYSTEM.md**](https://github.com/Nireus79/Socrates/blob/main/ECOSYSTEM.md#layer-2-specialized-libraries) for detailed integration examples showing how to use socratic-morality with other Socratic packages.

**Related packages you might use together:**
- See [Complete Package Map](https://github.com/Nireus79/Socrates/blob/main/ECOSYSTEM.md)

### More Information:
- 📖 [Full Socrates Documentation](https://github.com/Nireus79/Socrates/tree/main/docs)
- 🏗️ [Complete Architecture Guide](https://github.com/Nireus79/Socrates/blob/main/ECOSYSTEM.md)
- 💬 [Socrates Discussions](https://github.com/Nireus79/Socrates/discussions)

---
