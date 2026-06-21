# PR-010 Implementation Plan: Capability Discovery Repair

**Status:** Planned — blocks CA End-to-End Integration Test  
**Author:** Architecture  
**Date:** 2026-06-22 (revised 2026-06-22 — architecture review incorporated)  
**Predecessor:** PR-009 (`bf29292` — documentation, schema, and Skill-5 boundary repairs)  
**Authoritative inputs:** ADR-007, ADR-008, PR-009 audit, CA capability discovery investigation (2026-06-22), architecture challenge review (2026-06-22), refutation review (2026-06-22), Option A architectural challenge (2026-06-22)

> **Note on PR-009 PR-010 reference:** PR-009 anticipated a "PR-010" scoped to ESM fixture expansion (×3) and B-02/B-03 baselines. That scope is superseded here. The capability-discovery gap is a blocking architectural defect that must be resolved before fixture expansion or end-to-end integration testing. The prior PR-010 scope is reclassified to PR-011.

---

## 1. Problem Statement

PR-009 implemented ADR-007 (M1) correctly: `Skill5Adapter._capability_list()` now reads `skill_3_json["matched_capabilities"]` as the primary source of capabilities to validate. This is the right architecture.

The prerequisite assumption — that Skill 3 produces named CPM capabilities from standard governance assessment inputs — is false.

**On every real client intake with the current executors, the CA chain halts at `HALTED_ESCALATION` before Skill 5 executes.** Gate 5c is never reached. The ECS calibration fixed in ADR-008 addresses a gate that is architecturally unreachable from a real intake.

A CA run can only reach Skill 5 today by supplying `ca_inputs["capabilities"]` or `ca_inputs["capability_name"]` — the explicit targeted-override paths that ADR-007 explicitly ranked below the natural extraction path and that ADR-007 Option B rejected as inconsistent with the architecture.

The saved runs in `agents/client-assessment-agent/runtime/runs/` that contain `"Immutable Audit Log"` as a capability (e.g., `TR-CA-2026-8631_state.json`) all used `ca_inputs["capability_name"]` at intake. None reached Immutable Audit Log through Skill 3 extraction.

---

## 2. Evidence

### 2.1 Complete Skill 1 control name inventory

Full source scan of `agents/regulatory-watch-agent/runtime/skill_executor.py`, every `control_requirements.append()` call in `execute_regulatory_mapping()`:

| Control name | Trigger condition | Lines |
|---|---|---|
| `"Human Oversight Gate"` | `"EU" in jurs` | 162–168 |
| `"Drift Monitoring"` | `"EU" in jurs` | 169–175 |
| `"Fairness and Bias Monitoring"` | `"UK" in jurs` AND `is_bfsi` | 211–217 |
| `"Consent Verification"` | `"India" in jurs` AND `is_nbfc` | 262–268 |
| `"Vendor Risk Assessment"` | `"India" in jurs` AND `is_nbfc` | 269–275 |
| `"Prompt Injection Filter"` | `ai_technology == "LLM"` | 287–293 |

This is the complete set. No other `control_requirements.append()` calls exist in the file.

### 2.2 CPM key space

`parse_canonical_model()` (`evaluations/scripts/claims_linter.py:80`) applied to the live CPM produces 52 keys. The four target Production capabilities parse to:

| CPM key | Status |
|---|---|
| `"immutable audit log"` | production |
| `"llm gateway"` | production |
| `"runtime guardrails"` | production |
| `"mcp security broker"` | production |

### 2.3 Bidirectional substring match result

`_match_capability()` (`solution_mapping_executor.py:77–93`) tests `key in name_l or name_l in key` for each CPM key against each control name. Executed against the real CPM:

| Control name | CPM hits |
|---|---|
| `"Human Oversight Gate"` | **none** |
| `"Drift Monitoring"` | **none** |
| `"Fairness and Bias Monitoring"` | **none** |
| `"Consent Verification"` | **none** |
| `"Vendor Risk Assessment"` | **none** |
| `"Prompt Injection Filter"` | **none** |

Zero matches across all 6 controls against all 52 CPM keys. `_match_capability()` returns `(None, None)` for every Skill 1 control.

### 2.4 Skill 3 `matched_capabilities` output

`_score_requirement()` (`solution_mapping_executor.py:99–149`) with `(cap_display=None, status_norm=None)`:

| Control | `coverage_classification` (Skill 2) | `matched_capability` output |
|---|---|---|
| Human Oversight Gate | Fully Covered by Ethana | `"Ethana Platform"` |
| Drift Monitoring | Fully Covered by Ethana | `"Ethana Platform"` |
| Prompt Injection Filter | Fully Covered by Ethana | `"Ethana Platform"` |
| Fairness and Bias Monitoring | Fully Covered by Ethana | `"Ethana Platform"` |
| Consent Verification | Partially Covered by Ethana | `"Ethana Platform"` |
| Vendor Risk Assessment | Covered by Cursory Service | `"Cursory advisory service"` |

### 2.5 Skill 5 adapter filter result

`Skill5Adapter._capability_list()` (`skill_adapters.py:259–281`) excludes `"Ethana Platform"` and `"Cursory advisory service"` by name. After filtering the six rows above:

```
caps = []
```

The adapter raises `SkillAdapterError`. The orchestrator catches it at `_run_skill_5()` (`orchestrator.py:484–487`) and transitions to `HALTED_ESCALATION`. Skill 5 is never invoked.

### 2.6 Single write site for `matched_capabilities`

`matched_capabilities` is written at exactly one location: `solution_mapping_executor.py:244`. `Skill3Adapter.map_output` is a single-line `dict(raw)` pass-through (`skill_adapters.py:501`). `skill_3_json` is written at exactly one location: `orchestrator.py:386`. No other code path touches either field between Skill 3 execution and Skill 5 reading.

