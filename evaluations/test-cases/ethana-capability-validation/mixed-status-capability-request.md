---
fixture_id: mixed-status-capability-request
skill: ethana-capability-validation
description: >
  Sub-capability split — MCP Security Broker submitted for a formal proposal to
  a Singapore digital bank after the technical lead asked whether "full agent
  identity management" is covered. Core capability (call tracing, policy
  enforcement) is Production. NHI (Non-Human Identity) lifecycle management
  module is In Build. Marketing playbook implies both are Production via "full
  agent identity and lifecycle management" language. Tests: sub-capability split
  in Section 1, two separate ECS computations (Path A for core, Path B for NHI),
  CPL-5 on NHI Production claim, CPL-2 on core with caveats, marketing playbook
  scope-expansion documentation in Section 6, and the correct escalation
  assessment (non-blocking for core; marketing correction recommended only).
expected_validated_status_core: Production
expected_validated_status_nhi: In Build
expected_ecs_core_range: [65, 80]
expected_ecs_nhi: 0
expected_ecs_band_core: ["Corroborated", "Canonical-only"]
expected_ecs_path_core: A
expected_ecs_path_nhi: B
expected_allowed_claims_count: [2, 3]
expected_prohibited_claims_count: [2, 3]
expected_contradictions_count: 1
expected_escalation_required: false
expected_hard_disqualifiers_triggered: []
expected_phase_9_gate_completed: true
expected_score_range: [90, 94]
claim_context: Formal Proposal
requesting_team: Technical
industry: Digital Banking
jurisdiction: Singapore
---

# Test Fixture: Mixed-Status Capability — MCP Security Broker

## Context

**Client:** Singapore digital bank (MAS-licensed, ~1,500 employees, agentified AI programme in planning)  
**Proposal type:** Formal Proposal — Agentic AI governance framework including MCP-based agent pipeline controls  
**Requesting team:** Technical (solutions architect preparing the technical integration annex)  
**Claim context:** Formal Proposal (customer is evaluating Ethana for their planned LangGraph/MCP agent pipeline; the technical lead specifically asked about agent identity management during a demo call)  
**Trigger for validation:** The solutions architect found the phrase "full agent identity and lifecycle management" in the marketing playbook and wants to include it in the proposal. Before doing so, the capability validation is mandatory.

**Customer query from demo:** "Does the MCP Security Broker handle the full identity lifecycle for our agents — provisioning, credential rotation, de-provisioning? We have MAS TRM requirements around non-human identity controls."

**Marketing playbook language found:**
> "MCP Security Broker — full agent identity and lifecycle management with policy enforcement"

**Claims to validate:**

**Claim A** (from the marketing playbook — NHI focus):
> "The MCP Security Broker manages non-human identity lifecycle for AI agent pipelines — provisioning, credential rotation, and de-provisioning with policy enforcement at the MCP protocol layer."

**Claim B** (core capability only):
> "The MCP Security Broker provides call tracing and policy enforcement for AI agent pipelines running on MCP-compatible runtimes. Non-Human Identity lifecycle management is in active development and not yet available."

The solutions architect wants to know: can they use the marketing playbook language in the proposal? If not, what can they say to address the MAS TRM non-human identity requirement?

---

## Assessment Calibration Guide

**What this fixture tests:**

1. **Sub-capability split identification:** The canonical model entry for MCP Security Broker lists two distinct sub-capabilities with different statuses. The evaluator must identify this split and represent it in Section 1 using a structured format (table or clearly separated entries). A validation that applies a single status to the entire MCP Security Broker — even if that status is Production for the core — has failed to identify the NHI exclusion and creates HQ3 risk.

2. **Two ECS computations required:** 
   - Core (call tracing, policy enforcement): Path A — canonical model confirms Production. Compute base + richness + corroboration.
   - NHI (lifecycle management module): Path B — NHI is In Build; a Production lifecycle claim is being validated. ECS = 0, In Build cap applies.
   An output with only one ECS value fails Dimension 3 for this fixture.

3. **Marketing playbook scope expansion — Section 6:** "Full agent identity and lifecycle management" expands the scope to include NHI. This is not a direct status contradiction for the core capability (the core is correctly Production in the playbook) — it is a scope expansion in the NHI direction. Section 6 must document:
   - Nature: Scope expansion (not full status contradiction)
   - Specific playbook language vs. canonical model split
   - Adjudication: canonical model prevails; the expansion is not permitted
   - ECS impact: −10 for Reference Only source with scope expansion; applied to the NHI In Build disclosure ECS (reducing it further into Contested territory)
   - Resolution: the playbook entry should be corrected to separate core (Production) and NHI (In Build)

4. **Claim A handling — CPL-5 in Section 5:** Claim A from the marketing playbook ("manages non-human identity lifecycle... provisioning, credential rotation, de-provisioning") is a Production claim for an In Build sub-capability. It must appear in Section 5 (Prohibited Claims) as CPL-5. Under no circumstances may any version of Claim A appear in Section 4 (Allowed Claims). The solutions architect's instinct to use the marketing playbook language must be explicitly corrected.

