---
fixture_id: eu-ai-act-high-risk-banking
skill: regulatory-mapping
trigger_type: new_use_case_registration
subject_type: AI System
jurisdictions: ["EU", "UK"]
industry: Banking
bfsi: true
ai_technology: ML classifier
subject_name: Consumer Credit Scoring Model
expected_risk_tier_eu: "High-risk (Annex III, Point 5)"
expected_risk_tier_uk: "PRA SS1/23 Tier 1"
expected_dpia_required: true
expected_regulations: ["EU AI Act", "GDPR", "UK GDPR", "DPA 2018", "FCA AI Guidance", "PRA SS1/23"]
expected_frameworks: ["ISO 42001", "NIST AI RMF"]
expected_owasp_applicable: false
expected_bfsi_applicable: true
expected_score_range: [85, 95]
expected_control_count_min: 8
claim_context: New Use Case Registration
---

# Test Fixture: EU AI Act High-Risk — Consumer Credit Scoring Model

## Context

**Organisation:** Eurobank Retail S.A. — mid-tier European retail bank with FCA-regulated UK subsidiary (Eurobank UK Ltd). Primary operations in Germany and the Netherlands under BaFin/DNB supervision. UK operations under FCA and PRA supervision.  
**Subject type:** AI System (deployed)  
**Use case:** Automated consumer credit scoring used in personal loan underwriting decisions for retail banking customers. The model scores loan applicants and produces a credit decision recommendation (Approve / Decline / Refer to human underwriter). Fully automated decisions are made for standard applications below €15,000; applications above the threshold or flagged by the model are referred to a human underwriter.  
**Trigger:** New AI system registration — the model passed internal UAT and is scheduled for production deployment in Q3 2026. Compliance review required before go-live.

---

## System Description

**Technology:** Gradient Boosting ML classifier (XGBoost-based). Not an LLM. No generative AI components.  
**Inputs:** Personal data — applicant name, date of birth, address, employment status, income, existing debt obligations; credit bureau data (credit score, repayment history, default history); behavioural data from the bank's own customer data (transaction history, product tenure, overdraft usage).  
**Outputs:** Credit score (0–1000 numeric), risk band (A–E), credit decision recommendation (Approve / Decline / Refer), feature importance breakdown (top 3 input factors).  
**Data subjects:** EU natural persons (Germany, Netherlands) and UK natural persons applying for personal loans.  
**Deployment model:** Cloud SaaS (hosted by Eurobank on AWS EU-West, Frankfurt region). UK traffic routes to the same model with EU-hosted data.  
**Automated decision-making:** Yes — for applications below €15,000, the model's Approve recommendation results in automatic loan contract generation without human review.  
**Bias risk:** Historical training data includes 8 years of prior loan decisions. Internal audit has noted that the prior approval rate for certain postal code clusters correlates with socioeconomic demographics.

---

## Jurisdictions

- **EU:** Confirmed in scope. Model processes personal data of EU data subjects. AI system deployed in the EU market for credit decisions affecting EU individuals. Germany (BaFin, BAFIN AI consultation) and Netherlands (AFM, DNB) are primary regulatory nexus points.
- **UK:** Confirmed in scope. UK subsidiary (FCA-regulated) uses the same model for UK customers. UK GDPR, FCA, and PRA apply to the UK operations.

---

## Sector and BFSI Overlay

**Primary sector:** Retail banking  
**Regulatory relationships:**
- EU: ECB Single Supervisory Mechanism (SSM) oversight; EBA Guidelines on internal governance
- UK: FCA (Financial Conduct Authority); PRA (Prudential Regulation Authority); Eurobank UK Ltd is a PRA-authorised bank

BFSI overlay is **mandatory** for this fixture. The PRA SS1/23 model risk management framework applies to any model that materially influences financial decisions. A credit scoring model with automated decisioning for personal loans is paradigmatically a PRA SS1/23 Tier 1 model.

---

## Data Categories

| Category | Specific data elements | Sensitivity |
|---|---|---|
| Identity data | Full name, DOB, NI number (UK), BSN (Netherlands) | Personal data |
| Contact data | Address history, phone, email | Personal data |
| Financial data | Income, employment status, existing debts, bank account transactions | Personal data (financial) |
| Credit data | Credit bureau score, repayment history, CCJs/defaults | Personal data (credit) |
| Behavioural data | Bank transaction patterns, product tenure, overdraft frequency | Personal data |
| Geographic data | Postal code (proxy variable risk) | Personal data |

No biometric data, no health data, no special category data in training or scoring inputs.

---

## Expected Regulatory Triggers

| Regulation | Jurisdiction | Expected finding | Key trigger |
|---|---|---|---|
| EU AI Act | EU | High-risk (Annex III, Point 5) | AI used by credit institutions subject to CRD IV/CRR to assess creditworthiness of natural persons |
| GDPR | EU | Confirmed applicable | Processing of personal data of EU natural persons; Article 22 (automated individual decision-making with legal or similarly significant effects) |
| UK GDPR | UK | Confirmed applicable | Processing of personal data of UK natural persons; UK GDPR Article 22 equivalent |
| Data Protection Act 2018 | UK | Confirmed applicable | DPA 2018 Schedule 1 processing grounds; Section 49 automated decision-making provisions |
| FCA AI Guidance | UK | Confirmed applicable | FCA-regulated entity using AI model for credit decisions affecting UK consumers; Consumer Duty obligations |
| PRA SS1/23 | UK | Tier 1 model confirmed | Material model — directly influences credit underwriting decisions with significant financial impact |
| Equality Act 2010 | UK | Conditional | Postal code proxy variable may introduce indirect discrimination on grounds of race or socioeconomic status — DPIA must assess |
| EU Banking Regulation (EBA) | EU | Applicable | EBA Guidelines on internal governance (EBA/GL/2021/05) require model risk management for material models |

