# Client Assessment Agent

**Version:** 1.0-spec  
**Certification level:** L2 (certifier-reported) — true readiness approximately L2.5; L3 blocked by missing ethana-solution-mapping baseline  
**Status:** Specification complete — implementation blocked (see Section 14, Readiness Report)  
**Skill chain:** regulatory-mapping → governance-control-mapping → ethana-solution-mapping → iso-42001-gap-assessment → ethana-capability-validation → ethana-proposal-review  
**Workflow reference:** `workflows/governance-assessment-workflow.md` (extended; see Section 6)  
**Architecture reference:** `docs/architecture/agent-readiness-audit.md` Section 6, Agent 3  
**Traceability ID format:** `TR-CA-{YYYY}-{NNNN}`

---

## 1. Purpose

The Client Assessment Agent orchestrates the Governance Assessment workflow end-to-end. Given a client's AI portfolio, existing governance policies, and target compliance framework, the agent produces an Executive Assessment Package: a complete, audit-ready governance dossier containing regulatory scoping, control design, platform coverage analysis, ISO 42001 maturity assessment, validated capability claims, and a compliance-reviewed assembly of all findings.

The agent bridges the compliance advisory and commercial advisory functions. It is not an expert system making judgements — it orchestrates certified skills through a defined sequence, enforces quality gates at every transition, and presents human-reviewable outputs at four mandatory approval gates before the final package is assembled.

**The agent is the sole orchestrator for the six-skill governance assessment chain.** No skill in the chain may be invoked out of sequence. No gate may be bypassed. No approval may be simulated.

### Primary use cases

| Trigger | Outcome |
|---|---|
| New client onboarding | Comprehensive governance + commercial baseline |
| Annual governance audit | Updated AMS/ARS and control maturity progression |
| Certification readiness check | ISO 42001 audit preparation package |
| Pre-proposal governance assessment | Compliance foundations for an Ethana commercial engagement |
| Regulatory change impact | Re-assessment of existing client's control posture |

---

## 2. Scope Constraints

The agent enforces the following hard constraints that no configuration, human override, or code path may relax:

| Constraint | Rule |
|---|---|
| Capability status decisions | The agent makes no capability status decisions. Every status determination comes from `knowledge/ethana/canonical-product-model.md` via the skills. |
| Canonical model override | No agent logic, operator instruction, or approval decision may override `canonical-product-model.md` |
| Claims Firewall | Any Claims Firewall violation detected by `claims_linter.py` after any skill halts the agent in `HALTED_FIREWALL_BREACH` (Gates 2c, 3b, 4b, 5b) or `HALTED_FIREWALL_BREACH_TERMINAL` (Gate 6b). There is no threshold — one violation halts the run. |
| Proposal Review Gate | The ethana-proposal-review skill is the terminal gate. No Executive Assessment Package may be assembled or delivered before the proposal review passes. |
| Capability Validation Gate | The ethana-capability-validation skill must execute and pass before the proposal review. No Claims Firewall check substitutes for capability validation. |
| Skill sequence | Skills execute in the order defined in Section 5. No skill may be skipped, reordered, or run in parallel. |

---

## 3. Operational Modes

### Mode A — Full Assessment

**Trigger:** New client onboarding, annual audit, or certification readiness check.

Executes the complete 6-skill chain. All four human approval gates are mandatory.

### Mode B — Incremental Re-Assessment

**Trigger:** Regulatory change alert affecting an existing client, or a partial update to a prior assessment (e.g., client has improved controls since the baseline).

Executes the 6-skill chain but loads the prior assessment from Client Memory as context. Skill outputs are delta-based — the agent flags which sections changed relative to the prior assessment.

**Prerequisite:** A prior completed run (`TR-CA-{YYYY}-{NNNN}`) must exist in Client Memory. Mode B is not available for first-run clients.

---

## 4. Trigger Events and Inputs

### 4.1 Required Fields (all trigger types)

| Field | Type | Validation rule |
|---|---|---|
| `traceability_id` | string | Auto-generated at intake; format `TR-CA-{YYYY}-{NNNN}` |
| `trigger_type` | enum | `new_client_onboarding` / `annual_governance_audit` / `certification_readiness_check` / `regulatory_change_impact` / `pre_proposal_assessment` |
| `client_name` | string | Unique client identifier; links run to Client Memory |
| `client_ai_portfolio` | string | Min 100 chars; inventory of deployed/planned AI systems — what each system does, who it affects, deployment status, system owner |
| `existing_policies` | string | Description of existing AI governance documentation: AI policy, risk register, control evidence, prior assessments |
| `target_framework` | enum | `ISO 42001` / `NIST AI RMF` / `ISO 42001 + NIST` / `Custom Baseline` |
| `target_maturity_level` | enum | `L1` through `L5` |
| `jurisdictions` | array | One or more of: `EU`, `UK`, `India` — unsupported jurisdictions halt at intake |

### 4.2 Optional / Contextual Fields

