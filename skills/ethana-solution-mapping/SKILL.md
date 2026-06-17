# Skill: Ethana Solution Mapping

**Version:** 1.0
**Category:** Commercial Intelligence
**Owner:** Cursory Governance Team

---

## Purpose

This skill maps governance requirements, regulatory obligations, and customer use cases to Ethana platform capabilities. For each requirement it determines whether Ethana addresses it, scores the coverage confidence, and decides what can be commercially proposed. It then produces an aggregate coverage profile, positions Ethana against likely alternatives, and recommends the optimal commercial motion.

The skill is the commercial translation layer of the Governance OS. Upstream skills (regulatory-mapping, ai-incident-analysis) produce governance artefacts. This skill converts those artefacts into a form usable in a proposal or RFP response — bridging the advisory-to-sales boundary while enforcing the capability claims firewall throughout.

**Primary authority source:** `knowledge/ethana/canonical-product-model.md` is the only permitted source for capability status determinations. The marketing playbook, historical repository files, and verbal claims from the product team may not override it.

---

## When to Use This Skill

Use this skill when:
- A regulatory mapping or incident analysis has produced control requirements that need matching to Ethana capabilities
- A customer RFP or requirements document needs a structured, claim-safe capability response
- A sales discovery has identified customer needs and a proposal is being assembled
- A customer asks "can Ethana do X?" and a structured answer is required
- A competitive situation requires positioning Ethana against alternatives for a specific requirement set
- A proposal or RFP response needs a claims compliance review before submission
- A commercial motion recommendation is needed before a customer meeting or negotiation

---

## Input Specification

### Required Inputs

At least one of the following is required:

| Field | Description | Format |
|---|---|---|
| `requirement_list` | Governance or control requirements to map. May be Section 6 output from regulatory-mapping, Section 9 output from ai-incident-analysis, an RFP section, or free-form requirements. | Structured list or free text |
| `capability_question` | Direct question about platform capability: "Does Ethana support X?" or "What can Ethana provide for Y?" | Free text |
| `customer_use_case` | A customer use case or problem statement. The skill extracts discrete requirements during intake. | Free text |

### Contextual Inputs

| Field | Values | Why it matters |
|---|---|---|
| `customer_sector` | BFSI / Healthcare / Government / General Enterprise | Triggers SOC 2 blocker for BFSI, sector-specific cautions, and motion selection |
| `jurisdictions` | EU, UK, India (list) | Determines which regulatory controls need platform mapping |
| `output_mode` | Formal Proposal / RFP Response / Discovery Conversation | Controls language register and prohibition strictness |
| `deployment_constraint` | Cloud / Customer VPC / On-prem / Air-gapped | On-prem requires mandatory scale caveat |
| `existing_subscription` | None / Build / Edge / Bundle | Avoids re-selling owned capabilities; identifies expansion vs. new sale |
| `upstream_skill_output` | Document from regulatory-mapping or ai-incident-analysis | Pre-structured requirements reduce intake effort |
| `competitive_context` | Known alternatives the customer is evaluating | Sharpens Section 8 (Competitive Positioning) |

### Input Format

Inputs do not need to be structured. The skill accepts free-form descriptions, RFP documents, or upstream skill outputs and extracts discrete requirements during intake.

Minimum viable input: "The customer is an Indian private bank deploying LLM-based credit analysis. What can Ethana provide?"

---

## Output Specification

Every execution produces ten sections. Depth is calibrated to input complexity and output mode — a single capability question produces a condensed output; an RFP response with twenty-plus requirements produces a full ten-section analysis.

### 1. Requirement Coverage Map

For each extracted requirement:
- **Requirement**: stated in plain language
- **Matched Ethana capability**: the specific capability from canonical-product-model.md
- **Capability status**: Production / In Build / Aspirational / Not addressed
- **Coverage Confidence Score (CCS)**: 0–100 (see definition below)
- **Disposition**: Include in proposal / Roadmap mention only / Bridge to Cursory / Gap register

**Coverage Confidence Score (CCS):** Measures how fully the matched *Production* capability addresses this specific requirement. It is requirement-specific, not capability-generic. A Production capability can have a low CCS if it only partially addresses the requirement.

