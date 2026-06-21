# Architecture Decision Record: ADR-009

## Title
ADR-009: ECS General Fallback Calibration and Per-Capability Evidence Architecture

---

## Status
**Proposed**

---

## Context

ADR-008 resolved M2 (Gate 5c ECS threshold 90 > CVA executor maximum 85) by implementing the missing `use-cases.md` +10 ECS increment for the Immutable Audit Log path. That increment raises the Audit Log from ECS 85 → 95, clearing Gate 5c with 5 points of headroom.

The ECS coverage audit (2026-06-21) established that ADR-008 Option A resolves M2 for exactly **1 of 17 Production capabilities**:

| Executor path | Trigger | Pre-ADR-008 ECS | Post-ADR-008 ECS | Gate 5c (≥90) |
|---|---|---|---|---|
| Audit fixture | `"audit" in cap_key` | 85 | **95** | **Pass** |
| Broker fixture | `"broker" in cap_key or "mcp" in cap_key` | 75 | 75 | Fail |
| General fallback | All other matched Production | 50–70 | 50–70 | Fail |

The general fallback path (`skill_executor.py`, general Production branch) computes:
```
ECS = 50 (base)
    + 20 if len(canonical_notes) > 50
    = 70 maximum
```

`product-architecture-investigation.md` and `use-cases.md` are checked (`skill_executor.py:172–185`) and added to `sources_checked`, but neither the +15 architecture corroboration increment nor the +10 use-cases increment is applied to the ECS integer in this branch. The SKILL.md specification defines both increments (lines 277–278). They are specified but unimplemented for the general fallback path.

The MCP Security Broker follows a separate named fixture (`"broker" in cap_key or "mcp" in cap_key`) with explicit arithmetic:
```
ECS = 50 (base)
    + 20 (detailed entry)
    + 15 (architecture corroboration — product-architecture-investigation.md)
    − 10 (contradiction — documented discrepancy in product-architecture-investigation.md)
    = 75
```
The contradiction is real: `product-architecture-investigation.md` documents an inconsistency between the NHI management claim in the CPM and the architecture section for MCP Broker. The −10 is a correct deduction, not an artifact.

**The ECS path selection architecture problem.** The CVA executor selects the ECS calculation path via keyword matching against the capability name string (`cap_key`). This architecture has three consequences:

1. **Silent regression risk.** Any CPM capability whose name does not contain `"audit"` or `"broker"` falls into the general fallback path regardless of available secondary source evidence. A new Production capability added to the CPM silently gets ECS ≤ 70 without the +15 and +10 increments — even if both secondary sources fully corroborate it.
2. **Evidence and arithmetic are decoupled.** The CPM records capability status, notes, and sources. The executor holds the ECS arithmetic as hardcoded logic. When evidence changes (a new use-case added, an architecture detail updated), the ECS does not change unless a developer also updates the executor.
3. **Inconsistency between specification and implementation.** SKILL.md specifies ECS increments as conditional on secondary source corroboration. The executor applies them only for the two named fixture paths. The increment structure cannot be understood from either file alone.

This ADR addresses three decision axes:

- **Q1:** How should the +15 architecture corroboration and +10 use-cases corroboration increments be applied to general fallback Production capabilities?
- **Q2:** Should MCP Security Broker remain below Gate 5c due to its documented contradiction?
- **Q3:** Should ECS path selection move from keyword matching to per-capability CPM metadata?

---

## Constraints

1. **ADR-001:** All capability status and evidence lookups must route through `canonical-product-model.md`. Any change to ECS calculation that requires reading the CPM must preserve ADR-001's single-source-of-truth guarantee.
2. **ADR-004:** ECS increments must reflect real, primary-source evidence. The +15 and +10 increments must not be applied to capabilities that lack actual corroboration in the secondary source files. Fabricating corroboration violates the primary-source evidence requirement.
3. **ADR-008:** The ECS threshold of 90 is correct and must not be lowered. The blast-radius rationale in SKILL.md stands. Any option that requires threshold adjustment is out of scope.
4. **SKILL.md:177:** ECS arithmetic must be reproducible from the validation report alone. The `ecs_arithmetic` string in the executor output must reflect all increments actually applied.
5. **SKILL.md:277–278:** The increment conditions are: `product-architecture-investigation.md` corroboration = +15; `use-cases.md` corroboration = +10. These are specified as conditional on the file corroborating the specific capability in context — not on file existence alone.
6. In Build and Aspirational capabilities must continue to produce ECS = 0. The constraints in this ADR apply only to Production capabilities.

