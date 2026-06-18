---
fixture_id: governance-ready-meridian-bank
skill: governance-review
description: >
  EU+UK BFSI High-Risk credit scoring AI. Full input set including capability_validation_output.
  18 mandatory controls across 4 domains. All GTG gates pass. GP-MGF downgraded to Minor Finding
  under GR-001 calibration. Tests the Governance Ready path with GP-MGF downgrade, CCR arithmetic
  identity, ISO 42001 pass-through, and full GTG gate table pass.
expected_classification: Governance Ready
expected_gas: 94
expected_ccr: 91.7
expected_ccr_numerator: 16.5
expected_ccr_denominator: 18
expected_cgc_count: 0
expected_mgf_count: 0
expected_minor_finding_count: 3
expected_high_risk_count: 0
expected_governance_gate_passed: true
expected_iso_42001_ams: 82
expected_iso_42001_ars: 76
expected_iso_42001_classification: Certification Ready
input_completeness: Full
sector: BFSI
jurisdictions: ["EU", "UK"]
ai_deployment_type: High-Risk
---

# Test Fixture: Governance Ready — Meridian Private Bank

## Context

**Client:** Meridian Private Bank (fictional)
**Sector:** BFSI
**Jurisdictions:** EU, UK
**AI Deployment Type:** High-Risk (credit scoring — EU AI Act Annex III)
**Deployment Model:** Customer VPC
**Input completeness:** Full (all four upstream inputs available)

This fixture is the primary calibration anchor for the **Governance Ready** classification path.
It demonstrates GP-MGF downgrade under GR-001 (the ISO 42001 major gap is classified as a
Minor Finding, not an MGF), allowing MGF count = 0 and enabling Governance Ready.

---

## What This Fixture Tests

1. **GP-MGF downgrade (GR-001):** `iso_42001_output.major_gaps = 1` must produce `minor_finding_count += 1` and NOT `mgf_count += 1`. The -2 GAS deduction applies (not -10). This is the defining GR-001 calibration decision.
2. **CCR arithmetic identity (GHD5):** `round(16.5 / 18 × 100, 1) == 91.7`
3. **ISO 42001 pass-through (GHD6):** `output.iso_42001_ams == 82`, `output.iso_42001_ars == 76`, `output.iso_42001_classification == "Certification Ready"` — values sourced from `iso_42001_output`, not recalculated.
4. **Full GTG gate table pass:** All 7 gates pass (GTG-4 passes because `capability_validation_output` is present).
5. **GAS arithmetic:** `100 − 0×15 − 0×10 − 3×2 = 94`
6. **Classification boundary:** GAS 94 ≥ 85, CCR 91.7 ≥ 80, CGC 0, MGF 0, High Risks 0 ≤ 1 → Governance Ready.

