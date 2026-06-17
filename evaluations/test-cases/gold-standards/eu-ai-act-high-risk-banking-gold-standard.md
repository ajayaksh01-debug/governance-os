---
fixture_id: eu-ai-act-high-risk-banking
gold_standard_id: eu-ai-act-high-risk-banking-gold-standard
skills_covered: ["regulatory-mapping", "governance-control-mapping"]
subject_name: Consumer Credit Scoring Model
jurisdictions: ["EU", "UK"]
industry: Banking
regulatory_mapping_score: 91
regulatory_mapping_band: Exemplary
governance_control_mapping_score: 88
governance_control_mapping_band: Exemplary
claims_firewall_status: Pass
date: 2026-06-18
---

# Gold Standard Output: EU AI Act High-Risk — Consumer Credit Scoring Model

> **Usage:** This document is an expected-output gold standard for the `eu-ai-act-high-risk-banking` fixture. It demonstrates structurally and substantively correct outputs from the regulatory-mapping and governance-control-mapping skills for a high-risk credit scoring system across EU and UK jurisdictions. Validate this document against baselines using regression_tester.py.

---

# Part A — Regulatory Mapping Output

**Date of Assessment:** 2026-06-18  
**Subject Type:** AI System (deployed)  
**Jurisdictions Assessed:** EU (Germany, Netherlands primary), UK  
**Industry:** Retail Banking (BFSI)  
**Evidence Quality:** High  
**Assessment Status:** Final  
**Traceability ID:** TR-RW-GOLD-001

score: 91/100

---

### 1. Applicable Regulations

| Regulation | Jurisdiction | Applicability Status | Trigger |
|---|---|---|---|
| EU AI Act (Regulation (EU) 2024/1689) | EU | Confirmed — High-risk (Annex III, Point 5) | AI system used by credit institution subject to CRD IV to assess creditworthiness of natural persons; automated credit decision with legal/significant effects |
| GDPR (Regulation (EU) 2016/679) | EU | Confirmed | Processing personal data of EU data subjects; Article 22 (automated individual decision-making with legal or similarly significant effects including credit refusals); Article 35 DPIA required |
| UK GDPR | UK | Confirmed | Processing personal data of UK data subjects (UK operations via Eurobank UK Ltd); Article 22 equivalent applies; ICO AI guidance in scope |
| Data Protection Act 2018 | UK | Confirmed | UK primary data protection legislation; Section 49 automated processing safeguards; Schedule 1 processing conditions |
| FCA AI and Data Guidance (including Consumer Duty PRIN 12) | UK | Confirmed | FCA-regulated entity (Eurobank UK Ltd); Consumer Duty outcomes framework engaged for AI credit decisioning affecting UK retail consumers |
| PRA SS1/23 — Model Risk Management | UK | Confirmed — Tier 1 | Material model: automated credit scoring driving underwriting decisions with direct impact on firm financial position and customer outcomes; Tier 1 classification applies |
| EBA Guidelines on Internal Governance (EBA/GL/2021/05) | EU | Confirmed | Credit institution using material model; EBA guidelines on internal governance require AI model risk management oversight at board and senior management level |
| Equality Act 2010 | UK | Conditional | Postcode proxy variable identified in training data; indirect discrimination risk on grounds of race and/or belief; materialises if postal code correlates with protected characteristics — DPIA must investigate |

**Regulations assessed and determined not applicable:**

| Regulation | Rationale |
|---|---|
| DPDP Act 2023 | No India nexus; organisation has no Indian operations or Indian data subjects |
| India RBI/SEBI/IRDAI regulations | No India nexus |
| OWASP LLM Top 10 | Subject is XGBoost ML classifier; no LLM or generative AI components present |

---

### 2. Applicable Governance Frameworks

**ISO 42001**

Relevant clauses and Annex A controls for a high-risk credit decisioning AI system:

| ISO 42001 Element | Applicability | Rationale |
|---|---|---|
| Clause 4 (Context) | Confirmed | Operating context of credit scoring model includes regulatory environment, affected stakeholders (retail borrowers), and organisational risk appetite |
| Clause 5 (Leadership) | Confirmed | Board-level accountability for AI risk management expected under EBA internal governance guidelines and PRA SS1/23 Principle 5 |
| Clause 6 (Planning) | Confirmed | AI risk assessment required; Annex III high-risk classification elevates planning obligations |
| Clause 8 (Operation) | Confirmed | Lifecycle controls, AI impact assessment (EU AI Act Article 27), training data governance (Article 10) |
| Clause 9 (Performance) | Confirmed | Post-market monitoring (EU AI Act Article 72), model performance monitoring (PRA SS1/23 Principle 3) |
| Clause 10 (Improvement) | Confirmed | Corrective action processes for model failures and bias findings |
| Annex A.2 (AI Policy) | Confirmed | Organisational AI policy must address high-risk AI system governance |
| Annex A.5 (AI Risk Management) | Confirmed | Risk management process for high-risk system required |
| Annex A.8 (Data for AI) | Confirmed | Training data quality, provenance, and governance (Article 10 EU AI Act requirement) |
| Annex A.9 (Transparency) | Confirmed | Transparency obligations under EU AI Act Article 13; explainability for credit decisions |
| Annex A.10 (Human Oversight) | Confirmed | Article 14 mandatory human oversight for high-risk systems |