| Field | Type | Effect |
|---|---|---|
| `industry` | string | Activates BFSI overlays in RM (FCA/PRA), GCM (model risk), ISO 42001 (Annex A SR 11-7), and solution mapping (SOC 2 blocker check) |
| `data_types` | array | Affects GDPR/DPDP applicability in regulatory mapping |
| `deployment_model` | enum | `Cloud SaaS` / `VPC` / `On-premises`; affects control design choices; on-premises triggers mandatory scale caveat in solution mapping |
| `existing_tooling` | array | Surfaced to GCM Phase 1.2 and solution mapping for integration design |
| `target_certification` | enum | `Third-party certification` / `Self-declaration` / `Internal audit only` / `Regulatory submission`; shapes ISO 42001 ARS calibration strictness |
| `prior_assessment_id` | string | Required for Mode B; references a prior completed `TR-CA-{YYYY}-{NNNN}` run |
| `regulatory_change_summary` | string | Required for `regulatory_change_impact` trigger; appended to RM subject description |
| `output_mode` | enum | `Formal Proposal` / `RFP Response` / `Governance Assessment`; defaults to `Governance Assessment`; shapes proposal review language register and In Build disclosure strictness |
| `competitive_context` | string | Surfaced to solution mapping Section 8 (Competitive Positioning) |

### 4.3 Input Validation

The intake sub-component validates before executing any skill:

1. All required fields present and non-empty
2. `jurisdictions` contains only `EU`, `UK`, `India` — unsupported values → `HALTED_INTAKE_UNSUPPORTED_JURISDICTION`
3. `client_ai_portfolio` meets minimum quality: identifies at least one AI system with deployment status — `Low` evidence quality triggers warning, does not block
4. `target_framework` is a supported value — `Custom Baseline` triggers a warning that ISO 42001 scoring will use partial criteria
5. For Mode B: `prior_assessment_id` resolves to a completed run in Client Memory
6. For `regulatory_change_impact` trigger: `regulatory_change_summary` is present

---

## 5. Skill Chain

### 5.1 Sequence Overview

```
[Trigger Event + Validated Inputs]
          │
          ▼
[Skill 1: regulatory-mapping]
  → Regulatory Scoping Matrix
  → Gate 1 (schema + score)
  → Approval Gate 1 (General Counsel / Compliance Lead)
          │
          ▼
[Skill 2: governance-control-mapping]
  → Operational Control Specification
  → Gate 2 (schema + Claims Firewall + score)
          │
          ▼
[Skill 3: ethana-solution-mapping]
  → Solution Mapping Report
  → Gate 3 (schema + Claims Firewall + score)
  → Approval Gate 2 (DPO + CISO)
          │
          ▼
[Skill 4: iso-42001-gap-assessment]
  → ISO 42001 Gap Assessment
  → Gate 4 (schema + Claims Firewall + score)
  → Approval Gate 3 (Client Risk Committee Lead)
          │
          ▼
[Skill 5: ethana-capability-validation]
  → Capability Validation Report
  → Gate 5 (schema + Claims Firewall + score)
          │
          ▼
[Skill 6: ethana-proposal-review]
  → Proposal Review Certificate
  → Gate 6 (schema + Claims Firewall + release classification)
  → Approval Gate 4 (Compliance Director + Sales Director)
          │
          ▼
[Assemble Executive Assessment Package]
[Deliver + Update Client Memory]
          │
          ▼
        COMPLETE
```

### 5.2 Skill 1: regulatory-mapping

**Purpose:** Scopes which regulations apply to the client's AI portfolio, assigns risk tiers, and extracts specific control obligations.

**Input mapping:**

| Source field | Skill input field | Notes |
|---|---|---|
| `client_ai_portfolio` | `subject_description` | Direct pass-through |
| `existing_policies` | Appended to `subject_description` | Prefix: "Existing governance context: " |
| `trigger.subject_type` | `subject_type` | Defaults to `AI Portfolio` |
| `jurisdictions` | `jurisdictions` | Direct pass-through |
| `industry` | `industry` | Defaults to "General Enterprise" if absent |
| `data_types` | `data_types` | Direct pass-through |
| `deployment_model` | `deployment_model` | Direct pass-through |
| `regulatory_change_summary` (Mode B) | Appended to `subject_description` | Prefix: "Regulatory change re-assessment context: " |

**Output used:** Full `regulatory_mapping_output.json` + `{traceability_id}-regulatory-scoping-matrix.md`

### 5.3 Skill 2: governance-control-mapping

**Purpose:** Translates regulatory obligations into specific, implementable technical and process controls. Produces the RACI matrix and Ethana Configuration Guide.

**Pre-execution check:** Skill 1 Section 6 (`applicable_regulations[*].control_requirements`) must be non-empty before constructing the inter-skill payload.

**Input mapping:**

| Source | Skill input field | Notes |
|---|---|---|
| Skill 1 full JSON | `upstream_payload` | Full object |
| `"Regulatory Mapping"` | `upstream_source_type` | Static |
| `run.traceability_id` | `traceability_id` | |
| `target_maturity_level` | `target_maturity_level` | From trigger payload |
| `jurisdictions` | `jurisdictions` | From trigger payload |
| `industry` | `client_sector` | |
| `deployment_model` | `infrastructure_model` | |
| `existing_tooling` | `existing_tooling` | |
| `approval_1_notes` | Additional context in prompt | Notes from AG-1 if "Approve with notes" was selected |

**Claims Firewall enforced:** Gate 2b checks `{traceability_id}-operational-control-spec.md` (Section 10 contains Ethana capability references).

### 5.4 Skill 3: ethana-solution-mapping

**Purpose:** Maps each designed control to Ethana platform capabilities. Produces CCS per requirement, proposal-safe claim language, prohibited claims register, and commercial motion recommendation.

**Input mapping:**

