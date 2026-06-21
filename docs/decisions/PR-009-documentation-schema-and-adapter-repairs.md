# PR-009 Implementation Plan: Documentation, Schema, and Skill-5 Boundary Repairs

**Status:** Planned (not implemented)
**Author:** Architecture
**Date:** 2026-06-21
**Predecessor:** PR-008 (RWA L4 Certification, tagged `v0.8.1-pr008-complete`)
**Authoritative inputs:** ADR-007, ADR-008, ADR-009, `reviews/governance-os-master-status.md`, `docs/roadmaps/governance-os-release-plan.md`

---

## 0. Scope and Non-Scope

PR-009 is the active critical path. It does two things: (A) clears the documentation/schema debt that makes the repository self-inconsistent, and (B) implements the two confirmed Skill-5 boundary blockers (M1, M2) so the CA chain can reach Skill FM for the first time.

**In scope (two work-streams):**

| Stream | Item | Source |
|---|---|---|
| A — Docs & schema | A1. Fix `CONFORMANT_FMO` test fixture (missing `markdown_output`) | master-status; verified |
| A — Docs & schema | A2. Fix M3 `ccs_distribution` key casing mismatch | master-status M3 |
| A — Docs & schema | A3. Update `governance-assessment-workflow.md` 4-skill → 6-skill chain (B-06) | master-status; CA AGENT.md B-06 |
| A — Docs & schema | A4. Create `agents/governance_review_agent/AGENT.md` (GRA) | master-status |
| A — Docs & schema | A5. Correct stale blockers in CA `AGENT.md` (B-01, B-04, B-05) | master-status |
| B — Skill-5 boundary | B1. Implement ADR-007 (M1) — `Skill5Adapter._capability_list()` reads `skill_3_json["matched_capabilities"]` | ADR-007 |
| B — Skill-5 boundary | B2. Implement ADR-008 Option A (M2) — CVA executor `use-cases.md` +10 in audit branch | ADR-008 |
| B — Skill-5 boundary | B3. Update CVA tests (ECS 85→95) and CA mock default (94→95) | ADR-008 |
| B — Skill-5 boundary | B4. Add defensive guard in `Skill6Adapter.map_output` for empty markdown (M5) | master-status pre-integration |

**Explicitly NOT in scope (deferred):**

- **ADR-009** (per-capability `ecs_evidence` metadata; evidence-driven ECS function; keyword-path elimination). ADR-009 is **Phase B**. PR-009 implements ADR-008 **Option A only** — the +10 increment in the audit branch. It does **not** touch the general fallback path, the MCP Broker path, or the CPM schema. After PR-009, 1 of 17 Production capabilities clears Gate 5c (Immutable Audit Log). This is intentional and sufficient for the v0.9 single-path integration test.
- **PR-010** fixture expansion (ESM ×3, FM ×3), and **B-02/B-03** (missing `ethana-solution-mapping` baselines/test-cases).
- **PR-011** scorecard compiler wiring into CA `ASSEMBLING_PACKAGE` (technical debt A3). Note: `scorecard_compiler.py` already exists at `evaluations/scripts/`; the remaining work is wiring, not implementation.
- **CA end-to-end integration test** (T3) — depends on B1+B2 landing first; scheduled after PR-009.
- GCM Section 10 / ISO Section 8 capability extraction (ADR-007 Phase B deferral).

---

## 1. Exact Files to Modify

