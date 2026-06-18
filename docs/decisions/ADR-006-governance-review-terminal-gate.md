# Architecture Decision Record: ADR-006

## Title
ADR-006: Mandatory Governance Review Terminal Gate for Client Assessment

---

## Status
**Proposed**

---

## Context

The Client Assessment Agent currently ends its chain by calling `skills/ethana-proposal-review/` as its terminal skill. This creates three documented problems.

**Problem 1 — Wrong terminal gate for the output type.**
Proposal Review is a commercial document compliance gate: it answers whether a draft proposal's capability claims are compliant with `knowledge/ethana/canonical-product-model.md`. The Client Assessment Agent does not produce a draft proposal — it produces a governance dossier containing regulatory mappings, control specifications, and ISO 42001 maturity assessments. Applying a commercial compliance gate to a governance output produces a verdict (a Proposal Compliance Score and Release Classification) that has no valid interpretation in a governance context.

**Problem 2 — Permanent structural defect producing wrong verdicts.**
The Client Assessment Agent passes `feature_mapping_output: null` to Proposal Review. `feature_mapping_output` is a required input to Proposal Review. Following the TG-3 contract fix (commit `3f71fb2`), the executor now correctly enforces TG-3: when `feature_mapping_output` is absent, it sets `traceability_gate_passed = false` and overrides `classification` to `Rejected`. This means every Client Assessment run now terminates with `classification: Rejected` — a commercially-scoped rejection verdict issued against a governance dossier. `agents/client-assessment-agent/AGENT.md §5.7.1` documents this null-pass as an "architectural constraint" and states it is "forbidden" to fabricate the value, confirming the defect is structural and permanent under the current terminal gate.

**Problem 3 — No terminal governance certificate.**
No skill in the current Client Assessment chain produces a cross-framework governance readiness certificate. The chain produces component outputs (regulatory obligations, control specifications, ISO 42001 scores) but no terminal synthesis that evaluates whether those outputs constitute an adequate governance posture. The engagement cannot deliver a formal governance verdict without a terminal synthesis skill.

ADR-005 established Proposal Review as the mandatory terminal gate for the Ethana Proposal Agent's commercial chain. An equivalent decision is required to establish a governance-appropriate terminal gate for the Client Assessment Agent's governance chain.

---

## Decision

Establish **Governance Review** (`skills/governance-review/`) as the mandatory, non-bypassable terminal skill for the Client Assessment Agent chain.

1. **Governance Review replaces Proposal Review** as the terminal skill (Skill 6) in the Client Assessment Agent workflow. Proposal Review is not removed from the system — it remains the mandatory terminal gate for the Ethana Proposal Agent's commercial chain, unchanged.

2. **Governance Review is mandatory and non-bypassable.** No Client Assessment engagement may deliver a governance verdict without a completed Governance Review producing a Governance Readiness Certificate. A run that cannot complete Governance Review halts at `HALTED_GOVERNANCE_INCOMPLETE`.

3. **The Governance Readiness Classification** (Governance Ready / Conditional Governance / Advisory Only / Not Governance Ready) replaces the Proposal Review Release Classification as the terminal verdict in the Client Assessment engagement package.

4. **The Governance Readiness Certificate** (`{engagement_id}-governance-review-certificate.md` + JSON payload) replaces the Release Audit Certificate in Client Assessment packages. The two certificates are not equivalent and must not be compared directly — GAS and CCR are not analogous to PCS and CTCS in value range or interpretation.

5. **The `feature_mapping_output` null-pass architectural defect is resolved** by this decision. Governance Review has no Feature Mapping dependency and no `feature_mapping_output` input requirement. The null-pass constraint documented in AGENT.md §5.7.1 is eliminated from the Client Assessment chain.

