# Ethana Feature Mapping — Workflow

This document defines the seven-phase execution workflow for the Ethana Feature Mapping skill. Follow each phase in order. Phase 5 runs only when `existing_tool_feature_list` is provided. Phase 6 runs only when `poc_scope` or `upstream_skill_output` is provided or when the customer explicitly asks about POC feasibility.

Every feature status determination must use `knowledge/ethana/canonical-product-model.md` as the sole authority. Do not accept status from the marketing playbook, verbal product team claims, or historical repository files.

---

## Workflow Overview

| Phase | Name | Duration | Description |
|---|---|---|---|
| 1 | Intake and Feature Extraction | 5–10 min | Parse inputs; extract discrete feature queries; classify query type; establish execution context |
| 2 | Status Gating | 5 min | Apply claims firewall at feature level before any technical analysis begins |
| 3 | Technical Feature Validation and TFS Scoring | 15–30 min | Deep technical description per Production feature; assign TFS per requirement |
| 4 | Integration Compatibility Assessment | 10–15 min | Map confirmed integrations to customer stack; classify each as Supported / Not Confirmed / Gap |
| 5 | Substitution Analysis | 10–15 min | When existing_tool_feature_list provided: assign Full / Partial / Complementary / Gap per feature |
| 6 | POC Readiness Assessment | 10 min | Apply DT3; determine POC inclusion, conditions, and exclusions per feature |
| 7 | Output Assembly, Arithmetic Gate, and Quality Check | 10–15 min | Assemble ten sections; run mandatory gate; verify against evaluation rubric; confirm release |

Total: 65–100 minutes for a full analysis
Condensed (single feature question): Phases 1, 2, 3, 7 only — 25–35 minutes

---

## Phase 1: Intake and Feature Extraction

**Objective:** Parse all inputs, extract discrete feature queries, classify the query type, and determine which phases are required.

### 1.1 Input Parsing

Read all provided inputs. Extract:
1. All explicitly named Ethana features (e.g., "the Immutable Audit Log," "the PII scanner," "the MCP Security Broker")
2. All technical requirements that imply a feature need (e.g., "must support Splunk export" → Audit Log SIEM connector; "must detect prompt injection" → Guardrails Prompt Injection Scanner)
3. All existing tool features provided for substitution: name the tool and each named feature
4. The proposed POC scope if provided: feature list, timeline, and success criteria as stated
5. Contextual parameters: deployment_constraint, existing_stack, customer_sector, volume_parameters, poc_duration, output_mode

### 1.2 Query Type Classification

Apply DT1 to determine query type and active phases. Record before proceeding to Phase 2.

### 1.3 Disambiguation

If a feature query could map to multiple Ethana features (e.g., "bias detection" could be the runtime Bias Scanner or a formal bias audit capability), flag both interpretations and resolve them separately. Do not collapse distinct requirements into a single feature match.

If a feature name does not appear in canonical-product-model.md, do not invent a match. Document as: "Not found in canonical product model — verify with Ethana engineering."

### 1.4 Volume and Deployment Context

Record the customer's volume_parameters and deployment_constraint. These affect which performance claims are valid:
- **Cloud / Customer VPC**: all published performance figures from the canonical model apply
- **On-prem**: single-node constraint applies; note throughput ceiling for Phase 4 and Section 4
- **Air-gapped**: no cloud update channel; offline update process required; note for Section 4

---

## Phase 2: Status Gating

**Objective:** Apply the claims firewall at feature level before any technical analysis. This phase determines what can be validated (Production), what must be disclosed as roadmap (In Build), and what must be excluded entirely (Aspirational).

### 2.1 Status Lookup

For every feature identified in Phase 1, look up its status in canonical-product-model.md. Record:
- Exact capability name as it appears in canonical-product-model.md
- Status: Production / In Build / Aspirational
- Any mandatory caveats listed for this capability in that file

