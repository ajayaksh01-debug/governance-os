# Governance OS Master Status

## Repository Version

**Current Milestone:** v0.8.2-pr010-complete
**Predecessor:** v0.8.1-pr009-complete (PR-009: Documentation, Schema, and Adapter Repairs)
**Status:** PR-010 Complete

---

## Current Completion

- **Internal Tool Readiness:** 67–70%
- **SaaS Product Readiness:** 22–27%

---

## Agent Status

### Genuine L4

- Capability Validation Agent (CVA) — ECS now 95 for Immutable Audit Log (ADR-008 implemented)
- Incident Intelligence Agent (IIA)
- Ethana Proposal Agent (EPA)
- Governance Review Agent (GRA) — AGENT.md created (PR-009)
- Regulatory Watch Agent (RWA) — certified PR-008

### Partial

- **Client Assessment Agent (CA)**

**Reason:** No successful end-to-end execution using real adapters. CA tests use mocked skill outputs. M1 and M2 blockers are now resolved (PR-009); the chain can reach Skill FM for the first time on Audit-Log-surfacing input. M7 (EPA scoring on concatenated governance markdown) is unknown-risk until the first real run. Scorecard compiler unwired (PR-011). Client Memory unimplemented.

---

## PR Status

### Complete

**✓ PR-008 — Regulatory Watch Agent L4 Certification**
- 34 dedicated runtime tests; all 24 RWA states covered
- Tagged: `v0.8.1-pr008-complete`

**✓ PR-009 — Documentation, Schema, and Skill-5 Boundary Repairs**

*Stream A (docs & schema):*
- **A1** — Fixed `CONFORMANT_FMO` fixture (added `markdown_output`); restores 326/326 per-module pass count
- **A2** — Fixed M3 `ccs_distribution` key casing (`full/high/...` → `Full/High/...`); executor now matches `solution_mapping_output.json` schema
- **A3** — Rewrote `governance-assessment-workflow.md` §4 to canonical 6-skill chain (RM → GCM → ESM → ISO → CapVal → FM → ProposalReview); removed stale 4-skill diagram; 4 approval gates documented; CA AGENT.md §6.1 superseding note removed (B-06 closed)
- **A4** — Created `agents/governance_review_agent/AGENT.md` (GRA spec: state machine, 7 GTG gates, GAS/CCR/high-risk scoring, classification thresholds, ADR-006 reference)
- **A5** — Corrected stale blockers in CA `AGENT.md` §14: B-01 reworded (scorecard_compiler.py exists, wiring = PR-011), B-04/B-05 marked resolved, B-06 closed

*Stream B (Skill-5 boundary — M1 and M2 now resolved):*
- **B1** — Implemented ADR-007 (M1): `Skill5Adapter._capability_list()` now extracts from `upstream["skill_3_json"]["matched_capabilities"]`; excludes generic fallbacks; deduplicates; raises informative error on empty list; docstring updated; 7 ADR-007 acceptance tests added
- **B2** — Implemented ADR-008 Option A (M2): CVA audit branch ECS 85 → 95; `ecs_arithmetic` includes `Use-cases.md corroboration: +10`; all `evidence_basis` strings updated to `ECS 95`. **ADR-009 (Phase B general fallback) NOT implemented — out of scope**
- **B3** — Updated CVA test assertion (ECS range 80–90 → exact 95); added ADR-008 arithmetic acceptance test; CA mock default 94 → 95
- **B4** — Added M5 defensive guard in `Skill6Adapter.map_output`: empty `proposal_review_md` now raises `SkillAdapterError` with diagnostic; 2 guard tests added

*Tests:*
- 10 new tests added (7 for B1/ADR-007, 1 for B2/ADR-008, 2 for B4/M5 guard)
- 1 existing test fixed (CONFORMANT_FMO schema assertion)
- 1 existing CVA ECS assertion updated (85→95)
- Per-module validation: 9/9 FM-PR, 18/18 Skill3, 4/4 CVA, 87/87 CA runtime, 34/34 RWA
- **Test count after PR-009: 326 total / 326 passing (per-module)**
- Full-suite: 298 passed / 28 failed — all 28 failures are pre-existing RWA test pollution (RWA 34/34 isolated); no new regressions introduced
- **Test count after PR-010: 352 total / 352 passing (per-module)** (+26: 21 T6 + 4 T1 + 1 T3)

