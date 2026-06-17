# Ethana Capability Validation — Regression Baseline

## Purpose

This document defines the expected output characteristics for each `ethana-capability-validation` test fixture. It is used by `regression_tester.py` to detect structural drift, scoring range violations, Claims Firewall failures, and Phase 9 gate omissions across validation runs.

**Authoritative fixtures:** `evaluations/test-cases/ethana-capability-validation/`  
**Skill version:** 1.0  
**Pass threshold:** 90/100 — stricter than all other skills; this is the foundational truth gate for all commercial outputs  
**Baseline established:** 2026-06-17  
**Governance Team review required to update:** Yes

---

## Fixture 1 — production-capability-request

**Description:** Clean Production capability validation — Immutable Audit Log for a formal proposal context. Two claims submitted: one with mandatory caveat embedded (CPL-1) and one without (CPL-2). Tests claim-specific CPL assignment, mandatory caveat handling, and Phase 9 gate completion for an uncontested Production capability.

### Expected Output Characteristics

| Metric | Expected value | Notes |
|---|---|---|
| validated_status | Production | Must match canonical-product-model.md verbatim |
| ecs | 80–90 | Base 50 + richness + corroboration; no contradictions |
| ecs_band | Authoritative or Corroborated | 85+ = Authoritative; 70-84 = Corroborated |
| ecs_path | A | Canonical model confirms Production |
| allowed_claims count | 2 | Claim with caveat (CPL-1) + same claim without caveat (CPL-2) |
| prohibited_claims count | 1–2 | At minimum: hardware-level WORM scope expansion |
| contradictions_count | 0 | No source directly contradicts Production status |
| escalation_required | false | ECS well above 45; no unresolved contradictions |
| hard_disqualifiers_triggered | [] | Zero hard disqualifiers on a clean Production validation |
| phase_9_gate_completed | true | All 7 steps must be confirmed |

### CPL Assignment Invariants

The two allowed claims for this fixture must demonstrate claim-specific CPL:
- **Claim with embedded caveat** (application-layer caveat text in claim body): `CPL-1` — Unrestricted; permitted in all contexts including Marketing
- **Claim without embedded caveat** (caveat absent from claim body): `CPL-2` — Advisory-restricted; requires caveat to be added inline before formal use

These two claims have the same ECS (same capability, same canonical source) but different CPLs because CPL is assigned per claim, not per capability. A reviewer who assigns both the same CPL has miscalibrated the claim-specific CPL model.

### Mandatory Canonical Caveats

The following caveats must appear in Section 1 (Status Determination) and in or alongside every CPL-1 or CPL-2 allowed claim:
- Application-layer immutability only — database-layer WORM enforcement not confirmed
- Coverage limited to gateway-routed calls — direct database access paths are not captured

### Source Requirements

```json
{
  "required_sources": [
    {
      "source_name": "canonical-product-model.md",
      "authority_level": "Primary",
      "position": "first"
    }
  ],
  "prohibited_authority_levels": {
    "capability-status.md": "Primary or Secondary",
    "source-of-truth.md": "Primary or Secondary",
    "ethana-status-reconciliation.md": "Primary or Secondary"
  }
}
```

### Structural Requirements

```json
{
  "required_sections": [
    "Section 1 — Capability Status Determination",
    "Section 2 — Evidence Sufficiency Summary",
    "Section 3 — Evidence Register",
    "Section 4 — Allowed Claims",
    "Section 5 — Prohibited Claims",
    "Section 6 — Contradiction Log",
    "Section 7 — Evidence Confidence Score",
    "Section 8 — Escalation Recommendation",
    "Section 9 — Validation Audit Trail"
  ],
  "section_6_must_state_zero_contradictions": true,
  "section_8_must_state_no_escalation_required": true,
  "section_9_must_confirm_gate_completed": true
}
```

### Disqualifier Verification

For this fixture the following HQ checks must all show "not triggered":
- HQ1: Section 1 status must be Production — matching canonical model
- HQ2: Not applicable (Aspirational not involved)
- HQ3: No scope expansion in Section 4 — hardware-level WORM or database-layer immutability must not appear in any Allowed Claim
- HQ4: Not triggered — if a caveat omission is noted in Section 6, it must be documented but does not constitute a contradiction requiring a Section 6 entry with adjudication; only direct status or property contradictions require Section 6 entries
- HQ5: canonical-product-model.md must appear in Section 3
- HQ6: Phase 9 gate completed — all 7 steps confirmed
- HQ7: No CPL-5 entry in Section 4

