# Ethana Product Architecture Investigation

**Date:** 2026-06-17
**Question:** Are the Sentry / Edge / Workspace / Build differences between the board briefing and the marketing playbook a rename, a repackaging, a product generation change, or something else?
**Sources used exclusively:**
- `[PB]` Ethana Marketing Playbook, Version 1.0, June 2026
- `[SE]` Study ethana (grounded in Board Briefing May 2026 + Barclays Governance Mapping May 2026)
- `[BB]` Ethana Board Briefing, May 2026, 15 pages (confidential)

---

## 1. What Each Source Says the Architecture Is

### 1.1 Board Briefing (May 2026) — the engineering architecture

Page 3 of [BB] is titled "Three product lines. Shared platform underneath." The three product lines are:

**Ethana Sentry** — "secure how employees use AI"
- Discovery: Shadow AI scanning
- AI Firewall: network egress · DLP
- Provides: visibility · access control · per-user attribution

**Ethana Edge** — "secure AI on the user's device"
- Endpoint Agent: Mac · Linux · Windows
- Browser Extension: Chrome · Edge · agentic browsers
- Dev-tool Config: Cursor · Copilot · Claude Code
- Pulls signed policy bundle
- Enforces locally · works offline
- Sends back: Installed tools (→ Discovery), Policy verdicts (→ Audit Log), Block / coach the user

**Ethana Build** — "secure the AI apps your company builds"
- Gateway: single LLM front door
- MCP Broker: hosts & brokers tools
- + Runtime Threat Detection: novel jailbreaks · agent misuse · abuse spikes on production traffic

**Platform services (shared by all three):**
Guardrails · Red Teaming · Governance · Audit & Compliance · FinOps · Account Management

**Packaging (page 13):**
- Suite: Sentry + Build + all platform services
- Sentry only: customer just has the Shadow AI / employee problem
- Build only: customer just builds AI apps and wants Gateway + Guardrails + MCP Broker

**Status (page 11 — "What we have. What we're building."):**

| Item | Column |
|---|---|
| Gateway | WHAT WE HAVE |
| MCP Broker | WHAT WE HAVE |
| Red Teaming (orchestrator + 21 OWASP probes) | WHAT WE HAVE |
| Guardrails (six scanners) | WHAT WE HAVE |
| Immutable Audit Log | WHAT WE HAVE |
| Account Management (tenants, projects, RBAC, SSO/OIDC) | WHAT WE HAVE |
| Cost & Budget tracking (per-tenant, per-project, with alert hooks) | WHAT WE HAVE |
| **Discovery** (seven connector families) | **WHAT WE'RE BUILDING** |
| **Edge** (endpoint agent, browser extension, dev-tool config) | **WHAT WE'RE BUILDING** |
| AI Firewall | **WHAT WE'RE BUILDING** |
| Governance (Policy Engine / OPA / Rego) | **WHAT WE'RE BUILDING** |
| Compliance Pack | **WHAT WE'RE BUILDING** |
| FinOps (per-user / per-team / GPU cost) | **WHAT WE'RE BUILDING** |
| Enterprise features (SSO, SCIM, RBAC, on-prem, audit retention) | **WHAT WE'RE BUILDING** |
| NHI for agents | **WHAT WE'RE BUILDING** |
| Compliance certifications (SOC 2, ISO 27001, HIPAA-ready) | **WHAT WE'RE BUILDING** |
| CI/CD Red-Teaming Gate | **WHAT WE'RE BUILDING** |

**Board briefing's surface horizon (page 12) — "Where AI lives today, and where it will live tomorrow":**

| Column | Examples |
|---|---|
| TODAY (surfaces covered now) | Server-side LLM apps (using Gateway), MCP tool servers, Self-hosted LLM stack, Internal agents, Audit & immutable event log, Policy & rate limiting, Red Teaming |
| EXPANDING INTO | Browsers, Endpoint devices, Developer tools, Code repositories, Cloud-hosted code, SaaS AI vendors, Cloud agents, Enterprise AI agent builders, Secure Web Gateways |
| EMERGING | Native AI hardware, OS-level AI, Computer-use agents, Agentic browsers, Voice & multimodal agents, etc. |