---

## Q1: Increment Application Strategy for the General Fallback Path

### Option A: Uniform application — apply +15 and +10 to all matched Production capabilities

**Description:** In the general fallback Production branch of `skill_executor.py`, unconditionally add `+15` and `+10` to the ECS when `matched_cap` is not None. All 15 general fallback Production capabilities reach ECS 95.

**Implementation:** In the general fallback branch:
```python
if matched_cap:
    ecs = 50 + 20 + 15 + 10   # Base + notes + arch + use-cases = 95
    ecs_arithmetic = "Base: +50; Detailed Entry: +20; Architecture Corroboration: +15; Use-cases.md corroboration: +10; Total: 95"
```

**Tradeoffs:**
- Pro: All 15 general fallback Production capabilities pass Gate 5c at ECS 95. Full resolution of M2 for the general fallback path.
- Pro: Simplest implementation change — two integer additions.
- Con: Violates ADR-004 and the SKILL.md increment conditions. The +15 and +10 are specified as conditional on the secondary source actually corroborating the specific capability. Applying them uniformly to all Production capabilities produces inflated ECS values for capabilities that are not meaningfully described in `product-architecture-investigation.md` or `use-cases.md`.
- Con: `ecs_arithmetic` string becomes false — it claims architecture corroboration and use-cases corroboration were checked when they were not. SKILL.md:177 requires that arithmetic be reproducible.
- Con: When the CVA runs against a real operator who reads the validation report, the arithmetic section will state corroboration that was not verified. This is a misrepresentation of evidence quality.

**Risk:** High. The ECS becomes meaningless as an evidence quality signal. Gate 5c passes for all Production capabilities regardless of actual documentation quality. The Claims Firewall downstream receives validation reports with inflated confidence scores.

---

### Option B: Conditional application — check secondary source files at runtime for each capability

**Description:** In the general fallback Production branch, check whether `product-architecture-investigation.md` and `use-cases.md` actually contain the specific capability name before applying the increments.

**Implementation:**
```python
arch_text = arch_file.read_text() if arch_file.exists() else ""
uc_text = usecases_file.read_text() if usecases_file.exists() else ""
cap_name = matched_cap.get("original_name", cap_key)

if cap_name.lower() in arch_text.lower():
    ecs += 15
    ecs_arithmetic += f"; Architecture Corroboration: +15"
if cap_name.lower() in uc_text.lower():
    ecs += 10
    ecs_arithmetic += f"; Use-cases.md corroboration: +10"
ecs_arithmetic += f"; Total: {ecs}"
```

**Tradeoffs:**
- Pro: Implements SKILL.md increment conditions as specified. ECS reflects actual secondary source presence.
- Pro: Reproducible arithmetic — the validation report accurately states which sources corroborated the capability.
- Pro: No CPM schema changes required.
- Con: String containment matching (`cap_name in text`) is fragile. A capability named `"Runtime Guardrails — PII detection and masking"` may not appear verbatim in the secondary source files if those files use shorthand (`"PII guardrail"`, `"runtime scanner"`). The match would fail and the increment would not apply, producing artificially low ECS for a well-documented capability.
- Con: The ECS becomes dependent on exact string matching against unstructured documents. This is brittle in exactly the same way as the keyword path selection the ADR is trying to improve.
- Con: Two full text file reads per capability validation call, at runtime, in production. Performance impact is minimal for the current scale but is architecturally undesirable — evidence lookup belongs at design time, not at validation time.

**Risk:** Medium. The brittle string matching means ECS values may be inconsistent across runs if the secondary source files are reformatted. Two capabilities that are equally well-documented may receive different ECS values based on naming convention differences.

---

### Option C: CPM metadata — add `ecs_evidence` fields to each CPM Production entry; executor reads from metadata

**Description:** Add an `ecs_evidence` block to each Production capability entry in `canonical-product-model.md`. The executor reads this block and applies the appropriate increments based on what the CPM records, rather than keyword path selection or runtime file scanning.

