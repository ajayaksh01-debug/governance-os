# Governance Review — Evaluation Criteria and Scoring Rubric

## Purpose

This document defines the quality standards for Governance Review outputs produced using this skill. It establishes:
- Seven Governance Hard Disqualifiers (GHD1 through GHD7) that invalidate the output regardless of numeric score
- A 100-point scoring rubric across all ten output sections
- A pass threshold of 85/100
- Common failure modes and corrective actions
- A peer review checklist for governance sign-off before any client delivery

Apply the GHD check first. Score only after confirming no hard disqualifiers are triggered. A disqualified output may not be delivered to a client or used as the basis for an engagement decision under any time pressure or commercial circumstance.

---

## Governance Hard Disqualifiers

**Check these before scoring. If any condition is true, the output is invalid — do not deliver it.**

| # | Condition | Check |
|---|---|---|
| GHD1 | Any mandatory GTG gate (GTG-1, GTG-2, GTG-3, GTG-7) failed but `governance_gate_passed` is not `false` in Section 10 — the gate result was misreported | [ ] Not triggered |
| GHD2 | Any Critical Governance Gap (CGC) is documented in Section 4 but the Governance Readiness Classification in Section 10 is not `Not Governance Ready` — the absolute rule was not applied to the classification | [ ] Not triggered |
| GHD3 | Any CGC is documented in Section 4 but GAS in Section 10 is greater than 0 — the absolute rule was not applied to the GAS | [ ] Not triggered |
| GHD4 | `ccr_denominator` in Section 10 is 0 but `regulatory_mapping_output.control_requirements` contains entries where `mandatory = true` — the denominator was miscounted or not sourced from the upstream input | [ ] Not triggered |
| GHD5 | The CCR arithmetic identity fails: `round(ccr_numerator / ccr_denominator × 100, 1) ≠ ccr` — the Section 10 values are internally inconsistent | [ ] Not triggered |
| GHD6 | ISO 42001 clause scores, AMS, ARS, or gap counts in Section 6 differ from the corresponding values in `iso_42001_output` — the upstream ISO 42001 output was re-scored rather than consumed | [ ] Not triggered |
| GHD7 | The Governance Readiness Classification in Section 10 is inconsistent with the GAS and CCR values against the classification threshold table — a classification was issued that the scores do not support | [ ] Not triggered |

**If any condition above is triggered, do not deliver the output.** Identify the specific failure, correct the relevant section(s), and re-score from Section 1.

**Most likely disqualifier triggers:**
- GHD2 and GHD3 together (CGC present, classification or GAS wrong) — the most commercially pressured failure; occurs when a reviewer attempts to reclassify a Not Governance Ready output to preserve an engagement
- GHD5 (CCR arithmetic inconsistency) — occurs when the numerator or denominator is updated in one place but not the other
- GHD6 (ISO 42001 re-scoring) — occurs when a reviewer recalculates clause scores rather than consuming them from `iso_42001_output`

---

## Scoring Overview

| Section | Maximum Score | Weight Rationale |
|---|---|---|
| **1. Executive Governance Summary** | 5 | Synthesis and communication quality — assessed after all other sections |
| **2. Regulatory Scope and Framework Matrix** | 8 | Completeness of scope framing — foundation for all downstream sections |
| **3. Control Coverage Assessment** | 20 | Core calculation — CCR arithmetic accuracy and explicit display are the primary audit signals |
| **4. Governance Gap Register** | 15 | Correctness and completeness of gap identification and severity classification |
| **5. Governance Risk Register** | 10 | Residual risk identification and severity assessment quality |
| **6. Framework Compliance Scores** | 10 | Completeness of per-framework assessment; fidelity to upstream ISO 42001 output |
| **7. Governance TG Gate Table** | 8 | Gate evaluation accuracy; governance_gate_passed correctly set |
| **8. Capability Governance Alignment** | 7 | Mapping quality when `capability_validation_output` provided; correct notice when absent |
| **9. Required Remediation Actions** | 7 | Action specificity, correct prioritisation (CGC actions first), and executability |
| **10. Governance Release Decision** | 10 | Scoring accuracy, arithmetic display, classification correctness, certificate completeness |
| **Total** | **100** | |

**Pass threshold: 85/100**

The 85/100 threshold reflects the greater qualitative judgment required in governance assessment relative to the binary claim-checking in Proposal Review. Reviewers should target 88+ to provide a buffer against adjacent-section weaknesses.

---

## Absolute Governance Rule

**Any Critical Governance Gap (CGC) automatically results in Governance Readiness Classification = Not Governance Ready and GAS = 0, regardless of CCR or any other score.**

