# Backlog Item: PR-008

## Title
Regulatory Watch Agent — L4 Test Coverage and Certification

## Status
**Scheduled** — Next in sequence. No prerequisites.

## Basis
Source code read 2026-06-21. Authoritative baselines:
- `reviews/governance-os-program-review-2026-06-21.md`
- `reviews/governance-os-master-status.md`

Primary sources consulted:
- `agents/regulatory-watch-agent/runtime/orchestrator.py` (969 lines)
- `agents/regulatory-watch-agent/runtime/skill_executor.py` (607 lines)
- `agents/regulatory-watch-agent/runtime/state_manager.py`
- `agents/regulatory-watch-agent/state-machine.md`
- `agents/regulatory-watch-agent/AGENT.md`
- `agents/regulatory-watch-agent/evaluation.md`
- `agents/regulatory-watch-agent/workflow.yaml`
- `evaluations/scripts/test_firewall_hardening.py`

---

## SECTION 1 — Problem Statement

### Why PR-008 Exists

The Regulatory Watch Agent has 969 lines of orchestrator code, a fully implemented 24-state machine, and two skills. It has two existing tests — both in `test_firewall_hardening.py`, both testing halt paths via direct method calls or manual state injection. Zero dedicated tests exercise the full Mode A execution cycle. Zero tests exercise Mode B (the Watch mode). The agent certifier reports L4 because `agents/regulatory-watch-agent/` is non-empty, not because any behavioral evidence exists.

The program review baseline (`reviews/governance-os-master-status.md`) correctly classifies RWA as "Partial." The certifier disagrees. The certifier is wrong.

### Current Risks

**Risk 1 — Silent regression.** Any change to `orchestrator.py` or `skill_executor.py` would not be caught before execution. The 969-line orchestrator has never been run start-to-finish in a test context.

**Risk 2 — False certification.** The certifier checks directory presence. A non-empty directory grants L4 regardless of whether any code executes correctly or any test passes.

**Risk 3 — Unexercised state machine.** 22 of 24 states have never been reached by any test. Both approval gate flows, all score-band transitions, and the re-gate path under "Approve with modifications" are entirely untested.

**Risk 4 — Mode B is the differentiating RWA feature and is completely untested.** Mode B (regulatory change detection and re-assessment queuing) exists only in RWA. Its 969-line implementation has never been invoked under test conditions. Its correctness is unknown.

### State Coverage Deficit

| Dimension | Current |
|---|---|
| Mode A happy-path tests | 0 |
| Mode B tests | 0 |
| States reached by tests | 2 of 24 |
| Approval gate tests | 0 |
| Gate 1/2/3a/3b/4 full-path tests (via `start_run`) | 0 |
| L4A fixture blocker (minimal-risk-internal-tool.md) | Missing |

### Success Definition

PR-008 is complete when:
1. `evaluations/scripts/test_regulatory_watch_runtime.py` exists with ≥ 34 passing tests
2. `evaluations/test-cases/regulatory-subjects/minimal-risk-internal-tool.md` exists (L4A blocker in `AGENT.md`)
3. All 3 Mode A fixture profiles (EU BFSI, India DPDP, UK Insurance) reach `COMPLETE` in tests
4. All 13 major halt states are reached and asserted in at least one test each
5. Mode B correctly identifies affected runs, enforces the 3-run concurrency cap, and returns correct `STARTED`/`QUEUED` statuses
6. No existing tests broken — `test_firewall_hardening.py` (9 tests) preserved intact

---

## SECTION 2 — Existing RWA Architecture

### Runtime Architecture

**`orchestrator.py` (969 lines)** — coordination layer.

Public API:

| Method | Role |
|---|---|
| `start_run(trigger_type, inputs)` | Validates inputs, maps to log fixture, initialises state, calls `_run_skill_1`. Returns when state reaches `APPROVAL_1_PENDING` or a halt state. |
| `submit_approval_1(traceability_id, action, actor, notes)` | Loads state from disk, validates action, transitions. On Approve: calls `_run_skill_2`. |
| `submit_approval_2(traceability_id, action, actor, notes)` | Handles 5 actions; "Approve with modifications" triggers re-gate on merged GCM markdown + notes. |
| `release_partial_package(traceability_id)` | Assembles S1 partial package if `APPROVAL_1_APPROVED` has been set; raises `ValueError` otherwise. |
| `execute_mode_b(regulatory_change_alert)` | Mode B entry point — see below. |

Internal methods of note:

- `_validate_inputs(trigger_type, inputs)` — enforces: `trigger_type` ∈ `{new_use_case_registration, jurisdictional_expansion, regulatory_change_alert}`; all required fields present; `subject_description` ≥ 50 chars; `subject_type` ∈ enum; `target_maturity_level` ∈ enum; `jurisdictions` non-empty and each element ∈ `{EU, UK, India}`
- `_map_to_fixture(inputs)` — routing: India in jurisdictions → `india-dpdp`; UK + "insurance" in desc/industry → `uk-insurance`; else → `eu-ai-act`. **Critical:** this result is logged only. `SkillExecutor` does not read it. Skill execution is entirely keyword-based from inputs.
- `_evaluate_gate_1(state_mgr, logger, s1_json, inputs)` — Claims Firewall runs **first** on S1 markdown; then schema validation with one retry. Simulation hooks: `simulate_gate_1_fail`, `simulate_gate_1_fail_double`.
- `_evaluate_gate_2(state_mgr, logger, s1_json, inputs)` — score from `inputs.get("mock_s1_score", s1_json.get("score", 91))`; thresholds: `< 55` → `HALTED_GATE_2_INSUFFICIENT`, `55–69` → `HALTED_GATE_2_PRELIMINARY`, `≥ 70` → `GATE_2_PASSED`.
- `_evaluate_gate_3(state_mgr, logger, s2_json, md_content, inputs)` — Gate 3a (schema, with retry) and Gate 3b (Claims Firewall) both evaluated; firewall breach takes precedence if both fail. Simulation hooks: `simulate_gate_3a_fail`, `simulate_gate_3a_fail_double`, `simulate_firewall_breach`.
- `_evaluate_gate_4(state_mgr, logger, s2_json, inputs)` — score from `inputs.get("mock_s2_score", s2_json.get("score", 88))`; thresholds: `< 70` → `HALTED_GATE_4_INSUFFICIENT`, `70–84` → `HALTED_GATE_4_BELOW_THRESHOLD`, `≥ 85` → `GATE_4_PASSED`.

