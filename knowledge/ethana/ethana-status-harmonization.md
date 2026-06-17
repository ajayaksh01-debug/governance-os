# Ethana Status Harmonization

**Purpose:** Cross-file conflict analysis. For every capability, this file identifies what each source says, surfaces the disagreement, recommends a canonical status, and sets claim eligibility. No existing file is modified.

**Sources compared:**
- `production-status.md` — the matrix built from confirmed engineering sources (board briefing, Study doc)
- `source-of-truth.md` — the June 2026 document that introduced the three-product architecture (Edge, Workspace, Build) and attempted to reconcile engineering vs marketing
- `ethana-status-reconciliation.md` — the reconciliation that elevated Discovery, Edge, and Workspace to Production based on "direct user observation" and the marketing playbook
- `claims-matrix.md` — the commercial claims layer, structured by product line

**Methodology:** Engineering-verified sources (board briefing, Study doc, the capability files built from them) outrank marketing materials where they conflict. "Direct user observation" and "marketing playbook says GA" are the weakest evidence types and are not sufficient to override engineering documentation without written product-team confirmation. This is the core judgment call in this file.

---

## Conflict severity legend

| Level | Meaning |
|---|---|
| **Critical** | Sources directly contradict each other on a binary claim (Production vs Roadmap). Using the wrong status in a regulated proposal is a procurement-disqualifying error. |
| **Moderate** | Sources give different granularity or sub-status but broadly agree on direction. |
| **Resolved** | All sources agree. No conflict. |

---

## Section 1 — Ethana Build (AI Infrastructure and Control Plane)

### LLM Gateway and Multi-Model Routing

| Source | Status stated |
|---|---|
| production-status.md | Production |
| source-of-truth.md | Production (GA) |
| ethana-status-reconciliation.md | Production (GA) |
| claims-matrix.md | Production (GA) |

**Conflict:** None.
**Canonical status: Production.**
**Claim eligibility: Yes (with LLM-only caveat).** Non-LLM REST API coverage is confirmed out of scope. All four files note this limitation.

---

### Runtime Guardrails (6 scanners: Secrets, PII, Prompt Injection, Jailbreak, Toxicity, Bias)

| Source | Status stated |
|---|---|
| production-status.md | Production |
| source-of-truth.md | Production (GA) |
| ethana-status-reconciliation.md | Production (GA) |
| claims-matrix.md | Production (GA) |

**Conflict:** None.
**Canonical status: Production.**
**Claim eligibility: Yes (with caveats).** The Bias scanner is a runtime text filter, not a model bias audit. Sub-200ms p95 requires load validation before quoting under high concurrency. Both caveats appear consistently across files.

---

### Immutable Audit Logs (Ethana Build layer)

| Source | Status stated |
|---|---|
| production-status.md | Production |
| source-of-truth.md | Production (GA) |
| ethana-status-reconciliation.md | Production (GA) |
| claims-matrix.md | Production (GA) |

**Conflict:** None.
**Canonical status: Production.**
**Claim eligibility: Yes.** The strongest single claim in the platform. All files agree this is the regulatory anchor (EU AI Act Art.12, FCA SYSC 9, RBI IT Outsourcing). Schema fit for specific regulator fields is a configuration engagement, not out-of-the-box.

---

### MCP Security Broker (core)

| Source | Status stated |
|---|---|
| production-status.md | Production (NHI In Build) |
| source-of-truth.md | Production (GA), NHI In Build |
| ethana-status-reconciliation.md | Production (GA) |
| claims-matrix.md | Production (GA), NHI In Build |

**Conflict:** None on the core broker. All sources separate the core (Production) from NHI (In Build).
**Canonical status: Production for broker core. In Build for NHI.**
**Claim eligibility: Yes for broker. No for NHI.** Proactively disclose the NHI gap: without it, agent identity separation is unsolved and agents run with human permissions.

---

### Red Teaming Orchestrator (21 OWASP probes)

| Source | Status stated |
|---|---|
| production-status.md | Production (CI/CD gate In Build) |
| source-of-truth.md | Production (GA), CI/CD In Build |
| ethana-status-reconciliation.md | Production (GA) |
| claims-matrix.md | Production (GA), CI/CD In Build |

**Conflict:** None.
**Canonical status: Production for orchestrator. In Build for CI/CD gate.**
**Claim eligibility: Yes for orchestrator. No for CI/CD gate.**

---

### Project-Level Cost Controls

| Source | Status stated |
|---|---|
| production-status.md | Production |
| source-of-truth.md | Production (GA) |
| ethana-status-reconciliation.md | Production (GA) |
| claims-matrix.md | Production (GA) |