Do not interpolate status from product descriptions, playbook claims, or previous outputs. The file is the authority.

### 2.2 Apply DT2

Apply the claims firewall decision tree (DT2) to each feature. Record the routing outcome before proceeding to Phase 3.

### 2.3 Pre-Analysis Status Register

Before proceeding, record three lists:
- **Production features**: proceed to Phase 3 for technical validation and TFS scoring
- **In Build features**: route to Section 6 (Prohibited) immediately; do not validate technically; do not include in POC scope
- **Aspirational features**: route to Section 6 immediately; do not describe, validate, or reference as available; do not annotate with anticipated TFS
- **Not found**: route to Section 6; label "Status unconfirmed — not in canonical product model"

### 2.4 CCS None-Band Pre-Flag

For each Production feature, anticipate whether it may score in the Not Viable band (TFS 0–24) based on the nature of the requirement. If likely, pre-flag for the three-part handling in Phase 3:
- Supplemental mention in Section 9 with explicit non-coverage caveat
- Route the unaddressed portion to Section 4 (Technical Constraints)
- Do not include as a primary claim in Section 9

---

## Phase 3: Technical Feature Validation and TFS Scoring

**Objective:** For each Production feature, produce a deep technical description against the specific requirement and assign a TFS score.

### 3.1 Technical Description

For each Production feature, document:
1. **Function**: what the feature does — in technical terms, for an engineer audience
2. **Mechanism**: how it works at the technical level — not the commercial benefit
3. **Performance characteristics**: state only figures confirmed in canonical-product-model.md; do not infer or extrapolate for configurations or volumes not documented
4. **Configuration options**: what parameters are customer-adjustable; what is fixed by the platform
5. **Data schema**: what data is produced, captured, or transformed by this feature
6. **Evidence reference**: cite the specific section or table in canonical-product-model.md for each claim; populate Section 8 as you write

### 3.2 TFS Assignment

Assign a TFS for each Production feature against the specific technical requirement being evaluated:

**TFS Calibration Table:**

| TFS | Band | When to assign |
|---|---|---|
| 90–100 | Ready | Feature directly addresses the requirement in its current production configuration with no significant prerequisite beyond standard deployment. No material constraint limits fitness for this specific requirement. |
| 70–89 | Viable | Feature addresses the requirement but requires specific customer-side configuration, a secondary integration step, or one documented constraint applies that does not block the use case. The constraint is manageable within a normal engagement. |
| 50–69 | Partial | Feature covers the core of the requirement but leaves a technical gap. Another Ethana component, customer-side integration step, or workaround is needed to fully close the requirement. |
| 25–49 | Thin | Feature has some relevance to the requirement but the gap between what the feature delivers and what the requirement needs is larger than the coverage. Do not lead with this feature as the primary response. |
| 0–24 | Not Viable | No Production feature materially addresses this specific technical requirement today. The feature may exist but its scope, modality, or architecture does not match what the requirement needs. |

**Scoring rules:**
- Score against the specific requirement and customer context, not the feature in general. The Gateway scores 95 against a >100ms latency budget; it scores 20 against a <30ms latency budget. These are different scores for the same feature.
- If an In Build feature was identified in Phase 2, assign TFS = 0 (current) and do not continue to Phase 3 analysis for it. Note anticipated TFS only if the customer explicitly asks about roadmap.
- A mandatory caveat in canonical-product-model.md that materially limits fitness for the requirement must reduce the TFS — it is not merely an annotation. The Bias Scanner's "runtime text filter only" caveat against a formal bias audit requirement reduces TFS from what it might be for a runtime detection requirement.
- Do not round up to avoid a lower band. A score of 67 is Partial, not Viable. A score of 72 is Viable, not Ready.
- A Production feature that cannot satisfy the requirement in this customer's deployment model (e.g., on-prem throughput ceiling exceeded) should score Thin or Not Viable for that specific requirement — not Viable.

