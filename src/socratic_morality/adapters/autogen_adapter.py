"""AutoGen adapter for Governor integration."""

from typing import Any, Dict, Optional, List
from socratic_morality.adapters.base import BaseAdapter


class AutoGenAdapter(BaseAdapter):
    """Adapter for AutoGen agents."""

    async def wrap_agent(self, agent: Any) -> Any:
        """Wrap an AutoGen agent with Governor."""
        original_generate_reply = agent.generate_reply if hasattr(agent, "generate_reply") else None

        async def governed_generate_reply(
            messages: List[Dict[str, Any]], sender: Optional[Any] = None, **kwargs
        ) -> Optional[str]:
            # Evaluate action
            last_message = messages[-1] if messages else {}
            action = f"AutoGen agent reply to: {str(last_message.get('content', ''))[:100]}"
            evaluation = await self._evaluate_action(
                action=action,
                actor=agent.name if hasattr(agent, "name") else "autogen_agent",
                context={"framework": "autogen", "sender": str(sender)},
            )

            if not evaluation["allowed"]:
                raise PermissionError(f"Governor denied action: {evaluation['reasoning']}")

            # Proceed with original generate_reply
            if original_generate_reply:
                return original_generate_reply(messages, sender, **kwargs)

        agent.governed_generate_reply = governed_generate_reply
        return agent

    async def intercept_action(
        self, action: str, agent_name: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Intercept and evaluate an AutoGen action."""
        return await self._evaluate_action(
            action=action, actor=agent_name, context={**(context or {}), "framework": "autogen"}
        )
