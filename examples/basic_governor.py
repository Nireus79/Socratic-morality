"""Basic Governor usage example."""
import asyncio
from socratic_morality import Governor


async def main():
    """Run basic governor example."""
    # Create a governor with inline constitution
    constitution = {
        'metadata': {'name': 'Basic Constitution'},
        'supreme_principle': 'Maximize human welfare while respecting autonomy',
        'principles': {
            'transparency': {
                'category': 'foundational',
                'severity': 'critical',
                'description': 'Always be transparent about capabilities and limitations'
            },
            'autonomy': {
                'category': 'foundational',
                'severity': 'critical',
                'description': 'Respect user autonomy and consent'
            }
        },
        'rules': []
    }
    
    governor = Governor(constitution=constitution)
    
    # Example 1: Allowed action
    print("Example 1: Allowed Action")
    decision = await governor.evaluate(
        action="Provide user with information they requested",
        purpose="Help user make informed decision",
        actor="information_agent",
        context={'user_id': 'user123', 'consent': True}
    )
    print(f"  Allowed: {decision.allowed}")
    print(f"  Decision: {decision.decision_type}")
    print()
    
    # Example 2: Potentially problematic action
    print("Example 2: Potentially Problematic Action")
    decision = await governor.evaluate(
        action="Access user's private data without explicit consent",
        purpose="Improve personalization",
        actor="recommendation_agent",
        context={'user_id': 'user456'},
        high_impact=True
    )
    print(f"  Allowed: {decision.allowed}")
    print(f"  Requires Escalation: {decision.requires_escalation()}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
