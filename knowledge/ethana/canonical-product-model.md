# Ethana Canonical Product Model

**Authority:** This is the single authoritative reference for Ethana product architecture, capability status, and claim eligibility in the Governance OS.

**Supersedes (as primary reference):**
- `knowledge/ethana/capability-status.md` — historical artifact, engineering-era status matrix. Do not update; do not use as primary status source.
- `knowledge/ethana/source-of-truth.md` — historical artifact, cross-source synthesis layer. Retained for narrative context.
- `knowledge/ethana/ethana-status-reconciliation.md` — historical artifact. The status elevations in this file are explicitly rejected by primary source evidence. Do not use for commercial decisions.

**Derived from primary sources only:**
- `[PB]` Ethana Marketing Playbook, Version 1.0, June 2026 — commercial vocabulary and pricing
- `[BB]` Ethana Board Briefing, May 2026 — engineering status authority
- `[SE]` Study ethana (grounded in Board Briefing May 2026 + Barclays Governance Mapping May 2026)

**Supporting investigation:** `knowledge/ethana/product-architecture-investigation.md`

---

## Status Definitions

| Status | Meaning | Primary source basis |
|---|---|---|
| **Production** | Confirmed in "What We Have" [BB page 11] or equivalent production statement | [BB] and/or [SE] |
| **In Build** | Confirmed in "What We're Building" [BB page 11] or described as in-build in [SE] | [BB] and/or [SE] |
| **Roadmap** | Explicitly labeled roadmap in [PB]; consistent with In Build or later in [BB] | [PB] + [BB] |
| **Aspirational** | Present in [PB] but absent from [BB] at any level — not in "What We Have," not in "What We're Building," not in surface horizons | [BB] absence |

---

## Architecture Summary

The commercial product lineup ([PB]) and the engineering product lineup ([BB]) diverge. Governance OS uses commercial naming with engineering status.

| Commercial name [PB] | Engineering equivalent [BB] | Canonical status |
|---|---|---|
| **Ethana Build** (AI Infrastructure & Control) | Build — Gateway, MCP Broker, Runtime Threat Detection + shared platform services | **Production (core capabilities)** |
| **Ethana Edge** (Endpoint AI Monitoring) | Sentry (Discovery + AI Firewall, network layer) + Edge (Endpoint agent + browser + dev-tool, device layer) | **In Build — neither engineering component is in production** |
| **Ethana Workspace** (Governed AI Workspaces) | No engineering equivalent in [BB] | **Aspirational — no engineering basis at any status level** |

---

## Section 1: Ethana Build

Build is the only product line with confirmed production capabilities. It is the correct entry point for regulated accounts.

### 1.1 Production Capabilities

