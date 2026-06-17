# Ethana Capability Validation — Worked Examples

These five examples are the calibration anchors for this skill. Each example shows a complete validation output across all nine sections. Read these before scoring any live validation — they demonstrate the evidence model, CPL assignment logic, contradiction handling, and the Phase 9 gate.

---

## Example 1: Clean Production Validation — Immutable Audit Log

**Demonstrates:** Correct Production adjudication; claim-specific CPL (two claims about the same capability with different CPLs based on caveat embedding).

### Input

```
capability_name: "Immutable Audit Log"
claim_context:   Formal Proposal
requesting_team: Advisory
```

Two claims submitted for validation:
- **Claim A**: "Ethana's Immutable Audit Log captures every gateway-routed AI call in a tamper-proof, insert-only event store with native SIEM export to Splunk, Elastic, and Datadog."
- **Claim B**: "Ethana's Immutable Audit Log captures every gateway-routed AI call in a tamper-proof, insert-only event store with native SIEM export to Splunk, Elastic, and Datadog. Immutability is enforced at the application layer — database-layer WORM enforcement has not been independently confirmed; verify with Ethana engineering before representing hardware-level immutability to a regulatory examiner."

Claim B is identical to Claim A with the mandatory caveat embedded.

---

### Section 1 — Capability Status Determination

**Validated status:** Production

**Status source (verbatim from canonical-product-model.md):**
> "Immutable Audit Log — Production. Insert-only event store capturing all gateway-routed calls. Native SIEM export to Splunk, Elastic, and Datadog. Configurable retention. Application-layer insert-only path — database-layer WORM not confirmed."

**Mandatory caveats:**
- Application-layer insert-only — immutability is enforced at the application layer, not at the database layer. Database-layer WORM enforcement has not been independently confirmed. This caveat must accompany every customer-facing claim about immutability in contexts where database-layer immutability could be inferred (regulatory, legal, compliance).

**Scope boundaries:**
- Covers: all calls routed through the Ethana LLM Gateway; export to Splunk, Elastic, and Datadog via native connectors
- Does not cover: direct database access paths that bypass the Gateway; non-Gateway AI calls; integrations beyond the three confirmed SIEM targets

**Status confidence:** Authoritative (ECS 85 — see Section 7)

---

### Section 2 — Evidence Sufficiency Summary

```
Capability:              Immutable Audit Log
Proposed claim context:  Formal Proposal
Validated status:        Production
ECS:                     85 / 100 — Authoritative

Claim A: "Ethana's Immutable Audit Log captures every gateway-routed AI call in a
tamper-proof, insert-only event store with native SIEM export to Splunk, Elastic,
and Datadog."
CPL:              CPL-2 — Advisory-restricted
                  (Mandatory caveat exists; caveat is NOT embedded in Claim A)
Sufficiency:      Conditionally Sufficient
Permitted in:     Formal Proposal (with caveat added inline before use), RFP Response
                  (with caveat), Discovery Conversation, Internal Briefing, Engineering
Restricted from:  Marketing (mandatory caveat required; not for unqualified marketing use)

Claim B: "Ethana's Immutable Audit Log captures every gateway-routed AI call in a
tamper-proof, insert-only event store with native SIEM export to Splunk, Elastic,
and Datadog. Immutability is enforced at the application layer — database-layer WORM
enforcement has not been independently confirmed; verify with Ethana engineering before
representing hardware-level immutability to a regulatory examiner."
CPL:              CPL-1 — Unrestricted
                  (Mandatory caveat IS embedded in Claim B)
Sufficiency:      Sufficient
Permitted in:     All contexts — Formal Proposal, RFP Response, Marketing, Discovery,
                  Internal Briefing, Engineering Documentation

Contradictions found:  0 — none
Escalation required:   No
```

**Note on CPL difference:** Claim A and Claim B describe the same capability with the same ECS (85). They receive different CPLs because the mandatory caveat from canonical-product-model.md is present in Claim B and absent from Claim A. CPL is assigned per claim, not per capability. A claim with the caveat embedded is CPL-1 (unrestricted); the same claim without the caveat is CPL-2 (requires caveat to be added before formal use). This is expected and correct behaviour — the ECS does not change, only the CPL.

**Scope-expansion note:** Both claims use the phrase "tamper-proof, insert-only event store." This term has been formally adjudicated in Section 4 (DT4 scope-expansion check). It is permitted only in combination with "insert-only" and the application-layer caveat; see Section 4 for the full DT4 reasoning.

---

### Section 3 — Evidence Register

| Source | Type | Claim made | Consistent with canonical model? | Authority level |
|---|---|---|---|---|
| canonical-product-model.md | Primary | "Immutable Audit Log — Production. Insert-only event store... Application-layer insert-only path — database-layer WORM not confirmed." | — | Primary |
| product-architecture-investigation.md | Approved Secondary | Confirms insert-only write path at application layer; describes architecture of SIEM export pipeline; consistent with canonical entry including immutability caveats | Yes | Secondary |
| use-cases.md | Approved Secondary | Silent — no entry corroborating a specific Immutable Audit Log Production claim in a use-case pattern | Silent | Secondary |
| Marketing playbook | Reference Only | "Tamper-proof audit trail with immutable logging and SIEM integration" — omits application-layer caveat | Expands — omits mandatory caveat | Reference Only |

---

### Section 4 — Allowed Claims

**Scope-expansion adjudication — DT4 Check 2 (Depth):** Both claims use the phrase "tamper-proof, insert-only event store." "Tamper-proof" does not appear verbatim in the canonical model entry ("insert-only event store"); the canonical capability name is "Immutable Audit Log." DT4 assessment: "tamper-proof" in combination with "insert-only" and the mandatory application-layer caveat falls within the confirmed scope of the "Immutable Audit Log" capability — the canonical name ("Immutable") encompasses tamper resistance as a design property; "insert-only" specifies the confirmed mechanism. "Tamper-proof" without the mandatory caveat, or without the "insert-only" qualifier, would constitute scope expansion — implying DB-layer or hardware-level enforcement not confirmed in the canonical model. This is precisely why Claim A receives CPL-2 (caveat required before use): without the caveat inline, "tamper-proof" makes an unqualified assurance that DT4 Check 2 would flag as a prohibited expansion. Claim B receives CPL-1 because the caveat is already embedded, fully qualifying the "tamper-proof" characterisation. DT4 result: passed for both claims in their stated forms.

```
Claim text:      "Ethana's Immutable Audit Log captures every gateway-routed AI call
                 in a tamper-proof, insert-only event store with native SIEM export to
                 Splunk, Elastic, and Datadog. Immutability is enforced at the
                 application layer — database-layer WORM enforcement has not been
                 independently confirmed; verify with Ethana engineering before
                 representing hardware-level immutability to a regulatory examiner."
CPL:             CPL-1 — Unrestricted (caveat embedded)
Permitted in:    All contexts
Required caveat: Embedded in claim — no additional caveat required
Evidence basis:  canonical-product-model.md — Production entry; ECS 85

──────────────────────────────────────────────────────────────────

Claim text:      "Ethana's Immutable Audit Log captures every gateway-routed AI call
                 in a tamper-proof, insert-only event store with native SIEM export to
                 Splunk, Elastic, and Datadog."
CPL:             CPL-2 — Advisory-restricted (caveat not embedded)
Permitted in:    Formal Proposal, RFP Response, Discovery Conversation,
                 Internal Briefing, Engineering Documentation
Required caveat: "Immutability is enforced at the application layer — database-layer
                 WORM enforcement has not been independently confirmed; verify with
                 Ethana engineering before representing hardware-level immutability to
                 a regulatory examiner."
                 This caveat must be added inline (not as a footnote) before use.
Evidence basis:  canonical-product-model.md — Production entry; ECS 85
```

