# Skill: Ethana Feature Mapping

**Version:** 1.0
**Category:** Technical Intelligence
**Owner:** Cursory Governance Team

---

## Purpose

This skill validates specific Ethana features against a customer's technical context. Where Ethana Solution Mapping maps governance requirements to commercial proposal language, Ethana Feature Mapping operates one level deeper — answering whether a specific feature works for a specific technical environment, can substitute a feature from the customer's existing tool set, and is ready to demonstrate in a proof of concept.

It is used by solution architects, technical evaluators, and POC teams after Solution Mapping has determined what to propose — or in parallel, when a customer's technical team asks specific feature questions that go beyond what a commercial proposal covers.

The same claims firewall that governs Solution Mapping applies here without relaxation. Production features can be validated technically and included in a POC scope. In Build features cannot be included in a technical evaluation document as available, cannot be demonstrated, and cannot appear in a POC scope without explicit "In Build — not yet available" disclosure. Aspirational features must not be described, demonstrated, or referenced as available at any depth of technical discussion.

**Primary authority source:** `knowledge/ethana/canonical-product-model.md` is the only permitted source for feature status determinations, performance characteristics, and capability scope. No invented feature, undocumented integration, or unconfirmed performance figure may appear in any output section.

---

## When to Use This Skill

Use this skill when:
- A technical evaluator or enterprise architect asks specific feature questions: "What does the Audit Log schema capture?", "Does the PII scanner cover structured data?", "What MCP runtimes does the Security Broker support?"
- A customer's engineering team submits a technical evaluation questionnaire, RFI, or feature checklist requiring feature-level technical answers
- A proposed POC scope needs technical feasibility validation before committing to the pilot
- A customer is evaluating whether Ethana Build can replace an existing AI observability, guardrails, or governance tool and needs a feature-by-feature substitution analysis
- Section 3 from Ethana Solution Mapping has been approved and the engagement moves to technical validation ahead of a contract or pilot
- A solution architect needs to verify which Ethana features integrate with the customer's existing stack before designing an implementation

---

## Relationship to Ethana Solution Mapping

| | Ethana Solution Mapping | Ethana Feature Mapping |
|---|---|---|
| **Question answered** | What can we propose? | Does this specific feature work here? |
| **Input** | Governance requirements, regulatory obligations | Feature questions, technical requirements, existing tool features, POC scope |
| **Output** | Commercial proposal language, competitive positioning, deal structure | Technical validation, integration steps, POC test scenarios, substitution analysis |
| **Audience** | Advisory team building the proposal | Solution architects, technical evaluators, POC teams |
| **Timing** | Pre-proposal | Post-proposal or parallel — before POC or contract |
| **Scoring metric** | Coverage Confidence Score (CCS) | Technical Fit Score (TFS) |
| **Pass threshold** | 70/100 | 85/100 |

Feature Mapping commonly receives Solution Mapping Section 3 as its primary input — the approved commercial capabilities become the feature set to validate technically before a pilot begins.

---

## Input Specification

### Required Inputs

At least one of the following is required:

| Field | Description | Format |
|---|---|---|
| `feature_question` | A specific technical question about an Ethana feature: "Does Ethana support X?", "How does [feature] work technically?", "What exactly does [feature] log?" | Free text |
| `technical_requirement` | Specific technical constraints the feature must satisfy: latency budget, schema requirements, API format, retention policy, throughput target, data modality | Structured list or free text |
| `existing_tool_feature_list` | Features of a tool the customer currently uses, submitted for feature-by-feature substitution analysis. Include the tool name and the specific features the customer values. | Structured list or free text |
| `poc_scope` | A proposed POC scope — feature set, timeline, and desired success criteria — that needs technical feasibility validation before committing to the pilot | Structured list or free text |
| `upstream_skill_output` | Section 3 (Proposal-Safe Platform Capabilities) from Ethana Solution Mapping. The Production capabilities in that section become the feature set to validate technically. | Skill output document |

