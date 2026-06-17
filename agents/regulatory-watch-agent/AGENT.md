# Regulatory Watch Agent

**Version:** 1.0-spec  
**Certification level:** L3 (Evaluation Certified) — L4 not yet achieved  
**Status:** Specification complete — implementation not started  
**Skill chain:** regulatory-mapping → governance-control-mapping  
**Workflow coverage:** `workflows/regulatory-compliance-workflow.md` Steps 4.1–4.2  
**Architecture reference:** `docs/architecture/regulatory-watch-agent-architecture.md`

---

## 1. Purpose

The Regulatory Watch Agent converts an AI subject (a use case, deployed system, or AI portfolio) into a Compliance and Coverage Package: a Regulatory Scoping Matrix produced by regulatory-mapping, followed by an Operational Control Specification produced by governance-control-mapping.

The agent is not an autonomous decision-maker. Every run contains two mandatory human approval gates. The agent orchestrates the skill sequence and enforces quality gates; humans approve the regulatory judgements.

**Scope boundary:** The agent executes Steps 4.1 and 4.2 of the Regulatory Compliance Workflow. Step 4.3 (ethana-solution-mapping) is outside the current agent's certified scope. The agent produces a structured handoff note for the Step 4.3 consumer but does not execute it. This is a certification constraint, not a permanent design decision.

---

## 2. Operational Modes

### Mode A — Assessment

Triggered by a specific AI subject. The agent executes the full two-skill chain against the submitted subject and delivers a Compliance and Coverage Package to named approvers.

**Entry triggers:** Trigger 1 (New AI Use Case Registration), Trigger 2 (Jurisdictional Expansion), or any Trigger 3 re-assessment that has been queued by Mode B.

### Mode B — Watch

Triggered by a regulatory change event. The agent determines which previously-assessed AI subjects are affected by the change and queues re-assessment Mode A runs for each.

**Rate limit:** No more than three concurrent re-assessment jobs from a single Trigger 3 event. If more than three subjects are affected, the remaining subjects are queued and a human operator authorises further queue processing.

---

## 3. Trigger Events

All triggers must carry a `traceability_id` generated at intake. Format: `TR-RW-{YYYY}-{NNNN}`. The traceability ID links all artifacts, approvals, and run logs for a single run.

### Trigger 1 — New AI Use Case Registration

| Field | Required | Description |
|---|---|---|
| `trigger_type` | Yes | `new_use_case_registration` |
| `subject_description` | Yes | Min 50 chars; must identify AI technology, data processed, affected individuals, deployment location |
| `subject_type` | Yes | `AI Use Case` / `AI System` / `AI Portfolio` |
| `jurisdictions` | Yes | One or more of: `EU`, `UK`, `India` |
| `target_maturity_level` | Yes | `L1` through `L5` |
| `industry` | No | Sector vertical; activates BFSI overlay if applicable |
| `data_types` | No | Array of data categories (personal, financial, biometric, health) |
| `deployment_model` | No | `Cloud SaaS` / `VPC` / `On-premises` |
| `existing_tooling` | No | Array of third-party tools already in use |

**Source:** AI portfolio registry (CRM, JIRA, or equivalent)  
**Signal:** AI use case reaches the "Compliance Review Required" lifecycle stage  
**Agent response:** Single Mode A run

### Trigger 2 — Jurisdictional Expansion

All Trigger 1 fields, plus:

| Field | Required | Description |
|---|---|---|
| `trigger_type` | Yes | `jurisdictional_expansion` |
| `existing_assessment_id` | Yes | Reference to the prior regulatory mapping output |
| `new_jurisdiction` | Yes | The jurisdiction being added |

**Agent response:** Mode A run scoped to the incremental jurisdiction. The prior assessment is loaded as context but a new assessment is produced — not amended.

### Trigger 3 — Regulatory Change Alert

