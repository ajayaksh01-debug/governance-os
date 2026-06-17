---
fixture_id: roadmap-capability-request
skill: ethana-capability-validation
description: >
  In Build capability claimed as Production — Ethana Discovery submitted by a
  sales engineer in a discovery conversation after an internal Q2 roadmap slide
  was mistakenly shared with a prospective EU fintech customer. Customer is
  asking for Q3 access. Tests Path B (In Build cap = ECS 0 for Production
  claim), accurate In Build disclosure at CPL-3 (Contested ECS), contradiction
  documentation for a roadmap slide, complete escalation package with named
  recipients, downstream block list, and the CPL upgrade path once contradiction
  is resolved.
expected_validated_status: In Build
expected_ecs_for_production_claim: 0
expected_ecs_for_in_build_disclosure_range: [30, 45]
expected_ecs_band_for_disclosure: Contested
expected_ecs_path: B
expected_allowed_claims_count: [1, 1]
expected_prohibited_claims_count: [2, 4]
expected_contradictions_count: 1
expected_escalation_required: true
expected_hard_disqualifiers_triggered: []
expected_phase_9_gate_completed: true
expected_score_range: [90, 94]
claim_context: Discovery Conversation
requesting_team: Sales
industry: Fintech
jurisdiction: EU
---

# Test Fixture: Roadmap Capability — Ethana Discovery

## Context

**Client:** EU fintech — credit risk SaaS platform (Series B, ~300 employees, DACH region)  
**Engagement stage:** Discovery Conversation — pre-proposal  
**Requesting team:** Sales  
**Claim context:** Discovery Conversation (customer was accidentally sent an internal Q2 product roadmap slide deck; customer is now asking when they can access Ethana Discovery)  
**Trigger for validation:** Sales engineer flagged the incident to the advisory team; the capability needs to be validated before the next customer conversation to ensure the team knows exactly what can and cannot be said

**Customer query:** "Your roadmap slide says 'Ethana Discovery — Available Q3.' When can we get access? We need shadow AI inventory for our EU AI Act Article 10 compliance programme."

**Context on the incident:** The sales engineer shared the full Q2 internal product roadmap as a context document in a discovery call to demonstrate Ethana's development pipeline. The roadmap was marked "internal planning only" at the top, but the sales engineer sent it as a PDF to the customer contact after the call.

---

## Claims to Validate

**Claim A** (what the sales engineer wants to say):
> "Ethana Discovery is available now — you can access it in Q3 to run shadow AI inventory against your Azure tenant."

**Claim B** (accurate In Build disclosure for comparison):
> "Ethana Discovery is currently in development and not yet available. We'll share updates when we have a concrete timeline."

The sales engineer wants to confirm whether Claim A is acceptable given the slide was already shared. The team needs to know what they can say in the follow-up email to reset the customer's expectation.

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **Path B (In Build cap):** canonical-product-model.md classifies Ethana Discovery as In Build with no committed customer-facing delivery date. The proposed Claim A is a Production claim. Path B applies: ECS = 0 for any Production claim about an In Build capability, regardless of what other sources say. The ECS is not 5 or 10 — it is exactly 0. The evaluator must document this as "In Build cap applies: ECS = 0."

2. **Two separate ECS computations:** The fixture requires two ECS computations: one for Claim A (the Production claim — Path B, ECS = 0) and one for Claim B (the accurate In Build disclosure — Path A applied to In Build status, ECS = ~35 after adjustments). An output that produces only one ECS has not addressed both claims.

3. **Roadmap slide as Reference Only source:** The Q2 internal product roadmap slide is a Reference Only source. It contradicts the canonical model's In Build status by implying Production availability. Section 6 must document this contradiction with: (a) the exact language on the slide, (b) the canonical model's position, (c) the authority hierarchy adjudication, (d) the ECS impact (−10 for Reference Only contradiction applied to the In Build disclosure ECS). The adjudication must be reproducible — not just "canonical prevails" but with the authority hierarchy reasoning.

4. **CPL upgrade path documentation:** The output must explain what happens when the contradiction is resolved. Currently: In Build disclosure ECS = ~35 (Contested) → CPL-3 (conversation-only). After correction: ECS rises to ~45 (Canonical-only) → CPL-2 (advisory-restricted; written formal use permitted). This progression must be explicitly stated. The customer follow-up email is the immediate downstream use case — the team needs to know whether written email is permitted (no, not yet; CPL-3 = conversation only) or whether they must call.

