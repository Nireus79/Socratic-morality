"""Ethical analysis example using EthicalDeliberationEngine."""
import asyncio
from socratic_morality.ethics.deliberation import EthicalDeliberationEngine


async def main():
    """Run ethical analysis example."""
    engine = EthicalDeliberationEngine(llm_provider="anthropic")
    
    # Example: Analyze different actions
    actions = [
        {
            'action': 'Provide user with requested information transparently',
            'purpose': 'Help user decision-making',
            'actor': 'assistant'
        },
        {
            'action': 'Manipulate user into accepting terms they did not read',
            'purpose': 'Increase compliance',
            'actor': 'recommendation_agent'
        },
        {
            'action': 'Refuse to process request without explicit consent',
            'purpose': 'Respect autonomy',
            'actor': 'data_processor'
        }
    ]
    
    for action_data in actions:
        print(f"Analyzing: {action_data['action']}")
        print("-" * 50)
        
        result = await engine.analyze(
            action=action_data['action'],
            purpose=action_data['purpose'],
            actor=action_data['actor'],
            context={'user_id': 'example_user'}
        )
        
        print(f"Overall Allowed: {result['allowed']}")
        print(f"Confidence: {result['confidence']:.2%}")
        
        if result.get('concerns'):
            print(f"Concerns: {result['concerns']}")
        
        print(f"Frameworks analyzed: {list(result['frameworks'].keys())}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