| Field | Required | Description |
|---|---|---|
| `trigger_type` | Yes | `regulatory_change_alert` |
| `regulation_name` | Yes | The regulation that changed |
| `jurisdiction` | Yes | Affected jurisdiction |
| `change_summary` | Yes | Description of what changed and effective date |
| `change_severity` | Yes | `Critical` / `Major` / `Minor` |

**Agent response (Mode B):**
1. Query assessment memory for all prior outputs referencing the affected regulation
2. Generate re-assessment jobs ordered by: Critical severity first, then by AI subject risk classification (Annex III high-risk first)
3. Execute Mode A runs sequentially per queued subject; do not batch
4. If more than 3 subjects affected and `change_severity = Critical`: halt queue processing until a human operator authorises continuation

---

## 4. Input Validation

Before any skill is executed, the intake sub-component validates:

1. All required fields present and non-empty
2. `jurisdictions` contains only `EU`, `UK`, or `India` — unsupported jurisdictions halt with `HALTED_INTAKE_UNSUPPORTED_JURISDICTION`
3. `subject_description` classified as `Low` / `Medium` / `High` evidence quality per regulatory-mapping Phase 1.4 — `Low` triggers a warning, does not block
4. For Trigger 2: `existing_assessment_id` resolves to a valid entry in assessment memory
5. For Trigger 3 with `change_severity = Critical` affecting ≥ 3 prior assessments: human operator confirmation required before Mode B queue processing begins

Intake validation failure halts the agent before any skill is executed and returns an error payload.

---

## 5. Outputs

### 5.1 Regulatory Scoping Matrix

Produced by Skill 1 (regulatory-mapping). Requires Approval Gate 1 (General Counsel) before Skill 2 begins.

| Artifact | Format | Validation |
|---|---|---|
| `{traceability_id}-regulatory-scoping-matrix.md` | 9-section Markdown | Structural regression: `evaluations/baselines/regulatory-mapping/structure.json` |
| `{traceability_id}-regulatory-mapping-payload.json` | JSON | Schema: `workflows/schemas/regulatory_mapping_output.json` |

**Release condition:** Schema valid + score ≥ 70/100 + Approval Gate 1 passed.

### 5.2 Operational Control Specification

Produced by Skill 2 (governance-control-mapping). Requires Approval Gate 2 (DPO + Information Security Lead) before package assembly.

| Artifact | Format | Validation |
|---|---|---|
| `{traceability_id}-operational-control-spec.md` | 10-section Markdown | Structural regression: `evaluations/baselines/governance-control-mapping/structure.json` |
| `{traceability_id}-control-mapping-payload.json` | JSON | Schema: `workflows/schemas/control_mapping_output.json` |

**Release condition:** Schema valid + Claims Firewall passes (0 violations) + score ≥ 85/100 + Approval Gate 2 passed.

### 5.3 Compliance and Coverage Package

The combined final deliverable, assembled after Approval Gate 2:

```
{traceability_id}-regulatory-scoping-matrix.md
{traceability_id}-operational-control-spec.md
{traceability_id}-regulatory-mapping-payload.json
{traceability_id}-control-mapping-payload.json
{traceability_id}-run-log.json
{traceability_id}-handoff-note.md
```

The `run-log.json` contains: trigger event, all state transitions with timestamps, gate scores (per-dimension), approval decisions, escalation events.

### 5.4 Handoff Note

`{traceability_id}-handoff-note.md` is the structured input for the downstream ethana-solution-mapping consumer (human practitioner or Client Assessment Agent):

```markdown
# Handoff Note: {traceability_id}

**Upstream traceability IDs:**
- Regulatory Mapping: TR-RW-{YYYY}-{NNNN}
- Control Mapping: TR-RW-{YYYY}-{NNNN} (same run)

**Control mapping payload location:** {path}
**Jurisdiction set:** {list}
**Sector:** {sector}
**Deployment model:** {model}
**Target maturity level:** {level}

**Ethana capability references in Section 10 requiring validation:**
[List of capabilities referenced in GCM Section 10, with canonical status at
assessment date, and whether capability-validation was run for each.]

**Recommended next step:** Execute ethana-solution-mapping against the
control-mapping-payload.json above to produce a Coverage Confidence Score
and proposal-safe capability mapping for each designed control.
```

