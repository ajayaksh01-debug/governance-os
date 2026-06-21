# Governance OS Master Status

## Repository Version

**Current Milestone:** v0.8.1-pr008-complete
**Commit:** b88c54f
**Status:** PR-008 Complete and Tagged

---

## Current Completion

- **Internal Tool Readiness:** 62–65%
- **SaaS Product Readiness:** 22–27%

---

## Agent Status

### Genuine L4

- Capability Validation Agent (CVA)
- Incident Intelligence Agent (IIA)
- Ethana Proposal Agent (EPA)
- Governance Review Agent (GRA)
- Regulatory Watch Agent (RWA) — certified PR-008

### Partial

- **Client Assessment Agent (CA)**

**Reason:** No successful end-to-end execution using real adapters. 205 tests pass with mocked skill outputs only. Two confirmed blocking failures at the Skill 5 adapter boundary (M1, M2). Scorecard compiler unwired. Client Memory unimplemented.

---

## PR Status

### Complete

**✓ PR-008 — Regulatory Watch Agent L4 Certification**

- 34 dedicated runtime tests (`test_regulatory_watch_runtime.py`)
- Mode A coverage: EU BFSI, India DPDP, UK Insurance happy paths
- Mode B coverage: affected run identification, 3-run concurrency cap enforcement
- Approval path coverage: Gate 1 and Gate 2 failure paths; AG-2 re-gate (clean modifications)
- Firewall coverage: Gate 3b Claims Firewall halt via `start_run` flow
- Minimal-risk fixture: `evaluations/test-cases/regulatory-subjects/minimal-risk-internal-tool.md` (closes L4A blocker)
- All 24 RWA state machine states reached in test assertions
- Tagged: `v0.8.1-pr008-complete`

**Test count after PR-008:** 316 total / 315 passing (CONFORMANT_FMO defect persists — resolved by PR-009)

### Active Critical Path

**PR-009 — Documentation & Schema Repairs**

- CONFORMANT_FMO `markdown_output` fix (restores 316/316 passing)
- `governance-assessment-workflow.md` update to 6-skill chain
- GRA `AGENT.md` creation
- CA `AGENT.md` stale blocker corrections (B-01, B-04, B-05)

**Dependencies:** None. Start immediately — the PR-009 parallel window alongside PR-008 has closed.

### Remaining

- **PR-010** — Fixture Expansion (ethana-solution-mapping × 3, ethana-feature-mapping × 3)
- **PR-011** — Scorecard Compiler Integration (wire into CA `ASSEMBLING_PACKAGE`)
- **PR-012** — Certifier Upgrade (evidence-based L4; blocked until CA end-to-end test exists)
- **CA End-to-End Validation** — one complete run: real EU BFSI input → 6 skills via real adapters → 4 approval gates → COMPLETE → all 12 artifacts

---

## Critical Technical Debt

### Architecture

| ID | Item | Severity for v0.9 |
|---|---|---|
| A1 | Cross-runtime coupling via `skill_adapters.py` — no interface contract enforcement; signature changes in RWA/CVA/EPA fail silently in CA | High |
| A3 | `scorecard_compiler.py` not wired into CA `ASSEMBLING_PACKAGE` — client scorecard cannot be produced by a CA run | High |
| A4 | `claims_linter.py` layer boundary violation — evaluation tool imported at runtime by production orchestrators | Medium |
| A7 | `feature_mapping_output.json` schema / FM executor out of sync — `markdown_output` field missing from CONFORMANT_FMO fixture; `ccs_distribution` key casing mismatch (lowercase vs. schema capitalised) | High |

### Testing

| ID | Item | Severity for v0.9 |
|---|---|---|
| T2 | CA tests mock skill execution — 205 tests use lambda overrides; real adapter chain never exercised | High |
| T3 | No CA 6-skill end-to-end integration test — chain has never run with real inter-skill data | Critical |
| T4 | `ethana-solution-mapping` has zero test fixtures — most logic-heavy local executor unvalidated | High |
| T5 | Certifier L4 evidence validation incomplete — grants L4 for non-empty directory; CA incorrectly certified | Medium |

