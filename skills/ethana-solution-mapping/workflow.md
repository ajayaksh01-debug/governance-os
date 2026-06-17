# Ethana Solution Mapping — Workflow

This document describes the phase-by-phase execution of the Ethana Solution Mapping skill, including decision trees, quality gates, time estimates, and the output document template.

---

## Workflow Overview

| Phase | Name | Duration | Description |
|---|---|---|---|
| 1 | Intake & Requirement Extraction | 10–15 min | Parse inputs; extract discrete requirements; determine mode and sector |
| 2 | Sector Gating | 5 min | Apply sector-specific blockers before capability matching |
| 3 | Capability Matching & Status Gating | 15–30 min | Look up each requirement in canonical-product-model.md; route to output section |
| 4 | Coverage Confidence Scoring | 10–15 min | Assign CCS per requirement; compute aggregate profile |
| 5 | Competitive Positioning | 10–15 min | Identify likely alternatives; apply claims firewall; build comparison table |
| 6 | Commercial Motion Design | 10 min | Select motion type; define phasing, guardrails, and success criteria |
| 7 | Output Assembly & Quality Check | 15–20 min | Compile all ten sections; run pre-release checklist; score against evaluation rubric |

Total: 75–110 minutes for a full-depth analysis

Condensed (single capability question): Phases 1, 2, 3, 4 only — 25–35 minutes

---

## Phase 1: Intake & Requirement Extraction

**Objective:** Convert raw inputs into a list of discrete, mappable requirements. Establish execution context.

### 1.1 Parse Inputs

Read all provided inputs:
- If `upstream_skill_output` is provided, extract requirements from Section 6 (regulatory-mapping) or Section 9 (ai-incident-analysis) directly — these are already structured
- If `requirement_list` is provided, parse into individual requirements
- If `customer_use_case` is provided, derive implied requirements from the use case description
- If `capability_question` is provided, treat each question as a single requirement

### 1.2 Establish Execution Context

Record the following for the session:
- `output_mode`: Formal Proposal / RFP Response / Discovery Conversation (default to Discovery Conversation if not provided)
- `customer_sector`: BFSI / Healthcare / Government / General Enterprise (default to General Enterprise if not provided)
- `jurisdictions`: list of applicable jurisdictions (affects Section 3 language caveats)
- `deployment_constraint`: Cloud / VPC / On-prem / Air-gapped (affects on-prem caveat trigger)
- `existing_subscription`: None / Build / Edge / Bundle (affects Section 3 — do not re-sell owned capabilities)

### 1.3 Requirement Type Classification (Decision Tree DT1)

Apply to each extracted requirement:

```
Is this a specific regulatory control requirement (from RBI, FCA, EU AI Act, etc.)?
  YES → Tag as REGULATORY CONTROL. Reference framework crosswalk in Phase 3.
  NO → Is this a governance capability request ("we need X in our AI platform")?
    YES → Tag as CAPABILITY REQUEST. Go directly to capability matching in Phase 3.
    NO → Is this a sector-specific use case question (e.g., "we need MRM-compliant audit trail")?
      YES → Tag as SECTOR USE CASE. Apply DT2 (sector gating) in Phase 2.
      NO → Tag as GENERAL. Map use case to implied controls, then proceed to Phase 3.
```

### 1.4 Intake Output

A numbered list of discrete requirements with:
- Requirement ID (R1, R2, R3...)
- Requirement statement in plain language
- Requirement type (Regulatory Control / Capability Request / Sector Use Case / General)
- Jurisdiction if applicable

Minimum: one requirement. Maximum depth is proportional to input complexity.

---

## Phase 2: Sector Gating

**Objective:** Apply sector-specific blockers and constraints before capability matching. Prevents certifications or sector-incompatible proposals from reaching the output.

### 2.1 Sector Gating Decision Tree (DT2)

