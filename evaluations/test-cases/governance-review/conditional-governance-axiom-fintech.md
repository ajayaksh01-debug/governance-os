---
fixture_id: conditional-governance-axiom-fintech
skill: governance-review
description: >
  EU General Enterprise Limited-Risk customer-facing AI assistant. Standard input set —
  capability_validation_output absent. 12 mandatory controls across 3 domains; 2 mandatory
  controls never designed (CC-MGF). ISO 42001 major_gaps downgraded to GP-MGF Minor Finding.
  GTG-4 Noted absent. Tests Conditional Governance path with CC-MGFs, GP-MGF downgrade,
  and advisory gate absence handling.
expected_classification: Conditional Governance
expected_gas: 76
expected_ccr: 75.0
expected_ccr_numerator: 9.0
expected_ccr_denominator: 12
expected_cgc_count: 0
expected_mgf_count: 2
expected_minor_finding_count: 2
expected_high_risk_count: 1
expected_governance_gate_passed: true
expected_iso_42001_ams: 63
expected_iso_42001_ars: 61
expected_iso_42001_classification: Near Ready
expected_gtg4_status: Noted absent
input_completeness: Standard
sector: General Enterprise
jurisdictions: ["EU"]
ai_deployment_type: Limited-Risk
---

# Test Fixture: Conditional Governance — Axiom FinTech Ltd

## Context

**Client:** Axiom FinTech Ltd (fictional)
**Sector:** General Enterprise
**Jurisdictions:** EU
**AI Deployment Type:** Limited-Risk (customer-facing AI assistant)
**Deployment Model:** Cloud
**Input completeness:** Standard (capability_validation_output absent)

This fixture is the calibration anchor for the **Conditional Governance** classification path.
It demonstrates two CC-MGFs (mandatory controls never designed), GP-MGF downgrade, GTG-4 Noted
absent, and the classification threshold boundary (GAS 76 ≥ 65, CCR 75.0 ≥ 60, CGC 0).

---

## What This Fixture Tests

1. **CC-MGF identification:** Two mandatory controls present in `control_requirements` have no matching entry in `control_taxonomy_matrix` (never designed). Each → CC-MGF (−10 GAS, +1 mgf_count).
2. **GP-MGF downgrade (GR-001):** `iso_42001_output.major_gaps = 3` → 1 GP-MGF entry (GGP-IS-001) → downgraded to Minor Finding (−2 GAS). Does NOT add to mgf_count.
3. **ISO minor gaps → Minor Finding:** `iso_42001_output.minor_gaps = 4` → 1 Minor Finding (GGP-IS-002, −2 GAS).
4. **GTG-4 Noted absent:** `capability_validation_output` absent → GTG-4 = "Noted absent", NOT Fail. `governance_gate_passed` remains true.
5. **Section 8 absence notice:** When GTG-4 not passed, Section 8 must state CCR limitation, not leave the section empty.
6. **GAS arithmetic:** `100 − 0×15 − 2×10 − 2×2 = 76`
7. **CCR arithmetic:** Two mandatory controls not in taxonomy → not_implemented count = 2.
8. **Classification:** GAS 76 ≥ 65, CCR 75.0 ≥ 60, CGC 0, any MGF → Conditional Governance.

