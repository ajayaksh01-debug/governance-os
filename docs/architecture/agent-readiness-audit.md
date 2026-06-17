# Agent Readiness Audit

**Date:** 2026-06-17  
**Scope:** Five candidate agents across skills/, workflows/, evaluations/, agents/, workflows/schemas/, evaluations/baselines/, evaluations/test-cases/  
**Status:** Audit-only. No agent files created.

---

## Executive Summary

| Agent | Certifier Level | True Readiness | Build Blocker |
|---|---|---|---|
| Regulatory Watch Agent | L3 | **80%** | Test fixtures missing; agent code not started |
| Incident Intelligence Agent | L2 | **68%** | ai-incident-analysis baseline directory missing; no test fixtures |
| Client Assessment Agent | L2 | **66%** | Stale workflow; scorecard compiler stub; baseline format mismatch; ethana-solution-mapping evaluation gap |
| Ethana Proposal Agent | **L0 (certifier bug)** | **63%** | Certifier name mismatch; stale workflow; mid-chain skill baselines missing |
| Capability Validation Agent | L2 | **40%** | No output schema; no baseline; no test fixtures — full evaluation layer absent |

**Agents that can begin building immediately:** Regulatory Watch Agent (L3 certified; only agent code is missing).

**Agents blocked by evaluation gaps:** Incident Intelligence, Client Assessment, Capability Validation.

**Agents blocked by certifier infrastructure bugs:** Ethana Proposal Agent (would be ~L2 if the bug were fixed).

**Critical infrastructure gap affecting all agents:** `agents/` directory is empty. No agent codebase has been started. The maximum achievable level without agent code is L3.

---

## Section 1 — Methodology

### Readiness Score Definition

The audit scores each agent across seven dimensions. The Readiness % in the Executive Summary is a weighted composite.

| Dimension | Weight | What passes |
|---|---|---|
| Skill chain complete | 30% | All required skills have SKILL.md, workflow.md, evaluation.md, examples.md |
| Workflow integration | 15% | Workflow file exists, references current (non-stale) skill names |
| Schemas | 15% | Input and/or output schemas exist for all skills in the chain |
| Baselines | 15% | Baseline exists in the format the certifier checks (`evaluations/baselines/{skill}/structure.json`) OR as the newer flat `.md` format |
| Test fixtures | 10% | `evaluations/test-cases/{skill}/` exists with at least one fixture per required skill |
| Evaluation gates | 10% | Relevant evaluation scripts (claims_linter.py, regression_tester.py, workflow_validator.py) are operational and certifier will pass |
| Agent codebase | 5% | `agents/{agent_name}/` directory exists with at least one implementation file |

### What the Certifier (`agent_certifier.py`) Actually Checks

The certifier checks four things in sequence:
1. **Level 0 → 1:** Do `skills/{skill_name}/SKILL.md` files exist for all required skills?
2. **Level 1 → 2:** Do required workflow `.md` files exist?
3. **Level 2 → 3:** Do `evaluations/baselines/{skill_name}/` **directories** exist for all required skills?
4. **Level 3 → 4:** Does `agents/{agent_name_lowercased}/` directory exist and contain files?

**Certifier does NOT check:**
- Whether test fixtures exist in `evaluations/test-cases/`
- Whether schemas exist in `workflows/schemas/`
- Whether baselines are accurate or complete
- Whether workflow files are current (stale "[FUTURE]" references are not detected)
- Whether evaluation scripts are runnable

### Known Certifier Bugs (Do Not Merge to Production Without Fixing)

| Bug | Effect |
|---|---|
| **Bug 1 — Skill name mismatch:** Certifier checks for skill `"proposal-review"` but the directory is `"ethana-proposal-review"` | Ethana Proposal Agent reports L0 (missing skill) when all required skills exist. False failure. |
| **Bug 2 — Baseline format mismatch:** Certifier checks for `evaluations/baselines/{skill}/` directories but newer baselines (`proposal-review-baseline.md`, `iso-42001-gap-assessment-baseline.md`) are flat `.md` files | iso-42001-gap-assessment and proposal-review baselines are invisible to the certifier. Agents depending on them report L2 rather than L3. False failures. |
| **Bug 3 — No schema check:** Certifier does not verify that `workflows/schemas/` contains the required input/output schemas for each skill | An agent can reach L3 with broken or missing schemas. |
| **Bug 4 — No fixture check:** Certifier does not verify test fixture existence in `evaluations/test-cases/` | An agent can reach L3 with zero test fixtures — the regression tests would simply fail at runtime. |

---

## Section 2 — Skills Inventory

All eight skills required by the five candidate agents exist and are complete (SKILL.md, workflow.md, evaluation.md, examples.md).