```
BFSI sector:
  → SOC 2 Type II: Not certified (In Build). This is a procurement gate for most enterprise BFSI.
    Flag as SOC 2 BLOCKER. This will force Advisory-First motion in Phase 6.
  → ISO 27001: Certification in progress. Cannot claim certified status.
    Flag as ISO 27001 BLOCKED.
  → On-prem deployment requested?
    YES → Deployment model supported. Mandatory note: "Ethana on-prem is single-node, unvalidated at Tier 1 bank scale."
  → Does the customer require HIPAA-ready infrastructure?
    YES → HIPAA-ready is In Build. Flag as HIPAA BLOCKED. Cursory bridge: VPC deployment + advisory.
  → NEVER lead with Edge or Workspace capabilities in BFSI proposals.
  → MRM (Model Risk Management) requirement?
    YES → Map to: Build Gateway (multi-model routing, audit) + Immutable Audit Log. Both Production.

HEALTHCARE sector:
  → HIPAA: In Build. Cannot claim compliant. Bridge: VPC deployment + advisory.
  → PHI data: DO NOT propose cloud deployment unless customer explicitly accepts shared-cloud PHI handling.

GOVERNMENT / PUBLIC SECTOR:
  → Air-gapped deployment requested?
    YES → Deployment model supported. Mandatory note on single-node scale limitation.
  → FedRAMP / IL4 / IL5 equivalent: Not available. Do not claim.

GENERAL ENTERPRISE (non-regulated):
  → Standard capability mapping. No automatic certification blockers.
  → Edge may be mentioned as In Build roadmap item without the BFSI restrictions.
  → Workspace: still Aspirational. Still prohibited regardless of sector.
```

### 2.2 Sector Gating Output

A brief sector assessment with:
- Sector confirmed
- Hard blockers identified (e.g., "SOC 2: BLOCKED")
- Soft cautions identified (e.g., "ISO 27001 cannot be claimed")
- Deployment model constraints (if on-prem or air-gapped, mandatory caveat text)
- Motion constraint if triggered (SOC 2 blocker → Advisory-First)

---

## Phase 3: Capability Matching & Status Gating

**Objective:** For each requirement, look up the Ethana capability in canonical-product-model.md, determine status, and route to the correct output section.

**Primary source:** `knowledge/ethana/canonical-product-model.md` only. No other source.

### 3.1 Capability Lookup Protocol

For each requirement from Phase 1:
1. Identify the relevant Ethana capability or capabilities from canonical-product-model.md
2. Confirm the capability's status (Production / In Build / Aspirational / Not in model)
3. Apply the Claims Firewall (DT3 below)
4. Record the matched capability, status, and output routing

### 3.2 Claims Firewall Decision Tree (DT3)

```
Look up capability in canonical-product-model.md:

  STATUS = Production:
    → Route to Section 3 (Proposal-Safe Capabilities)
    → Include any mandatory caveats from canonical-product-model.md
    → Proceed to Phase 4 (assign CCS)
    → After Phase 4: if CCS scores None (0–24), do NOT include as a primary coverage item in Section 3.
      Instead: add a supplemental mention with an explicit scope caveat stating what the capability does NOT do.
      Also route to Section 7 (Gap Register) for the unaddressed portion of the requirement.
      Never allow a CCS 0–24 item to appear in Section 3 without an explicit non-coverage caveat directly below it.

  STATUS = In Build:
    → Route to Section 4 (Roadmap Disclosure) for conversational mention
    → Route to Section 6 (Cursory Bridge) for today's alternative
    → DO NOT include in Section 3 (Proposal-Safe Capabilities)
    → In Formal Proposal or RFP Response: must not appear as a deliverable
    → CCS = 0 (current). Annotate anticipated CCS when shipped.

  STATUS = Aspirational:
    → Route to Section 5 (Prohibited Claims Register)
    → DO NOT mention in any proposal, RFP, or discovery output
    → Route to Section 7 (Gap Register) for gap documentation
    → Route to Section 8 (Competitive Positioning) if the customer has asked about this capability
      → Frame as customer-built or Cursory advisory, not as an Ethana roadmap item

  STATUS = Not in canonical model:
    → Route to Section 7 (Gap Register)
    → Route to Section 6 (Cursory Bridge) if a Cursory service addresses the need
    → Route to specialist referral if neither Ethana nor Cursory covers it

HARD DISQUALIFIER CHECK (run after routing):
  Is any Aspirational capability appearing in Section 3? → STOP. Remove. Disqualification if released.
  Is any In Build capability framed as a proposal deliverable in Section 3? → STOP. Remove. Disqualification if released.
```