| # | File | Change type | Stream |
|---|---|---|---|
| 1 | `evaluations/scripts/test_feature_mapping_proposal_review_integration.py` | Edit (test fixture) | A1 |
| 2 | `agents/client-assessment-agent/runtime/skills/solution_mapping_executor.py` | Edit (key casing) | A2 |
| 3 | `workflows/governance-assessment-workflow.md` | Rewrite §4 + downstream sections | A3 |
| 4 | `agents/governance_review_agent/AGENT.md` | **Create** | A4 |
| 5 | `agents/client-assessment-agent/AGENT.md` | Edit (§14 blocker table + §5.6/§ scorecard refs) | A5 |
| 6 | `agents/client-assessment-agent/runtime/skill_adapters.py` | Edit (`Skill5Adapter._capability_list`) | B1 |
| 7 | `agents/capability_validation_agent/runtime/skill_executor.py` | Edit (audit branch +10, arithmetic string) | B2 |
| 8 | CVA executor test(s) asserting `ecs=85` for Audit Log | Edit (→ `ecs=95`) | B3 |
| 9 | `agents/client-assessment-agent/runtime/orchestrator.py` | Edit (mock default 94→95) | B3 |
| 10 | `agents/client-assessment-agent/runtime/skill_adapters.py` | Edit (`Skill6Adapter.map_output` guard) | B4 |
| 11 | `reviews/governance-os-master-status.md` | Edit (status updates, mark items done) | closeout |
| 12 | `agents/client-assessment-agent/AGENT.md` §3 line 308 | Edit (remove "workflow file should be updated" once A3 done) | closeout |

Tests touched in stream B must be located precisely during implementation; candidate is `evaluations/scripts/test_capability_validation_runtime.py` (verify the exact assertion file before editing).

---

## 2. Exact Code Changes

### A1 — `CONFORMANT_FMO` fixture missing `markdown_output`

**Defect (verified):** `workflows/schemas/feature_mapping_output.json` requires `markdown_output` (line 9). The `CONFORMANT_FMO` dict in the test omits it. The standalone-schema test fails; the proposal-review sub-schema test passes (sub-schema only requires `feature_validation_table`). The FM executor itself already emits `markdown_output` (`feature_mapping_executor.py:180`) — so this is a **stale test fixture**, not a production bug.

**File:** `evaluations/scripts/test_feature_mapping_proposal_review_integration.py`, the `CONFORMANT_FMO` dict (lines 31–50).

```python
# After "production_tfs_score": 78, add:
    "markdown_output": (
        "## Feature Validation Table\n\n"
        "| Proposed Feature | Canonical Capability | Integration Path | TFS | PoC |\n"
        "|---|---|---|---|---|\n"
        "| AI Risk Monitoring Dashboard | Risk Monitoring Dashboard | Native API Integration | 85 | Ready |\n"
        "| Model Explainability Reports | Explainability Engine | Sidecar Service | 72 | Ready |\n"
    ),
```

**Verification:** the failing test `test_conformant_fmo_satisfies_feature_mapping_output_schema` passes; `test_conformant_fmo_satisfies_..._subschema` continues to pass.

---

### A2 — M3 `ccs_distribution` key casing mismatch

**Defect (verified):** schema `solution_mapping_output.json:30–40` declares capitalised keys (`Full`, `High`, `Partial`, `Thin`, `None`); executor emits lowercase.

**File:** `agents/client-assessment-agent/runtime/skills/solution_mapping_executor.py`

```python
# Line 210 — before:
ccs_distribution = {"full": 0, "high": 0, "partial": 0, "thin": 0, "none": 0}
# after:
ccs_distribution = {"Full": 0, "High": 0, "Partial": 0, "Thin": 0, "None": 0}
```

`_band_of()` (used at line 212 as the dict key) must return capitalised band names to match. Inspect `_band_of` and align its return values (`"Full"/"High"/"Partial"/"Thin"/"None"`). Any markdown compiler or downstream reader of `ccs_distribution` keys must be updated in the same change.

**Decision basis:** align executor to schema (not schema to executor) — the schema is the published contract; lowercasing the schema would ripple to any external consumer.

---

### A3 — `governance-assessment-workflow.md` 4-skill → 6-skill

**Defect (verified):** workflow §4 documents a 4-skill chain (regulatory-mapping → iso-42001-gap-assessment → governance-control-mapping → ethana-capability-validation). The CA agent implements the 6-skill chain.

