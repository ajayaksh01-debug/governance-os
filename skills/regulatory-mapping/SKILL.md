# Skill: Regulatory Mapping

**Version:** 1.0  
**Category:** Governance Intelligence  
**Owner:** Cursory Governance Team

---

## Purpose

This skill maps AI use cases, incidents, controls, and systems to applicable regulations and governance frameworks across jurisdictions. The output is a structured regulatory and framework alignment assessment that identifies which laws, standards, and governance requirements apply to a given AI subject — and what obligations, classifications, documentation, controls, and audit evidence follow from that applicability.

The skill converts a description of an AI subject (a use case being planned, a deployed system, an incident under review, or a control being evaluated) into a reusable governance artefact: a document that captures which regulations apply, which governance frameworks are relevant, what the specific obligations are, how the subject is classified under each regime, and what the organisation must do to demonstrate compliance.

---

## When to Use This Skill

Use this skill when:
- A new AI use case is being planned and requires regulatory exposure assessment before development
- An existing AI system requires a compliance review against current regulatory requirements
- An AI incident has occurred and the regulatory implications need to be mapped
- A client onboarding or assessment requires a regulatory landscape analysis for their AI portfolio
- A regulatory change has occurred and its impact on existing AI systems must be assessed
- An AI control framework is being designed and must be mapped to applicable regulatory requirements
- A cross-jurisdictional deployment requires identification of obligations across multiple legal regimes
- A governance framework alignment assessment is required alongside regulatory mapping

---

## Input Specification

### Required Inputs

The skill requires at minimum a description of the AI subject and the jurisdictions in scope. The subject may be:
- An AI use case description (planned or deployed)
- An AI system specification or architecture
- An AI incident report
- An AI control or control framework under evaluation

### Input Fields

| Field | Required | Description |
|---|---|---|
| `subject_description` | Yes | Description of the AI use case, system, incident, or control to be mapped. Can be a design document, product specification, incident report, or informal summary. |
| `subject_type` | Yes | One of: AI Use Case, AI System, AI Incident, AI Control, AI Portfolio |
| `jurisdictions` | Yes | List of jurisdictions to assess. Supported: EU, UK, India. For India, specify if BFSI-regulated. |
| `industry` | No | Industry sector of the organisation. Critical for BFSI, healthcare, critical infrastructure. |
| `data_types` | No | Types of data processed by the AI subject (personal data, financial data, health data, biometric data, public data). |
| `affected_individuals` | No | Categories of individuals affected by the AI system's outputs or decisions (employees, customers, public, minors). |
| `deployment_model` | No | How the AI system is deployed (cloud, on-premise, hybrid, third-party SaaS, GCC-operated). |
| `client_context` | No | If this mapping is for a specific client, their sector, size, AI maturity, and regulatory relationships. |
| `ai_technology` | No | The AI technology involved (LLM, ML classifier, computer vision, NLP, autonomous agent, ensemble). Affects OWASP LLM Top 10 applicability. |

### Input Format

Inputs do not need to be structured. The skill accepts free-form descriptions and extracts structured information during analysis. For a new AI use case, a minimum viable input is:

> "What the AI system does, what data it processes, who it affects, and where it operates."

---

## Output Specification

Every regulatory mapping assessment produces the following nine sections. Each section has a defined structure and quality standard (see `evaluation.md`).

### 1. Applicable Regulations
A jurisdiction-by-jurisdiction identification of every regulation that applies to the AI subject. For each regulation:
- Regulation name and jurisdiction
- Why it applies (the specific trigger — personal data processing, high-risk classification, financial services activity, etc.)
- Whether applicability is confirmed, likely, or conditional on facts not yet determined

Regulations assessed include, but are not limited to:
- **EU:** EU AI Act, GDPR
- **UK:** UK GDPR, Data Protection Act 2018, Equality Act 2010, FCA/PRA guidance, PRA SS1/23
- **India:** DPDP Act 2023, RBI IT Governance and MRM guidance, SEBI AI/ML circular, IRDAI guidance, MEITY advisories

