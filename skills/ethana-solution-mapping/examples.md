# Ethana Solution Mapping — Worked Examples

This document contains three fully worked solution mappings produced using the Ethana Solution Mapping skill. Each example demonstrates application of the complete workflow and all ten output sections. They serve as calibration anchors for evaluation scoring.

---

---

# Example 1: Indian Private Bank — LLM Credit AI Governance

**Date of Mapping:** 2026-06-17
**Customer:** Indian private sector bank (₹25,000 Cr asset base; subsidiary of Singapore-headquartered banking group)
**Sector:** BFSI (primary jurisdiction: India; secondary: UK via parent group)
**Output Mode:** Formal Proposal
**Requirement Source:** Section 6 output from regulatory-mapping (RBI MRM expectations, DPDP Act 2023, ISO 42001 Annex A controls)
**Deployment Constraint:** Customer VPC (Mumbai AWS region)
**Existing Subscription:** None
**Analysis Status:** Final

**Customer context:** The bank is deploying LLM-based credit analysis assistants for relationship managers. The LLMs route through the bank's VPC. The CISO requires: immutable audit trail for RBI examiners, PII masking at the API layer for DPDP Act compliance, prompt injection protection, credit model bias documentation (for RBI Fair Practices Code compliance), and NHI support for the emerging agent workflows being prototyped by the engineering team. The Group CISO in Singapore has raised SOC 2 Type II as a vendor onboarding requirement for the parent group's supply chain programme.

---

## 1. Requirement Coverage Map

| # | Requirement | Matched Ethana Capability | Status | CCS | Disposition |
|---|---|---|---|---|---|
| R1 | Immutable audit trail for every LLM decision (RBI MRM, IT Governance) | Immutable Audit Log | Production | 88 | Include in proposal |
| R2 | PII masking at API layer for DPDP Act data minimisation | Guardrails: PII Scanner | Production | 80 | Include in proposal (with caveat) |
| R3 | Prompt injection detection for credit AI assistants | Guardrails: Prompt Injection Scanner | Production | 92 | Include in proposal |
| R4 | Jailbreak and toxicity detection | Guardrails: Jailbreak + Toxicity Scanners | Production | 90 | Include in proposal |
| R5 | Credit model bias documentation / runtime bias detection (RBI Fair Practices) | Guardrails: Bias Scanner | Production | 18 | Section 3 (runtime safeguard only — scoped non-audit caveat required) + Section 5 (formal audit claim prohibited) + Section 7 (formal audit gap) |
| R6 | LLM gateway with multi-model routing and fallback | LLM Gateway | Production | 90 | Include in proposal |
| R7 | NHI for emerging agent workflows | MCP Security Broker (core) + NHI module | Production (core) / In Build (NHI) | 42 | Include MCP core in proposal; NHI in roadmap disclosure |
| R8 | SOC 2 Type II for Group CISO vendor onboarding | SOC 2 Type II (In Build) | In Build | 0 | Procurement blocker — Section 5; bridge in Section 9 |
| R9 | Customer VPC deployment | VPC Deployment Model | Production | 95 | Include in proposal |
| R10 | Red teaming of deployed credit AI | Red Teaming Orchestrator | Production | 82 | Include in proposal (CI/CD gate caveat) |

---

## 2. Coverage Confidence Summary

**Average CCS (across all requirements including blockers):** 67.7/100 (sum: 88+80+92+90+18+90+42+0+95+82 = 677 ÷ 10)
**Distribution:** Full (90–100): 4 req (R3=92, R4=90, R6=90, R9=95) | High (70–89): 3 req (R1=88, R2=80, R10=82) | Partial (50–69): 0 req | Thin (25–49): 1 req (R7=42) | None (0–24): 2 req (R5=18, R8=0)
**Coverage characterisation:** Platform-Primary — 70% of requirements (7 of 10) land at High or Full; average CCS 67.7 exceeds the Platform-Primary threshold of 65. The SOC 2 blocker (R8) is a procurement gate, not a capability gap — it does not reflect on Build coverage quality and is handled separately in Section 9 (Commercial Motion).

**Coverage story:** Ethana Build addresses the core of this requirement set with strong production coverage. Gateway, guardrails, audit log, and VPC deployment all score High or Full. Two requirements are unaddressed: (a) the formal credit model bias audit — Ethana's Bias Scanner is a runtime text safeguard, not a statistical model audit; a specialist firm is required for RBI Fair Practices Code compliance; and (b) SOC 2 Type II, which is a Group CISO procurement gate. Despite the Platform-Primary coverage profile, Advisory-First motion is triggered by the SOC 2 blocker — the motion reflects the procurement constraint, not a capability weakness.

---

## 3. Proposal-Safe Platform Capabilities

*Output mode: Formal Proposal. Language is quotable directly in the customer document.*

### LLM Gateway
**Status:** Production | **CCS:** 90/100 (Full)
**Claim language:** "Ethana's LLM Gateway provides multi-model routing across GPT-4o, Claude 3.x, and open-source models with configurable fallback chains, per-request latency overhead of approximately 50ms at p95, deployed natively within the customer's AWS VPC to ensure all LLM traffic remains within the data perimeter."

### Runtime Guardrails: PII, Prompt Injection, Jailbreak, Toxicity
**Status:** Production | **CCS (by scanner):** PII: 80/100, Injection: 92/100, Jailbreak: 90/100, Toxicity: 90/100
**Claim language — PII:** "Ethana's Guardrails PII Scanner detects and redacts personally identifiable information in both LLM requests (before model submission) and LLM responses (before delivery to the user), operating at sub-200ms p95 latency. Coverage includes Indian PAN, Aadhaar, phone number, and address patterns in addition to standard PII types."
**Mandatory caveat (PII):** Coverage applies to API-layer traffic routed through the Ethana Gateway. PII entered via browser-native AI tools or endpoint applications not routed through the Gateway is not covered by this control.
**Claim language — Guardrails:** "Ethana's Prompt Injection, Jailbreak, and Toxicity Scanners operate bidirectionally on all LLM calls at sub-200ms p95 latency, flagging adversarial instructions in user inputs and detecting harmful content in model outputs."

### Immutable Audit Log
**Status:** Production | **CCS:** 88/100 (High)
**Claim language:** "Ethana's Immutable Audit Log captures every LLM gateway call — request, response, scanner disposition, model identity, and latency — in a tamper-proof, insert-only event store. Records cannot be modified or deleted post-write. Logs export natively to Splunk, Elastic, and Datadog via SIEM connectors. Audit records are retained per configurable policy and are designed for presentation to RBI examiners."
**Mandatory caveat:** Log schema is configurable within Ethana's defined schema set. Custom fields required by the customer's specific RBI examination template may require configuration during implementation.

