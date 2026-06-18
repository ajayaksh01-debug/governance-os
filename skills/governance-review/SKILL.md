# Skill: Governance Review

**Version:** 1.0
**Category:** Governance Intelligence
**Owner:** Cursory Governance Team

---

## Purpose

This skill synthesises the outputs of the Client Assessment chain into a terminal governance readiness verdict. Where upstream skills identify regulatory obligations (Regulatory Mapping), design control specifications (Governance Control Mapping), and assess AI management system maturity (ISO 42001 Gap Assessment), Governance Review evaluates whether those outputs — taken together — constitute a governance posture adequate for AI deployment in the client's context.

**The question it answers:** Is this organisation's AI governance framework sufficient for their deployment context, regulatory obligations, and AI risk profile?

The skill produces two composite scores and a Governance Readiness Classification:

- **Governance Assessment Score (GAS):** A 0–100 score measuring governance posture completeness across all assessed frameworks. Base 100, reduced by missing mandatory frameworks (−15 each), Major Governance Findings (−10 each), and Minor Governance Findings (−2 each). Any Critical Governance Gap sets GAS to 0.
- **Control Coverage Rate (CCR):** A 0–100 score measuring the percentage of mandatory regulatory controls that have been addressed. CCR = (Implemented + (Partially Implemented × 0.5)) / Total Mandatory Controls × 100.
- **Governance Readiness Classification:** Governance Ready / Conditional Governance / Not Governance Ready (Advisory Only classification is not supported per GR-001).

This skill is the terminal skill in the Client Assessment Agent chain. Its output is the Governance Readiness Certificate that the Client Assessment Agent packages and delivers as the final engagement deliverable. The Governance Readiness Certificate is the governance-chain equivalent of the Release Audit Certificate produced by Proposal Review in the commercial chain.

---

## When to Use This Skill

Use this skill when:
- The Client Assessment Agent has completed Regulatory Mapping, Governance Control Mapping, and ISO 42001 Gap Assessment for a client and requires a terminal governance readiness verdict
- A client requires a governance readiness verdict across multiple regulatory frameworks and a single synthesised certificate
- A governance programme completion review is needed — a formal determination of whether control design and gap closure work has reached a deployable state
- A re-assessment is required after remediation to verify that previous findings have been addressed

Do not use this skill for:
- Assessing Ethana capability claims in customer-facing commercial proposals (use `skills/ethana-proposal-review/`)
- Performing a regulatory mapping from scratch (use `skills/regulatory-mapping/`)
- Designing control specifications (use `skills/governance-control-mapping/`)
- Assessing ISO 42001 maturity in depth (use `skills/iso-42001-gap-assessment/`)
- Technical feature validation for POC scoping (use `skills/ethana-feature-mapping/`)

---

## Relationship to Client Assessment Chain

| | Regulatory Mapping | Governance Control Mapping | ISO 42001 Gap Assessment | Capability Validation | Governance Review |
|---|---|---|---|---|---|
| **Question** | What applies? | How to address it? | How mature is the AIMS? | What can Ethana do? | Is the posture sufficient? |
| **Input** | AI subject + context | Regulatory output | Organisation + AI portfolio | Capability questions | All upstream outputs |
| **Output** | Obligations + control requirements | Control specifications + evidence registry | AMS + ARS + gap register | ECS + CPL register | GAS + CCR + certificate |
| **Terminal?** | No | No | No | No | **Yes** |

Governance Review does not re-perform regulatory analysis, gap assessment, or control design. It synthesises upstream outputs. If an upstream skill made an error, it surfaces here as a finding — the fix is applied in the upstream skill and a re-assessment is run.

---

## Input Specification

### Required Inputs

Absence of any required input fails a mandatory GTG gate and produces `governance_gate_passed = false` with `classification = Not Governance Ready`.

