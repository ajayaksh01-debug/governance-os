# Ethana Solution Mapping — Evaluation Rubric

This rubric is used to score every output produced by the Ethana Solution Mapping skill. Score before releasing any output. Apply the hard disqualifier check first.

---

## Hard Disqualifier

**Check this before scoring. If any condition is true, do not release the output.**

| Condition | Check |
|---|---|
| Any Aspirational capability (Workspace features, Visual Agent Builder) appears in Section 3 (Proposal-Safe Capabilities) | [ ] Not present |
| Any In Build item is framed as a proposal deliverable in Section 3 | [ ] Not present |
| "ISO 27001 certified", "SOC 2 Type II certified", or "HIPAA compliant" appear as positive claims for Ethana | [ ] Not present |
| Workspace or Visual Agent Builder appear in Section 8 (Competitive Positioning) as Ethana's production capabilities | [ ] Not present |

**If any item above is checked, the output is automatically disqualified regardless of total score.** Remove the offending content, re-run Phase 7 quality check, and re-score.

---

## Scoring Overview

| # | Dimension | Points |
|---|---|---|
| 1 | Claims Firewall Compliance | 25 |
| 2 | Requirement Coverage Completeness | 10 |
| 3 | Canonical Model Accuracy | 15 |
| 4 | Coverage Confidence Calibration | 10 |
| 5 | Proposal Language Specificity | 10 |
| 6 | Cursory Bridge Quality | 8 |
| 7 | Competitive Positioning Quality | 8 |
| 8 | Commercial Motion Appropriateness | 7 |
| 9 | Sector Appropriateness | 5 |
| 10 | Gap Register and Executive Summary Quality | 2 |
| **Total** | | **100** |

**Pass threshold: 70/100**

---

## Dimension 1: Claims Firewall Compliance — 25 points

The primary quality gate. No output that fails this dimension at zero may be released for a formal proposal or RFP response.

| Score | Criteria |
|---|---|
| 22–25 | Section 5 (Prohibited Claims) is present, complete, and explicitly lists all Aspirational and In Build items relevant to the engagement. No prohibited claim appears in Section 3. No certification is claimed. Section 4 items are clearly labelled as roadmap and appear in no proposal deliverable. |
| 16–21 | Section 5 is present but incomplete (misses one or two relevant prohibited items). All claims in Section 3 are still correct — the gap is in documentation, not in what was claimed. |
| 8–15 | One In Build item appears in Section 3 without clear roadmap labelling, but it is not framed as a deliverable. Or: Section 5 is absent but Section 3 contains only Production items. |
| 1–7 | A significant compliance gap exists: an In Build item is framed as a near-term deliverable, or a certification is mentioned as pending without disclosure that it is not certified, or Section 5 is absent and the output would require substantial revision before use. |
| 0 | Any Aspirational capability appears in Section 3, any certification is positively claimed, or Section 5 is entirely absent with unchecked prohibited claims present. (Hard disqualifier territory — also triggers automatic disqualification above.) |

---

## Dimension 2: Requirement Coverage Completeness — 10 points

| Score | Criteria |
|---|---|
| 9–10 | Every requirement extracted in Phase 1 appears in Section 1 with a CCS score and disposition. No requirement is silently dropped. |
| 6–8 | One or two requirements are missing from Section 1 but appear in the correct output section (Section 5, 6, or 7). The omission is from the Coverage Map only, not from the overall output. |
| 3–5 | Two or more requirements are missing from Section 1. Some appear later in the output but the Coverage Map does not give a complete picture. |
| 0–2 | Three or more requirements are absent from Section 1, or the Coverage Map is so incomplete that the overall coverage story in Section 2 is unreliable. |

---

## Dimension 3: Canonical Model Accuracy — 15 points

| Score | Criteria |
|---|---|
| 13–15 | Every capability status in Section 1 and Section 3 is sourced from canonical-product-model.md. All mandatory caveats from that file are reflected in Section 3 language. No status is sourced from the marketing playbook, claims-matrix.md, or derived repository files. |
| 9–12 | All status determinations are correct. One or two mandatory caveats from canonical-product-model.md are missing from Section 3 (e.g., the NHI caveat for MCP Broker is absent), but no incorrect status was assigned. |
| 5–8 | One capability status is incorrect — a capability is labelled Production when it is In Build, or vice versa. No Aspirational capability is mislabelled as Production. The error is from the canonical-product-model.md being referenced incorrectly, not from using a prohibited source. |
| 0–4 | A capability is labelled Production when it is Aspirational, or a prohibited derived file (claims-matrix.md, source-of-truth.md) was used as the status source, resulting in an incorrect status determination. |

---

## Dimension 4: Coverage Confidence Calibration — 10 points