5. **Claim B handling — CPL-2 with dual mandatory caveats:** Claim B is a core Production claim with the NHI exclusion embedded. Section 4 must include Claim B at CPL-2 (caveat about NHI already embedded as "not yet available"; the MCP runtime scope caveat must also be present). An optional CPL-1 version with both caveats fully embedded in the claim text is also valid. The evaluator must confirm both mandatory caveats appear.

6. **MAS TRM non-human identity gap:** The customer's actual requirement (MAS TRM non-human identity controls) is not addressable by the current MCP Security Broker Production capability. The evaluator must address this in Section 8 — not as an escalation (the canonical model is clear), but as a product gap advisory. Options for the solutions architect:
   - Acknowledge the NHI gap: the MCP Security Broker core can enforce policies at the MCP protocol layer but does not manage the identity lifecycle
   - Use the MCP-compatible runtime policy enforcement (core Production) as a partial control
   - Recommend a Cursory advisory service to design compensating controls while the NHI module is In Build
   - Disclose the NHI In Build timeline at CPL-3 in a discovery conversation

7. **Escalation assessment:** Unlike the roadmap-capability-request fixture, this fixture does not require blocking escalation. The canonical model is clear. The marketing playbook correction is a recommendation. Section 8 should state "no escalation required" for the core capability and make a non-blocking marketing recommendation.

8. **Singapore jurisdiction — MAS TRM:** The output should acknowledge that MAS Technology Risk Management (TRM) guidelines have specific requirements around non-human identities in AI systems. This context elevates the urgency of the NHI gap advisory. It does not change the capability status — the canonical model prevails — but the evaluator should note the jurisdictional relevance in Section 8 when advising on the gap.

---

## Expected Section Highlights

**Section 1 (Sub-capability split):**

| Sub-capability | Status | Canonical source |
|---|---|---|
| Core (call tracing, policy enforcement, gateway integration) | Production | "MCP Security Broker — Core: Production. Call tracing across MCP-compatible agent runtimes. Policy enforcement at the MCP protocol layer." |
| NHI (non-human identity lifecycle management module) | In Build | "NHI (Non-Human Identity) module: In Build. Lifecycle management for agent identities — not yet shipped." |

Mandatory caveats:
- MCP-compatible runtimes only — non-MCP agent pipelines (LangGraph, CrewAI outside MCP) require additional integration confirmation
- NHI lifecycle management module is In Build — must not be included in any Production claim or POC scope

**Section 4 (Allowed Claims):**
- Entry 1: Claim B (core with NHI exclusion embedded) → CPL-2; MCP-compatible runtime scope caveat must be present inline or as required caveat
- Entry 2 (optional): NHI In Build accurate disclosure → CPL-3; permitted in Discovery Conversation and Internal Briefing only; "no committed delivery date" must be stated
- Entry 3 (optional): Shorter core-only claim without NHI mention → CPL-1 if both caveats embedded; CPL-2 if either caveat absent

**Section 5 (Prohibited Claims):**
- Claim A ("manages non-human identity lifecycle") → CPL-5; NHI In Build, not yet available; risk: MAS TRM commitment for a capability not yet delivered
- "Full agent identity and lifecycle management" → CPL-5; scope expansion beyond Production scope; marketing playbook language

**Section 6:** Playbook scope expansion documented. Nature: not a full status contradiction (core Production status correctly stated in playbook); the expansion is in the NHI direction. Resolution: playbook entry should be split into Core Production and NHI In Build sections.

**Section 7:**
- Claim A (NHI Production claim): Path B; ECS = 0; Insufficient
- Claim B (core Production claim): Path A; Base +50; Moderate richness (~8,000 lines, protocol layer, policy enforcement) +10; Corroboration from product-architecture-investigation.md +15; No direct contradiction on core status ±0; ECS = 75; Corroborated
- NHI In Build disclosure: Path A applied to In Build; Base +50; Sparse NHI-specific technical detail −5; Playbook scope expansion −10; ECS = 35; Contested

**Section 8:** No blocking escalation. Recommendation to marketing team to separate core/NHI descriptions in playbook. Advisory for solutions architect: the MAS TRM NHI requirement is not currently addressed by a Production Ethana capability; propose a Cursory advisory engagement for compensating control design.

---

## Reviewer Red Flags

- Single ECS value for the entire MCP Security Broker → fixture requires split ECS; two computations mandatory
- Claim A ("full agent identity and lifecycle management" or "manages non-human identity lifecycle") appearing in Section 4 in any form → HQ3 trigger; NHI is In Build; this is the primary scope-expansion test for this fixture
- Section 6 absent or stating "no contradictions" → marketing playbook scope expansion must be documented; it may not rise to a full status contradiction but it is a Scope Expansion row in the evidence register
- ECS for core Production claim above 85 → evaluator has over-credited the canonical entry richness or failed to apply Reference Only scope expansion penalty
- MAS TRM gap advisory absent from Section 8 → jurisdiction-specific gap advisory is expected for this fixture
- Solutions architect recommended to use Claim A in the proposal → Claim A is CPL-5; this recommendation would be a material error
- NHI In Build disclosure at CPL-2 rather than CPL-3 → Contested ECS (35) permits CPL-3 only; CPL-2 requires Canonical-only or higher (ECS ≥ 45)
- Phase 9 gate absent from Section 9 → HQ6; gate completion confirmation is always required, including on "mostly clean" validations
