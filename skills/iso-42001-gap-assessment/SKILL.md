# Skill: ISO 42001 Gap Assessment

**Version:** 1.0  
**Category:** Standards Compliance — Gap Assessment  
**Owner:** Cursory Governance Team

---

## Purpose

This skill conducts a structured, clause-by-clause gap assessment of an organisation's current practices against ISO/IEC 42001:2023, the international standard for AI Management Systems (AIMS). It produces a conformity assessment, a consolidated gap register, risk prioritisation, evidence requirements, a phased remediation roadmap, an Ethana platform coverage analysis, and two composite scores that measure certification readiness.

Where Regulatory Mapping identifies which governance frameworks apply to an organisation's AI portfolio, this skill audits how well the organisation currently satisfies those frameworks — specifically ISO 42001. Where Governance Control Mapping translates requirements into control specifications, this skill identifies which requirements have gaps that need to be filled. The two skills together form the standards compliance chain: identify what applies → assess what exists → design what is missing.

The skill produces two organisation-level scores and a Certification Classification that determines the organisation's readiness for third-party ISO 42001 certification or formal self-declaration:

- **AIMS Maturity Score (AMS):** A 0–100 score measuring how mature the organisation's AI Management System is against ISO 42001's seven operative clauses (Clauses 4–10) and 38 Annex A controls. AMS measures "how complete is the AIMS?"
- **Audit Readiness Score (ARS):** A 0–100 composite score measuring the organisation's readiness to present its AIMS to an external auditor. ARS measures "can the AIMS withstand scrutiny?" ARS is independent of AMS — a mature AIMS with poor documentation can score high on AMS and low on ARS.

**Mandatory authority sources:**
- `knowledge/frameworks/iso-42001.md` — the ISO 42001 knowledge base; all clause and Annex A references are grounded here.
- `knowledge/ethana/canonical-product-model.md` — the sole permitted source for Ethana capability status determinations in Section 8. Any Ethana capability cited as Production in the Ethana Coverage Analysis must trace to this file.
- `docs/decisions/ADR-002-claims-firewall.md` — enforced in Section 8.5 (Claims Firewall Review); governs which Ethana capabilities may be presented as current in a client-facing assessment.

---

## When to Use This Skill

Use this skill when:
- An organisation wants to understand its readiness for ISO 42001 certification
- A Regulatory Mapping has identified ISO 42001 as applicable and the client needs to know how far they are from compliance
- A client is building a business case for AI governance investment and needs a structured maturity baseline
- An organisation holds ISO 27001 and wants to understand the incremental gap to ISO 42001
- A regulatory submission, board-level AI governance report, or enterprise procurement due-diligence requires a formal AIMS gap assessment
- A client needs to understand which Ethana capabilities close specific ISO 42001 gaps and which gaps remain

Do not use this skill to assess framework alignment against NIST AI RMF or OWASP LLM Top 10 — those assessments are conducted within the Regulatory Mapping skill. This skill is specific to ISO 42001.

---

## Relationship to Other Skills

| | Regulatory Mapping | ISO 42001 Gap Assessment | Governance Control Mapping |
|---|---|---|---|
| **Question answered** | Which frameworks apply? | How mature is our AIMS against ISO 42001? | How do we implement the controls? |
| **Layer** | Regulatory Intelligence | Standards Compliance | Control Operationalisation |
| **Input** | AI subject description | Organisation description + AI portfolio + RM Section 2 | Gap Register (Section 4) + upstream findings |
| **Output** | Obligations, clauses, frameworks | AMS + ARS + Gap Register + Remediation Roadmap | Control specifications + Ethana configuration guide |
| **Audience** | Legal & Compliance | CISO, CRO, Chief AI Officer, Certification body | AI Engineering, Security, Operations |
| **Timing** | Pre-assessment | After regulatory framing; before control design | After gap assessment |
| **Primary metric** | Framework coverage | AMS + ARS | Control coverage % |
| **Pass threshold** | 70/100 | **85/100** | 85/100 |

**Why 85/100?** An error in the gap assessment propagates directly into the remediation roadmap, the evidence requirements, and the Ethana coverage analysis. If a gap is missed here, no downstream skill will catch it — Governance Control Mapping assumes the gap register is complete. The assessment standard is correspondingly strict.

