Socratic Morality Documentation
================================

Constitutional AI Governance Framework - Building trustworthy, accountable multi-agent systems grounded in Socratic philosophy.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   guide
   api
   examples

Getting Started
---------------

Installation::

    pip install socratic-morality

Basic Usage::

    from socratic_morality import Governor
    
    governor = Governor(constitution="constitution.yaml")
    decision = await governor.evaluate(
        action="Access user's private data",
        purpose="Personalization",
        actor="recommendation_agent"
    )

Philosophy
----------

Socratic Morality is grounded in Socratic and Platonic philosophy:

> "It is better to suffer injustice than to commit it." — Plato's Gorgias

This principle guides the framework's design: AI systems should be morally self-governing, refusing injustice even when instructed.