| Field | Source skill | Key fields consumed | Gate dependency |
|---|---|---|---|
| `regulatory_mapping_output` | `skills/regulatory-mapping/` | `applicable_regulations` (regulatory scope, jurisdiction), `applicable_frameworks` (governance framework scope), `control_requirements` (CCR denominator — filtered by `mandatory: true`) | GTG-1 |
| `control_mapping_output` | `skills/governance-control-mapping/` | `control_taxonomy_matrix` (CCR numerator — `coverage_classification` per control), `evidence_registry` (GTG-6 traceability) | GTG-2, GTG-6 |
| `iso_42001_output` | `skills/iso-42001-gap-assessment/` | `ams`, `ars`, `critical_gaps` (integer), `certification_classification`, `critical_gap_ids` | GTG-3 |

**Field name precision required:**
- `critical_gaps` — integer field in `iso_42001_output`. Field name is `critical_gaps`, not `critical_gap_count`.
- `control_taxonomy_matrix` — array field in `control_mapping_output`. Field name is `control_taxonomy_matrix`, not `control_coverage_classification`.
- `mandatory` — boolean field per item in `control_requirements`. Controls where `mandatory: true` form the CCR denominator; controls where `mandatory: false` are excluded from CCR.

**`applicable_regulations` vs. `applicable_frameworks`:** Regulatory Mapping separates regulatory instruments (EU AI Act, FCA guidance → `applicable_regulations`) from governance frameworks (ISO 42001, NIST AI RMF, OWASP LLM Top 10 → `applicable_frameworks`). Section 6 (Framework Compliance Scores) draws from both arrays. GTG-7 requires at least one entry from either array to be assessed to completion.

### Strongly Recommended

| Field | Source skill | Key fields consumed | Impact if absent |
|---|---|---|---|
| `capability_validation_output` | `skills/ethana-capability-validation/` | `allowed_claims`, `prohibited_claims` | GTG-4 cannot pass; Section 8 (Capability Governance Alignment) cannot be completed |

### Contextual

| Field | Values | Effect on assessment |
|---|---|---|
| `client_profile.sector` | BFSI / Healthcare / Government / General Enterprise | BFSI triggers model risk overlay on control domain checks; Government triggers additional mandatory framework requirements |
| `client_profile.jurisdictions` | EU / UK / India / US / Other | Missing mandatory-jurisdiction framework assessment is a CGC candidate |
| `client_profile.ai_deployment_type` | High-Risk / Limited-Risk / Minimal-Risk | High-Risk: `iso_42001_output` absence is a Critical Governance Gap (CGC); Limited-Risk: framework adequacy checks apply |
| `client_profile.deployment_model` | Cloud / Customer VPC / On-prem / Air-gapped | Constrains which `coverage_classification` entries are technically realisable |

**Input completeness signal:**
- `Full` — all four inputs including `capability_validation_output`
- `Standard` — three required inputs, no `capability_validation_output`
- `Minimal` — required inputs present, `client_profile` absent (CGC threshold evaluation for jurisdiction-specific mandatory frameworks cannot be completed)

---

## Output Specification

Every execution produces ten sections. For an abbreviated re-assessment or spot-check, Sections 3, 6, 7, and 10 are the minimum. Full assessments require all ten sections.

### 1. Executive Governance Summary

A concise governance verdict written for a client governance team or Cursory engagement lead: classification, GAS, CCR, CGC count, the top three most significant findings, and the single most important next action.

- **Not Governance Ready:** State which CGC(s) or score/risk thresholds are blocking the classification and the required remediation sequence. No positive classification is possible until all CGCs are resolved, gate checks pass, and score/risk thresholds are met.
- **Conditional Governance:** State which MGF(s) must be addressed before deployment is permissible.
- **Governance Ready:** Confirm the readiness verdict. Note any time-bounded conditions (framework reassessment schedules, certification milestones).

### 2. Regulatory Scope and Framework Matrix

The regulatory and framework scope established for this assessment. Derived entirely from `regulatory_mapping_output.applicable_regulations` and `applicable_frameworks` — no new regulatory analysis is performed here.

