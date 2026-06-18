# Governance Review — Worked Examples

These three examples are the calibration anchors for this skill. Each example demonstrates a complete review output across the ten sections — or the sections most critical to the scenario's primary challenge. Read these before scoring any live review.

Example 1 demonstrates a Governance Ready outcome with full input coverage. Example 2 demonstrates a Conditional Governance outcome with Major Governance Findings. Example 3 demonstrates a Not Governance Ready outcome driven by a mandatory gate failure and a Critical Governance Gap.

---

## Example 1: Governance Ready — Meridian Private Bank

**Demonstrates:** Full CCR arithmetic; all mandatory GTG gates pass; ISO 42001 pass-through values; Governance Ready classification with minor finding.

### Input

```
Client:                       Meridian Private Bank (fictional)
Sector:                       BFSI
Jurisdictions:                EU, UK
AI Deployment Type:           High-Risk (credit scoring — EU AI Act Annex III)
Deployment Model:             Customer VPC

regulatory_mapping_output:    Available
  applicable_regulations:     EU AI Act (Confirmed), UK FCA Model Risk Guidance (Confirmed)
  applicable_frameworks:      ISO 42001
  control_requirements:       18 mandatory controls across 4 domains:
                               Model Risk (6), Data Governance (5), Transparency (4), Monitoring (3)

control_mapping_output:       Available
  control_taxonomy_matrix:    18 entries (all 18 mandatory controls mapped):
                               12 × Fully Covered by Ethana
                                3 × Covered by Cursory Service
                                3 × Partially Covered by Ethana
                                0 × Third-Party Control Required
                                0 × Customer-Owned Control
  evidence_registry:          14 entries covering all Implemented controls

iso_42001_output:             Available
  ams:                        82
  ars:                        76
  critical_gaps:              0
  major_gaps:                 1
  minor_gaps:                 2
  certification_classification: Certification Ready
  critical_gap_ids:           []
  ams_clause_scores:          clause_4: 4.2, clause_5: 3.8, clause_6: 4.0, clause_7: 3.9,
                               clause_8: 4.1, clause_9: 3.7, clause_10: 3.5

capability_validation_output: Available
  allowed_claims:             8 claims (CPL-1 and CPL-2) across LLM Gateway,
                               Audit Log, Guardrails, Red Teaming Orchestrator
  prohibited_claims:          2 claims (SOC 2 certified, Visual Agent Builder)

client_profile:               sector: BFSI, jurisdictions: [EU, UK],
                               ai_deployment_type: High-Risk, deployment_model: Customer VPC

Input completeness:           Full
```

---

### Section 2 — Regulatory Scope and Framework Matrix

| Entry | Type | Jurisdiction | Mandatory | Status |
|---|---|---|---|---|
| EU AI Act | Regulation | EU | Yes — High-Risk AI in Annex III | Confirmed |
| UK FCA Model Risk Guidance | Regulation | UK | Yes — BFSI sector | Confirmed |
| ISO 42001 | Framework | Global | Yes — High-Risk AI deployment | Assessed |

No entries excluded from assessment. All confirmed mandatory items assessed to completion.

---

### Section 3 — Control Coverage Assessment

**Denominator:** 18 mandatory controls from `regulatory_mapping_output.control_requirements`

| Domain | Mandatory Controls | Implemented | Partially Implemented | Third-Party Gap | Domain CCR |
|---|---|---|---|---|---|
| Model Risk | 6 | 5 | 1 | 0 | (5 + 0.5) / 6 × 100 = 91.7 |
| Data Governance | 5 | 4 | 1 | 0 | (4 + 0.5) / 5 × 100 = 90.0 |
| Transparency | 4 | 4 | 0 | 0 | 4 / 4 × 100 = 100.0 |
| Monitoring | 3 | 2 | 1 | 0 | (2 + 0.5) / 3 × 100 = 83.3 |
| **Total** | **18** | **15** | **3** | **0** | |

**CCR arithmetic:**

