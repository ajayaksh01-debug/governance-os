# Governance OS v1 Internal Tool Roadmap

**Date:** 2026-06-21  
**Basis:** Program Review (2026-06-21), Master Status Baseline, PR-008 Architecture Design  
**Authoritative sources:**
- `reviews/governance-os-program-review-2026-06-21.md`
- `reviews/governance-os-master-status.md`
- `docs/decisions/PR-008-regulatory-watch-agent-l4-readiness.md`

---

## Mission

Define the shortest path from the current repository state to a usable Governance OS v1 Internal Tool capable of executing a complete client assessment and producing an Executive Assessment Package.

v1 Internal Tool is the minimum configuration in which a human operator — without writing custom code or reading JSON state files — can initiate a governance assessment for a real enterprise AI subject, advance through all approval gates, and receive a complete, Claims-Firewall-verified Executive Assessment Package including regulatory scoping matrix, operational control specification, ISO 42001 gap assessment, solution mapping, feature validation, proposal review, and client scorecard.

---

## Current State

### Internal Tool Readiness: 55–60%

The architecture is sound and the Claims Firewall is production-hardened. Four of six agents have verified runtimes and passing test suites. The remaining two agents — which together constitute the full governance assessment capability — are at Prototype status.

### SaaS Product Readiness: 20–25%

Production infrastructure (REST API, approval notifications, multi-tenant persistence, CI/CD) does not exist. Client Memory is unimplemented. No deployment mechanism exists beyond direct Python invocation.

### Complete Agents

| Agent | Certification | Test Evidence |
|---|---|---|
| Capability Validation Agent (CVA) | L4 | 3 tests — production/in-build/mixed-status paths, approval flows, all failure modes |
| Incident Intelligence Agent (IIA) | L4 | 5 tests — Samsung happy path, 3 failure modes, approval bypass firewall |
| Ethana Proposal Agent (EPA) | L4 | 15 tests — 6 runtime + 9 FM→PR integration contract; approval bypass tested |
| Governance Review Agent (GRA) | L4 | 45 tests — 3 fixture paths, dotted-import runtime, natively immune to sys.modules pollution |

All four agents cover incident response, standalone proposal review, and individual capability validation.

### Partial Agents

**Regulatory Watch Agent (RWA) — Prototype**
- 969-line orchestrator; Mode A (Assessment) and Mode B (Watch) defined; 2 approval gates implemented
- 2 tests exist, both in `test_firewall_hardening.py`, both exercising failure paths via direct method calls
- Happy path has never been tested; Mode B (regulatory change re-assessment queue) is entirely untested
- 22 of 24 state machine states never reached by any test
- Certifier incorrectly reports L4 — based on non-empty directory, not test evidence

**Client Assessment Agent (CA) — Prototype**
- Specification: production-quality (AGENT.md, state-machine.md, evaluation.md are comprehensive)
- Runtime: 835-line orchestrator, `skill_adapters.py` Option C adapter chain, 3 local executors, 59-state machine
- ~205 tests validate the state machine using mocked skill outputs only
- The 6-skill chain has never run end-to-end with real data flowing through real adapters
- `scorecard_compiler.py` not wired into ASSEMBLING_PACKAGE orchestrator step — the defining CA output (client scorecard JSON) cannot be produced by a CA run
- Client Memory (tiers 2 and 3) unimplemented — Mode B incremental re-assessment is unreachable
- Certifier incorrectly reports L4 for the same directory-presence reason

### Major Technical Debt

**A1 — Cross-runtime coupling:** CA's `skill_adapters.py` imports SkillExecutor classes from RWA, CVA, and EPA runtimes. No interface contract enforcement exists. Signature changes in source runtimes fail silently in CA with no schema-level warning.

**A3 — Scorecard compiler unwired:** `scorecard_compiler.py` is 181 lines of functional code that cannot be invoked by CA's ASSEMBLING_PACKAGE state. The code exists; the wiring does not.

