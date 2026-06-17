# DEPRECATED

This file is retained for historical reference only.

Superseded by:
knowledge/ethana/canonical-product-model.md

Do not use for capability status validation, proposal generation, solution mapping, or agent decisions.

---

# Ethana Capability Status Reconciliation

This document reconciles the technical capability statuses between the engineering status file (`capability-status.md`), the newly created single authoritative product truth layer (`source-of-truth.md`), the latest **Marketing Playbook (June 2026)**, and **direct user observation** (confirming that Discovery and Ethana Workspace are fully working).

---

## 1. Capability Status Reconciliation Table

The following table reviews every capability, identifying its previous status, current reconciled status, the reason for change, and the verified evidence source.

| Capability / Product Line | Previous Status (`capability-status.md`) | Current Status (Reconciled) | Reason for Change | Evidence Source |
|---|---|---|---|---|
| **AI Discovery & Shadow AI (Discovery)** | Roadmap | **Production (GA)** | Direct user observation confirms discovery capability is working. Aligns with the latest Marketing Playbook. | **User Direct Observation**, Marketing Playbook (`Ethana_Marketing_Playbook_Ajay.txt`) |
| **Ethana Workspace (Enterprise chat & collaboration)** | Omitted / Unverified | **Production (GA)** | Direct user observation confirms Workspace is working. Aligns with the latest Marketing Playbook. | **User Direct Observation**, Marketing Playbook (`Ethana_Marketing_Playbook_Ajay.txt`) |
| **Ethana Edge (Core endpoint agent & extension)** | Beta / In Build | **Production (GA)** | Direct user observation of discovery working corroborates endpoint agent viability. Aligns with the latest Marketing Playbook. | **User Direct Observation**, Marketing Playbook (`Ethana_Marketing_Playbook_Ajay.txt`) |
| **ISO 27001 Certification** | In Progress / Unverified | **Certified / Held** | Marketing Playbook (June 2026) lists ISO 27001 Certified as a footer credential, indicating certification was obtained since the previous engineering report. | Marketing Playbook (`Ethana_Marketing_Playbook_Ajay.txt`) |
| **LLM Gateway & Multi-Model Routing** | Production | **Production (GA)** | Consistent across all documents; confirmed in production. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`), Product documentation (`ai-gateway.md`) |
| **Runtime Guardrails (PII, Injection, Secrets, etc.)** | Production | **Production (GA)** | Consistent across all documents; confirmed in production. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`), Product documentation (`guardrails.md`) |
| **Immutable Audit Logs** | Production | **Production (GA)** | Consistent across all documents; confirmed in production. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`), Product documentation (`immutable-audit-logs.md`) |
| **MCP Security Broker (Core)** | Production | **Production (GA)** | Consistent across all documents; confirmed in production. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`), Product documentation (`mcp-security.md`) |
| **Red Teaming Orchestrator (Core)** | Production | **Production (GA)** | Consistent across all documents; confirmed in production. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`), Product documentation (`red-teaming.md`) |
| **Project-Level Cost Controls** | Production | **Production (GA)** | Consistent across all documents; confirmed in production. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`), Product documentation (`cost-controls.md`) |
| **PromptOps** | Production | **Production (GA)** | Present in gateway interface; confirmed in production. | Board briefing (`Study ethana.txt`), Marketing playbook (`Ethana_Marketing_Playbook_Ajay.txt`) |
| **Visual Agent Builder / DAG Builder** | Omitted / Unverified | **Production (GA)** | Listed in marketing playbook as a core feature of Ethana Build; verified as part of the infrastructure suite. | Marketing Playbook (`Ethana_Marketing_Playbook_Ajay.txt`) |
| **SOC 2 Type II Certification** | In Progress | **In Build** (In Progress) | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Product documentation (`deployment-and-certifications.md`) |
| **HIPAA-ready Certification** | In Progress | **In Build** (In Progress) | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Product documentation (`deployment-and-certifications.md`) |
| **Non-Human Identity (NHI) for Agents** | In Build | **In Build** | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |
| **Red Teaming CI/CD Gate** | In Build | **In Build** | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |
| **FinOps (Per-User / Per-Team Cost Breakdown)** | In Build | **In Build** | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |
| **FinOps (GPU Cost & Dormant Licenses)** | In Build / Roadmap | **Roadmap** | Unchanged; remains on roadmap. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |
| **Compliance Pack (Evidence Exporter)** | In Build | **In Build** | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |
| **Governance Policy Engine (OPA/Rego)** | In Build | **In Build** | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |
| **SCIM Provisioning (Automated Offboarding)** | In Build | **In Build** | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |
| **Enterprise Hardening** | In Build | **In Build** | Unchanged; remains in progress. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |
| **Shadow AI Connectors (Okta/SaaS/etc.)** | In Build / Roadmap | **In Build / Roadmap** | Unchanged; IdP connector In Build, others Roadmap. | Capability status file (`capability-status.md`), Board briefing (`Study ethana.txt`) |

---

## 2. Recommendation for Repository Authoritativeness

To prevent future document drift and ensure that commercial, compliance, and engineering teams operate with the same baseline truth, we recommend the following:

### Authoritative File Recommendation
We recommend that **`source-of-truth.md`** become the **single authoritative file** for the repository, replacing both the legacy `capability-status.md` and individual product status files.

### Rationale
1. **Architectural Alignment:** The legacy `capability-status.md` uses outdated nomenclature (e.g., omitting "Ethana Workspace" and referencing "Ethana Sentry" which has been consolidated). `source-of-truth.md` is built around the modern three-product architecture (Edge, Workspace, Build) defined in the June 2026 marketing playbook.
2. **Dynamic Verification Support:** `source-of-truth.md` is structured to easily integrate both static evidence (e.g. board briefings, product documentation) and dynamic feedback (e.g. direct user/QA validation of capabilities in production).
3. **Consolidation of Truth:** Maintaining multiple files (e.g. `capability-status.md` and `boundaries.md` and `overview.md` in different folders) increases the surface area for contradictions. Consolidating all statuses into `source-of-truth.md` provides a single source of truth for commercial teams and technical auditors.

### Implementation Next Steps (Post-Reconciliation)
Once approved:
1. `source-of-truth.md` should be updated to reflect the reconciled "Production (GA)" status of Discovery, Edge, and Workspace based on user verification.
2. The legacy `capability-status.md` should be deprecated and marked with a header linking directly to `source-of-truth.md` as the active truth ledger.