| Skill | Directory | Files complete | Output schema | Baseline format | Test fixtures |
|---|---|---|---|---|---|
| ai-incident-analysis | `skills/ai-incident-analysis/` | ✅ 4/4 | ✅ `incident_analysis_output.json` | ❌ No baseline directory | ❌ No fixtures |
| regulatory-mapping | `skills/regulatory-mapping/` | ✅ 4/4 | ✅ `regulatory_mapping_output.json` | ✅ `regulatory-mapping/structure.json` | ❌ No fixtures |
| governance-control-mapping | `skills/governance-control-mapping/` | ✅ 4/4 | ✅ `control_mapping_output.json` | ✅ `governance-control-mapping/structure.json` | ❌ No fixtures |
| ethana-capability-validation | `skills/ethana-capability-validation/` | ✅ 4/4 | ❌ **No output schema** | ❌ No baseline directory | ❌ No fixtures |
| ethana-solution-mapping | `skills/ethana-solution-mapping/` | ✅ 4/4 | ✅ `solution_mapping_output.json` | ❌ No baseline directory | ❌ No fixtures |
| ethana-feature-mapping | `skills/ethana-feature-mapping/` | ✅ 4/4 | ✅ `feature_mapping_output.json` | ❌ No baseline directory | ❌ No fixtures |
| ethana-proposal-review | `skills/ethana-proposal-review/` | ✅ 4/4 | ✅ `proposal-review-input.schema.json` + `proposal-review-output.schema.json` | ✅ `proposal-review-baseline.md` (flat format) | ✅ 3 fixtures |
| iso-42001-gap-assessment | `skills/iso-42001-gap-assessment/` | ✅ 4/4 | ✅ `iso-42001-gap-assessment-input.schema.json` + `iso-42001-gap-assessment-output.schema.json` | ✅ `iso-42001-gap-assessment-baseline.md` (flat format) | ✅ 3 fixtures |

**Key observation:** Only two skills (ethana-proposal-review and iso-42001-gap-assessment) have full evaluation infrastructure. The other six have output schemas but incomplete or absent baselines and zero test fixtures.

---

## Section 3 — Workflows Inventory

All five workflow files exist. Two contain stale placeholder text that pre-dates completed skills.

| Workflow file | Used by agent | Status | Stale content |
|---|---|---|---|
| `incident-assessment-workflow.md` | Incident Intelligence Agent | ✅ Current | None |
| `regulatory-compliance-workflow.md` | Regulatory Watch Agent | ✅ Current | None |
| `governance-assessment-workflow.md` | Client Assessment Agent | ⚠️ **Stale** | Step 4.2 reads "[FUTURE: ISO 42001 Gap Assessment]" — skill now exists |
| `ethana-solution-design-workflow.md` | Capability Validation Agent | ✅ Current | None |
| `proposal-development-workflow.md` | Ethana Proposal Agent | ⚠️ **Stale** | Step 4.5 reads "[FUTURE: Proposal Review]" — skill now exists |

---

## Section 4 — Schemas Inventory

| Schema file | Skill | Direction | Status |
|---|---|---|---|
| `incident_analysis_output.json` | ai-incident-analysis | Output | ✅ |
| `regulatory_mapping_output.json` | regulatory-mapping | Output | ✅ |
| `control_mapping_output.json` | governance-control-mapping | Output | ✅ |
| `solution_mapping_output.json` | ethana-solution-mapping | Output | ✅ |
| `feature_mapping_output.json` | ethana-feature-mapping | Output | ✅ |
| `proposal-review-input.schema.json` | ethana-proposal-review | Input | ✅ |
| `proposal-review-output.schema.json` | ethana-proposal-review | Output | ✅ |
| `iso-42001-gap-assessment-input.schema.json` | iso-42001-gap-assessment | Input | ✅ |
| `iso-42001-gap-assessment-output.schema.json` | iso-42001-gap-assessment | Output | ✅ |
| **`capability-validation-output.schema.json`** | ethana-capability-validation | Output | ❌ **Missing** |

**One schema gap:** `ethana-capability-validation` has no output schema. Every agent that consumes Capability Validation output (Incident Intelligence, Client Assessment, Ethana Proposal) cannot validate the handoff payload without it.

---

## Section 5 — Evaluations Inventory

### 5.1 Baselines

| Baseline | Format | Skill covered | Certifier sees it |
|---|---|---|---|
| `evaluations/baselines/regulatory-mapping/structure.json` | Directory + JSON | regulatory-mapping | ✅ Yes |
| `evaluations/baselines/governance-control-mapping/structure.json` | Directory + JSON | governance-control-mapping | ✅ Yes |
| `evaluations/baselines/proposal-review-baseline.md` | Flat .md | ethana-proposal-review | ❌ No (format mismatch) |
| `evaluations/baselines/iso-42001-gap-assessment-baseline.md` | Flat .md | iso-42001-gap-assessment | ❌ No (format mismatch) |
| `ai-incident-analysis` baseline | — | ai-incident-analysis | ❌ **Missing entirely** |
| `ethana-capability-validation` baseline | — | ethana-capability-validation | ❌ **Missing entirely** |
| `ethana-solution-mapping` baseline | — | ethana-solution-mapping | ❌ **Missing entirely** |
| `ethana-feature-mapping` baseline | — | ethana-feature-mapping | ❌ **Missing entirely** |

