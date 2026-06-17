# Ethana Proposal Review — Evaluation Criteria and Scoring Rubric

## Purpose

This document defines the quality standards for Proposal Review outputs produced using this skill. It establishes:
- Seven hard disqualifiers (HD1 through HD7) that block release regardless of numeric score
- A 100-point scoring rubric across all ten output sections
- A pass threshold of 95/100
- Common failure modes and corrective actions
- A peer review checklist for compliance sign-off before any client release

Apply the hard disqualifier check first. Score only after confirming no hard disqualifiers are triggered. A disqualified output may not be released under any time pressure or commercial circumstance.

---

## Hard Disqualifiers

**Check these before scoring. If any condition is true, do not release the output.**

| # | Condition | Check |
|---|---|---|
| HD1 | Any Aspirational capability (e.g., Workspace, Visual Agent Builder, or any capability listed as Aspirational in canonical-product-model.md) is presented as currently available, active, or deployable anywhere in the draft proposal, and Section 8 does not flag this as a Critical Firewall Breach | [ ] Not triggered |
| HD2 | Any In Build capability is presented as currently available or deployable without explicit "In Build — roadmap, not yet available" disclosure in the proposal, and Section 8 does not flag this as a Critical Firewall Breach | [ ] Not triggered |
| HD3 | Any certification not confirmed as currently held in canonical-product-model.md (e.g., SOC 2 Type II, ISO 27001, ISO 42001 certification) is stated as current for Ethana or Cursory, and Section 8 does not flag this as a Critical Firewall Breach | [ ] Not triggered |
| HD4 | canonical-product-model.md was not directly consulted during Phase 4 — evidenced by Section 4 (Capability Status Validation) containing no verbatim canonical model quotes for Production capability claims | [ ] Not triggered |
| HD5 | The Mandatory Traceability Gate (TG-1 through TG-7) was not completed — any of TG-1, TG-2, TG-3, or TG-7 is marked failed or absent in Section 10 | [ ] Gate completed |
| HD6 | The review was applied to fewer than 100% of proposal sections containing Ethana capability claims — any section of the draft containing a capability claim was excluded from the Claim Inventory in Section 2 | [ ] Not triggered |
| HD7 | A PCS of 0 was computed (one or more CFBs present) but the Release Classification in Section 10 reads anything other than Rejected | [ ] Not triggered |

**If any condition above is triggered, the output is automatically disqualified regardless of the total score.** Correct the specific failure, re-run from the Traceability Gate (Phase 1, Step 1.1), and re-score from the beginning.

**Most likely disqualifier triggers:**
- HD1 or HD2 (Aspirational / In Build as Production) — the most commercially pressured failure; occurs when sales team language is copied into the proposal without Section 4 verification
- HD4 (canonical model not consulted) — occurs on expedited reviews where the reviewer relies solely on upstream skill outputs without checking the ground truth
- HD6 (incomplete audit) — occurs when a boilerplate section or appendix containing capability claims is classified as "out of scope"
- HD7 (PCS 0 but not marked Rejected) — occurs when the reviewer attempts to reclassify a Rejected document under commercial pressure

---

## Scoring Overview

| Section | Maximum Score | Weight Rationale |
|---|---|---|
| **1. Executive Assessment** | 5 | Synthesis and communication quality — assessed after all other sections |
| **2. Claim Inventory** | 10 | Completeness is foundational — every missed claim undermines CTCS integrity |
| **3. Claim Traceability Matrix** | 20 | Core audit output — CTCS accuracy and traceability evidence quality |
| **4. Capability Status Validation** | 20 | Claims Firewall enforcement — the highest-stakes section |
| **5. Regulatory Coverage Validation** | 8 | Coverage adequacy and gap identification |
| **6. Control Coverage Validation** | 7 | Configuration consistency with upstream control design |
| **7. Commercial Risk Register** | 5 | Risk classification quality and completeness |
| **8. Critical Firewall Breaches (CFB)** | 10 | Accuracy and completeness of CFB identification and remediation guidance |
| **9. Major Risk Findings (MRF)** | 5 | MRF quality and actionability |
| **10. Release Decision** | 10 | Scoring accuracy, gate completion, classification correctness, certificate quality |
| **Total** | **100** | |

**Pass threshold: 95/100**

---

## Absolute Release Rule

**Any Critical Firewall Breach (CFB) automatically results in Release Classification = Rejected regardless of PCS or CTCS.**

