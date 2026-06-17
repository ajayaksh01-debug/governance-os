---
fixture_id: uk-insurance-claims-model
skill: regulatory-mapping
trigger_type: regulatory_change_alert
subject_type: AI System
jurisdictions: ["UK"]
industry: Insurance
bfsi: true
ai_technology: ML classifier
subject_name: Motor Insurance Claims Triage Model
change_trigger: "FCA published updated Dear CEO letter on AI model risk in insurance (June 2026)"
change_severity: Major
expected_risk_tier_uk: "FCA Material; PRA SS1/23 Tier 1 (conditional)"
expected_regulations: ["UK GDPR", "DPA 2018", "FCA Consumer Duty", "FCA AI Guidance", "Equality Act 2010"]
expected_frameworks: ["ISO 42001", "NIST AI RMF"]
expected_owasp_applicable: false
expected_bfsi_applicable: true
expected_dpia_required: true
expected_article22_applicable: true
expected_equality_act_risk: "Conditional — depends on proxy variable analysis"
expected_score_range: [78, 90]
expected_control_count_min: 7
claim_context: Regulatory Change Alert (re-assessment)
---

# Test Fixture: UK Insurance Claims Triage Model — Regulatory Change Re-Assessment

## Context

**Organisation:** Meridian Motor Insurance Ltd — UK motor insurance provider (FCA-regulated, also PRA-regulated as a Solvency II insurer). ~750,000 active policies, majority personal lines.  
**Subject type:** AI System (previously assessed; re-assessment triggered by regulatory change)  
**Use case:** ML model scoring incoming motor insurance claims for complexity and fraud risk. The model routes claims automatically:
- Score 0–30 (Low complexity, low fraud risk) → Auto-settlement within 24 hours, no human review
- Score 31–70 (Medium) → Human adjuster review
- Score 71–100 (High complexity or fraud flag) → Senior adjuster review + potential referral to Special Investigations Unit  

**Trigger:** Regulatory Change Alert (Mode B re-assessment). The FCA published an updated Dear CEO letter in June 2026 addressing AI model risk in insurance claims processing. The letter introduces new expectations on explainability for automated claim routing decisions and requires insurers to demonstrate that AI systems do not systematically disadvantage customers with protected characteristics. The prior regulatory mapping for this system (assessed in Q1 2026) pre-dates this guidance and requires re-assessment.

**Prior assessment ID:** TR-RW-2026-0041 (Q1 2026 assessment; jurisdictions: UK; score: 78/100)

---

## System Description

**Technology:** Random Forest classifier. Not an LLM. Uses tabular features derived from claim submissions.  
**Inputs:** Claim metadata (date, time, location of incident), vehicle data (make, model, age, registration), driver data (age, driving licence duration, named driver status, no-claims history), claim description (free text — features extracted via NLP pipeline), claim history data (prior claims count, claim types, prior fraud flags), third-party data (weather APIs, traffic incident reports, DVLA data).  
**Outputs:** Complexity score (0–100), fraud risk flag (yes/no with confidence score), routing decision (Auto-settle / Human review / Senior review + SIU), feature importance list (top 5 input factors driving the score).  
**Data subjects:** UK policyholders submitting motor claims.  
**Deployment model:** On-premises (Meridian internal data centre). No cloud processing.  
**Automated decision-making:** Yes — the auto-settlement routing (score 0–30) constitutes an automated decision with legal or similarly significant effects: a policyholder in the 0–30 band receives an automated settlement without human review. A policyholder in the 71–100 band is routed to fraud investigation without human review of the routing decision itself.  
**Bias concern:** Claims in certain postcode areas are disproportionately routed to the high-complexity band. Internal review has not confirmed whether this reflects genuine claim complexity or a proxy for protected characteristics.

---

## Jurisdictions

- **UK:** Confirmed in scope. Organisation is UK-domiciled, FCA and PRA regulated. All data subjects are UK individuals.
- **EU:** Not in scope — UK entity post-Brexit; Solvency II UK equivalent applies but EU GDPR does not.
- **India:** Not in scope.

---

## Sector and BFSI Overlay