| Source | Skill input field | Notes |
|---|---|---|
| Skill 2 Section 10 + full JSON | `requirement_list` | GCM control specifications as the requirement set |
| Skill 2 full JSON | `upstream_skill_output` | Pre-structured requirements |
| `customer_sector` (= `industry`) | `customer_sector` | |
| `jurisdictions` | `jurisdictions` | |
| `output_mode` | `output_mode` | Defaults to "Formal Proposal" for governance assessment |
| `deployment_model` | `deployment_constraint` | |
| `existing_tooling` | `existing_subscription` context | |
| `competitive_context` | `competitive_context` | |

**Claims Firewall enforced:** Gate 3b checks `{traceability_id}-solution-mapping-report.md` (Section 3 contains proposal-safe capability claims; Sections 4–5 contain prohibited claims register).

**Approval Gate 2 follows Gate 3.** The DPO and CISO review both the control design (Skill 2) and the platform coverage (Skill 3) together — this is a combined review of the control specifications and what Ethana natively delivers.

### 5.5 Skill 4: iso-42001-gap-assessment

**Purpose:** Conducts a clause-by-clause audit of the client's ISO 42001 conformance. Produces AMS, ARS, Certification Classification, gap register, and phased remediation roadmap.

**Input mapping:**

| Source | Skill input field | Notes |
|---|---|---|
| `client_ai_portfolio` | `ai_portfolio` | Direct pass-through from trigger |
| `client_name` + `existing_policies` | `organisation_description` | Combined into organisation context |
| `jurisdictions` | `jurisdictions` | |
| Skill 1 full JSON | `regulatory_mapping_output` | Strongly recommended; Section 2 pre-populates applicable ISO 42001 clauses |
| Skill 2 full JSON | `control_mapping_output` | Recommended; Section 3 identifies controls already designed |
| `existing_policies` | `existing_documentation` | ISO 27001 certificate, SOC 2 report, prior assessments |
| `target_certification` | `target_certification` | |
| `industry` | `industry` | BFSI triggers model risk overlay |
| Prior run AMS/ARS (Mode B, from Client Memory) | `current_maturity_baseline` | Enables gap-closure tracking |

**Claims Firewall enforced:** Gate 4b checks `{traceability_id}-iso42001-gap-assessment.md` (Section 8.5 contains Ethana Coverage Analysis with capability status claims).

**Approval Gate 3 follows Gate 4.** The Client Risk Committee Lead reviews the maturity assessment and approves the gap findings and maturity targets before commercial claims are validated.

### 5.6 Skill 5: ethana-capability-validation

**Purpose:** Validates every Ethana capability claim referenced across the upstream chain (GCM Section 10, solution mapping Sections 3–4, ISO 42001 Section 8). Produces ECS, CPL, allowed/prohibited claim language, and contradiction log.

**What is validated:** The agent extracts all Ethana capability names from:
- GCM Section 10 (Ethana Configuration Guide)
- Solution Mapping Section 3 (Proposal-Safe Platform Capabilities)
- Solution Mapping Section 4 (Roadmap Disclosure items)
- ISO 42001 Section 8 (Ethana Coverage Analysis)

One capability-validation execution is run per unique capability name identified. All outputs are collected as the Capability Validation Report.

**Input mapping (per capability):**

| Source | Skill input field | Notes |
|---|---|---|
| Extracted capability name | `capability_name` | |
| Full claim sentence from upstream | `proposed_claim` | |
| `output_mode` | `claim_context` | Governance Assessment context |
| `industry` | `requesting_team` context | BFSI calibrates mandatory caveat strictness |
| `jurisdictions` | `jurisdiction` | |

**Claims Firewall enforced:** Gate 5b verifies that no capability validated as In Build or Aspirational is described as Production in any upstream-section reference. The cap-val skill itself enforces this through ECS/CPL determination; the linter provides independent verification.

### 5.7 Skill 6: ethana-proposal-review

**Purpose:** Final compliance audit of the assembled Executive Assessment Package. Verifies that every Ethana capability claim in the package traces to a validated upstream skill output and contains no Claims Firewall violations.

**Input mapping:**

| Source | Skill input field | Required by skill | Notes |
|---|---|---|---|
| Assembled assessment package | `draft_proposal` | Yes | All 5 upstream markdown outputs combined |
| Skill 3 JSON | `solution_mapping_output` | Yes | |
| `null` | `feature_mapping_output` | Yes (schema) | **Architectural gap** — see Section 5.7.1 |
| Skill 5 JSON (all validations) | `capability_validation_output` | Strongly Recommended | |
| Skill 1 JSON | `regulatory_mapping_output` | Recommended | |
| Skill 2 JSON | `control_mapping_output` | Recommended | |
| `output_mode` | `output_mode` | No | Passed as "Governance Assessment" |
| `industry` | `customer_sector` | No | |
| `jurisdictions` | `jurisdictions` | No | |

**Claims Firewall enforced:** Gate 6b is the terminal Claims Firewall check. Any violation at this gate is `HALTED_FIREWALL_BREACH_TERMINAL` — the hardest fail in the agent.

**Proposal Review is terminal.** No package is assembled without Gate 6 passing. A `Rejected` release classification halts the agent in `HALTED_PROPOSAL_REJECTED`. A `Conditional` classification requires Compliance Director review (AG-4) before release.

#### 5.7.1 Architectural Constraint: feature_mapping_output Not Available

The ethana-proposal-review skill lists `feature_mapping_output` as a required input. The Client Assessment Agent's chain does not include ethana-feature-mapping; this skill is part of the Ethana Proposal Agent's commercial chain (POC scoping, technical RFI responses), not the governance assessment chain.

