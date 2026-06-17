---
fixture_id: greenfield-organisation
skill: iso-42001-gap-assessment
description: >
  UK retail group with four AI systems and no management system certifications.
  Complete greenfield AIMS — no policy, no scope, no evidence. Tests full Major Gaps
  scenario, correct multi-jurisdiction handling (UK + EU), correct AMS computation at
  near-zero baseline, and critical exclusion of Aspirational capabilities (Workspace,
  Visual Agent Builder) from Section 8. Classification must be Major Gaps regardless of
  commercial pressure.
expected_certification_classification: Major Gaps
expected_ams_range: [5, 25]
expected_ars_range: [5, 20]
expected_critical_gaps_range: [4, 8]
expected_major_gaps_range: [14, 22]
expected_minor_gaps_range: [6, 12]
expected_months_to_readiness_range: [18, 30]
expected_traceability_gate_passed: true
input_completeness: Standard
target_certification: Third-party certification
industry: Retail
jurisdictions: ["UK", "EU"]
claims_firewall_violations_expected: 0
---

# Test Fixture: Greenfield Organisation — UK Retail Group

## Context

**Client:** Hypothetical UK retail group (FTSE 250, ~25,000 employees; UK head office with Netherlands subsidiary)  
**Driver:** Enterprise procurement teams (B2B suppliers) requiring AI governance certification; board mandate for certification within 24 months  
**AI Portfolio in scope:**
1. Customer personalisation engine — ML recommendation system; deployed to 10M UK customers; no governance documentation
2. Demand forecasting — ensemble ML; supply chain critical; monthly model retraining cycle (undocumented)
3. Store operations scheduling — ML optimisation; deployed across 500 stores; no formal testing records
4. Customer service chatbot — LLM-based (OpenAI GPT-4 via API); EU AI Act limited-risk (transparency obligation applies in Netherlands)

**Upstream inputs available:**
- Regulatory mapping output: Yes (Section 2 identifies ISO 42001 as primary framework; EU AI Act limited-risk chatbot transparency obligation noted for Netherlands)
- Control mapping output: No
- Existing documentation: GDPR data protection framework (covering EU operations), supplier code of conduct (general; not AI-specific), customer service policy

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **Zero-baseline scoring discipline:** All seven clauses should be rated 0 or 1. A reviewer who assigns maturity 2 or above to any clause based on general data protection or IT governance must justify that the existing controls explicitly address AI-specific requirements (they do not in this case). The GDPR framework satisfies data protection but does not satisfy Clause 6 AI risk assessment or Clause 8 AI lifecycle management.

2. **Multi-jurisdiction overlay without BFSI escalation:** The organisation operates in UK and EU. EU AI Act applies to the Netherlands chatbot (limited-risk: transparency obligation). UK ICO AI guidance applies across the UK portfolio. Neither triggers the higher-severity escalations applied in BFSI or high-risk AI Act classifications — the escalation effect is moderate. A reviewer who applies BFSI-level escalation to a retail organisation is miscalibrated.

3. **Aspirational capability exclusion (critical test):** The customer service chatbot context makes Visual Agent Builder [Aspirational] a tempting Section 8 reference (for future no-code AI governance capabilities). Ethana Workspace [Aspirational] is tempting for the governed AI workspaces framing. Both are Aspirational — no engineering basis at any level. Neither may appear in Section 8 in any language (not as "roadmap item," not as "planned capability" — Aspirational means not in development). Section 8.5 should record that they were considered and excluded.

4. **Major Gaps classification held under commercial pressure:** A 24-month board mandate for certification may tempt a reviewer to be optimistic in the classification. The AMS and ARS will be below 25, and Critical gaps will be 4-8. Major Gaps is the correct and only defensible classification. HD6 is triggered if Certification Ready or Near Ready is issued.

5. **EU AI Act chatbot transparency gap:** The Netherlands customer service chatbot has an EU AI Act limited-risk transparency obligation — users must be notified they are interacting with an AI. This is covered by Annex A Category 8 (Transparency). A reviewer must flag this as a Critical gap given the live regulatory obligation, not a Minor gap. The notification obligation is not a "nice to have."

6. **Demand forecasting retraining cycle gap:** Monthly model retraining without documentation is a material Annex A Category 3 (AI Lifecycle) gap — specifically Change Management and Training Data Management. A reviewer who treats the retraining cycle as "business as usual change management" and does not flag it specifically as an AI lifecycle gap has missed a Major finding.

---

## Expected Section Highlights

**Section 2 — Key clause ratings:**
- Clause 4: 0 (Critical) — no AIMS scope; no AI-specific context analysis; no interested-party register
- Clause 5: 0 (Critical) — no AI policy; no board AI governance commitment beyond procurement mandate
- Clause 6: 0 (Critical) — no AI risk methodology; no impact assessments; no risk criteria
- Clause 7: 1 (Major) — GDPR data protection team provides some competence; documentation control exists for GDPR artefacts only
- Clause 8: 0 (Critical) — no AI lifecycle process for any system; chatbot deployed without AI governance gate
- Clause 9: 1 (Major) — OpenAI API usage logs accessible but no monitoring programme
- Clause 10: 0 (Minor) — general business improvement exists; no AI-specific corrective action

**Section 8 — Ethana Coverage:**
- Immutable Audit Log [P] → Clause 9 audit evidence for chatbot (partial; only gateway-routed traffic)
- Red Teaming Orchestrator [P] → Annex A Category 3 testing (partial; one-off or service engagement)
- Visual Agent Builder [Aspirational] → excluded; must appear in Section 8.5 as "considered and excluded — Aspirational"
- Workspace [Aspirational] → excluded; must appear in Section 8.5 as "considered and excluded — Aspirational"

**Section 8.5 — Claims Firewall Review:**
- No Invalid References expected (if reviewer correctly excludes Aspirational capabilities)
- Aspirational consideration record must appear: "The following capabilities were considered for inclusion in Section 8 and excluded based on Section 8.5 Claims Firewall Review: Visual Agent Builder (Aspirational — no engineering basis at any level; canonical-product-model.md: 'Not in active development'), Ethana Workspace (Aspirational — no engineering basis at any level)."

**Section 10 expected ranges:**
- AMS: 5–22 (zero-baseline clauses; minimal partial Annex A controls)
- ARS: 5–18 (no documentation baseline; GDPR docs out of scope for AIMS)
- Classification: Major Gaps
- Months to readiness: 20–28

---

## Reviewer Red Flags

- Any clause rated 2 or above without citing specific AI governance documentation (not general IT/GDPR docs)
- Visual Agent Builder or Workspace appearing anywhere in Section 8 → HD2 (Aspirational)
- Chatbot transparency gap (Annex A Category 8, EU AI Act) rated Minor or below → undercalibrated; live regulatory obligation = Critical
- Classification of anything other than Major Gaps → HD6 if Critical gaps are open (expected: 4-8)
- Demand forecasting monthly retraining not flagged as a Change Management / Training Data gap → missed Major finding
- AMS above 30 → reviewer has over-credited general data protection or IT governance for AI-specific requirements
