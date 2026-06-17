# Banking AI Governance — Use Cases and Risk Landscape

## Overview

Banks are among the most intensive users of AI globally. From credit scoring and fraud detection to customer service and regulatory compliance, AI is embedded throughout the banking value chain. This creates a concentrated governance challenge: high stakes, high volume, heavy regulation, and significant potential for both value creation and harm.

This document maps the primary AI use cases in banking against their governance requirements and risk profile.

---

## Use Case 1 — Credit Decisioning

### Business Context
AI models are used to assess creditworthiness for retail lending (mortgages, personal loans, credit cards), SME lending, and corporate credit. Models range from traditional scorecard approaches to complex ML models and increasingly to LLM-assisted underwriting narratives.

### Risk Profile

**Fairness and discrimination:** Credit AI must not produce decisions that discriminate on the basis of protected characteristics — race, gender, age, disability, religion, or (in many jurisdictions) postcode as a proxy. This is a legal requirement, not merely an ethical preference. Historical lending data reflects decades of discriminatory practice; models trained on this data will reproduce that discrimination unless explicitly addressed.

**Explainability:** Adverse credit decisions must be explainable to applicants. Regulatory requirements in the EU (GDPR Article 22), UK (Consumer Duty, FCA expectations), and US (Equal Credit Opportunity Act) require that individuals can understand why credit was denied and what they could do to improve their position. Black-box models that cannot support explanation create compliance exposure.

**Model risk:** Inaccurate credit models cause financial loss (through incorrect approvals or inappropriate rejections) and regulatory exposure. Model validation under SR 11-7 or PRA SS1/23 is mandatory for significant credit models.

### Governance Requirements
- Full model validation including fairness testing before production deployment
- Adverse action notices with model-derived reasons
- Periodic revalidation (at least annually for high-risk models)
- Human review process for marginal decisions and appeals
- Monitoring for demographic disparate impact in production

---

## Use Case 2 — Fraud Detection

### Business Context
AI-driven fraud detection is one of the highest-value AI applications in banking. Models identify fraudulent transactions in real time, detect account takeover, flag suspicious patterns in payments and transfers, and support AML transaction monitoring.

### Risk Profile

**False positives — customer harm:** Incorrectly flagging legitimate transactions as fraud blocks customer access to funds. For vulnerable customers, this can cause significant harm. Excessive false positive rates are increasingly a focus of FCA Consumer Duty reviews.

**False negatives — financial loss:** Missed fraud causes direct financial loss. Model performance must be balanced between false positive (customer harm) and false negative (financial loss) rates — this is an explicit governance decision, not merely a technical optimisation.

**Bias in fraud models:** Fraud detection models can exhibit demographic bias — flagging legitimate transactions from certain demographic groups at higher rates. This constitutes unlawful discrimination if protected characteristics are direct or proxy inputs.

**AML-specific risks:** AI used in AML transaction monitoring is subject to specific regulatory expectations from FCA, FinCEN, RBI, and others. Overly-sensitive models generate Suspicious Activity Reports (SARs) that overwhelm financial intelligence units; under-sensitive models miss genuine money laundering. Model calibration is a regulatory matter, not just a technical one.

### Governance Requirements
- Real-time and periodic performance monitoring (false positive/negative rates)
- Bias audit across customer demographic segments
- Customer complaint tracking for false positives
- Human review process for high-value or complex fraud decisions
- Regulatory reporting on model performance for AML systems

---

## Use Case 3 — Customer Service and Virtual Assistants

### Business Context
Banks deploy conversational AI — chatbots and virtual assistants — for customer enquiries, account management, complaint handling, and increasingly for financial guidance and product recommendations.

### Risk Profile

**Misinformation and hallucination:** AI customer service that provides incorrect information about products, interest rates, fees, or regulatory rights causes direct customer harm. In regulated activities (financial advice, mortgage information), misinformation creates regulatory liability.

**Mis-selling risk:** AI systems recommending products or services must meet suitability and appropriateness standards. An AI that recommends a product without assessing the customer's circumstances creates mis-selling risk equivalent to a human adviser doing the same.

**Prompt injection:** Customer-facing AI is exposed to the full public — including adversarial users attempting to manipulate the AI to provide incorrect information, bypass limits, or access other customers' data.