**`state_manager.py`** — enforces `VALID_TRANSITIONS`; persists all state as JSON to `runs_dir/TR-RW-*_state.json`. State structure: `{status, traceability_id, inputs, intermediate_data, history, approvals}`. Every `submit_approval_*` call creates a fresh `StateManager` and loads from disk — state persistence is architectural, not optional. No separate process-restart test is needed; this is guaranteed by design.

**`skill_executor.py` (607 lines)** — deterministic, keyword-based, no LLM calls in test context.
- `execute_regulatory_mapping(inputs, logger)` — classifies AI technology from description keywords; scans EU/UK/India regulatory paths based on jurisdiction list and BFSI keywords in description/industry; score = `80 + modifiers` (capped 98). Modifiers: +5 if `len(desc) > 100`, +5 if industry set, +5 if `ai_technology` set, +3 if multiple data_types.
- `execute_governance_control_mapping(s1_json, logger)` — builds full control taxonomy from `control_requirements`; score = `86 + 4 if ≥ 4 requirements` (capped 98).
- `generate_traceability_id()` — globs `runs_dir/TR-RW-{year}-*.json` and auto-increments. Override via `self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id` in tests.

**Schema location** — `agents/regulatory-watch-agent/runtime/contracts/` (NOT `workflows/schemas/`). Files: `regulatory_mapping_output.json`, `governance_control_output.json`. This is RWA-specific; all other agents use `workflows/schemas/`.

### Simulation Hooks (all read from `inputs` dict passed at `start_run`)

| Key | Type | Effect |
|---|---|---|
| `simulate_gate_1_fail` | bool | Corrupts Gate 1 JSON payload on first attempt |
| `simulate_gate_1_fail_double` | bool | Also corrupts Gate 1 retry → `HALTED_GATE_1_SCHEMA` |
| `mock_s1_score` | int | Overrides Gate 2 score |
| `simulate_firewall_breach` | bool | Appends "Visual Agent Builder is currently in build." to S2 markdown |
| `simulate_gate_3a_fail` | bool | Corrupts Gate 3a JSON payload on first attempt |
| `simulate_gate_3a_fail_double` | bool | Also corrupts Gate 3a retry → `HALTED_GATE_3A_SCHEMA` |
| `mock_s2_score` | int | Overrides Gate 4 score |

Defaults when keys absent: `mock_s1_score` falls back to `s1_json.score` then 91 (always passes Gate 2). `mock_s2_score` falls back to `s2_json.score` then 88 (always passes Gate 4). Happy-path tests must NOT include simulation keys.

### Approval Architecture

**AG-1 (General Counsel):** Single approver. Valid actions: `"Approve"`, `"Reject"`, `"Timeout"`. Approve transitions `APPROVAL_1_PENDING` → `APPROVAL_1_APPROVED` → `SKILL_2_RUNNING`. Notes are attached to run log and included in inter-skill payload as `approval_1_notes`.

**AG-2 (DPO + InfoSec Lead joint):** Five actions:
- `"Approve"` → `APPROVAL_2_APPROVED` → `COMPLETE`
- `"Reject"` → `HALTED_APPROVAL_2_REJECTED`
- `"Partial"` → `HALTED_APPROVAL_2_PARTIAL` (one approves, one rejects)
- `"Timeout"` → `APPROVAL_TIMED_OUT` (recoverable — NOT terminal)
- `"Approve with modifications"` → re-gate: merges original GCM markdown with notes, runs Claims Firewall (Gate 3b on merged content), runs Gate 3a schema check on existing `s2_json`, runs Gate 4 score check on existing score; if all pass → `COMPLETE`; if firewall fails → `HALTED_FIREWALL_BREACH`

### Claims Firewall Integration

Three enforcement points in the RWA runtime:

1. **Gate 1 path** (`_evaluate_gate_1`): `claims_linter.py` runs on S1 markdown BEFORE schema validation. If breach: `HALTED_FIREWALL_BREACH`; schema not evaluated. Tested by `TestSkill1FirewallBypass` in `test_firewall_hardening.py` via direct `_evaluate_gate_1` call.

2. **Gate 3b** (`_evaluate_gate_3`): runs on S2 markdown. Evaluated concurrently with Gate 3a schema check. If both fail, firewall breach takes precedence. `simulate_firewall_breach=True` appends "Visual Agent Builder is currently in build." to S2 markdown before linting.

3. **AG-2 modifications re-gate**: notes content merged with original GCM markdown; combined text sent to `claims_linter.py`. Tested by `TestApprovalModificationBypass` in `test_firewall_hardening.py`.

### Mode A Flow

```
start_run → INTAKE_VALIDATING → INTAKE_COMPLETE → SKILL_1_RUNNING → SKILL_1_COMPLETE
  → (Gate 1: Firewall, then Schema) → GATE_1_PASSED
  → (Gate 2: Score) → GATE_2_PASSED → APPROVAL_1_PENDING
  [human: submit_approval_1("Approve")]
  → APPROVAL_1_APPROVED → SKILL_2_RUNNING → SKILL_2_COMPLETE
  → (Gate 3a: Schema concurrent with Gate 3b: Firewall) → GATE_3_PASSED
  → (Gate 4: Score) → GATE_4_PASSED → APPROVAL_2_PENDING
  [human: submit_approval_2("Approve")]
  → APPROVAL_2_APPROVED → COMPLETE
```

### Mode B Flow