---

### Section 5 — Prohibited Claims

```
Prohibited claim:   "Immutable Audit Log with hardware-level WORM storage"
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: Scope expansion — database-layer or hardware-level WORM not
                    confirmed in canonical-product-model.md
Risk if used:       Regulatory misrepresentation in BFSI or legal contexts where
                    WORM storage has a specific technical and regulatory meaning
Source of claim:    Inferred from marketing use of "immutable" without qualification

──────────────────────────────────────────────────────────────────

Prohibited claim:   "Real-time streaming audit log" or "streaming to [any target]"
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: Scope expansion — canonical model confirms event-on-write export
                    to SIEM; streaming is not confirmed
Risk if used:       Technical misrepresentation; creates false integration expectations
Source of claim:    Sometimes inferred from "SIEM export" language without reading
                    the export mechanism detail
```

---

### Section 6 — Contradiction Log

The marketing playbook (Reference Only source) presents the Immutable Audit Log without the mandatory application-layer caveat. This is an omission, not a direct contradiction of the Production status. The marketing language "tamper-proof audit trail with immutable logging" does not contradict the canonical model's Production status — it omits the qualification.

**Assessment:** This is a caveat omission, not a status contradiction. It does not trigger a status re-adjudication. It does add one Prohibited Claim (scope expansion toward hardware-level WORM implication) and requires that the marketing language not be used as-is in any formal context.

**ECS impact:** Assessed at −10 for a Reference Only source with caveat omission. Decision: not applied — see Section 7 for the full arithmetic. The ECS model's −10 adjustment applies to sources that *contradict* the canonical model — i.e., claim a different status or a different technical property. The marketing playbook does not contradict: it agrees the capability is production-ready and real; it omits the mandatory application-layer qualification. A caveat omission is incomplete representation, not contradiction. The canonical model's position ("insert-only event store, application-layer enforcement") is uncontradicted by any source. Applying −10 would penalise the evidence quality for the canonical model's position because a secondary source produced an incomplete description — which is an incorrect application of the ECS penalty rule. Final ECS adjustment from the marketing playbook: ±0.

**Full contradiction count across all sources examined: 0 direct contradictions.** The marketing playbook omission is documented above. No source directly contradicts the Production status or the insert-only mechanism.

---

### Section 7 — Evidence Confidence Score (ECS)

```
Claimed status:   Production
Path:             A — canonical model confirms Production

Base (Production confirmed in canonical-product-model.md):              +50
Rich canonical entry (insert-only path, SIEM targets named, configurable
  retention, application-layer caveat documented):                      +20
Corroboration: product-architecture-investigation.md (insert-only
  architecture confirmed with technical detail, SIEM pipeline described): +15
Marketing playbook omits mandatory caveat (Reference Only source
  with caveat omission — treated as minor conflict):                    −10 would apply...
  ...however: the omission is documented in Section 6 but does not
  constitute a source "contradicting" the canonical model status.
  The canonical model still provides the richest and most complete
  description. Applying -10 would penalise the canonical model for a
  marketing omission.
  Decision: no ECS penalty — the omission is noted in Section 6 and
  handled via the Prohibited Claims in Section 5. ECS reflects the
  quality of evidence for the canonical model's position, which is
  uncontradicted.                                                        ±0
                                                                        ────
ECS:                                                                       85 → Authoritative
```

**ECS band:** Authoritative (85–100)

---

### Section 8 — Escalation Recommendation

No escalation required. ECS 85 (Authoritative). Allowed Claims at CPL-1 (Claim B) are permitted in all contexts. Allowed Claims at CPL-2 (Claim A) are permitted in Formal Proposal and below with mandatory caveat added inline.

**Recommendation for canonical model maintainer:** The marketing playbook presents the Immutable Audit Log without the mandatory application-layer caveat. Recommend updating the playbook to reflect the caveat inline. This is not a blocking escalation — the canonical model entry is correct and complete.

---

### Section 9 — Validation Audit Trail

```
Validation date:          2026-06-17
Claims validated:         (1) Claim A — SIEM export claim without caveat
                          (2) Claim B — same claim with caveat embedded
Capability:               Immutable Audit Log
Sources checked:          (1) canonical-product-model.md — Primary, Production confirmed
                          (2) product-architecture-investigation.md — Secondary, corroborates
                          (3) use-cases.md — Secondary, Silent (no Audit Log entry)
                          (4) Marketing playbook — Reference Only, caveat omission noted
Contradictions:           0 direct contradictions; 1 caveat omission (playbook)
ECS:                      85 — Authoritative (see Section 7)
Final status:             Production
CPL assignments:          Claim A → CPL-2 (caveat not embedded)
                          Claim B → CPL-1 (caveat embedded)
Hard disqualifiers:       HQ1: not triggered (status correct)
                          HQ2: not triggered (no Aspirational in Section 4)
                          HQ3: not triggered (no scope expansion in Section 4)
                          HQ4: not triggered (no unresolved contradictions)
                          HQ5: not triggered (canonical model consulted, appears in Section 3)
                          HQ6: gate completed below
                          HQ7: not triggered (no CPL-5 in Section 4)
Phase 9 gate:             Completed. All 7 steps passed.
                          Step 1 — ECS arithmetic: verified (85 = 50+20+15)
                          Step 2 — CPL completeness: verified (both claims have CPL)
                          Step 3 — Source traceability: verified (canonical model in Section 3)
                          Step 4 — Prohibited source check: verified (no prohibited sources)
                          Step 5 — Contradiction completeness: verified (0 direct; omission noted)
                          Step 6 — Scope-expansion check: verified (no expansion in Section 4)
                          Step 7 — Audit trail: this section
Allowed Claims:           2
Prohibited Claims:        2
Escalation status:        Not required
```

---
---

## Example 2: Certification Claim Contradiction — ISO 27001

**Demonstrates:** In Build canonical status overriding a marketing Production claim; scope-expansion detection (certification not held); ECS Path B; prohibited claim with risk documentation.

### Input

```
capability_name:      "ISO 27001 certification"
proposed_claim:       "Ethana is ISO 27001 certified"
source_document:      Marketing playbook — page 7: "ISO 27001 certified security
                      posture with annual third-party audit"
claim_context:        Formal Proposal (BFSI customer — asking for the certificate)
requesting_team:      Advisory
contradiction_sources: ["marketing playbook"]
```

---

### Section 1 — Capability Status Determination

**Validated status:** In Build

**Status source (verbatim from canonical-product-model.md):**
> "ISO 27001 — In Build. Target: H2 2025. Not yet certified. No committed delivery date for customer-facing purposes."

**Mandatory caveats:**
- Ethana is not currently ISO 27001 certified. No certification has been issued. The target timeline is H2 2025 but this is not a customer-facing commitment. This caveat is mandatory whenever ISO 27001 is mentioned in any context.

