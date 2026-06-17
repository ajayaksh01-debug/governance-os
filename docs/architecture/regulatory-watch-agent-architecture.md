# Regulatory Watch Agent — Architecture

**Document type:** Architecture specification (no implementation code)  
**Agent:** Regulatory Watch Agent  
**Certifier level at architecture date:** L3 (certified)  
**Skill chain:** regulatory-mapping → governance-control-mapping  
**Workflow:** `workflows/regulatory-compliance-workflow.md` (Steps 4.1–4.2)  
**Status:** Ready for implementation

---

## 1. Agent Purpose

The Regulatory Watch Agent converts a description of an AI subject (a use case, deployed system, or AI portfolio) into a compliance and control package: a Regulatory Scoping Matrix produced by regulatory-mapping followed by an Operational Control Specification produced by governance-control-mapping.

The agent serves two distinct operational modes:

**Mode A — Assessment mode:** Triggered by a specific AI subject (new use case, jurisdictional expansion, or explicit compliance review request). The agent executes the full two-skill chain against the submitted subject and delivers a Compliance and Coverage Package to named approvers.

**Mode B — Watch mode:** Triggered by a regulatory change event (new enforcement guidance, updated regulation, or jurisdiction-specific rule change). The agent determines which previously-assessed AI subjects are affected by the change and queues re-assessment runs for each affected subject. Each re-assessment runs as a Mode A execution.

The boundary of the agent's certified skill chain is regulatory-mapping → governance-control-mapping. The third step of the regulatory-compliance-workflow (ethana-solution-mapping) is outside the current agent scope — its output is a structured hand-off that downstream agents or human practitioners consume. This boundary is a certification constraint, not a permanent design decision.

The agent is not an autonomous decision-maker. Every assessment run contains two mandatory human approval gates that prevent progression to the next skill until a named approver has reviewed and signed off. The agent orchestrates the skill sequence and enforces quality gates; humans approve the regulatory judgements.

---

## 2. Trigger Events

The agent responds to three trigger event types. All triggers must carry a `traceability_id` generated at intake. The traceability ID links all artifacts, approvals, escalations, and outputs for a single run.

### Trigger 1 — New AI Use Case Registration

**Source:** AI portfolio registry (CRM system, JIRA, or equivalent)  
**Signal:** A new AI use case reaches the "Compliance Review Required" lifecycle stage  
**Payload required:**
- `subject_description` — description of the AI use case, technology, data processed, affected individuals
- `subject_type` — `AI Use Case`
- `jurisdictions` — list of target jurisdictions (EU / UK / India)
- `industry` — sector vertical
- `target_maturity_level` — target control maturity (L1–L5)

**Agent response:** Single Mode A run against the submitted subject.

### Trigger 2 — Jurisdictional Expansion

**Source:** Project team or CRM system  
**Signal:** An existing AI system is proposed for deployment in a new jurisdiction  
**Payload required:**
- All fields from Trigger 1
- `existing_assessment_id` — reference to the prior regulatory mapping output for the base jurisdiction
- `new_jurisdiction` — the jurisdiction being added (EU / UK / India)

**Agent response:** Single Mode A run scoped to the incremental jurisdiction. The prior assessment is loaded as context but a new assessment is produced — not amended.

### Trigger 3 — Regulatory Change Alert

**Source:** Compliance team manual trigger or automated regulatory monitoring feed  
**Signal:** A material regulatory update has occurred (new enforcement guidance published, regulation amended, new supervisory circular issued)  
**Payload required:**
- `regulation_name` — the regulation that changed
- `jurisdiction` — affected jurisdiction
- `change_summary` — description of what changed and effective date
- `change_severity` — Critical (prohibited/mandatory changes), Major (new obligations), Minor (guidance update)

**Agent response (Mode B):**
1. Query the assessment memory for all prior regulatory-mapping outputs that include the affected regulation
2. For each affected prior assessment, generate a re-assessment job with the original `subject_description` plus the change summary as an addendum
3. Prioritise re-assessment jobs by: Critical change severity first, then by the AI subject's risk classification (Annex III high-risk first)
4. Execute Mode A runs sequentially for each queued re-assessment; do not batch them (each requires its own approval gates)

**Rate limit:** The agent must not initiate more than three concurrent re-assessment jobs from a single regulatory change alert. If more than three subjects are affected, the remaining subjects are queued and notified; a human operator authorises queue processing.

---

## 3. Inputs

### 3.1 Required Inputs (all trigger types)

| Field | Type | Validation rule |
|---|---|---|
| `traceability_id` | string | Auto-generated at intake; format `TR-RW-{YYYY}-{NNNN}` |
| `trigger_type` | enum | `new_use_case_registration` / `jurisdictional_expansion` / `regulatory_change_alert` |
| `subject_description` | string | Minimum 50 characters; must identify AI technology type, data processed, affected individuals, and deployment location |
| `subject_type` | enum | `AI Use Case` / `AI System` / `AI Portfolio` |
| `jurisdictions` | array of enum | One or more of: `EU`, `UK`, `India` |
| `target_maturity_level` | enum | `L1` through `L5` |

### 3.2 Optional Inputs

| Field | Type | Effect on execution |
|---|---|---|
| `industry` | string | Activates BFSI overlay in regulatory-mapping Phase 1.3; loads sector-specific baselines |
| `data_types` | array | Affects GDPR / DPDP Act applicability determination |
| `deployment_model` | enum | `Cloud SaaS` / `VPC` / `On-premises`; affects control design choices in governance-control-mapping |
| `existing_tooling` | array | Surfaced to governance-control-mapping Phase 1.2 for third-party integration design |
| `existing_assessment_id` | string | Required for Trigger 2; loads prior output as incremental context |