**A4 — Layer boundary violation:** `claims_linter.py` is an evaluation tool (`evaluations/scripts/`) imported at runtime by production orchestrators (RWA, CA). Evaluation tools should not be runtime dependencies of production agents.

**T1 — RWA has no dedicated test suite:** 969-line orchestrator; Mode A/B; 3-concurrent-job rate limiter; 2 approval gates. Only 2 tests exist, both failure-path only.

**T2 — CA tests never execute real adapters:** All 205 CA tests use lambda overrides to mock skill outputs. The adapter chain crossing RWA, CVA, and EPA runtimes is never exercised.

**T5 — Certifier grants L4 without evidence:** Current check: skills + workflows + baselines + non-empty directory = L4. Grants L4 to CA (~L2.5 by AGENT.md) and RWA (Prototype) without any test verification.

**D1 — governance-assessment-workflow.md is stale:** Specifies 4-skill chain (RM → GCM → ISO → ECV). CA implements 6-skill chain (RM → GCM → ESM → ISO → CapVal → ProposalReview) with different ordering.

**D3 — RWA L4A fixture missing:** `evaluations/test-cases/regulatory-subjects/minimal-risk-internal-tool.md` is cited as a P1 requirement in `AGENT.md` but does not exist.

### Major Missing Components

1. RWA dedicated test suite (Mode A happy path, Mode B, all approval gates)
2. CA 6-skill end-to-end integration test with real data through real adapters
3. ethana-solution-mapping test fixtures (0 exist; minimum 3 required)
4. ethana-feature-mapping standalone test fixtures
5. scorecard_compiler.py wired into CA ASSEMBLING_PACKAGE
6. Certifier upgrade to require test evidence for L4

---

## Target Definition

### v1 Internal Tool

Governance OS v1 Internal Tool is achieved when:

1. **All six agents achieve genuine L4 readiness** — each agent has a passing test suite exercising happy-path execution and all major failure modes; the agent certifier correctly reflects this based on test evidence, not directory presence
2. **Full Client Assessment workflow executes end-to-end** — a complete CA run from intake through COMPLETE with real data flowing through all 6 skills via real adapters, producing all 12 output artifacts
3. **Executive Assessment Package successfully generated** — all 12 defined artifacts assembled by the CA orchestrator ASSEMBLING_PACKAGE state, including the client scorecard produced by `scorecard_compiler.py`
4. **Human approval gates operational** — all 4 CA approval gates and all agent-level approval gates (2 in RWA, 2 in IIA, 1 in EPA, 1 in CVA, 1 in GRA) function correctly with state persisted to disk across approval transitions
5. **Claims Firewall enforced across all workflows** — zero-tolerance capability claim checking active in all production agent runtimes, verified by `claims_linter.py` against `canonical-product-model.md`

v1 Internal Tool explicitly excludes: REST API, web portal, multi-tenancy, LLM-backed execution, approval notification infrastructure (Slack/email), and Client Memory persistence (tiers 2/3). These belong to Phase C and Phase D.

---

## Roadmap

### PR-008 — Regulatory Watch Agent L4 Certification

**Objective:** Convert RWA from Prototype to genuine L4. Create the first dedicated RWA test suite exercising Mode A happy paths, all gate failure modes, both approval gates, Mode B basic operation, and Claims Firewall integration via `start_run`.

**Dependencies:** None. Ready for implementation immediately.

**Deliverables:**

- `evaluations/scripts/test_regulatory_watch_runtime.py` — 34 tests across 2 classes
  - `TestRegulatoryWatchRuntimeModeA` (28 tests): 5 intake validation, 3 Mode A happy paths (EU BFSI, India DPDP, UK Insurance), 1 package file verification, Gate 1/2/3a/3b/4 failure paths, both approval gate failure paths, AG-2 re-gate (clean modifications), partial package release, state guard assertions
  - `TestRegulatoryWatchRuntimeModeB` (6 tests): affected run identification, 3-run concurrency cap, empty result, missing field error, change summary addendum, Annex III prioritisation
