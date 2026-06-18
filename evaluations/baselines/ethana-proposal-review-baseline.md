# Proposal Review — Regression Baseline

**Skill:** ethana-proposal-review  
**Baseline version:** 1.0  
**Date established:** 2026-06-17  
**Authority:** Cursory Governance Team

This baseline documents the expected score ranges, CTCS values, classification outcomes, and structural requirements for the three proposal-review test fixtures. It is the reference used by `regression_tester.py` to detect drift in reviewer calibration or skill output structure.

---

## 1. Score Range Baselines by Fixture

### 1.1 `clean-proposal`

| Metric | Expected Range | Notes |
|---|---|---|
| PCS | 98–100 | No CFBs, no MRFs. Full compliance. |
| CTCS | 95–100 | Full input set; all Production claims fully traced. |
| CFB count | 0 | Roadmap items are disclosed in the Roadmap section — compliant. |
| MRF count | 0 | No material risk findings. |
| Minor count | 0 | No minor findings expected on the clean path. |
| Classification | **Approved** | Both PCS ≥ 98 and CTCS ≥ 95 required. |
| Traceability gate | Passed | All six inputs available; TG-1 through TG-7 all Pass. |

**Regression alert:** Any output with PCS < 98 or CTCS < 95 for this fixture indicates calibration drift — likely over-triggering of HD2 on the correctly-disclosed roadmap items, or undercounting Traced claims. Investigate Section 3 traceability assignments.

---

### 1.2 `firewall-breach`

| Metric | Expected Range | Notes |
|---|---|---|
| PCS | 0 | Absolute Release Rule: any CFB → PCS = 0. |
| CTCS | 40–65 | Standard inputs (no Capability Validation); multiple untraced/prohibited claims. |
| CFB count | 3 | CFB-001 (Visual Agent Builder/HD1), CFB-002 (SOC 2/HD3), CFB-003 (deployment claim/HD5). |
| MRF count | 0 | All material findings escalate to CFB level. |
| Minor count | 0 | No sub-CFB findings expected. |
| Classification | **Rejected** | Absolute Release Rule enforced; CFBs present. |
| Traceability gate | Passed | TG-4 (Capability Validation) absent but noted; TG-1, TG-2, TG-3, TG-7 all Pass. |

**Regression alert:** Any output that classifies this fixture as anything other than Rejected has violated the Absolute Release Rule (HD7). Any output that identifies fewer than 3 CFBs has missed at least one firewall breach. Investigate Section 4 (Capability Status Validation) for missed Aspirational/uncertified claims.

---

### 1.3 `mixed-roadmap-claims`

**Pre-correction state (as submitted):**

| Metric | Expected Range | Notes |
|---|---|---|
| PCS | 0 | Absolute Release Rule: CFBs present. |
| CTCS | 60–75 | Full inputs; In Build claims in Current section counted as Prohibited. |
| CFB count | 2 | CFB-001 (SCIM/HD2), CFB-002 (CI/CD Gate/HD2). |
| MRF count | 0 | Findings escalate to CFB, not MRF. |
| Minor count | 1 | EU AI Act Annex IV scope understated (−1 PCS, but PCS already 0). |
| Classification | **Rejected** | Absolute Release Rule enforced; 2 CFBs present. |

**Post-correction state (after moving In Build claims to labelled Roadmap section):**

| Metric | Expected Range | Notes |
|---|---|---|
| PCS | 94–99 | 0 CFBs. 1 Minor Finding (−1). Optional MRF if roadmap delivery commitment not cleaned up (−5). |
| CTCS | 78–92 | SCIM and CI/CD now Partially Traced (roadmap disclosure present). |
| CFB count | 0 | Correct roadmap section disclosure resolves both CFBs. |
| MRF count | 0–1 | MRF if roadmap disclosure includes an unauthorized delivery commitment. |
| Minor count | 1 | EU AI Act Annex IV scope remains a Minor Finding. |
| Classification | **Approved with Revisions** | PCS ≥ 95 and CTCS ≥ 80 expected; MRF must be addressed before release. |