**File:** `workflows/governance-assessment-workflow.md` — rewrite §4 "Skill Sequence" and the per-skill subsections (lines ~23–60+) to the authoritative chain:

```
1. regulatory-mapping (RM via RWA)
2. governance-control-mapping (GCM via RWA)
3. ethana-solution-mapping (ESM, local)
4. iso-42001-gap-assessment (ISO, local)
5. ethana-capability-validation (CapVal via CVA)  — Gate 5 / Truth Gate
FM. ethana-feature-mapping (FM, local)
6. ethana-proposal-review (ProposalReview via EPA) — release gate
```

Reconcile the ordering against the CA `AGENT.md` and `state-machine.md` as the authoritative source for the canonical sequence and gate placement before writing. Remove the stale 4-skill diagram and the per-skill "Skill Engaged" links that no longer match. After this lands, also remove the superseding note at CA `AGENT.md:308`.

---

### A4 — Create GRA `AGENT.md`

**Defect (verified):** every agent has an `AGENT.md` except `agents/governance_review_agent/` (runtime exists; spec doc absent).

**File (create):** `agents/governance_review_agent/AGENT.md`

Author from the existing GRA runtime as ground truth: `orchestrator.py`, `state_manager.py`, `skill_executor.py`, `output_builder.py`, `schema_validator.py`, `config.yaml`. Match the structure of a sibling AGENT.md (e.g. CVA or EPA) — purpose, skill(s) engaged, state machine, gates (governance-review terminal gate per ADR-006), inputs/outputs, schemas, blockers/readiness. Cross-reference ADR-006 (Governance Review Terminal Gate).

---

### A5 — Correct stale blockers in CA `AGENT.md`

**Finding (verified):** B-01, B-04, B-05 are stale — the code is already fixed; only the doc lags.

- **B-01** (`scorecard_compiler.py` is a stub): FALSE now. The file exists at `evaluations/scripts/scorecard_compiler.py` (181 lines, implemented: `compile_scorecard`, arg parsing, JSON IO). The real remaining work is **wiring it into CA `ASSEMBLING_PACKAGE`** (technical debt A3 → PR-011). Reword B-01 from "is a stub — not implemented" to "exists but not wired into CA `ASSEMBLING_PACKAGE`; integration is PR-011."
- **B-04** (certifier checks `"proposal-review"` vs `"ethana-proposal-review"`): FIXED. `agent_certifier.py:30` already lists `"ethana-proposal-review"`. Mark resolved.
- **B-05** (flat `.md` baselines invisible to certifier): FIXED. `agent_certifier.py:70–82` checks both directory and flat `{skill}-baseline.md` formats. Mark resolved.

**File:** `agents/client-assessment-agent/AGENT.md` — update the §14 blocker table (lines 697–718): re-classify B-01, strike B-04 and B-05 (or move to a "Resolved" subsection with the fixing reference), and update the "Required Before L4A" table rows accordingly. Do **not** alter B-02/B-03 (still open, PR-010) or B-06 (closed by A3 in this PR).

---

### B1 — ADR-007 (M1): `Skill5Adapter._capability_list()` reads Skill 3 output

**File:** `agents/client-assessment-agent/runtime/skill_adapters.py`, `Skill5Adapter._capability_list()` (lines 234–254).

Per ADR-007 Decision (Option D). After the existing `ca_inputs["capabilities"]` and `ca_inputs["capability_name"]` primary-path checks, and **before** the `raise`, insert extraction from `upstream`:

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
        "proposed_claim": (
            f"Ethana {name} addresses the governance requirement: "
            f"{row.get('requirement', '')}"
        ),
    })
if caps:
    return caps