- `evaluations/test-cases/regulatory-subjects/minimal-risk-internal-tool.md` — L4A fixture (HR scheduling tool, EU only, no BFSI keywords); closes the L4A blocker in `AGENT.md`

**Success Criteria** (from `docs/decisions/PR-008-regulatory-watch-agent-l4-readiness.md`):

- L4A: `minimal-risk-internal-tool.md` present; `regression_tester.py` passes on all 3 subject fixtures; `claims_linter.py` passes on all 3 gold standards
- L4B: already satisfied — all runtime files present, all 24 states implemented, gates call `claims_linter.py` and `schema_validator`, `config.yaml` exposes all thresholds
- L4C: 34 passing tests; all 3 Mode A fixture profiles reach `COMPLETE`; Mode B enforces 3-run cap; Claims Firewall (Gate 3b) correctly halts via `start_run` flow; 13 major halt states reached in test assertions

**No existing files modified.** `test_firewall_hardening.py` (9 tests) preserved intact.

**Estimated effort:** 3–4 days.

**Status:** Ready for implementation.

---

### PR-009 — Documentation and Schema Repairs

**Objective:** Eliminate stale documentation that misrepresents the current system and fix the one remaining test suite defect (CONFORMANT_FMO `markdown_output`).

**Dependencies:** None. Runs in parallel with PR-008.

**Deliverables:**

- **CONFORMANT_FMO fixture repair** — add `markdown_output` field to `CONFORMANT_FMO` in `test_feature_mapping_proposal_review_integration.py`; resolves the 1 remaining genuine test failure from PR-007 (from current 281/282 to 282/282 passing)
- **`governance-assessment-workflow.md` update** — replace the stale 4-skill chain (RM → GCM → ISO → ECV) with the actual 6-skill chain (RM → GCM → ESM → ISO → CapVal → ProposalReview); align workflow steps with CA's `skill_adapters.py` implementation
- **GRA `AGENT.md`** — create the missing specification document for the most-tested agent; define: scope, input/output contracts, 3-fixture test corpus, memory model, escalation rules, retry policy, certification level
- **CA `AGENT.md` cleanup** — update stale blockers: B-01 (`scorecard_compiler.py` is not a stub — it is 181 lines of functional code); B-04/B-05 (certifier bugs appear resolved in current code); align Section 14 blockers with actual current state

**Estimated effort:** 2–3 days.

**Status:** Pending. No prerequisites.

---

### PR-010 — Fixture Expansion

**Objective:** Close the zero-fixture gap for `ethana-solution-mapping` and `ethana-feature-mapping`. Both skills have deterministic executors with meaningful scoring logic; neither has test fixtures to validate output quality.

**Dependencies:** PR-009 (governance-assessment-workflow.md update clarifies the CA chain; understanding the chain is a prerequisite for writing good fixtures).

**Deliverables:**

- **`ethana-solution-mapping` test fixtures (minimum 3):**
  - Fixture 1: EU BFSI full coverage — high CCS score, Ethana control suite fully matched
  - Fixture 2: India DPDP partial coverage — mixed CCS band, coverage gaps identified
  - Fixture 3: UK Insurance low coverage — below CCS threshold, commercial motion = Pilot
  - Each fixture: input (from prior RM+GCM output), expected output (structured JSON per `solution_mapping_output.json` schema), baseline entry in `evaluations/baselines/ethana-solution-mapping/`

- **`ethana-feature-mapping` test fixtures (minimum 3):**
  - Fixture 1: high TFS score — all features validated, production-ready integration paths
  - Fixture 2: mixed TFS — partial validation, some features require POC
  - Fixture 3: low TFS — multiple features fail validation, TFS below threshold
  - Each fixture: input, expected output (per `feature_mapping_output.json` schema), baseline entry in `evaluations/baselines/ethana-feature-mapping/`

- **Fixture validation:** run `regression_tester.py` against all new fixtures against their respective structure baselines; run `claims_linter.py` on all fixture markdown outputs

