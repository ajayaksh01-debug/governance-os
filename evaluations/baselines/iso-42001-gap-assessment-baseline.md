# ISO 42001 Gap Assessment — Regression Baseline

## Purpose

This document defines the expected output characteristics for each `iso-42001-gap-assessment` test fixture. It is used by `regression_tester.py` to detect structural drift, scoring range violations, and Claims Firewall failures across assessment runs.

**Authoritative fixtures:** `evaluations/test-cases/iso-42001-gap-assessment/`  
**Skill version:** 1.0  
**Baseline established:** 2026-06-17  
**Governance Team review required to update:** Yes

---

## Fixture 1 — bank-certification-readiness

**Description:** Indian private bank, four AI systems (credit scoring, chatbot, fraud detection, trade finance), ISO 27001 certificate for IT infrastructure, RBI MRM policy for credit model only.

### Expected Score Ranges

| Metric | Minimum | Maximum | Notes |
|---|---|---|---|
| AMS | 20 | 50 | Range reflects evidence access variability; conservative evidence-based scoring drives toward lower end; fuller evidence access with workshop methods reaches upper end |
| ARS | 20 | 40 | Audit Log and Red Teaming provide operating evidence; no governance documentation baseline |
| Critical gaps | 3 | 6 | Expected ~4: Clause 4 scope, Clause 5 policy, Clause 8 lifecycle (multi-system), possibly Annex A Category 4 data governance |
| Major gaps | 10 | 18 | Expected ~13 including all Annex A Category 2, 3, 7, 9 gaps |
| Minor gaps | 4 | 10 | Including Clause 10, minor Category 8 transparency gaps |
| Months to readiness | 14 | 20 | 14-month minimum assumes aggressive programme launch with Cursory support |

**Certification Classification: Significant Gaps** (invariant — must not vary based on evidence access level)

### Structural Requirements

```json
{
  "required_sections": [
    "Executive Summary",
    "Clause Coverage Matrix",
    "Annex A Control Assessment",
    "Gap Register",
    "Risk Prioritisation",
    "Evidence Requirements",
    "Remediation Roadmap",
    "Ethana Coverage Analysis",
    "Audit Readiness Assessment",
    "Overall Maturity Score"
  ],
  "required_clause_ratings": ["Cl.4", "Cl.5", "Cl.6", "Cl.7", "Cl.8", "Cl.9", "Cl.10"],
  "required_annex_a_categories": 9,
  "required_gap_id_schemes": ["GAP-CL", "GAP-AA"],
  "section_8_5_required": true
}
```

### Claims Firewall Verification

```json
{
  "expected_valid_references": ["Immutable Audit Log", "Red Teaming Orchestrator", "Bias Scanner"],
  "expected_invalid_references_if_present": ["Compliance Pack"],
  "aspirational_exclusions_required": [],
  "mandatory_caveats": {
    "Bias Scanner": "runtime text filter only; does not perform statistical disparate impact analysis",
    "Immutable Audit Log": "logs only gateway-routed traffic"
  }
}
```

### Disqualifier Verification

For this fixture, the following checks must pass:
- HD1: Section 2 contains Clause 4 rating — **must be 1 (not 0 or absent)**
- HD2: If Compliance Pack appears in Section 8 body as a current capability → assessment fails
- HD3: All 9 Annex A categories present in Section 3
- HD4: Every gap in Section 4 has a clause/control reference
- HD5: AMS computed from complete Section 2 and Section 3 data only
- HD6: Classification is Significant Gaps (not Certification Ready or Near Ready)

### Calibration Anchor Points

- Clause 8 rating must be 1 or 2 — not 3 (credit scoring model validation ≠ ISO 42001 AI lifecycle)
- RBI jurisdiction overlay must elevate Annex A Category 3 and Category 9 gap severity
- ISO 27001 credit applies only to Clause 7 and partial Clause 4 — not Clause 8

---

## Fixture 2 — fintech-extension-from-iso27001

**Description:** EU fintech SaaS, ISO 27001 certificate (SaaS platform scope), credit risk API (EU AI Act high-risk candidate), HR hiring assistant (Azure OpenAI, internal).

### Expected Score Ranges

| Metric | Minimum | Maximum | Notes |
|---|---|---|---|
| AMS | 55 | 75 | ISO 27001 credit on Clauses 4-7 significantly lifts clause scores; Annex A AI-specific gaps keep ceiling below 80 |
| ARS | 50 | 70 | ISO 27001 documentation infrastructure provides strong documentation completeness; AI-specific evidence thin |
| Critical gaps | 1 | 3 | Expected 2: Clause 6 AI impact assessment (EU AI Act escalation); Clause 8 AI lifecycle (EU AI Act escalation) |
| Major gaps | 6 | 12 | Expected ~8-10 including Annex A Categories 3, 5 |
| Minor gaps | 4 | 8 | Minor documentation gaps on Clauses 4, 5, 7, 10 |
| Months to readiness | 5 | 10 | Fastest path among the three fixtures given ISO 27001 infrastructure |

