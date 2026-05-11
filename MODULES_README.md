# Three New Modules for Socratic-Morality

This document describes the three new modules added to the Socratic-Morality library.

## Module 1: Care Ethics Framework

**File**: `src/socratic_morality/ethics/care_ethics.py`

### Overview

The Care Ethics Framework provides context-aware moral analysis emphasizing relationships, vulnerability, and interdependence. Unlike other ethical frameworks that focus on rules or consequences, care ethics prioritizes:

- Relational morality (relationships matter morally)
- Vulnerability requires attention and protection
- Interdependence and context-specific judgment
- Care as a moral priority

### Key Classes

#### CareEthicsAnalyzer

Main class for care ethics analysis. Key methods:

```python
from socratic_morality.ethics import CareEthicsAnalyzer

analyzer = CareEthicsAnalyzer()

# Analyze an action through care ethics lens
result = await analyzer.analyze(
    action="provide support to vulnerable patient",
    context={
        "stakeholders": ["patient", "family"],
        "affected_parties": ["patient"]
    }
)
```

**Key Methods:**

- `analyze(action, context)` - Complete care ethics analysis
- `identify_relationships(stakeholders)` - Map relationships between parties
- `assess_vulnerability(stakeholder)` - Identify vulnerable stakeholders
- `evaluate_care_response(action, affected_parties)` - Check care adequacy
- `detect_care_violations(action)` - Find care ethics breaches

#### CareEthicsResult

Complete analysis result containing:

```python
class CareEthicsResult:
    action: str
    conclusion: CareConclusion  # CARING, INDIFFERENT, or HARMFUL
    vulnerability_concerns: List[str]
    relationship_analysis: List[Relationship]
    care_response_adequacy: float  # 0-1 score
    violations: List[CareViolation]
    recommendations: List[str]
    reasoning: str
    confidence: float  # 0-1
```

#### Supporting Data Classes

- `Relationship` - Describes relationships between stakeholders
- `VulnerabilityScore` - Vulnerability assessment with risk level
- `CareViolation` - Detected care ethics violations
- `CareAnalysis` - Care response adequacy analysis

### Example Usage

```python
async def analyze_medical_decision():
    analyzer = CareEthicsAnalyzer()

    result = await analyzer.analyze(
        action="increase pain medication for terminally ill patient",
        context={
            "stakeholders": ["patient", "family", "medical_team"],
            "affected_parties": ["patient", "family"]
        }
    )

    if result.conclusion == CareConclusion.CARING:
        print("Action demonstrates adequate care")
        print(f"Care score: {result.care_response_adequacy:.1%}")
    else:
        print("Action inadequate in care response")
        for rec in result.recommendations:
            print(f"  - {rec}")
```

---

## Module 2: Remediation Engine

**File**: `src/socratic_morality/governance/remediation_engine.py`

### Overview

The Remediation Engine addresses constraint violations and enables decision reversals. It proposes and executes remediations for actions that violate ethical constraints, with varying levels of automation and human oversight.

### Key Classes

#### RemediationEngine

Main class for remediation management:

```python
from socratic_morality.governance import RemediationEngine

engine = RemediationEngine()

# Suggest remediation for a violation
suggestion = await engine.suggest_remediation(
    decision=governor_decision,
    constraint_violated="consent required but not obtained"
)

# Auto-remediate if safe
result = await engine.auto_remediate(decision)
```

**Key Methods:**

- `suggest_remediation(decision, constraint)` - Propose fixes
- `auto_remediate(decision)` - Auto-execute safe remediations
- `rollback_decision(decision_id)` - Reverse a decision
- `implement_safeguards(action)` - Add protective measures
- `get_remediation_history()` - Track all remediations

#### RemediationType

Available remediation strategies:

```python
class RemediationType:
    MODIFY_ACTION = "modify_action"
    ADD_SAFEGUARDS = "add_safeguards"
    REJECT_AND_PROPOSE_ALTERNATIVE = "reject_and_propose_alternative"
    ESCALATE_WITH_CONSTRAINTS = "escalate_with_constraints"
    ROLLBACK = "rollback"
```

#### RemediationSuggestion

Proposed remediation containing:

```python
class RemediationSuggestion:
    remediation_type: RemediationType
    description: str
    required_changes: List[str]
    risk_level: RiskLevel  # LOW, MEDIUM, HIGH
    implementation_steps: List[str]
    estimated_impact: Dict[str, Any]
    reversibility: str  # "reversible" or "irreversible"
    estimated_effort: str  # "low", "medium", "high"
```

#### SafeguardPlan

