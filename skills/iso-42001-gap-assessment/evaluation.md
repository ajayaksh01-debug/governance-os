# ISO 42001 Gap Assessment — Evaluation Criteria and Scoring Rubric

## Purpose

This document defines the quality standards for ISO 42001 Gap Assessment outputs produced using this skill. It establishes:
- Six hard disqualifiers (HD1 through HD6) that block release regardless of numeric score
- A 100-point scoring rubric across all ten output sections
- A pass threshold of 85/100
- An Absolute Release Rule for Claims Firewall violations in Section 8.5
- Common failure modes and corrective actions
- A peer review checklist for compliance sign-off
- A calibration reference mapping each example to expected scores

Apply the hard disqualifier check first. Score only after confirming no hard disqualifiers are triggered. A disqualified output may not be released under any commercial or time pressure.

---

## Hard Disqualifiers

**Check these before scoring. If any condition is true, do not release the output.**

| # | Condition | Check |
|---|---|---|
| HD1 | Clause 4 (Context of the Organisation) assessment is absent from Section 2 — no Clause 4 maturity rating is assigned and no AIMS scope statement appears in the output | [ ] Not triggered |
| HD2 | Any Ethana capability cited in Section 8 (Ethana Coverage Analysis) is classified as In Build or Aspirational in `knowledge/ethana/canonical-product-model.md`, and Section 8.5 (Claims Firewall Review) does not flag it as an Invalid Reference and correct it | [ ] Not triggered |
| HD3 | Section 3 (Annex A Control Assessment) covers fewer than all nine Annex A control categories — even if all controls in a category are N/A, the category must appear in Section 3 with a rationale | [ ] Not triggered |
| HD4 | Any gap in Section 4 (Gap Register) has a severity rating assigned without citing a specific ISO 42001 clause number or Annex A category reference | [ ] Not triggered |
| HD5 | The AMS in Section 10 is calculated without both Section 2 (Clause Coverage Matrix, all seven clauses rated) and Section 3 (Annex A Control Assessment, all applicable controls assessed) being complete | [ ] Not triggered |
| HD6 | The Certification Classification in Section 10 is "Certification Ready" when one or more Critical-severity gaps remain open in Section 4 | [ ] Not triggered |

**If any condition above is triggered, the output is automatically disqualified regardless of the total score.** Correct the specific failure, re-run from Phase 1, and re-score from the beginning. Do not release a disqualified output.

**Most likely disqualifier triggers:**
- HD2 (In Build capability as Production) — occurs when the reviewer relies on `framework-crosswalk.md` capability suggestions without cross-checking canonical-product-model.md status. Compliance Pack [IB] is the most common offending capability — it maps perfectly to ISO 42001 but is In Build.
- HD5 (AMS computed from incomplete assessment) — occurs on abbreviated assessments where a single clause or Annex A category is omitted because it appears not to apply; occurs frequently for Clause 10 (Improvement) on first assessments where no correction process exists.
- HD6 (Certification Ready with open Critical gaps) — occurs under commercial pressure to present a more favourable outcome; also occurs when the reviewer applies the AMS threshold (≥ 80) without checking the Critical gap count.

---

## Absolute Release Rule — Claims Firewall

**Any Ethana capability referenced in Section 8 that is classified as In Build or Aspirational in canonical-product-model.md automatically becomes HD2 and blocks release of the assessment.**

This rule applies whether the capability is cited as fully closing a gap or partially closing one. The canonical model's status determines eligibility — not the relevance of the capability to the gap or the commercial desirability of the claim. The assessment may only be released after all Invalid References in Section 8.5 are corrected and Section 8 is updated to remove or reclassify the offending capability references.

---

## Scoring Overview