# GCM Section 10 / ISO Section 8 extraction deferred to Phase B (ADR-007).
raise SkillAdapterError(
    "Skill 5 pre-check failed: skill_3_json matched_capabilities contained "
    "no named CPM capabilities (only generic fallbacks)."
)
```

Update the docstring (lines 235–241) to remove the "Until Skill 3 is implemented" deferral language and document the Phase B GCM/ISO deferral instead. Both Production and In Build entries are included (In Build → ECS 0 → contradiction documentation, per ADR-007 §3).

---

### B2 — ADR-008 Option A (M2): apply `use-cases.md` +10 in the audit branch

**File:** `agents/capability_validation_agent/runtime/skill_executor.py`, audit-branch Path A (lines 188–202).

```python
# Line 200–202 — before:
ecs = 85
ecs_band = "Authoritative"
ecs_arithmetic = "Base: +50; Detailed Entry: +20; Architecture Corroboration: +15; Total: 85"
# after:
ecs = 95
ecs_band = "Authoritative"
ecs_arithmetic = (
    "Base: +50; Detailed Entry: +20; Architecture Corroboration: +15; "
    "Use-cases.md corroboration: +10; Total: 95"
)
```

ADR-008 shows a conditional form (`if usecases_file.exists() and matched_cap: ecs += 10`). The audit branch already runs only when matched; `usecases_file` is checked at line 172. Either form is acceptable; the literal `95` with the corrected arithmetic string is simplest and matches the branch's existing literal style. The `evidence_basis` strings in `allowed_claims` (lines 210, 217) that read "ECS 85" must also be updated to "ECS 95".

**Scope guard:** do **not** modify the MCP Broker branch (`"broker"/"mcp"`) or the general fallback branch. Those remain at 75 and ≤70 respectively until ADR-009 (Phase B).

---

### B3 — Update CVA tests and CA mock default

**File:** CVA executor test asserting the Audit Log fixture ECS — change `ecs == 85` → `ecs == 95` and any `ecs_arithmetic` substring assertions to include the +10 term. (Locate the exact file/line during implementation; verify with `grep -rn "85" evaluations/scripts/test_capability_validation*`.)

**File:** `agents/client-assessment-agent/runtime/orchestrator.py:509`:

```python
# before:
ecs = s5_json.get("ecs", inputs.get("mock_skill_5_score", 94))
# after:
ecs = s5_json.get("ecs", inputs.get("mock_skill_5_score", 95))
```

Any CA test that passes `mock_skill_5_score` explicitly at a passing value (≥90) is unaffected; tests relying on the default 94 now see 95 — both pass Gate 5c (threshold 90), so no behavioural change to gate outcomes.

---

### B4 — M5 defensive guard in `Skill6Adapter.map_output`

**File:** `agents/client-assessment-agent/runtime/skill_adapters.py`, `Skill6Adapter.map_output` (around line 415, `out["markdown_output"] = intermediate.get("proposal_review_md", "")`).

```python
md = intermediate.get("proposal_review_md", "")
if not md:
    raise SkillAdapterError(
        "Skill 6 (proposal-review) markdown missing: EPA executor did not write "
        "'proposal_review_md' to intermediate_data before Skill6Adapter.map_output. "
        "This is the M5 out-of-band delivery path (see ADR / master-status)."
    )