```
CCR denominator:              18 (mandatory controls)
Implemented:                  15 (12 Fully Covered by Ethana + 3 Covered by Cursory Service)
Partially Implemented:        3 × 0.5 = 1.5
Third-Party Required (gap):   0
CCR numerator:                15 + 1.5 = 16.5
CCR:                          round(16.5 / 18 × 100, 1) = round(91.7, 1) = 91.7
```

No domains below 50% — no CGC candidates from CCR analysis. All domains above 70% — no MGF candidates from CCR analysis.

---

### Section 4 — Governance Gap Register

ISO 42001 `critical_gap_ids` is empty. No Critical severity gaps from the ISO 42001 upstream output.

| Gap ID | Description | Source | Severity | Domain | Remediation Category |
|---|---|---|---|---|---|
| GGP-IS-001 | ISO 42001 Clause 10 (Improvement) — Major gap: no formal nonconformity tracking process documented | ISO 42001 Gap Assessment | Major | Management System | Process |
| GGP-IS-002 | ISO 42001 Clause 9 (Performance Evaluation) — Minor gap: internal audit schedule defined but not yet executed | ISO 42001 Gap Assessment | Minor | Management System | Process |
| GGP-IS-003 | ISO 42001 Clause 9 (Performance Evaluation) — Minor gap: management review evidence incomplete | ISO 42001 Gap Assessment | Minor | Management System | Evidence |

GGP-IS-001 is a Gap/Process Major Governance Finding (GP-MGF) (sourced from `iso_42001_output.major_gaps`). Per GR-001 calibration, GP-MGF is downgraded and classified as a Minor Governance Finding, carrying a -2 GAS deduction and not counting as an MGF.

CGC count: 0.

---

### Section 5 — Governance Risk Register

| Risk ID | Description | Severity | Residual After Controls | Owner | Status |
|---|---|---|---|---|---|
| GRK-001 | Nonconformity tracking gap (GGP-IS-001) — model risk decisions may not be formally documented and escalated | Medium | Low (controls reduce exposure; gap is in process documentation, not technical controls) | Chief Risk Officer | Residual |
| GRK-002 | Internal audit not yet executed (GGP-IS-002) — ISO 42001 control effectiveness unconfirmed | Low | Low | Head of AI Governance | Accepted |

High risk count: 0.

---

### Section 6 — Framework Compliance Scores

**EU AI Act:**
- Transparency obligations: Compliant (all 4 transparency controls Fully Covered)
- Risk management: Partial (3 of 4 Model Risk controls Fully Covered; 1 Partially)
- Technical documentation: Compliant
- Human oversight: Compliant
- Overall: Near-Compliant — one Model Risk control requires completion

**UK FCA Model Risk Guidance:**
- Model governance: Compliant
- Model validation: Partial (Monitoring domain — 2 of 3 controls Fully Covered; 1 Partially)
- Data quality: Compliant
- Overall: Near-Compliant — one Monitoring control requires completion

**ISO 42001:**
- AMS: 82 / 100 (sourced from `iso_42001_output.ams` — not recalculated)
- ARS: 76 / 100 (sourced from `iso_42001_output.ars` — not recalculated)
- Certification Classification: Certification Ready (sourced from `iso_42001_output.certification_classification`)
- Clause scores (from `ams_clause_scores`): Cl.4: 4.2, Cl.5: 3.8, Cl.6: 4.0, Cl.7: 3.9, Cl.8: 4.1, Cl.9: 3.7, Cl.10: 3.5
- Overall: ISO 42001 Certification Ready. One Major gap (Clause 10 improvement process).

All three entries assessed to completion — GTG-7 condition satisfied.

---

### Section 7 — Governance TG Gate Table