### Guardrails: Bias Scanner (runtime safeguard — supplemental only)
**Status:** Production | **CCS:** 18/100 (None — runtime text filter; does not satisfy formal bias audit)
**Claim language:** "Ethana's Bias Scanner monitors LLM outputs in real time and flags bias-related signals — differential framing, demographic stereotyping, or biased language patterns — in credit AI responses before they reach the end user."
**Mandatory caveat — must appear immediately after the claim in any proposal document:** This is a runtime operational safeguard against biased LLM outputs, not a statistical bias audit. It does not satisfy the formal credit model disparate impact testing obligation under RBI Fair Practices Code or ISO 42001 Annex A Bias Evaluation controls. Formal bias audit is addressed separately — see Gap Register.
**Placement note:** Include only in a "Runtime Controls" or "Operational Safeguards" subsection. Never in response to a formal bias documentation requirement. If the customer asks specifically about bias compliance, direct them to Section 7 (Gap Register) and Section 6 (specialist referral bridge).

### MCP Security Broker (core capabilities)
**Status:** Production | **CCS:** 42/100 (Thin — due to NHI gap; core tracing is Production)
**Claim language (limited to core):** "Ethana's MCP Security Broker provides per-call tracing for all MCP tool invocations in AI agent workflows — capturing the tool called, parameters passed, and response returned in the Immutable Audit Log. The broker is implemented in approximately 8,000 lines of production code with multi-tenant isolation."
**Mandatory caveat:** Non-Human Identity (NHI) provisioning and lifecycle management for agents is currently In Build. The proposal scope covers per-call tracing and audit. Agent identity management is a roadmap item.

### Red Teaming Orchestrator
**Status:** Production | **CCS:** 82/100 (High)
**Claim language:** "Ethana's Red Teaming Orchestrator runs 21 OWASP LLM Top 10 probes against deployed AI models, with multi-turn attack simulation targeting model behaviour, application-layer controls, and agent orchestration. Red teaming can be run on-demand during the engagement or on a scheduled cadence."
**Mandatory caveat:** Automated CI/CD pipeline integration (triggering red teaming on every deployment) is In Build. The production capability covers on-demand and scheduled orchestration.

### VPC Deployment
**Status:** Production | **CCS:** 95/100 (Full)
**Claim language:** "Ethana is available as a fully managed deployment within the customer's AWS VPC, ensuring all LLM traffic, audit logs, and configuration data remain within the customer's data perimeter. The VPC deployment model is the recommended option for BFSI customers requiring data residency control."

---

## 4. Roadmap Disclosure

*Output mode is Formal Proposal. Include the items below only in a clearly-labelled "Ethana Roadmap — Not In Scope of This Proposal" section of the proposal document. Do not include in scope-of-work, deliverables, or SLA sections. No delivery commitment may be made for any item below. If the customer asks for a timeline commitment, decline — these items have no committed ship date.*

### Non-Human Identity (NHI) for Agent Workflows
**Status:** In Build
**When shipped, will provide:** Automated identity provisioning and lifecycle management for AI agents — including credential issuance, access scoping, and rotation — enabling full NHI governance alongside the existing per-call MCP tracing.
**Today, Cursory bridges this with:** Governance Programs service to design and operate a manual NHI policy (agent credential register, access review schedule, and offboarding checklist). This is a human-operated equivalent that establishes the governance process before the automated platform capability ships.
**Anticipated CCS when shipped:** 85/100

### CI/CD Red Teaming Gate
**Status:** In Build
**When shipped, will provide:** Automated red teaming triggered on every AI model deployment in the CI/CD pipeline, blocking deploys that fail OWASP probe thresholds.
**Today, Cursory bridges this with:** Red Teaming as a Service — Cursory-run scheduled red team exercises (monthly or per-deployment cycle) that simulate what the automated gate will do.
**Anticipated CCS when shipped:** 90/100

---

## 5. Prohibited Claims Register

The following must not appear in any proposal document for this engagement:

- **SOC 2 Type II:** Not certified. Currently In Build. Must not be referenced as available, achievable within the proposal term, or pending in a way that implies near-term availability.
- **ISO 27001 Certified:** Certification in progress. Must not be claimed.
- **HIPAA-Ready:** Not available. Not applicable to this engagement but must not be used as a general Ethana claim.
- **Ethana Workspace (enterprise chat, RAG, copilots):** Aspirational. Must not appear anywhere.
- **Visual Agent Builder / DAG Builder:** Aspirational. Must not appear anywhere.
- **Ethana Edge (endpoint monitoring, browser extension):** In Build. Must not appear as a proposal deliverable.
- **"Deployed with regulated Indian banks today":** No confirmed production deployment with RBI-regulated customers. Do not claim.
- **Full credit model bias audit:** Ethana's Bias Scanner is a runtime text filter. It does not perform statistical bias testing on credit model outputs. Do not position as satisfying the RBI Fair Practices bias audit requirement.
- **NHI as a deliverable:** In Build. Core MCP tracing is the deliverable; NHI is a roadmap item.

---

## 6. Cursory Bridge Recommendations

### Gap: Credit Model Bias Audit (R5)
**Cursory service:** Specialist firm referral (Cursory does not perform statistical model bias audits)
**Delivers:** A qualified ML fairness specialist conducts the statistical disparate impact testing — demographic parity, equalised odds — across protected characteristics (gender, caste, religion, age) required by RBI Fair Practices Code and ISO 42001 Annex A Bias Evaluation controls. Cursory will provide a curated shortlist of qualified specialists with demonstrated experience in credit model bias evaluation under Indian regulatory requirements (firms such as Credo AI, Vijil, or equivalent). If the customer requires a specific firm approved by their internal vendor panel, Cursory scopes the work and the customer selects from their panel. Cursory facilitates the statement of work and provides audit evidence requirements so the specialist's deliverable is regulator-ready.
**Alongside Ethana:** Ethana's Bias Scanner detects bias-related signals in LLM output at runtime — this is an operational safeguard, not a formal audit. The two controls are complementary and non-overlapping: the specialist firm audits the training-time model for statistical bias; Ethana guards runtime outputs for biased language patterns in individual responses. Both should be referenced in the proposal as part of the bias control framework.

### Gap: Agent NHI Lifecycle Management (R7 NHI component)
**Cursory service:** Governance Programs
**Delivers:** Design and operation of a manual NHI policy: agent credential register (names, access scopes, owners), quarterly access review checklist, offboarding procedure for decommissioned agents, and an exception process for elevated-privilege agents.
**Alongside Ethana:** Ethana MCP Broker provides per-call tracing today. The Governance Programs layer adds the lifecycle governance (issuance and review) that NHI module will automate when shipped. The two are complementary and the manual policy transitions naturally to the automated platform capability.