**✓ PR-010 — Capability Discovery Repair (Natural Extraction Path)**

Fixes M4: Skill 1 produces 6 regulatory control names that zero-match all 52 CPM keys via
bidirectional substring matching → generic fallback cascade → `SkillAdapterError` → `HALTED_ESCALATION`.
Solution: semantic knowledge bridge via `knowledge/ethana/control-capability-map.md`;
`suggested_capability` field threaded through Skill 2 → Skill2Adapter → Skill 3;
direct CPM dict access in `_score_requirement()` bypasses `_match_capability()`.

*Files changed:*
- **C1** — Created `knowledge/ethana/control-capability-map.md` (Option D): 6 control → CPM-key mappings, Option B pre-population, control-name covenant preamble
- **C2** — Added `load_control_capability_map()` to `evaluations/scripts/claims_linter.py` (+63 lines): Phase A loader (secondary always `[]`), CPM key cross-validation, graceful file-not-found
- **C3** — `agents/regulatory-watch-agent/runtime/skill_executor.py`: added `import sys`, `_ccm` cache, `_load_ccm()`, `ccm = self._load_ccm()` before control loop, `"suggested_capability"` field in `control_taxonomy_matrix.append()`
- **C4** — `agents/client-assessment-agent/runtime/skill_adapters.py` (`Skill2Adapter.map_output`): added `"suggested_capability": row.get("suggested_capability", "")`
- **C5** — `agents/client-assessment-agent/runtime/skills/solution_mapping_executor.py` (`_score_requirement`): direct CPM lookup via `self._load_cpm().get(suggested)` when `suggested_capability` non-empty; `_match_capability()` NOT modified

*Tests:*
- **T6** — 21 new tests in `test_control_capability_map.py`: T6(a) happy path, T6(b) missing file, T6(c) unknown key, T6(d) invalid CPM key warning, T6(e) covenant bijection validation
- **T1** — 4 new tests in `test_client_assessment_skill3.py` (`TestSkill3SuggestedCapability`): Immutable Audit Log, Runtime Guardrails, empty primary fallback, invalid key graceful degradation
- **T3** — 1 new test in `test_client_assessment_runtime.py` (`TestNaturalExtractionPath`): full chain EU BFSI + LLM → "Immutable Audit Log" in matched_capabilities, Production status, ccs > 0
- **T2** — 18 pre-existing Skill3 tests: all pass, no modifications (confirmed no-op)
- **T4** — Pre-existing runtime tests: no assertions on "Ethana Platform" for Skill 1 control names; confirmed no-op
- **T5** — 34 RWA tests: all pass after `suggested_capability` field addition

*Test count after PR-010: 352 total / 352 passing (per-module)*
*(+26 new: 21 T6 + 4 T1 + 1 T3)*

*M4 status:* **Resolved.** Human Oversight Gate → `immutable audit log` → `Immutable Audit Log` (Production, CCS 95) in matched_capabilities. Gate 5c (ECS ≥ 90) is now reachable from real intake for EU BFSI + LLM clients.

### Remaining

- **PR-011** — Scorecard Compiler Integration (wire into CA `ASSEMBLING_PACKAGE`)
- **PR-012** — Certifier Upgrade (evidence-based L4; blocked until CA end-to-end test exists)
- **CA End-to-End Validation** — first real run: Audit-Log-surfacing EU BFSI input → 6 skills via real adapters → 4 approval gates → COMPLETE; unlocked by PR-009 M1+M2 + PR-010 M4 fixes

---

## Critical Technical Debt

### Architecture