**Critical observation from the surfaces slide:** Browsers, Endpoint devices, and Developer tools — the capabilities that define Ethana Edge in the board briefing — are in the "EXPANDING INTO" column, not "TODAY." Enterprise chat / governed workspaces / RAG do not appear in any column on this slide.

---

### 1.2 Marketing Playbook (June 2026) — the commercial architecture

**Ethana Edge** — "Endpoint AI Monitoring"
- AI discovery & shadow AI
- Browser AI monitoring
- Developer tool monitoring
- Prompt & response visibility
- AI asset inventory
- Per-user attribution
- Compliance audit logs
- Security & blocking (roadmap)

**Ethana Workspace** — "Governed AI Workspaces"
- Enterprise chat & collaboration
- Knowledge-grounded assistants
- RAG on internal documents
- Department AI copilots
- Self-hosted / air-gapped
- Role-based access control
- Immutable prompt/response logs
- Document drafting & workflows

**Ethana Build** — "AI Infrastructure & Control"
- OpenAI-compatible LLM gateway
- Multi-model routing & fallback
- Guardrails & PII masking
- PromptOps & versioning
- Evaluation & hallucination testing
- MCP lifecycle management
- Agent orchestration & DAG builder ← **absent from board briefing**
- Observability & cost tracking

**Pricing:**
- Edge: $10,000/year
- Workspace: $10,000/year
- Build: $30,000/year
- Bundle: $45,000/year

---

### 1.3 Study Ethana (May 2026) — confirms board briefing architecture

[SE] explicitly states it is "grounded exclusively in the Board Briefing (May 2026) and Barclays Governance Mapping Document (May 2026)."

[SE] describes three products: Build, Sentry, and Edge — consistent with the board briefing. Relevant passages:

- **Build:** "Status: In production. Multi-tenant LLM gateway with routing, fallback, per-call cost tracking, and CallTrace shipped."
- **Sentry:** "Status: Discovery (the core of Sentry) is still in build. The connector layer is being built. Identity Provider connector is first. The AI Firewall (network egress control) is also in build. This is the most roadmap-heavy product line in the suite."
- **Edge:** "Status: In build. Endpoint agent (Mac, Linux, Windows), browser extension, and dev-tool config push are all in the build column. Not in production."

[SE] makes no mention of "Ethana Workspace," governed enterprise chat, or RAG workspaces. [SE] makes no mention of a visual agent builder or DAG workflow tool.

---

## 2. Feature-by-Feature Mapping Across All Three Sources

### 2.1 Mapping playbook's "Edge" back to board briefing products

| Playbook Edge feature | Board Briefing equivalent | BB Product | BB Status |
|---|---|---|---|
| AI discovery & shadow AI | Discovery: "Show me every AI tool in my org" | **Sentry** | In Build |
| Browser AI monitoring | Browser Extension: Chrome · Edge · agentic browsers | **Edge** | In Build |
| Developer tool monitoring | Dev-tool Config: Cursor · Copilot · Claude Code | **Edge** | In Build |
| Prompt & response visibility | Edge → Guardrails "on local prompt capture" (page 5) | **Edge** (via platform) | Edge In Build |
| AI asset inventory | Edge → "Sends back: Installed tools (→ Discovery)" | **Edge + Sentry** | Both In Build |
| Per-user attribution | Sentry provides "per-user attribution" (page 3) | **Sentry** | In Build (via Discovery connectors) |
| Compliance audit logs | Immutable Audit Log | **Platform service** | In Production |
| Security & blocking (roadmap) | AI Firewall: "network egress · DLP" | **Sentry** | In Build |

**Conclusion:** The playbook's commercial "Edge" product is a brand consolidation of the board briefing's **two separate products** — Sentry (network/SaaS layer) and Edge (device layer). Every capability in the playbook's Edge maps either to Sentry (In Build) or to Edge (In Build). No playbook Edge capability maps to a board briefing Production item except Immutable Audit Log, which is a shared platform service available to all products.

### 2.2 Mapping playbook's "Workspace" back to board briefing products

| Playbook Workspace feature | Board Briefing equivalent | BB Product | BB Status |
|---|---|---|---|
| Enterprise chat & collaboration | No equivalent | — | **ABSENT** |
| Knowledge-grounded assistants (RAG) | No equivalent | — | **ABSENT** |
| RAG on internal documents | No equivalent | — | **ABSENT** |
| Department AI copilots | No equivalent | — | **ABSENT** |
| Self-hosted / air-gapped deployment | Deployment model (confirmed) | Platform | In Production |
| Role-based access control | Account Management: RBAC | Platform | In Production |
| Immutable prompt/response logs | Immutable Audit Log | Platform | In Production |
| Document drafting & workflows | No equivalent | — | **ABSENT** |