```
execute_mode_b(alert) →
  glob TR-RW-*_state.json in runs_dir →
  filter: status == COMPLETE →
  filter: alert.jurisdiction ∈ state.inputs.jurisdictions →
  filter: alert.regulation_name substring-matches any applicable_regulation.regulation_name →
  sort: severity_weight DESC, then is_annex_iii DESC, then init_timestamp ASC →
  for idx, item in enumerate(affected):
    idx < 3: start_run("regulatory_change_alert", re_inputs) → {"status": "STARTED", ...}
    idx ≥ 3: {"status": "QUEUED", "traceability_id": None, ...}
  return list of {status, traceability_id, prior_assessment_id}
```

`execute_mode_b` appends a `--- REGULATORY CHANGE RE-ASSESSMENT ---` marker and the `change_summary` to `subject_description` before calling `start_run`. Sets `existing_assessment_id` to the prior run's traceability ID.

---

## SECTION 3 — Test Architecture Design

### Test Categories and Coverage Map

| # | Category | Tests | States Exercised |
|---|---|---|---|
| 1 | Intake Validation | 5 | `HALTED_INTAKE_INVALID`, `HALTED_INTAKE_UNSUPPORTED_JURISDICTION` |
| 2 | Mode A Happy Paths | 3 | `COMPLETE` (all intermediate states en route) |
| 3 | Package File Verification | 1 | `COMPLETE` (artifact assertions) |
| 4 | Gate 1 Schema Failures | 2 | `HALTED_GATE_1_SCHEMA` + retry-success path |
| 5 | Gate 2 Score Failures | 2 | `HALTED_GATE_2_PRELIMINARY`, `HALTED_GATE_2_INSUFFICIENT` |
| 6 | Approval Gate 1 Failures | 2 | `HALTED_APPROVAL_1_REJECTED`, `APPROVAL_TIMED_OUT` |
| 7 | Gate 3b Claims Firewall — S2 | 1 | `HALTED_FIREWALL_BREACH` (via `start_run` flow) |
| 8 | Gate 3a Schema Failures | 2 | `HALTED_GATE_3A_SCHEMA` + retry-success path |
| 9 | Gate 4 Score Failures | 2 | `HALTED_GATE_4_BELOW_THRESHOLD`, `HALTED_GATE_4_INSUFFICIENT` |
| 10 | Approval Gate 2 Failures | 3 | `HALTED_APPROVAL_2_REJECTED`, `HALTED_APPROVAL_2_PARTIAL`, `APPROVAL_TIMED_OUT` |
| 11 | AG-2 Modifications — Clean | 1 | `COMPLETE` (via re-gate path) |
| 12 | Partial Package Release | 2 | (halted state after AG-1) |
| 13 | State Guard Assertions | 2 | (exception paths) |
| 14 | Mode B | 6 | `STARTED`, `QUEUED`, empty result, error |
| **Total** | | **34** | **13 distinct halt/active states** |

### Fixture Strategy

**There are no new Python test fixture files.** `SkillExecutor` is keyword-based — it derives all output from the `inputs` dict at runtime. The three `.md` files in `evaluations/test-cases/regulatory-subjects/` are used by the AGENT.md regression commands (`regression_tester.py`), not directly by Python tests.

Python test behaviour is controlled entirely by:
1. **Input parameters** — jurisdiction list, description keywords, industry field control which branches in `skill_executor.py` execute
2. **Simulation keys** — the 7 injection flags in `inputs` control gate behaviour

### Three Base Input Profiles

**EU BFSI Profile** (triggers EU AI Act Annex III + UK FCA path when `jurisdictions=["EU","UK"]`):
```
subject_description: "AI-powered credit scoring system using machine learning to assess
  loan applications for retail banking customers in the EU and UK. Processes financial
  history, credit bureau data, and employment records to predict default probability.
  Affects individual consumers applying for personal and mortgage loans."
subject_type: "AI Use Case"
jurisdictions: ["EU", "UK"]
industry: "BFSI"
target_maturity_level: "L4"
data_types: ["personal", "financial"]
```
Expected: `risk_tier = "High-risk (Annex III, Point 5)"`; Gate 2 default score ≈ 98 (passes ≥ 70); Gate 4 default score ≈ 90 (passes ≥ 85).

**India DPDP Profile** (triggers DPDP Act 2023 + RBI NBFC path):
```
subject_description: "AI customer support chatbot for an NBFC customer service platform
  in India, processing customer queries about loan accounts, EMI schedules, and account
  management. Handles personal financial data and interacts with individual retail
  customers across digital channels."
subject_type: "AI Use Case"
jurisdictions: ["India"]
industry: "BFSI"
target_maturity_level: "L3"
data_types: ["personal", "financial"]
```

**UK Insurance + Trigger 3 Profile** (triggers UK GDPR/DPA + FCA PRIN 12 path):
```
subject_description: "AI claims assessment model for UK general insurance operations,
  evaluating motor and property claims using computer vision and NLP to classify damage
  severity and estimate repair costs. Processes policyholder data and claims
  documentation for automated triage."
subject_type: "AI System"
jurisdictions: ["UK"]
industry: "BFSI"
trigger_type: "regulatory_change_alert"
target_maturity_level: "L4"
data_types: ["personal", "financial"]
```

### Import Pattern

New test file uses the same `_load_rwa_classes()` approach already in `test_firewall_hardening.py`. Copy the function verbatim into the new file (do not import from test_firewall_hardening.py — keep the file self-contained):

```
_load_rwa_classes():
  clears flat keys: orchestrator, state_manager, audit_logger, schema_validator,
                    output_builder, skill_executor from sys.modules
  loads via importlib with aliases: _rwa_audit_logger, _rwa_state_manager, _rwa_orchestrator
  assigns: Orchestrator, StateManager, AuditLogger into module globals
```

Both test classes call `_load_rwa_classes()` in `setUpClass`.

Traceability ID control: `self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id` in `setUp`.

### Class 1: TestRegulatoryWatchRuntimeModeA

**setUp:** create `Orchestrator`, set `trace_id = "TR-RW-TEST-8001"`, override ID generator, call `_cleanup()`.

**tearDown:** call `_cleanup()`.