### Gap: SOC 2 Procurement Gate (R8)
**Cursory service:** Regulatory Gap Analysis
**Delivers:** A Cursory advisory engagement assessing Ethana's current SOC 2 readiness posture, identifying the expected certification timeline, and providing the bank's TPRM team with a documented risk acceptance framework for engaging pre-certified vendors. This does not substitute for the certification — it provides the bank's risk team with the evidence package to support a conditional approval or pilot scope.
**Alongside Ethana:** The outcome of the Regulatory Gap Analysis informs the advisory-first Phase 1 and creates the conditions for a phased platform entry once the certification milestone is met.

---

## 7. Gap Register

| # | Requirement | Why it is a gap | Best available alternative |
|---|---|---|---|
| R5 | Formal credit model bias audit (RBI Fair Practices) | Ethana Bias Scanner is a runtime text filter; does not perform statistical bias testing on credit model outputs | Specialist ML fairness firm for formal bias evaluation; Ethana Bias Scanner for runtime monitoring |
| R8 | SOC 2 Type II for Group CISO vendor programme | Ethana SOC 2 is In Build; no certification exists today | Cursory Regulatory Gap Analysis + conditional TPRM approval; revisit once SOC 2 achieved |

---

## 8. Competitive Positioning

### vs. LangSmith (Databricks) / Langfuse — LLM Observability
**Ethana differentiated strength:** Compliance-native architecture. Ethana's Immutable Audit Log is insert-only at the database layer — not a policy-level WORM, not a SIEM bolt-on. Every LLM call is audit-ready by design. VPC and on-prem deployment options are native, not add-ons. BFSI-targeted product decisions (per-tenant isolation, RBI-aligned schema options).
**Ethana honest gap:** LangSmith and Langfuse have significantly richer developer observability UIs — trace waterfall views, latency heatmaps, prompt playground. For teams where developer productivity is the primary driver, these tools have superior UX. They are also open-ecosystem with broader LLM framework integrations.
**Win condition:** The bank's primary driver is RBI compliance evidence (audit trail, examiner-ready logs), not developer observability. The CISO and compliance team are the buying centre. VPC data residency is non-negotiable.
**Loss condition:** The primary buyer is the engineering team and developer experience is the weighted priority. Observability depth is more important than compliance-native architecture.

### vs. Aporia / Lakera Guard — Runtime AI Guardrails
**Ethana differentiated strength:** Six production scanners natively integrated with the LLM gateway in a single API call — no separate middleware layer or second integration point. Bidirectional coverage (request and response) by design. Every guardrail decision is written to the Immutable Audit Log, creating a tamper-proof chain: LLM call → scanner disposition → audit record. For an RBI examiner reviewing AI controls, this linkage — platform-native and insert-only — is the proof of control. Aporia and Lakera are guardrail-first products; they require separate integration with whatever audit layer the customer assembles.
**Ethana honest gap:** Aporia and Lakera offer broader custom policy libraries and finer-tuning options for domain-specific classifiers. A BFSI customer with specific credit-terminology guardrail requirements (regional language patterns, product-specific jargon filtering) will find more configurability in Aporia's custom policy framework than in Ethana's six out-of-box scanners. Lakera's injection detection depth is also deeper than Ethana's prompt injection scanner in edge-case adversarial scenarios.
**Win condition:** The bank's buying centre is the CISO and compliance team, not the AI engineering team. The requirement is runtime coverage with a linked, regulator-ready audit record. Gateway-native integration and RBI audit trail are the weighted criteria. Purchasing a point guardrail tool (Aporia) separately from a gateway (LangSmith) requires two integrations and produces two audit streams.
**Loss condition:** The bank's security engineering team wants to write and maintain custom domain-specific classifiers — credit jargon detection in Hindi and regional languages — that exceed Ethana's configurability. Or the team already has a SIEM-centric audit architecture and wants guardrails that emit directly to their existing pipeline.

### vs. Manual CISO Processes — Audit Trail
**Ethana differentiated strength:** The Immutable Audit Log replaces three manual processes in one: (1) application-layer logging (today done via custom CloudWatch rules), (2) manual SIEM export scripting, and (3) ad-hoc incident reconstruction. The insert-only design eliminates the possibility of log tampering that manual processes cannot prevent.
**Ethana honest gap:** Manual processes can be tailored to exact RBI examiner formats without constraint. Ethana's schema is configurable but not fully bespoke.
**Win condition:** The bank wants to demonstrate to RBI examiners that AI audit controls are systematic, not ad-hoc. The immutability guarantee is the differentiator.
**Loss condition:** The bank's IT team has existing SIEM infrastructure they prefer to extend, and the compliance requirement is light enough that custom SIEM rules suffice.

---

## 9. Recommended Commercial Motion

**Motion type:** Advisory-First

**Trigger:** SOC 2 Type II is a procurement gate for the Singapore Group CISO's vendor programme. The platform cannot be commercially onboarded as a vendor until SOC 2 is achieved, regardless of capability quality. Advisory services fall under a different procurement track.

**Phase 1 (Immediate — 6 to 8 weeks):**
- Cursory Regulatory Gap Analysis: maps the bank's RBI IT Governance and DPDP Act control requirements to Ethana Build capabilities; produces the TPRM evidence package for conditional vendor approval; identifies SOC 2 expected timeline.
- Cursory Governance Programs: designs the NHI policy for agent workflows (manual, pending NHI module).
- Cursory Red Teaming as a Service: one red team exercise against the credit AI assistants currently in prototype (using 21 OWASP probes); baseline security evidence for the CISO.

**Phase 2 (Conditional on TPRM approval or SOC 2 milestone — target Q4 2026):**
- Ethana Build license: Gateway + Guardrails (PII, Injection, Jailbreak, Toxicity) + Immutable Audit Log + MCP Broker core + Red Teaming Orchestrator.
- Deployed in customer VPC (Mumbai AWS).
- Cursory Implementation Service for VPC deployment and configuration (guardrail rules, audit log schema, SIEM connector setup).

**Phase 3 (When In Build capabilities ship):**
- NHI module added to existing Build license.
- CI/CD Red Teaming Gate added.
- Ethana Edge for any endpoint AI monitoring requirements that emerge from the agent programme.

**Deal guardrails:**
- Phase 1 proposal must not include a Build platform license.
- Phase 2 proposal must not claim SOC 2 certification as achieved.
- NHI must not appear as a deliverable in Phase 2.
- Bias Scanner must be presented as a runtime control, not as satisfying the formal bias audit requirement.
- ISO 27001 must not be claimed in any phase.

**Success criteria for Phase 1:** TPRM evidence package accepted by Group CISO team; NHI manual policy designed and approved by bank CISO; red team baseline exercise completed with findings report.

**Expansion path:** Phase 2 Build license is the natural follow-on. If the agent programme scales, NHI module and Edge become the expansion. If the bank's parent group rolls out Ethana group-wide, the individual bank instance can be federated under the parent's tenant.

---

## 10. Customer-Facing Executive Summary