| Capability | Status | Customer Claim Allowed? | Proposal Safe? | Alternative Cursory Service | Notes |
|---|---|---|---|---|---|
| **LLM Gateway** — OpenAI-compatible, multi-tenant, multi-model routing and fallback | Production | Yes | Yes | N/A — platform capability | Stated ~50ms overhead. p95 latency under batch load with full guardrail stack needs test data before committing in latency-sensitive proposals. Routes to OpenAI, Anthropic, Gemini, Groq, Cerebras, self-hosted (vLLM, Ollama, llama.cpp). Non-LLM REST API proxying (AVM, NLP classifiers, ASR) is unconfirmed. |
| **Runtime Guardrails — PII detection and masking** | Production | Yes | Yes | N/A — platform capability | One of six confirmed native scanners [BB page 5 STATUS]. Bidirectional. Sub-200ms p95. False positive rate at volume unconfirmed. |
| **Runtime Guardrails — Prompt injection detection** | Production | Yes | Yes | N/A — platform capability | One of six confirmed native scanners. Jailbreak (advanced) variant also confirmed. |
| **Runtime Guardrails — Jailbreak detection** | Production | Yes | Yes | N/A — platform capability | One of six confirmed native scanners. |
| **Runtime Guardrails — Toxicity detection** | Production | Yes | Yes | N/A — platform capability | One of six confirmed native scanners. |
| **Runtime Guardrails — Secret detection** | Production | Yes | Yes | N/A — platform capability | One of six confirmed native scanners. |
| **Runtime Guardrails — Bias detection** | Production | Yes — with mandatory caveat | Yes — with caveat stated | N/A for runtime filter; bias audit → specialist firm referral | This is a **runtime text filter only**. It does not audit model weights, test disparate impact across demographic groups, or validate training data. [SE] states explicitly: "Ethana does not inspect ML training data, test disparate impact across demographic groups, or validate vendor AI Act conformity." EU AI Act Art.10 and NYC LL144 bias audit requirements cannot be met by this scanner. |
| **Runtime Guardrails — Hallucination grounding** | Production | Yes | Yes | N/A — platform capability | Appears in [BB] page 5 diagram alongside the six named scanners. Checks whether AI responses are grounded in retrieved documents. Validates output relevance, not factual accuracy against the real world. |
| **Immutable Audit Log** — insert-only event store, multi-tenant, SIEM export | Production | Yes — lead claim | Yes | N/A — platform capability. Evidence delivery → Regulatory Gap Analysis service | **Ethana's strongest and most consistent enterprise claim across all use cases** [SE]. Every [BB] production scenario references it. Write-once at the database layer. SIEM export to Splunk, Elastic, Datadog. Schema customisation for specific regulator fields (FCA SYSC 9, RBI templates) is a configuration engagement, not out-of-the-box. Logs only traffic routed through the gateway — bypassed calls are unlogged. |
| **MCP Security Broker — core** — registry, hosted runtime, tool allow-list, rate limits, per-call tracing, admin UI | Production | Yes — with NHI caveat | Yes — with NHI caveat stated | N/A — platform capability | [BB] page 7: "~8,000 lines in production. Per-call tracing shipped." NHI and ephemeral tokens are In Build (see Section 1.2). Until NHI ships, agents reuse human credentials. Mandatory disclosure: "A compromised agent is a compromised user." |
| **Red Teaming Orchestrator** — 21 OWASP probes, multi-turn attacks, targets model / LLM-app / agent | Production | Yes | Yes | Red Teaming as a Service (quarterly exercises, custom probe development) | [BB] page 6 STATUS: "Orchestrator + 21 OWASP probes in production. CI/CD gate in build." Probe coverage for RAG-specific attacks and non-LLM ML classifiers is unconfirmed. Does not block attacks at runtime — that is Guardrails. |
| **Account Management** — tenants, projects, RBAC, SSO via OIDC | Production | Yes | Yes | N/A — platform capability | [BB] page 11 "What We Have." SCIM provisioning is In Build (see Section 1.2). Automated AI vendor offboarding not yet available. |
| **Cost and Budget Tracking** — per-tenant, per-project, real-time dashboard, alert hooks | Production | Yes | Yes | N/A — platform capability | [BB] page 11 "What We Have." Per-user and per-team FinOps breakdown is In Build (see Section 1.2). |
| **PromptOps** — prompt registry, versioning, rollback, A/B testing, environment management | Production (present in platform) | Yes | Yes — with sub-feature caveat | N/A — platform capability | [SE]: "MODERATE. Present in the platform but not a standalone selling point." Not explicitly named in [BB] page 11 "What We Have" list, but consistent with Gateway production status. A/B testing confirmed; canary releases not separately validated (see Section 1.3). |
| **On-premises / VPC / Air-gapped deployment** | Production (deployment model confirmed) | Yes | Yes — with scale caveat | Ethana Implementation Service (4–8 weeks for enterprise deployment) | [BB] page 13 confirms three deployment topologies. **Critical caveat from [SE]:** "On-prem deployment at Tier 1 bank scale is unproven." State this proactively in any regulated account proposal. |
| **India VPC with gateway PII masking** | Production | Yes | Yes | N/A — platform capability | Strong differentiator for RBI-regulated accounts. All AI traffic stays in-country. Relevant for DPDP and RBI IT Outsourcing compliance. |
| **Multi-model routing — SLA / cost / reliability-aware fallback** | Production | Yes | Yes | N/A — platform capability | [BB] page 4. Enables vendor-neutral architecture — application routing without rewrites. Key objection handler for cloud-native gateway comparison. |

---

### 1.2 In Build — Ethana Build

Capabilities that are engineering-confirmed as in active development but not yet in production. May be mentioned conversationally as roadmap. Must not be committed as deliverables in proposals.