**Regression alert:** Any output with `mgf_count > 0` for this fixture has misapplied the GP-MGF rule — the ISO 42001 major gap must downgrade to a Minor Finding, not count as an MGF. Any output with `gas ≠ 94` has miscalculated the GAS arithmetic. Any output with `iso_42001_ams ≠ 82` has violated GHD6 (ISO pass-through).

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
      "applicability": "High-Risk AI — Annex III credit scoring"
    },
    {
      "name": "UK FCA Model Risk Guidance",
      "jurisdiction": "UK",
      "status": "Confirmed",
      "applicability": "BFSI sector — model governance"
    }
  ],
  "applicable_frameworks": [
    {
      "name": "ISO 42001",
      "mandatory": true,
      "basis": "High-Risk AI deployment"
    }
  ],
  "control_requirements": [
    {"control_name": "Model Risk Framework Policy", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Model Validation Protocol", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Credit Decision Audit Trail", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 12"},
    {"control_name": "Real-Time Model Performance Dashboard", "domain": "Model Risk", "mandatory": true, "source": "UK FCA MRG"},
    {"control_name": "Model Explainability Documentation", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 13"},
    {"control_name": "Adversarial Probe Coverage", "domain": "Model Risk", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Data Quality Assessment Process", "domain": "Data Governance", "mandatory": true, "source": "EU AI Act Art. 10"},
    {"control_name": "PII Detection and Output Sanitisation", "domain": "Data Governance", "mandatory": true, "source": "UK GDPR Art. 25"},
    {"control_name": "Data Retention and Lifecycle Policy", "domain": "Data Governance", "mandatory": true, "source": "UK GDPR Art. 5"},
    {"control_name": "Training Data Lineage Documentation", "domain": "Data Governance", "mandatory": true, "source": "EU AI Act Art. 10"},
    {"control_name": "Data Access Controls", "domain": "Data Governance", "mandatory": true, "source": "UK GDPR Art. 32"},
    {"control_name": "Transparency Disclosure Statement", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 13"},
    {"control_name": "Automated Decision Explanation", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 13"},
    {"control_name": "Human Oversight Notification", "domain": "Transparency", "mandatory": true, "source": "EU AI Act Art. 14"},
    {"control_name": "Regulatory Reporting Interface", "domain": "Transparency", "mandatory": true, "source": "UK FCA MRG"},
    {"control_name": "Real-Time Anomaly Detection", "domain": "Monitoring", "mandatory": true, "source": "EU AI Act Art. 9"},
    {"control_name": "Regulatory Threshold Alerting", "domain": "Monitoring", "mandatory": true, "source": "UK FCA MRG"},
    {"control_name": "Continuous Performance Review", "domain": "Monitoring", "mandatory": true, "source": "EU AI Act Art. 9"}
  ]
}
```

### control_mapping_output

```json
{
  "control_taxonomy_matrix": [
    {"control_name": "Model Risk Framework Policy", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Model Validation Protocol", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Credit Decision Audit Trail", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Real-Time Model Performance Dashboard", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Model Explainability Documentation", "coverage_classification": "Covered by Cursory Service"},
    {"control_name": "Adversarial Probe Coverage", "coverage_classification": "Partially Covered by Ethana"},
    {"control_name": "Data Quality Assessment Process", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "PII Detection and Output Sanitisation", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Data Retention and Lifecycle Policy", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Training Data Lineage Documentation", "coverage_classification": "Covered by Cursory Service"},
    {"control_name": "Data Access Controls", "coverage_classification": "Partially Covered by Ethana"},
    {"control_name": "Transparency Disclosure Statement", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Automated Decision Explanation", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Human Oversight Notification", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Regulatory Reporting Interface", "coverage_classification": "Covered by Cursory Service"},
    {"control_name": "Real-Time Anomaly Detection", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Regulatory Threshold Alerting", "coverage_classification": "Fully Covered by Ethana"},
    {"control_name": "Continuous Performance Review", "coverage_classification": "Partially Covered by Ethana"}
  ],
  "evidence_registry": [
    {"evidence_id": "EVID-MR-01", "control_name": "Model Risk Framework Policy", "source": "Ethana Audit Log v2.1"},
    {"evidence_id": "EVID-MR-02", "control_name": "Model Validation Protocol", "source": "Ethana Red Team Orchestrator"},
    {"evidence_id": "EVID-MR-03", "control_name": "Credit Decision Audit Trail", "source": "Ethana Immutable Audit Log"},
    {"evidence_id": "EVID-MR-04", "control_name": "Real-Time Model Performance Dashboard", "source": "Ethana LLM Gateway Metrics"},
    {"evidence_id": "EVID-MR-05", "control_name": "Model Explainability Documentation", "source": "Cursory Advisory Deliverable"},
    {"evidence_id": "EVID-DG-01", "control_name": "Data Quality Assessment Process", "source": "Ethana Data Pipeline Controls"},
    {"evidence_id": "EVID-DG-02", "control_name": "PII Detection and Output Sanitisation", "source": "Ethana PII Scanner"},
    {"evidence_id": "EVID-DG-03", "control_name": "Data Retention and Lifecycle Policy", "source": "Ethana Data Lifecycle Manager"},
    {"evidence_id": "EVID-DG-04", "control_name": "Training Data Lineage Documentation", "source": "Cursory Data Governance Advisory"},
    {"evidence_id": "EVID-TR-01", "control_name": "Transparency Disclosure Statement", "source": "Ethana Guardrails Output"},
    {"evidence_id": "EVID-TR-02", "control_name": "Automated Decision Explanation", "source": "Ethana LLM Gateway Explanation API"},
    {"evidence_id": "EVID-TR-03", "control_name": "Human Oversight Notification", "source": "Ethana Runtime Guardrails"},
    {"evidence_id": "EVID-TR-04", "control_name": "Regulatory Reporting Interface", "source": "Cursory Reporting Framework"},
    {"evidence_id": "EVID-MN-01", "control_name": "Real-Time Anomaly Detection", "source": "Ethana LLM Gateway Anomaly Module"},
    {"evidence_id": "EVID-MN-02", "control_name": "Regulatory Threshold Alerting", "source": "Ethana Monitoring Dashboard"}
  ]
}
```

### iso_42001_output

```json
{
  "ams": 82,
  "ars": 76,
  "critical_gaps": 0,
  "major_gaps": 1,
  "minor_gaps": 2,
  "certification_classification": "Certification Ready",
  "critical_gap_ids": [],
  "ams_clause_scores": {
    "clause_4": 4.2,
    "clause_5": 3.8,
    "clause_6": 4.0,
    "clause_7": 3.9,
    "clause_8": 4.1,
    "clause_9": 3.7,
    "clause_10": 3.5
  }
}
```

### capability_validation_output

```json
{
  "allowed_claims": [
    {"claim": "LLM Gateway rate limiting and content policy enforcement", "cpl": "CPL-1"},
    {"claim": "LLM Gateway prompt logging", "cpl": "CPL-1"},
    {"claim": "LLM Gateway anomaly detection", "cpl": "CPL-1"},
    {"claim": "Immutable Audit Log — application-layer audit trail", "cpl": "CPL-2"},
    {"claim": "Immutable Audit Log — event retention", "cpl": "CPL-2"},
    {"claim": "Immutable Audit Log — regulatory export", "cpl": "CPL-2"},
    {"claim": "Runtime Guardrails PII Scanner — text modality", "cpl": "CPL-1"},
    {"claim": "Red Teaming Orchestrator — 21 adversarial probes (Production)", "cpl": "CPL-1"}
  ],
  "prohibited_claims": [
    {"claim": "SOC 2 certified", "reason": "Not certified — assessment in progress"},
    {"claim": "Visual Agent Builder — production ready", "reason": "In Build"}
  ]
}
```

### client_profile

```json
{
  "sector": "BFSI",
  "jurisdictions": ["EU", "UK"],
  "ai_deployment_type": "High-Risk",
  "deployment_model": "Customer VPC"
}
```

---

## Expected Output

### CCR Arithmetic

| Domain | Mandatory Controls | Implemented | Partially Implemented | Third-Party Gap | Domain CCR |
|---|---|---|---|---|---|
| Model Risk | 6 | 5 | 1 | 0 | 91.7 |
| Data Governance | 5 | 4 | 1 | 0 | 90.0 |
| Transparency | 4 | 4 | 0 | 0 | 100.0 |
| Monitoring | 3 | 2 | 1 | 0 | 83.3 |
| **Total** | **18** | **15** | **3** | **0** | |

```
CCR denominator:       18
Implemented:           15 (12 Fully Covered by Ethana + 3 Covered by Cursory Service)
Partially Implemented: 3 × 0.5 = 1.5
CCR numerator:         16.5
CCR:                   round(16.5 / 18 × 100, 1) = 91.7
```

### GAS Arithmetic

```
GAS base:                         100
Missing mandatory frameworks:      0 × −15 = 0
Major Governance Findings (MGF):   0 × −10 = 0
Minor Governance Findings:         3 × −2  = −6
  GGP-IS-001 (GP-MGF downgraded)  −2
  GGP-IS-002 (iso minor gap 1)    −2
  GGP-IS-003 (iso minor gap 2)    −2
Critical Governance Gap present:   No
Final GAS:                         94
```

### Expected JSON Payload

```json
{
  "gas": 94,
  "ccr": 91.7,
  "ccr_numerator": 16.5,
  "ccr_denominator": 18,
  "cgc_count": 0,
  "mgf_count": 0,
  "minor_finding_count": 3,
  "high_risk_count": 0,
  "classification": "Governance Ready",
  "governance_gate_passed": true,
  "iso_42001_ams": 82,
  "iso_42001_ars": 76,
  "iso_42001_classification": "Certification Ready",
  "frameworks_assessed": ["EU AI Act", "UK FCA Model Risk Guidance", "ISO 42001"],
  "input_completeness": "Full"
}
```

### GTG Gate Table

| Gate | Step | Status |
|---|---|---|
| GTG-1 | Regulatory scope confirmed | Pass |
| GTG-2 | Control mapping present | Pass |
| GTG-3 | Gap assessment present | Pass |
| GTG-4 | Capability alignment confirmed | Pass |
| GTG-5 | Risk register complete | Pass |
| GTG-6 | Evidence traceability confirmed | Pass |
| GTG-7 | Framework coverage confirmed | Pass |
