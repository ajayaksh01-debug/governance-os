# AI Incident Analysis — Evaluation Criteria and Scoring Rubric

## Purpose

This document defines the quality criteria for AI incident analyses produced using this skill. It provides:
- A scoring rubric for each output section
- A pass/fail threshold and release criteria
- Common failure modes and how to correct them
- A peer review checklist for high-stakes analyses

Every completed analysis must be scored before release. An analysis scoring below 70/100 must be revised or reclassified as preliminary pending additional information.

---

## Scoring Overview

| Section | Maximum Score | Weight Rationale |
|---|---|---|
| 1. Incident Summary | 10 | Foundation of the analysis — must be accurate |
| 2. Root Cause Analysis | 15 | Highest weight; differentiates useful analysis from surface description |
| 3. Risk Category | 5 | Objective classification; low complexity but must be correct |
| 4. Control Failures | 15 | Actionability depends on accurate control failure identification |
| 5. Applicable Frameworks | 10 | Framework mapping is a core skill output |
| 6. Regulatory Implications | 10 | High value to compliance audience; jurisdiction accuracy is critical |
| 7. BFSI Impact | 5 | Sector-specific; weighted lower as not always applicable |
| 8. Lessons Learned | 10 | Transferability and generalisability determine long-term value |
| 9. Recommended Controls | 15 | Actionability; the analysis must produce something implementable |
| 10. Executive Summary | 5 | Clarity and compression of key findings |
| **Total** | **100** | |

---

## Section-by-Section Rubric

### Section 1 — Incident Summary (10 points)

| Score | Criteria |
|---|---|
| 9–10 | Factually accurate, concise (≤200 words), covers who/what/when/how/impact, distinguishes confirmed facts from inferences, AI-specific dimension is clear, no technical jargon, suitable for executive audience |
| 7–8 | Mostly meets the above; minor omissions in who/what/when/how/impact; slight use of jargon; within 220 words |
| 5–6 | Covers the incident but misses at least one key dimension; some blurring of confirmed facts and inferences; borderline executive-accessible |
| 3–4 | Incomplete or inaccurate summary; significant missing information; not clearly executive-ready |
| 0–2 | Missing, incorrect, or unsuitable for release |

**Common failures:**
- Stating inferences as facts (e.g., "The attacker used X" when this is not confirmed)
- Missing the impact dimension — the summary covers what happened but not what it cost
- Technical detail that belongs in root cause analysis, not the summary
- Over-length — summaries exceeding 250 words indicate a lack of synthesis

---

### Section 2 — Root Cause Analysis (15 points)

| Score | Criteria |
|---|---|
| 13–15 | Proximate cause stated precisely in one sentence; 5 Whys chain is logical and each level is genuinely distinct; root cause is actionable at the governance level (not "the model was wrong"); contributing factors are specific and non-redundant; analysis reaches a level where intervention is possible |
| 10–12 | 5 Whys chain is mostly sound with one weak link; root cause is correct category but imprecisely stated; contributing factors are relevant |
| 7–9 | Identifies contributing factors but does not clearly distinguish proximate cause from root cause; the "why" chain stops prematurely |
| 4–6 | Identifies what happened but not why; root cause is at the symptom level ("the AI produced biased outputs" rather than "no fairness evaluation was required") |
| 0–3 | Missing or descriptive rather than analytical |

**Common failures:**
- **Premature stopping:** The 5 Whys chain stops at a technical cause ("the model was trained on biased data") without asking why that was permitted (the governance failure)
- **Circular causation:** "The root cause was that no controls existed" without explaining why no controls existed
- **Over-attribution:** Blaming individuals rather than systems, processes, or governance structures
- **Under-attribution:** Attributing everything to a single cause when multiple contributing factors existed

---

### Section 3 — Risk Category (5 points)

| Score | Criteria |
|---|---|
| 5 | Primary category correctly assigned from taxonomy; secondary categories (if used) are applicable and not redundant with primary; classification is defensible and consistent with the root cause analysis |
| 3–4 | Primary category is correct but secondary categories are misapplied or missing where applicable |
| 1–2 | Primary category is arguable; analysis would be better served by a different classification |
| 0 | Missing or clearly incorrect |

**Note:** Risk categories should be consistent with the root cause. If the root cause is a governance failure, "Governance Failure" should be a primary or secondary category — not absent while a technical category appears as primary.

---

### Section 4 — Control Failures (15 points)