| Capability | Status | Customer Claim Allowed? | Proposal Safe? | Alternative Cursory Service | Notes |
|---|---|---|---|---|---|
| **Non-Human Identity (NHI) for agents** — ephemeral scoped tokens, OAuth 2.0 Token Exchange / SPIFFE-style workload identity, on-behalf-of delegation | In Build | Mention as roadmap only | No | Advisory on agent identity architecture (interim manual scoping) | [BB] page 11 "What We're Building"; [BB] page 7 STATUS: "NHI & ephemeral tokens in build." Until shipped, every agent reuses the calling user's credentials. This is the most strategically important In Build item for agentic deployments. |
| **CI/CD Red-Teaming Gate** — `ethana eval` action blocking pull requests on probe failure | In Build | Mention as roadmap only | No | Manual pre-deployment red teaming engagement via Cursory Red Teaming as a Service | [BB] page 6 STATUS: "CI/CD gate in build." [BB] page 11 "What We're Building." Orchestrator + probes are Production; the automated gate is not. |
| **Governance Policy Engine** — OPA / Rego with signed policy bundles pushed to every surface | In Build | Mention as roadmap only | No | Policy & Control Design service (manual policy design and guardrail configuration) | [BB] page 11 "What We're Building." Until shipped, guardrail rules require manual configuration rather than a governed policy bundle deployment model. |
| **Compliance Pack** — one-click evidence export for EU AI Act, ISO 42001, NIST AI RMF, MITRE ATLAS | In Build | Mention as roadmap only | No | Regulatory Gap Analysis service + manual evidence collection via Audit Log + SIEM | [BB] page 11 "What We're Building." Evidence collection today is human-delivered via Cursory services using the production Immutable Audit Log as the source. |
| **FinOps — full granularity** — per-user / per-team token spend, GPU cost, dormant-licence detection | In Build | Mention as roadmap only | No | AI Inventory & Classification service for licence waste identification | [BB] page 11 "What We're Building." Per-tenant / per-project tracking is Production. Per-user attribution and GPU cost tracking are not. |
| **SCIM provisioning** — automated AI vendor offboarding | In Build | Mention as roadmap only | No | Manual offboarding process advisory via Governance Programs service | [BB] page 11 "What We're Building." [SE]: "When someone leaves the bank. Their ChatGPT Enterprise, Copilot, and Cursor accounts remain active, licensed, and accessible." |
| **Enterprise features bundle** — on-prem deployment at scale, full SCIM/SSO/RBAC/audit-retention package as a hardened enterprise set | In Build | Partial — individual features (SSO, RBAC) are Production; the bundle is In Build | Partial — individual features only | Ethana Implementation Service | [BB] page 11 "What We're Building." SSO via OIDC is Production per [BB] page 11. SCIM is In Build. |

---

### 1.3 Aspirational — Ethana Build

Capabilities that appear in the commercial playbook but have no engineering basis in the board briefing at any level. Do not include in proposals or customer claims.

| Capability | Status | Customer Claim Allowed? | Proposal Safe? | Alternative Cursory Service | Notes |
|---|---|---|---|---|---|
| **Visual Agent Builder** — drag-and-drop DAG workflow design, agents / APIs / conditions / routers / loops / parallel execution / evaluators / human-in-the-loop | Aspirational | No | No | Advisory on agent architecture using code frameworks (LangGraph, CrewAI) routed through Ethana Build MCP Broker | Absent from all 15 pages of [BB]. Not in "What We Have." Not in "What We're Building." The Build section of [BB] covers Gateway and MCP Broker — no visual workflow layer. Developers must build agent logic in code. |
| **Evaluation — Dataset management** | Aspirational | No | No | Cursory advisory on evaluation dataset design | [PB] Section 4.3 lists this alongside hallucination detection, but [BB] does not separately confirm it. Hallucination grounding (runtime) and Red Teaming (adversarial) are Production; dataset management as a standalone capability is not confirmed. |
| **Evaluation — Model benchmarking** | Aspirational | No | No | Red Teaming as a Service (adversarial benchmarking) | Same basis as dataset management. [BB] Red Teaming is Production; model benchmarking as a distinct offline evaluation capability is not confirmed. |
| **Evaluation — Production sampling** | Aspirational | No | No | Advisory on sampling strategy using existing Audit Log | [PB] lists this; not referenced in [BB] at any level. |
| **PromptOps — Canary releases** | Aspirational (pending confirmation) | No until confirmed | No until confirmed | Advisory on staged rollout strategy using existing A/B testing | [PB] lists this as a PromptOps sub-feature. Not separately confirmed in [BB]. If confirmed by engineering, update status to Production. |
| **Guardrails — Custom policy enforcement** | Aspirational (pending confirmation) | No until confirmed | No until confirmed | Policy & Control Design service for manual guardrail rule configuration | [PB] lists "custom policy enforcement" as a Guardrails feature. The six native scanners are Production; custom policy rules are managed via the (In Build) Governance Policy Engine. Until the OPA/Rego engine ships, custom enforcement is advisory. |
| **MCP — Composable MCP creation** | Aspirational (pending confirmation) | No until confirmed | No until confirmed | Advisory on MCP server design and registry integration | [PB] lists this in the MCP lifecycle section. [BB] covers the MCP Broker (registry, runtime, tracing) as Production. Composable creation as a distinct capability is not confirmed. |