**Conflict:** None.
**Canonical status: Production.**
**Claim eligibility: Yes at project level.** Full FinOps (per-user, GPU, dormant licences) is In Build across all sources.

---

### PromptOps

| Source | Status stated |
|---|---|
| production-status.md | Not listed separately — noted as "present in gateway interface" |
| source-of-truth.md | Production (GA) |
| ethana-status-reconciliation.md | Production (GA) |
| claims-matrix.md | Not listed |

**Conflict:** Moderate. production-status.md omitted it as a standalone capability. source-of-truth.md and reconciliation both call it Production. The Study doc / board briefing is the tiebreaker — PromptOps (prompt registry, versioning, A/B testing) appears there as a named capability.
**Canonical status: Production.** Recommend adding it explicitly to production-status.md.
**Claim eligibility: Yes.** Prompt registry, versioning, rollback. Confirm A/B testing is live before claiming it specifically.

---

### Evaluation Engine (hallucination detection, regression testing, dataset management, benchmarking)

| Source | Status stated |
|---|---|
| production-status.md | Not listed separately |
| source-of-truth.md | Split: hallucination detection and regression testing Production; dataset management and benchmarking Unverified |
| ethana-status-reconciliation.md | Not addressed separately |
| claims-matrix.md | Not listed |

**Conflict:** Moderate. The capability exists in source-of-truth.md with an internal split.
**Canonical status:** Hallucination detection and regression testing — **Production, pending single-source confirmation.** Dataset management and model benchmarking — **Unverified, treat as not available.** The sub-capability split in source-of-truth.md is the right approach; the unverified half must not be claimed.
**Claim eligibility: Yes for hallucination detection and regression testing only. No for dataset management and benchmarking until engineering confirms.**

---

### Visual Agent Builder (DAG workflow)

| Source | Status stated |
|---|---|
| production-status.md | Not listed |
| source-of-truth.md | Unverified — Product Validation Required |
| ethana-status-reconciliation.md | Listed as Production (GA) |
| claims-matrix.md | Unverified — Do not claim or sell |

**Conflict: Critical.** ethana-status-reconciliation.md elevates it to Production. source-of-truth.md and claims-matrix.md both mark it Unverified with explicit "do not claim" instructions. No engineering documentation exists for it in any board briefing or Study doc.
**Canonical status: Unverified.** The reconciliation file's elevation to Production has no engineering evidence. The marketing playbook is the only source, which is insufficient.
**Claim eligibility: No.** Do not mention in proposals until engineering validates the codebase.

---

### Compliance Pack (evidence export)

| Source | Status stated |
|---|---|
| production-status.md | In Build |
| source-of-truth.md | In Build |
| ethana-status-reconciliation.md | In Build |
| claims-matrix.md | In Build — Do not claim availability |

**Conflict:** None.
**Canonical status: In Build.**
**Claim eligibility: No.** Human-delivered equivalent is a Cursory Service today.

---

### Governance Policy Engine (OPA/Rego)

| Source | Status stated |
|---|---|
| production-status.md | In Build |
| source-of-truth.md | In Build |
| ethana-status-reconciliation.md | In Build |
| claims-matrix.md | Not listed |

**Conflict:** None.
**Canonical status: In Build.**
**Claim eligibility: No.**

---

### NHI, SCIM, Enterprise Hardening, FinOps (full), CI/CD Gate

All four sources agree: **In Build**. No conflict. Claim eligibility: **No** across the board. Omitted from detailed rows to avoid repetition.

---

### Shadow AI Connectors

| Source | Status stated |
|---|---|
| production-status.md | Roadmap (IdP connector In Build) |
| source-of-truth.md | In Build / Roadmap (IdP In Build, others Roadmap) |
| ethana-status-reconciliation.md | In Build / Roadmap |
| claims-matrix.md | IdP In Build per Edge section |

**Conflict:** None on substance. All agree on the IdP / rest split.
**Canonical status: IdP connector In Build. All other connectors Roadmap.**
**Claim eligibility: No for any connector.** Use the shadow AI problem to create urgency. Do not imply tooling is available.

---

## Section 2 — Ethana Edge (Endpoint AI Monitoring and Governance)

This is the highest-conflict product line. The reconciliation file elevated it to Production based on "direct user observation." The engineering files do not support this.

### Core Edge status

| Source | Status stated |
|---|---|
| production-status.md | Beta — controlled demo only, not at institutional scale; never lead in BFSI |
| source-of-truth.md | Beta — explicitly warns "do not pitch as Production-ready GA in regulated accounts" |
| ethana-status-reconciliation.md | Production (GA) — based on direct user observation and marketing playbook |
| claims-matrix.md | Beta across all Edge capabilities |