**`_cleanup()`:** delete `runs_dir/{trace_id}_state.json`, `logs_dir/{trace_id}_audit.jsonl`, `packages_dir/{trace_id}/` (shutil.rmtree if exists).

**`_run_to_approval_2_pending(inputs)`:** calls `start_run`, calls `submit_approval_1("Approve")`, asserts `status == "APPROVAL_2_PENDING"`. Returns loaded state for further assertions.

---

**Category 1: Intake Validation (5 tests)**

`test_intake_missing_required_field_halts_intake_invalid`
EU BFSI profile with `subject_description` key removed.
Assert: `state["status"] == "HALTED_INTAKE_INVALID"`.

`test_intake_subject_description_too_short_halts_intake_invalid`
EU BFSI profile with `subject_description = "AI credit scoring system."` (29 chars).
Assert: `state["status"] == "HALTED_INTAKE_INVALID"`.

`test_intake_invalid_subject_type_halts_intake_invalid`
EU BFSI profile with `subject_type = "AI Product"`.
Assert: `state["status"] == "HALTED_INTAKE_INVALID"`.

`test_intake_invalid_maturity_level_halts_intake_invalid`
EU BFSI profile with `target_maturity_level = "L9"`.
Assert: `state["status"] == "HALTED_INTAKE_INVALID"`.

`test_intake_unsupported_jurisdiction_halts_unsupported_jurisdiction`
EU BFSI profile with `jurisdictions = ["US"]`.
Assert: `state["status"] == "HALTED_INTAKE_UNSUPPORTED_JURISDICTION"`.

---

**Category 2: Mode A Happy Paths (3 tests)**

`test_eu_bfsi_happy_path_reaches_complete`
Inputs: EU BFSI profile. No simulation keys.
`start_run` → assert `status == "APPROVAL_1_PENDING"`.
`submit_approval_1(trace_id, "Approve", "General Counsel Test", None)` → assert `status == "APPROVAL_2_PENDING"`.
`submit_approval_2(trace_id, "Approve", "DPO Test", None)` → assert `status == "COMPLETE"`.

`test_india_dpdp_happy_path_reaches_complete`
Inputs: India DPDP profile. No simulation keys.
Same approval flow. Assert `status == "COMPLETE"`.
Additional: assert `state["intermediate_data"]["regulatory_mapping_output_json"]` contains a regulation with "DPDP" or "Digital Personal Data" in `regulation_name`.

`test_uk_insurance_trigger3_trigger_type_accepted_reaches_complete`
Inputs: UK Insurance + Trigger 3 profile. No simulation keys.
Same approval flow. Assert `status == "COMPLETE"`.
Note in docstring: `trigger_type="regulatory_change_alert"` verifies intake validation accepts this trigger type. Mode B-specific change_summary addendum behaviour is verified in `TestRegulatoryWatchRuntimeModeB`.

---

**Category 3: Package File Verification (1 test)**

`test_complete_run_package_files_exist`
Inputs: EU BFSI profile. Run full happy path to `COMPLETE`.
Assert all five artifacts exist in `packages_dir/{trace_id}/`:
- `README.md`
- `{trace_id}-regulatory-scoping-matrix.md`
- `{trace_id}-operational-control-spec.md`
- `{trace_id}-regulatory-mapping-payload.json`
- `{trace_id}-control-mapping-payload.json`

---

**Category 4: Gate 1 Schema Failures (2 tests)**

`test_gate_1_schema_single_fail_retry_passes`
Inputs: EU BFSI + `simulate_gate_1_fail=True` (no double fail).
Orchestrator corrupts JSON on first attempt; retry uses original JSON; schema passes.
Assert: `status == "APPROVAL_1_PENDING"` (run continued past Gate 1; Gate 2 passed on default score 91).

`test_gate_1_schema_double_fail_halts_gate_1_schema`
Inputs: EU BFSI + `simulate_gate_1_fail=True`, `simulate_gate_1_fail_double=True`.
Assert: `status == "HALTED_GATE_1_SCHEMA"`.

---

**Category 5: Gate 2 Score Failures (2 tests)**

`test_gate_2_preliminary_band_halts_gate_2_preliminary`
Inputs: EU BFSI + `mock_s1_score=65`.
Assert: `status == "HALTED_GATE_2_PRELIMINARY"`.

`test_gate_2_insufficient_band_halts_gate_2_insufficient`
Inputs: EU BFSI + `mock_s1_score=40`.
Assert: `status == "HALTED_GATE_2_INSUFFICIENT"`.

---

**Category 6: Approval Gate 1 Failures (2 tests)**

`test_approval_1_reject_halts_approval_1_rejected`
Run to `APPROVAL_1_PENDING`. Call `submit_approval_1(trace_id, "Reject", "General Counsel Test", "Risk classification insufficient.")`.
Assert: `status == "HALTED_APPROVAL_1_REJECTED"`.

`test_approval_1_timeout_transitions_approval_timed_out`
Run to `APPROVAL_1_PENDING`. Call `submit_approval_1(trace_id, "Timeout", "System Scheduler", None)`.
Assert: `status == "APPROVAL_TIMED_OUT"`.

---

**Category 7: Gate 3b Claims Firewall — S2 Output (1 test)**

`test_gate_3b_firewall_breach_halts_firewall_breach`
Inputs: EU BFSI + `simulate_firewall_breach=True`.
`start_run` → `APPROVAL_1_PENDING`. `submit_approval_1(trace_id, "Approve", ...)`.
Assert: `status == "HALTED_FIREWALL_BREACH"`.
Docstring note: this exercises Gate 3b via the full `start_run` → `submit_approval_1` path, complementing `TestSkill1FirewallBypass` which tests Gate 1 firewall via direct `_evaluate_gate_1` call.

---

**Category 8: Gate 3a Schema Failures (2 tests)**

`test_gate_3a_schema_single_fail_retry_passes`
Inputs: EU BFSI + `simulate_gate_3a_fail=True` (no double fail).
Run to `APPROVAL_1_PENDING`. `submit_approval_1(trace_id, "Approve", ...)`.
Assert: `status == "APPROVAL_2_PENDING"` (Gate 3a retry succeeded; Gate 4 passed on default score 88).