### 3.3 Key Capability Mapping Reference

The following are the most common requirement-to-capability mappings. All statuses are from canonical-product-model.md.

**PRODUCTION (claimable):**
- LLM call routing, fallback, multi-model → LLM Gateway (Production; ~50ms overhead caveat)
- Prompt injection detection → Runtime Guardrails: Prompt Injection Scanner (Production; sub-200ms p95)
- PII detection and redaction → Runtime Guardrails: PII Scanner (Production; API-layer only caveat)
- Jailbreak and toxicity detection → Runtime Guardrails: Jailbreak + Toxicity Scanners (Production)
- Secrets and credentials in LLM output → Runtime Guardrails: Secret Leakage Scanner (Production)
- Hallucination grounding → Runtime Guardrails: Hallucination Grounding (Production)
- Immutable AI audit trail → Immutable Audit Log (Production; strongest enterprise claim)
- SIEM export of AI events → Immutable Audit Log (Production; Splunk, Elastic, Datadog)
- MCP tool call tracing → MCP Security Broker: per-call tracing (Production; NHI for agents: In Build)
- Red teaming of AI applications → Red Teaming Orchestrator: 21 OWASP probes, multi-turn (Production; CI/CD gate: In Build)
- Multi-tenant enterprise deployment → Account Management: RBAC, SSO/OIDC, tenant isolation (Production; SCIM: In Build)
- AI cost tracking by project/tenant → Cost & Budget Tracking (Production; per-user granularity: In Build)
- On-prem or VPC deployment → Deployment Models (Production; mandatory scale caveat for on-prem)

**IN BUILD (roadmap mention only):**
- Shadow AI discovery, SaaS connector inventory → Ethana Discovery (In Build; IdP connector first)
- Endpoint AI monitoring, browser extension → Ethana Edge (In Build)
- Non-human identity (NHI) for agents → NHI module (In Build)
- CI/CD red teaming gate → Red Teaming CI/CD integration (In Build)
- OPA/Rego policy engine → Governance Policy Engine (In Build)
- SOC 2 Type II, ISO 27001, HIPAA-ready → Certifications (all In Build / In Progress)
- SCIM automated provisioning → SCIM (In Build)

**ASPIRATIONAL (do not mention):**
- Enterprise chat interface → Workspace (Aspirational)
- RAG on internal documents → Workspace (Aspirational)
- Department AI copilots → Workspace (Aspirational)
- Visual agent builder / DAG builder → Visual Agent Builder (Aspirational)
- "Governed enterprise chat" of any kind → Workspace (Aspirational)

---

## Phase 4: Coverage Confidence Scoring

**Objective:** Score each Production-matched requirement on how fully the capability addresses it. Compute an aggregate coverage profile.

### 4.1 Scoring Method

For each requirement routed to Section 3 (Production), assign a Coverage Confidence Score (CCS) from 0–100:

| Score | Band | Decision criteria |
|---|---|---|
| 90–100 | Full | Capability directly addresses the requirement in its current production state. Stated caveats are minor. |
| 70–89 | High | Capability substantially addresses the requirement. One or two known caveats reduce completeness (e.g., API-layer PII for a DPDP Act requirement; endpoint PII not covered). |
| 50–69 | Partial | Capability addresses the core of the requirement but leaves a meaningful gap. A second capability or Cursory service is needed to complete coverage. |
| 25–49 | Thin | Capability is tangentially related to the requirement. The gap is larger than the coverage. Cursory bridge should lead. |
| 0–24 | None | No Production capability materially addresses this requirement. Assign to Section 7 (Gap) or Section 6 (Bridge). |