Ethana Build addresses the core of the bank's LLM governance requirements with production-grade capabilities. The LLM Gateway provides multi-model routing with approximately 50ms overhead, deployed natively within the bank's AWS VPC. Runtime Guardrails — covering PII masking, prompt injection, jailbreak, and toxicity detection — operate bidirectionally at sub-200ms p95 latency. The Immutable Audit Log captures every LLM call in a tamper-proof, insert-only store with SIEM export designed for RBI examiner review. The Red Teaming Orchestrator runs 21 OWASP probes against deployed AI systems on demand. MCP Security Broker provides per-call tracing for agent workflows today, with Non-Human Identity management coming in the next phase.

Two gaps require bridging. First, the bias audit requirement under RBI Fair Practices Code cannot be addressed by Ethana's runtime Bias Scanner, which detects bias signals in LLM output but does not perform the statistical disparate impact testing required for formal compliance. Cursory will facilitate engagement with a qualified ML fairness specialist for this control. Second, Ethana's SOC 2 Type II certification is currently In Build, which creates a procurement gate for the Group CISO's vendor programme.

The recommended approach is Advisory-First: Cursory engages on regulatory mapping, NHI policy design, and a baseline red team exercise under advisory procurement — building the evidence package and design blueprint the bank needs — while the platform onboards once the SOC 2 milestone enables vendor approval. The initial advisory scope is deliverable within six to eight weeks and creates the conditions for a full Build deployment in the second half of 2026.

---

---

# Example 2: European Fintech — Employee Shadow AI Discovery

**Date of Mapping:** 2026-06-17
**Customer:** Series C European fintech, 800 employees, UK-headquartered with EU operations (Germany, Netherlands)
**Sector:** Fintech (FCA-licensed in UK; not PRA-regulated; BaFin-registered in Germany)
**Output Mode:** Discovery Conversation (preparing a proposal for next meeting)
**Requirement Source:** CISO discovery conversation + implied requirements from FCA SYSC 9 obligations
**Deployment Constraint:** Cloud preferred; EU data residency for employee data
**Existing Subscription:** None
**Analysis Status:** Final

**Customer context:** The fintech's CISO attended a board session where shadow AI use (employees using ChatGPT, Claude.ai, Perplexity) was flagged as a risk. The CISO wants: (a) visibility into what AI tools employees are using, (b) some form of monitoring or policy for browser-native AI, (c) governance for the internal LLM applications the engineering team is building on top of OpenAI API, and (d) a general AI security and compliance posture. No formal procurement gate has been identified yet — this is an early discovery meeting preparing for a proposal.

---

## 1. Requirement Coverage Map

| # | Requirement | Matched Ethana Capability | Status | CCS | Disposition |
|---|---|---|---|---|---|
| R1 | Shadow AI employee inventory (what tools are employees using?) | Ethana Discovery — SaaS connectors | In Build | 0 | Roadmap mention + Cursory bridge |
| R2 | Browser-native AI monitoring (ChatGPT, Claude.ai in browser) | Ethana Edge — browser extension | In Build | 0 | Roadmap mention + Cursory bridge |
| R3 | Per-user AI usage attribution (who is using what, how much?) | Ethana Discovery — usage analytics | In Build | 0 | Roadmap mention + Cursory bridge |
| R4 | AI traffic policy enforcement (block/allow AI tools by category) | AI Firewall — policy enforcement | In Build | 0 | Roadmap mention + Cursory bridge |
| R5 | Audit log for internal LLM applications (engineering team) | Immutable Audit Log | Production | 80 | Include in discovery output |
| R6 | FCA SYSC 9 AI-related audit evidence | Immutable Audit Log | Production | 75 | Include in discovery output (caveat: API-layer only) |
| R7 | Runtime guardrails for internal LLM apps (PII, injection, jailbreak) | Runtime Guardrails (6 scanners) | Production | 90 | Include in discovery output |
| R8 | Automated red teaming for internal AI | Red Teaming Orchestrator | Production | 78 | Include in discovery output (CI/CD gate caveat) |
| R9 | EU data residency for employee data | VPC / EU-region deployment | Production | 88 | Include in discovery output |

---

## 2. Coverage Confidence Summary

**Average CCS (across all requirements):** 35/100
**Distribution:** Full/High (70+): 4 req (R5–R9) | Partial (50–69): 0 req | Thin/None (0–24): 5 req (R1–R4)
**Coverage characterisation:** Cursory-Primary for the employee monitoring layer (R1–R4); Platform-Primary for the internal AI application governance layer (R5–R9)

**Coverage story:** The requirement set splits cleanly into two tracks. Track A (shadow AI discovery and browser monitoring, R1–R4) is the CISO's primary concern but maps entirely to Ethana Edge and Discovery, both In Build — Cursory AI Inventory & Classification service is the bridge for this track today. Track B (internal LLM application governance, R5–R9) maps strongly to Ethana Build with a Production coverage profile — this is the natural platform entry point. Land-and-Expand motion recommended: enter with Build for Track B now; Track A expands when Edge and Discovery ship.

---

## 3. Proposal-Safe Platform Capabilities

*Output mode: Discovery Conversation. Language is engaged and direct, not formal proposal copy.*

### Immutable Audit Log + LLM Gateway (for internal LLM apps)
**Status:** Production | **CCS:** 80/100 (High)
**Discovery language:** "For the internal applications your engineering team is building on OpenAI's API — the audit trail, the guardrails, the routing controls — that's exactly what Ethana Build does in production today. Every LLM call goes through the gateway, every request and response is captured in an immutable log that feeds into Splunk or Datadog, and every output is scanned for PII, prompt injection, and jailbreak attempts in real time. That's your FCA SYSC 9 audit trail, your data protection controls for employee data, and your AI security layer — all in one."
**Mandatory caveat:** Coverage is for API-routed LLM traffic. Browser-native AI tools (ChatGPT.com, Claude.ai) are not captured by this layer — that requires Edge, which is in build.

### Runtime Guardrails
**Status:** Production | **CCS:** 90/100 (Full)
**Discovery language:** "The guardrails are bidirectional — they scan what goes in and what comes out. PII, prompt injection, jailbreak, toxicity, secrets, hallucination grounding. Sub-200ms. They run on every call, in production, not as a separate evaluation step."

### EU VPC Deployment
**Status:** Production | **CCS:** 88/100 (High)
**Discovery language:** "EU data residency is straightforward — we deploy inside your GCP or AWS VPC in the EU region you specify. Employee audit log data and model traffic stay within the data perimeter."

---

## 4. Roadmap Disclosure

*Discovery register only. Not for any written proposal deliverable.*

### Shadow AI Discovery (Ethana Discovery)
**Status:** In Build
**What it will provide when shipped:** SaaS connector-based inventory of AI tools in use across the organisation — identity provider integration to see what AI services employees have authenticated to, OAuth scope analysis, and per-user usage attribution. IdP connector is first in the build sequence.
**Today, Cursory bridges this with:** AI Inventory & Classification service. Cursory consultants conduct a structured discovery exercise: IdP data pull, browser history sampling (with employee consent), SaaS spend analysis, and a structured employee survey. Outputs: AI tool inventory map, risk classification per tool, and a use policy recommendation. Typically deliverable in four to six weeks.
**Anticipated CCS when shipped:** 70/100