**Scope boundaries:**
- ISO 27001 certification is an external attestation, not an internal control. The In Build status means the certification process is underway — it does not mean the security controls referenced by ISO 27001 are absent. The distinction matters for customer conversations.

**Status confidence:** Insufficient for any Production claim. ECS = 0 for the proposed claim "Ethana is ISO 27001 certified" (Path B — In Build cap). See Section 7.

---

### Section 2 — Evidence Sufficiency Summary

```
Capability:              ISO 27001 certification
Proposed claim context:  Formal Proposal
Validated status:        In Build
ECS:                     0 / 100 — Insufficient (Path B: In Build cap)

Claim: "Ethana is ISO 27001 certified"
CPL:              CPL-5 — Prohibited in all contexts
                  (In Build status; certification not held; scope expansion on
                  certification claim — DT4 Check 3 triggered)
Sufficiency:      Insufficient
Permitted in:     None
Restricted from:  All contexts

Contradictions found:  1 — marketing playbook vs. canonical model; resolved
Escalation required:   Yes — marketing playbook must be corrected;
                        BFSI proposal blocked pending correction
```

---

### Section 3 — Evidence Register

| Source | Type | Claim made | Consistent with canonical model? | Authority level |
|---|---|---|---|---|
| canonical-product-model.md | Primary | "ISO 27001 — In Build. Target: H2 2025. Not yet certified. No committed delivery date." | — | Primary |
| product-architecture-investigation.md | Approved Secondary | Silent on ISO 27001 certification status | Silent | Secondary |
| Marketing playbook (page 7) | Reference Only | "ISO 27001 certified security posture with annual third-party audit" | Contradicts — claims Production (certified) when canonical says In Build | Reference Only |

---

### Section 4 — Allowed Claims

No Production claims for ISO 27001 certification are permitted. The only permitted claim is an accurate In Build disclosure, and only in conversation and internal contexts.

```
Claim text:      "Ethana is actively working toward ISO 27001 certification —
                 the certification process is underway. Ethana is not currently
                 certified and no committed delivery date is available."
CPL:             CPL-3 — Conversation-only
                 (In Build accurate disclosure; DT6 In Build conversational
                 roadmap mention path)
Permitted in:    Discovery Conversation, Internal Briefing only
Required caveat: Already embedded — the claim is itself a disclosure of In Build
                 status; no additional caveat required
Evidence basis:  canonical-product-model.md — In Build entry; ECS 35 for
                 In Build disclosure (Contested: canonical clear but playbook
                 contradicts)
```

---

### Section 5 — Prohibited Claims

```
Prohibited claim:   "Ethana is ISO 27001 certified"
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: In Build status, not yet available — certification has not
                    been issued. Scope expansion — certification is an external
                    attestation; claiming it without holding it is a misrepresentation.
Risk if used:       Regulatory misrepresentation in BFSI; potential contractual
                    liability if included in an RFP response or proposal; immediate
                    trust damage if the customer requests the certificate and it
                    cannot be provided.
Source of claim:    Marketing playbook, page 7

──────────────────────────────────────────────────────────────────

Prohibited claim:   "ISO 27001 certified security posture"
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: Same as above; "certified security posture" implies holding
                    the ISO 27001 certification. The security posture may exist;
                    the certification does not.
Risk if used:       Same as above — "certified" is the legally significant word
Source of claim:    Marketing playbook, page 7 (exact language)

──────────────────────────────────────────────────────────────────

Prohibited claim:   "Ethana is ISO 27001 ready" or "ISO 27001 ready"
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: "Ready" implies imminent certification or that the external
                    audit process has been completed and certification is pending
                    issue. Neither is confirmed in the canonical model.
Risk if used:       Misleads BFSI customers who will ask for a timeline and
                    cannot be given a committed one

──────────────────────────────────────────────────────────────────

Prohibited claim:   "ISO 27001 certified with annual third-party audit"
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: Scope expansion — "annual third-party audit" implies the
                    certification cycle is active and a recent audit has been
                    completed. Not confirmed at any status level.
Risk if used:       Fabricated audit claim; immediate contractual risk
Source of claim:    Marketing playbook, page 7
```

---

### Section 6 — Contradiction Log

**Source A:** Marketing playbook, page 7 — "ISO 27001 certified security posture with annual third-party audit"

**Source B (canonical):** canonical-product-model.md — "ISO 27001 — In Build. Target: H2 2025. Not yet certified."

**Nature of contradiction:** Direct status conflict. Source A claims Production (certified); canonical model says In Build (not certified). Additionally, Source A adds "annual third-party audit" — a claim not present at any status level in the canonical model.

**Authority hierarchy:** canonical-product-model.md is Primary. Marketing playbook is Reference Only. Primary always supersedes Reference Only. There is no ambiguity in the hierarchy.

**Adjudication:** canonical-product-model.md prevails. ISO 27001 certification status is In Build. The marketing playbook entry is incorrect and must be corrected.

**Resolution:** Status in Section 1 is In Build. The proposed claim "Ethana is ISO 27001 certified" is prohibited (Section 5).

**ECS impact:** −10 (Reference Only source contradicts canonical model; applied to the In Build disclosure ECS, not to the Production claim ECS which is capped at 0 by Path B regardless).

**DT4 scope expansion:** Check 3 (Certification) also triggers independently of the contradiction. "Ethana is ISO 27001 certified" claims an external certification that canonical-product-model.md does not confirm as held. Both the contradiction (DT3) and the scope expansion (DT4) prohibit this claim — either one alone would be sufficient.

---

### Section 7 — Evidence Confidence Score (ECS)

**For the proposed claim "Ethana is ISO 27001 certified" (Production claim):**

```
Claimed status:   Production (certified)
Path:             B — canonical model shows In Build; Production claim validated

In Build cap applies: ECS = 0, regardless of any other adjustments.

Note: Even if Path A arithmetic were applied (which it must not be):
  Non-authoritative source (playbook) base:  5
  No Approved Secondary corroboration:       0
  Contradiction with canonical model:       -10 (would floor at 0)
  Result:                                    0
Both paths produce ECS = 0. Path B is the binding constraint.
                                            ────
ECS for Production claim:                   0 → Insufficient
```

**For the allowed In Build disclosure ("Ethana is actively working toward ISO 27001 certification..."):**

```
Claimed status:   In Build (accurate disclosure)
Path:             A — canonical model confirms In Build

Base (In Build status confirmed in canonical-product-model.md):     +50
Sparse entry (limited technical detail beyond status and H2 target):-5
Marketing playbook contradicts canonical position (Reference Only): -10
                                                                    ────
ECS for In Build disclosure:                                         35 → Contested
```

**ECS band for In Build disclosure:** Contested (20–44). This means the In Build disclosure is restricted to Discovery Conversation and Internal Briefing only (CPL-3) until the marketing playbook is corrected and the contradiction is resolved. Once the playbook is corrected, ECS for the In Build disclosure rises to 45 (Canonical-only) and CPL-2 becomes available for written formal use.

---

### Section 8 — Escalation Recommendation

**Escalation trigger:** ECS = 0 for the proposed Production claim. Marketing playbook contains a direct misstatement of Ethana's ISO 27001 certification status. BFSI customer is actively asking for the certificate.

**Escalation recipient:** Canonical model maintainer + Marketing team + Ethana product/compliance lead