| Section | Maximum Score | Weight Rationale |
|---|---|---|
| **1. Executive Summary** | 5 | Synthesis and communication quality |
| **2. Clause Coverage Matrix** | 18 | Foundation of the AMS; maturity ratings determine the entire certification trajectory |
| **3. Annex A Control Assessment** | 18 | Equal weight to Section 2 — together they constitute the full gap picture |
| **4. Gap Register** | 15 | Completeness and accuracy of gap identification; drives all downstream sections |
| **5. Risk Prioritisation** | 10 | Prioritisation accuracy determines whether the remediation roadmap is actionable |
| **6. Evidence Requirements** | 8 | ARS Evidence Availability component depends on the accuracy of this section |
| **7. Remediation Roadmap** | 7 | Practical realism and sequencing quality |
| **8. Ethana Coverage Analysis** | 10 | Commercial precision; Claims Firewall compliance; Section 8.5 must be complete |
| **9. Audit Readiness Assessment** | 5 | ARS calculation accuracy and Stage 1/2 verdict quality |
| **10. Overall Maturity Score** | 4 | Arithmetic accuracy; classification correctness |
| **Total** | **100** | |

**Pass threshold: 85/100**

---

## Section-by-Section Rubric

### Section 1 — Executive Summary (5 points)

| Score | Criteria |
|---|---|
| 5 | 200–250 words; written for CISO, CRO, Chief AI Officer, and board; accurately states AMS, ARS, Certification Classification, total gap count by severity, the single highest-priority action, and months to Stage 1 readiness; no technical jargon without explanation; written after all other sections are complete; consistent with Section 10 |
| 3–4 | Correct but slightly over/under length; one element missing (e.g., ARS score absent); Classification stated correctly |
| 1–2 | Present but does not accurately reflect the body of the assessment; or written before Sections 2–9 are complete and states a Classification that differs from Section 10 |
| 0 | Missing or states a Certification Classification that contradicts Section 10 |

---

### Section 2 — Clause Coverage Matrix (18 points)

| Score | Criteria |
|---|---|
| 16–18 | All seven clauses (4–10) assessed; maturity ratings (0–5) are correctly assigned with justification; current state descriptions accurately reflect available evidence; ISO 27001 credit (if applicable) is documented with scope and overlap rationale; clause gaps are identified and provisionally severity-rated; no clause is omitted |
| 13–15 | All seven clauses present; one or two maturity ratings are off by one level with minor justification issues; ISO 27001 credit applied but overlap rationale is thin |
| 9–12 | One clause is absent or rated without justification; or a maturity rating is off by two levels (e.g., rating maturity 3 where the evidence supports only maturity 1); or ISO 27001 credit applied beyond the scope of the certificate |
| 5–8 | Multiple clauses absent or rated without justification; Clause 8 (the most complex) is treated superficially at the same level as simpler clauses |
| 0–4 | Clause 4 absent (triggers HD1 regardless of other scores); or fewer than four clauses assessed |

**Common failures:**
- Assigning maturity 3 (Defined) when documentation exists but is not approved or version-controlled — "someone wrote it down" is not maturity 3 unless it is formally controlled
- Rating Clause 8 as maturity 3 when AI lifecycle management exists for some systems in the portfolio but not all — consistent coverage across the AI portfolio is the Clause 8 standard
- Not crediting ISO 27001 for Clauses 4–7 when the certificate scope clearly overlaps — this understates the baseline and overstates the gap severity

---

### Section 3 — Annex A Control Assessment (18 points)

| Score | Criteria |
|---|---|
| 16–18 | All 9 categories and all 38 controls assessed; N/A controls include rationale; status assignments (Implemented / Partially Implemented / Not Implemented / N/A) are accurate; evidence basis is cited for Implemented and Partially Implemented controls; control-level gap descriptions are specific enough to drive remediation |
| 13–15 | All 9 categories present; one or two status assignments are incorrect (e.g., Partially Implemented where evidence only exists for part of the portfolio); evidence citations are mostly specific |
| 9–12 | One category is absent (triggers HD3 if zero assessment for the category); or status assignments are frequently miscalibrated (e.g., calling controls Partially Implemented that have no evidence basis); or evidence citations are generic ("we have a monitoring process" without specifying what it is) |
| 5–8 | Multiple categories partially covered; significant controls within assessed categories omitted; no distinction made between controls that are N/A and those that are Not Implemented |
| 0–4 | Fewer than 6 categories assessed; or the Annex A assessment is replaced with a high-level summary that does not go to the control level |

