# Regulatory Watch Agent — Evaluation Criteria

**Version:** 1.0-spec  
**Scope:** Agent-level evaluation gates, run-level success metrics, and certification criteria.

This document defines the evaluation framework for the Regulatory Watch Agent. It does not duplicate the skill-level evaluation rubrics — it references them and defines the agent-level gates, thresholds, and success criteria.

For skill-level rubrics:
- Regulatory Mapping scoring: `skills/regulatory-mapping/evaluation.md`
- Governance Control Mapping scoring: `skills/governance-control-mapping/evaluation.md`

---

## 1. Gate Summary

| Gate ID | Name | Tool | Threshold | Position |
|---|---|---|---|---|
| Gate 1 | RM Schema Validation | `workflow_validator.py` | 0 errors | After Skill 1 |
| Gate 2 | RM Quality Score | RM evaluation rubric | ≥ 70/100 | After Gate 1 |
| AG-1 | Approval Gate 1 | Human (General Counsel) | Approve | After Gate 2 |
| Gate 3a | GCM Schema Validation | `workflow_validator.py` | 0 errors | After Skill 2 |
| Gate 3b | Claims Firewall | `claims_linter.py` | 0 violations | After Skill 2, concurrent |
| Gate 4 | GCM Quality Score | GCM evaluation rubric | ≥ 85/100 | After Gate 3 |
| AG-2 | Approval Gate 2 | Human (DPO + InfoSec Lead) | Joint approve | After Gate 4 |

No gate may be bypassed or skipped. Claims Firewall violations may not be cleared by a human reviewer — only a new run after Compliance Director sign-off can resolve a `HALTED_FIREWALL_BREACH` state.

---

## 2. Gate 1 — Regulatory Mapping Schema Validation

**Purpose:** Confirm the Skill 1 JSON output is structurally correct before it is used as the inter-skill payload for Skill 2.

**Tool:** `evaluations/scripts/workflow_validator.py`

**Command:**
```bash
python evaluations/scripts/workflow_validator.py \
  {traceability_id}-regulatory-mapping-payload.json \
  workflows/schemas/regulatory_mapping_output.json
```

**Pass condition:** Zero validation errors.

**Retry policy:** One automatic retry with an augmented Skill 1 prompt that includes the specific validation error messages. The retry prompt must quote each error verbatim; vague "try again" prompts are not permitted.

**Outcomes after retry:**

| Result | State | Action |
|---|---|---|
| Pass | `GATE_1_PASSED` | Proceed to Gate 2 |
| Fail after retry | `HALTED_GATE_1_SCHEMA` | Escalate to Compliance Analyst with error dump |

**Structural regression check (advisory):** After Gate 1 passes, the agent may also run:
```bash
python evaluations/scripts/regression_tester.py \
  {traceability_id}-regulatory-scoping-matrix.md \
  evaluations/baselines/regulatory-mapping/structure.json
```
This check is advisory at the agent level — structural regression is the primary quality signal for the gold standard library, not the individual run gate. However, a regression failure should be flagged in the run log for the approver's awareness.

---

## 3. Gate 2 — Regulatory Mapping Quality Score

**Purpose:** Ensure the Regulatory Scoping Matrix meets the minimum quality threshold before human review is requested.

**Rubric:** `skills/regulatory-mapping/evaluation.md` — 9-section scoring matrix.

**Pass threshold:** 70/100.

**Score computation:** The agent must apply the full 9-dimension rubric. Approximation or heuristic scoring is not permitted. The per-dimension breakdown must be stored in run-scoped memory and included in the Gate 2 summary presented to the approver.

### Scoring Dimensions

| Dimension | Max score | Pass indicator |
|---|---|---|
| 1. Applicable Regulations | 15 | All applicable regulations correctly identified for every jurisdiction; triggers are specific |
| 2. Applicable Governance Frameworks | 10 | Frameworks are specific to the subject, not generic |
| 3. Regulatory Obligations | 15 | Obligations are specific and cite specific legal provisions (Article/Section) |
| 4. Risk Classification | 10 | Classification is accurate and defensible; ambiguous cases are flagged |
| 5. Documentation Requirements | 10 | Complete and specific |
| 6. Control Requirements | 15 | Controls are specific, actionable, correctly classified as mandatory/recommended |
| 7. Audit Evidence Required | 5 | Complete; linked to regulatory sources |
| 8. BFSI Considerations | 10 | Sector-specific, not generic (only scored if BFSI is applicable) |
| 9. Executive Summary | 10 | Accurately compresses the full analysis for a senior audience |