### 2.7 Scope of the gap relative to PR-009

PR-009 Stream B correctly implemented what ADR-007 specified: the Skill 5 adapter reads from Skill 3's output. PR-009 did not investigate whether Skill 3 would produce usable output from realistic intakes. That assumption was inherited from ADR-007's framing, which documented the fix (adapter wiring) but not the upstream condition (whether Skill 3 produces named capabilities at all). The gap predates PR-009; PR-009 made it observable via the improved error message at `skill_adapters.py:278`.

---

## 3. Root Cause

**Root cause:** Skill 2 (`execute_governance_control_mapping`, `agents/regulatory-watch-agent/runtime/skill_executor.py:327`) assigns a coverage classification per control (`"Fully Covered by Ethana"`, `"Partially Covered by Ethana"`, `"Covered by Cursory Service"`) but never names the specific Ethana CPM capability that provides that coverage. The coverage verdict reaches Skill 3 without a capability name.

**Consequence:** Skill 3's `_match_capability()` must reverse-engineer a CPM capability name from a regulatory control name using substring matching. The two vocabularies — regulatory control taxonomy (e.g., "Human Oversight Gate") and Ethana product taxonomy (e.g., "Immutable Audit Log") — have no substring overlap. The reverse-engineering is structurally impossible with the current algorithm.

**Contributing factor:** The two vocabularies cannot be bridged by algorithm. "Human Oversight Gate" is a regulatory concept derived from EU AI Act Art.14. "Immutable Audit Log" is an Ethana engineering capability. No mechanical string operation connects them. The bridge requires a knowledge judgment about which platform capability implements which regulatory control obligation. That judgment is not expressed anywhere in the current system.

**What ADR-007 fixed:** The wiring from Skill 3's output to Skill 5's input. ADR-007 correctly resolved M1.

**What ADR-007 did not fix:** Whether Skill 3's output contains anything usable. ADR-007's description (`skill_adapters.py:240`) states that `matched_capability` values "originate from `parse_canonical_model()`." This is true when `_match_capability` returns a hit. It is not true when it returns `(None, None)`, which is the universal result for all Skill 1 controls.

**Specification gap:** GCM SKILL.md (`skills/governance-control-mapping/SKILL.md:130`) Section 10 specifies exactly this capability-attribution function:
> *"Specific configuration instructions mapping designed technical controls directly to Ethana capabilities… Production Mappings: Configurations utilizing verified, active Production features… (e.g., LLM Gateway routing fallbacks, Runtime Guardrails PII filters, Immutable Audit Log configurations)."*

Section 10 is unimplemented in the current GCM executor. The specification was written correctly; the executor was not.

---

## 4. Why the Mapping is Knowledge, Not Code

The central design decision in this PR is that the control-to-capability attribution must be expressed as a knowledge artifact, not as a hardcoded mapping table in an executor.

**The attribution is a compliance judgment.** The statement "Human Oversight Gate is addressed by the Immutable Audit Log" is a determination that requires understanding both EU AI Act Art.14's audit trail obligations and the Ethana Audit Log's engineering capabilities. It is not derivable from string operations. It requires a maintainer who holds both knowledge domains simultaneously. That maintainer is a compliance expert — not an engineer writing Python.

**Code has the wrong ownership model.** A hardcoded dict inside `execute_governance_control_mapping()` is owned and reviewed by engineering. It cannot be updated without a code change, a test run, and a merge. A compliance expert who identifies a mapping error — or who needs to add a new regulatory obligation's mapping when a new jurisdiction is implemented — must file an engineering ticket rather than updating the knowledge base directly. This is the same mismatch that the CPM was created to resolve for capability status.

**Code is undiscoverable.** A mapping dict in the RWA executor is invisible to:
- Any other skill that needs the same mapping (ESM, GRA, future agents)
- The compliance team auditing whether the system's regulatory claims are supported
- Automated tests that need to verify mapping correctness independently of the executor
- The PR-010 reviewer who must verify each mapping against CPM primary source notes

**Code creates silent cross-layer coupling.** If the mapping lives in the RWA executor, any other agent that needs it must import the RWA executor — creating a dependency between agents that should be architecturally independent. If instead each agent hardcodes its own copy of the mapping, the copies diverge.

**Knowledge files are independently auditable and testable.** A markdown table can be:
- Reviewed by a compliance expert without Python knowledge
- Loaded and validated against the CPM at test time as a standalone assertion
- Updated when Ethana ships a new capability that better serves a regulatory obligation
- Versioned alongside the CPM so the mapping's commit history is traceable

The CPM itself demonstrates the correct pattern: engineering status information that was previously scattered across playbooks and verbal product claims was consolidated into a single, authoritative, machine-parseable markdown file. The control-to-capability mapping repeats that consolidation for a different domain of compliance knowledge.

---

## 5. Architectural Options

### Option A (original) — Hardcoded mapping table in Skill 2 executor

**Description:** `execute_governance_control_mapping()` adds a `suggested_capability` field using a hardcoded dict inside the executor, keyed on control name.

**Verdict: Superseded by Option D.** The layer assignment (Skill 2) is correct. The implementation mechanism (hardcoded dict in code) is wrong. Option D implements the same layer assignment with the correct mechanism.

---

### Option B — Semantic translation table in Skill 3 executor

**Description:** `_match_capability()` in `solution_mapping_executor.py` checks an internal dict mapping control names to CPM keys before the substring loop.

