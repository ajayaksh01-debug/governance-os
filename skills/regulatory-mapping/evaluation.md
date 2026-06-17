# Regulatory Mapping — Evaluation Criteria and Scoring Rubric

## Purpose

This document defines the quality criteria for regulatory mapping assessments produced using this skill. It provides:
- A scoring rubric for each output section
- A pass/fail threshold and release criteria
- Common failure modes and how to correct them
- A peer review checklist for high-stakes assessments

Every completed regulatory mapping must be scored before release. An assessment scoring below 70/100 must be revised or reclassified as preliminary pending additional information.

---

## Scoring Overview

| Section | Maximum Score | Weight Rationale |
|---|---|---|
| 1. Applicable Regulations | 15 | Foundation of the assessment — incorrect applicability determination invalidates all downstream sections |
| 2. Applicable Governance Frameworks | 10 | Framework mapping must be specific to the subject, not generic |
| 3. Regulatory Obligations | 15 | Highest practitioner value; obligations must be specific and legally cited |
| 4. Risk Classification | 10 | Classification accuracy determines compliance burden; must be defensible |
| 5. Documentation Requirements | 10 | Completeness and specificity determine practical usefulness |
| 6. Control Requirements | 15 | Actionability; controls must be specific and correctly classified as mandatory or recommended |
| 7. Audit Evidence Required | 5 | Lower complexity but must be complete and linked to regulatory sources |
| 8. BFSI Considerations | 10 | High value for the primary client segment; must be sector-specific, not generic |
| 9. Executive Summary | 10 | Must accurately compress the full analysis for a senior audience |
| **Total** | **100** | |

---

## Section-by-Section Rubric

### Section 1 — Applicable Regulations (15 points)

| Score | Criteria |
|---|---|
| 13–15 | All applicable regulations correctly identified for every jurisdiction in scope; applicability triggers are specific (not just "processes personal data" but "processes personal data of EU individuals, triggering GDPR Article 2(1) territorial scope"); non-applicable regulations are explicitly addressed with rationale; conditional applicability is flagged with determining factors; no regulation is missed that a competent compliance officer would identify |
| 10–12 | Most applicable regulations identified correctly; one minor omission or one trigger stated without sufficient specificity; non-applicability mostly documented |
| 7–9 | Major regulations identified but secondary regulations missed (e.g., Equality Act when discrimination risk exists); triggers are generic; non-applicability not documented |
| 4–6 | Only the most obvious regulations identified; significant gaps in coverage; no non-applicability analysis |
| 0–3 | Missing, incorrect, or jurisdiction-blind |

**Common failures:**
- Missing sectoral regulations: identifying GDPR but not FCA/PRA obligations for a financial services subject
- Treating GDPR as automatically applicable without establishing the territorial nexus (EU individuals, EU establishment, EU market targeting)
- Omitting the DPDP Act for subjects processing Indian personal data
- Failing to check SEBI applicability for trading-related AI at Indian brokers
- Stating applicability without the specific trigger — "GDPR applies" without explaining why

---

### Section 2 — Applicable Governance Frameworks (10 points)

| Score | Criteria |
|---|---|
| 9–10 | ISO 42001 mapping references specific clauses and Annex A controls with rationale tied to the subject; NIST AI RMF functions are correctly assigned with specific categories identified; OWASP LLM Top 10 is correctly applied (with specific risk categories) or correctly marked N/A; cross-framework coherence is demonstrated; framework mappings connect to regulatory obligations |
| 7–8 | Correct framework identification; most mappings are specific; one framework mapping is at the category level rather than the clause/function level |
| 5–6 | Frameworks correctly identified but mappings are generic (e.g., "ISO 42001 Clause 8 applies" without specifying which Clause 8 requirements); OWASP LLM assessment is present but superficial |
| 3–4 | Frameworks identified but not meaningfully mapped to the subject; no connection between framework requirements and regulatory obligations |
| 0–2 | Missing, incorrect, or frameworks confused with each other |

**Common failures:**
- Mapping everything to ISO 42001 Clause 8 without distinguishing lifecycle, supply chain, and impact assessment requirements
- Assigning all NIST AI RMF functions as "applicable" without identifying the primary governance requirement
- Applying OWASP LLM Top 10 to a non-LLM AI system (e.g., an ML classifier)
- Omitting OWASP LLM Top 10 for an LLM-based chatbot or agent
- No cross-reference between framework requirements and regulatory obligations — the two sections exist in isolation

---

### Section 3 — Regulatory Obligations (15 points)

| Score | Criteria |
|---|---|
| 13–15 | Every applicable regulation has specific obligations extracted; each obligation cites the specific legal provision (Article number, Section, Clause); obligation types are correctly classified; timelines are accurate and reflect the current compliance calendar; consequences of non-compliance are correctly characterised with penalty ranges; no material obligation is missing |
| 10–12 | Most obligations correctly identified with legal citations; one or two obligations missing or imprecisely cited; timelines mostly accurate |
| 7–9 | Obligations identified at the category level ("must comply with GDPR") without specific provisions; timelines not addressed; consequences generic |
| 4–6 | Obligations stated without legal citations; significant gaps; timelines and consequences absent |
| 0–3 | Missing, generic, or incorrect |