AIMS scope: The credit scoring model falls within the scope of a certifiable AI Management System. If the organisation is pursuing ISO 42001 certification, this system is a primary in-scope AI system.

**NIST AI RMF**

| Function | Applicability | Primary engagement |
|---|---|---|
| GOVERN | Confirmed | AI governance policy, risk appetite for high-risk credit decisions, board-level accountability, third-party oversight (credit bureau data vendors) |
| MAP | Confirmed | Risk context: affected population (loan applicants), harm pathways (credit refusal, discriminatory scoring), impact assessment |
| MEASURE | Confirmed | Bias testing, performance monitoring, validation (independent model validation under PRA SS1/23), explainability metrics |
| MANAGE | Confirmed | Human oversight controls, corrective action for adverse outputs, incident response for model failure |

---

### 3. Regulatory Obligations

| Obligation Description | Legal Basis | Type | Timeline |
|---|---|---|---|
| Register AI system in EU AI Act database as high-risk AI system | EU AI Act Article 49, Annex III | Registration | Before deployment; registration must precede go-live |
| Prepare and maintain Technical Documentation as specified in Annex IV | EU AI Act Article 11, Annex IV | Documentation | Before deployment; update on material changes |
| Conduct Fundamental Rights Impact Assessment before deployment | EU AI Act Article 27 | Assessment | Before deployment; deployer obligation |
| Implement human oversight mechanism — natural persons must be able to understand and override the system | EU AI Act Article 14 | Assessment / Monitoring | Before deployment; ongoing |
| Ensure transparency to affected natural persons — information about automated processing of their data | EU AI Act Article 13 | Disclosure | Before deployment; ongoing |
| Conduct and document post-market monitoring of system performance and accuracy | EU AI Act Article 72 | Monitoring | Ongoing from deployment |
| Conduct Data Protection Impact Assessment (DPIA) | GDPR Article 35(3)(a); UK GDPR Article 35 | Assessment | Before deployment; update on material change |
| Implement GDPR Article 22 safeguards for automated credit decisions — right to human review, contest, expression of view | GDPR Article 22(2)(b), (3); UK GDPR Article 22 | Monitoring / Disclosure | Before deployment; ongoing |
| Provide meaningful information to data subjects about automated credit decisions (right to explanation) | GDPR Article 22(3); UK GDPR Article 22(3) | Disclosure | On request; before decision finalised |
| Ensure data quality, representativeness, and absence of discriminatory patterns in training data | EU AI Act Article 10(3), (4) | Assessment / Documentation | Before deployment; ongoing with data updates |
| Comply with Records of Processing Activities (ROPA) obligation | GDPR Article 30 | Documentation | Ongoing |
| Maintain model documentation per PRA SS1/23 Principle 1 | PRA SS1/23 Principles 1–5 | Documentation | Before deployment; update on material change |
| Conduct independent model validation per PRA SS1/23 Principle 2 | PRA SS1/23 Principle 2 | Assessment | Before deployment; periodic review |
| Implement ongoing model performance monitoring and risk reporting per PRA SS1/23 Principle 3 | PRA SS1/23 Principle 3 | Monitoring / Reporting | Ongoing from deployment |
| Demonstrate compliance with FCA Consumer Duty — fair treatment of customers in AI credit decisioning | FCA PRIN 12; Consumer Duty Product/Service and Consumer Understanding outcomes | Assessment / Monitoring | Ongoing |
| Assess Equality Act indirect discrimination risk arising from postcode proxy variable | Equality Act 2010, Sections 19, 29 | Assessment | Before deployment; update on DPIA findings |

---

### 4. Risk Classification

**EU AI Act Classification**

**Classification: High-risk — Annex III, Point 5**

Rationale: The EU AI Act Annex III, Point 5(b) explicitly lists AI systems used by credit institutions subject to Directive 2013/36/EU (CRD IV) to evaluate the creditworthiness of natural persons as a high-risk AI system. Eurobank Retail S.A. is subject to CRD IV. The credit scoring model evaluates creditworthiness and produces automated approval/decline recommendations with legal or similarly significant effects on applicants.

Full high-risk obligations apply under EU AI Act Articles 8–15:
- Article 8: General obligations for high-risk AI systems
- Article 9: Risk management system
- Article 10: Training data requirements
- Article 11: Technical documentation
- Article 12: Record-keeping and logging
- Article 13: Transparency and provision of information
- Article 14: Human oversight
- Article 15: Accuracy, robustness, and cybersecurity

**GPAI:** Not applicable — system is a purpose-built ML classifier, not a General Purpose AI model.

**UK Regulatory Classification**