### Browser AI Monitoring (Ethana Edge — browser extension)
**Status:** In Build
**What it will provide when shipped:** Browser extension that monitors AI tool interactions at the endpoint — capturing what tools employees access, what data is pasted in, and whether AI outputs are saved or shared. Enforcement policy (block/warn/allow by tool category) configurable by the CISO.
**Today, Cursory bridges this with:** Partial coverage via AI Inventory service (identifies the tools but not the content). A Zscaler or Netskope integration can provide network-layer AI traffic blocking for sanctioned/unsanctioned categories if the fintech has existing SWG infrastructure.
**Anticipated CCS when shipped:** 75/100

### Per-User AI Attribution and AI Traffic Policy (Ethana Discovery + AI Firewall)
**Status:** In Build
**What it will provide when shipped:** Per-user AI usage dashboards (volume, tool, data classification of queries) and policy enforcement (block tool categories, enforce approved-tools-only at the gateway layer for internal apps).
**Today, Cursory bridges this with:** AI Inventory service plus manual policy design (Governance Programs) — an approved tools list and use policy. Policy enforcement is manual and relies on awareness training until Edge/Discovery ship.
**Anticipated CCS when shipped:** 60/100

---

## 5. Prohibited Claims Register

The following must not appear in any written follow-up or proposal for this engagement:

- **Ethana Edge (browser monitoring, endpoint visibility):** In Build. Cannot be delivered as part of a proposal commitment.
- **Ethana Discovery (SaaS connector inventory, per-user attribution):** In Build. Cannot be delivered as a proposal commitment.
- **AI Firewall (traffic policy enforcement):** In Build. Cannot be delivered as a proposal commitment.
- **"Real-time employee AI monitoring" as a current capability:** Not available. Discovery and Edge are the capabilities that provide this; both In Build.
- **SOC 2 Type II, ISO 27001:** Not certified. Should not arise in this engagement (non-BFSI) but must not be claimed if asked.
- **Ethana Workspace (enterprise chat, RAG):** Aspirational. Must not appear.
- **"We can show you what employees are pasting into ChatGPT today":** Not producible from Production capabilities. Do not claim in discovery conversation.

---

## 6. Cursory Bridge Recommendations

### Gap: Shadow AI Employee Inventory (R1, R3)
**Cursory service:** AI Inventory & Classification
**Delivers:** Structured discovery of AI tools in use across the organisation. Methodology: IdP data pull (Google Workspace or Azure AD), browser history sampling (with appropriate employee consent framework), SaaS spend analysis, and a 15-minute structured employee survey. Output: an AI tool inventory map classified by risk tier (consumer AI, API-integrated AI, unapproved enterprise AI), per-department attribution, and a use policy recommendation. Deliverable in four to six weeks.
**Alongside Ethana:** The inventory identifies which AI tools need governance. Ethana Build governs the internal AI applications immediately; Edge/Discovery extends coverage to shadow tools when shipped.

### Gap: Browser AI Monitoring (R2)
**Cursory service:** AI Inventory & Classification (partial coverage) + SWG integration advisory (if fintech has Zscaler or Netskope)
**Delivers:** Network-layer AI traffic categorisation for managed devices via existing SWG infrastructure, if available. Cursory advises on category configuration and policy rules. If no SWG exists, Cursory designs the policy framework for when Edge ships.
**Note:** No human service equivalent for real-time browser content monitoring. This is an honest gap until Edge ships.

### Gap: AI Traffic Policy Enforcement (R4)
**Cursory service:** Policy & Control Design
**Delivers:** An AI use policy covering approved tools, prohibited tools, data classification guidance for AI queries, and an attestation process. Paired with an awareness programme. Manual enforcement until AI Firewall ships.

---

## 7. Gap Register

| # | Requirement | Why it is a gap | Best available alternative |
|---|---|---|---|
| R1 | Shadow AI employee inventory | Ethana Discovery In Build; no production equivalent | AI Inventory & Classification service (Cursory) |
| R2 | Browser-native AI monitoring | Ethana Edge In Build; no production endpoint equivalent | SWG integration advisory (if existing SWG); awareness training |
| R3 | Per-user AI usage attribution | Ethana Discovery In Build | AI Inventory service (aggregated, not real-time per-user) |
| R4 | AI traffic policy enforcement | AI Firewall In Build | Policy & Control Design (Cursory) + approved tools list |

---

## 8. Competitive Positioning

### vs. Zscaler / Netskope — Shadow AI Discovery and Browser Monitoring
**Ethana differentiated strength:** Ethana Build governs the engineering team's internal LLM applications — API-layer governance, immutable audit log, bidirectional guardrails. This is production capability that SWG players do not address (they monitor network traffic, not application-layer LLM governance). Ethana is the governance layer that activates after SWG identifies what tools are in use.
**Ethana honest gap:** Zscaler and Netskope have production browser and endpoint AI monitoring today. They can see that an employee opened ChatGPT and block it at the network layer. Ethana Edge, which will do this at the endpoint level, is In Build. For shadow AI discovery and browser monitoring specifically, these SWG players have production capability that Ethana does not.
**Win condition:** Customer wants API-layer governance for internal AI applications (what the engineering team builds) alongside shadow AI visibility. Ethana owns the internal governance; SWG owns or bridges the shadow monitoring.
**Loss condition:** Customer's primary need is shadow AI blocking at the network layer and they want a single vendor solution — Zscaler or Netskope win the immediate requirement. Ethana becomes additive when internal AI applications mature.
**Positioning recommendation:** Do not compete against Zscaler/Netskope on browser monitoring. Instead, position Ethana as the governance layer that works alongside them — "once Zscaler tells you what tools employees are using, Ethana governs what your engineers build."

### vs. ChatGPT Enterprise / Microsoft Copilot — "Can we just use one of these instead?"
**Ethana differentiated strength:** ChatGPT Enterprise and Copilot lock the fintech into one AI vendor. Ethana Build governs any AI model — OpenAI, Anthropic, open-source — with a single audit trail and guardrail stack. As the engineering team wants to experiment with different models, vendor-agnostic governance becomes the moat.
**Ethana honest gap:** ChatGPT Enterprise is a turnkey employee AI product — no integration required. If the CISO's primary goal is "let employees use AI safely with minimal IT burden," ChatGPT Enterprise is a simpler path. Ethana requires engineering integration.
**Win condition:** The fintech has an active engineering team building internal AI applications and wants to govern both internal apps and employee tools under one control layer, vendor-agnostically.
**Loss condition:** The CISO wants turnkey employee AI with minimal engineering. Single-vendor is acceptable.

---

## 9. Recommended Commercial Motion

**Motion type:** Land-and-Expand

