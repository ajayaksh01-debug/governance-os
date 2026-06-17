# Buyer Solution Mapping

This replaces the earlier `solution-mapping.md`. The personas and use cases are retained where sound and re-grounded in real platform capabilities. The competitive positioning is corrected: the old file compared Ethana to GRC platforms and AI-safety monitoring tools, which is the wrong field for a control plane.

Every capability referenced below carries its status. Only Production capabilities are presented as available.

---

## Buyer personas

Start from the buyer's problem, not from a feature. Lead with the entry capability that is Production.

### CISO

- Problem: shadow AI exfiltrating customer data, no AI inventory, audit-evidence gaps, an AI-specific attack surface (prompt injection, jailbreak, data extraction) that conventional security tooling does not cover.
- Entry capability: Guardrails **[P]** plus Immutable Audit Log **[P]**.
- What they fear: regulatory action, and an incident they cannot reconstruct.
- Talk-track anchor: "If a regulator asked for your AI usage register by end of day, what would you produce?"
- Honesty note: the CISO will ask for shadow-AI Discovery and the AI Firewall. Both are not in production. Use the problem to create urgency; state that the tooling is Roadmap and that the inventory is available now as a Cursory engagement.

### CRO

- Problem: AI systems making decisions that cannot be explained, hallucinating outputs, no change control.
- Entry capability: Immutable Audit Log **[P]** plus Red Teaming **[P]**.
- What they fear: a bad AI decision causing customer harm or a regulatory fine.
- Talk-track anchor: "Which of your AI systems in production has an audit trail that would satisfy an FCA or RBI inspector?"
- Honesty note: a CRO expects more than a control layer (framework, validation, policy). That gap is filled by Cursory Services, not by the platform.

### CIO / CTO

- Problem: AI sprawl, no central infrastructure, multiple teams building ad hoc, no cost attribution.
- Entry capability: Gateway **[P]** plus Cost Controls **[P]**.
- What they fear: runaway AI spend, building the same infrastructure five times, vendor lock-in.
- Talk-track anchor: "How many different AI providers are your teams using right now, and how do you control what goes to each one?"
- Honesty note: per-user cost attribution is In Build. Project-level is live.

### Chief Compliance Officer

- Problem: the AI regulatory landscape is changing faster than the compliance team can absorb (EU AI Act in force, DPDP live, RBI FREE-AI live).
- Entry: Framework Mapping **[SVC]** plus Regulatory Analysis **[SVC]**, with Immutable Audit Log **[P]** as the evidence base.
- Honesty note: most of what a CCO needs here is Service, not platform. The Compliance Pack that would automate it is In Build.

### Head of AI / Chief AI Officer

- Problem: governance slows deployment; the business wants AI now.
- Entry: Gateway **[P]** plus Guardrails **[P]** (governed pathways that clear the path rather than block it).
- Honesty note: position governance as enabling speed through approved, audited pathways. Do not claim Discovery-based automation.

### Internal Audit

- Problem: AI is material but audit methodology has not kept pace; no AI-specific expertise.
- Entry: Immutable Audit Log **[P]** as the evidence base; AI Governance Health Check **[SVC]** for methodology.

---

## Industry use cases

### BFSI — Model risk management for LLMs

- Buyer: Head of Model Risk, CRO.
- Problem: SR 11-7 / SS1/23 require validation, but LLM validation methodology is undefined and the model-risk team lacks LLM expertise.
- Ethana fit: Red Teaming **[P]** provides LLM-specific testing; Immutable Audit Log **[P]** provides monitoring evidence; Framework Mapping **[SVC]** maps LLM governance to SR 11-7. Traditional quantitative validation remains a **[GAP]**.
- Outcome: the model-risk function extends to LLMs through testing and monitoring, without claiming it replaces quantitative validation.

### BFSI — EU AI Act readiness

