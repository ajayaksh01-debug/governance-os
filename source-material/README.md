# Ethana / Cursory Knowledge Base

Audience: BFSI buyers, procurement, risk, and security teams, and the Cursory commercial team supporting them.

Principle: accuracy over marketing language. Every capability claim is classified by production status. Conflating roadmap with production is treated as a disqualifying error in regulated procurement.

## The two-layer split

This knowledge base separates two things that the earlier files incorrectly merged:

1. **Ethana Platform** — the runtime AI control plane. A product that sits inline between enterprise applications and AI models. Software with a defined, classifiable capability set.

2. **Cursory Services** — the advisory and implementation practice that wraps the platform. Human-delivered governance work. The regulatory mapping, risk frameworks, policy design, and control testing are Cursory IP. None of it is a platform feature.

A capability is either software that runs (Platform) or work that people do (Services). It is never both. When in doubt, ask: does this run without a consultant present? If no, it is a Service.

## Status legend (Platform only)

| Status | Meaning | Selling rule |
|---|---|---|
| **Production** | In production now. Confirmed in board briefing or shown in demo. | Lead with it. Full claim defensible. |
| **In Build** | Actively being built and documented. Not live. Includes Beta items, flagged. | Use to deepen a conversation. Never use as a door-opener or claim as available. |
| **Roadmap** | Not in production. No confirmed date. | Use the problem narrative to create urgency. State explicitly that tooling is not yet available. |

Where a capability has a Production core and an In Build sub-capability, both are shown. The core is Production; the named gap is In Build. This is the only honest way to present partial capabilities.

## Repository structure

```
ethana-cursory-knowledge/
├── README.md                              this file
├── ethana-platform/
│   ├── overview.md                        what the control plane is, and is not
│   ├── capability-status.md               master status matrix (the procurement artifact)
│   ├── capabilities/
│   │   ├── ai-gateway.md
│   │   ├── guardrails.md
│   │   ├── immutable-audit-logs.md
│   │   ├── mcp-security.md
│   │   ├── red-teaming.md
│   │   └── cost-controls.md
│   ├── deployment-and-certifications.md   on-prem/VPC, SOC 2 / ISO 27001 status, hard blockers
│   └── boundaries.md                      what Ethana does not solve
├── cursory-services/
│   ├── overview.md                        the advisory practice and its relationship to the platform
│   └── services-catalog.md                the five service lines
├── framework-crosswalk.md                 frameworks mapped to real capabilities + services, status-flagged
└── buyer-solution-mapping.md              personas, industry use cases, corrected competitive positioning
```

## Migration notes (what changed from the old files)

The previous `capabilities.md`, `feature-mapping.md`, and `solution-mapping.md` described Ethana as an assessment / advisory / GRC-intelligence platform. That is not the product. Corrections applied:

- **AI System Inventory and Classification** was presented as a foundational live capability. It is Discovery, which is Roadmap. Moved to platform Roadmap, and the human-delivered version moved to Cursory Services (AI Inventory and Classification engagement).
- **Risk Assessment and Gap Analysis** is not a platform capability. Moved to Cursory Services.
- **Framework Mapping and Compliance Tracking** maps to the Governance Policy Engine and Compliance Pack, both In Build. Delivery today is a Cursory Service.
- **Control Implementation Guidance** is advisory. Moved to Cursory Services.
- **Regulatory Intelligence and Watch** is not a platform capability. Moved to Cursory Services (Regulatory Analysis).
- **Incident Intelligence** had no basis in the confirmed or roadmap product. Excluded from both layers pending confirmation that Cursory actually delivers it as a service. Do not claim it.
- **Audit Evidence and Reporting** was split. The Immutable Audit Log is Production. Automated evidence packs and regulator-specific reporting are the Compliance Pack, In Build.
- Competitor set corrected. The old files compared Ethana to GRC platforms and AI-safety monitoring tools, which is the wrong field for a control plane. See `buyer-solution-mapping.md`.

## Open items to resolve before external use

- Brisk to Ethana rename. External name is confirmed: Ethana. The marketing PDFs that brand the platform as Brisk® need updating to Ethana before reuse.
- Confirm whether the sixth guardrail scanner is Secrets or Hallucination Grounding. Internal sources disagree. See `capabilities/guardrails.md`.
- Written confirmation of non-LLM REST API coverage at the gateway (AVM, NLP scoring, ASR). Until then, scope all gateway claims to the LLM API layer.
- SOC 2 Type II and ISO 27001 completion dates. Both are hard financial-services procurement blockers and are currently in progress, not complete.