---

## Input Specification

### Required Inputs

| Field | Required | Description |
|---|---|---|
| `organisation_description` | Yes | Description of the organisation: sector, size, AI use cases currently deployed or planned, and the context driving the assessment (certification preparation, regulatory requirement, board mandate, procurement due-diligence). This provides the baseline for scope definition in Phase 1. |
| `ai_portfolio` | Yes | A list of AI systems currently in scope for the AIMS — what they do, who they affect, their deployment status, and who owns them. The scope of the assessment cannot be defined without knowing what AI is in it. Assessments run against an undefined portfolio cannot receive a valid AMS. |
| `jurisdictions` | Yes | Jurisdictions in scope. EU (triggers EU AI Act and GDPR overlay on Annex A controls), UK (triggers UK GDPR and FCA/PRA model risk overlay), India (triggers DPDP Act and RBI MRM overlay on Annex A controls). |

### Contextual Inputs

| Field | Required | Description |
|---|---|---|
| `regulatory_mapping_output` | Strongly Recommended | Full output from `skills/regulatory-mapping/`. Section 2 (Applicable Governance Frameworks) pre-populates which ISO 42001 clauses are implicated by the organisation's AI systems; Section 6 (Control Requirements) maps existing control obligations to specific Annex A categories. Without this input, clause identification must be performed from scratch in Phase 2, adding significant time and risk of omission. |
| `control_mapping_output` | Recommended | Output from `skills/governance-control-mapping/`. Section 3 (Control Coverage Classification) identifies controls already designed and documented — prevents duplication in the Gap Register. Without this, the assessment cannot determine whether identified Annex A gaps have already been addressed by existing control specifications. |
| `existing_documentation` | Recommended | Any documentation the organisation already holds that may satisfy ISO 42001 requirements: ISO 27001 certificate (enables Annex SL credit in Clauses 4–7), SOC 2 report, existing AI policy, prior gap assessment, board-level AI ethics statement, model risk framework, AI incident log. Providing this input allows accurate partial-credit scoring rather than assuming zero baseline. |
| `target_certification` | Contextual | `Third-party certification` / `Self-declaration` / `Internal audit only` / `Regulatory submission`. Third-party certification applies the strictest evidence standards (Stage 1 documentation review + Stage 2 on-site audit). Self-declaration is lighter — policy documentation may suffice where certification would require implemented controls. Shapes ARS severity calibration and Section 9 verdict language. |
| `industry` | Contextual | BFSI / Healthcare / Government / Critical Infrastructure / Retail / Technology / General Enterprise. BFSI triggers a model risk overlay (SR 11-7, PRA SS1/23) in the Annex A control assessment — specifically on Annex A Category 3 (AI System Lifecycle) and Category 9 (Monitoring). |
| `current_maturity_baseline` | Contextual | Prior assessment results (AMS, ARS, and critical gap count at the baseline date). Enables gap closure tracking between assessments and adjusts the phrasing of Section 7 (Remediation Roadmap) from "from scratch" to "continuation of ongoing programme." |

### Input Format

Inputs do not need to be structured. The skill accepts free-form descriptions and extracts structured information during Phase 1. Minimum viable input:

> "What the organisation is, what AI systems are in scope, and which jurisdictions apply."

Full-quality assessment requires `regulatory_mapping_output` to be provided. Without it, Section 2 (Clause Coverage Matrix) is constructed from first principles and is more likely to miss jurisdiction-specific clause requirements.

---

## Output Specification

Every assessment produces the following ten sections. For an abbreviated spot-check on a single clause or Annex A category, Sections 2 or 3 (as applicable), Section 4 (restricted to the relevant clause), and Section 10 are sufficient. Full assessments require all ten sections.

### 1. Executive Summary

A 200–250 word non-technical summary of the gap assessment findings, written for the CISO, CRO, Chief AI Officer, and board. Covers:
- The scope of the assessment (organisation, AI systems, jurisdictions)
- The AMS and ARS scores and what they mean in plain language
- The Certification Classification verdict
- The total gap count by severity (Critical / Major / Minor)
- The single most important action required before certification readiness is achievable
- The estimated time to Stage 1 readiness (if target is third-party certification)

Written last, after all other sections are complete. Must not state a Certification Classification that contradicts Section 10.

