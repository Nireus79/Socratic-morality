"""Advanced explanation generation for ethical decisions."""
from typing import Any, Dict, List, Optional

class ExplanationGenerator:
    def __init__(self):
        pass
    def generate_explanation(self, decision_result: Dict[str, Any], precedent_cases: Optional[List[Dict[str, Any]]] = None) -> str:
        parts = []
        allowed = decision_result.get("allowed", False)
        confidence = decision_result.get("confidence", 0.5)
        headline = self._generate_headline(allowed, confidence)
        parts.append(headline)
        frameworks_summary = self._generate_frameworks_summary(decision_result.get("frameworks", {}))
        if frameworks_summary:
            parts.append(frameworks_summary)
        concerns = decision_result.get("concerns")
        if concerns:
            concerns_text = self._format_concerns(concerns)
            parts.append(concerns_text)
        if precedent_cases:
            precedent_text = self._generate_precedent_references(precedent_cases)
            if precedent_text:
                parts.append(precedent_text)
        stakeholders = decision_result.get("stakeholders", [])
        if stakeholders:
            stakeholder_text = self._generate_stakeholder_analysis(stakeholders)
            parts.append(stakeholder_text)
        confidence_text = self._generate_confidence_statement(confidence)
        parts.append(confidence_text)
        return "\n\n".join(parts)
    @staticmethod
    def _generate_headline(allowed: bool, confidence: float) -> str:
        if allowed:
            if confidence >= 0.9: return "DECISION: Approved with high confidence."
            elif confidence >= 0.7: return "DECISION: Approved with some concerns."
            else: return "DECISION: Approved but with low confidence."
        else:
            if confidence >= 0.9: return "DECISION: Denied with high confidence."
            elif confidence >= 0.7: return "DECISION: Denied; concerns outweigh benefits."
            else: return "DECISION: Denied but with low confidence."
    @staticmethod
    def _generate_frameworks_summary(frameworks: Dict[str, Any]) -> str:
        if not frameworks:
            return ""
        summaries = []
        for name, analysis in frameworks.items():
            if not analysis: continue
            allowed = analysis.get("allowed", True)
            principle = analysis.get("principle", "Unknown")
            status = "approves" if allowed else "rejects"
            summaries.append(f"* {name.replace('_', ' ').title()} ({principle}): {status}")
        return "Framework Analysis:\n" + "\n".join(summaries) if summaries else ""
    @staticmethod
    def _format_concerns(concerns_str: str) -> str:
        if not concerns_str: return ""
        concerns_list = [c for c in concerns_str.split("; ") if c]
        if not concerns_list: return ""
        formatted = "Ethical Concerns:\n"
        for concern in concerns_list:
            formatted += f"* {concern}\n"
        return formatted.rstrip()
    @staticmethod
    def _generate_precedent_references(cases: List[Dict[str, Any]]) -> str:
        if not cases: return ""
        relevant = cases[:3]
        if not relevant: return ""
        text = "Related Precedent Cases:\n"
        for i, case in enumerate(relevant, 1):
            action = case.get("action", "Unknown")[:50]
            decision = "allowed" if case.get("allowed") else "denied"
            similarity_pct = int(case.get("similarity_score", 1.0) * 100)
            text += f"* Case {i}: {action}... ({similarity_pct}% similar) - {decision}\n"
        return text.rstrip()
    @staticmethod
    def _generate_stakeholder_analysis(stakeholders: List[str]) -> str:
        if not stakeholders: return ""
        text = "Stakeholders Affected:\n"
        for stakeholder in stakeholders:
            if stakeholder.startswith("user:"): text += f"* User: {stakeholder[5:]} (direct impact)\n"
            elif stakeholder.startswith("org:"): text += f"* Organization: {stakeholder[4:]} (institutional)\n"
            else: text += f"* {stakeholder}\n"
        return text.rstrip()
    @staticmethod
    def _generate_confidence_statement(confidence: float) -> str:
        confidence_pct = int(confidence * 100)
        if confidence >= 0.9: return f"Confidence: {confidence_pct}% (Very High)"
        elif confidence >= 0.7: return f"Confidence: {confidence_pct}% (High)"
        elif confidence >= 0.5: return f"Confidence: {confidence_pct}% (Moderate)"
        else: return f"Confidence: {confidence_pct}% (Low)"
    def generate_counter_arguments(self, decision_result: Dict[str, Any]) -> Optional[str]:
        allowed = decision_result.get("allowed", False)
        confidence = decision_result.get("confidence", 0.5)
        if confidence >= 0.8 or confidence <= 0.2: return None
        frameworks = decision_result.get("frameworks", {})
        opposing_views = []
        for name, analysis in frameworks.items():
            if not analysis: continue
            framework_allowed = analysis.get("allowed", True)
            if framework_allowed != allowed:
                concern = analysis.get("concerns", "alternative perspective")
                opposing_views.append(f"* {name.replace('_', ' ').title()}: {concern}")
        if not opposing_views: return None
        text = "Alternative Perspectives:\n"
        text += "\n".join(opposing_views)
        return text
