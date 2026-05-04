"""LangChain adapter for Governor integration."""
from typing import Any, Dict, Optional
from socratic_morality.adapters.base import BaseAdapter


class LangChainAdapter(BaseAdapter):
    """Adapter for LangChain agents."""

    async def wrap_agent(self, agent: Any) -> Any:
        """Wrap a LangChain agent with Governor."""
        original_invoke = agent.invoke if hasattr(agent, 'invoke') else None
        original_run = agent.run if hasattr(agent, 'run') else None

        async def governed_invoke(input_data: Any, **kwargs) -> Any:
            # Evaluate action
            action = f"LangChain agent invoke with input: {str(input_data)[:100]}"
            evaluation = await self._evaluate_action(
                action=action,
                actor=agent.name if hasattr(agent, 'name') else 'langchain_agent',
                context={'framework': 'langchain'}
            )

            if not evaluation['allowed']:
                raise PermissionError(
                    f"Governor denied action: {evaluation['reasoning']}"
                )

            # Proceed with original invoke
            if original_invoke:
                return original_invoke(input_data, **kwargs)

        agent.governed_invoke = governed_invoke
        return agent

    async def intercept_action(
        self,
        action: str,
        agent_name: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Intercept and evaluate a LangChain action."""
        return await self._evaluate_action(
            action=action,
            actor=agent_name,
            context={**(context or {}), 'framework': 'langchain'}
        )