### Score Band Actions

| Score | State | Action |
|---|---|---|
| ≥ 70 | `GATE_2_PASSED` | Proceed to Approval Gate 1 |
| 55–69 | `HALTED_GATE_2_PRELIMINARY` | Reclassify output as Preliminary; generate revision request specifying each failing dimension and the score delta required to pass |
| < 55 | `HALTED_GATE_2_INSUFFICIENT` | Escalate to Compliance Analyst with per-dimension breakdown; do not auto-retry |

### Common Gate 2 Failure Modes

- **Missing sectoral regulations:** Identified GDPR but not FCA/PRA obligations for a BFSI subject
- **Generic obligation statements:** "Comply with GDPR" without citing specific Articles
- **Non-applicability not documented:** No explicit statement of which regulations were considered and rejected, and why
- **Ambiguous risk classification without flagging:** EU AI Act Annex III classification unclear but not escalated
- **Generic control requirements:** "Implement access controls" without specifying control type, scope, or regulatory mapping

---

## 4. Approval Gate 1 (AG-1) — Regulatory Scoping Matrix Review

**Approver:** General Counsel (or designated Legal Representative)

**Payload presented:**

| Item | Description |
|---|---|
| `{traceability_id}-regulatory-scoping-matrix.md` | Full 9-section document |
| Gate 2 score | Per-dimension breakdown |
| Evidence quality rating | High / Medium / Low (from regulatory-mapping Phase 1.4) |
| Conditional applicability flags | Regulations whose applicability depends on facts requiring legal judgement |
| Annex III ambiguity flags | Any EU AI Act Annex III classification marked as ambiguous |

**Approval scope:** The Regulatory Scoping Matrix is accurate as a statement of regulatory applicability and obligation scope. Risk classifications are legally defensible. This approval **does not** authorise the control design.

**Run log must record:** "General Counsel approval of Regulatory Scoping Matrix is not a formal legal opinion and does not constitute legal advice."

**Timeout:** 5 business days. On timeout → `APPROVAL_TIMED_OUT` → Compliance Analyst notified.

---

## 5. Gate 3a — Control Mapping Schema Validation

**Purpose:** Confirm the Skill 2 JSON output is structurally correct before it is included in the Compliance and Coverage Package.

**Tool:** `evaluations/scripts/workflow_validator.py`

**Command:**
```bash
python evaluations/scripts/workflow_validator.py \
  {traceability_id}-control-mapping-payload.json \
  workflows/schemas/control_mapping_output.json
```

**Pass condition:** Zero validation errors.

**Retry policy:** Same as Gate 1 — one automatic retry with augmented prompt and verbatim error messages.

**Outcomes:**

| Result | State | Action |
|---|---|---|
| Pass | Contributes to `GATE_3_PASSED` | (Gate 3b must also pass) |
| Fail after retry | `HALTED_GATE_3A_SCHEMA` | Escalate to Compliance Analyst |

**Concurrent with:** Gate 3b (Claims Firewall). Both must pass for `GATE_3_PASSED`. If Claims Firewall fails regardless of schema result, `HALTED_FIREWALL_BREACH` takes precedence.

---

## 6. Gate 3b — Claims Firewall Compliance Check

**Purpose:** Prevent any In Build or Aspirational Ethana capability from being presented as Production in the Operational Control Specification. This gate enforces the Claims Firewall policy.

**Authority:** `knowledge/ethana/canonical-product-model.md` is the sole authority for Ethana capability status. The linter reads this file on each run.

**Tool:** `evaluations/scripts/claims_linter.py` (hardened version, 2026-06-18)

**Command:**
```bash
python evaluations/scripts/claims_linter.py \
  {traceability_id}-operational-control-spec.md
```

**Pass condition:** Zero violations.

**Bypass permitted:** No. Under no circumstances.

**Outcomes:**

| Result | State | Action |
|---|---|---|
| 0 violations | Contributes to `GATE_3_PASSED` | (Gate 3a must also pass) |
| ≥ 1 violation | `HALTED_FIREWALL_BREACH` | See below |

### HALTED_FIREWALL_BREACH Protocol

1. Agent halts immediately. No further processing.
2. Auto-escalation to Compliance Director with:
   - The specific capability name(s) that triggered the violation
   - The canonical model entry (status at assessment date from `canonical-product-model.md`)
   - The exact line(s) from the Operational Control Specification that triggered each violation
   - The linter output in full