| Gate | Step | Status |
|---|---|---|
| GTG-1 | Regulatory scope confirmed | **Pass** — `applicable_regulations` non-empty; EU AI Act and UK FCA MRG both status = Confirmed |
| GTG-2 | Control mapping present | **Pass** — `control_taxonomy_matrix` has 18 entries; all 18 mandatory controls mapped |
| GTG-3 | Gap assessment present | **Pass** — `iso_42001_output` present; `ams` = 82, `critical_gaps` = 0 |
| GTG-4 | Capability alignment confirmed | **Pass** — `capability_validation_output` present; 8 `allowed_claims` mapped to 3 control domains in Section 8 |
| GTG-5 | Risk register complete | **Pass** — Section 5 populated; both MGF-derived gaps (GGP-IS-001) have GRK entries |
| GTG-6 | Evidence traceability confirmed | **Pass** — all 15 Implemented controls cite `evidence_id` from `evidence_registry` |
| GTG-7 | Framework coverage confirmed | **Pass** — Section 6 has 3 entries; all assessed to completion (at least one domain rated) |

`governance_gate_passed: true`

---

### Section 8 — Capability Governance Alignment

| Capability (from `allowed_claims`) | Control Domains Addressed | Mandatory Controls Satisfied | CCR Contribution |
|---|---|---|---|
| LLM Gateway (CPL-1) | Model Risk, Monitoring | 4 mandatory controls — rate limiting, content policy, prompt logging, anomaly detection | Implemented (Fully Covered by Ethana) |
| Immutable Audit Log (CPL-2) | Data Governance, Transparency | 3 mandatory controls — audit trail, event retention, regulatory export | Implemented (Fully Covered by Ethana — note: application-layer only caveat embedded per CPL-2 requirement) |
| Runtime Guardrails — PII Scanner (CPL-1) | Data Governance | 2 mandatory controls — PII detection, output sanitisation | Implemented (Fully Covered by Ethana — text modality only; structured database fields require supplementary control) |
| Red Teaming Orchestrator (CPL-1) | Model Risk | 1 mandatory control — adversarial probe coverage | Partially Implemented (Partially Covered by Ethana — 21 probes Production; CI/CD gate integration In Build) |

Control gaps where no validated Ethana capability provides coverage:
- Model risk explainability documentation (1 mandatory control) — covered by Cursory AI Governance Advisory service

---

### Section 10 — Governance Release Decision

**Traceability Gate:** GTG-1 through GTG-7 all Pass.

**GAS arithmetic:**

```
GAS base:                          100
Missing mandatory frameworks:       0 (all 3 assessed in Section 6)
Major Governance Findings:          0 × −10 = 0
Minor Governance Findings:          3 × −2  = −6 (GGP-IS-001, GGP-IS-002, GGP-IS-003)
Critical Governance Gap present:    No
Final GAS:                          100 − 6 = 94
```

**CCR arithmetic:**

```
CCR denominator:      18 (mandatory controls from regulatory_mapping_output)
Implemented:          15
Partially Implemented: 3 × 0.5 = 1.5
CCR numerator:        16.5
CCR:                  round(16.5 / 18 × 100, 1) = 91.7
```

**Supporting scores:**

```
AIMS Maturity Score (AMS):        82 / 100  (from iso_42001_output)
Audit Readiness Score (ARS):      76 / 100  (from iso_42001_output)
ISO 42001 Classification:         Certification Ready
```

**Classification check:**

```
GAS 94 ≥ 85 ✓
CCR 91.7 ≥ 80 ✓
CGC count: 0 ✓
MGF count: 0 ✓
High Risks: 0 ≤ 1 ✓
```

Under GR-001 calibration, GP-MGF items (such as the ISO 42001 Clause 10 Major gap, GGP-IS-001) are downgraded and classified as Minor Findings. Therefore:
MGF count: 0
Minor finding count: 3 (GGP-IS-001, GGP-IS-002, GGP-IS-003)
High Risks: 0 ≤ 1

Correct classification: Governance Ready

GAS 94 ≥ 85 ✓, CCR 91.7 ≥ 80 ✓, CGC 0 ✓, MGF = 0 ✓, High Risks 0 ≤ 1 ✓.

This is the correct outcome. With GGP-IS-001 classified as a Minor Finding under GR-001, Meridian meets all requirements for a Governance Ready classification.