---

## CA Adapter Audit Findings

**Audit date:** 2026-06-21
**Scope:** All 6 skill handoffs traced from source runtime through adapter to consumer; all schemas verified.

### Critical Blockers (certain failures on first real run)

**M1 — Skill5Adapter does not consume Skill 3 output**

`Skill5Adapter._capability_list()` reads only from `ca_inputs`. Neither `capabilities` nor `capability_name` is a required intake field. `skill_3_json["matched_capabilities"]` contains exactly the capability list needed but is not read by the adapter (the extraction was deferred when Skill 3 was built).

**Effect:** Every standard CA run halts at `HALTED_ESCALATION` after Skill 4. Skills FM, 6, and package assembly are unreachable.

**Fix location:** `agents/client-assessment-agent/runtime/skill_adapters.py` — `Skill5Adapter._capability_list()`. Extract from `upstream["skill_3_json"]["matched_capabilities"]`.

**Status:** ADR-007 approved — decision recorded at `docs/decisions/ADR-007-skill5-capability-source.md`. Pending implementation in PR-009 sprint.

---

**M2 — Gate 5c ECS threshold exceeds CVA executor maximum**

Gate 5c threshold: **90** (from `config.yaml`, read at `orchestrator.py:824`).
CVA executor maximum ECS: **85** (Authoritative path, Immutable Audit Log).
Mock default used by all 205 tests: **94**.

Root cause: `skills/ethana-capability-validation/SKILL.md` documents a `use-cases.md` corroboration increment of +10 ECS. The CVA executor checks for the file and logs it in `sources_checked` but never applies the increment to the ECS integer. With the increment applied: Immutable Audit Log reaches 95, clearing Gate 5c. The threshold of 90 is correct and intentional.

**Effect:** Even after M1 is fixed, every CA run halts at `HALTED_GATE_5_SCORE_INSUFFICIENT`. The back half of the chain is unreachable until the executor omission is corrected.

**Status:** ADR-008 approved — decision recorded at `docs/decisions/ADR-008-gate5-ecs-calibration.md`. Fix: implement missing `use-cases.md` +10 ECS increment in CVA executor. Threshold remains at 90. Pending implementation in PR-009 sprint.

---

### High Risk (unknown until first real run)

**M5 — EPA markdown delivered out-of-band via state_mgr**

EPA executor writes `proposal_review_md` to `state_mgr` as a side effect rather than including it in the return value. `Skill6Adapter.map_output` reads it back from `state_mgr.get_state()`. Works synchronously in-process; breaks if decoupled. Gate 6b failure message (`"empty markdown content"`) does not identify the real cause.

**M7 — EPA scoring against concatenated governance markdown unverified**

`draft_proposal` fed to EPA is the concatenated Skills 1–5 markdown — regulatory analysis, control specifications, ISO gap assessment, solution mapping, and capability validation. EPA's claim extractor was designed for standalone proposal documents. Unexpected CTCS scoring or false-positive CFBs are possible when applied to governance analysis content. Has never been exercised.

### Lower Risk

| ID | Issue | Notes |
|---|---|---|
| M3 | `ccs_distribution` key casing mismatch — executor produces lowercase keys; schema declares capitalised | Not a runtime blocker; will affect scorecard compiler if it reads this field |
| M4 | Empty `control_requirements` for India non-NBFC non-BFSI profiles causes Skill 2 pre-check halt | Outside v0.9 fixture scope |
| M6 | `platform_coverage` boolean derived from string match `"Ethana" in coverage_classification` — silent failure if RWA string format changes | Latent; no contract enforcement |

---

## Approved Architecture Decisions

| ADR | Title | Resolves | Status |
|---|---|---|---|
| [ADR-007](../docs/decisions/ADR-007-skill5-capability-source.md) | Capability Source for Skill 5 in the Client Assessment Chain | M1 | **Accepted** |
| [ADR-008](../docs/decisions/ADR-008-gate5-ecs-calibration.md) | ECS Threshold and CVA Executor Scoring Calibration for Gate 5c | M2 | **Accepted** |