### Contextual Inputs

| Field | Values | Why it matters |
|---|---|---|
| `deployment_constraint` | Cloud / Customer VPC / On-prem / Air-gapped | Integration options and performance characteristics differ by model. On-prem is single-node — throughput ceiling affects POC sizing. Air-gapped eliminates cloud update paths. |
| `existing_stack` | Named tools: Splunk, Azure AD, Kong, Datadog, GitHub Actions, Okta, Kubernetes, LangChain, etc. | Determines which integrations are confirmed, which require API paths, and which are gaps |
| `customer_sector` | BFSI / Healthcare / Government / General Enterprise | BFSI certification constraints (SOC 2, ISO 27001) remain relevant in technical documents. On-prem scale caveat is a hard requirement in BFSI contexts. |
| `volume_parameters` | LLM call volume per day, user count, data volume | Determines which performance claims are valid for this customer's throughput profile |
| `poc_duration` | 30 / 60 / 90 days | Constrains the POC Feature Set — setup-heavy features must be flagged or excluded |
| `output_mode` | Technical Evaluation / POC Scope / RFI Response / Internal Technical Memo | Controls language register and output depth |

### Input Format

Inputs do not need to be structured. The skill accepts free-form technical questions, RFI documents, POC proposals, and upstream skill outputs, extracting discrete feature queries during intake.

Minimum viable input: "Does Ethana's Audit Log meet the insert-only immutability requirement for a bank's regulatory audit evidence?"

---

## Output Specification

Every execution produces ten sections. For a single feature question, condensed output is acceptable — Sections 1, 2, 4, 6, 8, 9, and 10 at minimum. For a full technical evaluation, POC scope validation, or substitution analysis, all ten sections are required.

### 1. Feature Validation Table

For each queried Ethana feature:
- **Feature name**: the specific feature from canonical-product-model.md (not the product line)
- **Capability status**: Production / In Build / Aspirational — sourced only from canonical-product-model.md
- **Technical Fit Score (TFS)**: 0–100 (see definition below)
- **Technical description**: what the feature does, how it works, relevant performance characteristics
- **Hard technical constraints**: specific limitations that affect fitness for this requirement
- **Evidence reference**: the canonical-product-model.md section or other approved source for each claim

**Technical Fit Score (TFS):** Measures how well a specific Production Ethana feature addresses a specific technical requirement. It is requirement-specific, not feature-generic — the same feature can score differently against different requirements from different customers.

| Band | Score | Meaning |
|---|---|---|
| Ready | 90–100 | Production feature directly addresses the requirement. Configurable. Demo-ready immediately with standard deployment. Claim confidently. |
| Viable | 70–89 | Production feature addresses the requirement with specific configuration or one documented constraint. Demo-ready with standard setup. Claim with caveat. |
| Partial | 50–69 | Feature covers the core but leaves a gap — another capability, integration, or customer-side step is needed to fully address the requirement. Claim the covered portion; disclose the gap. |
| Thin | 25–49 | Feature is tangentially related to the requirement. The gap exceeds the coverage. Lead with the gap; mention the partial coverage. |
| Not Viable | 0–24 | No Production feature materially addresses this technical requirement today. POC cannot demonstrate this. |

For In Build features: current TFS = 0. Annotate with "Anticipated TFS when shipped: X/100" only when directly asked about the roadmap.
For Aspirational features: TFS = 0. Route to Section 6 (Prohibited). Do not annotate an anticipated TFS.

### 2. Technical Fit Summary