**Conclusion:** Of eight Workspace proof points, five have no board briefing equivalent. The three that do (self-hosted, RBAC, Immutable Audit Log) are shared platform capabilities that apply to ALL products — they are not specific to a "Workspace" product. The enterprise chat, RAG, document workflows, and copilot features have no board briefing equivalent at any status level — not in production, not in build, not in roadmap.

Workspace also does not appear in the board briefing's "Surfaces & Horizons" slide in any column — not TODAY, not EXPANDING INTO, not EMERGING. This means as of May 2026, governed enterprise chat / RAG was not a committed direction in the engineering surface roadmap.

### 2.3 Mapping playbook's "Build" back to board briefing products

| Playbook Build feature | Board Briefing equivalent | BB Product | BB Status |
|---|---|---|---|
| OpenAI-compatible LLM gateway | Gateway: "single LLM front door" | Build | In Production |
| Multi-model routing & fallback | Gateway: "Multi-LLM Routing, Fallback & Retry" | Build | In Production |
| Guardrails & PII masking | Guardrails (six scanners, bidirectional) | Platform service | In Production |
| PromptOps & versioning | Referenced in [SE] as "MODERATE. Present in the platform." | Build (implied) | Moderate / present |
| Evaluation & hallucination testing | Red Teaming / Guardrails (hallucination grounding) | Platform service | Partially in production |
| MCP lifecycle management | MCP Broker (~8,000 lines in production) | Build | In Production (core) |
| Agent orchestration & DAG builder | No equivalent | — | **ABSENT from BB** |
| Observability & cost tracking | Cost & Budget tracking (per-tenant, per-project) | Platform service | In Production |

**Conclusion:** The playbook's Build section is largely accurate for core capabilities — with one significant exception. The "Agent orchestration & DAG builder" (which [PB] Section 4.3 describes as "Visual agent builder: drag-and-drop DAG workflow design") has no equivalent in the board briefing. It appears in neither "What We Have" nor "What We're Building." The board briefing's Build section (page 3) shows Gateway and MCP Broker as the two named Build components, plus "+ Runtime Threat Detection." No visual workflow tool appears.

---

## 3. The Three Hypotheses Evaluated

### Hypothesis A: Renaming — Sentry became Edge, Edge was absorbed

**The argument:** Between May and June 2026, the product team renamed Sentry → Edge and merged the old endpoint-level Edge into the new commercial Edge. A separate "Workspace" product was created as a new commercial addition.

**Evidence for:**
- "Sentry" disappears entirely from the playbook and no explicit transition note exists
- The playbook's "Edge" provides Discovery and AI Firewall capabilities (which were Sentry) alongside endpoint agent capabilities (which were Edge)
- One-month interval between documents is consistent with a brand decision, not an engineering rebuild

**Evidence against:**
- Renaming does not explain the addition of Workspace, which has no Sentry equivalent
- Renaming does not explain why the Visual Agent Builder appeared in Build with no board briefing basis
- A pure rename would preserve the two-product structure (Sentry + Edge). The playbook collapses two products into one "Edge" — which is a packaging change, not just a name change

**Verdict on Hypothesis A:** Partially correct for Sentry/Edge. Does not explain Workspace or Visual Agent Builder.

---

### Hypothesis B: Repackaging — Technical architecture vs. commercial architecture

**The argument:** The board briefing reflects the engineering/technical product taxonomy (three separate engineering projects: Sentry, Edge, Build). The playbook reflects the commercial packaging (how these are sold to customers). Between May and June 2026, the commercial packaging was reorganized:
- Sentry + Edge → consolidated under one commercial SKU called "Edge"
- A new commercial SKU "Workspace" was introduced for an aspirational enterprise chat/RAG direction
- Build remained, with the Visual Agent Builder added to the product vision