- **FCA materiality:** The credit scoring model is material to Eurobank UK Ltd's regulated activities. Consumer credit decisioning is a regulated activity; AI use in credit decisions is explicitly within FCA AI guidance scope.
- **PRA SS1/23 model tier:** Tier 1. The model directly influences credit underwriting decisions with material financial impact on the firm's credit portfolio and direct impact on customer outcomes. Independent validation and senior management oversight are required.
- **ICO high-risk processing:** DPIA mandatory under UK GDPR Article 35 — systematic automated evaluation of natural persons with financial decisions resulting from that evaluation.

**India Regulatory Classification**

Not applicable — no India nexus.

---

### 5. Documentation Requirements

| Document | Regulatory source | Content requirements | Maintenance |
|---|---|---|---|
| Technical Documentation (Annex IV) | EU AI Act Article 11 | General description, design methodology, training/validation/test data description, performance metrics, human oversight design, risk management system description | Before deployment; update on material changes |
| Fundamental Rights Impact Assessment | EU AI Act Article 27 | Assessment of likely impact on fundamental rights; categories of affected persons; safeguards implemented | Before deployment; update on material change |
| Data Protection Impact Assessment (DPIA) | GDPR Article 35 / UK GDPR Article 35 | Description of processing, necessity and proportionality assessment, risks to data subjects, measures to address risks | Before deployment; review annually or on material change |
| EU AI Act Database Registration Record | EU AI Act Article 49 | Registration data per Annex VIII | Before deployment; update on change |
| Records of Processing Activities (ROPA) | GDPR Article 30 / UK GDPR Article 30 | Purpose, categories of data, data subjects, recipients, retention, security measures | Ongoing |
| Model Documentation | PRA SS1/23 Principle 1 | Model purpose, scope, inputs/outputs, methodology, limitations, performance expectations, validation history | Before deployment; update on material change |
| Independent Model Validation Report | PRA SS1/23 Principle 2 | Validation scope, methodology, findings, remediation tracking | Before deployment; periodic review (annual minimum) |
| Training Data Governance Record | EU AI Act Article 10 | Data sources, quality criteria, bias assessment, representativeness assessment, data lineage | Before deployment; update on each significant data refresh |
| Consumer Duty Assessment | FCA PRIN 12 | Evidence of how each Consumer Duty outcome is met for AI-driven credit decisions | Before deployment; annual board review |
| Equality Act Bias Audit Record | Equality Act 2010 (conditional) | Proxy variable analysis, protected characteristic correlation assessment, remediation plan if risk confirmed | Before deployment; periodic review |

---

### 6. Control Requirements

| Control | Regulatory source | Type | Mandatory |
|---|---|---|---|
| Human oversight mechanism — the model's recommendations must be reviewable, understandable, and overridable by designated natural persons | EU AI Act Article 14 | Preventive | Mandatory |
| Right to human review — applicants declined via automated decision must be offered human review before the decision is finalised | GDPR Article 22(3); UK GDPR Article 22(3) | Preventive / Process | Mandatory |
| Explainability output — model must generate a plain-language explanation of credit decisions for applicant disclosure | EU AI Act Article 13; GDPR Article 22(3); FCA Consumer Duty | Detective / Disclosure | Mandatory |
| Training data quality gate — statistical tests for representativeness and bias before each model retrain | EU AI Act Article 10(3)(4) | Preventive | Mandatory |
| Bias monitoring — ongoing runtime analysis of approval/decline rates by demographic proxy (postcode band) | EU AI Act Article 9; Equality Act 2010 | Detective | Mandatory |
| Model performance monitoring — monthly drift detection and accuracy tracking against holdout dataset | EU AI Act Article 72; PRA SS1/23 Principle 3 | Detective | Mandatory |
| Audit logging — immutable log of every scoring event: input hash, output score, routing decision, timestamp, model version | EU AI Act Article 12; GDPR Article 5(2) accountability | Detective | Mandatory |
| Model access controls — only authorised AI engineers and compliance functions may access model weights, training data, and scoring API | ISO 42001 Annex A.5; GDPR Article 32 | Preventive | Mandatory |
| Incident response procedure — defined response for model outage, significant accuracy drift, or bias audit finding | EU AI Act Article 72; PRA SS1/23 Principle 4 | Corrective | Mandatory |
| Annual independent model validation — validation by a party independent of the model development team | PRA SS1/23 Principle 2 | Process | Mandatory |

Note on Bias Scanner (Ethana): Ethana's Bias Scanner (Production) detects and flags statistical disparity in model outputs at runtime. It is appropriate for the runtime bias monitoring control listed above. It does **not** satisfy EU AI Act Article 10 training data quality requirements, which require bias assessment on training datasets — not runtime outputs. The Bias Scanner's mandatory caveat applies: it does not audit training data, statistical disparity across demographic groups in the training corpus, or satisfy the bias audit requirements of EU AI Act Art.10 or NYC Local Law 144. Separate training data governance controls are required for Art.10 compliance.

---

