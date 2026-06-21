# Architecture Decision Record: ADR-007

## Title
ADR-007: Capability Source for Skill 5 in the Client Assessment Chain

---

## Status
**Accepted**

---

## Context

`Skill5Adapter._capability_list()` (`agents/client-assessment-agent/runtime/skill_adapters.py:234`) resolves which Ethana capabilities to submit for validation in Skill 5 (ethana-capability-validation). Its current implementation reads only from `ca_inputs`:

```python
caps = ca_inputs.get("capabilities")       # explicit list from caller
single = ca_inputs.get("capability_name")  # single explicit name
# raises SkillAdapterError if neither present
```

The comment at line 238 acknowledges the deferral explicitly:

> *"Until Skill 3 (solution-mapping) is implemented, fall back to a single capability from `capability_name`. Full extraction from solution-mapping Section 3 lands when Skill 3 is built."*

Skill 3 (`ethana-solution-mapping`) is now built and operational. `REQUIRED_INTAKE_FIELDS` (`orchestrator.py:34`) does not include `capabilities` or `capability_name`. Every standard CA run therefore reaches Skill 5 without either field in `ca_inputs` and halts at `HALTED_ESCALATION`. This is Adapter Audit Mismatch M1.

The CA `AGENT.md` (§5.6, lines 244–251) specifies the intended source explicitly:

> *"The agent extracts all Ethana capability names from: GCM Section 10 (Ethana Configuration Guide); Solution Mapping Section 3 (Proposal-Safe Platform Capabilities); Solution Mapping Section 4 (Roadmap Disclosure items); ISO 42001 Section 8 (Ethana Coverage Analysis)."*

Skill 3 (`solution_mapping_executor.py`) produces a structured `matched_capabilities` list in `skill_3_json` containing `{requirement, matched_capability, capability_status, ccs_score, disposition}` per entry. The `matched_capability` string contains either a named Ethana capability (e.g., `"Immutable Audit Log"`, `"MCP Security Broker — core"`) or a generic non-CPM fallback (`"Ethana Platform"`, `"Cursory advisory service"`).

GCM Section 10 (Skill 2 output) and ISO 42001 Section 8 (Skill 4 output) contain capability references embedded in markdown strings only. No structured field equivalent to `matched_capabilities` exists in either executor's output.

---

## Constraints

1. **ADR-001:** All capability status lookups must route through `knowledge/ethana/canonical-product-model.md`. Any extracted capability name must be matchable against the CPM.
2. **ADR-003:** The adapter's role is I/O transformation only. It must not contain scoring logic or call `state_mgr.transition_to`.
3. The CVA executor (`execute_validation()`, `agents/capability_validation_agent/runtime/skill_executor.py:94`) accepts one capability at a time via `capability_name` and `proposed_claim`. The adapter already handles multiple capabilities via loop at `skill_adapters.py:275`.
4. Generic fallback values from Skill 3 (`"Ethana Platform"`, `"Cursory advisory service"`) are not valid CVA inputs. The CVA returns `validated_status: Unresolved` for names that do not match any CPM entry, forcing `escalation_required: true` and a guaranteed gate failure on any run where these are the only entries.
5. Capabilities with `capability_status` of `"In Build"` or `"Aspirational"` produce `ecs: 0` in the CVA executor. Including them in the capability list generates prohibited-claim documentation — the CA `AGENT.md` §5.6 specifies this as intentional for Roadmap Disclosure items (the Claims Firewall purpose).
6. `ca_inputs["capabilities"]` as an explicit override must be preserved as the primary path. It exists for targeted single-capability validation use cases outside standard governance assessment.

---

## Options

### Option A: Extract from `skill_3_json["matched_capabilities"]` only (implement the deferred extraction)

**Description:** `_capability_list()` reads `upstream["skill_3_json"]["matched_capabilities"]`, filters to CPM-matchable entries, deduplicates by name, and constructs the capability list. The `ca_inputs["capabilities"]` explicit override remains primary.