This is not a deduction — it is an override. The Release Classification is set to Rejected the moment a CFB is confirmed in Section 8, irrespective of all other scores. A review that identifies CFBs and correctly classifies the document as Rejected scores full marks on Section 8 and Section 10 (for correct identification and classification). A review that identifies CFBs and fails to flag them is disqualified under HD1, HD2, or HD3.

---

## Section-by-Section Rubric

### Section 1 — Executive Assessment (5 points)

| Score | Criteria |
|---|---|
| 5 | 200–250 words; written for Sales Director, Compliance Director, and Legal Counsel; accurately reflects all findings; covers document type, client, claim count, compliance status, and Release Classification; identifies the single most important action; written last and consistent with all other sections; no jargon |
| 3–4 | Correct but slightly over or under length; one element missing (e.g., claim count absent); Release Classification stated correctly |
| 1–2 | Present but does not accurately reflect the body of the review; or written before sections 2–9 are complete and contains a position that differs from the final findings |
| 0 | Missing or incorrect Release Classification stated |

---

### Section 2 — Claim Inventory (10 points)

| Score | Criteria |
|---|---|
| 9–10 | Every Ethana capability claim in every section of the proposal is catalogued; claim IDs are sequential and consistent; each entry has verbatim text, claim type, and proposal section reference; total count in Section 2 matches the denominator in the CTCS calculation |
| 7–8 | One or two claims missed; all identified claims have complete entries; missed claims are not of a type that would change the Release Classification |
| 5–6 | A whole section of the proposal was not reviewed; or claims are catalogued at the product level rather than the claim level ("Ethana is secure" is not a claim — it is not specific enough); or claim types are frequently misclassified |
| 3–4 | Significant claims missed; CTCS denominator is understated; the omitted claims are of types likely to contain prohibited language |
| 0–2 | Section 2 is incomplete to the point where the CTCS is not reliable |

**Common failures:**
- Treating the Executive Summary of the proposal as out of scope — it often contains the most promotional capability language
- Missing certification claims because they appear in a compliance section rather than a capabilities section
- Combining two separate capability claims into one entry, deflating the total count and distorting CTCS

---

### Section 3 — Claim Traceability Matrix (20 points)

| Score | Criteria |
|---|---|
| 18–20 | Every claim in Section 2 has a traceability entry; upstream source citations are specific (section + entry, not just skill name); CTCS arithmetic is correct and shows numerator, denominator, and result; Partially Traced claims correctly score 0.5; traceability statuses are correctly assigned; no Traced claim cites a Prohibited Claims Register entry |
| 14–17 | One or two traceability assignments are incorrect (e.g., a Partially Traced claim is assigned Traced because a mandatory caveat was overlooked); CTCS arithmetic is correct; citations are specific |
| 10–13 | CTCS arithmetic has an error (wrong count, incorrect 0.5 weighting for Partially Traced); or multiple traceability assignments are incorrect; or citations are generic ("solution mapping" without naming the specific entry) |
| 5–9 | Multiple traceability errors that materially affect CTCS; a claim that should be Prohibited is marked Untraced; or CTCS is not calculated |
| 0–4 | Section 3 is incomplete or does not cover all claims from Section 2 |

**Common failures:**
- Marking a claim Traced when the upstream source uses different language or omits a mandatory caveat — this is Partially Traced at most
- Marking a Prohibited claim as Untraced rather than Prohibited — Prohibited is a more severe status and changes the PCS deduction model

---

### Section 4 — Capability Status Validation (20 points)

| Score | Criteria |
|---|---|
| 18–20 | Every unique Ethana capability referenced in the proposal is checked; canonical-product-model.md verbatim quote present for every capability; match verdicts are correct; every CFB correctly triggers a Section 8 entry; every MRF correctly triggers a Section 9 entry; no Production capability is missed; scope expansion is correctly identified even when base status is Production |
| 14–17 | Status determinations are correct; one minor scope expansion missed that does not affect the Release Classification; all CFBs correctly identified |
| 10–13 | One capability is missed entirely; or a scope expansion that constitutes a CFB is classified as an MRF; or verbatim canonical model quotes are absent (paraphrasing instead) |
| 5–9 | Multiple capabilities missed; or In Build capability is classified as Compliant; or canonical-product-model.md was not consulted (triggers HD4) |
| 0–4 | Section 4 is absent or does not contain any canonical model references — automatic disqualification under HD4 |

