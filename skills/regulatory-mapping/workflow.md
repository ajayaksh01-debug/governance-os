# Regulatory Mapping — Workflow

## Overview

This workflow defines the step-by-step process for executing the Regulatory Mapping skill. It is designed to produce consistent, high-quality regulatory and framework alignment assessments regardless of the analyst, the input format, or the subject type.

The workflow has seven phases. Each phase has defined inputs, outputs, and quality gates. The full workflow typically takes 60–120 minutes for a multi-jurisdictional assessment. For a single-jurisdiction, single-regulation assessment with clear applicability, a condensed analysis may take 30–45 minutes.

---

## Phase 1 — Intake and Subject Classification

**Objective:** Understand what is being assessed before starting the regulatory analysis.

### Step 1.1 — Read and Classify the Subject Material

Read the full subject description without analysing regulatory implications. On first pass, identify:
- What type of AI subject this is (use case, system, incident, control, portfolio)
- What the AI technology is (LLM, ML model, agent, ensemble, rule-based with AI components)
- What data the subject processes and from whom
- Who is affected by the subject's outputs or decisions
- Where the subject operates or will operate

Resist the urge to begin regulatory classification during this step. Understanding the subject fully before assessing it produces more accurate mapping.

### Step 1.2 — Determine Jurisdictions

Identify all jurisdictions with a legitimate regulatory nexus to the subject:

```
Does the AI system's output affect EU individuals or is the system placed on the EU market?
├── Yes → EU jurisdiction in scope (EU AI Act, GDPR)
└── No → EU out of scope (document rationale)

Does the AI system process data of UK individuals or operate under UK-regulated entities?
├── Yes → UK jurisdiction in scope (UK GDPR, FCA/PRA, Equality Act)
└── No → UK out of scope (document rationale)

Does the AI system process data of Indian individuals, operate in India, or operate under Indian-regulated entities?
├── Yes → India jurisdiction in scope (DPDP Act, sectoral regulators)
└── No → India out of scope (document rationale)
```

If the input specifies jurisdictions, validate the selection. If jurisdictions are missing that should be in scope based on the subject description, flag this to the requesting party.

### Step 1.3 — Determine Industry Classification

Classify the organisation's industry for the purpose of sectoral regulation:

| Industry | Sectoral Regulators in Scope |
|---|---|
| Banking / Lending | FCA, PRA, PRA SS1/23 (UK); RBI IT Governance, RBI MRM (India); EBA, ECB (EU) |
| Insurance | FCA, PRA (UK); IRDAI (India); EIOPA (EU) |
| Securities / Trading | FCA, MiFID II (UK); SEBI (India); ESMA (EU) |
| Wealth Management | FCA (UK); SEBI, AMFI (India) |
| Healthcare | CQC, MHRA (UK); CDSCO (India); MDR (EU) |
| General Enterprise | Data protection authorities only |

### Step 1.4 — Assess Evidence Quality

Rate the quality of input information:

| Rating | Description | Effect on Analysis |
|---|---|---|
| High | Detailed system specification, data flow documentation, or formal incident report | Full analysis; high-confidence classifications |
| Medium | Product description, informal summary, or partial technical details | Full analysis; flag classification uncertainties |
| Low | Brief description, limited context, or early-stage concept | Condensed analysis; state assumptions explicitly |

### Phase 1 Output
- Subject type classification
- AI technology identification
- Jurisdictions in scope with rationale
- Industry classification
- Evidence quality rating
- List of data types, affected individuals, and deployment model

---

## Phase 2 — Regulation Scanning

**Objective:** Identify every applicable regulation across all in-scope jurisdictions.

### Step 2.1 — Apply EU Regulation Decision Tree

```
Does the subject involve an AI system as defined by the EU AI Act (Article 3)?
├── Yes → EU AI Act applies. Proceed to risk classification in Phase 4.
└── Possibly → Flag for classification review. Note the ambiguity.

Does the subject process personal data of EU individuals?
├── Yes → GDPR applies.
└── No → GDPR does not apply (document rationale).

Is the subject a GPAI model or does it use a GPAI model?
├── Yes → GPAI provider/deployer obligations may apply.
└── No → GPAI not applicable.
```

### Step 2.2 — Apply UK Regulation Decision Tree