**Implementation:** In `Skill5Adapter._capability_list()` (`skill_adapters.py:234`), after the `ca_inputs` checks, add:
```python
rows = upstream.get("skill_3_json", {}).get("matched_capabilities", [])
seen = set()
caps = []
for row in rows:
    name = row.get("matched_capability", "")
    if name in ("Ethana Platform", "Cursory advisory service") or name in seen:
        continue
    seen.add(name)
    caps.append({
        "capability_name": name,
        "proposed_claim": f"Ethana {name} addresses the governance requirement: {row.get('requirement', '')}",
    })
if not caps:
    raise SkillAdapterError("Skill 5 pre-check failed: no named capabilities in skill_3_json matched_capabilities")
return caps
```

**Tradeoffs:**
- Pro: Directly implements the deferred extraction documented in the adapter comment. No changes to `REQUIRED_INTAKE_FIELDS` or the CA orchestrator.
- Pro: `matched_capabilities` is structured data — no parsing required. `matched_capability` values originate from `parse_canonical_model()` in `solution_mapping_executor.py`, which reads from the same CPM the CVA will validate against. Name format consistency is guaranteed by construction.
- Pro: Preserves `ca_inputs["capabilities"]` explicit override.
- Con: Partial coverage of AGENT.md §5.6. GCM Section 10 and ISO 42001 Section 8 capability references are not included.
- Con: If Skill 3 produces only generic fallback entries for a given intake, the filtered list is empty and `SkillAdapterError` is raised.

**Risk:** Low for the documented v0.9 fixture scope (EU BFSI, India DPDP, UK Insurance). Those profiles produce named Production capabilities in `matched_capabilities`. The empty-list edge case requires a meaningful error message.

---

### Option B: Add `capabilities` as a required intake field

**Description:** Add `capabilities` (list of `{capability_name, proposed_claim}`) to `REQUIRED_INTAKE_FIELDS` in `orchestrator.py:34`. The operator explicitly provides the capability list at run initiation. No changes to `Skill5Adapter._capability_list()`.

**Tradeoffs:**
- Pro: Simplest code change — one line in `REQUIRED_INTAKE_FIELDS`.
- Pro: Explicit operator control over which capabilities are validated.
- Con: Directly contradicts AGENT.md §5.6, which specifies extraction from upstream skill outputs.
- Con: The operator initiating a governance assessment cannot know which capabilities Skill 2 (GCM) and Skill 3 will reference before those skills execute. Intake must be pre-populated with assumptions.
- Con: Creates a structural consistency risk: if operator-listed capabilities do not match those referenced in the assessment package, Skill 5 produces a Capability Validation Report about capabilities not actually in the deliverable.

**Risk:** High. Converts an architectural guarantee (automatic extraction from upstream outputs) into an operator responsibility. Inconsistency between intake capabilities and package capabilities is invisible to Gate 5 checks.

---

### Option C: Extract from all three upstream sources (Skill 2, Skill 3, Skill 4)

**Description:** Combine Skill 3 `matched_capabilities` (structured) with regex extraction against Skill 2 markdown (GCM Section 10 "Ethana Configuration Guide") and Skill 4 markdown (ISO 42001 Section 8 "Ethana Coverage Analysis"). Full implementation of AGENT.md §5.6.

**Tradeoffs:**
- Pro: Full specification compliance with AGENT.md §5.6.
- Pro: Captures capabilities referenced in GCM or ISO contexts that may not appear in solution mapping.
- Con: Markdown parsing is inherently fragile. Section 10 and Section 8 are markdown-formatted strings; their headings and capability name formats depend on each executor's `_compile_markdown()` output. Any reformatting breaks Skill 5 input extraction without a schema-level warning.
- Con: Adds significant complexity to the adapter, which violates ADR-003's principle of adapters as pure I/O transformers. Parsing logic inside an adapter creates a silent coupling to executor output formats.
- Con: GCM and ISO executors do not produce structured capability name lists. Extraction would be tightly coupled to RWA's `compile_control_mapping_to_markdown()` and the ISO executor's `_compile_markdown()`.

**Risk:** High implementation fragility. Not appropriate for v0.9.

---

### Option D: Extract from Skill 3 only, with explicit Phase B deferral documented

**Description:** Identical to Option A, with an explicit code comment and a tracked follow-up item documenting that GCM Section 10 and ISO Section 8 extraction is deferred to Phase B, pending structured capability output from those executors.

This is Option A with scope acknowledgment rather than silent omission.

**Tradeoffs:** Same as Option A, with the addition that the partial coverage is explicitly acknowledged in code and documentation rather than left as a silent gap.

---

## Comparison