**Common failures:**
- Checking the product line (e.g., "Ethana Build is Production") rather than the specific capability (e.g., "CI/CD gate integration for Red Teaming Orchestrator is In Build")
- Accepting upstream skill outputs as canonical authority without cross-checking the canonical model directly
- Missing certification claims that appear in a different section of the proposal from the capability descriptions

---

### Section 5 — Regulatory Coverage Validation (8 points)

*Score 8 if regulatory-mapping output was not provided and section correctly states it was skipped.*

| Score | Criteria |
|---|---|
| 7–8 | Every control requirement in Regulatory Mapping Section 6 is mapped to a proposal response; coverage adequacy is correctly assessed; gaps are identified and classified as MRF or Minor Finding as appropriate |
| 5–6 | Most requirements mapped; one or two coverage gaps not identified; or adequacy assessment is superficial |
| 3–4 | Section present but coverage assessment is generic; requirements are listed without assessing how the proposal addresses them |
| 0–2 | Section missing when regulatory-mapping output was provided; or material coverage gaps not flagged |

---

### Section 6 — Control Coverage Validation (7 points)

*Score 7 if control-mapping output was not provided and section correctly states it was skipped.*

| Score | Criteria |
|---|---|
| 6–7 | Every Ethana configuration in Control Mapping Section 10 is compared against the proposal; inconsistencies correctly identified; configuration claims in the proposal that contradict Section 10 specifications are flagged as MRFs |
| 4–5 | Most configurations checked; one inconsistency missed; assessments are generally accurate |
| 2–3 | Superficial comparison; inconsistencies not identified or not classified as MRFs |
| 0–1 | Section missing when control-mapping output was provided |

---

### Section 7 — Commercial Risk Register (5 points)

| Score | Criteria |
|---|---|
| 5 | All MRFs and Minor Findings correctly separated from CFBs; MRF entries include finding, risk if unaddressed, required action, and -5 PCS deduction; Minor Finding entries include finding and -1 PCS deduction; Advisory Notes present where relevant; no CFB-level issue is classified as an MRF |
| 3–4 | Classification is mostly correct; one MRF is classified as Minor Finding (or vice versa) — deduction miscalibrated but not materially wrong |
| 1–2 | Findings are not classified by tier; PCS deductions are not assigned; or a CFB-level finding is classified as an MRF |
| 0 | Missing or contains no findings when the proposal had identifiable risk issues |

---

### Section 8 — Critical Firewall Breaches (10 points)

| Score | Criteria |
|---|---|
| 9–10 | Every CFB is documented with: CFB ID, breach type, verbatim proposal text, verbatim canonical model status, ADR provision violated, and specific required corrective action; if no CFBs detected, the section states this explicitly with the claim count audited |
| 7–8 | All CFBs identified; one entry is missing the ADR provision reference or corrective action is general rather than specific |
| 5–6 | Most CFBs identified; one CFB missed that would not change the Release Classification (proposal was already Rejected on other grounds); entries lack verbatim canonical model quotes |
| 2–4 | One or more CFBs missed that would change the Release Classification from Rejected to Approved (the most serious scoring failure in this skill) |
| 0 | A CFB exists in the proposal and is not identified — automatic disqualification under HD1, HD2, or HD3 depending on breach type |

**Critical calibration note:** A score of 2–4 on Section 8 that results from missing a CFB means the Release Classification is wrong. A Rejected document was issued an Approved or Approved with Revisions classification. This is the highest-severity failure in the skill — it constitutes a Claims Firewall bypass and triggers HD7.

---

### Section 9 — Major Risk Findings (5 points)

| Score | Criteria |
|---|---|
| 5 | All MRFs from Section 7 are consolidated; each entry has: MRF ID, description, risk if unaddressed, specific required action, and -5 PCS deduction confirmation; if no MRFs, section explicitly states this |
| 3–4 | All MRFs present; one or two entries have generic required actions rather than specific corrective steps |
| 1–2 | MRF list is incomplete; or required actions are not specific enough to act on |
| 0 | Missing when MRFs exist |

---

### Section 10 — Release Decision (10 points)