---

## Section 2: Ethana Edge

The commercial "Edge" product ([PB]) is a consolidation of two board briefing engineering workstreams: Sentry (network/SaaS layer) and Edge (endpoint/device layer). Both are In Build per [BB] page 11. Neither component is in production.

**Sales guidance:** Do not lead with Edge in regulated accounts (BFSI, insurance, healthcare, government). The correct entry product for regulated accounts is Ethana Build (Gateway + Immutable Audit Log). Edge may be positioned as the in-development employee AI governance layer for non-regulated accounts where a Beta engagement is acceptable.

**Mandatory pre-deployment disclosure for any Edge conversation:** Endpoint and browser monitoring requires HR and employment-law sign-off before deployment.

### 2.1 Endpoint / Device Layer (board briefing: Ethana Edge)

| Capability | Status | Customer Claim Allowed? | Proposal Safe? | Alternative Cursory Service | Notes |
|---|---|---|---|---|---|
| **Endpoint Agent** — Mac, Linux, Windows; MDM-deployable via Jamf / Intune | In Build | Mention as in-development only | No | N/A — no human equivalent for endpoint monitoring | [BB] page 11 "What We're Building": "endpoint agent (Mac, Linux, Windows)." [SE]: "Not in production." [BB] page 10 describes the architecture but no production status line appears on the slide. Enforces locally, works offline. |
| **Browser Extension** — Chrome, Edge (browser), agentic browsers (Dia, Comet) | In Build | Mention as in-development only | No | N/A — no human equivalent | [BB] page 11 "What We're Building": "browser extension." [SE]: "Not in production." Browser store approval timeline is an open question [SE]. |
| **Dev-tool Config push** — Cursor, Copilot, Claude Code | In Build | Mention as in-development only | No | Advisory on developer AI tool policy design | [BB] page 11 "What We're Building": "dev-tool config push for Cursor, Copilot, Claude Code." [SE]: "Not in production." |
| **Local MCP Discovery** — identifies MCP servers running on the endpoint | In Build | Mention as in-development only | No | AI Inventory & Classification service (manual MCP inventory) | [BB] page 10 lists "Local MCP Discovery" as an Edge Agent component. Status follows the endpoint agent (In Build). |
| **Browser prompt and response monitoring** — ChatGPT, Claude, Gemini, consumer AI surfaces | In Build | Mention as in-development only | No | N/A — no human equivalent | Part of [BB] Edge (browser extension). [SE]: "Not in production." Observability only when shipped — not real-time blocking. |
| **Developer AI tool monitoring** — IDE assistants (Cursor, Copilot, Claude Code, Windsurf, Cline, Aider) | In Build | Mention as in-development only | No | AI Inventory & Classification service for manual developer tool audit | Part of [BB] Edge (dev-tool config push). [SE]: "Not in production." |
| **Device-level AI asset inventory** — installed AI tools, browser extensions, local models, MCP servers | In Build | Mention as in-development only | No | AI Inventory & Classification service | Edge "sends back: Installed tools (→ Discovery)" per [BB] page 10. This data feeds Sentry's Discovery system — both components are In Build. |
| **Policy verdicts and local enforcement** — block / coach the user at source, works offline | In Build | Mention as in-development only | No | Governance Programs service (manual policy design) | [BB] page 10: Edge "block / coach the user at the source." Enforcement capability; in build. |
| **Per-user attribution** (endpoint layer) | In Build | No | No | AI Inventory & Classification service (manual HR-crosswalk attribution) | [PB] lists this as a current Edge GA capability. [BB] page 11: Sentry provides "per-user attribution" via Discovery connectors — also In Build. Neither the endpoint nor the network layer has shipped per-user attribution in production. |

---

### 2.2 Network / SaaS Layer (board briefing: Ethana Sentry)