### 3.3 Handling Not Viable Production Features

When a Production feature scores Not Viable (TFS 0–24) against a specific requirement:
1. Do not include it as a primary coverage item in Section 9. If it appears at all, it must carry an explicit caveat: "This feature does NOT address [the formal/statistical/structured-data aspect] of this requirement."
2. Route the unaddressed portion of the requirement to Section 4 (Technical Constraints) and Section 6 (Prohibited) to prevent false confidence.
3. Do not use the feature's existence as justification for the requirement being "partially met" unless TFS ≥ 25.

---

## Phase 4: Integration Compatibility Assessment

**Objective:** Determine which Production features integrate with the customer's named stack components and classify each integration path.

### 4.1 Stack Component Mapping

For each component named in `existing_stack`, apply DT5 to determine integration type. For each Ethana Production feature + stack component pair that is relevant to the evaluation:
1. Check canonical-product-model.md for a documented integration
2. If found: classify and document with configuration steps
3. If not found: label as Not Confirmed; do not guess or infer

### 4.2 Integration Classification Standards

**Supported — Native Connector:** The integration is explicitly documented in canonical-product-model.md or product-architecture-investigation.md with a named connector. State the connector type, protocol, and customer configuration requirement.

**Supported — SIEM Export:** The integration is achievable via Ethana's documented SIEM export. Applicable to the Immutable Audit Log. Confirmed targets: Splunk, Elastic, Datadog. For other SIEM targets, classify as Not Confirmed.

**Supported — OIDC/SSO:** The integration is via standard OIDC/SSO. Applicable to Account Management for Azure AD, Okta, and other OIDC-compatible identity providers. SCIM provisioning is separate from OIDC/SSO and is In Build.

**Supported — API:** The integration is achievable via Ethana's documented API or webhook. State the integration method and what the customer must implement on their side.

**Not Confirmed:** The integration is not documented in any approved source. Use this exact language: "Integration with [Component] is not confirmed in the canonical product model — verify with Ethana engineering before including in any customer-facing commitment."

**Gap:** Ethana has no documented integration path with this component at any status level. Use this exact language: "No integration path between Ethana and [Component] is documented in approved sources. Do not claim compatibility."

### 4.3 Volume and Performance Scope

Where volume_parameters are provided:
- State whether the customer's declared volume (calls/day, concurrent users) falls within the documented performance envelope of canonical-product-model.md
- If the canonical model does not state throughput figures for the specific deployment model: flag as "Performance at [N] calls/day in [deployment model] is not confirmed — verify with Ethana engineering before committing"
- For on-prem single-node: the throughput ceiling must be documented in Section 4; if the ceiling is not stated explicitly in the canonical model, state "On-prem single-node throughput ceiling is not quantified in the canonical product model — verify before committing to a high-volume POC"

---

## Phase 5: Substitution Analysis

**Run only when `existing_tool_feature_list` is provided.**

**Objective:** Assign a substitution category to each feature of the customer's existing tool and document the customer's gain, loss, and transition path.

### 5.1 Feature-Level Comparison

For each feature of the existing tool:
1. Identify the Ethana equivalent from canonical-product-model.md (Production only)
2. Apply DT4 to assign a substitution category
3. Document gains, losses, migration path, or bridge as appropriate to the category

### 5.2 Substitution Category Application

**Full Substitute:** Ethana Production feature covers this existing tool feature without material capability loss for this customer's use case. Document what the customer gains (compliance trail, immutability, gateway integration) and any differences in interface or workflow that do not affect the outcome.

**Partial Substitute:** Ethana covers the core but lacks one or more specific sub-features the customer currently uses. Be explicit about what is lost. Offer a bridge recommendation for the gap — Cursory advisory service or a named third-party tool. Do not describe a Partial Substitute as a Full Substitute by downplaying the gap.

**Complementary:** Ethana is designed to augment the existing tool on this feature, not replace it. Both should be retained. Document the integration point and what each tool handles.