### 7. Audit Evidence Required

| Evidence type | Purpose | Source | Retention |
|---|---|---|---|
| EU AI Act Annex IV Technical Documentation (signed) | Demonstrates conformity with high-risk AI obligations | AI development team; model card | Duration of system lifecycle + 10 years post-withdrawal |
| DPIA (signed, dated) | Demonstrates Article 35 compliance; identifies and mitigates risks to data subjects | DPO-led assessment | Duration of processing + 3 years |
| Fundamental Rights Impact Assessment | Demonstrates deployer compliance with Article 27 | Compliance team | Duration of deployment |
| Model Validation Report (independent) | Demonstrates PRA SS1/23 Principle 2 compliance | Independent model risk function or third-party validator | 7 years (PRA examination standard) |
| Scoring event audit log (immutable) | Provides traceability of every automated credit decision | Immutable logging system (e.g., Ethana Immutable Audit Log) | 6 years (FCA consumer credit record-keeping) |
| Bias monitoring reports (monthly) | Evidence of ongoing fairness monitoring | Automated model monitoring pipeline | 5 years |
| Training data quality assessment reports | Evidence of Article 10 compliance | Data governance function | Duration of model lifecycle |
| Consumer Duty board papers and sign-offs | Evidence of FCA Consumer Duty compliance | Board secretariat | 7 years |
| Customer Article 22 disclosure records | Evidence that automated decision safeguards were communicated | Customer-facing system logs | 6 years |

---

### 8. BFSI Considerations

**EU BFSI:**

EBA Guidelines on Internal Governance (EBA/GL/2021/05) require credit institutions to have robust internal governance arrangements for material models. For a credit scoring model:
- The management body must be informed of material AI models and their risk profile
- There must be a clear model risk framework addressing development, validation, deployment, and ongoing monitoring
- Third-party data vendors (credit bureaus, data providers) must be subject to vendor risk management under EBA outsourcing guidelines

The European Central Bank's SSM expectations on AI in banking note that AI credit decisioning models should be subject to the same level of governance scrutiny as internal ratings-based (IRB) models for capital purposes.

**UK BFSI:**

**PRA SS1/23 (Supervisory Statement — Model Risk Management Principles for Banks):**
- **Principle 1 (Model identification and model risk classification):** Credit scoring model with automated decisioning must be formally identified and classified. Tier 1 classification applies given material financial and customer impact.
- **Principle 2 (Model validation):** Independent validation required before deployment. Validation must cover conceptual soundness, implementation integrity, outcome analysis, and ongoing monitoring.
- **Principle 3 (Effective use):** Model outputs (approve/decline/refer) must be used within defined parameters; model limitations must be communicated to business users; override rates must be monitored.
- **Principle 4 (Model risk management):** Senior management must approve and periodically review material models. Model risk appetite statement required.
- **Principle 5 (Governance):** Board-level visibility of material model inventory and performance.

**FCA Consumer Duty (PRIN 12) — Insurance and banking applications:**
- **Products and Services Outcome:** The credit decisioning algorithm is a product feature; it must produce fair outcomes for customers.
- **Consumer Understanding Outcome:** Customers must understand the basis on which credit decisions are made; plain-language explanations are required.
- **Consumer Support Outcome:** Customers who receive adverse automated decisions must be supported in exercising their rights (human review, data subject access, dispute).

**Supervisory examination expectations:** A PRA/FCA examination of this model would expect: (a) model inventory entry with Tier 1 classification; (b) validation report from independent function; (c) evidence of human oversight mechanism; (d) DPIA and FRIA documentation; (e) Consumer Duty assessment; (f) audit log of automated decisions.

---

### 9. Executive Summary

Eurobank Retail S.A.'s consumer credit scoring model presents the highest level of regulatory complexity currently in scope: the system is explicitly classified as high-risk under EU AI Act Annex III, Point 5, triggering a full conformity obligation set including technical documentation, fundamental rights impact assessment, mandatory human oversight, post-market monitoring, and EU AI Act database registration. These obligations must be met before go-live.

In parallel, GDPR Article 22 applies because the model produces automated decisions with legal effects for applicants. Applicants must be provided with meaningful information about the decision, offered the right to human review, and given the ability to contest the outcome. The current system design (fully automated for sub-€15,000 applications) does not include these safeguards and must be re-engineered before deployment.

In the UK, Eurobank UK Ltd's FCA Consumer Duty and PRA SS1/23 obligations compound the EU requirements. Independent model validation is required, and the Consumer Duty imposes specific obligations to ensure customers understand and can contest AI-driven credit decisions. The postcode proxy variable represents a conditional Equality Act 2010 risk that must be assessed in the DPIA.

The highest-priority compliance actions are: (1) halt deployment until the fundamental rights impact assessment and DPIA are complete; (2) re-design the sub-€15,000 automated approval path to include a Article 22 safeguard mechanism; (3) commission independent model validation before go-live; (4) commission a training data bias assessment for the postcode variable.

---

