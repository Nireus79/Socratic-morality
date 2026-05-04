"""Framework adapters for integrating Governor with various agent systems."""

from socratic_morality.adapters.base import BaseAdapter
from socratic_morality.adapters.langchain_adapter import LangChainAdapter
from socratic_morality.adapters.autogen_adapter import AutoGenAdapter
from socratic_morality.adapters.crewai_adapter import CrewAIAdapter

__all__ = ["BaseAdapter", "LangChainAdapter", "AutoGenAdapter", "CrewAIAdapter"]