Plan for protective measures:

```python
class SafeguardPlan:
    action_description: str
    safeguards: List[str]  # Protective measures
    monitoring_requirements: List[str]
    fallback_procedures: List[str]
    escalation_triggers: List[str]
    estimated_effectiveness: float  # 0-1
```

### Example Usage

```python
async def handle_constraint_violation():
    engine = RemediationEngine()

    # Decision that violates constraints
    decision = GovernorDecision(
        allowed=False,
        action="access user data without explicit consent",
        violations=[...]
    )

    # Get suggestion
    suggestion = await engine.suggest_remediation(
        decision,
        "consent principle violated"
    )

    if suggestion.remediation_type == RemediationType.MODIFY_ACTION:
        # Auto-remediate if safe
        result = await engine.auto_remediate(decision)
        if result.success:
            print(f"Auto-remediated: {result.action_taken}")

    elif suggestion.remediation_type == RemediationType.ADD_SAFEGUARDS:
        # Add protective measures
        plan = await engine.implement_safeguards(decision.action)
        print(f"Safeguards: {plan.safeguards}")

    # Get history
    history = engine.get_remediation_history()
```

---

## Module 3: Resource Monitor

**File**: `src/socratic_morality/security/resource_monitor.py`

### Overview

The Resource Monitor tracks and enforces resource limits (CPU, memory, file descriptors, processes) for monitored processes. It detects violations, enforces limits, and generates comprehensive usage reports.

### Key Classes

#### ResourceMonitor

Main class for resource monitoring:

```python
from socratic_morality.security import ResourceMonitor

monitor = ResourceMonitor()

# Start monitoring a process
session = monitor.start_monitoring(
    process_id=os.getpid(),
    limits={
        "cpu_percent": 80.0,
        "memory_mb": 2048.0,
        "file_descriptors": 1024,
        "processes": 128
    }
)

# Get current usage
usage = monitor.get_current_usage(session.session_id)

# Check for violations
violations = monitor.check_limits_violated(session.session_id)

# Stop and get report
report = monitor.stop_monitoring(session.session_id)
```

**Key Methods:**

- `start_monitoring(process_id, limits)` - Begin tracking
- `get_current_usage(session_id)` - Current resource snapshot
- `check_limits_violated(session_id)` - Detect breaches
- `enforce_limits(session_id, hard)` - Apply limits
- `get_usage_history(session_id)` - Historical data
- `stop_monitoring(session_id)` - End and report
- `list_active_sessions()` - List all active monitoring
- `get_session_status(session_id)` - Current session status

#### ResourceUsage

Current resource usage snapshot:

```python
class ResourceUsage:
    cpu_percent: float  # CPU percentage 0-100
    memory_mb: float  # Memory in MB
    file_descriptors: int  # Open file descriptors
    processes: int  # Running processes/threads
    timestamp: str  # ISO format timestamp
    within_limits: bool
    usage_details: Dict[str, Any]
```

#### LimitViolation

Resource limit violation record:

```python
class LimitViolation:
    resource: ResourceType  # cpu, memory, fd, process
    current_value: float
    limit: float
    severity: SeverityLevel  # WARNING or CRITICAL
    action_taken: str
    timestamp: str
    description: str
```

#### FinalReport

Final monitoring report:

```python
class FinalReport:
    session_id: str
    process_id: int
    duration_seconds: float
    peak_cpu_percent: float
    peak_memory_mb: float
    total_violations: int
    critical_violations: int
    average_usage: Dict[str, float]
    recommendations: List[str]
```

### Example Usage

```python
import asyncio
from socratic_morality.security import ResourceMonitor

async def monitor_task():
    monitor = ResourceMonitor()

    # Start monitoring
    session = monitor.start_monitoring(
        os.getpid(),
        limits={
            "cpu_percent": 80.0,
            "memory_mb": 1024.0,
        }
    )

    # Simulate work
    await asyncio.sleep(5)

    # Check for violations
    violations = monitor.check_limits_violated(session.session_id)
    for v in violations:
        print(f"WARNING: {v.resource.value} usage {v.current_value:.1f} "
              f"exceeds limit {v.limit:.1f}")

    # Enforce soft limits (warn only)
    result = monitor.enforce_limits(session.session_id, hard=False)

    # Get history
    history = monitor.get_usage_history(session.session_id)
    print(f"Collected {len(history)} usage snapshots")

    # Stop and get report
    report = monitor.stop_monitoring(session.session_id)
    print(f"Peak CPU: {report.peak_cpu_percent:.1f}%")
    print(f"Peak Memory: {report.peak_memory_mb:.1f}MB")
    print(f"Total violations: {report.total_violations}")
    for rec in report.recommendations:
        print(f"  - {rec}")

asyncio.run(monitor_task())
```