**Impact:** The Claim Traceability Coverage Score (CTCS) is limited to approximately 85–90/100 when `feature_mapping_output = null`. Feature-level Technical Fit Score (TFS) validations are absent. Claims about specific deployment configurations and technical integration scenarios cannot be traced to TFS scores.

**Mitigation:** This agent targets `Conditional Release (PCS ≥ 80, CTCS ≥ 80)` as its minimum passing bar for the proposal review gate. Approval Gate 4 (Compliance Director) provides the human review layer that compensates for the missing TFS traceability. If a full `Approved (PCS ≥ 95)` classification is required, the engagement must also run ethana-feature-mapping through the Ethana Proposal Agent before the governance assessment package is delivered.

**Forbidden:** The agent must not fabricate or synthesise a feature_mapping_output to fill this field. It passes `feature_mapping_output = null` and the proposal review skill handles the missing input per its own documented behaviour.

---

## 6. Workflow Integration

### 6.1 Relationship to governance-assessment-workflow.md

`workflows/governance-assessment-workflow.md` documents the canonical 6-skill chain (updated PR-009). Key ordering rationale:
- **Order:** RM → GCM → solution-mapping → ISO → CapVal → FM → proposal-review (GCM precedes ISO to supply `control_mapping_output`; solution-mapping precedes ISO to provide the full platform coverage picture)
- **Approval gates:** 4 human gates (AG-1 through AG-4)

This specification and the workflow document are now consistent.

### 6.2 Handoff From Regulatory Watch Agent

When the Regulatory Watch Agent has already completed Steps 4.1 and 4.2 for the same AI subject (producing a Regulatory Scoping Matrix and Operational Control Specification), the Client Assessment Agent may load those outputs from Assessment Memory rather than re-running Skill 1 and Skill 2. 

Loading prior outputs:
- The agent sets `SKILL_1_RUNNING` → `SKILL_1_COMPLETE` (no execution; output loaded from memory)
- Gate 1 validation runs on the loaded output (schema + structural regression)
- If Gate 1 passes, the agent proceeds to AG-1 as normal
- The run log records that Skills 1 and 2 were loaded from a prior Regulatory Watch run, not re-executed

This handoff is optional — it is not required, and re-executing Skills 1 and 2 fresh is always valid.

### 6.3 Output Consumed by Downstream

The Client Assessment Agent's Executive Assessment Package is the upstream input for:
- The Ethana Proposal Agent (for commercial proposals that follow a governance assessment)
- Client-facing delivery (governance audit binder, certification preparation package)

---

## 7. Outputs

### 7.1 Skill Outputs (produced during run, released after approval)

| Artifact | Produced after | Released after |
|---|---|---|
| `{traceability_id}-regulatory-scoping-matrix.md` | Skill 1 | AG-1 approved |
| `{traceability_id}-regulatory-mapping-payload.json` | Skill 1 | AG-1 approved |
| `{traceability_id}-operational-control-spec.md` | Skill 2 | AG-2 approved |
| `{traceability_id}-control-mapping-payload.json` | Skill 2 | AG-2 approved |
| `{traceability_id}-solution-mapping-report.md` | Skill 3 | AG-2 approved |
| `{traceability_id}-solution-mapping-payload.json` | Skill 3 | AG-2 approved |
| `{traceability_id}-iso42001-gap-assessment.md` | Skill 4 | AG-3 approved |
| `{traceability_id}-iso42001-gap-assessment-payload.json` | Skill 4 | AG-3 approved |
| `{traceability_id}-capability-validation-report.md` | Skill 5 | AG-4 approved |
| `{traceability_id}-capability-validation-payload.json` | Skill 5 | AG-4 approved |
| `{traceability_id}-proposal-review-certificate.md` | Skill 6 | AG-4 approved |
| `{traceability_id}-proposal-review-payload.json` | Skill 6 | AG-4 approved |

### 7.2 Executive Assessment Package

Assembled after AG-4:

```
{traceability_id}-executive-assessment-package/
├── {traceability_id}-regulatory-scoping-matrix.md
├── {traceability_id}-operational-control-spec.md
├── {traceability_id}-solution-mapping-report.md
├── {traceability_id}-iso42001-gap-assessment.md
├── {traceability_id}-capability-validation-report.md
├── {traceability_id}-proposal-review-certificate.md
├── {traceability_id}-client-scorecard.json     ← compiled by scorecard_compiler.py
├── payloads/
│   ├── {traceability_id}-regulatory-mapping-payload.json
│   ├── {traceability_id}-control-mapping-payload.json
│   ├── {traceability_id}-solution-mapping-payload.json
│   ├── {traceability_id}-iso42001-gap-assessment-payload.json
│   ├── {traceability_id}-capability-validation-payload.json
│   └── {traceability_id}-proposal-review-payload.json
└── {traceability_id}-run-log.json
```

### 7.3 Client Scorecard

`{traceability_id}-client-scorecard.json` is produced by `scorecard_compiler.py` from all six skill outputs. It contains:

