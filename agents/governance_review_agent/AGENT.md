# Governance Review Agent (GRA) — Agent Specification

**Version:** 1.0
**Status:** Genuine L4
**Traceability prefix:** `TR-GR-YYYY-NNNN`

---

## 1. Purpose

The Governance Review Agent evaluates a client's AI governance posture against mandatory frameworks (ISO 42001, EU AI Act, NIST AI RMF, etc.) and produces a **Governance Readiness Certificate** — the authoritative verdict on whether the client's governance program is ready for external certification or must remediate before proceeding.

The GRA is the terminal quality gate for governance assessments. Its classification drives downstream decisions on certification submission, remediation roadmap prioritisation, and executive reporting. It is invoked by the Client Assessment Agent as a standalone verification pass, or directly for governance audit requests.

See **ADR-006** (`docs/decisions/ADR-006-governance-review-terminal-gate.md`) for the architectural decision establishing the GRA as a mandatory terminal gate.

---

## 2. Skill

| Skill | Runtime | Schema |
|---|---|---|
| `governance-review` | GRA local executor (`skill_executor.py`) | Input: `governance_review_input` / Output: `governance_review_output` |

---

## 3. Inputs

**Required intake fields** (validated against `governance_review_input` schema):

| Field | Type | Description |
|---|---|---|
| `regulatory_mapping_output` | Object | Regulatory Scoping Matrix from Skill 1 (RM). Contains `applicable_regulations`, `applicable_frameworks`, `control_requirements`. |
| `control_mapping_output` | Object | Operational Control Specification from Skill 2 (GCM). Contains `control_taxonomy_matrix`, `evidence_registry`. |
| `iso_42001_output` | Object | ISO 42001 Gap Assessment from Skill 4. Contains `ams`, `ars`, `certification_classification`, `major_gaps`, `minor_gaps`. |

**Optional fields:**

| Field | Type | Description |
|---|---|---|
| `capability_validation_output` | Object | CVA output from Skill 5. If present, GTG-4 passes (claims present). Used for `input_completeness = "Full"`. |
| `client_profile` | Object | Client context. If present, `input_completeness = "Standard"`. |

---

## 4. State Machine

**Total states:** 11 (6 active, 5 halted)
**Approval gates:** 1 (single approval gate — CSM / Account Director)
**Terminal state (success):** `COMPLETE`
**Terminal states (failure):** all `HALTED_*` states

### State Transitions

```
[Trigger]
    │
    ▼
INTAKE_VALIDATING  ──(schema fail)──►  HALTED_INTAKE_INVALID
    │ valid
    ▼
INTAKE_COMPLETE
    │
    ▼
RUNNING_REVIEW  ──(executor error)──►  HALTED_GOVERNANCE_INCOMPLETE
    │           ──(schema fail)─────►  HALTED_REVIEW_SCHEMA
    │ success
    ▼
REVIEW_COMPLETE
    │
    ├──(governance_gate_passed=false)──►  HALTED_GATE_INSUFFICIENT
    │
    ▼
GATE_VALIDATION_PASSED
    │
    ▼
APPROVAL_PENDING
    │
    ├──(Reject)──►  HALTED_APPROVAL_REJECTED
    │
    ▼
APPROVAL_APPROVED
    │
    ▼
COMPLETE
```

**Forbidden transitions (enforced by StateManager):**
- `APPROVAL_PENDING` → `COMPLETE` (approval gate cannot be skipped)
- `GATE_VALIDATION_PASSED` → `COMPLETE`
- `RUNNING_REVIEW` → `COMPLETE`

---

## 5. Scoring

The GRA executor computes three primary scores:

### 5.1 GAS — Governance Assessment Score (0–100)

```
GAS (arithmetic) = 100
    − (15 × missing_mandatory_framework_count)
    − (10 × mgf_count)
    − (2  × minor_finding_count)
```

**Absolute rule:** if `cgc_count > 0`, GAS = 0 regardless of arithmetic. A Critical Governance Concern (CGC) — any mandatory control domain with < 50% coverage rate — unconditionally fails the governance readiness classification.