- Jurisdictions confirmed in scope and their basis (from `regulation.jurisdiction` field values)
- Applicable regulations per jurisdiction with `status` field (Confirmed / Likely / Conditional, sourced from upstream)
- Applicable governance frameworks assessed (from `applicable_frameworks`) — mandatory vs. optional designation per `client_profile.jurisdictions`
- Frameworks and regulations identified but not assessed in this review — reason for exclusion

### 3. Control Coverage Assessment

The CCR calculation shown in full with explicit arithmetic.

```
CCR denominator:       count of control_requirements where mandatory = true

coverage_classification mapping:
  Implemented:         "Fully Covered by Ethana"
                       "Covered by Cursory Service"
                       "Customer-Owned Control"
  Partially Implemented: "Partially Covered by Ethana"
  Gap (not counted):   "Third-Party Control Required"
                       (no confirmed coverage — client must engage third party)

CCR numerator:         Implemented + (Partially Implemented × 0.5)
CCR:                   round(numerator / denominator × 100, 1)
```

Show the arithmetic explicitly: denominator, implemented count, partially implemented count, numerator, and result. For each mandatory control domain, state the domain-level implementation rate. Flag any domain where the rate is below 50% — this is a CGC candidate.

**Note on "Third-Party Control Required":** This `coverage_classification` value indicates the control design has identified a third-party dependency. It does not confirm the third party is in place. Until confirmation is obtained, these entries contribute 0 to the CCR numerator and represent residual coverage gaps.

### 4. Governance Gap Register

A consolidated gap register synthesised from `iso_42001_output.critical_gap_ids` and any additional gaps identified during CCR calculation.

For each gap:
- **Gap ID:** `GGP-[domain abbreviation]-[number]` — e.g., `GGP-IS-001` (ISO 42001 source), `GGP-CM-001` (control mapping source), `GGP-RM-001` (regulatory mapping source)
- **Description** — specific gap, not a generic category
- **Source** — which upstream skill identified this gap
- **Severity** — Critical / Major / Minor
- **Control domain affected**
- **Remediation category** — Policy / Process / Technical / Evidence

ISO 42001 `critical_gap_ids` entries map to Critical severity here. Evaluate each Critical severity gap against the CGC criteria in the Scoring Model section. A Critical severity gap is a CGC candidate; not all Critical gaps are automatically CGCs — apply the CGC criteria.

### 5. Governance Risk Register

Residual risks after the assessed control set is applied. For each risk:
- **Risk ID:** `GRK-[number]`
- **Description**, **Severity** (High / Medium / Low), **residual likelihood and impact after controls**, **owner** (client role), **status** (Accepted / Escalated / Residual)

Severity distribution: count of High / Medium / Low. More than 2 High residual risks prevents Governance Ready classification even when GAS and CCR thresholds are met — document these explicitly in Section 10.

### 6. Framework Compliance Scores

Per-entry compliance status for each regulatory instrument in `applicable_regulations` and each governance framework in `applicable_frameworks`.

For each entry:
- Name and version (regulation or framework)
- Per-domain compliance: Compliant / Partial / Non-Compliant / Not Assessed
- Dominant finding per non-compliant domain
- Overall compliance characterisation

**For ISO 42001:** Draw directly from `iso_42001_output.ams`, `ars`, and `ams_clause_scores`. Do not re-score. Any ISO 42001 score in Section 6 that differs from `iso_42001_output` values is a GHD6 violation.

An entry rated Not Assessed on all domains is not assessed to completion and does not satisfy GTG-7.

### 7. Governance TG Gate Table

```
| Gate  | Step                                | Status              |
|-------|-------------------------------------|---------------------|
| GTG-1 | Regulatory scope confirmed          | Pass / Fail         |
| GTG-2 | Control mapping present             | Pass / Fail         |
| GTG-3 | Gap assessment present              | Pass / Fail         |
| GTG-4 | Capability alignment confirmed      | Pass / Noted absent |
| GTG-5 | Risk register complete              | Pass / Noted absent |
| GTG-6 | Evidence traceability confirmed     | Pass / Noted absent |
| GTG-7 | Framework coverage confirmed        | Pass / Fail         |
```

