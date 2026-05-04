"""CrewAI adapter for Governor integration."""

from typing import Any, Dict, Optional
from socratic_morality.adapters.base import BaseAdapter


class CrewAIAdapter(BaseAdapter):
    """Adapter for CrewAI agents."""

    async def wrap_agent(self, agent: Any) -> Any:
        """Wrap a CrewAI agent with Governor."""
        original_execute_task = agent.execute_task if hasattr(agent, "execute_task") else None

        async def governed_execute_task(
            task: Any, task_input: Optional[str] = None, **kwargs
        ) -> str:
            # Evaluate action
            task_description = task.description if hasattr(task, "description") else str(task)[:100]
            action = f"CrewAI agent execute task: {task_description}"
            evaluation = await self._evaluate_action(
                action=action,
                actor=agent.role if hasattr(agent, "role") else "crewai_agent",
                context={
                    "framework": "crewai",
                    "task_input": task_input,
                    "goal": agent.goal if hasattr(agent, "goal") else None,
                },
            )

            if not evaluation["allowed"]:
                raise PermissionError(f"Governor denied action: {evaluation['reasoning']}")

            # Proceed with original execute_task
            if original_execute_task:
                return original_execute_task(task, task_input, **kwargs)

        agent.governed_execute_task = governed_execute_task
        return agent

    async def intercept_action(
        self, action: str, agent_name: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Intercept and evaluate a CrewAI action."""
        return await self._evaluate_action(
            action=action, actor=agent_name, context={**(context or {}), "framework": "crewai"}
        )