**CPM entry format (proposed `ecs_evidence` addition):**
```markdown
### Capability: Immutable Audit Log
Status: Production
...existing fields...
ECS Evidence:
  architecture_corroboration: true   # product-architecture-investigation.md §4
  use_cases_corroboration: true      # use-cases.md scenarios 1.1, 1.2, 5.1
  contradictions: []
```

```markdown
### Capability: MCP Security Broker — core
Status: Production
...existing fields...
ECS Evidence:
  architecture_corroboration: true   # product-architecture-investigation.md §4
  use_cases_corroboration: true      # use-cases.md scenario 1.2
  contradictions:
    - source: product-architecture-investigation.md
      description: NHI management claim inconsistency
      deduction: 10
```

**Executor behaviour:** The executor calls `parse_canonical_model()` (already invoked for CPM lookup) and reads the `ecs_evidence` block for the matched capability. Each flag applies the corresponding increment. Contradictions apply their deductions. The `ecs_arithmetic` string is constructed from the metadata.

**Tradeoffs:**
- Pro: Evidence and ECS arithmetic are co-located in the CPM. When a new secondary source is added, the CPM entry is updated and the ECS automatically changes on the next validation run. No executor code changes needed for new capabilities.
- Pro: Satisfies ADR-001: the CPM becomes the authoritative source not only for capability status but for capability evidence quality. All ECS calculation flows through the CPM.
- Pro: Satisfies SKILL.md:177: `ecs_arithmetic` is derived from structured metadata, not hardcoded strings. It is reproducible by anyone who reads the CPM entry and the SKILL.md specification.
- Pro: Eliminates keyword path selection entirely. New capabilities added to the CPM get correct ECS without executor modification.
- Con: Requires updating the CPM schema — adding `ecs_evidence` blocks to all Production capability entries. This is a one-time authoring cost but it requires careful per-capability review.
- Con: `parse_canonical_model()` must be extended to read and return the `ecs_evidence` block. Minor executor change, but a change to the CPM parser.
- Con: The CPM `ecs_evidence` fields must be maintained as evidence evolves. If `use-cases.md` is updated to add or remove coverage for a capability, the CPM must also be updated. Two files must be kept in sync.

**Risk:** Low for long-term correctness; medium for one-time authoring. The CPM authoring requires per-capability review of both secondary source files to determine which corroboration flags are accurate. This review is necessary regardless of approach — Option B defers it to runtime, Option C does it at authoring time.

---

### Option D: Maintain status quo for the general fallback path (no changes)

**Description:** Accept that 15 of 17 Production capabilities remain at ECS ≤ 70 after ADR-008. Do not extend the +15 and +10 increments to the general fallback path. Phase B recalibration is deferred indefinitely or until a specific triggering event.

**Tradeoffs:**
- Pro: No changes required. No CPM schema change. No executor logic change.
- Con: 15 of 17 Production capabilities cannot pass Gate 5c. The CA integration test is constrained to Immutable Audit Log path only indefinitely. Any governance assessment surfacing primarily Guardrails, LLM Gateway, or Red Teaming capabilities in Skill 3 halts at Gate 5c.
- Con: Contradicts the Phase B commitment documented in ADR-008.

**Risk:** High for product completeness. Option D means the CA chain's Skill 5 gate is only passable for assessments centred on audit trail requirements. It is unacceptable as a long-term position.

---

## Q2: MCP Security Broker Contradiction Treatment

The MCP Security Broker produces ECS 75 under current arithmetic and ECS 85 after Phase B calibration (50 + 20 + 15 + 10 − 10 = 85). At ECS 85 it is 5 points below Gate 5c threshold. The contradiction is documented and real.

### Option X: Maintain −10 contradiction deduction; MCP Security Broker remains below Gate 5c at Phase B

**Description:** The contradiction deduction stays at −10. Under Phase B calibration (with +15 and +10 applied), MCP Broker reaches ECS 85. Gate 5c threshold is 90. MCP Broker fails Gate 5c. A CA governance assessment whose primary capability match is MCP Broker halts at `HALTED_GATE_5_SCORE_INSUFFICIENT`.

**Rationale:** The contradiction in `product-architecture-investigation.md` documents a real inconsistency in the NHI management capability claim. The Claims Firewall's purpose is zero-tolerance enforcement against capability misrepresentation. A Production capability with a documented architecture inconsistency producing ECS below the gate threshold is the Firewall functioning correctly — the inconsistency must be resolved in the CPM before the capability earns full gate clearance.