**Rationale:** The requirement set has two distinct tracks — one where Ethana is strong today (internal app governance) and one where Ethana is In Build (employee monitoring). Enter on Track B, bridge Track A with Cursory, and expand to Track A when Edge/Discovery ship.

**Phase 1 (Immediate — proposal for next meeting):**
- Ethana Build license: Gateway + Guardrails (all six scanners) + Immutable Audit Log + Red Teaming Orchestrator. EU VPC deployment.
- Cursory AI Inventory & Classification: four to six week engagement to map the shadow AI landscape and produce the CISO's board-ready risk report.
- Cursory Policy & Control Design: approved AI tools policy and employee use framework.

**Phase 2 (Advisory bridge — parallel to Phase 1):**
- Cursory advisory to design the policy rules for Edge enforcement (so rules are ready when Edge ships).
- If fintech has Zscaler or Netskope: Cursory to configure AI traffic categories — partial shadow monitoring coverage now, full coverage when Edge ships.

**Phase 3 (When Ethana Edge and Discovery ship):**
- Edge browser extension deployment across managed devices.
- Discovery IdP connector for per-user attribution.
- AI Firewall policy activation.
- Phase 1 advisory scope transitions to platform — no new advisory needed.

**Deal guardrails:**
- Phase 1 proposal must not include Edge or Discovery as deliverables.
- Phase 1 proposal must not reference per-user real-time monitoring as a current capability.
- AI Firewall must not appear as a Phase 1 deliverable.
- Do not reference SOC 2 or ISO 27001 in this proposal (not a BFSI procurement gate here, but still uncertified).

**Success criteria for Phase 1:** Build deployed in EU VPC, internal LLM applications routing through Gateway, shadow AI inventory report delivered to CISO, employee AI use policy in place.

**Expansion path:** Phase 3 Edge and Discovery expand coverage from internal apps (Build) to all employee AI (Edge + Discovery), converting the Cursory advisory scope into a platform capability without re-selling.

---

## 10. Customer-Facing Executive Summary

The CISO's concern covers two distinct areas with different timelines. For the internal LLM applications the engineering team is building — the API-layer audit trail, guardrails, and security controls — Ethana Build addresses these in production today. The LLM Gateway routes all engineering AI traffic through bidirectional guardrails (PII masking, prompt injection, jailbreak, toxicity) at sub-200ms latency, and the Immutable Audit Log captures every call in an insert-only, SIEM-ready event store. This gives the CISO FCA SYSC 9-grade audit evidence for internal AI immediately, deployed within the fintech's EU VPC.

For the shadow AI question — what employees are using in their browsers, how much, and what data they are sharing with ChatGPT — Ethana's Edge and Discovery products address this, but they are currently In Build. Cursory fills this gap today with the AI Inventory & Classification service: a structured four to six week exercise that maps the shadow AI landscape, classifies tools by risk, and produces the board-ready risk report the CISO needs. Cursory Policy & Control Design then creates the approved tools list and employee use policy, with rules designed to activate on the Edge platform when it ships.

The recommended path is to enter on the internal governance side now, bridge the shadow AI question with Cursory advisory, and expand to full employee monitoring coverage when Edge and Discovery ship. This gives the CISO a defensible posture immediately while building toward complete coverage.

---

---

# Example 3: Enterprise Technology Company — RFP with Aspirational Traps

**Date of Mapping:** 2026-06-17
**Customer:** 2,400-employee SaaS company, US-headquartered, EU and UK operations. Not BFSI. Expanding AI use across engineering, customer support, and operations teams.
**Sector:** General Enterprise (EU and UK jurisdiction exposure via operations)
**Output Mode:** RFP Response
**Requirement Source:** Customer-issued RFP — eight numbered questions
**Deployment Constraint:** Cloud (no specific data residency constraint stated)
**Existing Subscription:** None
**Analysis Status:** Final

**Customer context:** The RFP was issued by the Head of IT and CISO jointly. The company has seen competitors deploy Copilot Studio and ChatGPT Enterprise. The RFP asks about enterprise AI chat, RAG, agent building, and ISO 27001 certification alongside the LLM security and governance requirements. The Workspace and Visual Agent Builder questions reflect the customer's exposure to competitor products. The LLM security requirements (items 5–8) are specific and well-articulated. This is a common pattern: an RFP written from a competitor's feature sheet, with Ethana's production strengths buried in items 5–8.

**RFP questions:**
1. Can you provide a governed enterprise chat interface for employees?
2. Can the platform support RAG on internal document repositories?
3. Does the platform include a visual agent builder or DAG orchestrator?
4. Is the vendor ISO 27001 certified?
5. Can the platform provide a multi-model LLM gateway with routing and fallback?
6. Does the platform include runtime guardrails (PII, prompt injection, jailbreak)?
7. Is there an immutable audit log of all AI interactions?
8. Does the platform support automated red teaming of deployed AI models?

---

## 1. Requirement Coverage Map

| # | RFP Item | Matched Ethana Capability | Status | CCS | Disposition |
|---|---|---|---|---|---|
| R1 | Governed enterprise chat interface | Workspace — Enterprise Chat | Aspirational | 0 | Section 5 (Prohibited) + redirect in RFP |
| R2 | RAG on internal document repositories | Workspace — RAG / Document Workflows | Aspirational | 0 | Section 5 (Prohibited) + redirect in RFP |
| R3 | Visual agent builder / DAG orchestrator | Visual Agent Builder | Aspirational | 0 | Section 5 (Prohibited) + redirect in RFP |
| R4 | ISO 27001 certified vendor | ISO 27001 (In Progress) | In Build | 0 | Section 5 (Prohibited) + honest RFP disclosure |
| R5 | Multi-model LLM gateway with routing and fallback | LLM Gateway | Production | 95 | Include in RFP response — YES |
| R6 | Runtime guardrails: PII, prompt injection, jailbreak | Guardrails: PII + Injection + Jailbreak Scanners | Production | 90 | Include in RFP response — YES |
| R7 | Immutable audit log of all AI interactions | Immutable Audit Log | Production | 90 | Include in RFP response — YES |
| R8 | Automated red teaming of deployed AI | Red Teaming Orchestrator | Production | 80 | Include in RFP response — YES (CI/CD gate caveat) |

---

## 2. Coverage Confidence Summary

**Average CCS (across all eight RFP items):** 44/100
**Distribution:** Full/High (70+): 4 req (R5–R8) | None (0): 4 req (R1–R4)
**Coverage characterisation:** Bifurcated — Platform-Primary for items 5–8 (Ethana Build core); zero coverage for items 1–4 (Aspirational and uncertified)

**Coverage story:** This RFP follows a known pattern — half the questions are about product categories Ethana does not compete in today (enterprise chat, RAG, visual agent builder, certification), and half are about what Ethana Build does exceptionally well in production. The right response is not to deflect items 1–4 but to answer them explicitly with NO (items 1–3) or ROADMAP (item 4) and redirect the evaluation toward what a governance-first buyer actually needs. The Build core items (5–8) score 80–95, which are among the strongest Production coverage scores in the capability set.