### 3.3 Input Validation

Before the agent executes any skill, the intake sub-component validates the payload against the following rules:

1. All required fields are present and non-empty
2. `jurisdictions` contains only supported values (EU / UK / India); unsupported jurisdictions trigger an immediate escalation (see Section 12)
3. `subject_description` is classified as `Low`, `Medium`, or `High` evidence quality using regulatory-mapping Phase 1.4 criteria; `Low` quality triggers a warning but does not block execution
4. For Trigger 2, `existing_assessment_id` references a valid prior output in assessment memory
5. For Trigger 3, `change_severity` is one of the three valid values; if the payload has `change_severity = Critical` and the affected regulation is in scope for three or more prior assessments, human operator confirmation is required before Mode B queue processing begins

Intake validation failure halts the agent at the intake stage and returns an error payload before any skill is executed.

---

## 4. Outputs

The agent produces three output artifacts per completed run.

### 4.1 Regulatory Scoping Matrix

Produced by the regulatory-mapping skill execution. Structured as:
- The full 9-section markdown document (Applicable Regulations, Frameworks, Obligations, Risk Classification, Documentation, Controls, Audit Evidence, BFSI Considerations, Executive Summary)
- The machine-readable JSON payload validated against `workflows/schemas/regulatory_mapping_output.json`
- Assessment score (minimum 70/100 for release)
- Evidence quality rating (High / Medium / Low)

This artifact is produced after Step 1 (regulatory-mapping) and must be approved by General Counsel before the agent proceeds to Step 2.

### 4.2 Operational Control Specification

Produced by the governance-control-mapping skill execution. Structured as:
- The full 10-section markdown document (Executive Summary, Taxonomy Matrix, Coverage Classification, Preventive Controls, Detective Controls, Corrective Controls, Evidence Registry, RACI Matrix, Maturity Roadmap, Ethana Configuration Guide)
- The machine-readable JSON payload validated against `workflows/schemas/control_mapping_output.json`
- Assessment score (minimum 85/100 for release)
- Claims Firewall compliance status (pass / breach — breach auto-blocks release)
- RACI matrix with named role assignments

This artifact is produced after Step 2 (governance-control-mapping) and must be approved by DPO and Information Security Lead before the agent delivers the final package.

### 4.3 Compliance and Coverage Package

The combined deliverable: a structured ZIP or folder containing:
- `{traceability_id}-regulatory-scoping-matrix.md` — Section 4.1 markdown document
- `{traceability_id}-operational-control-spec.md` — Section 4.2 markdown document
- `{traceability_id}-regulatory-mapping-payload.json` — Section 4.1 machine-readable output
- `{traceability_id}-control-mapping-payload.json` — Section 4.2 machine-readable output
- `{traceability_id}-run-log.json` — Agent execution log: trigger event, timestamps, approval decisions, gate scores, escalation events
- `{traceability_id}-handoff-note.md` — Structured handoff note for the ethana-solution-mapping downstream step, containing: the control_mapping_output.json path, the jurisdiction set, the sector, and any Ethana capability references from Section 10 that require validation before a proposal can be prepared

### 4.4 Handoff Contract to Downstream

The Compliance and Coverage Package is the upstream input for two downstream consumers:

| Downstream consumer | Consumes | Via |
|---|---|---|
| Human practitioner (solution mapping) | `control-mapping-payload.json` → ethana-solution-mapping | Manual step; not in agent scope |
| Client Assessment Agent | `regulatory-mapping-payload.json` + `control-mapping-payload.json` | Automated hand-off when Client Assessment Agent is built |

The agent must produce the JSON payloads in schema-valid format regardless of whether downstream consumers are automated agents or human practitioners.

---

## 5. Skill Orchestration Sequence

The agent executes two skills in strict sequence. Skill 2 does not begin until Skill 1 is complete and approved.

```
[Trigger Event Received]
          │
          ▼
[Intake: Validate Inputs]
          │
   ┌──────┴────────┐
   │ Validation    │
   │ failure?      │
   └──────┬────────┘
          │ No
          ▼
[SKILL 1: regulatory-mapping]
          │
          ├── Phase 1: Intake and Subject Classification
          │     (7-step protocol per skills/regulatory-mapping/workflow.md)
          ├── Phase 2: Regulation Scanning
          │     (EU, UK, India decision trees)
          ├── Phase 3: Framework Mapping
          │     (ISO 42001 clauses, NIST AI RMF functions, OWASP LLM Top 10)
          ├── Phase 4: Risk Classification
          │     (EU AI Act tier, UK PRA model tier, India DPDP/RBI/SEBI)
          ├── Phase 5: Obligation and Requirements Extraction
          │     (obligations, documentation, controls, audit evidence)
          ├── Phase 6: BFSI Analysis (if applicable)
          └── Phase 7: Output Production
                │
                ▼
[Schema validation: regulatory_mapping_output.json]
[Score evaluation: ≥ 70/100 required]
[Structural regression: regulatory-mapping/structure.json]
          │
   ┌──────┴────────────────────┐
   │ Gate failure or score     │
   │ < 70?                     │
   └──────┬────────────────────┘
          │ No
          ▼
[APPROVAL GATE 1: General Counsel]
     (see Section 9)
          │
          ▼
[SKILL 2: governance-control-mapping]
    Input: Section 6 (Control Requirements) from Skill 1 output
           + full agent context (jurisdictions, sector, target maturity,
             deployment model, existing tooling)
          │
          ├── Phase 1: Intake and Baseline Calibration
          ├── Phase 2: Risk and Trigger Extraction
          ├── Phase 3: Control Strategy Formulation
          ├── Phase 4: Control Coverage Classification
          ├── Phase 5: Platform Status Audit (Claims Firewall Gate)
          │     → consult canonical-product-model.md for every Ethana reference
          ├── Phase 6: Ownership and Evidence Assignment
          └── Phase 7: Maturity Phasing and Quality Gates
                │
                ▼
[Schema validation: control_mapping_output.json]
[Score evaluation: ≥ 85/100 required]
[Claims Firewall check: claims_linter.py]
[Structural regression: governance-control-mapping/structure.json]
          │
   ┌──────┴────────────────────┐
   │ Gate failure, score < 85, │
   │ or Firewall breach?       │
   └──────┬────────────────────┘
          │ No
          ▼
[APPROVAL GATE 2: DPO + Information Security Lead]
     (see Section 9)
          │
          ▼
[Assemble Compliance and Coverage Package]
[Deliver + update assessment memory]
[Generate handoff note for downstream]
          │
          ▼
[COMPLETE]
```