**Specific question for Marketing team:**
"The marketing playbook on page 7 states 'ISO 27001 certified security posture with annual third-party audit.' canonical-product-model.md classifies ISO 27001 as In Build — not yet certified — with a target of H2 2025 and no committed customer-facing delivery date. The playbook statement is incorrect. Required action: (1) Remove 'ISO 27001 certified' language from playbook page 7. (2) Replace with: 'Ethana is working toward ISO 27001 certification — not yet certified, no committed delivery date.' (3) Confirm when this correction will be made."

**Specific question for Ethana product/compliance lead:**
"The canonical model states H2 2025 as the ISO 27001 target. For this BFSI customer engagement, we need to know: (1) Is the H2 2025 target still current? (2) Is there any internal milestone (e.g., gap assessment completed, audit scope defined) that can be described without creating a committed delivery expectation?"

**Interim position:** ISO 27001 certification must not be mentioned in the current BFSI proposal in any form. In discovery conversations, the advisory team may say: "Ethana is actively working toward ISO 27001 certification — not yet certified, no committed timeline for customer use." No written reference to ISO 27001 is permitted in any deliverable until this escalation is resolved.

**Downstream blocks:** Any Solution Mapping output for this BFSI customer that references ISO 27001 in Section 3 (Proposal-Safe) must be revised to Section 5 (Prohibited Claims). The SOC 2 and ISO 27001 blocker advisory applies: Advisory-First commercial motion is required for BFSI customers where certifications are procurement-critical.

---

### Section 9 — Validation Audit Trail

```
Validation date:          [current date]
Claims validated:         "Ethana is ISO 27001 certified" (proposed claim)
                          "Ethana is actively working toward ISO 27001 certification..."
                          (allowed alternative)
Capability:               ISO 27001 certification
Sources checked:          (1) canonical-product-model.md — Primary, In Build confirmed
                          (2) product-architecture-investigation.md — Secondary, Silent
                          (3) Marketing playbook (page 7) — Reference Only, Contradicts
Contradictions:           1 — marketing playbook claims Production; canonical says In Build
                          Resolved: canonical model prevails; playbook incorrect
ECS:                      0 (Production claim — Path B); 35 (In Build disclosure — Contested)
Final status:             In Build
CPL assignments:          Proposed claim ("certified") → CPL-5
                          In Build disclosure → CPL-3
Hard disqualifiers:       HQ1: not triggered (Section 1 correctly says In Build)
                          HQ2: not triggered (Aspirational not involved)
                          HQ3: not triggered (scope expansion claim correctly in Section 5)
                          HQ4: not triggered (contradiction documented in Section 6)
                          HQ5: not triggered (canonical model in Section 3)
                          HQ6: gate completed below
                          HQ7: not triggered (no CPL-5 in Section 4)
Phase 9 gate:             Completed. All 7 steps passed.
                          Step 1 — ECS arithmetic: verified (0 for Production claim;
                                   35 = 50-5-10 for In Build disclosure)
                          Step 2 — CPL completeness: verified (CPL-3 in Section 4;
                                   CPL-5 in Section 5)
                          Step 3 — Source traceability: verified
                          Step 4 — Prohibited source check: verified
                          Step 5 — Contradiction completeness: verified (1 contradiction;
                                   Section 6 has 1 entry)
                          Step 6 — Scope-expansion check: verified (Production claim
                                   correctly in Section 5; DT4 Check 3 triggered)
                          Step 7 — Audit trail: this section
Allowed Claims:           1 (CPL-3 In Build disclosure only)
Prohibited Claims:        4
Escalation status:        Required — marketing playbook correction and
                          Ethana compliance lead confirmation pending
```

---
---

## Example 3: Caveated Production — MCP Security Broker

**Demonstrates:** Sub-capability split (core Production; NHI module In Build); two separate CPL assignments for claims about the same capability; mandatory caveat that NHI is excluded from permitted claims.

### Input

```
capability_name: "MCP Security Broker"
proposed_claim:  "The MCP Security Broker manages non-human identity lifecycle
                 for AI agent pipelines."
claim_context:   Formal Proposal
requesting_team: Technical
```

Second claim also submitted for comparison:
- **Claim A (NHI)**: "The MCP Security Broker manages non-human identity lifecycle for AI agent pipelines."
- **Claim B (Core)**: "The MCP Security Broker provides call tracing and policy enforcement for AI agent pipelines running on MCP-compatible runtimes."

---

### Section 1 — Capability Status Determination

**Validated status (by sub-capability):**

| Sub-capability | Status |
|---|---|
| Core (call tracing, policy enforcement, gateway integration) | Production |
| NHI (non-human identity) lifecycle management module | In Build |

**Status source (verbatim from canonical-product-model.md):**
> "MCP Security Broker — Core: Production. Call tracing across MCP-compatible agent runtimes. Policy enforcement at the MCP protocol layer. Approximately 8,000 lines of implementation code. NHI (Non-Human Identity) module: In Build. Lifecycle management for agent identities — not yet shipped."

**Mandatory caveats:**
- MCP Security Broker core operates only with MCP-compatible agent runtimes. Non-MCP agent pipelines (LangGraph, CrewAI operating outside MCP) are not covered by this capability without additional integration confirmation.
- The NHI lifecycle management module is In Build and must not be included in any Production claim or POC scope.

**Scope boundaries — Core Production:**
- Covers: call tracing, policy enforcement, gateway integration for MCP-compatible runtimes
- Does not cover: non-MCP runtimes without separate integration confirmation; NHI lifecycle management (In Build)

**Status confidence (Core):** Corroborated (ECS 75 — see Section 7)
**Status confidence (NHI claim):** Insufficient (ECS 0 — Path B)

---

### Section 2 — Evidence Sufficiency Summary

```
Capability:              MCP Security Broker
Proposed claim context:  Formal Proposal
Validated status:        Production (Core) / In Build (NHI module)
ECS (Core):              75 / 100 — Corroborated
ECS (NHI claim):         0 / 100 — Insufficient (Path B)

Claim A: "The MCP Security Broker manages non-human identity lifecycle for
AI agent pipelines."
CPL:              CPL-5 — Prohibited in all contexts
                  (NHI module is In Build; this claim addresses only NHI)
Sufficiency:      Insufficient
Permitted in:     None
Restricted from:  All contexts

Claim B: "The MCP Security Broker provides call tracing and policy enforcement
for AI agent pipelines running on MCP-compatible runtimes."
CPL:              CPL-2 — Advisory-restricted
                  (Core is Production, ECS 75 Corroborated; mandatory caveat
                  not embedded — MCP-compatible runtime scope and NHI In Build
                  status must be disclosed)
Sufficiency:      Conditionally Sufficient
Permitted in:     Formal Proposal (with mandatory caveat inline), RFP Response,
                  Discovery, Internal, Engineering
Restricted from:  Marketing (mandatory caveat required)

Contradictions found:  0 — none
Escalation required:   No
```

---

### Section 3 — Evidence Register

| Source | Type | Claim made | Consistent with canonical model? | Authority level |
|---|---|---|---|---|
| canonical-product-model.md | Primary | Core Production (call tracing, policy enforcement); NHI In Build — verbatim above | — | Primary |
| product-architecture-investigation.md | Approved Secondary | Confirms MCP protocol layer architecture; ~8,000 lines of code corroborated; SIEM integration path described; does not address NHI module | Yes (for core) | Secondary |
| Marketing playbook | Reference Only | "MCP Security Broker — full agent identity and lifecycle management with policy enforcement" | Expands — "full agent identity and lifecycle management" implies NHI; NHI is In Build | Reference Only |

