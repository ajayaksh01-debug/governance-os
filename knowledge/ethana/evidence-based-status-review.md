# Evidence-Based Capability Status Review

**Date:** 2026-06-17
**Scope:** Workspace · Discovery · Edge · Visual Agent Builder · ISO 27001
**Method:** Neutral evidence adjudication — neither the marketing playbook nor any repository file is presumed correct. Each source is evaluated on evidence quality and specificity.

---

## Methodology

### Sources evaluated

| Source | Abbreviation | Type |
|---|---|---|
| Ethana Marketing Playbook v1.0, June 2026 | [PB] | Product team authored marketing document |
| `capability-status.md` | [CAP] | Internal engineering status matrix |
| `source-of-truth.md` | [SOT] | Cross-source product truth layer |
| `claims-matrix.md` | [CLM] | Commercial claims and selling rules |
| `ethana-status-reconciliation.md` | [REC] | Status reconciliation based on user observation + playbook |
| `deployment-and-certifications.md` | [DEP] | Deployment and certification status |
| `competitor-positioning.md` | [CMP] | Competitive positioning and honest boundaries |
| `Study ethana.txt` (board briefing) | [BB] | Referenced throughout [SOT] as an engineering evidence source. Not directly read, but cited consistently by [SOT] for capability statuses. Treated as engineering testimony. |

### Evidence weight hierarchy

This review does not pre-assign authority to any single file. Instead it weights evidence by the specificity and type of claim:

| Evidence type | Weight | Rationale |
|---|---|---|
| Named certificate, audit scope, registrar, expiry date | Highest | External, verifiable, falsifiable |
| Codebase reference with line count / API documentation | Very high | Engineering artifact, not assertion |
| Named customer deployment reference | High | External validation of production claim |
| Board briefing / engineering briefing | Medium-high | Internal but intended to be accurate to engineering leadership |
| Product team playbook assertion with specific feature detail | Medium | Authoritative on intent; less authoritative on completion state |
| "Direct user observation" without named context | Low-medium | Real but un-contextualized (demo ≠ production scale) |
| Inferred status ("if the playbook says X it must be true") | Low | Circular if playbook itself is the disputed source |

### Confidence score definition

All scores in this document are **Confidence in Production/GA status** — the probability, given all available evidence, that the capability is genuinely production-ready for enterprise deployment today. A score of 100 would require convergent evidence from multiple independent sources including external validation. A score of 0 would indicate active evidence of non-existence.

---

## 1. Ethana Workspace

### 1.1 Evidence supporting existence

- **[PB]** Section 4.2 provides a highly specific description of Workspace, naming six distinct capability areas: enterprise chat, RAG on named sources (SharePoint, Confluence, Notion, Google Drive), document workflows, RBAC on knowledge sources, PII auto-masking, immutable audit logging, and custom chat widgets. The specificity of named integrations (SharePoint, Confluence, Google Drive) suggests product team familiarity, not generic marketing copy.
- **[PB]** Workspace is priced at $10,000/year with an extra-node fee of $2,000/year. Pricing of a specific product with node-expansion economics implies commercial intent beyond vaporware.
- **[REC]** States: "Direct user observation confirms Workspace is working. Aligns with the latest Marketing Playbook." One person claims to have used it. This is real evidence that something called Workspace exists in some operational form.
- **[PB]** Section 2.3 positions Workspace specifically against Microsoft Copilot and Glean — competitors that have very specific, known capabilities. Constructing specific differentiation claims (on-premises parity, immutable audit logging) against known competitors implies at least a design reference if not a working product.

### 1.2 Evidence supporting Production status

- **[PB]** No status caveats applied to Workspace in the playbook. Every proof point is presented as current.
- **[REC]** Explicitly elevates to Production (GA) based on user observation.

### 1.3 Evidence supporting Beta or lower status