**Certification Classification: Near Ready** (invariant — the ISO 27001 baseline and low Critical gap count drives Near Ready, not Significant Gaps)

### Structural Requirements

```json
{
  "required_sections": [
    "Executive Summary",
    "Clause Coverage Matrix",
    "Annex A Control Assessment",
    "Gap Register",
    "Risk Prioritisation",
    "Evidence Requirements",
    "Remediation Roadmap",
    "Ethana Coverage Analysis",
    "Audit Readiness Assessment",
    "Overall Maturity Score"
  ],
  "required_clause_ratings": ["Cl.4", "Cl.5", "Cl.6", "Cl.7", "Cl.8", "Cl.9", "Cl.10"],
  "required_annex_a_categories": 9,
  "section_8_5_required": true
}
```

### Claims Firewall Verification

```json
{
  "expected_valid_references": ["Immutable Audit Log", "Red Teaming Orchestrator", "LLM Gateway"],
  "expected_invalid_references_if_present": ["Discovery", "Ethana Sentry"],
  "aspirational_exclusions_required": [],
  "mandatory_caveats": {
    "Immutable Audit Log": "logs only gateway-routed traffic; monitoring programme design required separately"
  }
}
```

### Disqualifier Verification

- HD1: Section 2 contains Clause 4 rating — may be 3 (ISO 27001 credit), not absent
- HD2: Discovery or Sentry cited as operational → assessment fails
- HD3: All 9 Annex A categories present, including Category 5 (Supply Chain — Azure OpenAI relationship)
- HD4: Every gap in Section 4 has clause/control reference
- HD5: AMS computed from complete assessment
- HD6: Classification is Near Ready — not Certification Ready (open Critical gaps)

### Calibration Anchor Points

- Clause 6 must be rated 2 (Critical, EU AI Act escalation) — not 3 (DPIA ≠ AI impact assessment)
- Clause 8 must be rated 2 (Critical, EU AI Act escalation) — not 3 (ISO 27001 change management ≠ AI lifecycle)
- Category 5 (Supply Chain) must include Azure OpenAI assessment gap — not N/A
- AMS must not exceed 75 — ISO 27001 does not cover AI lifecycle controls in Category 3

---

## Fixture 3 — greenfield-organisation

**Description:** UK retail group, four AI systems, no management system certifications, Netherlands subsidiary (EU AI Act limited-risk chatbot).

### Expected Score Ranges

| Metric | Minimum | Maximum | Notes |
|---|---|---|---|
| AMS | 5 | 25 | Zero-baseline clauses; minimal partial Annex A; range reflects depth of informal practice discovered |
| ARS | 5 | 20 | No AIMS documentation; GDPR framework is out of scope for ARS computation |
| Critical gaps | 4 | 8 | Expected 5: Clause 4 scope, Clause 5 policy, Clause 6 risk/impact, Clause 8 lifecycle, Annex A Category 8 (EU AI Act chatbot transparency) |
| Major gaps | 14 | 22 | Expected ~16-18 across all major Annex A categories |
| Minor gaps | 6 | 12 | Expected ~8 |
| Months to readiness | 18 | 30 | Largest programme among the three fixtures |

**Certification Classification: Major Gaps** (invariant — zero-baseline AMS and 4+ Critical gaps; no exceptions regardless of board mandate timeline)

### Structural Requirements

```json
{
  "required_sections": [
    "Executive Summary",
    "Clause Coverage Matrix",
    "Annex A Control Assessment",
    "Gap Register",
    "Risk Prioritisation",
    "Evidence Requirements",
    "Remediation Roadmap",
    "Ethana Coverage Analysis",
    "Audit Readiness Assessment",
    "Overall Maturity Score"
  ],
  "required_clause_ratings": ["Cl.4", "Cl.5", "Cl.6", "Cl.7", "Cl.8", "Cl.9", "Cl.10"],
  "required_annex_a_categories": 9,
  "section_8_5_required": true,
  "section_8_5_aspirational_exclusion_record_required": true
}
```

### Claims Firewall Verification

```json
{
  "expected_valid_references": ["Immutable Audit Log", "Red Teaming Orchestrator"],
  "expected_invalid_references_if_present": ["Visual Agent Builder", "Workspace", "Ethana Workspace"],
  "aspirational_exclusions_required": ["Visual Agent Builder", "Workspace"],
  "mandatory_caveats": {
    "Immutable Audit Log": "logs only gateway-routed LLM Gateway traffic; direct OpenAI API calls are not logged"
  }
}
```