Where a regulation does not apply, this is stated with a brief rationale. Absence of applicability is an affirmative finding, not an omission.

### 2. Applicable Governance Frameworks
Mapping of the AI subject to relevant governance frameworks. For each framework:

**ISO 42001:**
- Relevant clauses (Clause 4–10) implicated by the subject
- Applicable Annex A controls
- Whether the subject falls within the scope of a certifiable AI Management System (AIMS)

**NIST AI RMF:**
- Relevant functions (GOVERN, MAP, MEASURE, MANAGE) applicable to the subject
- Specific categories and subcategories engaged
- How the subject maps to the AI RMF lifecycle

**OWASP LLM Top 10:**
- Applicable risk categories (if the subject involves an LLM or LLM-based application)
- If the subject does not involve an LLM, this is marked N/A with rationale
- Where applicable, specific OWASP risk categories are mapped to the regulatory obligations identified in Section 1

### 3. Regulatory Obligations
For each applicable regulation identified in Section 1, the specific obligations that apply. Each obligation is documented with:
- Obligation description (what the organisation must do)
- Legal basis (the specific article, clause, or provision)
- Obligation type (Registration, Notification, Documentation, Assessment, Monitoring, Reporting, Disclosure)
- Timeline (when compliance is required — immediate, transitional period, or triggered by specific events)
- Consequence of non-compliance (penalty range, enforcement mechanism, supervisory action)

### 4. Risk Classification
Classification of the AI subject under each applicable regulatory regime:

**EU AI Act:** Prohibited / High-risk (Annex I or III) / Limited risk / Minimal risk / GPAI model obligations

**UK:** Risk level under FCA/PRA supervisory frameworks; model tier under PRA SS1/23 (if BFSI)

**India:** Significant Data Fiduciary status under DPDP Act; material model classification under RBI MRM guidance; algorithmic trading classification under SEBI

Each classification is stated with the rationale and the specific provision that determines the classification. Where classification is ambiguous, both possible classifications are stated with the factors that would determine the outcome.

### 5. Documentation Requirements
The specific documentation the organisation must produce and maintain to demonstrate compliance. For each requirement:
- Document type (Technical documentation, Risk assessment, Impact assessment, Conformity declaration, Audit trail, Policy document)
- Regulatory source (which regulation or framework requires it)
- Content requirements (what the document must contain)
- Maintenance obligation (one-time or ongoing; retention period if specified)

### 6. Control Requirements
The technical and organisational controls required by applicable regulations and frameworks. For each control:
- Control name and description
- Regulatory source (specific article, clause, or Annex A control)
- Control type (Preventive / Detective / Corrective)
- Whether the control is mandatory (legally required) or recommended (best practice under frameworks)
- Implementation guidance (sufficient detail to scope the control, not to implement it)

### 7. Audit Evidence Required
The evidence the organisation must be able to produce for regulators, auditors, or certification bodies. For each evidence item:
- Evidence type (Log, Report, Assessment, Test result, Policy document, Training record)
- Purpose (what it demonstrates)
- Regulatory or framework source
- Retention requirement (if specified)
- Format guidance (structured data, narrative report, or either)

### 8. BFSI Considerations
Where the AI subject is deployed in or relevant to financial services, a dedicated assessment covering:
- Which BFSI-specific regulatory frameworks apply (PRA SS1/23, FCA Consumer Duty, RBI IT Governance, RBI MRM, SEBI AI/ML circular, IRDAI guidance)
- BFSI-specific obligations beyond general AI regulation
- Model risk management requirements (SR 11-7, SS1/23)
- Consumer and customer impact obligations
- Supervisory examination expectations

If the subject is not BFSI-relevant, this section is marked N/A with a brief rationale.