**Common failures:**
- Conflating general IT controls with AI-specific Annex A controls — an IT incident response process does not satisfy Annex A Category 7 unless it explicitly covers AI-specific incident types
- Marking Category 5 (Supply Chain) controls as N/A for organisations that use third-party LLM APIs — those are AI supply chain relationships and Category 5 applies
- Marking Category 6 (Human Oversight) as Implemented without evidence of documented override mechanisms — informal human review is not the same as a defined, tested override capability

---

### Section 4 — Gap Register (15 points)

| Score | Criteria |
|---|---|
| 13–15 | Every gap from Sections 2 and 3 appears in the register; Gap IDs follow the correct scheme; all four severity levels (Critical/Major/Minor) are correctly applied; every gap has a clause/control reference; effort estimates are proportionate; proposed owners are role-level (not named individuals) |
| 10–12 | One or two gaps from Sections 2 or 3 are not in the register; severity ratings are mostly correct; one or two entries are missing clause references |
| 7–9 | Notable gaps from the clause or Annex A assessment are absent from the register; severity ratings are systematically wrong (e.g., all gaps rated Major when some are clearly Critical); triggers HD4 if any gap lacks a clause reference |
| 3–6 | Significant proportion of identified gaps not registered; Gap ID scheme not used; effort estimates absent |
| 0–2 | Gap Register is incomplete to the point of being unreliable as a remediation input |

**Common failures:**
- Omitting a gap because it appears in both Section 2 (clause level) and Section 3 (control level) — both levels must be registered separately if they represent distinct remediation items
- Rating a scope-definition gap (Clause 4, AIMS scope undefined) as Major rather than Critical — an undefined scope is a fundamental AIMS failure that no auditor will pass
- Including gaps without severity ratings because "the severity depends on context" — severity must be assigned; contextual caveats go in the description field, not instead of a severity

---

### Section 5 — Risk Prioritisation (10 points)

| Score | Criteria |
|---|---|
| 9–10 | All gaps from Section 4 appear in the risk matrix; both axes (certification blocker, business risk) are correctly assessed; Priority ranks (P1–P5) are correctly assigned and consistent with severity ratings; P1 gaps align with Critical gaps; no Critical gap is rated P3 or lower |
| 7–8 | All gaps present; one or two Priority rank assignments are slightly miscalibrated (a Major gap rated P2 that could be P3); axes are correctly applied |
| 5–6 | Several gaps are missing; or Priority ranks do not align with severity ratings (Critical gaps at P3); or the two axes are collapsed into a single dimension |
| 2–4 | Priority ranking is applied without reference to the risk matrix axes; or all gaps receive the same rank |
| 0–1 | Section missing or does not reference the Gap Register |

---

### Section 6 — Evidence Requirements (8 points)

| Score | Criteria |
|---|---|
| 7–8 | Every gap in the register has an evidence entry; evidence type, description, source system, retention requirement, and readiness status are all populated; ARS Evidence Availability component can be directly derived from the readiness status column; evidence descriptions are specific enough for an auditor to verify |
| 5–6 | Most gaps have evidence entries; readiness status is missing for some; evidence descriptions are occasionally generic ("relevant documentation") |
| 3–4 | Evidence entries exist but are consistently generic; retention requirements absent; readiness status not assessed |
| 0–2 | Section missing or does not map to the Gap Register entries |

---

### Section 7 — Remediation Roadmap (7 points)

| Score | Criteria |
|---|---|
| 6–7 | Four phases present (30/60/90/180-day); all P1–P5 gaps appear in the appropriate phase; each action specifies the gap it closes, the deliverable, the responsible role, and dependencies; critical path is identified; time estimates are proportionate to effort estimates in Section 4 |
| 4–5 | All phases present; most actions have deliverable and owner; some dependencies missing; one or two gaps not accounted for in the roadmap |
| 2–3 | Phases present but actions are high-level (e.g., "implement AI lifecycle controls") without mapping to specific gaps; dependencies not addressed |
| 0–1 | Roadmap is a generic list of activities not tied to the Gap Register |

