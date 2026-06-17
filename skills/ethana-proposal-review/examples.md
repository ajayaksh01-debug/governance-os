# Ethana Proposal Review — Worked Examples

These three examples are the calibration anchors for this skill. Each example demonstrates a complete review output across the ten sections — or the sections most critical to the scenario's primary challenge. Read these before scoring any live review.

Example 1 demonstrates a clean Approved outcome with full traceability. Example 2 demonstrates a Rejected outcome driven by Critical Firewall Breaches. Example 3 demonstrates an Approved with Revisions outcome with correctly classified MRFs.

---

## Example 1: Clean Approved Review — Indian Private Bank RFP Response

**Demonstrates:** Full traceability audit; correct CTCS calculation; Approved classification under zero CFBs.

### Input

```
draft_proposal:            RFP response for Indian private bank, LLM-based credit underwriting
output_mode:               RFP Response
customer_sector:           BFSI
jurisdictions:             India
solution_mapping_output:   Available (Section 3 and Section 5)
feature_mapping_output:    Available (Section 1 and Section 6)
capability_validation_output: Available (Section 4 and Section 5)
regulatory_mapping_output: Available (Section 6)
control_mapping_output:    Available (Section 10)
Input completeness:        Full
```

---

### Phase 1 — Traceability Gate

| Gate | Status |
|---|---|
| TG-1 | Pass — full RFP response document received, 6 capability sections identified |
| TG-2 | Pass — solution-mapping output loaded; Section 3 has 8 Production capability entries; Section 5 lists 3 prohibited claims |
| TG-3 | Pass — feature-mapping output loaded; Section 1 has 6 features with TFS scores; Section 6 lists 2 prohibited feature claims |
| TG-4 | Pass — capability-validation output loaded; Section 4 has 4 Allowed Claims with CPL assignments |
| TG-5 | Pass — regulatory-mapping output loaded; Section 6 has 7 control requirements |
| TG-6 | Pass — governance-control-mapping output loaded; Section 10 has 9 Ethana configuration entries |
| TG-7 | Pass — canonical-product-model.md directly accessible; will be consulted in Phase 4 |

Input completeness: Full. CTCS ceiling: 100.

---

### Section 2 — Claim Inventory (abbreviated to 6 representative claims)

| Claim ID | Claim text (verbatim) | Claim type | Proposal section |
|---|---|---|---|
| CLM-RFP-001 | "Ethana's LLM Gateway routes and monitors all credit model prompts in real time, enforcing configurable rate limits and content policies before outputs reach the underwriting system." | Production Capability | Section 3.1 — Platform Architecture |
| CLM-RFP-002 | "The Immutable Audit Log captures every model call in a tamper-proof, insert-only event store with native export to Splunk, ensuring full regulatory audit defensibility under RBI IT Governance guidelines." | Production Capability | Section 3.2 — Compliance Architecture |
| CLM-RFP-003 | "Ethana's Runtime Guardrails PII Scanner detects and redacts personally identifiable information in model outputs before they reach downstream credit decisioning systems." | Production Capability | Section 3.3 — Data Protection |
| CLM-RFP-004 | "Ethana's Red Teaming Orchestrator runs 21 OWASP LLM Top 10 adversarial probes against the credit model on a scheduled basis, producing a certified test report for RBI submission." | Production Capability | Section 3.4 — Model Testing |
| CLM-RFP-005 | "On the roadmap, Ethana's Sentry Discovery connector will provide automated shadow AI detection across the bank's Microsoft 365 environment." | Roadmap Item | Section 5 — Future Capabilities |
| CLM-RFP-006 | "Cursory's AI Governance Advisory service will design and maintain the bank's model risk management framework aligned to RBI Circular 2023-ML-001." | Cursory Service | Section 4 — Advisory Scope |

Total claims audited: 14 (6 shown above; 8 additional in the full review).

---

### Section 3 — Claim Traceability Matrix (representative entries)

