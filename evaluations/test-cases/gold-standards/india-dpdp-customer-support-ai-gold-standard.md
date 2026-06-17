---
fixture_id: india-dpdp-customer-support-ai
gold_standard_id: india-dpdp-customer-support-ai-gold-standard
skills_covered: ["regulatory-mapping"]
subject_name: LLM Customer Support Chatbot (NBFC)
jurisdictions: ["India"]
industry: Fintech (NBFC)
regulatory_mapping_score: 78
regulatory_mapping_band: Acceptable
claims_firewall_status: Pass
date: 2026-06-18
---

# Gold Standard Output: India DPDP — LLM Customer Support Chatbot

> **Usage:** Expected-output gold standard for the `india-dpdp-customer-support-ai` fixture. Demonstrates structurally and substantively correct regulatory-mapping output for an LLM-based customer support chatbot operated by an Indian NBFC. Validate against `evaluations/baselines/regulatory-mapping/structure.json`.

---

**Date of Assessment:** 2026-06-18  
**Subject Type:** AI Use Case (pre-deployment)  
**Jurisdictions Assessed:** India  
**Industry:** Fintech / NBFC (BFSI)  
**Evidence Quality:** Medium  
**Assessment Status:** Final  
**Traceability ID:** TR-RW-GOLD-002

score: 78/100

---

### 1. Applicable Regulations

| Regulation | Jurisdiction | Applicability Status | Trigger |
|---|---|---|---|
| Digital Personal Data Protection Act 2023 (DPDP Act) | India | Confirmed | Processing of personal data of Indian Data Principals (loan account holders); consent, purpose limitation, and data principal rights obligations apply |
| RBI IT Governance Master Direction 2023 | India | Confirmed | Organisation is RBI-regulated NBFC; customer-facing AI system within regulated technology operations; IT governance, vendor management, and operational resilience obligations apply |
| RBI Guidelines on Customer Service in NBFCs | India | Confirmed | Customer-facing chatbot handling financial service queries; fair practice, grievance redressal, and disclosure obligations for customer-facing AI |
| MEITY AI Advisories and Guidelines | India | Confirmed (advisory) | MEITY has issued AI governance advisories applicable to LLM-based systems operated by Indian entities; advisory status — not legally binding but represents regulatory expectation |
| EU AI Act | EU | Not applicable | No EU nexus — organisation has no EU market presence and processes no data of EU data subjects |
| GDPR | EU | Not applicable | No EU nexus — confirmed absence of EU data subjects or EU market targeting |

---

### 2. Applicable Governance Frameworks

**ISO 42001**

| ISO 42001 Element | Applicability | Rationale |
|---|---|---|
| Clause 4 (Context) | Confirmed | Operating context includes RBI regulatory environment, customer data sensitivity, and NBFC operational constraints |
| Clause 6 (Planning) | Confirmed | AI risk assessment for LLM deployment; vendor risk assessment for OpenAI/Azure dependency |
| Clause 7 (Support) | Confirmed | Resources, competence in LLM governance; awareness training for staff interacting with chatbot outputs |
| Clause 8 (Operation) | Confirmed | LLM supply chain controls; prompt engineering governance; customer data injection controls |
| Clause 9 (Performance) | Confirmed | Monitoring of chatbot quality, accuracy, and incident rates |
| Clause 10 (Improvement) | Confirmed | Incident response and continuous improvement for chatbot failures |
| Annex A.8 (Data for AI) | Confirmed | Customer data injected into LLM context requires data governance controls |
| Annex A.9 (Transparency) | Confirmed | AI interaction disclosure to customers; MEITY guidance on AI transparency |

**NIST AI RMF**

| Function | Applicability | Primary engagement |
|---|---|---|
| GOVERN | Confirmed | LLM deployment policy, vendor risk governance (OpenAI/Azure), accountability for customer-facing AI |
| MAP | Confirmed | Risk context: affected population (2M borrowers), harm pathways (unauthorised data disclosure, financial misadvice, prompt injection) |
| MEASURE | Confirmed | LLM quality testing, adversarial prompt testing, PII leakage testing, response accuracy evaluation |
| MANAGE | Confirmed | Prompt injection controls, human escalation path, incident response for chatbot failures |

**OWASP LLM Top 10**

Applicable — system uses GPT-4o LLM with customer account data in context.

