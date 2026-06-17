# Ethana Capability Validation — Evaluation Rubric

This rubric is used to score every output produced by the Ethana Capability Validation skill. Apply the hard disqualifier check first. Score only after confirming no hard disqualifiers are triggered.

The pass threshold for this skill is **90/100**. Capability Validation is the foundational truth gate for all Ethana commercial and technical outputs. An error here propagates downstream into every Solution Mapping and Feature Mapping output that references the validated capability. The standard is correspondingly the strictest of the three skills.

---

## Hard Disqualifiers

**Check these before scoring. If any condition is true, do not release the output.**

| # | Condition | Check |
|---|---|---|
| 1 | Section 1 status is Production but canonical-product-model.md says In Build or Aspirational for this capability | [ ] Not triggered |
| 2 | Any Aspirational capability appears in Section 4 (Allowed Claims) in any context or at any CPL level | [ ] Not triggered |
| 3 | Any claim in Section 4 (Allowed Claims) expands the capability's scope, modality, certification, coverage, or performance beyond what canonical-product-model.md explicitly confirms — even if the base capability status is correctly Production | [ ] Not triggered |
| 4 | A contradiction between sources is visible in Section 3 (Evidence Register) — a source is marked "Contradicts" or "Expands" — but has no corresponding entry in Section 6 (Contradiction Log) | [ ] Not triggered |
| 5 | canonical-product-model.md is not present in Section 3 (Evidence Register) — the canonical model was not consulted | [ ] Not triggered |
| 6 | The Phase 9 Mandatory Traceability Gate was not completed — any of the 7 gate steps was skipped or is undocumented in Section 9 | [ ] Gate completed |
| 7 | Any entry in Section 4 (Allowed Claims) is tagged CPL-5 | [ ] Not triggered |

**If any condition above is triggered, the output is automatically disqualified regardless of the total score.** Correct the specific failure, re-run from Phase 9 Gate Step 1, and re-score from the beginning. Do not release a disqualified output under any time pressure.

**The most likely disqualifier triggers:**
- HQ3 (scope expansion in Section 4) — the most common failure; occurs when a claim is copied from a marketing source without DT4 verification
- HQ4 (undocumented contradiction) — occurs when a Reference Only source is reviewed but the contradiction it contains is not logged in Section 6
- HQ6 (gate not completed) — occurs on abbreviated validation paths where the evaluator omits the gate because "there were no contradictions"

---

## Scoring Overview

| # | Dimension | Points |
|---|---|---|
| 1 | Status Determination Accuracy | 30 |
| 2 | Evidence Register Completeness | 20 |
| 3 | ECS Computation Accuracy | 15 |
| 4 | Contradiction Documentation Quality | 15 |
| 5 | Claims Adjudication and CPL Assignment Quality | 10 |
| 6 | Escalation Recommendation Specificity | 7 |
| 7 | Audit Trail and Gate Completeness | 3 |
| **Total** | | **100** |

**Pass threshold: 90/100**

---

## Dimension 1: Status Determination Accuracy — 30 points

The primary scoring dimension. A wrong status determination is the most serious failure this skill can produce.

| Score | Criteria |
|---|---|
| 28–30 | Section 1 status exactly matches canonical-product-model.md. The verbatim canonical model entry is quoted. All mandatory caveats from the canonical entry are recorded in Section 1. Scope boundaries are stated accurately. Status confidence band correctly maps to the ECS in Section 7. No status is sourced from a secondary or non-canonical file. |
| 21–27 | Status is correct. Verbatim quote is present. One or two mandatory caveats from the canonical model are absent from Section 1 (though they may be present in Section 4 claim entries). Scope boundaries are partially stated — one known boundary is absent. Status confidence band is correctly assigned. |
| 10–20 | Status is correct but the mandatory caveats are absent from Section 1 and from Section 4 claim entries — they are effectively invisible in the output. Or: scope boundaries are significantly understated, giving a false impression of broader capability than the canonical model confirms. Or: status is sourced from an Approved Secondary source when the canonical model also has an entry that was not consulted. |
| 0–9 | Status is incorrect — In Build adjudicated as Production, or Aspirational adjudicated as In Build. Or: canonical-product-model.md was not the primary source and a secondary or derived file was used instead. Or: the canonical entry does not exist and a status was invented from secondary sources without escalation. |