6. **The Client Assessment Agent AGENT.md, workflow.yaml, and state machine must be updated** to reflect this change. The update to `agents/client-assessment-agent/` is out of scope for Governance Review's skill specification and must be scheduled as a separate implementation item after Governance Review reaches L3 certification (structural baselines established and fixtures validated against the design).

---

## Consequences

**Positive:**
- Eliminates the permanent structural defect: no more `classification: Rejected` verdicts on governance assessments
- Aligns the Client Assessment terminal gate with the type of output the chain produces
- Produces a governance-appropriate terminal certificate that can be delivered to clients
- Proposal Review is freed from misuse as a governance gate — it operates only on commercial documents
- The `feature_mapping_output` null-pass constraint is eliminated from the codebase
- Governance Review as a standalone skill (per this architecture decision, following ADR-003 analysis) is reusable by future agents — a Remediation Validation Agent or Portfolio Governance Agent can call it independently

**Negative:**
- Client Assessment Agent AGENT.md, workflow.yaml, and state machine require non-trivial updates to replace Proposal Review with Governance Review as Skill 6
- Governance Review must reach L3 certification before the Client Assessment Agent update can safely proceed — this is a prerequisite gate
- Existing Client Assessment runs that produced Proposal Review certificates are not directly comparable to Governance Readiness Certificates — GAS/CCR and PCS/CTCS are different metrics

---

## Alternatives Considered

**Add Feature Mapping to the Client Assessment chain to satisfy the TG-3 gate.**
Rejected. Feature Mapping is a technical validation skill for POC scoping and RFI responses — it produces Technical Fit Scores (TFS) against a customer's technical environment. TFS scores have no interpretation in a governance assessment context. Adding a commercially-oriented technical validation skill to a governance chain would produce scores that cannot inform the governance verdict and would require the chain to run an irrelevant skill on every engagement.

**Make `feature_mapping_output` optional in the Proposal Review input schema, resolving the null-pass defect without replacing the terminal gate.**
Rejected. Proposal Review's TG-3 gate exists precisely because Feature Mapping output is material to proposal traceability — without it, the CTCS ceiling is artificially constrained and TG-3 cannot pass. Making `feature_mapping_output` optional weakens the commercial gate to resolve a structural mismatch that exists because the wrong gate was chosen, not because Feature Mapping is optional in the commercial context. The correct resolution is a governance gate, not a weakened commercial gate.

**Embed terminal synthesis logic in the Client Assessment Runtime rather than a standalone skill.**
Rejected following architecture review. Sections 1, 4, 5, 8, and 9 of the Governance Review output (executive summary, gap register, risk register, capability alignment, remediation actions) require LLM reasoning. Embedding LLM reasoning inside a runtime violates the separation established by ADR-003: runtimes orchestrate, skills reason. A runtime containing LLM reasoning is also not independently testable, versionable, or reusable by future agents. The architectural decision to implement Governance Review as a standalone skill was confirmed after evaluating this alternative against all seven relevant criteria (ADR-003 atomicity, reusability, certification burden, runtime complexity, multi-agent use, auditability, repository consistency). Six of seven criteria favour the standalone skill; the only criterion favouring embedded runtime logic is initial certification burden, which is a front-loaded cost that does not compound.

---

## Implementation Prerequisites

In order of dependency:

1. `skills/governance-review/SKILL.md` — complete (this phase)
2. `workflows/schemas/governance-review-input.schema.json` — complete (this phase)
3. `workflows/schemas/governance-review-output.schema.json` — complete (this phase)
4. `evaluations/baselines/governance-review-baseline.md` — L2 prerequisite
5. `evaluations/test-cases/governance-review/` — three fixtures — L2 prerequisite
6. Governance Review runtime implementation and L3 certification — prerequisite for step 7
7. `agents/client-assessment-agent/AGENT.md` + `workflow.yaml` + state machine update — final step; must not proceed before step 6

This ADR takes effect for the Client Assessment Agent update only after prerequisite 6 (L3 certification) is satisfied.