| ID | Item | Severity for v0.9 | Status |
|---|---|---|---|
| A1 | Cross-runtime coupling via `skill_adapters.py` — no interface contract enforcement | High | Open |
| A3 | `scorecard_compiler.py` not wired into CA `ASSEMBLING_PACKAGE` | High | PR-011 |
| A4 | `claims_linter.py` layer boundary violation | Medium | Open |
| ~~A7~~ | ~~`feature_mapping_output.json` / FM executor out of sync~~ | ~~High~~ | **Resolved (PR-009): ccs_distribution casing fixed, CONFORMANT_FMO fixture corrected** |

### Testing

| ID | Item | Severity for v0.9 | Status |
|---|---|---|---|
| T2 | CA tests mock skill execution — 205 tests use lambda overrides; real adapter chain never exercised | High | Unlocked (CA end-to-end next) |
| T3 | No CA 6-skill end-to-end integration test | Critical | Next milestone after PR-009 |
| T4 | `ethana-solution-mapping` has zero test fixtures | High | PR-010 |
| T5 | Certifier L4 evidence validation incomplete | Medium | PR-012 |

---

## CA Adapter Audit Findings

**Audit date:** 2026-06-21 | **Updated:** 2026-06-22 (PR-009)

### Resolved (PR-009)

**M1 — Skill5Adapter now reads Skill 3 output (ADR-007 implemented)**

`Skill5Adapter._capability_list()` now extracts named capabilities from `upstream["skill_3_json"]["matched_capabilities"]`. Generic fallbacks excluded. Both Production and In Build entries included (In Build → ECS 0 → contradiction documentation). Standard CA runs on Audit-Log-surfacing input can proceed past Skill 4.

**M2 — Gate 5c ECS ceiling raised to 95 (ADR-008 Option A implemented)**

CVA executor audit branch: ECS 85 → **95**. Gate 5c threshold remains 90. Immutable Audit Log clears Gate 5c with 5 points of headroom. 1 of 17 Production capabilities clears Gate 5c. Remaining 16 capabilities require Phase B (ADR-009).

**M3 — ccs_distribution key casing fixed**

`solution_mapping_executor.py`: lowercase keys (`full/high/partial/thin/none`) corrected to capitalised (`Full/High/Partial/Thin/None`) matching `solution_mapping_output.json` schema contract.

**M5 — Skill6Adapter defensive guard added**

`Skill6Adapter.map_output` now raises `SkillAdapterError` with M5 diagnostic when `proposal_review_md` is absent. Converts opaque "empty markdown content" Gate 6b failure into an actionable error. Architecture (out-of-band delivery) unchanged.

### High Risk (unknown until first real run)

**M7 — EPA scoring against concatenated governance markdown unverified**

`draft_proposal` fed to EPA is the concatenated Skills 1–5 markdown. EPA's claim extractor was designed for standalone proposal documents. Unexpected CTCS or false-positive CFBs are possible. First real-adapter run will expose this.

### Lower Risk (open)

| ID | Issue | Notes |
|---|---|---|
| ~~M4~~ | ~~Capability discovery gap: Skill 1 control names zero-match CPM via substring → generic fallback cascade~~ | **Resolved (PR-010): knowledge bridge + suggested_capability field** |
| M6 | `platform_coverage` boolean derived from `"Ethana" in coverage_classification` — silent failure if RWA format changes | Latent; no contract enforcement |

---

## Approved Architecture Decisions

| ADR | Title | Resolves | Status |
|---|---|---|---|
| [ADR-007](../docs/decisions/ADR-007-skill5-capability-source.md) | Capability Source for Skill 5 in the Client Assessment Chain | M1 | **Accepted — Implemented PR-009** |
| [ADR-008](../docs/decisions/ADR-008-gate5-ecs-calibration.md) | ECS Threshold and CVA Executor Scoring Calibration for Gate 5c | M2 | **Accepted — Option A Implemented PR-009** |
| [ADR-009](../docs/decisions/ADR-009-ecs-general-fallback-calibration.md) | ECS General Fallback Calibration and Per-Capability Evidence Architecture | M2 (Phase B) | **Proposed — Phase B; NOT implemented in PR-009** |

**ADR-007 decision:** `Skill5Adapter._capability_list()` derives capabilities from `upstream["skill_3_json"]["matched_capabilities"]`. Generic fallback entries excluded. GCM/ISO extraction deferred to Phase B.