**Regression alert:** Any output with `mgf_count ≠ 2` has miscounted CC-MGFs (the 2 undesigned mandatory controls are the MGFs; the ISO major_gaps must be downgraded to a Minor Finding). Any output with `governance_gate_passed = false` has incorrectly failed GTG-4 — GTG-4 is advisory and its absence must be Noted, not Failed. Any output classifying this as Governance Ready has ignored the MGF count (MGF > 0 prevents Governance Ready).

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
      "applicability": "Limited-Risk AI — Art. 52 transparency obligations"
    }
  ],
  "applicable_frameworks": [
    {
      "name": "ISO 42001",
      "mandatory": true,
      "basis": "AI management system baseline"
    },
    {
      "name": "NIST AI RMF",
      "mandatory": false,
      "basis": "Best practice — optional for Limited-Risk"
    }
  ],
  "control_requirements": [
    {"control_name": "AI System Transparency Disclosure", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 52"},
    {"control_name": "Automated Decision Notification", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 52"},
    {"control_name": "User Rights Information", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 52"},
    {"control_name": "Explanation of AI-Generated Recommendations", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 52"},
    {"control_name": "Transparency Disclosure Statement", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 52"},
    {"control_name": "Data Minimisation Policy", "domain": "Data Governance", "mandatory": true, "source": "GDPR Art. 5"},
    {"control_name": "User Data Consent Management", "domain": "Data Governance", "mandatory": true, "source": "GDPR Art. 7"},
    {"control_name": "Data Retention Schedule", "domain": "Data Governance", "mandatory": true, "source": "GDPR Art. 5"},
    {"control_name": "Data Quality Assessment Process", "domain": "Data Governance", "mandatory": true, "source": "EU AI Act Art. 10"},
    {"control_name": "System Performance Monitoring", "domain": "Monitoring", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Incident Detection and Alerting", "domain": "Monitoring", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Continuous Risk Assessment", "domain": "Monitoring", "mandatory": true, "source": "EU AI Act Art. 9"}
  ]
}
```

### control_mapping_output

Note: `Transparency Disclosure Statement` and `Data Quality Assessment Process` are **absent** from the taxonomy — these are the two CC-MGFs (mandatory controls never designed).

```json
{
  "control_taxonomy_matrix": [
    {"control_name": "AI System Transparency Disclosure", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Automated Decision Notification", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "User Rights Information", "coverage_classification": "Customer-Owned Control"},
    {"control_name": "Explanation of AI-Generated Recommendations", "coverage_classification": "Partially Covered by Ethana"},
    {"control_name": "Data Minimisation Policy", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "User Data Consent Management", "coverage_classification": "Customer-Owned Control"},
    {"control_name": "Data Retention Schedule", "coverage_classification": "Partially Covered by Ethana"},
    {"control_name": "System Performance Monitoring", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Incident Detection and Alerting", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Continuous Risk Assessment", "coverage_classification": "Fully Covered by Ethana"}
  ],
  "evidence_registry": [
    {"evidence_id": "EVID-TP-01", "control_name": "AI System Transparency Disclosure", "source": "Ethana Guardrails"},
    {"evidence_id": "EVID-TP-02", "control_name": "Automated Decision Notification", "source": "Ethana Runtime Guardrails"},
    {"evidence_id": "EVID-TP-03", "control_name": "User Rights Information", "source": "Customer Privacy Policy"},
    {"evidence_id": "EVID-DG-01", "control_name": "Data Minimisation Policy", "source": "Ethana Data Controls"},
    {"evidence_id": "EVID-DG-02", "control_name": "User Data Consent Management", "source": "Customer Consent Platform"},
    {"evidence_id": "EVID-MN-01", "control_name": "System Performance Monitoring", "source": "Ethana Monitoring Dashboard"},
    {"evidence_id": "EVID-MN-02", "control_name": "Incident Detection and Alerting", "source": "Ethana Anomaly Detection"},
    {"evidence_id": "EVID-MN-03", "control_name": "Continuous Risk Assessment", "source": "Ethana Risk Monitor"}
  ]
}
```

### iso_42001_output

```json
{
  "ams": 63,
  "ars": 61,
  "critical_gaps": 0,
  "major_gaps": 3,
  "minor_gaps": 4,
  "certification_classification": "Near Ready",
  "critical_gap_ids": []
}
```

### capability_validation_output

`null` — not provided for this assessment.

### client_profile

```json
{
  "sector": "General Enterprise",
  "jurisdictions": ["EU"],
  "ai_deployment_type": "Limited-Risk",
  "deployment_model": "Cloud"
}
```

---

## Expected Output

### CCR Arithmetic

| Domain | Mandatory Controls | In Matrix | Implemented | Partially Implemented | Not in Matrix | Domain CCR |
|---|---|---|---|---|---|---|
| Transparency | 5 | 4 | 3 | 1 | 1 | 70.0 |
| Data Governance | 4 | 3 | 2 | 1 | 1 | 62.5 |
| Monitoring | 3 | 3 | 3 | 0 | 0 | 100.0 |
| **Total** | **12** | **10** | **8** | **2** | **2** | |

```
CCR denominator:       12
Implemented:           8 (6 Fully Covered by Ethana + 2 Customer-Owned Control)
Partially Implemented: 2 × 0.5 = 1.0
Not in matrix (gap):   2 (CC-MGFs — never designed)
CCR numerator:         9.0
CCR:                   round(9.0 / 12 × 100, 1) = 75.0
```

No domains below 50% — no CGC candidates from CCR analysis.
Transparency at 70.0% and Data Governance at 62.5% — both in MGF range (50–70%). Two mandatory controls never designed → CC-MGF (not CGC).

### GAS Arithmetic

```
GAS base:                         100
Missing mandatory frameworks:      0 × −15 = 0
Major Governance Findings (MGF):   2 × −10 = −20  (GGP-CM-001, GGP-CM-002)
Minor Governance Findings:         2 × −2  = −4
  GGP-IS-001 (GP-MGF downgraded)  −2  (from iso_42001_output.major_gaps = 3)
  GGP-IS-002 (iso minor gaps)     −2  (from iso_42001_output.minor_gaps = 4)
Critical Governance Gap present:   No
Final GAS:                         76
```

### Expected JSON Payload

```json
{
  "gas": 76,
  "ccr": 75.0,
  "ccr_numerator": 9.0,
  "ccr_denominator": 12,
  "cgc_count": 0,
  "mgf_count": 2,
  "minor_finding_count": 2,
  "high_risk_count": 1,
  "classification": "Conditional Governance",
  "governance_gate_passed": true,
  "iso_42001_ams": 63,
  "iso_42001_ars": 61,
  "iso_42001_classification": "Near Ready",
  "frameworks_assessed": ["EU AI Act", "ISO 42001", "NIST AI RMF"],
  "input_completeness": "Standard"
}
```

### GTG Gate Table

| Gate | Step | Status |
|---|---|---|
| GTG-1 | Regulatory scope confirmed | Pass |
| GTG-2 | Control mapping present | Pass |
| GTG-3 | Gap assessment present | Pass |
| GTG-4 | Capability alignment confirmed | **Noted absent** |
| GTG-5 | Risk register complete | Pass |
| GTG-6 | Evidence traceability confirmed | Pass |
| GTG-7 | Framework coverage confirmed | Pass |
