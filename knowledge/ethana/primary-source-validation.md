# Primary Source Validation Report

**Date:** 2026-06-17
**Validates:** `knowledge/ethana/evidence-based-status-review.md`
**Sources used exclusively:**
- `[PB]` Ethana Marketing Playbook, Version 1.0, June 2026
- `[SE]` Study ethana (grounded in Board Briefing May 2026 + Barclays Governance Mapping May 2026)
- `[BB]` Ethana Board Briefing, May 2026 (15-page PDF, confidential)

**Excluded per instruction:** source-of-truth.md, claims-matrix.md, ethana-status-harmonization.md, and all other derived repository files.

---

## 1. What Each Primary Source Directly States

### 1.1 Marketing Playbook [PB] — direct capability statements

| Capability | Playbook claim | Exact text or section |
|---|---|---|
| Edge (observability) | GA | Section 4.1: "Current capability (GA): Observability. Edge currently delivers full AI visibility and audit capabilities." |
| Edge (blocking) | Roadmap | Section 4.1: "On the roadmap (do not position as current): PII masking…source code masking…AI website allowlists and blocklists…Secret detection." |
| Per-user attribution | GA (implied current) | Section 4.1 observability proof points: "Per-user attribution and session-level activity tracking." No status caveat applied. |
| Workspace (all capabilities) | GA (implied current) | Section 4.2: full proof point list, no status caveats of any kind |
| Visual Agent Builder | GA (implied current) | Section 4.3: "Visual agent builder: drag-and-drop DAG workflow design with agents, APIs, functions, conditions, routers, loops, parallel execution, evaluators, guardrails, and human-in-the-loop steps." No status caveat. |
| Discovery (device-level) | GA (implied current) | Section 4.1: "Continuous device-level discovery of every AI tool, browser extension, developer assistant, and local model." Listed as current observability proof point. |
| ISO 27001 | Certified | Section 8.4 footer principles: "Footer credentials: ISO 27001 certified, NVIDIA Inception Program, deployed with regulated customers today." Also: final page footer: "ethana.ai · ISO 27001 Certified · NVIDIA Inception Program" |
| Gateway | GA | Section 4.3 proof point, no caveat |
| Guardrails | GA | Section 4.3 proof point, no caveat |
| Red Teaming (21 OWASP) | Not named explicitly as a standalone proof point in Build section | Section 4.3 mentions "Evaluation & hallucination testing" but "red teaming" is only in Section 5.2 objection handling: "21 OWASP red-teaming probes" mentioned as a differentiator |
| MCP lifecycle management | GA | Section 4.3: "MCP lifecycle management: hosting, versioning, deployment, tool access controls, observability, and composable MCP creation." |
| Pricing | Confirmed | Section 7.1: Edge $10k, Workspace $10k, Build $30k, Bundle $45k |

---

### 1.2 Study Ethana [SE] — direct capability statements

Study ethana is explicitly "grounded exclusively in the Board Briefing (May 2026) and Barclays Governance Mapping Document (May 2026)."

**Critical structural observation:** Study ethana describes a three-product architecture of **Build**, **Sentry**, and **Edge** — not Build, Workspace, and Edge as in the playbook.

| Capability / Product | Study Ethana status | Exact text |
|---|---|---|
| Ethana Build (Gateway) | In production | "Status: In production. Multi-tenant LLM gateway with routing, fallback, per-call cost tracking, and CallTrace shipped." |
| Guardrails (6 scanners) | In production | "Capability status: STRONG — all six scanners in production. Sub-200ms p95 confirmed in briefing." |
| Immutable Audit Log | In production | "Capability status: STRONG — in production." |
| Red Teaming orchestrator | Partial | "Capability status: PARTIAL. Orchestrator + 21 OWASP probes in production. CI/CD gate is still in build." |
| MCP Broker | Partial | "Capability status: PARTIAL. ~8,000 lines in production, per-call tracing shipped. Non-Human Identity (NHI) and ephemeral tokens — the critical identity features — are still in build." |
| PromptOps | Moderate | "Capability status: MODERATE. Present in the platform but not a standalone selling point." |
| FinOps | In Build | "Capability status: IN BUILD. Per-tenant/per-project cost tracking shipped in production. Full FinOps (per-user, per-team, dormant licence detection) is on the roadmap." |
| NHI | In Build | "Capability status: IN BUILD. This is explicitly listed in the 'What We're Building' column of the board briefing. Do not position as available today." |
| **Discovery** | **IN BUILD** | "Capability status: IN BUILD. Connector layer is being built. Identity Provider connector is first. This is roadmap for the critical seven-connector families. **Honest position: don't promise this capability in a bank deployment today.**" Part 6 table: "❌ Not in production." |
| **AI Firewall** | **IN BUILD** | Part 6 table: "❌ Not in production. In build — Zscaler/Netskope integration." |
| **Ethana Edge** | **In Build. Not in production.** | "Status: In build. Endpoint agent (Mac, Linux, Windows), browser extension, and dev-tool config push are all in the build column. **Not in production.**" Part 6 table: "❌ Not in production." |
| **Ethana Sentry** (≠ Workspace) | **Most roadmap-heavy product** | "Status: Discovery (the core of Sentry) is still in build. The connector layer is being built. Identity Provider connector is first. The AI Firewall (network egress control) is also in build. **This is the most roadmap-heavy product line in the suite.**" |
| **Workspace** | **ABSENT** | No mention of "Ethana Workspace" or a governed enterprise chat / RAG product anywhere in Study ethana. |
| **Visual Agent Builder** | **ABSENT** | No mention of a visual agent builder, DAG builder, or drag-and-drop workflow tool anywhere. |
| **ISO 27001** | **❌ Not certified** | Part 6 table: "Compliance Certifications | ❌ Not certified | SOC 2 Type II, ISO 27001, HIPAA-ready — in progress." |
| SOC 2 Type II | Not certified | Same entry as ISO 27001 above. "Hard Gate for BFSI." |