3. The output is **not** revised, corrected, or re-submitted by the agent
4. The Compliance Director must review the breach and authorise any re-run
5. A new run must be initiated with a new traceability ID; the breached output is discarded

### Violation Types (from linter)

| Violation type | Description | Severity |
|---|---|---|
| Firewall Breach | In Build/Aspirational capability explicitly referred to as Production | Critical |
| Hard Rule Violation | Aspirational capability (Visual Agent Builder, Ethana Workspace, Ethana Edge/Sentry) claimed as available | Critical |
| Ambiguity Warning | Non-production capability mentioned without status disclosure | High |
| Missing Workaround | Status disclosed but no manual/Cursory bridge described | Medium |

All violation types trigger `HALTED_FIREWALL_BREACH`. There is no threshold — even one Ambiguity Warning is a Claims Firewall breach.

### Claims Firewall — Mandatory Capability Status

The following capabilities have known non-production status as of the canonical model's current state. Their status must be accurately reflected in any Section 10 Ethana Configuration Guide:

| Capability | Canonical Status | Claims Firewall rule |
|---|---|---|
| Visual Agent Builder | Aspirational | May not be mentioned in any commercial or technical context as available or deployable |
| Ethana Workspace | Aspirational | Must not be claimed as active or available |
| SOC 2 Type II | In Build | Must not be claimed as currently held certification |
| SCIM Provisioning | In Build | Must not be claimed as current capability |
| CI/CD Gate Integration (CI/CD Red-Teaming Gate) | In Build | Must not be claimed as deployable |
| Compliance Pack | In Build | Must not be claimed as available for evidence collection |
| Non-Human Identity (NHI) for Agents | In Build | Must not be claimed as current capability |
| Governance Policy Engine | In Build | Must not be claimed as deployed |

*Source of record: `knowledge/ethana/canonical-product-model.md`. This table is illustrative at the time of writing; the linter reads the canonical model directly on each run and reflects its current state.*

---

## 7. Gate 4 — Control Mapping Quality Score

**Purpose:** Ensure the Operational Control Specification meets the minimum quality threshold before joint DPO + InfoSec Lead review is requested.

**Rubric:** `skills/governance-control-mapping/evaluation.md`

**Pass threshold:** 85/100.

**Score computation:** The agent must apply the full section-level rubric. Per-section breakdown stored in run-scoped memory and presented to approvers at Approval Gate 2.

### Scoring Sections (from GCM evaluation rubric)

| Section | Description | Key quality signal |
|---|---|---|
| Section 1: Executive Summary | Accuracy of control landscape summary | Correctly identifies total control count, coverage gaps, maturity baseline |
| Section 2: Control Taxonomy Matrix | Completeness of control classification | All required columns present; no orphan controls |
| Section 3: Coverage Classification | Accuracy of coverage gap identification | Gaps aligned with Skill 1 Section 6 obligations |
| Section 4: Preventive Controls | Specificity and implementability | Implementation steps are engineering-level, not generic |
| Section 5: Detective Controls | Same | |
| Section 6: Corrective Controls | Same | |
| Section 7: Evidence Requirements | Completeness | Every control in Section 2 has a matching entry here |
| Section 8: RACI Matrix | Zero orphan controls | Every control has exactly one Accountable role |
| Section 9: Maturity Roadmap | Realism of phased plan | Phase timelines align with target maturity level; no skipped phases |
| Section 10: Ethana Configuration Guide | Accuracy and Claims Firewall compliance | In Build capabilities are flagged as roadmap; no Production claims for non-production items |

### Score Band Actions

| Score | State | Action |
|---|---|---|
| ≥ 85 | `GATE_4_PASSED` | Proceed to Approval Gate 2 |
| 70–84 | `HALTED_GATE_4_BELOW_THRESHOLD` | Generate revision request with each failing section and score delta needed to reach 85 |
| < 70 | `HALTED_GATE_4_INSUFFICIENT` | Escalate to Compliance Analyst; do not auto-retry |

### Critical Section 10 Requirements

Section 10 (Ethana Configuration Guide) must satisfy additional Claims Firewall criteria beyond what the linter checks:

1. Every Ethana capability referenced in Section 10 must cite its canonical status (Production / In Build / Roadmap / Aspirational) at the time of assessment
2. In Build capabilities must include an explicit statement that the capability is roadmap-only and not yet deployable
3. Any capability referenced in Section 10 that has not been through `ethana-capability-validation` must be flagged in the handoff note (advisory, not a gate failure)