**Evidence for:**
- The board briefing's packaging slide (page 13) already shows a different packaging from the technical architecture: "Suite = Sentry + Build + all platform services" — Edge is missing from the commercial suite despite being a named product line. This suggests the board briefing itself was already treating Edge (the endpoint product) as an add-on or extension, not a primary commercial motion.
- The board briefing shows Edge feeding telemetry into Sentry's Discovery product — architecturally, Edge is a data collection mechanism FOR Sentry. Commercially packaging them together makes sense.
- [SE] describes the commercial story as centered on Build (for production deployments) and Sentry (for employee governance), with Edge as the endpoint extension of Sentry.
- The playbook prices are consistent with a repackaging: if Sentry ($X) + Edge ($X) → combined "Edge" ($10,000), that's a single commercial SKU for both previously separate products.

**Evidence against:**
- The board briefing's "WHAT WE'RE BUILDING" lists both Discovery (core of Sentry) and Edge as separate engineering workstreams. Commercially combining two separate In Build engineering projects into one commercial SKU and calling it "available" overstates the status of both.
- Workspace cannot be explained by repackaging existing products. There is no existing product to repackage into an enterprise chat/RAG offering.

**Verdict on Hypothesis B:** This is the most accurate explanation for the Sentry/Edge consolidation. The commercial "Edge" SKU packages what the board briefing treats as two engineering workstreams (Sentry network layer + Edge endpoint layer). However, Workspace remains unexplained by repackaging alone.

---

### Hypothesis C: Different product generations — Playbook represents v2

**The argument:** The board briefing (May 2026) represents the v1 product architecture that the engineering team has built or is building. The playbook (June 2026) represents a v2 commercial vision that the product team drafted for fundraising, sales, or board-level positioning — incorporating aspirational product directions (Workspace, Visual Agent Builder) alongside the confirmed engineering roadmap.

**Evidence for:**
- The board briefing's final slide (page 14) says: "Greenlight the suite. Line up design partners. Move." This is a pitch for investment approval to build the full suite — not an announcement of a completed suite. The board briefing is asking for permission to build.
- The playbook was published one month after the board briefing. A full product suite (including Workspace with enterprise chat, RAG, and department copilots) cannot be designed, built, and validated in one month following a board-level investment request.
- The board briefing's "EXPANDING INTO" column includes Browsers, Endpoint devices, and Developer tools — surfaces the playbook's Edge claims as current. These are aspirational in the board briefing but presented as current in the playbook.
- [SE] notes about enterprise reality: "The honest answer on Ethana's current stage should be framed as: early-stage, founder access, customisation opportunity, not an established enterprise reference list." This characterization is inconsistent with a mature three-product platform including Workspace.
- The board briefing ends: "A meaningful portion of what we're building is extending live production code · not greenfield invention." The core Build capabilities are being extended, not rebuilt. But Edge (all of it) and Sentry (all of it) are new product builds.

**Evidence against:**
- The playbook was written to be used in sales conversations, not as a speculative vision document. Playbook language is direct and explicit: "Current capability (GA): Observability."
- The playbook explicitly labels blocking, PII redaction, and egress control as "roadmap" — demonstrating that the authors do distinguish current from future for at least some capabilities.

**Verdict on Hypothesis C:** This is the most accurate explanation for Workspace and the Visual Agent Builder. The playbook represents a commercial architecture that includes both the confirmed engineering roadmap (Build = Production) and aspirational new products (Workspace, Visual Agent Builder) that are not in the engineering roadmap at all.

---

## 4. Synthesis: What Actually Changed Between May and June 2026

Based on all three primary sources, the most complete picture is:

### 4.1 The Build line is consistent and production-anchored

Both documents agree on Build's core capabilities: Gateway, MCP Broker, Guardrails, Immutable Audit Log, Red Teaming. These are Production per both sources. The playbook adds "Agent orchestration & DAG builder" which has no board briefing equivalent — this appears to be an aspirational addition to the Build product description.

### 4.2 Sentry + Edge → "Edge" is a commercial consolidation, not a technical rename

The board briefing treated Sentry (network/SaaS layer) and Edge (endpoint/device layer) as two separate engineering workstreams. Both are In Build. The playbook combined them into one commercial SKU called "Edge" — a packaging decision that makes commercial sense (one SKU for "govern how employees use AI") but obscures the fact that neither component is in production.

The board briefing's own architecture already anticipated this consolidation: Edge (the endpoint product) "sends back" data to Sentry's Discovery system. Architecturally, Edge is a data collection instrument for Sentry. Packaging them as one commercial product reflects how they work together.