---

### 1.3 Board Briefing [BB] — direct capability statements (May 2026, 15 pages)

**Critical structural observation:** The board briefing describes three products: **Ethana Sentry**, **Ethana Edge**, **Ethana Build**. No product named "Ethana Workspace" appears anywhere in the 15-page document.

**Page 3 (The Suite):**
- Sentry: "secure how employees use AI" → Discovery (Shadow AI scanning) + AI Firewall (network egress · DLP)
- Edge: "secure AI on the user's device" → Endpoint Agent (Mac · Linux · Windows), Browser Extension (Chrome · Edge · agentic browsers), Dev-tool Config (Cursor · Copilot · Claude Code)
- Build: "secure the AI apps your company builds" → Gateway (single LLM front door), MCP Broker (hosts & brokers tools), + Runtime Threat Detection (novel jailbreaks · agent misuse · abuse spikes on production traffic)
- Platform services (shared by all three): Guardrails · Red Teaming · Governance · Audit & Compliance · FinOps

**Page 4 (Gateway):** STATUS: "In production. CallTrace and cost capture shipped."

**Page 5 (Guardrails):** STATUS: "All six scanners in production. Sub-200ms p95." (Note: the slide diagram shows more scanner types visually — Hallucination Grounding, Relevance & No-Refusal, Code & Substring Banning, Competitor & Topic Banning, Gibberish & Invisible Text, Language Detection — in addition to the six named in status.)

**Page 6 (Red Teaming):** STATUS: "Orchestrator + 21 OWASP probes in production. CI/CD gate in build."

**Page 7 (MCP Broker):** STATUS: "~8,000 lines in production. Per-call tracing shipped. NHI & ephemeral tokens in build."

**Page 8 (AI Firewall):** No production status stated. Described as the Sentry product for network-layer AI egress control.

**Page 9 (Discovery):** STATUS: **"Connector layer in build. Identity Provider connector first."** Connected sources listed: Identity Provider, SaaS vendor APIs, Code repos, Cloud agents, Edge telemetry (endpoint + browser), Firewall logs.

**Page 10 (Edge):** Described as "The parts of Ethana that live on the user's own laptop and browser · where AI traffic starts." Components: Endpoint Agent, Browser Extension, Dev-tool Config, Local MCP Discovery, Pulls Signed Policy bundle, Enforces locally · works offline. **No production status line is present on this slide.** Status is determined by page 11.

**Page 11 (Status — "What we have. What we're building."):**

*WHAT WE HAVE:*
- Gateway: multi-tenant LLM gateway in production, with routing, fallback, per-call cost tracking, and CallTrace
- MCP Broker: server registry, hosted runtime, per-tool-call tracing, admin UI · multi-tenant, in production
- Red Teaming: orchestrator with scoring, cost cap, 21 OWASP probes, and multi-turn attacks
- Guardrails: six native scanners · Secrets, PII, Prompt Injection, Jailbreak, Toxicity, Bias
- Immutable Audit Log: insert-only event store, multi-tenant
- Account Management: tenants, projects, RBAC, SSO via OIDC
- Cost & Budget tracking: per-tenant, per-project, with alert hooks

*WHAT WE'RE BUILDING:*
- **Discovery**: seven connector families · Identity Provider, SaaS APIs, code repos, cloud agents, endpoint, browser, SWG
- **Edge**: endpoint agent (Mac, Linux, Windows), browser extension, dev-tool config push for Cursor, Copilot, Claude Code
- AI Firewall: network-egress AI app control with DLP and per-user quota
- Governance: Policy Engine (OPA / Rego) with Signed Policy Bundles pushed to every surface
- Compliance Pack: evidence collectors for EU AI Act, ISO 42001, NIST AI RMF, MITRE ATLAS · one-click export
- FinOps: per-user / per-team token spend, GPU cost, dormant-license findings
- Enterprise features: SSO, SCIM provisioning, RBAC, on-prem deployment, audit retention
- Non-Human Identity (NHI) for agents: ephemeral scoped tokens, OAuth 2.0 Token Exchange / SPIFFE-style workload identity, on-behalf-of delegation
- **Compliance certifications: SOC 2 Type II, ISO 27001, HIPAA-ready · in progress**
- CI/CD Red-Teaming Gate: the `ethana eval` action for every pull request