**Common failures:**
- Stating "comply with GDPR" without extracting the specific GDPR obligations triggered (lawful basis, DPIA, data subject rights, breach notification)
- Omitting notification obligation timelines — Article 33 (72-hour breach notification) is often the most operationally urgent obligation
- Conflating the EU AI Act's transitional timeline — different obligations apply at different dates (prohibitions from Feb 2025, GPAI from Aug 2025, Annex III from Aug 2026)
- Stating penalties without the specific penalty provision and range
- Missing BFSI-specific obligations that overlay general AI regulation (PRA SS1/23 model validation requirements on top of general GDPR obligations)

---

### Section 4 — Risk Classification (10 points)

| Score | Criteria |
|---|---|
| 9–10 | Classification under every applicable regime is stated with the specific provision determining the classification; EU AI Act tier references the specific Annex I or III category; UK classification references PRA SS1/23 model tier criteria; India classification addresses SDF status, RBI materiality, and SEBI registration; ambiguous classifications are documented with both possible outcomes and determining factors |
| 7–8 | Classifications mostly correct; one regime's classification is correct but insufficiently detailed; ambiguities not fully addressed |
| 5–6 | Major classifications correct but secondary classifications missing (e.g., EU AI Act classification present but PRA model tier absent for a UK BFSI subject) |
| 3–4 | Only the most obvious classification stated; no supporting rationale |
| 0–2 | Missing, incorrect, or contradictory |