```
Does the subject process personal data of UK individuals?
├── Yes → UK GDPR and Data Protection Act 2018 apply.
└── No → UK data protection not applicable.

Does the subject make decisions affecting UK individuals based on protected characteristics?
├── Yes → Equality Act 2010 applies (check for direct/indirect discrimination risk).
└── No → Equality Act not applicable to this subject.

Is the organisation FCA or PRA-regulated?
├── Yes → FCA/PRA AI guidance applies.
│   Is AI used as a model in regulated activities?
│   ├── Yes → PRA SS1/23 applies. Determine model tier.
│   └── No → PRA SS1/23 not applicable.
└── No → FCA/PRA not applicable.
```

### Step 2.3 — Apply India Regulation Decision Tree

```
Does the subject process personal data of Indian individuals (Data Principals)?
├── Yes → DPDP Act 2023 applies.
│   Does the organisation process large volumes of sensitive personal data?
│   ├── Yes or likely → Significant Data Fiduciary (SDF) obligations may apply.
│   └── No → Standard Data Fiduciary obligations apply.
└── No → DPDP Act not applicable.

Is the organisation an RBI-regulated entity (bank, NBFC, payment system operator)?
├── Yes → RBI IT Governance Master Direction applies.
│   Does the AI system constitute a material model (credit, fraud, customer-facing)?
│   ├── Yes → RBI model risk management expectations apply.
│   └── No → General IT governance obligations only.
└── No → RBI not applicable.

Is the organisation a SEBI-registered entity?
├── Yes → Does the AI system involve algorithmic trading or automated investment advice?
│   ├── Yes → SEBI AI/ML circular applies.
│   └── No → General SEBI governance expectations only.
└── No → SEBI not applicable.

Is the organisation an IRDAI-regulated insurer?
├── Yes → IRDAI AI guidance applies (underwriting fairness, claims explainability).
└── No → IRDAI not applicable.

Is the AI system developed or operated from a GCC?
├── Yes → Check extraterritorial obligations from parent company jurisdiction.
└── No → GCC considerations not applicable.
```

### Step 2.4 — Document Applicability Determinations

For each regulation assessed, record:
- **Applicable** — the regulation applies with stated trigger
- **Not applicable** — the regulation does not apply with stated rationale
- **Conditional** — applicability depends on facts not yet determined; state the determining factors

### Phase 2 Output
- Complete list of applicable regulations with triggers
- List of regulations assessed and determined not applicable with rationale
- Flags for conditional or ambiguous applicability

---

## Phase 3 — Framework Mapping

**Objective:** Map the AI subject to applicable governance frameworks to connect regulatory obligations to standards-based controls.

### Step 3.1 — Map to ISO 42001

Identify which ISO 42001 elements are relevant to the subject:

1. **Clause mapping:** Which clauses (4–10) are engaged by the subject's lifecycle stage and governance requirements?
   - Clause 4 (Context): Is the AI subject's operating context defined?
   - Clause 5 (Leadership): Are governance roles and accountability assigned?
   - Clause 6 (Planning): Has an AI risk assessment been conducted?
   - Clause 7 (Support): Are resources, competence, and awareness in place?
   - Clause 8 (Operation): Are lifecycle controls, supply chain controls, and impact assessments implemented?
   - Clause 9 (Performance): Are monitoring, audit, and management review in place?
   - Clause 10 (Improvement): Are corrective action and continuous improvement mechanisms functioning?

2. **Annex A control mapping:** Which of the 38 Annex A controls are applicable? Prioritise controls related to:
   - AI policy and governance
   - Data governance
   - Supply chain management
   - Human oversight
   - Transparency and explainability
   - Monitoring and incident management

3. **AIMS scope:** Does the AI subject fall within the scope of a certifiable AI Management System? If the organisation is pursuing or considering ISO 42001 certification, state the implications.

Reference `knowledge/frameworks/iso-42001.md` for clause and control details.

### Step 3.2 — Map to NIST AI RMF

Identify which NIST AI RMF functions and categories apply to the subject:

- **GOVERN:** Does the subject require governance structures — AI policy, accountability, risk appetite definition, third-party oversight?
- **MAP:** Has the subject's risk context been identified — who is affected, what could go wrong, what is the impact?
- **MEASURE:** Does the subject require testing, evaluation, verification, and validation — bias testing, security testing, performance monitoring?
- **MANAGE:** Does the subject require risk treatment — controls, response plans, documentation, continuous monitoring?

For each applicable function, identify the specific categories and subcategories engaged. Note which function represents the primary governance requirement for this subject.

Reference `knowledge/frameworks/nist-ai-rmf.md`.

### Step 3.3 — Map to OWASP LLM Top 10