| OWASP Category | Applicability | Risk assessment for this system |
|---|---|---|
| LLM01 — Prompt Injection | High | Adversarial user input could attempt to exfiltrate other customers' account data injected in system prompt; primary security risk |
| LLM06 — Sensitive Information Disclosure | High | System prompt contains loan account data; risk of LLM revealing data belonging to other customers if prompt injection succeeds |
| LLM08 — Excessive Agency | Medium | Chatbot must not initiate transactions or modify account data; scope boundaries must be enforced architecturally |
| LLM09 — Overreliance | Medium | Customers may act on chatbot responses regarding loan terms or EMI calculations without seeking confirmation; disclaimer controls required |
| LLM02 — Insecure Output Handling | Low | Responses rendered in mobile/web app; XSS risk in output handling must be assessed by mobile team |
| LLM05 — Supply Chain Vulnerabilities | Medium | OpenAI/Azure dependency; model updates may change behaviour unexpectedly; vendor change management required |
| LLM03, LLM04, LLM07, LLM10 | Low / N/A | LLM03 (Training data poisoning) N/A for hosted API; LLM04 (DoS) low priority for chatbot; LLM07 (Plugin design) N/A; LLM10 (Model theft) N/A for API consumer |

---

### 3. Regulatory Obligations

| Obligation Description | Legal Basis | Type | Timeline |
|---|---|---|---|
| Obtain free, specific, informed, unconditional, and unambiguous consent from Data Principals before processing their personal data in the chatbot context | DPDP Act 2023, Section 6 | Assessment / Documentation | Before deployment; review and update consent mechanism if existing loan consent is insufficient |
| Provide a clear notice to Data Principals at the point of consent describing the purpose of data processing, categories of data, and rights | DPDP Act 2023, Section 5 | Disclosure | Before deployment |
| Implement mechanisms for Data Principals to exercise right to correction, erasure, and grievance redressal | DPDP Act 2023, Sections 12–14 | Monitoring / Process | Before deployment; operational on day 1 |
| Disclose to customers that they are interacting with an AI system, not a human agent | RBI Customer Service Guidelines; MEITY AI Advisories | Disclosure | Before deployment; disclosure must appear at session initiation |
| Assess and document cross-border data transfer implications of Azure OpenAI processing | DPDP Act 2023, Section 16 (pending government notification) | Assessment / Documentation | Before deployment; monitor for cross-border transfer rule notification |
| Conduct vendor risk assessment and establish contractual data handling obligations with OpenAI/Microsoft Azure | RBI IT Governance Master Direction 2023 (vendor management provisions) | Assessment / Documentation | Before deployment; annual review |
| Maintain audit trail of chatbot interactions sufficient for grievance redressal and regulatory examination | RBI IT Governance Master Direction; RBI Customer Service Guidelines | Monitoring | Ongoing from deployment |
| Implement human escalation path for customer grievances and complex queries | RBI Customer Service Guidelines | Process | Before deployment |
| Assess whether organisation meets Significant Data Fiduciary (SDF) thresholds and prepare for additional SDF obligations if designated | DPDP Act 2023, Section 10 (SDF designation pending government notification) | Assessment | Conditional — when SDF thresholds are notified; monitor for notification |
| Implement technical and organisational measures to ensure security of personal data in chatbot context | DPDP Act 2023, Section 8(4) | Documentation / Monitoring | Before deployment; ongoing |

---

### 4. Risk Classification

**EU AI Act Classification:** Not applicable — no EU nexus.

**India Regulatory Classification:**

- **DPDP Act — Data Fiduciary classification:** FinServ India Pvt. Ltd. is a Data Fiduciary under DPDP Act 2023. With approximately 2 million active borrowers, the organisation may meet Significant Data Fiduciary (SDF) thresholds once notified by the central government. SDF classification is **conditional** — it depends on government-notified thresholds for data volume, sensitivity, risk to data principals, and national security implications. If designated SDF, additional obligations apply: mandatory Data Protection Impact Assessment (DPIA), periodic data audit, appointment of Data Protection Officer, and additional data localisation requirements.

- **RBI — IT Governance classification:** The chatbot is a customer-facing technology system within the NBFC's regulated operations. Under RBI IT Governance, it is classified as a customer-facing technology service. The organisation's board and senior management are responsible for IT risk management. The chatbot's dependency on a US-based AI vendor (OpenAI/Azure) creates a regulated outsourcing arrangement that must be managed per RBI outsourcing guidelines.