---

### Section 8 — Ethana Coverage Analysis (10 points)

*Section 8.5 (Claims Firewall Review) is mandatory. A Section 8 without Section 8.5 scores maximum 4 points regardless of Section 8 body quality.*

| Score | Criteria |
|---|---|
| 9–10 | Every gap in the register has a Section 8 entry; Ethana capabilities are correctly categorised (Production [P] vs In Build [IB] vs Aspirational vs Cursory service vs Third party); Section 8.5 is complete with all four sub-tables populated; verbatim canonical model quotes present for all Production capability citations; all required caveats appear inline in Section 8 body; all Invalid References corrected before release |
| 7–8 | All gaps covered; one capability cited without a verbatim canonical model quote; Section 8.5 present but one sub-table is thin |
| 5–6 | Some gaps not covered in Section 8; Section 8.5 present but missing one or two Invalid References that should have been flagged; or a Production capability is cited without its mandatory caveat |
| 2–4 | Section 8 body is present but Section 8.5 is absent or incomplete — do not release without Section 8.5 |
| 0–1 | Section 8 absent; or an uncorrected In Build or Aspirational capability is cited as currently available (triggers HD2) |

**Common failures:**
- Citing Compliance Pack as closing Clause 9 evidence requirements — Compliance Pack is In Build [IB] and may not be presented as Production. The correct citation is "Regulatory Gap Analysis service (Cursory Service) using the production Immutable Audit Log as the evidence source."
- Citing Ethana Sentry / Edge as addressing Annex A Category 9 monitoring — Ethana Edge/Sentry is In Build [IB]. The correct entry is the Immutable Audit Log [P] for evidence collection; Sentry/Edge as a roadmap item only.
- Missing caveats: the Bias Scanner [P] carries a mandatory caveat (runtime text filter only; does not perform statistical bias audits) — citing it without the caveat for Annex A Category 2 bias controls overstates its coverage.

---

### Section 9 — Audit Readiness Assessment (5 points)

| Score | Criteria |
|---|---|
| 5 | ARS calculation shown with all four component scores and weighted result; Stage 1 verdict (Ready/Not Ready) stated with rationale; Stage 2 verdict stated with rationale; months to Stage 1 readiness estimated with basis; ARS is consistent with Section 10 |
| 3–4 | ARS calculation present; one component score poorly justified; Stage verdicts present but rationale thin |
| 1–2 | ARS present but component scores not shown; or Stage verdicts absent |
| 0 | Section missing or ARS contradicts Section 10 |

---

### Section 10 — Overall Maturity Score (4 points)

| Score | Criteria |
|---|---|
| 4 | AMS arithmetic shown (per-clause ratings, clause average, Annex A counts); ARS total stated consistently with Section 9; Certification Classification correctly determined by the classification table; months to readiness stated; classification does not grant Certification Ready when Critical gaps are open (HD6) |
| 3 | AMS and ARS present; one arithmetic step not shown; Classification correct |
| 1–2 | AMS present but no arithmetic shown; or Classification is borderline but the reviewer applied the wrong threshold (e.g., AMS 79 classified as Certification Ready) |
| 0 | Certification Ready classification with open Critical gaps (triggers HD6); or Section 10 absent |

---

## Score Thresholds and Release Criteria

| Score | Classification | Release Action |
|---|---|---|
| 95–100 | Exemplary | Release as final. Suitable for inclusion in the examples library as a calibration anchor. |
| 85–94 | Acceptable | Release as final. Note any dimensional weaknesses for the next review cycle. |
| 70–84 | Below standard | Do not release. Identify specific failing sections and revise. |
| Below 70 | Insufficient | Do not release. Major revision required. If Section 2 or Section 3 is the primary failure, the entire assessment should be re-run from Phase 2. |

