API Reference
=============

Governor
--------

.. py:class:: Governor(constitution, llm_provider="anthropic")

    Core class for constitutional AI governance.

    .. py:method:: async evaluate(action, purpose="", actor="", context=None, high_impact=False)
    
        Evaluate an action against the constitution.
        
        :param str action: Action to evaluate
        :param str purpose: Purpose of the action
        :param str actor: Agent performing the action
        :param dict context: Contextual information
        :param bool high_impact: Whether action has high impact
        :return: GovernorDecision object
        :rtype: GovernorDecision

Ethical Deliberation
--------------------

.. py:class:: EthicalDeliberationEngine(llm_provider="anthropic", constitution=None)

    Performs multi-framework ethical analysis.

    .. py:method:: async analyze(action, purpose="", actor="", context=None, violations=None)
    
        Analyze action using 4 ethical frameworks:
        - Kantian ethics
        - Utilitarian ethics
        - Virtue ethics
        - Rights-based ethics
        
        :param str action: Action to analyze
        :return: Dictionary with frameworks and overall decision

Moral Precedent
---------------

.. py:class:: MoralPrecedentEngine(storage_type="memory", constitution=None)

    Stores and retrieves decision precedents.

    .. py:method:: async store_case(action, decision, reasoning, principles_cited, stakeholders_affected)
    
        Store a precedent case.
        
        :return: Case ID

    .. py:method:: async find_similar_cases(action, limit=5, threshold=0.3)
    
        Find similar precedent cases.
        
        :param str action: Action to find similar cases for
        :return: List of similar cases with similarity scores

    .. py:method:: async find_similar_cases_semantic(action, limit=5, threshold=0.3)
    
        Find semantically similar cases using embeddings.
        
        Requires sentence-transformers: pip install socratic-morality[semantics]

Storage Backends
----------------

.. py:class:: SQLiteStorage(database_path="socratic_morality.db")

    SQLite storage for development and testing.

.. py:class:: PostgreSQLStorage(host="localhost", port=5432, database="socratic_morality")

    PostgreSQL storage for production deployments.
    
    Requires asyncpg: pip install socratic-morality[storage-postgres]

Capability Management
---------------------

.. py:class:: CapabilityToken(agent_id, capabilities)

    Token representing agent capabilities.

    .. py:method:: has_capability(capability)
    
        Check if agent has a specific capability.

.. py:class:: CapabilityValidator()

    Manages and validates agent capabilities.

    .. py:method:: register_agent(agent_id, capabilities)
    
        Register an agent with capabilities.

    .. py:method:: validate(agent_id, required_capability)
    
        Validate agent has required capability.

Framework Adapters
------------------

.. py:class:: LangChainAdapter(governor)

    Integrates Governor with LangChain agents.

.. py:class:: AutoGenAdapter(governor)

    Integrates Governor with AutoGen agents.

.. py:class:: CrewAIAdapter(governor)

    Integrates Governor with CrewAI agents.