### 5.2 CCR — Control Coverage Rate (0–100%)

```
CCR = (implemented_controls + partial_controls × 0.5) / mandatory_controls × 100
```

Mandatory controls are those with `mandatory: true` in `control_requirements`. A control taxonomy entry is "implemented" if its `coverage_classification` is one of: `"Fully Covered by Ethana"`, `"Covered by Cursory Service"`, `"Customer-Owned Control"`. Partial = `"Partially Covered by Ethana"`.

### 5.3 High-Risk Count

```
high_risk_count = cgc_count + (1 if iso_ams < 70 else 0)
```

---

## 6. Classification

| Classification | Conditions |
|---|---|
| **Governance Ready** | `governance_gate_passed=true` AND `cgc_count=0` AND `gas ≥ 85` AND `ccr ≥ 80%` AND `mgf_count=0` AND `high_risk_count ≤ 1` |
| **Conditional Governance** | `governance_gate_passed=true` AND `cgc_count=0` AND `gas ≥ 65` AND `ccr ≥ 60%` AND `high_risk_count ≤ 2` |
| **Not Governance Ready** | All other cases (any failed mandatory GTG gate, any CGC, or below Conditional thresholds) |

---

## 7. GTG Gates

Seven Governance Technical Gates (GTGs) are evaluated by the executor. Only GTG-1, GTG-2, GTG-3, and GTG-7 are mandatory. GTG-4, GTG-5, GTG-6 are advisory ("Noted absent" if not present).

| Gate | Description | Mandatory | Pass Condition |
|---|---|---|---|
| GTG-1 | Confirmed regulations present | Yes | `applicable_regulations` non-empty AND at least one with `status="Confirmed"` |
| GTG-2 | Control taxonomy populated | Yes | `control_taxonomy_matrix` non-empty |
| GTG-3 | ISO 42001 output present | Yes | `iso_42001_output` is non-null (enforced at intake) |
| GTG-4 | Capability validation present | No | `capability_validation_output` is present with `allowed_claims` |
| GTG-5 | Findings documented | No | At least one gap, CGC, MGF, or high-risk item exists |
| GTG-6 | Evidence registry populated | No | `evidence_registry` is non-empty |
| GTG-7 | Regulatory frameworks identified | Yes | `applicable_regulations` OR `applicable_frameworks` is non-empty |

`governance_gate_passed = all(gates[g] == "Pass" for g in ["GTG-1","GTG-2","GTG-3","GTG-7"])`

---

## 8. Findings

The executor identifies three categories of findings in the gap register:

| Type | ID format | Description |
|---|---|---|
| **MGF** (Mandatory Gap Finding) | `GGP-CM-NNN` | Mandatory control not in the control taxonomy matrix and not in a CGC domain. Each MGF deducts 10 from GAS arithmetic. |
| **Minor Finding** | `GGP-IS-NNN` | ISO 42001 major/minor gaps (aggregated — each ISO gap category → one Minor Finding). Each Minor Finding deducts 2 from GAS arithmetic. |
| **CGC** (Critical Governance Concern) | `CGC-NNN` | A mandatory control domain where coverage rate < 50%. CGC presence sets GAS = 0 and blocks Governance Ready / Conditional Governance classification. |

MGFs that fall within a CGC domain are logged with `subsumed_by_cgc: true` and do not separately deduct from GAS (subsumed by the CGC absolute rule).

---

## 9. Outputs

**Package (on `COMPLETE`):** 3 artifacts in `runtime/packages/{traceability_id}/`

| Artifact | File |
|---|---|
| README | `README.md` |
| Governance Review Report | `{traceability_id}-governance-review-report.md` |
| Governance Readiness Certificate | `{traceability_id}-governance-readiness-certificate.json` |
| Audit Trail | `{traceability_id}-audit-log.jsonl` |

**JSON payload fields** (`governance_review_output` schema):