**Tradeoffs:**
- Pro: The −10 deduction is evidence-grounded and meaningful. Removing or reducing it without resolving the underlying inconsistency weakens the Firewall.
- Pro: The correct resolution is to resolve the NHI claim inconsistency in the CPM and the secondary source — not to reduce the penalty.
- Con: MCP Security Broker remains ungated in Skill 5 until the contradiction is resolved. Any BFSI assessment centred on Zero Trust / network access controls halts at Gate 5c.

**Risk:** Low for Claims Firewall integrity. Medium for CA completeness — MCP Broker is a significant capability in zero-trust architecture governance assessments.

---

### Option Y: Reduce contradiction deduction from −10 to −5; MCP Broker reaches ECS 90

**Description:** Change the contradiction deduction to −5. Under Phase B calibration: 50 + 20 + 15 + 10 − 5 = 90. MCP Broker exactly meets the Gate 5c threshold.

**Tradeoffs:**
- Pro: MCP Broker clears Gate 5c without resolving the underlying contradiction.
- Con: The deduction value becomes arbitrary. −10 was set to reflect a material inconsistency; −5 has no documented basis. SKILL.md does not define a scale for contradiction severity.
- Con: ECS arithmetic for MCP Broker becomes misleading: the report states corroboration increments and a contradiction deduction, producing an ECS that exactly meets the gate. The gate is designed to ensure quality — a capability at exactly 90 with a known contradiction is not a signal of confidence.
- Con: Sets a precedent that contradiction deductions can be calibrated to produce gate passage, undermining the Firewall.

**Risk:** High. Arbitrary deduction values corrupt the ECS as a quality signal and weaken the Claims Firewall's evidence standard.

---

### Option Z: Compound gate — contradiction-bearing capabilities pass at ECS ≥ 85 if `required_actions` is non-empty

**Description:** Modify Gate 5c logic: a capability with `contradictions` recorded in CPM metadata and ECS ≥ 85 passes the gate if its `required_actions` list is non-empty. The required action documents what must be resolved before the claim is commercially usable.

**Tradeoffs:**
- Pro: Allows MCP Broker (ECS 85 after Phase B) to pass Gate 5c while ensuring the contradiction is documented and flagged for resolution.
- Pro: The Claims Firewall still catches the inconsistency — it appears in `required_actions`, which is surfaced in the validation report and visible to the human approval gate.
- Con: Changes the Gate 5c contract in the CA orchestrator, introducing a compound condition. This adds complexity to the gate and must be documented in SKILL.md and AGENT.md.
- Con: `required_actions` is populated by the CVA executor's contradiction logic — if the executor does not correctly populate it for all contradiction cases, the compound check may pass silently.

**Risk:** Medium. The compound gate is architecturally sound but requires SKILL.md and orchestrator changes. It should be a named option in Phase B with explicit product review — not an ad-hoc modification to pass one capability.

---

## Q3: ECS Path Selection Architecture

### Option α: Maintain keyword matching (current architecture)

**Description:** Keep `"audit" in cap_key` and `"broker" in cap_key` as the path selectors. New capabilities added to the CPM fall into the general fallback path unless a developer also adds a keyword branch to the executor.

**Tradeoffs:**
- Pro: No changes required.
- Con: Coupling between CPM capability names and executor keyword strings. If a capability is renamed in the CPM, the keyword branch silently stops matching. New capabilities silently receive lower ECS.
- Con: The ECS architecture cannot be understood from either the CPM or the SKILL.md alone — it requires reading the executor's keyword logic.

**Risk:** High long-term. Every new CPM Production capability is a latent ECS calibration risk.

---

### Option β: Add `executor_path` field to CPM entries; executor reads path identifier

**Description:** Add a structured `executor_path` field to each CPM Production entry. The executor reads this field and routes to the corresponding ECS arithmetic function.

```markdown
### Capability: Immutable Audit Log
executor_path: audit_log
```

**Tradeoffs:**
- Pro: Eliminates keyword matching. New capabilities explicitly declare their execution path.
- Pro: Path routing is visible in the CPM and auditable.
- Con: `executor_path` is a code-coupling artifact embedded in a knowledge file. The CPM must know about executor implementation details (`"audit_log"`, `"mcp_broker"`, `"general"`). This is an inappropriate dependency direction — the knowledge layer should not reference the agent layer.
- Con: Adding named fixture paths for each Production capability would require adding ~17 named branches to the executor, defeating the purpose of a general fallback.