| Claim ID | Upstream source | Section reference | Traceability status |
|---|---|---|---|
| CLM-RFP-001 | solution-mapping Section 3 | "Ethana's LLM Gateway provides real-time prompt routing, rate limiting, and content policy enforcement." | Traced |
| CLM-RFP-002 | solution-mapping Section 3 + capability-validation Section 4 (Allowed Claim, CPL-2) | Solution mapping: "Immutable Audit Log — tamper-proof, insert-only event store with native SIEM export to Splunk, Elastic, and Datadog." Capability validation CPL-2 with mandatory caveat: "Application-layer insert-only — database-layer WORM not independently confirmed." Proposal text does not embed this caveat. | Partially Traced |
| CLM-RFP-003 | solution-mapping Section 3 + feature-mapping Section 1 (TFS 88) | Full Production match. PII scanner text modality constraint is disclosed in solution-mapping — "scans text-format model outputs; structured data requires supplementary controls." Proposal text does not embed this constraint. | Partially Traced |
| CLM-RFP-004 | feature-mapping Section 1 (Red Teaming Orchestrator, TFS 90) | "21 OWASP LLM Top 10 probes confirmed Production. CI/CD gate integration is In Build." Proposal does not reference CI/CD gate. 21-probe claim is exact match. | Traced |
| CLM-RFP-005 | solution-mapping Section 4 (Roadmap Disclosure) | "Sentry Discovery — In Build. Automated shadow AI detection across SaaS endpoints." Section 5 of the proposal correctly labels this as "roadmap" — disclosure is compliant. | Traced |
| CLM-RFP-006 | Not an Ethana platform claim — Cursory service; out of scope for capability audit | N/A | N/A — Cursory service claim |

**CTCS calculation:**

```
Total capability claims (excluding Cursory service claims): 13
Traced:                                                     9
Partially Traced:                                           4 × 0.5 = 2.0
Untraced:                                                   0
Prohibited:                                                 0

CTCS numerator:   9 + 2.0 = 11.0
CTCS:             (11.0 / 13) × 100 = 84.6 → 85 (rounded)
```

Note: CTCS 85 falls below the Approved threshold of 95. The Partially Traced claims (CLM-RFP-002, CLM-RFP-003, and two others) are missing mandatory caveats. This places the document at Approved with Revisions unless the caveats are added.

**Revised CTCS after adding mandatory caveats to Partially Traced claims:**
All 4 Partially Traced claims become Traced when mandatory caveats are embedded. CTCS rises to (13 / 13) × 100 = 100. Post-revision: CTCS 100.

---

### Section 4 — Capability Status Validation (key entries)

| Capability | Claimed status in proposal | Canonical model status | Match verdict | Firewall determination |
|---|---|---|---|---|
| LLM Gateway | Production | "Production. Real-time prompt routing, configurable rate limits, content policy enforcement. Available on both Build and Edge tiers." | Confirmed | Compliant |
| Immutable Audit Log | Production | "Production. Insert-only event store capturing all gateway-routed calls. Native SIEM export to Splunk, Elastic, Datadog. Application-layer insert-only path — database-layer WORM not confirmed." | Confirmed — mandatory caveat not embedded in proposal claim CLM-RFP-002 | MRF — caveat omission |
| Runtime Guardrails PII Scanner | Production | "Production. Real-time text-output scanner. Detects PII entities in LLM response text. Audio, image, and structured database fields are not scanned." | Confirmed — modality constraint not embedded in proposal claim CLM-RFP-003 | MRF — constraint omission |
| Red Teaming Orchestrator (21 probes) | Production | "Production. 21 OWASP LLM Top 10 adversarial probes. CI/CD gate integration: In Build." | Confirmed. CI/CD gate not mentioned in proposal — no false claim made. | Compliant |
| Sentry Discovery | Roadmap | "In Build. Automated shadow AI detection for network traffic and SaaS endpoints." | Confirmed — proposal correctly labels as Roadmap with no delivery commitment. | Compliant |

No Critical Firewall Breaches detected.

---

### Section 7 — Commercial Risk Register

**Major Risk Findings (MRF):**
- MRF-001: CLM-RFP-002 (Immutable Audit Log) — mandatory caveat "Application-layer insert-only — database-layer WORM not independently confirmed" is absent. In an RBI audit context, this caveat is essential — a bank regulator may challenge tamper-proof claims without evidence of database-layer enforcement. Required action: embed caveat inline in the Immutable Audit Log description in Section 3.2 of the proposal. PCS deduction: -5 points.
- MRF-002: CLM-RFP-003 (PII Scanner) — modality constraint "text-format model outputs only; structured database fields and audio not scanned" is absent. RBI data protection obligations extend to structured data. Required action: add modality constraint inline in Section 3.3 of the proposal. PCS deduction: -5 points.

**Minor Risk Findings:** None.

---

### Section 8 — Critical Firewall Breaches

No Critical Firewall Breaches detected across 13 capability claims audited against canonical-product-model.md.

---

### Section 9 — Major Risk Findings (Consolidated)

