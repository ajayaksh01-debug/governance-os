---
fixture_id: india-dpdp-customer-support-ai
skill: regulatory-mapping
trigger_type: new_use_case_registration
subject_type: AI Use Case
jurisdictions: ["India"]
industry: Fintech (NBFC)
bfsi: true
ai_technology: LLM
subject_name: LLM Customer Support Chatbot
expected_risk_tier_eu: "N/A (no EU nexus)"
expected_risk_tier_india: "Standard Data Fiduciary (SDF designation conditional)"
expected_dpia_required: false
expected_regulations: ["DPDP Act 2023", "RBI IT Governance", "RBI Customer Service Guidelines"]
expected_frameworks: ["ISO 42001", "NIST AI RMF", "OWASP LLM Top 10"]
expected_owasp_applicable: true
expected_bfsi_applicable: true
expected_score_range: [72, 85]
expected_control_count_min: 6
claim_context: New Use Case Registration
---

# Test Fixture: India DPDP — LLM Customer Support Chatbot (NBFC)

## Context

**Organisation:** FinServ India Pvt. Ltd. — mid-tier non-banking financial company (NBFC) registered with the Reserve Bank of India. Primary operations in India, focused on digital personal loan origination and servicing (~2 million active borrowers). No operations outside India.  
**Subject type:** AI Use Case (pre-deployment)  
**Use case:** LLM-based conversational AI chatbot deployed on the company's mobile application and web portal to handle customer support queries for loan products. The chatbot answers questions about loan status, EMI schedules, part-prepayment options, interest rate queries, and grievance escalation. It authenticates customers via OTP, accesses their loan account details, and generates personalised responses.  
**Trigger:** New use case registration — the chatbot has been built by a third-party vendor and is pending compliance sign-off before production launch in Q4 2026.

---

## System Description

**Technology:** Large Language Model (LLM), RAG-based. Base model: OpenAI GPT-4o via Azure OpenAI Service API. Retrieval-Augmented Generation against the company's product documentation and customer FAQs. Customer-specific context (loan account data) is injected into the system prompt at session initialisation.  
**Inputs:** Customer queries (natural language), customer account data (loan ID, EMI schedule, outstanding balance, repayment history) retrieved from core banking system via API.  
**Outputs:** Natural language responses. The chatbot does not make credit decisions, modify account data, or initiate transactions. It can escalate to a human agent and log grievances.  
**Data subjects:** Indian individuals (Data Principals under DPDP Act 2023) — existing borrowers and prospective customers.  
**Personal data processed:**
- Loan account details (loan ID, outstanding balance, EMI schedule)
- Customer identity data (name, mobile number, PAN number from authentication)
- Repayment history
- Conversation content (stored for quality assurance purposes)

**Deployment model:** Cloud SaaS (Azure OpenAI Service); conversation logs stored in company-managed Azure India region.  
**Third-party AI vendor:** OpenAI / Microsoft Azure OpenAI Service — vendor is US-based; data processing outside India may be implicated depending on Azure region configuration.  
**Human escalation:** Available; chatbot can route to human agent during business hours.

---

## Jurisdictions

- **India:** Confirmed in scope. The organisation processes personal data of Indian Data Principals (DPDP Act 2023 applies). The NBFC is regulated by RBI. Operations are India-based.
- **EU:** Not in scope — no EU data subjects, no EU market presence.
- **UK:** Not in scope — no UK data subjects, no UK operations.

---

## Sector and BFSI Overlay

**Primary sector:** Fintech / NBFC (financial services)  
**Regulatory relationships:**
- RBI-registered NBFC (Master Direction – Non-Banking Financial Company – Systemically Important Non-Deposit taking Company, 2016)
- Subject to RBI IT Governance Master Direction (2023)
- Subject to RBI Guidelines on Customer Service in NBFC

BFSI overlay is **mandatory** for this fixture. The RBI IT Governance framework applies to all RBI-regulated entities. The customer support use case involves customer-facing AI within a regulated financial services context. While this is not a credit decisioning system, the chatbot accesses account data and provides information that customers may act on financially.

---

## Data Categories

| Category | Specific data elements | Sensitivity under DPDP Act |
|---|---|---|
| Identity data | Name, PAN number, Aadhaar-linked mobile (via OTP auth) | Personal data |
| Financial data | Loan account details, EMI schedule, outstanding balance, repayment history | Personal data (financial) |
| Contact data | Mobile number, email address | Personal data |
| Conversation data | Chat history stored for 90 days for quality review | Personal data |
| Behavioural data | Session timestamps, interaction patterns | Personal data |

Note: PAN number processing may constitute processing of government-issued identifier data. The DPDP Act 2023 does not separately categorise "sensitive personal data" in the same manner as older frameworks; however, financial data and government identifiers warrant elevated protection standards under the Act's data fiduciary obligations.

---

## Expected Regulatory Triggers

| Regulation | Jurisdiction | Expected finding | Key trigger |
|---|---|---|---|
| DPDP Act 2023 | India | Confirmed applicable | Processing of personal data of Indian Data Principals; consent required; data principal rights apply |
| RBI IT Governance Master Direction | India | Confirmed applicable | NBFC is RBI-regulated; customer-facing AI system within technology operations |
| RBI Customer Service Guidelines | India | Confirmed applicable | Customer-facing chatbot handling financial service queries; fair practice obligations |
| MEITY AI Advisories | India | Applicable (advisory) | MEITY has issued AI governance advisories relevant to LLM deployments by Indian entities |
| EU AI Act | EU | Not applicable | No EU nexus — organisation has no EU market presence and processes no EU data subjects |

---