**Baseline format split:** Older skills use `evaluations/baselines/{skill}/structure.json`. Newer skills use `evaluations/baselines/{skill}-baseline.md`. The certifier only handles the older format. This creates an invisible false-negative state where newer baselines exist but the certifier cannot see them. Resolving this requires either: (a) migrating newer baselines to the directory/JSON format, or (b) updating the certifier to detect both formats.

### 5.2 Test Fixtures

| Test case directory | Fixtures present | Skills covered |
|---|---|---|
| `evaluations/test-cases/proposal-review/` | ✅ 3 (clean-proposal, firewall-breach, mixed-roadmap-claims) | ethana-proposal-review |
| `evaluations/test-cases/iso-42001-gap-assessment/` | ✅ 3 (bank-certification-readiness, fintech-extension-from-iso27001, greenfield-organisation) | iso-42001-gap-assessment |
| `evaluations/test-cases/incident-reports/` | ❌ **Missing entirely** | ai-incident-analysis |
| `evaluations/test-cases/regulatory-subjects/` | ❌ **Missing entirely** | regulatory-mapping |
| `evaluations/test-cases/gold-standards/` | ❌ **Missing entirely** | governance-control-mapping |

### 5.3 Evaluation Scripts

| Script | Status | Notes |
|---|---|---|
| `claims_linter.py` | ✅ Operational | Parses canonical-product-model.md; enforces Claims Firewall |
| `workflow_validator.py` | ✅ Operational | Validates JSON payloads against schemas; falls back to native engine if `jsonschema` not installed |
| `regression_tester.py` | ✅ Operational | Validates markdown structure against JSON baseline files; only handles JSON baselines, not `.md` baselines |
| `agent_certifier.py` | ⚠️ Operational with bugs | Runs correctly for levels 0-2 checks; bugs in level 3 check (baseline format) and level 0 check (Proposal Agent skill name) |
| `scorecard_compiler.py` | ❌ **Stub only** | Prints placeholder message; not implemented; needed by Client Assessment Agent to compile AMS/ARS/CCS into a unified client scorecard |

---

## Section 6 — Agent Profiles

---

### Agent 1: Regulatory Watch Agent

**Readiness: 80% — Highest readiness of the five candidates**

**Certifier output:** L3 — Skills, workflows, and structural evaluations complete. Ready for agent codebase implementation.

**What the certifier correctly identifies:** Both required skills (regulatory-mapping, governance-control-mapping) have SKILL.md files, the workflow file exists, and both `evaluations/baselines/{skill}/structure.json` directories exist. This is the only agent that passes L3.

**What the certifier does NOT catch:**
- No test fixtures in `evaluations/test-cases/regulatory-subjects/` — regression tests would error out at runtime
- No test fixtures in `evaluations/test-cases/gold-standards/` for governance-control-mapping
- `agents/regulatory_watch_agent/` directory does not exist

**Required skills:**

| Skill | Status |
|---|---|
| regulatory-mapping | ✅ Complete |
| governance-control-mapping | ✅ Complete |

**Required workflows:**

| Workflow | Status |
|---|---|
| `regulatory-compliance-workflow.md` | ✅ Current — no stale references |

**Required evaluations:**

| Item | Status |
|---|---|
| `evaluations/baselines/regulatory-mapping/structure.json` | ✅ Exists |
| `evaluations/baselines/governance-control-mapping/structure.json` | ✅ Exists |
| `evaluations/test-cases/regulatory-subjects/` | ❌ Missing — at least 3 fixtures required |
| `evaluations/test-cases/gold-standards/` | ❌ Missing — at least 1 fixture for GCM |

**Required schemas:**

| Schema | Status |
|---|---|
| `regulatory_mapping_output.json` | ✅ Exists |
| `control_mapping_output.json` | ✅ Exists |

**Blocking items (in priority order):**

1. Create test fixtures in `evaluations/test-cases/regulatory-subjects/` (minimum 3: BFSI high-risk, minimal-risk internal tool, multi-jurisdiction)
2. Create `agents/regulatory_watch_agent/` directory with implementation
3. Extend regression baseline for regulatory-mapping from structure-only JSON to include output range validation (currently the structure.json only validates headers, not content accuracy)

**Recommended build order position:** **Build first.** Only agent at L3. Lowest remaining dependency gap. Provides a tested agent build pattern for the remaining four agents.

---

### Agent 2: Incident Intelligence Agent

**Readiness: 68%**

**Certifier output:** L2 — Missing structural baseline in `evaluations/baselines/ai-incident-analysis/`.

**What is complete:** The skill chain (ai-incident-analysis → governance-control-mapping) is fully built. The workflow file is current and does not contain stale placeholder text. The output schema (`incident_analysis_output.json`) exists. The governance-control-mapping baseline exists.