Determine if the subject involves an LLM or LLM-based application:

- **If yes:** Identify all applicable OWASP LLM Top 10 risk categories:
  - LLM01 — Prompt Injection
  - LLM02 — Insecure Output Handling
  - LLM03 — Training Data Poisoning
  - LLM04 — Model Denial of Service
  - LLM05 — Supply Chain Vulnerabilities
  - LLM06 — Sensitive Information Disclosure
  - LLM07 — Insecure Plugin Design
  - LLM08 — Excessive Agency
  - LLM09 — Overreliance
  - LLM10 — Model Theft

  For each applicable risk category, map it to the regulatory obligations identified in Phase 2. State which regulatory requirements are addressed by mitigating this OWASP risk.

- **If no:** Mark as N/A with rationale (e.g., "Subject is an ML classifier, not an LLM-based system").

Reference `knowledge/frameworks/owasp-llm-top-10.md`.

### Step 3.4 — Cross-Framework Coherence Check

Verify that framework mappings are coherent:
- Do ISO 42001 clause references align with the NIST AI RMF function assignments?
- Are OWASP LLM risk categories consistent with the regulatory obligations identified?
- Do framework gaps align with regulatory gaps?

### Phase 3 Output
- ISO 42001 clause and Annex A control mappings with rationale
- NIST AI RMF function and category mappings with rationale
- OWASP LLM Top 10 applicability determination and risk category mappings (or N/A)
- Cross-framework coherence verification

---

## Phase 4 — Risk Classification

**Objective:** Classify the AI subject under each applicable regulatory and framework regime.

### Step 4.1 — EU AI Act Risk Classification

Apply the EU AI Act risk tier classification:

```
Is the AI use prohibited under Article 5?
├── Yes → STOP. Prohibited use. Flag immediately for legal review.
└── No → Continue.

Is the AI system a component of a product regulated under Annex I Union harmonisation legislation?
├── Yes → High-risk (Annex I). Full conformity assessment required.
└── No → Continue.

Does the AI system fall within one of the eight Annex III domains?
├── Yes → High-risk (Annex III). Full obligations apply.
│   Specific domain: [identify from Annex III list]
└── No → Continue.

Does the AI system interact directly with natural persons?
├── Yes → Limited risk. Transparency obligations apply.
└── No → Minimal risk. No mandatory obligations (voluntary codes encouraged).

Does the AI system use or constitute a GPAI model?
├── Yes → GPAI obligations apply (separate from risk tier).
└── No → GPAI not applicable.
```

Document the classification with the specific Annex reference and the rationale.

### Step 4.2 — UK Regulatory Risk Classification

