# Next Skill Prioritization Analysis

**Date:** 2026-06-17  
**Scope:** Post-implementation state assessment — workflow implementation, governance-control-mapping, ADR creation, audit consolidation, and authority cleanup complete.  
**Decision:** Choose between `ethana-proposal-review` and `iso-42001-gap-assessment` as the next skill to implement.

---

## 1. Recommendation

**Build `ethana-proposal-review` next.**

`iso-42001-gap-assessment` serves a valuable secondary workflow but is not architecturally critical at this stage. `ethana-proposal-review` is the terminal enforcement gate for the Claims Firewall, is mandated by an accepted ADR, carries an explicit architecture score deduction, and is the sole blocker for the highest-value commercial agent in the repository.

---

## 2. Repository State at Decision Point

The following layers are fully complete as of this assessment:

| Layer | Status |
|---|---|
| Knowledge base | Complete |
| Canonical product model | Complete — single authority (`canonical-product-model.md`) |
| Skills (Phase 1) | Complete — 6 active skills: `ai-incident-analysis`, `regulatory-mapping`, `ethana-capability-validation`, `ethana-solution-mapping`, `ethana-feature-mapping`, `governance-control-mapping` |
| Workflow documentation | Complete — 5 workflows in `workflows/` |
| Evaluation layer (Phase 1) | Complete — scripts, baselines for 2 skills, schemas |
| ADRs | Complete — ADR-001 through ADR-005, all accepted |
| Audit consolidation | Complete — 3 canonical audits in `docs/audits/` |
| Authority cleanup | Complete — deprecated status files archived |

Two skills remain unimplemented: `ethana-proposal-review` and `iso-42001-gap-assessment`.

---

## 3. Dependency Analysis

### 3.1 `ethana-proposal-review`

**Upstream dependencies (all satisfied):**

```
regulatory-mapping           [COMPLETE]
        │ Section 6
        ▼
governance-control-mapping   [COMPLETE]
        │ Technical control specs
        ▼
ethana-solution-mapping      [COMPLETE]
        │ Section 3 + CCS
        ▼
ethana-feature-mapping       [COMPLETE]
        │ Section 1 + TFS
        ▼
ethana-capability-validation [COMPLETE]
        │ Section 4 + CPL
        ▼
[ethana-proposal-review]     ← MISSING
```

Every upstream input to `ethana-proposal-review` is implemented. The skill has zero blocking dependencies — it can be built immediately.

**Downstream dependencies:** None. This is the terminal gate of the commercial chain.

**Workflow position:** Step 4.5 of `proposal-development-workflow.md` — the final step. Without it, the pipeline cannot produce a Release Audit Certificate or a Release Classification verdict. The four preceding steps run, but their output exits the pipeline without a compliance gate.

**ADR mandate:** ADR-005 (accepted) establishes this skill as mandatory and non-bypassable. The decision was made at the architectural level; the skill is the implementation artefact that fulfills it. No equivalent ADR exists for `iso-42001-gap-assessment`.

**Architecture score impact:** `repository-readiness-review.md` §1.1 attributes a **-10 point deduction** to the absence of this skill, explicitly identified as a primary architectural deficiency.

---

### 3.2 `iso-42001-gap-assessment`

**Upstream dependencies (all satisfied):**

```
regulatory-mapping           [COMPLETE]
        │ Section 2 (Applicable Governance Frameworks)
        ▼
[iso-42001-gap-assessment]   ← MISSING
        │ Gap register
        ▼
governance-control-mapping   [COMPLETE]
        │ Maturity roadmap
        ▼
ethana-capability-validation [COMPLETE]
        ▼
[Client Governance Audit Binder]
```

One upstream dependency (regulatory-mapping). Both downstream skills (governance-control-mapping and ethana-capability-validation) are implemented. Like `ethana-proposal-review`, this skill has no blocking dependencies.

**Workflow position:** Step 4.2 of `governance-assessment-workflow.md` — a mid-pipeline step. Without it, the workflow skips directly from regulatory scoping to control mapping. The Governance Assessment Workflow can produce outputs in degraded form by omitting the ISO 42001 clause-by-clause gap analysis, whereas the Proposal Development Workflow cannot produce its terminal output (Release Audit Certificate) at all.

**ADR mandate:** None. The skill is referenced in `repository-skill-architecture.md` §7 as Priority 3 and in §4 as a phantom reference from 2 existing skills.

**Architecture score impact:** Not cited as a deduction in `repository-readiness-review.md`. No explicit scoring penalty attributed to its absence.

---

## 4. Blocked Workflows