**Page 13 (Deployment / Packaging):** Suite packaging: "Sentry + Build + all platform services." Options: Suite, Sentry only, Build only. No "Workspace" product or packaging option appears.

**Page 14 (The Ask):** "A platform that already runs." Does not name a new or forthcoming Workspace product. "Greenlight the suite. Line up design partners. Move."

**Workspace:** Not mentioned on any of the 15 pages.
**Visual Agent Builder / DAG Builder:** Not mentioned on any of the 15 pages — not in the Build section, not in "What We Have," not in "What We're Building."

---

## 2. Capability-by-Capability Validation

### 2.1 Workspace

#### What the original review claimed vs. what primary sources directly support

| Claim in evidence-based-status-review.md | Primary source verdict | Classification |
|---|---|---|
| "Playbook provides a highly specific description of Workspace, naming six distinct capability areas" | CONFIRMED — [PB] Section 4.2 directly lists these | Directly supported |
| "Workspace is priced at $10,000/year" | CONFIRMED — [PB] Section 7.1 | Directly supported |
| "[REC] states: 'Direct user observation confirms Workspace is working.'" | CANNOT BE VERIFIED from primary sources. [REC] is a derived file. No primary source describes a user observing Workspace. | Inferred — from derived file |
| "Complete absence from [CAP] capability-status.md" | CANNOT BE DIRECTLY VERIFIED from primary sources (that is a derived file claim). Equivalent PRIMARY SOURCE finding: Workspace is absent from all 15 pages of [BB] and from [SE]. | Inferred — equivalent primary source finding is stronger: absent from board briefing |
| "[SOT] says 'does not appear in any engineering capability status documents, product documentation, or board briefings'" | CANNOT BE VERIFIED (SOT is a derived file). Primary source equivalent: [BB] directly confirms Workspace absence across all 15 pages. | Inferred — but now directly confirmed by primary source |
| "Board briefing apparently doesn't mention Workspace (per [SOT])" | Previously cited via derived file. Now DIRECTLY CONFIRMED by reading [BB]. | Inferred in original review — now directly confirmed |
| "claims-matrix.md marks every Workspace capability Unverified" | CANNOT BE VERIFIED — CLM is a derived file excluded from this review | Inferred — from derived file |
| "competitor-positioning.md: 'Do not represent Workspace as available to clients'" | CANNOT BE VERIFIED — CMP is a derived file | Inferred — from derived file |

**Additional primary source findings not in the original review:**
- [BB] page 3 names the three product lines as Sentry, Edge, and Build — with no Workspace. This means the board briefing's architecture does not include an enterprise chat/RAG product at all.
- [BB] page 13 packages the suite as "Sentry + Build + all platform services" — no Workspace SKU.
- [SE] mentions Sentry as the employee-AI governance product line and Edge as the endpoint product. Neither describes a governed enterprise chat or RAG workspace.
- The May 2026 board briefing predates the June 2026 playbook by one month. A product that is Production/GA would appear in a board briefing — Workspace does not.

**Revised confidence score (primary sources only):** **8 / 100** (down from 18/100)

The original score of 18/100 partly reflected derived file claims that something named Workspace is "unverified." The primary source picture is more absolute: the board briefing — a governance document prepared one month before the playbook — contains no Workspace product, no Workspace pricing, no Workspace feature description, and no Workspace packaging option. The playbook is the sole source for Workspace's existence as a product.

---

### 2.2 Discovery

#### What the original review claimed vs. what primary sources directly support

| Claim in evidence-based-status-review.md | Primary source verdict | Classification |
|---|---|---|
| "Playbook lists 'Continuous device-level discovery of every AI tool' as current GA observability proof point" | CONFIRMED — [PB] Section 4.1 | Directly supported |
| "'30 minutes of install' demo claim in sales plays" | CONFIRMED — [PB] Section 6.1 | Directly supported |
| "Study ethana says Discovery is IN BUILD. 'Don't promise this capability in a bank deployment today.'" | CONFIRMED — [SE] Part 4, Part 6 table | Directly supported |
| "Board briefing: Discovery in 'What We're Building'" | CONFIRMED — [BB] page 11, Discovery explicitly listed under "WHAT WE'RE BUILDING" | Directly supported |
| "Discovery slide status: 'Connector layer in build. Identity Provider connector first.'" | CONFIRMED — [BB] page 9 STATUS field | Directly supported |
| "claims-matrix.md says device-level AI discovery is Beta (not Roadmap)" | CANNOT BE VERIFIED — CLM is a derived file. Both primary sources ([SE], [BB]) say In Build / not in production — not Beta. This was the key distinction between "Beta" and "In Build." | Inferred — from derived file. Primary sources are more conservative. |
| "[REC] user observation confirms discovery works" | CANNOT BE VERIFIED from primary sources | Inferred — from derived file |
| "The previous 42/100 [confidence] partly reflects a Beta label from claims-matrix.md" | The CLM Beta label has no primary source support. Both [SE] and [BB] explicitly say "Not in production." | Inferred basis identified |

