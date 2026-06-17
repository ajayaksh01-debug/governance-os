# Ethana Feature Mapping — Evaluation Rubric

This rubric is used to score every output produced by the Ethana Feature Mapping skill. Score before releasing any output. Apply the hard disqualifier check first.

The pass threshold for this skill is **85/100**. Feature Mapping is a technical validation skill used to support POC commitments, RFI responses, and technical evaluation decisions. These outputs are more often acted upon directly by engineers and procurement teams than commercial proposals — a higher release standard applies.

---

## Hard Disqualifier

**Check this before scoring. If any condition is true, do not release the output.**

| Condition | Check |
|---|---|
| Any Aspirational capability (Workspace features, Visual Agent Builder) is described as technically available or demonstrable in any section | [ ] Not present |
| Any In Build feature appears in Section 5 (POC Feature Set) as includable without explicit "In Build — cannot be demonstrated" disclosure in that section | [ ] Not present |
| "ISO 27001 certified," "SOC 2 Type II certified," or "HIPAA compliant" appear as positive claims for Ethana | [ ] Not present |
| Any invented integration compatibility claim: a connector claimed as supported that is not in canonical-product-model.md or product-architecture-investigation.md; Azure AD, Okta, Splunk, Datadog, Kubernetes, or any other tool claimed as natively compatible without a confirmed source; an API integration path presented as available without a confirmed source; a deployment model claim that exceeds the confirmed scope | [ ] Not present |
| The mandatory arithmetic and traceability gate (Phase 7.2, Steps 1–6) has not been completed and documented | [ ] Gate completed |

**If any item above is checked, the output is automatically disqualified regardless of total score.** Remove the offending content, re-run the Phase 7 gate and quality check, and re-score from the beginning.

---

## Scoring Overview

| # | Dimension | Points |
|---|---|---|
| 1 | Claims Firewall Compliance | 25 |
| 2 | Feature Validation Accuracy | 20 |
| 3 | Technical Constraint Completeness | 15 |
| 4 | POC Readiness Assessment Quality | 12 |
| 5 | Integration Compatibility Accuracy | 10 |
| 6 | Substitution Analysis Quality | 8 |
| 7 | Technical Language Specificity | 7 |
| 8 | Prohibited Feature Claims Register | 2 |
| 9 | Sector Appropriateness | 1 |
| **Total** | | **100** |

**Pass threshold: 85/100**

---

## Dimension 1: Claims Firewall Compliance — 25 points

The primary quality gate. No output that fails this dimension at zero may be released for any technical evaluation, POC scope, or RFI response.

| Score | Criteria |
|---|---|
| 22–25 | Section 6 (Prohibited Feature Claims Register) is present and complete — all In Build and Aspirational features relevant to this evaluation are listed by feature name with their canonical status. No In Build feature appears in Section 5 as demonstrable without disclosure. No Aspirational feature appears in Sections 1, 3, 5, 7, or 9. No certification claim is made. Every TFS = 0 entry is correctly attributed to In Build or Aspirational status. Section 8 confirms no prohibited sources were used. |
| 16–21 | Section 6 is present but incomplete — one or two relevant In Build features are missing from it. All claims in Sections 1, 9, and 5 are still correct. The gap is in documentation completeness, not in what was claimed or proposed. |
| 8–15 | One In Build feature appears in Section 1 with a non-zero current TFS, without the required "Anticipated TFS when shipped" framing that clearly distinguishes current from future status. No Aspirational feature is mislabelled. The error is ambiguity, not an incorrect claim. |
| 1–7 | An In Build feature is included in Section 5 (POC Feature Set) without explicit "In Build" disclosure. Or: a certification is mentioned as "expected" or "in progress" without explicit statement that Ethana is not currently certified. Or: Section 6 is absent and the output would require substantial revision before use. |
| 0 | Any Aspirational feature appears as technically available. Any In Build feature is in Section 5 as a POC deliverable without disclosure. Any certification is positively claimed. (Hard disqualifier territory — also triggers automatic disqualification above.) |

---

## Dimension 2: Feature Validation Accuracy — 20 points

