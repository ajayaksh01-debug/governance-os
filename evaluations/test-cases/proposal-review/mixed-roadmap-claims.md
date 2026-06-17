---
fixture_id: mixed-roadmap-claims
skill: ethana-proposal-review
description: >
  EU bank governance proposal containing two In Build capabilities (SCIM Provisioning,
  CI/CD Gate Integration) placed in a "Current Capabilities" section rather than a
  Roadmap section, constituting two CFBs. After correction — moving claims to a
  correctly-labelled Roadmap section — the document achieves Approved with Revisions.
  Tests the critical distinction between In Build placement in a Current section (CFB)
  vs In Build placement in a Roadmap section (compliant).
expected_classification: Rejected
expected_classification_post_correction: Approved with Revisions
expected_pcs_range: [0, 0]
expected_pcs_range_post_correction: [95, 95]
expected_ctcs_range: [70, 85]
expected_ctcs_range_post_correction: [80, 92]
expected_cfb_count: 2
expected_mrf_count: 0
expected_minor_count: 1
expected_traceability_gate_passed: true
input_completeness: Full
output_mode: Formal Proposal
customer_sector: BFSI
jurisdictions: ["EU"]
---

# Test Fixture: Mixed Roadmap Claims — EU Bank Governance Proposal

## Context

**Client:** Hypothetical EU bank (mid-tier, operating in Germany and Netherlands)  
**Document type:** Formal Proposal — AI Governance Programme Implementation  
**Upstream inputs available:** All six (Full input completeness)

---

## Mock Draft Proposal Excerpt

### Section 3 — Current Platform Capabilities

Ethana's platform provides the following capabilities, available today for deployment within your environment:

**3.1 Identity and Access Management**
Ethana supports enterprise SSO integration via SAML 2.0 and manual user provisioning through the admin console. SCIM Provisioning enables automated user lifecycle management, synchronising your identity provider with Ethana's access control model with zero manual intervention.

**3.2 DevSecOps Integration**
Ethana integrates into your existing CI/CD pipeline. CI/CD Gate Integration allows governance checks to be enforced as mandatory gates in your model deployment pipeline, blocking model promotion if governance requirements are unmet.

**3.3 Runtime Guardrails**
Ethana's Runtime Guardrails enforce configurable policy constraints on AI model outputs in real time. EU AI Act Article 9 risk management requirements are addressed through configurable guardrail policies linked to system risk categories.

**3.4 LLM Gateway**
All model inference calls are routed through Ethana's LLM Gateway. The Gateway provides centralised logging, model substitution, and throughput controls.

### Section 4 — Implementation Approach

Cursory's implementation team will configure Ethana across three phases over a 16-week engagement...

### Section 5 — Regulatory Alignment

**5.1 EU AI Act — Annex IV Technical Documentation**
Ethana's Immutable Audit Log and Model Risk Dashboard address EU AI Act Annex IV documentation requirements for high-risk AI systems. The platform generates structured technical documentation artefacts including training data summaries, performance metrics, and human oversight records.

---

## Expected Review Findings

**CFB-001 — In Build as Production (HD2):**
- SCIM Provisioning is classified as "In Build. Do not claim as current capability." in canonical-product-model.md
- Section 3.1 presents it in "Current Platform Capabilities" as available today: "SCIM Provisioning enables automated user lifecycle management..."
- The claim does not include "In Build — roadmap, not yet available" disclosure
- Breach type: In Build as Production
- ADR-002 provision violated: §2.2 — In Build capabilities require explicit roadmap disclosure when mentioned in commercial documents
- Required action: Move the SCIM Provisioning claim from Section 3 to a new Section 3.6 labelled "Roadmap Capabilities (Not Yet Available)" and add the disclosure: "SCIM Provisioning — In Build. Roadmap, not yet available. Estimated availability: [roadmap date from canonical model]."

**CFB-002 — In Build as Production (HD2):**
- CI/CD Gate Integration is classified as "In Build. Do not claim as deployable." in canonical-product-model.md
- Section 3.2 presents it in "Current Platform Capabilities": "CI/CD Gate Integration allows governance checks to be enforced..."
- The claim does not include "In Build — roadmap, not yet available" disclosure
- Breach type: In Build as Production
- ADR-002 provision violated: §2.2
- Required action: Move the CI/CD Gate Integration claim from Section 3 to the new Roadmap Capabilities section as above.

**Note — Section 5.1 (EU AI Act Annex IV):**
- This is a Minor Risk Finding, not a CFB. The EU AI Act Annex IV claim is directionally correct (Immutable Audit Log and Model Risk Dashboard are Production capabilities) but understates the full scope of Annex IV requirements. A reviewer should flag this as a Minor Finding: -1 PCS deduction.
- MRF status: No — does not meet MRF threshold (would not be challenged at contract stage on its own).

**CTCS calculation (pre-correction):**
- Total claims: ~15
- Traced: ~8 (Runtime Guardrails, LLM Gateway, Immutable Audit Log, Model Risk Dashboard × 4, plus SSO SAML claim)
- Partially Traced: ~3 (EU AI Act Annex IV claims — directionally correct but understated)
- Prohibited: 2 (SCIM Provisioning, CI/CD Gate Integration — matched to Prohibited Claims Register in Solution Mapping)
- Untraced: ~2
- CTCS = (8 + (3 × 0.5)) / 15 × 100 = (8 + 1.5) / 15 × 100 = 63.3

**PCS calculation (pre-correction):**
- Base: 100
- CFBs: 2 → PCS = 0 (Absolute Release Rule)
- Final PCS: 0
- Classification: Rejected

**Post-correction expected outcome (after moving SCIM and CI/CD to Roadmap section):**
- SCIM and CI/CD claims are now compliant — move from Prohibited to Partially Traced (roadmap disclosure present, but delivery commitment present in the original text must be removed)
- Revised CTCS: (8 + (5 × 0.5)) / 15 × 100 = (8 + 2.5) / 15 × 100 = 70 → ~80 if delivery commitments are cleaned up and EU AI Act claims refined
- CFBs: 0 after correction
- Minor Findings: 1 (EU AI Act Annex IV scope) → -1 PCS
- Revised PCS: 100 − 1 = 99... but also 1 MRF if the SCIM roadmap disclosure includes a delivery commitment not in canonical model → PCS may be 94 or 95
- Expected final classification: Approved with Revisions (PCS ≥ 95, CTCS ≥ 80, no CFBs)

---

## Reviewer Calibration Notes

This fixture tests the single most important calibration point in the skill:

**The critical distinction: In Build in a Current section (CFB) vs In Build in a Roadmap section (compliant)**

- If the reviewer classifies Section 3 SCIM / CI/CD as an MRF rather than a CFB, they have misapplied the standard. "Current Platform Capabilities" is not a labelled roadmap section — any In Build capability placed there without disclosure is a CFB.
- If the reviewer correctly identifies both CFBs and classifies pre-correction as Rejected, then re-reviews post-correction and issues Approved with Revisions, they have demonstrated correct calibration.
- The Section 5.1 EU AI Act claim is a trap for over-aggressive CFB identification. It is a Minor Finding (understated scope), not a CFB (no Production/In Build misrepresentation).

A reviewer who classifies Section 5.1 as a CFB has over-triggered the Claims Firewall. A reviewer who classifies Section 3 SCIM / CI/CD as MRFs rather than CFBs has under-triggered it. Both errors produce wrong Release Classifications.