**Critical:** `aspirational_exclusions_required` entries must appear in Section 8.5 as "considered and excluded" records, not as corrections — they should never have been included in Section 8 in the first place. A reviewer who includes them and then corrects them in Section 8.5 has passed the Claims Firewall gate but failed the calibration test (Aspirational capabilities should never be drafted into Section 8).

### Disqualifier Verification

- HD1: Section 2 contains Clause 4 rating — must be 0; critical that Clause 4 is present even at maturity 0
- HD2: Visual Agent Builder or Workspace cited in Section 8 as capability → assessment fails
- HD3: All 9 Annex A categories present; none marked N/A wholesale for "retail doesn't use AI training"
- HD4: Every gap in Section 4 has clause/control reference
- HD5: AMS computed from complete Section 2 (7 clauses, all rated) and Section 3 (all 9 categories)
- HD6: Classification is Major Gaps — Certification Ready or Near Ready trigger HD6 given 4+ Critical gaps

### Calibration Anchor Points

- Clause 7 must be rated 1 (not 0) — GDPR data protection team provides some competence basis
- Clause 9 must be rated 1 (not 0) — OpenAI API usage logs accessible
- Annex A Category 8 must contain a Critical gap for the chatbot (EU AI Act limited-risk transparency obligation in Netherlands is a live regulatory requirement, not aspirational)
- Demand forecasting retraining must appear as an Annex A Category 3 gap (Change Management or Training Data Management) — not a general IT change management note

---

## Cross-Fixture Invariants

These rules apply across all three fixtures and will be flagged as regression failures if violated:

### AMS Formula Compliance
For every fixture, the output must show AMS arithmetic:
```
Clause_Score = (Cl.4 + Cl.5 + Cl.6 + Cl.7 + Cl.8 + Cl.9 + Cl.10) / 7 × 20
Annex_A_Score = (Implemented + Partially_Implemented × 0.5) / Total_Applicable × 100
AMS = (Clause_Score × 0.60) + (Annex_A_Score × 0.40)
```
An AMS that does not show per-clause ratings and Annex A counts fails HD5.

### ARS Formula Compliance
For every fixture:
```
ARS = (Doc_Completeness × 0.30) + (Evidence_Availability × 0.40)
    + (Control_Operationalization × 0.20) + (Mgmt_Review_Readiness × 0.10)
```
All four component scores must be visible in Section 9.

### Classification Table Compliance
| Condition | Classification |
|---|---|
| AMS ≥ 80 AND ARS ≥ 75 AND Critical = 0 | Certification Ready |
| AMS 60-79 OR ARS 60-74 AND Critical 0-2 | Near Ready |
| AMS 40-59 OR Critical 3-5 | Significant Gaps |
| AMS < 40 OR Critical 6+ | Major Gaps |

No output may classify as Certification Ready if Critical > 0. HD6 is enforced unconditionally.

### Section 8.5 Presence
Section 8.5 (Claims Firewall Review) must appear in every assessment. An assessment without Section 8.5 scores maximum 4/10 on Section 8 regardless of Section 8 body quality.

### Compliance Pack Exclusion
`Compliance Pack` must not appear as a Production capability in any assessment. It is In Build [IB]. Expected Cursory alternative: Regulatory Gap Analysis service using the Immutable Audit Log as evidence source.

### Discovery/Sentry/Edge Exclusion
`Discovery`, `Sentry`, `Ethana Edge`, and `Sentry Edge` must not appear as operational capabilities. These are Roadmap [RM] or In Build [IB]. No valid reference exists in the current assessment period.

### Visual Agent Builder and Workspace Exclusion
Both capabilities are Aspirational. They must not appear in any Section 8 entry, even as "planned" or "roadmap" items. The distinction from In Build [IB] capabilities is important: In Build capabilities may appear in Section 8 as roadmap items with the caveat "not available in current assessment period." Aspirational capabilities must not appear in Section 8 at all.

---

## Baseline Update Protocol

### When to update this baseline

This baseline may only be updated when:
1. The ISO 42001 skill (SKILL.md, workflow.md, evaluation.md) is formally revised and version-bumped
2. The canonical-product-model.md is updated, changing the status of a capability referenced in these fixtures
3. New test fixtures are added that require corresponding baseline entries
4. A systematic miscalibration is identified affecting expected ranges (requires Governance Team review and documented rationale)

### When NOT to update this baseline

- Observed AMS or ARS scores from live assessments that fall outside the ranges do not constitute a baseline update — they are potential calibration errors in the live assessment
- Commercial preference for a more favourable classification does not constitute a baseline update
- A single assessment run producing an outlier score is not a baseline update trigger

### Update procedure

1. Submit a proposed update to the Governance Team with rationale
2. Governance Team reviews and approves the update with documented basis
3. Update this baseline file with version note and date
4. Update the regression test commands in `evaluations/evaluation-index.md` if fixture metadata changes