**Estimated effort:** 3–4 days.

**Status:** Pending. Blocked on PR-009.

---

### PR-011 — Scorecard Compiler Integration

**Objective:** Wire `scorecard_compiler.py` into the CA orchestrator `ASSEMBLING_PACKAGE` state so that a complete CA run produces the client scorecard as part of the Executive Assessment Package.

**Dependencies:** PR-010 (solution-mapping fixtures provide the inputs that flow through to the scorecard; end-to-end integration test requires all fixture coverage to be in place first).

**Deliverables:**

- **ASSEMBLING_PACKAGE integration** — call `scorecard_compiler.py` from the CA orchestrator `ASSEMBLING_PACKAGE` state; pass all 6 skill outputs (Skill 1–6 JSON payloads) as inputs; write the resulting scorecard JSON to the package directory alongside the other 11 artifacts
- **Scorecard generation validation** — verify the scorecard JSON is produced and schema-conformant for at least one complete CA run using EU BFSI test data
- **Package assembly validation** — verify all 12 defined artifacts exist in the package directory after a complete CA run: regulatory scoping matrix, control spec, ISO gap assessment, solution mapping report, feature validation table, proposal review report, client scorecard, plus associated JSON payloads and a README

**Estimated effort:** 2–3 days.

**Status:** Pending. Blocked on PR-010.

---

### PR-012 — Certifier Upgrade

**Objective:** Make the agent certifier's L4 certification evidence-based. The current certifier grants L4 for any non-empty agent directory. After PR-012, L4 requires a passing test file to exist for the agent.

**Dependencies:** PR-008 (RWA must have a test file before the upgraded certifier checks for one). Effectively requires all other PRs to be complete so that CA also has adequate test coverage before the stricter check is applied.

**Deliverables:**

- **Test existence check** — for L4 certification, require that a test file exists in `evaluations/scripts/` whose name matches `test_{agent_slug}_runtime.py`; if absent, certifier outputs L3 regardless of other checks
- **Pass-rate validation** — run the test file via subprocess and verify zero failures; if any test fails, certifier outputs warning with failing test count
- **Certifier summary message fix** — correct the summary message bug that reports incorrect status for some agents
- **Certification integrity verification** — after PR-012, run certifier against all 6 agents: CVA, IIA, EPA, GRA should report L4 (test files exist and pass); RWA should report L4 (test file created in PR-008 passes); CA should report L4 if end-to-end integration test was added in PR-011, or L3 if not yet present

**Estimated effort:** 2–3 days.

**Status:** Pending. Effectively depends on PR-008 through PR-011.

---

## Critical Path

```
PR-008 (RWA test suite)
  ↓
  ↓ [Parallel: PR-009 — documentation repairs, runs alongside PR-008]
  ↓
PR-010 (fixture expansion: solution-mapping + feature-mapping)
  ↓
PR-011 (scorecard integration: wire scorecard_compiler into CA)
  ↓
PR-012 (certifier upgrade: evidence-based L4)
  ↓
CA End-to-End Validation
(one complete CA run with real EU BFSI data through all 6 real adapters)
  ↓
Governance OS v1 Internal Tool
```

**Parallel execution opportunity:**
- PR-008 and PR-009 share no files and can be implemented simultaneously
- PR-012 certifier upgrade logic can be designed in parallel with PR-010 and PR-011; only final execution waits on PR-008

**Estimated total calendar time:** 5–6 focused development weeks

| Phase | Duration | Work |
|---|---|---|
| Week 1 | PR-008 + PR-009 in parallel | RWA test suite (34 tests), minimal-risk fixture, doc repairs, CONFORMANT_FMO fix |
| Week 2 | PR-010 | 3 solution-mapping fixtures + 3 feature-mapping fixtures |
| Week 3 | PR-011 | Scorecard compiler wiring, package assembly validation |
| Week 4 | PR-012 | Certifier upgrade, pass-rate validation, summary fix |
| Weeks 5–6 | CA End-to-End | First complete CA run with real data, integration debugging, v1 validation |