---

## Fixture 2 — roadmap-capability-request

**Description:** In Build capability being claimed as Production — Ethana Discovery in a sales discovery context where an internal roadmap slide was mistakenly shared with a customer. The customer is asking when they can access it. Tests Path B (In Build cap), ECS = 0 for Production claim, ECS computation for accurate In Build disclosure, contradiction documentation for a roadmap slide, and the escalation package.

### Expected Output Characteristics

| Metric | Expected value | Notes |
|---|---|---|
| validated_status | In Build | Must match canonical-product-model.md |
| ecs (for Production claim) | 0 | Path B — In Build cap; ECS = 0 regardless of other adjustments |
| ecs (for In Build disclosure) | 30–45 | Depends on whether product-architecture-investigation.md has an entry; if Silent: 50 - sparse_penalty - contradiction_adjustment; roadmap slide contradiction = -10 |
| ecs_band (for In Build disclosure) | Contested | 20-44 range |
| ecs_path | B | Canonical model shows In Build; Production claim being validated |
| allowed_claims count | 1 | In Build accurate disclosure at CPL-3 only |
| prohibited_claims count | 2–4 | At minimum: "available now" claim, Q3 delivery date claim |
| contradictions_count | 1 | Roadmap slide contradicts canonical In Build status |
| escalation_required | true | ECS = 0 for Production claim; active customer expectation mismatch |
| hard_disqualifiers_triggered | [] | All HQs must show "not triggered" — this is correct handling of a roadmap trap |
| phase_9_gate_completed | true | All 7 steps must be confirmed |

### CPL Assignment Invariants

- The proposed Production claim ("available now" / "Q3 access") must appear in Section 5 (Prohibited Claims) as CPL-5 — never in Section 4
- The accurate In Build disclosure must appear in Section 4 at CPL-3 only (Contested ECS restricts to conversation contexts)
- No written formal deliverable reference to Ethana Discovery is permitted until the contradiction is resolved

### ECS Progression Logic

The baseline requires that the output correctly document what happens to ECS if the contradiction is resolved:
- Current ECS for In Build disclosure: 30–45 (Contested)
- ECS after contradiction resolution: ~45 (Canonical-only) — the −10 adjustment is removed
- CPL improvement: CPL-3 → CPL-2 (written formal use becomes available)

This progression must be stated in Section 7 or Section 8. An output that does not explain the CPL upgrade path scores no higher than 7/15 on Dimension 3.

### Structural Requirements

```json
{
  "required_sections": [
    "Section 1 — Capability Status Determination",
    "Section 2 — Evidence Sufficiency Summary",
    "Section 3 — Evidence Register",
    "Section 4 — Allowed Claims",
    "Section 5 — Prohibited Claims",
    "Section 6 — Contradiction Log",
    "Section 7 — Evidence Confidence Score",
    "Section 8 — Escalation Recommendation",
    "Section 9 — Validation Audit Trail"
  ],
  "section_4_must_contain_in_build_disclosure": true,
  "section_5_must_contain_production_claim_as_cpl5": true,
  "section_6_must_have_exactly_one_entry": true,
  "section_8_must_name_specific_escalation_recipient": true,
  "section_8_must_state_interim_position": true,
  "section_8_must_list_downstream_blocks": true,
  "section_9_must_confirm_gate_completed": true
}
```

### Disqualifier Verification

- HQ1: Not triggered — Section 1 correctly says In Build, not Production
- HQ2: Not applicable — Aspirational not involved
- HQ3: Not triggered — Production claim correctly in Section 5; In Build disclosure in Section 4 makes no scope expansion
- HQ4: **Must not be triggered** — the roadmap slide contradiction must be documented in Section 6 with full adjudication
- HQ5: canonical-product-model.md must appear in Section 3
- HQ6: Phase 9 gate completed — all 7 steps confirmed
- HQ7: Not triggered — no CPL-5 in Section 4

### Escalation Package Requirements

Section 8 must include:
1. Named recipient: product team or canonical model maintainer (not "ask engineering" — specific)
2. Named secondary recipient: the sales engineer who shared the roadmap slide
3. Specific question: references the exact slide content, the canonical model entry, and asks whether Q3 remains an internal estimate only
4. Interim position: Discovery must not be mentioned as a deliverable; the permitted CPL-3 disclosure language must be quoted
5. Downstream blocks: must name the specific output types blocked (any Solution Mapping or Feature Mapping output referencing Discovery in a proposal-safe section)