Critically: the commercial consolidation does not change the engineering status. The playbook's "Edge" = Sentry (In Build) + Edge (In Build) = **In Build overall, not GA**.

### 4.3 Workspace is entirely new and has no board briefing basis

Workspace cannot be explained by any renaming or repackaging of existing board briefing products. It is a new commercial concept — governed enterprise chat + RAG on internal documents — that:
- Does not appear in the board briefing's product architecture (pages 1–15)
- Does not appear in the board briefing's "WHAT WE'RE BUILDING" list
- Does not appear in the board briefing's "EXPANDING INTO" or any surface horizon column
- Is not described in Study ethana at any status level

The most likely explanation is that Workspace was added to the playbook as a commercial direction for the June 2026 product positioning, without corresponding engineering validation or a committed engineering roadmap. It represents the product team's intention for where the platform should go, not what engineering has built or committed to build.

### 4.4 Visual Agent Builder is similarly new and has no board briefing basis

Like Workspace, the Visual Agent Builder is absent from all 15 pages of the board briefing. It does not appear in the Build product description (page 3), in "What We Have" (page 11), or in "What We're Building" (page 11). The board briefing's Build section consists of: Gateway + MCP Broker + Runtime Threat Detection. No DAG workflow builder, no visual orchestration layer, no drag-and-drop interface.

### 4.5 What the timeline implies

The board briefing (May 2026) is a presentation asking the board to "Greenlight the suite. Line up design partners. Move." It is a pitch for investment approval. One month later, the marketing playbook (June 2026) describes the full suite as commercially available. This one-month gap is not consistent with the board having approved, designed, engineered, and deployed Workspace and the Visual Agent Builder. It is consistent with the commercial team having drafted a forward-looking playbook that reflects the intended product architecture rather than the current engineering reality.

---

## 5. Architectural Comparison Table

| Dimension | Board Briefing (May 2026) | Marketing Playbook (June 2026) |
|---|---|---|
| Product 1 | **Sentry** (Discovery + AI Firewall) | **Edge** (Discovery + browser + endpoint + developer tools) |
| Product 2 | **Edge** (Endpoint agent + browser extension + dev-tool config) | **Workspace** (Enterprise chat + RAG + document workflows) |
| Product 3 | **Build** (Gateway + MCP Broker + Runtime Threat Detection) | **Build** (Gateway + Guardrails + PromptOps + MCP + DAG builder + cost tracking) |
| Platform services | Guardrails · Red Teaming · Governance · Audit & Compliance · FinOps | Shared observability and compliance layer (implied) |
| Employee AI governance | Two products: Sentry (network) + Edge (endpoint) | One product: Edge (combined) |
| Governed enterprise chat/RAG | Not present in any form | Workspace (full product with pricing) |
| Visual Agent Builder | Not present in any form | Listed as Build proof point |
| Production items | Gateway · MCP Broker · Red Teaming · Guardrails · Audit Log · Account Mgmt · Cost tracking | Implied for all Build proof points; no status labels applied |
| In-Build items | Discovery · Edge · AI Firewall · NHI · Compliance Pack · Governance · FinOps · Certifications | Not labeled; roadmap items identified only for Edge blocking/PII redaction |
| Document purpose | Internal board governance presentation | External commercial sales playbook |
| Audience | Board of directors | Sales team, marketing, customer conversations |
| Posture | Honest about what exists vs. what's being built | GA presentation with selective roadmap labeling |

---

## 6. Final Recommendation: Canonical Ethana Architecture for Governance OS

### 6.1 The finding

Neither source alone provides the complete and accurate picture. The board briefing gives the engineering reality. The playbook gives the commercial naming. Governance OS requires both: the playbook's commercial vocabulary for customer conversations and the board briefing's status accuracy for claims governance.

### 6.2 Canonical architecture

**Use the playbook's commercial product names. Use the board briefing's engineering status.**