| Workflow | Missing Skill | Blocking Point | Consequence of Absence |
|---|---|---|---|
| `proposal-development-workflow.md` | `ethana-proposal-review` | Step 4.5 (terminal gate) | Cannot produce Release Classification or Release Audit Certificate. Proposals exit without a Claims Firewall terminal check. |
| `governance-assessment-workflow.md` | `iso-42001-gap-assessment` | Step 4.2 (mid-pipeline) | Gap analysis section is skipped. Workflow degrades to control mapping without a structured ISO 42001 clause audit. Remaining steps still execute. |

The `proposal-development-workflow` is terminally blocked — its defined success output is unreachable. The `governance-assessment-workflow` is partially degraded — it still produces outputs, but they are incomplete.

---

## 5. Blocked Agents

| Agent | Blocking Skill | Current Level | Target Level |
|---|---|---|---|
| Ethana Proposal Agent | `ethana-proposal-review` | Level 0 (Missing Dependencies) | Level 3 (Evaluations Passing) |
| Client Assessment Agent | `iso-42001-gap-assessment` | Level 0 (Missing Dependencies) | Level 3 (Evaluations Passing) |

Both agents are at Level 0. Each is blocked by exactly one missing skill.

**Ethana Proposal Agent** orchestrates the full commercial pipeline: `regulatory-mapping → governance-control-mapping → ethana-solution-mapping → ethana-feature-mapping → ethana-proposal-review`. It is the automated path for RFP and proposal generation — the highest-revenue operational workflow.

**Client Assessment Agent** orchestrates: `regulatory-mapping → iso-42001-gap-assessment → governance-control-mapping → ethana-capability-validation`. It serves client onboarding and periodic audit cycles — high value but lower frequency than the proposal pipeline.

Three other agents (Incident Intelligence, Regulatory Watch, Capability Validation) are at Level 3 and not blocked by either skill.

---

## 6. Rationale

### 6.1 Claims Firewall has no terminal enforcement point

ADR-002 establishes the Claims Firewall as the architectural principle preventing unauthorized capability claims from reaching clients. ADR-005 establishes the Proposal Review skill as its enforcement mechanism at the point of customer delivery. Without `ethana-proposal-review`, the Claims Firewall is enforced at internal skill boundaries (capability validation, solution mapping, feature mapping) but has no final audit gate. A proposal can still exit the system carrying undetected firewall violations.

The other 6 skills are defense-in-depth; `ethana-proposal-review` is the perimeter.

### 6.2 Commercial pipeline is terminally blocked, not degraded

The distinction matters. The Governance Assessment Workflow produces degraded output without `iso-42001-gap-assessment` — it still generates a control mapping, RACI, and maturity roadmap, just without a structured clause audit preceding it. The Proposal Development Workflow produces no Release Audit Certificate without `ethana-proposal-review` — the terminal artifact of the pipeline simply does not exist.

### 6.3 ADR-005 is an accepted architectural decision, not a recommendation

The repository has already made the build decision. ADR-005 mandates the Proposal Review gate. The skill is the code artefact that fulfills an accepted decision record. `iso-42001-gap-assessment` has no equivalent mandate — it is a referenced phantom skill rated Medium priority in `repository-skill-architecture.md`.

### 6.4 Architecture score deduction is explicit

`repository-readiness-review.md` awards the architecture a score of 78/100 with a **-10 point deduction** specifically attributing the absence of `ethana-proposal-review` as one of two primary deficiencies. The other deficiency (-12 points) is the empty `agents/` directory. Implementing `ethana-proposal-review` closes the second-largest architectural gap and unblocks the Ethana Proposal Agent, which directly addresses the agent directory deficit.

### 6.5 `iso-42001-gap-assessment` does not change the agent readiness picture meaningfully at this stage

Three agents are already at Level 3 and ready for codebase development. Implementing either missing skill would bring one more agent to Level 3. The Ethana Proposal Agent is the higher-value target given its role in the revenue pipeline.

### 6.6 ISO 42001 knowledge is already present

`knowledge/frameworks/iso-42001.md` documents all 38 Annex A controls, certification pathways, and framework relationships. The knowledge layer for `iso-42001-gap-assessment` is complete. The skill is a lower-risk build and will not lose optionality by being sequenced second.

---

## 7. Sequencing Summary

| Priority | Skill | Rationale |
|---|---|---|
| **1** | `ethana-proposal-review` | ADR-005 mandate, terminal Claims Firewall gate, terminal workflow blocker, architecture score deduction, unblocks highest-value commercial agent |
| **2** | `iso-42001-gap-assessment` | Mid-workflow blocker, no ADR mandate, knowledge layer complete, unblocks Client Assessment Agent |

After both skills are implemented, the remaining Phase 2 work is: scorecard compiler, centralized regression test suite, and agent codebase development under `agents/`.