| Criterion | Option A/D (Skill 3 extraction) | Option B (intake field) | Option C (all sources) |
|---|---|---|---|
| Implements deferred adapter comment | Yes | No | Exceeds it |
| Consistent with AGENT.md §5.6 | Partial | No | Full |
| Requires structured output from GCM/ISO | No | No | Yes |
| Code complexity in adapter | Low | Minimal | High |
| Fragility risk | Low | Low | High |
| Operator burden at intake | None | High | None |
| Consistency guarantee | Strong (structured data) | Weak (operator-provided) | Moderate (markdown parsing) |
| Changes to REQUIRED_INTAKE_FIELDS | No | Yes | No |
| Violates ADR-003 | No | No | Yes |
| Appropriate for v0.9 | Yes | No | No |

---

## Decision

**Option D — Extract from `skill_3_json["matched_capabilities"]`, with GCM Section 10 and ISO Section 8 extraction deferred to Phase B.**

1. `Skill5Adapter._capability_list()` reads `upstream["skill_3_json"]["matched_capabilities"]` after exhausting the `ca_inputs["capabilities"]` and `ca_inputs["capability_name"]` primary paths.
2. Generic fallback entries (`"Ethana Platform"`, `"Cursory advisory service"`) are excluded from the capability list before submission to the CVA executor.
3. Both Production and In Build / Roadmap entries are included. In Build entries produce `ecs: 0` and `escalation_required: true` in the CVA executor — this is the Claims Firewall functioning correctly, generating prohibited-claim documentation per AGENT.md §5.6.
4. Entries are deduplicated by `matched_capability` string before submission.
5. `proposed_claim` is constructed as: `f"Ethana {matched_capability} addresses the governance requirement: {requirement}"`
6. If the filtered, deduplicated list is empty after exclusions, `SkillAdapterError` is raised with a diagnostic message.
7. `ca_inputs["capabilities"]` explicit override remains the primary path, checked before upstream extraction.
8. A code comment documents the GCM/ISO deferral explicitly.

Option B is rejected: it inverts the architectural intent and creates a consistency risk invisible to downstream gate checks. Option C is rejected: markdown parsing in the adapter creates a silent coupling to executor output formats, violating ADR-003. Option A and Option D are identical in implementation; Option D is adopted because the explicit deferral documentation prevents future contributors from treating the partial coverage as an oversight.

---

## Consequences

**Positive:**
- Resolves Adapter Audit Mismatch M1. The CA chain can proceed past Skill 4 without operator-supplied capability fields on standard governance assessment intakes.
- `REQUIRED_INTAKE_FIELDS` does not change — existing CA intake specifications remain valid.
- `matched_capability` values originate from the same CPM that the CVA validates against, ensuring name-format consistency between extraction and validation.
- In Build capability entries flow to the CVA as documented, producing contradiction documentation in the assessment package.

**Negative:**
- Partial coverage of AGENT.md §5.6. Capabilities referenced in GCM Section 10 or ISO Section 8 that do not appear in Skill 3 `matched_capabilities` are not validated.
- If Skill 3 produces only generic fallback entries (no named capabilities matched), the CA run halts at `HALTED_ESCALATION` with a diagnostic error rather than proceeding with an empty capability list. This is correct behaviour but requires the error message to be informative.

---

## Deferred

- **GCM Section 10 capability extraction** — Phase B. Requires `execute_governance_control_mapping()` in the RWA runtime to produce a structured capability name list, not only embedded markdown text.
- **ISO 42001 Section 8 capability extraction** — Phase B. Requires the ISO executor to produce a structured Ethana coverage list alongside its markdown output.
- **Empty filtered list handling** — ensure the `SkillAdapterError` message specifies that `matched_capabilities` contained only generic fallback entries, not that the upstream skill failed.

---

## Related Decisions

- **ADR-001:** All capability names extracted by this decision must be matchable against `canonical-product-model.md`. The CPM is the ground truth for CVA validation.
- **ADR-003:** The adapter must remain a pure I/O transformer. Option C was rejected specifically because markdown parsing inside an adapter violates this principle.
- **ADR-008:** Resolves Gate 5c ECS threshold miscalibration, which is the second blocking failure on the Skill 5 boundary (M2). ADR-007 and ADR-008 must both be implemented before the CA end-to-end integration test can produce a `COMPLETE` run.