`test_gate_3a_schema_double_fail_halts_gate_3a_schema`
Inputs: EU BFSI + `simulate_gate_3a_fail=True`, `simulate_gate_3a_fail_double=True`.
Run to `APPROVAL_1_PENDING`. `submit_approval_1(trace_id, "Approve", ...)`.
Assert: `status == "HALTED_GATE_3A_SCHEMA"`.

---

**Category 9: Gate 4 Score Failures (2 tests)**

`test_gate_4_below_threshold_halts_gate_4_below_threshold`
Inputs: EU BFSI + `mock_s2_score=75`.
Run to `APPROVAL_1_PENDING`. `submit_approval_1(trace_id, "Approve", ...)`.
Assert: `status == "HALTED_GATE_4_BELOW_THRESHOLD"`.

`test_gate_4_insufficient_halts_gate_4_insufficient`
Inputs: EU BFSI + `mock_s2_score=55`.
Run to `APPROVAL_1_PENDING`. `submit_approval_1(trace_id, "Approve", ...)`.
Assert: `status == "HALTED_GATE_4_INSUFFICIENT"`.

---

**Category 10: Approval Gate 2 Failures (3 tests)**

`test_approval_2_reject_halts_approval_2_rejected`
Run to `APPROVAL_2_PENDING` via helper. `submit_approval_2(trace_id, "Reject", "DPO Test", "RACI assignments unacceptable.")`.
Assert: `status == "HALTED_APPROVAL_2_REJECTED"`.

`test_approval_2_partial_halts_approval_2_partial`
Run to `APPROVAL_2_PENDING`. `submit_approval_2(trace_id, "Partial", "DPO Test", "One approver rejected.")`.
Assert: `status == "HALTED_APPROVAL_2_PARTIAL"`.

`test_approval_2_timeout_transitions_approval_timed_out`
Run to `APPROVAL_2_PENDING`. `submit_approval_2(trace_id, "Timeout", "System Scheduler", None)`.
Assert: `status == "APPROVAL_TIMED_OUT"`.

---

**Category 11: AG-2 Modifications — Clean Path (1 test)**

`test_approval_2_modifications_clean_reaches_complete`
Inputs: EU BFSI profile. No simulation keys (Gate 4 passes on default score 88 → 90).
Run to `APPROVAL_2_PENDING`.
`submit_approval_2(trace_id, "Approve with modifications", "DPO Test", "Change CTRL-01 Accountable role from Head of Retail Lending to Chief Risk Officer. No capability changes requested.")`.
Re-gate: Gate 3b (claims_linter on merged content — no violation in plain RACI text), Gate 3a schema on existing `s2_json` (passes), Gate 4 on existing score (passes).
Assert: `status == "COMPLETE"`.

---

**Category 12: Partial Package Release (2 tests)**

`test_partial_package_release_after_gate_4_fail`
Inputs: EU BFSI + `mock_s2_score=55`. Run to `APPROVAL_1_PENDING`. `submit_approval_1(trace_id, "Approve", ...)`. State halts at `HALTED_GATE_4_INSUFFICIENT`.
Call `release_partial_package(trace_id)`.
Assert: does not raise; partial package directory exists containing the S1 regulatory-scoping-matrix artifact; state remains `HALTED_GATE_4_INSUFFICIENT`.

`test_partial_package_release_before_approval_1_approved_raises`
Run to `APPROVAL_1_PENDING` (do NOT call `submit_approval_1`).
Call `release_partial_package(trace_id)`.
Assert: raises `ValueError`.

---

**Category 13: State Guard Assertions (2 tests)**

`test_submit_approval_1_on_wrong_state_raises`
Run full happy path to `APPROVAL_2_PENDING`. Then call `submit_approval_1(trace_id, "Approve", ...)` again.
Assert: raises `ValueError` (state is no longer `APPROVAL_1_PENDING`).

`test_submit_approval_2_on_wrong_state_raises`
Run to `APPROVAL_1_PENDING` (do NOT call `submit_approval_1`). Then call `submit_approval_2(trace_id, "Approve", ...)`.
Assert: raises `ValueError`.

---

### Class 2: TestRegulatoryWatchRuntimeModeB

**setUp:** create `Orchestrator`; initialise `self.pre_created_paths = []` and `self.mode_b_results = []`.

**tearDown:**
```
for path in self.pre_created_paths:
    if path.exists(): path.unlink()
for result in self.mode_b_results:
    tid = result.get("traceability_id")
    if tid:
        delete runs_dir/{tid}_state.json, logs_dir/{tid}_audit.jsonl, packages_dir/{tid}/
```

**`_create_completed_run_state(trace_id, jurisdictions, regulations_list, risk_tier, timestamp)`**
Creates `runs_dir/{trace_id}_state.json` with structure:
```json
{
  "status": "COMPLETE",
  "traceability_id": "<trace_id>",
  "inputs": {
    "jurisdictions": <jurisdictions>,
    "subject_description": "AI credit scoring system for BFSI retail lending in the
      financial services sector. Processes personal and financial data for loan
      application decisions affecting individual retail customers.",
    "subject_type": "AI Use Case",
    "target_maturity_level": "L4",
    "industry": "BFSI"
  },
  "intermediate_data": {
    "regulatory_mapping_output_json": {
      "applicable_regulations": [
        {"regulation_name": "<reg>", "jurisdiction": "<jur>"} for each pair
      ],
      "risk_tier": "<risk_tier>",
      "score": 85
    }
  },
  "history": [{"timestamp": "<timestamp>"}]
}
```
Appends path to `self.pre_created_paths`.

**Trace ID naming for pre-created files:** use `TR-RW-PRIOR-{N:04d}` (e.g. `TR-RW-PRIOR-0001`). The `generate_traceability_id()` globs `TR-RW-{year}-*.json` — files named `TR-RW-PRIOR-*` do not collide with the ID counter. Mode B's glob (`TR-RW-*_state.json`) still finds them.