---

## Fixture 3 — mixed-status-capability-request

**Description:** Sub-capability split — MCP Security Broker where the core capability is Production and the NHI (Non-Human Identity) lifecycle management module is In Build. Tests the split validation path, separate ECS computations for two sub-capabilities, correct CPL assignment for each, marketing playbook scope expansion handling, and mandatory caveat embedding.

### Expected Output Characteristics

| Metric | Expected value | Notes |
|---|---|---|
| validated_status | Production (core) / In Build (NHI module) | Section 1 must show split by sub-capability |
| ecs (core Production claim) | 65–80 | Base 50 + richness (moderate) + corroboration; marketing playbook scope expansion noted |
| ecs (NHI Production claim) | 0 | Path B — NHI In Build cap |
| ecs_band (core) | Corroborated or Canonical-only | 70+ = Corroborated |
| ecs_path | A for core; B for NHI | Two separate ECS computations required |
| allowed_claims count | 2–3 | Core CPL-2 claim + NHI In Build disclosure CPL-3; optionally a core CPL-1 if mandatory caveats embedded |
| prohibited_claims count | 2–3 | NHI Production claim + "full agent identity" marketing language |
| contradictions_count | 1 | Marketing playbook implies NHI is Production; canonical model says In Build |
| escalation_required | false | Core claim is sufficient for the proposal; marketing playbook update is a recommendation, not a blocking escalation |
| hard_disqualifiers_triggered | [] | Correct handling — NHI claim in Section 5 prevents HQ3 trigger |
| phase_9_gate_completed | true | All 7 steps confirmed |

### Sub-Capability Split Requirements

Section 1 must use a table or clearly structured format showing both sub-capabilities:
- Row 1: Core (call tracing, policy enforcement, gateway integration) → Production
- Row 2: NHI (non-human identity lifecycle management module) → In Build

A validation that treats the entire MCP Security Broker as Production fails HQ1 and triggers an automatic disqualifier.

### Mandatory Caveats

The following caveats must appear in Section 1 and in or alongside every core Production allowed claim:
- MCP-compatible runtimes only — non-MCP agent pipelines not covered without additional integration confirmation
- NHI lifecycle management module is In Build — must not be included in any Production claim or POC scope

### Marketing Playbook Contradiction

The marketing playbook ("full agent identity and lifecycle management") expands the scope of what is Production to include NHI. This must be documented in Section 6 with:
- Nature: Scope expansion (not direct status contradiction for core)
- Adjudication: canonical model prevails; NHI is In Build
- ECS impact: −10 for Reference Only source with scope expansion (applied to NHI In Build disclosure ECS)
- Resolution: Core Production claims permitted; NHI Production claims prohibited; marketing playbook should be corrected

### Structural Requirements

```json
{
  "required_sections": [
    "Section 1 — Capability Status Determination",
    "Section 2 — Evidence Sufficiency Summary",
    "Section 3 — Evidence Register",
    "Section 4 — Allowed Claims",
    "Section 5 — Prohibited Claims",
    "Section 6 — Contradiction Log",
    "Section 7 — Evidence Confidence Score",
    "Section 8 — Escalation Recommendation",
    "Section 9 — Validation Audit Trail"
  ],
  "section_1_must_show_sub_capability_split": true,
  "section_2_must_show_two_ecs_values": true,
  "section_5_must_contain_nhi_production_claim_as_cpl5": true,
  "section_6_must_document_playbook_expansion": true,
  "section_7_must_show_two_separate_ecs_computations": true,
  "section_9_must_confirm_gate_completed": true
}
```

### Disqualifier Verification

- HQ1: Not triggered — Section 1 correctly splits core (Production) and NHI (In Build); the entire capability is NOT claimed as Production
- HQ2: Not triggered — Aspirational not involved
- HQ3: **Must not be triggered** — NHI claim must be in Section 5 (Prohibited), not Section 4 (Allowed). The marketing playbook's "full agent identity and lifecycle management" language must not appear in Section 4 in any form.
- HQ4: Not triggered — marketing playbook scope expansion documented in Section 6
- HQ5: canonical-product-model.md must appear in Section 3
- HQ6: Phase 9 gate completed — all 7 steps confirmed
- HQ7: Not triggered — no CPL-5 in Section 4