| MRF ID | Finding | Risk if unaddressed | Required action | PCS deduction |
|---|---|---|---|---|
| MRF-001 | Immutable Audit Log mandatory caveat absent in CLM-RFP-002 (Section 3.2) | RBI regulatory examiner challenges tamper-proof claim; bank discovers database-layer limitation post-contract; vendor audit fails on this point | Add inline caveat: "Immutability is enforced at the application layer — database-layer WORM enforcement has not been independently confirmed; verify with Ethana engineering before representing hardware-level immutability to a regulatory examiner." | -5 |
| MRF-002 | PII Scanner modality constraint absent in CLM-RFP-003 (Section 3.3) | Bank assumes scanner covers structured credit database fields; post-deployment gap identified; RBI compliance assessment fails | Add inline constraint: "The PII Scanner operates on text-format model outputs only. Audio, image, and structured database fields are not covered by the scanner and require supplementary data protection controls." | -5 |

---

### Section 10 — Release Decision

**Traceability Gate:**

| Gate | Status |
|---|---|
| TG-1 | Pass |
| TG-2 | Pass |
| TG-3 | Pass |
| TG-4 | Pass |
| TG-5 | Pass |
| TG-6 | Pass |
| TG-7 | Pass — canonical-product-model.md consulted directly; verbatim quotes recorded in Section 4 |

**Scoring (pre-revision):**
```
Base PCS:                          100
Critical Firewall Breaches:        0 (no CFBs)
Major Risk Findings (2 × -5):     -10
Minor Risk Findings:               0
Final PCS (pre-revision):          90 / 100

CTCS (pre-revision):               85 / 100
```

**Release Classification (pre-revision):** Conditional Release — PCS 90 ≥ 80 and CTCS 85 ≥ 60; but PCS < 95, so not Approved with Revisions on PCS alone; CTCS 85 does meet the CTCS ≥ 80 threshold for Approved with Revisions.

Actually: PCS 90 < 95 → cannot receive Approved with Revisions (requires PCS ≥ 95). Classification: **Conditional Release** (PCS ≥ 80, CTCS ≥ 60) — internal use only; external release requires correction of both MRFs and re-review.

**Scoring (post-revision — after adding mandatory caveats):**
```
Base PCS:                          100
Critical Firewall Breaches:        0
Major Risk Findings:               0 (resolved)
Minor Risk Findings:               0
Final PCS (post-revision):         100 / 100

CTCS (post-revision):              100 / 100
```

**Release Classification (post-revision): Approved**

```
Proposal Review — Release Audit Certificate
─────────────────────────────────────────────────────────────
Document reviewed:    RFP Response — Indian Private Bank Credit AI — 2026-06-17
Review date:          2026-06-17
Total claims audited: 13 (capability claims; 1 Cursory service claim excluded)
CFBs:                 0
MRFs (resolved):      2 — both resolved by embedding mandatory caveats
Minor Findings:       0
PCS:                  100 / 100 (post-revision)
CTCS:                 100 / 100 (post-revision)
Traceability Gate:    Completed 2026-06-17 — all mandatory gates passed
Release Classification: Approved
─────────────────────────────────────────────────────────────
```

---

## Example 2: Rejected — UK Insurance Pitch Deck

**Demonstrates:** CFB identification (Aspirational as Production + uncertified certification); correct Rejected classification; HD1 and HD3 prevention.

### Input

```
draft_proposal:            Pitch deck for UK commercial insurer — AI claims processing
output_mode:               Pitch Deck
customer_sector:           BFSI
jurisdictions:             UK
solution_mapping_output:   Available
feature_mapping_output:    Available
capability_validation_output: Not provided
Input completeness:        Standard
```

---

### Section 2 — Claim Inventory (key claims)

| Claim ID | Claim text (verbatim) | Claim type | Proposal section |
|---|---|---|---|
| CLM-DECK-003 | "Ethana's Visual Agent Builder enables your claims team to automate AI-driven workflow orchestration without writing code." | Production Capability | Slide 8 — Automation |
| CLM-DECK-007 | "Ethana is SOC 2 Type II certified, meeting the audit requirements of Lloyd's of London and the FCA's operational resilience framework." | Certification | Slide 12 — Trust & Compliance |
| CLM-DECK-009 | "The Ethana LLM Gateway is deployed with four major UK insurance companies today." | Production Capability | Slide 4 — Customer Evidence |

Total claims: 11.

---

### Section 4 — Capability Status Validation (critical entries)

