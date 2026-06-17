# Data Protection Controls for AI Systems

## Purpose

AI systems create distinctive data protection challenges. They consume data at scale (training), generate outputs that may reflect or reveal that data (inference), and often operate as black boxes that make it difficult to understand what data influenced a given output.

This document defines data protection controls for AI systems across the data lifecycle — from collection and training through deployment and retirement.

---

## The AI Data Protection Problem

Traditional data protection controls were designed for systems where data flows are deterministic and traceable. AI systems challenge this model in several ways:

- **Training data incorporation:** Personal data used to train a model is not simply stored and retrieved — it is incorporated into the model's weights in a distributed, non-extractable form. Standard deletion mechanisms do not apply.
- **Inference-time disclosure:** A model trained on personal data may reproduce or reveal that data in its outputs, even when not asked. This is a data breach with no clear single point of failure.
- **Emergent correlations:** AI models identify correlations in data that humans would not anticipate. A model trained on non-sensitive data can learn to make inferences about sensitive attributes (health status, political views, sexual orientation) through proxy variables.
- **Third-party model dependencies:** When an organisation uses a third-party model (GPT-4, Claude, Gemini), it must assess what data the model provider retains and how it is used.

---

## Controls by Lifecycle Stage

### 1. Data Collection and Sourcing

**Lawful basis verification**
Before collecting or using data for AI purposes, verify and document the lawful basis for processing. For personal data:
- Consent must be freely given, specific, informed, and unambiguous — "consent to our terms" is insufficient for AI training
- Legitimate interests must be balanced against the rights and expectations of data subjects
- Statutory obligations must be verified jurisdiction-by-jurisdiction

**Purpose limitation**
Data collected for one purpose cannot be freely repurposed for AI training. Assess whether AI training is compatible with the original collection purpose, or whether a new lawful basis is required.

**Data minimisation**
Collect only the data necessary for the specific AI purpose. Common failures:
- Collecting granular personal attributes when aggregate or anonymised data would suffice
- Training on historical data that includes sensitive attributes not relevant to the model's purpose
- Using real personal data when synthetic data could serve the same function

**Data quality**
Inaccurate or incomplete training data creates inaccurate, biased, and potentially discriminatory models. Implement data quality checks before use in AI training:
- Completeness assessment
- Consistency checks
- Recency review — old data may not reflect current patterns and may encode historical discrimination
- Representativeness assessment — training data that underrepresents or misrepresents demographic groups creates biased models

---

### 2. Data Preparation and Anonymisation

**Anonymisation vs. Pseudonymisation**
These are not equivalent. Pseudonymised data (where a key could re-identify individuals) remains personal data under GDPR and equivalent laws. Truly anonymised data — where re-identification is not reasonably possible — falls outside data protection regulation.

For AI training data, anonymisation is preferable where technically feasible. However, the risk of re-identification from AI outputs (where the model regurgitates training data) means that anonymisation must be validated in the context of the trained model, not just the training dataset.

**Differential Privacy**
Differential privacy is a mathematical technique that adds calibrated noise to training data or model outputs, limiting how much the model can learn about any individual training example. It provides formal privacy guarantees and is increasingly a best-practice control for training on personal data at scale.

**Synthetic Data Generation**
Where the statistical properties of a dataset are needed for training but the specific data points are not, synthetic data generation can produce training data with equivalent statistical characteristics but no direct correspondence to real individuals.

**Data Masking**
For training data where anonymisation or synthetic data is not feasible, apply masking to sensitive fields: replace names with tokens, generalise dates to ranges, mask financial values to ranges, and suppress or generalise geographic data to appropriate levels.

---

### 3. Training Data Governance

**Training Data Registry**
Maintain a registry of all datasets used to train each model, including:
- Dataset name, source, and version
- Data classification (public, internal, confidential, personal data)
- Lawful basis for use (for personal data)
- Consent or licence status
- Processing applied (anonymisation, masking, filtering)
- Retention and deletion schedule

**Third-Party Data Assessment**
Third-party datasets — whether purchased, licensed, or scraped — carry data protection obligations that must be assessed before use:
- What consent was obtained from data subjects?
- Does the licence permit use for AI training?
- Does the dataset contain personal data of individuals from jurisdictions with data localisation requirements?
- Has the dataset been audited for sensitive categories of data?