### 5.1 Inter-Skill Payload

The payload passed from Skill 1 to Skill 2 is not only Section 6 of the regulatory-mapping output — the governance-control-mapping skill needs full context to calibrate control severity and BFSI overlays. The inter-skill payload is:

```json
{
  "upstream_source_type": "Regulatory Mapping",
  "traceability_id": "TR-RW-2026-XXXX",
  "upstream_payload": "{full regulatory_mapping_output JSON}",
  "target_maturity_level": "L4",
  "jurisdictions": ["EU", "UK"],
  "client_sector": "BFSI",
  "deployment_model": "Cloud SaaS",
  "existing_tooling": ["Splunk", "Zscaler"]
}
```

The `upstream_payload` field carries the full `regulatory_mapping_output.json` object, not just Section 6. The governance-control-mapping Phase 1.1 validation step requires Section 6 to be present and non-empty; the agent must verify this before handing off.

---

## 6. Workflow Integration

### 6.1 Workflow Coverage

The agent executes Steps 4.1 and 4.2 of `workflows/regulatory-compliance-workflow.md`:
- Step 4.1 → regulatory-mapping
- Step 4.2 → governance-control-mapping

Step 4.3 (ethana-solution-mapping) is a documented downstream handoff. The agent produces the inputs required for Step 4.3 but does not execute it. The `{traceability_id}-handoff-note.md` output artifact contains the structured context required for a human practitioner or a downstream agent to execute Step 4.3.

### 6.2 Workflow Scope Boundary

The agent does not produce a Coverage Confidence Score (CCS) or Ethana capability mapping — those are produced by ethana-solution-mapping. If a practitioner requests CCS as part of an assessment, they must initiate a separate ethana-solution-mapping execution using the control-mapping-payload.json as input. This is a design constraint, not an error; the CCS requires ethana-solution-mapping to have a certified evaluation baseline before it can be included in an automated agent chain.

### 6.3 Interaction with the Incident Intelligence Agent

The Regulatory Watch Agent and the Incident Intelligence Agent share the governance-control-mapping skill. When an AI incident occurs, the Incident Intelligence Agent executes ai-incident-analysis → governance-control-mapping on the incident context, then may escalate control failures to the Regulatory Watch Agent's governance-assessment workflow for a full re-mapping. The hand-off from Incident Intelligence to Regulatory Watch is:
- The incident's governance-control-mapping output is appended to the Regulatory Watch trigger payload as an addendum
- The Regulatory Watch Agent treats it as a Trigger 1 (New Use Case Registration) with `subject_type = AI Incident`
- The prior control assessment from the incident context is loaded in Phase 1.1 of governance-control-mapping as baseline context

### 6.4 Interaction with the Client Assessment Agent

The Client Assessment Agent (when built) will consume the Regulatory Watch Agent's outputs as one of four upstream skill inputs. The integration point is:
- `regulatory-mapping-payload.json` → Client Assessment Agent's regulatory-mapping step
- `control-mapping-payload.json` → Client Assessment Agent's governance-control-mapping step

When the Client Assessment Agent is operational, the Regulatory Watch Agent must be configured to store its output payloads in a location accessible to the Client Assessment Agent's input loader.

---

## 7. Evaluation Gates

The agent enforces four automated evaluation gates. No gate may be bypassed or overridden by a human operator (except the Claims Firewall disposition which must be reviewed by the Compliance Director, not bypassed).

### Gate 1 — Regulatory Mapping Schema Validation

**Tool:** `workflow_validator.py`  
**Schema:** `workflows/schemas/regulatory_mapping_output.json`  
**Timing:** Immediately after Skill 1 execution completes  
**Pass condition:** Zero schema validation errors  
**Fail action:** Agent halts at Gate 1. Skill 1 output is flagged as schema-invalid. The skill is re-run with a revised prompt or the run is escalated to the Compliance Analyst. The agent does not proceed to Approval Gate 1.

```bash
python evaluations/scripts/workflow_validator.py \
  {traceability_id}-regulatory-mapping-payload.json \
  workflows/schemas/regulatory_mapping_output.json
```

### Gate 2 — Regulatory Mapping Quality Score

**Tool:** Evaluation rubric (evaluation.md Sections 1–9)  
**Pass threshold:** 70/100  
**Timing:** After Gate 1 passes  
**Pass condition:** Total score ≥ 70  
**Fail action:** Agent halts. If score is 55–69, the output is reclassified as Preliminary and a revision request is generated. If score is < 55, the run is escalated to the Compliance Analyst with the specific failing dimensions identified.