**Risk:** Medium. Creates knowledge-layer / agent-layer coupling that violates ADR-003's layer separation principle.

---

### Option γ: Derive ECS arithmetic from CPM evidence metadata; eliminate keyword path selection

**Description:** The CPM carries per-capability `ecs_evidence` metadata (as defined in Q1 Option C). The executor reads this metadata and derives all ECS arithmetic from it. The named fixture paths (`audit_log`, `mcp_broker`) are eliminated — every capability routes through a single evidence-driven calculation function.

```python
def compute_ecs(cap_key, cpm_entry):
    evidence = cpm_entry.get("ecs_evidence", {})
    ecs = 50
    arithmetic = ["Base: +50"]
    if len(cpm_entry.get("notes", "")) > 50:
        ecs += 20
        arithmetic.append("Detailed Entry: +20")
    if evidence.get("architecture_corroboration"):
        ecs += 15
        arithmetic.append("Architecture Corroboration: +15")
    if evidence.get("use_cases_corroboration"):
        ecs += 10
        arithmetic.append("Use-cases.md corroboration: +10")
    for contradiction in evidence.get("contradictions", []):
        deduction = contradiction.get("deduction", 0)
        ecs -= deduction
        arithmetic.append(f"Contradiction ({contradiction['description']}): -{deduction}")
    arithmetic.append(f"Total: {ecs}")
    return ecs, "; ".join(arithmetic)
```

**Tradeoffs:**
- Pro: ECS arithmetic is fully driven by CPM evidence metadata. No keyword matching. No hardcoded fixture paths. New Production capabilities added to the CPM with correct `ecs_evidence` blocks automatically receive correct ECS.
- Pro: Satisfies ADR-001: the CPM is authoritative for both status and evidence quality.
- Pro: Satisfies SKILL.md:177: arithmetic is reproducible directly from CPM metadata fields.
- Pro: The executor becomes a general-purpose evidence evaluator rather than a collection of hardcoded paths. It is smaller, more testable, and easier to maintain.
- Con: Requires Q1 Option C (CPM `ecs_evidence` blocks) as a prerequisite. Options γ and C are a combined decision.
- Con: The named fixture paths currently in `skill_executor.py` (Immutable Audit Log, MCP Broker) must be replaced by the general function — a breaking change to the executor. Existing CVA tests that assert specific ECS values for these paths must be updated.

**Risk:** Low for long-term correctness. Medium for implementation — the named fixture paths have subtly different arithmetic (MCP Broker has contradictions; Audit Log does not) that must be correctly captured in CPM metadata before removing the named paths.

---

## Comparison

### Q1: Increment Application Strategy

| Criterion | A (Uniform) | B (Runtime scan) | C (CPM metadata) | D (Status quo) |
|---|---|---|---|---|
| ADR-004 compliance | No — inflates ECS without evidence check | Partial — checks presence, not relevance | Yes — evidence recorded at authoring time | N/A |
| SKILL.md:177 arithmetic accuracy | No | Yes | Yes | Yes (ECS 70 is correct for current state) |
| M2 resolution scope | All 15 fallback capabilities | Depends on string matching | All 15 with correct metadata | None |
| Fragility risk | Low | High (string matching) | Low | None |
| CPM schema change required | No | No | Yes | No |
| Executor change required | Minimal | Moderate | Moderate | None |
| Appropriate for Phase B | No | No | Yes | No |

### Q2: MCP Broker Contradiction

| Criterion | X (Maintain −10) | Y (Reduce to −5) | Z (Compound gate at 85) |
|---|---|---|---|
| Evidence-grounded | Yes | No | Yes |
| MCP Broker passes Gate 5c (Phase B) | No (ECS 85) | Yes (ECS 90, exactly) | Yes (if required_actions non-empty) |
| Weakens Claims Firewall | No | Yes | Minimal |
| Requires product decision to resolve | Yes (resolve contradiction in CPM) | No (arbitrary change) | Yes (compound gate design) |
| Appropriate for Phase B | Yes — requires contradiction review | No | Possible — needs SKILL.md update |

### Q3: ECS Path Selection Architecture