## Expected Control Themes

The assessment must identify, at minimum, the following control requirement themes. An output missing more than two of these fails the minimum control coverage test for this fixture.

1. **Consent mechanism** (DPDP Act Section 6) — the organisation must obtain free, specific, informed, unconditional, and unambiguous consent from Data Principals before processing their personal data in the chatbot. Existing loan agreement consent may or may not cover AI chatbot processing — this must be assessed.
2. **Purpose limitation and data minimisation** (DPDP Act Section 4) — personal data must be collected for specified purposes only; account data injected into LLM context must be limited to what is necessary for the query.
3. **Data principal rights** (DPDP Act Sections 11–14) — right to information, correction, erasure, and grievance redressal must be operationalised.
4. **AI interaction disclosure** — customers must be informed they are interacting with an AI system, not a human agent (RBI Customer Service fair practice obligations; MEITY AI guidance).
5. **Prompt injection prevention** (OWASP LLM01) — malicious user inputs designed to override system instructions and exfiltrate other customers' account data represent a material security risk.
6. **Sensitive information disclosure prevention** (OWASP LLM06) — the LLM must not surface account data belonging to customers other than the authenticated session user.
7. **Human escalation path** (RBI Customer Service Guidelines) — automated system must provide clear escalation to human agents for grievances and complex queries.
8. **Conversation logging and audit trail** (RBI IT Governance, DPDP Act Section 8) — audit trails of AI interactions required for grievance redressal and regulatory examination.
9. **Third-party vendor management** (RBI IT Governance — vendor oversight obligations) — OpenAI/Azure is a critical technology vendor; RBI requires documented vendor risk assessment and contractual data handling obligations.
10. **Data localisation consideration** — if Azure processes conversation data outside India, this must be assessed under DPDP Act cross-border transfer provisions once notified (cross-border rules pending government notification as of 2026).

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **DPDP Act as the primary regulation — India-only scope:** This is a single-jurisdiction (India) assessment. The evaluator must correctly exclude EU AI Act and GDPR from the applicable regulations list and provide explicit rationale ("No EU nexus — organisation has no EU market presence and does not process data of EU data subjects"). An output that applies EU AI Act to this fixture has failed the jurisdiction scoping test.

2. **SDF (Significant Data Fiduciary) conditional status:** The DPDP Act 2023 designates certain Data Fiduciaries as Significant Data Fiduciaries (SDFs) based on volume and sensitivity of data processed, risk to data principals, and national security implications. With ~2 million active borrowers, FinServ India may meet SDF thresholds when notified by the central government. The evaluator must flag SDF status as **conditional** — applicable if the organisation meets government-notified thresholds — and document the additional SDF obligations (Data Protection Impact Assessment, Data Audits, Data Protection Officer appointment). Treating SDF status as definitively confirmed or definitively inapplicable both fail this fixture.

3. **OWASP LLM Top 10 applied correctly:** The system uses an LLM (GPT-4o). OWASP LLM Top 10 applies. The evaluator must identify, at minimum:
   - LLM01 (Prompt Injection): high risk — adversarial prompts could attempt to exfiltrate other customers' account data
   - LLM06 (Sensitive Information Disclosure): high risk — system prompt contains account data; exfiltration risk
   - LLM09 (Overreliance): medium risk — customers may make financial decisions based on chatbot responses

4. **RBI IT Governance applicability — vendor management scope:** OpenAI/Azure is a critical technology vendor under RBI IT Governance. The vendor risk assessment obligation must be identified. A common evaluator error is treating the API call to Azure OpenAI as a generic cloud service rather than as a critical AI technology vendor relationship requiring specific risk management.

5. **Consent scope question:** Existing loan agreement terms may include general data processing consent but are unlikely to specifically cover LLM-based processing of customer queries. The evaluator must flag this as a consent scope gap requiring legal review — not assume existing consent is sufficient.

6. **Section 8 BFSI — RBI, not PRA/FCA:** This is an India-only BFSI assessment. Section 8 must cover RBI IT Governance and RBI Customer Service Guidelines. References to PRA SS1/23 or FCA are incorrect for this fixture and indicate jurisdiction confusion.

7. **Risk classification — not high-risk under EU AI Act:** The EU AI Act is not applicable. The evaluator must not attempt to apply EU AI Act risk classification to this fixture. Any EU AI Act risk tier assigned is an error.

8. **Bias Scanner — N/A for this use case:** The Bias Scanner runtime filter is not relevant to a customer support chatbot. The evaluator should not recommend it. If mentioned, it must be clearly scoped to its actual capability (runtime output filter) and noted as not applicable to conversational AI quality assurance.

---

## Reviewer Red Flags

- EU AI Act or GDPR cited as applicable → jurisdiction scoping failure; no EU nexus exists
- SDF status confirmed definitively (either confirmed applicable or confirmed inapplicable) → must be conditional pending government notification
- OWASP LLM Top 10 marked N/A → system is LLM-based; OWASP LLM Top 10 is applicable
- LLM01 (Prompt Injection) not identified → highest-risk OWASP category for this use case; must be flagged
- OpenAI/Azure treated as generic cloud vendor without vendor risk management obligation → RBI IT Governance requires specific vendor oversight for critical technology vendors
- Section 8 references PRA SS1/23 or FCA obligations → incorrect jurisdiction; India-only assessment
- Existing loan consent assumed to cover LLM processing → consent scope gap requires legal review
- EU AI Act risk tier assigned → EU AI Act does not apply to this fixture
- No mention of AI interaction disclosure obligation → RBI Customer Service and MEITY guidance require disclosure to customers that they are interacting with AI
