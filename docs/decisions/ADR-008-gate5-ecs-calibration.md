# Architecture Decision Record: ADR-008

## Title
ADR-008: ECS Threshold and CVA Executor Scoring Calibration for Gate 5c

---

## Status
**Accepted**

---

## Context

Gate 5c in the CA orchestrator (`agents/client-assessment-agent/runtime/orchestrator.py:509–522`) evaluates the Evidence Confidence Score (ECS) returned by the CVA executor against a configurable threshold:

```python
ecs = s5_json.get("ecs", inputs.get("mock_skill_5_score", 94))
pass_threshold = int(self.config.get("thresholds", {}).get("skill_5_pass", 90))
if ecs < pass_threshold or escalation_required:
    state_mgr.transition_to("HALTED_GATE_5_SCORE_INSUFFICIENT", ...)
```

The threshold is `90` (`config.yaml:18`). The mock default is `94` (`orchestrator.py:509`). All 205 CA tests use the mock — none invoke the real CVA executor, hiding the mismatch completely.

The CVA executor (`agents/capability_validation_agent/runtime/skill_executor.py`) produces ECS by fixture path:

| Path | Capability | ECS | Band |
|---|---|---|---|
| A | Immutable Audit Log (Production) | **85** | Authoritative |
| A | MCP Security Broker (Production, with contradiction) | **75** | Corroborated |
| B | Ethana Discovery (In Build) | **0** | Insufficient |
| General fallback — any other matched Production | **50–70** | Canonical-only / Corroborated |
| F | Unresolved (no CPM match) | **0** | Insufficient |

Maximum achievable ECS: **85**. Gate 5c threshold: **90**. No real capability path passes Gate 5c. This is Adapter Audit Mismatch M2.

**Critical finding from `skills/ethana-capability-validation/SKILL.md`:**

The SKILL.md (lines 277–278) explicitly documents the ECS increment structure:

> - `product-architecture-investigation.md` corroboration: ECS **+15** when it corroborates
> - `use-cases.md` corroboration: ECS **+10** when it corroborates a Production claim in context

The Immutable Audit Log ECS arithmetic as coded (`skill_executor.py:202`):
`"Base: +50; Detailed Entry: +20; Architecture Corroboration: +15; Total: 85"`

The executor at line 172 already checks whether `use-cases.md` exists and adds the source to `sources_checked`. But the executor **never applies the +10 increment to the ECS integer**. The documented increment is specified in SKILL.md but was not implemented in the executor.

With the missing +10 applied: `50 + 20 + 15 + 10 = 95`. The threshold of 90 is achievable with the increment in place. This is an implementation omission, not a design disagreement between the threshold and the executor.

SKILL.md (lines 49–51) documents the rationale for the 90/100 threshold explicitly:

> *"Pass threshold: 90/100. Why 90/100? An error in Capability Validation propagates downstream into every Solution Mapping and Feature Mapping output referencing that capability. The blast radius is the highest of the three skills. The release standard is correspondingly the strictest."*

This rationale is sound and must be preserved. Any option that lowers the threshold must address it directly.

Additional context from source:
- `AGENT.md:621`: the escalation trigger is `ECS < 45` — a separate, lower threshold. Gate 5c and escalation are intentionally decoupled.
- `SKILL.md:233`: ECS band "Authoritative" is defined as **85–100**. With the +10 increment applied, the Immutable Audit Log reaches 95 — firmly within the Authoritative band and 5 points above the gate.

---

## Constraints

1. The ECS threshold of 90 is documented with explicit rationale in SKILL.md (blast radius justification). Any option that lowers the threshold must address that rationale directly.
2. ECS arithmetic must remain reproducible from the validation report alone (SKILL.md:177): `"The arithmetic must be reproducible from this section alone."` The `ecs_arithmetic` string in the executor output must reflect all increments applied.
3. The gate condition `ecs < threshold OR escalation_required` must remain compound. A high ECS on an escalated capability would be contradictory; the compound condition is not negotiable.
4. In Build capabilities must continue to produce `ecs: 0`. This is the Claims Firewall functioning correctly — not a gate defect — and must not be weakened.
5. The mock default of `94` at `orchestrator.py:509` must be updated to a realistic value after a real gate ceiling is established. A mock that exceeds any achievable real ECS produces false confidence in test results.

---

## Options

### Option A: Implement the missing `use-cases.md` +10 ECS increment in the CVA executor

**Description:** The SKILL.md at line 278 defines that `use-cases.md` corroboration adds +10 to ECS for a Production capability. The CVA executor already checks for the file and logs it in `sources_checked`, but never applies the increment to the ECS integer. Adding the +10 when `usecases_file.exists()` and `matched_cap` is not None raises the Immutable Audit Log path from 85 to 95, making Gate 5c passable.