out["markdown_output"] = md
```

This converts the opaque "empty markdown content" Gate 6b failure into an actionable diagnostic. It does not change the architecture (out-of-band delivery via `state_mgr` remains) — that is deferred.

---

## 3. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | **Full-suite test pollution masks/produces failures.** Running the whole suite currently yields 29 failures; RWA passes 34/34 in isolation. PR-007 claimed to fix pollution but it is still observable in this environment. | High | Medium | Validate every change per-module (`pytest <file>`) AND full-suite. Treat per-module green as the gate; flag any *new* full-suite-only failure for investigation. Do not let pollution noise hide a real regression in B1–B3. |
| R2 | **A2 casing change has downstream readers.** `ccs_distribution` keys may be read by the markdown compiler, scorecard compiler, or tests with lowercase literals. | Medium | Medium | `grep -rn "ccs_distribution\['"` and `\"full\"\|\"high\"` across runtime + tests + scorecard before editing; update all readers in the same commit. |
| R3 | **B1 changes capability set entering Skill 5**, so existing CA mock tests that never exercised the real adapter may now reach different states. | Medium | Medium | B1 only adds a fallback *after* `ca_inputs` checks; tests supplying `capabilities`/`capability_name` are unaffected. Confirm no CA test relies on the old `SkillAdapterError` being raised when Skill 3 data is present. |
| R4 | **A3 workflow rewrite diverges from `state-machine.md`.** Hand-written sequence could contradict the authoritative state machine. | Medium | Low | Derive the 6-skill sequence and gate placement strictly from CA `AGENT.md` + `state-machine.md`; do not invent ordering. |
| R5 | **A4 GRA AGENT.md drifts from runtime.** A spec written without reading every runtime module may misstate gates/states. | Low | Low | Author strictly from GRA runtime source; cross-check ADR-006. |
| R6 | **B2 misread as full M2 fix.** ADR-008 Option A resolves only the Audit Log path; 16/17 capabilities still fail Gate 5c. | Medium | Medium | Plan, master-status, and commit message must state explicitly that PR-009 = Option A only; ADR-009 (Phase B) covers the rest. The v0.9 integration test must use Audit-Log-surfacing input. |
| R7 | **Scope creep into ADR-009.** Temptation to "just also fix the general fallback." | Medium | High | Hard scope guard in B2: touch only the audit branch. Reviewer rejects any change to fallback/broker branches or the CPM. |

---

## 4. Test Impact

**New behaviour validated:**
- A1: `test_conformant_fmo_satisfies_feature_mapping_output_schema` flips fail → pass. Restores the headline "316/316 (per-module)" claim.
- B2/B3: CVA Audit Log fixture assertion moves 85 → 95; CA Gate 5c with default mock (now 95) still passes.

**Regression surface:**
- A2: any test asserting lowercase `ccs_distribution` keys must be updated; any schema-validation test of `solution_mapping_output` now passes where it may have silently not validated this field.
- B1: CA adapter tests — confirm none asserts the old "no capability" `SkillAdapterError` when `skill_3_json` is populated.
- B4: add/extend a Skill6Adapter test for the empty-markdown guard (asserts `SkillAdapterError` with the M5 diagnostic).

**New tests to add (minimum):**
1. `Skill5Adapter._capability_list` extracts and filters `matched_capabilities` (excludes generic fallbacks; dedups; raises informative error on empty filtered list). — ADR-007 acceptance.
2. CVA Audit Log ECS == 95 with arithmetic string containing the +10 term. — ADR-008 acceptance.
3. `Skill6Adapter.map_output` raises the M5 diagnostic on missing `proposal_review_md`.

**Out of scope for PR-009 tests:** the full CA 6-skill end-to-end integration test (T3) — it depends on B1+B2 and is the next milestone after PR-009.

**Validation protocol:** run each touched test file individually first (authoritative pass/fail), then the full suite to characterise pollution; record both counts in the PR description.

---

## 5. Rollback Strategy