**Primary sector:** Insurance  
**Regulatory relationships:**
- FCA (Financial Conduct Authority) — conduct regulator; Consumer Duty (PRIN 12) obligations
- PRA (Prudential Regulation Authority) — prudential regulator; Solvency II UK equivalent
- ICO (Information Commissioner's Office) — data protection regulator

BFSI overlay is **mandatory**. Insurance is a BFSI sector. FCA Consumer Duty (PRIN 12) is the primary conduct obligation. PRA SS1/23 may apply if the claims model is classified as a material model with impact on the firm's financial position (reserving, claims ratios) — conditional on materiality assessment.

---

## Data Categories

| Category | Specific data elements | Notes |
|---|---|---|
| Identity data | Policyholder name, DOB, driving licence number | Personal data |
| Contact data | Address, phone, email | Personal data |
| Vehicle data | Registration, make, model, age | Personal data (linked to policyholder) |
| Claim data | Incident description, location, damage assessment | Personal data |
| Claims history | Prior claims, prior fraud flags, no-claims discount | Personal data |
| Driver behaviour data | Named driver history, conviction records (spent convictions must be handled per DPA 2018 Schedule 1) | Personal data; potentially spent conviction data |
| Geographic data | Postcode (proxy variable risk) | Personal data |

No biometric data. No health/medical data in standard claims (injury claims may include medical reports — separate processing and separate GDPR lawful basis consideration, but standard motor claims are the scope of this fixture).

---

## Expected Regulatory Triggers

| Regulation | Jurisdiction | Expected finding | Key trigger |
|---|---|---|---|
| UK GDPR | UK | Confirmed applicable | Processing personal data of UK data subjects; Article 22 (automated individual decisions with significant effects on policyholders) |
| Data Protection Act 2018 | UK | Confirmed applicable | UK data protection law; Schedule 1 lawful bases for processing; Section 49 automated decision-making provisions |
| FCA Consumer Duty (PRIN 12) | UK | Confirmed applicable | Material impact on customer outcomes — automated claim routing and settlement directly affects consumer financial outcomes |
| FCA AI Guidance (June 2026 Dear CEO letter) | UK | Confirmed applicable — CHANGE DRIVER | Updated FCA expectations on explainability and protected characteristic monitoring in insurance AI |
| Equality Act 2010 | UK | Conditional applicable | Postcode proxy variable may constitute indirect discrimination on grounds of race, national origin, or religion and belief — requires bias audit to determine |
| PRA SS1/23 | UK | Conditional applicable | Potential Tier 1 classification if claims model materially affects the firm's financial position (reserving accuracy, claims ratios); requires materiality assessment |
| ICO AI and Data Protection Guidance | UK | Applicable (regulatory guidance) | ICO guidance on AI decision-making, transparency obligations, and fairness in automated systems |

---

## Expected Control Themes

The assessment must identify, at minimum, the following control requirement themes. An output missing more than two of these fails the minimum control coverage test for this fixture.

1. **UK GDPR Article 22 safeguards** — mandatory for automated claim routing: right to obtain human intervention, right to express a point of view, right to contest the automated decision; the auto-settlement path must be re-designed to include at least one safeguard mechanism
2. **DPIA** (UK GDPR Article 35) — mandatory; automated decision-making producing significant effects on data subjects at scale requires DPIA
3. **Explainability mechanism** (FCA Consumer Duty, ICO AI Guidance, new FCA Dear CEO letter) — claims routing decisions must be explainable to customers in plain language; top-5 feature importance must be communicable in human-readable form
4. **Bias audit and ongoing fairness monitoring** (Equality Act 2010 conditional, FCA June 2026 guidance) — postcode proxy variable must be analysed for indirect discrimination; ongoing demographic fairness monitoring required
5. **Human review override mechanism** — customers must be able to request human review of their claim routing decision regardless of automated score
6. **Model documentation** — technical documentation of the Random Forest model including training data provenance, feature selection rationale, validation methodology
7. **Model monitoring and drift detection** — claims fraud patterns change over time; model performance monitoring to detect accuracy drift and bias drift required
8. **Vendor and data supply chain management** — third-party data feeds (DVLA, weather APIs, traffic data) introduce supply chain risk; data quality controls required
9. **Spent conviction data handling** (DPA 2018 Schedule 1, Part 3) — claims history may include prior fraud convictions; processing of spent conviction data requires specific Schedule 1 condition
10. **Regulatory change impact reassessment process** (new control triggered by this re-assessment itself) — process control to ensure AI systems are re-assessed when material regulatory guidance changes

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **Regulatory change alert trigger — Mode B re-assessment:** This fixture tests the evaluator's ability to identify and incorporate a regulatory change event into an existing system assessment. The June 2026 FCA Dear CEO letter on AI model risk in insurance is the change driver. The assessment must explicitly:
   - Identify what changed (new explainability expectations, protected characteristic monitoring obligations)
   - Compare new requirements against the prior assessment (TR-RW-2026-0041)
   - Identify incremental obligations created by the new guidance
   - Not re-assess obligations already captured in the prior assessment (avoid duplication)

2. **UK GDPR Article 22 applicability — not conditional:** The auto-settlement path (score 0–30) constitutes an automated decision with significant effects on policyholders. The evaluator must confirm Article 22 applies — it is not conditional on whether the claim is settled "favourably." An automated settlement without human review is still a significant decision: the policyholder has no opportunity to contest the assessment before settlement. A correct assessment notes that Article 22 applies regardless of whether the automated decision benefits or harms the data subject.

3. **Equality Act 2010 conditional applicability:** The postcode proxy variable risk must be flagged as triggering a conditional Equality Act risk. The evaluator must not confirm or deny Equality Act violation without a bias audit — the risk is conditional on whether postcode correlates with protected characteristics. The correct treatment: conditional applicability with a DPIA obligation to investigate.

4. **OWASP LLM Top 10 — correctly marked N/A:** The Random Forest classifier has an NLP pipeline for feature extraction from claim descriptions, but the core model is not an LLM. OWASP LLM Top 10 must be marked N/A for the core model. If the NLP pipeline uses an LLM, this must be explicitly scoped and assessed separately.

5. **FCA Consumer Duty — not just a reference:** Consumer Duty (PRIN 12) must be applied with specificity. The evaluator must identify which of the four Consumer Duty outcomes are engaged:
   - Products and Services Outcome: automated routing algorithm is a product
   - Price and Value Outcome: auto-settlement amounts must be fair
   - Consumer Understanding Outcome: customers must understand their routing decision
   - Consumer Support Outcome: support for customers who want to contest automated decisions

6. **PRA SS1/23 — conditional, not confirmed:** Whether the claims triage model constitutes a PRA SS1/23 model depends on a materiality assessment. The evaluator must flag this as conditional and explain the determining factors (does the model materially affect reserving accuracy or claims ratios?). Confirming or denying PRA SS1/23 without a materiality assessment fails this test.

7. **Section 6 Claims Firewall — no In Build capabilities as controls:** If Section 6 references any Ethana capability to illustrate a control, only Production capabilities may be referenced as active. Compliance Pack (In Build), CI/CD Gate Integration (In Build), and SCIM Provisioning (In Build) are examples of capabilities that must not be referenced as controls deliverable today.

8. **Re-assessment incremental framing:** Because this is a Mode B regulatory change re-assessment, the output should be framed as an update to the prior assessment, not a blank-slate assessment. The executive summary should note: "Re-assessment triggered by FCA June 2026 Dear CEO letter; prior assessment TR-RW-2026-0041 remains valid for [list of unchanged obligations]; incremental obligations arising from new guidance are [list]."

---

## Reviewer Red Flags

- EU AI Act cited as applicable → no EU nexus post-Brexit; UK AI regulatory framework applies, not EU AI Act
- UK GDPR Article 22 treated as conditional → auto-settlement constitutes automated decision with significant effects; Article 22 applies
- OWASP LLM Top 10 applied to the Random Forest model → core model is not LLM-based
- PRA SS1/23 confirmed as applicable without noting materiality assessment requirement → conditional on materiality threshold
- Equality Act 2010 not mentioned → postcode proxy variable risk must trigger conditional Equality Act assessment
- FCA Consumer Duty not broken down into the four outcomes → specific outcomes framework must be applied
- Output not framed as an incremental re-assessment → this is a Mode B regulatory change alert; prior assessment must be referenced
- Section 6 references Compliance Pack, CI/CD Gate Integration, or SCIM Provisioning as active controls → Claims Firewall violation; these are In Build
- DPIA classified as optional or "likely needed" → mandatory under UK GDPR Article 35 for automated decisions at scale affecting policyholders
- Spent conviction data (prior fraud flags) not addressed → DPA 2018 Schedule 1 processing condition required