The gate score must be computed per the rubric — not approximated. The agent must apply the 9-dimension scoring matrix and store the per-dimension breakdown in the run log.

### Gate 3 — Control Mapping Schema Validation + Claims Firewall

**Tool 1:** `workflow_validator.py`  
**Schema:** `workflows/schemas/control_mapping_output.json`  
**Tool 2:** `claims_linter.py`  
**Timing:** Immediately after Skill 2 execution completes  
**Pass condition (Gate 3a):** Zero schema validation errors  
**Pass condition (Gate 3b):** Zero Claims Firewall violations  
**Fail action (Gate 3a):** Agent halts; Skill 2 output is schema-invalid; re-run or escalate  
**Fail action (Gate 3b):** Agent halts immediately with `HALTED_FIREWALL_BREACH` state; the specific In Build or Aspirational capability reference is identified; the run is auto-routed to the Compliance Director. This gate cannot be bypassed under any circumstance.

```bash
python evaluations/scripts/workflow_validator.py \
  {traceability_id}-control-mapping-payload.json \
  workflows/schemas/control_mapping_output.json

python evaluations/scripts/claims_linter.py \
  {traceability_id}-operational-control-spec.md
```

### Gate 4 — Control Mapping Quality Score

**Tool:** Evaluation rubric (governance-control-mapping evaluation.md)  
**Pass threshold:** 85/100  
**Timing:** After Gate 3 passes  
**Pass condition:** Total score ≥ 85  
**Fail action:** Agent halts. If score is 70–84, a revision request is generated with the specific failing sections. If score is < 70, the run is escalated to the Compliance Analyst.

### Gate Summary

| Gate | Tool | Threshold | Fail action |
|---|---|---|---|
| Gate 1 — RM Schema | workflow_validator.py | 0 errors | Halt; re-run or escalate |
| Gate 2 — RM Score | evaluation rubric | ≥ 70/100 | Halt; revise if 55–69; escalate if < 55 |
| Gate 3a — GCM Schema | workflow_validator.py | 0 errors | Halt; re-run or escalate |
| Gate 3b — Claims Firewall | claims_linter.py | 0 violations | Auto-halt; route to Compliance Director |
| Gate 4 — GCM Score | evaluation rubric | ≥ 85/100 | Halt; revise if 70–84; escalate if < 70 |

---

## 8. Failure Handling

### 8.1 Failure Classifications

| Failure type | Agent state | Recovery path |
|---|---|---|
| Input validation failure | `HALTED_INTAKE_INVALID` | Return error payload; operator corrects inputs and re-submits |
| Skill 1 schema failure | `HALTED_GATE_1_SCHEMA` | Agent re-runs Skill 1 with augmented prompt; if second attempt fails, escalate to Compliance Analyst |
| Skill 1 score below 55 | `HALTED_GATE_2_INSUFFICIENT` | Escalate to Compliance Analyst for reassignment; do not auto-retry |
| Skill 1 score 55–69 | `HALTED_GATE_2_PRELIMINARY` | Reclassify output as Preliminary; generate revision request with failing dimension breakdown; operator reviews before re-run |
| Approval 1 rejected | `HALTED_APPROVAL_1_REJECTED` | Return to Skill 1 with reviewer notes; the agent does not auto-retry; operator initiates revised run |
| Skill 2 schema failure | `HALTED_GATE_3A_SCHEMA` | Agent re-runs Skill 2 with augmented prompt; if second attempt fails, escalate |
| Claims Firewall breach | `HALTED_FIREWALL_BREACH` | Auto-route to Compliance Director; do not revise the output; flag the specific capability reference; complete halt |
| Skill 2 score below 70 | `HALTED_GATE_4_INSUFFICIENT` | Escalate to Compliance Analyst; do not auto-retry |
| Skill 2 score 70–84 | `HALTED_GATE_4_BELOW_THRESHOLD` | Generate revision request with failing section breakdown; operator reviews before re-run |
| Approval 2 rejected | `HALTED_APPROVAL_2_REJECTED` | Return to Skill 2 with reviewer notes; operator initiates revised run |
| Jurisdiction unsupported | `HALTED_INTAKE_UNSUPPORTED_JURISDICTION` | Immediate escalation; agent cannot execute for unsupported jurisdictions (US, Canada, Australia, etc.) |

### 8.2 Retry Policy

The agent auto-retries a skill execution exactly once on schema failure. The retry must use an augmented prompt that includes the specific validation error messages. If the retry fails, the agent halts and does not continue retrying — automated retry loops without analyst review produce progressively worse outputs.

The agent never auto-retries on:
- Score failures (the rubric failure analysis must be reviewed before re-execution)
- Claims Firewall breaches (these are not re-runnable without Compliance Director sign-off)
- Approval rejections (these require operator initiation of a new run)

### 8.3 Partial Output Handling

If the agent halts after Approval Gate 1 (i.e., Skill 1 is approved but Skill 2 fails), the Skill 1 output is valid and may be released as a standalone Regulatory Scoping Matrix. The agent must not automatically release partial outputs — an operator must explicitly request the partial release.

### 8.4 Timeout Handling

Human approval gates have a configurable timeout period (default: 5 business days). If an approval gate times out:
- The agent transitions to `APPROVAL_TIMED_OUT` state
- The Compliance Analyst is notified
- The agent does not auto-approve or auto-escalate the work; it waits for a human to either approve or reject

---

## 9. Human Approval Points

### Approval Point 1 — Regulatory Scoping Matrix Review