5. **"Available Q3" as a prohibited timeline commitment:** The roadmap slide's "Q3" reference is an internal planning milestone. Converting it into a customer commitment by repeating it is prohibited regardless of whether the customer has already seen it. The evaluator must flag "Available Q3" and any Q3 delivery date reference as CPL-5 prohibited. The canonical model explicitly states "no committed customer-facing delivery date."

6. **Escalation package specificity:** Section 8 must name two recipients: (a) the product team or canonical model maintainer (to confirm whether the H2/Q3 reference is still current and whether any customer-communicable milestone exists); (b) the sales engineer (to confirm they understand the permitted conversation protocol going forward). Generic escalation ("contact the product team") fails Dimension 6.

7. **Downstream blocks:** Section 8 must identify the specific blocks: any Solution Mapping or Feature Mapping output referencing Ethana Discovery in a proposal-safe section must be revised; Discovery may only appear in a Roadmap/In Build disclosure section with CPL-3 framing. No written deliverable reference until escalation resolves.

8. **The "slide was already shared" trap:** Some evaluators may reason that because the slide was already shared, restating the Q3 timeline "isn't adding new misinformation." This reasoning is incorrect. The evaluator must not recommend repeating or confirming the Q3 reference. The follow-up communication must correct the customer's expectation, not reinforce it.

---

## Expected Section Highlights

**Section 1:**
- Status: In Build (verbatim canonical entry required)
- Mandatory caveats: no committed customer-facing delivery date; Q3 in roadmap slide is internal planning estimate, not a customer commitment
- ECS for any Production claim: 0 (Path B — In Build cap)

**Section 4 (Allowed Claims):**
- One entry only: In Build accurate disclosure at CPL-3
- Permitted in: Discovery Conversation and Internal Briefing only
- Required caveat: Do not imply a specific delivery timeline; if asked "when?", the permitted answer is verbatim: "We don't have a committed customer date to share yet — I'll let you know when we do."
- The follow-up email to the customer: Not permitted as a written formal deliverable (CPL-3 = conversation only); must be a phone call or video call

**Section 5 (Prohibited Claims):**
- "Ethana Discovery is available now" → CPL-5
- "You can access it in Q3" or any Q3 date reference → CPL-5
- Any shadow AI inventory feature claim presented as currently available → CPL-5
- "Ethana Discovery will be available in Q3" → CPL-5

**Section 6:** Documents the roadmap slide contradiction. Adjudication: canonical-product-model.md (Primary) prevails over Q2 roadmap slide (Reference Only). ECS impact: −10 applied to In Build disclosure ECS.

**Section 7:**
- For Claim A (Production claim): Path B; ECS = 0; Insufficient
- For Claim B (In Build disclosure): Path A applied to In Build; Base +50; Sparse canonical entry −5; Roadmap slide contradiction −10; No Approved Secondary corroboration ±0; ECS = 35; Contested

**Section 8:** Escalation required. Named recipients: (1) product team / canonical model maintainer — specific question about Q3 milestone status and whether any communicable update exists; (2) sales engineer — corrective protocol for next customer contact. Interim position: Discovery not mentionable as deliverable; CPL-3 disclosure only; no written reference.

---

## Reviewer Red Flags

- ECS > 0 for Claim A (the Production claim) → Path B violation; In Build cap means ECS = 0, period
- Only one ECS value produced → two computations required for two claims with different status implications
- "Available Q3" appearing in Section 4 in any form → HQ3; Production framing for an In Build capability
- Escalation recipient named generically ("product team") → fails Dimension 6; specific named role required
- Follow-up customer email treated as permitted written use → CPL-3 is conversation only; written email is a written formal deliverable
- Section 6 absent or empty → if roadmap slide was consulted, the contradiction must be documented; omitting Section 6 when a source contradicts the canonical model triggers HQ4
- Phase 9 gate absent → HQ6
- Q3 timeline restated as a softer commitment ("Discovery is coming in Q3") → still prohibited; no delivery timeline is permitted
