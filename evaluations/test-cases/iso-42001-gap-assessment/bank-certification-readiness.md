---
fixture_id: bank-certification-readiness
skill: iso-42001-gap-assessment
description: >
  Indian private bank with four AI systems (credit scoring, LLM chatbot, fraud detection,
  trade finance extraction), RBI MRM mandate, partial ISO 27001 coverage, and a board
  mandate to achieve ISO 42001 certification within 18 months. Tests correct severity
  escalation under RBI jurisdiction overlay, correct partial credit for ISO 27001 shared
  infrastructure, and correct exclusion of Compliance Pack [IB] from Section 8.
expected_certification_classification: Significant Gaps
expected_ams_range: [20, 50]
expected_ars_range: [20, 40]
expected_critical_gaps_range: [3, 6]
expected_major_gaps_range: [10, 18]
expected_minor_gaps_range: [4, 10]
expected_months_to_readiness_range: [14, 20]
expected_traceability_gate_passed: true
input_completeness: Standard
target_certification: Third-party certification
industry: BFSI
jurisdictions: ["India"]
claims_firewall_violations_expected: 0
---

# Test Fixture: Bank Certification Readiness — Indian Private Bank

## Context

**Client:** Hypothetical Indian private bank (publicly listed, ~1,000 branches)  
**Driver:** RBI AI governance circular references ISO 42001 as preferred framework; board mandated certification  
**AI Portfolio in scope:**
1. Credit scoring model — ML classifier; RBI model risk policy applies; partial validation documentation exists
2. Customer service chatbot — LLM-based (vendor: Anthropic via Cursory LLM Gateway); Ethana deployed
3. Fraud detection system — ensemble ML; production-critical; no formal AI governance documentation
4. Trade finance document extraction — LLM-based; recently deployed with no governance artefacts

**Upstream inputs available:**
- Regulatory mapping output: Yes (identifies ISO 42001 Clauses 4, 5, 6, 8, 9 and Annex A Categories 2, 3, 7, 9 as high-priority)
- Control mapping output: No
- Existing documentation: ISO 27001 certificate (scope: IT infrastructure), RBI SR 1/24 model risk policy (credit scoring only), data governance policy (general)

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **Jurisdiction overlay application:** RBI MRM guidance escalates Annex A Category 3 (AI Lifecycle) and Category 9 (Monitoring) gaps by one severity level for BFSI-India organisations. A reviewer who does not apply this overlay will understate severity on lifecycle and monitoring gaps.

2. **ISO 27001 partial credit — scope boundary:** The ISO 27001 scope is "IT infrastructure" — not the AI Management System. A reviewer should apply credit on Clause 7 (documentation control, resource management) and partial credit on Clause 4 (context documentation infrastructure) but not on Clause 8 (AI lifecycle has no ISO 27001 equivalent in this scope).

3. **Compliance Pack exclusion:** Compliance Pack (one-click evidence export for ISO 42001) is In Build [IB]. A reviewer tempted to cite it for Clause 9 evidence requirements must instead cite the Immutable Audit Log [P] as the evidence source and Cursory's Regulatory Gap Analysis service for the monitoring programme. Any mention of Compliance Pack as Production triggers HD2.

4. **Clause 8 depth:** The bank has four AI systems, only one of which (credit scoring) has any lifecycle documentation. A reviewer who rates Clause 8 above maturity 1 is over-crediting the partial RBI model validation — that documentation covers financial risk, not AI lifecycle governance per ISO 42001.

5. **Bias Scanner caveat:** Annex A Category 2 includes a bias risk assessment control. Ethana's Bias Scanner [P] may be cited but must carry its mandatory caveat: "runtime text filter only; does not perform statistical disparate impact analysis." The credit scoring model bias assessment requires a specialist statistical bias auditor — Bias Scanner does not substitute.

---

## Expected Section Highlights

**Section 2 — Key clause ratings:**
- Clause 4: 1 (Critical) — AIMS scope undefined; ISO 27001 scope is IT infrastructure, not AIMS
- Clause 5: 1 (Critical) — No AI policy; RBI model risk policy is not an AI policy
- Clause 6: 2 (Major) — Credit model has validation; LLM systems have nothing; no AI impact methodology
- Clause 7: 2 (Major) — ISO 27001 credit applies partially; AI competence absent
- Clause 8: 1 (Critical) — Lifecycle exists for credit model only; three systems ungoverned; RBI overlay escalates
- Clause 9: 2 (Major) — Immutable Audit Log operating for chatbot; no monitoring programme
- Clause 10: 1 (Minor) — No AI-specific corrective action

**Section 8 — Ethana Coverage:**
- Immutable Audit Log [P] → Clause 9 evidence collection (partial; caveat: logs gateway-routed calls only)
- Bias Scanner [P] → Annex A Category 2 runtime screening (partial; caveat: runtime filter, not statistical audit)
- Red Teaming Orchestrator [P] → Annex A Category 3 testing (partial)
- Compliance Pack [IB] → Section 8.5 Invalid Reference if cited; must be corrected to "Cursory Regulatory Gap Analysis service" as Cursory Service alternative

**Section 10 expected ranges:**
- AMS: 20–45 depending on evidence access during assessment
- ARS: 20–35
- Classification: Significant Gaps
- Months to readiness: 14–18

---

## Reviewer Red Flags

- AMS above 60 → reviewer has over-credited ISO 27001 or under-assessed Annex A gaps
- Compliance Pack appearing as Production in Section 8 → HD2; assessment blocked
- Clause 8 rated 3 or above → reviewer has conflated RBI model validation with ISO 42001 AI lifecycle
- Classification of Near Ready → HD6 if Critical gaps exceed 2 (expected: 4)
- Bias Scanner cited without runtime-filter caveat for the credit model bias control → HD2 (scope expansion beyond canonical model entry)