**Data disclosure:** Customer service AI often has access to account data. Poorly controlled systems can disclose one customer's data to another — a breach with significant regulatory consequences.

**Consumer vulnerability:** Financial services customers include vulnerable individuals (elderly, bereaved, financially stressed). AI systems that cannot recognise vulnerability indicators and escalate to human agents cause disproportionate harm to these groups.

### Governance Requirements
- Content accuracy controls and hallucination testing before deployment
- Suitability guardrails for any product recommendations
- Prompt injection testing and controls
- Session isolation controls
- Vulnerability escalation protocols
- Regulatory compliance review of all AI-generated customer communications
- Human escalation pathway clearly available at all times

---

## Use Case 4 — KYC and Customer Due Diligence

### Business Context
AI accelerates Know Your Customer (KYC) processes — document verification, identity checking, adverse media screening, PEP (Politically Exposed Person) screening, and sanctions screening.

### Risk Profile

**False negatives — regulatory breach:** Missing a sanctioned entity, PEP, or adverse media result creates significant regulatory exposure. Fines for sanctions screening failures have reached hundreds of millions of dollars.

**False positives — customer exclusion:** Over-sensitive KYC AI creates friction for legitimate customers, damages the customer experience, and can disproportionately affect customers from certain backgrounds (names that trigger adverse media, nationalities that correlate with PEP status).

**Bias in identity verification:** AI identity verification systems have documented lower accuracy for darker skin tones and non-Western document formats. Banks deploying these systems may inadvertently discriminate against customers on grounds of race or national origin.

**Data residency:** KYC data frequently includes highly sensitive personal data. Cross-border AI processing for KYC purposes must comply with data localisation requirements.

### Governance Requirements
- Performance testing across demographic subgroups for identity verification
- Sanctions screening false negative rate monitoring and thresholds
- Human review for all adversely screened customers before action
- Data residency compliance for cross-border KYC AI

---

## Use Case 5 — Regulatory Compliance and Reporting

### Business Context
Banks use AI to automate regulatory reporting, identify compliance gaps, monitor employee conduct, and manage regulatory change. This includes using LLMs to interpret regulation, summarise reporting requirements, and draft compliance documentation.

### Risk Profile

**Hallucination in regulatory interpretation:** An LLM that incorrectly interprets a regulatory requirement — and confidently states that interpretation — can cause a bank to mis-report or fail to meet a regulatory obligation. The confidence of LLM outputs makes hallucinated regulatory interpretations particularly dangerous.

**Over-reliance:** Compliance teams may over-rely on AI regulatory interpretation without independent verification, reducing the human expertise that should backstop AI-assisted compliance work.

### Governance Requirements
- All AI-generated regulatory interpretations must be verified by qualified human compliance professionals
- AI-assisted regulatory reporting must have human sign-off before submission
- Clear disclosure that AI assistance was used in specific regulatory deliverables

---

## Applicable Regulatory Frameworks for Banking AI

| Regulation | Key Requirements |
|---|---|
| SR 11-7 (US) | Model risk management for all significant models |
| PRA SS1/23 (UK) | Model risk management principles for banks and insurers |
| EU AI Act | Credit scoring as explicit high-risk AI (Annex III) |
| FCA Consumer Duty | Fair outcomes for customers; appropriate AI safeguards |
| GDPR / UK GDPR | Automated decision-making rights; data minimisation |
| RBI IT Governance | AI governance for Indian banks |
| DPDP Act (India) | Personal data protection for AI systems |
| Basel III Operational Risk | AI failures as operational risk events |

---

## Recommendations

1. Conduct an AI inventory audit covering all models in production — many banks have dozens or hundreds of models in credit, fraud, and operations that lack formal model risk management.
2. Prioritise credit scoring, fraud detection, and KYC AI for formal governance — these are the highest-risk use cases with the clearest regulatory obligations.
3. Implement adverse action explanation capability for all credit AI before deployment — this is a regulatory requirement in multiple jurisdictions and a common examination finding.
4. Test all customer-facing AI for demographic bias in outputs — mis-selling risk and discrimination risk are both live issues that regulators are examining.
5. Treat LLM-assisted compliance work as human-assisted, not AI-automated — human sign-off is non-negotiable for regulatory submissions.