**Verdict: Rejected.** Places a compliance judgment (which Ethana capability implements a regulatory control) inside a commercial scoring executor. The coupling is invisible in code. Any new Skill 1 control type requires a change to Skill 3 code, which is removed from both the Skill 1 source and the compliance knowledge domain. Also violates ADR-003: taxonomy translation is not an I/O transformation.

---

### Option C — Skill 1 generates CPM capability names

**Description:** Skill 1 replaces regulatory-vocabulary control names with CPM product names directly in `control_requirements`.

**Verdict: Rejected unconditionally.** Skill 1's output is a regulatory-mapping artifact. A control named "Immutable Audit Log" is a product claim, not a regulatory control requirement. This inverts the model the entire chain is built on and creates Claims Firewall risk in downstream skill outputs.

---

### Option D — Shared knowledge artifact: `knowledge/ethana/control-capability-map.md` (recommended)

**Description:** A new knowledge file at `knowledge/ethana/control-capability-map.md` expresses the authoritative mapping from regulatory control names to CPM capability keys. A minimal loader function reads the file and returns a lookup dict. Skill 2 loads the map and populates `suggested_capability` per control. Skill 3 reads `suggested_capability` from the control dict rather than attempting substring matching. Future agents load the same file directly.

**Why this is architecturally correct:**
- The mapping is compliance knowledge. It belongs in the knowledge directory alongside the CPM, under compliance team ownership.
- The layer assignment remains at Skill 2 (GCM), consistent with GCM SKILL.md Section 10's specification.
- Skill 3's role remains capability scoring, not vocabulary translation.
- Other agents and skills consume the same knowledge artifact without depending on each other's executors.
- The file is independently auditable against CPM primary source notes.
- Updates require no code change: a new jurisdiction or regulatory obligation requires one new row in the table.

**Relationship to Option A:** Option D implements the same architectural judgment as Option A (Skill 2 is the correct layer). It replaces only the implementation mechanism — knowledge file instead of hardcoded dict.

---

### Option E — CPM regulatory control annotations

**Description:** Add a "Regulatory Control Tags" column to each CPM capability row. `parse_canonical_model()` returns the tags alongside status. Skill 3 looks up capabilities by tag.

**Verdict: Rejected.** The CPM's authority derives from its narrow scope: engineering-evidence-grounded facts about what Ethana has built. Its primary sources (Board Briefing, Study Ethana) do not cover regulatory compliance taxonomy. Adding regulatory control tags to the CPM mixes two concerns with different maintainers, different authority sources, and different change cadences. The CPM's authority model depends on its scope remaining narrow.

---

## 6. Recommended Approach: Option D

### 6.1 Overview

Introduce `knowledge/ethana/control-capability-map.md` as the authoritative knowledge source for the regulatory-control-to-Ethana-capability attribution. Implement a minimal loader function. Wire Skill 2 to load the map and populate `suggested_capability` per control. Wire Skill 3 to read `suggested_capability` before falling back to substring matching. This is Phase A.

Phase B extends the map to support primary/secondary capability relationships and multi-capability mappings, enabling richer coverage analysis without structural changes to Phase A's data flow.

### 6.2 Knowledge file: `knowledge/ethana/control-capability-map.md`

**Placement rationale:** The file belongs in `knowledge/ethana/` alongside `canonical-product-model.md`. Both files express knowledge about the relationship between Ethana's capabilities and the compliance domain. The CPM answers "what is the status of this capability?" The control-capability map answers "which capability implements this regulatory control?" They are complementary knowledge artifacts with the same authority model: compliance team maintained, primary-source grounded, machine-parseable.

**Phase A format:**

```markdown
# Ethana Control-to-Capability Map

**Authority:** Authoritative source for regulatory control-to-Ethana-capability attribution.
**Maintained by:** Cursory Governance Team
**Synchronized with:** knowledge/ethana/canonical-product-model.md
**CPM key format:** Lowercase base name as returned by parse_canonical_model()
**Control name contract:** The `Control Name` column is a shared string contract with
  `execute_regulatory_mapping()` in the RWA executor. Values must match Skill 1 output
  exactly (modulo case). Any change to Skill 1 control name literals requires a simultaneous
  update to this file. T6(e) enforces this contract in CI.

---

## Format Notes

- `Primary Capability`: The CPM key of the Ethana capability that is the primary implementation
  of this regulatory control. Must match a key returned by parse_canonical_model() exactly.
  Empty string if no Ethana capability is the primary implementation.
- `Phase B: Secondary Capabilities`: Comma-separated CPM keys for supporting capabilities.
  Pre-populate with full knowledge on Day 1. The Phase A loader reads this column but does not
  consume it — the loader always returns `"secondary": []` regardless of column content in Phase A.
  Complete knowledge belongs in the file from the start; which columns the code consumes is a code
  concern, not a knowledge concern.
- `Notes`: Compliance rationale. Must reference CPM primary source notes where relevant.

---

## Control-to-Capability Mappings

| Control Name | Framework Reference | Primary Capability | Phase B: Secondary Capabilities | Notes |
|---|---|---|---|---|
| Human Oversight Gate | EU AI Act Art.14 | immutable audit log | | Audit Log provides the tamper-proof record for every human-override decision on AI output. CPM: "Every [BB] production scenario references it." |
| Drift Monitoring | EU AI Act Art.72; ISO 42001 Annex A.9 | immutable audit log | | Gateway telemetry (logged to Audit Log) is the primary detection source for performance drift. Alerting thresholds are customer-configured against the log export. |
| Fairness and Bias Monitoring | FCA PRIN 12; Equality Act 2010 | runtime guardrails | immutable audit log | Guardrails bias scanner is the primary detection mechanism. CPM mandatory caveat: runtime text filter only; does not audit model weights or test disparate impact across demographic groups. EU AI Act Art.10 bias audit obligations cannot be met by this scanner alone. |
| Prompt Injection Filter | OWASP LLM01; NIST AI RMF | runtime guardrails | | Guardrails prompt injection and jailbreak detection scanners are the primary prevention mechanism. CPM: "One of six confirmed native scanners." |
| Consent Verification | DPDP Act 2023 §6 | | | No primary Ethana capability. Customer-owned control; consent database is customer infrastructure. Cursory advisory service for consent architecture design. |
| Vendor Risk Assessment | RBI IT Governance MD 2023 | | | No primary Ethana capability. Customer-owned process control. Cursory advisory service for supply-chain risk assessment. |
```