---

## 6. Skill Chain

### Skill 1: regulatory-mapping

**Input mapping from trigger payload:**

| Trigger field | Skill 1 field | Notes |
|---|---|---|
| `subject_description` | `subject_description` | Direct pass-through |
| `subject_type` | `subject_type` | Direct pass-through |
| `jurisdictions` | `jurisdictions` | Direct pass-through |
| `industry` | `industry` | Defaults to "General Enterprise" if absent |
| `data_types` | `data_types` | Direct pass-through |
| `deployment_model` | `deployment_model` | Direct pass-through |
| `change_summary` (Trigger 3 only) | Appended to `subject_description` | Prefix: "This assessment is a regulatory change re-assessment. Change summary: " |

**Output used:** Full `regulatory_mapping_output.json` → stored in run-scoped memory and passed as `upstream_payload` to Skill 2.

**Minimum viable Section 6:** Skill 2 Phase 1.1 validation requires `applicable_regulations[*].control_requirements` to be present and non-empty. The agent must verify this before handing off.

### Inter-Skill Payload

```json
{
  "upstream_source_type": "Regulatory Mapping",
  "traceability_id": "TR-RW-{YYYY}-{NNNN}",
  "upstream_payload": "{full regulatory_mapping_output JSON}",
  "target_maturity_level": "{from trigger payload}",
  "jurisdictions": "{from Skill 1 output}",
  "client_sector": "{from trigger payload industry field}",
  "deployment_model": "{from trigger payload}",
  "existing_tooling": "{from trigger payload}"
}
```

Approval Gate 1 approver notes, if any, are included as an additional field:

```json
"approval_1_notes": "{text from General Counsel's Approve with notes action, or null}"
```

### Skill 2: governance-control-mapping

**Input:** The inter-skill payload above.

**Phases executed:** Phase 1 (Intake and Baseline Calibration) through Phase 7 (Maturity Phasing and Quality Gates), including Phase 5 Platform Status Audit — which must consult `knowledge/ethana/canonical-product-model.md` for every Ethana capability reference and is subject to the Claims Firewall gate.

**Output used:** `control_mapping_output.json` + `{traceability_id}-operational-control-spec.md`.

---

## 7. Evaluation Gates

Four automated gates enforce output quality. No gate may be bypassed. See `evaluation.md` for gate specifications.

| Gate | Tool | Threshold | Position |
|---|---|---|---|
| Gate 1 — RM Schema | `workflow_validator.py` | 0 errors | After Skill 1 |
| Gate 2 — RM Score | evaluation rubric | ≥ 70/100 | After Gate 1 |
| Gate 3a — GCM Schema | `workflow_validator.py` | 0 errors | After Skill 2 |
| Gate 3b — Claims Firewall | `claims_linter.py` | 0 violations | After Skill 2, concurrent with Gate 3a |
| Gate 4 — GCM Score | evaluation rubric | ≥ 85/100 | After Gate 3 |

**Claims Firewall is non-negotiable.** A Gate 3b violation halts the agent in `HALTED_FIREWALL_BREACH` state, auto-routes to the Compliance Director, and cannot be re-run without Compliance Director sign-off. The output is never released.

---

## 8. Approval Gates

### Approval Gate 1 — Regulatory Scoping Matrix Review

**Approver:** General Counsel (or designated Legal Representative)  
**Triggered:** After Gates 1 and 2 pass  
**Timeout:** 5 business days (configurable)

**Payload presented:**
- `{traceability_id}-regulatory-scoping-matrix.md`
- Per-dimension score breakdown from Gate 2
- Evidence quality rating (High / Medium / Low)
- Any conditional applicability flags requiring legal judgement
- Any ambiguous EU AI Act Annex III classifications with determining factors