```json
{
  "traceability_id": "TR-CA-{YYYY}-{NNNN}",
  "client_name": "{client}",
  "assessment_date": "{ISO 8601}",
  "regulatory_assessment": {
    "score": 0,
    "jurisdictions": [],
    "risk_tier": ""
  },
  "control_assessment": {
    "score": 0,
    "control_count": 0,
    "orphan_controls": 0
  },
  "platform_coverage": {
    "ccs_average": 0,
    "production_coverage_percent": 0,
    "commercial_motion": ""
  },
  "iso42001_assessment": {
    "ams": 0,
    "ars": 0,
    "certification_classification": "",
    "critical_gaps": 0,
    "major_gaps": 0
  },
  "capability_validation": {
    "capabilities_validated": 0,
    "all_production_confirmed": false,
    "escalations_required": 0
  },
  "proposal_review": {
    "pcs": 0,
    "ctcs": 0,
    "release_classification": "",
    "claims_firewall_status": "pass"
  },
  "overall_readiness_band": ""
}
```

**`scorecard_compiler.py` must be implemented before this output can be produced.** This is the single most critical implementation blocker for the Client Assessment Agent (see Section 14, Blocker B-01).

---

## 8. Evaluation Gates

Eight automated gates enforce output quality across the six-skill chain. All gates are mandatory. See `evaluation.md` for full gate specifications.

### Gate Summary

| Gate | Skills | Tool | Threshold | Claims Firewall |
|---|---|---|---|---|
| Gate 1 — RM Schema | Skill 1 | `workflow_validator.py` | 0 errors | — |
| Gate 2a — RM Score | Skill 1 | evaluation rubric | ≥ 70/100 | — |
| Gate 2b — GCM Schema | Skill 2 | `workflow_validator.py` | 0 errors | — |
| Gate 2c — GCM Firewall | Skill 2 | `claims_linter.py` | 0 violations | ✅ mandatory |
| Gate 2d — GCM Score | Skill 2 | evaluation rubric | ≥ 85/100 | — |
| Gate 3a — SM Schema | Skill 3 | `workflow_validator.py` | 0 errors | — |
| Gate 3b — SM Firewall | Skill 3 | `claims_linter.py` | 0 violations | ✅ mandatory |
| Gate 3c — SM Score | Skill 3 | evaluation rubric | ≥ 70/100 | — |
| Gate 4a — ISO Schema | Skill 4 | `workflow_validator.py` | 0 errors | — |
| Gate 4b — ISO Firewall | Skill 4 | `claims_linter.py` | 0 violations | ✅ mandatory |
| Gate 4c — ISO Score | Skill 4 | evaluation rubric | ≥ 85/100 | — |
| Gate 5a — CV Schema | Skill 5 | `workflow_validator.py` | 0 errors | — |
| Gate 5b — CV Firewall | Skill 5 | `claims_linter.py` | 0 violations | ✅ mandatory |
| Gate 5c — CV Score | Skill 5 | evaluation rubric | ≥ 90/100 | — |
| Gate 6a — PR Schema | Skill 6 | `workflow_validator.py` | 0 errors | — |
| Gate 6b — PR Firewall | Skill 6 | `claims_linter.py` | 0 violations | ✅ terminal |
| Gate 6c — PR Release | Skill 6 | proposal review rubric | PCS ≥ 80, CTCS ≥ 80 | — |

**Claims Firewall violations are the hardest fail.** A `HALTED_FIREWALL_BREACH_TERMINAL` (at Gate 6b) is irrecoverable without Compliance Director sign-off and a full new run. `HALTED_FIREWALL_BREACH` (Gates 2c, 3b, 4b, 5b) shares the same characteristic — no in-run recovery; new run required. The audit log `trigger` field identifies which gate caused the breach.

---

## 9. Approval Gates

### Approval Gate 1 — Regulatory Scoping Review

**Approver:** General Counsel (or designated Compliance Lead)  
**Triggered:** After Gates 1 and 2a pass  
**Timeout:** 5 business days

**Payload:** Regulatory Scoping Matrix, Gate 2a score breakdown, evidence quality rating, conditional applicability flags, EU AI Act Annex III ambiguities.

**Scope of approval:** The regulatory applicability and risk classification are accurate. Obligations are correctly identified. This approves the regulatory scoping; it does not approve the control design or the ISO 42001 findings.

**Actions:** Approve / Approve with notes / Reject with revision request

### Approval Gate 2 — Control Design and Platform Coverage

**Approvers:** DPO + CISO (joint; both required)  
**Triggered:** After Gates 2b, 2c, 2d, 3a, 3b, and 3c all pass  
**Timeout:** 5 business days

**Payload:** Operational Control Specification, Solution Mapping Report, Gate 2d score breakdown (per-section), Gate 3c score breakdown, Claims Firewall confirmed pass (for both Skill 2 and Skill 3), RACI matrix with named role assignments, Section 10 Ethana Configuration Guide with In Build capabilities flagged.

**Scope of approval:** The control specifications are implementable. The platform coverage assessment is accurate. RACI assignments are accepted. The commercial motion recommendation is appropriate.

**One-approver partial:** If one approves and one rejects → `HALTED_APPROVAL_2_PARTIAL` → conflict resolution.

### Approval Gate 3 — ISO 42001 Maturity Assessment

**Approver:** Client Risk Committee Lead  
**Triggered:** After Gates 4a, 4b, and 4c pass  
**Timeout:** 5 business days

**Payload:** ISO 42001 Gap Assessment, Gate 4c score breakdown (AMS/ARS/Certification Classification), gap register with Critical/Major/Minor counts, maturity roadmap (30-60-90 day phases), Ethana coverage analysis with In Build items flagged.

**Scope of approval:** The gap findings match the organisation's known control posture. The maturity targets are realistic. The Certification Classification reflects the organisation's true readiness.

**Actions:** Approve / Approve with revisions to specific gap findings / Reject with revision request

### Approval Gate 4 — Final Release