| Score | Criteria |
|---|---|
| 13–15 | All material control failures identified; each failure correctly typed (Preventive/Detective/Corrective) and classified (Absent/Inadequate design/Inadequate operation); descriptions are specific enough to be actionable; no control failures conflated or missed; consistent with root cause analysis |
| 10–12 | Most material controls identified; one or two minor omissions or misclassifications; descriptions are generally specific |
| 7–9 | Identifies the most obvious control failures but misses secondary failures; some descriptions are generic |
| 4–6 | Identifies that controls were absent but does not specify which controls; descriptions are not actionable |
| 0–3 | Missing or incorrect |

**Common failures:**
- Listing "lack of governance" as a single control failure instead of identifying the specific controls (AI use policy, vendor assessment, DLP, training programme) that were absent
- Confusing failure types: an absent control is categorically different from a control that existed but did not operate
- Including controls that are irrelevant to this incident
- Missing detective controls — analyses often identify absent preventive controls but miss absent detective controls (monitoring, logging, testing) that would have enabled earlier detection

---

### Section 5 — Applicable Frameworks (10 points)

| Score | Criteria |
|---|---|
| 9–10 | ISO 42001 clauses and Annex A controls correctly identified with specific references; NIST AI RMF functions correctly assigned to the right failure type with rationale; OWASP LLM Top 10 correctly applied where relevant (or correctly marked N/A); mappings are specific, not generic; cross-framework coherence (same incident mapped consistently across frameworks) |
| 7–8 | Correct in most respects; one framework mapping is generic or slightly misapplied |
| 5–6 | Correct framework identification but mapping is at the category level without specific clause/control references |
| 3–4 | Frameworks identified but not mapped to specific incident facts |
| 0–2 | Missing, incorrect, or frameworks confused with each other |

**Common failures:**
- Mapping everything to NIST GOVERN rather than identifying the specific function where the failure sits
- Citing ISO 42001 Clause 5 (Leadership) for every incident regardless of whether leadership was the failure point
- Applying OWASP LLM Top 10 to incidents involving non-LLM AI systems
- Omitting OWASP LLM Top 10 for incidents that are clearly LLM-related

---

### Section 6 — Regulatory Implications (10 points)

| Score | Criteria |
|---|---|
| 9–10 | Correct jurisdictions identified; specific regulatory provisions cited (not just framework names); notification obligations assessed and finding stated; enforcement consequences characterised accurately; if no regulatory implications, this is correctly stated with rationale |
| 7–8 | Correct jurisdictions and frameworks; specific provisions not always cited; notification obligation addressed |
| 5–6 | Major applicable regulations identified; provisions not cited; notification obligation not addressed |
| 3–4 | Regulatory implications listed generically without jurisdiction or provision specificity |
| 0–2 | Missing, incorrect, or jurisdiction-blind (stating EU regulations apply to a purely domestic US incident) |

**Common failures:**
- Treating GDPR as universally applicable regardless of whether EU personal data was involved
- Omitting notification obligation assessment — this is often the most time-sensitive implication for an affected organisation
- Conflating "this regulation exists" with "this regulation applies to this incident"
- Omitting BFSI-specific regulations for incidents involving financial institutions

---

### Section 7 — BFSI Impact (5 points)

| Score | Criteria |
|---|---|
| 5 | Applicability correctly determined; if applicable, specific BFSI use cases identified, regulatory frameworks named, and the specific BFSI risk characterised; if not applicable, rationale is stated |
| 3–4 | Applicability determination is correct; BFSI analysis is mostly complete with minor omissions |
| 1–2 | Section present but generic; does not connect the incident to specific BFSI use cases or regulatory frameworks |
| 0 | Missing or incorrectly determined as N/A when applicable |

---

### Section 8 — Lessons Learned (10 points)

| Score | Criteria |
|---|---|
| 9–10 | 3–5 lessons; each lesson is specific, actionable, and generalisable beyond this incident; applicability clearly defined (who does this apply to?); urgency characterised; no lesson is a restatement of the control failure (lessons should be transferable insights, not "implement DLP") |
| 7–8 | Good lessons but one is too specific to this incident to transfer; or urgency not characterised |
| 5–6 | Lessons are valid but generic ("have better AI governance"); not specific enough to act on |
| 3–4 | Lessons are restatements of control failures without the transferable insight |
| 0–2 | Missing or platitudinous |

