# DEPRECATED

This file is retained for historical reference only.

Superseded by:
knowledge/ethana/canonical-product-model.md

Do not use for capability status validation, proposal generation, solution mapping, or agent decisions.

---

# Ethana Platform — Capability Status Matrix

This is the single most important artifact in this knowledge base for a procurement conversation. It states, for every platform capability, what is in production today and what is not. It does not overstate.

Status definitions are in the root `README.md`.

## Production (lead with these)

| Capability | What is confirmed in production | Known open question a bank will ask |
|---|---|---|
| AI Gateway | OpenAI-compatible front door. Routes to OpenAI, Anthropic, Gemini, Groq, self-hosted. Multi-tenant. Routing, fallback, CallTrace, per-call cost capture. Stated ~50ms overhead for the gateway itself. | Can it proxy non-LLM REST APIs (AVM, NLP scoring, ASR) and log them in the same schema? Unconfirmed. p95 under batch load with full guardrail stack? Needs test data. |
| Guardrails | Six native scanners, bidirectional (input and output). Sub-200ms p95 stated. | Does sub-200ms hold under the full stack at production throughput (for example 500 rps on a live-call app)? Needs load data. PII false-positive rate at volume? Unconfirmed. |
| Immutable Audit Logs | Insert-only event store. Multi-tenant. Logs timestamp, identity, project, guardrail verdict per call. SIEM export to Splunk, Elastic, Datadog. Retention configurable. | Is it write-once at the database layer? Can the schema be customised for specific regulator fields (for example FCA SYSC 9)? Schema work is a config engagement. |
| MCP Security (core) | Server registry, hosted runtime, tool allow-list, rate limits, per-call tracing, admin UI. ~8,000 lines in production. | Agent identity separation (NHI) is not solved yet. See In Build below. |
| Red Teaming (core) | Orchestrator with scoring, cost cap, 21 OWASP probes, multi-turn attacks. Targets model, LLM-app, and agent. | Probe coverage for RAG-specific attacks? Can it test non-LLM ML classifiers? Both unconfirmed. |
| Cost Controls (core) | Virtual API keys per team and project. Per-project budget caps. Real-time dashboard. Budget alerts. Per-tenant and per-project tracking. | Per-user attribution and GPU cost are not available yet. See In Build below. |
| Account Management | Tenants, projects, RBAC, SSO via OIDC. | SCIM provisioning not available yet. |

## In Build (use to deepen, never to open)

| Capability | What is confirmed | What is not yet available |
|---|---|---|
| MCP Non-Human Identity (NHI) | Listed in board briefing "what we are building". | Ephemeral scoped tokens, OAuth 2.0 token exchange / SPIFFE-style workload identity, on-behalf-of delegation. Until shipped, agents reuse user credentials. A compromised agent equals a compromised employee. |
| Red Teaming CI/CD gate | Probes and orchestrator are live. | The per-pull-request eval gate ("ethana eval action") is in build. Bank-specific custom YAML probes require configuration investment. |
| FinOps (full cost) | Project-level tracking is live. | Per-user attribution, per-team breakdowns, GPU cost tracking, dormant-licence detection. |
| Governance Policy Engine | Documented and in build. | OPA / Rego policy engine with signed policy bundles pushed to every surface. Not live. |
| Compliance Pack | Documented and in build. | Evidence collectors for EU AI Act, ISO 42001, NIST AI RMF, MITRE ATLAS, with one-click export. Not live. The human-delivered version is a Cursory Service today. |
| SCIM provisioning | In build. | Automated AI-vendor offboarding. Do not claim it. |
| Enterprise hardening | In build. | The full SSO / SCIM / on-prem / audit-retention enterprise bundle as a packaged set. |

## In Build, Beta-flagged (do not lead in regulated accounts)

| Capability | Status | Caution |
|---|---|---|
| Ethana Edge | Beta. Endpoint agent (Mac, Linux, Windows), browser extension, dev-tool config push for Cursor, Copilot, Claude Code. Confirmed in controlled demo only, not at institutional scale. | Never lead with this in BFSI, insurance, healthcare, or government. Requires HR and employment-law sign-off (endpoint and browser monitoring). |

## Roadmap (problem narrative only, never claim availability)

| Capability | Status | Rule |
|---|---|---|
| Discovery (Shadow AI inventory) | Roadmap. Connector layer in build. Seven connector families planned: Identity Provider, SaaS APIs, code repos, cloud agents, endpoint, browser, SWG. Identity Provider connector first. | This is one of the two most-requested CISO capabilities and it is not in production. Use the shadow-AI problem to create urgency. State explicitly that the tooling is not yet available. The human-delivered inventory is a Cursory Service. |
| AI Firewall (network egress control) | Roadmap / in build. DLP and per-user quota. Zscaler / Netskope / Palo Alto integration planned. | The other most-requested CISO capability. Not available. Do not position as live. |
| Compliance certifications | In progress, not complete: SOC 2 Type II, ISO 27001, HIPAA-ready. | Hard procurement blockers for financial services. See `deployment-and-certifications.md`. Do not state as held. |

## The two truths to carry into every regulated conversation

1. The Gateway plus Immutable Audit Log is the only capability that is Production, maps to a hard regulatory requirement (EU AI Act Art.12, FCA SYSC 9, RBI IT Outsourcing, ISO 42001 Cl.9.1), and is not a native feature of a standard API gateway. It is the opening line.

2. The two headline capabilities a CISO most wants to see, Discovery and the AI Firewall, are both not in production. Being honest about this earns credibility. Overselling it ends the deal.
