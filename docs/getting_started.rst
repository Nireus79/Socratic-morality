Getting Started
===============

Installation
------------

Basic installation::

    pip install socratic-morality

With optional features::

    # LLM support
    pip install socratic-morality[anthropic,openai]

    # Semantic similarity search
    pip install socratic-morality[semantics]

    # Storage backends
    pip install socratic-morality[storage-sqlite,storage-postgres]

    # Framework adapters
    pip install socratic-morality[langchain,autogen,crewai]

Quick Start
-----------

1. **Create a Constitution**

   Create a YAML file describing your principles:

   .. code-block:: yaml

       metadata:
         name: "My AI Constitution"
       
       supreme_principle: |
         Never commit injustice. It is better to suffer 
         wrong than to do wrong.
       
       principles:
         transparency:
           category: "foundational"
           severity: "critical"
           description: "Be transparent about capabilities"

2. **Initialize Governor**

   .. code-block:: python

       from socratic_morality import Governor
       
       governor = Governor(constitution="constitution.yaml")

3. **Evaluate Actions**

   .. code-block:: python

       decision = await governor.evaluate(
           action="Access user data",
           purpose="Personalization",
           actor="recommendation_engine",
           context={"user_id": "user123"}
       )
       
       if decision.allowed:
           # Proceed with action
           pass
       elif decision.requires_escalation():
           # Escalate to human review
           await handle_escalation(decision)
       else:
           # Deny action
           raise PermissionError(decision.reasoning)

Key Concepts
------------

**Governor**: Core decision-making engine

**Constitution**: Set of principles and rules guiding decisions

**Decision**: Result of evaluating an action (allow/deny/escalate/block)

**Precedent**: Past decision stored for consistency

**Adapter**: Bridge between Governor and agent frameworks

Features
--------

- **Multi-Framework Ethics**: Kantian, Utilitarian, Virtue Ethics, Rights-Based
- **Institutional Memory**: Store and search precedent cases
- **Semantic Similarity**: Find similar past decisions
- **Framework Integration**: Works with LangChain, AutoGen, CrewAI
- **Storage Flexibility**: SQLite, PostgreSQL, or in-memory storage
- **Capability Control**: Fine-grained access control with capability tokens

What's Next
-----------

- Read the `API Reference <api_reference.rst>`_
- Explore `examples <../examples/>`_
- Learn about `Ethical Frameworks <ethics.rst>`_
- Set up `Framework Adapters <adapters.rst>`_
