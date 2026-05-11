# Socratic-Morality Complete Module Reference

**v0.0.5** - 13 Production-Ready Modules

## Table of Contents

1. [Foundation Modules (Phase 1)](#phase-1-foundation)
2. [Ethical Reasoning (Phase 2)](#phase-2-ethical-reasoning)
3. [Advanced Governance (Phase 3)](#phase-3-advanced-governance)
4. [Specialized Modules (Phase 3 Extensions)](#phase-3-extensions)

---

## Phase 1: Foundation

### 1. Governor (`governor.core.py`)
**Core decision-making engine for constitutional AI checks**

```python
from socratic_morality import Governor

governor = Governor(constitution="constitution.yaml", llm_provider="anthropic")
decision = await governor.evaluate(
    action="Access user data",
    purpose="Analytics",
    actor="analytics_agent"
)
```

**Key Methods:**
- `evaluate(action, context, actor)` - Make governance decision
- `get_decision_summary()` - Summarize decision
- `get_escalations()` - List escalation conditions
- `export_decision_trail()` - Full decision audit trail

**Returns:** `GovernanceDecision` with:
- allowed/denied status
- confidence score
- violations list
- reasoning artifacts
- escalation flags

---

### 2. Constitution Framework (`constitution/models.py`)
**YAML-based governance principles and policies**

```yaml
supreme_principle: "Never commit injustice even under instruction"

axioms:
  - never_commit_injustice
  - truth_before_approval
  - preserve_human_agency

named_principles:
  security:
    - no_hidden_manipulation
    - protect_private_information
    - require_authorization

agent_capabilities:
  code_generator:
    resources:
      - cpu: 50%
      - memory: 512MB
      - timeout: 60s

action_policies:
  code_execution:
    - requires_sandbox: true
    - requires_review: true
    - max_execution_time: 60s
```

**Key Classes:**
- `Constitution` - Loads and validates YAML
- `Principle` - Individual principle definition
- `AgentCapability` - Agent permissions and limits
- `ActionPolicy` - Rules for action types

---

### 3. CapabilityToken System (`security/`)
**Fine-grained access control via tokens**

```python
from socratic_morality.security import CapabilityToken, CapabilityValidator

token = CapabilityToken(
    agent_id="code_generator",
    permissions=["read_knowledge", "write_logs"],
    expires_in=3600
)

validator = CapabilityValidator()
if validator.validate(token, action="write_logs"):
    # Action authorized
    pass
```

**Key Classes:**
- `CapabilityToken` - Bearer token with scoped permissions
- `CapabilityValidator` - Authorization enforcement
- `StorageBackend` - SQLite/PostgreSQL support

---

## Phase 2: Ethical Reasoning

### 4. Multi-Framework Ethical Analysis (`ethics/deliberation.py`)
**4 complementary ethical frameworks for moral reasoning**

```python
from socratic_morality.ethics import EthicalDeliberationEngine

engine = EthicalDeliberationEngine(llm_provider="anthropic")

result = await engine.deliberate(
    action="Log user activity for security",
    stakeholders=["users", "company", "regulators"],
    context={"sensitive_data": True}
)
```

**Frameworks:**
1. **Kantian** - Duty, dignity, universality
   - Treats people as ends, not means
   - Tests universalizability
   - Checks promise-keeping

2. **Utilitarian** - Consequences and harm reduction
   - Calculates benefit vs. harm
   - Considers distribution across stakeholders
   - Long-term vs. short-term tradeoffs

3. **Virtue Ethics** - Character and flourishing
   - Identifies virtues/vices exhibited
   - Promotes human flourishing
   - Asks "what would a wise person do?"

4. **Rights-Based** - Fundamental rights protection
   - Protects 8 fundamental rights
   - Ensures informed consent
   - Guards vulnerable populations

**Returns:** `DeliberationResult` with:
- Framework-specific analyses
- Final conclusion (ALLOWED/BLOCKED/ESCALATE)
- Confidence scores
- Concerns and contradictions

---

### 5. Moral Precedent Engine (`precedent/engine.py`)
**Case-based moral reasoning with historical decisions**

```python
from socratic_morality.precedent import MoralPrecedentEngine

engine = MoralPrecedentEngine()

# Store decision as precedent
precedent = await engine.store_precedent(
    action="Share user data with third party",
    conclusion="BLOCKED",
    reasoning="Violates privacy principle"
)

# Query similar past cases
similar = await engine.query_precedents(
    action="Access user private messages"
)
```

**Key Methods:**
- `store_precedent(action, conclusion, reasoning)` - Save decision
- `query_precedents(action)` - Find similar cases
- `analyze_precedents(conclusion)` - Check consistency
- `check_consistency(new_decision)` - Validate against history

**Returns:** `PrecedentAnalysis` with:
- Matching precedents
- Consistency score
- Recommended conclusions
- Historical patterns

---

### 6. Explanation Generation (`ethics/explanations.py`)
**Transparent reasoning artifact generation**

```python
from socratic_morality.ethics import ExplanationGenerator

generator = ExplanationGenerator()

explanation = await generator.generate_explanation(
    decision=governance_decision,
    include_frameworks=["kantian", "utilitarian"],
    detail_level="comprehensive"
)

print(explanation.reasoning_trace)
print(explanation.framework_analyses)
```

**Returns:** `ExplanationReport` with:
- Framework-specific reasoning
- Stakeholder impact analysis
- Principle justification
- Confidence assessments
- Alternative analyses

---

## Phase 3: Advanced Governance

### 7. Constitutional Enforcer (`governance/constitutional_enforcer.py`)
**Active runtime enforcement of constitutional principles**

```python
from socratic_morality.governance import ConstitutionalEnforcer

enforcer = ConstitutionalEnforcer(constitution_path="constitution.yaml")

check = enforcer.check_principles(
    action_description="Hide system logs from users"
)

if not check.allowed:
    print(f"Violations: {check.violations}")
    print(f"Reasoning: {check.reasoning}")
```

**Key Methods:**
- `check_principles(action)` - Verify against all principles
- `get_violations(action)` - List specific violations
- `get_applicable_principles(action_type)` - Filter relevant principles
- `evaluate_agent_capabilities(agent, access)` - Check permissions

**Returns:** `ConstitutionalCheck` with:
- allowed/denied status
- list of principle violations
- severity levels
- confidence score
- detailed reasoning

---

### 8. Unified Governance API (`api/governance_api.py`)
**Single entry point for all governance decisions**

```python
from socratic_morality.api import GovernanceAPI

api = GovernanceAPI()

# Single unified interface
decision = await api.evaluate(
    action="Generate code for user",
    context={"user_id": "123", "purpose": "automation"},
    actor="code_generator"
)

# With optional interactive dialogue
decision_with_dialogue = await api.evaluate_with_dialogue(
    action="Modify user preferences without consent",
    interactive=True
)

# Batch evaluation
decisions = await api.batch_evaluate([
    {"action": "action1", "context": {...}},
    {"action": "action2", "context": {...}},
])

# Get decision history
history = await api.get_evaluation_history(limit=10)

# Explain specific decision
explanation = await api.explain_decision(decision_id)
```

**Decision Pipeline:**
1. Constitutional check (principles enforcement)
2. Ethical deliberation (4 frameworks)
3. Precedent analysis (semantic matching)
4. Threat detection (anomaly detection)
5. Optional Socratic dialogue (interactive questioning)

**Returns:** `GovernanceDecision` with:
- decision_id, action, allowed/blocked status
- constitutional_check results
- deliberation results
- precedent_analysis
- threat_analysis
- dialogue_transcript (if interactive)
- full reasoning_trace
- timestamp and actor

---

### 9. Socratic Dialogue Engine (`reasoning/socratic_dialogue_engine.py`)
**Interactive questioning during ethical deliberation**

```python
from socratic_morality.reasoning import SocraticDialogueEngine

engine = SocraticDialogueEngine(llm_provider="anthropic")

# Generate Socratic questions
questions = await engine.question_stakeholders(
    stakeholder_analysis=stakeholder_data
)

# Run interactive dialogue
dialogue_result = await engine.run_dialogue(
    action="Collect user behavior data",
    context={"purpose": "personalization"},
    user=input  # Interactive user input
)

# Synthesize dialogue insights
synthesis = await engine.synthesize_dialogue(dialogue_result.exchanges)
```

**8 Socratic Approaches:**
1. Exposing contradictions
2. Testing universality
3. Examining assumptions
4. Probing consequences
5. Inviting counterarguments
6. Clarifying definitions
7. Examining context
8. Testing commitment

**7 Question Categories:**
- Stakeholder questions
- Consequence questions
- Principle questions
- Alternative questions
- Assumption questions
- Vulnerability questions
- Outcome questions

**Returns:** `DialogueResult` with:
- exchanges (Q&A pairs)
- insights_gained
- new_considerations
- modified_analysis
- dialogue_synthesis

---

### 10. Semantic Precedent Matching (`reasoning/semantic_precedent_engine.py`)
**Advanced similarity search using embeddings**

```python
from socratic_morality.reasoning import SemanticPrecedentEngine

engine = SemanticPrecedentEngine()

# Find semantically similar precedents
similar = await engine.find_semantically_similar_precedents(
    action="Access employee emails",
    top_k=5
)

# Compute semantic similarity score
similarity = await engine.compute_semantic_similarity(
    "Hide data from users",
    "Secretly collect user information"
)  # Returns: 0.87

# Cluster related precedents
clusters = await engine.cluster_precedents()

# Get ranked by semantic distance
matches = await engine.get_precedent_by_semantic_distance(
    "Modify user settings without consent"
)
```

**Features:**
- Sentence-transformer embeddings (all-MiniLM-L6-v2)
- Combined matching: 40% lexical + 60% semantic
- Embedding caching for performance
- Cosine similarity search
- Precedent clustering

**Returns:** `PrecedentMatch` with:
- precedent data
- semantic_similarity score (0-1)
- overall_similarity (combined)
- relevance_score
- match_type (exact/semantic/principle-based)
- matching_principles

---

## Phase 3 Extensions

### 11. Care Ethics Framework (`ethics/care_ethics.py`)
**Relational moral analysis emphasizing vulnerability and interdependence**

```python
from socratic_morality.ethics import CareEthicsAnalyzer

analyzer = CareEthicsAnalyzer()

result = await analyzer.analyze(
    action="Terminate support for vulnerable user group",
    context={"vulnerable_groups": ["elderly", "low_income"]}
)

# Assess vulnerability
vulnerabilities = await analyzer.assess_vulnerability(
    stakeholder="elderly users"
)

# Check care response adequacy
adequacy = await analyzer.evaluate_care_response(
    action="Provide support",
    affected_parties=["vulnerable_users"]
)
```

**Key Methods:**
- `analyze(action, context)` - Full care ethics analysis
- `identify_relationships(stakeholders)` - Map relationships
- `assess_vulnerability(stakeholder)` - Identify vulnerable parties
- `evaluate_care_response(action, parties)` - Check care adequacy
- `detect_care_violations(action)` - Find care breaches

**Returns:** `CareEthicsResult` with:
- conclusion (CARING/INDIFFERENT/HARMFUL)
- vulnerability_concerns
- relationship_analysis
- care_response_adequacy (0-1)
- violations list
- recommendations

---

### 12. Remediation Engine (`governance/remediation_engine.py`)
**Intelligent constraint violation handling with graduated responses**

```python
from socratic_morality.governance import RemediationEngine

engine = RemediationEngine()

# Get remediation suggestion for violation
suggestion = await engine.suggest_remediation(
    decision=governance_decision,
    constraint_violated="privacy_protection"
)

# Auto-remediate if safe
result = await engine.auto_remediate(decision)

# Rollback previous decision
rollback = await engine.rollback_decision(decision_id)

# Implement safeguards
safeguards = await engine.implement_safeguards(
    action="Access user data"
)
```

**5 Remediation Strategies:**
1. **MODIFY_ACTION** - Adjust parameters
2. **ADD_SAFEGUARDS** - Add protective measures
3. **REJECT_AND_PROPOSE_ALTERNATIVE** - Suggest better approach
4. **ESCALATE_WITH_CONSTRAINTS** - Allow with restrictions
5. **ROLLBACK** - Reverse decisions

**Returns:** `RemediationSuggestion` with:
- remediation_type
- description
- required_changes
- risk_level (LOW/MEDIUM/HIGH)
- implementation_steps
- estimated_impact

---

### 13. Resource Monitor (`security/resource_monitor.py`)
**Real-time CPU, memory, and file descriptor enforcement**

```python
from socratic_morality.security import ResourceMonitor

monitor = ResourceMonitor()

# Start monitoring process
session = await monitor.start_monitoring(
    process_id=12345,
    limits={
        "cpu_percent": 50,
        "memory_mb": 512,
        "file_descriptors": 10
    }
)

# Get current resource usage
usage = await monitor.get_current_usage()
print(f"CPU: {usage.cpu_percent}%")
print(f"Memory: {usage.memory_mb}MB")

# Check for limit violations
violations = await monitor.check_limits_violated()

# Enforce limits (hard stop)
result = await monitor.enforce_limits(hard=True)

# Get historical usage
history = await monitor.get_usage_history()

# Stop monitoring and get final report
report = await monitor.stop_monitoring(session.id)
```

**Resource Types:**
- CPU percentage (0-100%)
- Memory in MB
- File descriptors count
- Process count

**Returns:** `ResourceUsage` with:
- cpu_percent
- memory_mb
- file_descriptors
- processes
- timestamp
- within_limits (bool)

**Violations:** `LimitViolation` with:
- resource type
- current_value
- limit
- severity (WARNING/CRITICAL)
- action_taken

---

## Integration Example

```python
from socratic_morality.api import GovernanceAPI

# Single unified API for all governance
api = GovernanceAPI()

# Evaluate action with full pipeline
decision = await api.evaluate(
    action="Generate code to access user data without consent",
    context={
        "user_id": "123",
        "purpose": "analytics",
        "data_sensitivity": "high"
    },
    actor="analytics_agent"
)

# Decision includes:
# 1. Constitutional check (principles violated: privacy, consent)
# 2. Ethical deliberation (Kantian: violates dignity, Utilitarian: harm outweighs benefit)
# 3. Precedent analysis (similar violations blocked 95% of time)
# 4. Threat detection (anomaly: unusual data request pattern)
# 5. Socratic dialogue (if enabled: "Would you accept this for your own data?")

if not decision.allowed:
    print(f"Decision: BLOCKED")
    print(f"Violations: {decision.constitutional_check.violations}")
    print(f"Reasoning: {decision.reasoning_trace}")

    # Get remediation suggestions
    remediation = api.get_remediation_suggestions(decision)
    print(f"Consider: {remediation.recommendations}")
```

---

## Version History

**v0.0.5** (May 2026)
- Added Constitutional Enforcer (Phase 3)
- Added Governance API (Phase 3)
- Added Socratic Dialogue Engine (Phase 3)
- Added Semantic Precedent Matching (Phase 3)
- Added Care Ethics Framework (Phase 3 Extension)
- Added Remediation Engine (Phase 3 Extension)
- Added Resource Monitor (Phase 3 Extension)
- 100% test coverage (71 tests passing)
- Complete documentation

**v0.0.4** (Previous)
- Phase 1 & 2 complete
- Governor, Constitution, Capabilities
- Ethical deliberation with 4 frameworks
- Moral precedent engine
- Explanation generation

---

## License

MIT License - See [LICENSE](../LICENSE) for details