---

## Risks

### CA Adapter-Chain Integration Risk

**Risk:** The CA 6-skill chain has never run end-to-end with real data. When it does, the adapter chain in `skill_adapters.py` imports SkillExecutor classes from RWA, CVA, and EPA runtimes. The actual inter-skill payload format — how RWA's `regulatory_mapping_output_json` maps into CA's inter-skill payload for Skill 2 — has never been validated by integration test.

**Specific failure modes:**
- RWA's SkillExecutor produces a `regulatory_mapping_output_json` structure that the CA GCM adapter does not correctly transform
- `solution_mapping_executor.py` receives GCM output that does not match its expected input format (no integration test covers this boundary)
- The adapter chain fails silently — no exception is raised but the inter-skill payload contains empty or malformed fields that propagate to ASSEMBLING_PACKAGE

**Mitigation:** PR-010 fixtures must be designed to exercise the real inter-skill boundary, not just the executor in isolation. The CA end-to-end integration test (post-PR-011) is the primary risk-discovery mechanism. Budget 2 weeks for the end-to-end test, not 1, to account for integration debugging.

**Likelihood:** High. The adapter chain imports from 3 separate runtimes with no contract enforcement.

**Impact:** Delays v1 by 1–3 weeks if integration failures require adapter refactoring.

### Scorecard Integration Risk

**Risk:** `scorecard_compiler.py` is implemented as a standalone CLI tool with its own argument parser (`--skill1` through `--skill6`). Wiring it into the CA orchestrator `ASSEMBLING_PACKAGE` state requires either calling it as a subprocess (fragile) or refactoring it to be importable as a module with a programmatic API. The current code was designed for CLI use; programmatic integration may require non-trivial changes.

**Specific failure modes:**
- Scorecard compiler arguments do not align with the keys available in the CA state at ASSEMBLING_PACKAGE
- Scorecard output JSON does not match the schema expected by the Executive Assessment Package structure
- Skills 3–6 (ESM, ISO, CapVal, ProposalReview) produce outputs that scorecard_compiler.py does not correctly score

**Mitigation:** Before PR-011 implementation begins, read `scorecard_compiler.py` lines 1–181 in full and map each `--skillN` argument to its corresponding CA state key. If the CLI-to-module refactor is non-trivial, create a thin wrapper function in PR-011 rather than a full refactor.

**Likelihood:** Medium. The code logic exists; the integration seam is the unknown.

**Impact:** Adds 3–5 days to PR-011 estimate if a wrapper layer is needed.

### Certifier Integrity Risk

**Risk:** After PR-012 upgrades the certifier to require test files, CA may fail the L4 check if the CA end-to-end integration test is not yet in place. The 205 existing CA tests use mocked skill outputs and do not count as genuine end-to-end coverage. PR-012 could force CA back to L3 on the certifier at exactly the moment when the program review claims v1 is complete.

**Mitigation:** PR-012 should be the last PR in the sequence, applied after the CA end-to-end test is written and passing. Do not merge PR-012 before the CA integration test exists in `evaluations/scripts/`.

**Likelihood:** Certain if ordering is wrong. Controlled entirely by PR sequence.

**Impact:** Blocks v1 certification milestone if ordering is violated.

### Claims Firewall Layer-Boundary Risk

**Risk:** `claims_linter.py` is imported at runtime by both RWA and CA orchestrators (Technical Debt A4). If `evaluations/scripts/` is ever restructured or the linter interface changes, production agent runtimes break at import time. This is a latent fragility that exists today and that every PR in the roadmap exercises.

**Mitigation:** For v1, accept the risk and document it in code. The correct fix (move claims_linter to a shared library) belongs to Phase B architecture hardening, not Phase A. Do not restructure the evaluations directory during any Phase A PR.

**Likelihood:** Low for v1 timeline. High if Phase B work is done out of sequence.