**Common failures:**
- Confusing lessons with recommended controls: "Implement DLP" is a recommended control, not a lesson. The lesson is "technical controls must enforce policy because employee compliance at scale is not reliable."
- Over-specific lessons that only apply to the exact incident scenario and do not transfer
- Missing the behavioural or organisational lesson — focusing only on technical lessons when a governance or cultural lesson is more important

---

### Section 9 — Recommended Controls (15 points)

| Score | Criteria |
|---|---|
| 13–15 | All critical controls identified (those that would have prevented the incident); controls are specific and implementable (not just categories); complexity assessed realistically; priority assigned logically (Critical controls are those that would have prevented the incident; Medium controls would have reduced impact); framework references accurate; no duplication with control failures (failure = what was absent; control = what should be implemented) |
| 10–12 | Most critical controls identified; one missing or imprecisely described; priority slightly miscalibrated |
| 7–9 | Core controls present but missing important secondary controls; descriptions are generic |
| 4–6 | Controls are correct categories but not specific enough to implement |
| 0–3 | Missing, generic, or do not connect to the identified control failures |

**Common failures:**
- Recommending the same control multiple times with slightly different wording
- Setting every control to "Critical" priority (a list where everything is critical has no priority)
- Underestimating implementation complexity — "implement DLP" is not Low complexity for most organisations
- Missing the most impactful control because it is obvious (obvious controls still need to be stated explicitly)

---

### Section 10 — Executive Summary (5 points)

| Score | Criteria |
|---|---|
| 5 | 150–200 words; suitable for board or C-suite; accurately reflects the full analysis; covers what happened, root cause (in governance terms), the key control gap, and recommended action; no jargon; written last (reflects actual analysis findings, not a draft position) |
| 3–4 | Correct but slightly over length, or one element missing |
| 1–2 | Present but too technical, too long, or does not accurately reflect the body analysis |
| 0 | Missing or not executive-ready |

---

## Score Thresholds and Release Criteria

| Score | Classification | Release Action |
|---|---|---|
| 85–100 | Exemplary | Release as final; candidate for inclusion in examples library |
| 70–84 | Acceptable | Release as final |
| 55–69 | Below standard | Reclassify as preliminary; revise before final release |
| Below 55 | Insufficient | Do not release; major revision or analyst reassignment required |

---

## Peer Review Checklist (for high-stakes analyses)

High-stakes analyses — those covering incidents with direct client relevance, significant regulatory implications, or intended for external use — require peer review before release. Reviewer checklist:

**Factual accuracy**
- [ ] All stated facts are verifiable against the source material
- [ ] Inferences are clearly distinguished from confirmed facts
- [ ] No factual errors that would undermine the analysis's credibility

**Analytical soundness**
- [ ] The root cause analysis reaches a level actionable for governance (not purely technical)
- [ ] The 5 Whys chain is logically coherent at each step
- [ ] Control failures are genuinely causal, not post-hoc additions

**Framework accuracy**
- [ ] ISO 42001 clause references are correct
- [ ] NIST AI RMF functions are correctly assigned to the right failure dimension
- [ ] OWASP LLM Top 10 categories are correctly applied where used

**Regulatory accuracy**
- [ ] Jurisdictions are correctly determined as applicable or not applicable
- [ ] Specific provisions cited are correct
- [ ] Notification obligation assessment reflects current regulatory requirements

**Actionability**
- [ ] Recommended controls are specific enough to implement
- [ ] Priority ratings are defensible
- [ ] Implementation complexity assessments are realistic

**Tone and audience**
- [ ] Executive Summary is genuinely executive-accessible
- [ ] No section contains unexplained technical jargon
- [ ] Analysis is objective — neither alarmist nor dismissive

---

## Calibration Reference

To support consistent scoring across analysts, the three worked examples in `examples.md` serve as calibration anchors:

| Example | Expected Score Range | Key Differentiators |
|---|---|---|
| Samsung Source Code Leak | 88–95 | High-evidence incident with clear governance root cause; straightforward framework mapping; strong control failure identification |
| Slack AI Indirect Injection | 85–92 | High-evidence technical incident; requires OWASP LLM mapping sophistication; BFSI impact requires inference |
| Amazon Recruitment AI Bias | 88–95 | Well-documented incident with multi-layer root cause; requires fairness framework knowledge; regulatory implications span multiple jurisdictions |

New analysts should score each calibration example independently and compare against expected ranges before conducting scored analyses.