---

### Section 4 — Allowed Claims

```
Claim text:      "The MCP Security Broker provides call tracing and policy enforcement
                 for AI agent pipelines running on MCP-compatible runtimes. Non-Human
                 Identity (NHI) lifecycle management is in active development and not
                 yet available — it is excluded from this proposal's scope."
CPL:             CPL-2 — Advisory-restricted
                 (Core is Production; mandatory caveats embedded — MCP runtime
                 scope and NHI In Build status both stated inline)
Permitted in:    Formal Proposal, RFP Response, Discovery, Internal, Engineering
Required caveat: Already embedded in this claim. If a shorter version of the
                 claim is needed, the following caveat must be added inline:
                 "NHI lifecycle management is In Build — not in scope.
                 Applies to MCP-compatible runtimes only."
Evidence basis:  canonical-product-model.md — Production entry (core);
                 product-architecture-investigation.md corroborates; ECS 75

──────────────────────────────────────────────────────────────────

Claim text:      "The MCP Security Broker is in active development. When the NHI
                 module ships, it will manage non-human identity lifecycle for agent
                 pipelines. No committed delivery date."
CPL:             CPL-3 — Conversation-only
                 (In Build accurate disclosure for NHI module; DT2 conversational
                 roadmap mention path)
Permitted in:    Discovery Conversation, Internal Briefing only
Required caveat: Already embedded — explicit "no committed delivery date" required
Evidence basis:  canonical-product-model.md — NHI In Build entry; ECS 35 for
                 this disclosure (Contested: playbook contradicts by implying NHI
                 is Production)
```

---

### Section 5 — Prohibited Claims

```
Prohibited claim:   "The MCP Security Broker manages non-human identity lifecycle
                    for AI agent pipelines."
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: In Build, not yet available — NHI module is classified as
                    In Build in canonical-product-model.md
Risk if used:       Customer expects NHI lifecycle management as a deliverable;
                    POC scoped with NHI fails; contractual exposure
Source of claim:    The proposed claim (input to this validation)

──────────────────────────────────────────────────────────────────

Prohibited claim:   "Full agent identity and lifecycle management"
                    or any language implying NHI is currently available
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: Scope expansion — "full agent identity and lifecycle
                    management" implies NHI module is Production; it is In Build
Risk if used:       Same as above; marketing playbook language must be replaced
Source of claim:    Marketing playbook (exact phrase)
```

---

### Section 6 — Contradiction Log

The marketing playbook describes the MCP Security Broker as offering "full agent identity and lifecycle management." This implies the NHI module is Production. canonical-product-model.md classifies the NHI module as In Build.

**Nature:** Scope expansion. The marketing claim expands the scope of what is Production to include a capability that is In Build.

**Adjudication:** canonical-product-model.md prevails. The NHI module is In Build. Marketing playbook language is incorrect for the NHI module specifically — the core capability description is accurate but the expansion to "full agent identity" is not.

**Resolution:** Core Production claims permitted (Section 4). NHI Production claims prohibited (Section 5). Marketing playbook should be updated to separate core (Production) and NHI (In Build) descriptions.

**ECS impact:** −10 (Reference Only source with scope expansion; applied to the NHI In Build disclosure ECS, reducing it to Contested territory).

---

### Section 7 — Evidence Confidence Score (ECS)

**For Claim A (NHI Production claim):**

```
Claimed status:   Production (NHI lifecycle management)
Path:             B — NHI module is In Build; Production claim validated

In Build cap: ECS = 0
                                                        ────
ECS for NHI Production claim:                           0 → Insufficient
```

**For Claim B (Core Production claim):**

```
Claimed status:   Production (core — call tracing, policy enforcement)
Path:             A — canonical model confirms Core as Production

Base (Production confirmed for core):                    +50
Moderate richness (~8,000 lines, protocol layer, policy
  enforcement, call tracing documented):                  +10
  (Not maximum +20 — entry is less technically specific
  than Audit Log canonical entry; no performance figures)
Corroboration: product-architecture-investigation.md
  (MCP protocol architecture and code scale confirmed):   +15
No approved secondary source contradicts core:            ±0
                                                         ────
ECS for Core Production claim:                            75 → Corroborated
```

**DT6 for Claim B:** ECS 75 (Corroborated) + Production + mandatory caveats exist (MCP runtime scope, NHI exclusion). Is the caveat embedded in Claim B as submitted? The submitted version of Claim B says "for AI agent pipelines running on MCP-compatible runtimes" — the MCP runtime caveat is partially embedded (MCP-compatible runtimes mentioned) but the NHI exclusion is not. CPL-2 applies: the NHI exclusion caveat must be added inline before formal use.

---

### Section 8 — Escalation Recommendation

No escalation required for the core capability. ECS 75 (Corroborated). Core claims at CPL-2 are permitted in Formal Proposal with mandatory caveats inline.

**Recommendation for marketing team:** The playbook's "full agent identity and lifecycle management" language implies NHI is Production. Recommend splitting the MCP Security Broker description into two explicit sections: (1) Core — Production, available now; (2) NHI module — In Build, not yet available. The single combined description creates consistent scope-expansion errors in downstream usage.

---

### Section 9 — Validation Audit Trail

```
Validation date:          [current date]
Claims validated:         (A) NHI lifecycle management claim (proposed)
                          (B) Core tracing/policy enforcement claim
Capability:               MCP Security Broker (sub-capabilities evaluated separately)
Sources checked:          (1) canonical-product-model.md — Primary
                          (2) product-architecture-investigation.md — Secondary, corroborates core
                          (3) Marketing playbook — Reference Only, scope expansion on NHI
Contradictions:           1 — playbook implies NHI is Production; canonical says In Build
                          Resolved: canonical prevails; playbook scope expansion noted
ECS:                      0 for NHI claim (Path B); 75 for core claim (Corroborated)
Final status:             Core Production; NHI In Build
CPL assignments:          Claim A (NHI) → CPL-5
                          Core with caveats embedded → CPL-2
                          NHI In Build disclosure → CPL-3
Hard disqualifiers:       HQ1: not triggered
                          HQ2: not triggered
                          HQ3: not triggered (NHI claim correctly in Section 5)
                          HQ4: not triggered (playbook contradiction in Section 6)
                          HQ5: not triggered
                          HQ6: gate completed below
                          HQ7: not triggered
Phase 9 gate:             Completed. All 7 steps passed.
                          Step 1 — ECS arithmetic: verified (0 for NHI; 75 = 50+10+15 for core)
                          Step 2 — CPL completeness: verified
                          Step 3 — Source traceability: verified
                          Step 4 — Prohibited source check: verified
                          Step 5 — Contradiction completeness: verified (1 contradiction in Section 6)
                          Step 6 — Scope-expansion check: verified (NHI claim in Section 5)
                          Step 7 — Audit trail: this section
Allowed Claims:           2 (core CPL-2; NHI In Build disclosure CPL-3)
Prohibited Claims:        2
Escalation status:        Not required (marketing recommendation noted — non-blocking)
```

---
---

## Example 4: Aspirational Trap — Visual Agent Builder