- **[CAP]** Workspace does not appear anywhere in `capability-status.md` — not in Production, In Build, Beta, or Roadmap tiers. A product that is genuinely Production would appear in a capability status matrix written to be "the single most important artifact in this knowledge base for a procurement conversation." Complete absence is stronger counter-evidence than an explicit Beta label.
- **[SOT]** States explicitly: "Ethana Workspace is entirely unverified. It does not appear in any engineering capability status documents, product documentation, or board briefings." The specific inclusion of "board briefings" is significant — [BB] (Study ethana.txt) is cited throughout [SOT] as an engineering source, and it apparently does not mention Workspace.
- **[CLM]** Every Workspace capability is marked "Unverified – Product Validation Required" with the selling rule "Do not claim or sell." This is a commercial claims document intended to prevent misrepresentation in proposals — its authors had reason to be accurate.
- **[CMP]** States: "Ethana Workspace is Unverified in the codebase. While marketed as GA, there is no engineering corroboration of Workspace in the repository. Do not represent Workspace as available to clients." This is a direct, falsifiable assertion about codebase state.
- **[SOT]** characterises Workspace as "a marketing-only concept that requires engineering validation before commercial commitment."
- **[REC]**'s "user observation" claim is un-contextualized — no setting described, no feature demonstrated, no version mentioned. A demo environment and a production product are different things.

### 1.4 Missing evidence

- No API documentation, version number, or changelog for Workspace
- No named or anonymised customer deployment
- No codebase reference or line count
- No engineering sign-off document
- [BB] (board briefing) does not mention Workspace per [SOT]'s cross-reference
- No description of the technology stack (which vector DB, which embedding model, which chat framework)

### 1.5 Confidence score

**18 / 100 — Workspace operates at Production/GA status**

The playbook is the sole substantive source for Workspace's existence as a production product. Four independent repository files (CAP, SOT, CLM, CMP) — including one that explicitly references a board briefing — find no engineering corroboration. "Direct user observation" from [REC] is real but un-contextualized and is the only non-playbook source supporting any operational status. Complete absence from a board briefing is a particularly strong counter-signal.

**Adjudication:** The evidence balance indicates Workspace exists in some form — the specific proof points and pricing suggest it is not purely fictional. However, it has not been corroborated as production-ready by any engineering source. Most likely state: pre-GA product in development, with marketing positioning ahead of engineering completion.

---

## 2. Discovery (Shadow AI Inventory)

### 2.1 Evidence supporting existence

- **[PB]** Section 4.1 lists "Continuous device-level discovery of every AI tool, browser extension, developer assistant, and local model — including unsanctioned tools" as a current observability proof point. The description is specific and consistent with what an endpoint agent could technically accomplish.
- **[CAP]** `capability-status.md` explicitly lists Ethana Edge as "Beta. Endpoint agent (Mac, Linux, Windows), browser extension, dev-tool config push for Cursor, Copilot, Claude Code." An endpoint agent that pushes config to those tools would inherently generate an inventory of what is installed. Discovery is a byproduct of the endpoint agent's operation.
- **[CLM]** Lists "Device-Level AI Discovery & Inventory" as Beta (not Unverified). The approved customer-facing claim is "Instantly build a comprehensive inventory of all AI tools, browser extensions, developer assistants, and local models active across the organization." This is an actual approved claim, not a withheld one.
- **[REC]** States "Direct user observation confirms discovery capability is working."
- **[SOT]** Assigns "Beta (GA claim uncorroborated)" — notably NOT "Unverified." Beta implies something exists.

### 2.2 Evidence supporting Production status

- **[PB]** The playbook explicitly marks Discovery as "Current capability (GA)" within the Edge observability proof points.
- **[PB]** The sales play (Section 6.1) says "Show the inventory within 30 minutes of install." This is a specific, timed demo claim that implies the product team has done this.
- **[PB]** The playbook accurately labels blocking, PII redaction, and website egress as roadmap — demonstrating that the authors are capable of distinguishing current from future capabilities. This internal consistency increases the credibility of the current claims.
- **[REC]** User observation confirms it works.

### 2.3 Evidence supporting Beta or lower status

- **[CAP]** Critically distinguishes two forms of discovery:
  - Endpoint agent-based discovery: listed under **Beta** (Ethana Edge)
  - Connector-based Shadow AI inventory (IdP, SaaS, code repos): listed under **Roadmap** — "Connector layer in build. Seven connector families planned."
  - This means the playbook's "discovery" claim is partially supported (endpoint agent = Beta) and partially not (connector layer = Roadmap). The playbook does not make this distinction.
- **[SOT]** References [BB] (board briefing): "Board briefing lists it as In Build" — the board briefing apparently places device-level discovery below even Beta status.
- **[CLM]** Selling rule: "Position as Beta. Pitch only as a controlled proof-of-concept. State that automated out-of-band SaaS/IdP discovery is currently In Build."
- **[SOT]** Notes "GA claim uncorroborated" even while assigning Beta status.

### 2.4 Missing evidence