**CLM-DECK-003 — Visual Agent Builder:**

Canonical-product-model.md entry (verbatim):
> "Visual Agent Builder — Aspirational. No-code agent construction interface. Not in active development. No ETA."

Claimed status in proposal: Production ("enables your claims team to...").
Match verdict: Critical mismatch — Aspirational capability presented as currently available Production feature.
**Firewall determination: CRITICAL FIREWALL BREACH (CFB-001)**

**CLM-DECK-007 — SOC 2 Type II:**

Canonical-product-model.md entry (verbatim):
> "SOC 2 Type II — In Build. Audit process initiated. Certification expected [no confirmed date]. Do not claim as held."

Claimed status in proposal: "SOC 2 Type II certified."
Match verdict: Uncertified certification stated as current.
**Firewall determination: CRITICAL FIREWALL BREACH (CFB-002)**

**CLM-DECK-009 — "Deployed with four major UK insurance companies":**

Canonical-product-model.md: No customer reference entry for UK insurance deployments. Customer reference claims are not in scope for this file — escalate to product marketing for confirmation.
Match verdict: Unconfirmed claim — no approved source.
**Firewall determination: CRITICAL FIREWALL BREACH (CFB-003)** — proposal makes a specific deployment claim without any confirmed upstream source.

---

### Section 8 — Critical Firewall Breaches

**CFB-001:**
- **Breach type:** Aspirational as Production
- **Proposal location:** Slide 8 — "Ethana's Visual Agent Builder enables your claims team to automate AI-driven workflow orchestration without writing code."
- **Canonical model status:** "Visual Agent Builder — Aspirational. No-code agent construction interface. Not in active development. No ETA."
- **ADR provision violated:** ADR-002 §3 (Claims Firewall — Aspirational claims may not be presented as available in any customer-facing context); ADR-005 §3 (Zero-Tolerance Firewall Gate — automatic Rejected classification)
- **Required action:** Remove the claim entirely. If workflow automation is a customer requirement, propose Cursory's Agent Design service as the current solution and reference Visual Agent Builder only in a clearly labelled "Longer-Term Roadmap" section with explicit "not in active development" disclosure.

**CFB-002:**
- **Breach type:** Uncertified certification stated as current
- **Proposal location:** Slide 12 — "Ethana is SOC 2 Type II certified, meeting the audit requirements of Lloyd's of London and the FCA's operational resilience framework."
- **Canonical model status:** "SOC 2 Type II — In Build. Certification expected [no confirmed date]. Do not claim as held."
- **ADR provision violated:** ADR-002 §4 (Certification Claims — no certification may be stated as current unless confirmed in canonical-product-model.md); ADR-005 §3 (Zero-Tolerance Firewall Gate)
- **Required action:** Replace with: "Ethana's SOC 2 Type II certification process is underway. For current engagements requiring SOC 2 Type II, Cursory provides a Data Processing Agreement and a security disclosure pack that meets most enterprise procurement requirements while certification is obtained." Do not state a completion date.

**CFB-003:**
- **Breach type:** Unconfirmed deployment claim — no approved source
- **Proposal location:** Slide 4 — "The Ethana LLM Gateway is deployed with four major UK insurance companies today."
- **Canonical model status:** No customer reference data in canonical-product-model.md. Customer reference claims require confirmation from Ethana product marketing — no approved source exists in the knowledge base.
- **ADR provision violated:** ADR-002 §2 (Claims must trace to an approved source — customer references that have not been approved for use cannot be stated as facts in proposals)
- **Required action:** Remove the specific "four major UK insurance companies" claim. Replace with general traction language only if a confirmed, approved customer reference statement exists from Ethana product marketing. If no approved reference exists, omit entirely.

---

### Section 10 — Release Decision

**Traceability Gate:** TG-1: Pass. TG-2: Pass. TG-3: Pass. TG-4: Noted absent. TG-5: Noted absent. TG-6: Noted absent. TG-7: Pass.

**Scoring:**
```
Base PCS:                          100
Critical Firewall Breaches (3):    Auto-reject → PCS = 0
Final PCS:                         0 / 100

CTCS calculation:
Total claims: 11
Traced: 5, Partially Traced: 2 (× 0.5 = 1.0), Untraced: 1, Prohibited: 3
CTCS: (5 + 1.0) / 11 × 100 = 54.5 / 100
```

**Release Classification: Rejected**