**Critical distinction from primary sources:**

The original review scored Discovery at 42/100 and said "Confidence for Beta (device-level, endpoint agent): 65/100." This was based on claims-matrix.md labeling device-level discovery as "Beta" — implying it was in some operational state. The primary sources give no such qualification:

- [BB] page 11: Discovery is explicitly in "WHAT WE'RE BUILDING" — the same column as NHI, Compliance Pack, and other acknowledged non-production items.
- [BB] page 9: STATUS is "Connector layer in build. Identity Provider connector first." Edge telemetry (endpoint + browser) is listed as a data source that Discovery will consume — but Edge itself is also "What We're Building" per page 11.
- [SE]: "❌ Not in production."

There is no primary source that assigns Discovery a "Beta" status. The Beta characterization originates in a derived repository file (claims-matrix.md) and was not verified against the board briefing.

**Additional finding:** The board briefing defines Discovery as a Sentry product. The playbook describes discovery capabilities within Edge. These are different product structures. The board briefing's Edge (endpoint agent, page 10) "sends back" installed tools data to the Discovery system — meaning edge telemetry is one of six Discovery data sources, not a standalone discovery mechanism. Neither Edge nor Discovery is in production per the board briefing.

**Revised confidence score (primary sources only):** **15 / 100** (down from 42/100)

The 42/100 was meaningfully inflated by the Beta characterisation from a derived file. Both primary engineering sources say Discovery is not in production. The playbook's GA claim is directly contradicted by both the board briefing (one month earlier) and Study ethana.

---

### 2.3 Edge

#### What the original review claimed vs. what primary sources directly support

| Claim in evidence-based-status-review.md | Primary source verdict | Classification |
|---|---|---|
| "[PB] Section 4.1: 'Current capability (GA): Observability.'" | CONFIRMED | Directly supported |
| "Playbook explicitly acknowledges blocking, PII redaction, and egress controls as Roadmap" | CONFIRMED — [PB] Section 4.1 roadmap list | Directly supported |
| "'Show the inventory within 30 minutes of install' (sales play 6.1)" | CONFIRMED — [PB] Section 6.1 | Directly supported |
| "capability-status.md says 'Beta. Confirmed in controlled demo only, not at institutional scale.'" | CANNOT BE VERIFIED — CAP is a derived file. Primary sources say "In Build, Not in production" — lower status than Beta. | Inferred — from derived file. Primary sources more conservative. |
| "Board briefing places Edge 'In Build' (previously cited via [SOT])" | DIRECTLY CONFIRMED — [BB] page 11 explicitly lists Edge under "WHAT WE'RE BUILDING": "endpoint agent (Mac, Linux, Windows), browser extension, dev-tool config push for Cursor, Copilot, Claude Code." | Previously inferred via derived file — now directly confirmed |
| "[SE]: 'In build. Endpoint agent (Mac, Linux, Windows), browser extension, and dev-tool config push are all in the build column. Not in production.'" | CONFIRMED | Directly supported |
| "claims-matrix.md: All Edge capabilities have selling rule 'Position as Beta'" | CANNOT BE VERIFIED — CLM is a derived file. Primary sources say "In Build" not "Beta." | Inferred — from derived file. Primary sources more conservative. |
| "HR/employment-law sign-off requirement" | CANNOT BE DIRECTLY CONFIRMED from any primary source. [BB] and [SE] do not mention HR/employment-law as a prerequisite. | Inferred — originated in a derived file, no primary source confirmation. |

**Critical finding from primary sources:**

The original review gave Edge a confidence score of 45/100, citing the Beta label from claims-matrix.md as partial support ("at least it's not just the playbook"). But the primary sources give no such Beta qualification. Both [SE] and [BB] say:
- "Not in production" ([SE])
- Listed under "WHAT WE'RE BUILDING" ([BB] page 11)

The 45/100 score was partly anchored to a Beta characterization that originated in a derived file, not in the primary sources.

Additionally, the original review noted the playbook's internal consistency (acknowledging blocking as roadmap) as a credibility signal. This observation remains valid — the playbook DOES appropriately label several Edge items as roadmap — but it cannot offset the direct primary source contradiction: the board briefing, one month before the playbook, placed Edge in "What We're Building," not in "What We Have."

**Additional finding:**

The board briefing's product architecture (Sentry + Edge + Build) differs from the playbook's (Edge + Workspace + Build). The playbook's "Edge" appears to combine the board briefing's "Sentry" capabilities (Discovery, AI Firewall — both In Build) with the board briefing's "Edge" capabilities (endpoint agent, browser extension, dev-tool config — also In Build). Every component of what the playbook calls "Edge" is In Build per the board briefing. There is no "Edge" component in production.

**Revised confidence score (primary sources only):** **20 / 100** (down from 45/100)

