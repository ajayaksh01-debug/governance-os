---
fixture_id: production-capability-request
skill: ethana-capability-validation
description: >
  Clean Production capability validation — Immutable Audit Log submitted for a
  formal proposal to a UK retail bank. Two claims submitted for concurrent
  validation: Claim A without the mandatory caveat (expects CPL-2), Claim B
  with the mandatory caveat embedded (expects CPL-1). Tests claim-specific CPL
  assignment, mandatory caveat propagation, scope-expansion detection on
  "tamper-proof" language, and complete Phase 9 gate execution for an
  uncontested Production capability.
expected_validated_status: Production
expected_ecs_range: [80, 92]
expected_ecs_band: ["Authoritative", "Corroborated"]
expected_ecs_path: A
expected_allowed_claims_count: [2, 2]
expected_prohibited_claims_count: [1, 3]
expected_contradictions_count: 0
expected_escalation_required: false
expected_hard_disqualifiers_triggered: []
expected_phase_9_gate_completed: true
expected_score_range: [93, 97]
claim_context: Formal Proposal
requesting_team: Advisory
industry: Retail Banking
jurisdiction: UK
---

# Test Fixture: Production Capability — Immutable Audit Log

## Context

**Client:** UK retail bank (mid-tier, ~£3bn AUM, FCA regulated)  
**Proposal type:** Formal Proposal — AI governance programme implementation  
**Requesting team:** Advisory  
**Claim context:** Formal Proposal (customer requires evidence of tamper-proof audit capability for FCA model risk guidance compliance)  
**Trigger for validation:** Advisory team preparing Section 3 (Ethana Platform Coverage) of a formal governance proposal; two alternative claim formulations submitted for pre-proposal validation

**Customer concern:** The FCA model risk guidance requires immutable records of model decisions. The customer's procurement lead has specifically asked whether Ethana's audit log is "truly immutable at the storage layer."

---

## Claims Submitted for Validation

**Claim A** (caveat not embedded):
> "Ethana's Immutable Audit Log captures every gateway-routed AI call in a tamper-proof, insert-only event store with native SIEM export to Splunk, Elastic, and Datadog."

**Claim B** (caveat embedded):
> "Ethana's Immutable Audit Log captures every gateway-routed AI call in a tamper-proof, insert-only event store with native SIEM export to Splunk, Elastic, and Datadog. Immutability is enforced at the application layer — database-layer WORM enforcement has not been independently confirmed; verify with Ethana engineering before representing hardware-level immutability to a regulatory examiner."

The advisory team wants to use Claim A in the main proposal body (shorter, cleaner) and Claim B in the technical annex. They want to know which claim can be used in which context.

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **Claim-specific CPL assignment:** Both claims describe the same capability with the same ECS. They must receive different CPLs because Claim B embeds the mandatory caveat and Claim A does not. The correct output assigns CPL-1 to Claim B (caveat embedded — unrestricted) and CPL-2 to Claim A (caveat absent — requires caveat to be added inline before formal use). An output that assigns both the same CPL has failed the claim-specific CPL model.

2. **Scope-expansion detection on "tamper-proof":** The phrase "tamper-proof" does not appear verbatim in the canonical model entry, which describes an "insert-only event store." The evaluator must run DT4 Check 2 (Depth) on this phrase. The correct adjudication: "tamper-proof" combined with "insert-only" and the application-layer caveat falls within the confirmed scope of the Immutable Audit Log. Without the caveat, "tamper-proof" implies database-layer or hardware-level enforcement that the canonical model does not confirm — this is why Claim A receives CPL-2 (the caveat must be added before formal use) rather than CPL-5 (it is not prohibited, just conditional).

3. **Mandatory caveat propagation:** The application-layer caveat must appear in Section 1 (Status Determination) and must be referenced in the Section 4 entry for Claim A (as required caveat) and embedded in the Section 4 entry for Claim B. An output where the caveat appears in Section 1 but is absent from Section 4 fails Dimension 1 (caveats are load-bearing parts of the claim).

4. **Customer query response — storage-layer immutability:** The customer specifically asked about "storage-layer" immutability. The correct handling is: this is precisely the application-layer caveat issue. The evaluator must flag in Section 5 (Prohibited Claims) any claim that asserts hardware-level WORM or database-layer immutability. The Prohibited Claims section should address this specific customer query.

5. **Section 6 handling:** The marketing playbook (if consulted) may present the Immutable Audit Log without the mandatory caveat. This is a caveat omission, not a direct status contradiction. Section 6 must document this assessment and conclude that the omission does not trigger a −10 ECS adjustment (the adjustment applies to direct contradictions, not omissions). An output that applies −10 for a caveat omission misapplies the ECS formula.

6. **Phase 9 gate:** All 7 steps must be confirmed in Section 9. HQ6 is the most common failure on a "clean" Production validation — evaluators skip the gate because "there were no issues." The gate is mandatory regardless.

---

## Expected Section Highlights

**Section 1:**
- Status: Production (verbatim canonical entry required)
- Mandatory caveats: application-layer only; no DB-layer WORM confirmation
- Scope: gateway-routed calls only; three named SIEM targets; configurable retention

**Section 4 (Allowed Claims):**
- Entry 1: Claim B → CPL-1 (caveat embedded); permitted in all contexts including Marketing
- Entry 2: Claim A → CPL-2 (caveat not embedded); permitted in Formal Proposal, RFP, Discovery, Internal, Engineering; not permitted in Marketing without caveat inline; required caveat quoted verbatim

**Section 5 (Prohibited Claims):**
- At minimum: "hardware-level WORM storage" or "immutable at the storage layer" → CPL-5; risk: regulatory misrepresentation in FCA context

**Section 6:** "Zero direct contradictions. Marketing playbook omits mandatory caveat — documented as caveat omission, not contradiction. ECS penalty not applied."

**Section 7:**
- Path A
- Base: +50 (Production confirmed)
- Richness: +15 to +20 (canonical entry specifies insert-only path, three SIEM targets, retention, application-layer caveat)
- Corroboration: +15 (product-architecture-investigation.md confirms architecture)
- Playbook caveat omission: ±0 (omission, not contradiction — see Section 6)
- ECS: 80–85 → Authoritative or Corroborated

**Section 8:** No escalation required. Non-blocking recommendation to update marketing playbook.

---

## Reviewer Red Flags

- Claim A and Claim B assigned the same CPL → claim-specific CPL model not applied
- "Tamper-proof" in Claim A/B flagged as CPL-5 scope expansion → incorrect; the phrase is permitted with the caveat present (Claim B) or required inline (Claim A)
- Mandatory caveat present in Section 1 but absent from Section 4 entries → caveats are load-bearing parts of the claim, not optional footnotes
- Marketing playbook caveat omission scored as −10 ECS contradiction → misapplication of ECS penalty rule; omissions ≠ contradictions
- Phase 9 gate absent from Section 9 → HQ6; most common failure on clean Production validations
- Any claim about "storage-layer WORM" or "database-layer immutability" in Section 4 → scope expansion; must be in Section 5