**Gap:** No Ethana Production feature addresses this existing tool feature today. If an In Build Ethana feature would cover it when shipped, note: "Gap today. Anticipated coverage when [Feature] ships — no committed timeline." Do not count In Build coverage as current substitution. Recommend whether the customer should retain the existing tool or accept the gap.

### 5.3 Migration Path (for Full and Partial Substitutes)

For each Full or Partial Substitute, provide:
1. What data or configuration needs to migrate
2. Whether the tools can run in parallel during transition
3. Estimated migration effort category (low / medium / high — not hours, as this is out of scope)
4. Any migration dependency on Ethana onboarding steps

---

## Phase 6: POC Readiness Assessment

**Run when `poc_scope` is provided, or when `upstream_skill_output` (Solution Mapping Section 3) is provided, or when the customer asks about POC feasibility.**

**Objective:** Determine which Production features can be included in a POC for this customer and document specific test scenarios, prerequisites, and success criteria.

### 6.1 Apply DT3 to Each Feature

For each feature in scope, apply the POC Readiness Gate (DT3). Record: Include / Conditional Include / Exclude.

### 6.2 For Each Included Feature

Write:
1. **Test scenario**: specific, executable demonstration — not "show the feature" but "submit a prompt containing [specific content] via the Gateway and verify [specific observable outcome]; confirm the event appears in the Audit Log with [specific fields] populated"
2. **Technical prerequisites**: name each prerequisite specifically. "MCP-compatible runtime" is not sufficient — specify: "LangChain ≥ 0.1 or LlamaIndex ≥ 0.10." "Customer environment" is not sufficient — specify: "sandboxed cloud tenant with [provider] API key and [deployment model] configuration"
3. **Measurable success criterion**: binary, observable, non-subjective. "The scanner correctly flags [specific content type] and the event is recorded in the Audit Log within [N] seconds" — not "the feature appears to function correctly"
4. **Estimated setup time**: realistic estimate in hours or days

### 6.3 For Each Excluded Feature

State the exclusion reason with specificity:
- "**In Build — cannot be demonstrated.** [Feature name] is In Build and must not appear in the POC scope."
- "**TFS [X] — not viable in this context.** [Feature name] does not address [requirement] for this customer because [specific technical reason]."
- "**Prerequisite cannot be met within [N]-day POC window.** [Feature name] requires [prerequisite], which the customer has not confirmed."
- "**Integration unconfirmed.** [Feature name] integration with [Stack Component] is not confirmed — cannot commit to a demonstration scenario."

"Not ready" or "out of scope" without a reason is not acceptable.

---

## Phase 7: Output Assembly, Arithmetic Gate, and Quality Check

**Objective:** Assemble all ten output sections, run the mandatory arithmetic and traceability gate, verify the output against the evaluation rubric, and confirm release disposition.

### 7.1 Section Assembly Order

Assemble in this order — Section 10 is always written last:

1. Feature Validation Table — from Phase 3 TFS scoring
2. Technical Fit Summary — computed from Section 1 TFS values; verify arithmetic here (Gate Step 1)
3. Integration Compatibility Assessment — from Phase 4
4. Technical Constraints and Caveats — from Phases 3 and 4; cross-check against Section 9 for contradictions
5. POC Feature Set — from Phase 6; omit if not applicable
6. Prohibited Feature Claims Register — from Phase 2 plus any Section 3 routing outcomes from Phase 3
7. Substitution Analysis — from Phase 5; omit if not applicable
8. Evidence References — compile from all claims written in Sections 1–7; this section is written after all others
9. Technical Proposal Language — from Phase 3; for Production features with TFS ≥ 50
10. Technical Summary — written last, after all sections are complete

### 7.2 Mandatory Arithmetic and Traceability Gate

**This gate must be completed before any output is released. Do not release output that has not passed every step of this gate.**