This is not a deduction — it is a double override: both GAS and the classification are overridden the moment a CGC is confirmed in Section 4. A review that correctly identifies a CGC and applies the absolute rule scores full marks on Section 4 and Section 10 for those elements. A review that identifies a CGC but fails to apply the absolute rule triggers GHD2 and GHD3 simultaneously.

GHD2 and GHD3 are separate disqualifiers because each addresses a different failure mode: GHD2 covers the classification; GHD3 covers the GAS. A review can fail GHD3 (GAS > 0 despite CGC) while appearing to correctly set the classification, or fail GHD2 (wrong classification) while correctly setting GAS to 0. Both must be checked independently.

---

## Section-by-Section Rubric

### Section 1 — Executive Governance Summary (5 points)

| Score | Criteria |
|---|---|
| 5 | Written last and consistent with all other sections; accurately states GAS, CCR, classification, and CGC count; identifies the three most significant findings; states the single most important next action; written for a governance team lead or engagement director; no unexplained acronyms |
| 3–4 | Correct classification stated; one element missing (e.g., CGC count absent or most important action not specific enough); consistent with body sections |
| 1–2 | Present but does not accurately reflect the body of the review; or written before sections 2–9 are complete and contains a finding that differs from the final output |
| 0 | Absent; or states a classification inconsistent with Section 10 |

---

### Section 2 — Regulatory Scope and Framework Matrix (8 points)

| Score | Criteria |
|---|---|
| 7–8 | Both `applicable_regulations` and `applicable_frameworks` are represented; all jurisdictions with status = Confirmed are included; mandatory vs. optional designation is explicit for each entry; entries not assessed in this review are listed with exclusion reason |
| 5–6 | Most entries present; one regulation or framework excluded without reason; mandatory designations mostly correct |
| 3–4 | Section present but draws from only one of the two upstream arrays; or mandatory designations are absent or guessed rather than derived from `client_profile.jurisdictions` |
| 0–2 | Section missing or does not represent the scope from `regulatory_mapping_output` |

**Common failures:**
- Treating `applicable_regulations` and `applicable_frameworks` as the same thing — regulations (EU AI Act, FCA guidance) are in `applicable_regulations`; governance frameworks (ISO 42001, NIST AI RMF) are in `applicable_frameworks`; both must appear in Section 2
- Omitting entries with status = Conditional from `applicable_regulations` — Conditional entries are in scope and must be noted

---

### Section 3 — Control Coverage Assessment (20 points)

| Score | Criteria |
|---|---|
| 18–20 | CCR denominator correctly sourced from `control_requirements` where `mandatory = true`; `coverage_classification` mapping applied correctly (Implemented / Partially Implemented / Gap — see SKILL.md); numerator arithmetic is correct; `round(ccr_numerator / ccr_denominator × 100, 1) == ccr` verifies; per-domain rates shown; domains below 50% flagged as CGC candidates; "Third-Party Control Required" entries explicitly noted as gap (not counted) |
| 14–17 | Correct arithmetic; one minor classification error (e.g., one "Covered by Cursory Service" entry miscounted); per-domain rates present but one domain missing |
| 10–13 | CCR arithmetic has an error (wrong denominator count, wrong 0.5 weighting); or "Third-Party Control Required" incorrectly counted as Implemented; or per-domain rates absent |
| 5–9 | Multiple CCR errors that materially affect the score; or denominator sourced from `control_taxonomy_matrix` count rather than `control_requirements` count — this is a structural error (GHD4 candidate if denominator = 0) |
| 0–4 | Section absent; or CCR calculation completely absent; or arithmetic not shown |

**Common failures:**
- Sourcing the CCR denominator from `control_taxonomy_matrix` entry count rather than `control_requirements` mandatory count — these are different numbers; the taxonomy matrix may have more or fewer entries than the mandatory control set
- Counting "Third-Party Control Required" as Implemented — this classification indicates a gap, not coverage

---

### Section 4 — Governance Gap Register (15 points)

| Score | Criteria |
|---|---|
| 13–15 | All gaps sourced from `iso_42001_output.critical_gap_ids` are represented with Critical severity; CCR-identified gaps (undesigned mandatory controls, low-rate domains) are added with correct severity; CGC criteria correctly applied — not every Critical gap is a CGC; each gap entry has ID, description, source, severity, domain, and remediation category |
| 10–12 | Most gaps identified; one severity misclassification (e.g., MGF-level gap classified as Critical); gap IDs follow the GGP-[domain]-[n] format |
| 7–9 | Gaps listed but severity classification is generic or not derived from CGC/MGF criteria; or ISO 42001 critical gaps from `critical_gap_ids` are missing |
| 3–6 | Section present but does not integrate ISO 42001 output with CCR gaps — treats them as separate registers rather than a consolidated gap register |
| 0–2 | Section absent; or a CGC exists but is not identified (triggers GHD2 and GHD3) |

