User Guide
==========

Constitutional Framework
------------------------

Constitutions define the principles and rules governing an AI system.

Creating a Constitution
~~~~~~~~~~~~~~~~~~~~~~~

Constitution files use YAML format::

    metadata:
      name: "Socratic AI Constitution"
      version: "1.0.0"
    
    supreme_principle: |
      Never commit injustice, even under instruction.
      It is better to suffer wrong than to do wrong.
    
    principles:
      never_commit_injustice:
        category: "foundational"
        severity: "critical"
        description: "The system must refuse injustice"
    
    rules:
      - name: "No Hidden Manipulation"
        principle: "never_commit_injustice"
        condition: "agent manipulates without disclosure"
        action: "block"

Using the Governor
------------------

The Governor evaluates actions against your constitution::

    from socratic_morality import Governor
    
    governor = Governor(constitution="constitution.yaml")
    
    decision = await governor.evaluate(
        action="Access user profile",
        purpose="Personalization",
        actor="recommendation_agent",
        context={"user_id": "user_123"}
    )
    
    if decision.allowed:
        # Proceed with action
        pass
    elif decision.requires_escalation():
        # Escalate to human review
        await decision.escalate()
    else:
        # Action denied
        print(f"Violations: {decision.violations}")