**Conflict: Critical.** The reconciliation file's Production elevation is contradicted by source-of-truth.md (the document it claims to extend), production-status.md, and claims-matrix.md. "Direct user observation" that a feature works in a demo or internal environment does not constitute institutional-scale GA for regulated procurement. The marketing playbook is not engineering validation.

**Canonical status: Beta.**
**Claim eligibility: No in regulated accounts (BFSI, insurance, healthcare, government).** In any sector, disclose Beta status. Do not lead with Edge. Position as a controlled proof-of-concept only.

**Specific Edge sub-capabilities:**

| Capability | Canonical status | Claim eligibility |
|---|---|---|
| Device-level discovery and inventory | Beta | No in regulated accounts |
| Browser AI monitoring (ChatGPT, Claude, Gemini) | Beta | No in regulated accounts |
| Developer tool monitoring (Cursor, Copilot, Claude Code) | Beta | No in regulated accounts |
| Per-user attribution | In Build | No |
| Endpoint agent (Intune/Jamf, Mac/Linux/Windows) | Beta | No in regulated accounts |
| Sensitive data redaction at browser (PII, secrets, code) | Roadmap | No |
| AI website egress blocking | Roadmap | No |

**Note on the HR / employment-law flag.** source-of-truth.md and production-status.md both flag that Edge-level endpoint and browser monitoring requires HR and employment-law sign-off before deployment. This is a procurement dependency, not just a product limitation. It must be raised in any regulated account conversation.

---

## Section 3 — Ethana Workspace (Governed Chat and RAG)

### Core Workspace status

| Source | Status stated |
|---|---|
| production-status.md | Not listed (predates the three-product naming) |
| source-of-truth.md | Entirely Unverified — Product Validation Required. Caution block: "does not appear in any engineering capability status documents, product documentation, or board briefings" |
| ethana-status-reconciliation.md | Production (GA) — based on direct user observation and marketing playbook |
| claims-matrix.md | Entirely Unverified — Do not claim or sell across all sub-capabilities |

**Conflict: Critical.** The reconciliation file's Production elevation is the only source making this claim. source-of-truth.md explicitly states the entire product line is marketing-only and engineering-unverified. claims-matrix.md independently marks every sub-capability as Do Not Claim. No board briefing or Study doc reference exists for Workspace.

**Canonical status: Unverified.**
**Claim eligibility: No across all sub-capabilities.**

**Specific Workspace sub-capabilities:**

| Capability | Canonical status | Claim eligibility |
|---|---|---|
| Governed enterprise chat | Unverified | No |
| Document RAG (SharePoint, Confluence, Notion) | Unverified | No |
| Workflows and drafting | Unverified | No |
| RBAC on knowledge sources | Unverified | No |
| PII auto-masking in vector storage | Unverified | No |
| Immutable chat logging | Unverified | No |

**Important boundary.** Even if Workspace is eventually validated, the Ethana platform does not govern what is inside the vector database: outdated, biased, or incorrect documents are not detectable or fixable by the platform. This boundary must be stated explicitly in any RAG-related conversation regardless of Workspace status.

---

## Section 4 — Certifications

### ISO 27001

| Source | Status stated |
|---|---|
| production-status.md | Complete (held) — based on direct user confirmation in session |
| source-of-truth.md | Unverified — marketing playbook claims certified, contradicted by capability-status.md and deployment-and-certifications.md which state "in progress / unverified" |
| ethana-status-reconciliation.md | Certified / Held — based on marketing playbook footer |
| claims-matrix.md | Not addressed |

**Conflict: Critical.** Three sources say three different things. source-of-truth.md explicitly says the marketing playbook claim is contradicted by engineering documents. production-status.md reflects a direct confirmation given in this working session (not engineering documentation). The reconciliation file relies solely on the marketing playbook footer.

**Canonical status: Treat as Unverified pending written confirmation from Ethana's engineering or legal team.**

**Claim eligibility: No until written confirmation received.** The direct session confirmation is noted but a marketing playbook footer and a verbal confirmation are both insufficient for regulated procurement. A certificate or auditor letter is required. Do not state as held until that document exists. If confirmed in writing, update production-status.md and this file simultaneously.

---

### SOC 2 Type II

| Source | Status stated |
|---|---|
| production-status.md | In Progress |
| source-of-truth.md | In Build (In Progress) |
| ethana-status-reconciliation.md | In Build (In Progress) |
| claims-matrix.md | Implicit (flagged as hard blocker in regulated accounts) |