| Score | Criteria |
|---|---|
| 18–20 | Every feature in Section 1 is named exactly as it appears in canonical-product-model.md. Every technical description accurately reflects what the feature does and does not do in production. Performance figures match the canonical model. TFS scores are consistent with the calibration anchors in workflow.md Phase 3.2 — no score is more than 15 points from the nearest calibration anchor without explicit justification. No feature is described as doing something it does not do in production today. |
| 13–17 | All feature descriptions are accurate. One or two TFS scores are more than 15 points from the nearest calibration anchor, but no materially incorrect claim about feature capability results from the scoring deviation. |
| 7–12 | One feature is described with a material inaccuracy — a capability it does not have in production is implied or stated, or a known limitation (e.g., text-only modality for the PII Scanner, non-audit scope for the Bias Scanner) is absent from the description when it is directly relevant to the requirement. Or: an In Build feature is described with specific technical detail as if it were Production, without a current-vs-anticipated distinction. |
| 0–6 | Two or more features are materially inaccurately described. Or: an In Build or Aspirational feature is described with specific technical parameters as if available for evaluation today — even if the section is hedged with "coming soon." |

---

## Dimension 3: Technical Constraint Completeness — 15 points

| Score | Criteria |
|---|---|
| 13–15 | All hard technical limits relevant to this customer's context appear in Section 4. On-prem single-node throughput ceiling is documented when deployment is on-prem. PII Scanner text-only modality is documented when structured data scanning is in scope. Bias Scanner non-audit scope is documented when any bias requirement is present. MCP runtime compatibility requirement is documented when agent pipelines are in scope. Audit Log schema configurability limits are documented when the customer has asked about schema. Performance figures are stated with their scope — not extrapolated beyond the documented envelope. |
| 9–12 | All material constraints are documented. One or two minor constraints are absent — missing constraints that do not affect the customer's evaluation outcome for this specific engagement. No missing constraint creates a false impression of greater suitability. |
| 4–8 | One material constraint is absent from Section 4, and its absence creates a false impression — the evaluator would reasonably conclude the feature is more capable or broader in scope than it is. Example: PII Scanner text-only limitation absent when the customer explicitly asked about structured data. Or: Section 4 is present but a constraint documented there is contradicted by Section 9 claim language. |
| 0–3 | Two or more material constraints are absent. Or: Section 4 is absent entirely. Or: Section 9 contains a claim that directly contradicts a constraint that should have been in Section 4. |

---

## Dimension 4: POC Readiness Assessment Quality — 12 points

*Score only when poc_scope, upstream_skill_output, or an explicit POC feasibility question is the input. If not applicable, score 12/12 automatically.*

| Score | Criteria |
|---|---|
| 11–12 | Section 5 (POC Feature Set) includes specific, measurable test scenarios for each included feature — not generic descriptions. Technical prerequisites are named specifically by name and version where applicable. Success criteria are binary and observable. Estimated setup times are present. All excluded features are listed with specific, named exclusion reasons. No In Build feature appears in the POC Feature Set without explicit "In Build — cannot be demonstrated" disclosure in that section. |
| 8–10 | Test scenarios are present but one or two lack specific measurable success criteria, stating "the feature appears to work" rather than a named observable outcome. Prerequisites are mostly specific but one is described generically. No structural failures — In Build features are correctly excluded. |
| 4–7 | Test scenarios are too generic to guide a POC execution ("demonstrate the audit log"). Prerequisites are largely absent or generic ("provide a test environment"). Success criteria are qualitative. Or: one In Build feature is in the POC Feature Set without explicit In Build disclosure. |
| 0–3 | Section 5 is absent when the input included a POC scope or upstream Solution Mapping output. Or: the majority of included features lack executable test scenarios. Or: multiple In Build features appear in Section 5 without disclosure. |

---

## Dimension 5: Integration Compatibility Accuracy — 10 points