```
Governance Review — Readiness Certificate
──────────────────────────────────────────────────────────────────
Client:                       Meridian Private Bank — Credit AI Governance Assessment
Review date:                  [assessment date]
AIMS Maturity Score (AMS):    82 / 100
Audit Readiness Score (ARS):  76 / 100
ISO 42001 Classification:     Certification Ready
CCR:                          91.7 / 100 (16.5 / 18 × 100)
GAS:                          94 / 100
CGC count:                    0
MGF count:                    0
Minor Finding count:          3 (GGP-IS-001, GGP-IS-002, GGP-IS-003)
High Residual Risks:          0
governance_gate_passed:       true
Governance Readiness:         GOVERNANCE READY
──────────────────────────────────────────────────────────────────
Required actions before next scheduled review:
1. [Before Certification] GRA-001: Implement formal nonconformity tracking and escalation
   process for model risk decisions. Addresses GGP-IS-001, GRK-001.
   Priority: Before Certification. Responsible: Head of AI Governance. Effort: Weeks.
──────────────────────────────────────────────────────────────────
```

**Calibration note:** This example demonstrates a Governance Ready outcome. With GGP-IS-001 classified as a Minor Finding under GR-001, GAS reaches 94 and MGF count is 0, satisfying the requirements for Governance Ready classification.

---

## Example 2: Conditional Governance — Axiom FinTech

**Demonstrates:** MGF identification for mandatory controls never designed; GTG-4 noted absent; Section 8 absence notice; Conditional Governance classification.

### Input

```
Client:                       Axiom FinTech Ltd (fictional)
Sector:                       General Enterprise
Jurisdictions:                EU
AI Deployment Type:           Limited-Risk (customer-facing AI assistant)
Deployment Model:             Cloud

regulatory_mapping_output:    Available
  applicable_regulations:     EU AI Act (Confirmed, Limited-Risk obligations)
  applicable_frameworks:      ISO 42001, NIST AI RMF
  control_requirements:       12 mandatory controls across 3 domains:
                               Transparency (5), Data Governance (4), Monitoring (3)

control_mapping_output:       Available
  control_taxonomy_matrix:    10 entries (2 mandatory controls absent from matrix — never designed)
                                6 × Fully Covered by Ethana
                                2 × Customer-Owned Control
                                2 × Partially Covered by Ethana
  evidence_registry:          8 entries

iso_42001_output:             Available
  ams:                        63
  ars:                        61
  critical_gaps:              0
  major_gaps:                 3
  minor_gaps:                 4
  certification_classification: Near Ready
  critical_gap_ids:           []

capability_validation_output: NOT PROVIDED

Input completeness:           Standard
```

---

### Section 3 — Control Coverage Assessment

**Denominator:** 12 mandatory controls from `control_requirements`

| Domain | Mandatory Controls | In Matrix | Implemented | Partially Implemented | Not in Matrix | Domain CCR |
|---|---|---|---|---|---|---|
| Transparency | 5 | 4 | 3 | 1 | 1 | (3 + 0.5) / 5 × 100 = 70.0 |
| Data Governance | 4 | 3 | 2 | 1 | 1 | (2 + 0.5) / 4 × 100 = 62.5 |
| Monitoring | 3 | 3 | 3 | 0 | 0 | 3 / 3 × 100 = 100.0 |
| **Total** | **12** | **10** | **8** | **2** | **2** | |

**CCR arithmetic:**

```
CCR denominator:              12 (mandatory controls)
Implemented:                  8 (6 Fully Covered by Ethana + 2 Customer-Owned Control)
Partially Implemented:        2 × 0.5 = 1.0
Not in matrix (gap):          2 — mandatory controls never designed
CCR numerator:                8 + 1.0 = 9.0
CCR:                          round(9.0 / 12 × 100, 1) = 75.0
```

No domains below 50% — no CGC candidates from CCR analysis. Transparency domain at 70.0% and Data Governance at 62.5% — both within MGF range (50–70%). However 70.0% is at the boundary; apply MGF criteria: two mandatory controls never designed in these domains → MGF.

---

### Section 4 — Governance Gap Register