- **AI risk level (India domestic):** Medium. The chatbot does not make credit decisions and does not modify account data. Primary risks are data exposure (personal and financial data in LLM context), customer misinformation (overreliance on LLM responses), and operational disruption (vendor dependency). These are material but do not approach the risk level of automated credit decisioning systems.

**UK Regulatory Classification:** Not applicable — no UK nexus.

---

### 5. Documentation Requirements

| Document | Regulatory source | Content requirements | Maintenance |
|---|---|---|---|
| Consent record and consent mechanism documentation | DPDP Act 2023, Section 6 | How consent is obtained, what the consent covers, mechanism for withdrawal, timestamp and record of consent for each Data Principal | Before deployment; update on purpose change |
| Privacy Notice (Data Processing Notice) | DPDP Act 2023, Section 5 | Categories of data processed, purpose, rights of Data Principal, grievance redressal contact | Before deployment; update on material change |
| Vendor Risk Assessment — OpenAI/Microsoft Azure | RBI IT Governance Master Direction (vendor management) | Vendor risk classification, data handling assessment, contractual terms review, business continuity assessment, exit plan | Before deployment; annual review |
| Data Processing Agreement with Azure/OpenAI | DPDP Act 2023, Section 8; RBI IT Governance | Data handling obligations, security standards, breach notification obligations, data deletion on termination | Before deployment |
| Cross-Border Transfer Assessment | DPDP Act 2023, Section 16 | Assessment of data flows to Azure US regions, applicable cross-border transfer mechanisms (pending government notification of approved countries/frameworks) | Before deployment; update when cross-border rules are notified |
| Chatbot Security Assessment | DPDP Act 2023, Section 8(4); RBI IT Governance | Adversarial prompt testing results, PII leakage test results, access control documentation, security measures for LLM context | Before deployment; annual review |
| SDF Readiness Assessment | DPDP Act 2023, Section 10 | Assessment of whether organisation meets SDF thresholds; gap analysis against SDF obligations; DPO appointment documentation (if designated) | Conditional — when SDF thresholds are notified |
| Grievance Redressal Procedure | RBI Customer Service Guidelines | How customers can raise complaints about chatbot interactions; escalation to human agents; resolution timelines | Before deployment |

---

### 6. Control Requirements

| Control | Regulatory source | Type | Mandatory |
|---|---|---|---|
| Consent management mechanism — obtain, record, and enable withdrawal of Data Principal consent for chatbot data processing | DPDP Act 2023, Section 6 | Preventive / Process | Mandatory |
| AI interaction disclosure — display at chatbot session initiation that the user is interacting with an AI, not a human | RBI Customer Service Guidelines; MEITY AI Advisories | Preventive / Disclosure | Mandatory |
| Prompt injection prevention — server-side input validation and prompt engineering controls to prevent adversarial inputs from accessing other customers' account data | OWASP LLM01; DPDP Act Section 8(4) security obligations | Preventive | Mandatory |
| Sensitive information disclosure prevention — context management to prevent LLM from revealing account data beyond the authenticated session scope | OWASP LLM06; DPDP Act Section 8(4) | Preventive | Mandatory |
| Scope boundary enforcement — architectural controls preventing the chatbot from initiating transactions, modifying account data, or executing actions beyond query-response scope | OWASP LLM08; RBI Customer Service Guidelines | Preventive | Mandatory |
| Human escalation path — mandatory escalation to human agent for grievance keywords, complex queries beyond chatbot scope, and customer requests for human assistance | RBI Customer Service Guidelines | Process | Mandatory |
| Conversation audit log — retention of chat transcripts for grievance redressal and regulatory examination | RBI IT Governance; DPDP Act accountability | Detective | Mandatory |
| Vendor change management — process to evaluate and test the impact of upstream LLM model updates (OpenAI model version changes) before deployment | OWASP LLM05; RBI IT Governance (operational resilience) | Process | Recommended (mandatory for material model updates) |
| Customer disclaimer — at points where the chatbot provides financial information (EMI calculations, interest rate queries), include a disclaimer advising customers to verify with the company's loan documentation or human representative | MEITY AI Advisories; RBI Customer Service (consumer protection) | Preventive / Disclosure | Recommended |

Note on Ethana capabilities for this use case: Ethana's Immutable Audit Log (Production) is appropriate for conversation logging (CTRL above — audit log control). Ethana's PII Scanner (Production) can be deployed on chatbot input/output to detect PII leakage in real-time. Ethana's Runtime Guardrails (Production) can be configured to enforce scope boundary controls (prevent transaction initiation commands from being processed). No In Build or Aspirational capabilities are referenced as currently available.