**Implementation:** In `skill_executor.py`, after the Path A ECS calculation for the Immutable Audit Log path:
```python
if usecases_file.exists() and matched_cap:
    ecs += 10
    ecs_arithmetic += f"; Use-cases.md corroboration: +10; Total: {ecs}"
```
- Immutable Audit Log: 85 → **95** (passes Gate 5c at threshold 90)
- MCP Security Broker: 75 + 10 − 10 (contradiction) = **75** (still below 90)
- General fallback Production: 50–70 + 10 = **60–80** (still below 90)
- Update CVA executor tests asserting `ecs=85` for the Audit Log fixture to `ecs=95`
- Update `orchestrator.py:509` mock default from `94` to `95`

**Tradeoffs:**
- Pro: Implements the SKILL.md specification as written. No threshold change required. ECS arithmetic remains reproducible and traceable.
- Pro: The `use-cases.md` source is already in `sources_checked`. The increment is the only missing piece.
- Pro: Immutable Audit Log reaches 95, passing Gate 5c with 5 points of headroom.
- Pro: Preserves the 90/100 threshold and its documented blast-radius rationale.
- Con: MCP Security Broker remains at 75 (below 90). A CA assessment referencing primarily MCP Broker capabilities still halts at Gate 5c until Phase B.
- Con: General fallback Production paths reach max 80 (below 90). CPM capabilities not covered by the named fixture paths still halt until Phase B.

**Risk:** After Option A, the Immutable Audit Log is the only path that reliably passes Gate 5c. A v0.9 integration test designed around EU BFSI data that primarily surfaces MCP Broker or general Production capabilities will still encounter gate failures. The v0.9 integration test must use data that exercises the Audit Log path.

---

### Option B: Lower Gate 5c threshold to 85

**Description:** Change `skill_5_pass` from `90` to `85` in `config.yaml:18`. The Immutable Audit Log (ECS=85) passes immediately without any executor changes.

**Tradeoffs:**
- Pro: Unblocks the Immutable Audit Log immediately with a one-line config change.
- Pro: No executor logic changes; no test assertion updates beyond config references.
- Con: Directly contradicts the SKILL.md rationale for the 90 threshold. Lowers the gate without addressing the executor's under-calibration — treats the symptom.
- Con: 85 is exactly the current executor ceiling. The gate passes/fails on a razor margin: one contradiction deduction (−10 for MCP Broker) drops ECS to 75, below the new threshold. No headroom.
- Con: MCP Security Broker (ECS=75) and general fallback Production (max 70) still fail at 85.
- Con: Requires spec updates in three files (`config.yaml`, `AGENT.md`, `SKILL.md`) and introduces a permanent inconsistency between the documented threshold rationale and the actual threshold value.

**Risk:** Medium. Setting the threshold exactly at the ceiling of the best-evidenced capability produces a brittle gate with no defensible margin. The SKILL.md rationale for 90 is specific and documented; lowering to 85 without updating or refuting that rationale leaves the specification internally inconsistent.

---

### Option C: Make the Gate 5c threshold configurable by assessment context

**Description:** Add a second threshold key in `config.yaml` — `skill_5_governance_pass: 75` alongside `skill_5_pass: 90`. Gate 5c reads `output_mode` from `ca_inputs` to select the threshold — `"Governance Assessment"` uses 75; formal proposal contexts use 90.

**Tradeoffs:**
- Pro: Acknowledges that a governance dossier and a commercial proposal have different risk profiles.
- Con: The CA always runs in `"Governance Assessment"` mode. `output_mode` has only one effective value in CA context; two threshold branches add complexity without benefit at v0.9.
- Con: The SKILL.md blast-radius rationale applies regardless of assessment context. A weakly-evidenced Production capability in a governance dossier feeds downstream into solution mapping, ISO assessment, and the feature validation table — the propagation risk is the same.
- Con: If the governance-context threshold is 75, Canonical-only Production capabilities (ECS 70) pass, weakening the quality signal below its minimum defensible level.

**Risk:** Medium. Dual thresholds for the same gate create maintenance risk and a threshold that becomes meaningless if set too low in the governance context.

---

### Option D: Full ECS recalibration across all Production capability paths

**Description:** Apply the `use-cases.md` +10 increment (Option A) and additionally enhance the general fallback Production path to apply `+15` architecture corroboration and `+10` use-cases where secondary source evidence exists in the CPM for that capability. All well-evidenced Production capabilities reach ECS ≥ 90.

**Tradeoffs:**
- Pro: All named Production capabilities in the CPM with secondary source evidence become capable of passing Gate 5c. The gate becomes meaningful across the full capability inventory.
- Pro: The general fallback path, currently producing max 70, reaches max 95 for fully-corroborated capabilities.
- Con: Requires examining each CPM Production capability entry against available secondary sources. Corroboration must be real — applying increments to capabilities that lack secondary evidence would produce inflated ECS values on paths that should not pass.
- Con: Wider test blast radius. CVA executor tests assert specific ECS values; assertions change for every path touched.
- Con: MCP Security Broker: +10 use-cases − 10 contradiction = net 0, landing at 85 — one point below Gate 5c. Phase B must decide whether a Production capability with a documented contradiction should be capable of passing.

**Risk:** Moderate. Recalibrating multiple ECS paths in a single change is higher risk for v0.9 than implementing the single documented omission.

---

## Comparison