The original 45/100 was substantially inflated by:
- The Beta label from claims-matrix.md (a derived file not supported by primary sources)
- The inference that "Beta means something works" — a characterisation with no primary source basis

Both primary engineering sources explicitly say Edge is not in production. The board briefing (May 2026) was prepared one month before the playbook. A capability that the product team's own board presentation labels as "What We're Building" is not GA.

---

### 2.4 Visual Agent Builder

#### What the original review claimed vs. what primary sources directly support

| Claim in evidence-based-status-review.md | Primary source verdict | Classification |
|---|---|---|
| "[PB] Section 4.3: specific DAG builder description with named node types" | CONFIRMED — [PB] Section 4.3 | Directly supported |
| "Listed alongside Production Build capabilities in Section 4.3" | CONFIRMED — [PB] Section 4.3 lists it without distinction | Directly supported |
| "Section 6.3 sales play mentions 'agent builder' in demo focus" | CONFIRMED — [PB] Section 6.3 | Directly supported |
| "[REC] elevates to Production based on playbook + 'verified as part of the infrastructure suite'" | CANNOT BE VERIFIED from primary sources. [REC] is a derived file. The "verified as part of the infrastructure suite" claim has no primary source. | Inferred — from derived file. Primary sources provide no corroboration. |
| "claims-matrix.md: 'No codebase or engineering documentation exists to support the presence of a visual builder'" | CANNOT BE VERIFIED — CLM is a derived file. Primary source equivalent: [BB] does not mention the Visual Agent Builder anywhere in 15 pages. | Inferred — from derived file. Primary source equivalent directly confirmed. |
| "capability-status.md: Visual Agent Builder absent" | CANNOT BE VERIFIED (derived file). Primary source equivalent: absent from all 15 pages of [BB], not in "What We Have," not in "What We're Building." | Inferred — from derived file. Primary source confirms absence independently. |
| "[BB] (board briefing) apparently does not mention it" | Previously cited via [SOT]. Now DIRECTLY CONFIRMED by reading all 15 pages of [BB]. | Inferred in original review — now directly confirmed |

**Primary source finding (direct):**

The board briefing dedicates individual slides to each major Build product component: Gateway (page 4), Guardrails (page 5), Red Teaming (page 6), MCP Broker (page 7). The Visual Agent Builder has no slide, no mention in the Build product description (page 3), no mention in "What We Have" (page 11), and no mention in "What We're Building" (page 11). Fifteen pages, zero mentions.

The board briefing's Build product line, as presented to the board, consists of: Gateway + MCP Broker + Runtime Threat Detection (listed as a + feature on page 3). No visual workflow builder.

The "Visual Agent Builder" claim in the playbook has no corroboration from either primary engineering source.

**Revised confidence score (primary sources only):** **8 / 100** (down from 12/100)

The original 12/100 was partially justified by the claim in claims-matrix.md that "no codebase documentation exists" (a derived file that the original review treated as authoritative). The primary source picture is structurally identical but more direct: the board briefing simply doesn't include the Visual Agent Builder in any form.

---

### 2.5 ISO 27001

#### What the original review claimed vs. what primary sources directly support

| Claim in evidence-based-status-review.md | Primary source verdict | Classification |
|---|---|---|
| "[PB] footer: 'ISO 27001 Certified'" (twice) | CONFIRMED — [PB] Section 8.4 and final page | Directly supported |
| "Other two footer credentials (NVIDIA Inception, deployed with regulated customers) are independently plausible" | Partially confirmed. NVIDIA Inception Program is an Anthropic partner programme with publicly verifiable membership — plausible. "Deployed with regulated customers today" is an unverified claim that appears only in the playbook footer with no primary source corroboration. | Partially inferred |
| "capability-status.md: 'In progress, not complete. Do not state as held.'" | CANNOT BE VERIFIED — CAP is a derived file | Inferred — from derived file |
| "deployment-and-certifications.md: 'In progress / unverified'" | CANNOT BE VERIFIED — DEP is a derived file | Inferred — from derived file |
| "[BB] (board briefing) apparently doesn't confirm certification" | Previously cited via [SOT]. Now DIRECTLY CONFIRMED: [BB] page 11 explicitly lists "Compliance certifications: SOC 2 Type II, ISO 27001, HIPAA-ready · in progress" under "WHAT WE'RE BUILDING." | Inferred in original review — now directly confirmed |
| "[SE]: '❌ Not certified'" | CONFIRMED — [SE] Part 6 table | Directly supported |
| "The most parsimonious explanation is that ISO 27001 was included prematurely or as an error" | This inference is supported by primary sources — [BB] was one month before [PB] and confirms "in progress." | Inference supported by primary source evidence |
| "No certificate number appears anywhere" | CONFIRMED by primary source absence — neither [BB] nor [SE] contains a certificate number, registrar, or audit scope for ISO 27001 | Directly supported (by absence) |

**Critical primary source finding:**