---

## 3. Proposal-Safe Platform Capabilities

*Output mode: RFP Response. Format follows YES / ROADMAP / NO convention.*

### Item 5: Multi-Model LLM Gateway
**Status:** Production | **CCS:** 95/100 | **RFP answer: YES**
**Claim language:** "YES. Ethana's LLM Gateway provides multi-model routing across GPT-4o, Claude 3.x, Gemini, Mistral, and open-source models (Llama 3, Qwen) with configurable fallback chains and per-call latency overhead of approximately 50ms at p95. The gateway supports priority routing, cost-based routing, and capacity-based failover. It is the foundation of Ethana Build and is in production with multi-tenant support."

### Item 6: Runtime Guardrails
**Status:** Production | **CCS:** 90/100 | **RFP answer: YES**
**Claim language:** "YES. Ethana includes six production runtime guardrail scanners: PII detection and redaction, prompt injection detection, jailbreak detection, toxicity detection, secret leakage detection, and hallucination grounding. All operate bidirectionally (on requests and responses) at sub-200ms p95 latency. Scanners are integrated into the gateway — no separate API call required."

### Item 7: Immutable Audit Log
**Status:** Production | **CCS:** 90/100 | **RFP answer: YES**
**Claim language:** "YES. Ethana's Immutable Audit Log captures every gateway-routed LLM call in a tamper-proof, insert-only event store. Records cannot be modified or deleted post-write. Native SIEM connectors export to Splunk, Elastic, and Datadog. The audit log is multi-tenant, supports per-project and per-user attribution, and is designed for regulatory evidence use cases."

### Item 8: Automated Red Teaming
**Status:** Production | **CCS:** 80/100 | **RFP answer: YES (with caveat)**
**Claim language:** "YES. Ethana's Red Teaming Orchestrator runs 21 OWASP LLM Top 10 probes against deployed AI models with multi-turn attack simulation — covering prompt injection, jailbreak, data poisoning, insecure output handling, and excessive agency risks. Orchestration runs on-demand or on a scheduled cadence."
**Mandatory caveat:** Automated CI/CD pipeline integration (triggering red teaming on every model deployment as a pipeline gate) is currently on the roadmap. The production capability covers on-demand and scheduled execution. If CI/CD integration is a requirement, please confirm and we will provide a roadmap update.

---

## 4. Roadmap Disclosure

*For transparency in the RFP. Not as a deliverable commitment.*

### Item 4: ISO 27001 Certification
**Status:** In Build (In Progress)
**RFP disclosure:** "ISO 27001 certification is currently in progress. Ethana is not certified at the time of this response. If ISO 27001 is a procurement gate, we are pleased to discuss the expected certification timeline and whether a conditional approval or pilot scope is feasible while the certification is in process."
**Today:** Ethana operates under security controls aligned with ISO 27001 requirements but does not hold the certification. Independent audit will validate this.

### Item 8 Caveat: CI/CD Gate for Red Teaming
**Status:** In Build
**Roadmap disclosure:** "CI/CD pipeline integration for automated red teaming is on the Ethana roadmap. The current production capability delivers on-demand and scheduled red team orchestration; the CI/CD gate (blocking deployments on probe failures) is the next development phase."

---

## 5. Prohibited Claims Register

The following must not appear in the RFP response under any framing:

- **Governed enterprise chat (Item 1):** Workspace is Aspirational. The answer to this RFP item is NO. Must not be softened to "ROADMAP" or "COMING SOON" — Workspace has no engineering basis confirmed in the board briefing. Do not claim.
- **RAG on internal documents (Item 2):** Workspace is Aspirational. The answer to this RFP item is NO, with a redirect (see Section 6). Must not be positioned as a current or near-term capability.
- **Visual agent builder / DAG orchestrator (Item 3):** Aspirational. Answer is NO. Ethana MCP Broker is the Production capability for agent security; it is not a visual builder. Do not conflate.
- **"ISO 27001 certified" (Item 4):** Not certified. The answer is ROADMAP / IN PROGRESS. Must not appear as a positive claim.
- **"Our enterprise customers can build workflows through a drag-and-drop interface":** References Visual Agent Builder. Prohibited.
- **"Ethana Workspace will be available to your employees as a governed chat interface":** Workspace is Aspirational. Any timeline claim is prohibited.
- **SOC 2 Type II:** Not certified. Must not be claimed.

---

## 6. Cursory Bridge Recommendations

### Gap: Enterprise Chat for Employees (R1) — Redirect
**Cursory service:** Advisory on Build Gateway + customer-built application architecture
**Delivers:** Rather than providing a chat interface, Ethana provides the governance layer that makes any chat interface enterprise-safe. Cursory advises on architecture: the customer's engineering team builds or deploys a lightweight chat UI (Next.js, Streamlit, or similar); Ethana Build Gateway routes and governs all model calls; the Immutable Audit Log captures every conversation. The customer retains full control over the chat UX while Ethana provides the compliance and security infrastructure.
**Note:** This is an architectural redirect, not an Ethana product. Position honestly: "Ethana is the governance layer. Your team — or a partner — builds the chat experience."

### Gap: RAG on Internal Documents (R2) — Redirect
**Cursory service:** Advisory on LangChain / LlamaIndex + Build Gateway architecture
**Delivers:** Cursory advises on integrating a standard RAG framework (LangChain, LlamaIndex) with Ethana Build Gateway — so all RAG retrieval calls go through the gateway, are guarded by guardrails (prompt injection on retrieval queries, PII in retrieved chunks), and are logged in the Immutable Audit Log. The RAG pipeline is customer-built or partner-built; Ethana governs it.

### Gap: Visual Agent Builder (R3) — Redirect
**Cursory service:** Advisory on LangGraph / CrewAI via Build MCP Broker
**Delivers:** Cursory advises on agent orchestration using code-first frameworks (LangGraph, CrewAI, Autogen). Ethana Build MCP Broker provides security and audit for all agent tool calls. The visual builder is replaced by a code-first approach appropriate for the customer's engineering team.

---

## 7. Gap Register

| # | RFP Item | Why it is a gap | Best available alternative |
|---|---|---|---|
| R1 | Governed enterprise chat | Workspace is Aspirational; no production equivalent | Build Gateway + customer-built chat UI; Microsoft Copilot Studio or ChatGPT Enterprise are production alternatives |
| R2 | RAG on internal documents | Workspace is Aspirational | LangChain/LlamaIndex + Build Gateway governance layer |
| R3 | Visual agent builder / DAG | Visual Agent Builder is Aspirational | Code-first agent frameworks (LangGraph, CrewAI) + MCP Broker |

---

## 8. Competitive Positioning