| Criterion | α (Keep keywords) | β (executor_path field) | γ (CPM evidence metadata) |
|---|---|---|---|
| ADR-003 layer separation | Violates (executor holds knowledge) | Violates (CPM references executor paths) | Compliant |
| New capability safety | Silent ECS degradation | Explicit path required | Automatic if CPM metadata correct |
| ADR-001 compliance | Partial | Partial | Full |
| Requires Q1 Option C | No | No | Yes (prerequisite) |
| Named fixture path elimination | No | Partial | Yes |
| Phase B implementation scope | Low | Medium | Medium |

---

## Recommended Decision

### Q1: Option C — CPM `ecs_evidence` metadata blocks

Add structured `ecs_evidence` to each Production capability entry in `canonical-product-model.md`. The executor reads this metadata to determine which increments apply. Option A is rejected because it inflates ECS without evidence verification, violating ADR-004. Option B is rejected because runtime string matching against unstructured documents is fragile and produces inconsistent ECS values. Option D is rejected because it leaves 15 of 17 Production capabilities permanently below Gate 5c.

### Q2: Option X — Maintain −10 contradiction deduction for MCP Security Broker

The NHI management inconsistency is real and documented. The correct resolution is to resolve the inconsistency in `canonical-product-model.md` and `product-architecture-investigation.md`, not to reduce the deduction. Option Y is rejected because arbitrary deduction values corrupt the ECS as a quality signal. Option Z is a sound compound gate design but belongs to a separate decision — it requires SKILL.md and orchestrator changes that should be reviewed independently. Phase B must include an explicit decision on whether the MCP Broker contradiction has been resolved or whether Option Z should be adopted.

### Q3: Option γ — Derive ECS arithmetic from CPM evidence metadata; eliminate keyword path selection

Q1 Option C and Q3 Option γ are a combined decision. Once the CPM carries `ecs_evidence` blocks, the named fixture paths in the executor are redundant and fragile. Option γ eliminates keyword matching entirely. The executor becomes a general-purpose evidence evaluator that reads from the CPM. This complies with ADR-001 (CPM as authoritative source) and ADR-003 (knowledge layer does not reference agent layer). Option α is rejected because it perpetuates the silent ECS degradation risk for new capabilities. Option β is rejected because `executor_path` embeds agent-layer knowledge in the CPM, violating ADR-003.

---

## Decision Summary

1. Add `ecs_evidence` blocks to all 17 Production capability entries in `canonical-product-model.md`. Each block records `architecture_corroboration: bool`, `use_cases_corroboration: bool`, and `contradictions: list`. Values are set based on per-capability review of `product-architecture-investigation.md` and `use-cases.md`.

2. Replace the keyword-path ECS calculation in `skill_executor.py` with a single evidence-driven function that reads from CPM `ecs_evidence` metadata. The Immutable Audit Log and MCP Security Broker named fixture paths are removed. All Production capabilities route through the same function.

3. MCP Security Broker `ecs_evidence` records `architecture_corroboration: true`, `use_cases_corroboration: true`, and `contradictions: [{source: "product-architecture-investigation.md", description: "NHI management claim inconsistency", deduction: 10}]`. Post-Phase B ECS = 85. Gate 5c result: Fail. Resolution requires either correcting the contradiction in the CPM (removing the deduction) or adopting Option Z in a separate ADR.

4. All other general fallback Production capabilities with full secondary source corroboration reach ECS 95 under this decision. Account Management, Cost Tracking, PromptOps, On-premises deployment, India VPC, and Multi-model routing reach ECS 90 where use-cases corroboration is weaker — borderline pass.

---

## Consequences

**Positive:**
- 15 of 17 Production capabilities pass Gate 5c under this decision (all general fallback capabilities with `ecs_evidence` corroboration set correctly).
- ECS arithmetic is reproducible from CPM metadata. SKILL.md:177 is satisfied.
- New Production capabilities added to the CPM receive correct ECS automatically if `ecs_evidence` is populated at authoring time.
- ADR-001 is extended: the CPM is now authoritative for capability evidence quality, not only capability status.
- The CVA executor is simplified: keyword paths are eliminated; one general function handles all Production capabilities.