**What is missing:**
- `evaluations/baselines/ai-incident-analysis/structure.json` — blocks certifier Level 3
- `evaluations/test-cases/incident-reports/` — no test fixtures exist for any known AI incident type
- `agents/incident_intelligence_agent/` directory does not exist

**Required skills:**

| Skill | Status |
|---|---|
| ai-incident-analysis | ✅ Complete |
| governance-control-mapping | ✅ Complete |

**Required workflows:**

| Workflow | Status |
|---|---|
| `incident-assessment-workflow.md` | ✅ Current |

**Required evaluations:**

| Item | Status |
|---|---|
| `evaluations/baselines/ai-incident-analysis/structure.json` | ❌ Missing — blocks certifier L3 |
| `evaluations/baselines/governance-control-mapping/structure.json` | ✅ Exists |
| `evaluations/test-cases/incident-reports/` | ❌ Missing — minimum 3 fixtures recommended |

**Required schemas:**

| Schema | Status |
|---|---|
| `incident_analysis_output.json` | ✅ Exists |
| `control_mapping_output.json` | ✅ Exists |

**Blocking items (in priority order):**

1. Create `evaluations/baselines/ai-incident-analysis/structure.json` — required headers and tables for a 10-section incident analysis output (unlocks certifier L3)
2. Create `evaluations/test-cases/incident-reports/` with minimum 3 fixtures: prompt-injection-incident.md (classification test), agent-failure-incident.md (BFSI severity test), supply-chain-model-incident.md (framework mapping test)
3. Create `agents/incident_intelligence_agent/` directory with implementation

**Recommended build order position:** **Build second.** One baseline creation unlocks L3. Incident intelligence has clear trigger semantics (SIEM alert or ticket), making the agent architecture simpler to define than assessment or proposal agents.

---

### Agent 3: Client Assessment Agent

**Readiness: 66%**

**Certifier output:** L2 — Missing baseline directories for `iso-42001-gap-assessment` and `ethana-solution-mapping`.

**Critical note on certifier output:** The iso-42001-gap-assessment baseline _does_ exist at `evaluations/baselines/iso-42001-gap-assessment-baseline.md` — it is a comprehensive document with per-fixture expected ranges, Claims Firewall verification blocks, and cross-fixture invariants. The certifier cannot see it because it checks for a directory, not a flat `.md` file. This is a certifier bug, not a real gap.

**What is complete:** The four-skill chain is fully built. All four output schemas exist. The iso-42001-gap-assessment skill has three test fixtures and a detailed baseline. The regulatory-mapping and governance-control-mapping baselines exist.

**What is missing:**
- Stale workflow: `governance-assessment-workflow.md` Step 4.2 labels iso-42001-gap-assessment as "[FUTURE: ISO 42001 Gap Assessment]" — the skill is now complete
- `ethana-solution-mapping` has no baseline (directory or flat file)
- `ethana-solution-mapping` has no test fixtures
- `scorecard_compiler.py` is a stub — the Client Assessment Agent is the only agent that needs to compile a multi-skill client scorecard (AMS + ARS + CCS → unified readiness report)
- `agents/client_assessment_agent/` directory does not exist

**Required skills:**

| Skill | Status |
|---|---|
| regulatory-mapping | ✅ Complete |
| iso-42001-gap-assessment | ✅ Complete with test fixtures + baseline |
| governance-control-mapping | ✅ Complete |
| ethana-solution-mapping | ✅ Complete |

**Required workflows:**

| Workflow | Status |
|---|---|
| `governance-assessment-workflow.md` | ⚠️ Stale — Step 4.2 references iso-42001 as "[FUTURE]" |

**Required evaluations:**

| Item | Status |
|---|---|
| `evaluations/baselines/regulatory-mapping/structure.json` | ✅ Exists |
| `evaluations/baselines/governance-control-mapping/structure.json` | ✅ Exists |
| `evaluations/baselines/iso-42001-gap-assessment-baseline.md` | ✅ Exists (flat format — certifier cannot detect) |
| `evaluations/baselines/ethana-solution-mapping/` | ❌ Missing entirely |
| `evaluations/test-cases/iso-42001-gap-assessment/` | ✅ 3 fixtures |
| `evaluations/test-cases/regulatory-subjects/` | ❌ Missing |
| `evaluations/test-cases/gold-standards/` | ❌ Missing |
| `scorecard_compiler.py` | ❌ Stub — implementation required |

**Required schemas:**

| Schema | Status |
|---|---|
| `regulatory_mapping_output.json` | ✅ Exists |
| `iso-42001-gap-assessment-input.schema.json` | ✅ Exists |
| `iso-42001-gap-assessment-output.schema.json` | ✅ Exists |
| `control_mapping_output.json` | ✅ Exists |
| `solution_mapping_output.json` | ✅ Exists |

**Blocking items (in priority order):**