**Note on the pass threshold:** 85/100 allows a reviewer to lose up to 15 points across all dimensions. In practice, the highest-value sections (Sections 2, 3, and 4 together total 51 points) must all score above 80% to reach the 85 threshold. A reviewer who adequately assesses all clauses and Annex A controls but produces a thin Remediation Roadmap can still pass. A reviewer who shortcuts the clause or control assessment cannot.

---

## Peer Review Checklist

Required before releasing any output with a Certification Ready or Near Ready classification. A separate reviewer (not the analyst who ran the assessment) must complete this checklist.

**Hard Disqualifier Confirmation:**
- [ ] Reviewer confirms Section 2 contains a Clause 4 assessment with an explicit maturity rating (HD1)
- [ ] Reviewer has independently checked Section 8.5 and confirms no capability listed as Invalid Reference remains uncorrected in Section 8 (HD2)
- [ ] Reviewer confirms all nine Annex A categories appear in Section 3, including those where all controls are N/A (HD3)
- [ ] Reviewer confirms every Gap Register entry in Section 4 cites a specific clause number or Annex A category (HD4)
- [ ] Reviewer confirms AMS in Section 10 is calculated from complete Section 2 and Section 3 data (HD5)
- [ ] Reviewer confirms no Critical gaps are open if the Certification Classification is Certification Ready (HD6)

**Clause Coverage Review:**
- [ ] Reviewer has sampled at least three clause maturity ratings and confirmed the rating matches the described current state
- [ ] Reviewer has confirmed ISO 27001 credit (if applied) does not extend to AI-specific requirements within credited clauses
- [ ] Reviewer has confirmed Clause 8 is assessed at the control level, not summarised at the clause level

**Annex A Review:**
- [ ] Reviewer has confirmed all supply chain controls (Category 5) are assessed — not marked N/A simply because third-party AI use is not formally recognised
- [ ] Reviewer has confirmed Bias Scanner [P] is cited with its mandatory runtime-filter caveat in Section 8 wherever it appears for Annex A Category 2
- [ ] Reviewer has confirmed Compliance Pack [IB] does not appear as a Production capability anywhere in Section 8

**Scoring Review:**
- [ ] Reviewer confirms AMS arithmetic is correct (per-clause ratings, clause average, Annex A coverage formula)
- [ ] Reviewer confirms ARS arithmetic is correct (four component scores, weights applied)
- [ ] Reviewer confirms Certification Classification is consistent with both AMS and ARS and Critical gap count

---

## Calibration Reference

The three worked examples in `examples.md` serve as scoring anchors.

| Example | Scenario | Key calibration challenge | Expected hard disqualifiers | Expected score |
|---|---|---|---|---|
| Example 1 | Indian private bank — preparing for certification alongside RBI programme | Correctly rate Clause 8 at maturity 1 despite existence of some model risk documentation; correctly cite Immutable Audit Log [P] with evidence caveat rather than as a full monitoring programme | None if correctly executed; HD2 if Compliance Pack [IB] used for Clause 9 | 87–91 — detailed clause and Annex A assessment; one or two minor calibration issues |
| Example 2 | EU fintech — extending ISO 27001 to AIMS | Correctly apply ISO 27001 credit on Clauses 4–7 without over-crediting AI-specific requirements; correctly identify Annex A gaps not covered by ISO 27001 | None if credit is applied correctly; HD2 if Discovery [RM] is cited as operational | 88–92 — ISO 27001 credit is the calibration test; AI-specific gaps within credited clauses must still be identified |
| Example 3 | UK retail group — greenfield, no management system | Correctly assign maturity 0 across most clauses without omitting them; correctly exclude Workspace [Aspirational] and Visual Agent Builder [Aspirational] from Section 8 | HD6 if reviewer classifies as Near Ready despite Critical gaps; HD2 if Aspirational capabilities cited | 86–90 — greenfield assessment is straightforward; the calibration test is the Claims Firewall Review for Aspirational capabilities |