The board briefing (May 2026) explicitly states under "WHAT WE'RE BUILDING": "Compliance certifications: SOC 2 Type II, ISO 27001, HIPAA-ready · in progress."

For ISO 27001 to be certified in the playbook's June 2026 footer, the certification would need to have been completed in the approximately four weeks between the board briefing and the playbook publication — a period in which the board was told it was "in progress." An ISO 27001 certification completion would typically require: a formal certification decision from the registrar, a certificate issued, and — critically — a board update if the board had just been told it was "in progress." The board briefing's "What We Have" does not include ISO 27001 certification. No primary source contains a certificate number, audit scope, registrar name, or expiry date.

Study ethana is equally direct: the Part 6 production reality table says "❌ Not certified" for compliance certifications including ISO 27001, with the note: "Critical gap for BFSI."

**Revised confidence score (primary sources only):** **5 / 100** (down from 22/100)

The original 22/100 was partly based on the argument that the playbook footer's inclusion of two other plausible credentials (NVIDIA Inception) marginally elevated the credibility of the ISO 27001 claim. The primary source picture removes this ambiguity: a board briefing one month before the playbook explicitly lists ISO 27001 as "in progress" under "What We're Building." The transition from "in progress" to "certified" in under four weeks, without any update to a primary engineering source, is not supported by any evidence.

---

## 3. Revised Confidence Scores (Primary Sources Only)

| Capability | Original score | Revised score | Key driver of change |
|---|---|---|---|
| **Workspace** | 18 / 100 | **8 / 100** | Board briefing (May 2026) has no Workspace product, no Workspace SKU, no Workspace slide — directly read, not inferred via derived files |
| **Discovery** | 42 / 100 | **15 / 100** | "Beta" characterisation from claims-matrix.md (derived file) was anchoring the score upward. Primary sources ([BB], [SE]) both say "not in production" / explicitly In Build. No Beta distinction exists in primary sources. |
| **Edge** | 45 / 100 | **20 / 100** | "Beta" characterisation from claims-matrix.md (derived file) was anchoring the score. [BB] page 11 explicitly places Edge in "WHAT WE'RE BUILDING." [SE] says "Not in production." No primary source supports Beta status. |
| **Visual Agent Builder** | 12 / 100 | **8 / 100** | Primary source picture confirms absence more directly than inferred via derived files. 15 pages of board briefing. Zero mentions. |
| **ISO 27001** | 22 / 100 | **5 / 100** | [BB] page 11 directly lists "ISO 27001 · in progress" under What We're Building — one month before the playbook claims "Certified." [SE] explicitly marks "❌ Not certified." No ambiguity. |

---

## 4. Complete Inferred Claims Inventory

Every statement in `evidence-based-status-review.md` that was cited from a derived repository file rather than directly from a primary source. These claims may or may not be accurate — they are flagged because they cannot be verified without reading a file that is excluded from this validation.