1. Update `governance-assessment-workflow.md` Step 4.2 to reference the completed `iso-42001-gap-assessment` skill (remove "[FUTURE]" language)
2. Create `evaluations/baselines/ethana-solution-mapping/` directory with `structure.json` (or flat `.md` baseline with CCS scoring ranges) — required for certifier L3
3. Create `evaluations/test-cases/regulatory-subjects/` with minimum 3 fixtures for the regulatory-mapping skill
4. Implement `scorecard_compiler.py` to aggregate skill outputs into a unified client governance scorecard
5. Create `agents/client_assessment_agent/` directory with implementation
6. Optionally: Fix certifier to detect flat `.md` baselines so iso-42001 is counted

**Recommended build order position:** **Build fourth.** Most dependencies are present, but the scorecard compiler stub and stale workflow need attention before the agent architecture can be finalized. The agent's output (a unified governance scorecard) must be defined before implementation begins.

---

### Agent 4: Ethana Proposal Agent

**Readiness: 63%**

**Certifier output:** L0 — Missing required skill `"proposal-review"`.

**Critical note:** This is entirely a certifier bug. The certifier checks for `skills/proposal-review/SKILL.md` but the directory is `skills/ethana-proposal-review/`. The skill is fully implemented with test fixtures, schemas, and a comprehensive baseline. The true certifier level (if the bug were fixed) would be approximately L2, because the ethana-solution-mapping and ethana-feature-mapping baselines are missing.

**What is complete:** The five-skill commercial chain is fully built. Seven schemas exist (all 5 output schemas plus proposal-review input/output). The ethana-proposal-review skill has three calibrated test fixtures and a complete regression baseline. The claims_linter.py and regression_tester.py are operational for this skill chain.

**What is missing:**
- Certifier Bug 1: `"proposal-review"` vs `"ethana-proposal-review"` skill name mismatch — reports L0 falsely
- Stale workflow: `proposal-development-workflow.md` Step 4.5 labels proposal-review as "[FUTURE: Proposal Review]" — the skill is now complete
- `ethana-solution-mapping` has no baseline (directory or flat file)
- `ethana-feature-mapping` has no baseline (directory or flat file)
- `ethana-solution-mapping` has no test fixtures in `evaluations/test-cases/`
- `ethana-feature-mapping` has no test fixtures in `evaluations/test-cases/`
- `agents/ethana_proposal_agent/` directory does not exist

**Required skills:**

| Skill | Status |
|---|---|
| regulatory-mapping | ✅ Complete |
| governance-control-mapping | ✅ Complete |
| ethana-solution-mapping | ✅ Complete |
| ethana-feature-mapping | ✅ Complete |
| ethana-proposal-review | ✅ Complete with test fixtures + baseline |

**Required workflows:**

| Workflow | Status |
|---|---|
| `proposal-development-workflow.md` | ⚠️ Stale — Step 4.5 references proposal review as "[FUTURE]" |

**Required evaluations:**

| Item | Status |
|---|---|
| `evaluations/baselines/regulatory-mapping/structure.json` | ✅ Exists |
| `evaluations/baselines/governance-control-mapping/structure.json` | ✅ Exists |
| `evaluations/baselines/proposal-review-baseline.md` | ✅ Exists (flat format — certifier cannot detect) |
| `evaluations/baselines/ethana-solution-mapping/` | ❌ Missing |
| `evaluations/baselines/ethana-feature-mapping/` | ❌ Missing |
| `evaluations/test-cases/proposal-review/` | ✅ 3 fixtures |
| `evaluations/test-cases/ethana-solution-mapping/` | ❌ Missing |
| `evaluations/test-cases/ethana-feature-mapping/` | ❌ Missing |

**Required schemas:**

| Schema | Status |
|---|---|
| `regulatory_mapping_output.json` | ✅ Exists |
| `control_mapping_output.json` | ✅ Exists |
| `solution_mapping_output.json` | ✅ Exists |
| `feature_mapping_output.json` | ✅ Exists |
| `proposal-review-input.schema.json` | ✅ Exists |
| `proposal-review-output.schema.json` | ✅ Exists |

**Blocking items (in priority order):**

1. Fix certifier Bug 1: change `"proposal-review"` to `"ethana-proposal-review"` in `agent_certifier.py` (one-line fix — unblocks L0 → L2 jump immediately)
2. Update `proposal-development-workflow.md` Step 4.5 to reference the completed `ethana-proposal-review` skill
3. Create `evaluations/baselines/ethana-solution-mapping/` and `evaluations/baselines/ethana-feature-mapping/` directories with `structure.json` files — unblocks certifier L3 (after Bug 1 is fixed)
4. Create test fixtures for ethana-solution-mapping (minimum 3: BFSI high-risk, general enterprise, competitive-context) and ethana-feature-mapping (minimum 3: POC scoping, substitution analysis, technical RFI)
5. Create `agents/ethana_proposal_agent/` directory with implementation