| Field | Type | Description |
|---|---|---|
| `gas` | Integer | Governance Assessment Score (0–100) |
| `ccr` | Float | Control Coverage Rate (0–100) |
| `ccr_numerator` | Float | Implemented + 0.5 × partial controls |
| `ccr_denominator` | Integer | Total mandatory controls |
| `cgc_count` | Integer | Number of Critical Governance Concerns |
| `cgc_ids` | List[str] | CGC identifiers (e.g., `["CGC-001"]`) |
| `mgf_count` | Integer | Number of Mandatory Gap Findings |
| `mgf_ids` | List[str] | MGF identifiers |
| `minor_finding_count` | Integer | Number of Minor Findings |
| `high_risk_count` | Integer | High-risk indicator count |
| `classification` | String | `"Governance Ready"` / `"Conditional Governance"` / `"Not Governance Ready"` |
| `governance_gate_passed` | Boolean | `true` if all mandatory GTG gates pass |
| `iso_42001_ams` | Integer | Pass-through from ISO input |
| `iso_42001_ars` | Integer | Pass-through from ISO input |
| `iso_42001_classification` | String | Pass-through from ISO input |
| `frameworks_assessed` | List[str] | All regulatory/framework names from inputs |
| `review_date` | String | ISO date (YYYY-MM-DD) |
| `input_completeness` | String | `"Full"` / `"Standard"` / `"Minimal"` |
| `required_actions` | List[Object] | Remediation actions for CGCs and MGFs |

---

## 10. Approval Gate

**Single approval gate** — `APPROVAL_PENDING` → CSM / Account Director.

**Method:** `orchestrator.submit_approval(traceability_id, action, actor, notes)`

| Action | Outcome |
|---|---|
| `"Approve"` | Transitions to `APPROVAL_APPROVED` → `COMPLETE`; package assembled |
| `"Reject"` | Transitions to `HALTED_APPROVAL_REJECTED` |

---

## 11. Thresholds (config.yaml)

| Key | Default | Description |
|---|---|---|
| `gas_governance_ready` | 85 | GAS threshold for Governance Ready |
| `gas_conditional` | 65 | GAS threshold for Conditional Governance |
| `ccr_governance_ready` | 80 | CCR threshold for Governance Ready |
| `ccr_conditional` | 60 | CCR threshold for Conditional Governance |
| `high_risk_governance_ready` | 1 | Max high_risk_count for Governance Ready |
| `high_risk_conditional` | 2 | Max high_risk_count for Conditional Governance |
| `iso_ams_high_risk_threshold` | 70 | ISO AMS below this → +1 to high_risk_count |

Note: The executor currently uses hardcoded threshold values matching these defaults. The config is loaded but the executor does not read from it at runtime. Phase B: wire thresholds from config into executor.

---

## 12. Traceability ID Format

`TR-GR-{YEAR}-{NNNN}` — sequential per calendar year, zero-padded to 4 digits.

Example: `TR-GR-2026-0001`

---

## 13. Related Decisions

- **ADR-006** (`docs/decisions/ADR-006-governance-review-terminal-gate.md`): Establishes the GRA as the mandatory terminal gate for governance assessments. The `governance_gate_passed` boolean and the four mandatory GTG gates are specified in ADR-006.

---

## 14. Agent Readiness

**Status:** Genuine L4

| Item | Status |
|---|---|
| Runtime implemented | ✅ |
| State machine (11 states) | ✅ |
| GTG gate evaluation (7 gates) | ✅ |
| GAS / CCR / high-risk scoring | ✅ |
| Classification logic | ✅ |
| Approval gate | ✅ |
| Output package assembly (3 artifacts) | ✅ |
| Schema validation (input + output) | ✅ |
| Audit trail | ✅ |
| ADR-006 terminal gate compliance | ✅ |
| AGENT.md specification | ✅ (this document, PR-009) |

**No critical blockers.** The GRA is fully operational. It is invoked by the Client Assessment Agent when the Governance Review step is reached in the 6-skill chain.