---

## Cross-Fixture Invariants

These rules apply across all three fixtures and will be flagged as regression failures if violated:

### ECS Arithmetic Visibility

For every fixture, the output must show explicit ECS arithmetic:
```
Path selected: [A/B/C/D/E/F]
Base:          +XX
[Adjustment 1: description]: ±XX
[Adjustment 2: description]: ±XX
ECS:           XX → [Band]
```
An ECS that appears without derivation arithmetic fails Dimension 3. An ECS that shows arithmetic but uses the wrong path fails Dimension 3.

### CPL-5 Never in Section 4

No output may contain a claim tagged CPL-5 in Section 4 (Allowed Claims). CPL-5 belongs exclusively in Section 5 (Prohibited Claims). Any CPL-5 claim in Section 4 triggers Hard Disqualifier HQ7 and automatic disqualification.

### Aspirational Claims Never in Section 4

No Aspirational capability may appear in Section 4 in any form — not as a roadmap mention, not as "coming soon," not with a caveat. Aspirational capabilities produce an empty Section 4. Any Aspirational claim in Section 4 triggers Hard Disqualifier HQ2.

### Phase 9 Gate Always Present

Section 9 must confirm Phase 9 gate completion with all 7 steps named and confirmed. An absent or incomplete Section 9 triggers Hard Disqualifier HQ6. The gate completion line is not optional even when there are no contradictions — "no contradictions" is documented in Section 6 as a positive statement; it does not permit omission of the gate.

### Mandatory Caveats Must Propagate to Section 4

Mandatory caveats identified in Section 1 must appear in or alongside every Section 4 (Allowed Claims) entry that could give rise to misrepresentation without the caveat. A CPL-2 entry where the caveat is not required (because it is embedded in the claim text) must be CPL-1. A CPL-1 entry where the caveat is not embedded must be downgraded to CPL-2. An output that assigns all claims the same CPL regardless of caveat embedding has failed the claim-specific CPL model.

### Prohibited Sources Never as Primary or Secondary

The following sources must never appear in Section 3 at authority level "Primary" or "Secondary":
- `capability-status.md`
- `source-of-truth.md`
- `ethana-status-reconciliation.md`

If these sources are consulted, they must be listed as "Reference Only" with a note that they are superseded by canonical-product-model.md.

### Canonical Model Always First in Evidence Register

`canonical-product-model.md` must appear as the first entry in Section 3 (Evidence Register) with authority level "Primary." A validation where the canonical model is not the first-listed or first-consulted source fails Hard Disqualifier HQ5.

---

## Calibration Reference

| Fixture | Primary challenge | Expected hard disqualifiers | Expected score range |
|---|---|---|---|
| production-capability-request | Claim-specific CPL (same capability, two CPLs based on caveat embedding) | None | 93–97 — clean Production validation with correct CPL split |
| roadmap-capability-request | Path B (In Build cap); correct routing of Production claim to Section 5; escalation package | None (if handled correctly); HQ3 if Production claim leaks into Section 4 | 90–94 — Accepted; high marks on contradiction handling and escalation specificity |
| mixed-status-capability-request | Sub-capability split; two separate ECS computations; marketing playbook scope expansion in Section 6 | None (if handled correctly); HQ3 if NHI claim leaks into Section 4 | 90–93 — Accepted; marks lost on marketing playbook adjudication completeness if not fully documented |

---

## Baseline Update Protocol

### When to update this baseline

This baseline may only be updated when:
1. The ethana-capability-validation skill (SKILL.md, workflow.md, evaluation.md) is formally revised and version-bumped
2. The canonical-product-model.md is updated, changing the status of a capability referenced in these fixtures
3. New test fixtures are added that require corresponding baseline entries
4. The ECS computation model (paths, adjustments, bands) is revised in evaluation.md

### When NOT to update this baseline

- A live validation run producing an ECS outside the expected range is a calibration error in the live run, not a baseline update trigger
- Commercial pressure to allow a higher CPL for a specific capability does not constitute a baseline update
- A single outlier run is not a baseline update trigger

### Update procedure

1. Submit proposed update to Governance Team with rationale
2. Governance Team reviews and approves with documented basis
3. Update this baseline file with version note and date
4. Update the regression test commands in `evaluations/evaluation-index.md` if fixture metadata changes
