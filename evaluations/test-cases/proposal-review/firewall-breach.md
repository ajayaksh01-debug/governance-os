---
fixture_id: firewall-breach
skill: ethana-proposal-review
description: >
  UK insurance pitch deck containing three Critical Firewall Breaches: an Aspirational
  capability (Visual Agent Builder) presented as Production, an uncertified SOC 2 Type II
  presented as currently held, and an unverified customer deployment claim. Tests the
  Rejected path and the Absolute Release Rule — PCS is set to 0 and classification is
  Rejected regardless of CTCS.
expected_classification: Rejected
expected_pcs_range: [0, 0]
expected_ctcs_range: [40, 65]
expected_cfb_count: 3
expected_mrf_count: 0
expected_minor_count: 0
expected_traceability_gate_passed: true
input_completeness: Standard
output_mode: Pitch Deck
customer_sector: BFSI
jurisdictions: ["UK"]
---

# Test Fixture: Firewall Breach — UK Insurance Pitch Deck

## Context

**Client:** Hypothetical UK insurance company (Tier 1 insurer)  
**Document type:** Pitch Deck — AI Governance Platform Evaluation  
**Upstream inputs available:** Draft + solution mapping + feature mapping (Standard — no capability validation)

---

## Mock Draft Proposal Excerpt

### Slide 5 — Platform Overview

Ethana by Cursory delivers a complete AI governance platform for insurance carriers. Our production capabilities include:

- **Visual Agent Builder** — Build, deploy, and monitor AI agents with a no-code visual interface. Currently deployed across four major UK insurance companies.
- **Runtime Guardrails** — Real-time policy enforcement on AI outputs across all models in your environment.
- **LLM Gateway** — Centralised routing and logging for all LLM inference calls.

### Slide 7 — Compliance & Certifications

Ethana holds the following certifications:
- SOC 2 Type II (certified — report available under NDA)
- ISO 27001 (in progress — expected Q3 2026)

### Slide 9 — Client Results

Ethana is currently deployed at four major UK insurance companies, including a FTSE 100 carrier, delivering measurable improvements in model governance and audit readiness.

---

## Expected Review Findings

**CFB-001 — Aspirational capability as Production (HD1):**
- Visual Agent Builder is classified as Aspirational in canonical-product-model.md: "Visual Agent Builder — Aspirational. Not in active development."
- Slide 5 presents it as a current production capability: "Build, deploy, and monitor AI agents with a no-code visual interface. Currently deployed..."
- Breach type: Aspirational as Production
- ADR-002 provision violated: §2.1 — Aspirational capabilities may not be represented as available
- Required action: Remove Visual Agent Builder claim entirely. It may not be mentioned in any commercial context as available or deployable.

**CFB-002 — Uncertified certification stated as current (HD3):**
- SOC 2 Type II is classified as "In Build. Do not claim as held." in canonical-product-model.md
- Slide 7 states: "SOC 2 Type II (certified — report available under NDA)"
- Breach type: Uncertified as Certified
- ADR-002 provision violated: §2.3 — Certification claims require confirmed status in canonical-product-model.md
- Required action: Replace with "SOC 2 Type II — currently in progress, not yet certified. Estimated certification Q4 2026."

**CFB-003 — Unverified customer deployment claim (HD5):**
- "Four major UK insurance companies" deployment claim appears in Slide 5 and Slide 9
- No entry in canonical-product-model.md confirms approved customer reference claims for UK insurance sector
- Breach type: Capability/claim not found in canonical-product-model.md
- ADR-002 provision violated: §2.4 — Customer reference claims require approved entries
- Required action: Remove deployment count and FTSE 100 reference. Replace with approved language from the customer reference section of solution-mapping output if available, or omit.

**CTCS calculation (Standard input — no Capability Validation):**
- Total claims: ~13 (including the three prohibited/untraced claims)
- Traced: ~5 (Runtime Guardrails, LLM Gateway, and 3 others against Solution Mapping)
- Partially Traced: ~2 (claims directionally correct but without full canonical confirmation)
- Untraced/Prohibited: ~6 (Visual Agent Builder, SOC 2 claims, deployment count, and related)
- CTCS ≈ (5 + 1) / 13 × 100 ≈ 46

**PCS calculation:**
- Base: 100
- CFBs detected: 3 → PCS set to 0 (Absolute Release Rule)
- Final PCS: 0

**Expected classification:** Rejected (Absolute Release Rule — CFBs present)

---

## Reviewer Calibration Notes

This fixture tests the reviewer's ability to:
1. Correctly apply the Absolute Release Rule — PCS = 0, classification = Rejected regardless of what CTCS would otherwise produce
2. Identify HD1 (Aspirational as Production) — not just In Build; Visual Agent Builder is not in active development
3. Identify HD3 (uncertified certification) independently of whether the reviewer "believed" the SOC 2 claim
4. Recognize HD5 for customer reference claims without canonical model backing
5. Continue calculating CTCS even after CFBs are identified — do not halt the review at CFB detection

A reviewer who sets classification to Conditional Release despite the CFBs has triggered HD7 and the output is automatically disqualified. The presence of any CFB mandates Rejected — no exceptions.