| Score | Criteria |
|---|---|
| 9–10 | Section 3 and Section 8 together confirm every integration claim with a traceable source in canonical-product-model.md or product-architecture-investigation.md. Unconfirmed integrations are labelled using the exact prescribed language. The distinction between Native Connector, SIEM Export, OIDC/SSO, API, Not Confirmed, and Gap is correctly applied throughout. No integration is claimed as "Supported" for a stack component not in an approved source. |
| 6–8 | All confirmed integrations are correctly classified. One or two unconfirmed integrations are described with slightly ambiguous language — not the exact prescribed phrasing — but no definitive unsupported compatibility claim is made. |
| 3–5 | One integration claim is made for a stack component not confirmed in any approved source, phrased as a soft assertion ("Ethana likely supports this," "this should work via the API"). Or: the distinction between OIDC/SSO (Production) and SCIM (In Build) is not clearly stated, creating ambiguity about what is available for the POC. |
| 0–2 | A definitive integration claim is made for a stack component that is not confirmed in any approved source. Or: the output claims native connector support for a tool that has no documented native integration. (Hard disqualifier territory if the claim is explicit — see above.) |

---

## Dimension 6: Substitution Analysis Quality — 8 points

*Score only when existing_tool_feature_list is provided. If not applicable, score 8/8 automatically.*

| Score | Criteria |
|---|---|
| 7–8 | Every feature in the existing tool's list is assigned a substitution category (Full / Partial / Complementary / Gap) with specific justification. Capability losses for Partial Substitutes are documented honestly and in full — not minimised. Migration path or integration approach is included for Full and Partial categories. Gap categories identify a specific bridge recommendation or state clearly that the customer should retain the existing tool. No In Build or Aspirational Ethana feature is used to claim substitution coverage it cannot provide. |
| 5–6 | All category assignments are correct. One or two entries are missing the migration path or have a generic bridge recommendation ("consider an alternative tool") rather than a specific one. |
| 2–4 | One substitution category is incorrectly assigned — a Gap is labelled Partial because an In Build Ethana feature is implicitly counted. Or: capability losses for Partial Substitutes are systematically minimised or omitted. |
| 0–1 | Section 7 is absent when existing_tool_feature_list was provided. Or: In Build features are systematically used to claim substitution coverage they cannot provide today. |

---

## Dimension 7: Technical Language Specificity — 7 points

| Score | Criteria |
|---|---|
| 6–7 | Section 9 (Technical Proposal Language) uses feature-level specificity throughout: performance metrics where confirmed, specific configuration parameter names, integration protocol specifics, data schema names. No generic product-level language ("Ethana provides AI security," "Ethana's platform addresses this"). Mandatory caveats from canonical-product-model.md are included inline within the claim text, not as separate paragraphs that could be detached. Language register matches the declared output_mode. |
| 4–5 | Language is specific for the majority of entries. One or two entries describe a feature at product level rather than feature level. Mandatory caveats are present but not always inline. |
| 2–3 | Multiple entries use product-level generic language. One or more mandatory caveats (Bias Scanner non-audit scope, on-prem single-node caveat, PII text-only modality) are absent from Section 9 for features where they should be inline. |
| 0–1 | Section 9 is absent. Or: language is generic throughout with no feature-level specifics, metrics, or configuration detail. |

---

## Dimension 8: Prohibited Feature Claims Register — 2 points

| Score | Criteria |
|---|---|
| 2 | Section 6 is present and lists every In Build and Aspirational feature relevant to this evaluation. Each entry is labelled with its canonical status and the prohibition scope (cannot be demonstrated / cannot be described as available). |
| 1 | Section 6 is present but missing one or two relevant entries. All entries that are present are correctly labelled with status and prohibition scope. |
| 0 | Section 6 is absent. Or: entries are present but missing canonical status labels. |

---

## Dimension 9: Sector Appropriateness — 1 point

| Score | Criteria |
|---|---|
| 1 | All sector-specific technical constraints are reflected: BFSI — SOC 2 and ISO 27001 not claimed as current certifications; on-prem single-node scale caveat documented when on-prem deployment is in scope. Healthcare — HIPAA-ready bridge noted if applicable. Government — air-gapped caveat and offline update process noted if applicable. |
| 0 | One or more sector-specific constraints absent when customer_sector requires them. Or: BFSI proposal positively claims SOC 2 or ISO 27001 certification status. |

---

## Score Thresholds