### vs. Microsoft Copilot Studio (Items 1, 2, 3)
**Ethana differentiated strength:** Vendor-agnostic governance. Ethana Build governs AI across any model — OpenAI, Anthropic, Google, open-source. If the company adds a new model, Ethana governs it without re-configuration. Copilot Studio is Microsoft-only. Ethana's Immutable Audit Log and Guardrails apply uniformly across the company's entire AI estate. Copilot Studio audits Copilot activity; it does not govern AI calls the engineering team makes to OpenAI or Anthropic directly.
**Ethana honest gap:** Microsoft Copilot Studio is in production and includes enterprise chat, RAG, and visual agent builder today. If items 1–3 are the company's primary requirements and they are willing to be Microsoft-only for AI, Copilot Studio solves those requirements without integration work. Ethana does not compete on turnkey enterprise chat or RAG.
**Win condition:** The company has a diverse AI strategy (multiple models, multiple vendors), an engineering team that builds internal AI applications, and compliance or audit requirements that require a vendor-agnostic governance layer. The evaluation weight on items 5–8 is equal to or greater than items 1–3.
**Loss condition:** The company wants a turnkey solution with no integration work, is already in the Microsoft ecosystem, and the evaluation weight on items 1–3 significantly outweighs items 5–8.
**Recommended positioning statement:** "Ethana is the governance layer that makes your AI strategy sustainable as it scales across vendors and models. Whether you deploy Copilot Studio for employee chat today, or switch to Claude next year, or build your own RAG pipeline — Ethana audits it, guards it, and red teams it. You don't need to choose Ethana instead of Copilot Studio. You can choose Ethana alongside it."

### vs. ChatGPT Enterprise (Item 1)
**Ethana differentiated strength:** ChatGPT Enterprise governs ChatGPT. Ethana governs ChatGPT and everything else. If the company also uses internal models, Anthropic, or Gemini, ChatGPT Enterprise provides no governance for those calls.
**Ethana honest gap:** ChatGPT Enterprise is turnkey enterprise chat with no integration required. If the company's AI use case is 100% OpenAI API and they do not need a vendor-agnostic layer, the operational simplicity of ChatGPT Enterprise is a real advantage.
**Win condition:** Multi-vendor AI strategy; engineering team building internal applications on diverse models; audit log required for non-OpenAI AI calls.
**Loss condition:** Single-vendor OpenAI-only strategy; primary requirement is employee chat with no governance beyond what OpenAI provides.

### vs. Guardrails.ai / Aporia (Item 6)
**Ethana differentiated strength:** Six production scanners natively integrated into the gateway in a single API call. Immutable audit log of every scan result built in. Bidirectional by design. Aporia and Guardrails.ai require separate integration with the model serving layer; audit trail is an add-on.
**Ethana honest gap:** Guardrails.ai and Aporia offer more customisable guardrail logic — the ability to write custom scanners, fine-tune existing ones, and build domain-specific classifiers. Ethana's six scanners are production and configurable but not fully bespoke.
**Win condition:** Customer wants integrated gateway + guardrails + audit as one product; native SIEM export; minimal integration points.
**Loss condition:** Customer needs highly customised domain-specific guardrails (medical terminology classifiers, financial jargon detection) that require fine-tuning beyond Ethana's configurability.

---

## 9. Recommended Commercial Motion

**Motion type:** Land-and-Expand (with RFP response strategy)

**RFP response strategy:**
- Items 1–3 (Workspace, Visual Builder): Answer NO. Accompany each NO with the governance-layer redirect (Section 6). Position the NO honestly — do not hedge, do not promise a ROADMAP timeline for Aspirational items.
- Item 4 (ISO 27001): Answer ROADMAP / IN PROGRESS. Offer to discuss conditional engagement.
- Items 5–8: Answer YES (with CI/CD gate caveat on item 8). Provide specific, quotable claims from Section 3.

**Phase 1 (RFP win — immediate):**
- Ethana Build license: Gateway + Guardrails (all six scanners) + Immutable Audit Log + Red Teaming Orchestrator.
- Cloud deployment.
- Cursory Implementation Service for initial deployment and guardrail configuration.
- Cursory advisory on chat + RAG architecture (how to use Build Gateway as the governance layer for whatever chat UI the company chooses).

**Phase 2 (six months post-deployment):**
- Review: has the company adopted an enterprise chat tool? If yes, route it through Ethana Gateway.
- CI/CD Red Teaming Gate when shipped.
- ISO 27001 update — revisit vendor programme if certification achieved.

**Phase 3 (twelve months):**
- Edge endpoint monitoring (if employee shadow AI becomes a concern as AI use scales).
- Potential MCP Broker expansion if engineering team builds more agent workflows.

**Deal guardrails:**
- Phase 1 proposal and all RFP response text must not include Workspace, Visual Agent Builder, SOC 2 certification, or ISO 27001 certification as positive claims.
- The CI/CD gate caveat must be present in Item 8 response.
- If the customer's evaluation team scores items 1–3 with high weight and is unwilling to accept NO answers, assess whether the deal is viable at all — do not inflate claims to win a deal that requires Aspirational capabilities.

**Success criteria for Phase 1:** Build deployed, engineering team's AI applications routed through Gateway, one red team exercise completed, audit log integrated with SIEM, governance layer advisory for chat/RAG architecture delivered.

**Expansion path:** Enterprise chat tooling (whichever the company chooses) routes through the Gateway in Phase 2, adding to the governance coverage without additional platform cost. Red teaming scales to CI/CD automation. Edge expands coverage if employee shadow AI becomes a priority.

---

## 10. Customer-Facing Executive Summary

Ethana Build directly addresses four of the eight RFP requirements with production capabilities today — multi-model LLM gateway, runtime guardrails, immutable audit log, and automated red teaming. These are the governance infrastructure requirements, and Ethana's answers are unambiguous: production, deployed, with specific performance characteristics and a native SIEM integration.

On the other four requirements — enterprise chat, RAG, visual agent builder, and ISO 27001 certification — Ethana's answer is equally direct. Enterprise chat, RAG, and visual agent building are not Ethana products, and we will not represent them as such. Ethana is the governance layer that makes your enterprise chat, your RAG pipeline, and your agent workflows auditable and secure — whichever tools you choose to build them with. ISO 27001 certification is in progress; we are not certified today.

The distinction matters because it changes what you are buying. A competitor that provides enterprise chat and a governance layer is a single-vendor bet. Ethana governs your entire AI estate — OpenAI, Anthropic, Google, open-source, or any combination — with a single audit log, a unified guardrail stack, and a red teaming programme that runs against any model you deploy. As your AI strategy grows beyond a single vendor, Ethana grows with it without re-procurement.

The recommended next step is a technical workshop with your engineering team to demonstrate the gateway, guardrails, and audit log in a sandbox environment. We can scope a 90-day pilot that gets Build deployed against your existing AI applications and delivers the first red team report within the quarter.
