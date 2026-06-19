# Client Assessment Agent — Evaluation Criteria

**Version:** 1.0-spec  
**Scope:** Agent-level evaluation gates, run-level success metrics, and certification criteria.

This document defines the evaluation framework for the Client Assessment Agent. It does not duplicate the skill-level evaluation rubrics — it references them and defines the agent-level gates, thresholds, and success criteria.

For skill-level rubrics, refer to:
- Regulatory Mapping scoring: `skills/regulatory-mapping/evaluation.md`
- Governance Control Mapping scoring: `skills/governance-control-mapping/evaluation.md`
- Ethana Solution Mapping scoring: `skills/ethana-solution-mapping/evaluation.md`
- ISO 42001 Gap Assessment scoring: `skills/iso-42001-gap-assessment/evaluation.md`
- Ethana Capability Validation scoring: `skills/ethana-capability-validation/evaluation.md`
- Ethana Proposal Review scoring: `skills/ethana-proposal-review/evaluation.md`

---

## 1. Gate Summary

| Gate ID | Name | Tool | Threshold | Position |
|---|---|---|---|---|
| **Gate 1** | RM Schema Validation | `workflow_validator.py` | 0 errors | After Skill 1 |
| **Gate 2a** | RM Quality Score | RM evaluation rubric | ≥ 70/100 | After Gate 1 |
| **AG-1** | Approval Gate 1 | Human (General Counsel) | Approve | After Gate 2a |
| **Gate 2b** | GCM Schema Validation | `workflow_validator.py` | 0 errors | After Skill 2 |
| **Gate 2c** | GCM Firewall | `claims_linter.py` | 0 violations | After Skill 2, concurrent |
| **Gate 2d** | GCM Quality Score | GCM evaluation rubric | ≥ 85/100 | After Gate 2b/2c |
| **Gate 3a** | SM Schema Validation | `workflow_validator.py` | 0 errors | After Skill 3 |
| **Gate 3b** | SM Firewall | `claims_linter.py` | 0 violations | After Skill 3, concurrent |
| **Gate 3c** | SM Quality Score | SM evaluation rubric | ≥ 70/100 | After Gate 3a/3b |
| **AG-2** | Approval Gate 2 | Human (DPO + InfoSec Lead) | Joint approve | After Gate 3c |
| **Gate 4a** | ISO Schema Validation | `workflow_validator.py` | 0 errors | After Skill 4 |
| **Gate 4b** | ISO Firewall | `claims_linter.py` | 0 violations | After Skill 4, concurrent |
| **Gate 4c** | ISO Quality Score | ISO evaluation rubric | ≥ 85/100 | After Gate 4a/4b |
| **AG-3** | Approval Gate 3 | Human (Risk Committee Lead) | Approve | After Gate 4c |
| **Gate 5a** | CV Schema Validation | `workflow_validator.py` | 0 errors | After Skill 5 |
| **Gate 5b** | CV Firewall | `claims_linter.py` | 0 violations | After Skill 5, concurrent |
| **Gate 5c** | CV Quality Score | CV evaluation rubric | ≥ 90/100 | After Gate 5a/5b |
| **Gate 6a** | PR Schema Validation | `workflow_validator.py` | 0 errors | After Skill 6 |
| **Gate 6b** | PR Firewall | `claims_linter.py` | 0 violations | After Skill 6, concurrent |
| **Gate 6c** | PR Release Classification | Proposal Review rubric | PCS ≥ 80, CTCS ≥ 80 | After Gate 6a/6b |
| **AG-4** | Approval Gate 4 | Human (Compliance + Sales) | Joint approve | After Gate 6c |

---

## 2. Phase 1 Gates: Regulatory Mapping (Skill 1)

### Gate 1 — RM Schema Validation
- **Purpose:** Confirm the Skill 1 JSON output is structurally correct before it is used as the inter-skill payload for Skill 2.
- **Tool:** `evaluations/scripts/workflow_validator.py`
- **Pass condition:** Zero validation errors.
- **Retry policy:** One automatic retry with an augmented Skill 1 prompt that includes the specific validation error messages.
- **Failure state:** `HALTED_GATE_1_SCHEMA` -> Escalate to Compliance Analyst.

### Gate 2a — RM Quality Score
- **Purpose:** Enforce regulatory scoping accuracy and depth.
- **Tool:** Scored against the `regulatory-mapping` rubric (`skills/regulatory-mapping/evaluation.md`).
- **Pass condition:** Score ≥ 70/100.
- **Failure state:** `HALTED_GATE_2A_QUALITY` -> Route to compliance designer for manual refinement.

### Approval Gate 1 (AG-1) — Regulatory Scoping Matrix Review
- **Approver:** General Counsel (or designated Compliance Lead).
- **Outcome:** Validates that the regulatory baseline and jurisdiction scoping match the client's corporate bounds.
- **Transition:** On approval, proceeds to Control Mapping.

---

## 3. Phase 2 Gates: Control Mapping and Solution Mapping (Skills 2 & 3)

