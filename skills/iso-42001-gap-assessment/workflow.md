# ISO 42001 Gap Assessment — Workflow

## Overview

This workflow defines the step-by-step process for executing the ISO 42001 Gap Assessment skill. It assesses an organisation's AI Management System against ISO/IEC 42001:2023, producing a clause-by-clause conformity assessment, a consolidated gap register, risk prioritisation, evidence requirements, an Ethana platform coverage analysis, and two composite scores — AMS and ARS — that determine the Certification Classification.

The workflow has seven phases. Each phase has defined inputs, procedures, outputs, and quality gates. A full assessment of an established organisation with existing documentation typically takes 90–120 minutes. A greenfield assessment with no existing AIMS documentation may take 3–4 hours.

The Claims Firewall Review (Section 8.5) must be completed in Phase 6 before Section 8 is finalised. Do not release any assessment containing Ethana capability references without completing Section 8.5.

---

## Phase 1 — Intake & Scope Definition

**Objective:** Establish the AIMS scope, confirm input completeness, and calibrate the assessment depth before substantive clause review begins.

### Step 1.1 — Validate Inputs

Review all provided inputs against the Input Specification:
- Confirm `organisation_description`, `ai_portfolio`, and `jurisdictions` are present
- Check whether `regulatory_mapping_output` is available — if yes, load Section 2 (Applicable Governance Frameworks) for clause pre-population and Section 6 (Control Requirements) for Annex A category mapping
- Check whether `control_mapping_output` is available — if yes, load Section 3 (Control Coverage Classification) to identify controls already designed
- Check whether `existing_documentation` has been provided — note any ISO 27001 certificate, SOC 2 report, or prior gap assessment

### Step 1.2 — Define the AIMS Scope