---

**Mode B Tests (6 tests)**

`test_mode_b_finds_matching_runs_and_starts_reassessments`
setUp: 2 completed states — `jurisdictions=["EU"]`, regulation `"EU AI Act"` / jurisdiction `"EU"`.
`execute_mode_b({"regulation_name": "EU AI Act", "jurisdiction": "EU", "change_summary": "Annex III credit scoring criteria updated.", "change_severity": "Major"})`.
Store result in `self.mode_b_results`.
Assert: len 2; both `status == "STARTED"`; both `traceability_id` non-null; both `prior_assessment_id` ∈ pre-created IDs.

`test_mode_b_rate_limits_to_3_concurrent_starts_rest_queued`
setUp: 5 completed states all matching EU AI Act / EU.
Call `execute_mode_b` with matching alert.
Assert: 5 results; first 3 `status == "STARTED"`; last 2 `status == "QUEUED"` and `traceability_id == None`.

`test_mode_b_returns_empty_when_no_matching_runs`
setUp: 2 completed states with `jurisdictions=["EU"]` and regulation `"EU AI Act"`.
`execute_mode_b({"regulation_name": "UK GDPR", "jurisdiction": "UK", ...})` — no match on either criterion.
Assert: returns `[]`.

`test_mode_b_missing_required_field_raises_value_error`
`execute_mode_b({"regulation_name": "EU AI Act", "jurisdiction": "EU"})` — missing `change_summary` and `change_severity`.
Assert: raises `ValueError`.

`test_mode_b_includes_change_summary_in_reassessment_subject`
setUp: 1 completed state matching EU AI Act / EU.
`execute_mode_b({"regulation_name": "EU AI Act", "jurisdiction": "EU", "change_summary": "New Article 10 data governance requirements for high-risk AI.", "change_severity": "Major"})`.
Load new run's state file. Assert:
- `state["inputs"]["subject_description"]` ends with `"--- REGULATORY CHANGE RE-ASSESSMENT ---\nNew Article 10 data governance requirements for high-risk AI."`
- `state["inputs"]["existing_assessment_id"] == prior_trace_id`

`test_mode_b_prioritizes_annex_iii_over_general_risk`
setUp: 2 completed states:
- `TR-RW-PRIOR-0001` — `risk_tier="General Enterprise"`, timestamp `"2026-01-01T10:00:00Z"` (earlier)
- `TR-RW-PRIOR-0002` — `risk_tier="High-risk (Annex III, Point 5)"`, timestamp `"2026-06-01T10:00:00Z"` (later)
Both match EU AI Act / EU. `change_severity="Major"` (same weight for both).
`execute_mode_b(...)`. Assert: result[0]["prior_assessment_id"] == "TR-RW-PRIOR-0002" (Annex III prioritised over General Enterprise despite later timestamp).

---

## SECTION 4 — Repository Changes

### New Files

**`evaluations/scripts/test_regulatory_watch_runtime.py`**
- ~390 lines
- Two test classes: `TestRegulatoryWatchRuntimeModeA` (28 tests), `TestRegulatoryWatchRuntimeModeB` (6 tests)
- `_load_rwa_classes()` helper (verbatim copy from `test_firewall_hardening.py`)
- `_cleanup()`, `_run_to_approval_2_pending()`, `_create_completed_run_state()` helpers
- Imports: `json`, `shutil`, `unittest`, `glob` at top; `repo_root = Path(__file__).resolve().parents[2]`

**`evaluations/test-cases/regulatory-subjects/minimal-risk-internal-tool.md`**
- Describes an internal HR scheduling optimisation tool; EU jurisdiction only; no BFSI, no high-risk keywords
- Must NOT contain: `credit`, `bank`, `loan`, `insurance`, `BFSI`, `claims`, `biometric`, `health`, `financial`
- Appropriate content: `industry: "General Enterprise"`, `jurisdictions: ["EU"]`, `trigger_type: new_use_case_registration`, `target_maturity_level: "L2"`, `data_types: ["personal"]`
- Skill executor result: EU AI Act low-risk path; GDPR applies; no Annex III classification
- Purpose: satisfies L4A blocker from `AGENT.md` — the one missing regulatory-subjects fixture
- Format: same front-matter and narrative structure as the existing 3 regulatory-subjects fixtures

### New Directories

None.

### Modified Files

None. Specifically:
- **`test_firewall_hardening.py`** — preserved intact. `TestApprovalModificationBypass` and `TestSkill1FirewallBypass` remain there. Do not move them.
- **`orchestrator.py`** — no changes. Simulation hooks are already present.
- **`AGENT.md`** — stale blockers (B-01, B-04, B-05) deferred to PR-009.
- **`agent_certifier.py`** — upgrade to require test file presence for L4 deferred to PR-012.

### Verification Commands

```bash
# After implementation:
python -m pytest evaluations/scripts/test_regulatory_watch_runtime.py -v
# Expected: 34 passed

python -m pytest evaluations/scripts/test_firewall_hardening.py -v
# Expected: 9 passed (no regressions)

# L4A regression commands (from AGENT.md §12 and evaluation.md §12):
python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/regulatory-subjects/eu-ai-act-high-risk-banking.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/regulatory-subjects/india-dpdp-customer-support-ai.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/regulatory-subjects/uk-insurance-claims-model.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md

python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/india-dpdp-customer-support-ai-gold-standard.md

python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/uk-insurance-claims-model-gold-standard.md
```

---

## SECTION 5 — Certification Criteria

### L4A — Test Case Gate

| Requirement | Verification |
|---|---|
| `minimal-risk-internal-tool.md` present | `ls evaluations/test-cases/regulatory-subjects/` — all 4 files listed |
| RM regression: eu-ai-act subject fixture | `regression_tester.py` command above returns PASS |
| RM regression: india-dpdp subject fixture | Same; PASS |
| RM regression: uk-insurance subject fixture | Same; PASS |
| GCM regression: EU AI Act gold standard | `regression_tester.py` against `governance-control-mapping/structure.json` returns PASS |
| Claims linter: all 3 gold standards | `claims_linter.py` on each — 0 violations |