**Actions:**

| Action | Agent state transition |
|---|---|
| Approve | → `APPROVAL_1_APPROVED` → `SKILL_2_RUNNING` |
| Approve with notes | → `APPROVAL_1_APPROVED` (notes attached to inter-skill payload) → `SKILL_2_RUNNING` |
| Reject with revision request | → `HALTED_APPROVAL_1_REJECTED` |

**Scope of approval:** The Regulatory Scoping Matrix is accurate as a statement of regulatory applicability and obligation scope. Risk classifications are legally defensible. This does not authorise the control design (Approval Gate 2 covers that). The run log must record that this is not a formal legal opinion.

### Approval Gate 2 — Control Specification and RACI Review

**Approvers:** DPO + Information Security Lead (joint; both required)  
**Triggered:** After Gates 3 and 4 pass  
**Timeout:** 5 business days (configurable)

**Payload presented:**
- `{traceability_id}-operational-control-spec.md`
- Per-section score breakdown from Gate 4
- Claims Firewall compliance status (confirmed pass)
- RACI matrix (Section 8) with named role assignments
- Section 10 Ethana Configuration Guide with all In Build capabilities flagged as roadmap items

**Actions:**

| Action | Agent state transition |
|---|---|
| Both approve | → `APPROVAL_2_APPROVED` → `COMPLETE` |
| Approve with modifications | → RACI/caveat amendments incorporated → Gates 3 and 4 re-run → `APPROVAL_2_APPROVED` |
| One approves, one rejects | → `HALTED_APPROVAL_2_PARTIAL` (conflict resolution required) |
| Both reject | → `HALTED_APPROVAL_2_REJECTED` |

**Scope of approval:** Controls are implementable given the organisation's current security posture and team structure. RACI assignments are accepted by the named role owners. The maturity roadmap timeline is realistic.

---

## 9. Memory Model

### Tier 1 — Run-Scoped Memory

Exists for the duration of a single run. Must survive system restarts when approval gates are open (in-process memory is insufficient).

| Data element | Format | Used for |
|---|---|---|
| Trigger event payload | JSON | Skill 1 input construction |
| Run state + timestamps | Enum + ISO 8601 | State persistence; run log |
| Skill 1 output (Markdown) | Markdown | Approval Gate 1 delivery |
| Skill 1 output (JSON) | JSON | Gate 1 validation; inter-skill payload |
| Skill 1 gate scores (per-dimension) | JSON | Gate 2 evaluation; run log |
| Approval Gate 1 decision + notes | JSON | Run log; Skill 2 context |
| Skill 2 output (Markdown) | Markdown | Approval Gate 2 delivery |
| Skill 2 output (JSON) | JSON | Gate 3 validation; final package |
| Skill 2 gate scores (per-dimension) | JSON | Gate 4 evaluation; run log |
| Claims Firewall report | JSON | Gate 3b; run log |
| Approval Gate 2 decision + notes | JSON | Run log; final package |

### Tier 2 — Assessment Memory

Persistent across runs. Indexed for Mode B re-assessment identification.

| Data element | Retention | Index keys |
|---|---|---|
| All regulatory-mapping outputs (JSON) | Indefinite until superseded | `traceability_id`, `subject_description`, `jurisdictions`, `regulations_applicable` |
| All control-mapping outputs (JSON) | Indefinite until superseded | `traceability_id`, Skill 1 `traceability_id` |
| Assessment status | Indefinite | `traceability_id` |
| Subject fingerprint | Indefinite | `subject_type` + `jurisdictions` + `industry` hash |

Assessment memory enables: Mode B affected-subject identification; deduplication; audit trail.

### Tier 3 — Regulatory Calendar Memory (Mode B only)

| Data element | Retention |
|---|---|
| Regulation name + change description | 3 years |
| Effective date | 3 years |
| Agent severity classification | 3 years |
| Number of affected assessments queued | 3 years |
| Queue processing status (Queued / In progress / Complete) | 3 years |