**Gate Step 1 — TFS Arithmetic Verification:**
- List all Section 1 TFS values explicitly
- Sum them: [TFS1] + [TFS2] + ... + [TFSn] = [sum]
- Divide by total feature count: [sum] ÷ [n] = [average]
- Verify that the average stated in Section 2 matches this computation exactly
- If they differ: correct Section 2 before proceeding

**Gate Step 2 — Distribution Count Verification:**
- Count features in each TFS band: Ready, Viable, Partial, Thin, Not Viable
- Verify: sum of all band counts = n (total feature count)
- If counts do not sum to n: recount and correct before proceeding
- Verify: band counts in Section 2 match the recount

**Gate Step 3 — Integration Claim Traceability:**
For every integration claim in Section 3 (Supported / Not Confirmed / Gap):
- Verify that Section 8 (Evidence References) contains a source entry for each "Supported" claim
- Any "Supported" claim without a Section 8 source must be changed to "Not Confirmed" or removed
- "Not Confirmed" claims do not need a source entry — they are already appropriately hedged

**Gate Step 4 — Performance Claim Traceability:**
For every performance figure in Sections 1 or 9 (sub-Xms latency, X probes, X nodes, throughput figures):
- Verify that Section 8 contains a source entry
- Any performance figure without a source entry must be removed or explicitly flagged as "Not confirmed — verify with engineering"

**Gate Step 5 — Status Verification:**
For every capability listed in Section 1 as Production:
- Verify the status against canonical-product-model.md
- If any capability is listed as Production that is In Build or Aspirational: disqualifying error — correct before proceeding

**Gate Step 6 — Prohibited Claims Cross-Check:**
Verify that no item listed in Section 6 (Prohibited Feature Claims Register) appears as an affirmative claim in Sections 1, 3, 5, 7, or 9. If an overlap is found: remove the affirmative claim from the section where it should not appear.

### 7.3 Pre-Release Quality Checklist

After passing all six gate steps:

**Claims integrity:**
- [ ] No In Build feature appears in Section 5 (POC Feature Set) as demonstrable without explicit "In Build — cannot be demonstrated" disclosure
- [ ] No Aspirational feature appears in Sections 1, 3, 5, 7, or 9
- [ ] No certification claim (SOC 2, ISO 27001, HIPAA) appears without explicit "In Build — not yet certified" caveat
- [ ] Section 6 (Prohibited) is present and complete

**Arithmetic and distribution:**
- [ ] Gate Step 1 passed: Section 2 average TFS matches the computed sum ÷ count
- [ ] Gate Step 2 passed: Section 2 distribution counts sum to total feature count
- [ ] Technical Characterisation in Section 2 matches the verified average TFS using the defined band thresholds

**Technical accuracy:**
- [ ] All TFS scores are consistent with the calibration table in Phase 3.2
- [ ] Section 4 documents all material constraints for this customer's deployment context
- [ ] Section 4 is not contradicted by any claim in Section 9

**Integration claims:**
- [ ] Gate Step 3 passed: all "Supported" claims in Section 3 have a source entry in Section 8
- [ ] No integration is claimed as "Supported" without a confirmed source
- [ ] "Not Confirmed" language is applied exactly as specified for all unverified integrations

**Evidence:**
- [ ] Gate Step 4 passed: all performance figures have a Section 8 source entry
- [ ] Gate Step 5 passed: all Production statuses verified
- [ ] Section 8 references no prohibited sources (capability-status.md, source-of-truth.md, ethana-status-reconciliation.md)

**Completeness:**
- [ ] Section 10 (Technical Summary) is written last and reflects the full analysis
- [ ] All sections required for this query type are present and substantive
- [ ] Output mode and language register match the declared output_mode

**Score against evaluation.md before releasing.**

---

## Decision Trees

### DT1 — Query Type Classification

