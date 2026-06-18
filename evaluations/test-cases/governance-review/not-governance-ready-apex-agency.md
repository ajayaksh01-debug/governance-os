---
fixture_id: not-governance-ready-apex-agency
skill: governance-review
description: >
  EU+UK Government High-Risk automated benefits eligibility decisions. All three required inputs
  present — intake passes. iso_42001_output provided with Significant Gaps classification (ams=41).
  15 mandatory controls across 4 domains; 6 not in taxonomy matrix. Model Risk domain CCR = 40.0%
  (below 50% CGC threshold) → CGC-001. governance_gate_passed = true — all mandatory GTG gates
  pass. Classification = Not Governance Ready driven solely by CGC absolute rule. Tests the pure
  CGC override scenario: all gates pass, gas = 0, ccr computed, runtime reaches COMPLETE.
expected_classification: Not Governance Ready
expected_gas: 0
expected_ccr: 53.3
expected_ccr_numerator: 8.0
expected_ccr_denominator: 15
expected_cgc_count: 1
expected_mgf_count: 3
expected_minor_finding_count: 2
expected_high_risk_count: 2
expected_governance_gate_passed: true
expected_iso_42001_ams: 41
expected_iso_42001_ars: 38
expected_iso_42001_classification: Significant Gaps
input_completeness: Standard
sector: Government
jurisdictions: ["EU", "UK"]
ai_deployment_type: High-Risk
---

# Test Fixture: Not Governance Ready — Apex Government Agency

## Context

**Client:** Apex Government Agency (fictional)
**Sector:** Government
**Jurisdictions:** EU, UK
**AI Deployment Type:** High-Risk (automated benefits eligibility decisions — EU AI Act Annex III)
**Deployment Model:** On-prem
**Input completeness:** Standard (capability_validation_output absent)

This fixture is the calibration anchor for the **Not Governance Ready** classification path.
It demonstrates the CGC absolute rule in its purest form: all four mandatory GTG gates pass,
`governance_gate_passed = true`, but `cgc_count = 1` (Model Risk domain CCR = 40.0%) forces
`gas = 0` and `classification = Not Governance Ready` regardless.

This is a stronger test of the CGC absolute rule than a scenario where a gate failure also
forces Not Governance Ready — here, CGC alone is the only reason for the negative verdict.

---

## What This Fixture Tests

1. **CGC from Model Risk domain CCR < 50%:** Model Risk domain at 40.0% (2 of 5 mandatory controls designed) → CGC-001. Domain below 50% CGC threshold.
2. **CGC absolute rule (GHD3):** `cgc_count = 1` → `gas = 0` regardless of arithmetic. Arithmetic result is 66, but final GAS is 0.
3. **CCR computed despite CGC (GHD4/GHD5):** CCR = 53.3 must be present in output even when classification = Not Governance Ready. CGC does not suppress CCR computation.
4. **governance_gate_passed = true with Not Governance Ready classification:** All four mandatory gates (GTG-1, GTG-2, GTG-3, GTG-7) pass. Gate passage does not prevent Not Governance Ready when CGC present. The CGC rule overrides classification independently of gate status.
5. **ISO 42001 pass-through (GHD6):** `output.iso_42001_ams == 41`, `output.iso_42001_ars == 38`, `output.iso_42001_classification == "Significant Gaps"` — values sourced from `iso_42001_output`, not recalculated.
6. **GP-MGF downgrade (GR-001):** `iso_42001_output.major_gaps = 6` → 1 GP-MGF entry (GGP-IS-001) → downgraded to Minor Finding (−2 GAS). Does NOT add to mgf_count.
7. **Not Governance Ready → COMPLETE state:** Unlike Proposal Review's Rejected (which halts), the runtime must proceed to package assembly and reach COMPLETE state. `HALTED_GOVERNANCE_INCOMPLETE` is reserved for system execution failures only.
8. **CGC domains do not generate duplicate MGFs:** The 3 undesigned Model Risk controls are subsumed into CGC-001 (domain rate < 50%). They do not also generate CC-MGFs. Only undesigned controls in non-CGC domains (Transparency, Human Oversight, Monitoring) generate MGFs.

**Regression alert:** Any output with `gas ≠ 0` when `cgc_count > 0` has violated the CGC absolute rule (GHD3). Any output with `ccr` absent or null has violated the CCR-always-computed rule. Any output with `governance_gate_passed = false` for these inputs has incorrectly failed a mandatory gate — all four mandatory gates pass with this input set. Any output with `classification ≠ "Not Governance Ready"` when `cgc_count > 0` has violated the CGC absolute rule. Any runtime that halts at a `HALTED_*` state for a Not Governance Ready classification has incorrectly modelled the state machine.

---

## Inputs

### regulatory_mapping_output