**Negative:**
- MCP Security Broker remains at ECS 85 (below Gate 5c threshold of 90) until its documented contradiction is resolved or Option Z is adopted.
- CPM authoring effort: `ecs_evidence` blocks must be written for all 17 Production capability entries. Each block requires per-capability review of both secondary source files. This is a one-time authoring cost but must be done carefully.
- CVA executor named fixture paths are removed. Existing CVA executor tests that assert hardcoded ECS values for the Audit Log and MCP Broker paths must be rewritten to test the evidence-driven function.
- The CPM becomes a dependency of ECS calculation at runtime. If the CPM is unavailable or malformed, the CVA executor cannot produce ECS values.

---

## Implementation Order

This decision requires three sequential implementation items:

1. **Per-capability evidence review** (authoring, not code): Review `product-architecture-investigation.md` and `use-cases.md` for each of the 17 Production capabilities. Record `architecture_corroboration`, `use_cases_corroboration`, and `contradictions` accurately.

2. **CPM `ecs_evidence` block authoring** (CPM update): Add the structured `ecs_evidence` block to each Production capability entry in `canonical-product-model.md`. This must accurately reflect the findings from step 1.

3. **Executor refactor** (code): Replace the keyword-path ECS logic in `skill_executor.py` with the evidence-driven function. Update CVA executor tests. Verify that Immutable Audit Log continues to produce ECS 95 and MCP Broker produces ECS 85 under the new function.

Step 3 must not begin before step 2 is complete — the executor reads from the CPM, and the CPM must be correctly populated before the executor refactor is testable.

---

## Impact Assessment

| Component | Impact |
|---|---|
| **Gate 5c** | 15 of 17 Production capabilities clear the gate after this decision. MCP Broker (ECS 85) remains below until contradiction is resolved. Gate threshold unchanged at 90. |
| **Claims Firewall** | Strengthened: ECS now reflects actual evidence quality per ADR-004, not keyword path assignment. Inflated ECS (Option A) is rejected. The Firewall's capability validation input is more accurate. |
| **CA integration** | The v0.9 integration test constraint (Immutable Audit Log path only) is lifted after this decision. Assessments surfacing Guardrails, LLM Gateway, Red Teaming, or other general Production capabilities can reach COMPLETE. Exception: assessments whose primary Skill 3 output is MCP Broker only. |
| **v0.9 readiness** | This decision is Phase B scope. v0.9 proceeds with the ADR-008 constraint: Immutable Audit Log path only. This decision must be implemented before Phase B CA integration tests cover the full Production capability inventory. |

---

## Deferred

- **MCP Security Broker contradiction resolution**: The NHI management claim inconsistency in `product-architecture-investigation.md` must be reviewed. If the inconsistency is resolved in the CPM and the secondary source, `contradictions: []` is set in the `ecs_evidence` block and MCP Broker reaches ECS 95 — clearing Gate 5c. This is the preferred resolution. If the inconsistency cannot be resolved, Option Z (compound gate at ECS ≥ 85 with required_actions) should be addressed in a follow-on ADR.
- **Option Z compound gate**: A formal ADR reviewing whether contradiction-bearing Production capabilities should pass Gate 5c via a compound ECS ≥ 85 + `required_actions` non-empty check. Out of scope for this decision.
- **Account Management, Cost Tracking, PromptOps ECS 90 borderline cases**: These capabilities are expected to reach ECS 90 (borderline) rather than 95 because use-cases corroboration is weaker. They pass Gate 5c but should be reviewed when the secondary source files are updated to confirm corroboration is correctly recorded.
- **In Build and Aspirational evidence metadata**: This decision applies only to Production capabilities. In Build and Aspirational capabilities produce ECS 0 by specification. Their `ecs_evidence` blocks, if any, are for documentation purposes only.

---

## Related Decisions

- **ADR-001:** This decision extends the CPM's authority to include evidence quality metadata, not only capability status. ADR-001's single-source-of-truth principle is the basis for choosing Option C (CPM metadata) over Option B (runtime file scanning).
- **ADR-003:** Option β (executor_path in CPM) was rejected because it embeds agent-layer references in the knowledge layer. Option γ (CPM evidence metadata) is ADR-003 compliant — the knowledge layer records facts; the agent layer reads them.
- **ADR-004:** The per-capability evidence review required by this decision is an application of ADR-004's primary-source evidence requirement to ECS calculation. Increments are only applied where corroboration is real.
- **ADR-008:** This decision is the Phase B follow-through to ADR-008 Option D, which was deferred. ADR-008 resolved M2 for one capability (Immutable Audit Log). This decision resolves M2 for the remaining 15 general fallback Production capabilities.
