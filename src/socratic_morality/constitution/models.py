"""Constitution model and related types."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml


@dataclass
class Principle:
    """A constitutional principle."""

    name: str
    category: str = ""
    severity: str = "medium"
    description: str = ""
    source: str = ""


@dataclass
class Rule:
    """A constitutional rule."""

    name: str
    principle: str
    condition: str
    action: str = "deny"
    severity: str = "medium"
    requires_human_approval: bool = False


@dataclass
class Constitution:
    """Constitutional framework for AI governance."""

    metadata: Dict[str, Any] = field(default_factory=dict)
    supreme_principle: str = ""
    principles: Dict[str, Principle] = field(default_factory=dict)
    rules: List[Rule] = field(default_factory=list)
    axioms: List[str] = field(default_factory=list)  # Fundamental truths
    capabilities: Dict[str, Any] = field(default_factory=dict)  # Agent capabilities definitions
    action_policies: Dict[str, Any] = field(default_factory=dict)  # Policies for specific actions

    @classmethod
    def load_from_file(cls, path: Union[str, Path]) -> "Constitution":
        """Load constitution from YAML file."""
        path = Path(path)
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Constitution":
        """Create constitution from dictionary."""
        principles = {}
        if "principles" in data:
            for name, p_data in data["principles"].items():
                # Extract name from p_data if provided, otherwise use the key
                principle_name = p_data.pop("name", name) if isinstance(p_data, dict) else name
                principles[name] = Principle(name=principle_name, **p_data)

        rules = []
        if "rules" in data:
            for r_data in data["rules"]:
                rules.append(Rule(**r_data))

        return cls(
            metadata=data.get("metadata", {}),
            supreme_principle=data.get("supreme_principle", ""),
            principles=principles,
            rules=rules,
            axioms=data.get("axioms", []),
            capabilities=data.get("capabilities", {}),
            action_policies=data.get("action_policies", {}),
        )