### L4B — Implementation Completeness Gate (already satisfied)

| Requirement | Evidence |
|---|---|
| All runtime files present | `ls agents/regulatory-watch-agent/runtime/` — 6 Python files + `config.yaml` |
| All 24 state transitions implemented | `VALID_TRANSITIONS` dict in `state_manager.py` covers all `state-machine.md` transitions |
| Gates call `claims_linter.py` and `schema_validator` | `_evaluate_gate_1` and `_evaluate_gate_3` in `orchestrator.py` call both tools |
| Score thresholds match `evaluation.md` | Gate 2 bands (55/70) and Gate 4 bands (70/85) match `evaluation.md §3` and `§7` |
| Schema location is `contracts/` | `orchestrator.py` loads from `agents/regulatory-watch-agent/runtime/contracts/` — confirmed |
| `config.yaml` exposes required thresholds | `gate_2_pass_threshold`, `gate_4_pass_threshold`, `approval_timeout_days` present |

### L4C — Production Readiness Gate (satisfied by PR-008 test suite)

| Requirement | Test Evidence |
|---|---|
| Mode A dry-run: EU BFSI → COMPLETE | `test_eu_bfsi_happy_path_reaches_complete` |
| Mode A dry-run: India DPDP → COMPLETE | `test_india_dpdp_happy_path_reaches_complete` |
| Mode A dry-run: UK Insurance (Trigger 3) → COMPLETE | `test_uk_insurance_trigger3_trigger_type_accepted_reaches_complete` |
| Complete run produces all package artifacts | `test_complete_run_package_files_exist` |
| Claims Firewall: Gate 3b breach via `start_run` | `test_gate_3b_firewall_breach_halts_firewall_breach` |
| Approval Gate 1 correctly transitions | `test_approval_1_reject_halts_approval_1_rejected` + `test_approval_1_timeout_transitions_approval_timed_out` |
| Approval Gate 2 correctly transitions | `test_approval_2_reject_*`, `test_approval_2_partial_*`, `test_approval_2_timeout_*` |
| AG-2 re-gate path: clean modifications → COMPLETE | `test_approval_2_modifications_clean_reaches_complete` |
| Mode B: finds affected runs, starts reassessments | `test_mode_b_finds_matching_runs_and_starts_reassessments` |
| Mode B: 3-run concurrency cap enforced | `test_mode_b_rate_limits_to_3_concurrent_starts_rest_queued` |
| Mode B: Annex III prioritisation | `test_mode_b_prioritizes_annex_iii_over_general_risk` |
| State persistence (implicit) | Every approval gate test that crosses a state boundary loads from disk |
| All 13 major halt states reached | Confirmed across 14 test categories |
| `agent_certifier.py` reports L4 | Already true; non-blocking for PR-008 |

### Certification Suspension Conditions

From `evaluation.md §11` — three conditions auto-suspend certification after it is granted:
1. Claims Firewall violation in production run not caught by Gate 3b
2. Regression test failure introduced by a skill update and not caught pre-execution
3. `canonical-product-model.md` updated without agent update within 5 business days

PR-008 does not add certifier tests for these conditions. Deferred to PR-012.

---

## SECTION 6 — Risks and Weaknesses

### Weakness 1: Gate 1 Claims Firewall path is not exercisable via `start_run` without monkey-patching

`SkillExecutor.compile_regulatory_mapping_to_markdown` never produces firewall-violating output — it is deterministic keyword-based logic that does not reference Ethana capabilities. No `simulate_s1_firewall_breach` hook exists in the orchestrator. The existing `TestSkill1FirewallBypass` in `test_firewall_hardening.py` covers this path via direct `_evaluate_gate_1` call.

**Risk:** if `_run_skill_1` is refactored to inline Gate 1 logic (rather than delegating to `_evaluate_gate_1`), the unit test stops covering the actual call path.

**Blind spot:** PR-008 does not test the Gate 1 Claims Firewall branch end-to-end via `start_run`. The combination of (S1 execution → compilation → firewall breach) is only tested at the `_evaluate_gate_1` boundary.

**Mitigation:** document this gap in the test file docstring. A future hardening PR should add a `simulate_s1_firewall_breach` hook to `orchestrator.py` and a corresponding test.

### Weakness 2: Mode B tests create real filesystem artifacts requiring careful cleanup

`execute_mode_b` calls `start_run` for up to 3 matched runs synchronously. Each creates a state file and an audit log in `runs_dir` and `logs_dir`. If tearDown is incomplete, artifacts contaminate subsequent test runs, and `generate_traceability_id()` (which scans for existing `TR-RW-{year}-*.json` files) will increment past leaked IDs.

**Risk:** a tearDown failure in one Mode B test corrupts subsequent Mode B tests in the same suite run.

**Mitigation:** tearDown must be defensive — collect every `traceability_id` returned by `execute_mode_b` in `self.mode_b_results`; delete each explicitly. Also delete all pre-created state files by their known paths in `self.pre_created_paths`. Recommend a `@classmethod tearDownClass` that globs `runs_dir/TR-RW-{year}-*` and removes any state file with a trace_id created during this test run, as a belt-and-suspenders measure for CI environments.

### Weakness 3: Simulation keys persist through the entire run; mis-authored tests can produce false green

Any base_inputs helper that accidentally includes a simulation key will push every test using it through the wrong path. A `mock_s1_score=70` left in a helper would cause Gate 2 failure tests to pass at the wrong threshold — appearing correct but asserting wrong behaviour.

**Mitigation:** base_inputs helpers must explicitly NOT include simulation keys. Keys are added only as inline additions in individual test bodies. Code review must check every test in categories 4–11 for accidental key inheritance.

### Weakness 4: The three Mode A happy-path tests exercise the same orchestrator code path

The `_map_to_fixture` routing result varies (eu-ai-act / india-dpdp / uk-insurance) but has no effect on skill execution — it is logged only. What genuinely differs between the three tests is the `skill_executor.py` regulatory path (EU Annex III, India DPDP, UK FCA). These are distinct branches. But the orchestrator-level state machine is exercised identically three times.