**Data Lineage**
Maintain lineage records that trace which data influenced which model version. This is essential for:
- Responding to right-to-erasure requests (understanding whether an individual's data was used in training)
- Investigating bias claims (identifying which training data may have contributed to biased outputs)
- Regulatory audit (demonstrating lawful basis for training data processing)

---

### 4. Inference-Time Data Minimisation

**Prompt Data Minimisation**
Users and internal processes frequently submit more personal data than necessary to get a useful AI response. Implement controls to minimise personal data in prompts:
- User education on what to include and exclude from AI queries
- Automatic detection and masking of common PII patterns (names, national IDs, account numbers, health information) in prompts before submission to the model
- For internal AI tools, integrate with data classification systems to prevent submission of classified data

**Context Window Management**
In conversational AI systems, earlier messages remain in the context window and influence later responses. Implement context window management:
- Define maximum context window length appropriate to the use case
- Implement session expiry and context clearing
- Do not persist conversation context across sessions unless explicitly designed and controlled

**Inference Logging Controls**
Inference logs (the inputs and outputs of AI model calls) are often highly sensitive — they contain whatever personal data users submitted. Apply the same data protection controls to inference logs as to any other sensitive data:
- Restrict access to inference logs on a need-to-know basis
- Apply retention limits appropriate to the business purpose
- Assess whether logging personal data in inference logs requires a lawful basis

---

### 5. Data Subject Rights

AI systems create challenges for exercising data subject rights under GDPR and equivalent laws.

**Right of Access (Subject Access Requests)**
Individuals have the right to know what personal data an organisation holds about them. For AI systems, this includes:
- Personal data in training datasets
- Personal data in inference logs
- Profile data derived from AI analysis

Organisations must be able to respond to SARs covering AI-derived data, which requires knowing what data the system holds and in what form.

**Right to Erasure**
The right to erasure ("right to be forgotten") is technically difficult to fulfil for personal data incorporated into model weights. If an individual's data was used in training, deleting it from the training database does not remove its influence from the model.

Approaches:
- **Retraining:** Retrain the model excluding the individual's data — expensive and often impractical
- **Machine unlearning:** Emerging techniques that can selectively reduce a model's dependence on specific training examples — not yet mature enough for reliable compliance use
- **Prevention:** The most practical approach is to prevent personal data from entering training in the first place, through data minimisation and anonymisation

Document the technical limitations of erasure for AI training data in privacy notices, so data subjects have accurate expectations.

**Automated Decision-Making Rights**
Under GDPR Article 22 and equivalent provisions, individuals have rights related to decisions made solely by automated means that significantly affect them — including the right to request human review.

Any AI system making significant automated decisions (credit decisions, insurance pricing, access to services, employment decisions) must:
- Be identified as an automated decision-making system
- Provide meaningful information about the logic involved
- Enable human review upon request
- Implement a functional human review process (not a rubber-stamp)

---

### 6. Cross-Border and Data Localisation

AI systems frequently process data across borders — training in one jurisdiction, inference in another, model providers in a third. Data localisation requirements create constraints:

- **EU GDPR:** Personal data may only be transferred outside the EEA where adequate protections exist (adequacy decision, SCCs, BCRs)
- **India DPDP Act:** Restrictions on cross-border transfer; approved jurisdictions list not yet published
- **RBI requirements:** Payment system data must be stored in India; implications for AI systems modelling on payment data
- **China PIPL:** Data localisation requirements for certain categories and volumes of data

For AI governance programmes, map data flows for each AI system — where training data originates, where training occurs, where inference occurs, and where outputs are stored — and verify compliance with applicable localisation requirements.

---

## Framework Mapping

| Framework | Relevant Requirements |
|---|---|
| ISO 42001 | Annex A — Data governance; data quality; supply chain data |
| NIST AI RMF | GOVERN — Data policies; MAP — Data risks; MEASURE — Data quality |
| GDPR / UK GDPR | Articles 5, 9, 17, 22, 25, 35 |
| India DPDP Act | Sections on consent, data fiduciary obligations, cross-border transfers |
| EU AI Act | Article 10 — Data and data governance for high-risk AI |

---

## Recommended Controls by AI System Type

| System Type | Priority Controls |
|---|---|
| LLM trained on internal data | Training data registry; anonymisation; data lineage; erasure limitation disclosure |
| Third-party LLM API (e.g., GPT, Claude) | Vendor data handling assessment; prompt PII masking; inference log controls |
| AI decision system (credit, hiring, insurance) | Article 22 compliance; human review mechanism; bias monitoring |
| RAG system with personal data | Retrieval access controls; minimisation of retrieved content; session isolation |
| Agentic system with data access | Least privilege; inference logging; HITL for data modification actions |
