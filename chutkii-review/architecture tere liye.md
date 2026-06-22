# System Architecture

## The Big Picture

The system is a **pipeline executor** for multi-step assessment workflows. Think of it as a job runner where:

- A "job" (called a *run*) consists of 6 sequential processing steps
- Each step produces structured JSON + a markdown report
- Between steps, human approvers must sign off before the next step starts
- Everything is coordinated by a state machine
- Final output is a directory of files (6 markdown reports + 6 JSON payloads + a scorecard + a run log)

There are 5 agents in the repo. One of them (`client-assessment-agent`, CA) is the main orchestrator. The other four are sub-agents that CA calls into to do specific processing work.

---

## The 5 Agents

```
agents/
├── client-assessment-agent/       ← Main orchestrator. Owns the run lifecycle.
├── capability_validation_agent/   ← Sub-agent. Called by CA for step 5.
├── ethana_proposal_agent/         ← Sub-agent. Called by CA for step 6.
├── regulatory-watch-agent/        ← Sub-agent. Called by CA for steps 1 & 2.
└── governance_review_agent/       ← Standalone agent. Not part of the CA pipeline.
    incident_intelligence_agent/   ← Standalone agent. Not part of the CA pipeline.
```

Each agent has an identical internal structure:

```
runtime/
├── orchestrator.py      ← Entry point. Runs the workflow.
├── state_manager.py     ← State machine + persistence (reads/writes JSON files)
├── skill_executor.py    ← Delegates to adapters or implements the logic directly
├── audit_logger.py      ← Appends events to a .jsonl file
├── schema_validator.py  ← Validates output dicts against JSON Schema files
├── output_builder.py    ← Assembles the final output package
├── config.yaml          ← Thresholds, directory paths, approval gate config
├── runs/                ← One JSON file per run (the run's state)
└── logs/                ← One JSONL file per run (the audit trail)
```

---

## How a Run Works (CA Pipeline)

```
Caller
  │
  ▼
Orchestrator.start_run(inputs)
  │
  ├─ Validates inputs
  ├─ Creates StateManager (writes initial state to disk)
  ├─ Creates AuditLogger (creates JSONL file)
  │
  ├─ Step 1: regulatory-mapping      ─────────── calls RWA's skill_executor.py
  │     └─ Gate 1: score check
  │
  ├─ [PAUSE] Approval Gate 1 ← caller must call submit_approval() separately
  │
  ├─ Step 2: control-mapping         ─────────── calls RWA's skill_executor.py
  │     └─ Gate 2: score + claims firewall check
  │
  ├─ [PAUSE] Approval Gate 2 (joint: two approvers required)
  │
  ├─ Step 3: solution-mapping        ─────────── local executor (skills/solution_mapping_executor.py)
  │     └─ Gate 3: score + claims firewall check
  │
  ├─ Step 4: gap-assessment          ─────────── local executor (skills/iso42001_executor.py)
  │     └─ Gate 4: score + claims firewall check
  │
  ├─ [PAUSE] Approval Gate 3
  │
  ├─ Step 5: capability-validation   ─────────── calls CVA's skill_executor.py
  │     └─ Gate 5: ECS score check
  │
  ├─ Step FM: feature-mapping        ─────────── local executor (skills/feature_mapping_executor.py)
  │     └─ Gate FM: table completeness + claims firewall
  │
  ├─ Step 6: proposal-review         ─────────── calls EPA's skill_executor.py
  │     └─ Gate 6: PCS/CTCS scores + terminal claims firewall
  │
  ├─ [PAUSE] Approval Gate 4 (joint: two approvers required)
  │
  └─ ASSEMBLING_PACKAGE → COMPLETE
        └─ OutputBuilder writes 14 files to packages/{run_id}/
```

The caller gets back a `traceability_id` (e.g. `TR-CA-2026-4216`) immediately. When a run pauses at an approval gate, the caller must call `orchestrator.submit_approval(traceability_id, ...)` to resume it.

---

## State Machine

The run's lifecycle is a finite state machine defined as a dict in `state_manager.py`. ~37 states, ~13 explicitly forbidden transitions. Every call to `transition_to()` validates against this dict before writing.

State is persisted to `runs/{traceability_id}_state.json` on every transition — that's a full JSON read + write to disk each time. A complete run does this ~37 times.

The state file contains the full run: inputs, all intermediate outputs from every step, approval records, and history of every transition.

```json
{
  "traceability_id": "TR-CA-2026-4216",
  "status": "APPROVAL_2_PENDING",
  "inputs": { ... },
  "intermediate_data": {
    "skill_1_json": { ... },
    "skill_1_md": "...",
    "skill_2_json": { ... },
    ...
  },
  "approvals": { ... },
  "history": [ ... ]
}
```