**Conflict:** None.
**Canonical status: In Progress.**
**Claim eligibility: No.** Hard procurement blocker for financial services. Raise proactively.

---

### HIPAA-ready

All sources agree: **In Progress.** Claim eligibility: **No.**

---

## Section 5 — Deployment models

| Capability | Canonical status | Conflict? | Claim eligibility |
|---|---|---|---|
| SaaS / VPC / On-Premise / Air-Gapped (model support) | Production | None — all sources agree | Yes (with Tier 1 scale caveat) |
| India VPC with gateway PII masking | Production | None | Yes (with scale caveat) |
| On-premise at Tier 1 bank scale | Beta — stated supported, unproven at scale | None | Yes (caveat mandatory): supported deployment model, not proven at institutional scale |

---

## Section 6 — Structural conflicts in the reconciliation file

The following problems in ethana-status-reconciliation.md must be noted for anyone using it as a reference.

**Problem 1: Evidential standard.** "Direct user observation" is used to override engineering documentation for Discovery, Edge, and Workspace. A working demo or internal test environment is not equivalent to GA status in regulated procurement. This elevation methodology is not acceptable for financial services proposals.

**Problem 2: Marketing playbook as primary source.** The reconciliation file uses the June 2026 marketing playbook to confirm GA status for multiple capabilities that the engineering files mark as Beta or Unverified. A marketing asset is not an engineering validation artifact.

**Problem 3: Workspace elevation.** source-of-truth.md (the document the reconciliation file claims to extend) explicitly marks Workspace as "entirely unverified" and states it "does not appear in any engineering capability status documents." The reconciliation file then marks Workspace as Production (GA). This is a direct contradiction of its own source.

**Problem 4: Edge elevation.** source-of-truth.md warns "do not pitch Ethana Edge as a Production-ready GA product in regulated accounts." The reconciliation file marks Edge as Production (GA). This is a direct contradiction.

**Recommendation:** Do not use ethana-status-reconciliation.md as a standalone reference. Use this harmonization file and production-status.md together, with source-of-truth.md as the narrative companion.

---

## Canonical status summary

| Capability | Canonical status | Claim eligibility |
|---|---|---|
| LLM Gateway | Production | Yes (LLM-only caveat) |
| Runtime Guardrails (6 scanners) | Production | Yes (load and bias caveats) |
| Immutable Audit Logs | Production | Yes — lead claim |
| MCP Security Broker (core) | Production | Yes (disclose NHI gap) |
| MCP NHI | In Build | No |
| Red Teaming Orchestrator | Production | Yes |
| Red Teaming CI/CD Gate | In Build | No |
| Project-Level Cost Controls | Production | Yes (project level only) |
| PromptOps | Production | Yes (confirm A/B testing sub-feature) |
| Hallucination Detection / Regression Testing | Production (pending single-source confirm) | Yes (with confirmation) |
| Dataset Management / Model Benchmarking | Unverified | No |
| Visual Agent Builder | Unverified | No |
| Full FinOps | In Build | No |
| Compliance Pack | In Build | No |
| Governance Policy Engine | In Build | No |
| SCIM / Enterprise Hardening | In Build | No |
| Shadow AI Connectors (IdP) | In Build | No |
| Shadow AI Connectors (all others) | Roadmap | No |
| Ethana Edge (all sub-capabilities) | Beta | No in regulated accounts |
| Edge PII/secrets redaction | Roadmap | No |
| Edge egress blocking | Roadmap | No |
| Ethana Workspace (all sub-capabilities) | Unverified | No |
| Discovery | Beta / Roadmap (Beta at best for demo; connector layer In Build / Roadmap) | No in regulated accounts |
| ISO 27001 | Unverified (pending written confirmation) | No until certificate confirmed |
| SOC 2 Type II | In Progress | No |
| HIPAA-ready | In Progress | No |
| On-Premise / VPC (model support) | Production | Yes (Tier 1 scale caveat mandatory) |
| India VPC + PII masking | Production | Yes (scale caveat) |

---

## Recommended file authority hierarchy

Use this order when sources conflict. Higher number wins.

1. ethana-status-reconciliation.md — lowest authority. Evidence standard is insufficient for regulated claims.
2. Marketing playbook — marketing asset, not engineering validation. Never use as primary evidence.
3. source-of-truth.md — narrative-layer reconciliation. Good for context and the three-product framing.
4. claims-matrix.md — commercial claims layer. Authoritative on claim wording and selling rules.
5. production-status.md — engineering-first matrix. Highest authority on binary status decisions.
6. This file (ethana-status-harmonization.md) — cross-file conflict resolution layer. Use when sources disagree.