**Approvers:** Compliance Director + Sales Director (joint; both required)  
**Triggered:** After Gates 5a, 5b, 5c, 6a, 6b, and 6c pass  
**Timeout:** 3 business days

**Payload:** Proposal Review Certificate (PCS/CTCS/Release Classification), Claims Firewall confirmed pass, Capability Validation Report with ECS and CPL summary, all six skill output documents.

**Scope of approval:** The Executive Assessment Package is accurate, compliant, and fit for client delivery. All Claims Firewall checks passed. The Release Classification is confirmed. If the proposal review returned a Conditional classification (PCS 80–94), the Compliance Director must review and manually sign off on each conditional item.

**Actions:** Approve for delivery / Approve Conditional with manual attestation of conditional items / Reject

---

## 10. Memory Model

### Tier 1 — Run-Scoped Memory

Temporary; must survive process restarts when approval gates are open.

| Data element | Format |
|---|---|
| Trigger event payload | JSON |
| Run state + timestamps | Enum + ISO 8601 |
| Extracted Ethana capability names (from all upstream skills) | Array of strings |
| All six skill outputs (Markdown + JSON) | Markdown + JSON per skill |
| Gate scores (per-dimension/per-section) | JSON per skill |
| Claims Firewall reports (one per skill checked) | JSON per skill |
| Capability validation results (one per capability) | Array of JSON objects |
| Approval decisions + notes (AG-1 through AG-4) | JSON |
| Assembly status (which artifacts have been collected) | JSON |

### Tier 2 — Assessment Memory

Persistent across runs. Indexed per client and per run.

| Data element | Retention | Index keys |
|---|---|---|
| All six skill outputs (JSON) per run | Indefinite until superseded | `traceability_id`, `client_name`, `jurisdictions`, `target_framework` |
| AMS / ARS scores per run | Indefinite | `client_name`, `assessment_date` |
| Run status (complete / preliminary / superseded) | Indefinite | `traceability_id` |
| Capability validation results per run | Indefinite | `traceability_id`, `capability_name` |
| Subject fingerprint (deduplication hash) | Indefinite | `client_name` + `jurisdictions` + `target_framework` |

Assessment Memory enables Mode B incremental re-assessment and tracks AMS/ARS progression over time.

### Tier 3 — Client Memory

Long-term, client-indexed store. Survives superseded assessments and provides longitudinal governance tracking.

| Data element | Retention | Notes |
|---|---|---|
| Client profile (sector, size, deployment model, existing tooling) | Until client offboarded | Reused on every run; reduces intake time |
| Engagement history (all `traceability_id` references) | 5 years | Audit trail |
| AMS/ARS progression over time | 5 years | Tracks certification readiness improvement |
| All Certification Classifications with dates | 5 years | Third-party certification evidence |
| Approval gate history (all decisions and approvers) | 7 years | Regulatory record-keeping |
| Capability claims allowed at each assessment date | 5 years | CPL/ECS history; supports future claims validation |

### Retention Constraints

The agent must not retain:
- Personally identifiable information about client employees beyond named role owners in RACI
- Confidential client data beyond what the trigger payload contained
- Intermediate outputs that did not pass quality gates (discard on halt; do not store)
- Approval decision reasoning beyond what the approver explicitly records

---

## 11. Failure Handling

### Failure State Map

| Failure type | State | Recovery |
|---|---|---|
| Input validation | `HALTED_INTAKE_INVALID` | Operator corrects inputs; resubmits |
| Unsupported jurisdiction | `HALTED_INTAKE_UNSUPPORTED_JURISDICTION` | Escalate to Compliance Analyst |
| Skill 1 schema (post-retry) | `HALTED_GATE_1_SCHEMA` | Escalate to Compliance Analyst |
| Skill 1 score 55–69 | `HALTED_GATE_1_SCORE_PRELIMINARY` | Revision request with failing dimensions |
| Skill 1 score < 55 | `HALTED_GATE_1_SCORE_INSUFFICIENT` | Escalate; do not auto-retry |
| AG-1 rejected | `HALTED_APPROVAL_1_REJECTED` | Operator initiates revised run |
| Skill 2 schema (post-retry) | `HALTED_GATE_2_SCHEMA` | Escalate to Compliance Analyst |
| Skill 2 Claims Firewall | `HALTED_FIREWALL_BREACH` | Auto-route to Compliance Director; no auto-retry |
| Skill 2 score 70–84 | `HALTED_GATE_2_SCORE_BELOW_THRESHOLD` | Revision request |
| Skill 2 score < 70 | `HALTED_GATE_2_SCORE_INSUFFICIENT` | Escalate |
| Skill 3 schema (post-retry) | `HALTED_GATE_3_SCHEMA` | Escalate |
| Skill 3 Claims Firewall | `HALTED_FIREWALL_BREACH` | Auto-route to Compliance Director; no auto-retry |
| Skill 3 score < 70 | `HALTED_GATE_3_SCORE_INSUFFICIENT` | Escalate |
| AG-2 one approved | `HALTED_APPROVAL_2_PARTIAL` | Conflict resolution |
| AG-2 rejected | `HALTED_APPROVAL_2_REJECTED` | Operator initiates revised run |
| Skill 4 schema (post-retry) | `HALTED_GATE_4_SCHEMA` | Escalate |
| Skill 4 Claims Firewall | `HALTED_FIREWALL_BREACH` | Auto-route to Compliance Director |
| Skill 4 score 70–84 | `HALTED_GATE_4_SCORE_BELOW_THRESHOLD` | Revision request |
| Skill 4 score < 70 | `HALTED_GATE_4_SCORE_INSUFFICIENT` | Escalate |
| AG-3 rejected | `HALTED_APPROVAL_3_REJECTED` | Operator initiates revised run |
| AG-3 partial | `HALTED_APPROVAL_3_PARTIAL` | Conflict resolution |
| Skill 5 schema (post-retry) | `HALTED_GATE_5_SCHEMA` | Escalate |
| Skill 5 Claims Firewall | `HALTED_FIREWALL_BREACH` | Auto-route to Compliance Director |
| Skill 5 score < 90 | `HALTED_GATE_5_SCORE_INSUFFICIENT` | Escalate (ECS/CPL failure is always escalated; no auto-retry) |
| Skill 6 schema (post-retry) | `HALTED_GATE_6_SCHEMA` | Escalate |
| Skill 6 Claims Firewall | `HALTED_FIREWALL_BREACH_TERMINAL` | Auto-route to Compliance Director; hardest fail |
| Skill 6 Rejected classification | `HALTED_PROPOSAL_REJECTED` | Escalate to Compliance Director; revised run required |
| Skill 6 Conditional classification | `HALTED_PROPOSAL_CONDITIONAL` | Present to AG-4; Compliance Director reviews conditional items |
| AG-4 rejected | `HALTED_APPROVAL_4_REJECTED` | Operator initiates revised run |
| AG-4 partial | `HALTED_APPROVAL_4_PARTIAL` | Conflict resolution |
| Approval gate timeout | `APPROVAL_TIMED_OUT` | Compliance Analyst notified; agent waits |
| Unresolvable execution error | `HALTED_ESCALATION` | External resolution required |