- No named deployment where Discovery was used at institutional scale
- No count of AI tools inventoried in a real production environment
- Connector-based discovery (IdP, SaaS) has no engineering completion timeline
- Unclear whether "30 minutes to inventory" applies to a single device or an enterprise fleet
- [BB] (board briefing) classifies discovery lower than the playbook — the reason for the discrepancy is not explained

### 2.5 Confidence score

**42 / 100 — Discovery operates at Production/GA status**

The endpoint agent-based discovery is supported across multiple sources as operational in a Beta state. The specific demo claim in the playbook ("inventory within 30 minutes") combined with the approved Beta claim in [CLM] suggests a working product. However, three issues prevent a higher score: (1) the board briefing places it below Beta; (2) the more useful connector-based discovery is Roadmap; (3) "controlled demo" and "institutional scale" are different operational contexts.

**Adjudication:** Device-level discovery via endpoint agent most likely exists and works. The correct status is **Beta** — operational in controlled environments, not verified at institutional scale. The playbook's GA label overstates this. The full Shadow AI inventory vision (connector-based) remains Roadmap.

---

## 3. Ethana Edge (Observability)

### 3.1 Evidence supporting existence

- **[CAP]** Edge is explicitly listed as a product in the Beta-flagged tier: "Endpoint agent (Mac, Linux, Windows), browser extension, dev-tool config push for Cursor, Copilot, Claude Code." This is the most specific engineering-grounded confirmation — three operating systems, a browser extension, and specific developer tools are named.
- **[CLM]** All Edge capabilities have approved customer claims with specific wording — not blanket "do not claim" entries. Beta-status claims are approved for use in the right context.
- **[PB]** Provides detailed observability proof points with specific tool names (ChatGPT, Claude, Gemini, Cursor, GitHub Copilot, Claude Code, Windsurf, Cline, Aider, VS Code AI extensions).
- **[SOT]** Assigns Beta status throughout, not Unverified — implying engineering has confirmed something exists.
- **[REC]** User observation of discovery corroborates endpoint agent viability.

### 3.2 Evidence supporting Production status

- **[PB]** Explicitly states "Current capability (GA): Observability. Edge currently delivers full AI visibility and audit capabilities." The playbook further specifies what is NOT GA (blocking, PII redaction, egress controls) — demonstrating the product team's awareness of the GA/Roadmap distinction. This internal consistency is a credibility signal.
- **[PB]** Section 5.2 (objection handling) describes Edge as the immediate answer to "We already have Zscaler/DLP" — framing it as deployable today with immediate AI inventory results.
- **[PB]** Sales Play 6.1 specifically states "Deploy the endpoint agent, and you get an immediate inventory of what is already running." Time-specific demo claims (30 minutes) suggest the product team has demonstrated this.
- **[PB]** The playbook was authored in June 2026 by the product team. If they were aware the engineering sources place Edge as Beta, they had the option to label it Beta. The explicit "GA" label alongside explicit "roadmap" labels for other features is a deliberate positioning choice.

### 3.3 Evidence supporting Beta or lower status

- **[CAP]** "Beta. Confirmed in controlled demo only, not at institutional scale. Never lead with this in BFSI, insurance, healthcare, or government." This is the clearest statement of gap between demo and production.
- **[SOT]** References [BB] (board briefing): Edge "listed as In Build" — below even Beta.
- **[SOT]** Warning block: "While the Marketing Playbook claims Ethana Edge is General Availability (GA), all engineering and board documents list it as Beta or In Build. Do not pitch Ethana Edge as a Production-ready GA product in regulated accounts."
- **[CLM]** All Edge capabilities have the selling rule "Position as Beta." Per-user attribution specifically says "Do not claim as GA."
- **[CAP]** Notes edge "Requires HR and employment-law sign-off (endpoint and browser monitoring)" — a procurement dependency that a GA product would typically have documented process for.

### 3.4 Missing evidence

- No reference deployment at institutional scale (500+ devices in a regulated environment)
- No load testing data or fleet-scale performance benchmark
- Difference between [CAP]'s Beta and [BB]'s In Build is unexplained — which is more recent?
- No version history or changelog for the endpoint agent
- The HR/employment-law sign-off process is not documented anywhere in the repository
- No mention of crash rates, bug count, or support SLA for a Beta product

### 3.5 Confidence score

**45 / 100 — Edge observability operates at Production/GA status**