```
Proposal Review — Release Audit Certificate
─────────────────────────────────────────────────────────────
Document reviewed:    Pitch Deck — UK Commercial Insurer Claims AI — 2026-06-17
Review date:          2026-06-17
Total claims audited: 11
CFBs:                 3 (see Section 8 for required corrections)
MRFs:                 0 (CFBs override MRF classification)
Minor Findings:       0
PCS:                  0 / 100 (auto-rejected — CFBs present)
CTCS:                 54 / 100
Traceability Gate:    Completed 2026-06-17 — mandatory gates passed
Release Classification: REJECTED
─────────────────────────────────────────────────────────────
Required actions before re-submission:
1. Remove Visual Agent Builder claim (CFB-001) — see Section 8 for replacement language
2. Replace SOC 2 Type II certified claim with in-progress disclosure (CFB-002) — see Section 8
3. Remove or obtain approved customer reference for UK insurance deployment claim (CFB-003)
4. After corrections, run full re-review from Phase 1 before external release
─────────────────────────────────────────────────────────────
```

---

## Example 3: Approved with Revisions — EU Bank Governance Proposal

**Demonstrates:** In Build capability correctly classified as MRF (not CFB) when disclosed in wrong section; correct Approved with Revisions classification.

### Input

```
draft_proposal:            Formal proposal for EU bank — AI governance programme
output_mode:               Formal Proposal
customer_sector:           BFSI
jurisdictions:             EU
solution_mapping_output:   Available
feature_mapping_output:    Available
capability_validation_output: Available
regulatory_mapping_output: Available
Input completeness:        Standard (control-mapping output not provided)
```

---

### Section 4 — Capability Status Validation (critical entry)

**SCIM Provisioning (discovered in proposal Section 3.4 "Identity and Access Management"):**

Proposal claim (CLM-PROP-006): "Ethana Build supports automated SCIM provisioning, enabling the bank's identity team to synchronise user access rights with the Ethana gateway through your existing Okta identity provider."

Canonical-product-model.md entry (verbatim):
> "SCIM provisioning — In Build. Automated user lifecycle management via SCIM protocol. SSO/OIDC is Production. SCIM: not yet available. Do not commit to SCIM in proposals."

The claim presents SCIM as currently available ("supports automated SCIM provisioning") — an In Build capability stated as Production.

**Is this a CFB or MRF?**

CFB (HD2) applies when an In Build capability is "presented as currently available or deployable without explicit 'In Build — roadmap, not yet available' disclosure." The proposal provides zero disclosure that SCIM is In Build. The claim is phrased as a current capability ("Ethana Build supports...").

→ **CRITICAL FIREWALL BREACH (CFB-001):** SCIM presented as Production without disclosure.

Contrast: if the claim had read "Ethana Build will support automated SCIM provisioning on the roadmap; current deployments use SSO/OIDC with manual access reviews via Cursory," that would be an MRF (In Build disclosed but in wrong section positioning) or potentially compliant if in a Roadmap section.

---

**CI/CD Gate Integration for Red Teaming Orchestrator (CLM-PROP-009):**

Proposal claim: "The Red Teaming Orchestrator integrates with the bank's GitHub Actions pipeline to automatically trigger adversarial probe runs on every model deployment."

Canonical-product-model.md entry (verbatim):
> "Red Teaming Orchestrator — 21 OWASP LLM Top 10 probes: Production. CI/CD gate integration: In Build. GitHub Actions trigger: In Build."

The proposal's CI/CD gate claim is In Build presented as Production.

However — the proposal contains a Roadmap section (Section 5) that lists "CI/CD Gate Integration (Q3 2026 roadmap)" with no delivery commitment language. The CI/CD gate claim appears in Section 3 as a current capability (no disclosure) AND in Section 5 as a roadmap item. The appearance in Section 3 without disclosure constitutes a firewall breach.

→ **CFB-002:** CI/CD gate integration presented as Production in Section 3 (no disclosure). Section 5 correctly discloses it as roadmap — but Section 3 must be corrected.

**Corrective action for CFB-002:** Remove the CI/CD gate claim from Section 3.3 entirely. The Red Teaming Orchestrator claim should read: "Ethana's Red Teaming Orchestrator runs 21 OWASP LLM Top 10 adversarial probes against the bank's credit models. CI/CD pipeline integration is on the roadmap — see Section 5." Section 5 disclosure is compliant and no changes are required there.

---

### Section 8 — Critical Firewall Breaches