### 2. Clause Coverage Matrix

A per-clause assessment covering ISO 42001 Clauses 4 through 10. Each clause is assessed on the following structure:

| Clause | Clause name | Key requirements | Current state | Evidence basis | Maturity rating (0–5) | Gap severity |
|---|---|---|---|---|---|---|
| Clause 4 | Context of the Organisation | [...] | [...] | [...] | [0–5] | Critical / Major / Minor / None |

**Maturity ratings:**
- **0 — Not Started:** No awareness of or activity against this clause's requirements
- **1 — Initial:** Ad hoc activities exist but are not documented, repeatable, or assigned to a responsible role
- **2 — Developing:** Requirements are acknowledged and some documentation exists, but coverage is partial and inconsistency across the AI portfolio is evident
- **3 — Defined:** Requirements are formally documented in policy or procedure; coverage is consistent across the assessed AI systems; roles are assigned
- **4 — Managed:** Documented requirements are monitored; metrics exist; management reviews occur; deviations are tracked and resolved
- **5 — Optimising:** Continuous improvement programme in place; metrics drive proactive adjustments; the clause's requirements are embedded in governance culture

**Clause-specific key requirements:**
- **Clause 4 (Context):** AIMS scope defined; internal and external context documented; interested parties and their requirements identified; risk appetite for AI established
- **Clause 5 (Leadership):** AI policy signed by top management; roles and responsibilities formally assigned; AI governance integrated into strategic planning
- **Clause 6 (Planning):** AI risk assessment methodology defined and applied; AI impact assessment process exists; treatment options documented
- **Clause 7 (Support):** Resources assigned to the AIMS; competence requirements defined and met; AI governance awareness programme in place; documentation control procedures established
- **Clause 8 (Operation):** AI system lifecycle managed end-to-end (design, training, testing, deployment, monitoring, retirement); AI impact assessments completed for systems in scope; third-party AI providers managed under contractual and assessment controls; operational changes controlled
- **Clause 9 (Performance Evaluation):** Production monitoring in place; internal audit programme established and executed; management reviews documented; performance metrics defined and tracked
- **Clause 10 (Improvement):** Nonconformity detection and corrective action process exists; continual improvement mechanism in place; lessons from incidents and audits are tracked and actioned

### 3. Annex A Control Assessment

A per-control assessment covering all 38 Annex A controls across 9 control categories. Every control must be assessed — controls that are not applicable to the organisation's AI portfolio must be marked N/A with a brief rationale; they may not be omitted.

**Status assignments per control:**
- **Implemented:** The control is in place, documented, and operating effectively with available evidence
- **Partially Implemented:** The control exists in some form but has gaps — incomplete coverage across the AI portfolio, missing documentation, or limited evidence
- **Not Implemented:** The control is applicable but no activity against it has occurred
- **N/A:** The control is not applicable to this organisation's AI portfolio; rationale stated

**The nine Annex A control categories:**

**Category 1 — AI Policy and Governance (4 controls):**
- AI policy (AI-specific policy statement, signed by top management, scope defined)
- Roles and responsibilities for AI governance (designated AI accountability; not delegated solely to technology or legal)
- AI risk criteria (organisation-defined thresholds for AI risk acceptance and treatment)
- AI governance framework (the documented structure connecting AI policy, risk, controls, and oversight)