### Retry Policy

One automatic retry on schema failure (augmented prompt with verbatim error messages). No auto-retry for:
- Score failures (must be reviewed)
- Claims Firewall breaches (require Compliance Director sign-off)
- Proposal Review `Rejected` classification (requires revised run)
- Approval rejections (require operator action)

### Partial Output Release

If the run halts after an approval gate has been passed, the approved artifacts may be released as a partial package upon explicit operator request. The run state remains halted; partial release is recorded in the run log.

---

## 12. Escalation Rules

### Automatic (No Human Authorisation Required)

| Condition | Target |
|---|---|
| Any Claims Firewall breach | Compliance Director — specific capability, canonical model entry, offending section |
| Unsupported jurisdiction | Requesting team + Compliance Analyst |
| Either skill score < 55 | Compliance Analyst with per-dimension breakdown |
| Cap-val ECS < 45 (escalation_required = true in schema) | Compliance Director + Product team |
| Proposal Review `Rejected` classification | Compliance Director + Sales Director |
| Ambiguous EU AI Act Annex III classification | General Counsel via run log flag |

### Human-Authorised

| Condition | Target | Authorisation required |
|---|---|---|
| AG-2 conflict (one approve, one reject) | Both approvers + Compliance Analyst | Conflict resolution meeting |
| AG-3 conflict | Client Risk Committee Lead + both approvers + Compliance Analyst | Conflict resolution |
| AG-4 conflict | Compliance Director + Sales Director + Compliance Analyst | Executive sign-off |
| Approval gate timeout | Compliance Analyst | Extend deadline or initiate revised run |
| Proposal Review `Conditional` — elevate to delivery | Compliance Director | Manual attestation of each conditional item |

---

## 13. Dependencies

### Skills (all must exist and be certified)

| Skill | Status | Path |
|---|---|---|
| regulatory-mapping | ✅ Complete | `skills/regulatory-mapping/` |
| governance-control-mapping | ✅ Complete | `skills/governance-control-mapping/` |
| ethana-solution-mapping | ✅ Complete | `skills/ethana-solution-mapping/` |
| iso-42001-gap-assessment | ✅ Complete | `skills/iso-42001-gap-assessment/` |
| ethana-capability-validation | ✅ Complete | `skills/ethana-capability-validation/` |
| ethana-proposal-review | ✅ Complete | `skills/ethana-proposal-review/` |

### Schemas

| Schema | Status | Path |
|---|---|---|
| `regulatory_mapping_output.json` | ✅ Exists | `workflows/schemas/` |
| `control_mapping_output.json` | ✅ Exists | `workflows/schemas/` |
| `solution_mapping_output.json` | ✅ Exists | `workflows/schemas/` |
| `iso-42001-gap-assessment-input.schema.json` | ✅ Exists | `workflows/schemas/` |
| `iso-42001-gap-assessment-output.schema.json` | ✅ Exists | `workflows/schemas/` |
| `ethana-capability-validation-output.schema.json` | ✅ Exists | `workflows/schemas/` |
| `proposal-review-input.schema.json` | ✅ Exists | `workflows/schemas/` |
| `proposal-review-output.schema.json` | ✅ Exists | `workflows/schemas/` |

### Evaluation Infrastructure