| Capability | Status | Customer Claim Allowed? | Proposal Safe? | Alternative Cursory Service | Notes |
|---|---|---|---|---|---|
| **Discovery — Identity Provider connector** (Okta, Entra, Workspace) | In Build — **first connector, highest priority** | Mention as in-development; IdP first | No | AI Inventory & Classification service (manual IdP-crosswalk inventory) | [BB] page 9 STATUS: "Connector layer in build. Identity Provider connector first." This is the first connector to ship. Do not imply all connectors are equally near. |
| **Discovery — SaaS vendor API connectors** (ChatGPT Enterprise, Copilot, Claude) | In Build | Mention as roadmap; later than IdP | No | AI Inventory & Classification service | [BB] page 9 lists as connected source. [BB] page 11 "What We're Building": "SaaS APIs" connector family. Timeline: after IdP connector. |
| **Discovery — Code repository connectors** (GitHub, GitLab) | In Build | Mention as roadmap | No | AI Inventory & Classification service | [BB] page 9, page 11. |
| **Discovery — Cloud agent connectors** (Bedrock, Vertex, Agentforce) | In Build | Mention as roadmap | No | AI Inventory & Classification service | [BB] page 9, page 11. |
| **Discovery — SWG / Firewall log connectors** | In Build | Mention as roadmap | No | Advisory on log extraction from existing SWG (Zscaler, Netskope) | [BB] page 9, page 11. |
| **Discovery — AI Inventory output** ("Shadow AI 48h report", risk register entries, CISO single screen) | In Build (output of Discovery connectors) | No until connectors ship | No | AI Inventory & Classification service delivers the human-produced equivalent today | [BB] page 9. The output is well-defined; the connectors that produce it are In Build. Human Cursory service bridges until platform ships. |
| **AI Firewall — URL categorization and allow/block/coach** | In Build | Mention as roadmap | No | Advisory on DLP policy using existing enterprise SWG (Zscaler, Netskope, Palo Alto) | [BB] page 8, page 11 "What We're Building." [SE]: "Not in production today." Integrates with Zscaler, Netskope, Palo Alto — or runs standalone via Edge. |
| **AI Firewall — Egress DLP on flagged content** | In Build | Mention as roadmap | No | Advisory on DLP policy design for AI traffic | [BB] page 8, page 11. |
| **AI Firewall — Per-user quota enforcement** | In Build | Mention as roadmap | No | Advisory on quota policy design | [BB] page 8. |

---

### 2.3 Roadmap — Ethana Edge

Capabilities explicitly labeled roadmap in [PB] Section 4.1. Consistent with In Build or later per [BB]. Do not position as current.

| Capability | Status | Customer Claim Allowed? | Proposal Safe? | Alternative Cursory Service | Notes |
|---|---|---|---|---|---|
| **PII masking and sensitive data redaction before browser egress** | Roadmap | No | No | Advisory on PII handling policies; Build Gateway PII masking (Production) covers API-layer traffic only | [PB] explicitly labels this roadmap. [BB] AI Firewall covers network-layer DLP (In Build). Until both ship, PII redaction before prompts leave the browser is unavailable. |
| **Source code masking for developer AI tools** | Roadmap | No | No | Advisory on developer AI acceptable use policy | [PB] explicitly labels this roadmap. Build Gateway (Production) prevents secrets in server-side API calls; browser/IDE-layer source code masking is roadmap. |
| **AI website allowlists and blocklists; browser-level policy enforcement** | Roadmap | No | No | Advisory on SWG integration for AI URL categorization | [PB] explicitly labels this roadmap. Covered by AI Firewall (In Build). |
| **Secret detection and masking at the browser** | Roadmap | No | No | Advisory on secrets hygiene policy for developer environments | [PB] explicitly labels this roadmap. Build Gateway secret scanner (Production) covers API calls only. |

---

## Section 3: Ethana Workspace

**Workspace is aspirational. It has no engineering equivalent in the board briefing at any status level.**

The board briefing (May 2026) contains no Workspace product, no Workspace pricing, no Workspace features, and no Workspace roadmap item across 15 pages. The board briefing's packaging slide shows the commercial suite as "Sentry + Build" — Workspace is not a packaging option. Workspace does not appear in the board briefing's "Surfaces & Horizons" slide in any column (Today, Expanding Into, or Emerging).

Do not include Workspace capabilities in any proposal, RFP response, or customer-facing claim until an updated primary engineering source confirms the codebase.

The alternative for every Workspace use case is one of: (a) Ethana Build Gateway with customer-built application layer, or (b) Cursory advisory services.