---

## 8. Approval Gate 2 (AG-2) — Control Specification and RACI Review

**Approvers:** DPO + Information Security Lead (joint sign-off; both required)

**Payload presented:**

| Item | Description |
|---|---|
| `{traceability_id}-operational-control-spec.md` | Full 10-section document |
| Gate 4 score | Per-section breakdown |
| Claims Firewall compliance status | "CONFIRMED PASS — 0 violations detected by claims_linter.py" |
| Section 8 RACI matrix | With all role assignments named for approver review |
| Section 10 Ethana Configuration Guide | With all In Build capabilities explicitly flagged as roadmap items |

**Approval scope:** Controls are implementable given the organisation's current security posture and team structure. RACI assignments are accepted. Maturity roadmap timeline is realistic.

**Single-approver partial approval:** If one approver acts and the other has not yet acted, the agent waits. If the first approver approves and the second later rejects, the state becomes `HALTED_APPROVAL_2_PARTIAL`.

**Modification scope:** Approvers may modify RACI role assignments or add caveats to specific controls. They may not modify the Claims Firewall compliance status or alter capability status claims in Section 10 — those require a re-run, not manual amendment.

**Timeout:** 5 business days. On timeout → `APPROVAL_TIMED_OUT` → Compliance Analyst notified.

---

## 9. Run-Level Success Metrics

These metrics are computed per completed run (state = `COMPLETE`) and stored in the run log.

### Quality Metrics

| Metric | Gate threshold | Aspirational target | Measurement |
|---|---|---|---|
| Regulatory Mapping score | ≥ 70 | ≥ 80 | Gate 2 rubric score |
| Control Mapping score | ≥ 85 | ≥ 90 | Gate 4 rubric score |
| Claims Firewall compliance | 100% (0 breaches) | 100% | Gate 3b linter output |
| Schema validation at first attempt | 100% | 100% | Gate 1 and 3a: pass without retry |

### Throughput Metrics

| Metric | Target | Measurement |
|---|---|---|
| Skill 1 execution time (single jurisdiction) | ≤ 90 minutes | `SKILL_1_RUNNING` → `SKILL_1_COMPLETE` |
| Skill 1 execution time (multi-jurisdiction) | ≤ 150 minutes | Same |
| Skill 2 execution time (single jurisdiction) | ≤ 90 minutes | `SKILL_2_RUNNING` → `SKILL_2_COMPLETE` |
| Skill 2 execution time (multi-jurisdiction) | ≤ 120 minutes | Same |
| Approval Gate 1 turnaround | ≤ 2 business days | `APPROVAL_1_PENDING` → `APPROVAL_1_APPROVED` |
| Approval Gate 2 turnaround | ≤ 3 business days | `APPROVAL_2_PENDING` → `APPROVAL_2_APPROVED` |
| End-to-end cycle time | ≤ 7 business days | `INTAKE_COMPLETE` → `COMPLETE` |

### Effectiveness Metrics

| Metric | Target | Measurement method |
|---|---|---|
| Compliance Coverage Rate | 100% of applicable obligations mapped to active controls | Human reviewer audit: Skill 1 Section 6 vs. Skill 2 Section 4 |
| Regulatory citation accuracy | 100% of obligations cite specific legal provisions | Reviewer verification: no obligation stated as "comply with [regulation]" without specific Article or Section |
| Audit Readiness Index | 100% of controls have defined evidence collection mechanisms | Section 7 completeness: every control in Section 2 has a matching entry in Section 7 |
| RACI completeness | Zero orphan controls | Every control in Section 2 has exactly one Accountable role in Section 8 |

---

## 10. Mode B Effectiveness Metrics

These metrics are computed per completed Trigger 3 event (all queued re-assessments completed).

| Metric | Target | Measurement |
|---|---|---|
| Regulatory change to first re-assessment triggered | ≤ 1 business day | Trigger 3 receipt → first Mode A run initiated |
| Re-assessment queue completion (Critical severity) | ≤ 5 business days | Trigger 3 receipt → all Critical re-assessments complete |
| Re-assessment coverage rate | ≥ 95% of affected assessments identified | Manual audit: did the agent query the full assessment memory correctly? |
| Duplicate prevention | 0 duplicate re-assessment queues for same regulation + jurisdiction | Regulatory calendar deduplication check |