| Band | Score | Meaning |
|---|---|---|
| Full | 90–100 | Production capability directly and completely addresses this requirement. Claim confidently. |
| High | 70–89 | Production capability substantially addresses the requirement with minor stated caveats. Claim with caveat. |
| Partial | 50–69 | Production capability addresses the core but leaves a meaningful gap that must be bridged. Claim the covered portion; disclose the gap. |
| Thin | 25–49 | Production capability tangentially addresses the requirement. The gap exceeds the coverage. Lead with Cursory bridge; mention the platform component. |
| None | 0–24 | No Production capability addresses this requirement today. Cursory bridge or gap register. |

For In Build capabilities, the current CCS is always 0. Annotate with "Anticipated CCS when shipped: X/100" to show roadmap value.

### 2. Coverage Confidence Summary

An aggregate view of coverage quality for the full requirement set:
- Count and percentage of requirements at each CCS band
- Overall coverage characterisation: Platform-Primary (Cursory bridge is the exception) or Cursory-Primary (platform is supplemental)
- Whether the gap profile warrants an Advisory-First commercial motion
- The coverage story in two to three sentences, suitable for internal briefing

### 3. Proposal-Safe Platform Capabilities

Exact claim language for every Production capability addressing a requirement. Language must be:
- Specific and quotable — not "Ethana provides governance" but "Ethana's Immutable Audit Log captures every gateway-routed AI call in a tamper-proof, insert-only event store with native SIEM export to Splunk, Elastic, and Datadog"
- Inclusive of all mandatory caveats from canonical-product-model.md
- Written in the register appropriate to the output mode (Formal Proposal / RFP Response / Discovery Conversation)

This section is proposal-ready. It may be copied directly into a customer document.

### 4. Roadmap Disclosure

Every In Build capability relevant to the requirement set, phrased for conversational mention only. Each item includes:
- What the capability will provide when shipped
- Current development status (In Build, with what is known about sequencing)
- The Cursory bridge service that addresses the need today

**Important:** Items in this section must not appear in proposal deliverables. In a Formal Proposal or RFP Response, they belong only in a clearly-labelled Roadmap section with no delivery commitment.

### 5. Prohibited Claims Register

An explicit list of:
- Aspirational capabilities that must not appear in any context (Workspace features, Visual Agent Builder, uncertified SOC 2 / ISO 27001, "deployed with regulated customers today")
- In Build items that must not appear as proposal deliverables
- Any playbook claim that lacks primary engineering source support

This section must be reviewed against the draft proposal before submission. It is not optional.

### 6. Cursory Bridge Recommendations

For each gap (In Build, Aspirational, or Not addressed), the specific Cursory service that addresses the need today:
- Service name (exact name from Cursory services catalogue)
- What it delivers for this specific requirement
- Why it fills the gap
- How it is positioned alongside any platform component

Generic entries ("consider Cursory advisory") do not meet the quality standard. Every bridge must be specific and deliverable.

### 7. Gap Register

Requirements that Ethana cannot address at any status level, with the best available alternative:
- Specialist firm referral (for formal bias audits, specific certifications)
- Customer-built solution (for governed chat, RAG workflows, agent pipelines)
- Adjacent Production capability + customer delta (for partial coverage)

Gaps are not failures — documenting them honestly is what prevents over-claiming.

### 8. Competitive Positioning

How Ethana compares to likely alternatives for this specific requirement set. For each significant competitor or alternative approach:

- **Ethana's differentiated strength**: what Production capabilities create an advantage in this context
- **Ethana's honest gap**: where the competitor has capability Ethana does not (Production vs. Aspirational or In Build)
- **Win condition**: the customer profile, priority weighting, or procurement context in which Ethana wins
- **Loss condition**: the context in which the competitor wins and the honest reason

**Claims firewall applies to this section:** Only Production Ethana capabilities may be used in competitive comparison. Aspirational capabilities (Workspace, Visual Agent Builder) must not be positioned against competitors' production products.

### 9. Recommended Commercial Motion

The recommended deal structure for this customer, including:
- **Motion type**: Platform-First / Advisory-First / Land-and-Expand / Design Partner
- **Entry product**: which Ethana product(s) to include in the initial commercial proposal
- **Cursory services to pair**: which services to sell alongside the platform
- **Phase sequencing**: what is proposed now, what follows in phase two and three
- **Deal guardrails**: what must not be included in the initial proposal (sector-specific and status-based)
- **Success criteria**: what a successful first engagement looks like
- **Expansion path**: how the initial deal grows into the full suite