Classify under UK frameworks:
- **PRA SS1/23 model tier:** Is this a Tier 1 model (material impact on firm's financial position, reputation, or customer outcomes) or a Tier 2 model (limited impact)?
- **FCA materiality:** Is this AI system material to the firm's regulated activities or consumer outcomes?
- **ICO risk assessment:** Does the system involve high-risk personal data processing requiring a DPIA under UK GDPR Article 35?

### Step 4.3 — India Risk Classification

Classify under Indian frameworks:
- **DPDP Act SDF status:** Does the organisation meet the threshold for Significant Data Fiduciary designation?
- **RBI material model:** Is this a material model requiring formal model risk management under RBI IT Governance guidance?
- **SEBI algorithmic classification:** Is this an algorithmic trading system requiring SEBI registration and audit trail?
- **IRDAI AI classification:** Does the system make underwriting or claims decisions requiring explainability and human review?

### Step 4.4 — Framework Risk Classification

- **ISO 42001:** AI impact level determination — high impact (significant decisions about individuals), medium impact (supporting decisions), or low impact (no direct individual impact)
- **NIST AI RMF:** Risk profile based on MAP function outputs — what is the consequence severity and likelihood?

### Phase 4 Output
- EU AI Act risk tier with specific Annex reference and rationale
- UK regulatory risk classification with rationale
- India regulatory risk classification with rationale
- Framework risk level assignments
- Ambiguities and conditional classifications flagged with determining factors

---

## Phase 5 — Obligation and Requirements Extraction

**Objective:** Derive the specific obligations, documentation, controls, and audit evidence required.

### Step 5.1 — Extract Regulatory Obligations

For each applicable regulation, extract the specific obligations that apply given the risk classification from Phase 4. For each obligation:
1. State the obligation in plain language
2. Cite the specific legal provision (Article, Clause, Section, Circular reference)
3. Classify the obligation type: Registration, Notification, Documentation, Assessment, Monitoring, Reporting, or Disclosure
4. State the compliance timeline (immediate, transitional, event-triggered)
5. State the consequence of non-compliance (penalty range, enforcement mechanism)

Obligation sources by regulation:

| Regulation | Key obligation sources |
|---|---|
| EU AI Act | Articles 6–15 (high-risk), Articles 50–52 (transparency), Articles 53–55 (GPAI) |
| GDPR | Articles 5–6 (lawful basis), Articles 12–22 (data subject rights), Articles 25, 32, 35 (security, DPIA) |
| UK GDPR | Mirror GDPR with ICO-specific guidance |
| DPDP Act | Sections 4–9 (consent, purpose limitation, security), Section 10 (SDF obligations) |
| PRA SS1/23 | Principles 1–5 (model identification, development, validation, monitoring, governance) |
| RBI IT Governance | IT governance, change management, vendor oversight, model risk provisions |
| SEBI AI/ML | Algorithmic trading registration, audit trail, risk controls, human oversight |
| IRDAI | Underwriting fairness, claims explainability, human review |

### Step 5.2 — Derive Documentation Requirements

From the obligations, derive the complete set of documents the organisation must produce:

| Regulatory Regime | Documentation Requirements |
|---|---|
| EU AI Act (high-risk) | Technical documentation (Annex IV), conformity declaration, EU database registration, risk management documentation, quality management system documentation |
| GDPR / UK GDPR | DPIA, Records of Processing Activities (ROPA), Legitimate Interest Assessment (LIA), data breach notification records |
| DPDP Act | Consent records, processing purpose records, DPIA (if SDF), Data Protection Officer appointment |
| PRA SS1/23 | Model documentation, validation report, ongoing performance monitoring reports, model risk governance records |
| RBI IT Governance | IT risk register, change management records, vendor assessment documentation, model documentation |
| SEBI AI/ML | Algorithm registration documentation, audit trail records, risk control documentation, human oversight records |
| ISO 42001 | AIMS documentation, AI policy, risk assessment records, AI impact assessment, internal audit records |

For each document, specify content requirements and whether the obligation is one-time or ongoing.

### Step 5.3 — Derive Control Requirements

Map obligations to required controls. For each control:
- State whether it is **mandatory** (legally required by a specific provision) or **recommended** (expected by a framework or regulator guidance but not legally compelled)
- Classify as Preventive, Detective, or Corrective
- Reference the specific regulatory provision or framework control

### Step 5.4 — Derive Audit Evidence Requirements

Identify what evidence must be producible for each audience:
- **Regulator examinations:** What would FCA, PRA, RBI, SEBI, or a supervisory authority expect to see?
- **Certification body audits:** What does ISO 42001 certification require as objective evidence?
- **Internal audit:** What does the organisation's own audit function need to verify?
- **Incident response:** What evidence is needed to satisfy breach notification obligations?

### Phase 5 Output
- Complete obligation register with legal citations
- Documentation requirements matrix
- Control requirements with mandatory/recommended classification
- Audit evidence register with retention requirements

---

## Phase 6 — BFSI Analysis

**Objective:** Produce the sector-specific assessment for financial services.

### Step 6.1 — Determine BFSI Relevance

Ask: Is the AI subject deployed by, operated by, or affecting a financial services organisation?

If no: mark the BFSI section as N/A with rationale and proceed to Phase 7.

If yes: continue.

### Step 6.2 — Identify BFSI-Specific Obligations

For each applicable BFSI regulatory framework:

- **PRA SS1/23:** Model risk management requirements — classification, validation, monitoring, governance. Does this AI system constitute a model under SS1/23's definition? What model tier is it?
- **FCA Consumer Duty:** Customer outcome obligations for AI systems affecting consumers. Does this AI system influence customer outcomes (product recommendations, pricing, service quality)?
- **FCA/PRA AI guidance:** Sector-specific expectations on bias, explainability, operational resilience.
- **RBI IT Governance:** Technology governance obligations for banks and NBFCs using AI. How does the AI system fit into the institution's IT risk framework?
- **RBI MRM:** Model risk management expectations for credit, fraud, and customer-facing AI. Is formal model validation required?
- **SEBI AI/ML circular:** Algorithmic trading controls, audit trail requirements, human oversight. Does the system execute or recommend trades?
- **IRDAI:** Fairness in underwriting, explainability for claims decisions, human review requirements. Does the system make or influence underwriting or claims decisions?

### Step 6.3 — Identify BFSI-Specific Risks

Assess:
- Which BFSI use cases are exposed? (Credit scoring, fraud detection, KYC/AML, customer service, advisory, algorithmic trading, underwriting, claims)
- What is the supervisory examination risk? (What would a bank examiner or insurance supervisor focus on during a review?)
- Are there customer harm pathways? (Unfair outcomes, discrimination, lack of redress, inappropriate advice)
- Are there systemic risk implications? (Could the AI system's failure affect market stability or systemic risk?)

### Phase 6 Output
- BFSI regulatory framework applicability with specific obligations
- BFSI-specific obligations beyond general AI regulation
- BFSI-specific risk assessment
- Supervisory examination expectations

---

## Phase 7 — Output Production

**Objective:** Produce the final regulatory mapping document.

### Step 7.1 — Assemble Sections 1–8

Compile the outputs from Phases 2–6 into the 9-section output structure defined in `SKILL.md`. Ensure:
- Each section is internally consistent
- Cross-references between sections are accurate (e.g., risk classifications in Section 4 are reflected in obligation scope in Section 3)
- Framework mappings in Section 2 align with control requirements in Section 6

### Step 7.2 — Write the Executive Summary

Write last. By this point, the full analysis is complete and the executive summary can accurately reflect the findings.

Structure:
- Sentence 1–2: What was assessed and across which jurisdictions
- Sentence 3–4: The most significant regulatory exposure (the regulation with the highest compliance burden or penalty risk)
- Sentence 5–6: The risk classification under the most consequential regime
- Sentence 7–8: The key framework alignment gaps (ISO 42001, NIST AI RMF)
- Sentence 9–10: The highest-priority compliance actions

### Step 7.3 — Final Quality Check

Before releasing the mapping, apply the evaluation rubric from `evaluation.md`. The analysis must score at least 70/100 to be released. Mappings scoring below 70 must be revised or reclassified as preliminary.

Cross-check:
- [ ] Every regulation assessed is either applicable (with trigger) or not applicable (with rationale)
- [ ] Every applicable regulation has specific obligations cited with legal references
- [ ] Risk classifications are consistent across sections
- [ ] Framework mappings reference specific clauses and controls, not just framework names
- [ ] OWASP LLM Top 10 is correctly applied (for LLM subjects) or correctly marked N/A
- [ ] BFSI section is correctly populated or correctly marked N/A
- [ ] Executive summary accurately reflects the body analysis
- [ ] No obligation is stated without a legal citation
- [ ] No framework mapping is generic — each references specific clauses, functions, or risk categories

---

## Output Document Structure

The completed regulatory mapping is produced in the following structure:

```markdown
# Regulatory Mapping: [Subject Name]

**Date of Assessment:** [Date]
**Subject Type:** [Use Case / System / Incident / Control / Portfolio]
**Jurisdictions Assessed:** [List]
**Industry:** [Industry]
**Evidence Quality:** [High / Medium / Low]
**Assessment Status:** [Final / Preliminary]

---

## 1. Applicable Regulations
[Jurisdiction-by-jurisdiction regulation identification with triggers]

## 2. Applicable Governance Frameworks
### ISO 42001
[Clause and Annex A control mappings]
### NIST AI RMF
[Function and category mappings]
### OWASP LLM Top 10
[Risk category mappings or N/A]

## 3. Regulatory Obligations
[Obligation register with legal citations]

## 4. Risk Classification
### EU AI Act Classification
### UK Regulatory Classification
### India Regulatory Classification

## 5. Documentation Requirements
[Documentation matrix with content and maintenance requirements]

## 6. Control Requirements
[Control register with mandatory/recommended classification]

## 7. Audit Evidence Required
[Evidence register with retention requirements]

## 8. BFSI Considerations
[Or N/A]

## 9. Executive Summary
[250 words max]
```

---

## Time Estimates

| Subject Type | Jurisdictions | Estimated Time |
|---|---|---|
| Single use case, single jurisdiction | 1 | 30–45 minutes |
| Single use case, multi-jurisdiction | 2–3 | 60–90 minutes |
| AI system (deployed), multi-jurisdiction | 2–3 | 90–120 minutes |
| AI portfolio assessment | 2–3 | 120–180 minutes |
| Incident regulatory mapping | 1–3 | 45–75 minutes |
| Condensed assessment (limited input) | 1 | 20–30 minutes |