**Demonstrates:** Aspirational capability correctly prohibited in all contexts; no escalation path exists for Aspirational; the trap of including an Aspirational feature in a proposal to appear competitive.

### Input

```
capability_name: "Visual Agent Builder"
proposed_claim:  "Ethana's Visual Agent Builder enables rapid no-code AI agent
                 deployment without developer resources."
claim_context:   Formal Proposal
requesting_team: Advisory
```

Context: The advisory team is competing against a vendor who has a no-code agent builder. The team wants to include Visual Agent Builder in the proposal to close the gap.

---

### Section 1 — Capability Status Determination

**Validated status:** Aspirational

**Status source (verbatim from canonical-product-model.md):**
> "Visual Agent Builder — Aspirational. No-code builder for agent pipelines. Not on committed roadmap. Not in active development."

**Mandatory caveats:**
- Visual Agent Builder is Aspirational and must not be mentioned in any customer-facing context under any framing. There is no permitted claim — not as a roadmap item, not as "coming soon," not as a design concept. It is not on a committed roadmap.

**Scope boundaries:** None applicable — the capability does not exist at any claimable status.

**Status confidence:** Not applicable. The status is definitively Aspirational. ECS = 0 (Path C). No further analysis is required for a status determination.

---

### Section 2 — Evidence Sufficiency Summary

```
Capability:              Visual Agent Builder
Proposed claim context:  Formal Proposal
Validated status:        Aspirational
ECS:                     0 / 100 — Insufficient (Path C: Aspirational)

Claim: "Ethana's Visual Agent Builder enables rapid no-code AI agent deployment
without developer resources."
CPL:              CPL-5 — Prohibited in all contexts
                  (Aspirational status — DT2 Aspirational path)
Sufficiency:      Insufficient
Permitted in:     None — including Internal Briefing and Engineering Documentation
                  if the intent is to represent it as an available or roadmap capability
Restricted from:  All contexts

Note: The advisory team's intent to use this capability to close a competitive
gap does not change the status. An Aspirational capability cannot be included
in a proposal under any framing without creating a false customer expectation.

Contradictions found:  0
Escalation required:   No — the Aspirational classification is definitive.
                       No escalation path changes an Aspirational status;
                       only a canonical model update can change this, and only
                       if the product team has moved the capability onto the roadmap.
```

---

### Section 3 — Evidence Register

| Source | Type | Claim made | Consistent with canonical model? | Authority level |
|---|---|---|---|---|
| canonical-product-model.md | Primary | "Visual Agent Builder — Aspirational. Not on committed roadmap. Not in active development." | — | Primary |
| product-architecture-investigation.md | Approved Secondary | Silent on Visual Agent Builder | Silent | Secondary |
| Marketing playbook | Reference Only | Visual Agent Builder mentioned as a "vision" capability in future roadmap section | Consistent (also aspirational framing) | Reference Only |

---

### Section 4 — Allowed Claims

No claims are permitted. Visual Agent Builder is Aspirational and may not be mentioned in any customer-facing context under any framing.

**Section 4 is empty for this validation.**

For the advisory team's competitive gap problem: the correct path is to acknowledge the gap honestly using the Cursory bridge (see Section 8), not to claim a capability that does not exist.

---

### Section 5 — Prohibited Claims

```
Prohibited claim:   "Ethana's Visual Agent Builder enables rapid no-code AI agent
                    deployment without developer resources."
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: Aspirational capability — not on committed roadmap, not in
                    active development
Risk if used:       Customer expects a demonstrable product feature; POC failure
                    when the feature cannot be shown; loss of customer trust;
                    potential contractual misrepresentation in a signed proposal
Source of claim:    Advisory team's proposed competitive response

──────────────────────────────────────────────────────────────────

Prohibited claim:   Any reference to Visual Agent Builder as a planned, upcoming,
                    or roadmap feature in any customer-facing document
CPL:                CPL-5 — Prohibited in all external contexts
                    (Internal engineering/product use of "Aspirational" label is
                    permitted for internal planning purposes only)
Prohibition reason: Not on committed roadmap — a roadmap mention implies a commitment
                    that does not exist; Aspirational means uncommitted
Risk if used:       Customer makes procurement decision based on expected future
                    capability that may never ship; trust and legal exposure
Source of claim:    General pattern — advisory teams sometimes use "vision capabilities"
                    as competitive responses

──────────────────────────────────────────────────────────────────

Prohibited claim:   "Ethana is building a no-code agent builder"
CPL:                CPL-5 — Prohibited in all external contexts
Prohibition reason: Aspirational — "not in active development" means no build activity
                    exists to claim. "Building" implies active In Build status.
Risk if used:       Misrepresents development activity; creates expectation of delivery
Source of claim:    Anticipated inference from the "Aspirational" label if misread
                    as "In Build"
```

---

### Section 6 — Contradiction Log

No contradictions found across 3 sources examined. canonical-product-model.md, product-architecture-investigation.md, and the marketing playbook are all consistent: Visual Agent Builder is not presented as a Production or In Build capability in any source.

---

### Section 7 — Evidence Confidence Score (ECS)

```
Claimed status:   Production (the proposed claim implies availability)
Path:             C — canonical model shows Aspirational; any claim validated

Aspirational cap applies: ECS = 0, regardless of any other factors.
No adjustments applicable.
                                                        ────
ECS:                                                    0 → Insufficient
```

---

### Section 8 — Escalation Recommendation

No escalation required. The Aspirational classification is definitive. No escalation to engineering, product, or canonical model maintainer will change an Aspirational status — only the product team deciding to put this capability on the active roadmap changes the status, which would then require a canonical model update, which would trigger a re-adjudication of this validation.

**Guidance for the advisory team on the competitive gap:**

The competitor's no-code agent builder creates a genuine gap in Ethana's current offer. The correct response to this gap is not to claim a capability that does not exist — it is one of:
1. Acknowledge the gap directly: "Ethana does not currently have a no-code agent builder. Building agent pipelines requires developer resources using the MCP Security Broker and LLM Gateway APIs."
2. Reframe the competitive positioning: "Ethana's architecture is designed for enterprise engineering teams — not citizen developers. If no-code accessibility is a primary procurement criterion, this may not be the right tool for your organisation at this stage."
3. Use the Cursory bridge: Cursory can provide advisory on building a governed agent pipeline architecture using Ethana's Production capabilities, which may address the underlying need even without a no-code builder.
4. Wait for product team update: If the product team upgrades Visual Agent Builder from Aspirational to In Build, this validation should be re-run at that time.

---

### Section 9 — Validation Audit Trail