The aggregate view of technical fitness for the full feature set:
- **Average TFS**: the arithmetic mean of all Section 1 TFS scores, including 0s for In Build, Aspirational, and unaddressed features. Calculated as: sum of all TFS values ÷ total feature count. Show the arithmetic explicitly — the sum, the count, and the result.
- **Distribution**: count of features in each TFS band (Ready / Viable / Partial / Thin / Not Viable). Counts must sum to total feature count. Verify this before writing.
- **Technical Characterisation**: determined by the verified average TFS:
  - **POC-Ready**: Average TFS ≥ 75 and majority of features at Ready or Viable. The feature set can be demonstrated in a POC with standard setup.
  - **POC-Ready with Conditions**: Average TFS 55–74, or majority at Viable/Partial. A POC is feasible with specific prerequisites or scope adjustments documented per feature.
  - **Limited POC Scope**: Average TFS 35–54. POC should be scoped to the subset of features scoring Viable or Ready. Features scoring Thin or Not Viable should be excluded.
  - **Not POC-Ready**: Average TFS < 35. The proposed feature set cannot be demonstrated as a coherent POC. Recommend feature scope reduction or Advisory-only engagement.
- **Coverage story**: two to three sentences for an internal technical briefing, suitable for a solution architect to share with the engagement lead

### 3. Integration Compatibility Assessment

For each Production feature in Section 1 and each relevant component of the customer's existing stack:
- **Integration type**: Native Connector / SIEM Export / API / Webhook / Configuration-only / Not Confirmed / Gap
- **Configuration steps**: specific steps, parameters, and credentials the customer must provide
- **Schema mapping**: where Ethana data maps to the customer's existing schema or data format
- **Compatibility constraints**: version requirements, protocol requirements, data format requirements
- **Evidence source**: where this integration is confirmed — referenced in Section 8

Do not invent connectors. Every integration claim must appear in canonical-product-model.md or another approved source listed in Section 8. Unconfirmed integrations must be labelled exactly: "Integration with [Component] is not confirmed in the canonical product model — verify with Ethana engineering before including in any customer-facing document."

### 4. Technical Constraints and Caveats

Specific technical limitations relevant to this customer's context. These are facts for a technical audience — not commercial caveats, not softened language.

Recurring constraints to check and document when applicable:
- On-prem deployment: single-node architecture; throughput ceiling — document explicitly for high-volume requirements
- Air-gapped: no cloud update channel; offline update process required
- PII Scanner: text-output modality only — audio, images, and structured database fields are not scanned
- Bias Scanner: runtime text-output filter only — not a statistical model audit; cannot satisfy formal bias evaluation requirements under any regulatory framework
- MCP Security Broker: requires MCP-compatible agent runtime — not all agent frameworks support the Model Context Protocol
- Audit Log schema: configurable field names and retention periods; the core capture schema is fixed; fields outside the configurable set cannot be added
- Red Teaming Orchestrator: 21 OWASP LLM Top 10 probes are Production; CI/CD gate integration is In Build
- SCIM provisioning: In Build — SSO/OIDC is Production; automated user provisioning is not yet available
- Any performance constraint relevant to the customer's volume_parameters not confirmed in the canonical model

A material constraint absent from Section 4 is a scoring failure. A constraint documented in Section 4 that is contradicted by claim language in Section 9 is a disqualifying inconsistency.

### 5. POC Feature Set

Which Production features are technically ready to include in a POC for this customer context. For each included feature:
- **Test scenario**: what to demonstrate and exactly how — specific and executable, not generic ("submit a prompt containing a credit card number via the Gateway and verify the PII scanner flags the response before it reaches the user; confirm the event is recorded in the Audit Log with scanner disposition" — not "show the guardrails dashboard")
- **Technical prerequisites**: what the customer must provide before this feature can be demonstrated; named specifically ("customer must provide: LangChain ≥ 0.1, test LLM API credentials, and a sandbox environment matching the target deployment model" — not "customer provides environment")
- **Measurable success criterion**: a specific, binary, observable outcome — not "the feature appears to work"
- **Estimated setup time**: realistic hours or days required before the POC can demonstrate this feature

