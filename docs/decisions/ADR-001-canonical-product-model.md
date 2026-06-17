# Architecture Decision Record: ADR-001

## Title
ADR-001: Authoritative Product Status Source

---

## Status
**Accepted**

---

## Context
Historically, the Governance OS had conflicting references regarding the development and release status of Ethana platform capabilities. Engineering briefs and board slides contradicted commercial battle-cards and marketing playbooks (which often claimed unreleased or in-development features, such as Sentry discovery connectors or local device agents, as production-ready). 

When these conflicting sources were ingested by sales, compliance, or advisory operators, it created significant risk of over-claiming capabilities to highly regulated enterprise accounts (e.g., G-SIB banks under PRA/FCA or RBI supervision). Over-claiming unreleased features leads to compliance breaches, lost procurement trust, and potential legal exposure.

---

## Decision
Establish `knowledge/ethana/canonical-product-model.md` as the single authoritative source of truth for all Ethana capability statuses within the Governance OS. 

1.  No secondary source, marketing deck, competitive positioning sheet, or verbal engineering claim can override the statuses declared in this file.
2.  All skills, workflows, evaluation scripts, and agents must route status lookups through this canonical model.
3.  Any file containing conflicting statuses (such as superseded historical files: `capability-status.md`, `source-of-truth.md`, and `ethana-status-reconciliation.md`) is officially prohibited from being read or referenced by any active system process.

---

## Consequences
- **Positive:**
  - Establishes a clear, single source of truth, removing ambiguity for both automated agents and human analysts.
  - Mitigates the compliance risk of over-claiming unreleased features to regulated clients.
  - Automatically aligns all downstream outputs (solutions, controls, and proposals) to engineering reality.
- **Negative:**
  - Creates a strict dependency on the upkeep of this single file; any failure to update this document when a new feature is shipped will result in the system under-representing platform capabilities.
  - Requires a rigorous, evidence-grounded change control process to update the canonical model itself.

---

## Alternatives Considered
- **Marketing Playbook as Authority:** Rejected. Playbooks reflect forward-looking commercial positioning and pricing, not the actual engineering codebase status. Proposing unreleased playbooks to regulated accounts poses extreme risk.
- **Direct Codebase / Git Tag Lookup:** Rejected. While technically accurate, direct code checks lack the necessary context, caveats, and human-readable explanations required by advisory and compliance operators.