**Note:** A status determination error that produces a Production claim for an In Build or Aspirational capability also triggers Hard Disqualifiers 1 and 2. Scoring this dimension at 0–9 is likely accompanied by automatic disqualification.

---

## Dimension 2: Evidence Register Completeness — 20 points

| Score | Criteria |
|---|---|
| 18–20 | Section 3 lists every source that was consulted. canonical-product-model.md appears first. All Approved Secondary sources (product-architecture-investigation.md, use-cases.md) are documented with their claim or "Silent." All Reference Only sources consulted are documented with their claim and consistency assessment. No prohibited source appears with an authority level above "Reference Only." Authority levels are correctly assigned to all sources. |
| 13–17 | All consulted sources are listed. One or two are missing authority level assignments, or one Reference Only source has an authority level of "Approved Secondary" — a classification error that inflates its ECS contribution. The underlying status determination is still correct. |
| 7–12 | An Approved Secondary source that was available and relevant was not consulted — its omission would have changed the ECS computation by ≥ 10 points (e.g., product-architecture-investigation.md has a relevant entry that would have added +15 to ECS). Or: a Reference Only source that makes a claim contradicting the canonical model was reviewed but not logged in Section 3. |
| 0–6 | Two or more relevant sources were not consulted. Or: a prohibited source (capability-status.md, source-of-truth.md, ethana-status-reconciliation.md) appears in Section 3 with authority level "Primary" or "Approved Secondary." Or: Section 3 is absent. |

---

## Dimension 3: ECS Computation Accuracy — 15 points

ECS computation accuracy covers both the arithmetic and the correctness of the path determination and CPL derivation. The ECS and CPL are computed separately but must be consistent with each other.

| Score | Criteria |
|---|---|
| 14–15 | The correct path (A/B/C/D/E/F) is identified for the claimed status. Every applicable adjustment is applied with its correct value. The sum is correct. The ECS band is correctly assigned from the total. For CPL: every Allowed Claim in Section 4 has a CPL consistent with DT6 given the ECS and capability status. The mandatory caveat split (CPL-1 with caveat embedded vs. CPL-2 without) is correctly applied for claims about the same capability. |
| 10–13 | Path is correct. Arithmetic has a minor error (one adjustment applied at the wrong value, or one adjustment missed) that changes the ECS by fewer than 10 points but does not change the ECS band. CPL assignments are all correct. Or: CPL is correct for the ECS band but the mandatory caveat split is not applied — all Production claims at the same ECS receive the same CPL regardless of whether the caveat is embedded. This is a CPL completeness error, not a CPL logic error. |
| 5–9 | Path is correct but arithmetic has an error that changes the ECS band (e.g., computed as Corroborated when it should be Canonical-only). CPL assignments may be technically consistent with the wrong ECS but incorrect given the true ECS. Or: Path B, C, or E applies (In Build or Aspirational with a Production claim) but Path A was used instead, resulting in a higher ECS than the model permits. |
| 0–4 | Path determination is incorrect. Or: ECS computation is not shown — the arithmetic is absent and the score appears without derivation. Or: ECS arithmetic contains an error large enough to inflate the ECS from one band to a materially higher one (e.g., Insufficient scored as Corroborated). |

---

## Dimension 4: Contradiction Documentation Quality — 15 points

| Score | Criteria |
|---|---|
| 14–15 | Every source conflict visible in Section 3 has an entry in Section 6. Each Section 6 entry states: Source A's claim verbatim, the canonical model's position, the nature of the contradiction, the adjudication (which source prevails and why), the resolution adopted in Section 1, and the ECS adjustment applied. The adjudication reasoning is reproducible — a reviewer with no prior knowledge of the case could re-adjudicate correctly from Section 6 alone. If no contradictions exist, Section 6 states this explicitly. |
| 10–13 | All contradictions are documented. One or two entries are missing the ECS adjustment or the adjudication reasoning is stated as a conclusion ("canonical model prevails") without the reasoning behind the authority hierarchy decision. All entries reach the correct resolution. |
| 5–9 | One contradiction was found in Section 3 but is absent from Section 6 — it was noted but not formally adjudicated. Or: a contradiction is documented in Section 6 but the resolution adopted in Section 1 differs from the Section 6 adjudication without explanation. Or: Section 6 is present but does not follow the required format, making the reasoning not independently reproducible. |
| 0–4 | A contradiction is present in Section 3 (source marked "Contradicts" or "Expands") but Section 6 is absent or has no entry for it. This also triggers Hard Disqualifier 4 — automatic disqualification. |