**ADR-007 decision:** `Skill5Adapter._capability_list()` derives capabilities from `upstream["skill_3_json"]["matched_capabilities"]`. Generic fallback entries excluded. GCM/ISO extraction deferred to Phase B.

**ADR-008 decision:** Gate 5c threshold remains at 90. Missing `use-cases.md` +10 ECS increment implemented in CVA executor. Immutable Audit Log path: 85 → 95. General fallback Production path recalibration deferred to Phase B.

---

## Updated Roadmap

```
PR-008 — RWA L4 Certification                   ✓ COMPLETE
  │
PR-009 — Documentation & Schema Repairs          ← ACTIVE CRITICAL PATH
  │   ADR-007 and ADR-008 decisions approved; implement M1 and M2 fixes in this sprint
  ↓
PR-010 — Fixture Expansion
  │   (ESM × 3, FM × 3)
  ↓
PR-011 — Scorecard Compiler Integration
  ↓
PR-012 — Certifier Upgrade
  │   (CA end-to-end test must exist before merge)
  ↓
CA End-to-End Validation
  │   M1 and M2 resolved per ADR-007 and ADR-008
  │   Budget 2–3 weeks; M7 EPA behaviour unknown
  ↓
Governance OS v0.9 Internal Tool
```

**Pre-integration actions required before CA end-to-end test:**
1. Implement ADR-007 — fix M1 in `Skill5Adapter._capability_list()` (extract from `skill_3_json["matched_capabilities"]`)
2. Implement ADR-008 — fix M2 by adding `use-cases.md` +10 ECS increment in CVA `skill_executor.py`; update mock default from 94 to 95
3. Add defensive guard in `Skill6Adapter.map_output` for empty markdown (M5)
4. Fix `ccs_distribution` key casing in `solution_mapping_executor.py` (M3)

---

## Updated Estimate to v0.9

| Scenario | Remaining | Basis |
|---|---|---|
| **Best case** | 3–4 weeks | M1/M2 resolved in PR-009 sprint; CA adapters clean once gates are corrected |
| **Expected** | 5–6 weeks | PR-009–012 take 2.5 weeks; CA end-to-end takes 2–3 weeks with one round of adapter debugging |
| **Conservative** | 7–8 weeks | Scorecard compiler requires non-trivial refactor; M7 EPA scoring produces unexpected results requiring iteration |

**Primary bottleneck:** CA adapter chain integration. M1 and M2 are certain failures. M7 and M5 are unknown-risk until first real run. All 205 existing CA tests must be supplemented with at least one real-adapter integration test before v0.9 can be declared.

---

## Program Assessment

| Dimension | Rating | Notes |
|---|---|---|
| Architecture | Good | Sound design; Claims Firewall production-hardened; 4-layer separation understood and documented |
| Specification | Good | CA AGENT.md, state-machine.md, evaluation.md are production-quality; ADRs document real decisions |
| Testing | Moderate | 315/316 passing; RWA now fully covered; CA mocks hide two certain integration failures |
| Documentation | Moderate | governance-assessment-workflow.md stale; GRA has no AGENT.md; CA AGENT.md has stale blockers |
| Integration | High Risk | CA adapter chain has never run end-to-end; M1 and M2 are confirmed blockers |
| Production Readiness | Low | No API, no notifications, no deployment infrastructure, no Client Memory |

**Primary risk:** Client Assessment integration through real adapter execution. The Skill 5 adapter boundary (M1 + M2) must be resolved before the CA end-to-end integration test can produce a COMPLETE run. Until that test passes, v0.9 cannot be declared.

---

## Next Milestone

**v0.9 Internal Tool:** All 6 agents at genuine L4; CA chain executes end-to-end with real data; Executive Assessment Package produced; scorecard compiler wired; certifier evidence-based.

**Immediate action:** Start PR-009. Resolve M1 and M2 during the PR-009 sprint to de-risk the CA integration path before fixture work begins.