# Part B — Governance Control Mapping Output

> **GCM Gold Standard:** This section demonstrates the expected governance-control-mapping output following the regulatory-mapping above. Validated against `evaluations/baselines/governance-control-mapping/structure.json`.

**Upstream source:** Regulatory Mapping (TR-RW-GOLD-001)  
**Target maturity level:** L3 (Defined)  
**Client sector:** BFSI (Banking)  
**Jurisdictions:** EU, UK  
**Deployment model:** Cloud SaaS  
**GCM Score:** 88/100  
**Claims Firewall:** Pass — 0 violations

---

### Section 1: Executive Summary & Control Landscape

The Eurobank credit scoring system requires a defence-in-depth control architecture spanning preventive, detective, and corrective layers across three domains: regulatory compliance (EU AI Act, GDPR Article 22, UK GDPR, PRA SS1/23), fairness and bias (Equality Act 2010, EU AI Act Article 10), and platform governance (explainability, audit trail, access control).

Of the 12 controls designed in this specification:
- 4 are Fully Covered by Ethana (Immutable Audit Log, Runtime Guardrails output filter, PII Scanner, LLM Gateway)
- 2 are Partially Covered by Ethana (Bias Scanner runtime monitoring with mandatory training-data caveat)
- 3 are Customer-Owned Controls (human oversight mechanism, Article 22 human review process, annual independent validation)
- 3 are Third-Party Controls Required (training data quality gate, credit bureau data governance, independent validation tooling)

The most critical control gap is the Article 22 human review path: the current system architecture does not include a mechanism for applicants to request human review before an automated credit decision is finalised. This is a mandatory control required before any deployment can be authorised.

**Claims Firewall Note:** All Ethana capabilities referenced in Section 10 are Production-status. Bias Scanner is referenced with its mandatory caveat: it addresses runtime bias monitoring (Section 5) but does NOT satisfy EU AI Act Article 10 training data governance requirements. Training data bias controls are classified as Third-Party Controls Required.

---

### Section 2: Control Taxonomy Matrix

| Control ID | Control Name | Control Type | Control Method | Primary Risk Mitigated |
|---|---|---|---|---|
| CTRL-EU-01 | Article 22 Human Review Path | Preventive | Process | Automated decision without safeguards (GDPR Art.22 violation) |
| CTRL-EU-02 | Explainability Output Engine | Preventive | Technical | Consumer credit decision opaque to applicant |
| CTRL-EU-03 | Training Data Quality Gate | Preventive | Process | Discriminatory/biased training data (EU AI Act Art.10) |
| CTRL-EU-04 | Human Oversight Interface | Preventive | Technical / Process | Model output followed without oversight (EU AI Act Art.14) |
| CTRL-EU-05 | Scoring Event Audit Log | Detective | Technical | Untraceable automated credit decisions |
| CTRL-EU-06 | Runtime Bias Monitor | Detective | Technical | Post-deployment discrimination (Equality Act, Art.9) |
| CTRL-EU-07 | Model Performance Monitor | Detective | Technical | Model drift leading to inaccurate credit decisions |
| CTRL-EU-08 | PII/Financial Data Access Control | Preventive | Technical | Unauthorised access to applicant personal data |
| CTRL-EU-09 | Model Access and Version Control | Preventive | Technical | Unauthorised model modification; version confusion |
| CTRL-EU-10 | Incident Response — Model Failure | Corrective | Process | Uncontrolled impact of model outage or accuracy failure |
| CTRL-EU-11 | Independent Model Validation | Corrective | Process | Undetected model deficiencies (PRA SS1/23 Principle 2) |
| CTRL-EU-12 | Consumer Duty Evidence Package | Detective | Process | Inability to demonstrate FCA Consumer Duty compliance |

---

### Section 3: Control Coverage Classification

| Control ID | Coverage Classification | Notes |
|---|---|---|
| CTRL-EU-01 | Customer-Owned Control | Process redesign of automated decision workflow; not addressable by platform |
| CTRL-EU-02 | Partially Covered by Ethana | Ethana's Immutable Audit Log captures scoring event and feature importance; explainability formatting for customer disclosure is customer-built on top |
| CTRL-EU-03 | Third-Party Control Required | Training data quality assessment tools (e.g., Great Expectations, custom statistical tests); not in Ethana Production scope |
| CTRL-EU-04 | Partially Covered by Ethana | Ethana provides model routing controls; human override interface is customer-built into origination system |
| CTRL-EU-05 | Fully Covered by Ethana | Ethana Immutable Audit Log (Production) — insert-only event store; SIEM export; configurable retention |
| CTRL-EU-06 | Partially Covered by Ethana | Ethana Bias Scanner (Production) covers runtime output monitoring. **Does NOT satisfy EU AI Act Art.10 training data bias audit requirements** — Bias Scanner is a runtime filter only and does not audit training data. Third-party training data bias tooling required for Art.10 compliance. |
| CTRL-EU-07 | Third-Party Control Required | Model performance monitoring (drift detection, accuracy tracking) requires MLOps tooling (e.g., Evidently, MLflow); not in Ethana Production scope |
| CTRL-EU-08 | Fully Covered by Ethana | Ethana Runtime Guardrails (Production) + Ethana PII Scanner (Production) for access and data protection at inference layer |
| CTRL-EU-09 | Customer-Owned Control | Model registry and version control (MLflow, DVC or equivalent); Ethana does not manage customer model weights |
| CTRL-EU-10 | Customer-Owned Control | Incident response procedure and runbook; Cursory Advisory can design the playbook (Covered by Cursory Service) |
| CTRL-EU-11 | Covered by Cursory Service | Cursory AI Governance Advisory — independent model validation engagement |
| CTRL-EU-12 | Fully Covered by Ethana | Ethana Immutable Audit Log (Production) provides the audit evidence chain; Consumer Duty reports are assembled by compliance team from Audit Log exports |