- **Granularity:** land PR-009 as discrete commits per item (A1, A2, A3, A4, A5, B1, B2+B3, B4) so any single item can be reverted independently with `git revert <sha>`.
- **Doc-only items (A3, A4, A5):** zero runtime risk; revert is cosmetic.
- **A1:** test-data only; revert restores the prior (failing) state — no production impact.
- **A2 (casing):** if a downstream reader is missed and breaks, revert the single executor commit; schema is unchanged so no contract regression on rollback.
- **B1 (M1):** revert restores the `ca_inputs`-only behaviour (CA halts at `HALTED_ESCALATION` on standard intake) — i.e. back to the known pre-PR-009 blocker, not a worse state. Safe.
- **B2+B3 (M2):** revert restores ECS 85 / mock 94. Gate 5c returns to its pre-fix ceiling. Safe; no data migration.
- **B4 (M5 guard):** pure defensive addition; revert removes the diagnostic only.
- **No schema/data migrations** in PR-009 (ADR-009's CPM `ecs_evidence` change — which *would* need migration discipline — is explicitly deferred), so rollback is always a clean `git revert` with no state cleanup.
- **Tag before merge:** confirm `v0.8.1-pr008-complete` is the restore point; do not tag PR-009 until the DoD passes.

---

## 6. Definition of Done

**Stream A (docs & schema):**
- [ ] `CONFORMANT_FMO` fixture includes `markdown_output`; `test_feature_mapping_proposal_review_integration.py` passes fully (per-module).
- [ ] `ccs_distribution` keys are capitalised in the executor and match `solution_mapping_output.json`; all readers updated; schema-validation test green.
- [ ] `governance-assessment-workflow.md` §4 documents the 6-skill chain consistent with CA `AGENT.md` and `state-machine.md`; stale 4-skill content removed; CA `AGENT.md:308` superseding note removed.
- [ ] `agents/governance_review_agent/AGENT.md` exists, authored from GRA runtime, cross-references ADR-006.
- [ ] CA `AGENT.md` §14: B-01 reworded (exists, wiring = PR-011), B-04 and B-05 marked resolved with fixing reference; B-02/B-03/B-06 status correct (B-06 closed by this PR).

**Stream B (Skill-5 boundary):**
- [ ] `Skill5Adapter._capability_list()` extracts from `skill_3_json["matched_capabilities"]`, excludes generic fallbacks, dedups, and raises an informative error on empty filtered list; docstring updated; ADR-007 acceptance test passes.
- [ ] CVA Audit Log path returns ECS 95 with corrected `ecs_arithmetic` and `evidence_basis` strings; ADR-008 acceptance test passes. **No change to MCP Broker or general fallback branches.**
- [ ] CVA tests updated 85 → 95; CA mock default updated 94 → 95.
- [ ] `Skill6Adapter.map_output` raises the M5 diagnostic on missing `proposal_review_md`; guard test passes.

**Cross-cutting:**
- [ ] Every touched test file passes in isolation (authoritative).
- [ ] Full-suite run characterised; any full-suite-only failures confirmed as pre-existing pollution (RWA isolation = 34/34) and recorded — no *new* real failures.
- [ ] `reviews/governance-os-master-status.md` updated: M1 → resolved (ADR-007 implemented), M2 → resolved-for-Audit-Log (ADR-008 Option A; remainder = ADR-009 Phase B), M3 → resolved, M5 → guarded, PR-009 → Complete; ADR-009 remains Proposed/Phase B.
- [ ] Commit messages state explicitly that ADR-009 is **not** implemented in this PR.
- [ ] No CPM schema change; no data migration; clean `git revert` available per item.

**Exit gate to next milestone:** with B1+B2 landed, the CA chain can reach Skill FM/6 on Audit-Log-surfacing input for the first time — enabling the CA end-to-end integration test (T3) as the immediate post-PR-009 task.

---

## 7. Sequencing Within PR-009

```
A4 (GRA AGENT.md)        ─┐  doc-only, parallelizable, zero runtime risk
A3 (workflow 6-skill)    ─┤
A5 (CA AGENT.md blockers)─┘
A1 (CONFORMANT_FMO)        → restores 316/316 per-module baseline first
A2 (ccs casing)            → grep readers, then edit
B1 (M1 Skill5 source)    ─┐  land together: both required before chain advances
B2+B3 (M2 ECS +10)       ─┘
B4 (M5 guard)              → after B1/B2 so the chain can actually reach Skill 6
closeout: master-status + counts
```

Land docs and A1 first (cheap, de-risks the baseline), then A2, then the B-stream as the substantive change, then the master-status closeout.