Excluded features must be listed with a specific exclusion reason:
- "In Build — cannot be demonstrated"
- "TFS [X] — feature does not sufficiently address the requirement in this customer's context"
- "Prerequisite [X] cannot be met within the [N]-day POC window"
- "Integration with [Component] is unconfirmed — cannot commit to demonstration"

Silence is not acceptable. Every feature in scope must be explicitly included or excluded with a reason.

### 6. Prohibited Feature Claims Register

What must not appear in any technical evaluation document, RFI response, POC scope, or demonstration:
- In Build features that cannot be demonstrated: list each by feature name with canonical status
- Aspirational features that cannot be described as available: list each by feature name
- Integration compatibility claims not confirmed in any approved source
- Performance claims that exceed the confirmed performance envelope for this deployment context
- Any claim sourced from the marketing playbook that lacks a canonical engineering source

This section is not optional. It must be reviewed against every other output section before release.

### 7. Substitution Analysis

Used only when `existing_tool_feature_list` is provided. For each feature of the customer's existing tool:

| Substitution Category | Definition |
|---|---|
| Full Substitute | Ethana Production feature provides equivalent or better functionality. No material capability loss for this use case. |
| Partial Substitute | Ethana Production feature covers the core but lacks specific sub-features. Customer accepts a reduced scope or pairs with a bridge. |
| Complementary | Ethana works alongside the existing tool on this feature — augments it but does not replace it. |
| Gap | No Ethana feature at any status level addresses this existing tool feature today. |

For each feature: the category, the Ethana equivalent (if any), what the customer gains and loses, migration path or integration approach for Full and Partial, and bridge recommendation for Gap. Entries must be specific — "consider alternatives" does not meet the standard.

In Build Ethana features must not be used to claim substitution coverage. An existing tool feature with only an Ethana In Build equivalent is a Gap today.

### 8. Evidence References

A source table for every major technical claim in this output. Compiled after all other sections are written. Required before release.

| Claim | Source | Section |
|---|---|---|
| [Specific claim text] | canonical-product-model.md — [capability name] entry | Section [N] |
| [Integration claim] | product-architecture-investigation.md — [relevant section] | Section [N] |
| [Unconfirmed claim] | Not found in approved sources — flagged as unconfirmed | Section [N] |

**Approved source hierarchy:**
1. `knowledge/ethana/canonical-product-model.md` — primary authority for all status, performance, and scope claims
2. `knowledge/ethana/product-architecture-investigation.md` — secondary; for architecture and protocol questions
3. Direct engineering confirmation — cite as "Ethana engineering confirmation, [date]"; use only when the canonical model is explicitly silent
4. `knowledge/ethana/use-cases.md` — for use case pattern matching only; not for performance or status claims

If a claim has no traceable source in the approved hierarchy, remove it from the output or flag it explicitly as unconfirmed — in this section and in the section where it appears.

### 9. Technical Proposal Language

Feature-level claim language for a technical audience — more specific than Solution Mapping Section 3. For each validated Production feature with TFS ≥ 50:
- Specific metric where confirmed: "sub-200ms p95 for all six scanners combined," "~50ms gateway overhead," "21 OWASP LLM Top 10 probes," "insert-only write path at the database layer"
- API endpoint structure or integration path where documented
- Configuration parameters that are customer-adjustable vs. fixed
- Mandatory caveats from canonical-product-model.md, included inline and not buried in footnotes

Quotable in a technical addendum, RFI response, architecture review, or SOW technical appendix. This section is not commercial proposal language — Solution Mapping Section 3 serves that purpose.

Features scoring Not Viable (TFS < 25) must not appear in Section 9 as primary claims. If they appear at all — for a supplemental caveat — they must include an explicit statement of what the feature does NOT do for this requirement.

### 10. Technical Summary

150–200 words for a technical decision memo. Written last, after all other sections are complete. Covers:
- Which features are validated as technically fit for this customer's context (TFS ≥ 70)
- Which features require specific conditions to be viable
- Which features are excluded from the POC scope and why
- What the solution architect should do next: proceed to POC, adjust scope, resolve prerequisites, or defer