**Regression alert:** Any output that classifies the pre-correction state as MRF rather than CFB for the SCIM or CI/CD claims has miscalibrated the HD2 trigger. The distinction is placement section, not claim content. Any output that classifies the EU AI Act Annex IV claim as a CFB has over-triggered the Claims Firewall.

---

### 1.4 TG-3 Fail path (executor direct — `feature_mapping_output` absent)

This fixture is exercised by `test_tg3_fail_when_feature_mapping_absent`. It calls the executor directly, bypassing orchestrator intake, because the input schema correctly rejects null `feature_mapping_output` at intake before the skill runs.

| Metric | Expected | Notes |
|---|---|---|
| CFB count | 0 | TG gate failure is not a Claims Firewall breach. |
| `traceability_gate_passed` | **False** | The authoritative schema signal for an incomplete review. |
| Classification | **Rejected** | TG-3 Fail overrides classification regardless of PCS or CTCS. |

**Regression alert:** Any output with `traceability_gate_passed = True` when `feature_mapping_output` is absent has failed the TG-3 secondary enforcement. Any output with a non-Rejected classification when `traceability_gate_passed = False` has violated the mandatory gate contract.

---

## 2. Structural Requirements

Every proposal review output must contain all ten required sections. The `regression_tester.py` script checks for the following headers in every output document:

```json
{
  "skill_name": "ethana-proposal-review",
  "pass_threshold": 95,
  "required_headers": [
    "## 1. Executive Assessment",
    "## 2. Claim Inventory",
    "## 3. Claim Traceability Matrix",
    "## 4. Capability Status Validation",
    "## 5. Regulatory Coverage Validation",
    "## 6. Control Coverage Validation",
    "## 7. Commercial Risk Register",
    "## 8. Critical Firewall Breaches",
    "## 9. Major Risk Findings (Consolidated)",
    "## 10. Release Decision"
  ],
  "required_tables": [
    {
      "preceding_header": "## 2. Claim Inventory",
      "required_columns": ["Claim ID", "Claim text", "Claim type", "Proposal section"]
    },
    {
      "preceding_header": "## 3. Claim Traceability Matrix",
      "required_columns": ["Claim ID", "Upstream source", "Traceability status"]
    },
    {
      "preceding_header": "## 4. Capability Status Validation",
      "required_columns": ["Capability name", "Canonical model status", "Firewall determination"]
    },
    {
      "preceding_header": "## 10. Release Decision",
      "required_columns": ["Gate", "Step", "Status"]
    }
  ]
}
```

**PR-002 — CTCS arithmetic requirement:** Every Section 10 Markdown block must contain a `CTCS numerator` label and a `CTCS denominator` label. The values must satisfy: `round(ctcs_numerator / ctcs_denominator × 100, 1) == ctcs` (when `ctcs_denominator > 0`). These fields are computed from non-roadmap claims only, before roadmap augmentation. They are not equal to `traced_count` and `total_claims_audited` when roadmap items are present in the proposal.

---

## 3. Absolute Release Rule Verification

For every test fixture where `expected_cfb_count > 0`, the regression tester must verify:

1. `classification` in the output payload equals `"Rejected"`
2. `pcs` in the output payload equals `0`
3. Section 8 contains at least `expected_cfb_count` CFB entries
4. Section 10 Release Classification text reads "Rejected"

Any output that passes these fixtures with a non-Rejected classification when CFBs are present fails the regression suite regardless of all other scores.

---

## 4. Baseline Update Protocol

This baseline must be updated when:
- A new test fixture is added to `evaluations/test-cases/proposal-review/`
- The PCS or CTCS thresholds in ADR-005 are revised
- The CTCS formula is updated in canonical skill documentation
- A calibration review reveals systematic drift in one or more score dimensions

Baseline updates require review by the Cursory Governance Team and must be committed with a rationale note in the commit message.