---

### Section 4: Preventive Control Specifications

**CTRL-EU-01 — Article 22 Human Review Path**

- **Trigger Condition:** Credit application receives automated Decline recommendation AND the applicant's data falls within automated decisioning scope (below €15,000)
- **Enforcement Mechanism:** Before the Decline is finalised and communicated to the applicant, the origination system must present the applicant with: (a) information about the automated nature of the decision, (b) the right to request human underwriter review, (c) the right to contest the decision, (d) the right to express a point of view. The automated decline must not be finalised until the disclosure is presented and the applicant has had an opportunity to exercise rights.
- **Failure Mode:** Fail-Closed — if the human review path cannot be offered (system failure), the application must be routed to a human underwriter by default.

**CTRL-EU-02 — Explainability Output Engine**

- **Trigger Condition:** Any automated credit decision (Approve, Decline, or Refer)
- **Enforcement Mechanism:** The scoring API must return, alongside every credit decision recommendation, a structured explainability payload: (a) the top 3 input features driving the decision and their directional contribution (increase/decrease score); (b) the risk band assigned; (c) a plain-language summary generated from a template using the feature importance data. The template must be approved by Compliance before deployment.
- **Failure Mode:** Fail-Closed — if the explainability payload cannot be generated, the decision must not be released to the origination system.

**CTRL-EU-03 — Training Data Quality Gate**

- **Trigger Condition:** Before each model training run and before each significant data refresh
- **Enforcement Mechanism:** Statistical validation suite must pass before new training data is used: (a) representativeness check — distribution of credit outcomes by postcode band must be logged and reviewed for proxy variable risk; (b) completeness check — missing data rates by feature must be within defined thresholds; (c) recency check — no training data older than 8 years; (d) bias baseline — approval rate differentials by postcode band must be documented and reviewed by Compliance.
- **Failure Mode:** Fail-Closed — training run blocked until quality gate passes.

**CTRL-EU-04 — Human Oversight Interface**

- **Trigger Condition:** Underwriter reviews a Refer-band application
- **Enforcement Mechanism:** The underwriter dashboard must display: (a) the model's score and band; (b) the top 5 contributing features with plain-language labels; (c) a mandatory "Override" button with an override reason field; (d) a disclaimer that the model recommendation is advisory and human judgement governs the final decision.
- **Failure Mode:** Fail-Open — if the oversight interface is unavailable, underwriters continue to review applications using their own judgement; model scores must not be the sole input.

**CTRL-EU-08 — PII/Financial Data Access Control**

- **Trigger Condition:** Any API call to the credit scoring endpoint
- **Enforcement Mechanism:** Ethana Runtime Guardrails (Production) configured with PII detection — applicant personal data fields are validated before entering the scoring pipeline; any response containing account data beyond the structured scoring output is blocked. Ethana PII Scanner (Production) monitors inference-time data leakage.
- **Failure Mode:** Fail-Closed on PII leakage detection.

---

### Section 5: Detective Control Specifications

**CTRL-EU-05 — Scoring Event Audit Log**

- **Logging Source:** Credit scoring API via Ethana Immutable Audit Log (Production)
- **Telemetry Format:** Structured JSON per scoring event — `{event_id, timestamp, application_id, model_version, input_hash (salted SHA-256), output_score, output_band, routing_decision, explainability_payload_hash, human_review_offered: boolean, human_review_taken: boolean}`
- **Alerting Thresholds:** Zero — all scoring events are logged unconditionally
- **Routing Target:** Compliance monitoring dashboard; SIEM (Splunk) via Ethana native export

**CTRL-EU-06 — Runtime Bias Monitor**

- **Logging Source:** Ethana Bias Scanner (Production) — runtime output filter
- **Telemetry Format:** Per-decision bias flag: `{event_id, postcode_band, output_band, bias_flag: boolean, confidence}`. Aggregated: weekly distribution report across postcode bands.
- **Alerting Thresholds:** If decline rate in any postcode quintile exceeds the overall decline rate by >25 percentage points for three consecutive weeks, alert to Chief Risk Officer
- **Routing Target:** Risk Management team; weekly report to Compliance; quarterly board pack inclusion
- **Mandatory caveat:** This control monitors runtime outputs only. It does NOT satisfy EU AI Act Article 10 requirements for training data bias assessment. See CTRL-EU-03 for training data governance.