---

## Constraints and Scope

**In scope:**
- Technical feature validation for any Production Ethana capability
- Integration compatibility assessment for named stack components when integration is confirmed in an approved source
- Substitution analysis for named AI observability, guardrails, and governance tools
- POC feasibility and scope validation
- Technical RFI and feature evaluation questionnaire responses
- BFSI, Healthcare, Government, and General Enterprise technical contexts

**Out of scope:**
- Implementation design and configuration detail (Ethana Implementation Service)
- Regulatory interpretation and legal advice (regulatory-mapping skill)
- Commercial proposal language and deal structure (Ethana Solution Mapping)
- Integration compatibility claims for stack components not confirmed in the approved source hierarchy
- Performance claims for customer-specific infrastructure configurations not covered by the documented performance envelope
- Any claim for a capability not in Ethana Build production today

**Hard constraint — claims firewall:**
Every feature status determination must be sourced from `knowledge/ethana/canonical-product-model.md`. No integration claim may be made for a connector or API integration path not confirmed in the approved source hierarchy. No performance figure may be stated without a traceable source. Historical repository files (capability-status.md, source-of-truth.md, ethana-status-reconciliation.md) must not be used.

**Depth calibration:**
- Single feature question → condensed output: Sections 1, 2, 4, 6, 8, 9, 10 required; Sections 3, 5, 7 at discretion
- Technical RFI or evaluation questionnaire → all ten sections required
- POC scope validation → Sections 1, 2, 3, 4, 5, 6, 8, 10 required; Sections 7 and 9 at discretion
- Substitution analysis → all ten sections required

---

## Knowledge Dependencies

### Tier 1 — PRIMARY (mandatory for every invocation)

- `knowledge/ethana/canonical-product-model.md`

Every feature status check, TFS score, integration claim, and performance figure routes through this file. When this file is silent on a specific technical detail, do not invent the answer — flag it as unconfirmed and recommend engineering verification.

### Tier 2 — SECONDARY (contextual, loaded when relevant)

- `knowledge/ethana/product-architecture-investigation.md` — for Edge, Sentry, and Workspace architecture questions; MCP protocol depth; multi-product naming conventions
- `knowledge/ethana/use-cases.md` — for use case pattern matching; not for performance or status claims
- `knowledge/ethana/competitor-positioning.md` — for Section 7 (Substitution Analysis) when competitor feature depth is needed

### Tier 3 — FRAMEWORK CROSSWALK (when technical requirements reference a governance framework)

- `knowledge/frameworks/owasp-llm-top-10.md` — for Red Teaming Orchestrator probe-to-OWASP mapping
- `knowledge/regulations/india-ai-landscape.md` — for RBI Fair Practices Code and SEBI technical control requirements
- `knowledge/regulations/eu-ai-act.md` — for EU AI Act Annex IV technical documentation requirements
- `knowledge/regulations/uk-ai-guidance.md` — for FCA operational resilience technical controls and ICO DPA obligations

### Tier 4 — UPSTREAM SKILL OUTPUTS (accepted as primary input)

- Output from `skills/ethana-solution-mapping/` Section 3 (Proposal-Safe Platform Capabilities) — the most common input
- Output from `skills/regulatory-mapping/` Section 6 (Control Requirements) — when technical requirements derive from a regulatory mapping

---

## Related Skills

- `skills/ethana-solution-mapping/` — upstream: determines what to propose commercially; this skill validates that it can be technically delivered
- `skills/regulatory-mapping/` — upstream: produces control requirements that may generate specific feature validation questions
- `skills/ai-incident-analysis/` — upstream: recommended controls may generate feature validation questions for implementation
- `skills/governance-control-mapping/` — downstream: takes validated features and designs specific implementation controls and evidence procedures
