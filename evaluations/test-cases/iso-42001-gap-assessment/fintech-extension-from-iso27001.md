---
fixture_id: fintech-extension-from-iso27001
skill: iso-42001-gap-assessment
description: >
  EU fintech SaaS provider with an active ISO 27001 certificate extending to an AIMS.
  Two AI systems: a credit risk API (candidate EU AI Act high-risk) and an internal HR
  hiring assistant (Azure OpenAI). Tests correct ISO 27001 Annex SL credit on Clauses
  4-7 without over-crediting AI-specific requirements, correct EU AI Act severity escalation
  on Clause 6 and 8, and correct exclusion of Discovery/Sentry [RM] from Section 8.
expected_certification_classification: Near Ready
expected_ams_range: [55, 75]
expected_ars_range: [50, 70]
expected_critical_gaps_range: [1, 3]
expected_major_gaps_range: [6, 12]
expected_minor_gaps_range: [4, 8]
expected_months_to_readiness_range: [5, 10]
expected_traceability_gate_passed: true
input_completeness: Full
target_certification: Third-party certification
industry: Technology
jurisdictions: ["EU"]
claims_firewall_violations_expected: 0
---

# Test Fixture: Fintech Extension from ISO 27001 — EU Fintech SaaS Provider

## Context

**Client:** Hypothetical EU fintech SaaS provider (500 employees, Series C; Germany and Netherlands)  
**Driver:** Investor due-diligence requirement; target ISO 42001 certification Q2 2027 alongside ISO 27001 renewal  
**AI Portfolio in scope:**
1. Credit risk API — ML classifier provided to B2B banking clients via SaaS API; subject to EU AI Act high-risk candidate assessment (Annex III, use in credit scoring)
2. HR hiring assistant — Internal tool; Azure OpenAI (GPT-4); no customer-facing use; limited-risk under EU AI Act

**Upstream inputs available:**
- Regulatory mapping output: Yes (Section 2 flags Clause 6, Clause 8, Annex A Categories 2, 3, 5, 8 as high-priority; EU AI Act high-risk classification applied)
- Control mapping output: Yes (Section 3 shows two Ethana controls operating: Red Teaming Orchestrator for credit API, LLM Gateway with Immutable Audit Log for HR assistant)
- Existing documentation: ISO 27001 certificate (scope: SaaS platform and credit risk API product; expires August 2027), DPIA for credit risk API, AI ethics statement (board-approved)

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **ISO 27001 credit precision:** The ISO 27001 certificate scope covers the SaaS platform — it overlaps with the AIMS scope for the credit risk API but not the HR assistant (which is an internal tool outside the ISO 27001 scope). A reviewer applying blanket ISO 27001 credit across both AI systems is over-crediting. Credit applies only where the ISO 27001 scope overlaps the AIMS scope.

2. **DPIA ≠ AI impact assessment:** The DPIA for the credit risk API satisfies GDPR data protection impact assessment requirements. It does not satisfy the ISO 42001 Clause 6 AI impact assessment requirement — which covers systemic AI risk (bias, opacity, accountability, societal impact), not data protection risk. A reviewer who credits the DPIA for Clause 6 will understate the Clause 6 gap.

3. **EU AI Act severity escalation:** The credit risk API is a high-risk candidate under EU AI Act Annex III. This escalates Clause 6 (planning/risk) and Clause 8 (operation/lifecycle) gaps by one severity level. Without this escalation, a reviewer will classify these as Major rather than Critical.

4. **Supply chain gap for Azure OpenAI:** The HR assistant uses Microsoft Azure OpenAI. This is an AI supply chain relationship covered by Annex A Category 5 (Supply Chain). Microsoft has not been assessed under AI governance criteria. A reviewer who marks Category 5 as N/A because "Microsoft is a trusted vendor" has miscalibrated — trusted vendor status under general procurement does not satisfy ISO 42001 Category 5 AI-specific assessment requirements.

5. **Discovery/Sentry [RM] exclusion:** Ethana's Discovery capability (AI inventory and vendor tracking) is listed as Roadmap [RM] in canonical-product-model.md. It would be a tempting reference for Annex A Category 5 supply chain risk management. It must not appear in Section 8 as a current capability. Any mention of Discovery as operational triggers HD2.

6. **Near Ready classification logic:** This organisation has 1-3 Critical gaps (Clause 6 AI impact assessment, Clause 8 AI lifecycle, possibly supply chain) but has documented closure plans in the form of a board-approved AI ethics statement and an active ISO 27001 programme. The classification should be Near Ready, not Significant Gaps — the distinction is that Near Ready permits 0-2 Critical gaps with documented remediation plans.

---

## Expected Section Highlights

**Section 2 — Key clause ratings:**
- Clause 4: 3 (Minor) — ISO 27001 credit; AIMS-specific scope extension needed for both AI systems
- Clause 5: 3 (Minor) — AI ethics statement + ISO 27001 governance structure; AI-specific role designation needed
- Clause 6: 2 (Critical, EU AI Act escalation) — DPIA does not satisfy AI impact assessment requirement
- Clause 7: 3 (Minor) — ISO 27001 infrastructure fully credited; AI competence training absent
- Clause 8: 2 (Critical, EU AI Act escalation) — ISO 27001 change management partial credit; no AI-specific lifecycle
- Clause 9: 3 (Major) — ISO 27001 audit programme credited; no AI-specific performance monitoring
- Clause 10: 3 (Minor) — ISO 27001 corrective action process credited; AI nonconformity categories undefined

**Section 8 — Ethana Coverage:**
- Immutable Audit Log [P] → Clause 9 audit evidence (partial; monitoring programme design is Cursory service)
- Red Teaming Orchestrator [P] → Annex A Category 3 testing/validation (partial; ongoing programme needed)
- LLM Gateway [P] → Clause 8 operational control of HR assistant (partial; lifecycle governance still needed)
- Discovery [RM] → Section 8.5 Invalid Reference if cited; must not appear; no alternative Production capability for AI inventory

**Section 10 expected ranges:**
- AMS: 55–72 (ISO 27001 credit significantly boosts clause scores; Annex A AI-specific controls remain partial)
- ARS: 50–68 (ISO 27001 documentation infrastructure is strong; AI-specific evidence is thin)
- Classification: Near Ready
- Months to readiness: 5–9

---

## Reviewer Red Flags

- Clause 6 rated 3 or above → reviewer has accepted DPIA as AI impact assessment (incorrect)
- Category 5 (Supply Chain) marked N/A for Azure OpenAI relationship → incorrect; Category 5 requires AI-specific assessment of all AI providers
- Discovery cited in Section 8 as addressing supply chain monitoring → HD2; Discovery is Roadmap [RM]
- Classification of Certification Ready → HD6 if Critical gaps are open (expected: 1-3)
- AMS above 75 → reviewer has over-credited ISO 27001 on Clause 8 where no AI lifecycle controls exist