**CTRL-EU-07 — Model Performance Monitor**

- **Logging Source:** MLOps monitoring pipeline (third-party — customer-managed)
- **Telemetry Format:** Monthly model performance report — AUC, Gini coefficient, KS statistic, default prediction accuracy against realised defaults (lagged 90 days), feature drift indicators
- **Alerting Thresholds:** AUC degradation >3% from baseline triggers Amber alert; >7% degradation triggers Red alert requiring immediate senior review
- **Routing Target:** Model Risk Management; Risk Committee; quarterly to PRA SS1/23 governance committee

**CTRL-EU-12 — Consumer Duty Evidence Package**

- **Logging Source:** Ethana Immutable Audit Log exports + compliance assessment records
- **Telemetry Format:** Quarterly Consumer Duty evidence pack — aggregate scoring decisions, override rates, complaints related to credit decisions, explainability satisfaction (if surveyed), Article 22 disclosure completion rates
- **Alerting Thresholds:** Consumer Duty complaints related to AI credit decisions exceeding 0.1% of total decisions triggers board-level review
- **Routing Target:** FCA Consumer Duty Board Champion; Compliance function; annual board review

---

### Section 6: Corrective Control Specifications

**CTRL-EU-10 — Incident Response — Model Failure**

- **Activation Trigger:** Red alert from CTRL-EU-07 (>7% AUC degradation); bias monitor Amber/Red alert for three consecutive weeks; regulatory notification of model investigation
- **Containment Protocol:** (1) Immediately disable automated decisioning below €15,000 threshold; (2) All applications routed to human underwriters; (3) Chief Risk Officer notified within 1 hour; (4) DPO notified within 2 hours (potential GDPR Article 33 notification assessment required)
- **Recovery Procedure:** (1) Model investigation by model risk team (within 5 business days); (2) If retraining required, CTRL-EU-03 data quality gate must be executed first; (3) Independent validation of updated model before restoring automated decisioning; (4) PRA notification if model risk event meets SS1/23 incident reporting threshold
- **Rollback SLA:** Automated decisioning disabled within 30 minutes of Red alert; full human underwriting capacity activated within 2 hours

**CTRL-EU-11 — Independent Model Validation**

- **Activation Trigger:** Before initial deployment; before major model retrain (>20% of training data replaced or feature set materially changed); annually thereafter
- **Containment Protocol:** Model validation is a preventive/detective process; "containment" = validation findings requiring remediation halt deployment or retrain release until findings are addressed
- **Recovery Procedure:** Findings classified as Critical (model cannot be used) → model withdrawn and rebuilt; Major (significant remediation required) → 30-day remediation with validation re-check; Minor (documentation gaps, monitoring improvements) → 90-day remediation
- **Rollback SLA:** Critical findings: automated decisioning disabled within 24 hours of finding

---

### Section 7: Evidence & Verification Requirements

| Evidence ID | Evidence Name | Artifact Description | Collection Method | Frequency | Retention Period |
|---|---|---|---|---|---|
| EVD-EU-01 | Scoring Event Log | Immutable JSON log of all credit scoring events | Automated — Ethana Immutable Audit Log | Real-time | 6 years (FCA consumer credit) |
| EVD-EU-02 | Runtime Bias Report | Aggregate weekly bias monitoring data | Automated — Ethana Bias Scanner export | Weekly (automated); quarterly report (manual compilation) | 5 years |
| EVD-EU-03 | Training Data Quality Gate Report | Statistical validation results for each training data assessment | Manual — data governance team | Each training run | Duration of model lifecycle |
| EVD-EU-04 | DPIA (signed, dated) | Full DPIA document per GDPR Article 35 requirements | Manual — DPO-led | Before deployment; on material change | Duration of processing + 3 years |
| EVD-EU-05 | Fundamental Rights Impact Assessment | FRIA per EU AI Act Article 27 | Manual — Compliance team | Before deployment; on material change | Duration of deployment |
| EVD-EU-06 | Technical Documentation (Annex IV) | EU AI Act-compliant technical documentation | Manual — AI development team | Before deployment; on material change | Lifecycle + 10 years |
| EVD-EU-07 | Independent Validation Report | PRA SS1/23-compliant model validation report | Manual — independent model risk function or Cursory | Annual + on material retrain | 7 years (PRA standard) |
| EVD-EU-08 | Consumer Duty Quarterly Evidence Pack | Compiled evidence per CTRL-EU-12 specification | Manual — Compliance function | Quarterly | 7 years |
| EVD-EU-09 | Article 22 Disclosure Completion Log | Record that Article 22 disclosure was presented and acknowledged for each automated decline | Automated — origination system log | Per-event | 6 years |
| EVD-EU-10 | Model Performance Monthly Report | AUC, Gini, KS, drift indicators | Automated — MLOps pipeline | Monthly | 5 years |

