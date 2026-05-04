# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0-alpha] - 2026-05-04

### Added
- Initial Governor class with `evaluate()` API
- Constitutional framework with YAML/JSON support
- GovernorDecision model with decision types (allow/deny/escalate/block)
- Ethical Deliberation Engine (Phase 1 - framework structure)
- Moral Precedent Engine for case storage and retrieval
- Basic test suite (6 tests)
- ReadTheDocs documentation setup
- GitHub Actions CI/CD workflows

### Features
- Constitutional principle and rule evaluation
- Decision tracking with unique IDs
- Precedent case storage
- Multi-framework ethical analysis structure
- Capability-based access control (CapabilityToken)
- Storage backend interface (InMemoryStorage)

### Documentation
- README with quick start guide
- Installation instructions
- User guide with examples
- API structure documentation

### Known Limitations
- LLM-based ethical analysis not yet integrated
- Framework adapters (LangChain, AutoGen, CrewAI) not yet implemented
- Storage backends (SQLite, PostgreSQL) not yet implemented
- No distributed storage or persistence
- Basic similarity search (string-based, not semantic)

## Planned Releases

### [1.0.0-beta] - Phase 2 (Weeks 3-9)
- Full multi-framework ethical analysis with LLM
- Moral precedent semantic similarity search
- Framework adapters
- Advanced explanation generation

### [1.0.0] - Phase 3 (Weeks 7-12)
- Zero-trust architecture
- Capability-based security system
- Multiple storage backends (SQLite, PostgreSQL)
- Advanced monitoring & observability
- Production-grade security