**Common failures:**
- Classifying a credit scoring system as "limited risk" under the EU AI Act when credit scoring is explicitly Annex III high-risk
- Omitting PRA SS1/23 model tier classification for a BFSI AI system operating in the UK
- Not addressing the ambiguity in EU AI Act classification for edge cases (e.g., fraud detection systems where Annex III applicability depends on the system's design and impact)
- Stating classifications without rationale — the classification must be traceable to a specific provision

---

### Section 5 — Documentation Requirements (10 points)

| Score | Criteria |
|---|---|
| 9–10 | Complete documentation matrix covering all applicable regimes; each document type specifies the regulatory source, content requirements, and maintenance obligation; documents required by frameworks (ISO 42001 AIMS documentation) are included alongside regulatory requirements; no material document is missing |
| 7–8 | Most documentation requirements identified; one or two minor omissions; content requirements mostly specified |
| 5–6 | Major documents identified but content requirements not specified; framework documentation requirements omitted |
| 3–4 | Documentation stated generically ("maintain documentation") without specificity |
| 0–2 | Missing or incorrect |

**Common failures:**
- Missing DPIA requirements for high-risk personal data processing
- Omitting EU AI Act Annex IV technical documentation requirements for high-risk AI
- Listing documents without specifying what they must contain — "risk assessment" without specifying the assessment scope and methodology
- Missing retention period requirements where specified by regulation

---

### Section 6 — Control Requirements (15 points)

| Score | Criteria |
|---|---|
| 13–15 | All material controls identified; each control correctly classified as mandatory or recommended; regulatory source is specific (Article, Clause, Annex A reference); control types are correctly assigned (Preventive/Detective/Corrective); implementation guidance is sufficient to scope the work; controls from frameworks and regulations are both covered; no overlap or duplication between controls |
| 10–12 | Most controls identified; one or two controls missing or misclassified; mandatory/recommended distinction mostly correct |
| 7–9 | Core controls present but missing important secondary controls; mandatory/recommended distinction not consistently applied |
| 4–6 | Controls identified at category level but not specific enough to scope implementation |
| 0–3 | Missing, generic, or unconnected to the regulatory obligations |

**Common failures:**
- Listing "human oversight" as a single control when multiple distinct oversight mechanisms may be required (approval gates, monitoring dashboards, override capabilities)
- Classifying all controls as mandatory when some are framework recommendations rather than legal requirements
- Missing detective controls — assessments frequently identify required preventive controls but miss required monitoring, audit, and testing controls
- Not connecting controls to the specific regulatory provisions that require them

---

### Section 7 — Audit Evidence Required (5 points)

| Score | Criteria |
|---|---|
| 5 | Evidence types correctly identified for each audience (regulator, certification body, internal audit); retention requirements stated where specified; format guidance provided; evidence items are linked to specific regulatory or framework requirements |
| 3–4 | Evidence types mostly identified; retention or format guidance missing; linkage to requirements mostly present |
| 1–2 | Evidence stated generically without specificity to regulatory requirements |
| 0 | Missing or incorrect |

---

### Section 8 — BFSI Considerations (10 points)

| Score | Criteria |
|---|---|
| 9–10 | Applicability correctly determined; if applicable, specific BFSI regulatory frameworks identified with concrete obligations beyond general AI regulation; model risk management requirements addressed (SR 11-7, PRA SS1/23, RBI MRM); supervisory examination expectations characterised; customer harm pathways identified; if not applicable, rationale is stated |
| 7–8 | Applicability correct; BFSI analysis mostly complete with minor omissions |
| 5–6 | Section present but generic; does not connect the subject to specific BFSI regulatory frameworks or supervisory expectations |
| 3–4 | BFSI relevance addressed superficially; no specific regulatory frameworks cited |
| 0–2 | Missing or incorrectly determined as N/A when applicable |

**Common failures:**
- Stating "FCA applies" without identifying which FCA obligations are specifically triggered (Consumer Duty, SMCR, conduct risk, etc.)
- Omitting PRA SS1/23 model tier assessment for a BFSI AI system
- Not identifying customer harm pathways — BFSI regulators focus on outcomes for consumers, not just process compliance
- Missing RBI-specific obligations for Indian banking AI deployments

---

### Section 9 — Executive Summary (10 points)

| Score | Criteria |
|---|---|
| 9–10 | 200–250 words; suitable for board or C-suite; accurately reflects the full analysis; identifies the most significant regulatory exposure and the most consequential risk classification; states the key framework alignment gaps; specifies highest-priority compliance actions; no jargon; no framework references without explanation; written last (reflects actual findings) |
| 7–8 | Correct but slightly over length, or one element missing; mostly executive-accessible |
| 5–6 | Present but too technical, or does not accurately prioritise — lists all regulations equally rather than highlighting the most consequential |
| 3–4 | Summary present but not executive-ready; significant jargon or inaccuracy |
| 0–2 | Missing or unsuitable for release |

**Common failures:**
- Listing every regulation without prioritising — an executive summary that gives equal weight to GDPR and a minor MEITY advisory is not useful
- Including framework clause references without explaining what they mean to a non-technical audience
- Not stating the most important action — what should the organisation do first?
- Exceeding 300 words — indicating a lack of synthesis

---

## Score Thresholds and Release Criteria

| Score | Classification | Release Action |
|---|---|---|
| 85–100 | Exemplary | Release as final; candidate for inclusion in examples library |
| 70–84 | Acceptable | Release as final |
| 55–69 | Below standard | Reclassify as preliminary; revise before final release |
| Below 55 | Insufficient | Do not release; major revision or analyst reassignment required |

---

## Peer Review Checklist (for high-stakes assessments)

High-stakes assessments — those covering subjects with direct client regulatory exposure, multi-jurisdictional obligations, or high-risk AI Act classification — require peer review before release. Reviewer checklist:

**Jurisdictional accuracy**
- [ ] All jurisdictions with a legitimate regulatory nexus are included
- [ ] Applicability triggers are specific and defensible
- [ ] Non-applicable regulations are documented with rationale, not simply omitted
- [ ] Conditional applicability is clearly flagged

**Obligation specificity**
- [ ] Every obligation cites a specific legal provision (Article, Section, Clause)
- [ ] Obligation types are correctly classified
- [ ] Compliance timelines reflect the current regulatory calendar
- [ ] Consequences of non-compliance reference specific penalty provisions

**Framework accuracy**
- [ ] ISO 42001 clause references are specific and correct
- [ ] NIST AI RMF functions are assigned to the correct governance dimension
- [ ] OWASP LLM Top 10 is correctly applied (or correctly marked N/A)
- [ ] Framework mappings connect to regulatory obligations — not isolated

**Risk classification defensibility**
- [ ] EU AI Act classification references the specific Annex and category
- [ ] UK classifications reference PRA SS1/23 model tier criteria (where applicable)
- [ ] India classifications address all applicable regulators
- [ ] Ambiguous classifications are documented with determining factors

**BFSI relevance**
- [ ] BFSI section is correctly populated (or correctly marked N/A)
- [ ] Sector-specific obligations go beyond generic AI regulation
- [ ] Customer harm pathways are identified where relevant
- [ ] Supervisory examination expectations are characterised

**Actionability**
- [ ] Documentation requirements are specific enough to produce
- [ ] Control requirements distinguish mandatory from recommended
- [ ] Audit evidence requirements are linked to specific regulatory sources
- [ ] Executive summary accurately prioritises the most consequential findings

**Tone and audience**
- [ ] Executive summary is genuinely executive-accessible
- [ ] No section contains unexplained regulatory or technical jargon
- [ ] Assessment is objective — neither alarmist nor dismissive about regulatory exposure

---

## Calibration Reference

To support consistent scoring across analysts, the three worked examples in `examples.md` serve as calibration anchors:

| Example | Expected Score Range | Key Differentiators |
|---|---|---|
| BFSI Credit Scoring Model (India/EU/UK) | 88–95 | Multi-jurisdiction high-risk AI Act Annex III classification; RBI MRM and PRA SS1/23 model tier analysis; strong BFSI section; complex obligation layering |
| Internal Employee GenAI Assistant | 85–92 | Limited-risk EU AI Act classification; DPDP Act employee data implications; OWASP LLM Top 10 fully applicable; BFSI section requires careful relevance determination |
| Algorithmic Trading System (India/UK) | 88–95 | SEBI AI/ML circular as primary regulatory driver; FCA MiFID II obligations; edge-case EU AI Act classification; strong BFSI section with systemic risk considerations |

New analysts should score each calibration example independently and compare against expected ranges before conducting scored assessments.