| Capability | Status | Customer Claim Allowed? | Proposal Safe? | Alternative | Notes |
|---|---|---|---|---|---|
| **Governed enterprise chat** — multi-user, shared workspaces, department-level assistants | Aspirational | No | No | Build Gateway + customer-built chat application | [BB]: absent entirely. Customer deploys their own chat UI; all AI calls routed through Build Gateway for governance, guardrails, and audit. |
| **RAG on internal documents** — SharePoint, Confluence, Notion, Google Drive, databases | Aspirational | No | No | Build Gateway governs RAG API calls; customer builds RAG pipeline | [BB]: absent entirely. The RAG content governance problem (stale documents, draft vs. approved) also cannot be solved by Workspace even when the product ships — [SE]: "Ethana has no visibility into what documents are in the vector database." |
| **Document drafting, summarisation, and review workflows** | Aspirational | No | No | Advisory on AI workflow design; customer builds on top of Build Gateway | [BB]: absent entirely. |
| **Role-based access control on knowledge sources** | Aspirational (as Workspace-specific capability) | No for Workspace; Yes for platform RBAC in Build | No (as Workspace feature) | Build Account Management RBAC (Production) applies to API-layer access control | Platform-level RBAC is Production. Workspace-specific document-level RBAC is aspirational. |
| **PII auto-masking in vector storage** | Aspirational | No | No | Build Gateway PII masking (Production) at API call layer | Build Gateway masks PII in transit. Masking inside a vector database requires Workspace (aspirational) or a separate data engineering solution. |
| **Immutable prompt/response/export audit log** (Workspace-specific) | Aspirational | No for Workspace | Yes via Build Audit Log | Build Immutable Audit Log (Production) covers all gateway-routed calls | Build's Immutable Audit Log is Production and covers all API calls — including those from a customer-built chat or RAG application. Workspace-specific logging is aspirational; Build logging is not. |
| **Custom chat widgets / department copilots** | Aspirational | No | No | Advisory on custom copilot architecture; customer builds on Build Gateway | [BB]: absent entirely. |

---

## Section 4: Shared Platform Services

Platform services are shared across all three commercial product lines and are confirmed in production.

| Service | Status | Customer Claim Allowed? | Proposal Safe? | Notes |
|---|---|---|---|---|
| **Guardrails engine** (all six production scanners) | Production | Yes | Yes | Bidirectional. Sub-200ms p95. Called by Gateway, MCP Broker, Edge (when shipped), and AI Firewall (when shipped). [BB] page 5: "All six scanners in production." |
| **Red Teaming** (orchestrator + 21 OWASP probes) | Production | Yes | Yes | [BB] page 6. CI/CD gate is In Build. Targeting: models, LLM apps, agents. |
| **Audit & Compliance** — Immutable Audit Log | Production | Yes — lead claim | Yes | [BB] page 11 "What We Have." Insert-only event store, multi-tenant. SIEM export. |
| **Governance Policy Engine** (OPA / Rego) | In Build | No | No | [BB] page 11 "What We're Building." Signed policy bundles pushed to every surface — when shipped, this is the mechanism by which guardrail policies are governed centrally. |
| **FinOps** — cost and budget tracking (project level) | Production | Yes — project level | Yes | [BB] page 11 "What We Have." Per-user / GPU / dormant-licence FinOps is In Build. |
| **Account Management** — tenants, projects, RBAC, SSO/OIDC | Production | Yes | Yes | [BB] page 11 "What We Have." SCIM provisioning In Build. |

---

## Section 5: Compliance Certifications

All three certifications are explicitly In Build per [BB] page 11 ("What We're Building: Compliance certifications: SOC 2 Type II, ISO 27001, HIPAA-ready · in progress").

The marketing playbook footer states "ISO 27001 Certified." This claim is not supported by the board briefing (one month prior), Study ethana, or any primary engineering source. Do not use this claim until a certificate number, certifying body, and audit scope can be cited.

| Certification | Status | Customer Claim Allowed? | Proposal Safe? | Cursory Bridge | Notes |
|---|---|---|---|---|---|
| **SOC 2 Type II** | In Progress | No | No — hard gate for financial services vendor onboarding | Structure opportunity to close post-certification; scope interim advisory or non-production pilot | [BB] page 11, [SE]: "Hard procurement blocker for financial services. Plan for 6–12 week TPRM assessment." G-SIB banks require this before any data routes through the platform. |
| **ISO 27001** | In Progress | No | No | Same bridge as SOC 2 | [BB] page 11 explicitly in "What We're Building." [SE]: "❌ Not certified." Playbook footer claim ("ISO 27001 Certified") is not supported by any primary engineering source and must not be used until a certificate is obtained and documented. |
| **HIPAA-ready** | In Progress | No | No | Advisory on HIPAA architecture using Build Gateway in VPC | [BB] page 11. Relevant for healthcare / life-sciences. Build Gateway PII masking in a customer VPC provides the data residency foundation; formal HIPAA certification not yet obtained. |