ISO 42001 `critical_gap_ids` is empty. No Critical severity gaps from upstream.

| Gap ID | Description | Source | Severity | Domain | Remediation Category |
|---|---|---|---|---|---|
| GGP-CM-001 | Mandatory Transparency control `transparency_disclosure_statement` not present in `control_taxonomy_matrix` — required by EU AI Act Art. 52; never designed | Control Mapping | Major | Transparency | Process + Technical |
| GGP-CM-002 | Mandatory Data Governance control `data_quality_assessment_process` not present in `control_taxonomy_matrix` — required by EU AI Act Art. 10; never designed | Control Mapping | Major | Data Governance | Process |
| GGP-IS-001 | ISO 42001 — Major gap count: 3 (Clauses 8, 9, and 10 deficiencies identified in upstream gap register) | ISO 42001 Gap Assessment | Major | Management System | Process + Evidence |
| GGP-IS-002 | ISO 42001 — Minor finding: 4 minor gaps identified in upstream gap register | ISO 42001 Gap Assessment | Minor | Management System | Evidence |

GGP-CM-001 and GGP-CM-002 evaluated against CGC criteria: Transparency domain is 70.0% (above 50% CGC threshold) and Data Governance is 62.5% (above 50% threshold). These are MGFs, not CGCs.

CGC count: 0.

---

### Section 7 — Governance TG Gate Table

| Gate | Step | Status |
|---|---|---|
| GTG-1 | Regulatory scope confirmed | **Pass** — EU AI Act Confirmed |
| GTG-2 | Control mapping present | **Pass** — `control_taxonomy_matrix` has 10 entries |
| GTG-3 | Gap assessment present | **Pass** — `iso_42001_output` present; `ams` = 63, `critical_gaps` = 0 |
| GTG-4 | Capability alignment confirmed | **Noted absent** — `capability_validation_output` not provided |
| GTG-5 | Risk register complete | **Pass** — all MGF items have GRK entries |
| GTG-6 | Evidence traceability confirmed | **Pass** — all Implemented controls cited in `evidence_registry` |
| GTG-7 | Framework coverage confirmed | **Pass** — EU AI Act, ISO 42001, and NIST AI RMF all assessed in Section 6 |

`governance_gate_passed: true`

---

### Section 8 — Capability Governance Alignment

GTG-4 not passed — `capability_validation_output` was not provided. Section 8 cannot be completed. Capability governance alignment is unknown for this assessment. CCR reflects `control_taxonomy_matrix` entries only — controls attributed to Ethana capabilities in the matrix have not been independently validated against the canonical product model.

**Impact on CCR:** The CCR value of 75.0 assumes that all "Fully Covered by Ethana" entries in `control_taxonomy_matrix` represent accurate coverage. Without `capability_validation_output`, this assumption is unverified. A follow-up Capability Validation run is recommended before the next re-assessment.

---

### Section 10 — Governance Release Decision

**GAS arithmetic:**

```
GAS base:                          100
Missing mandatory frameworks:       0 (EU AI Act, ISO 42001, NIST AI RMF all assessed)
Major Governance Findings:          2 × −10 = −20 (GGP-CM-001, GGP-CM-002)
Minor Governance Findings:          2 × −2  = −4 (GGP-IS-001, GGP-IS-002)
Critical Governance Gap present:    No
Final GAS:                          100 − 20 − 4 = 76
```

**CCR arithmetic:**

```
CCR denominator:      12
Implemented:          8
Partially Implemented: 2 × 0.5 = 1.0
CCR numerator:        9.0
CCR:                  round(9.0 / 12 × 100, 1) = 75.0
```