| Criterion | Option A (implement +10) | Option B (lower threshold) | Option C (context-sensitive) | Option D (full recalibration) |
|---|---|---|---|---|
| SKILL.md spec consistency | Full | Requires spec change | Partial | Full |
| Threshold change required | No | Yes | No | No |
| Preserves 90/100 rationale | Yes | No | Partial | Yes |
| Unblocks Immutable Audit Log | Yes (95) | Yes (85 — no headroom) | Depends | Yes |
| Unblocks MCP Security Broker | No (75 < 90) | No (75 < 85) | Depends on value | Requires contradiction review |
| Unblocks general Production paths | No (max 80) | No (max 70 < 85) | Depends on value | Yes |
| Executor changes | Minimal (one increment) | None | None | Moderate |
| ECS score defensibility | High | Low | Medium | High |
| v0.9 scope | Targeted | Targeted | Not recommended | Too broad |
| Test blast radius | Low (1 path) | Very low | Very low | Moderate (multiple paths) |

---

## Decision

**Option A for v0.9 (implement the missing `use-cases.md` +10 ECS increment); Option D as Phase B follow-through.**

The SKILL.md at line 278 documents the +10 use-cases.md increment. The CVA executor already checks `usecases_file.exists()` and logs the source in `sources_checked`. The increment is the only missing step. This is a specification omission in the executor — not a design question, and not a threshold calibration decision.

1. **The threshold of 90/100 is correct and must not be changed.** The SKILL.md blast-radius rationale is specific and documented. Capability validation errors propagate into every downstream skill that references the validated capability. The gate standard is correspondingly strict.

2. **The executor omission must be corrected.** The `use-cases.md` +10 increment is applied to the Immutable Audit Log path in `skill_executor.py`. The `ecs_arithmetic` string is updated to include the increment. The Immutable Audit Log reaches ECS 95, passing Gate 5c with 5 points of headroom.

3. **The mock default is updated.** `orchestrator.py:509` mock default changes from `94` to `95` to reflect the real executor ceiling for the Audit Log path.

4. **CVA executor tests are updated.** Assertions for the Immutable Audit Log fixture change from `ecs=85` to `ecs=95`.

5. **Option D is the Phase B target.** All well-evidenced CPM Production capabilities should be capable of producing ECS ≥ 90 with full secondary source corroboration. Phase B implements the general fallback Production path enhancement, after CPM secondary-source review per capability. The MCP Security Broker contradiction path (net ECS 85 after +10 and −10) is a Phase B decision: whether a Production capability with a documented contradiction should clear Gate 5c requires explicit product review.

Option B is rejected: setting the threshold to exactly the executor ceiling is brittle, does not fix the underlying calibration, and leaves the SKILL.md rationale internally inconsistent. Option C is rejected: context-sensitive thresholds add complexity for a distinction that has no effective difference in CA's current operating mode. Option D is the correct long-term target but has a broader test blast radius than is appropriate for v0.9.

---

## Consequences

**Positive:**
- Resolves Adapter Audit Mismatch M2 for the Immutable Audit Log capability path.
- The 90/100 threshold and its blast-radius rationale are preserved intact.
- ECS arithmetic is now correct and reproducible for the Audit Log path: `Base: +50; Detailed Entry: +20; Architecture Corroboration: +15; Use-cases.md corroboration: +10; Total: 95`.
- The `use-cases.md` source, already in `sources_checked`, now matches the increment applied — no inconsistency between logged sources and arithmetic.
- CVA executor test suite is updated to reflect real-execution values.

**Negative:**
- MCP Security Broker (ECS=75 after contradiction deduction) and general fallback Production paths (max 80) remain below Gate 5c until Phase B recalibration. A CA end-to-end integration test must be designed around the Immutable Audit Log path for v0.9.
- CVA executor tests require ECS assertion updates. The test blast radius is narrow (one fixture path), but the change must be made before any test suite is considered current.

---

## Deferred

- **General fallback Production path ECS recalibration** — Phase B. Apply `use-cases.md` +10 and `product-architecture-investigation.md` +15 to CPM Production capabilities with documented secondary source evidence. Corroboration must be verified per capability, not applied uniformly.
- **MCP Security Broker contradiction path review** — Phase B. After use-cases.md +10 increment: ECS = 75 + 10 − 10 = 75. Separate decision required on whether a Production capability with a documented contradiction should be capable of clearing Gate 5c, and at what ECS value.
- **Assessment context-sensitive thresholds** — Phase C, if the governance/commercial threshold distinction becomes operationally necessary at v1.0 scale.

---

## Related Decisions

- **ADR-001:** CPM is the authoritative source for all capability status lookups. The CVA executor validates against CPM entries; ECS reflects evidence strength for entries in that model.
- **ADR-004:** Primary-source evidence requirements inform the ECS increment structure. The `product-architecture-investigation.md` +15 and `use-cases.md` +10 increments exist precisely because ADR-004 established that status elevation requires primary-source corroboration.
- **ADR-007:** Resolves Gate 5c input source (M1). ADR-008 resolves Gate 5c threshold calibration (M2). Both must be implemented before the CA end-to-end integration test can produce a `COMPLETE` run.