**Challenge:** Are three separate happy-path tests necessary, or is one sufficient?

**Answer:** Yes — the value is regression coverage for skill_executor changes. If the India DPDP path is modified and starts producing a score below 70 (Gate 2 would halt), or starts producing output that accidentally matches a firewall term, the India test catches it. The three tests provide independent signal for the three jurisdiction code paths. The cost is low; the regression protection is real.

### Weakness 5: Mode B Trigger 3 operator confirmation requirement is unimplemented

`workflow.yaml` rule V-05 specifies: for `trigger_type=Critical` with ≥ 3 affected subjects, human operator confirmation is required before Mode B queue processing begins. The current `execute_mode_b` implementation starts runs immediately for the first 3 matches and queues the rest, regardless of severity level or affected count.

**Risk:** `test_mode_b_rate_limits_to_3_concurrent_starts_rest_queued` will assert 3 STARTED without operator confirmation — which is the current behaviour. The test will pass, but it will implicitly validate a spec violation without marking it.

**Mitigation:** add a comment to the relevant Mode B test: `# NOTE: workflow.yaml V-05 requires operator confirmation before queue processing for Critical severity + ≥3 affected runs. This gate is not yet enforced in execute_mode_b. When implemented, this test must require an operator confirmation step before asserting STARTED.` This makes the gap visible without blocking PR-008.

### Weakness 6: UK Insurance Trigger 3 test name does not accurately reflect scope

`start_run` treats all `trigger_type` values identically after intake validation. The `regulatory_change_alert` trigger type has no special orchestrator handling — the change_summary addendum is added by `execute_mode_b`, not by `start_run`. A direct `start_run("regulatory_change_alert", ...)` call verifies that the trigger type is accepted at intake, nothing more.

**Mitigation:** rename the test to `test_uk_insurance_trigger3_trigger_type_accepted_reaches_complete` to accurately reflect what is tested. The Mode B addendum behaviour is covered by `test_mode_b_includes_change_summary_in_reassessment_subject`.

### Weakness 7: APPROVAL_TIMED_OUT recovery path is untested

`APPROVAL_TIMED_OUT` is explicitly not terminal. `state-machine.md` and `VALID_TRANSITIONS` show recovery paths: `APPROVAL_TIMED_OUT` → `APPROVAL_1_PENDING`, `APPROVAL_2_PENDING`, `APPROVAL_1_APPROVED`, `APPROVAL_2_APPROVED`. After a timeout, a human can reactivate the approval. PR-008 reaches `APPROVAL_TIMED_OUT` but does not test resume from it.

**Risk:** a regression that breaks the timeout-recovery transition would not be caught.

**Recommendation:** defer `test_approval_1_timeout_then_resume` to PR-012. That test would: reach `APPROVAL_TIMED_OUT` via timeout action → call `submit_approval_1("Approve")` from that state → assert run resumes correctly to `APPROVAL_2_PENDING`.

### Self-Challenge: Does PR-008 Prove the RWA Produces Correct Outputs, or Just That It Runs?

Honest answer: both, but predominantly the latter. PR-008 verifies that the 969-line orchestrator executes without crashing and transitions through the correct states. It does not verify that the regulatory analysis produced for a UK insurance AI system is accurate, complete, or legally defensible.

The real L4 quality verification is the regression suite from `evaluation.md §12` — `regression_tester.py` commands run against known-good gold standards and subject fixtures. PR-008 creates the Python safety net. The regression commands create the quality evidence. Both are required for genuine L4. The certification criteria in Section 5 require both.

---

## SECTION 7 — Final Recommendation

**Proceed with PR-008 as designed.** Scope is minimal and correct: 2 new files, 0 modified files, 34 tests. No existing code is touched.

### Implementation Order

1. **Create `minimal-risk-internal-tool.md` first.** This takes 20 minutes, has zero risk, and unblocks L4A. Run the six regression commands from Section 4 immediately after to confirm L4A is satisfied before writing any test code.

2. **Implement `TestRegulatoryWatchRuntimeModeA` in blocks of 5–7 tests.** These are self-contained. Run `python -m pytest -k TestRegulatoryWatchRuntimeModeA -v` after each block. The intake validation tests should pass immediately. The happy-path tests will surface any discrepancy between the simulation hook keys and the actual orchestrator implementation.

3. **Implement `TestRegulatoryWatchRuntimeModeB` last.** Write `tearDown` and `_create_completed_run_state` before writing any test bodies. Run Mode B tests in isolation first (`-k TestRegulatoryWatchRuntimeModeB`) before the full suite. Mode B test cleanup is the highest implementation risk in this PR.

### Scope Boundary

PR-008 does not:
- Modify any existing file
- Update `AGENT.md` stale blockers (deferred to PR-009)
- Upgrade `agent_certifier.py` to require test file presence (deferred to PR-012)
- Add the `simulate_s1_firewall_breach` hook (deferred to a future hardening PR)
- Add `APPROVAL_TIMED_OUT` recovery tests (deferred to PR-012)

### After PR-008

- RWA certification status genuinely changes. Program review can be updated: RWA moves from "Prototype — 0 happy-path tests" to "L4 — full Mode A cycle verified, Mode B basic operation verified, Claims Firewall integration verified, 34 passing tests."
- `reviews/governance-os-master-status.md` "Partial Agents" section can remove RWA upon successful PR-008 merge.
- PR-008 and PR-009 have no shared files. They can be implemented in parallel.

### Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| Mode B tearDown incomplete → test pollution | Medium | Medium | Defensive tearDown + tearDownClass glob cleanup |
| Simulation key accidentally in base_inputs | Low | Low | Code review gate; helpers have no simulation keys by design |
| Gate 1 Firewall gap not caught post-refactor | Low | Low | Document in test docstring; add hook in future hardening PR |
| Mode B V-05 operator confirmation gap | Medium | Low | Comment in test marking the unimplemented spec requirement |