**ADR-008 Option A:** Gate 5c threshold remains at 90. `use-cases.md` +10 ECS increment applied in CVA executor audit branch. Immutable Audit Log: 85 → 95. General fallback (16/17 capabilities) deferred to Phase B per ADR-009.

**ADR-009 decision (Proposed — Phase B):** Add per-capability `ecs_evidence` blocks to CPM; replace keyword-path ECS selection with evidence-driven function. 15 of 17 Production capabilities reach ECS 95 after Phase B. MCP Broker stays at 85 until contradiction resolved.

---

## Updated Roadmap

```
PR-008 — RWA L4 Certification                   ✓ COMPLETE
  │
PR-009 — Documentation & Schema Repairs          ✓ COMPLETE
  │   M1/M2/M3/M5 resolved; 326/326 per-module; GRA AGENT.md; workflow updated
  │
PR-010 — Capability Discovery Repair             ✓ COMPLETE
  │   M4 resolved; knowledge bridge; suggested_capability threaded; 352/352 per-module
  ↓
CA End-to-End Validation                         ← NEXT MILESTONE
  │   Immutable Audit Log path end-to-end viable (M1+M2+M4 all resolved)
  │   v0.9 integration test: EU BFSI + LLM real-adapter run → COMPLETE
  │   M7 risk will manifest here; budget 1–2 weeks with M5 guard now in place
  ↓
PR-011 — Scorecard Compiler Integration
  ↓
PR-012 — Certifier Upgrade
  │   (CA end-to-end test must exist before merge)
  ↓
Governance OS v0.9 Internal Tool
```

---

## Updated Estimate to v0.9

| Scenario | Remaining | Basis |
|---|---|---|
| **Best case** | 2–3 weeks | CA end-to-end passes cleanly; M7 does not produce unexpected EPA behaviour |
| **Expected** | 4–5 weeks | CA end-to-end needs one iteration on M7 EPA calibration; PR-010/011 run in parallel |
| **Conservative** | 6–7 weeks | M7 EPA scoring on concatenated governance markdown produces false-positive CFBs requiring explicit calibration ADR and executor change |

**Primary bottleneck (updated):** CA end-to-end integration test. M1, M2, and M4 are all resolved. M7 (EPA scoring on concatenated governance markdown) and M5 (now guarded) are the remaining unknowns. The first real-adapter run on EU BFSI + LLM input will surface M7 behaviour.

---

## Program Assessment

| Dimension | Rating | Notes |
|---|---|---|
| Architecture | Good | Sound design; Claims Firewall production-hardened; ADRs 7–9 document adapter boundary decisions |
| Specification | Good | All 6 agents have AGENT.md; CA state-machine.md and workflow.yaml are authoritative; GRA AGENT.md added PR-009 |
| Testing | Good | 352/352 per-module; +26 PR-010 tests (T6 loader/covenant, T1 direct CPM path, T3 natural extraction); CVA ECS 95 asserted |
| Documentation | Good | governance-assessment-workflow.md updated to 6-skill chain; CA AGENT.md stale blockers corrected |
| Integration | Medium Risk | M1+M2 resolved; CA chain can reach Skill 6 on Audit-Log input; M7 unknown until first real run |
| Production Readiness | Low | No API, no notifications, no deployment infrastructure, no Client Memory |

---

## Next Milestone

**CA End-to-End Validation:** first complete CA run using real adapters on EU BFSI + LLM input → COMPLETE state → 12 artifacts. M1, M2, and M4 are now all resolved — the Immutable Audit Log path is end-to-end viable without fixture injection. This is the blocker for v0.9 certification. M7 EPA behaviour will be exposed here.

**Immediate action:** Execute the CA end-to-end integration test (wire all 6 skills without lambda overrides). Use the EU AI Act Article 12 audit trail fixture (EU + BFSI + LLM: Human Oversight Gate → immutable audit log → ECS 95 clears Gate 5c). Monitor Gate 6 for M7 EPA scoring behaviour on concatenated governance markdown.