**Approver:** General Counsel (or designated Legal Representative)  
**Triggered after:** Skill 1 complete + Gates 1 and 2 passed  
**Payload presented to approver:**
- `{traceability_id}-regulatory-scoping-matrix.md` — full 9-section document
- Per-dimension score breakdown from Gate 2
- Evidence quality rating (High / Medium / Low)
- Any conditional applicability flags requiring legal judgement
- Any ambiguous risk classifications with determining factors

**Approval actions:**
- `Approve` — agent proceeds to Skill 2
- `Approve with notes` — agent proceeds to Skill 2 with the approver's notes attached to the run log and included in the inter-skill payload context
- `Reject with revision request` — agent halts; operator reviews notes; revised run initiated

**What approval authorises:** The Regulatory Scoping Matrix is accurate as a statement of regulatory applicability and obligation scope. The risk classifications are legally defensible. This approval does not authorise the control design (Approval Point 2 covers that).

**What approval does not authorise:** The General Counsel's approval of the regulatory mapping is not a legal opinion and does not constitute legal advice. The run log must record this explicitly.

### Approval Point 2 — Operational Control Specification and RACI Review

**Approvers:** DPO + Information Security Lead (joint sign-off required from both)  
**Triggered after:** Skill 2 complete + Gates 3 and 4 passed  
**Payload presented to approvers:**
- `{traceability_id}-operational-control-spec.md` — full 10-section document
- Per-section score breakdown from Gate 4
- Claims Firewall compliance status (confirmed pass)
- RACI matrix with named role assignments for their review
- Section 10 Ethana Configuration Guide with all In Build capabilities flagged as roadmap items

**Approval actions:**
- `Approve` — agent assembles the Compliance and Coverage Package and delivers it
- `Approve with modifications` — approver may modify RACI role assignments or add caveats to specific controls; agent incorporates modifications and re-runs Gates 3 and 4 before final delivery
- `Reject with revision request` — agent halts; operator reviews notes; revised run initiated

**What joint approval authorises:** The control specifications are implementable given the organisation's current security posture and team structure. The RACI assignments are accepted by the named role owners. The maturity roadmap timeline is realistic.

**Joint sign-off requirement:** Both the DPO and the Information Security Lead must approve. A single approval does not unblock the agent. If one approver approves and the other rejects, the agent halts in `HALTED_APPROVAL_2_PARTIAL` state and generates a conflict resolution request.

---

## 10. Runtime State Model

The agent's state must be persisted to durable storage after every transition. Approval gate states may last multiple business days; in-memory state is not sufficient.

### 10.1 State Definitions

```
INTAKE_VALIDATING          → Parsing and validating trigger payload
INTAKE_COMPLETE            → Payload valid; traceability ID assigned
SKILL_1_RUNNING            → regulatory-mapping executing
SKILL_1_COMPLETE           → Skill 1 output ready; schema and score gates pending
GATE_1_PASSED              → Schema valid
GATE_2_PASSED              → Score ≥ 70
APPROVAL_1_PENDING         → Awaiting General Counsel sign-off
APPROVAL_1_APPROVED        → General Counsel approved; proceeding to Skill 2
SKILL_2_RUNNING            → governance-control-mapping executing
SKILL_2_COMPLETE           → Skill 2 output ready; schema, firewall, and score gates pending
GATE_3_PASSED              → Schema valid and Claims Firewall clean
GATE_4_PASSED              → Score ≥ 85
APPROVAL_2_PENDING         → Awaiting DPO + InfoSec Lead sign-off
APPROVAL_2_APPROVED        → Both approvers signed off; assembling final package
COMPLETE                   → Compliance and Coverage Package delivered

HALTED_INTAKE_INVALID                → Input validation failed
HALTED_INTAKE_UNSUPPORTED_JURISDICTION → Unsupported jurisdiction in scope
HALTED_GATE_1_SCHEMA                 → Skill 1 schema invalid (after retry)
HALTED_GATE_2_PRELIMINARY            → Skill 1 score 55–69; revision pending
HALTED_GATE_2_INSUFFICIENT           → Skill 1 score < 55; analyst escalation
HALTED_APPROVAL_1_REJECTED           → General Counsel rejected; revision pending
HALTED_GATE_3A_SCHEMA                → Skill 2 schema invalid (after retry)
HALTED_FIREWALL_BREACH               → Claims Firewall violation; Compliance Director notified
HALTED_GATE_4_BELOW_THRESHOLD        → Skill 2 score 70–84; revision pending
HALTED_GATE_4_INSUFFICIENT           → Skill 2 score < 70; analyst escalation
HALTED_APPROVAL_2_PARTIAL            → One approver approved; conflict resolution pending
HALTED_APPROVAL_2_REJECTED           → Both/one approver(s) rejected; revision pending
HALTED_ESCALATION                    → External resolution required; awaiting response
APPROVAL_TIMED_OUT                   → Approval gate timeout; analyst notified
```

### 10.2 Valid State Transitions

