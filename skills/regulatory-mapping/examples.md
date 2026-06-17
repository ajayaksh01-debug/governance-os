# Regulatory Mapping — Worked Examples

This document contains three fully worked regulatory mapping assessments produced using the Regulatory Mapping skill. Each example demonstrates application of the complete workflow and output structure, covering both regulatory identification and governance framework mapping.

---

---

# Example 1: BFSI Credit Scoring Model — Multi-Jurisdictional Assessment

**Date of Assessment:** 2025-03-15  
**Subject Type:** AI Use Case  
**Jurisdictions Assessed:** EU, UK, India  
**Industry:** Banking / Lending (BFSI)  
**Evidence Quality:** High (detailed system specification provided)  
**Assessment Status:** Final

**Subject Description:** A mid-size Indian private sector bank, subsidiary of a UK-headquartered banking group, is deploying an ML-based credit scoring model. The model uses applicant demographic data, credit bureau data, transaction history, and alternative data (mobile usage patterns, utility payments) to generate a credit risk score for retail unsecured lending (personal loans, credit cards). The model will be used for automated pre-approval decisions up to ₹5 lakh and as a decision-support tool for higher amounts. The system processes personal data of Indian residents, UK residents (via the parent group's shared model infrastructure), and EU residents (via the parent group's European branch operations). The model is trained on historical lending data and is deployed on cloud infrastructure hosted in India (AWS Mumbai), with model artefacts replicated to the parent group's UK and EU environments.

---

## 1. Applicable Regulations