**Mandatory pass gates: GTG-1, GTG-2, GTG-3, GTG-7.** Failure of any mandatory gate → `governance_gate_passed = false` → `classification = Not Governance Ready`.

Gate evaluation criteria:
- **GTG-1 Pass:** `regulatory_mapping_output` present; `applicable_regulations` non-empty; at least one jurisdiction status = Confirmed
- **GTG-2 Pass:** `control_mapping_output` present; `control_taxonomy_matrix` non-empty
- **GTG-3 Pass:** `iso_42001_output` present; `ams` and `critical_gaps` populated
- **GTG-4 Pass:** `capability_validation_output` present; at least one `allowed_claims` entry mapped to a control domain in Section 8
- **GTG-5 Pass:** Section 5 (Risk Register) populated; all CGC and MGF items have a corresponding risk entry with severity
- **GTG-6 Pass:** All Implemented controls in Section 3 cite a traceable `evidence_id` from `control_mapping_output.evidence_registry`
- **GTG-7 Pass:** Section 6 contains at least one entry from `applicable_regulations` or `applicable_frameworks` assessed to completion — all domains rated (at least one domain rated Compliant, Partial, or Non-Compliant; no entry with all domains rated Not Assessed)

GTG-4, GTG-5, and GTG-6 are advisory gates. Their absence is noted in the gate table but does not set `governance_gate_passed = false`.

### 8. Capability Governance Alignment

For each `allowed_claims` entry in `capability_validation_output`:
- Governance control domain(s) the capability addresses
- Mandatory controls from `control_requirements` the capability satisfies (fully or partially — informs `coverage_classification` in CCR)
- Control gaps where no validated Ethana capability provides coverage — these require Cursory advisory services or Customer-Owned implementations

If `capability_validation_output` absent: "GTG-4 not passed — Section 8 cannot be completed. Capability governance alignment is unknown. CCR ceiling is limited to control_taxonomy_matrix entries only."

### 9. Required Remediation Actions

Ordered list of actions required before re-assessment or deployment approval. CGC-addressing actions listed first; MGF actions second; advisory actions last.

For each action:
- **Action ID:** `GRA-[number]`
- **Description** — specific and executable
- **Addresses** — gap or risk ID(s) from Sections 4 or 5
- **Priority** — Immediate (blocks any positive classification) / Before Deployment / Before Certification
- **Responsible** — client role
- **Effort category** — Days / Weeks / Months

### 10. Governance Release Decision

The machine-readable governance verdict. All values must match the JSON payload exactly.

```
AIMS Maturity Score (AMS):          [iso_42001_output.ams] / 100
Audit Readiness Score (ARS):        [iso_42001_output.ars] / 100
ISO 42001 Classification:           [iso_42001_output.certification_classification]

CCR denominator:                    [mandatory control count]
  Implemented:                      [count]
  Partially Implemented:            [count] × 0.5 = [weighted]
  Third-Party Required (gap):       [count] — not counted
CCR numerator:                      [implemented + weighted]
Control Coverage Rate (CCR):        round([numerator] / [denominator] × 100, 1) = [ccr]

GAS base:                           100
  Missing mandatory frameworks:     [count] × −15 = −[total]
  Major Governance Findings:        [count] × −10 = −[total]
  Minor Governance Findings:        [count] × −2  = −[total]
  Critical Governance Gap present:  [Yes / No — if Yes: GAS = 0, absolute rule]
Final GAS:                          [gas] / 100

Critical Governance Gaps (CGC):     [count]
Major Governance Findings (MGF):    [count]
High Residual Risks:                [count]
governance_gate_passed:             [true / false]
Governance Readiness:               [classification]
```