---

## Expected Control Themes

The assessment must identify, at minimum, the following control requirement themes. An output missing more than two of these themes fails the minimum control coverage test for this fixture.

1. **Technical documentation** (EU AI Act Article 11, Annex IV) — mandatory; one-time with update obligations
2. **Conformity assessment** (EU AI Act Article 43) — mandatory for high-risk systems; internal or third-party depending on system type
3. **Fundamental rights impact assessment** (EU AI Act Article 27, Recital 48) — mandatory for deployers of high-risk systems
4. **DPIA** (GDPR Article 35) — mandatory; automated individual decision-making with systematic evaluation of natural persons
5. **Human oversight mechanism** (EU AI Act Article 14) — mandatory for high-risk systems; natural persons must be able to understand and oversee outputs
6. **Explainability and right to explanation** (GDPR Article 22(3), EU AI Act Article 13) — mandatory; data subjects have the right to meaningful information about automated decisions
7. **Data governance and training data quality** (EU AI Act Article 10) — mandatory; high-risk AI systems must use training, validation, and testing data meeting quality criteria
8. **Bias testing and ongoing fairness monitoring** — mandatory; Equality Act (UK indirect discrimination), EU AI Act Article 10 (data quality), Article 9 (risk management)
9. **Post-market monitoring** (EU AI Act Article 72) — mandatory; operators must conduct post-market monitoring of high-risk systems
10. **Model validation** (PRA SS1/23 Principle 2) — mandatory for Tier 1 model; independent validation required

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **EU AI Act Annex III, Point 5 identification:** The evaluator must identify this as a high-risk AI system under EU AI Act Annex III, Point 5 (AI systems used by credit institutions for creditworthiness assessment). This identification must cite Annex III, Point 5 explicitly — a general statement that "credit scoring AI may be high-risk" without the specific Annex reference fails the regulatory citation test.

2. **GDPR Article 22 applicability:** The model produces automated decisions below €15,000 without human review. GDPR Article 22 applies where automated processing produces legal or similarly significant effects on individuals. A credit refusal is explicitly cited in GDPR Recital 71 as an example of a significantly significant effect. The evaluator must confirm GDPR Article 22 applies and note the right to obtain human intervention, express a point of view, and contest the decision.

3. **DPIA as mandatory, not conditional:** Given the combination of automated decision-making, large-scale personal data processing, and systematic processing of financial data, DPIA is mandatory under GDPR Article 35(3)(a). The evaluator must not treat DPIA as "recommended" or "likely required" — it is mandatory. An output classifying DPIA as "likely needed" rather than "required" fails the obligation precision test.

4. **PRA SS1/23 Tier 1 — not just "applicable":** The evaluator must classify the model as Tier 1 under PRA SS1/23 (not merely state PRA SS1/23 "applies"). Tier 1 classification applies to models with material impact on the firm's financial position, reputation, or customer outcomes. A credit scoring model driving automated underwriting decisions is definitionally Tier 1.

5. **Bias risk and Equality Act 2010:** The postal code proxy variable risk must be identified. The evaluator must flag the conditional Equality Act 2010 risk (indirect discrimination on grounds of race or socioeconomic status may arise if postal code correlates with protected characteristics). This is a conditional applicability — the DPIA and model documentation must investigate this risk.

6. **OWASP LLM Top 10 — correctly marked N/A:** The model is an XGBoost classifier, not an LLM. OWASP LLM Top 10 must be marked N/A with the rationale: "Subject is an ML classifier; no LLM or LLM-based components are present."

7. **Bias Scanner caveat — Claims Firewall critical test:** If Section 6 (Control Requirements) references Ethana's Bias Scanner for training data bias auditing or EU AI Act Article 10 compliance, this is a Claims Firewall violation. Bias Scanner is Production but is a **runtime filter only** — it does not audit training data, statistical disparity across demographic groups, or satisfy EU AI Act Art.10's data governance requirements or NYC Local Law 144 bias audit requirements. Any Section 6 reference to Bias Scanner must explicitly state this caveat. An output that recommends Bias Scanner as sufficient for EU AI Act Art.10 compliance fails the Claims Firewall test for this fixture.

8. **Section 8 BFSI — both EU and UK overlays:** Section 8 must cover BFSI obligations for both jurisdictions: EBA internal governance guidelines for EU, and PRA SS1/23 Tier 1 for UK. An output that covers only one jurisdiction's BFSI overlay is incomplete.

---

## Reviewer Red Flags

- EU AI Act cited as applicable without identifying the specific Annex III point → citation failure; must specify Point 5
- DPIA classified as "recommended" rather than "mandatory" → GDPR Article 35(3)(a) makes it mandatory for automated decision-making systems at scale
- PRA SS1/23 mentioned without Tier 1 classification → incomplete BFSI assessment
- Equality Act 2010 not mentioned → proxy variable bias risk must trigger conditional Equality Act assessment
- OWASP LLM Top 10 applied to this ML classifier → incorrect; the system is not LLM-based
- Bias Scanner referenced as satisfying EU AI Act Art.10 training data requirements → Claims Firewall violation; runtime filter ≠ training data audit
- Section 8 covers only EU or only UK BFSI obligations → fixture is dual-jurisdiction; both must be addressed
- "Fundamental rights impact assessment" absent from Section 5 (Documentation Requirements) → EU AI Act Article 27 makes it mandatory for deployers of high-risk systems
- Human oversight mechanism treated as optional → EU AI Act Article 14 makes it mandatory for high-risk systems