```
Is the input a direct feature question or feature questions?
  → Query type: Feature Validation
  → Active phases: 1, 2, 3, 7
  → Required output sections: 1, 2, 4, 6, 8, 9, 10
  → Condensed output acceptable
  → Phase 4 at discretion if existing_stack provided; Phase 5 and 6 inactive

Is the input a technical requirements document, RFI, or feature questionnaire?
  → Query type: Technical Requirements Response
  → Active phases: 1, 2, 3, 4, 7
  → Required output sections: all ten
  → Full output required

Is the input an existing tool feature list (substitution request)?
  → Query type: Substitution Analysis
  → Active phases: 1, 2, 3, 4, 5, 7
  → Required output sections: all ten (Section 7 is the lead output)
  → Full output required

Is the input a proposed POC scope?
  → Query type: POC Feasibility Assessment
  → Active phases: 1, 2, 3, 4, 6, 7
  → Required output sections: 1, 2, 3, 4, 5, 6, 8, 10
  → Full output required for formal POC scope commitments

Is the input Section 3 from Ethana Solution Mapping?
  → Query type: Post-Solution-Mapping Technical Validation
  → Feature set is pre-determined by the upstream output; skip Phase 1 feature extraction
  → Active phases: 2, 3, 4, 6, 7 (add Phase 5 if existing_tool_feature_list also provided)
  → Required output sections: 1, 2, 3, 4, 5, 6, 8, 10
  → Full output required
```

### DT2 — Claims Firewall (Feature Level)

```
Is the feature confirmed as Production in canonical-product-model.md?
  YES → Route to Phase 3 (technical validation and TFS scoring). Proceed.

Is the feature confirmed as In Build in canonical-product-model.md?
  YES → Route to Section 6 (Prohibited Feature Claims Register).
         Label: "[Feature name] — In Build. Status: not available. Cannot be demonstrated or
         included in a POC scope. Cannot appear in a technical evaluation as available."
         Do not proceed to Phase 3. Do not assign a non-zero current TFS.
         If the customer asks about the roadmap: add "Anticipated TFS when shipped: [X]/100"
         as a footnote to Section 6 only — not to Section 1.

Is the feature confirmed as Aspirational in canonical-product-model.md?
  YES → Route to Section 6 (Prohibited Feature Claims Register).
         Label: "[Feature name] — Aspirational. Must not be described, demonstrated, or
         referenced as available in any output section at any level of technical discussion."
         Do not proceed to Phase 3. Do not annotate an anticipated TFS. Do not reference in
         Section 7 (Substitution Analysis) as an Ethana feature.

Is the feature not found in canonical-product-model.md?
  → Route to Section 6.
    Label: "[Feature name] — Status unconfirmed. Not present in canonical product model.
    Do not claim, validate technically, or include in POC scope. Verify with Ethana
    engineering before any use."
```

### DT3 — POC Readiness Gate

```
Is the feature confirmed as Production in canonical-product-model.md?
  NO → Exclude. Reason: "[Feature] is [In Build / Aspirational] — cannot be demonstrated."

Does the feature score Viable or Ready (TFS ≥ 70) for this specific requirement?
  TFS 50–69 (Partial) → Conditional Include.
    Document: "Include only if the following gap is acceptable to the customer: [specific gap].
    Test scenario covers the Partial coverage only — the gap remains undemonstratable."
  TFS < 50 (Thin or Not Viable) → Exclude.
    Reason: "TFS [X] — feature does not sufficiently address the requirement in this context."

Does the customer's deployment_constraint support this feature at the required performance level?
  NO → Conditional Include or Exclude depending on severity.
    If the constraint prevents any viable demonstration: Exclude.
    If the constraint limits but does not prevent: Conditional Include with explicit scope note.

Are the technical prerequisites for this feature met by the customer's environment?
  YES → Continue evaluation.
  NO — can be resolved within poc_duration → Conditional Include.
    State exactly: "Include if customer provides [specific prerequisite] before Day [N]."
  NO — cannot be resolved within poc_duration → Exclude.
    Reason: "Prerequisite [X] cannot be met within the [N]-day POC window."

Can this feature be meaningfully demonstrated within poc_duration (including setup time)?
  NO → Exclude. Reason: "Setup time for this feature exceeds the available POC window."

All gates passed → Include in Section 5 POC Feature Set with full test scenario.
```