---

## Scoring Model

### Governance Assessment Score (GAS)

```
GAS = 100
    − (15 × missing_mandatory_framework_count)
    − (10 × mgf_count)
    − (2  × minor_finding_count)

Any CGC present → GAS = 0  [absolute rule — cannot be overridden]
```

GAS is still computed and displayed in Section 10 even when the absolute rule applies. The arithmetic is shown for transparency; the final value is 0 when any CGC is present regardless of the arithmetic result.

**What constitutes a Critical Governance Gap (CGC):**
- No regulatory framework assessment for a jurisdiction where `applicable_regulations` confirms a mandatory AI compliance obligation (status = Confirmed)
- `iso_42001_output` absent when `client_profile.ai_deployment_type = "High-Risk"`
- Any mandatory control domain where the implementation rate is below 50% (fewer than half of mandatory controls in that domain have any level of coverage)
- Material mismatch between declared `ai_deployment_type` and the AI systems in scope — e.g., a system making automated credit or benefits decisions declared as Minimal-Risk

**Major Governance Finding (MGF) Categories (per GR-001 calibration):**
- **Scope Major Governance Finding (S-MGF):** A regulatory instrument in `applicable_regulations` or framework in `applicable_frameworks` that is mandatory for the client's jurisdiction has no Section 6 entry at all (not assessed).
- **Control Coverage Major Governance Finding (CC-MGF):**
  - A mandatory control from `control_requirements` (where `mandatory: true`) has no matching entry in `control_taxonomy_matrix` — the control was required but never designed.
  - A mandatory control domain with implementation rate between 50% and 70%.

- **Gap/Process Major Governance Finding (GP-MGF):** An ISO 42001 major management-system gap (from `iso_42001_output.major_gaps`). Per GR-001 calibration, GP-MGF is downgraded and classified as a **Minor Governance Finding** (-2 GAS deduction, does not count as an MGF, and does not block Governance Ready status).

**What does not constitute a CGC or MGF:**
- Optional controls (`mandatory: false`) that are unimplemented
- ISO 42001 Major or Minor gaps (`major_gaps`, `minor_gaps`) with no cascading control impact on mandatory domains
- "Third-Party Control Required" entries in the taxonomy matrix (gap, but not MGF unless the domain rate falls below the MGF threshold)
- Frameworks in `applicable_frameworks` that are optional for the client's jurisdiction

### Control Coverage Rate (CCR)

CCR measures what fraction of the mandatory regulatory control set has been addressed by any combination of Ethana platform capabilities, Cursory services, or customer-owned implementations.

```
denominator = count(control_requirements where mandatory = true)

implemented = count of mandatory controls matched to control_taxonomy_matrix entries
              where coverage_classification ∈ {
                "Fully Covered by Ethana",
                "Covered by Cursory Service",
                "Customer-Owned Control"
              }

partially_implemented = count of mandatory controls matched to control_taxonomy_matrix entries
                        where coverage_classification = "Partially Covered by Ethana"

not_implemented = denominator − implemented − partially_implemented
                  (includes "Third-Party Control Required" and unmatched mandatory controls)

numerator = implemented + (partially_implemented × 0.5)
CCR       = round(numerator / denominator × 100, 1)
```

The 0.5 partial credit for "Partially Covered by Ethana" controls is applied for consistency with the CTCS formula (PR-002) and the ISO 42001 Annex A coverage score — the same pattern governs all three coverage metrics in the Governance OS.

`ccr_numerator` and `ccr_denominator` must be reported in the Section 10 JSON payload to enable independent arithmetic verification: `round(ccr_numerator / ccr_denominator × 100, 1) == ccr`. This is the governance equivalent of `ctcs_numerator` / `ctcs_denominator` in Proposal Review.

### Classification Thresholds (Calibrated per GR-001)