| Score | Criteria |
|---|---|
| 9–10 | CCS scores in Section 1 are consistent with the calibration anchors in workflow.md Phase 4. In Build and Aspirational capabilities score 0. Production capabilities score based on requirement-specific fit, not capability-generic quality. The aggregate CCS in Section 2 is the correct arithmetic average of Section 1 scores. Coverage characterisation (Platform-Primary / Mixed / Cursory-Primary) matches the distribution. |
| 6–8 | CCS scores are broadly correct but one or two are more than 15 points off the expected calibration. Aggregate and characterisation are still correct. |
| 3–5 | CCS scores are present but miscalibrated in multiple cases. An In Build capability has a non-zero CCS (other than an anticipated future CCS annotation). Or: the aggregate CCS does not match Section 1 scores, or the coverage characterisation does not match the distribution. |
| 0–2 | CCS scores are absent from three or more requirements, or In Build and Aspirational items have non-zero current CCS scores, or the aggregate CCS is not computed. |

---

## Dimension 5: Proposal Language Specificity — 10 points

| Score | Criteria |
|---|---|
| 9–10 | Every Production capability in Section 3 is described with specific, quotable language. Named feature (not product line). Specific metric where available (sub-200ms p95, 21 OWASP probes, insert-only DB-layer immutability, ~50ms gateway overhead). No generic language ("Ethana provides AI security"). All mandatory caveats from canonical-product-model.md are included inline. Language register matches `output_mode`. |
| 6–8 | Language is specific but one or two entries use product-level description ("Ethana Build provides audit logging") rather than feature-level ("Ethana's Immutable Audit Log captures every gateway-routed AI call in a tamper-proof, insert-only event store"). No incorrect claims. |
| 3–5 | Multiple entries use generic or product-level language. One mandatory caveat is missing. Language register is wrong for the output mode (e.g., formal proposal language used in a discovery output). |
| 0–2 | Section 3 uses generic language throughout, or is missing for one or more Production capabilities. No metrics or specific feature names. |

---

## Dimension 6: Cursory Bridge Quality — 8 points

| Score | Criteria |
|---|---|
| 7–8 | Every gap (In Build, Aspirational, or Not addressed) in Section 6 has a specific Cursory service named. The service is from the Cursory services catalogue. A description of what it delivers for this specific gap is included. Bridge is positioned alongside any adjacent Production capability. |
| 5–6 | One or two gaps have generic bridge recommendations ("consider Cursory advisory") rather than a named service. All gaps that require a bridge have at least one. |
| 2–4 | Three or more gaps have generic or absent bridge recommendations. Or: a bridge is recommended for a gap that is actually a hard Aspirational item (bridge is inappropriate — gap register is the correct routing). |
| 0–1 | Section 6 is absent, or the majority of gaps have no bridge recommendation, or a Cursory service is named that does not exist. |

**Standard Cursory bridge mapping (verify these are the services named):**

| Gap | Bridge service |
|---|---|
| Shadow AI inventory | AI Inventory & Classification |
| Formal bias audit | Specialist firm referral (not Cursory) |
| Compliance evidence / regulatory response | Regulatory Gap Analysis |
| Governed chat / RAG architecture | Advisory on Build Gateway + customer-built application |
| Agent orchestration (DAG / CrewAI) | Advisory on LangGraph / CrewAI via Build MCP Broker |
| Red teaming (managed) | Red Teaming as a Service |
| Policy design / guardrail rule authoring | Policy & Control Design |
| On-prem at Tier 1 bank scale | Ethana Implementation Service |
| SCIM / offboarding automation | Governance Programs (manual offboarding policy) |
| EU AI Act documentation (Annex IV) | Regulatory Gap Analysis |
| ISO 27001 / SOC 2 readiness | Regulatory Gap Analysis + timeline advisory |

---

## Dimension 7: Competitive Positioning Quality — 8 points

| Score | Criteria |
|---|---|
| 7–8 | Section 8 identifies the two or three most relevant alternatives for this requirement set. For each: Ethana's specific Production differentiator is named (not generic "we're better"), Ethana's honest gap is stated (where the competitor has production capability Ethana lacks), a win condition and loss condition are both included. Claims firewall applied — no Aspirational Ethana capability used in comparison. |
| 5–6 | One competitor entry lacks a loss condition, or Ethana's differentiator is described at product level rather than capability level. All comparisons are honest. |
| 2–4 | One competitor comparison uses an In Build or Aspirational Ethana capability as a differentiator ("Ethana will have Workspace which competes with Copilot Studio"). Or: the most relevant competitors for this requirement set are not identified. |
| 0–1 | Section 8 is absent. Or: Section 8 uses Aspirational Ethana capabilities (Workspace, Visual Agent Builder) as production competitive claims. |

---

## Dimension 8: Commercial Motion Appropriateness — 7 points