Edge scores higher than Workspace or Visual Agent Builder because multiple repository sources confirm it exists in an operational state (Beta-flagged with named OS support and developer tools). The playbook's specific, time-bounded demo claims add credibility. However, the gap between "works in a controlled demo" and "Production/GA" is significant and acknowledged by [CAP] explicitly. Two engineering sources (CAP = Beta, BB = In Build) both fall short of GA.

**Adjudication:** Edge observability most likely exists and works in controlled settings. The correct status is **Beta** — the product is real, deployable, and functional for discovery and monitoring on individual devices or small controlled groups. It is not verified for institutional-scale rollout. The playbook's GA label is an acceleration of the true status by one tier. For non-regulated, non-BFSI accounts open to Beta products, this distinction may not materially affect deployment. For regulated accounts, it matters significantly.

---

## 4. Visual Agent Builder

### 4.1 Evidence supporting existence

- **[PB]** Provides a detailed, specific description: "drag-and-drop DAG workflow design with agents, APIs, functions, conditions, routers, loops, parallel execution, evaluators, guardrails, and human-in-the-loop steps." The granularity of this description (specific node types: conditions, routers, loops, parallel execution) suggests someone wrote it with an actual product in mind.
- **[PB]** Listed under Ethana Build Section 4.3 alongside capabilities that are verifiably Production (Gateway, Guardrails, MCP Broker, Red Teaming). Its placement in the same section with no status distinction suggests the product team treats it as equivalent.
- **[REC]** Elevates to Production (GA), stating it is "verified as part of the infrastructure suite" — though the source of this verification is not cited.

### 4.2 Evidence supporting Production status

- **[PB]** No status caveat applied. Product team treats it as current.
- **[PB]** Section 6.3 (AI Infrastructure Play) mentions "agent builder" in the demo focus: "PromptOps workflow, multi-model gateway, evaluation pipeline, agent builder." If the sales motion includes demoing the agent builder, the product team believes it can be shown.
- **[REC]** Elevated to Production (GA).

### 4.3 Evidence supporting Beta or lower (Unverified)

- **[CLM]** Most explicit counter-evidence: "No codebase or engineering documentation exists to support the presence of a visual builder." This is a specific, falsifiable factual claim — not just a status assignment. If this is accurate, the Visual Agent Builder does not exist as an implemented product.
- **[CAP]** Visual Agent Builder is entirely absent from `capability-status.md` — not listed in Production, In Build, Beta, or Roadmap. This absence is conspicuous given that the file lists even Roadmap items like AI Firewall and Shadow AI Connectors.
- **[SOT]** Lists it as "Unverified – Product Validation Required. Supported only by Marketing Playbook; uncorroborated in product docs/board briefings." The board briefing ([BB]) apparently does not mention the Visual Agent Builder.
- **[CMP]** States: "The Visual Agent Builder (DAG Builder) is Unverified in the codebase. Do not claim visual workflow capabilities exist. Developers must write agent logic in code and route tool calls through Ethana's MCP Broker."
- **[REC]**'s "verified as part of the infrastructure suite" claim cites no source and may be the reconciliation author's interpretation of the playbook — making it circular evidence.
- The Build section's Production capabilities (Gateway, Guardrails, Audit Logs, MCP Broker, Red Teaming) are each corroborated by [CAP], [SOT], and [BB]. Visual Agent Builder has none of that corroboration.

### 4.4 Missing evidence

- No API documentation for the DAG builder
- No demo recording or screenshot
- No codebase reference — [CLM] explicitly states no codebase documentation exists
- No technical architecture description (what engine runs the DAG?)
- [BB] (board briefing) does not mention it
- Not present in capability-status.md in any tier

### 4.5 Confidence score

**12 / 100 — Visual Agent Builder operates at Production/GA status**

The playbook is the sole source for this capability's existence. Two independent files ([CLM] and [CMP]) make explicit, specific assertions that there is no engineering or codebase documentation for it. [CAP] and [BB] omit it entirely. The [REC] elevation to GA is based on the playbook plus an uncited "verified as part of the infrastructure suite" claim. The playbook's specificity about node types (conditions, routers, loops) is real evidence that someone designed this, but design is not implementation.

**Adjudication:** The Visual Agent Builder is most likely a designed product concept — the feature list reflects real product planning — but without any engineering corroboration, it cannot be treated as Production or even Beta. Most likely state: **Roadmap/pre-Beta** — a designed and potentially partially implemented feature that has not reached a testable, demonstrable state. The lowest-confidence item in this review.

