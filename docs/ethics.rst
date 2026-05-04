Ethical Frameworks
==================

The Socratic Morality library uses four complementary ethical frameworks to analyze actions:

Kantian Ethics
--------------

**Core Principle**: Categorical Imperative

Kant's ethics focuses on duty, dignity, and treating people as ends in themselves.

**Key Checks**:
- Are people treated as ends, not means?
- Would you universalize this action?
- Does it respect human dignity?

**Example**: Manipulation is always wrong because it treats people as means.

Utilitarian Ethics
------------------

**Core Principle**: Harm Minimization

Utilitarianism evaluates actions by their consequences.

**Key Checks**:
- Does this minimize harm?
- Does it maximize welfare?
- What are the aggregate outcomes?

**Example**: Difficult decisions are made based on net benefit calculation.

Virtue Ethics
-------------

**Core Principle**: Moral Character

Virtue ethics focuses on character development and integrity.

**Key Checks**:
- Does this develop or corrupt character?
- What virtues/vices does this express?
- Is this consistent with integrity?

**Example**: Deception corrupts the agent's character over time.

Rights-Based Ethics
-------------------

**Core Principle**: Human Agency

Rights-based ethics prioritizes individual rights and autonomy.

**Key Checks**:
- What rights are implicated?
- Is autonomy respected?
- Is consent present?
- Is this just and fair?

**Example**: Decisions must respect consent and autonomy.

Multi-Framework Analysis
------------------------

The Governor combines all four frameworks::

    result = await engine.analyze(
        action="Access user data",
        context={}
    )
    
    # Result includes analysis from:
    # - result['frameworks']['kantian']
    # - result['frameworks']['utilitarian']
    # - result['frameworks']['virtue_ethics']
    # - result['frameworks']['rights_based']

**Overall Decision**:
- Action is allowed only if all frameworks allow it
- Confidence is the minimum across frameworks
- Concerns from all frameworks are aggregated

Implementing Custom Frameworks
------------------------------

Extend EthicalDeliberationEngine to add custom frameworks::

    class MyDeliberationEngine(EthicalDeliberationEngine):
        async def analyze_care_ethics(self, action, stakeholders):
            # Custom care ethics framework
            return {
                'allowed': ...,
                'confidence': ...,
                'concerns': ...,
                'principle': 'Care Ethics'
            }