```
Governance Review — Readiness Certificate
──────────────────────────────────────────────────────────────────
Client:                       Axiom FinTech Ltd — AI Assistant Governance Assessment
Review date:                  [assessment date]
AIMS Maturity Score (AMS):    63 / 100
Audit Readiness Score (ARS):  61 / 100
ISO 42001 Classification:     Near Ready
CCR:                          75.0 / 100 (9.0 / 12 × 100)
GAS:                          76 / 100
CGC count:                    0
MGF count:                    2 (GGP-CM-001, GGP-CM-002)
Minor Finding count:          2 (GGP-IS-001, GGP-IS-002)
High Residual Risks:          1
governance_gate_passed:       true
Governance Readiness:         CONDITIONAL GOVERNANCE
──────────────────────────────────────────────────────────────────
Required actions:
1. [Before Deployment] GRA-001: Design and implement transparency disclosure
   statement control. Addresses GGP-CM-001. Responsible: Head of AI Ethics.
   Effort: Weeks.
2. [Before Deployment] GRA-002: Design and implement data quality assessment
   process control. Addresses GGP-CM-002. Responsible: Data Governance Lead.
   Effort: Weeks.
3. [Before Certification] GRA-003: Address ISO 42001 Clause 8, 9, and 10 deficiencies
   per upstream Gap Register. Addresses GGP-IS-001. Responsible: AIMS Owner.
   Effort: Months.
──────────────────────────────────────────────────────────────────
```

---

## Example 3: Not Governance Ready — Apex Government Agency

**Demonstrates:** GTG-3 mandatory gate failure; CGC absolute rule (GAS = 0); CCR computed and reported even when `governance_gate_passed = false`; the two-guard pattern for GTG-3.

### Input

```
Client:                       Apex Government Agency (fictional)
Sector:                       Government
Jurisdictions:                EU, UK
AI Deployment Type:           High-Risk (automated benefits eligibility decisions)
Deployment Model:             On-prem

regulatory_mapping_output:    Available
  applicable_regulations:     EU AI Act (Confirmed, Annex III — public sector High-Risk AI)
                               UK CDEI AI Assurance Framework (Confirmed — Government sector)
  applicable_frameworks:      ISO 42001
  control_requirements:       15 mandatory controls across 4 domains:
                               Model Risk (5), Transparency (4), Human Oversight (4), Monitoring (2)

control_mapping_output:       Available
  control_taxonomy_matrix:    9 entries (6 mandatory controls absent — never designed)
                                5 × Fully Covered by Ethana
                                2 × Customer-Owned Control
                                2 × Partially Covered by Ethana
  evidence_registry:          7 entries

iso_42001_output:             NOT PROVIDED
                              (ai_deployment_type = High-Risk → absence is a CGC)

capability_validation_output: NOT PROVIDED

client_profile:               sector: Government, jurisdictions: [EU, UK],
                               ai_deployment_type: High-Risk, deployment_model: On-prem

Input completeness:           Standard (iso_42001_output absent — required for High-Risk AI)
```

**GTG-3 two-guard pattern:** The intake schema (`governance-review-input.schema.json`) requires `iso_42001_output` as type `object`. A null or absent value fails type validation at intake and halts the run at `HALTED_INTAKE_INVALID` before the skill executes. This test scenario exercises the executor's secondary enforcement: when called directly with `iso_42001_output = None`, the executor correctly sets GTG-3 = Fail, `governance_gate_passed = false`, and triggers the CGC (High-Risk AI without ISO 42001 assessment). CCR is still computed from the available inputs.

---

### Section 3 — Control Coverage Assessment

**CCR is computed even when `governance_gate_passed = false`.** The CCR value documents the control coverage posture for audit purposes and is required in Section 10.

**Denominator:** 15 mandatory controls from `control_requirements`

| Domain | Mandatory Controls | In Matrix | Implemented | Partially Implemented | Not in Matrix | Domain CCR |
|---|---|---|---|---|---|---|
| Model Risk | 5 | 2 | 2 | 0 | 3 | 2 / 5 × 100 = 40.0 |
| Transparency | 4 | 3 | 2 | 1 | 1 | (2 + 0.5) / 4 × 100 = 62.5 |
| Human Oversight | 4 | 3 | 2 | 1 | 1 | (2 + 0.5) / 4 × 100 = 62.5 |
| Monitoring | 2 | 1 | 1 | 0 | 1 | 1 / 2 × 100 = 50.0 |
| **Total** | **15** | **9** | **7** | **2** | **6** | |