| # | Claim as written | Source cited | Primary source equivalent |
|---|---|---|---|
| 1 | "Direct user observation confirms Workspace is working" | [REC] | No primary source corroboration. Board briefing has no Workspace product. |
| 2 | "[CAP] Workspace does not appear anywhere in capability-status.md" | [CAP] (derived) | Equivalent: Workspace absent from [BB] pages 1–15 |
| 3 | "[SOT] states explicitly: 'Ethana Workspace is entirely unverified. It does not appear in any engineering capability status documents, product documentation, or board briefings.'" | [SOT] (derived, excluded) | Equivalent: [BB] directly confirms Workspace absence. Statement substantively accurate but cited from excluded file. |
| 4 | "[SOT] characterises Workspace as 'a marketing-only concept'" | [SOT] (derived, excluded) | Characterisation consistent with primary sources but not in them |
| 5 | "[CLM] Every Workspace capability is marked 'Unverified – Product Validation Required' with selling rule 'Do not claim or sell.'" | [CLM] (derived, excluded) | Cannot be verified from primary sources |
| 6 | "[CMP] states: 'Do not represent Workspace as available to clients. Microsoft Copilot, Glean, and ChatGPT Enterprise are fully operational production platforms.'" | [CMP] (derived) | Cannot be verified from primary sources |
| 7 | "[CLM]: selling rule for Discovery: 'Position as Beta.'" | [CLM] (derived, excluded) | Primary sources say "not in production" — no Beta characterisation |
| 8 | "[CAP]: Device-Level AI Discovery listed as Beta (not Roadmap)" | [CAP] (derived) | Primary sources: [BB] and [SE] both say In Build / not in production. No Beta tier in primary sources. |
| 9 | "[REC] user observation confirms discovery works" | [REC] (derived) | No primary source corroboration |
| 10 | "Board briefing apparently places it [Discovery] below even Beta status (from Study ethana)" | This was cited indirectly. [SE] directly says "Not in production." [BB] page 11 directly confirms "What We're Building." | Claim was accurate but now directly confirmed rather than inferred |
| 11 | "[CAP]: 'Beta. Confirmed in controlled demo only, not at institutional scale. Never lead with this in BFSI, insurance, healthcare, or government.'" (Edge) | [CAP] (derived) | Primary source: [BB] says "What We're Building" (In Build). [SE]: "Not in production." No "Beta" tier in primary sources. |
| 12 | "[CLM]: All Edge capabilities have selling rule 'Position as Beta'" | [CLM] (derived, excluded) | Cannot be verified. Primary sources indicate lower status (In Build, not Beta) |
| 13 | "[CLM]: Per-user attribution is In Build / Roadmap — 'Do not claim as GA'" | [CLM] (derived, excluded) | Cannot be verified from primary sources. Per-user attribution appears in playbook as GA but Edge (which contains it) is In Build per [BB]. |
| 14 | "HR and employment-law sign-off requirement for Edge" | A derived file (capability-status.md) | No mention in [BB] or [SE]. Unconfirmed by primary sources. |
| 15 | "[CLM]: 'No codebase or engineering documentation exists to support the presence of a visual builder'" (Visual Agent Builder) | [CLM] (derived, excluded) | Cannot be verified from primary sources. Primary source equivalent: [BB] does not mention Visual Agent Builder in any of 15 pages. |
| 16 | "[CAP]: Visual Agent Builder absent from capability-status.md" | [CAP] (derived) | Equivalent: absent from all 15 pages of [BB] |
| 17 | "[SOT]: 'Supported only by Marketing Playbook; uncorroborated in product docs/board briefings'" (Visual Agent Builder) | [SOT] (derived, excluded) | Substantively confirmed by directly reading [BB]: not mentioned. |
| 18 | "[REC] elevation of Visual Agent Builder to Production 'verified as part of the infrastructure suite'" — treated as circular | [REC] (derived) | No primary source for this "verified" claim. [BB] Build section has no visual builder. |
| 19 | "[CAP]: 'In progress, not complete: SOC 2 Type II, ISO 27001, HIPAA-ready. Do not state as held.'" (ISO 27001) | [CAP] (derived) | Primary source equivalent: [BB] page 11: "Compliance certifications: SOC 2 Type II, ISO 27001, HIPAA-ready · in progress" under "WHAT WE'RE BUILDING" |
| 20 | "[DEP]: 'ISO 27001 / In progress / unverified'" | [DEP] (derived) | Equivalent: same [BB] page 11 finding |
| 21 | "[SOT] explicitly says 'Marketing Playbook claims certified; contradicted by Capability status file and Product documentation'" | [SOT] (derived, excluded) | Substantively confirmed by primary sources |
| 22 | "Bias scanner is a runtime text filter, not a model bias audit" | Derived files (claims-matrix.md, source-of-truth.md) | [SE] partially corroborates: "Ethana does not inspect ML training data, test disparate impact across demographic groups, or validate vendor AI Act conformity." Directionally supported. |
| 23 | "On-prem at Tier 1 bank scale is unproven" | [DEP] (derived) | [SE] directly confirms: "On-Prem Deployment: Supported (stated). Likely Enterprise Maturity: Unproven at bank scale." Supported by [SE]. |
| 24 | "Discovery Roadmap in [CAP] refers to connector layer; Beta in [CLM] refers to endpoint agent" — the nuance between the two | Both [CAP] and [CLM] (derived) | [BB] page 9 confirms six Discovery data sources including "Edge telemetry (endpoint + browser)." But Edge itself is In Build per page 11. The distinction between connector vs. endpoint discovery has no Beta/Roadmap breakdown in primary sources — both are In Build. |

---

## 5. Structural Findings Not in the Original Review

### Finding 1: The board briefing and playbook describe different product architectures

**Board briefing (May 2026):** Sentry + Edge + Build
**Marketing playbook (June 2026):** Edge + Workspace + Build

The board briefing's "Sentry" (Discovery + AI Firewall, both In Build) does not appear as a named product in the playbook. The board briefing's "Edge" (endpoint agent + browser extension + dev-tool config, explicitly "What We're Building") becomes part of the playbook's "Edge" section. A new product — "Workspace" (governed enterprise chat + RAG) — appears in the playbook with no board briefing equivalent.

This structural divergence means:
- Everything the playbook calls "Edge" is In Build per the board briefing (Sentry and Edge are both "What We're Building")
- The playbook's "Workspace" is entirely absent from the board briefing
- The board briefing's product suite is internally consistent and limited to Production capabilities

### Finding 2: Edge's playbook description combines two board briefing products

