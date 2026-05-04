"""LangChain adapter example."""
import asyncio
from socratic_morality import Governor
from socratic_morality.adapters import LangChainAdapter


async def main():
    """Run LangChain adapter example."""
    # Create governor
    governor = Governor(constitution={'principles': {}, 'rules': []})
    
    # Create adapter
    adapter = LangChainAdapter(governor)
    
    # Create mock LangChain agent
    class MockLangChainAgent:
        def __init__(self):
            self.name = "langchain_agent"
        
        def invoke(self, input_data):
            return f"Response to: {input_data}"
    
    # Wrap agent with Governor
    agent = MockLangChainAgent()
    governed_agent = await adapter.wrap_agent(agent)
    
    print(f"Wrapped agent: {governed_agent.name}")
    print("Agent is now governed by the Constitution!")
    
    # Check action
    result = await adapter.intercept_action(
        action="Process user query",
        agent_name=agent.name
    )
    
    print(f"Action allowed: {result['allowed']}")
    print(f"Decision: {result['decision_type']}")


if __name__ == "__main__":
    asyncio.run(main())