Determine the boundary of the AI Management System that will be assessed. The scope must specify:
- Which organisational units are included
- Which AI systems from `ai_portfolio` are in scope (note any systems explicitly excluded and why)
- Geographic scope (which jurisdictions' AI operations are included)
- Whether the scope covers the organisation as an AI provider, AI deployer, or both

If `regulatory_mapping_output` is available, cross-reference its scope definition with the `ai_portfolio` to confirm alignment. If no regulatory mapping has been run, the scope is defined from `organisation_description` alone.

**Clause 4 dependency:** The AIMS scope is the first requirement of Clause 4. If the organisation has never formally defined an AIMS scope, GAP-CL4-001 (Critical) is raised immediately.

### Step 1.3 — Assess Input Completeness

Rate the input quality for this assessment:

| Rating | Condition | Effect on assessment quality |
|---|---|---|
| Full | All six inputs present (organisation description, AI portfolio, jurisdictions, regulatory mapping, control mapping, existing documentation) | AMS and ARS can be computed with full accuracy. ISO 27001 credit can be applied. |
| Standard | Organisation description + AI portfolio + jurisdictions present; regulatory mapping available; control mapping or existing documentation absent | Annex A assessment proceeds from first principles for controls not covered by control mapping. Some ARS components may be estimated. |
| Minimal | Organisation description + AI portfolio + jurisdictions only; no upstream outputs; no existing documentation | Assessment is based on interview-style evidence from the organisation description alone. ARS Evidence Availability component capped at ~40 without documentation. |

Record the input completeness rating. It will be stated in Section 1 (Executive Summary) and Section 10.

### Step 1.4 — Apply Jurisdiction Overlays

For each jurisdiction identified:
- **EU:** EU AI Act high-risk classification triggers urgency on Clause 6 (planning/risk assessment), Clause 8 (AI lifecycle management), and Annex A Categories 2 (risk assessment) and 3 (lifecycle). Note which AI systems in the portfolio may be classified as high-risk under Annex III.
- **UK:** FCA/PRA model risk framework (SR 11-7, PRA SS1/23) triggers overlay on Annex A Category 3 (AI Lifecycle) and Category 9 (Monitoring) for BFSI-sector organisations. Note which AI systems qualify as models under the supervisory definition.
- **India:** RBI MRM guidance and DPDP Act overlay Annex A Categories 2 (bias/data quality) and 4 (data governance). Note DPDP Act significant data fiduciary implications.

Record jurisdiction overlays. They shape severity calibration in Phase 4 (GAP severity ratings) and the BFSI commentary in Section 9.

### Phase 1 Output
- Defined AIMS scope (or GAP-CL4-001 raised if undefined)
- Input completeness rating (Full / Standard / Minimal)
- Jurisdiction overlay notes
- Confirmed list of AI systems in scope
- Go / stop decision

---

## Phase 2 — Clause Gap Assessment (Clauses 4–10)

**Objective:** Assess the organisation's current practices against each of the seven operative ISO 42001 clauses and assign a maturity rating.

### Step 2.1 — Assess Each Clause Systematically

Work through Clauses 4 through 10 in order. For each clause:

1. Review the clause's key requirements (from `knowledge/frameworks/iso-42001.md` and from SKILL.md Section 2 Clause-specific key requirements)
2. Determine the current state from available inputs: organisation description, existing documentation, regulatory mapping output
3. Assign a maturity rating (0–5) with justification
4. Identify gaps — requirements that are absent, partially met, or inconsistently applied

**Phase 2 calibration guidance:**

- **Clause 4 (Context):** The most foundational clause. If AIMS scope is undefined → maturity 0. If scope is informal but understood → maturity 1. If scope is documented and approved → maturity 3+.
- **Clause 5 (Leadership):** Assess whether AI governance is an executive-level responsibility or delegated entirely to a technical team. AI policy signed by C-suite → evidence of maturity 3. No AI policy → maturity 0.
- **Clause 6 (Planning):** Focus on AI risk assessment methodology. The key question is whether the organisation has a documented process for assessing AI-specific risks — not just IT risks — before deploying AI systems.
- **Clause 7 (Support):** Look for AI governance resources, competence programmes, and documentation control. ISO 27001 organisations typically have mature Clause 7 infrastructure from their ISMS — apply credit where scope overlaps.
- **Clause 8 (Operation):** The most complex clause. Assess all six Annex A Category 3 (AI Lifecycle) controls here — design requirements, training data, testing, deployment, change management, retirement. This is where the largest gaps typically appear for organisations new to ISO 42001.
- **Clause 9 (Performance Evaluation):** Assess monitoring, internal audit, and management review. Ethana's Immutable Audit Log [P] provides operating evidence for this clause — note where it contributes but be precise: it provides audit evidence, not the audit programme itself.
- **Clause 10 (Improvement):** Assess whether the organisation has a corrective action process for AI governance nonconformities and a continual improvement cycle. Often the most underdeveloped clause in first assessments.

### Step 2.2 — Apply ISO 27001 Credit

If the organisation holds a current ISO 27001 certificate and its scope overlaps with the AIMS scope:
- Clauses 4, 5, 6, 7: Apply partial credit where Annex SL requirements are shared. Document which ISO 27001 requirements satisfy which ISO 42001 requirements.
- Record the ISO 27001 certificate scope, scope overlap determination, and the credit applied per clause.
- Do not apply credit for AI-specific requirements within those clauses — Clause 6 AI risk assessment methodology and Clause 5 AI-specific roles are not covered by ISO 27001.

### Step 2.3 — Record Clause Gaps

For each gap identified within a clause, record a provisional gap entry (to be formalised in Phase 4):
- Clause reference
- Gap description (what is missing or inadequate)
- Provisional severity (Critical / Major / Minor)
- Evidence basis for the gap determination

### Phase 2 Output
- Clause Coverage Matrix (Section 2) — all seven clauses rated 0–5 with justification
- Provisional gap list from clause assessment
- ISO 27001 credit record (if applicable)

---

## Phase 3 — Annex A Control Assessment

**Objective:** Assess the organisation's current control posture against all 38 Annex A controls across 9 categories.

### Step 3.1 — Assess All 9 Categories

Work through each Annex A control category in order. For each control:
1. Determine applicability to the organisation's AI portfolio — if a control is not applicable (e.g., training data management for an organisation that only deploys third-party AI models), mark N/A with rationale; do not omit
2. Assess status: Implemented / Partially Implemented / Not Implemented / N/A
3. If implemented or partially implemented: identify the evidence basis
4. If not implemented: note the gap

**Category-by-category calibration guidance:**

**Category 1 — AI Policy and Governance:** The AI policy is the anchor for this category. Its existence and approval level determines whether the remaining governance controls have a foundation. No AI policy → Category 1 controls cannot be Implemented regardless of other activity.

**Category 2 — AI Risk Assessment and Impact:** Focus on whether an AI impact assessment has been completed for each AI system in scope. Many organisations have generic IT risk processes but lack AI-specific impact methodology. The data quality assessment control is frequently Not Implemented even in data-mature organisations.

**Category 3 — AI System Lifecycle:** This is where the gap density is highest for organisations new to AI governance. Assess each of the 6 controls independently. Deployment controls and change management controls are typically missing even in organisations with mature SDLC processes — because those processes were designed for software, not for AI models with retraining and drift considerations.

**Category 4 — Data Governance:** Distinguish between general data protection controls (which the organisation may have from GDPR compliance) and AI-specific data governance (data provenance for training data, data quality for inference inputs). The former does not satisfy the latter.

**Category 5 — Supply Chain:** For organisations that deploy third-party AI systems (including LLM APIs), assess whether they have conducted formal assessments of those providers against defined criteria. Most organisations have vendor security assessments but not AI-specific governance assessments.

**Category 6 — Human Oversight:** This category is consistently underdeveloped. Many organisations have human-in-the-loop processes informally but lack documented override mechanisms and defined escalation paths. The operator explainability control is frequently Not Implemented for ML models deployed before AI governance programmes were established.

**Category 7 — Incident Management:** Cross-reference with any `ai-incident-analysis` outputs provided. Assess whether the organisation's existing incident response process covers AI-specific incident types (bias events, unexpected model behaviour, adversarial attacks). Generic IT incident processes typically do not.

**Category 8 — Transparency and Explainability:** Assess disclosure and explainability documentation. EU AI Act requirements sharply increase the priority of this category for EU-jurisdiction organisations — Article 13 transparency requirements overlap directly.

**Category 9 — Monitoring and Performance:** If Regulatory Mapping was provided, cross-reference Section 6 for monitoring obligations. Ethana's Immutable Audit Log [P] provides audit evidence for this category — record the mapping but note that the Audit Log provides evidence collection (one control), not the monitoring programme itself.

### Step 3.2 — Record Annex A Control Gaps

For each control that is Partially Implemented or Not Implemented, record a provisional gap entry.

### Step 3.3 — Compute Annex A Coverage Counts

Tally:
- Implemented controls: [n]
- Partially Implemented controls: [p]
- Not Implemented controls: [u]
- N/A controls: [a]
- Total applicable controls: [n + p + u] (excludes N/A)

Annex A Score (for AMS) = (n + p × 0.5) / (n + p + u) × 100

### Phase 3 Output
- Annex A Control Assessment (Section 3) — all 38 controls assessed
- Annex A coverage counts (for AMS calculation)
- Provisional gap list from Annex A assessment

---

## Phase 4 — Gap Register Construction

**Objective:** Consolidate all provisional gaps from Phases 2 and 3 into a complete, formally identified Gap Register.

### Step 4.1 — Assign Gap IDs

For each provisional gap identified in Phases 2 and 3:
- Assign a unique Gap ID using the scheme: `GAP-[CL{number} or AA{category number}]-[sequential three-digit number]`
- Clause 4 gaps: GAP-CL4-001, GAP-CL4-002
- Clause 8 gaps: GAP-CL8-001, GAP-CL8-002
- Annex A Category 3 gaps: GAP-AA3-001, GAP-AA3-002
- Annex A Category 9 gaps: GAP-AA9-001

Number sequentially within each clause/category; do not leave gaps in the sequence.

### Step 4.2 — Finalise Severity Ratings

Apply severity definitions from SKILL.md Section 4, adjusted for jurisdiction overlays from Phase 1:
- EU AI Act high-risk classification → Clause 6, Clause 8, and Annex A Categories 2, 3 gaps are automatically elevated one severity level if the organisation has high-risk AI systems in scope
- BFSI with India jurisdiction → Annex A Category 3 (lifecycle) and Category 9 (monitoring) gaps are elevated one severity level per RBI MRM guidance
- UK BFSI → Annex A Category 3 gaps covering validation and change management are elevated per PRA SS1/23 model risk requirements

### Step 4.3 — Estimate Remediation Effort

For each gap, estimate the remediation effort in person-weeks assuming Cursory advisory support. Use these benchmarks:
- Policy or procedure document creation (no implementation required): 1–2 weeks
- Process design and documentation (new process, no tooling): 2–4 weeks
- Process design + control implementation (tooling or platform configuration required): 4–8 weeks
- Programme design (multiple interdependent controls across the AI portfolio): 8–16 weeks

Effort estimates are indicative. They assume Cursory advisory support and a cooperative client. Double estimates for organisations with complex procurement and approval processes.

### Step 4.4 — Complete the Gap Register

Produce the full Gap Register (Section 4) with all fields populated: Gap ID, clause/control reference, description, severity, effort, and proposed owner.

### Phase 4 Output
- Gap Register (Section 4) — all gaps identified, IDed, and severity-rated
- Total gap counts by severity (Critical / Major / Minor)

---

## Phase 5 — Risk Prioritisation & Evidence Mapping

**Objective:** Organise gaps by remediation priority and specify the evidence required to close each gap at audit.

### Step 5.1 — Build the Risk Matrix

Apply the two-axis risk matrix from SKILL.md Section 5:
- Axis 1: Certification blocker (would this gap cause a Stage 1 or Stage 2 audit failure?)
- Axis 2: Business risk (what is the operational consequence of this gap if left open?)

Assign Priority ranks P1 through P5 to every gap. Ensure all Critical-severity gaps are P1 or P2.

### Step 5.2 — Specify Evidence Requirements

For each gap, determine what evidence would satisfy a Stage 2 auditor that the gap has been closed. Apply these rules:
- Policy gaps require: signed policy document + evidence of communication (meeting minutes or distribution record)
- Process gaps require: process document + at least one record of the process being executed (completed form, log entry, meeting minutes)
- Control gaps require: control specification + evidence of operation (test results, audit log entries, monitoring outputs)
- Management review gaps require: meeting minutes with attendance and agenda items covering the AIMS

Record the Evidence Availability status for each gap: Evidence exists / Partially available / Not available. This feeds the ARS Evidence Availability component.

### Step 5.3 — Note Ethana Evidence Sources

Where Ethana Production capabilities provide audit evidence relevant to gap closure, note them here:
- Immutable Audit Log [P] → provides evidence for Clause 9 monitoring, Annex A Category 9 controls
- Red Teaming Orchestrator [P] → provides evidence for Annex A Category 3 (testing/validation) and Category 7 (incident management)
- Runtime Guardrails [P] → provides evidence for Annex A Category 3 (deployment controls) and Category 6 (human oversight support)

These references are flagged for Claims Firewall Review in Phase 6.

### Phase 5 Output
- Risk Prioritisation (Section 5) — all gaps ranked P1–P5
- Evidence Requirements (Section 6) — per-gap evidence specification and availability status
- ARS Evidence Availability component score (preliminary, to be confirmed in Phase 7)

---

## Phase 6 — Ethana Coverage Analysis & Claims Firewall Review

**Objective:** Map ISO 42001 gaps to Ethana platform capabilities and Cursory services. Execute the Claims Firewall Review to validate all capability references before the section is finalised.

### Step 6.1 — Initial Capability Mapping

Using `knowledge/ethana/framework-crosswalk.md` (ISO 42001 section) as a starting reference, identify which Ethana capabilities map to the gaps in the Gap Register:

| Gap ID | Gap description | Ethana capability indicated in crosswalk | Coverage type | Cursory service alternative |
|---|---|---|---|---|
| GAP-CL9-001 | No audit evidence collection process | Immutable Audit Log | Partial | Regulatory Gap Analysis service |
| GAP-AA3-002 | No pre-deployment testing process | Red Teaming Orchestrator | Partial | Red Teaming as a Service |

Record each capability as it appears in the crosswalk. Do not yet confirm status — that is Step 6.2.

### Step 6.2 — Claims Firewall Review (Section 8.5)

**This step is mandatory before Section 8 can be finalised.**

Open `knowledge/ethana/canonical-product-model.md` directly. For every Ethana capability identified in Step 6.1:

1. Locate the capability in the canonical model
2. Read its canonical status: Production / In Build / Aspirational / Not Found
3. Apply the Claims Firewall:

**Production [P] → Valid Reference:**
The capability may be cited in Section 8 as closing or partially closing the gap today. Record the verbatim canonical model entry. If the capability carries mandatory caveats (e.g., Bias Scanner runtime-filter caveat; on-premises scale caveat), record the caveats and confirm they appear inline in Section 8 alongside the capability reference.

**In Build [IB] → Invalid as Production Reference:**
The capability may not be cited as closing a gap in the current period. Record as Invalid Reference in Section 8.5. Correct the Section 8 entry: reclassify as "roadmap item — not available in current assessment period" and substitute the Cursory service alternative where available.

**Aspirational → Invalid Reference:**
The capability does not exist at any engineering status level. Remove from Section 8 entirely. Record in Section 8.5 Invalid References. Do not substitute aspirational capabilities with roadmap language — the status is Aspirational, not In Build.

**Not Found → Invalid Reference:**
Any capability cited in Section 8 that does not appear in canonical-product-model.md is an invalid reference. Record in Section 8.5 Invalid References with "Not found in canonical model."

Any invalid reference found in Section 8.5 becomes HD2 — do not release the assessment until all invalid references are corrected.

### Step 6.3 — Map Remaining Gaps to Cursory Services and Third Parties

For gaps not addressed by Production Ethana capabilities:
- **Cursory Service:** Which Cursory advisory service addresses this gap (e.g., AI Policy Design service, Regulatory Gap Analysis service, AI Impact Assessment service, Red Teaming as a Service)
- **Third Party Required:** Which third-party capability is needed and why (e.g., accredited certification body for Stage 2 audit; specialist statistical bias auditor for Annex A Category 2 bias controls; formal model validation firm for quantitative model testing in BFSI)
- **Unaddressed:** Gaps that neither Ethana, Cursory services, nor identified third parties currently close (flag for further advisory scoping)

### Step 6.4 — Finalise Section 8

Produce the complete Ethana Coverage Analysis (Section 8) with Section 8.5 Claims Firewall Review embedded. Confirm that:
- All Valid References have verbatim canonical model quotes
- All Invalid References have been corrected in the body of Section 8
- All Required Caveats appear inline alongside the capability reference
- Third-Party Alternatives are specified for all uncovered gaps

### Phase 6 Output
- Section 8 (Ethana Coverage Analysis) — complete
- Section 8.5 (Claims Firewall Review) — complete with Valid/Invalid/Caveat/Third-Party tables
- Claims Firewall violation count (0 for a clean assessment)

---

## Phase 7 — Maturity Scoring, Remediation Roadmap & Audit Readiness

**Objective:** Compute AMS and ARS, produce the phased Remediation Roadmap, complete the Audit Readiness Assessment, and issue the final Certification Classification.

### Step 7.1 — Compute AMS

Gather the per-clause maturity ratings from Phase 2 and the Annex A coverage counts from Phase 3.

```
Clause_Score = ([Cl.4 rating] + [Cl.5 rating] + [Cl.6 rating] + [Cl.7 rating]
               + [Cl.8 rating] + [Cl.9 rating] + [Cl.10 rating]) / 7 × 20

Annex_A_Score = ([Implemented count] + [Partially Implemented count × 0.5])
                / [Total applicable count] × 100

AMS = (Clause_Score × 0.60) + (Annex_A_Score × 0.40)
```

Show arithmetic explicitly. Round to one decimal place.

### Step 7.2 — Compute ARS

Score each of the four ARS components on a 0–100 scale using evidence from the assessment:

**Documentation Completeness (weight 30%):**
Score based on which required documents exist and are version-controlled. Key documents: AI policy, AIMS scope document, AI risk assessment, AI impact assessments per system in scope, Annex A statement of applicability, internal audit plan.
- 90–100: All present, current, approved, version-controlled
- 70–89: Core documents present; supplementary documents partial
- 40–69: Policy present; major gaps in risk assessment or impact assessments
- 0–39: AI policy or AIMS scope absent

**Evidence Availability (weight 40%):**
Based on the evidence availability status recorded in Section 6 (Evidence Requirements). Tally: evidence exists / partially available / not available for each gap's evidence requirement. Score proportionally.

**Control Operationalization (weight 20%):**
Based on the Implemented vs Partially Implemented vs Not Implemented counts from Phase 3. A control that is Implemented provides operating evidence; Partially Implemented provides partial evidence; Not Implemented provides none.
- Score = Implemented / Total applicable × 100 (as a rough guide; adjust down for controls where Partial is very partial)

**Management Review Readiness (weight 10%):**
Based on evidence of management engagement from `organisation_description` and `existing_documentation`. Look for: board-level AI agenda items, AI governance committee charter, management review minutes, AI objectives set by leadership.

```
ARS = (Documentation_Completeness × 0.30)
    + (Evidence_Availability × 0.40)
    + (Control_Operationalization × 0.20)
    + (Management_Review_Readiness × 0.10)
```

Show each component score and the weighted result.

### Step 7.3 — Produce the Remediation Roadmap

Organise all P1–P5 gaps from Phase 5 into the phased roadmap (Section 7):

- **30-day sprint:** All Critical (P1) gaps — scope definition, AI policy, top management sign-off
- **60-day sprint:** P2 gaps — foundational documentation; reach maturity 2 across all clauses
- **90-day sprint:** P3 gaps — reach maturity 3 on key clauses; begin accumulating operating evidence
- **180-day programme:** P4 and P5 gaps — maturity 4 on Clauses 8 and 9; all Minor gaps closed before Stage 2

For each action: state the gap ID it closes, the deliverable, the responsible role, and any dependencies. Identify the critical path — the sequence of actions that determines the minimum time to Stage 1 readiness.

### Step 7.4 — Complete the Audit Readiness Assessment

Produce the full Audit Readiness Assessment (Section 9):
- Stage 1 readiness verdict with justification
- Stage 2 readiness verdict with justification
- Estimated months to Stage 1 readiness based on critical path in the Remediation Roadmap
- Key actions required before scheduling Stage 1

### Step 7.5 — Determine the Certification Classification

Apply the classification table from SKILL.md Section 10:

| AMS | ARS | Critical Gaps | Classification |
|---|---|---|---|
| ≥ 80 | ≥ 75 | 0 | Certification Ready |
| 60–79 or (≥80 with ARS 60–74) | 60–74 | 0–2 | Near Ready |
| 40–59 | Any | 3–5 | Significant Gaps |
| < 40 | Any | 6+ | Major Gaps |

If any Critical gap is open, the classification cannot be Certification Ready regardless of AMS or ARS. This is enforced by HD6.

Produce Section 10 with the complete AMS and ARS arithmetic, the classification table row that applies, and the months-to-readiness estimate.

### Step 7.6 — Write the Executive Summary

Write Section 1 (Executive Summary) last. It must accurately reflect all findings in Sections 2–10. It must state:
- AMS and ARS scores
- Certification Classification
- Total gap count by severity
- The single highest-priority action
- Months to Stage 1 readiness (if target is third-party certification)

### Phase 7 Output
- Section 7 (Remediation Roadmap) — phased plan for all gaps
- Section 9 (Audit Readiness Assessment) — ARS calculation + Stage 1/2 verdicts
- Section 10 (Overall Maturity Score) — AMS + ARS + Certification Classification
- Section 1 (Executive Summary) — written last, reflects all findings

---

## Output Document Structure

```markdown
# ISO 42001 Gap Assessment: [Organisation Name] — [Date]

**Assessment Date:** [Date]
**AIMS Scope:** [Scope statement]
**AI Systems Assessed:** [Count and names]
**Jurisdictions:** [List]
**Input Completeness:** [Full / Standard / Minimal]
**Target Outcome:** [Third-party certification / Self-declaration / Internal audit]

---

## 1. Executive Summary
[200–250 words]

## 2. Clause Coverage Matrix
[Table: Clause | Name | Key requirements | Current state | Evidence basis | Maturity rating | Gap severity]

## 3. Annex A Control Assessment
### Category 1 — AI Policy and Governance
[Per-control table: Control | Status | Evidence basis | Gap description]
### Category 2 — AI Risk Assessment and Impact
[...]
[Through Category 9 — Monitoring and Performance]

## 4. Gap Register
[Table: Gap ID | Clause/Control ref | Description | Severity | Effort | Owner]

## 5. Risk Prioritisation
[Table: Gap ID | Severity | Certification blocker | Business risk | Priority rank]

## 6. Evidence Requirements
[Per-gap: Gap ID | Evidence type | Description | Source system | Retention | Readiness status]

## 7. Remediation Roadmap
### 30-Day Sprint
[P1 actions]
### 60-Day Sprint
[P2 actions]
### 90-Day Sprint
[P3 actions]
### 180-Day Programme
[P4-P5 actions]

## 8. Ethana Coverage Analysis
[Table: Gap ID | Ethana capability | Coverage type | Canonical status | Cursory service | Third party]

### 8.5 Claims Firewall Review
#### Valid References
[Capability | Canonical model entry | Caveats applied]
#### Invalid References
[Capability | How cited | Canonical status | Required correction]
#### Required Caveats
[Capability | Caveat text | Confirmed in Section 8]
#### Third-Party Alternatives
[Gap ID | Third-party capability | Rationale]

## 9. Audit Readiness Assessment
### ARS Calculation
Documentation Completeness: [score] × 0.30 = [weighted]
Evidence Availability: [score] × 0.40 = [weighted]
Control Operationalization: [score] × 0.20 = [weighted]
Management Review Readiness: [score] × 0.10 = [weighted]
ARS: [total]
### Stage 1 Verdict
[Ready / Not Ready + rationale]
### Stage 2 Verdict
[Ready / Not Ready + rationale]
### Months to Stage 1 Readiness
[Estimate and basis]

## 10. Overall Maturity Score
### AMS Calculation
Clause ratings: Cl.4=[n] Cl.5=[n] Cl.6=[n] Cl.7=[n] Cl.8=[n] Cl.9=[n] Cl.10=[n]
Clause Score: ([sum] / 7) × 20 = [clause_score]
Annex A Score: ([implemented] + [partial × 0.5]) / [total applicable] × 100 = [aa_score]
AMS: ([clause_score] × 0.60) + ([aa_score] × 0.40) = [AMS]
### ARS
[Total from Section 9]
### Certification Classification
[Certification Ready / Near Ready / Significant Gaps / Major Gaps]
### Months to Readiness
[Estimate]
```

---

## Time Estimates

| Scenario | Input Completeness | Estimated Time |
|---|---|---|
| Full assessment, all upstream outputs available | Full | 90–120 minutes |
| Full assessment, regulatory mapping available, no control mapping | Standard | 75–95 minutes |
| Full assessment, no upstream skill outputs, no existing documentation | Minimal | 3–4 hours |
| Single-clause spot-check | Any | 30–45 minutes |
| ISO 27001 extension assessment (Clauses 4–7 credited, AI-specific gaps only) | Full | 60–75 minutes |
| Greenfield assessment, complex AI portfolio, multi-jurisdiction | Minimal | 4–6 hours |
| Re-assessment after remediation programme | Standard or Full | 45–60 minutes |

---

## Schema Integration

### Input Schema

Input payloads for this skill must conform to `workflows/schemas/iso-42001-gap-assessment-input.schema.json`. The three required fields are `organisation_description`, `ai_portfolio`, and `jurisdictions`. Validate before Phase 1:

```bash
python evaluations/scripts/workflow_validator.py path/to/input.json workflows/schemas/iso-42001-gap-assessment-input.schema.json
```

### Output Schema

Every completed assessment must serialize the Overall Maturity Score (Section 10) to a structured payload conforming to `workflows/schemas/iso-42001-gap-assessment-output.schema.json`. Required minimum fields:

```json
{
  "ams": 0,
  "ars": 0,
  "critical_gaps": 0,
  "major_gaps": 0,
  "minor_gaps": 0,
  "certification_classification": "Certification Ready|Near Ready|Significant Gaps|Major Gaps",
  "months_to_readiness": 0
}
```

Validate before routing to the Client Assessment Agent or any downstream governance workflow:

```bash
python evaluations/scripts/workflow_validator.py path/to/output.json workflows/schemas/iso-42001-gap-assessment-output.schema.json
```