```json
{
  "applicable_regulations": [
    {
      "name": "EU AI Act",
      "jurisdiction": "EU",
      "status": "Confirmed",
      "applicability": "High-Risk AI — Annex III public sector automated decisions"
    },
    {
      "name": "UK CDEI AI Assurance Framework",
      "jurisdiction": "UK",
      "status": "Confirmed",
      "applicability": "Government sector AI deployment"
    }
  ],
  "applicable_frameworks": [
    {
      "name": "ISO 42001",
      "mandatory": true,
      "basis": "High-Risk AI — mandatory AIMS assessment"
    }
  ],
  "control_requirements": [
    {"control_name": "Model Risk Framework Policy", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Algorithmic Fairness Assessment", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 10"},
    {"control_name": "Human Oversight Procedure for Automated Decisions", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 14"},
    {"control_name": "Model Validation Protocol", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Model Performance Monitoring", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Transparency Disclosure Statement", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 13"},
    {"control_name": "AI System Notification to Citizens", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 52"},
    {"control_name": "Decision Explanation for Benefits Eligibility", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 13"},
    {"control_name": "Public Register of AI Systems", "domain": "Transparency", "mandatory": true, "source": "UK CDEI Framework"},
    {"control_name": "Human Review Procedure for Automated Decisions", "domain": "Human Oversight", "mandatory": true, "source": "EU AI Act Art. 14"},
    {"control_name": "Appeal and Redress Mechanism", "domain": "Human Oversight", "mandatory": true, "source": "EU AI Act Art. 14"},
    {"control_name": "Operator Intervention Capability", "domain": "Human Oversight", "mandatory": true, "source": "EU AI Act Art. 14"},
    {"control_name": "Escalation Protocol for High-Risk Decisions", "domain": "Human Oversight", "mandatory": true, "source": "UK CDEI Framework"},
    {"control_name": "Continuous Operational Monitoring", "domain": "Monitoring", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Post-Deployment Performance Review", "domain": "Monitoring", "mandatory": true, "source": "EU AI Act Art. 9"}
  ]
}
```

### control_mapping_output

Note: 6 mandatory controls are **absent** from the taxonomy — 3 in Model Risk, 1 in Transparency,
1 in Human Oversight, 1 in Monitoring. Model Risk domain has only 2 of 5 controls designed,
producing a 40.0% domain CCR — below the 50% CGC threshold.

```json
{
  "control_taxonomy_matrix": [
    {"control_name": "Model Risk Framework Policy", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Algorithmic Fairness Assessment", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Transparency Disclosure Statement", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "AI System Notification to Citizens", "coverage_classification": "Customer-Owned Control"},
    {"control_name": "Decision Explanation for Benefits Eligibility", "coverage_classification": "Partially Covered by Ethana"},
    {"control_name": "Human Review Procedure for Automated Decisions", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Appeal and Redress Mechanism", "coverage_classification": "Customer-Owned Control"},
    {"control_name": "Operator Intervention Capability", "coverage_classification": "Partially Covered by Ethana"},
    {"control_name": "Continuous Operational Monitoring", "coverage_classification": "Fully Covered by Ethana"}
  ],
  "evidence_registry": [
    {"evidence_id": "EVID-MR-01", "control_name": "Model Risk Framework Policy", "source": "Ethana Audit Log"},
    {"evidence_id": "EVID-MR-02", "control_name": "Algorithmic Fairness Assessment", "source": "Ethana Red Team Orchestrator"},
    {"evidence_id": "EVID-TR-01", "control_name": "Transparency Disclosure Statement", "source": "Ethana Guardrails"},
    {"evidence_id": "EVID-TR-02", "control_name": "AI System Notification to Citizens", "source": "Customer Notification System"},
    {"evidence_id": "EVID-HO-01", "control_name": "Human Review Procedure for Automated Decisions", "source": "Ethana Human-in-Loop Module"},
    {"evidence_id": "EVID-HO-02", "control_name": "Appeal and Redress Mechanism", "source": "Customer Appeals Process"},
    {"evidence_id": "EVID-MN-01", "control_name": "Continuous Operational Monitoring", "source": "Ethana Monitoring Dashboard"}
  ]
}
```

### iso_42001_output

Present. Agency has completed a basic ISO 42001 gap assessment but is at an early maturity stage
with significant gaps across management system clauses. No critical gaps identified in the ISO
assessment itself — the CGC derives from the Model Risk domain CCR rate, not from ISO gaps.

```json
{
  "ams": 41,
  "ars": 38,
  "critical_gaps": 0,
  "major_gaps": 6,
  "minor_gaps": 4,
  "certification_classification": "Significant Gaps",
  "critical_gap_ids": [],
  "ams_clause_scores": {
    "clause_4": 2.8,
    "clause_5": 2.1,
    "clause_6": 2.5,
    "clause_7": 2.0,
    "clause_8": 1.8,
    "clause_9": 1.5,
    "clause_10": 1.2
  }
}
```

### capability_validation_output

`null` — not provided.

### client_profile

```json
{
  "sector": "Government",
  "jurisdictions": ["EU", "UK"],
  "ai_deployment_type": "High-Risk",
  "deployment_model": "On-prem"
}
```