For In Build requirements: CCS = 0 (current). Note anticipated CCS when shipped in the Coverage Map row.

### 4.2 CCS Calibration Examples

Use these anchors for consistent scoring:

| Requirement | Capability | CCS | Rationale |
|---|---|---|---|
| Immutable AI decision trail for RBI MRM | Immutable Audit Log | 88 | Production, insert-only, SIEM export. Minor caveat: RBI schema customisation may be needed. |
| DPDP Act data minimisation for API-layer LLM calls | Guardrails PII Scanner | 80 | Production bidirectional PII masking on API calls. Caveat: browser/endpoint PII not covered (Edge In Build). |
| Prompt injection prevention for internal LLM apps | Guardrails Prompt Injection | 92 | Production, bidirectional, sub-200ms. Near-complete match. |
| Jailbreak protection for deployed LLM | Guardrails Jailbreak Scanner | 90 | Production. Full match. |
| Formal credit model bias audit (RBI Fair Practices) | Guardrails Bias Scanner | 18 | Runtime text filter; not a statistical model audit. Does not satisfy formal bias testing obligation. |
| Shadow AI employee inventory | Discovery (In Build) | 0 | In Build. Anticipated CCS when shipped: 65. |
| Agent NHI provisioning and tracing | MCP Broker + NHI (split) | 42 | MCP core Production; NHI In Build. Core tracing covered; identity lifecycle not addressed today. |
| Automated red teaming in CI/CD pipeline | Red Teaming Orchestrator | 72 | 21 OWASP probes Production. CI/CD gate integration In Build. Core orchestrator addresses the requirement; automation into pipeline deferred. |
| SOC 2 Type II vendor attestation | Certification: In Build | 0 | In Build. Cannot claim. |
| Enterprise chat for employees | Workspace | 0 | Aspirational. Prohibited. |

### 4.3 Aggregate Coverage Profile

After scoring all requirements:

1. **Calculate average CCS:** Sum all CCS values from Section 1 (including every 0 for In Build, Aspirational, and procurement blockers such as SOC 2) and divide by the total requirement count. Do not exclude blockers — they represent real gaps. Verify the arithmetic before writing Section 2. Example: 10 requirements summing to 677 → average = 67.7, not 58 or 65.

2. **Calculate distribution:** Count how many requirements fall in each band. Use the exact band boundaries — 90–100 is Full, 70–89 is High. A CCS of 90 is Full, not High. Verify the band counts add up to the total requirement count before writing.

3. **Determine coverage characterisation** based on the verified average:
   - **Platform-Primary**: Average CCS ≥ 65 AND majority of requirements at High or Full
   - **Mixed**: Average CCS 40–64, significant production coverage alongside meaningful gaps
   - **Cursory-Primary**: Average CCS < 40, production coverage is supplemental to bridge
   - Note: a SOC 2 blocker does not change the characterisation — it changes the commercial motion. A Platform-Primary profile with a SOC 2 blocker is still Platform-Primary in coverage; Advisory-First in commercial motion.

4. **Flag SOC 2 blocker separately** from the characterisation. State it explicitly: "SOC 2 is a procurement blocker — this triggers Advisory-First motion regardless of coverage characterisation."

---

## Phase 5: Competitive Positioning

**Objective:** Identify the alternatives the customer is most likely evaluating for this requirement set. Produce an honest comparison for Section 8.

### 5.1 Competitor Identification

Identify the top two or three alternatives based on requirement set and sector:

| Requirement cluster | Likely alternatives |
|---|---|
| LLM gateway and observability | LangSmith (DataBricks), Langfuse, Portkey, Kong AI Gateway |
| Runtime guardrails and AI security | Aporia, Guardrails.ai, Lakera Guard, Prompt Security, CalypsoAI |
| Enterprise AI chat and RAG | Microsoft Copilot Studio, ChatGPT Enterprise, Glean, Notion AI |
| Shadow AI discovery and DLP | Metomic, Nightfall AI, Cyberhaven, Zscaler, Netskope |
| AI audit and compliance | Securiti AI, BigID (AI governance module), manual CISO processes |
| Agent security and MCP | No direct competitors established (Ethana first-mover in MCP security) |
| Red teaming automated | Garak, Promptfoo, HiddenLayer, Protect AI |

**Mandatory competitor coverage rules:**
- When any guardrails requirement is in the requirement set (PII, injection, jailbreak, toxicity, bias, secret leakage), Section 8 must include a comparison against at least one of: Aporia, Lakera Guard, Guardrails.ai. These are the most direct competitors to Ethana's Guardrails product. LangSmith does not substitute for a guardrails comparison — LangSmith is observability, not runtime security.
- When red teaming is in the requirement set, Section 8 must include a comparison against at least one of: Garak, HiddenLayer, Promptfoo.
- When both gateway and guardrails are in the requirement set (the common case), include one entry for the gateway-observability space (LangSmith or Langfuse) AND one for the guardrails space (Aporia or Lakera). Do not substitute one for the other.
- The competitor selection must reflect the actual requirement set, not a default set. A BFSI engagement with guardrails as the primary requirement should compare Ethana against Aporia, not just against LangSmith.

### 5.2 Competitive Framing Principle

Apply the claims firewall before any competitive comparison:
- Only Production Ethana capabilities may be compared
- If the customer requirement is satisfied by a competitor's Production capability and Ethana's equivalent is Aspirational → do not compete on that dimension. Redirect to an adjacent Production capability where Ethana wins.
- If the customer requirement is satisfied by a competitor's Production capability and Ethana's equivalent is In Build → disclose "Ethana is building this; today Cursory bridges the gap." Do not claim competitive equivalence.

### 5.3 Key Competitive Positions

**LLM Gateway — Ethana vs. Kong AI Gateway, Portkey, LangSmith:**
- Ethana differentiator: Compliance-native (immutable audit log embedded, not a bolt-on); governance-first not observability-first; India VPC and on-prem deployment; BFSI-targeted design
- Ethana gap: LangSmith/Langfuse have deeper developer workflow integration and richer observability UX; Kong has broader API management ecosystem
- Win condition: Compliance and audit requirements are primary; regulated industry; multi-model routing with security controls needed
- Loss condition: Developer productivity is the priority, not regulatory compliance; observability dashboard depth required

**Guardrails — Ethana vs. Aporia, Guardrails.ai, Lakera Guard:**
- Ethana differentiator: Six production scanners natively integrated with the gateway (single API call); bidirectional (request and response); sub-200ms p95; immutable log of every flagged call
- Ethana gap: Aporia/Lakera offer broader custom policy libraries and finer-tuning options; some competitors offer model evaluation beyond runtime
- Win condition: Runtime security integrated with audit trail; bidirectional controls; gateway-native approach
- Loss condition: Customer wants deep custom guardrail logic and fine-tuning their own classifiers

**Immutable Audit Log — Ethana vs. Splunk AI Security, Datadog AI Observability:**
- Ethana differentiator: Immutable by design (insert-only at the database layer, not policy-level WORM); AI-specific schema natively; not a SIEM bolt-on; purpose-built for regulatory evidence
- Ethana gap: Splunk/Datadog have vastly broader non-AI event coverage and established enterprise contracts; better SOC integration
- Win condition: Regulator-ready AI audit trail is the primary requirement; customer wants AI-first not SIEM-retrofitted
- Loss condition: Customer's SOC team runs on Splunk and wants AI governance there; primary need is correlation with non-AI security events