---

## 11. Certification Criteria

### Level 3 (Current — Achieved)

Requirements: `skills/regulatory-mapping/SKILL.md`, `skills/governance-control-mapping/SKILL.md`, `workflows/regulatory-compliance-workflow.md`, and both structure baselines exist. All confirmed present.

### Level 4A — Test Coverage Gate

The following must pass before Level 4B implementation begins:

| Requirement | Verification command |
|---|---|
| regulatory-subjects fixtures contain BFSI multi-jurisdiction | Manual review: `eu-ai-act-high-risk-banking.md` has `jurisdictions: ["EU", "UK"]` |
| regulatory-subjects fixtures contain Trigger 3 case | Manual review: `uk-insurance-claims-model.md` has `trigger_type: regulatory_change_alert` |
| regulatory-subjects fixtures contain minimal-risk tool | **MISSING** — must create before L4A complete |
| RM regression on eu-ai-act fixture | `python evaluations/scripts/regression_tester.py evaluations/test-cases/regulatory-subjects/eu-ai-act-high-risk-banking.md evaluations/baselines/regulatory-mapping/structure.json` |
| RM regression on india-dpdp fixture | Same command, india-dpdp fixture |
| RM regression on uk-insurance fixture | Same command, uk-insurance fixture |
| GCM regression on EU AI Act gold standard | `python evaluations/scripts/regression_tester.py evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md evaluations/baselines/governance-control-mapping/structure.json` |
| Claims linter on EU AI Act gold standard | `python evaluations/scripts/claims_linter.py evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md` |
| Claims linter on all 3 gold standards | Same command for india-dpdp and uk-insurance gold standards |

### Level 4B — Implementation Completeness Gate

When the implementation files exist, confirm:

| Requirement | Check |
|---|---|
| All 7 implementation files present | `ls agents/regulatory-watch-agent/*.py agents/regulatory-watch-agent/config.yaml` |
| `orchestrator.py` implements all state transitions from state-machine.md | Code review |
| `gates.py` calls `claims_linter.py`, `workflow_validator.py`, applies rubric | Code review |
| `memory.py` writes to durable store (not in-process dict) | Code review |
| `config.yaml` exposes approval_timeout_days, max_concurrent_mode_b, supported_jurisdictions, score thresholds | Manual check |

### Level 4C — Production Readiness Gate

| Requirement | Verification |
|---|---|
| Mode A dry-run on all 3 regulatory-subjects fixtures | All gates pass; run logs in `evaluations/scorecards/` |
| Mode B dry-run | Trigger 3 event with `uk-insurance-claims-model` as known affected subject; re-assessment queue correctly populated |
| Deliberate Claims Firewall integration test | One GCM output with an In Build capability claimed as Production; agent must halt in `HALTED_FIREWALL_BREACH` and route to Compliance Director |
| State persistence test | Process restart during `APPROVAL_1_PENDING`; agent resumes without data loss |
| Approval gate integration | Both gates wired to notification channels; no simulated approvals in any configuration |

### Certification Suspension Conditions

Once certified, the agent's certification is suspended if:

1. A Claims Firewall violation is detected in a production run that was not caught by Gate 3b
2. A regression test failure is introduced by a skill update and not caught before agent execution
3. `canonical-product-model.md` is updated and the agent is not updated within 5 business days
4. `knowledge/regulations/` is updated and the agent continues to use the prior version

Certification reinstated when the specific condition is remediated and verified by re-running the relevant Level 4C tests.

---

## 12. Evaluation Regression Tests

The following commands form the standard regression suite for the agent, to be run before any release:

```bash
# --- Gold standard structural integrity ---
python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md \
  evaluations/baselines/governance-control-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/gold-standards/india-dpdp-customer-support-ai-gold-standard.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/gold-standards/uk-insurance-claims-model-gold-standard.md \
  evaluations/baselines/regulatory-mapping/structure.json

# --- Claims Firewall on all gold standards ---
python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md

python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/india-dpdp-customer-support-ai-gold-standard.md

python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/uk-insurance-claims-model-gold-standard.md

# --- RM structural regression on subject fixtures ---
python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/regulatory-subjects/eu-ai-act-high-risk-banking.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/regulatory-subjects/india-dpdp-customer-support-ai.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/regulatory-subjects/uk-insurance-claims-model.md \
  evaluations/baselines/regulatory-mapping/structure.json
```

All commands must return pass status before any production run or agent update is deployed.