**Recommended build order position:** **Build third.** The richest evaluation infrastructure in the repository is already in place for the terminal skill (ethana-proposal-review). One certifier line-change transforms the certifier from L0 to L2 immediately. Mid-chain evaluation gaps (solution-mapping, feature-mapping) need baselines but those are mechanical compared to designing new skills.

---

### Agent 5: Capability Validation Agent

**Readiness: 40% — Most blocked agent**

**Certifier output:** L2 — Missing structural baseline in `evaluations/baselines/ethana-capability-validation/`.

**What is complete:** The single required skill (ethana-capability-validation) is fully built with a comprehensive 9-section output spec, ECS/CPL scoring framework, and knowledge dependency tiers. No workflow file is required (the certifier spec notes it "executes on CPM commits directly"). Both conditions for Level 2 are satisfied.

**What is missing — in full:**
- No output schema for `ethana-capability-validation` — this is the only skill in the repository without one. Every downstream agent (Incident Intelligence via validation step, Ethana Solution Design workflow Step 4.1) consumes this output without schema validation
- No baseline in any format (directory or flat file)
- No test fixtures in any format
- The certifier check for baselines fails, blocking Level 3
- `agents/capability_validation_agent/` directory does not exist

**Why this is the most blocked:** The Capability Validation skill is the truth gate for all commercial claims. It is invoked in three workflows (incident-assessment, ethana-solution-design, governance-assessment). Despite being foundational to the entire claims integrity architecture, it has less evaluation infrastructure than any other skill. A Capability Validation Agent running without a calibrated baseline is structurally unvalidated — it can produce incorrect ECS or CPL assignments without detection.

**Required skills:**

| Skill | Status |
|---|---|
| ethana-capability-validation | ✅ Complete |

**Required workflows:**

| Workflow | Status |
|---|---|
| None — certifier spec: operates directly on canonical-product-model.md commits | ✅ N/A |

**Required evaluations:**

| Item | Status |
|---|---|
| `evaluations/baselines/ethana-capability-validation/structure.json` | ❌ Missing — blocks certifier L3 |
| `evaluations/test-cases/capability-validation/` | ❌ Missing — minimum 4 fixtures required |

**Recommended test fixtures (not yet created):**

| Fixture | Tests |
|---|---|
| `production-capability-clean.md` | Single Production capability; ECS 85+; CPL-1 claim |
| `in-build-capability.md` | In Build capability cited in a formal proposal; HD triggered |
| `source-conflict.md` | Marketing playbook claims Production; canonical model says In Build; contradiction log |
| `scope-expansion.md` | Canonical model entry is silent on a specific scope claim; CPL-4 maximum |

**Required schemas:**

| Schema | Status |
|---|---|
| `capability-validation-output.schema.json` | ❌ **Missing — only skill without an output schema** |

The output schema must include at minimum: `capability_name`, `validated_status` (enum: Production/In Build/Aspirational/Unresolved), `ecs` (number 0-100), `claim_permission_level` (enum: CPL-1 through CPL-5), `escalation_required` (boolean).

**Blocking items (in priority order):**

1. Create `workflows/schemas/capability-validation-output.schema.json` — required fields: capability_name, validated_status, ecs, cpl (array of {claim_text, cpl_level, permitted_contexts}), escalation_required, contradictions_found
2. Create `evaluations/baselines/ethana-capability-validation/structure.json` — required headers for 9-section output (unlocks certifier L3)
3. Create `evaluations/test-cases/capability-validation/` with 4 fixtures (production-clean, in-build, source-conflict, scope-expansion)
4. Create `agents/capability_validation_agent/` directory with implementation

**Recommended build order position:** **Build fifth (last).** The evaluation layer must be built before the agent, and the schema must be defined before the evaluation layer. The ECS and CPL scoring model is the most sophisticated in the repository — the baseline and test fixtures require careful calibration against examples.md to prevent drift. Rush-building this agent without a proper evaluation layer creates structural risk across the entire skill chain that depends on it.

---

## Section 7 — Missing Dependencies Summary

### Required Schemas (not yet created)

| Schema | Required by | Priority |
|---|---|---|
| `capability-validation-output.schema.json` | Capability Validation Agent; all agents consuming Capability Validation output | P1 — Critical |

### Required Baselines (not yet created)

| Baseline | Format recommendation | Required by | Priority |
|---|---|---|---|
| `evaluations/baselines/ai-incident-analysis/structure.json` | Directory + JSON (certifier-compatible) | Incident Intelligence Agent | P1 |
| `evaluations/baselines/ethana-capability-validation/structure.json` | Directory + JSON | Capability Validation Agent | P1 |
| `evaluations/baselines/ethana-solution-mapping/structure.json` | Directory + JSON | Client Assessment Agent, Ethana Proposal Agent | P2 |
| `evaluations/baselines/ethana-feature-mapping/structure.json` | Directory + JSON | Ethana Proposal Agent | P2 |