**CCR arithmetic:**

```
CCR denominator:              15 (mandatory controls)
Implemented:                  7 (5 Fully Covered by Ethana + 2 Customer-Owned Control)
Partially Implemented:        2 × 0.5 = 1.0
Not in matrix (gap):          6 — mandatory controls never designed
CCR numerator:                7 + 1.0 = 8.0
CCR:                          round(8.0 / 15 × 100, 1) = 53.3
```

**CGC candidate — Model Risk domain:** Domain CCR = 40.0% — below the 50% CGC threshold. This is a CGC from CCR analysis, independent of the GTG-3 failure.

---

### Section 4 — Governance Gap Register

| Gap ID | Description | Source | Severity | Domain | Remediation Category |
|---|---|---|---|---|---|
| GGP-RM-001 | `iso_42001_output` not provided — ISO 42001 assessment required for High-Risk AI deployment; absence prevents AIMS maturity determination and GTG-3 evaluation | Governance Review (GTG-3 gate) | Critical → **CGC-001** | AI Management System | Assessment |
| GGP-CM-001 | Model Risk domain CCR = 40.0% — below 50% CGC threshold; 3 of 5 mandatory Model Risk controls have no design in `control_taxonomy_matrix` | Control Mapping | Critical → **CGC-002** | Model Risk | Process + Technical |
| GGP-CM-002 | 3 mandatory Model Risk controls not in `control_taxonomy_matrix` — human oversight procedure, model validation protocol, model performance monitoring | Control Mapping | Major | Model Risk | Process |
| GGP-CM-003 | 1 mandatory Transparency control not in `control_taxonomy_matrix` | Control Mapping | Major | Transparency | Process |
| GGP-CM-004 | 1 mandatory Human Oversight control not in `control_taxonomy_matrix` | Control Mapping | Major | Human Oversight | Process |
| GGP-CM-005 | 1 mandatory Monitoring control not in `control_taxonomy_matrix` | Control Mapping | Major | Monitoring | Technical |

**CGC count: 2** — GGP-RM-001 (missing ISO 42001 for High-Risk AI) and GGP-CM-001 (Model Risk domain below 50%).

**GAS = 0 — absolute rule applies.**

---

### Section 7 — Governance TG Gate Table

| Gate | Step | Status |
|---|---|---|
| GTG-1 | Regulatory scope confirmed | **Pass** — EU AI Act and UK CDEI both Confirmed |
| GTG-2 | Control mapping present | **Pass** — `control_taxonomy_matrix` has 9 entries |
| GTG-3 | Gap assessment present | **FAIL** — `iso_42001_output` not provided; `ams` and `critical_gaps` cannot be evaluated |
| GTG-4 | Capability alignment confirmed | **Noted absent** — `capability_validation_output` not provided |
| GTG-5 | Risk register complete | **Noted absent** — Risk register covers CGC items; complete risk register deferred to re-assessment when iso_42001_output available |
| GTG-6 | Evidence traceability confirmed | **Noted absent** — 7 Implemented controls cited; 2 Partially Implemented controls without full evidence traceability |
| GTG-7 | Framework coverage confirmed | **FAIL** — ISO 42001 framework in `applicable_frameworks` cannot be assessed in Section 6 without `iso_42001_output`; no framework assessed to completion across all domains |

`governance_gate_passed: false` — GTG-3 and GTG-7 mandatory gates both failed.

---

### Section 10 — Governance Release Decision

**GAS arithmetic:**

```
GAS base:                          100
[Not applied — CGC present, absolute rule]
Critical Governance Gap present:   YES — CGC count = 2
Final GAS:                         0  [absolute rule; arithmetic otherwise: 100 − 15 − 30 − 0 = 55]
```

GAS arithmetic is shown for transparency only. The final value is 0 per the absolute rule.

**CCR arithmetic (computed regardless of gate or CGC status):**

```
CCR denominator:      15
Implemented:          7
Partially Implemented: 2 × 0.5 = 1.0
CCR numerator:        8.0
CCR:                  round(8.0 / 15 × 100, 1) = 53.3
```