---

## Dimension 5: Claims Adjudication and CPL Assignment Quality — 10 points

This dimension covers both the quality of the claim language (is it specific and quotable?) and the correctness of CPL assignment (does each claim have the right permission level?).

| Score | Criteria |
|---|---|
| 9–10 | Every Section 4 (Allowed Claims) entry contains specific, quotable language — not "you can say it's reliable" but an exact sentence ready for use. Each entry has a CPL correctly derived from DT6. CPL-2 entries include the mandatory caveat text. Entries for the same capability with different CPLs (e.g., one with caveat embedded = CPL-1, one without = CPL-2) demonstrate the claim-specific CPL model correctly. Every Section 5 (Prohibited Claims) entry has CPL-5, a specific prohibition reason from the approved list, and a named risk if used. |
| 7–8 | All CPL assignments are correct. One or two Section 4 entries use language that is correct but not quotable ("Ethana's audit capabilities are strong") — requires rewrite before use. Mandatory caveat is present in CPL-2 entries. Section 5 entries have CPL-5 and prohibition reasons but one or two are missing the risk assessment. |
| 4–6 | One CPL assignment is incorrect — a claim that should be CPL-3 (contested) is assigned CPL-2, or a claim that should be CPL-5 (scope expansion) is assigned CPL-2. Or: the mandatory caveat split is not applied — all claims for the same Production capability receive the same CPL regardless of whether the caveat is embedded, losing the claim-specific distinction. |
| 0–3 | Two or more CPL assignments are incorrect. Or: Section 4 contains a claim with CPL-5 (automatic disqualification — HQ7). Or: Section 4 is absent — no Allowed Claims are produced despite the capability being Production with evidence. Or: claims in Section 4 are so generic they cannot be used without complete rewrite. |

---

## Dimension 6: Escalation Recommendation Specificity — 7 points

*Score only when ECS < 45 or status is Unresolved. If ECS ≥ 45 and Section 8 correctly states no escalation is required, score 7/7.*

| Score | Criteria |
|---|---|
| 6–7 | Section 8 names the specific escalation recipient (not "the product team" but "canonical model maintainer" or "Ethana engineering lead"). The specific question is answerable — it identifies the exact conflict or gap and asks for a specific confirmation, correction, or canonical model update. The interim position is stated: what may and may not be said while escalation is pending. Downstream blocks are listed by output type (e.g., "blocks any Solution Mapping output that includes this capability in Section 3"). |
| 4–5 | Escalation recipient is named. Question is specific but incomplete — it identifies the conflict but does not include the context needed for the recipient to answer it without additional research. Interim position is present. Downstream blocks are named generically ("blocks downstream use") rather than by output type. |
| 2–3 | Escalation recipient is named generically ("ask engineering"). Question is generic ("can you confirm this capability's status?"). Interim position is absent — the output leaves the requesting team without guidance on what to say while waiting. |
| 0–1 | Section 8 is absent when ECS < 45. Or: Section 8 states no escalation is required when ECS < 45 and status is Unresolved. Or: escalation is recommended but targets the wrong recipient (e.g., marketing is asked to confirm a technical capability status). |

---

## Dimension 7: Audit Trail and Gate Completeness — 3 points

| Score | Criteria |
|---|---|
| 3 | Section 9 is present and contains all required fields: validation date, claims validated verbatim, sources checked in order, ECS arithmetic or reference, final status, CPL for each Section 4 claim, hard disqualifier check confirmation, Phase 9 gate completion with date, escalation status. |
| 2 | Section 9 is present and mostly complete. One or two required fields are absent (e.g., CPL assignments for Section 4 claims are not listed in Section 9, or the Phase 9 gate confirmation line is absent). |
| 1 | Section 9 is present but significantly incomplete — fewer than half the required fields are populated. The gate completion is not confirmed. |
| 0 | Section 9 is absent entirely. This also triggers Hard Disqualifier 6 — automatic disqualification. |