---

## Integration with Existing Modules

### Care Ethics with EthicalDeliberation

Care Ethics can complement the existing `EthicalDeliberationEngine`:

```python
from socratic_morality.ethics import (
    EthicalDeliberationEngine,
    CareEthicsAnalyzer
)

async def comprehensive_analysis(action, context):
    # Traditional ethical frameworks
    deliberation = EthicalDeliberationEngine()
    frameworks_result = await deliberation.analyze(
        action=action,
        purpose=context.get("purpose"),
        actor=context.get("actor"),
        context=context
    )

    # Care ethics perspective
    care = CareEthicsAnalyzer()
    care_result = await care.analyze(action, context)

    # Combine results
    return {
        "frameworks": frameworks_result,
        "care_ethics": care_result
    }
```

### Remediation with Governor

Remediation Engine works with the existing `Governor`:

```python
from socratic_morality.governor import Governor
from socratic_morality.governance import RemediationEngine

async def evaluate_with_remediation(governor, action, context):
    # Get Governor decision
    decision = await governor.evaluate(action, context=context)

    if not decision.allowed:
        # Suggest remediation
        remediation = RemediationEngine()
        suggestion = await remediation.suggest_remediation(
            decision,
            decision.violations[0].description if decision.violations else "unknown"
        )

        # Auto-remediate if possible
        if suggestion.remediation_type == RemediationType.MODIFY_ACTION:
            result = await remediation.auto_remediate(decision)
            return result

    return decision
```

### Resource Monitor with Sandbox

Resource Monitor can secure agent sandboxes:

```python
from socratic_morality.security import ResourceMonitor

async def monitor_agent_execution():
    monitor = ResourceMonitor()

    # Start monitoring agent process
    session = monitor.start_monitoring(
        agent_process_id,
        limits={
            "cpu_percent": 50.0,
            "memory_mb": 512.0,
        }
    )

    try:
        # Execute agent work
        result = await agent.run()
    finally:
        # Check if agent exceeded limits
        violations = monitor.check_limits_violated(session.session_id)
        if violations:
            print("Agent exceeded resource limits!")

        # Stop monitoring and report
        report = monitor.stop_monitoring(session.session_id)
```

---

## Testing

All three modules include comprehensive test suites:

- `tests/test_care_ethics.py` - 24 tests covering care ethics analysis
- `tests/test_remediation_engine.py` - 18 tests covering remediation workflows
- `tests/test_resource_monitor.py` - 29 tests covering resource monitoring

Run tests:

```bash
# All tests
pytest tests/test_care_ethics.py tests/test_remediation_engine.py tests/test_resource_monitor.py -v

# Individual module tests
pytest tests/test_care_ethics.py -v
pytest tests/test_remediation_engine.py -v
pytest tests/test_resource_monitor.py -v
```

---

## Architecture & Design Principles

### Care Ethics Framework
- **Contextual**: Decisions depend on specific relationships and context
- **Relational**: Prioritizes relationships as morally relevant
- **Adaptive**: Vulnerability assessment drives recommendations
- **Comprehensive**: Analyzes relationships, vulnerabilities, and violations

### Remediation Engine
- **Graduated Response**: From modification to escalation
- **Safe Automation**: Only auto-remediates LOW-risk changes
- **Reversible First**: Prefers reversible remediations
- **Traceable**: Complete history of all remediations

### Resource Monitor
- **Proactive**: Detects violations before they become critical
- **Flexible**: Soft (warning) or hard (enforcement) modes
- **Informative**: Historical data and recommendations
- **Session-Based**: Multiple independent monitoring sessions

---

## Dependencies

All modules use only standard library and existing Socratic-Morality dependencies:

- `dataclasses` - Type definitions
- `typing` - Type hints
- `enum` - Enumeration types
- `datetime` - Timestamp handling
- `psutil` - Resource monitoring (for ResourceMonitor)

No external dependencies beyond what Socratic-Morality already requires.

---

## Future Enhancements

### Care Ethics
- LLM-based relationship analysis
- Temporal tracking of relationships
- Integration with precedent system

### Remediation Engine
- Machine learning for remediation strategy selection
- Cost-benefit analysis of remediations
- Stakeholder preference learning

### Resource Monitor
- Predictive limit enforcement
- Resource-aware scheduling
- System-wide resource policies

---

## License

These modules are part of the Socratic-Morality project and follow the same license terms.