### 9. Executive Summary
A 200–250 word summary of the entire mapping, written for a board or C-suite audience. Covers: what was assessed, the most significant regulatory exposures, the risk classification under the most consequential regime, the key framework alignment gaps, and the highest-priority compliance actions. No technical jargon. No framework references without explanation.

---

## Constraints and Scope

**In scope:**
- AI systems (LLMs, ML models, AI agents, AI-enabled products, autonomous systems)
- AI use cases at any lifecycle stage (planning, development, deployment, production, retirement)
- AI incidents with regulatory implications
- AI controls being evaluated for regulatory sufficiency
- Multi-jurisdictional assessments across EU, UK, and India
- Governance framework alignment assessment (ISO 42001, NIST AI RMF, OWASP LLM Top 10)

**Out of scope:**
- Pure cybersecurity assessments with no AI-specific regulatory dimension
- General IT compliance (ISO 27001, SOC 2) unless directly triggered by AI-specific regulation
- Regulatory mapping for jurisdictions not currently covered in the knowledge base (US, Canada, Australia, etc.)
- Legal advice — this skill produces regulatory intelligence, not legal opinions

**Depth calibration:**
Analysis depth should be proportionate to the subject's risk profile and the number of jurisdictions. A high-risk BFSI use case operating across three jurisdictions warrants a full 9-section analysis. A minimal-risk internal tool in a single jurisdiction may produce a condensed assessment noting limited regulatory engagement.

**Ethana capability references:**
When Section 6 (Control Requirements) or Section 8 (BFSI Considerations) references an Ethana capability to illustrate how a control requirement maps to the platform, the capability status must be sourced from `knowledge/ethana/canonical-product-model.md`. This skill does not validate Ethana capability claims — that is the function of `skills/ethana-capability-validation/`. If a capability's status is uncertain, reference the capability by name and note "status to be confirmed by Capability Validation" rather than asserting a status.

---

## Knowledge Dependencies

This skill draws on the following knowledge base documents:

**Frameworks:**
- `knowledge/frameworks/iso-42001.md`
- `knowledge/frameworks/nist-ai-rmf.md`
- `knowledge/frameworks/owasp-llm-top-10.md`

**Regulations:**
- `knowledge/regulations/eu-ai-act.md`
- `knowledge/regulations/uk-ai-guidance.md`
- `knowledge/regulations/india-ai-landscape.md`

**Controls:**
- `knowledge/controls/data-protection-controls.md`
- `knowledge/controls/model-risk-controls.md`
- `knowledge/controls/audit-controls.md`
- `knowledge/controls/agent-governance-controls.md`
- `knowledge/controls/prompt-injection-controls.md`

**BFSI:**
- `knowledge/bfsi/banking-ai-governance-use-cases.md`
- `knowledge/bfsi/insurance-ai-governance.md`
- `knowledge/bfsi/wealth-management-ai-governance.md`
- `knowledge/bfsi/gcc-ai-governance-patterns.md`

**Ethana:**
- `knowledge/ethana/canonical-product-model.md` — primary authority for all Ethana capability status references in Section 6 or Section 8. When this skill references an Ethana capability to illustrate a control mapping, the capability status must be sourced from this file. No other Ethana knowledge file may override it.
- `knowledge/ethana/framework-crosswalk.md` — framework-to-capability mapping reference. Status flags in this file (`[P]`, `[IB]`, `[RM]`) should be cross-checked against `canonical-product-model.md` before inclusion in any output section. This file is useful for identifying which Ethana capabilities map to which framework controls, but it is not an authority for capability status.

---

## Related Skills

- `skills/ai-incident-analysis/` — for incidents requiring full governance root cause analysis beyond regulatory mapping
- `skills/governance-control-mapping/` — for translating regulatory control requirements into specific control implementations (planned)
- `skills/ethana-solution-mapping/` — for mapping regulatory control requirements to Ethana platform capabilities
- `skills/iso-42001-gap-assessment/` — for detailed ISO 42001 gap analysis following framework identification (planned)