### DT4 — Substitution Fit

```
Does Ethana have a Production feature that addresses this existing tool feature?
  NO → Does Ethana have an In Build feature anticipated to address it?
    YES → Gap today. In Section 7, label: "Gap — Ethana In Build coverage anticipated.
           No committed timeline. Customer should retain existing tool until In Build
           feature ships."
    NO → Gap. In Section 7: "Gap — no Ethana feature at any status level addresses
          this today." Recommend bridge or retention of existing tool.

  YES → Does the Production feature address it completely for this customer's use case?
    YES → Full Substitute.
           Document: what the customer gains; any workflow differences that are immaterial
           to the outcome; migration path.

    NO → What is the nature of the gap?
      Gap is minor (different UI, one edge-case sub-feature, format difference, non-core
      workflow difference) → Partial Substitute.
        Document the specific gap. State whether the customer must accept it or can bridge it.
        Provide a bridge recommendation if bridgeable.

      Gap is in a whole capability dimension (e.g., no custom policy authoring, no dataset
      management, no prompt playground) → evaluate whether the tools are designed to
      work alongside each other:
        YES (complementary architecture) → Complementary.
          Document how they integrate and what each handles.
        NO (substitution expectation but Ethana lacks it) → Partial Substitute with
          significant gap. Be explicit: "The customer loses [capability] — this is a
          material difference, not a workflow adjustment."
```

### DT5 — Integration Compatibility

```
Does canonical-product-model.md or product-architecture-investigation.md document an
integration with this stack component?
  YES → What type?
    Explicitly named as a SIEM export target (Splunk, Elastic, Datadog) →
      Supported — SIEM Export.
      Document: export format, endpoint configuration, what Ethana sends.
    
    Explicitly named as OIDC/SSO compatible (any OIDC-compliant identity provider) →
      Supported — OIDC/SSO.
      Document: protocol, what the customer must configure in their IdP.
      Note: SCIM provisioning is separate and In Build.
    
    Explicitly documented API or webhook integration →
      Supported — API/Webhook.
      Document: method, auth, data format.
    
    Named native connector →
      Supported — Native Connector.
      Document: connector name, protocol, configuration steps, schema.

  NO → Is there a general Ethana API that could support this integration in principle?
    YES → Not Confirmed — API Possible. Use exactly:
          "Integration with [Component] is not confirmed in the canonical product model.
          An API-based integration may be possible — verify with Ethana engineering before
          including in any customer-facing commitment."
    
    NO → Gap. Use exactly:
         "No integration path between Ethana and [Component] is documented in approved
         sources. Do not claim compatibility. Verify independently whether the customer
         can ingest Ethana SIEM export format into [Component] without a native connector."
```

---

## TFS Calibration Anchors

Reference these when assigning TFS scores. A score more than 20 points from a comparable anchor requires explicit justification.