---

## Expected Output

### CCR Arithmetic

CCR is always computed and reported, including when `cgc_count > 0`. The CGC does not suppress
the CCR — it only forces `gas = 0` and `classification = Not Governance Ready`.

| Domain | Mandatory Controls | In Matrix | Implemented | Partially Implemented | Not in Matrix | Domain CCR |
|---|---|---|---|---|---|---|
| Model Risk | 5 | 2 | 2 | 0 | 3 | 40.0 ← CGC-001 |
| Transparency | 4 | 3 | 2 | 1 | 1 | 62.5 |
| Human Oversight | 4 | 3 | 2 | 1 | 1 | 62.5 |
| Monitoring | 2 | 1 | 1 | 0 | 1 | 50.0 |
| **Total** | **15** | **9** | **7** | **2** | **6** | |

```
CCR denominator:       15
Implemented:           7 (5 Fully Covered by Ethana + 2 Customer-Owned Control)
Partially Implemented: 2 × 0.5 = 1.0
Not in matrix (gap):   6 — mandatory controls never designed
CCR numerator:         8.0
CCR:                   round(8.0 / 15 × 100, 1) = 53.3
```

Model Risk domain = 40.0% — below 50% CGC threshold → CGC-001.

### GAS Arithmetic (shown for transparency; absolute rule applies)

```
GAS base:                         100
Missing mandatory frameworks:      0 × −15 = 0  (ISO 42001 assessed in Section 6)
Major Governance Findings (MGF):   3 × −10 = −30  (GGP-CM-003, GGP-CM-004, GGP-CM-005)
Minor Governance Findings:         2 × −2  = −4
  GGP-IS-001 (GP-MGF downgraded)  −2  (from iso_42001_output.major_gaps = 6)
  GGP-IS-002 (iso minor gaps)     −2  (from iso_42001_output.minor_gaps = 4)
Critical Governance Gap present:   YES — CGC count = 1
GAS arithmetic result:             [100 − 30 − 4 = 66]
Final GAS:                         0  [absolute rule — CGC present overrides arithmetic]
```

The 3 undesigned Model Risk controls (GGP-CM-002) are subsumed into CGC-001 and do not generate
additional MGFs. Only the undesigned controls in non-CGC domains (Transparency, Human Oversight,
Monitoring — one each) generate CC-MGFs: GGP-CM-003, GGP-CM-004, GGP-CM-005.

### Expected JSON Payload

```json
{
  "gas": 0,
  "ccr": 53.3,
  "ccr_numerator": 8.0,
  "ccr_denominator": 15,
  "cgc_count": 1,
  "cgc_ids": ["CGC-001"],
  "mgf_count": 3,
  "minor_finding_count": 2,
  "high_risk_count": 2,
  "classification": "Not Governance Ready",
  "governance_gate_passed": true,
  "iso_42001_ams": 41,
  "iso_42001_ars": 38,
  "iso_42001_classification": "Significant Gaps",
  "frameworks_assessed": ["EU AI Act", "UK CDEI AI Assurance Framework", "ISO 42001"],
  "input_completeness": "Standard"
}
```

### GTG Gate Table

| Gate | Step | Status |
|---|---|---|
| GTG-1 | Regulatory scope confirmed | Pass — EU AI Act and UK CDEI both Confirmed |
| GTG-2 | Control mapping present | Pass — `control_taxonomy_matrix` has 9 entries |
| GTG-3 | Gap assessment present | Pass — `iso_42001_output` present; `ams` = 41, `critical_gaps` = 0 |
| GTG-4 | Capability alignment confirmed | Noted absent — `capability_validation_output` not provided |
| GTG-5 | Risk register complete | Pass — CGC item has corresponding GRK entry with severity |
| GTG-6 | Evidence traceability confirmed | Noted absent — 7 evidence entries cover Implemented controls; 2 Partially Implemented without full evidence |
| GTG-7 | Framework coverage confirmed | Pass — EU AI Act, UK CDEI, and ISO 42001 all assessed to completion in Section 6 |

`governance_gate_passed: true` — GTG-1, GTG-2, GTG-3, and GTG-7 all pass.
Classification = Not Governance Ready is driven solely by CGC-001. Gate passage is irrelevant
when any CGC is present.

### CGC Register

| CGC ID | Source | Domain | Description |
|---|---|---|---|
| CGC-001 | Control Coverage Assessment | Model Risk | Domain implementation rate 40.0% — 2 of 5 mandatory controls designed; below 50% CGC threshold |

### State Machine Requirement

The run must reach `COMPLETE` state after approval, not halt at any `HALTED_*` state due to
the Not Governance Ready classification. The Not Governance Ready Governance Readiness Certificate
is the deliverable. `HALTED_GOVERNANCE_INCOMPLETE` is reserved for system execution failures only.

This is the key behavioural difference from Proposal Review: a Rejected classification in
Proposal Review halts the run. Not Governance Ready in Governance Review does not.