**Critical calibration note:** A Section 4 failure that results from not identifying a CGC means Section 10 will report an incorrect classification. This is the highest-severity failure in this skill — it triggers GHD2 and GHD3 simultaneously and invalidates the entire output.

---

### Section 5 — Governance Risk Register (10 points)

| Score | Criteria |
|---|---|
| 9–10 | All CGC and MGF items from Section 4 have corresponding risk entries; severity (High / Medium / Low) is consistent with CGC → High, MGF → Medium default (adjustable with rationale); risk IDs follow GRK-[n] format; residual likelihood and impact documented; owner and status present; High risk count in Section 10 matches High count here |
| 7–8 | All CGC/MGF-derived risks present; one MGF-level risk classified as Low without rationale; or one risk missing an owner |
| 4–6 | Risk register present but not all CGC/MGF items have corresponding entries; or severity classification is generic |
| 0–3 | Section absent; or risk count in Section 10 does not match this section |

---

### Section 6 — Framework Compliance Scores (10 points)

| Score | Criteria |
|---|---|
| 9–10 | All entries from `applicable_regulations` and `applicable_frameworks` in Section 2 appear here; for ISO 42001, AMS and ARS values exactly match `iso_42001_output.ams` and `ars`; clause scores drawn from `ams_clause_scores` without modification; at least one entry assessed to completion (GTG-7 condition); entries with all domains Not Assessed are not claimed as assessed |
| 7–8 | ISO 42001 values match upstream; one non-ISO entry missing or assessed superficially; GTG-7 condition met |
| 4–6 | ISO 42001 values present but differ from `iso_42001_output` by rounding or adjustment (GHD6 candidate); or no entry is assessed to completion |
| 0–3 | Section absent; or ISO 42001 clause scores differ materially from `iso_42001_output` — GHD6 triggered |

---

### Section 7 — Governance TG Gate Table (8 points)

| Score | Criteria |
|---|---|
| 7–8 | All seven gates present in correct format; mandatory gates (GTG-1, GTG-2, GTG-3, GTG-7) correctly evaluated; advisory gates (GTG-4, GTG-5, GTG-6) correctly shown as Pass or Noted absent — never as Fail; `governance_gate_passed` in Section 10 correctly set to false if any mandatory gate fails |
| 5–6 | Gate table complete; one advisory gate marked Fail rather than Noted absent; `governance_gate_passed` correctly set |
| 3–4 | Gate table incomplete (fewer than 7 gates); or a mandatory gate failure not reflected in `governance_gate_passed` (GHD1 candidate) |
| 0–2 | Section absent; or mandatory gate failed but `governance_gate_passed = true` — GHD1 triggered |

**Key distinction:** Advisory gates (GTG-4, GTG-5, GTG-6) are "Pass" or "Noted absent" — never "Fail." Using "Fail" for an advisory gate incorrectly implies the review is invalid.

---

### Section 8 — Capability Governance Alignment (7 points)

*If `capability_validation_output` was not provided, score 7 if Section 8 correctly states "GTG-4 not passed — Section 8 cannot be completed."*

| Score | Criteria |
|---|---|
| 6–7 | Each `allowed_claims` entry mapped to at least one control domain; mandatory controls satisfied (fully or partially) identified per capability; control gaps where no capability provides coverage explicitly named; mapping is traceable to `allowed_claims` entries not invented |
| 4–5 | Most capabilities mapped; one capability missing a domain assignment; control gaps identified but not all named |
| 2–3 | Capability list present but control domain mapping is generic; gaps not identified |
| 0–1 | Section absent when `capability_validation_output` was provided; or Section 8 claims capability alignment when `capability_validation_output` was not provided |

---

### Section 9 — Required Remediation Actions (7 points)

| Score | Criteria |
|---|---|
| 6–7 | CGC-addressing actions listed first with Priority = Immediate; MGF actions listed second; advisory actions last; each action references the gap or risk ID it addresses; actions are specific enough to execute without further clarification |
| 4–5 | Correct ordering; one action is generic rather than specific ("address control gaps" rather than "design and implement [specific control] per GGP-CM-001"); all CGC actions are Priority = Immediate |
| 2–3 | Actions present but not ordered by CGC / MGF / advisory priority; or CGC-addressing actions are Priority = Before Deployment rather than Immediate |
| 0–1 | Section absent when findings exist; or actions do not reference gap or risk IDs |

---

### Section 10 — Governance Release Decision (10 points)