```
INTAKE_VALIDATING → INTAKE_COMPLETE | HALTED_INTAKE_INVALID | HALTED_INTAKE_UNSUPPORTED_JURISDICTION

INTAKE_COMPLETE → SKILL_1_RUNNING

SKILL_1_RUNNING → SKILL_1_COMPLETE | HALTED_ESCALATION

SKILL_1_COMPLETE → GATE_1_PASSED | HALTED_GATE_1_SCHEMA

GATE_1_PASSED → GATE_2_PASSED | HALTED_GATE_2_PRELIMINARY | HALTED_GATE_2_INSUFFICIENT

GATE_2_PASSED → APPROVAL_1_PENDING

APPROVAL_1_PENDING → APPROVAL_1_APPROVED | HALTED_APPROVAL_1_REJECTED | APPROVAL_TIMED_OUT

APPROVAL_1_APPROVED → SKILL_2_RUNNING

SKILL_2_RUNNING → SKILL_2_COMPLETE | HALTED_ESCALATION

SKILL_2_COMPLETE → GATE_3_PASSED | HALTED_GATE_3A_SCHEMA | HALTED_FIREWALL_BREACH

GATE_3_PASSED → GATE_4_PASSED | HALTED_GATE_4_BELOW_THRESHOLD | HALTED_GATE_4_INSUFFICIENT

GATE_4_PASSED → APPROVAL_2_PENDING

APPROVAL_2_PENDING → APPROVAL_2_APPROVED | HALTED_APPROVAL_2_REJECTED | HALTED_APPROVAL_2_PARTIAL | APPROVAL_TIMED_OUT

APPROVAL_2_APPROVED → COMPLETE
```

### 10.3 State Persistence Requirements

Each state transition must persist:
- The new state value
- The timestamp of the transition
- The trigger that caused the transition (gate result, approval action, error message)
- The identity of any human actor who caused the transition (approval actions)

The run log in the final output package is constructed from the persisted state transition history.

---

## 11. Memory Requirements

The agent requires three distinct memory tiers.

### 11.1 Run-Scoped Memory (Required)

Memory that exists for the duration of a single run and is discarded after the Compliance and Coverage Package is delivered (or the run is permanently halted).

| Data | Format | Required for |
|---|---|---|
| Trigger event payload | JSON | Skill 1 input construction |
| Run state | enum + timestamp | State persistence |
| Skill 1 output (markdown) | Markdown document | Approval Gate 1 delivery |
| Skill 1 output (JSON) | JSON object | Gate 1 schema validation; inter-skill payload |
| Skill 1 gate scores | JSON (per-dimension) | Gate 2 evaluation; run log |
| Approval 1 decision + notes | JSON | Run log; Skill 2 context |
| Skill 2 output (markdown) | Markdown document | Approval Gate 2 delivery |
| Skill 2 output (JSON) | JSON object | Gate 3 schema validation; final package |
| Skill 2 gate scores | JSON (per-dimension) | Gate 4 evaluation; run log |
| Claims Firewall report | JSON | Gate 3 validation; run log |
| Approval 2 decision + notes | JSON | Run log; final package |

Run-scoped memory must survive system restarts if approval gates are open. The agent cannot rely on in-process memory for states that require human approval.

### 11.2 Assessment Memory (Required)

Persistent memory indexed by `traceability_id`. Maintained across runs. Used by Mode B (Regulatory Change Alert) to identify affected prior assessments.

| Data | Retention | Indexed by |
|---|---|---|
| All regulatory-mapping outputs (JSON) | Indefinite until superseded | `traceability_id`, `subject_description`, `jurisdictions`, `regulations_applicable` |
| All control-mapping outputs (JSON) | Indefinite until superseded | `traceability_id`, skill 1 traceability ID |
| Assessment status (complete / preliminary / superseded) | Indefinite | `traceability_id` |
| Subject fingerprint | Indefinite | `subject_type` + `jurisdictions` + `industry` hash |

Assessment memory enables:
- Mode B re-assessment identification (which prior assessments reference the changed regulation?)
- Deduplication (has this exact subject been assessed before in these jurisdictions?)
- Audit trail (what was the regulatory mapping for this AI system at a given date?)

### 11.3 Regulatory Calendar Memory (Required for Mode B)

A structured record of regulatory changes that have been processed as Trigger 3 events. Used to prevent duplicate re-assessment queues for the same regulatory change.

| Data | Retention | Format |
|---|---|---|
| Regulation name + change description | 3 years | String |
| Effective date | 3 years | ISO 8601 date |
| Agent change severity classification | 3 years | Critical / Major / Minor |
| Number of affected assessments queued | 3 years | Integer |
| Queue processing status | 3 years | Queued / In progress / Complete |

### 11.4 What the Agent Does Not Retain

The agent must not retain:
- Personally identifiable information beyond what is minimally required to identify the AI subject
- Client confidential data beyond what the trigger payload contained
- Approval decision reasoning beyond what the approver explicitly records
- Interim Skill outputs that did not pass quality gates (these are discarded, not stored)

---

## 12. Escalation Rules

### 12.1 Automatic Escalations (No Human Authorisation Required)

| Condition | Escalation target | Message |
|---|---|---|
| Claims Firewall breach in Skill 2 output | Compliance Director | Auto-routed with the specific capability reference, the canonical model entry, and the control that incorrectly referenced it |
| Input payload contains unsupported jurisdiction | Requesting team + Compliance Analyst | "Unsupported jurisdiction [{jurisdiction}] in scope. Regulatory mapping coverage does not include this jurisdiction. Assessment halted." |
| Skill score < 55 (either skill) | Compliance Analyst | Assessment insufficient — per-dimension breakdown attached |
| Ambiguous EU AI Act Annex III classification detected | General Counsel via run log flag | "Annex III classification for [{subject}] is ambiguous. Determining factors: [{factors}]. Legal review required before finalising Section 4." |

### 12.2 Human-Authorised Escalations

| Condition | Escalation target | Human must authorise |
|---|---|---|
| Legal counsel disputes risk classification (Section 4 of Skill 1) | Chief Compliance Officer | General Counsel formally escalates; the Chief Compliance Officer provides written sign-off |
| Mode B re-assessment queue exceeds three affected subjects | Human operator | Operator authorises further queue processing before the agent continues |
| Approval gate timeout after 5 business days | Compliance Analyst | Analyst either extends the deadline or initiates a revised run |
| Approval 2 conflict (one approver approves, one rejects) | Both approvers + Compliance Analyst | Conflict resolution meeting required; outcome recorded in run log |