Purpose: prevents duplicate re-assessment queues for the same regulatory change event.

### What the Agent Must Not Retain

- Personally identifiable information beyond what is minimally required to identify the AI subject
- Client confidential data beyond what the trigger payload contained
- Approval decision reasoning beyond what the approver explicitly records
- Intermediate skill outputs that did not pass quality gates (discard, do not store)

---

## 10. Failure Handling

### Failure States

| Failure type | State | Recovery path |
|---|---|---|
| Input validation failure | `HALTED_INTAKE_INVALID` | Operator corrects inputs and resubmits |
| Unsupported jurisdiction | `HALTED_INTAKE_UNSUPPORTED_JURISDICTION` | Escalate to Compliance Analyst; do not extrapolate |
| Skill 1 schema invalid (post-retry) | `HALTED_GATE_1_SCHEMA` | Escalate to Compliance Analyst |
| Skill 1 score 55–69 | `HALTED_GATE_2_PRELIMINARY` | Reclassify as Preliminary; generate revision request with failing dimension breakdown |
| Skill 1 score < 55 | `HALTED_GATE_2_INSUFFICIENT` | Escalate to Compliance Analyst; do not auto-retry |
| Approval Gate 1 rejected | `HALTED_APPROVAL_1_REJECTED` | Return to Skill 1 with reviewer notes; operator initiates revised run |
| Skill 2 schema invalid (post-retry) | `HALTED_GATE_3A_SCHEMA` | Escalate to Compliance Analyst |
| Claims Firewall breach | `HALTED_FIREWALL_BREACH` | Auto-route to Compliance Director; complete halt; no auto-retry |
| Skill 2 score 70–84 | `HALTED_GATE_4_BELOW_THRESHOLD` | Generate revision request with failing section breakdown |
| Skill 2 score < 70 | `HALTED_GATE_4_INSUFFICIENT` | Escalate to Compliance Analyst; do not auto-retry |
| One approver approved at Gate 2 | `HALTED_APPROVAL_2_PARTIAL` | Conflict resolution meeting required; both approvers + Compliance Analyst |
| Approval Gate 2 rejected | `HALTED_APPROVAL_2_REJECTED` | Return to Skill 2 with reviewer notes; operator initiates revised run |
| Approval gate timed out | `APPROVAL_TIMED_OUT` | Notify Compliance Analyst; agent waits; does not auto-approve |

### Retry Policy

The agent auto-retries a skill execution exactly once on schema failure, with an augmented prompt that includes the specific validation error messages.

The agent **never** auto-retries on:
- Score failures — rubric failure analysis must be reviewed before re-execution
- Claims Firewall breaches — not re-runnable without Compliance Director sign-off
- Approval rejections — require operator initiation of a new run

### Partial Output Release

If the agent halts after Approval Gate 1 is passed but Skill 2 fails, the Skill 1 Regulatory Scoping Matrix is valid and may be released as a standalone document. An operator must explicitly request this partial release — the agent must not automatically release partial outputs.

---

## 11. Escalation Rules

### Automatic Escalations (No Human Authorisation Required)

| Condition | Target | Message |
|---|---|---|
| Claims Firewall breach in Skill 2 output | Compliance Director | Specific capability reference, canonical model entry, and the control that incorrectly referenced it |
| Unsupported jurisdiction in payload | Requesting team + Compliance Analyst | "Unsupported jurisdiction [{jurisdiction}]. Supported: EU, UK, India." |
| Either skill score < 55 | Compliance Analyst | Per-dimension breakdown attached |
| Ambiguous EU AI Act Annex III classification | General Counsel (via run log flag) | "Annex III classification for [{subject}] is ambiguous. Determining factors: [{factors}]. Legal review required." |

### Human-Authorised Escalations

