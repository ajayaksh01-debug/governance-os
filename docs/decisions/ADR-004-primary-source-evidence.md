# Architecture Decision Record: ADR-004

## Title
ADR-004: Primary-Source Evidence Requirements

---

## Status
**Accepted**

---

## Context
In previous iterations, the Governance OS suffered from "capability inflation," where marketing playbooks and sales sheets claimed that unreleased products (e.g., Sentry Discovery, Edge browser extensions, and the Visual Agent Builder) were "Production (GA)". These elevations were made because commercial documents listed pricing and features as active options.

However, subsequent engineering audits of primary source materials (e.g., the May 2026 Board Briefing and active repository indexes) confirmed that these components were In Build or Aspirational, and lacked any backing codebase. Relying on marketing materials to determine system capability statuses creates extreme liability for compliance and sales processes.

---

## Decision
Any update, elevation, or modification to a capability status in `canonical-product-model.md` must be grounded in direct, primary-source engineering evidence.

1.  **Acceptable Primary Sources:**
    *   Engineering release notes and changelogs.
    *   Official Board Briefings or technical roadmap reviews signed by Product/Engineering leadership.
    *   Direct codebase inspection (verifying the presence of code and active API endpoints).
    *   Third-party audit reports (for compliance certifications).
2.  **Prohibited Sources:**
    *   Commercial playbooks and marketing brochures.
    *   objection-handling scripts and competitor battle-cards.
    *   Verbal assertions or sales discovery notes.
3.  Any change to the product model without a cited primary source in the notes is automatically rejected by the change control gate.

---

## Consequences
- **Positive:**
  - Protects the system against commercial bias and capability inflation.
  - Ensures that client proposals and configurations map only to technically operational features.
  - Protects the integrity of the Claims Firewall.
- **Negative:**
  - Creates a bottleneck for commercial updates; sales teams cannot sell a newly shipped feature until the engineering team formally documents it.
  - Requires continuous monitoring of release logs and active update processes.

---

## Alternatives Considered
- **Playbook-Synced Statuses:** Rejected. Synced statuses reflect commercial aspirations and deal packaging rather than code availability. Selling unreleased software to audited entities violates vendor compliance.
- **Dual-Status System (Sales vs. Engineering):** Rejected. Having one status for sales ("GA") and another for engineering ("In Build") defeats the purpose of the Governance OS and directly violates the Claims Firewall.