```
Validation date:          [current date]
Claims validated:         "Ethana's Visual Agent Builder enables rapid no-code AI
                          agent deployment without developer resources."
Capability:               Visual Agent Builder
Sources checked:          (1) canonical-product-model.md — Primary, Aspirational confirmed
                          (2) product-architecture-investigation.md — Secondary, Silent
                          (3) Marketing playbook — Reference Only, aspirational framing (consistent)
Contradictions:           0 — no contradictions across 3 sources
ECS:                      0 — Path C (Aspirational)
Final status:             Aspirational
CPL assignments:          Proposed claim → CPL-5
                          All other claims for this capability → CPL-5
Hard disqualifiers:       HQ1: not triggered (Section 1 correctly says Aspirational)
                          HQ2: not triggered (no Aspirational claim in Section 4)
                          HQ3: not triggered (DT4 not reached — DT2 exits at Aspirational)
                          HQ4: not triggered (no contradictions)
                          HQ5: not triggered
                          HQ6: gate completed below
                          HQ7: not triggered (Section 4 is empty — no CPL-5 in it)
Phase 9 gate:             Completed. All 7 steps passed.
                          Step 1 — ECS arithmetic: verified (0 — Path C; no arithmetic required)
                          Step 2 — CPL completeness: Section 4 is empty; Section 5 has CPL-5
                          Step 3 — Source traceability: verified
                          Step 4 — Prohibited source check: verified
                          Step 5 — Contradiction completeness: "No contradictions found
                                   across 3 sources" — documented in Section 6
                          Step 6 — Scope-expansion check: not applicable — DT2 exits at
                                   Aspirational before DT4 is reached
                          Step 7 — Audit trail: this section
Allowed Claims:           0
Prohibited Claims:        3
Escalation status:        Not required — Aspirational classification is definitive
```

---
---

## Example 5: Contested Status — Ethana Discovery

**Demonstrates:** Roadmap slide contradicting canonical In Build status; two ECS computations (one for an incorrect Production claim, one for an accurate In Build disclosure); why the accurate disclosure is CPL-3 rather than CPL-2 until the contradiction is resolved.

### Input

```
capability_name:       "Ethana Discovery"
claim_context:         Discovery Conversation (pre-proposal)
requesting_team:       Sales
contradiction_sources: ["Q2 internal product roadmap slide"]
```

Context: A sales engineer sent a customer a link to an internal Q2 roadmap slide deck. The slide shows "Ethana Discovery — Available Q3." The customer is now asking when they can get access. The sales team wants to know what they can say.

Additional claims to validate:
- **Claim A (Production)**: "Ethana Discovery is available now — you can access it in Q3."
- **Claim B (In Build disclosure)**: "Ethana Discovery is currently in development and not yet available. We'll share updates when we have a concrete timeline."

---

### Section 1 — Capability Status Determination

**Validated status:** In Build

**Status source (verbatim from canonical-product-model.md):**
> "Ethana Discovery — In Build. Shadow AI inventory, AI usage classification, and application risk scoring. Not yet available. No committed customer-facing delivery date."

**Mandatory caveats:**
- No committed delivery date exists for customer-facing use. The H2 / Q3 reference in the roadmap slide is an internal planning milestone, not a customer commitment. Stating or implying a specific delivery date is prohibited.
- "Available Q3" in the roadmap slide was an internal estimate, not a product announcement.

**Scope boundaries:**
- In Build capabilities include: shadow AI inventory, AI usage classification, application risk scoring
- None of these sub-capabilities may be demonstrated or included in any proposal scope

**Status confidence:** Insufficient for any Production claim. ECS = 0 for Claim A. ECS = 35 for Claim B (In Build accurate disclosure) — Contested, because the roadmap slide contradicts canonical status. See Section 7.

---

### Section 2 — Evidence Sufficiency Summary

```
Capability:              Ethana Discovery
Proposed claim context:  Discovery Conversation
Validated status:        In Build
ECS (Production claim):  0 / 100 — Insufficient (Path B: In Build cap)
ECS (In Build disclosure): 35 / 100 — Contested

Claim A: "Ethana Discovery is available now — you can access it in Q3."
CPL:              CPL-5 — Prohibited in all contexts
                  (In Build status; "available" and "Q3 access" are Production
                  framing for an In Build capability)
Sufficiency:      Insufficient
Permitted in:     None
Restricted from:  All contexts

Claim B: "Ethana Discovery is currently in development and not yet available.
We'll share updates when we have a concrete timeline."
CPL:              CPL-3 — Conversation-only
                  (In Build accurate disclosure at Contested ECS — CPL-3 is
                  the maximum permitted. Once the roadmap slide contradiction
                  is resolved, ECS rises to Canonical-only and CPL-2 becomes
                  available for written use.)
Sufficiency:      Conditionally Sufficient (conversation contexts only)
Permitted in:     Discovery Conversation, Internal Briefing only
Restricted from:  Formal Proposal, RFP Response, Marketing, any written deliverable

Contradictions found:  1 — Q2 roadmap slide ("Available Q3") vs. canonical
                       model ("In Build, no committed delivery date"); resolved
Escalation required:   Yes — roadmap slide must be corrected;
                       customer expectation must be reset
```

---

### Section 3 — Evidence Register

| Source | Type | Claim made | Consistent with canonical model? | Authority level |
|---|---|---|---|---|
| canonical-product-model.md | Primary | "Ethana Discovery — In Build. No committed customer-facing delivery date." | — | Primary |
| product-architecture-investigation.md | Approved Secondary | Silent on Ethana Discovery (early architecture phase; not yet documented) | Silent | Secondary |
| Q2 internal product roadmap slide | Reference Only | "Ethana Discovery — Available Q3" | Contradicts — implies Production availability; canonical says In Build | Reference Only |

---

### Section 4 — Allowed Claims

```
Claim text:      "Ethana Discovery is currently in development and not yet available.
                 We'll share updates when we have a concrete timeline."
CPL:             CPL-3 — Conversation-only
                 (ECS 35 — Contested; roadmap slide contradicts canonical In
                 Build position; until the slide is corrected, the In Build
                 disclosure carries Contested ECS and cannot appear in writing)
Permitted in:    Discovery Conversation, Internal Briefing only
Required caveat: Do not imply a Q3 timeline or any specific delivery date.
                 If the customer asks "when?", the permitted answer is:
                 "We don't have a committed customer date to share yet —
                 I'll let you know when we do."
Evidence basis:  canonical-product-model.md — In Build entry; ECS 35 (Contested)
```

---

### Section 5 — Prohibited Claims

```
Prohibited claim:   "Ethana Discovery is available now — you can access it in Q3."
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: In Build, not yet available; "available now" and "access in Q3"
                    are Production framing
Risk if used:       Customer expects a product they can evaluate in Q3; this has
                    already happened with the roadmap slide; continued use amplifies
                    the misaligned expectation
Source of claim:    Claim A (the proposed claim); inferred from roadmap slide

──────────────────────────────────────────────────────────────────

Prohibited claim:   "Ethana Discovery will be available in Q3" or any claim that
                    cites a specific delivery timeline
CPL:                CPL-5 — Prohibited in all external contexts
Prohibition reason: No committed delivery date — canonical model explicitly states
                    "no committed customer-facing delivery date." A Q3 reference
                    converts an internal planning milestone into a customer commitment.
Risk if used:       Contractual expectation; customer may make procurement decisions
                    based on a Q3 delivery that is not committed
Source of claim:    Q2 roadmap slide (internal planning estimate mistakenly shared)

──────────────────────────────────────────────────────────────────

Prohibited claim:   Any specific feature claim about Discovery (shadow AI inventory
                    results, application risk scores, AI usage classification reports)
                    presented as currently available
CPL:                CPL-5 — Prohibited in all external contexts
Prohibition reason: All Discovery sub-capabilities are In Build — not available
                    for demonstration or validation
Risk if used:       Creates false feature expectations; POC failure if scoped with
                    Discovery capabilities
Source of claim:    Anticipated inference from "Available Q3" framing
```

---

### Section 6 — Contradiction Log