### 12.3 Jurisdiction Escalation

The agent's knowledge base covers EU, UK, and India. If a trigger payload specifies a jurisdiction outside these three:
- The agent halts immediately with `HALTED_INTAKE_UNSUPPORTED_JURISDICTION`
- The requesting team is notified with a list of supported jurisdictions
- The Compliance Analyst is notified to assess whether the jurisdiction requires a bespoke knowledge base extension
- The agent does not attempt to extrapolate from supported jurisdictions to unsupported ones

### 12.4 Capability Validation Escalation

If Skill 2 (governance-control-mapping) references an Ethana capability in Section 10 that has not been validated by the ethana-capability-validation skill, the agent flags this in the run log and in the handoff note. This is not a blocking escalation — it is an advisory to the downstream practitioner or Client Assessment Agent that the capability's status in the control design should be confirmed by capability validation before the control design is included in a client proposal.

---

## 13. Success Metrics

Metrics are measured per completed run (state = `COMPLETE`) and reported in the run log.

### 13.1 Quality Metrics

| Metric | Target | Measurement |
|---|---|---|
| Regulatory Mapping score | ≥ 80/100 (aspirational) | Gate 2 rubric score per run |
| Control Mapping score | ≥ 90/100 (aspirational) | Gate 4 rubric score per run |
| Claims Firewall compliance rate | 100% | Zero breaches across all runs |
| Schema validation pass rate | 100% | Zero schema errors at first attempt (no retry required) |
| Runs requiring Schema retry | < 5% | Fraction of runs where a schema retry was needed |

### 13.2 Throughput Metrics

| Metric | Target | Measurement |
|---|---|---|
| Assessment Mode A execution time (single jurisdiction) | ≤ 90 minutes (Skill 1) + ≤ 90 minutes (Skill 2) | Timestamp delta: `SKILL_N_RUNNING` → `SKILL_N_COMPLETE` |
| Assessment Mode A execution time (multi-jurisdiction) | ≤ 150 minutes (Skill 1) + ≤ 120 minutes (Skill 2) | Same |
| Approval Gate 1 turnaround time | ≤ 2 business days | Timestamp delta: `APPROVAL_1_PENDING` → `APPROVAL_1_APPROVED` |
| Approval Gate 2 turnaround time | ≤ 3 business days | Timestamp delta: `APPROVAL_2_PENDING` → `APPROVAL_2_APPROVED` |
| End-to-end cycle time (trigger to complete) | ≤ 7 business days | Timestamp delta: `INTAKE_COMPLETE` → `COMPLETE` |

### 13.3 Effectiveness Metrics

| Metric | Target | Measurement method |
|---|---|---|
| Compliance Coverage Rate | 100% of applicable obligations mapped to active controls | Human reviewer audit of Section 6 (Skill 1) vs. Section 4 (Skill 2) |
| Regulatory citation accuracy | 100% of obligations cite specific legal provisions | Reviewer verification: no obligation stated as "comply with [regulation]" without specific Article or Section reference |
| Audit Readiness Index | 100% of controls have defined evidence collection mechanisms | Section 7 completeness check: every control in Section 2 has a matching entry in Section 7 |
| RACI completeness | Zero orphan controls | Every control in Section 2 has exactly one Accountable role in Section 8 |

### 13.4 Mode B Watch Metrics

| Metric | Target | Measurement |
|---|---|---|
| Regulatory change to first re-assessment triggered | ≤ 1 business day | Timestamp delta: Trigger 3 receipt → first Mode A run initiated |
| Re-assessment queue completion (Critical severity) | ≤ 5 business days | Timestamp delta: Trigger 3 receipt → all Critical re-assessments complete |
| Re-assessment coverage rate | ≥ 95% of affected assessments identified | Manual audit: did the agent identify all prior assessments referencing the changed regulation? |

---

## 14. Agent Certification Criteria

The agent is certified for production use when it meets all criteria across the following four levels.

### Level 3 — Evaluation Certified (Current status: ACHIEVED)

The certifier (`agent_certifier.py`) confirms L3. Required conditions:
- [x] `skills/regulatory-mapping/SKILL.md` exists
- [x] `skills/governance-control-mapping/SKILL.md` exists
- [x] `workflows/regulatory-compliance-workflow.md` exists
- [x] `evaluations/baselines/regulatory-mapping/structure.json` exists
- [x] `evaluations/baselines/governance-control-mapping/structure.json` exists

### Level 4A — Test Coverage (Not yet achieved)

Before agent code is written, the following test infrastructure must be complete:

| Requirement | Status | Notes |
|---|---|---|
| `evaluations/test-cases/regulatory-subjects/` contains ≥ 3 fixtures | ❌ Missing | Required fixtures: BFSI multi-jurisdiction, minimal-risk internal tool, regulatory-change-trigger re-assessment |
| `evaluations/test-cases/gold-standards/` contains ≥ 1 GCM fixture | ❌ Missing | Required: control mapping output for at least one known-good assessment |
| Regression tests pass for all regulatory-mapping fixtures | ❌ Cannot run (no fixtures) | Command: `python evaluations/scripts/regression_tester.py {fixture} evaluations/baselines/regulatory-mapping/structure.json` |
| Regression tests pass for all GCM fixtures | ❌ Cannot run (no fixtures) | Command: `python evaluations/scripts/regression_tester.py {fixture} evaluations/baselines/governance-control-mapping/structure.json` |
| Claims linter passes on all GCM fixtures | ❌ Cannot run (no fixtures) | Command: `python evaluations/scripts/claims_linter.py {fixture}` |