**Note on baseline format consolidation:** The two existing flat `.md` baselines (`proposal-review-baseline.md`, `iso-42001-gap-assessment-baseline.md`) are richer documents than the existing JSON `structure.json` files — they contain content calibration guidance, cross-fixture invariants, and Claims Firewall verification blocks that the JSON format cannot represent. Two options:
- **Option A:** Extend the certifier to also accept flat `.md` baselines (check for `{skill}-baseline.md` in addition to `{skill}/structure.json`). Recommended.
- **Option B:** Migrate the flat `.md` baselines into directory format. Loses richness without rework.

### Required Test Fixtures (not yet created)

| Directory | Minimum fixtures needed | Priority |
|---|---|---|
| `evaluations/test-cases/incident-reports/` | 3 (prompt-injection, agent-failure, supply-chain) | P1 |
| `evaluations/test-cases/regulatory-subjects/` | 3 (BFSI multi-jurisdiction, minimal-risk internal, regulatory-change trigger) | P1 |
| `evaluations/test-cases/gold-standards/` | 1+ for governance-control-mapping | P2 |
| `evaluations/test-cases/capability-validation/` | 4 (production-clean, in-build, source-conflict, scope-expansion) | P2 |
| `evaluations/test-cases/ethana-solution-mapping/` | 3 (BFSI, general enterprise, competitive) | P2 |
| `evaluations/test-cases/ethana-feature-mapping/` | 3 (POC scoping, substitution, technical RFI) | P2 |

### Required Evaluation Gates (not yet operational)

| Gate | Current state | Required action |
|---|---|---|
| `scorecard_compiler.py` | Stub — prints placeholder | Implement to compile ECS, TFS, CCS, AMS, ARS into unified client scorecard |
| Certifier Bug 1 fix | Ethana Proposal Agent mislabelled L0 | Change `"proposal-review"` → `"ethana-proposal-review"` in agent_certifier.py |
| Certifier baseline format | Flat `.md` baselines invisible to certifier | Add `.md` baseline detection to certifier |
| Stale workflow: governance-assessment-workflow.md | Step 4.2 reads "[FUTURE]" | Replace placeholder with actual iso-42001-gap-assessment skill reference |
| Stale workflow: proposal-development-workflow.md | Step 4.5 reads "[FUTURE]" | Replace placeholder with actual ethana-proposal-review skill reference |

---

## Section 8 — Recommended Build Order

Build order is determined by: certifier level, number of blocking items, agent architecture simplicity, and whether the agent unlocks downstream agents.

### Phase 1 — Immediate (can begin now)

**Regulatory Watch Agent**

Certifier status: L3. Only remaining gap is agent code and test fixtures. Build this agent first to establish the agent implementation pattern for the repository. The regulatory-mapping → governance-control-mapping skill chain is fully evaluated and schema-validated. Once the test fixtures are created, this agent becomes the repository's first fully certified (L4) agent.

**Prerequisite work before agent code:**
- Create `evaluations/test-cases/regulatory-subjects/` with 3 fixtures
- Create `evaluations/test-cases/gold-standards/` with at least 1 GCM fixture

### Phase 2 — Near-term (1-2 infrastructure items each)

**Incident Intelligence Agent**

One baseline directory creation unlocks certifier L3. Test fixtures exist as a clear template (use the 5 existing `knowledge/ai-incidents/` files as fixture sources). This agent has the clearest trigger semantics (SIEM alert → analysis → remediation package) which simplifies the agent architecture design.

**Prerequisite work before agent code:**
- Create `evaluations/baselines/ai-incident-analysis/structure.json`
- Create `evaluations/test-cases/incident-reports/` with 3 fixtures drawn from `knowledge/ai-incidents/`

**Ethana Proposal Agent**

One certifier line-fix (skill name) transforms this from L0 to the most evaluation-mature agent in the repository. The terminal skill (ethana-proposal-review) has the most complete evaluation infrastructure of any skill. Stale workflow update and two baseline directories complete the gap.

**Prerequisite work before agent code:**
- Fix certifier Bug 1 (one line)
- Update `proposal-development-workflow.md` Step 4.5
- Create `evaluations/baselines/ethana-solution-mapping/structure.json`
- Create `evaluations/baselines/ethana-feature-mapping/structure.json`

### Phase 3 — Medium-term (multiple dependencies)

**Client Assessment Agent**

The iso-42001-gap-assessment skill (the primary differentiator for this agent) is complete with full evaluation infrastructure. The main blockers are the stale workflow, missing ethana-solution-mapping evaluation baseline, and the scorecard_compiler.py stub. This agent's output (a unified client governance scorecard combining AMS, ARS, and CCS into a single readiness report) requires the scorecard compiler to be defined and implemented before the agent architecture can be finalised.

**Prerequisite work before agent code:**
- Update `governance-assessment-workflow.md` Step 4.2 (remove "[FUTURE]" language)
- Create `evaluations/baselines/ethana-solution-mapping/structure.json`
- Implement `scorecard_compiler.py`
- Create `evaluations/test-cases/regulatory-subjects/` (if not completed in Phase 1)

