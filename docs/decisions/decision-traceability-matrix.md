# Decision Traceability Matrix

This document maps all Architecture Decision Records (ADRs) to the affected system components, including **skills**, **workflows**, **agents**, and **knowledge files**. This matrix ensures that changes to governance policies, product capabilities, and compliance standards can be tracked directly to their implementation layers within the Governance OS.

---

## 1. Traceability Mapping Summary

| ADR ID & Title | Affected Skills | Affected Workflows | Affected Agents | Affected Knowledge Files |
| :--- | :--- | :--- | :--- | :--- |
| **[ADR-001](file:///Users/ajayrajsingh/Documents/governance-os/docs/decisions/ADR-001-canonical-product-model.md)**<br>Authoritative Product Status Source | - [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/)<br>- [ethana-solution-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/)<br>- [ethana-feature-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-feature-mapping/)<br>- [ethana-proposal-review](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-proposal-review/) | - [proposal-development-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/proposal-development-workflow.md)<br>- [ethana-solution-design-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/ethana-solution-design-workflow.md) | - Ethana Assessment Agent<br>- Control Validation Agent | - [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md)<br><br>*Prohibited/Superseded:*<br>- [capability-status.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/capability-status.md)<br>- [source-of-truth.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/source-of-truth.md)<br>- [ethana-status-reconciliation.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/ethana-status-reconciliation.md) |
| **[ADR-002](file:///Users/ajayrajsingh/Documents/governance-os/docs/decisions/ADR-002-claims-firewall.md)**<br>Mandatory Claims Firewall Compliance | - [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/)<br>- [ethana-solution-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/)<br>- [ethana-proposal-review](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-proposal-review/) | - [proposal-development-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/proposal-development-workflow.md)<br>- [ethana-solution-design-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/ethana-solution-design-workflow.md) | - Ethana Assessment Agent | - [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md)<br>- [claims-matrix.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/claims-matrix.md)<br>- [buyer-solution-mapping.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/buyer-solution-mapping.md) |
| **[ADR-003](file:///Users/ajayrajsingh/Documents/governance-os/docs/decisions/ADR-003-skills-vs-workflows.md)**<br>Separation of Architectural Layers | - All current and future skills in [skills/](file:///Users/ajayrajsingh/Documents/governance-os/skills/) | - All current and future workflows in [workflows/](file:///Users/ajayrajsingh/Documents/governance-os/workflows/) | - Ethana Assessment Agent<br>- Incident Intelligence Agent<br>- Regulatory Watch Agent<br>- Control Validation Agent | - All current and future knowledge bases in [knowledge/](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/) |
| **[ADR-004](file:///Users/ajayrajsingh/Documents/governance-os/docs/decisions/ADR-004-primary-source-evidence.md)**<br>Primary-Source Evidence Requirements | - [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/)<br>- [ethana-proposal-review](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-proposal-review/) | - [proposal-development-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/proposal-development-workflow.md)<br>- [ethana-solution-design-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/ethana-solution-design-workflow.md) | - Ethana Assessment Agent<br>- Control Validation Agent | - [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md)<br>- [primary-source-validation.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/primary-source-validation.md)<br>- [evidence-based-status-review.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/evidence-based-status-review.md)<br>- [product-architecture-investigation.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/product-architecture-investigation.md)<br><br>*Prohibited/Superseded:*<br>- [buyer-persona-playbook.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/buyer-persona-playbook.md)<br>- [sales-objection-handling.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/sales-objection-handling.md)<br>- [competitive-positioning.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/competitive-positioning.md) |
| **[ADR-005](file:///Users/ajayrajsingh/Documents/governance-os/docs/decisions/ADR-005-proposal-review-gate.md)**<br>Mandatory Proposal Review Release Gate | - [ethana-proposal-review](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-proposal-review/)<br>- [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/)<br>- [ethana-solution-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/)<br>- [ethana-feature-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-feature-mapping/) | - [proposal-development-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/proposal-development-workflow.md) | - Ethana Assessment Agent | - [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md)<br>- [claims-matrix.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/claims-matrix.md) |

---

## 2. Detailed Traceability Breakdown

### ADR-001: Authoritative Product Status Source

Establish [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) as the single authoritative source of truth for all Ethana capability statuses.

- **Why it affects Skills:**
  - [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/): This skill is responsible for outputting capability status verdicts. It must look up and align with the statuses declared in the canonical product model.
  - [ethana-solution-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/): Uses the canonical product statuses to determine whether proposed solution designs map to active Production components or need roadmap caveats.
  - [ethana-feature-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-feature-mapping/): Validates technical fit of platform features. Statuses from the product model govern the boundaries of what features are eligible for POC sandboxes.
  - [ethana-proposal-review](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-proposal-review/): Audits proposals by directly verifying that claims match the canonical model statuses.
- **Why it affects Workflows:**
  - [proposal-development-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/proposal-development-workflow.md): Integrates the shared `comp.truth_gate` component to cross-check capability references against the canonical product model.
  - [ethana-solution-design-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/ethana-solution-design-workflow.md): Mandates status check-offs at transition states in the design sequence.
- **Why it affects Agents:**
  - **Ethana Assessment Agent:** When this agent generates automated assessments or capability summaries, it is prohibited from referencing any status other than the canonical ones.
  - **Control Validation Agent:** Ensures that operational controls mapped to client risk points correspond to Production-status features.
- **Why it affects Knowledge Files:**
  - Establishes [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) as the sole active status repository.
  - Formally deprecates and prohibits system reads on historical status files including [capability-status.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/capability-status.md), [source-of-truth.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/source-of-truth.md), and [ethana-status-reconciliation.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/ethana-status-reconciliation.md).

---

### ADR-002: Mandatory Claims Firewall Compliance

Enforces the Claims Firewall rule: all customer-facing proposals, RFPs, and solution designs must match canonical statuses and permission levels.

- **Why it affects Skills:**
  - [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/): Must produce a Claim Permission Level (CPL) and allowed/prohibited claim statements to guide downstream firewall checks.
  - [ethana-solution-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/): Must include mandatory roadmap disclosures and manual workaround controls for any feature mapping to *In Build* or *Roadmap*.
  - [ethana-proposal-review](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-proposal-review/): Runs the linter rules and deducts points for firewall breaches (PCS/CTCS scoring).
- **Why it affects Workflows:**
  - [proposal-development-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/proposal-development-workflow.md): Integrates the firewall check as Quality Gate Section 6. A firewall breach halts the workflow automatically.
- **Why it affects Agents:**
  - **Ethana Assessment Agent:** Programmatically restricted from adding any non-Production claim without appending the required manual workaround options.
- **Why it affects Knowledge Files:**
  - [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md): Serves as the firewall's status dictionary.
  - [claims-matrix.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/claims-matrix.md): Holds validation rules for platform statements.

---

### ADR-003: Separation of Architectural Layers

Decouples the repository into distinct layers: Knowledge, Skills, Workflows, Evaluations, and Agents.

- **Why it affects Skills:**
  - Restructures all folder systems under [skills/](file:///Users/ajayrajsingh/Documents/governance-os/skills/). Every skill directory must contain a spec `SKILL.md` and keep logic parameterized, separating local rubrics (`evaluation.md`) from prompts.
- **Why it affects Workflows:**
  - Workflows under [workflows/](file:///Users/ajayrajsingh/Documents/governance-os/workflows/) must act solely as state and data routers. They are prohibited from embedding LLM prompt templates or local evaluation rules.
- **Why it affects Agents:**
  - Agent runtimes under `agents/` are decoupled from task definitions. Agents function as orchestrators, registering skills as MCP tools.
- **Why it affects Knowledge Files:**
  - Static files in [knowledge/](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/) must contain only raw facts, framework crosswalks, or regulations. Reasoning guidelines and rubrics are banned from this layer.

---

### ADR-004: Primary-Source Evidence Requirements

Enforces that capability status elevations in the product model must be grounded in direct, primary-source engineering evidence.

- **Why it affects Skills:**
  - [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/): Applies evidence sufficiency standards when grading capability levels.
  - [ethana-proposal-review](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-proposal-review/): Verifies that referenced capability records cite primary evidence sources.
- **Why it affects Workflows:**
  - Enforces that solution development workflows halt if design elements depend on capabilities whose statuses have not been verified by a primary-source audit.
- **Why it affects Agents:**
  - **Ethana Assessment Agent / Control Validation Agent:** Restricts these agents from declaring controls as active if they lack verified primary-source implementation logs.
- **Why it affects Knowledge Files:**
  - [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md): Status notes must link directly to engineering records.
  - [primary-source-validation.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/primary-source-validation.md) & [evidence-based-status-review.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/evidence-based-status-review.md): Store engineering and validation logs.
  - Prohibits referencing commercial or sales playbooks (e.g. [buyer-persona-playbook.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/buyer-persona-playbook.md), [sales-objection-handling.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/sales-objection-handling.md)) to establish capability status.

---

### ADR-005: Mandatory Proposal Review Release Gate

Establishes Proposal Review as the mandatory final compliance and quality release gate.

- **Why it affects Skills:**
  - [ethana-proposal-review](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-proposal-review/): Implements the metrics (PCS/CTCS), redlining algorithms, and release classification logic.
  - Integrates inputs from upstream skills: capability validation (CPL), solution mapping (CCS), and feature mapping (TFS).
- **Why it affects Workflows:**
  - [proposal-development-workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/workflows/proposal-development-workflow.md): Promotes Step 4.5 from a planned placeholder to a mandatory, blocking execution step.
- **Why it affects Agents:**
  - **Ethana Assessment Agent:** When orchestrating proposal pipelines, this agent must call the proposal review skill and verify a classification of "Approved" or "Approved with Revisions" before presenting outputs.
- **Why it affects Knowledge Files:**
  - [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md): Serves as the ultimate compliance baseline for the proposal audit.