| Condition | Target | Authorisation required |
|---|---|---|
| General Counsel disputes risk classification | Chief Compliance Officer | General Counsel formally escalates; written sign-off required |
| Mode B queue exceeds 3 affected subjects | Human operator | Operator authorises further queue processing |
| Approval gate timeout after 5 business days | Compliance Analyst | Analyst extends deadline or initiates revised run |
| Approval Gate 2 conflict | Both approvers + Compliance Analyst | Conflict resolution meeting; outcome recorded in run log |

---

## 12. Dependencies

### Skills

| Skill | Status | Location |
|---|---|---|
| regulatory-mapping | ✅ Available | `skills/regulatory-mapping/` |
| governance-control-mapping | ✅ Available | `skills/governance-control-mapping/` |

### Evaluation Infrastructure

| Component | Status | Location |
|---|---|---|
| `claims_linter.py` | ✅ Available (hardened 2026-06-18) | `evaluations/scripts/claims_linter.py` |
| `workflow_validator.py` | ✅ Available | `evaluations/scripts/workflow_validator.py` |
| `regression_tester.py` | ✅ Available | `evaluations/scripts/regression_tester.py` |
| `agent_certifier.py` | ✅ Available | `evaluations/scripts/agent_certifier.py` |
| RM structure baseline | ✅ Available | `evaluations/baselines/regulatory-mapping/structure.json` |
| GCM structure baseline | ✅ Available | `evaluations/baselines/governance-control-mapping/structure.json` |
| RM output schema | ✅ Available | `workflows/schemas/regulatory_mapping_output.json` |
| GCM output schema | ✅ Available | `workflows/schemas/control_mapping_output.json` |

### Knowledge Base

| Source | Status | Notes |
|---|---|---|
| `canonical-product-model.md` | ✅ Available | Sole authority for Ethana capability status |
| `knowledge/regulations/` | Verify before L4C | Must be current before production use |

### Test Infrastructure

| Fixture | Status | Notes |
|---|---|---|
| `eu-ai-act-high-risk-banking.md` (RM fixture) | ✅ Available | BFSI, EU+UK, ML classifier, Trigger 1 |
| `india-dpdp-customer-support-ai.md` (RM fixture) | ✅ Available | India NBFC, LLM, Trigger 1 |
| `uk-insurance-claims-model.md` (RM fixture) | ✅ Available | UK Insurance, ML classifier, Trigger 3 (regulatory change) |
| `eu-ai-act-high-risk-banking-gold-standard.md` | ✅ Available | Dual-skill (RM + GCM) gold standard |
| Minimal-risk internal tool fixture | ❌ Missing | Required for L4A complete coverage |

---

## 13. Implementation Roadmap

### Level 3 — Evaluation Certified (Current status: ✅ ACHIEVED)

All L3 conditions are met. The certifier confirms L3.

### Level 4A — Test Coverage (Not yet achieved)

| Requirement | Status | Notes |
|---|---|---|
| `regulatory-subjects/` contains ≥ 3 fixtures | ✅ Partially met | 3 fixtures exist; minimal-risk type missing |
| Minimal-risk internal tool fixture | ❌ Missing | Must be created before L4A can be declared complete |
| ≥ 1 GCM gold standard fixture | ✅ Met | EU AI Act gold standard (Part B) satisfies this |
| Regression tests pass for all RM fixtures | ✅ Run-ready | Execute: `python evaluations/scripts/regression_tester.py {fixture} evaluations/baselines/regulatory-mapping/structure.json` |
| Regression tests pass for all GCM gold standards | ✅ Run-ready | Execute: `python evaluations/scripts/regression_tester.py {fixture} evaluations/baselines/governance-control-mapping/structure.json` |
| Claims linter passes on all GCM gold standards | ✅ Run-ready | Execute: `python evaluations/scripts/claims_linter.py {fixture}` |

**L4A blocker:** Create `evaluations/test-cases/regulatory-subjects/minimal-risk-internal-tool.md` — a Trigger 1 fixture for a low-risk internal AI tool (e.g., internal document summariser with no personal data of external individuals), where the expected outcome is that EU AI Act High-Risk classification does NOT apply, OWASP LLM Top 10 is the primary framework, and the expected maturity level is L2.