### Phase 4 — Final (requires full evaluation layer first)

**Capability Validation Agent**

This agent cannot be built responsibly until its evaluation layer is complete. The ECS and CPL scoring logic is the most nuanced in the repository — a miscalibrated Capability Validation Agent produces errors that propagate downstream into every commercial output. Build the output schema, the baseline, and all four test fixtures first. Run manual calibration against examples.md. Only then design the agent implementation.

**Prerequisite work before agent code:**
- Create `workflows/schemas/capability-validation-output.schema.json`
- Create `evaluations/baselines/ethana-capability-validation/structure.json`
- Create all 4 test fixtures in `evaluations/test-cases/capability-validation/`

---

## Section 9 — Runtime Architecture Recommendation

### Current architecture assumption

All five workflow files define Human Approval points — typically 2 per workflow. These are non-optional: the workflows halt and require sign-off before proceeding to the next step. This means none of the five agents should be designed as fully autonomous end-to-end executors. They are **orchestration agents with human-in-the-loop gates** at defined checkpoints.

### Recommended agent architecture: Sequential Orchestrator with Approval Gates

```
[Trigger: SIEM alert / CRM opportunity / Client onboarding event]
                │
                ▼
    [Intake Agent: validate inputs against schema]
                │
                ▼
    [Skill 1 execution: structured output]
                │
                ▼
    [Human Approval Gate 1: Cursory practitioner reviews]
                │
    ┌──────────────────────────────────┐
    │ Approve │ Reject (back to Skill 1)│
    └──────────────────────────────────┘
                │
                ▼
    [Skill 2 execution: consumes Skill 1 output]
                │
                ▼
    [Human Approval Gate 2: Director / DPO sign-off]
                │
                ▼
    [Structured output serialized to schema]
                │
                ▼
    [claims_linter.py + workflow_validator.py automated gates]
                │
                ▼
    [Deliver output package]
```

### Three specific architectural decisions

**Decision 1 — Claims Firewall at the runtime layer, not just the skill layer.**

The `claims_linter.py` script currently runs offline against a markdown file. For agents, it should be integrated as a runtime gate invoked automatically after any skill that produces Ethana capability references (governance-control-mapping Section 10, ethana-solution-mapping Section 3, ethana-proposal-review Section 8). The agent must not proceed to the next skill if the linter fails.

**Decision 2 — Schema-validated inter-skill payload passing.**

The `workflow_validator.py` should be invoked between every skill transition — after Skill N produces its output JSON, before Skill N+1 consumes it. This prevents a malformed or incomplete upstream output from silently producing a corrupted downstream output. All 9 schemas currently in `workflows/schemas/` make this feasible for all five workflows.

**Decision 3 — Separate agent roles for intake, orchestration, and output.**

Each agent should decompose into three roles:
- **Intake sub-agent:** Validates inputs against the skill's input schema, determines input completeness rating, and routes to the correct execution path (full vs. condensed assessment)
- **Orchestration sub-agent:** Sequences skill invocations, manages inter-skill payload passing, invokes the claims linter and schema validator at transition points, presents findings to human approval gates
- **Output sub-agent:** Serializes the final structured output to the relevant schema, generates the human-readable document, and triggers downstream notifications

This decomposition means the Regulatory Watch Agent (the simplest chain) can be built with a minimal orchestrator, while the Ethana Proposal Agent (five skills, seven schemas, three approval gates) uses the full three-role pattern.

### Infrastructure gap that blocks all runtime agents

`scorecard_compiler.py` is the only evaluation script that is a stub. This script is needed by the Client Assessment Agent to aggregate multi-skill outputs (AMS from iso-42001, CCS from ethana-solution-mapping, gap register from governance-control-mapping) into a single client governance scorecard. Without it, the Client Assessment Agent's output cannot be automatically validated for structural completeness. All other agents can proceed without it.

---

## Appendix — Certifier Output at Audit Date

```
==================================================
         Agent Readiness Certification Report
==================================================

* Incident Intelligence Agent [Status: L2]
  Details: Skills & workflows complete, but missing structural baselines
           in evaluations/baselines/ for: ['ai-incident-analysis']

* Regulatory Watch Agent [Status: L3]
  Details: Skills, workflows, and structural evaluations complete.
           Ready for agent codebase implementation.

* Capability Validation Agent [Status: L2]
  Details: Skills & workflows complete, but missing structural baselines
           in evaluations/baselines/ for: ['ethana-capability-validation']

* Client Assessment Agent [Status: L2]
  Details: Skills & workflows complete, but missing structural baselines
           in evaluations/baselines/ for: ['iso-42001-gap-assessment',
           'ethana-solution-mapping']

* Ethana Proposal Agent [Status: L0]
  Details: Missing required skills: ['proposal-review']
  NOTE: This is a certifier bug. The skill directory is 'ethana-proposal-review'.
        True level is approximately L2.

==================================================
Certification Status: BLOCKED (One or more agents lack required
                               skills/workflows).
```