### EU Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| EU AI Act | **Applicable — High-risk (Annex III)** | Credit scoring is explicitly listed in Annex III, Category 5(b): "AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score." No ambiguity. |
| GDPR | **Applicable** | The system processes personal data of EU residents (via the parent group's European branch). Article 2(1) territorial scope is triggered. Article 22 (automated individual decision-making) is directly engaged for automated pre-approval decisions. |

### UK Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| UK GDPR / Data Protection Act 2018 | **Applicable** | The system processes personal data of UK residents via the parent group's shared model infrastructure. |
| Equality Act 2010 | **Applicable** | The credit scoring model makes decisions affecting access to financial services. If the model produces differential outcomes by protected characteristic (race, sex, age, disability), this constitutes indirect discrimination under Section 19. |
| FCA Handbook / Consumer Duty | **Applicable** | The parent group is FCA-authorised. The AI system directly affects consumer outcomes in lending — FCA Consumer Duty (PS22/9) applies. |
| PRA SS1/23 | **Applicable** | The parent group is PRA-regulated. A credit scoring model used for lending decisions is a material model under SS1/23. |

### India Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| DPDP Act 2023 | **Applicable** | The system processes personal data of Indian Data Principals (loan applicants). The bank is a Data Fiduciary. Given the volume of personal data processed (retail lending at scale), Significant Data Fiduciary (SDF) designation is likely. |
| RBI IT Governance Master Direction | **Applicable** | The bank is an RBI-regulated entity. The AI system is a technology system used in regulated banking activities. |
| RBI Model Risk Management Expectations | **Applicable** | Credit scoring is a material model directly affecting lending decisions. RBI supervisory expectations for model risk management apply. |
| SEBI AI/ML Circular | **Not applicable** | The bank is not a SEBI-registered entity for the purpose of this AI system. The credit scoring model does not involve securities trading or investment advisory. |
| IRDAI Guidance | **Not applicable** | The bank is not an IRDAI-regulated insurer. |

---

## 2. Applicable Governance Frameworks

### ISO 42001

**Applicable clauses:**
- **Clause 5 (Leadership):** The credit scoring model requires board-level or senior management oversight given its direct impact on consumer lending decisions and regulatory scrutiny. AI policy must cover model governance.
- **Clause 6 (Planning):** An AI risk assessment addressing bias risk, data quality risk, and regulatory compliance risk must be conducted before deployment. An AI impact assessment is required given the model directly affects individuals' access to credit.
- **Clause 8 (Operation):** Full lifecycle management — development, validation, deployment, and monitoring controls. Supply chain controls apply to the cloud infrastructure provider (AWS) and any third-party data providers (credit bureaus, alternative data sources).
- **Clause 9 (Performance Evaluation):** Ongoing monitoring for model performance degradation, bias drift, and regulatory compliance. Internal audit of the model governance framework.

**Applicable Annex A controls:**
- AI risk assessment and impact assessment controls
- Data governance controls (data provenance, data quality, data minimisation)
- Bias evaluation controls
- Human oversight controls (for decisions above automated threshold)
- Monitoring and drift detection controls
- Supply chain controls (credit bureau data, alternative data providers)
- Transparency and explainability controls

**AIMS scope:** The credit scoring model should be within the scope of the organisation's AIMS if pursuing ISO 42001 certification. Given the model's materiality, it would be a priority system within the AIMS.

### NIST AI RMF

- **GOVERN (Primary):** AI governance structure must be defined — who owns the model, who validates it, who approves deployment, and who monitors performance. AI risk appetite for credit decisions must be articulated.
- **MAP:** The risk context is well-defined: the model affects individuals' access to credit, creating bias risk, accuracy risk, and regulatory risk. Stakeholder analysis must include borrowers, regulators (RBI, FCA, EU authorities), and internal risk functions.
- **MEASURE:** Bias testing (demographic parity, equalised odds across gender, caste, religion, age), accuracy validation, performance monitoring in production, and adversarial robustness testing.
- **MANAGE:** Risk treatment controls — model validation programme, bias remediation procedures, incident response for model failures, and documentation for regulatory examination.

### OWASP LLM Top 10

**Not applicable.** The subject is an ML classifier (gradient boosting / logistic regression ensemble), not an LLM-based system. OWASP LLM Top 10 risk categories do not apply.

---

## 3. Regulatory Obligations

### EU AI Act Obligations (High-Risk AI System)

| Obligation | Legal Basis | Type | Timeline | Non-Compliance Consequence |
|---|---|---|---|---|
| Establish and maintain a risk management system throughout the AI system lifecycle | Article 9 | Assessment / Monitoring | By 2 August 2026 (Annex III) | Up to €15M or 3% global turnover |
| Implement data governance and management practices for training, validation, and test data | Article 10 | Documentation / Assessment | By 2 August 2026 | Up to €15M or 3% global turnover |
| Produce and maintain technical documentation (Annex IV) | Article 11 | Documentation | By 2 August 2026; ongoing maintenance | Up to €15M or 3% global turnover |
| Design the system to enable automatic recording of events (logging) | Article 12 | Documentation | By 2 August 2026 | Up to €15M or 3% global turnover |
| Ensure transparency — provide deployers with sufficient information to understand outputs | Article 13 | Disclosure | By 2 August 2026 | Up to €15M or 3% global turnover |
| Design for human oversight — enable human review and override of automated decisions | Article 14 | Assessment | By 2 August 2026 | Up to €15M or 3% global turnover |
| Ensure accuracy, robustness, and cybersecurity appropriate to the intended purpose | Article 15 | Assessment / Monitoring | By 2 August 2026 | Up to €15M or 3% global turnover |
| Conduct conformity assessment before placing on the market or putting into service | Article 43 | Registration | Before deployment in EU | Up to €15M or 3% global turnover |
| Register in the EU AI database | Article 49 | Registration | Before deployment in EU | Up to €7.5M or 1.5% global turnover |

### GDPR Obligations

| Obligation | Legal Basis | Type | Timeline | Non-Compliance Consequence |
|---|---|---|---|---|
| Establish lawful basis for processing personal data in AI training and inference | Article 6 | Assessment | Immediate (pre-deployment) | Up to €20M or 4% global turnover |
| Conduct DPIA for high-risk automated processing of personal data | Article 35 | Assessment / Documentation | Before deployment | Up to €20M or 4% global turnover |
| Provide meaningful information about automated decision-making logic | Article 22(3), Article 13(2)(f) | Disclosure | Immediate | Up to €20M or 4% global turnover |
| Ensure right not to be subject to solely automated decision-making with legal or significant effects | Article 22(1) | Assessment | Immediate | Up to €20M or 4% global turnover |
| Implement data subject access and rectification rights | Articles 15, 16 | Assessment | Immediate | Up to €20M or 4% global turnover |
| Report personal data breaches to supervisory authority within 72 hours | Article 33 | Notification | Triggered by breach event | Up to €20M or 4% global turnover |

### UK GDPR / Data Protection Act 2018 Obligations

Mirror GDPR obligations above with ICO as the supervisory authority. Additional UK-specific obligations:

| Obligation | Legal Basis | Type | Timeline |
|---|---|---|---|
| ICO AI and data protection guidance — conduct AI-specific impact assessment | ICO Guidance on AI and Data Protection | Assessment | Before deployment |
| Ensure compliance with Equality Act 2010 — no indirect discrimination in credit outcomes | Equality Act 2010 Section 19 | Assessment / Monitoring | Ongoing |

### PRA SS1/23 Obligations

| Obligation | Legal Basis | Type | Timeline |
|---|---|---|---|
| Identify and classify the model under the firm's model inventory | SS1/23 Principle 1 | Registration | Before deployment |
| Document model development, assumptions, and limitations | SS1/23 Principle 2 | Documentation | Before deployment; ongoing |
| Conduct independent model validation | SS1/23 Principle 3 | Assessment | Before deployment; periodic revalidation |
| Monitor model performance, stability, and outcomes in production | SS1/23 Principle 4 | Monitoring | Ongoing |
| Establish model risk governance with clear accountability | SS1/23 Principle 5 | Assessment | Immediate |

### DPDP Act 2023 Obligations

| Obligation | Legal Basis | Type | Timeline |
|---|---|---|---|
| Obtain consent or establish lawful basis for processing applicant personal data | DPDP Act Section 4–6 | Assessment | Before deployment |
| Implement reasonable security safeguards for personal data in training and inference | DPDP Act Section 8 | Assessment | Immediate |
| Accommodate Data Principal rights (access, correction, erasure) | DPDP Act Sections 11–14 | Assessment | Immediate |
| If designated SDF: appoint Data Protection Officer and conduct DPIA | DPDP Act Section 10 | Registration / Assessment | Upon SDF designation |

### RBI Obligations

| Obligation | Legal Basis | Type | Timeline |
|---|---|---|---|
| Governance of AI/ML systems under IT risk management framework | RBI IT Governance Master Direction 2023 | Assessment | Immediate |
| Model documentation, validation, and ongoing monitoring for credit models | RBI MRM supervisory expectations | Documentation / Monitoring | Before deployment; ongoing |
| Data localisation — payment system data must be stored in India | RBI Data Localisation Circular 2018 | Assessment | Immediate |
| Fair lending — explainability of credit decisions regardless of AI/human mechanism | RBI Fair Practices Code | Disclosure | Immediate |

---

## 4. Risk Classification

### EU AI Act Classification

**Classification: High-risk (Annex III, Category 5(b))**

Rationale: The AI system is "intended to be used to evaluate the creditworthiness of natural persons or establish their credit score" — this is explicitly listed in EU AI Act Annex III as a high-risk AI system. No ambiguity in classification. Full high-risk obligations apply from 2 August 2026.

### UK Regulatory Classification

**PRA SS1/23 Model Tier: Tier 1 (Material Model)**

Rationale: The credit scoring model directly affects the firm's lending decisions, financial performance (credit losses), and consumer outcomes. It meets all criteria for a Tier 1 model under SS1/23: material financial impact, significant consumer impact, and regulatory scrutiny.

**FCA Consumer Duty: Material AI System**

Rationale: The model directly determines consumer access to credit products. FCA Consumer Duty requires the firm to demonstrate good outcomes for retail customers — a credit model that produces unfair outcomes (bias, inaccuracy) would constitute a Consumer Duty breach.

### India Regulatory Classification

**DPDP Act: Likely Significant Data Fiduciary (SDF)**

Rationale: A bank processing credit application data at retail scale processes large volumes of personal data. SDF designation is likely, triggering additional obligations including mandatory DPIA and DPO appointment. Final determination depends on the SDF threshold criteria, which have not yet been published by MEITY.

**RBI: Material Model**

Rationale: Credit scoring models are within the core supervisory focus of RBI model risk management expectations. The model directly affects credit decisions for retail customers. Formal model documentation, independent validation, and ongoing monitoring are expected by RBI examiners.

---

## 5. Documentation Requirements

| Document | Regulatory Source | Content Requirements | Maintenance |
|---|---|---|---|
| EU AI Act Technical Documentation (Annex IV) | EU AI Act Article 11 | System description, design specifications, development methodology, data governance practices, testing results, risk management measures, human oversight measures, accuracy metrics | Ongoing; update upon material changes |
| DPIA (EU) | GDPR Article 35 | Description of processing, necessity assessment, risk assessment for data subject rights, mitigation measures | Before deployment; review periodically |
| DPIA (India) | DPDP Act Section 10 (if SDF) | Processing purpose, data types, risk assessment, safeguards implemented | Before deployment; review periodically |
| Model Documentation | PRA SS1/23 Principle 2, RBI MRM | Model design, assumptions, limitations, intended use, training data description, feature engineering, validation results, performance benchmarks | Before deployment; update upon retraining |
| Model Validation Report | PRA SS1/23 Principle 3, RBI MRM | Independent validation methodology, findings, limitations identified, recommendations, sign-off | Before deployment; periodic revalidation |
| Conformity Declaration | EU AI Act Article 47 | Declaration that the AI system complies with high-risk requirements | Before EU deployment |
| AI Policy | ISO 42001 Clause 5 | Organisational AI policy covering governance structure, risk appetite, roles and responsibilities | Ongoing |
| AI Impact Assessment | ISO 42001 Clause 6 | Assessment of potential impacts on individuals and groups from the credit scoring system | Before deployment; review upon changes |
| Bias Evaluation Report | ISO 42001 Annex A, NIST MEASURE | Fairness metrics, demographic analysis, disparate impact testing results | Before deployment; ongoing monitoring reports |
| Data Governance Records | EU AI Act Article 10, ISO 42001 Annex A | Training data provenance, quality assessment, demographic representation analysis | Ongoing |

---

## 6. Control Requirements

| Control | Source | Type | Classification | Guidance |
|---|---|---|---|---|
| Bias testing across protected characteristics | EU AI Act Art.10, Equality Act 2010, ISO 42001 Annex A | Preventive / Detective | Mandatory | Test model outputs for demographic parity, equalised odds, and disparate impact across gender, age, caste/ethnicity, and disability before deployment and periodically in production |
| Human oversight for automated decisions | EU AI Act Art.14, GDPR Art.22, RBI Fair Practices | Preventive | Mandatory | Enable human review and override for credit decisions. For automated pre-approval, ensure a meaningful human review mechanism exists for appeals and edge cases |
| Model validation by independent function | PRA SS1/23 Principle 3, RBI MRM | Detective | Mandatory | Model validation must be conducted by a team independent of model development. Validation must cover accuracy, stability, bias, and regulatory compliance |
| Explainability for credit decisions | FCA Consumer Duty, RBI Fair Practices, GDPR Art.22 | Preventive | Mandatory | Provide applicants with meaningful reasons for credit decisions. Model must support feature importance or counterfactual explanations |
| Data quality assessment for training data | EU AI Act Art.10, ISO 42001 Annex A | Preventive | Mandatory | Assess training data for completeness, accuracy, demographic representation, and historical bias before model training |
| Production performance monitoring | PRA SS1/23 Principle 4, RBI MRM, ISO 42001 Cl.9 | Detective | Mandatory | Monitor model performance metrics (accuracy, stability, bias metrics) in production. Alert on degradation or drift |
| Data localisation compliance | RBI Data Localisation Circular | Preventive | Mandatory | Ensure payment system data and personal data processed for Indian lending decisions is stored in India. Model inference for Indian applicants must use India-hosted infrastructure |
| Audit logging of all credit decisions | EU AI Act Art.12, RBI IT Governance, ISO 42001 Annex A | Detective | Mandatory | Log every credit decision with input data, model version, score, and outcome. Logs must be immutable and retained per regulatory requirements |
| Supply chain assessment for data providers | ISO 42001 Cl.8.4, NIST MAP | Preventive | Recommended | Assess credit bureau and alternative data providers for data quality, bias, and contractual compliance |
| Adversarial robustness testing | EU AI Act Art.15, NIST MEASURE | Preventive | Recommended | Test model for robustness against adversarial inputs (data manipulation, feature gaming) |

---

## 7. Audit Evidence Required

| Evidence | Purpose | Source | Retention | Format |
|---|---|---|---|---|
| Model validation report (initial and periodic) | Demonstrates independent validation of model accuracy, bias, and fitness | PRA SS1/23, RBI MRM | Duration of model use + 5 years | Narrative report with quantitative results |
| Bias testing results (pre-deployment and periodic) | Demonstrates fairness across protected characteristics | EU AI Act Art.10, Equality Act 2010, ISO 42001 | Duration of model use + 5 years | Structured data (metrics by demographic group) |
| DPIA documentation | Demonstrates risk assessment and mitigation for personal data processing | GDPR Art.35, DPDP Act Section 10 | Duration of processing + 3 years | Narrative report |
| Decision audit logs | Demonstrates traceability of individual credit decisions | EU AI Act Art.12, RBI IT Governance | Per RBI retention requirements (minimum 8 years for banking records) | Structured data (immutable log) |
| Training data provenance records | Demonstrates data governance and quality | EU AI Act Art.10, ISO 42001 Annex A | Duration of model use | Structured data and narrative |
| Consumer complaint and appeal records | Demonstrates human oversight and redress | FCA Consumer Duty, GDPR Art.22 | Per FCA complaints retention (minimum 3 years) | Structured data |
| Conformity assessment documentation | Demonstrates EU AI Act compliance | EU AI Act Art.43 | 10 years after AI system placed on market | Narrative report with evidence pack |
| Board/governance approval records | Demonstrates senior management oversight | PRA SS1/23, ISO 42001 Cl.5 | Duration of model use + 5 years | Minutes, approval records |

---

## 8. BFSI Considerations

**Applicability:** Core BFSI use case. Credit scoring is the canonical example of high-risk AI in financial services.

### PRA SS1/23 — Model Risk Management

This credit scoring model is a Tier 1 material model under PRA SS1/23. The full model risk management framework applies:
- Model must be inventoried and classified in the firm's model inventory
- Independent model validation must be conducted before deployment and at regular intervals
- Model performance monitoring must include accuracy, stability, and fairness metrics
- Model risk governance must include clear accountability at senior management level (Senior Managers and Certification Regime — SMCR)

### FCA Consumer Duty

The model directly affects consumer outcomes in lending. Under FCA Consumer Duty (PS22/9):
- The firm must demonstrate that the model produces fair outcomes for retail customers
- Price and value assessment must consider whether AI-driven credit decisions create systematic disadvantage for vulnerable customers
- Consumer understanding — borrowers must understand how credit decisions are made and how to contest them

### RBI Model Risk Management

RBI examiners are increasing focus on AI/ML models in credit decisions:
- The bank must be able to explain the model's methodology, features, and validation results to RBI examiners
- Fair lending obligations require that AI credit scoring does not discriminate based on caste, religion, gender, or other protected characteristics under Indian law
- Data localisation is a hard requirement — credit decision processing for Indian applicants must occur on India-hosted infrastructure

### Supervisory Examination Expectations

A bank examiner (PRA, FCA, or RBI) reviewing this credit scoring system would expect to see:
- Complete model documentation including design, assumptions, and limitations
- Evidence of independent validation with bias testing results
- Production monitoring dashboards showing model performance and fairness metrics
- Governance records showing senior management approval and periodic review
- Complaint and appeal records demonstrating effective human oversight
- Data governance documentation for training data including demographic representation analysis

### Customer Harm Pathways
- **Discriminatory lending:** If the model produces differential approval rates or pricing by protected characteristic, this creates both regulatory and reputational risk
- **Opaque decisioning:** If applicants cannot understand why they were denied credit, this creates Consumer Duty and fair lending compliance risk
- **Model degradation:** If the model's accuracy degrades in production without detection, this creates credit risk and customer harm risk

---

## 9. Executive Summary

This assessment maps a credit scoring model deployed by an Indian bank (subsidiary of a UK banking group) to applicable regulations across the EU, UK, and India. The model processes personal data of applicants in all three jurisdictions and makes or supports lending decisions for retail unsecured credit products.

The most significant regulatory exposure is the EU AI Act, under which credit scoring is explicitly classified as high-risk AI (Annex III, Category 5b). Full conformity assessment, technical documentation, and ongoing monitoring obligations apply from August 2026. In the UK, the model is a Tier 1 material model under PRA SS1/23, requiring independent validation, performance monitoring, and senior management governance. In India, the DPDP Act and RBI model risk management expectations create parallel obligations around data protection, fair lending, and model documentation.

The model requires bias testing across protected characteristics in all three jurisdictions — this is both a legal requirement (EU AI Act, Equality Act, RBI Fair Practices) and a governance framework expectation (ISO 42001 Annex A, NIST MEASURE). Human oversight mechanisms must enable meaningful review and appeal of automated credit decisions.

The highest-priority compliance actions are: conduct a comprehensive bias evaluation across all protected characteristics before deployment; establish independent model validation per PRA SS1/23 and RBI expectations; produce EU AI Act Annex IV technical documentation; and implement production monitoring for accuracy, stability, and fairness drift. Data localisation compliance for India-hosted processing must be verified.

---

---

# Example 2: Internal Employee GenAI Knowledge Assistant

**Date of Assessment:** 2025-05-10  
**Subject Type:** AI Use Case  
**Jurisdictions Assessed:** EU, UK, India  
**Industry:** Insurance (BFSI)  
**Evidence Quality:** Medium (product description and deployment plan provided; technical architecture not yet finalised)  
**Assessment Status:** Final

**Subject Description:** A multinational insurance group headquartered in the UK, with operations in the EU (Germany, France) and India (GCC in Bengaluru), plans to deploy an LLM-based knowledge assistant for internal employees. The assistant uses a retrieval-augmented generation (RAG) architecture to answer employee questions about internal policies, HR procedures, compliance guidelines, and product documentation. The system uses a third-party LLM (GPT-4o via Azure OpenAI Service) and retrieves from an internal document corpus stored in SharePoint. The assistant is accessible to all employees across all geographies via the corporate intranet. It does not make decisions about individuals — it provides information retrieval and summarisation. No customer data is processed. Employee queries and the assistant's responses are logged.

---

## 1. Applicable Regulations

### EU Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| EU AI Act | **Applicable — Limited risk** | The system is an AI system that directly interacts with natural persons (employees). Article 50 transparency obligations apply. The system is not high-risk (Annex III) as it does not make decisions about employees regarding employment access, task allocation, or performance monitoring. |
| GDPR | **Applicable** | The system processes personal data of EU-based employees: employee queries (which may contain personal information), query logs linked to employee identities, and retrieved documents that may contain personal data. Article 6 lawful basis is required. |

### UK Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| UK GDPR / Data Protection Act 2018 | **Applicable** | The system processes personal data of UK-based employees (queries, logs). Same trigger as GDPR. |
| Equality Act 2010 | **Conditional** | If the assistant's responses influence employment-related decisions (e.g., providing policy guidance that leads to differential treatment), indirect discrimination risk may arise. Current design — information retrieval only — makes this unlikely but should be monitored. |
| FCA/PRA AI Guidance | **Conditional** | If the assistant is used by employees to retrieve compliance or regulatory guidance that informs regulated activities, FCA/PRA expectations on AI use in regulated activities may apply. Current design is general knowledge retrieval, not directly supporting regulated decisions. |
| PRA SS1/23 | **Not applicable** | The assistant is not a model used in regulated activities. It provides information retrieval, not risk modelling or decision support. |

### India Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| DPDP Act 2023 | **Applicable** | The system processes personal data of Indian GCC employees. Employee queries and logs constitute personal data of Data Principals. The insurer is a Data Fiduciary. |
| RBI | **Not applicable** | The insurer is not an RBI-regulated entity. |
| SEBI | **Not applicable** | The insurer is not a SEBI-registered entity. |
| IRDAI Guidance | **Conditional** | The assistant does not make underwriting or claims decisions. However, if it is used by underwriting or claims staff to retrieve policy guidance, IRDAI expectations on AI in insurance may apply indirectly. Current design makes direct applicability unlikely. |
| MEITY AI Advisories | **Applicable** | The system uses generative AI. MEITY expectation that AI-generated content be labelled as such applies. The system should clearly indicate that responses are AI-generated. |

---

## 2. Applicable Governance Frameworks

### ISO 42001

**Applicable clauses:**
- **Clause 6 (Planning):** An AI risk assessment should be conducted, though impact is low given the system does not make decisions about individuals. The assessment should focus on data handling risks (employee queries containing sensitive information, retrieved documents containing personal data).
- **Clause 7 (Support):** Employee awareness — users must understand that the assistant is AI-powered, that their queries are logged, and that responses should be verified against source documents.
- **Clause 8 (Operation):** Supply chain controls for the third-party LLM provider (Azure OpenAI). Data governance controls for the document corpus. Lifecycle management for the RAG retrieval pipeline.

**Applicable Annex A controls:**
- Transparency and disclosure controls (AI-generated content labelling)
- Data governance controls (employee query data, document corpus)
- Supply chain controls (Azure OpenAI third-party assessment)
- Human oversight controls (employees must verify AI responses against source documents)

### NIST AI RMF

- **GOVERN:** AI governance for the deployment — who owns the system, how is it updated, who reviews performance.
- **MAP:** Risk context — primary risks are data handling (sensitive information in queries), accuracy (hallucination leading to incorrect policy guidance), and supply chain (third-party LLM provider).
- **MEASURE:** Accuracy evaluation of RAG responses against source documents. Hallucination rate monitoring. User satisfaction tracking.
- **MANAGE:** Content filtering for sensitive information in queries. Response quality monitoring. Incident response for inaccurate guidance.

### OWASP LLM Top 10

**Applicable.** The system uses GPT-4o (an LLM) in a RAG architecture. Applicable risk categories:

- **LLM01 — Prompt Injection:** Risk of indirect injection via documents in the SharePoint corpus. If a document contains injected instructions, the assistant may follow them. Mitigated by corpus curation but not eliminated.
- **LLM02 — Insecure Output Handling:** Risk of the assistant generating responses containing sensitive information from retrieved documents that the querying employee should not have access to.
- **LLM05 — Supply Chain Vulnerabilities:** Third-party LLM (Azure OpenAI) introduces supply chain risk. Data processing terms, model updates, and availability are controlled by Microsoft.
- **LLM06 — Sensitive Information Disclosure:** Employee queries may contain sensitive personal or business information. Query logs create a sensitive data repository. Retrieved documents may contain information beyond the querying employee's access level.
- **LLM09 — Overreliance:** Employees may treat AI-generated policy guidance as authoritative without verifying against source documents, leading to incorrect actions.

---

## 3. Regulatory Obligations

### EU AI Act Obligations (Limited Risk)

| Obligation | Legal Basis | Type | Timeline | Non-Compliance Consequence |
|---|---|---|---|---|
| Inform employees that they are interacting with an AI system | Article 50(1) | Disclosure | By 2 August 2025 (transparency obligations) | Up to €15M or 3% global turnover |
| Label AI-generated content as such where technically feasible | Article 50(2) | Disclosure | By 2 August 2025 | Up to €15M or 3% global turnover |

### GDPR Obligations

| Obligation | Legal Basis | Type | Timeline |
|---|---|---|---|
| Establish lawful basis for processing employee queries and logs | Article 6 | Assessment | Before deployment |
| Provide privacy notice to employees regarding AI system data processing | Articles 13–14 | Disclosure | Before deployment |
| Conduct DPIA if query logging constitutes systematic monitoring of employees | Article 35(3)(c) | Assessment | Before deployment |
| Ensure data minimisation — do not retain query logs beyond necessary period | Article 5(1)(c) | Assessment | Ongoing |

### UK GDPR Obligations

Mirror GDPR obligations above. Additionally:

| Obligation | Legal Basis | Type | Timeline |
|---|---|---|---|
| Follow ICO Employment Practices Code regarding monitoring of employee AI interactions | ICO Guidance | Assessment | Before deployment |

### DPDP Act Obligations

| Obligation | Legal Basis | Type | Timeline |
|---|---|---|---|
| Obtain consent or establish lawful basis for processing employee queries | DPDP Act Section 4–6 | Assessment | Before deployment |
| Implement reasonable security safeguards for query logs | DPDP Act Section 8 | Assessment | Immediate |
| Accommodate Data Principal rights for employee data | DPDP Act Sections 11–14 | Assessment | Immediate |

### MEITY Obligations

| Obligation | Legal Basis | Type | Timeline |
|---|---|---|---|
| Label AI-generated responses as AI-generated | MEITY AI Advisory (March 2024) | Disclosure | Immediate |

---

## 4. Risk Classification

### EU AI Act Classification

**Classification: Limited risk (Article 50 transparency obligations)**

Rationale: The system is an AI system that directly interacts with natural persons (employees) and therefore triggers transparency obligations. It is not high-risk under Annex III because it does not fall within any of the eight listed domains — it does not make employment decisions (Annex III, Category 4), does not assess creditworthiness (Category 5), and does not evaluate access to services (Category 5). It is an internal knowledge retrieval tool, not a decision-making system.

**Classification caveat:** If the system evolves to provide guidance that directly influences employment decisions (e.g., HR policy interpretation affecting termination, promotion, or performance assessment), it may need reclassification as high-risk under Annex III, Category 4 (employment and worker management). The current design — information retrieval and summarisation — does not meet this threshold.

### UK Regulatory Classification

**FCA/PRA:** Not a regulated model. Conditional applicability only if used to support regulated decisions.

**ICO:** Moderate risk. Employee monitoring (query logging) requires DPIA assessment. Not high-risk data processing as the system does not make decisions about individuals.

### India Regulatory Classification

**DPDP Act:** Standard Data Fiduciary obligations. SDF designation unlikely for this specific system unless the insurer is designated SDF based on overall data processing volume (not specific to this system).

**IRDAI:** Not applicable. The system does not make insurance decisions.

---

## 5. Documentation Requirements

| Document | Regulatory Source | Content Requirements | Maintenance |
|---|---|---|---|
| Employee privacy notice for AI system | GDPR Art.13, UK GDPR, DPDP Act | What data is collected, how it is processed, retention period, employee rights | Before deployment; update upon changes |
| DPIA (if query logging constitutes systematic monitoring) | GDPR Art.35, ICO Guidance | Processing description, necessity assessment, risk to employees, mitigation measures | Before deployment; review annually |
| AI system transparency notice | EU AI Act Art.50, MEITY Advisory | Clear notice that the system is AI-powered; AI-generated content labelling | Before deployment |
| Third-party LLM assessment | ISO 42001 Cl.8.4 | Azure OpenAI data processing terms, security assessment, data residency, model update policy | Before deployment; review annually |
| AI risk assessment | ISO 42001 Cl.6, NIST MAP | Risk identification (data handling, accuracy, supply chain), impact assessment, mitigation plan | Before deployment; review annually |

---

## 6. Control Requirements

| Control | Source | Type | Classification | Guidance |
|---|---|---|---|---|
| AI system transparency labelling | EU AI Act Art.50, MEITY Advisory | Preventive | Mandatory | Clearly indicate to employees that they are interacting with an AI system. Label responses as AI-generated. |
| Employee privacy notice and consent | GDPR Art.13, DPDP Act | Preventive | Mandatory | Inform employees about query logging, data retention, and their rights before system use |
| Query content filtering | OWASP LLM06, GDPR Art.5 | Preventive | Recommended | Filter or warn employees when queries contain sensitive personal data, financial data, or customer information |
| Document access controls in RAG | OWASP LLM02, OWASP LLM06 | Preventive | Recommended | Ensure the RAG retrieval pipeline respects document-level access controls — employees should only retrieve from documents they are authorised to access |
| Response accuracy monitoring | NIST MEASURE, ISO 42001 Cl.9 | Detective | Recommended | Monitor response quality and hallucination rate. Implement user feedback mechanism for inaccurate responses |
| Third-party LLM vendor assessment | ISO 42001 Cl.8.4, NIST MAP | Preventive | Recommended | Assess Azure OpenAI data processing terms, security posture, and data residency. Ensure employee queries are not used for model training |
| Query log retention limits | GDPR Art.5(1)(e), DPDP Act | Preventive | Mandatory | Define and enforce retention period for employee query logs. Delete logs beyond the retention period |

---

## 7. Audit Evidence Required

| Evidence | Purpose | Source | Retention | Format |
|---|---|---|---|---|
| Employee privacy notice (published) | Demonstrates GDPR/DPDP compliance | GDPR Art.13, DPDP Act | Duration of system use | Document |
| DPIA (if conducted) | Demonstrates risk assessment for employee monitoring | GDPR Art.35 | Duration of processing + 3 years | Narrative report |
| AI transparency notice (in-product) | Demonstrates EU AI Act Art.50 compliance | EU AI Act Art.50 | Duration of system use | Screenshot / design specification |
| Third-party vendor assessment record | Demonstrates supply chain due diligence | ISO 42001 Cl.8.4 | Duration of vendor relationship | Narrative report |
| Query log retention policy and audit | Demonstrates data minimisation compliance | GDPR Art.5, DPDP Act | Duration of system use | Policy document + audit records |
| Response accuracy monitoring reports | Demonstrates ongoing quality management | ISO 42001 Cl.9, NIST MEASURE | Duration of system use | Structured data |

---

## 8. BFSI Considerations

**Applicability:** Conditional. The insurance group is BFSI, but the AI system is an internal knowledge tool, not a regulated insurance activity.

### IRDAI
The assistant does not make underwriting or claims decisions. IRDAI AI guidance does not directly apply. However, if claims or underwriting staff use the assistant to retrieve policy documents that inform their decisions, the assistant becomes part of the decision chain. The insurer should:
- Monitor which employee groups use the assistant most frequently
- Assess whether any regulated activity outcomes are influenced by assistant responses
- If so, reclassify the system's BFSI relevance

### FCA/PRA
Same conditional applicability. If compliance staff use the assistant to retrieve regulatory guidance that informs supervisory responses, the accuracy of AI-generated guidance becomes a regulatory risk. The insurer should:
- Add disclaimers that AI responses must be verified against source documents
- Implement a feedback mechanism for compliance staff to flag inaccurate responses

### Supervisory Examination Risk
Low for the current use case. A regulator examining this system would focus on:
- Employee data handling (query logging, privacy)
- Whether the system is being used beyond its intended scope (e.g., as a decision support tool for regulated activities)
- Third-party LLM vendor risk management

---

## 9. Executive Summary

This assessment maps an internal employee GenAI knowledge assistant, planned for deployment by a UK-headquartered multinational insurer across the EU, UK, and India. The system uses an LLM (GPT-4o via Azure OpenAI) with a retrieval-augmented generation architecture to help employees find and summarise internal policy documents.

The system is classified as limited-risk under the EU AI Act — it must clearly inform employees they are interacting with AI and label AI-generated content, but it does not trigger full high-risk conformity assessment obligations. Under GDPR and the DPDP Act, the system must have a lawful basis for processing employee queries and logs, and employees must be informed about how their data is used. A DPIA should be considered if query logging constitutes systematic monitoring of employees.

The primary technical risks are LLM-specific: prompt injection via document corpus, sensitive information disclosure through retrieved documents, and employee overreliance on AI-generated guidance. These are addressed by OWASP LLM Top 10 risk categories LLM01, LLM02, LLM06, and LLM09.

BFSI relevance is conditional — the system is not a regulated insurance activity, but if regulated staff use AI-generated policy guidance to inform underwriting, claims, or compliance decisions, the system's risk classification may need to be elevated.

The highest-priority actions are: implement AI transparency labelling before deployment to meet the August 2025 EU AI Act transparency deadline; publish an employee privacy notice; assess Azure OpenAI's data processing terms; and establish query log retention limits.

---

---

# Example 3: Algorithmic Trading Signal System

**Date of Assessment:** 2025-07-20  
**Subject Type:** AI System  
**Jurisdictions Assessed:** India, UK  
**Industry:** Securities / Trading (BFSI)  
**Evidence Quality:** High (detailed system architecture and trading strategy documentation provided)  
**Assessment Status:** Final

**Subject Description:** A SEBI-registered stockbroker with a UK subsidiary (FCA-authorised) operates an ML-based trading signal system. The system uses an ensemble of gradient boosting models and a transformer-based time series model to generate short-term trading signals (buy/sell/hold) for Indian equities (NSE/BSE) and UK equities (LSE). Signals are generated every 15 seconds during market hours. The system does not execute trades autonomously — signals are delivered to a trading desk where human traders make execution decisions. However, in practice, traders follow approximately 85% of signals without modification. The system processes market data (price, volume, order book depth), alternative data (satellite imagery of retail locations, shipping traffic), and news sentiment (NLP analysis of news feeds). No personal data of individuals is processed. The system is hosted on proprietary infrastructure in Mumbai (for Indian markets) and London (for UK markets).

---

## 1. Applicable Regulations

### India Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| SEBI Circular on Algorithmic Trading (2012, as amended) | **Applicable** | The system generates trading signals used for equities trading on NSE/BSE by a SEBI-registered stockbroker. Although the system does not auto-execute, the high follow-through rate (85%) and 15-second signal frequency mean it functionally operates as algorithmic trading infrastructure. |
| SEBI AI/ML Circular | **Applicable** | The system uses ML models for investment-related signal generation by a SEBI-registered entity. Audit trail, risk controls, and human oversight requirements apply. |
| DPDP Act 2023 | **Not applicable** | The system processes market data, alternative data, and news sentiment. No personal data of Indian Data Principals is processed. |
| RBI | **Not applicable** | The entity is a stockbroker, not a bank or NBFC. |

### UK Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| FCA Handbook (MAR, SYSC) | **Applicable** | The UK subsidiary is FCA-authorised. The trading signal system is used for UK equities trading. FCA Market Conduct rules (MAR) and Systems and Controls requirements (SYSC) apply. |
| MiFID II / UK MiFIR | **Applicable** | Algorithmic trading requirements under UK MiFID II (retained EU law) apply. The system generates trading signals at sub-minute frequency, meeting the definition of algorithmic trading under MiFID II Article 4(1)(39). |
| UK GDPR | **Not applicable** | No personal data of UK individuals is processed. Market data and alternative data sources do not contain personal data. |
| PRA SS1/23 | **Conditional** | If the UK subsidiary is PRA-regulated (dual-regulated), SS1/23 model risk management applies to the trading signal model. If the subsidiary is solo FCA-regulated, PRA SS1/23 does not apply directly but the model risk management principles are considered good practice by FCA. |

### EU Jurisdiction

| Regulation | Applicability | Trigger |
|---|---|---|
| EU AI Act | **Conditional** | The system does not operate in the EU market and does not affect EU individuals. If the UK subsidiary's trading activity involves EU-listed instruments or EU counterparties, AI Act obligations may apply extraterritorially. Based on current information (Indian and UK equities only), the EU AI Act does not apply. |
| GDPR | **Not applicable** | No personal data of EU individuals is processed. |

---

## 2. Applicable Governance Frameworks

### ISO 42001

**Applicable clauses:**
- **Clause 5 (Leadership):** Senior management oversight of the trading AI system is critical given its direct impact on trading decisions and potential market conduct implications. Clear accountability under SMCR (UK) and SEBI Fit and Proper requirements (India).
- **Clause 6 (Planning):** AI risk assessment must cover model risk (inaccurate signals leading to trading losses), market conduct risk (signals that could contribute to market manipulation or disorderly trading), and operational risk (system failure during market hours).
- **Clause 8 (Operation):** Full lifecycle management including model development, backtesting, validation, deployment, and ongoing monitoring. Supply chain controls for alternative data providers (satellite imagery, shipping data, news sentiment feeds).
- **Clause 9 (Performance Evaluation):** Continuous monitoring of signal accuracy, model stability, and risk-adjusted performance. Internal audit of the trading AI governance framework.
- **Clause 10 (Improvement):** Post-incident review for trading losses attributable to signal errors. Corrective action and model retraining processes.

**Applicable Annex A controls:**
- AI risk assessment and impact assessment
- Model lifecycle controls (development, testing, deployment, retirement)
- Data governance (market data quality, alternative data provenance)
- Monitoring and drift detection
- Incident management (trading errors, model failures)
- Human oversight (trader override capability)

### NIST AI RMF

- **GOVERN (Primary):** Governance structure for trading AI — model ownership, validation authority, deployment approval, risk limits. Trading AI governance must integrate with the firm's broader market risk and operational risk frameworks.
- **MAP:** Risk context includes model risk (signal accuracy), market conduct risk (potential for market disruption), operational risk (system availability), and data risk (alternative data quality and reliability).
- **MEASURE:** Backtesting validation, out-of-sample testing, signal accuracy tracking, risk-adjusted performance measurement, model stability monitoring, and stress testing under extreme market conditions.
- **MANAGE:** Kill switches for signal generation, trading limits tied to model confidence, escalation procedures for anomalous signal patterns, and incident response for model-attributed trading losses.

### OWASP LLM Top 10

**Partially applicable.** The primary models (gradient boosting ensemble) are not LLM-based. However, the news sentiment component uses NLP analysis which may involve an LLM or transformer model.

If the news sentiment component uses an LLM:
- **LLM03 — Training Data Poisoning:** Risk of adversarial news content designed to manipulate sentiment analysis and therefore trading signals.
- **LLM05 — Supply Chain Vulnerabilities:** Third-party news data feed introduces supply chain risk.
- **LLM09 — Overreliance:** Traders following 85% of signals without modification indicates significant overreliance on model outputs.

If the news sentiment component does not use an LLM (e.g., uses a fine-tuned BERT classifier), OWASP LLM Top 10 is not directly applicable but the principles of adversarial robustness and supply chain risk remain relevant.

---

## 3. Regulatory Obligations

### SEBI Obligations

| Obligation | Legal Basis | Type | Timeline | Non-Compliance Consequence |
|---|---|---|---|---|
| Register algorithmic trading systems with the exchange | SEBI Algo Trading Circular 2012 | Registration | Before deployment | SEBI enforcement action; exchange trading suspension |
| Maintain audit trail of all algo-generated signals and orders | SEBI Algo Trading Circular, SEBI AI/ML Circular | Documentation | Ongoing | SEBI enforcement action |
| Implement risk controls — order-level limits, price bands, quantity limits | SEBI Algo Trading Circular | Assessment | Before deployment | Exchange-imposed trading restrictions |
| Conduct annual system audit by a certified auditor | SEBI Algo Trading Circular | Assessment | Annual | SEBI enforcement action |
| Ensure human oversight and kill switch capability | SEBI AI/ML Circular | Assessment | Ongoing | SEBI enforcement action |
| Maintain records of model changes, retraining events, and performance | SEBI AI/ML Circular | Documentation | Ongoing | SEBI enforcement action |

### UK MiFID II / FCA Obligations

| Obligation | Legal Basis | Type | Timeline | Non-Compliance Consequence |
|---|---|---|---|---|
| Notify FCA of algorithmic trading activity | MiFID II Art.17; FCA SUP 15 | Notification | Before deployment | FCA enforcement action |
| Implement effective risk controls and systems | MiFID II Art.17(1); FCA SYSC 6A | Assessment | Before deployment | FCA enforcement action; up to unlimited fine |
| Maintain records of algorithmic trading systems — description, nature, parameters | MiFID II RTS 6, Art.1 | Documentation | Ongoing (minimum 5 years) | FCA enforcement action |
| Ensure business continuity arrangements for algorithmic trading systems | MiFID II Art.17(1); FCA SYSC 6A | Assessment | Before deployment | FCA enforcement action |
| Annual self-assessment and validation of algorithmic trading systems | MiFID II RTS 6 | Assessment | Annual | FCA enforcement action |
| Ensure the system does not contribute to disorderly trading conditions | MiFID II Art.17(1) | Monitoring | Ongoing | FCA enforcement action; market abuse investigation |
| SMCR — assign a Senior Manager with responsibility for algorithmic trading | FCA SYSC 4 | Registration | Before deployment | FCA enforcement action against individual |

---

## 4. Risk Classification

### SEBI Classification

**Classification: Algorithmic Trading System**

Rationale: The system generates trading signals at 15-second intervals for a SEBI-registered broker. Although the system does not auto-execute trades, the high signal frequency and high trader follow-through rate (85%) mean it functionally constitutes algorithmic trading infrastructure under SEBI's definition. SEBI's algorithmic trading circular applies in full.

### UK MiFID II Classification

**Classification: Algorithmic Trading (MiFID II Article 4(1)(39))**

Rationale: The system uses a computer algorithm to determine individual parameters of orders (timing, price, quantity recommendations) with limited or no human intervention in the signal generation process. This meets the MiFID II definition of algorithmic trading. Full MiFID II Article 17 obligations apply.

**High-Frequency Trading (HFT):** The 15-second signal frequency is unlikely to meet the HFT threshold (typically sub-second). HFT-specific obligations under MiFID II Article 17(2) are not triggered. However, if signal frequency increases, HFT classification should be reassessed.

### EU AI Act Classification

**Classification: Not applicable (current deployment)**

Rationale: The system operates on Indian (NSE/BSE) and UK (LSE) equities only. No EU market activity, no EU counterparties, no EU individuals affected. If the system expands to EU-listed instruments, EU AI Act classification would need to be assessed — algorithmic trading AI may be classified under Annex III Category 5 (access to essential services) depending on its impact on market participants.

---

## 5. Documentation Requirements

| Document | Regulatory Source | Content Requirements | Maintenance |
|---|---|---|---|
| Algorithmic trading system description | SEBI Algo Trading Circular, MiFID II RTS 6 | System architecture, model description, signal generation logic, data inputs, risk controls, kill switch design | Before deployment; update upon material changes |
| Model documentation | ISO 42001 Cl.8, NIST MAP/MEASURE | Model design, features, training methodology, backtesting results, validation results, assumptions, limitations | Before deployment; update upon retraining |
| Signal and order audit trail | SEBI Algo Trading Circular, MiFID II RTS 6 | Complete record of every signal generated (timestamp, instrument, direction, confidence), every order associated with a signal, and every trader override | Ongoing; retain minimum 5 years (UK), per SEBI requirements (India) |
| Risk control documentation | SEBI Algo Trading Circular, MiFID II Art.17 | Order limits, price bands, quantity limits, kill switch procedures, escalation procedures | Before deployment; review annually |
| Annual system audit report (India) | SEBI Algo Trading Circular | Independent auditor assessment of system controls, performance, and compliance | Annual |
| Annual self-assessment (UK) | MiFID II RTS 6 | Self-assessment of system governance, stress testing, risk controls, business continuity | Annual |
| SMCR responsibility allocation | FCA SYSC 4 | Documentation of Senior Manager responsible for algorithmic trading systems | Before deployment |
| Alternative data provider assessment | ISO 42001 Cl.8.4 | Assessment of satellite imagery, shipping data, and news sentiment providers — data quality, reliability, contractual terms | Before deployment; review annually |

---

## 6. Control Requirements

| Control | Source | Type | Classification | Guidance |
|---|---|---|---|---|
| Kill switch for signal generation | SEBI AI/ML Circular, MiFID II Art.17 | Corrective | Mandatory | Real-time capability to halt signal generation across all instruments. Must be accessible to risk function and trading desk. Tested regularly. |
| Order-level risk limits | SEBI Algo Trading Circular, MiFID II Art.17 | Preventive | Mandatory | Per-order maximum size, price deviation limits, and daily position limits. Automatically enforced. |
| Pre-trade risk controls | MiFID II RTS 6 | Preventive | Mandatory | Automated checks on signal-derived orders before exchange submission — price limits, size limits, market impact assessment |
| Human oversight with override capability | SEBI AI/ML Circular, ISO 42001 Annex A | Preventive | Mandatory | Traders must retain ability to override or ignore signals. Override decisions must be logged. |
| Model validation (backtesting and out-of-sample) | ISO 42001 Cl.8, NIST MEASURE | Detective | Recommended | Independent validation of signal accuracy, risk-adjusted performance, and stability across market regimes. Stress testing under extreme conditions. |
| Signal accuracy monitoring in production | ISO 42001 Cl.9, NIST MEASURE | Detective | Recommended | Real-time monitoring of signal accuracy (hit rate), P&L attribution to signals, and model stability metrics. Alert on degradation. |
| Market conduct monitoring | FCA MAR, SEBI | Detective | Mandatory | Monitor whether signal patterns could contribute to market manipulation, spoofing, or disorderly trading. Alert compliance function on anomalous patterns. |
| Alternative data quality monitoring | ISO 42001 Annex A, NIST MAP | Detective | Recommended | Monitor alternative data feeds for quality degradation, latency, or manipulation. Assess impact of data quality issues on signal accuracy. |
| Business continuity for trading systems | MiFID II Art.17, SEBI | Preventive | Mandatory | Redundancy, failover, and recovery procedures for the trading signal system. Regular testing of business continuity arrangements. |

---

## 7. Audit Evidence Required

| Evidence | Purpose | Source | Retention | Format |
|---|---|---|---|---|
| Complete signal audit trail | Demonstrates traceability of every signal to market data inputs and model outputs | SEBI Algo Trading, MiFID II RTS 6 | Minimum 5 years (UK); per SEBI requirements (India) | Structured data (timestamp, instrument, signal, confidence, inputs) |
| Trader override log | Demonstrates human oversight is exercised | SEBI AI/ML Circular, ISO 42001 | Minimum 5 years | Structured data |
| Annual system audit report | Demonstrates independent audit of trading system | SEBI Algo Trading Circular | Per SEBI requirements | Narrative report by certified auditor |
| Annual self-assessment report | Demonstrates governance review of algorithmic trading | MiFID II RTS 6 | Minimum 5 years | Narrative report |
| Model validation report | Demonstrates model accuracy and fitness for purpose | ISO 42001 Cl.8, NIST MEASURE | Duration of model use + 5 years | Narrative report with quantitative results |
| Risk control testing records | Demonstrates risk controls are operating effectively | MiFID II Art.17, SEBI | Minimum 5 years | Test records, results |
| Kill switch test records | Demonstrates kill switch is functional | SEBI, MiFID II | Minimum 5 years | Test records with timestamps |
| SMCR responsibility map | Demonstrates Senior Manager accountability | FCA SYSC 4 | Duration of role + 5 years | Document |

---

## 8. BFSI Considerations

**Applicability:** Core BFSI use case. Algorithmic trading AI is one of the most heavily regulated AI applications in financial services.

### SEBI — Algorithmic Trading Governance

SEBI's algorithmic trading framework is the primary regulatory regime for this system in India:
- The system must be registered with the exchange (NSE/BSE) as an algorithmic trading system
- An annual system audit by a certified auditor is mandatory
- Risk controls (order limits, price bands, kill switch) are exchange-mandated
- SEBI's evolving AI/ML guidance adds expectations around model documentation, audit trails, and human oversight

### FCA / MiFID II — Algorithmic Trading

UK MiFID II algorithmic trading requirements are comprehensive:
- Notification to FCA before deployment
- Full risk control framework (pre-trade, post-trade, kill switch)
- Annual self-assessment of system governance and controls
- SMCR accountability — a named Senior Manager must be responsible
- Market conduct monitoring — the system must not contribute to disorderly trading

### Model Risk Management

Although PRA SS1/23 may not directly apply (depending on the subsidiary's regulatory status), the trading signal model is a material model by any definition:
- Signal accuracy directly affects trading P&L
- Model failure could cause significant financial loss
- Model behaviour could create market conduct risk
- Independent model validation, ongoing performance monitoring, and governance are essential

### Systemic Risk Considerations

The system processes market data across Indian and UK markets simultaneously. Potential systemic risk factors:
- **Correlated trading:** If multiple firms use similar ML models with similar training data, correlated signal generation could amplify market volatility
- **Flash crash risk:** Rapid signal generation (15-second intervals) combined with high follow-through (85%) creates the potential for the system to contribute to rapid market movements
- **Cross-market contagion:** A signal error on Indian equities could, through portfolio effects, influence UK trading decisions

### Supervisory Examination Expectations

A SEBI or FCA examiner reviewing this system would focus on:
- Complete signal audit trail with trader decision logs
- Kill switch testing records and response time metrics
- Model validation reports including stress testing under extreme market conditions
- Risk control effectiveness (are order limits and price bands actually preventing problematic trades?)
- Senior Manager accountability (who is responsible if the model causes trading losses or market disruption?)
- Alternative data governance (are satellite imagery and news sentiment providers assessed for reliability and manipulation risk?)
- The 85% follow-through rate — a regulator may question whether "human oversight" is meaningful if traders rarely deviate from signals

---

## 9. Executive Summary

This assessment maps an ML-based trading signal system operated by a SEBI-registered Indian stockbroker with an FCA-authorised UK subsidiary. The system generates buy/sell/hold signals every 15 seconds for Indian and UK equities using an ensemble of gradient boosting models and transformer-based time series analysis, with alternative data inputs including satellite imagery and news sentiment.

The most significant regulatory exposures are SEBI's algorithmic trading framework and UK MiFID II. Both regimes require comprehensive risk controls (order limits, price bands, kill switches), complete audit trails, annual system reviews, and effective human oversight. In the UK, a named Senior Manager must be accountable under SMCR. In India, an annual system audit by a certified auditor is mandatory.

The system's 85 percent trader follow-through rate raises a critical governance question: while human oversight formally exists, the practical reality is that the model drives the majority of trading decisions. Both SEBI and FCA examiners are likely to scrutinise whether oversight is genuine or nominal.

The EU AI Act does not currently apply, as the system trades only Indian and UK equities. If trading expands to EU-listed instruments, EU AI Act classification will need to be assessed.

Framework alignment requires particular attention to ISO 42001 Clause 8 (lifecycle management) and Clause 9 (performance monitoring), and to NIST AI RMF MEASURE function (backtesting, validation, production monitoring). OWASP LLM Top 10 is partially applicable if the news sentiment component uses an LLM.

The highest-priority actions are: register the system with Indian exchanges; notify the FCA; implement and test kill switch procedures; establish a comprehensive signal audit trail; and address the gap between formal and effective human oversight.