**Category 2 — AI Risk Assessment and Impact (5 controls):**
- AI impact assessment process (methodology for assessing societal, individual, and organisational impacts before deploying new AI systems)
- AI risk identification (structured identification of risks from AI systems — bias, opacity, autonomy, data quality, adversarial attack)
- AI risk evaluation (scoring and prioritisation of identified risks against defined criteria)
- Bias risk assessment (structured evaluation of bias risks specific to the AI system's use context and affected population)
- Data quality assessment (assessment of whether training and operational data meets requirements for intended use)

**Category 3 — AI System Lifecycle (6 controls):**
- AI design requirements (defined functional, ethical, and governance requirements before AI system development or procurement)
- Training data management (controls over selection, labelling, and documentation of training data)
- AI system testing and validation (pre-deployment testing including adversarial, bias, and performance testing)
- Deployment controls (approval gates, configuration baselines, and access controls governing system deployment)
- Change management (controls over modifications to production AI systems, including re-validation requirements)
- System retirement and decommissioning (process for safely retiring AI systems and managing associated data)

**Category 4 — Data Governance (4 controls):**
- Data provenance (documented origin and transformation history of data used in AI systems)
- Data quality (ongoing assurance that data meets defined quality requirements in production)
- Data minimisation (controls ensuring AI systems use only the data necessary for their intended function)
- Third-party data controls (assessment and contractual control of data obtained from external sources for AI training or operation)

**Category 5 — Supply Chain and Third Parties (4 controls):**
- Third-party AI provider assessment (evaluation of AI vendors and tools before adoption against defined governance criteria)
- Contractual controls for AI supply chain (contractual requirements imposed on third-party AI providers covering data, security, transparency, and audit rights)
- Third-party AI provider monitoring (ongoing monitoring of third-party AI providers against contractual requirements and governance criteria)
- Supply chain risk management (management of risks arising from the AI supply chain, including model updates, data source changes, and provider discontinuation)

**Category 6 — Human Oversight (3 controls):**
- Human review requirements (defined cases where AI outputs require human review before action; override mechanisms available to operators)
- Override mechanisms (the ability for authorised humans to override, suspend, or override AI system outputs; tested and documented)
- Operator explainability (AI systems can be explained to operators in terms appropriate to their role; explanation depth matched to consequentiality of the AI decision)

**Category 7 — Incident Management (3 controls):**
- AI incident detection and response (defined process for detecting, classifying, and responding to AI-specific incidents — bias events, unexpected behaviour, adversarial attacks)
- Post-incident review (structured review of AI incidents to identify root causes and governance lessons)
- Incident lessons learned (mechanism for translating incident lessons into AIMS improvements — policy, control, or training updates)

**Category 8 — Transparency and Explainability (3 controls):**
- Disclosure requirements (documented determination of what must be disclosed about AI systems to affected individuals, regulators, and customers)
- Explainability documentation (documentation of how AI systems reach outputs, at the depth required by the risk profile and regulatory context)
- User notification (process for notifying affected individuals when they are subject to AI decision-making, at the level required by applicable regulation)

**Category 9 — Monitoring and Performance (6 controls):**
- Production monitoring (ongoing monitoring of AI system performance, accuracy, and behaviour in production)
- Performance metrics (defined metrics for evaluating AI system performance against governance objectives)
- Drift detection (mechanisms for detecting model drift, distribution shift, or performance degradation over time)
- Audit evidence collection (systematic collection of evidence from AI system operations to support internal and external audits)
- Management review triggers (defined conditions under which AI governance performance triggers a formal management review)
- Continual improvement mechanism (structured process for incorporating monitoring findings, audit results, and incident lessons into AIMS improvements)

### 4. Gap Register

A consolidated, uniquely identified register of every gap identified in Sections 2 and 3. Each gap entry:

| Gap ID | Clause / Control reference | Gap description | Severity | Effort estimate | Owner |
|---|---|---|---|---|---|
| GAP-CL4-001 | Clause 4 — Context | AIMS scope has not been formally documented | Critical | 2 weeks | CISO |
| GAP-AA3-001 | Annex A Category 3 — AI Lifecycle | No deployment approval gate exists for new AI systems | Major | 6 weeks | AI Platform Team |

**Gap ID scheme:** `GAP-[CL{clause number} or AA{category number}]-[sequential three-digit number]`
- `GAP-CL4-001` = first Clause 4 gap; `GAP-CL8-003` = third Clause 8 gap
- `GAP-AA3-001` = first Annex A Category 3 gap; `GAP-AA9-002` = second Annex A Category 9 gap

**Severity definitions:**
- **Critical:** The gap represents a fundamental absence that would cause a Stage 2 audit failure. No certification is possible while this gap is open. Examples: AIMS scope undefined; AI policy absent; no impact assessment process; Clause 8 lifecycle management completely absent.
- **Major:** The gap represents a material weakness that would be flagged as a significant nonconformity at audit. Certification is unlikely while this gap is open. Examples: impact assessments defined but not completed for systems in scope; monitoring defined but not operating; supplier assessment criteria not applied to existing vendors.
- **Minor:** The gap represents an area of improvement that an auditor would note but that would not block certification. Examples: documentation exists but is not version-controlled; monitoring metrics defined but thresholds not yet calibrated; operator training conducted but not recorded.

**Effort estimates** are stated in person-weeks and assume Cursory advisory support. They are indicative, not contractually binding.

### 5. Risk Prioritisation

A risk matrix organising all gaps from Section 4 on two axes: certification risk (whether the gap would block certification) and business risk (the operational consequence of the gap if unaddressed).

| Gap ID | Severity | Certification blocker | Business risk | Priority rank |
|---|---|---|---|---|
| GAP-CL4-001 | Critical | Yes | High | P1 |
| GAP-AA3-001 | Major | Yes | Medium | P2 |
| GAP-AA8-001 | Minor | No | Low | P5 |

**Priority ranks:**
- **P1:** Critical gap + certification blocker — address immediately; blocks Stage 1 readiness
- **P2:** Major gap + certification blocker — address before Stage 1; may be conditioned at Stage 2
- **P3:** Major gap + not a direct certification blocker — address within 90 days
- **P4:** Minor gap + certification blocker for specific clauses — address before Stage 2
- **P5:** Minor gap + not a certification blocker — address as part of continual improvement

### 6. Evidence Requirements

For each gap in the register, the evidence the organisation must be able to produce to a Stage 2 auditor to demonstrate that the gap has been closed. This section is structured per gap and specifies:

- **Evidence type:** Policy document / Process document / Risk assessment / Test result / Audit log / Training record / Management meeting minutes / Contractual document
- **Evidence description:** What the document must contain to satisfy the auditor
- **Source system:** Where the evidence would come from (ISMS documentation system, Ethana Immutable Audit Log, HR training records, etc.)
- **Retention requirement:** How long the evidence must be retained under ISO 42001 or applicable regulation
- **Readiness status:** Evidence exists / Partially available / Not available

This section is the direct input to the Audit Readiness Score (ARS) component "Evidence Availability" computed in Phase 7.

### 7. Remediation Roadmap

A phased action plan for closing all gaps in the Gap Register, organised by priority. Phases are:

**30-day sprint (Critical and P1 gaps only):**
Actions required to establish the minimum viable AIMS — scope definition, AI policy, top management commitment, and basic impact assessment capability.

**60-day sprint (Critical completion + Major P2 gaps):**
Actions required to achieve a documentable AIMS structure covering all seven clauses at maturity level 2 or above.

**90-day sprint (Major P3 gaps):**
Actions required to achieve a documentable AIMS at maturity level 3 across key clauses, with operating evidence beginning to accumulate.

**180-day programme (Minor gaps + maturity elevation):**
Actions required to reach maturity level 4 across clauses 8 and 9 (the most evidence-intensive clauses) and close all Minor gaps in advance of Stage 2.

Each action in the roadmap specifies: the gap it closes, the deliverable, the responsible role, and the dependency chain (actions that must complete before this action can start).

### 8. Ethana Coverage Analysis

An analysis of which ISO 42001 gaps can be partially or fully addressed by the Ethana platform, and which require Cursory advisory services or third-party solutions.

For each gap in the Gap Register:
- **Ethana capability mapped:** The specific Ethana capability (e.g., Immutable Audit Log, Runtime Guardrails, Red Teaming Orchestrator) that addresses this gap
- **Coverage type:** Full (the platform capability fully closes the gap) / Partial (the capability provides evidence or tooling support but does not close the gap without additional policy or process work) / None (no Ethana capability addresses this gap)
- **Status:** Production / In Build / Aspirational / N/A (from canonical-product-model.md)
- **Cursory service alternative:** Where Ethana does not provide Production coverage, the Cursory advisory service that addresses the gap
- **Third-party requirement:** Where neither Ethana nor Cursory services address the gap (e.g., accredited certification body, specialist bias auditor)

**How to read this section:** Every entry represents a commercial positioning opportunity — a specific gap, the Ethana or Cursory response to it, and the constraints on what can be claimed. Do not present In Build capabilities as closing gaps today.

#### Section 8.5 — Claims Firewall Review

**Purpose:** Validate every Ethana capability reference in this section against `knowledge/ethana/canonical-product-model.md` before the assessment is released. This sub-section is mandatory and must be completed before Section 8 can be finalised.

**Valid References:**
All Ethana capabilities cited in Section 8 where the canonical model confirms Production status. State the verbatim canonical model entry for each.

**Invalid References:**
Any Ethana capability cited as current or available where the canonical model classifies it as In Build or Aspirational. For each invalid reference:
- Capability name
- How it was cited in Section 8 (the incorrect assertion)
- Canonical model status (verbatim)
- Required correction (reclassify as roadmap item / remove / replace with Cursory service)

Any invalid reference found in Section 8.5 becomes HD2 — the assessment is blocked from release until all invalid references are corrected.

**Required Caveats:**
Valid Production capabilities that carry mandatory caveats in the canonical model (e.g., Bias Scanner — runtime filter only; on-premises deployment — scale at Tier 1 unproven). List each caveat and confirm it appears in Section 8 alongside the capability reference.

**Third-Party Alternatives:**
For gaps where neither Production Ethana capabilities nor Cursory services provide coverage, the specific third-party capability recommended (e.g., accredited certification body for Stage 2 audit, specialist bias auditor for statistical bias validation, formal model validation firm for quantitative model testing).

### 9. Audit Readiness Assessment

A structured assessment of the organisation's readiness to present its AIMS to a Stage 1 (documentation review) and Stage 2 (on-site evidence review) audit. Produces the Audit Readiness Score (ARS).

**ARS calculation:**

```
ARS = (Documentation_Completeness × 0.30)
    + (Evidence_Availability × 0.40)
    + (Control_Operationalization × 0.20)
    + (Management_Review_Readiness × 0.10)
```

**Documentation Completeness (0–100, weight 30%):**
The degree to which required AIMS documentation — AI policy, scope document, risk assessment, impact assessments, control specifications, internal audit plan — exists and is controlled (versioned, approved, accessible).
- 90–100: All required documents exist, are current, approved, and under version control
- 70–89: Core documents (policy, scope, risk assessment) exist; supplementary documents partially complete
- 40–69: Policy exists; impact assessments or control specifications incomplete; documentation not version-controlled
- 0–39: Critical documents (AI policy or AIMS scope) absent

**Evidence Availability (0–100, weight 40%):**
The degree to which evidence of AIMS operation is available and retrievable — audit logs, test results, management review minutes, training records, supplier assessments.
- 90–100: Evidence exists for all required controls; retrievable in structured form; retention period met
- 70–89: Most evidence available; some gaps in retention or structured access
- 40–69: Evidence available for some controls; significant gaps for Clause 8 and 9 controls
- 0–39: Evidence largely unavailable or unstructured

**Control Operationalization (0–100, weight 20%):**
The degree to which defined controls are actively operating — not just documented but demonstrably in use.
- 90–100: All controls in scope are operating; operating evidence available
- 70–89: Most controls operating; one or two controls defined but not yet active
- 40–69: Controls defined but significant fraction not yet operating
- 0–39: Controls documented but not operating; paper AIMS only

**Management Review Readiness (0–100, weight 10%):**
The degree to which management is engaged and prepared to discuss the AIMS — review meetings held, objectives set, AI governance on the board agenda.
- 90–100: Management review cycle established; last review documented; objectives traceable
- 70–89: Management review held at least once; some objectives set but tracking incomplete
- 40–69: Management awareness exists but no formal review cycle
- 0–39: No evidence of management engagement with the AIMS

**Stage verdicts:**
- **Stage 1 Ready:** Documentation Completeness ≥ 70 and ARS ≥ 60 — the organisation can proceed to a documentation review audit
- **Stage 1 Not Ready:** Documentation Completeness < 70 — at least one core document is absent; Stage 1 will fail
- **Stage 2 Ready:** ARS ≥ 75 and Control Operationalization ≥ 70 and 0 Critical gaps open
- **Stage 2 Not Ready:** ARS < 75 or Critical gaps open

**Estimated time to Stage 1:** Based on the gap between current Documentation Completeness score and 70, and the estimated effort in the Remediation Roadmap, state the number of months before the organisation could reasonably schedule a Stage 1 audit.

### 10. Overall Maturity Score

The definitive quantitative verdict on the organisation's ISO 42001 readiness.

**AMS Calculation:**

```
AMS = (0.60 × Clause_Score) + (0.40 × Annex_A_Score)

Clause_Score = (average maturity across Clauses 4–10, each rated 0–5) × 20
              = ([Cl.4 + Cl.5 + Cl.6 + Cl.7 + Cl.8 + Cl.9 + Cl.10] / 7) × 20

Annex_A_Score = (Implemented + [Partially Implemented × 0.5]) / Total Applicable × 100
```

Show the arithmetic explicitly: per-clause ratings, clause average, Annex A counts, and final AMS.

**ARS Calculation:**

```
ARS = (Documentation_Completeness × 0.30)
    + (Evidence_Availability × 0.40)
    + (Control_Operationalization × 0.20)
    + (Management_Review_Readiness × 0.10)
```

Show each component score and the weighted result.

**Certification Classification:**

| Classification | AMS | ARS | Critical Gaps | Meaning |
|---|---|---|---|---|
| **Certification Ready** | ≥ 80 | ≥ 75 | 0 | AIMS is mature and auditable. Proceed to select a certification body and schedule Stage 1. |
| **Near Ready** | 60–79 | 60–74 | 0–2 | Core AIMS exists with documented gaps. 3–9 months of targeted remediation before Stage 1. |
| **Significant Gaps** | 40–59 | Any | 3–5 | Foundational elements present but major gaps across Clause 8 or Annex A. 12–18 months to certification. |
| **Major Gaps** | < 40 | Any | 6+ | Fundamental AIMS elements absent. 18–36 months to certification; begin with AI policy and scope. |

**Months to Readiness estimate:** Based on the Priority 1 gap closure effort in the Remediation Roadmap and the current Certification Classification, state the estimated calendar months until the organisation could schedule a Stage 1 audit.

---

## AMS and ARS — Two Scoring Constructs

Understanding the distinction is essential for applying this skill correctly and for communicating results to clients.

**AMS (AIMS Maturity Score):** Measures the completeness and depth of the AI Management System itself. A high AMS means the AIMS covers all clauses and most Annex A controls at a defined or managed level. AMS answers: "Does the organisation have an AIMS?"

**ARS (Audit Readiness Score):** Measures the organisation's ability to demonstrate its AIMS to an external auditor. A high ARS means documents exist, evidence is retrievable, controls are operating, and management is engaged. ARS answers: "Can the organisation prove it has an AIMS?"

**The critical relationship:** A high AMS with a low ARS indicates a paper AIMS — requirements are defined and controls are specified but operating evidence does not exist. An auditor will fail this AIMS at Stage 2 regardless of AMS. A low AMS with a high ARS is unusual but possible — it indicates an organisation with strong audit culture but immature AI governance content. Both conditions prevent Certification Ready classification.

**Why Certification Ready requires both AMS ≥ 80 AND ARS ≥ 75:** ISO 42001 certification requires both a conforming AIMS (content) and demonstrated operation (evidence). The certification body auditor examines both. A score of AMS 82, ARS 60 means the AIMS is substantively sound but the auditor cannot verify it from available evidence — Stage 2 will produce nonconformities on evidence even if Stage 1 passes.

---

## Constraints and Scope

**In scope:**
- Organisations deploying, developing, or using AI systems in production
- All seven operative ISO 42001 clauses (Clauses 4–10) and all 38 Annex A controls
- Multi-jurisdiction engagements — the assessment calibrates regulatory overlay per jurisdiction but the core clause assessment is framework-consistent
- Organisations at any starting maturity level, including those with no existing AIMS
- Organisations extending an existing ISO 27001 ISMS to an AIMS (Annex SL credit assessment)

**Out of scope:**
- Compliance assessment against NIST AI RMF, OWASP LLM Top 10, EU AI Act, or sector-specific regulations as primary outputs — those are produced by Regulatory Mapping
- ISO 27001 gap assessments — this skill assumes information security is addressed through existing channels
- Technical implementation of controls — that is Governance Control Mapping
- Commercial proposal development — that is Ethana Solution Mapping and Ethana Proposal Review
- Legal advice — this skill produces governance intelligence, not legal opinions

**Ethana capability constraints:**
When Section 8 references an Ethana capability, it must be sourced from `knowledge/ethana/canonical-product-model.md`. The framework-crosswalk.md file (`knowledge/ethana/framework-crosswalk.md`) is the starting point for identifying which Ethana capabilities map to which ISO 42001 requirements, but the canonical product model is the authority for whether those capabilities are Production. Do not cite In Build or Aspirational capabilities as closing gaps in the current assessment period. Cite them as roadmap items only.

**ISO 27001 credit rule:**
Organisations with ISO 27001 certification may receive partial credit on Clauses 4, 5, 6, and 7 where their existing ISMS scope overlaps with the AIMS scope. This credit must be documented with the ISO 27001 certificate scope and expiry date. Credit applies to shared Annex SL infrastructure only — AI-specific requirements within those clauses (e.g., AI-specific risk criteria in Clause 6, AI-specific roles in Clause 5) still require assessment.

**Depth calibration:**
- Single-clause spot-check (e.g., "Is our Clause 8 practice mature?") → Sections 2 (restricted to the clause), 4, 10 — 30–45 minutes
- Full assessment, established organisation with existing documentation → all ten sections — 90–120 minutes
- Full assessment, greenfield with no AIMS and complex AI portfolio → all ten sections at maximum depth — 3–4 hours

---

## Knowledge Dependencies

### Tier 1 — PRIMARY (mandatory for every invocation)

- `knowledge/frameworks/iso-42001.md` — the primary knowledge source for all clause requirements, Annex A controls, certification pathway, and framework relationship context.
- `knowledge/ethana/canonical-product-model.md` — the sole permitted source for Ethana capability status determinations in Section 8 and Section 8.5. No other Ethana file may override it for Production status claims.
- `docs/decisions/ADR-002-claims-firewall.md` — the policy authority governing what Ethana claims are permitted; enforced in Section 8.5.

### Tier 2 — UPSTREAM SKILL OUTPUTS (strongly recommended as inputs)

- `skills/regulatory-mapping/` Section 2 and Section 6 — identifies which ISO 42001 clauses and controls are implicated by the organisation's regulatory context; pre-populates Phase 2 clause assessment
- `skills/governance-control-mapping/` Section 3 and Section 10 — identifies controls already designed; prevents duplication in the Gap Register

### Tier 3 — CONTEXTUAL REFERENCES (when relevant)

- `knowledge/ethana/framework-crosswalk.md` — ISO 42001 section provides the starting mapping from ISO 42001 clauses and Annex A categories to Ethana capabilities and Cursory services. Use as a starting point; validate against Tier 1 canonical model before including in Section 8.
- `knowledge/frameworks/nist-ai-rmf.md` — for organisations seeking dual-framework alignment (ISO 42001 + NIST AI RMF); the framework relationship section in iso-42001.md documents the mapping
- `knowledge/bfsi/banking-ai-governance-use-cases.md` — for BFSI engagements requiring SR 11-7 / PRA SS1/23 overlay on Annex A Category 3 (AI Lifecycle) and Category 9 (Monitoring)

### Tier 4 — PROHIBITED SOURCES (must not be used as authority for Ethana capability status)

- `knowledge/ethana/capability-status.md` — deprecated historical artifact; archived
- `knowledge/ethana/source-of-truth.md` — deprecated; archived
- `knowledge/ethana/ethana-status-reconciliation.md` — deprecated; explicitly rejected; archived
- Any marketing document, press release, or verbal claim about Ethana capabilities — not an authority for status determinations

---

## Related Skills

- `skills/regulatory-mapping/` — the upstream skill that identifies ISO 42001 as applicable and maps clauses to the organisation's AI systems. Run this first.
- `skills/governance-control-mapping/` — the downstream skill that translates the Gap Register from this assessment into implementation-ready control specifications. The Gap Register (Section 4) is the primary input.
- `skills/ethana-capability-validation/` — for formal validation of specific Ethana capability claims before they are cited in Section 8. Run this when an Ethana capability's status is uncertain.
- `skills/ethana-solution-mapping/` — for translating the Ethana Coverage Analysis (Section 8) into a commercial proposal capability map. The ISO 42001 gap context directly shapes which Ethana capabilities to highlight.
- `skills/ethana-proposal-review/` — the terminal gate before any ISO 42001 assessment containing Ethana capability references is released to a client. Section 8 of this assessment is within scope of the Proposal Review if the assessment is a client-facing document.