---

## Score Thresholds

| Score | Label | Disposition |
|---|---|---|
| 97–100 | Exemplary | Release. May be cited by Solution Mapping and Feature Mapping as the named validation authority for this capability. Suitable for customer-facing challenge situations where the claim basis must be disclosed. |
| 90–96 | Acceptable | Release. Note any dimensional weaknesses to address in the next validation cycle. Suitable for all downstream use. |
| 75–89 | Preliminary | Do not use in downstream skills. Internal review only. Revise the specific failing dimensions before re-scoring. Do not submit as the basis for a Formal Proposal or RFP response. |
| < 75 | Do not release | Document specific dimension failures. Address and re-run Phase 9 gate before re-scoring. |

---

## Peer Review Checklist

Required before releasing any output scored 90–96 (Acceptable) that will be cited in a formal customer deliverable (Formal Proposal, RFP Response, POC scope commitment).

**Status and Scope Review:**
- [ ] Reviewer has confirmed Section 1 status against canonical-product-model.md directly — not relying on the evaluator's Section 3 quote
- [ ] Reviewer has confirmed all mandatory caveats from the canonical model entry appear in Section 1 and in every relevant Section 4 claim
- [ ] Reviewer has read every Section 4 claim and confirmed none attributes scope, modality, certification, or performance the canonical model does not explicitly confirm

**CPL and Claims Review:**
- [ ] Reviewer has confirmed every Section 4 entry has a CPL
- [ ] Reviewer has confirmed that for claims about the same Production capability, the CPL-1 vs. CPL-2 distinction correctly reflects whether the mandatory caveat is embedded in the claim text
- [ ] Reviewer has confirmed every Section 5 entry is CPL-5 with a named prohibition reason

**Contradiction Review:**
- [ ] Reviewer has counted "Contradicts" or "Expands" rows in Section 3 and confirmed the count matches the number of Section 6 entries
- [ ] Reviewer has confirmed the adjudication in each Section 6 entry is reproducible — the reasoning is present, not just the conclusion

**Gate Review:**
- [ ] Reviewer has confirmed Section 9 contains the Phase 9 gate completion confirmation
- [ ] Reviewer has confirmed that no gate step is marked "not applicable" for a full validation run — abbreviated path applies only to Phases, not Gate Steps

---

## Calibration Reference

The five worked examples in `examples.md` serve as scoring anchors.

| Example | Capability | Primary challenge | Expected hard disqualifiers | Expected score |
|---|---|---|---|---|
| Example 1 | Immutable Audit Log | Two claims, two CPLs for the same capability; demonstrating claim-specific CPL with and without embedded caveat | None | 95–97 — clean validation, well-evidenced, gate confirmed |
| Example 2 | ISO 27001 certification | In Build canonical status; marketing playbook claims Production (certified); scope expansion on certification | HQ3 if evaluator puts the certified claim in Section 4; none if correctly routed to Section 5 | 90–93 if handled correctly; automatic disqualification if HQ3 triggered |
| Example 3 | MCP Security Broker | Core is Production (CPL-2); NHI module is In Build (CPL-5); sub-capability split required | HQ3 if NHI lifecycle claim appears in Section 4 | 91–94 if split handled correctly |
| Example 4 | Visual Agent Builder | Aspirational; proposed for Formal Proposal | HQ2 if any Aspirational claim appears in Section 4 | 92–95 if correctly prohibited; automatic disqualification if HQ2 triggered |
| Example 5 | Ethana Discovery | Roadmap slide claims Production; canonical says In Build; two ECS evaluations (Production claim vs. accurate In Build disclosure) | HQ3 if the Production claim is in Section 4 | 90–93 if contradiction correctly adjudicated and two-claim split handled |

**Calibration principle:** An output that correctly handles the primary challenge but omits the mandatory caveat from all Section 4 entries for that capability scores no higher than 21/30 on Dimension 1 (which alone prevents a 90/100 pass). Mandatory caveats are not optional — they are load-bearing parts of the claim.

An output that omits Section 6 (Contradiction Log) when a contradiction exists scores 0–4 on Dimension 4 and triggers Hard Disqualifier 4. No output with a triggered hard disqualifier may pass regardless of total score.