### Gate 2b & 2c — GCM Schema and Firewall
- **Schema:** `workflow_validator.py` validates GCM JSON output against `control_mapping_output.json`.
- **Firewall:** `claims_linter.py` checks GCM configuration files for unauthorized claims.
- **Threshold:** 0 validation errors, 0 firewall violations.
- **Failure state:** `HALTED_FIREWALL_BREACH` (for firewall) or `HALTED_GATE_2B_SCHEMA` (for schema).

### Gate 2d — GCM Quality Score
- **Threshold:** Score ≥ 85/100 against GCM rubric.
- **Failure state:** `HALTED_GATE_2D_QUALITY`.

### Gate 3a & 3b — SM Schema and Firewall
- **Schema:** `workflow_validator.py` validates SM JSON output against `solution_mapping_output.json`.
- **Firewall:** `claims_linter.py` checks SM proposal text for unreleased features.
- **Threshold:** 0 validation errors, 0 firewall violations.
- **Failure state:** `HALTED_FIREWALL_BREACH`.

### Gate 3c — SM Quality Score
- **Threshold:** Score ≥ 70/100 against SM rubric.
- **Failure state:** `HALTED_GATE_3C_QUALITY`.

### Approval Gate 2 (AG-2) — Control Design & Platform Coverage
- **Approvers:** DPO + CISO (joint sign-off).
- **Scope:** Approves control implementation feasibility and validated platform positioning.

---

## 4. Phase 3 Gates: ISO 42001 & Capability Validation (Skills 4 & 5)

### Gate 4a & 4b — ISO Schema and Firewall
- **Schema:** `workflow_validator.py` validates ISO 42001 output against schema.
- **Firewall:** `claims_linter.py` checks gap assessments for unreleased modules.
- **Threshold:** 0 errors, 0 violations.

### Gate 4c — ISO Quality Score
- **Threshold:** Score ≥ 85/100 against ISO rubric.
- **Failure state:** `HALTED_GATE_4C_QUALITY`.

### Approval Gate 3 (AG-3) — ISO 42001 Maturity Assessment
- **Approver:** Client Risk Committee Lead.
- **Scope:** Verifies that the gap register, AMS/ARS scores, and 30-60-90 day roadmap are client-acceptable.

### Gate 5a & 5b — CV Schema and Firewall
- **Schema:** `workflow_validator.py` validates CV output against schema.
- **Firewall:** `claims_linter.py` checks capability determinations for Claims Firewall compliance.
- **Threshold:** 0 errors, 0 violations.

### Gate 5c — CV Quality Score
- **Threshold:** Score ≥ 90/100 against CV rubric.

---

## 5. Phase 4 Gates: Proposal Review & Release (Skill 6)

### Gate 6a & 6b — PR Schema and Firewall
- **Schema:** `workflow_validator.py` validates proposal review decision.
- **Firewall:** `claims_linter.py` performs a terminal scan of the final Executive Assessment Package.
- **Threshold:** 0 errors, 0 violations.
- **Failure state:** `HALTED_FIREWALL_BREACH_TERMINAL`.

### Gate 6c — PR Release Classification
- **Threshold:** PCS ≥ 80, CTCS ≥ 80.
- **Outcome mapping:**
  - PCS ≥ 95 AND CTCS = 100: **Approved**
  - PCS 90-94 OR CTCS 90-99: **Approved with Revisions**
  - PCS 80-89: **Conditional Release**
  - PCS < 80 OR CTCS < 80: **Rejected**

### Approval Gate 4 (AG-4) — Final Release
- **Approvers:** Compliance Director + Sales Director.
- **Scope:** Joint sign-off confirming the package is 100% compliant, accurate, and ready for client delivery.

---

## 6. Run-Level Success Metrics

### Quality Metrics
- **Firewall Compliance Rate (FCR):** Percentage of runs with zero Claims Firewall violations. Target: 100%.
- **First-Pass Approval Rate (FPA):** Percentage of runs passing all human approval gates without a revision loop. Target: ≥ 80%.
- **Average Quality Score (AQS):** Average score across all skill rubrics. Target: ≥ 85/100.

### Throughput Metrics
- **Orchestration Execution Time (OET):** End-to-end run time excluding human queue time. Target: < 6 hours.
- **Human Response Time (HRT):** Average turn-around time at approval gates. Target: < 3 business days.

---

## 7. Certification Criteria

The Agent Readiness Certifier (`agent_certifier.py`) certifies the Client Assessment Agent across five readiness levels:

- **Level 0 — Missing Dependencies:** Blocked. Missing one or more required skills or workflow files.
- **Level 1 — Skills Complete:** All six required skills exist and are documented.
- **Level 2 — Workflows Complete:** All orchestrating workflows exist.
- **Level 3 — Evaluations Passing:** Structural baselines exist in `evaluations/baselines/` and all test fixtures pass.
- **Level 4 — Production Ready:** Agent runtime codebase committed, telemetry active, and integration tests passing.