**Format rules enforced by the loader (Phase A):**
1. The header row and separator row are skipped.
2. Column 1 (`Control Name`) is the lookup key — lowercased on read.
3. Column 3 (`Primary Capability`) must be a CPM key exactly as `parse_canonical_model()` produces it (lowercase, pre-em-dash base name), or an empty string.
4. Column 4 (`Phase B: Secondary Capabilities`) is read but not consumed in Phase A.
5. Empty `Primary Capability` is a valid result — it signals no Ethana capability implements this control. The loader returns `""` and the executor handles it by leaving `suggested_capability` empty.

### 6.3 Loader function

A minimal loader function is added to `evaluations/scripts/claims_linter.py` alongside `parse_canonical_model()`. It follows the same pattern: reads a markdown table, returns a dict.

```python
def load_control_capability_map(map_path: Path) -> dict:
    """
    Parse control-capability-map.md into a lookup dict.

    Returns:
        {control_name_lower: {"primary": "cpm-key-or-empty", "secondary": []}}

    Phase A: only "primary" is populated. "secondary" is always [].
    Phase B: "secondary" is populated from column 4.
    """
```

The loader is placed in `claims_linter.py` for the same reason `parse_canonical_model()` lives there: it is a knowledge-file parser that must be importable by any executor without creating cross-agent dependencies. Both loaders share the same import path.

### 6.4 Data flow: Phase A

```
CA Intake (jurisdiction, industry, ai_portfolio)
│
▼
Skill 1 — regulatory-mapping (RWA executor)
  Produces: control_requirements = [
    {"control_name": "Human Oversight Gate", ...},
    {"control_name": "Drift Monitoring", ...},
    ...
  ]
│
▼
Skill 2 — governance-control-mapping (RWA executor)
  Loads: control-capability-map.md via load_control_capability_map()
  Per control: looks up control_name → primary CPM key
  Produces: control_taxonomy_matrix = [
    {
      "control_name": "Human Oversight Gate",
      "coverage_classification": "Fully Covered by Ethana",
      "suggested_capability": "immutable audit log",   ← NEW
      ...
    },
    ...
  ]
│
▼
Skill2Adapter.map_output()
  Propagates suggested_capability through to skill_2_json["controls"]
│
▼
Skill 3 — ethana-solution-mapping (CA-local executor)
  Per control: reads control.get("suggested_capability")
    IF non-empty:
      self._load_cpm().get(suggested_capability)
        → direct dict access: {"original_name": "Immutable Audit Log", "status": "production"}
        → matched_capability = entry["original_name"]   ← NAMED CPM CAPABILITY
    ELSE:
      _match_capability(requirement)   ← existing substring fallback (unchanged)
  Produces: matched_capabilities = [
    {"matched_capability": "Immutable Audit Log", "capability_status": "Production", ...},
    {"matched_capability": "Runtime Guardrails", "capability_status": "Production", ...},
    ...
  ]
│
▼
Skill5Adapter._capability_list()
  Filters: excludes "Ethana Platform", "Cursory advisory service"
  Returns: [
    {"capability_name": "Immutable Audit Log", "proposed_claim": "..."},
    {"capability_name": "Runtime Guardrails", "proposed_claim": "..."},
  ]
│
▼
Skill 5 — ethana-capability-validation (CVA executor)
  Immutable Audit Log → ECS 95 → passes Gate 5c (threshold 90)
│
▼
GATE_5_PASSED → Skill FM → Skill 6 → COMPLETE
```

**Before PR-010 (broken path):**
```
Skill 2 → skill_2_json["controls"][*].suggested_capability = (missing)
Skill 3 → _match_capability("Human Oversight Gate") = (None, None)
        → matched_capability = "Ethana Platform"
Skill5Adapter → filters all entries → caps = [] → SkillAdapterError → HALTED_ESCALATION
```

### 6.5 How each consumer uses the knowledge artifact

**Skill 2 (GCM executor — `agents/regulatory-watch-agent/runtime/skill_executor.py`):**

Loads the map at executor initialisation (same pattern as `_load_cpm()` in Skill 3). For each control being appended to `control_taxonomy_matrix`, looks up `control_name.lower()` in the map and populates `suggested_capability` from the primary key. If the map returns an empty string, `suggested_capability` is set to `""` and no override occurs in Skill 3. The map is loaded once and cached — the same pattern the CPM uses.

GCM is the correct layer for this lookup. GCM SKILL.md Section 10 specifies "configuration instructions mapping designed technical controls directly to Ethana capabilities." Populating `suggested_capability` is the structured-data implementation of that specification.

**Skill 3 (ESM executor — `agents/client-assessment-agent/runtime/skills/solution_mapping_executor.py`):**

`_score_requirement()` reads `control.get("suggested_capability", "")` before the existing CPM lookup path. When `suggested_capability` is non-empty, `_score_requirement()` calls `self._load_cpm().get(suggested_capability)` directly — bypassing `_match_capability()` entirely for the known-CPM-key path. This is a direct dict access on the parsed CPM dict, keyed by lowercase base name. It is deterministic and collision-free: it returns exactly the entry for the given CPM key regardless of how many other keys are added to the CPM in future. It does not use substring matching.

