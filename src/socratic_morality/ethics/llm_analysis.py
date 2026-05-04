"""LLM-based ethical analysis for multiple frameworks."""
import json
import re
from typing import Any, Dict, List, Optional

class LLMEthicalAnalyzer:
    def __init__(self, llm_client: Optional[Any] = None):
        self.llm_client = llm_client
    async def analyze_kantian(self, action: str, stakeholders: list, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.llm_client:
            return await self._llm_analyze_kantian(action, stakeholders, context)
        return self._fallback_analyze_kantian(action, stakeholders)
    async def analyze_utilitarian(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.llm_client:
            return await self._llm_analyze_utilitarian(action, context)
        return self._fallback_analyze_utilitarian(action)
    async def analyze_virtue_ethics(self, action: str, actor: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.llm_client:
            return await self._llm_analyze_virtue(action, actor, context)
        return self._fallback_analyze_virtue(action)
    async def analyze_rights_based(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.llm_client:
            return await self._llm_analyze_rights(action, context)
        return self._fallback_analyze_rights(action)
    async def _llm_analyze_kantian(self, action: str, stakeholders: list, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze: {action}"
        response = await self.llm_client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=500, messages=[{"role": "user", "content": prompt}])
        result = self._extract_json(response.content[0].text)
        return result or {"allowed": False, "confidence": 0.5, "principle": "Categorical Imperative", "concerns": "Unable", "reasoning": "Failed"}
    async def _llm_analyze_utilitarian(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze: {action}"
        response = await self.llm_client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=500, messages=[{"role": "user", "content": prompt}])
        result = self._extract_json(response.content[0].text)
        return result or {"allowed": True, "confidence": 0.8, "principle": "Harm Minimization", "concerns": None, "reasoning": "Unavailable"}
    async def _llm_analyze_virtue(self, action: str, actor: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze: {action}"
        response = await self.llm_client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=500, messages=[{"role": "user", "content": prompt}])
        result = self._extract_json(response.content[0].text)
        return result or {"allowed": True, "confidence": 0.7, "principle": "Moral Character", "concerns": None, "reasoning": "Unavailable"}
    async def _llm_analyze_rights(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze: {action}"
        response = await self.llm_client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=500, messages=[{"role": "user", "content": prompt}])
        result = self._extract_json(response.content[0].text)
        return result or {"allowed": True, "confidence": 0.8, "principle": "Human Agency", "concerns": None, "reasoning": "Unavailable"}
    @staticmethod
    def _fallback_analyze_kantian(action: str, stakeholders: list) -> Dict[str, Any]:
        has_v = any(kw in action.lower() for kw in ["manipulate", "deceive", "coerce"])
        return {"allowed": not has_v, "confidence": 0.75 if has_v else 0.6, "principle": "Categorical Imperative", "concerns": "Violates" if has_v else None, "reasoning": "Complete"}
    @staticmethod
    def _fallback_analyze_utilitarian(action: str) -> Dict[str, Any]:
        has_h = any(kw in action.lower() for kw in ["harm", "hurt", "damage"])
        return {"allowed": not has_h, "confidence": 0.7 if has_h else 0.8, "principle": "Harm Minimization", "concerns": "Harm" if has_h else None, "reasoning": "Complete"}
    @staticmethod
    def _fallback_analyze_virtue(action: str) -> Dict[str, Any]:
        has_v = any(kw in action.lower() for kw in ["deceive", "lie", "betray"])
        return {"allowed": not has_v, "confidence": 0.8 if has_v else 0.6, "principle": "Moral Character", "concerns": "Vice" if has_v else None, "reasoning": "Complete"}
    @staticmethod
    def _fallback_analyze_rights(action: str) -> Dict[str, Any]:
        has_v = any(kw in action.lower() for kw in ["coerce", "force", "override"])
        return {"allowed": not has_v, "confidence": 0.85 if has_v else 0.8, "principle": "Human Agency", "concerns": "Autonomy" if has_v else None, "reasoning": "Complete"}
    @staticmethod
    def _extract_json(text: str) -> Any:
        match = re.search(r"{.*}", text, re.DOTALL)
        if match:
            try: return json.loads(match.group(0))
            except: return None
        return None