**Source A:** Q2 internal product roadmap slide — "Ethana Discovery — Available Q3"

**Source B (canonical):** canonical-product-model.md — "Ethana Discovery — In Build. No committed customer-facing delivery date."

**Nature of contradiction:** Direct status conflict. Source A implies Production availability (Available Q3 = product is ready or will be ready by Q3 for customer access). canonical-product-model.md classifies Discovery as In Build with no committed delivery date.

**Additional conflict:** Source A provides a specific delivery timeline (Q3). The canonical model explicitly prohibits a committed customer-facing delivery date. Source A's Q3 reference converts an internal milestone into an implied customer commitment.

**Authority hierarchy:** canonical-product-model.md is Primary. Q2 roadmap slide is Reference Only (internal planning document). Primary supersedes Reference Only without exception.

**Adjudication:** canonical-product-model.md prevails. Discovery is In Build. The "Available Q3" language in the roadmap slide is incorrect for customer-facing use and must not be repeated. The Q3 milestone is an internal planning estimate that must not be shared with customers without explicit product team approval for a customer commitment.

**Resolution:** Section 1 status is In Build. Claim A is prohibited. Claim B (In Build accurate disclosure) is permitted at CPL-3.

**ECS impact:** −10 (Reference Only source contradicts canonical In Build position; applied to the In Build disclosure ECS).

**What should have happened:** The Q2 roadmap slide should have been marked "internal use only — do not share with customers." Sharing it with a customer without clearance from the product team created the expectation problem this validation is now managing.

---

### Section 7 — Evidence Confidence Score (ECS)

**For Claim A (Production claim: "Available Q3"):**

```
Claimed status:   Production (Available)
Path:             B — canonical model shows In Build; Production claim validated

In Build cap: ECS = 0
                                                        ────
ECS for Production claim:                               0 → Insufficient
```

**For Claim B (In Build accurate disclosure):**

```
Claimed status:   In Build (accurate disclosure — "currently in development")
Path:             A — canonical model confirms In Build

Base (In Build confirmed in canonical-product-model.md):           +50
Sparse canonical entry (limited technical detail;
  sub-capabilities listed but not architecturally described;
  no performance figures):                                           -5
Q2 roadmap slide (Reference Only) contradicts canonical
  In Build position by implying Production availability:            -10
No Approved Secondary corroboration:                                 ±0
                                                                    ────
ECS for In Build disclosure:                                         35 → Contested
```

**ECS band for Claim B:** Contested (20–44). DT6 → CPL-3 (Conversation-only).

**What happens to ECS when the roadmap slide is corrected:**
After the contradiction is resolved (roadmap slide corrected to say "In Build — not yet available for customers"), the −10 Reference Only contradiction adjustment is removed.
Revised ECS: 50 − 5 = 45 → Canonical-only.
At ECS 45 (Canonical-only): DT6 → CPL-2 (Advisory-restricted).
At CPL-2, the In Build disclosure can appear in written formal deliverables (Formal Proposal, RFP Response) with mandatory caveat inline.

This is the concrete benefit of resolving the escalation: CPL improves from CPL-3 (conversation only) to CPL-2 (written formal use permitted).

---

### Section 8 — Escalation Recommendation

**Escalation trigger:** Active customer expectation mismatch created by the roadmap slide. Sales engineer shared an internal planning document with a customer who is now expecting Q3 access. ECS = 35 (Contested) for the In Build disclosure — written formal use is blocked until the contradiction is resolved.

**Escalation recipient 1 — Product team:**
"The Q2 internal product roadmap slide for Ethana Discovery states 'Available Q3.' canonical-product-model.md classifies Discovery as In Build with no committed customer-facing delivery date. The slide has been shared with [customer name]. Required action: (1) Confirm whether any updated Discovery timeline exists that can be communicated to customers. (2) If Q3 remains an internal planning estimate only — not a customer commitment — confirm this in writing so the advisory team can correct the customer's expectation. (3) If a customer-facing milestone is now available, update canonical-product-model.md and we will re-run this validation."

**Escalation recipient 2 — Sales engineer:**
"The Q2 roadmap slide shared with [customer name] created an expectation that Ethana Discovery will be available in Q3. This is an internal planning estimate, not a customer commitment. Do not share roadmap slides with customers without product team approval for customer-facing use. In the next conversation with this customer, use the permitted Claim B language: 'Ethana Discovery is currently in development and not yet available. We'll share updates when we have a concrete timeline.' Do not reference Q3."

**Interim position:** Discovery must not be mentioned as a deliverable or POC candidate in any current engagement with this customer. The In Build disclosure (Claim B) may be used in conversation to reset the expectation. No written reference to Discovery or its timeline is permitted in any deliverable until escalation resolves.

**Downstream blocks:** Any Solution Mapping output for this customer that includes Discovery in Section 3 (Proposal-Safe) must be revised. Discovery belongs in Section 4 (Roadmap) at most — with explicit In Build disclosure and no delivery date.

---

### Section 9 — Validation Audit Trail

```
Validation date:          [current date]
Claims validated:         (A) "Ethana Discovery is available now — you can access it in Q3."
                          (B) "Ethana Discovery is currently in development and not yet
                              available. We'll share updates when we have a concrete timeline."
Capability:               Ethana Discovery
Sources checked:          (1) canonical-product-model.md — Primary, In Build confirmed
                          (2) product-architecture-investigation.md — Secondary, Silent
                          (3) Q2 internal product roadmap slide — Reference Only, Contradicts
Contradictions:           1 — roadmap slide ("Available Q3") vs. canonical model ("In Build,
                          no committed delivery date")
                          Resolved: canonical model prevails; slide is incorrect for
                          customer use; escalation required
ECS:                      0 for Claim A (Production claim — Path B)
                          35 for Claim B (In Build disclosure — Contested)
Final status:             In Build
CPL assignments:          Claim A → CPL-5
                          Claim B (In Build disclosure) → CPL-3
Hard disqualifiers:       HQ1: not triggered (Section 1 correctly says In Build)
                          HQ2: not triggered (Aspirational not involved)
                          HQ3: not triggered (Production claim correctly in Section 5;
                               In Build disclosure in Section 4 makes no scope expansion)
                          HQ4: not triggered (contradiction documented in Section 6)
                          HQ5: not triggered (canonical model in Section 3)
                          HQ6: gate completed below
                          HQ7: not triggered (no CPL-5 in Section 4)
Phase 9 gate:             Completed. All 7 steps passed.
                          Step 1 — ECS arithmetic: verified (0 for Claim A — Path B;
                                   35 = 50-5-10 for Claim B)
                          Step 2 — CPL completeness: verified (CPL-3 in Section 4;
                                   CPL-5 in Section 5)
                          Step 3 — Source traceability: verified (all 3 sources named)
                          Step 4 — Prohibited source check: verified (roadmap slide
                                   listed as Reference Only, not Primary or Secondary)
                          Step 5 — Contradiction completeness: verified (1 Contradicts
                                   row in Section 3; 1 entry in Section 6)
                          Step 6 — Scope-expansion check: verified (Claim B makes no
                                   scope expansion; it accurately describes In Build status)
                          Step 7 — Audit trail: this section
Allowed Claims:           1 (Claim B — CPL-3)
Prohibited Claims:        3
Escalation status:        Required — product team and sales engineer escalation packages
                          prepared in Section 8
```