When `suggested_capability` is empty, `_match_capability(requirement)` is called as before. `_match_capability()` itself is not modified.

The `requirement` variable used for the `"requirement"` key in the output dict (the human-readable control name, e.g. `"Human Oversight Gate"`) is unchanged — only the CPM lookup input changes. The output dict's `"requirement"` field always reflects `control.get("name")`, not the CPM key in `suggested_capability`.

All downstream logic (capability_status, ccs_score, matched_capability, disposition) is unchanged.

Skill 3 does NOT independently load the map in Phase A. It reads only what Skill 2 has propagated. This keeps Phase A minimal and maintains the chain dependency (Skill 3 depends on Skill 2's output, as it does today). Phase B can optionally add an independent map load as a semantic fallback for contexts where Skill 2 has not been called.

**Future agents (GRA, regulatory-change-impact, others):**

Any agent that needs to answer "which Ethana capabilities are implicated by this regulatory control?" calls `load_control_capability_map()` directly, without depending on any other agent's executor. The loader is in `claims_linter.py`, importable by all runtimes. The knowledge artifact is a stable file in the knowledge directory.

Example use cases that become possible after Phase A:

- **Governance Review Agent:** Given a new regulatory obligation (from a regulatory-change alert), look up which capabilities are mapped to it and trigger re-validation of those capabilities in the CVA.
- **Regulatory-change-impact agent:** Given that DPDP Act Section 6 has been amended, find all controls that reference it in the map and identify which CA runs need reassessment.
- **CA Mode B (incremental re-assessment):** Load the map to identify which controls have changed capability attribution since the prior run.

None of these use cases require importing the RWA executor. The knowledge artifact is the shared layer, not the executor.

---

## 7. Phase Boundaries

### Phase A — v0.9 (this PR)

**Scope:** Minimum changes to unblock T3 (CA end-to-end integration test without intake override).

| Deliverable | Description |
|---|---|
| `knowledge/ethana/control-capability-map.md` | Knowledge file — all 6 controls, primary and secondary capabilities fully populated; Phase A loader ignores secondary column |
| `load_control_capability_map()` in `claims_linter.py` | Minimal loader — returns `{control_name_lower: {"primary": str, "secondary": []}}` |
| Skill 2 loads the map | `execute_governance_control_mapping()` loads map, populates `suggested_capability` per control |
| `Skill2Adapter` propagates field | `map_output()` passes `suggested_capability` through to `skill_2_json["controls"]` |
| Skill 3 reads `suggested_capability` | `_score_requirement()` prefers `suggested_capability` over substring match when non-empty |

**Phase A constraints:**
- `suggested_capability` is typed as `str` (single primary CPM key or empty string)
- Loader returns primary only; secondary list is always `[]` in Phase A
- Skill 3 does not independently load the map
- Map covers all 6 current Skill 1 control names; 4 have primary CPM keys, 2 are empty

### Phase B — v1

**Scope:** Richer relationship model, multi-capability mappings, independent Skill 3 load.

| Deliverable | Description |
|---|---|
| `suggested_capability` → `suggested_capabilities: list[str]` | Rename field; type widens to list; Phase A callers updated to read `[0]` for primary |
| Populate `Phase B: Secondary Capabilities` column | Add secondary CPM keys to map entries where multiple capabilities are relevant |
| Skill 3 independent map load | `_match_capability()` loads map directly as a semantic fallback when `suggested_capability` is absent — supports non-CA call paths |
| Confidence weights | Optional: map encodes primary/secondary distinction with relative weight for multi-capability CCS scoring |
| GCM Section 10 full implementation | Full structured Ethana Configuration Guide output per control, not just `suggested_capability` |
| GCM Section 10 / ISO Section 8 capability extraction | ADR-007 Phase B deferral; enables Skill 5 to receive capabilities from all three upstream sources |

**Phase B is not in scope for this PR.** The Phase A field name (`suggested_capability: str`) is intentionally singular and typed conservatively to keep Phase A minimal. The Phase B rename is a breaking change to the `skill_2_json["controls"]` schema and requires a coordinated update of Skill2Adapter, Skill 3, and any test that asserts on the field type.

---

## 8. Architecture Review Response

This section records the recommendations from the Option A architectural challenge (2026-06-22) and their disposition.

### Accepted

**Mapping belongs in a knowledge file, not in executor code.**
The challenge correctly identified that a hardcoded dict in `execute_governance_control_mapping()` has wrong ownership, wrong discoverability, and wrong maintenance characteristics. Option D replaces it with `control-capability-map.md`. The layer assignment (Skill 2 owns capability attribution, per GCM SKILL.md Section 10) is unchanged; only the implementation mechanism changes.

**CPM demonstrates the correct pattern.**
The challenge noted that the CPM itself was created to consolidate scattered capability status knowledge into a single authoritative, machine-parseable file. The control-capability map repeats that consolidation for a different knowledge domain. This is accepted as the explicit design rationale (Section 4 of this document).

**`suggested_capability` as `list[str]` for Phase B compatibility.**
The challenge recommended typing the field as `list[str]` from the start, defaulting to a single-element list in Phase A. This is partially accepted: the knowledge file includes the `Phase B: Secondary Capabilities` column from the start, making the format Phase-B-ready without schema changes to the file. However, `suggested_capability` remains `str` in Phase A code to minimize blast radius. The Phase B widening is explicitly documented as a known breaking change. The field name is also documented as subject to rename in Phase B.

**Future-agent consumption without executor dependency.**
The challenge noted that a hardcoded mapping in the RWA executor creates coupling risk for future agents. Accepted: `load_control_capability_map()` is placed in `claims_linter.py`, which all runtimes can import without importing each other.

### Rejected

**Option E — CPM regulatory control annotations.**
Rejected. The CPM's authority derives from its narrow engineering-evidence scope. Mixing regulatory control taxonomy into it violates the source authority model. The two files have different maintainers, different primary sources, and different change cadences. They must remain separate.

**Option B — Semantic translation table in Skill 3.**
Rejected, consistent with the original PR-010 assessment and with ADR-003. The challenge confirmed that Skill 3's role is CCS scoring, not vocabulary translation. The map belongs upstream, not in the scoring layer.

**Option C — Skill 1 generates CPM names.**
Rejected unconditionally for the same reason as in the original PR-010.

### Preserved from original PR-010

**Skill 2 owns capability attribution.**
GCM SKILL.md Section 10 specifies that GCM maps controls to Ethana capabilities. This assignment is correct and is preserved in Option D. The knowledge file is the source; Skill 2 is the executor that reads it and propagates the result.

**Option B acceptable as v0.9 fallback.**
The original PR-010 stated that Option B was acceptable if Option A's scope was judged too broad. This fallback is removed in the revised document. Option D is not materially more complex than the original Option A and is architecturally sounder. There is no reason to accept Option B's wrong-layer coupling when Option D is available at equivalent scope.

---

## 9. Risks

### Risk 1 — RWA executor is shared

`execute_governance_control_mapping()` is used by both the CA chain (via `Skill2Adapter`) and the standalone RWA chain (via `agents/regulatory-watch-agent/runtime/orchestrator.py:401`). The `suggested_capability` field must be additive — existing callers that do not read the new field are unaffected.

**Mitigation:** Verify that `compile_control_mapping_to_markdown()` (`skill_executor.py:~530`) does not iterate over `control_taxonomy_matrix` row keys in a way that would break on an unexpected field. Grep for all consumers of `control_taxonomy_matrix` before implementing. Run T5 (34 existing RWA tests) to confirm no regression.

### Risk 2 — Mapping correctness

An incorrect primary-capability mapping (e.g., mapping "Drift Monitoring" to "governance policy engine" instead of "immutable audit log") produces a wrong CPM key in `suggested_capability`. Skill 3 would pass the wrong key to the CPM lookup, producing a named capability that doesn't actually implement the regulatory control. The CVA would validate that capability and produce a passing ECS — but the capability validated is not the one relevant to the control. This is a semantic correctness risk, not a structural failure.

**Mitigation:** Every `Primary Capability` entry in `control-capability-map.md` must be reviewed against the CPM notes column before merging. The CPM notes for Immutable Audit Log explicitly state "Every [BB] production scenario references it" and "Ethana's strongest and most consistent enterprise claim across all use cases" — confirming it as the lead capability for audit-trail controls. The review must be documented in the PR commit message. The loader validates that each primary key exists in the CPM at load time and logs a warning if not.

### Risk 3 — Test blast radius

Introducing `suggested_capability` changes the data flowing from Skill 2 into Skill 3. Existing Skill 3 tests that use hardcoded control dicts without `suggested_capability` remain valid (the field is read with `dict.get()`, defaulting to `""`). However, any test asserting that a specific control name produces `"Ethana Platform"` as `matched_capability` will now produce a named CPM capability when the map entry is populated.

**Mitigation:** Run the Skill 3 test suite (`test_client_assessment_skill3.py`, 18 tests) after implementing and update assertions for controls that now resolve to named capabilities. Document which assertions changed and what the new expected values are in the PR.

### Risk 4 — Loader availability at runtime

`load_control_capability_map()` in `claims_linter.py` must be importable from the RWA executor and from the ESM executor. Both already import from `evaluations/scripts/`. Confirm the import path is consistent with how `parse_canonical_model()` is imported in `solution_mapping_executor.py:70`.

**Mitigation:** Add a unit test that imports `load_control_capability_map` from `claims_linter` in both the RWA and CA test suites to confirm import availability before the full test run.

### Risk 5 — Map file not found at runtime

If `control-capability-map.md` is not found at the path the loader expects, the loader must fail gracefully. A missing map must not halt a CA run — it must fall back to the existing substring-matching behavior (which produces generic fallbacks, the current behavior). This preserves the pre-PR-010 failure mode rather than introducing a new one.

**Mitigation:** Loader returns an empty dict if the file is not found. Skill 2 sets `suggested_capability: ""` for all controls. Skill 3 falls back to substring matching. A warning is logged. A test verifies this fallback path explicitly (T6).

### Risk 6 — E2E test still uses override path until this lands

Until PR-010 is merged, any CA "end-to-end" test claiming a `COMPLETE` run must use `ca_inputs["capabilities"]`. Those tests must be labeled "Gate 5c integration test" or "targeted validation test" in their docstrings, not "end-to-end test," to prevent false confidence in the master status report.

### Risk 7 — Skill 1 / knowledge file control-name covenant

The knowledge file is indexed on `Control Name` lowercased. Skill 2 performs the lookup using `control_name.lower()` from Skill 1's output. The entire attribution path depends on Skill 1 emitting control names that exactly match the knowledge file's `Control Name` column (modulo case).

If Skill 1 ever changes any control name — even a minor change such as `"Human Oversight Gate"` → `"Human Oversight Control"` — the knowledge file lookup returns `None`. Skill 2 sets `suggested_capability: ""`. Skill 3 falls back to `_match_capability(requirement)`, which returns `(None, None)` for all current Skill 1 controls. `matched_capabilities` contains only generic fallbacks. Skill5Adapter raises `SkillAdapterError`. The run reaches `HALTED_ESCALATION`. No error is raised at the lookup failure point — the failure is silent and indistinguishable at the symptom level from a missing map file (Risk 5).

This covenant is not enforced by any existing test or CI check. The risk materialises when: (a) a new jurisdiction is added and Skill 1 emits new control names not yet in the map; (b) a compliance terminology update changes an existing control name string; (c) a Skill 1 refactor renames control name literals.

**Mitigation:** The `Control Name` column in `control-capability-map.md` is a shared string contract between `execute_regulatory_mapping()` and the knowledge file. This must be stated in the knowledge file's preamble. Any change to Skill 1 control name output strings requires a simultaneous update to the knowledge file. T6(e) (covenant validation — see Section 11) enforces this at CI time.

---

## 10. Files Affected

| # | File | Change | Reason | Phase |
|---|---|---|---|---|
| 1 | `knowledge/ethana/control-capability-map.md` | **Create** — knowledge file with mapping table, all 6 Skill 1 controls; primary and secondary capabilities fully populated; control-name contract preamble included | Root cause fix — authoritative knowledge source | A |
| 2 | `evaluations/scripts/claims_linter.py` | Edit — add `load_control_capability_map(path)` loader alongside `parse_canonical_model()` | Shared loader importable by all executors | A |
| 3 | `agents/regulatory-watch-agent/runtime/skill_executor.py` | Edit — `execute_governance_control_mapping()` loads the map, populates `suggested_capability` per control in `control_taxonomy_matrix` | Skill 2 emits capability attribution | A |
| 4 | `agents/client-assessment-agent/runtime/skill_adapters.py` | Edit — `Skill2Adapter.map_output()` (lines 205–214): propagate `suggested_capability` from `control_taxonomy_matrix` into `skill_2_json["controls"]` | Adapter passes new field through | A |
| 5 | `agents/client-assessment-agent/runtime/skills/solution_mapping_executor.py` | Edit — `_score_requirement()` (line 102): read `suggested_capability`; when non-empty call `self._load_cpm().get(suggested_capability)` directly (bypasses `_match_capability`); when empty fall through to existing `_match_capability(requirement)` path; `_match_capability()` itself is not modified; `"requirement"` output field is unchanged | Skill 3 consumes capability attribution | A |
| 6 | `evaluations/scripts/test_client_assessment_skill3.py` | Edit — update assertions for controls that now resolve to named CPM capabilities; add T1, T2 | Test consistency | A |
| 7 | `evaluations/scripts/test_client_assessment_runtime.py` | Edit/add — T3 (natural extraction path, no intake override) | End-to-end path | A |
| 8 | `evaluations/scripts/test_claims_linter.py` (or new) | Edit/add — T6 (loader unit tests: happy path, missing file fallback, invalid key warning) | Loader correctness | A |
| 9 | `reviews/governance-os-master-status.md` | Edit — record capability-discovery gap resolved, PR-010 complete, T3 available | Status hygiene | A |

**Explicitly not in scope for PR-010:**
- `suggested_capability` → `suggested_capabilities: list[str]` rename — Phase B
- Secondary capability code consumption (file is pre-populated; code ignores it until Phase B)
- Independent Skill 3 map load — Phase B
- GCM Section 10 full structured output — Phase B
- GCM Section 10 / ISO Section 8 capability extraction (ADR-007 Phase B deferral) — Phase B
- MCP Security Broker ECS path (ECS 75, below Gate 5c threshold 90) — Phase B
- General fallback Production path recalibration (ADR-009) — Phase B
- ESM fixture expansion and B-02/B-03 baselines — PR-011

---

## 11. Test Strategy

### T1 — Unit: `_score_requirement` with `suggested_capability` set

**File:** `test_client_assessment_skill3.py`  
**What:** Construct a control dict with `suggested_capability="immutable audit log"` and `coverage_classification="Fully Covered by Ethana"`. Assert that `matched_capability` in the output equals `"Immutable Audit Log"` (CPM `original_name`) and `capability_status` equals `"Production"`.  
**Why:** Confirms the new field is read and routes to the CPM lookup correctly, bypassing the substring match.

### T2 — Unit: `_score_requirement` without `suggested_capability` (regression)

**File:** `test_client_assessment_skill3.py`  
**What:** Existing tests with control dicts that lack `suggested_capability`. Assert behavior is identical to pre-PR-010 — substring match returns `(None, None)`, producing `"Ethana Platform"` for Ethana-covered controls.  
**Why:** Confirms the change is additive and non-breaking for callers that do not supply `suggested_capability`.

### T3 — Integration: natural extraction path, no intake override

**File:** `test_client_assessment_runtime.py`  
**What:** Construct a CA intake for EU BFSI: `jurisdictions=["EU"]`, `industry="BFSI"`, `client_ai_portfolio` containing an LLM description. Call `orchestrator.start_run()` and drive through approval gates. Assert: (a) the run reaches at least `GATE_5_PASSED`; (b) `skill_3_json["matched_capabilities"]` contains at least one entry where `matched_capability` is `"Immutable Audit Log"` (not `"Ethana Platform"`); (c) no `ca_inputs["capabilities"]` or `ca_inputs["capability_name"]` is supplied.  
**Why:** This is the test that proves the natural extraction path works end-to-end. It is the definition of a genuine CA integration test. It did not exist before PR-010.  
**Prerequisite:** ADR-008 +10 ECS increment (implemented in PR-009 B2).

### T4 — Assertion updates: controls that now resolve to named capabilities

**File:** `test_client_assessment_skill3.py`  
**What:** For each control whose map entry has a non-empty `Primary Capability`, update the existing assertion that expected `"Ethana Platform"` to assert the new named CPM capability. Document the expected value and the CPM key it derives from.  
**Why:** Prevents pre-existing tests from failing after Skill 2 starts populating `suggested_capability`.

### T5 — RWA regression: Skill 2 output in standalone chain

**File:** `test_regulatory_watch_runtime.py` (existing, 34 tests)  
**What:** Run the existing RWA test suite without modification. Assert all 34 tests pass.  
**Why:** The RWA standalone chain uses `execute_governance_control_mapping()`. The new `suggested_capability` field must not break the standalone chain, which does not consume the field.

### T6 — Loader unit tests and covenant validation

**File:** `test_claims_linter.py` (existing or new)  
**What:**  
  (a) Happy path: load `control-capability-map.md` and assert `"human oversight gate"` maps to primary `"immutable audit log"`. Assert secondary is `[]` (Phase A loader ignores populated secondary column).  
  (b) Missing file: loader receives a non-existent path; asserts it returns an empty dict and does not raise.  
  (c) Unknown key: call with a control name not in the map; assert the loader returns `{"primary": "", "secondary": []}` rather than raising.  
  (d) Invalid CPM key warning: if `Primary Capability` value is not in the parsed CPM, assert a warning is emitted (logged, not raised).  
  (e) Covenant validation: load `control-capability-map.md` and extract all `Control Name` values (lowercased). Separately, enumerate all control names that `execute_regulatory_mapping()` can produce across all jurisdiction/industry/AI-technology combinations (EU, UK, India, BFSI, NBFC, LLM — derived from the complete set in Section 2.1). Assert (i) every control name in the knowledge file appears in the Skill 1 production set — detects orphaned map entries; (ii) every Skill 1 control name has a corresponding map entry — detects capability attribution gaps when Skill 1 adds new controls. This test runs in CI as a static consistency check and raises on failure.  
**Why:** Sub-cases (a)–(d) verify loader correctness and graceful degradation. Sub-case (e) enforces the Skill 1 / knowledge file control-name covenant (Risk 7) at build time, converting a silent runtime regression risk into a CI-detectable contract violation.

---

## 12. Definition of Done

PR-010 is complete when all of the following are true:

1. **`control-capability-map.md` exists, is reviewed, and is fully populated.** The file is present at `knowledge/ethana/control-capability-map.md`. All 6 Skill 1 control names have entries. Each `Primary Capability` value has been reviewed against the CPM notes column and confirmed as the correct implementation capability. Two entries have empty primary (Consent Verification, Vendor Risk Assessment) — this is correct and deliberate. The `Phase B: Secondary Capabilities` column is populated with full knowledge for all applicable entries. The control-name contract preamble is present.

2. **`load_control_capability_map()` is implemented and tested.** The loader is in `claims_linter.py`. T6 (five sub-cases: happy path, missing file, unknown key, invalid CPM key warning, covenant validation) passes. T6(e) confirms that the Skill 1 control name set and the knowledge file `Control Name` column are in bijective correspondence.

3. **Skill 2 emits `suggested_capability`.** `execute_governance_control_mapping()` loads the map and populates `suggested_capability` on every `control_taxonomy_matrix` row. Verified by inspecting a sample run's `skill_2_json`.

4. **`Skill2Adapter` propagates the field.** `skill_2_json["controls"]` contains `suggested_capability` on every control dict. Verified by a unit assertion on the adapter output shape.

5. **Skill 3 consumes `suggested_capability`.** `_score_requirement()` reads `suggested_capability` before the CPM lookup. When non-empty, `self._load_cpm().get(suggested_capability)` is called directly — no substring matching. When empty, `_match_capability(requirement)` applies unchanged. `_match_capability()` itself is not modified.

6. **T3 passes without any intake override.** A CA run from a real EU BFSI intake (no `ca_inputs["capabilities"]`, no `ca_inputs["capability_name"]`) reaches `GATE_5_PASSED`. The run's `skill_3_json["matched_capabilities"]` contains at least one entry where `matched_capability` equals `"Immutable Audit Log"`.

7. **T5 passes unmodified.** All 34 existing RWA runtime tests pass without changes to test code.

8. **T1, T2, T4, T6 pass.** New and updated tests pass.

9. **No intake-override dependency in E2E tests.** Any CA test labeled "end-to-end" in `test_client_assessment_runtime.py` does not supply `ca_inputs["capabilities"]` or `ca_inputs["capability_name"]`. Tests that use those override paths are labeled "Gate 5c integration test" or "targeted validation test" in their docstrings.

10. **Master status updated.** `reviews/governance-os-master-status.md` records PR-010 as complete, the capability-discovery gap as resolved, and the CA end-to-end integration test (T3) as available.

---

## Related Decisions

- **ADR-001:** CPM is the authoritative source for all capability status lookups. `control-capability-map.md` references CPM keys exactly as `parse_canonical_model()` produces them. The map does not duplicate CPM status information — it references CPM keys.
- **ADR-003:** Adapters are pure I/O transformers. Option B (semantic translation in Skill 3) was rejected for this reason. Option D preserves the adapter's role: `Skill2Adapter.map_output()` propagates `suggested_capability` without interpreting it.
- **ADR-007:** Resolved M1 (Skill 5 input source). PR-010 resolves the upstream condition ADR-007 assumed: that Skill 3 produces named CPM capabilities from standard intakes.
- **ADR-008:** Resolved M2 (Gate 5c ECS calibration). ADR-008's fix is correct and necessary but addresses a gate that remains unreachable without PR-010.
- **PR-009:** Implemented ADR-007 and ADR-008. PR-010 is the successor that closes the remaining gap in the natural execution path. PR-009 + PR-010 together complete the prerequisites for T3.
- **ADR-009:** General fallback ECS recalibration — Phase B. Not affected by PR-010.