---

## 5. ISO 27001

### 5.1 Evidence supporting certification (Certified status)

- **[PB]** Footer on the final page: "ethana.ai · ISO 27001 Certified · NVIDIA Inception Program." This is the end of a sales playbook — a document used in customer conversations. Placing a false credential in a customer-facing document is a material misrepresentation with legal consequences.
- **[PB]** Section 8.4 explicitly lists "ISO 27001 certified" as a footer credential for outbound emails: "Footer credentials: ISO 27001 certified, NVIDIA Inception Program, deployed with regulated customers today." This is a deliberate, repeated inclusion — not an accidental footer.
- **[REC]** Argues: "Marketing Playbook (June 2026) lists ISO 27001 Certified as a footer credential, indicating certification was obtained since the previous engineering report." This is a plausible interpretation — the playbook may be more recent than the engineering status files.
- The other two footer credentials — "NVIDIA Inception Program" and "deployed with regulated customers today" — are independently plausible (NVIDIA Inception is a well-known startup programme with a public application process; having some regulated customers is consistent with being an active commercial product). The credibility of the other two credentials adds marginal support to the ISO 27001 claim.

### 5.2 Evidence supporting Beta / In Progress / Unverified status

- **[CAP]** "Compliance certifications: In progress, not complete: SOC 2 Type II, ISO 27001, HIPAA-ready. Hard procurement blockers for financial services. Do not state as held." This is an explicit, specific instruction.
- **[DEP]** "ISO 27001 | In progress / unverified | Frequently mandated for vendor information-security assurance." Also states: "Do not list any of these as obtained." This file is designed specifically to track certification status as a procurement-relevant fact.
- **[SOT]** "Marketing Playbook claims certified; contradicted by Capability status file and Product documentation which state 'In progress / unverified'." Names the contradiction explicitly.
- **[SOT]** Lists ISO 27001 as "Unverified – Product Validation Required" with evidence sources being the playbook (for the Certified claim) vs. [CAP] and [DEP] (for the In Progress claim).
- No certificate number appears anywhere in the repository. ISO 27001 certificates have: registration number, audit scope, registrar name, certification body (e.g., BSI, Bureau Veritas, TÜV), issue date, and expiry date. None of these appear in any file.
- A company that had obtained ISO 27001 certification would typically have this information readily available and would cite it in at least one product or security document.

### 5.3 Missing evidence

- No certificate registration number
- No audit scope (what processes / locations are covered)
- No certification body / registrar name
- No issue date or expiry date
- No mention of ISO 27001 in `deployment-and-certifications.md` as Certified (that file specifically tracks certifications and lists it as In Progress)
- No external link to a registrar's certificate database (standard for verifying ISO 27001 status)
- NVIDIA Inception Programme is the type of membership that is confirmed by a public database — ISO 27001 is similar

### 5.4 Reconciliation logic assessment

[REC] argues the playbook footer indicates certification was obtained after the engineering reports were written. This requires:
1. The engineering reports to pre-date the playbook — plausible but unconfirmed
2. The product team to have updated the playbook footer upon certification completion — possible
3. The playbook to be the only document updated (not `deployment-and-certifications.md`, not `capability-status.md`) — implausible. A certification completion would normally update the dedicated certifications file first.

The most parsimonious explanation for ISO 27001 appearing only in the playbook footer is that it was included prematurely — either as aspirational positioning or as an error — and was not caught before the playbook was finalised. The fact that `deployment-and-certifications.md` (the file most designed to track this) still says "In progress / unverified" is the strongest single counter-signal.

### 5.5 Confidence score

**22 / 100 — ISO 27001 Certified status is accurate**

Two purpose-built repository files ([CAP] and [DEP]) explicitly say In Progress and explicitly prohibit claiming it as held. No certificate details appear anywhere. The playbook's footer inclusion, while not dispositive, is outweighed by the specificity of the counter-evidence and the total absence of any certificate artifact. The [REC] reconciliation logic requires an implausible update sequence (playbook updated, dedicated certification file not updated).

**Adjudication:** ISO 27001 is most likely **In Progress**. The playbook footer reflects either a premature inclusion or an optimistic projection. It should not be cited in customer-facing materials until a certificate number and registrar can be named. The risk of claiming Certified status without a certificate is high — a single procurement due-diligence request for the certificate number would immediately expose the gap.

---

## Summary Table