| Score | Criteria |
|---|---|
| 6–7 | Motion type is consistent with the decision tree in workflow.md Phase 6. SOC 2 blocker → Advisory-First. Aspirational primary requirements + low CCS → Advisory-Only or Advisory-First. High CCS, no blocker → Platform-First or Land-and-Expand. Design Partner requires explicit disclosure. All four elements present: motion type, entry product, deal guardrails, success criteria. |
| 4–5 | Motion type is correct but one of the four elements (entry product, deal guardrails, success criteria, expansion path) is absent or insufficiently specific. |
| 2–3 | Motion type is correct but the deal structure conflicts with the motion (e.g., Advisory-First motion with a Build license in Phase 1). Or: motion type is inconsistent with the sector gating output (SOC 2 blocker present but Platform-First selected without justification). |
| 0–1 | Section 9 is absent. Or: motion type violates sector gating (Platform-First for BFSI with SOC 2 blocker and no exception documented). |

---

## Dimension 9: Sector Appropriateness — 5 points

| Score | Criteria |
|---|---|
| 5 | All BFSI-specific cautions are reflected: SOC 2 blocker flagged, ISO 27001 not claimed, on-prem scale caveat included if applicable, Edge and Workspace not led in BFSI proposals. For healthcare: HIPAA bridge present. For government: air-gapped caveat present if applicable. |
| 3–4 | Sector gating is applied but one caution is missing (e.g., on-prem scale caveat absent in a BFSI on-prem engagement, or ISO 27001 mentioned as achievable without caveat). |
| 1–2 | A significant sector-specific error: BFSI proposal includes Edge or Workspace as a feature. Or: ISO 27001 is presented as certified in a proposal context. |
| 0 | No sector gating applied when sector was provided. Or: a BFSI proposal actively claims SOC 2 certification. |

---

## Dimension 10: Gap Register and Executive Summary Quality — 2 points

| Score | Criteria |
|---|---|
| 2 | Section 7 (Gap Register) documents all unaddressable requirements with a best available alternative noted. Section 10 (Executive Summary) is 200–250 words, written last, reflects the full analysis, and is suitable for a customer document. |
| 1 | One of the two sections meets the standard; the other does not. |
| 0 | Both sections are absent or so brief as to be non-functional. |

---

## Score Thresholds

| Score | Label | Disposition |
|---|---|---|
| 85–100 | Exemplary | Release. May be used in formal proposals, RFP responses, and customer presentations. |
| 70–84 | Acceptable | Release. Suitable for formal use. Note any dimensional weaknesses to address in the next iteration. |
| 55–69 | Preliminary | Release only for discovery conversations. Acknowledge limitations. Do not use in formal proposals or RFP responses without revision. |
| < 55 | Do not release | Document specific deficiencies by dimension. Address before release. |

---

## Peer Review Checklist

Required before releasing any output scored 70–84 (Acceptable) for a formal proposal to a BFSI or Healthcare customer:

**Claims Review:**
- [ ] Reviewer has read Section 5 (Prohibited Claims) in full
- [ ] Reviewer has checked Section 3 against Section 5 (no overlap)
- [ ] Reviewer has confirmed no certification claims appear anywhere in the document

**Competitive Positioning Review:**
- [ ] Reviewer has confirmed that Workspace and Visual Agent Builder do not appear in Section 8 as Ethana production capabilities
- [ ] Reviewer has confirmed that the loss conditions in Section 8 are honest and present

**Commercial Motion Review:**
- [ ] Reviewer has confirmed the motion type matches the sector gating output
- [ ] Reviewer has confirmed the deal guardrails exclude all In Build and Aspirational items
- [ ] Reviewer has confirmed that no delivery date commitment exists for any In Build capability

**BFSI Specific (when applicable):**
- [ ] SOC 2 blocker is documented in Section 9 deal guardrails
- [ ] Advisory-First motion is selected or a documented exception is noted

---

## Calibration Reference

These three worked examples in `examples.md` serve as calibration anchors.

| Example | Sector | Primary challenge | Expected motion | Expected CCS average |
|---|---|---|---|---|
| Example 1: Indian Private Bank LLM Credit AI | BFSI (India) | SOC 2 blocker; Build strong match; bias audit gap | Advisory-First | 67.7/100 (Platform-Primary characterisation); SOC 2 at 0 is a procurement blocker not a coverage signal; key items: Gateway 90, Injection 92, Audit Log 88, Bias Scanner 18 (supplemental runtime only) |
| Example 2: European Fintech Shadow AI Discovery | Fintech (EU, UK) | Most requirements In Build; Build is the bridgehead | Land-and-Expand | ~25 overall; In Build-heavy profile |
| Example 3: Enterprise RFP with Aspirational Traps | General Enterprise | Workspace / Visual Builder traps; Build solid | Land-and-Expand | ~50 overall; bifurcated (90s on Build; 0s on traps) |

An output scoring 80+ for Example 1 but 30 for Example 3 is likely failing the Claims Firewall check — the Aspirational traps in Example 3 must be caught and scored 0, not claimed.