**CFB-001 — SCIM Provisioning:**
- **Proposal location:** Section 3.4, CLM-PROP-006 — "Ethana Build supports automated SCIM provisioning..."
- **Canonical status:** "In Build. Not yet available. Do not commit to SCIM in proposals."
- **Required action:** Replace with: "Ethana Build uses SSO/OIDC for identity integration (Production). Automated SCIM provisioning is on the roadmap. For this engagement, Cursory's Identity Governance service will provide access control mapping and quarterly entitlement reviews until SCIM is available."

**CFB-002 — CI/CD Gate Integration:**
- **Proposal location:** Section 3.3, CLM-PROP-009 — "integrates with the bank's GitHub Actions pipeline to automatically trigger adversarial probe runs..."
- **Canonical status:** "CI/CD gate integration: In Build."
- **Required action:** Remove CI/CD integration claim from Section 3.3. Replace with: "The Red Teaming Orchestrator runs 21 OWASP LLM Top 10 probes; CI/CD pipeline integration is on the roadmap — see Section 5 for roadmap details." Confirm Section 5 disclosure already present (compliant — no changes needed there).

---

### Section 7 — Commercial Risk Register

**Major Risk Findings:**
- MRF-001 (CLM-PROP-011): EU AI Act Annex IV technical documentation requirement cited as "addressed by Ethana's Audit Log" — Audit Log covers audit trails but not the full Annex IV documentation package (risk assessment, design documentation, training data information). Required action: add sentence: "The Immutable Audit Log addresses the audit trail component of Annex IV documentation. A full Annex IV technical documentation package requires supplementary Cursory Advisory services for design documentation and risk assessment artefacts." PCS deduction: -5 points.

---

### Section 10 — Release Decision

**Traceability Gate:** All mandatory gates (TG-1, TG-2, TG-3, TG-7) passed.

**Scoring (pre-correction):**
```
Base PCS:                     100
CFBs (2):                     Auto-reject → PCS = 0
Release Classification:       REJECTED (pre-correction)
```

**Scoring (post-correction — after CFBs removed and MRF addressed):**
```
Base PCS:                     100
CFBs:                         0 (resolved)
MRFs (1 × -5):                -5
Minor Findings:               0
Final PCS (post-correction):  95 / 100

CTCS: 14 Traced / 16 total = 87.5 / 100
```

**Release Classification (post-correction): Approved with Revisions**

PCS 95 ≥ 95 ✓ — CTCS 88 ≥ 80 ✓ — No CFBs ✓

```
Proposal Review — Release Audit Certificate
─────────────────────────────────────────────────────────────
Document reviewed:    Formal Proposal — EU Bank AI Governance — 2026-06-17
Review date:          2026-06-17
Total claims audited: 16
CFBs (resolved):      2 — SCIM and CI/CD gate claims corrected per Section 8
MRFs:                 1 — EU AI Act Annex IV scope clarification (MRF-001)
Minor Findings:       0
PCS:                  95 / 100 (post-correction)
CTCS:                 88 / 100
Traceability Gate:    Completed 2026-06-17 — all mandatory gates passed
Release Classification: Approved with Revisions
─────────────────────────────────────────────────────────────
Required actions before external release:
1. Address MRF-001: add Annex IV scope clarification sentence in Section 3.6
2. Obtain Sales Director and Compliance Director sign-off on revised proposal
3. Spot-check revised sections (3.4 and 3.3) before submission — no full re-review required
   if corrections are limited to the CFB-identified sections
─────────────────────────────────────────────────────────────
```

---

## Calibration Principles

**On CFB vs. MRF for In Build capabilities:**
An In Build capability is a CFB when it appears in a current-capabilities section without any disclosure. It is an MRF when it is disclosed in a Roadmap section but with language that could be mistaken as a commitment (e.g., "Q3 2026" without a "subject to change" qualifier). The line is: does a reasonable client reading this section believe the capability is available today?

**On CTCS and mandatory caveats:**
A claim that matches an upstream source's language but omits a mandatory caveat is Partially Traced, not Traced. Mandatory caveats are not optional enhancements — they are load-bearing parts of the claim. Example 1 demonstrates this: adding the immutability caveat and the PII scanner modality constraint moved four Partially Traced claims to Traced and raised CTCS from 85 to 100.

**On post-correction re-review:**
A Rejected document always requires a full re-review from Phase 1 before it can receive any positive Release Classification. An Approved with Revisions document requires a spot-check of the corrected sections only — a full re-review is not required if the revisions are limited to the identified MRF sections. A Conditional Release requires a full re-review of the entire document.