### Level 4B — Agent Implementation (Not yet achieved)

Implementation files required (not to be created until L4A is complete):

| File | Purpose |
|---|---|
| `intake.py` | Input validation, traceability ID generation, subject classification |
| `orchestrator.py` | State machine: triggers skill executions, manages gate transitions |
| `gates.py` | Gate execution: calls `workflow_validator.py`, `claims_linter.py`, applies rubric scoring |
| `memory.py` | Assessment memory read/write |
| `escalations.py` | Escalation routing |
| `config.yaml` | Runtime configuration: timeouts, max concurrent Mode B runs, supported jurisdictions, score thresholds |

The `orchestrator.py` state machine must implement all state transitions in `state-machine.md` exactly. No implicit transitions.

### Level 4C — Production Readiness (Not yet achieved)

| Requirement | Notes |
|---|---|
| Dry-run against all 3 regulatory-subjects fixtures | Mode A; all gates must pass; run logs in `evaluations/scorecards/` |
| Mode B dry-run | Trigger 3 with `uk-insurance-claims-model` as known affected subject |
| Approval gate integration | Wired to real notification channels; no simulated approvals |
| Claims Firewall integration test | One deliberate GCM In Build reference must halt in `HALTED_FIREWALL_BREACH` |
| State persistence test | Survive process restart during `APPROVAL_1_PENDING` state |
| Certifier upgrade to L4 | `agent_certifier.py` confirms L4 |

---

## 14. Readiness Report

**Date:** 2026-06-18  
**Agent status:** Specification complete. Implementation blocked pending L4A completion.

### Blockers for L4A

| Blocker | Severity | Resolution |
|---|---|---|
| Missing minimal-risk internal tool test fixture | High | Create `evaluations/test-cases/regulatory-subjects/minimal-risk-internal-tool.md` with Trigger 1, no-EU-AI-Act-Annex-III, OWASP-primary expected outcomes |

### Discrepancies Requiring Resolution Before L4C

| Issue | Severity | Details |
|---|---|---|
| Claims Firewall escalation routing conflict | Medium | `regulatory-compliance-workflow.md` Section 9 routes breaches to "Sales Operations Lead"; `regulatory-watch-agent-architecture.md` Section 8.1 routes to "Compliance Director". The architecture is authoritative (more specific context). `regulatory-compliance-workflow.md` Section 9 must be updated to read "Compliance Director" before L4C. |
| Workflow.md does not reflect agent approval gate structure | Low | `regulatory-compliance-workflow.md` Section 8 correctly lists both approval gates; Section 9 escalation text is incomplete. Update Section 9 to add the Compliance Director (Claims Firewall) and Chief Compliance Officer (disputed risk classification) escalation paths. |

### Ready (No Blockers)

| Item | Status |
|---|---|
| Both upstream skills available | ✅ |
| All evaluation scripts available | ✅ |
| `claims_linter.py` hardened (2026-06-18) | ✅ |
| RM and GCM baselines available | ✅ |
| RM and GCM output schemas available | ✅ |
| 3 regulatory-subjects fixtures available | ✅ |
| EU AI Act dual-skill gold standard available | ✅ |
| `canonical-product-model.md` current | ✅ |
| State machine specification complete | ✅ (`state-machine.md`) |
| Evaluation gate specification complete | ✅ (`evaluation.md`) |
| Workflow YAML specification complete | ✅ (`workflow.yaml`) |

### Items to Verify Before L4C (Not Blockers Yet)

| Item | Verification command |
|---|---|
| `knowledge/regulations/` is current before production use | Manual audit; check last-updated dates against current regulatory calendar |
| Approval notification channels (email/Slack) are configured | Operational; requires implementation context |
| Assessment memory store (database/filesystem) is provisioned | Operational; requires infrastructure context |