### Level 4B — Agent Implementation (Not yet achieved)

Code requirements for the agent directory (when created):

| Requirement | Description |
|---|---|
| `agents/regulatory-watch-agent/README.md` | Agent overview: purpose, trigger events, dependencies, how to run |
| `agents/regulatory-watch-agent/intake.py` | Input validation, traceability ID generation, subject classification |
| `agents/regulatory-watch-agent/orchestrator.py` | State machine: triggers skill executions, manages gate transitions, handles human approval gate states |
| `agents/regulatory-watch-agent/gates.py` | Gate execution: calls `workflow_validator.py`, `claims_linter.py`, applies evaluation rubric scoring |
| `agents/regulatory-watch-agent/memory.py` | Assessment memory read/write: stores and queries prior regulatory-mapping outputs |
| `agents/regulatory-watch-agent/escalations.py` | Escalation routing: Maps conditions to escalation targets and formats escalation messages |
| `agents/regulatory-watch-agent/config.yaml` | Runtime configuration: approval timeout periods, max concurrent Mode B runs, supported jurisdictions list, score thresholds |

The `orchestrator.py` state machine must implement all state transitions defined in Section 10.2 exactly. No implicit state transitions are permitted — every transition must be an explicit recorded operation.

### Level 4C — Production Readiness (Not yet achieved)

Before the agent is used in client-facing workflows:

| Requirement | Description |
|---|---|
| Dry-run against all 3 test fixtures | Mode A run against each fixture; all gates must pass; run logs stored in `evaluations/scorecards/` |
| Mode B dry-run | Trigger 3 event simulated with a known-affected prior assessment; re-assessment queue correctly populated |
| Approval gate integration | Both human approval gates must be wired to actual notification channels (email, Slack, or equivalent); the agent must not simulate approvals in any configuration |
| Claims Firewall integration test | At least one test run must deliberately include an In Build capability reference in the GCM output; the agent must halt in `HALTED_FIREWALL_BREACH` state and correctly route to Compliance Director |
| State persistence test | The agent must survive a process restart during `APPROVAL_1_PENDING` state and resume correctly without data loss |
| Certifier upgrade to L4 | `agents/regulatory-watch-agent/` directory exists with at least one implementation file; `agent_certifier.py` confirms L4 |

### Certification Maintenance

Once certified, the agent's certification is suspended if:
- Any Claims Firewall violation is detected in a production run that was not detected by Gate 3
- A regression test failure is introduced by a skill update and not caught before agent execution
- A canonical-product-model.md update changes the status of a capability referenced in the GCM knowledge base and the agent is not updated within 5 business days
- The regulatory knowledge base (`knowledge/regulations/`) is updated and the agent continues to use the prior version

Certification is reinstated when the specific condition is remediated and verified.

---

## Appendix A — Inter-Skill Payload Contracts

### A.1 Trigger Payload → Skill 1 Input Mapping

| Trigger field | Skill 1 input field | Notes |
|---|---|---|
| `subject_description` | `subject_description` | Direct pass-through |
| `subject_type` | `subject_type` | Direct pass-through |
| `jurisdictions` | `jurisdictions` | Direct pass-through |
| `industry` | `industry` | Direct pass-through; defaults to General Enterprise if absent |
| `data_types` | `data_types` | Direct pass-through |
| `deployment_model` | `deployment_model` | Direct pass-through |
| `change_summary` (Trigger 3) | Appended to `subject_description` | "This assessment is a regulatory change re-assessment. Change summary: {change_summary}" |

### A.2 Skill 1 Output → Skill 2 Input Mapping

| Skill 1 output field | Skill 2 input field | Notes |
|---|---|---|
| Full `regulatory_mapping_output` JSON | `upstream_payload` | Full object; not just Section 6 |
| `applicable_regulations[*].control_requirements` (Section 6) | Primary input for Phase 2 | Phase 1.1 validation checks Section 6 presence |
| `applicable_regulations[*].jurisdiction` | `jurisdictions` | Passed as context for BFSI overlay activation |
| Agent context: `client_sector` | `client_sector` | Passed from trigger payload |
| Agent context: `target_maturity_level` | `target_maturity_level` | Passed from trigger payload |
| Agent context: `deployment_model` | `infrastructure_model` | Passed from trigger payload |
| Agent context: `existing_tooling` | `existing_tooling` | Passed from trigger payload |
| `"Regulatory Mapping"` (static) | `upstream_source_type` | Always set to "Regulatory Mapping" for this agent |

### A.3 Skill 2 Output → Handoff Note Mapping

The `{traceability_id}-handoff-note.md` contains the following structured fields for the downstream ethana-solution-mapping consumer:

```markdown
# Handoff Note: {traceability_id}

**Upstream traceability IDs:**
- Regulatory Mapping: TR-RW-{YYYY}-{NNNN}
- Control Mapping: TR-RW-{YYYY}-{NNNN} (same run)

**Control mapping payload location:** {path to control-mapping-payload.json}
**Jurisdiction set:** {list}
**Sector:** {sector}
**Deployment model:** {model}
**Target maturity level:** {level}

**Ethana capability references in Section 10 requiring validation:**
[List of capabilities referenced in the GCM Section 10 Ethana Configuration Guide,
with their canonical status at assessment date, and whether capability-validation
was run for each.]

**Recommended next step:** Execute ethana-solution-mapping against the
control-mapping-payload.json above to produce a Coverage Confidence Score
and proposal-safe capability mapping for each designed control.
```