- Buyer: CCO, CRO.
- Problem: credit scoring, underwriting, and fraud detection are high-risk under Annex III; the 2026 deadline is approaching; systems are not yet classified.
- Ethana fit: Audit Log **[P]** for Art.12; Red Teaming **[P]** for Art.15; classification and gap analysis via Cursory **[SVC]**; technical documentation via Compliance Pack **[IB]** or Service today. Conformity assessment is a **[GAP]** (notified body).
- Note: this is a post-SOC-2 market for the platform sale. Advisory can begin earlier.

### Enterprise / agentic AI deployment

- Buyer: CISO, Head of AI.
- Problem: agents connected to internal systems via MCP are moving faster than security and governance.
- Ethana fit: MCP Broker **[P]** for registry, allow-list, rate limits, and per-call tracing. The critical identity control (NHI) is **[IB]**, so agent identity separation is not yet solved. State this plainly.
- Outcome: agent tool calls are brokered, controlled, and traced today; agent identity arrives with NHI.

### India BFSI — RBI FREE-AI and DPDP

- Buyer: CISO, CRO, Head of Compliance.
- Problem: RBI FREE-AI (August 2025) and DPDP (November 2025) made AI governance a board-level priority; customer data cannot route through external cloud.
- Ethana fit: the strongest immediate fit. Audit Log **[P]** plus Guardrails **[P]** plus on-prem / India VPC with PII masking at the gateway **[P]**. Caveat: on-prem at Tier 1 scale is unproven.
- This is priority one. Entry capability: Immutable Audit Trail plus Guardrails.

### Healthcare / life sciences — clinical AI

- Buyer: CISO, CRO, Head of Digital Health.
- Problem: clinical decision-support AI is high-risk and patient-safety-critical.
- Ethana fit: Guardrails (PII) **[P]** plus Audit Log **[P]**; risk assessment via Cursory **[SVC]**. HIPAA-ready certification is In Progress, not held. This is a Q4-horizon market gated on certification.

---

## Competitive positioning (corrected)

The control-plane field is not GRC platforms or AI-safety monitoring tools. The real comparison set:

### vs. AI gateways and routing tools (Portkey, LiteLLM-style gateways)

- Honest read: these are mature on routing and observability. Ethana's differentiation is not breadth of gateway features. It is the Gateway plus Immutable Audit Log plus embedded Guardrails as a governance combination, with on-prem / VPC deployment and the Cursory services wrap.
- Do not claim feature superiority on pure gateway function. Claim governance integration and deployment fit for regulated buyers.

### vs. cloud-native agent platforms (AWS Bedrock / AgentCore, Azure)

- Honest read: these are deeply integrated within their own cloud. Ethana's differentiation is vendor neutrality (model-agnostic across providers) and on-prem / VPC for buyers who cannot or will not centralise on one hyperscaler. Against a single-cloud bank already standardised on AWS, this is a weaker wedge; lead with audit and on-prem instead.

### vs. observability tools (Langfuse, Helicone, PromptLayer)

- Honest read: these are monitoring and tracing tools. Ethana is a control layer: it enforces (guardrails) and brokers (MCP), not only observes. The immutable, regulator-grade audit log is a stronger claim than general observability. This is a favourable comparison.

### vs. IBM watsonx and large enterprise AI suites

- Honest read: broad, expensive, slow to deploy. Ethana's edge is focus, speed, deployment flexibility, and the Cursory advisory wrap. Do not compete on breadth.

### The standing weakness to acknowledge

Early-stage product maturity. Discovery and Edge are Roadmap or Beta. SOC 2 and ISO 27001 are in progress, not held. Any competitor can point to more complete coverage or held certifications today. The honest counter is the audit-log-plus-on-prem fit for regulated buyers, plus the Cursory services layer that no pure-software competitor offers. Do not counter a maturity objection by overstating the roadmap.

---

## The single strongest opening, across all personas and industries

The Gateway plus Immutable Audit Log is the only capability that is Production, maps to a hard regulatory requirement (EU AI Act Art.12, FCA SYSC 9, RBI IT Outsourcing, ISO 42001 Cl.9.1), and is not native to a standard API gateway. Open there. Everything else is additive.