| Commercial name (Playbook) | Engineering equivalent (Board Briefing) | Canonical Status | Claim eligibility |
|---|---|---|---|
| **Ethana Edge** | Sentry (Discovery + AI Firewall) + Edge (Endpoint agent + browser + dev-tool) | **In Build — neither component is in production** | Do not claim as GA. Can be positioned as the in-development employee AI governance layer. |
| **Ethana Workspace** | No board briefing equivalent | **Unverified / Aspirational** | Do not claim. No engineering basis in any primary source. |
| **Ethana Build — core** | Gateway + MCP Broker + Red Teaming + Guardrails + Audit Log | **Production** | These capabilities may be claimed as Production. Each has a known production caveat (see below). |
| **Ethana Build — Visual Agent Builder** | No board briefing equivalent | **Aspirational** | Do not claim. Absent from board briefing in any column. |

### 6.3 What can be claimed — production items from primary sources

From the board briefing's "What We Have" (page 11):

| Capability | Production evidence | Known caveat |
|---|---|---|
| LLM Gateway (multi-tenant, routing, fallback, CallTrace, cost tracking) | [BB] page 4 + page 11 | Non-LLM REST API proxying unconfirmed; p95 latency under batch load needs test data |
| Guardrails (six scanners: Secrets, PII, Prompt Injection, Jailbreak, Toxicity, Bias) | [BB] page 5: "All six scanners in production. Sub-200ms p95" | False positive rate at volume unconfirmed; bias scanner is a runtime text filter, not a model audit |
| Immutable Audit Log (insert-only, multi-tenant) | [BB] page 11 | Schema customisation for specific regulators is a configuration engagement |
| MCP Broker (registry, hosted runtime, per-tool-call tracing, admin UI) | [BB] page 7: "~8,000 lines in production. Per-call tracing shipped." | NHI and ephemeral tokens In Build — until shipped, agents reuse human credentials |
| Red Teaming (orchestrator + 21 OWASP probes, multi-turn attacks) | [BB] page 6: "Orchestrator + 21 OWASP probes in production." | CI/CD gate In Build; RAG-specific probe coverage unconfirmed |
| Account Management (tenants, projects, RBAC, SSO via OIDC) | [BB] page 11 | SCIM provisioning In Build |
| Cost & Budget tracking (per-tenant, per-project, alert hooks) | [BB] page 11 | Per-user / per-team FinOps In Build |

### 6.4 What is In Build — with no production claim

From the board briefing's "What We're Building" (page 11):

- Discovery (all seven connector families, including the edge telemetry connector)
- Ethana Edge (endpoint agent, browser extension, dev-tool config push)
- AI Firewall (network-egress AI app control, DLP, per-user quota)
- Governance Policy Engine (OPA / Rego, signed policy bundles)
- Compliance Pack (evidence collectors, one-click export)
- FinOps (per-user / per-team spend, GPU cost, dormant-licence findings)
- Enterprise features (SSO, SCIM provisioning, on-prem deployment at scale, audit retention)
- Non-Human Identity (NHI) for agents
- Compliance certifications (SOC 2 Type II, ISO 27001, HIPAA-ready — all in progress)
- CI/CD Red-Teaming Gate

### 6.5 What is Aspirational — no primary source basis at any status

- Ethana Workspace (governed enterprise chat, RAG, document workflows, department copilots)
- Visual Agent Builder (drag-and-drop DAG workflow design)
- "Deployed with regulated customers today" (footer claim in [PB], directly contradicted by [SE]: "early-stage, founder access, customisation opportunity, not an established enterprise reference list")

### 6.6 How to handle Sentry in Governance OS documents

The name "Sentry" does not exist in the commercial playbook. However, the engineering architecture that Sentry represents (network-layer Discovery + AI Firewall) is real and In Build. In Governance OS documents:

- Use **"Ethana Edge"** as the commercial product name for customer-facing contexts
- Distinguish internally between the **endpoint layer** (device agent, browser extension, dev-tool config) and the **network/SaaS layer** (Discovery connectors, AI Firewall) — both In Build, but different delivery timelines (Identity Provider connector first per [BB] page 9)
- Do not use the name "Sentry" in customer-facing materials — it is not in the playbook and would create confusion

### 6.7 Authoritative tiebreaker rule for Governance OS

When the playbook and the board briefing conflict on status, use the following rule:

> **The board briefing's status column (page 11) is the canonical status source. The playbook's product names and pricing are the canonical commercial vocabulary. Where the playbook presents a capability the board briefing does not mention (Workspace, Visual Agent Builder), treat the capability as aspirational and do not include it in proposals until a primary engineering source validates it.**