| Score | Criteria |
|---|---|
| 9–10 | GAS arithmetic shown (base, each deduction type, result — or 0 if CGC present); CCR arithmetic shown (denominator, implemented, partially implemented, numerator, result); classification matches threshold table; `governance_gate_passed` correctly set; ISO 42001 pass-through values match `iso_42001_output`; Governance Readiness Certificate complete with all fields |
| 7–8 | All fields present; arithmetic correct; one minor format omission (e.g., ISO 42001 classification absent) |
| 4–6 | GAS or CCR arithmetic not shown; or classification is correct but the certificate section is incomplete |
| 0–3 | Classification is wrong because a CGC was not identified — GHD2 and GHD3 triggered; or Section 10 absent |

---

## Score Thresholds and Delivery Criteria

| Score | Assessment | Delivery Action |
|---|---|---|
| 90–100 | Exemplary | Deliver as final. Suitable for inclusion in the examples library as a calibration anchor. |
| 85–89 | Acceptable | Deliver as final. Note dimensional weaknesses for the next engagement cycle. |
| 70–84 | Below standard | Do not deliver. Identify failing dimensions and revise. Re-score before delivery. |
| Below 70 | Insufficient | Do not deliver. Major revision required. If Section 3 or Section 4 is the primary failure, the upstream control mapping or ISO 42001 output may also need correction before re-assessment. |

---

## Peer Review Checklist

Required before delivering any output with classification Governance Ready or Conditional Governance. A separate reviewer (not the analyst who ran the review) must complete this checklist.

**Hard Disqualifier Confirmation:**
- [ ] Reviewer has confirmed that if any CGC was identified in Section 4, the classification is Not Governance Ready and GAS = 0 (GHD2, GHD3)
- [ ] Reviewer has confirmed all mandatory GTG gates are correctly evaluated and `governance_gate_passed` matches gate table results (GHD1)
- [ ] Reviewer has confirmed `ccr_denominator` matches the count of `control_requirements` entries where `mandatory = true` from the upstream input (GHD4)
- [ ] Reviewer has confirmed CCR arithmetic identity: `round(ccr_numerator / ccr_denominator × 100, 1) == ccr` (GHD5)
- [ ] Reviewer has opened `iso_42001_output` and confirmed Section 6 AMS, ARS, and clause scores match exactly (GHD6)
- [ ] Reviewer has confirmed the classification matches the calibrated threshold table (GR-001: Governance Ready allows High Risks <= 1, Conditional Governance allows High Risks <= 2, and no Advisory Only classification exists) (GHD7)
- [ ] Reviewer has confirmed that GP-MGF items (ISO 42001 major management-system gaps) are classified as Minor Findings rather than Major findings per GR-001 (deducting -2 GAS instead of -10)

**CCR Verification:**
- [ ] Reviewer has independently counted mandatory controls from `control_requirements`
- [ ] Reviewer has confirmed `coverage_classification` mapping: "Fully Covered by Ethana", "Covered by Cursory Service", and "Customer-Owned Control" count as Implemented; "Partially Covered by Ethana" counts as 0.5; "Third-Party Control Required" counts as 0
- [ ] Reviewer has confirmed each mandatory domain rate is stated and domains below 50% are flagged

**Gap Register Verification:**
- [ ] Reviewer has confirmed all entries in `iso_42001_output.critical_gap_ids` appear in Section 4 with Critical severity
- [ ] Reviewer has confirmed CGC criteria were applied correctly — not every Critical severity gap is a CGC
- [ ] Reviewer has confirmed Section 5 (Risk Register) has a GRK entry for every CGC and MGF from Section 4

---

## Calibration Reference

The three worked examples in `examples.md` serve as scoring anchors, calibrated per GR-001.

| Example | Scenario | Key challenge | Expected GHDs | Expected score |
|---|---|---|---|---|
| Example 1 | Meridian Private Bank — BFSI, EU + UK, High-Risk AI, Governance Ready | Full CCR arithmetic; GP-MGF downgraded to Minor under GR-001; 0 MGFs and High Risks = 0 results in Governance Ready classification | None | 88–92 — solid review; deductions for minor findings in Section 5 and Section 9 specificity |
| Example 2 | Axiom FinTech — EU, Limited-Risk AI, Conditional Governance with MGFs | MGF identification for undesigned mandatory controls; GP-MGF downgraded to Minor under GR-001; Conditional Governance classification | None if MGFs correctly identified and GTG-4 correctly marked Noted absent | 85–88 — correct classification; typical deductions in Section 8 and Section 9 ordering |
| Example 3 | Apex Government Agency — EU + UK, High-Risk AI, GTG-3 failure and CGC | GTG-3 mandatory gate fail; CGC absolute rule (GAS = 0); CCR computed even when gate fails; fallback to Not Governance Ready classification | GHD1 if gate fail not reflected; GHD2/GHD3 if CGC misclassified | 85–90 if absolute rule and gate correctly applied; automatic disqualification under GHD1/GHD2/GHD3 if not |
