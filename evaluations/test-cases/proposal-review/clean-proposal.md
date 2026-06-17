---
fixture_id: clean-proposal
skill: ethana-proposal-review
description: >
  RFP response for a mid-size Indian private bank with 13 Production capability claims,
  full upstream traceability from all six inputs, no CFBs, and two minor mandatory-caveat
  omissions that are corrected during revision. Tests the full Approved path.
expected_classification: Approved
expected_pcs_range: [98, 100]
expected_ctcs_range: [95, 100]
expected_cfb_count: 0
expected_mrf_count: 0
expected_minor_count: 0
expected_traceability_gate_passed: true
input_completeness: Full
output_mode: RFP Response
customer_sector: BFSI
jurisdictions: ["India"]
---

# Test Fixture: Clean Proposal — Indian Private Bank RFP

## Context

**Client:** Hypothetical Indian private bank (mid-tier, 1,000+ branches)  
**Document type:** RFP Response — AI Governance Platform Selection  
**Upstream inputs available:** All six (draft + solution mapping + feature mapping + capability validation + regulatory mapping + control mapping)

---

## Mock Draft Proposal Excerpt

This excerpt contains the sections relevant to capability claims. In a real test run, the full proposal would be provided.

### Section 3 — Ethana Platform Capabilities

Cursory's Ethana platform provides the following production-ready capabilities for your AI governance programme:

**3.1 Immutable Audit Log**
Ethana maintains an immutable audit log of every AI system action, model inference call, and human review decision. The log is tamper-resistant and supports export in structured JSON format for integration with your existing SIEM infrastructure.

**3.2 Runtime Guardrails**
Ethana's Runtime Guardrails enforce configurable policy constraints on AI model outputs in real time. Guardrails can be configured to block, flag, or route outputs based on content categories defined by your governance team.

**3.3 LLM Gateway**
All model inference calls are routed through Ethana's LLM Gateway, which provides centralised logging, rate limiting, and model substitution capabilities. The Gateway supports major LLM providers including OpenAI, Anthropic, and Azure OpenAI Service.

**3.4 Red Teaming Orchestrator**
Ethana's Red Teaming Orchestrator enables structured adversarial testing of AI systems. Tests are configurable across attack categories and can be scheduled or triggered on model change events.

**3.5 Bias Scanner**
Ethana's Bias Scanner evaluates AI model outputs for statistical disparity across demographic groups. Scanner results are logged to the Immutable Audit Log and flagged for human review when thresholds are exceeded.

**3.6 PII Scanner**
Ethana's PII Scanner detects and flags personally identifiable information in AI model inputs and outputs. Detection coverage includes common Indian PII categories (Aadhaar numbers, PAN, mobile numbers).

### Section 4 — Roadmap Items

The following capabilities are currently in active development and are expected to be available within the next 12–18 months. They are not included in the scope of this proposal:

- SCIM Provisioning (In Build — roadmap, not yet available)
- CI/CD Gate Integration (In Build — roadmap, not yet available)

### Section 5 — Compliance and Certifications

Cursory maintains SOC 2 Type II certification for the Ethana platform. Certification documentation is available upon request under NDA.

---

## Expected Review Findings

**Claim inventory (13 claims):**
- CLM-RFP-001 through CLM-RFP-013 covering Immutable Audit Log, Runtime Guardrails, LLM Gateway, Red Teaming Orchestrator, Bias Scanner (×2), PII Scanner (×2), SCIM Provisioning, CI/CD Gate Integration, SOC 2 Type II

**Traceability expected outcome:**
- All Production capability claims trace to Solution Mapping Section 3 and/or Capability Validation Section 4
- SCIM Provisioning and CI/CD Gate Integration are disclosed in Section 4 (Roadmap) — compliant; no CFB
- SOC 2 Type II traces to canonical-product-model.md certification entry — compliant

**CTCS calculation:**
- 11 claims Traced, 0 Partially Traced, 2 claims (SCIM, CI/CD) correctly labelled as Roadmap (not production claims — not in denominator if labelled as roadmap), 0 Untraced
- CTCS = (11 + (0 × 0.5)) / 11 × 100 = 100

**CFB check:** None expected. All Production claims confirmed in canonical-product-model.md. Roadmap items correctly disclosed.

**PCS calculation:** 100 (no CFBs, no MRFs, no Minor Findings)

**Expected classification:** Approved

---

## Reviewer Calibration Notes

This fixture tests the reviewer's ability to:
1. Correctly exclude properly-disclosed Roadmap items from the CFB check (HD2 requires *undisclosed* In Build as Production — roadmap section disclosure is compliant)
2. Confirm SOC 2 certification against canonical-product-model.md before accepting the claim
3. Achieve CTCS = 100 when all Production claims are fully traced
4. Issue Approved at PCS 100, CTCS 100 with no findings

A reviewer who marks SCIM Provisioning or CI/CD Gate Integration as a CFB has misapplied HD2. The test of HD2 is whether the In Build capability is presented *as currently available* — disclosure in a Roadmap section labelled "not yet available" is compliant.