**Motion definitions:**

| Motion | When to use |
|---|---|
| Platform-First | Customer is procurement-ready; strong SOC 2/ISO 27001 posture; primary requirements are Production; no certification blocker |
| Advisory-First | SOC 2 or ISO 27001 is a hard procurement gate; primary requirements are In Build or Aspirational; or customer needs education before platform |
| Land-and-Expand | Some requirements are Production (entry point); others are In Build (expansion when shipped); enter with Build, expand with Edge when available |
| Design Partner | Customer is willing to co-shape an In Build capability; formal design partnership; requires engineering team involvement and explicit status disclosure |

### 10. Customer-Facing Executive Summary

200–250 words suitable for inclusion in a proposal cover letter or discovery debrief. Covers:
- What Ethana delivers today (Production capabilities relevant to this customer)
- What Cursory bridges (the gap between requirements and current production state)
- What is coming on the roadmap (In Build items relevant to this customer)
- Recommended next step

Written last, reflecting the full analysis. Not a draft position.

---

## Constraints and Scope

**In scope:**
- Mapping any governance, regulatory, or security control requirement to Ethana capabilities
- BFSI, Healthcare, Government, and General Enterprise requirement sets
- Formal proposals, RFP responses, and discovery conversations
- Competitive positioning against known alternatives
- Commercial motion recommendation and deal structure

**Out of scope:**
- Deep technical implementation design (handled by Ethana Implementation service)
- Regulatory interpretation and legal advice (handled by regulatory-mapping skill)
- Root cause analysis (handled by ai-incident-analysis skill)
- Jurisdictions not covered by the knowledge base (US, Canada, Australia, etc.)
- Claiming capabilities for products not yet launched (Workspace, Visual Agent Builder)

**Hard constraint — claims firewall:**
Every capability status determination must be sourced from `knowledge/ethana/canonical-product-model.md`. The marketing playbook may be referenced for commercial language and pricing only. Historical repository files (capability-status.md, source-of-truth.md, ethana-status-reconciliation.md) must not be used for status determinations.

**Depth calibration:**
- Single capability question → condensed output, Sections 1, 3, 5, and 10 are sufficient
- Discovery conversation → medium depth, all ten sections but briefer
- Formal proposal or RFP response → full ten-section analysis at maximum depth

---

## Knowledge Dependencies

### Tier 1 — PRIMARY (mandatory for every invocation)

- `knowledge/ethana/canonical-product-model.md`

Every capability status check, CCS score, and claim decision routes through this file. Do not substitute or override with any other source.

### Tier 2 — SECONDARY (contextual, loaded when relevant)

- `knowledge/ethana/product-architecture-investigation.md` — for Edge / Sentry / Workspace naming questions
- `knowledge/ethana/use-cases.md` — for use case pattern matching to capabilities
- `knowledge/ethana/competitor-positioning.md` — for Section 8 (Competitive Positioning)

### Tier 3 — FRAMEWORK CROSSWALK (when upstream skill output is the input)

- `knowledge/frameworks/iso-42001.md` — for mapping Annex A controls → Ethana capabilities
- `knowledge/frameworks/nist-ai-rmf.md` — for mapping NIST AI RMF categories → Ethana capabilities
- `knowledge/frameworks/owasp-llm-top-10.md` — for mapping OWASP LLM risks → Guardrails and Red Teaming
- `knowledge/regulations/india-ai-landscape.md` — for mapping RBI / SEBI / IRDAI controls
- `knowledge/regulations/eu-ai-act.md` — for mapping EU AI Act obligations
- `knowledge/regulations/uk-ai-guidance.md` — for mapping FCA / PRA / ICO obligations

### Tier 4 — UPSTREAM SKILL OUTPUTS (accepted as input format)

- Output from `skills/regulatory-mapping/` Section 6 (Control Requirements) — most common input
- Output from `skills/ai-incident-analysis/` Section 9 (Recommended Controls)

---

## Related Skills

- `skills/regulatory-mapping/` — produces control requirements that commonly feed into this skill
- `skills/ai-incident-analysis/` — produces recommended controls that commonly feed into this skill
- `skills/governance-control-mapping/` — for translating the capability recommendations into specific implementation designs
- `skills/iso-42001-gap-assessment/` — for ISO 42001 gap analysis when framework alignment is the primary need