| Score | Label | Disposition |
|---|---|---|
| 92–100 | Exemplary | Release. Suitable for formal technical evaluations, RFI responses, POC scope commitments, and internal technical decision memos. |
| 85–91 | Acceptable | Release. Suitable for formal use with noted dimensional weaknesses. Peer review required before submitting to customer in BFSI or Healthcare contexts. |
| 70–84 | Preliminary | Release only for internal briefings and discovery conversations with the customer's technical team. Do not submit as a formal technical evaluation, RFI response, or POC scope commitment without revision. |
| < 70 | Do not release | Document specific deficiencies by dimension. Address before release. Do not use in any customer-facing context. |

---

## Peer Review Checklist

Required before releasing any output scored 85–91 (Acceptable) for a formal technical evaluation, RFI response, or POC scope commitment.

**Claims Review:**
- [ ] Reviewer has read Section 6 (Prohibited Feature Claims Register) in full
- [ ] Reviewer has checked Sections 1, 3, 5, 7, and 9 against Section 6 — no overlap
- [ ] Reviewer has confirmed no certification claims appear anywhere in the document
- [ ] Reviewer has confirmed no Aspirational feature appears in any active section

**Arithmetic and Traceability Review:**
- [ ] Reviewer has independently verified the TFS sum: listed all Section 1 TFS values and recomputed the average
- [ ] Reviewer has verified that Section 2 distribution band counts sum to total feature count
- [ ] Reviewer has confirmed that Section 8 (Evidence References) contains a source entry for every performance figure in Sections 1 and 9
- [ ] Reviewer has confirmed that Section 8 contains a source entry for every "Supported" integration claim in Section 3

**Integration Claims Review:**
- [ ] Reviewer has confirmed every "Supported" claim in Section 3 traces to an approved source
- [ ] Reviewer has confirmed "Not Confirmed" language is applied exactly as specified for all unverified integrations
- [ ] Reviewer has confirmed no integration is claimed as "Supported" without an approved source

**POC Scope Review (when applicable):**
- [ ] Reviewer has confirmed every feature in Section 5 is Production status in canonical-product-model.md
- [ ] Reviewer has confirmed every excluded feature has a specific, named exclusion reason
- [ ] Reviewer has confirmed all test scenarios have measurable, binary success criteria

**BFSI Specific (when applicable):**
- [ ] SOC 2 and ISO 27001 are explicitly identified as In Build — not certified — if referenced
- [ ] On-prem single-node scale constraint is documented in Section 4 if on-prem deployment is in scope

---

## Calibration Reference

These three worked examples in `examples.md` serve as scoring anchors.

| Example | Context | Primary challenge | Expected characterisation | Expected average TFS |
|---|---|---|---|---|
| Example 1: BFSI Audit Log Deep Dive | BFSI (India) — 5 technical questions about the Immutable Audit Log from an enterprise architect | On-prem throughput uncertainty; insert-only vs. DB-layer distinction; schema configurability limits | POC-Ready with Conditions | ~70.8 overall; 4 of 5 features Viable; on-prem throughput scores Thin due to unconfirmed ceiling at 50K calls/day |
| Example 2: LangSmith Substitution Analysis | General Enterprise — full LangSmith feature list for substitution | Prompt playground and dataset management are Gaps; guardrails and routing are Partial Substitutes; audit log and cost tracking are Full Substitutes | Limited POC Scope | ~53.9 overall; two Aspirational Gaps drag the average; three strong Production features (SIEM export 90, tracing 85, cost tracking 82) |
| Example 3: Post-Solution-Mapping POC Scope Validation | UK Financial Services — 60-day POC, stack: Azure AD, Datadog, GitHub Actions, LangChain | CI/CD gate and SCIM are In Build exclusions; MCP Broker requires LangChain prerequisite confirmation; Datadog SIEM export confirmed | POC-Ready | ~84.5 overall; 6 of 6 Production features at Viable or Ready; conditions limited to OIDC setup and LangChain version confirmation |

An output scoring 90 for Example 3 but missing the CI/CD gate In Build exclusion in Section 5 is failing the Claims Firewall — automatic disqualification. The CI/CD gate must appear in Section 6 (Prohibited) and be explicitly excluded from Section 5, regardless of how strong the rest of the output is.

An output that correctly identifies LangSmith's prompt playground and dataset management as Gaps in Example 2 but then cites Ethana Workspace as covering them — even aspirationally — is an Aspirational misuse and is automatically disqualified.