---

## Section 6: Deployment Models

| Model | Status | Customer Claim Allowed? | Proposal Safe? | Notes |
|---|---|---|---|---|
| **Ethana Cloud (SaaS / hosted)** | Production | Yes | Yes | Self-serve onboarding. Best for pilots and SMB. [BB] page 13. |
| **Customer VPC** (AWS, Azure, GCP) | Production | Yes | Yes | Customer's own database, identity provider, model keys. Data never leaves their account. Best for regulated mid-market. [BB] page 13. |
| **On-premises** (customer data center) | Production (model supported) | Yes — with mandatory caveat | Yes — with caveat | Mandatory caveat: "On-prem at Tier 1 bank scale is unproven. TPRM and deployment engineering engagement required." [SE] explicitly states this. Best for BFSI and public sector. |
| **Air-gapped environments** | Production (model supported) | Yes | Yes | Same caveat as on-premises. No customer data, prompts, or telemetry leaves the controlled environment. |
| **Pricing parity** (SaaS = VPC = on-prem pricing) | Confirmed | Yes | Yes | No premium for the deployment model regulated buyers are required to use. Strong commercial differentiator vs. SaaS-only vendors. |

---

## Section 7: Pricing Reference

Confirmed in both [PB] and consistent with [BB] packaging structure.

| Product / Bundle | Annual License | Included Nodes | Extra Node/year |
|---|---|---|---|
| Ethana Edge | $10,000 | 1 | $2,000 |
| Ethana Workspace | $10,000 | 1 | $2,000 |
| Ethana Build | $30,000 | 1 | $5,000 |
| Enterprise AI Control Plane Bundle | $45,000 | 1 of each | As above |

**Note on Workspace pricing:** Workspace pricing is confirmed in [PB]. However, Workspace is Aspirational — the pricing reflects commercial intent, not product availability. Do not quote Workspace pricing in proposals until the product is engineering-validated.

**Licensing model:** Per platform node per year. No per-seat, per-user, or per-token fees. A node is an independently deployed, managed, or governed instance (e.g., additional region, business unit, subsidiary, or air-gapped environment). Pricing is consistent across all deployment models.

---

## Section 8: Cursory Services Reference

Cursory Services are human-delivered and available today. They bridge platform gaps and are independently deliverable without any Ethana platform purchase.

| Service | What it delivers | Primary use case | Bridges which platform gap |
|---|---|---|---|
| **AI Readiness Assessment** | Current AI estate audit, gap analysis against frameworks, risk register, prioritisation | Entry engagement for regulated accounts | Governance Policy Engine (In Build); Compliance Pack (In Build) |
| **AI Inventory & Classification** | Asset register mapping regulatory exposure, sanctioned vs. shadow tools, risk scoring | Shadow AI inventory before Discovery ships | Discovery (all connectors In Build); per-user attribution (In Build) |
| **Regulatory Gap Analysis** | Control mapping and gap identification for RBI, EU AI Act, ISO 42001, NIST AI RMF, or DPDP | Framework alignment without automation | Compliance Pack (In Build); Compliance Evidence Export (In Build) |
| **Policy & Control Design** | Acceptable use policy, risk appetite statements, guardrail rule configuration, control libraries | Governance architecture for guardrail configuration | Governance Policy Engine (In Build); custom policy enforcement (Aspirational) |
| **Ethana Implementation** | Gateway setup, guardrail tuning, audit schema mapping, SIEM integration, on-prem deployment | Technical delivery for Build customers | All Build Production capabilities; on-prem scale (unproven) |
| **Horizon Monitoring** | Monthly board-ready brief on RBI, SEBI, IRDAI, EU AI Act, DPDP developments | Ongoing regulatory intelligence for compliance teams | Compliance Pack (In Build) |
| **Managed Gov Retainer** | Ongoing guardrail updates, quarterly risk reviews, committee support | Long-term governance programme delivery | Governance Policy Engine (In Build) |
| **Managed Ethana Ops** | Running the platform, alert triage, model cost optimisation, CISO reporting | Operational support for teams without internal AI ops | All Build Production capabilities |
| **Red Teaming as a Service** | Quarterly adversarial exercises on production AI, custom probe development, remediation advisory | Model validation and robustness testing | CI/CD Red-Teaming Gate (In Build); custom YAML probes (configuration engagement) |
| **Bias Audit Referral** | Specialist firm referral for EU AI Act Art.10, NYC LL144 requirements | High-risk AI system bias auditing | Bias scanner is a runtime text filter only — cannot satisfy formal bias audit requirements |