| Score | Criteria |
|---|---|
| 9–10 | Traceability Gate table is complete with pass/fail status for all seven steps; PCS arithmetic is shown (base, deductions by type, final); CTCS arithmetic is shown (numerator, denominator, result); Release Classification is correct for the PCS and CTCS values; Release Audit Certificate is complete with all required fields; required actions listed if not Approved |
| 7–8 | All fields present; arithmetic is correct; one minor format omission (e.g., claim count missing from certificate) |
| 5–6 | PCS or CTCS arithmetic is present but has a minor error; or the Release Classification is correct but the certificate is incomplete |
| 2–4 | Release Classification is incorrect for the stated PCS and CTCS values; or Traceability Gate table is absent; or arithmetic is not shown |
| 0 | Release Classification is wrong because a CFB was missed (triggers HD7); or Section 10 is absent |

---

## Score Thresholds and Release Criteria

| Score | Classification | Release Action |
|---|---|---|
| 98–100 | Exemplary | Release as final. Suitable for inclusion in the examples library as a calibration anchor. |
| 95–97 | Acceptable | Release as final. Note any dimensional weaknesses for the next review cycle. |
| 80–94 | Below standard | Do not release. Identify the specific failing dimensions and revise. A re-review from Phase 1 is required before issuing a classification. |
| Below 80 | Insufficient | Do not release. Major revision required. If Section 4 or Section 8 is the primary failure, the upstream proposal also requires revision before re-review. |

**Note on the pass threshold:** The 95/100 threshold means that a review may lose up to 5 points across all dimensions and still be released. In practice, a single missed MRF in Section 9 (-5 points, landing at 95) plus a Section 1 that is 1 point below full score (landing at 94) would block release. Reviewers should target 97+ to provide a buffer.

---

## Peer Review Checklist

Required before releasing any output that results in an Approved or Approved with Revisions classification. A separate reviewer (not the analyst who ran the review) must complete this checklist.

**Hard Disqualifier Confirmation:**
- [ ] Reviewer has independently confirmed no Aspirational capabilities are presented as Production in the draft proposal (HD1)
- [ ] Reviewer has independently confirmed no In Build capabilities are presented as Production without disclosure (HD2)
- [ ] Reviewer has independently confirmed no uncertified certifications are claimed (HD3)
- [ ] Reviewer has confirmed Section 4 contains verbatim canonical-product-model.md quotes (HD4)
- [ ] Reviewer has confirmed TG-1, TG-2, TG-3, and TG-7 are marked Pass in Section 10 (HD5)
- [ ] Reviewer has confirmed Section 2 covers all proposal sections containing capability claims (HD6)
- [ ] Reviewer has confirmed the Release Classification is consistent with the PCS and CTCS values (HD7)

**Claim Traceability Review:**
- [ ] Reviewer has sampled at least 5 Traced claims and confirmed each traces to a specific upstream entry — not just a skill name
- [ ] Reviewer has confirmed CTCS arithmetic is correct (numerator + denominator + result)
- [ ] Reviewer has confirmed Prohibited claims are marked Prohibited, not Untraced

**Firewall Review:**
- [ ] Reviewer has opened canonical-product-model.md and independently confirmed the canonical status for each unique capability listed in Section 4
- [ ] Reviewer has confirmed every CFB entry in Section 8 has a specific corrective action — not "remove this claim" but "replace with: [specific compliant language from solution-mapping Section 3 entry X]"

**Scoring Review:**
- [ ] Reviewer has confirmed PCS arithmetic: base 100, minus (MRF count × 5), minus (Minor Finding count × 1)
- [ ] Reviewer has confirmed the Release Classification matches the threshold table for the stated PCS and CTCS values
- [ ] Reviewer has confirmed the Release Audit Certificate is complete

---

## Calibration Reference

The three worked examples in `examples.md` serve as scoring anchors.

| Example | Scenario | Key challenge | Expected hard disqualifiers | Expected score |
|---|---|---|---|---|
| Example 1 | Indian bank RFP — clean proposal, all upstream outputs available | Full CTCS audit; verify no CFBs in a large claim set | None | 96–98 — clean review with full traceability |
| Example 2 | UK insurer pitch deck — Aspirational capability as Production + uncertified certification | CFB identification and Rejected classification under commercial pressure | HD1 and HD3 if reviewer misses or reclassifies; none if correctly identified | 95–97 if CFBs correctly identified and document classified Rejected; automatic disqualification if HD1 or HD3 triggered |
| Example 3 | EU bank proposal — Approved with Revisions; In Build disclosed in wrong section | MRF classification for In Build in non-Roadmap section; correct Release Classification | None if In Build is correctly identified as MRF not CFB | 95–96 if MRF correctly classified and document receives Approved with Revisions |