| Feature | Requirement context | TFS | Band | Rationale |
|---|---|---|---|---|
| LLM Gateway | Latency budget > 100ms | 95 | Ready | ~50ms overhead is well within budget; routing is configurable |
| LLM Gateway | Latency budget < 30ms | 20 | Not Viable | ~50ms overhead exceeds the budget; feature cannot meet this requirement |
| Immutable Audit Log | Tamper-proof AI call record for regulatory examination | 90 | Ready | Insert-only write path; native SIEM export; field-level retention configurable |
| Immutable Audit Log | Real-time streaming to Kafka | 28 | Thin | SIEM export is event-based, not a real-time stream; Kafka not a confirmed target |
| Guardrails (all 6 scanners) | Runtime PII detection in LLM text outputs | 88 | Viable | Sub-200ms p95 combined; bidirectional; 6 production scanners; mandatory text-only caveat |
| Guardrails: PII Scanner | PII detection in structured database field values | 32 | Thin | Scanner operates on LLM text output only; structured data fields not in scope |
| Guardrails: Bias Scanner | Runtime bias signal detection in LLM outputs | 72 | Viable | Detects bias-related signals in LLM text outputs in production; known to be a runtime text filter |
| Guardrails: Bias Scanner | Formal statistical credit model bias audit | 18 | Not Viable | Runtime text filter; not a statistical model evaluation; does not satisfy RBI Fair Practices Code |
| Red Teaming Orchestrator | Automated adversarial probing across OWASP LLM Top 10 | 90 | Ready | 21 probes in production; comprehensive coverage |
| Red Teaming Orchestrator | CI/CD gate integration for automated release checks | 0 | Not Viable | CI/CD gate is In Build |
| MCP Security Broker (core) | LLM call tracing for MCP-compatible agent pipelines | 72 | Viable | Core tracing is Production; requires MCP-compatible runtime; NHI is In Build |
| MCP Security Broker (core) | Non-human identity lifecycle management | 15 | Not Viable | NHI module is In Build; core broker does not manage agent identity lifecycle |
| Account Management: SSO/OIDC | OIDC-based SSO with Azure AD or Okta | 85 | Viable | SSO/OIDC is Production; standard OIDC/SAML integration; customer configures IdP app |
| Account Management: SCIM | Automated SCIM user provisioning | 0 | Not Viable | SCIM is In Build |
| On-prem Deployment | Data residency in customer-controlled infrastructure | 80 | Viable | On-prem is Production; single-node constraint applies — document for high-volume requirements |
| Cost and Budget Tracking | Per-tenant LLM spend tracking | 85 | Viable | Per-tenant tracking is Production; per-user tracking is In Build |

---

## Output Section Templates

### Section 2 — Technical Fit Summary (arithmetic format)

```
## 2. Technical Fit Summary

**Average TFS (arithmetic verification):**
[TFS1] + [TFS2] + [TFS3] + ... + [TFSn] = [sum]
[sum] ÷ [n features] = [average]

**Distribution:**
| Band | Score range | Count | Features |
|---|---|---|---|
| Ready | 90–100 | [n] | [feature names] |
| Viable | 70–89 | [n] | [feature names] |
| Partial | 50–69 | [n] | [feature names] |
| Thin | 25–49 | [n] | [feature names] |
| Not Viable | 0–24 | [n] | [feature names] |
| **Total** | | **[n]** | |

**Technical Characterisation:** [POC-Ready / POC-Ready with Conditions / Limited POC Scope / Not POC-Ready]

**Coverage story:** [2–3 sentences: what the average and distribution mean for the customer's situation; what conditions or exclusions apply; what the solution architect should know before the next customer conversation]
```

### Section 8 — Evidence References (table format)

```
## 8. Evidence References

| Claim | Source | Section |
|---|---|---|
| [Specific quoted or paraphrased claim] | canonical-product-model.md — [capability name] | [Section N] |
| [Specific quoted or paraphrased claim] | product-architecture-investigation.md — [section name] | [Section N] |
| [Claim flagged as unconfirmed] | Not found in approved sources — flagged as unconfirmed | [Section N] |

**Sources used in this output:**
- canonical-product-model.md: [yes / no]
- product-architecture-investigation.md: [yes / no]
- use-cases.md: [yes / no]
- Engineering confirmation: [yes — date / no]

**Prohibited sources — confirmed not used:**
- capability-status.md: not used
- source-of-truth.md: not used
- ethana-status-reconciliation.md: not used
- Marketing playbook (for status or performance claims): not used
```