---

### Section 8: Control Ownership Matrix (RACI)

| Control ID | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|---|---|---|---|---|
| CTRL-EU-01 | Credit Operations Engineering | Chief Risk Officer | DPO; Legal Counsel | Compliance; Model Risk |
| CTRL-EU-02 | AI Engineering | Head of AI Engineering | DPO; Compliance | Legal; Credit Operations |
| CTRL-EU-03 | Data Governance Team | Chief Data Officer | AI Engineering; Compliance | Model Risk; DPO |
| CTRL-EU-04 | AI Engineering | Head of AI Engineering | Credit Underwriting; Compliance | Model Risk |
| CTRL-EU-05 | AI Platform Engineering | CISO | Compliance; DPO | Audit; Credit Operations |
| CTRL-EU-06 | Model Risk Management | Chief Risk Officer | Compliance; DPO | Credit Operations; Board Risk Committee |
| CTRL-EU-07 | Model Risk Management | Chief Risk Officer | AI Engineering | Credit Operations; Audit |
| CTRL-EU-08 | AI Platform Engineering | CISO | DPO | Compliance |
| CTRL-EU-09 | AI Engineering | Head of AI Engineering | Model Risk Management | Compliance; Audit |
| CTRL-EU-10 | AI Platform Engineering | Chief Risk Officer | DPO; Legal; Compliance | Board Risk Committee; PRA (if notifiable) |
| CTRL-EU-11 | Model Risk Management | Chief Risk Officer | External Validator (Cursory Advisory) | PRA; Board Risk Committee |
| CTRL-EU-12 | Compliance Function | Chief Compliance Officer | DPO; AI Engineering | FCA Consumer Duty Board Champion; Board |

---

### Section 9: Maturity & Phased Roadmap

**Phase 1 — Days 1–30 (Foundations)**
- Halt automated deployment pending DPIA and FRIA completion (Compliance; DPO)
- Commission independent model validation (Model Risk Management; Cursory Advisory engagement)
- Activate Ethana Immutable Audit Log for scoring API (AI Platform Engineering)
- Deploy CTRL-EU-08 PII/data access controls (AI Platform Engineering)
- Assign all Accountable roles from RACI matrix; confirm acceptance (CRO)

**Phase 2 — Days 31–60 (Compliance Engineering)**
- Re-engineer application flow to include Article 22 human review path (Credit Operations Engineering)
- Deploy explainability output engine (CTRL-EU-02) and test customer disclosure templates with Compliance
- Activate Ethana Bias Scanner (Production) for runtime monitoring (AI Platform Engineering)
- Execute training data quality gate for current training dataset (Data Governance)
- Draft Technical Documentation (Annex IV) structure; assign writing responsibilities (AI Engineering)

**Phase 3 — Days 61–90 (Validation and Go-Live Readiness)**
- Complete and sign DPIA and FRIA (DPO; Compliance)
- Complete independent model validation; address findings (Model Risk Management)
- Submit EU AI Act database registration (Compliance; Legal)
- Conduct mock PRA examination preparation (Model Risk Management; Compliance)
- Verify all EVD-EU-01 through EVD-EU-10 evidence collection is operational before go-live approval

---

### Section 10: Ethana Configuration Guide

**Production Capability Mappings:**

| Control | Ethana Capability | Status | Configuration guidance |
|---|---|---|---|
| CTRL-EU-05 (Audit Log) | Immutable Audit Log | Production | Configure Ethana Audit Log on credit scoring API gateway. Enable structured JSON export. Configure Splunk SIEM integration for real-time log forwarding. Set 6-year retention policy. |
| CTRL-EU-06 (Bias Monitor) | Bias Scanner | Production | Deploy Bias Scanner on scoring API output stream. Configure postcode-band grouping for demographic proxy monitoring. Set weekly aggregate reporting. **Mandatory caveat: Bias Scanner monitors runtime outputs only — it does NOT satisfy EU AI Act Article 10 training data requirements. Training data bias assessment (CTRL-EU-03) requires separate tooling.** |
| CTRL-EU-08 (PII Control) | PII Scanner + Runtime Guardrails | Production | Deploy Ethana PII Scanner on inference input/output. Configure Runtime Guardrails to block responses containing personal data fields beyond structured scoring output. Fail-Closed mode. |

**Roadmap Capability References (not available for deployment):**

| Requirement | In Build Capability | Available workaround |
|---|---|---|
| Automated compliance pack evidence collection | Compliance Pack (In Build — not yet available) | Evidence collection via Ethana Immutable Audit Log exports + manual compilation per EVD-EU-08 Consumer Duty Evidence Pack specification |
| CI/CD model deployment gating | CI/CD Gate Integration (In Build — not yet available) | Manual validation sign-off gate by Model Risk Management and Compliance before each model version release; gate is documented in CTRL-EU-09 Model Access and Version Control |