This rule acknowledges:
- The playbook is more recent (June 2026) but serves a commercial audience
- The board briefing is from May 2026 but prepared for governance accountability
- In the absence of an updated engineering status document, the board briefing's explicit status table is the stronger evidence

---

## 7. Architectural Diagram for Governance OS

```
ETHANA — CANONICAL ARCHITECTURE (June 2026)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ETHANA EDGE [COMMERCIAL SKU — IN BUILD]
  ├── Endpoint Layer (board briefing: Ethana Edge)
  │     endpoint agent (Mac · Linux · Windows)
  │     browser extension (Chrome · Edge · agentic browsers)
  │     dev-tool config push (Cursor · Copilot · Claude Code)
  │     local MCP discovery
  │     Status: In Build. Not in production.
  │
  └── Network / SaaS Layer (board briefing: Ethana Sentry)
        Discovery connectors (Identity Provider · SaaS APIs · code repos · cloud agents · browser · SWG)
        AI Firewall (network egress · DLP · per-user quota)
        Status: In Build. Identity Provider connector first. Not in production.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ETHANA WORKSPACE [COMMERCIAL SKU — ASPIRATIONAL. NO ENGINEERING BASIS.]
  Enterprise chat, RAG, document workflows, department copilots
  No board briefing equivalent. Not in "What We're Building."
  Do not include in proposals.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ETHANA BUILD [COMMERCIAL SKU — PRODUCTION CORE]
  ├── PRODUCTION (safe to claim with stated caveats)
  │     Gateway (multi-tenant, routing, fallback, CallTrace)
  │     Guardrails (six scanners, bidirectional, sub-200ms p95)
  │     Immutable Audit Log (insert-only, SIEM export)
  │     MCP Broker core (registry, runtime, per-call tracing — ~8,000 lines)
  │     Red Teaming (orchestrator + 21 OWASP probes)
  │     Account Management (tenants, RBAC, SSO/OIDC)
  │     Cost tracking (per-tenant, per-project, alert hooks)
  │
  ├── IN BUILD (disclose, do not claim)
  │     NHI for agents (ephemeral tokens, OAuth 2.0 / SPIFFE)
  │     CI/CD Red-Teaming Gate
  │     Governance Policy Engine (OPA / Rego)
  │     Compliance Pack (one-click evidence export)
  │     FinOps (per-user / per-team / GPU cost / dormant licences)
  │     Enterprise features (SCIM, on-prem enterprise bundle)
  │
  └── ASPIRATIONAL (do not claim at any level)
        Visual Agent Builder / DAG Builder
        No board briefing equivalent at any status.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SHARED PLATFORM SERVICES [PRODUCTION — underlies all product lines]
  Guardrails · Red Teaming · Governance Policy · Audit & Compliance · FinOps

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPLIANCE CERTIFICATIONS [IN PROGRESS — do not claim]
  SOC 2 Type II · ISO 27001 · HIPAA-ready
  Source: [BB] page 11 explicitly "in progress."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 8. Answer to the Four Questions

**1. Are these renamed products?**
Partially. "Sentry" was renamed (or absorbed into) "Edge" in the commercial playbook. The underlying engineering workstreams (Sentry's network layer and the original Edge endpoint layer) are distinct in the board briefing. The renaming consolidated two separate In Build products under one commercial brand.

**2. Are these different packaging models?**
Yes, for the Sentry/Edge consolidation. The board briefing shows the engineering taxonomy (Sentry separate from Edge). The playbook shows the commercial packaging (one "Edge" SKU covering both). This is a deliberate simplification for market positioning — one product name for the full "employee AI governance" motion.

**3. Are these different product generations?**
Yes, for Workspace and the Visual Agent Builder. These appear in the June 2026 commercial playbook but have no foundation in the May 2026 board briefing — not even as roadmap items. They represent a generation of product vision beyond what engineering had committed to build as of May 2026. The board briefing's final slide asked the board to "greenlight the suite and line up design partners" — suggesting the full three-product commercial vision had not yet been approved for engineering investment.

**4. Which architecture should Governance OS use?**
The **board briefing's engineering taxonomy** for all status determinations. The **playbook's commercial naming** for customer-facing vocabulary. Never the playbook's status claims for Workspace, Edge observability, or Visual Agent Builder, which all exceed what the board briefing supports. The canonical Governance OS architecture is the diagram in Section 7 above.