| Classification | GAS | CCR | CGC | MGF | High Risks |
|---|---|---|---|---|---|
| **Governance Ready** | ≥ 85 | ≥ 80 | 0 | 0 | ≤ 1 |
| **Conditional Governance** | ≥ 65 | ≥ 60 | 0 | Any | ≤ 2 |
| **Not Governance Ready** | < 65 or any CGC | < 60 or any CGC | ≥ 1 | Any | > 2 |

**Any CGC → Not Governance Ready regardless of GAS or CCR.** This rule cannot be overridden commercially or under time pressure.

**Any mandatory GTG gate failure → Not Governance Ready** regardless of scores.

**Any score below Conditional thresholds** (GAS < 65 or CCR < 60) or High Residual Risks > 2 results in a classification of **Not Governance Ready**. The "Advisory Only" classification is not supported.

**The two-score relationship:** High GAS with low CCR indicates the governance documentation and framework coverage is adequate but control implementation has significant gaps — well-designed but underbuilt. Low GAS with high CCR indicates controls are in place but governance process findings are numerous — operationally active but non-conformant. Both conditions prevent Governance Ready and both must be diagnosed before re-assessment.

---

## Constraints and Scope

**In scope:**
- Synthesis of regulatory mapping, control mapping, and ISO 42001 gap assessment into a terminal governance verdict
- Cross-framework CCR calculation using `control_taxonomy_matrix` and `control_requirements`
- Governance gap and risk register consolidation
- GTG gate evaluation
- Capability governance alignment when `capability_validation_output` provided

**Out of scope:**
- New regulatory analysis — Governance Review accepts `regulatory_mapping_output` as-is and does not re-interpret jurisdictions or obligations
- New control design — `control_mapping_output` is accepted as-is
- ISO 42001 re-scoring — `iso_42001_output` scores are consumed, not recalculated (GHD6 if violated)
- Commercial proposal compliance — use `skills/ethana-proposal-review/`
- Technical feature validation — use `skills/ethana-feature-mapping/`

**Hard constraint — upstream authority:** Governance Review does not override or contradict upstream skill outputs. If `iso_42001_output.critical_gaps > 0`, those critical gaps are CGC candidates regardless of any other assessment result. If `control_requirements` identifies a mandatory control, it is in scope for CCR regardless of whether it was deprioritised during the engagement.

---

## Knowledge Dependencies

### Tier 1 — Required for every invocation

- `regulatory_mapping_output` — defines regulatory scope and mandatory control set
- `control_mapping_output` — provides implementation status per control
- `iso_42001_output` — provides AIMS maturity scores and gap register

These are not knowledge files — they are skill outputs passed as inputs. Every GTG gate check and every scoring calculation depends on these three inputs.

### Tier 2 — Contextual (loaded when relevant)

- `knowledge/frameworks/iso-42001.md` — for interpreting ISO 42001 clause scores and gap severity taxonomy when Section 4 gap register entries from ISO 42001 require severity adjudication
- `knowledge/regulations/eu-ai-act.md` — for evaluating EU jurisdiction CGC thresholds and mandatory framework scope
- `knowledge/regulations/india-ai-landscape.md` — for India jurisdiction checks
- `knowledge/regulations/uk-ai-guidance.md` — for UK FCA operational resilience and ICO DPA checks

---

## Related Skills

- `skills/regulatory-mapping/` — upstream; provides regulatory scope, jurisdiction coverage, and mandatory control requirements (CCR denominator)
- `skills/governance-control-mapping/` — upstream; provides control implementation status (CCR numerator) and evidence registry (GTG-6)
- `skills/iso-42001-gap-assessment/` — upstream; provides AMS, ARS, and gap register (GTG-3, Section 4, Section 6)
- `skills/ethana-capability-validation/` — upstream (optional); provides validated capability claims for Section 8 (GTG-4)
- `skills/ethana-proposal-review/` — parallel commercial gate; operates on draft proposals; not part of the governance chain; must not be used as the terminal gate for governance assessments (see ADR-006)