```
Governance Review — Readiness Certificate
──────────────────────────────────────────────────────────────────
Client:                       Apex Government Agency — Benefits AI Governance Assessment
Review date:                  [assessment date]
AIMS Maturity Score (AMS):    Not available — iso_42001_output not provided
Audit Readiness Score (ARS):  Not available — iso_42001_output not provided
ISO 42001 Classification:     Not assessed — GTG-3 failed
CCR:                          53.3 / 100 (8.0 / 15 × 100)
GAS:                          0 / 100 — Critical Governance Gap absolute rule
CGC count:                    2 (CGC-001: ISO 42001 absent for High-Risk AI;
                                 CGC-002: Model Risk domain CCR = 40.0%)
MGF count:                    3 (GGP-CM-003, GGP-CM-004, GGP-CM-005)
High Residual Risks:          2 (minimum — risk register cannot be completed without iso_42001_output)
governance_gate_passed:       false (GTG-3 and GTG-7 failed)
Governance Readiness:         NOT GOVERNANCE READY
──────────────────────────────────────────────────────────────────
Required actions — Immediate (blocks any positive classification):
1. [Immediate] GRA-001: Commission and complete ISO 42001 Gap Assessment.
   Addresses CGC-001, GGP-RM-001. Responsible: Head of AI Governance. Effort: Months.
2. [Immediate] GRA-002: Design and implement the 3 mandatory Model Risk controls
   currently absent from control_taxonomy_matrix. Addresses CGC-002, GGP-CM-002.
   Responsible: Chief Risk Officer. Effort: Months.
──────────────────────────────────────────────────────────────────
No positive Governance Readiness Classification may be issued until both CGCs
are resolved and GTG-3 and GTG-7 mandatory gates pass.
──────────────────────────────────────────────────────────────────
```

---

## Calibration Principles

**On CGC vs. MGF from CCR domain rates:**
A mandatory control domain below 50% implementation rate is a CGC. A domain between 50% and 70% is an MGF (−10 GAS). A domain above 70% has no finding from CCR analysis alone. The boundary is the domain rate, not the individual control classification. Example 3 shows the Model Risk domain at 40.0% — CGC. Example 2 shows Transparency at 70.0% — boundary case, classify as MGF because two mandatory controls are undesigned (not just partially implemented).

**On GAS arithmetic when CGC is present:**
Always show the arithmetic even when GAS = 0. The arithmetic documents what the posture would be without the CGC, which is diagnostic for the client — it tells them how far the non-CGC findings contribute. Example 3 shows GAS arithmetic of 41 before the absolute rule. Showing this helps the client understand that resolving only the CGCs would not achieve Governance Ready; the MGFs also need to be addressed.

**On the GTG-3 two-guard pattern:**
The intake schema requires `iso_42001_output` as a typed object. A null or absent value fails at intake before the skill executes. This makes GTG-3 analogous to TG-3 in Proposal Review: intake is the primary guard; executor enforcement is the secondary guard. The runtime test `test_gtg3_fail_iso_absent` must call the executor directly to test the secondary guard — the same pattern as `test_tg3_fail_when_feature_mapping_absent`.

**On CCR when `governance_gate_passed = false`:**
CCR is always computed and reported, even when the review is incomplete. A gate failure does not invalidate the control coverage posture — it invalidates the classification. The CCR value is an accurate statement of coverage based on available inputs and belongs in Section 10 regardless of gate status.

**On GGP-IS-001 in Example 1 and GR-001 Calibration:**
Under GR-001 calibration, GP-MGF items (management system gaps like GGP-IS-001) are downgraded to Minor Findings (-2 GAS). This reduces the MGF count to 0, which (coupled with GAS 94 ≥ 85, CCR 91.7 ≥ 80, CGC = 0, and High Risks = 0 ≤ 1) allows the Meridian Private Bank review to achieve a **Governance Ready** classification. This demonstrates how GP-MGF downgrades directly affect the terminal classification.