**Impact:** Could break all agent runtimes simultaneously if triggered.

---

## Definition of Done

Governance OS v1 Internal Tool is complete when all of the following are true:

### Agent Certification

- [ ] CVA reports genuine L4 — existing 3 tests pass; certifier confirms
- [ ] IIA reports genuine L4 — existing 5 tests pass; certifier confirms
- [ ] EPA reports genuine L4 — existing 15 tests pass; certifier confirms
- [ ] GRA reports genuine L4 — existing 45 tests pass; certifier confirms
- [ ] **RWA reports genuine L4** — 34 new tests pass (PR-008); regression suite passes; certifier (post-PR-012) confirms
- [ ] **CA reports genuine L4** — end-to-end integration test passes; scorecard generated; certifier (post-PR-012) confirms

### Test Suite Health

- [ ] All 282 tests pass (resolves the 1 remaining CONFORMANT_FMO defect via PR-009)
- [ ] `test_regulatory_watch_runtime.py` — 34 tests pass (PR-008)
- [ ] CA end-to-end integration test passes — at minimum 1 complete run with real EU BFSI data
- [ ] `agent_certifier.py` (post-PR-012) confirms L4 for all 6 agents based on test evidence

### Workflow Execution

- [ ] Complete CA run executes from intake through COMPLETE with real data through all 6 real adapters (no lambda mocks)
- [ ] Executive Assessment Package assembled: all 12 artifacts present in package directory
- [ ] Client scorecard JSON produced by `scorecard_compiler.py` and included in package
- [ ] All 4 CA approval gates transition correctly (state persists to disk across gate transitions)

### Claims Firewall

- [ ] Claims Firewall enforced at Gate 1 (RWA S1 output) — confirmed by test
- [ ] Claims Firewall enforced at Gate 3b (RWA S2 output) — confirmed by `test_gate_3b_firewall_breach_halts_firewall_breach`
- [ ] Claims Firewall enforced at AG-2 modifications re-gate (RWA) — confirmed by existing `TestApprovalModificationBypass`
- [ ] Claims Firewall enforced in CA Proposal Review step — confirmed by existing `TestClaimsLinterFinalVerification`
- [ ] `claims_linter.py` passes on all 3 gold standard documents

### Documentation

- [ ] `governance-assessment-workflow.md` reflects the actual 6-skill CA chain
- [ ] GRA `AGENT.md` exists and documents scope, contracts, and certification level
- [ ] CA `AGENT.md` stale blockers (B-01, B-04, B-05) corrected
- [ ] `reviews/governance-os-master-status.md` updated: RWA and CA moved from "Partial Agents" to "Complete Agents"

### No Open Blockers from Program Review

Program Review technical debt items that must be resolved before v1:
- [x] A2 — Dual naming convention (acknowledged; accepted for v1; targeted for Phase B)
- [ ] A3 — `scorecard_compiler.py` not integrated (resolved by PR-011)
- [ ] D1 — `governance-assessment-workflow.md` stale (resolved by PR-009)
- [ ] D3 — RWA minimal-risk fixture missing (resolved by PR-008)
- [ ] T1 — RWA has no dedicated test suite (resolved by PR-008)
- [ ] T5 — Certifier L4 check insufficient (resolved by PR-012)

Program Review items **deferred to Phase B** (not blockers for v1):
- A1 — Cross-runtime coupling via `skill_adapters.py` (Phase B: interface contract definition)
- A4 — `claims_linter.py` layer boundary violation (Phase B: move to shared library)
- A5 — GRA has no AGENT.md (partially resolved by PR-009; full specification is Phase B)
- A6 — CA state machine durable persistence (Phase C: Assessment Memory)
- T2 — CA adapter chain never tested with real data (resolved by CA end-to-end test, post-PR-011)
- T3 — No CA 6-skill integration test (resolved by CA end-to-end test, post-PR-011)
- P1–P4 — Deployment, notifications, memory, LLM (Phase C / Phase D)