The playbook's Edge section describes both:
- Endpoint-level monitoring (board briefing's Edge: endpoint agent, browser extension, dev-tool config)
- Employee-AI governance at the network level (board briefing's Sentry: Discovery, AI Firewall)

Per the board briefing, BOTH of these product lines are "What We're Building." The playbook's Edge is a commercial umbrella for two engineering products that are both pre-production.

### Finding 3: The board briefing contains no mention of PromptOps by name

The original review accepted PromptOps as Production without direct primary source verification. The board briefing's "What We Have" list does not name PromptOps explicitly. It is referenced indirectly via the Gateway slide (which shows version control in the diagram). Study ethana describes it as "MODERATE. Present in the platform but not a standalone selling point." Neither primary source assigns it a clean "Production" label by name, though the Gateway status implies core prompt management is production-adjacent.

### Finding 4: "Deployed with regulated customers today" (playbook footer) has no primary source corroboration

The playbook footer states: "deployed with regulated customers today." Neither [BB] nor [SE] names or describes a regulated customer deployment. [SE] explicitly states about procurement: "The honest answer on Ethana's current stage should be framed as: early-stage, founder access, customisation opportunity, not an established enterprise reference list." This directly contradicts the footer claim.

### Finding 5: Red Teaming's production status in primary sources excludes CI/CD gate

The original review's accuracy on Red Teaming is confirmed: [BB] page 6 STATUS: "Orchestrator + 21 OWASP probes in production. CI/CD gate in build." [SE] says "PARTIAL. Orchestrator + 21 OWASP probes in production. CI/CD gate is still in build." These are fully consistent.

### Finding 6: Guardrails slide shows more than six scanner types

[BB] page 5 visually depicts more scanner types than the "six native scanners" mentioned in the status text — including Hallucination Grounding, Relevance & No-Refusal, Code & Substring Banning, Competitor & Topic Banning, Gibberish & Invisible Text, and Language Detection in addition to the core six. The STATUS text on the same slide says "All six scanners in production." This is not directly reconciled in the board briefing. The "six" label appears to refer to the core guardrail categories (Secrets/PII, Injection, Jailbreak, Toxicity, Bias, Hallucination) with the other types potentially being sub-types or extensions.

---

## 6. Claims in evidence-based-status-review.md That Are Directly Confirmed by Primary Sources

For completeness — claims that survived primary source validation:

| Claim | Confirmed by |
|---|---|
| Playbook describes Workspace in detail with named source integrations | [PB] Section 4.2 |
| Playbook explicitly labels blocking, PII redaction, and egress as Edge Roadmap | [PB] Section 4.1 |
| Playbook says "30 minutes to inventory" (sales play) | [PB] Section 6.1 |
| Study ethana: Edge is "In Build, Not in production" | [SE] Part 3, Part 6 |
| Study ethana: Discovery is "IN BUILD. Don't promise this in a bank deployment today." | [SE] Part 4, Part 6 |
| Study ethana: ISO 27001 "❌ Not certified" | [SE] Part 6 |
| Board briefing: Edge is in "WHAT WE'RE BUILDING" | [BB] page 11 |
| Board briefing: Discovery is in "WHAT WE'RE BUILDING" | [BB] pages 9, 11 |
| Board briefing: ISO 27001 listed as "in progress" under "WHAT WE'RE BUILDING" | [BB] page 11 |
| Board briefing: Workspace absent from all 15 pages | [BB] pages 1–15 (read in full) |
| Board briefing: Visual Agent Builder absent from all 15 pages | [BB] pages 1–15 (read in full) |
| Gateway is Production | [BB] page 4, [SE] |
| Guardrails (six scanners) are Production | [BB] page 5, [SE] |
| Immutable Audit Log is Production | [BB] page 11, [SE] |
| MCP Broker core (~8,000 lines) is Production; NHI in build | [BB] page 7, [SE] |
| Red Teaming orchestrator + 21 OWASP probes is Production; CI/CD gate in build | [BB] page 6, [SE] |
| On-prem deployment supported but unproven at Tier 1 bank scale | [SE] Part 6 |
| SOC 2 Type II not yet certified | [BB] page 11, [SE] Part 6 |
| NHI is In Build | [BB] pages 7, 11; [SE] |
| Playbook's credibility is enhanced by accurate roadmap labeling within Edge section | Confirmed — [PB] roadmap items (blocking, PII redaction, egress) directly match "WHAT WE'RE BUILDING" in [BB] |

---

## 7. Summary

The five capabilities reviewed in `evidence-based-status-review.md` were generally adjudicated in the right direction, but multiple confidence scores were inflated by derived file claims — particularly the "Beta" characterisation applied to Edge and Discovery by claims-matrix.md. When validated against primary sources only:

- **Workspace**: Absent from the board briefing (a document produced one month before the playbook). 8/100.
- **Discovery**: Explicitly "in build" in both the board briefing and Study ethana. No primary source supports Beta status. 15/100.
- **Edge**: Explicitly "What We're Building" in the board briefing. Study ethana says "Not in production." No primary source supports Beta status. 20/100.
- **Visual Agent Builder**: Not mentioned in 15 pages of the board briefing, including the Build product section. 8/100.
- **ISO 27001**: The board briefing (May 2026) lists it under "What We're Building: Compliance certifications … in progress." One month later, the playbook says "Certified." No primary source certificate exists. 5/100.

The marketing playbook (June 2026) consistently makes claims one to two status tiers above what the board briefing (May 2026) documents. The most significant finding is structural: the board briefing does not contain the "Workspace" product at all — not as a roadmap item, not as a planned SKU, not as a named concept.