---

## Section 9: Capability Claims Firewall

Before making any capability claim in a customer conversation, proposal, or RFP response, apply the following test:

```
STEP 1 — Is the capability listed in [BB] page 11 "What We Have"?
  YES → Production. Claim allowed. State any caveats listed in Section 1.1 of this document.
  NO  → Continue to Step 2.

STEP 2 — Is the capability listed in [BB] page 11 "What We're Building"?
  YES → In Build. Mention as roadmap only. Do not commit in proposals. Offer Cursory bridge service.
  NO  → Continue to Step 3.

STEP 3 — Does the capability appear in [PB] but not in [BB] at any level?
  YES → Aspirational. Do not claim. Do not mention as roadmap. Do not include in proposals.
        Offer alternative: (a) adjacent Production capability, or (b) Cursory advisory service.
  NO  → Capability does not exist in any source. Do not claim.
```

**Default answer when uncertain:** Treat as Aspirational until a primary engineering source confirms otherwise. The cost of under-claiming is a lost upsell. The cost of over-claiming in a regulated account is a destroyed relationship and potential regulatory exposure for the customer.

---

## Section 10: Historical File Reference

The following files are retained as historical artifacts. They contain useful narrative context and earlier analytical work but should not be used as primary status references.

| File | Historical value | Why superseded |
|---|---|---|
| `capability-status.md` | Engineering-era status matrix. First systematic attempt to catalogue platform capabilities with status. | Assigns "Beta" to Edge/Discovery — a status tier not supported by primary sources ([BB] and [SE] both say "In Build, not in production"). Does not reflect the Sentry/Workspace product architecture divergence. |
| `source-of-truth.md` | Cross-source synthesis. Good narrative context for the three-product architecture and regulatory alignment. | References "Study ethana.txt" as an engineering source throughout, but the interpretations were made before the board briefing PDF was read directly. Workspace is marked "Unverified" (correct direction) but without the architectural explanation that it has no engineering equivalent whatsoever. |
| `ethana-status-reconciliation.md` | Documents the specific capability elevations that were made based on "direct user observation" and playbook evidence. Useful for understanding the origin of elevated claims. | Elevated Edge, Workspace, Discovery, and Visual Agent Builder to Production (GA) using the marketing playbook as corroboration. All four elevations are directly contradicted by primary sources. The reconciliation file's status conclusions for these capabilities are not operationally usable. |
| `ethana-status-harmonization.md` | Conflict resolution layer. Correctly identifies the hierarchy of evidence and explicitly rejects the reconciliation file's elevations. | Directionally correct but based on inferences from derived files rather than direct primary source reading. This canonical model supersedes the harmonization decisions with primary-source-grounded findings. |
| `evidence-based-status-review.md` | Neutral adjudication of five contested capabilities. Correctly identified the direction of status for all five. | Confidence scores were inflated by "Beta" characterisations sourced from claims-matrix.md (a derived file). Revised scores appear in `primary-source-validation.md`. |
| `primary-source-validation.md` | Line-by-line verification of evidence-based-status-review.md against primary sources only. Identifies every inferred claim. | Validation report, not an operational reference. |
| `product-architecture-investigation.md` | Full investigation of the Sentry / Edge / Workspace / Build naming and architecture discrepancy. Findings are incorporated into this document. | Investigation document. This canonical model is the operational output. |

---

## Section 11: When This Document Should Be Updated

This document must be updated when any of the following occur. Updates require direct primary source evidence — do not update based on verbal confirmation or marketing materials alone.

| Trigger | Section to update | Evidence required |
|---|---|---|
| Edge endpoint agent shipped to production | Section 2.1 → Production | Updated board briefing, engineering release note, or equivalent primary source |
| Identity Provider Discovery connector shipped | Section 2.2 → first connector Production | Same as above |
| NHI for agents shipped | Section 1.2 → Production | Same as above |
| ISO 27001 certification obtained | Section 5 → Production | Certificate number, certifying body (e.g., BSI, TÜV), audit scope, expiry date |
| SOC 2 Type II certification obtained | Section 5 → Production | Same — Type II report reference, auditor, period |
| Workspace receives engineering validation | Section 3 → update to In Build or Production | Codebase confirmation, engineering sign-off, or updated board briefing |
| Visual Agent Builder receives engineering validation | Section 1.3 → update to In Build | Same as Workspace |
| Pricing changes | Section 7 | Updated playbook or commercial document |
| New capability shipped | Add to appropriate section | Board briefing update, engineering release note |