---

## How CA Calls Sub-Agents

CA does not call sub-agents over HTTP or any network. It imports their `skill_executor.py` files **directly by filesystem path** using `importlib.util.spec_from_file_location()`.

```python
# From skill_adapters.py — this is production code, not a test
abs_path = REPO_ROOT / "agents/capability_validation_agent/runtime/skill_executor.py"
spec = importlib.util.spec_from_file_location("ca_src_capability_validation", abs_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
executor = module.SkillExecutor(runs_dir, logs_dir)
```

This means all agents must live in the same directory tree at the same relative paths, always.

The imported modules are cached in a module-level dict:
```python
_SOURCE_MODULE_CACHE: dict = {}  # lives in skill_adapters.py, shared for the process lifetime
```

---

## The Adapter Layer (CA-specific)

CA sits between the orchestrator and the sub-agents via an adapter layer (`skill_adapters.py`). Each adapter wraps one step:

```
Orchestrator
    │
    ▼
SkillExecutor.execute_skill_N()
    │
    ▼
BaseSkillAdapter.execute()  ← template method
    ├─ map_inputs()     ← translate CA's data model → sub-agent's expected input
    ├─ invoke()         ← call the sub-agent's executor
    ├─ map_output()     ← translate sub-agent's output → CA's data model
    └─ _check_envelope()← assert required keys present
```

**The lambda override pattern (used heavily in tests):**
```python
# Tests bypass the entire adapter by replacing the bound method:
orchestrator.executor.execute_skill_5 = lambda sm, inp, lg: FIXTURE_DICT
```
This replaces `execute_skill_5` on the instance, skipping `map_inputs`, `invoke`, `map_output`, and `_check_envelope` entirely.

---

## Knowledge Sources

Three types of runtime knowledge, all stored as files:

| File | Format | Used by | Parsed how |
|---|---|---|---|
| `knowledge/ethana/canonical-product-model.md` | Markdown table | CVA, SolutionMapping | Regex on every call |
| `knowledge/ethana/control-capability-map.md` | Markdown table | RWA, CA | Regex, cached per process |
| `workflows/schemas/*.json` | JSON Schema | All agents | `jsonschema` library |

---

## Cross-Agent Coupling Map

```
CA orchestrator
    ├── imports RWA skill_executor.py    (via file path)
    ├── imports CVA skill_executor.py    (via file path)
    └── imports EPA skill_executor.py    (via file path)
            └── EPA executor mutates CA's StateManager directly
                (CA passes its state_mgr object into EPA's function)

SolutionMappingExecutor (CA-local, step 3)
    └── imports claims_linter.py         (from evaluations/scripts/ — the test folder)

RWA skill_executor (sub-agent)
    └── imports claims_linter.py         (from evaluations/scripts/ — the test folder)
```

---

## Audit Logging

Every event in a run is logged to `logs/{traceability_id}_audit.jsonl`. Each line is a JSON object:

```json
{"traceability_id": "TR-CA-2026-4216", "timestamp": "2026-06-22T10:00:00Z",
 "step": "GATE_3_PASSED", "status": "SUCCESS", "message": "Gate 3 passed.", "details": {}}
```

The logger also `print()`s every event to stdout. Errors in writing the log are caught and printed — they do not fail the run.

---

## Test Setup

Tests live in `evaluations/scripts/`, not alongside the code they test.

```
evaluations/scripts/
├── conftest.py                          ← 6-line sys.path setup, nothing else
├── test_client_assessment_runtime.py    ← 88 tests for CA (205 use lambda overrides)
├── test_client_assessment_adapters.py   ← adapter unit tests
├── test_client_assessment_skill3.py     ← Skill 3 unit tests
├── test_capability_validation_runtime.py
├── test_regulatory_watch_runtime.py
├── test_proposal_review_runtime.py
└── ...
```

Total: **352 tests, all passing** (per-module). Of those, **205 use lambda overrides** that bypass real adapter execution. The system has never been exercised end-to-end with all real adapters — the first integration test covering the full 6-step chain is the next milestone.

---

## What Does NOT Exist Yet

- No HTTP API / web server
- No database (state is JSON files on disk)
- No authentication or authorization
- No multi-tenant isolation
- No background job processing (all execution is synchronous, blocking)
- No Dockerfile, no deployment config
- No requirements.txt or pyproject.toml
- No CI/CD configuration
- No metrics, no tracing, no log aggregation
- No approval gate timeout enforcement (config has `timeout_business_days` but nothing fires it)
- No run cleanup / TTL