| Capability | Most Likely True Status | Playbook Claim | Repository Consensus | Confidence (GA/Production) | Key missing evidence |
|---|---|---|---|---|---|
| **Workspace** | Pre-GA / In Development | GA (no caveats) | Unverified (not in board briefings) | **18 / 100** | Engineering documentation, codebase reference, board briefing mention |
| **Discovery (device-level)** | Beta (endpoint agent) / Roadmap (connectors) | GA | Beta (endpoint) / Roadmap (connectors) | **42 / 100** | Institutional-scale deployment reference; connector timeline |
| **Edge (observability)** | Beta | GA | Beta (CAP) / In Build (BB) | **45 / 100** | Scale evidence; employment-law process documentation |
| **Visual Agent Builder** | Roadmap / Pre-Beta | GA | Unverified (explicit "no codebase docs") | **12 / 100** | Any codebase reference, demo recording, API documentation |
| **ISO 27001** | In Progress | Certified | In Progress / Unverified (DEP, CAP) | **22 / 100** | Certificate number, registrar name, audit scope, expiry date |

---

## Cross-Cutting Observations

### Observation 1: The playbook has meaningful internal consistency

The playbook accurately labels blocking, PII redaction, source code masking, and website egress controls as Roadmap for Edge. It accurately describes NHI as absent from the MCP section (it does not claim NHI). This pattern of honest roadmap labeling within the same document that claims GA for observability capabilities suggests the product team is applying judgment, not simply marking everything as GA. This raises the credibility of the current claims slightly above what a pure marketing document would warrant.

### Observation 2: Repository files are not a monolith

The repository contains internal contradictions:
- `capability-status.md` says Edge is Beta; [BB] (board briefing) says In Build. These are different status tiers.
- `capability-status.md` says Discovery is Roadmap (connector layer); `claims-matrix.md` says device-level discovery is Beta. These are consistent only if you correctly distinguish connector-based from endpoint-based discovery — a distinction the playbook does not make.
- `ethana-status-reconciliation.md` elevates multiple capabilities to GA, while four other files disagree.

Repository files should not be treated as a unified engineering verdict. Where they converge on a status, that convergence is significant. Where they diverge, the specific evidence type cited in each file matters.

### Observation 3: The board briefing is the highest-weight counter-source

[SOT] repeatedly cites `Study ethana.txt` (board briefing) as engineering corroboration. For Production capabilities (Gateway, Guardrails, Audit Logs, MCP, Red Teaming), the board briefing is cited alongside capability-status.md. For disputed capabilities (Edge, Discovery, Workspace, Visual Agent Builder), the board briefing either places them lower than the playbook or does not mention them. A board briefing is prepared for governance, not marketing — it has strong incentives to be accurate. Its divergence from the playbook on these five items is significant.

### Observation 4: The absence pattern is telling

For four capabilities — Visual Agent Builder, Workspace, Discovery (connector layer), and ISO 27001 as Certified — the evidence gap is not just "repository says something different." The evidence gap is the complete absence of technical detail: no version numbers, no API schemas, no certificate numbers, no load test results. Production capabilities in a software company generate documentation artifacts. Their absence is evidence of a status gap, not just a documentation gap.

### Observation 5: Two distinct questions are in play

**Does this capability exist in some form?** Evidence suggests: Workspace = probably yes, in development. Edge/Discovery = yes, in Beta. Visual Agent Builder = possibly designed but not implemented. ISO 27001 = certification in progress.

**Is this capability Production-ready for enterprise deployment today?** Evidence suggests: Workspace = no. Discovery (endpoint) = Beta, not Production. Edge (observability) = Beta, not Production. Visual Agent Builder = no. ISO 27001 = not yet certified.

These two questions have different answers. The confidence scores reflect the second, more demanding question.

---

## What Would Move These Scores

| Capability | Evidence needed to reach 70+ confidence in GA/Production |
|---|---|
| Workspace | Engineering sign-off document; codebase reference; one named pilot customer; appearance in board briefing |
| Discovery | Two reference deployments at 100+ devices; connector-layer ETA; resolution of CAP vs. BB status discrepancy |
| Edge | One institutional-scale deployment (500+ devices, regulated environment); HR sign-off process documented; engineering update confirming Beta → GA transition |
| Visual Agent Builder | Any codebase reference; one demo recording with working DAG execution; claims-matrix.md retraction of "no codebase documentation" statement |
| ISO 27001 | Certificate registration number; certifying body name; audit scope; expiry date |