**Enterprise Chat and RAG — Ethana vs. Microsoft Copilot Studio, ChatGPT Enterprise, Glean:**
- Ethana honest position: Ethana has NO production enterprise chat. Workspace is Aspirational. Do not compete on this dimension.
- Redirect position (claimable): Ethana Build Gateway governs ChatGPT Enterprise or Copilot Studio if the customer adopts one. Ethana is vendor-agnostic governance, not a competing chat product. Position as complementary.
- Win condition with redirect: Customer wants to govern multiple AI tools (not be locked into one vendor's chat); compliance evidence layer needed on top of whatever chat they choose
- Loss condition: Customer wants a single turnkey chat product with no custom integration

**Shadow AI Discovery — Ethana vs. Metomic, Nightfall, Zscaler, Netskope:**
- Ethana honest position: Ethana Discovery is In Build. Cannot compete today on feature-for-feature discovery.
- Redirect position (claimable): Ethana Build Gateway captures all LLM API calls for sanctioned AI. Cursory AI Inventory service provides the human-led discovery layer for unsanctioned AI.
- Bridge positioning: Position Ethana Gateway as the governance layer that activates once discovery is complete (whether by Ethana Discovery when shipped or a SWG partner)
- Win condition with redirect: Customer needs both discovery and governance; Ethana solves the governance side today; design partner relationship for Discovery
- Loss condition: Customer needs production discovery now and is buying a single point solution

**Red Teaming — Ethana vs. Garak, Promptfoo, HiddenLayer:**
- Ethana differentiator: 21 OWASP LLM Top 10 probes orchestrated; multi-turn attacks; targets model/app/agent layer; integrated with production guardrails loop
- Ethana gap: Garak/Promptfoo are open-source with active community probe libraries; HiddenLayer offers broader model security (weights, supply chain)
- Win condition: Enterprise-managed red teaming with audit log; orchestrated vs. DIY; OWASP alignment required
- Loss condition: Customer has in-house security team that prefers OSS tooling; or model supply chain security (weights, MLOps) is the primary concern

---

## Phase 6: Commercial Motion Design

**Objective:** Select the appropriate commercial motion and define the deal structure.

### 6.1 Motion Selection Decision Tree

```
Has Phase 2 flagged a SOC 2 BLOCKER for a BFSI customer?
  YES → Advisory-First (regardless of CCS average)

Is the average CCS from Phase 4 below 25?
  YES → Are there ANY Production capabilities with High or Full CCS?
    NO → No Commercial Motion recommended. Document gaps. Revisit in 6 months.
    YES → Advisory-First (Production capabilities form a slim entry only with advisory-heavy engagement)

Are Aspirational capabilities (Workspace, Visual Agent Builder) the primary requirements?
  YES → Average CCS < 40 for the Aspirational items?
    YES → Advisory-Only. No platform proposal. Cursory advisory only.

Average CCS ≥ 65 AND no SOC 2 blocker?
  YES → Platform-First. Lead with Build capabilities.

Average CCS 40–64 AND some Production match AND significant In Build gap?
  YES → Land-and-Expand. Enter with Production capabilities now; plan In Build handoff.

Customer has explicitly expressed interest in shaping the roadmap / design partnership language?
  YES → Design Partner. Requires explicit In Build status disclosure and Ethana product team alignment.

Default: Land-and-Expand for mixed profiles.
```

### 6.2 Motion Templates

**Advisory-First:**
- Entry: Cursory engagement (Regulatory Gap Analysis, AI Readiness Assessment, or Policy & Control Design — most relevant to this customer's requirements)
- Platform timeline: Deferred to (a) after SOC 2 obtained, (b) after key In Build capabilities ship, or (c) after the advisory creates the requirement specification the platform satisfies
- Phase 2: Build pilot in non-production or customer VPC once procurement gate is cleared
- Deal guardrails: No platform license in initial proposal; no claims for SOC 2, ISO 27001, or In Build capabilities

**Platform-First:**
- Entry: Ethana Build license (Gateway + Guardrails + Audit Log + Red Teaming as applicable to requirements)
- Cursory pairing: Implementation Service (deployment and configuration); Policy & Control Design (guardrail rule authoring)
- Phase 2: Edge when shipped (if discovery requirements exist)
- Deal guardrails: Do not include Workspace or Visual Agent Builder; do not reference SOC 2 as current

**Land-and-Expand:**
- Entry: Ethana Build (Production capabilities only) + Cursory advisory for gap
- Phase 2: Edge when shipped; Discovery when shipped
- Cursory pairing: AI Inventory & Classification (for shadow AI discovery gap); Red Teaming as a Service (for CI/CD gap)
- Success criteria: Build deployed, two Production capabilities in active use, joint roadmap session scheduled
- Deal guardrails: In Build items excluded from deliverables; Aspirational items absent from all documents

**Design Partner:**
- Entry: Design Partner Agreement with Ethana product team; Cursory advisory alongside
- Disclosure requirement: Customer must receive explicit written disclosure of In Build status for any capability they are co-shaping
- This motion requires Ethana product team alignment before commercial proposal is issued
- Deal guardrails: No delivery commitments on In Build timelines

---

## Phase 7: Output Assembly & Quality Check

**Objective:** Compile all ten sections, run the pre-release checklist, and verify the output meets the minimum quality threshold before release.

### 7.1 Section Assembly Order

Assemble sections in this order (even if some are empty):

1. Requirement Coverage Map — one row per requirement with CCS and disposition
2. Coverage Confidence Summary — aggregate profile, coverage characterisation, story
3. Proposal-Safe Platform Capabilities — exact quotable language per Production capability
4. Roadmap Disclosure — per In Build item with bridge service. Header label must match output_mode:
   - **Formal Proposal / RFP Response:** "Ethana Roadmap — Not In Scope of This Proposal. Include only in a clearly-labelled roadmap section. Do not include in scope-of-work, deliverables, or SLA sections. No delivery commitment may be made."
   - **Discovery Conversation:** "For conversational use only. Not for any written proposal deliverable."
5. Prohibited Claims Register — explicit list; must be present even if the output is clean
6. Cursory Bridge Recommendations — per gap, specific service named
7. Gap Register — unaddressable requirements with best alternative
8. Competitive Positioning — per relevant competitor with Ethana strength / gap / win / loss
9. Recommended Commercial Motion — full deal structure per motion template
10. Customer-Facing Executive Summary — 200–250 words, written last

### 7.2 Pre-Release Checklist

Run all checks before releasing any output. Do not release if any item fails.

**Claims Firewall:**
- [ ] No Aspirational capability appears in Section 3 (Proposal-Safe Capabilities)
- [ ] No In Build item appears as a proposal deliverable in Section 3
- [ ] "ISO 27001 certified," "SOC 2 certified," "HIPAA compliant" do not appear as positive claims anywhere in the output
- [ ] Workspace features (enterprise chat, RAG, department copilots) do not appear in Sections 3, 4, or 8 as Ethana capabilities
- [ ] Visual Agent Builder does not appear in Sections 3, 4, or 8 as an Ethana capability

**Canonical Model Accuracy:**
- [ ] Every capability status claim is sourced from canonical-product-model.md, not from the marketing playbook, claims-matrix.md, or source-of-truth.md
- [ ] Every mandatory caveat from canonical-product-model.md is reflected in the corresponding Section 3 entry
- [ ] The NHI (Non-Human Identity) caveat is present if MCP Security Broker is included
- [ ] The CI/CD gate caveat is present if Red Teaming is included
- [ ] The on-prem scale caveat is present if on-prem deployment is included

**Coverage Confidence:**
- [ ] Every requirement in Section 1 has a CCS score (0 for In Build/Aspirational, not blank)
- [ ] The aggregate CCS profile in Section 2 is consistent with the individual scores
- [ ] Calibration anchors (bias audit = ~18, Gateway = ~92) are used as a reference for scoring plausibility

**Completeness:**
- [ ] Every requirement from Phase 1 appears in Section 1
- [ ] Section 5 (Prohibited Claims) is present and explicitly lists all relevant prohibited items
- [ ] Section 9 (Commercial Motion) includes a motion type, entry product, and deal guardrails

**Language Mode:**
- [ ] Section 3 language register matches the `output_mode` (active-voice quotable for proposals; conversational for discovery)
- [ ] Section 4 items are in discovery/conversational language, not as formal commitments

### 7.3 Release Criteria

| Score | Decision |
|---|---|
| 85–100 | Exemplary. Release. |
| 70–84 | Acceptable. Release. |
| 55–69 | Preliminary. Acknowledge limitations in Section 2 or 10. Do not use for formal proposal. |
| < 55 | Do not release. Note specific deficiencies. |

Score against the evaluation.md rubric.

**Hard disqualifier (overrides score):** Any Aspirational capability appearing in Section 3, any In Build item framed as a deliverable, or any prohibited certification claim in the output → Automatic disqualification. Remove the offending content and re-run the checklist before release.

---

## Output Document Template

```markdown
# Ethana Solution Mapping
[Customer Name] | [Date] | [Output Mode] | [Sector] | [Jurisdictions]

---

## 1. Requirement Coverage Map

| # | Requirement | Matched Capability | Status | CCS | Disposition |
|---|---|---|---|---|---|
| R1 | [requirement] | [capability] | [status] | [0-100] | [routing] |

---

## 2. Coverage Confidence Summary

**Average CCS:** [X/100]
**Distribution:** Full (>90): X req | High (70-89): X req | Partial (50-69): X req | Thin (25-49): X req | None (<25): X req
**Coverage characterisation:** [Platform-Primary / Mixed / Cursory-Primary]
**Summary:** [2-3 sentence coverage story]

---

## 3. Proposal-Safe Platform Capabilities

### [Capability Name]
**Status:** Production
**Coverage Confidence:** [X/100] ([Band])
**Claim language:** "[Exact quotable text]"
**Mandatory caveats:** [list caveats from canonical-product-model.md]

---

## 4. Roadmap Disclosure

*For conversational use only. Not for formal proposal deliverables.*

### [Capability Name]
**Status:** In Build
**When shipped, will provide:** [description]
**Today, Cursory bridges this with:** [service name and description]
**Anticipated CCS when shipped:** [X/100]

---

## 5. Prohibited Claims Register

The following must not appear in any proposal, RFP response, or customer-facing document for this engagement:

- **[Capability/Certification]:** [Why it is prohibited]

---

## 6. Cursory Bridge Recommendations

### Gap: [Requirement description]
**Cursory service:** [Service name]
**Delivers:** [What the service provides for this specific gap]
**Positions alongside:** [Any platform component it complements]

---

## 7. Gap Register

| Requirement | Why it is a gap | Best available alternative |
|---|---|---|
| [R#] [requirement] | [No Ethana capability at any level] | [Specialist / customer-built / adjacent capability] |

---

## 8. Competitive Positioning

### vs. [Competitor Name]
**Ethana differentiated strength:** [Production capability and why it wins]
**Ethana honest gap:** [Where competitor has production capability Ethana lacks]
**Win condition:** [Customer profile and context where Ethana wins]
**Loss condition:** [Honest context where competitor wins]

---

## 9. Recommended Commercial Motion

**Motion type:** [Platform-First / Advisory-First / Land-and-Expand / Design Partner]
**Entry product:** [Ethana product(s) and Cursory service(s)]
**Phase 1 scope:** [What is in the initial proposal]
**Phase 2 scope:** [What follows — timing tied to In Build ship date or advisory completion]
**Deal guardrails:** [What must NOT be in this proposal]
**Success criteria:** [What a successful first engagement looks like]
**Expansion path:** [How the deal grows]

---

## 10. Customer-Facing Executive Summary

[200-250 words: Production capabilities → Cursory bridge → roadmap → next step]
```