---

### 7. Audit Evidence Required

| Evidence type | Purpose | Source | Retention |
|---|---|---|---|
| Consent records | Demonstrates DPDP Act Section 6 compliance for each Data Principal | Consent management system | Duration of data processing |
| Chat transcripts (anonymised) | Grievance redressal evidence; regulatory examination | Chatbot platform audit log | 90 days (operational); 2 years for grievance-related transcripts |
| Vendor risk assessment (signed) | Demonstrates RBI IT Governance vendor oversight compliance | Annual vendor review process | 3 years |
| PII leakage test results | Evidence of security assessment | Penetration test / chatbot security audit | Annual; retain latest 2 cycles |
| Adversarial prompt test results | Evidence of LLM01 (prompt injection) controls | Red-team security assessment | Annual; retain latest 2 cycles |
| Customer grievance resolution records | Demonstrates RBI Customer Service compliance | Grievance management system | 3 years |
| AI disclosure confirmation log | Evidence that AI interaction disclosure was presented at session initiation | Chatbot platform session log | 1 year |
| SDF readiness documentation | Demonstrates preparedness for conditional SDF obligations | Compliance team | Update when SDF notification issued |

---

### 8. BFSI Considerations

**India BFSI:**

**RBI IT Governance Master Direction 2023:** The chatbot is a customer-facing technology system operated by an RBI-regulated NBFC. Key RBI IT Governance obligations include:
- The Board and senior management are responsible for technology risk management and must be aware of material technology systems including customer-facing AI
- The chatbot's dependency on OpenAI/Microsoft Azure constitutes a regulated technology outsourcing arrangement requiring vendor due diligence, contractual safeguards, and business continuity planning
- Operational resilience requirements: what is the fallback if the Azure OpenAI API is unavailable? A human agent backup must be available

**RBI Customer Service Guidelines:** Customer-facing AI for financial services must:
- Not mislead customers about the nature of the interaction (AI must be disclosed)
- Provide accurate information about financial products (LLM responses about loan terms must be validated or disclaimed)
- Provide a clear escalation path to human agents for grievances and complex queries
- Not substitute for the formal complaint management process required under RBI guidelines

**Model risk considerations:** Unlike the credit scoring system in the EU AI Act fixture, this LLM chatbot does not constitute a "material model" under RBI MRM guidance (it does not make credit decisions or influence financial risk calculations). Standard IT governance vendor management obligations apply; formal model risk management (independent validation, model documentation per SS1/23 equivalent) is not required for this use case.

**Section 8 N/A items:** PRA SS1/23 (UK regulation), FCA Consumer Duty (UK regulation), SEBI regulations (not a SEBI-registered entity), and IRDAI guidelines (not an insurer) are not applicable to this use case.

---

### 9. Executive Summary

FinServ India Pvt. Ltd.'s LLM customer support chatbot is subject to India's Digital Personal Data Protection Act 2023 (DPDP Act) as the primary regulatory obligation, alongside RBI IT Governance requirements as an RBI-regulated NBFC. The system is not subject to EU AI Act, GDPR, or any UK regulation — the organisation's operational scope is India-only.

The most significant compliance risk is the adequacy of Data Principal consent for LLM-based processing of personal financial data. Existing loan agreement consent is unlikely to specifically cover AI chatbot processing, and this gap must be addressed before deployment. The organisation must also assess whether it will be designated a Significant Data Fiduciary (SDF) once the government notifies thresholds — if designated, a Data Protection Impact Assessment, data audit, and Data Protection Officer appointment become mandatory.

From a security perspective, the primary risk is prompt injection (OWASP LLM01): an adversarial user could attempt to manipulate the chatbot into disclosing another customer's account data injected into the system context. This is the highest-priority technical control to implement before deployment.

The dependency on OpenAI/Microsoft Azure as a US-based AI vendor creates an RBI IT Governance outsourcing arrangement that requires documented vendor risk assessment and contractual data handling obligations. Data localisation implications under the DPDP Act's cross-border transfer provisions must also be assessed — the rules are pending government notification but organisations should position for compliance now.

Highest-priority compliance actions: (1) Audit existing consent language and update if AI chatbot processing is not explicitly covered; (2) Deploy prompt injection and sensitive information disclosure controls; (3) Complete RBI vendor risk assessment for OpenAI/Azure; (4) Implement AI interaction disclosure at session initiation; (5) Monitor for SDF threshold notification.