| Component | Status | Path |
|---|---|---|
| `claims_linter.py` | ✅ Available (hardened 2026-06-18) | `evaluations/scripts/` |
| `workflow_validator.py` | ✅ Available | `evaluations/scripts/` |
| `regression_tester.py` | ✅ Available | `evaluations/scripts/` |
| `agent_certifier.py` | ⚠️ Operational with bugs | `evaluations/scripts/` |
| `scorecard_compiler.py` | ❌ **Stub — not implemented** | `evaluations/scripts/` |
| RM structure baseline | ✅ Exists | `evaluations/baselines/regulatory-mapping/structure.json` |
| GCM structure baseline | ✅ Exists | `evaluations/baselines/governance-control-mapping/structure.json` |
| ISO 42001 baseline | ✅ Exists (flat format) | `evaluations/baselines/iso-42001-gap-assessment-baseline.md` |
| Cap-val baseline | ✅ Exists (flat format) | `evaluations/baselines/ethana-capability-validation-baseline.md` |
| Proposal review baseline | ✅ Exists (flat format) | `evaluations/baselines/ethana-proposal-review-baseline.md` |
| **Solution mapping baseline** | ❌ **Missing entirely** | `evaluations/baselines/ethana-solution-mapping/` (needed) |

### Test Fixtures

| Fixture set | Status | Notes |
|---|---|---|
| `regulatory-subjects/` | ✅ 3 fixtures | BFSI/EU+UK, India fintech, UK insurance |
| `iso-42001-gap-assessment/` | ✅ 3 fixtures | Bank certification, fintech extension, greenfield |
| `ethana-capability-validation/` | ✅ 3 fixtures | Production, roadmap, mixed-status |
| `proposal-review/` | ✅ 3 fixtures | Clean, firewall-breach, mixed-roadmap |
| `gold-standards/` | ✅ 3 dual-skill gold standards | RM + GCM combined |
| **`ethana-solution-mapping/`** | ❌ **Missing entirely** | Minimum 3 fixtures required |

---

## 14. Readiness Report

**Date:** 2026-06-18  
**Agent status:** Specification complete. Implementation blocked. True readiness: ~L2.5.

### Critical Blockers (B-01 through B-06)

| ID | Blocker | Severity | What it blocks |
|---|---|---|---|
| B-01 | `scorecard_compiler.py` exists (`evaluations/scripts/scorecard_compiler.py`, 181 lines) but is not wired into CA `ASSEMBLING_PACKAGE` | **Critical** | `{traceability_id}-client-scorecard.json` cannot be produced; Executive Assessment Package is incomplete. Integration is PR-011. |
| B-02 | `evaluations/baselines/ethana-solution-mapping/` missing entirely | **Critical** | Certifier cannot reach L3; regression testing for Skill 3 output is impossible; Gate 3c score has no structural reference |
| B-03 | `evaluations/test-cases/ethana-solution-mapping/` missing entirely | **Critical** | Level 4A cannot be achieved; no fixtures for Skill 3 dry-run |
| ~~B-04~~ | ~~Certifier Bug 1: checks for `"proposal-review"` skill but directory is `"ethana-proposal-review"`~~ | ~~**High**~~ | **Resolved (pre-PR-009):** `agent_certifier.py:30` already lists `"ethana-proposal-review"`. |
| ~~B-05~~ | ~~Certifier baseline format bug: flat `.md` baselines invisible to certifier~~ | ~~**High**~~ | **Resolved (pre-PR-009):** `agent_certifier.py:70–82` checks both directory and flat `{skill}-baseline.md` formats. |
| ~~B-06~~ | ~~`workflows/governance-assessment-workflow.md` defines a 4-skill chain; agent implements 6 skills~~ | ~~**Medium**~~ | **Resolved (PR-009):** `governance-assessment-workflow.md` updated to canonical 6-skill chain. |

### Required Before L4A

| Requirement | Status | Priority |
|---|---|---|
| Create `evaluations/baselines/ethana-solution-mapping/structure.json` | ❌ Missing | P1 |
| Create `evaluations/test-cases/ethana-solution-mapping/` with ≥ 3 fixtures | ❌ Missing | P1 |
| Wire `scorecard_compiler.py` into CA `ASSEMBLING_PACKAGE` | ⚠️ Unwired (PR-011) | P1 |
| ~~Create `evaluations/test-cases/regulatory-subjects/minimal-risk-internal-tool.md`~~ | ✅ Created (PR-008) | — |
| ~~Update `governance-assessment-workflow.md` to 6-skill chain~~ | ✅ Done (PR-009) | — |
| ~~Fix certifier Bug 1 (skill name mismatch)~~ | ✅ Already fixed | — |
| ~~Fix certifier baseline format detection~~ | ✅ Already fixed | — |

### Items Ready (No Blockers)

| Item | Status |
|---|---|
| All 6 skills available and complete | ✅ |
| All 8 required schemas available | ✅ |
| Claims Firewall linter hardened (2026-06-18) | ✅ |
| RM and GCM baselines (JSON format) | ✅ |
| ISO 42001, cap-val, proposal-review baselines (flat format) | ✅ |
| ISO 42001, cap-val, proposal-review test fixtures | ✅ |
| Gold standard dual-skill outputs | ✅ |
| State machine specification complete | ✅ (`state-machine.md`) |
| Evaluation gate specification complete | ✅ (`evaluation.md`) |
| Workflow YAML specification complete | ✅ (`workflow.yaml`) |

### Recommended Resolution Sequence

1. Create `evaluations/baselines/ethana-solution-mapping/structure.json` — unblocks certifier L3 for this agent
2. Create 3 ethana-solution-mapping test fixtures — unblocks L4A
3. Implement `scorecard_compiler.py` — unblocks Executive Assessment Package assembly
4. Fix certifier Bug 1 (one-line change) — unblocks Ethana Proposal Agent too
5. Update `governance-assessment-workflow.md` — documentation hygiene before implementation
6. Begin Level 4B implementation after items 1–3 are complete
