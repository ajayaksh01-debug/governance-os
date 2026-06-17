# Ethana Feature Mapping — Worked Examples

Three complete worked examples. Each demonstrates all ten output sections and the mandatory arithmetic gate. Use these as calibration anchors when scoring outputs.

---

# Example 1: BFSI Audit Log Deep Dive

**Context:** Indian private bank. Enterprise architect submits five specific technical questions about the Immutable Audit Log as part of a pre-POC technical due diligence exercise. This follows a completed Solution Mapping engagement where the Audit Log was included in Section 3.

**Input:**
```
feature_question: Five questions about the Immutable Audit Log:
  Q1. What fields does the Audit Log event record capture? Can we add custom fields?
  Q2. What is the data retention policy? Can it be configured?
  Q3. How does the Splunk HEC connector work? What must we configure on our side?
  Q4. What is the write throughput at 50,000 LLM calls per day on an on-premises deployment?
  Q5. Is the insert-only guarantee enforced at the application layer, the database layer, or both?

customer_sector: BFSI
deployment_constraint: On-prem
volume_parameters: 50,000 LLM calls per day
existing_stack: Splunk (existing SIEM)
output_mode: Technical Evaluation
```

**Query type:** Feature Validation (condensed) — Phases 1, 2, 3, 4, 7

---

## 1. Feature Validation Table

| # | Feature queried | Status | TFS | Evidence |
|---|---|---|---|---|
| Q1 | Audit Log: Event Schema and Custom Fields | Production | 72 | canonical-product-model.md — Immutable Audit Log entry |
| Q2 | Audit Log: Retention Policy Configurability | Production | 80 | canonical-product-model.md — Immutable Audit Log entry |
| Q3 | Audit Log: Splunk HEC Connector | Production | 78 | canonical-product-model.md — Immutable Audit Log entry; SIEM export section |
| Q4 | Audit Log: Write Throughput at 50K calls/day On-prem | Production | 42 | canonical-product-model.md — Deployment Models entry (on-prem single-node caveat) |
| Q5 | Audit Log: Immutability Enforcement Layer | Production | 82 | canonical-product-model.md — Immutable Audit Log entry |

**Q1 — Audit Log: Event Schema and Custom Fields**
**Status:** Production | **TFS:** 72 (Viable)
**Technical description:** The Immutable Audit Log captures a standard event record for every LLM call routed through the Ethana Gateway. Captured fields include: request metadata (timestamp, tenant ID, model ID, routing path), request body or a configurable hash/redacted form, response body or a configurable redacted form, guardrail scanner dispositions (scanner name, verdict, latency), gateway processing time, and user or session identifier where available. Retention period is configurable per tenant (see Q2). Field names within the configurable set are adjustable; the core event structure (which fields exist in the record) is fixed by the platform.
**Hard technical constraint:** Custom field addition is not supported — fields outside the configurable set cannot be injected into the event record. A bank requiring a custom regulatory tag field (e.g., a loan-application-ID or regulatory-purpose-code) must either map this to an existing configurable field or track it separately in an upstream system that joins against the Audit Log's call identifier. This is the most common schema limitation raised by BFSI customers during technical due diligence.
**TFS rationale:** 72 (Viable) — schema is comprehensive and configurable within defined limits; the fixed-structure constraint is a real limitation but does not prevent use for RBI audit evidence purposes, where the standard call metadata and scanner disposition chain is what examiners look for.

**Q2 — Audit Log: Retention Policy Configurability**
**Status:** Production | **TFS:** 80 (Viable)
**Technical description:** Retention policy is configurable per tenant. The bank sets the retention period at onboarding and can modify it. Retention is applied to the event store — events older than the retention period are eligible for deletion. The insert-only property applies during the retention period; deletion after expiry is a standard data lifecycle operation, not a modification of the audit record. For BFSI customers subject to RBI audit trail requirements, retention should be set to align with the applicable record-keeping obligation (typically 5–7 years for credit-related AI decisions).
**Hard technical constraint:** Retention configuration controls how long records are kept, not the granularity at which they are kept — all events are retained equally; selective retention (keep some call types longer than others) is not supported within the standard configuration. If a bank needs differential retention by call type, this would require a downstream data pipeline with selective archival.
**TFS rationale:** 80 (Viable) — retention is configurable and meets the standard BFSI use case; differential retention is a gap but is rarely a hard requirement at due diligence stage.

**Q3 — Audit Log: Splunk HEC Connector**
**Status:** Production | **TFS:** 78 (Viable)
**Technical description:** The Audit Log supports SIEM export to Splunk via the Splunk HTTP Event Collector (HEC) protocol. Events are forwarded from Ethana's event store to the customer's Splunk deployment. The customer must configure: a Splunk HEC endpoint URL, a Splunk HEC token with write permissions to the target index, the target Splunk index name, and the event source type mapping. Ethana sends events in JSON format over HTTPS. Ethana-side configuration requires the customer to provide the HEC endpoint, token, and index in the Ethana tenant configuration panel.
**Hard technical constraint:** The SIEM export is event-based (export on write), not a real-time streaming connection. Splunk receives events as they are written to the Audit Log. There is no Splunk native app or Splunk-native data model from Ethana — the customer's Splunk team must build or adapt dashboards and saved searches against the Ethana event schema. For an RBI examiner demonstration, the bank should plan time to build at least a basic Splunk dashboard mapping Audit Log fields to the examiner's evidence checklist before the demonstration.
**TFS rationale:** 78 (Viable) — integration is confirmed and operational; customer-side Splunk configuration and dashboard build is a normal integration step that does not indicate a gap.

**Q4 — Audit Log: Write Throughput at 50,000 LLM Calls/Day On-prem**
**Status:** Production | **TFS:** 42 (Thin)
**Technical description:** The Ethana on-prem deployment model runs on a single-node architecture. At 50,000 LLM calls per day — approximately 0.58 calls per second on average with burst capacity depending on the intraday distribution — the write volume to the Audit Log is within typical ranges for a single-node deployment. However, the canonical product model does not state a specific throughput ceiling for on-prem deployments, and throughput at sustained peak periods (e.g., 500–1,000 simultaneous credit analysis calls during a peak business window) is not confirmed in approved sources.
**Hard technical constraint:** On-prem single-node constraint is documented in canonical-product-model.md. The specific throughput ceiling at this deployment model is not quantified. A bank with bursty intraday traffic profiles — common in credit AI where the morning underwriting window generates a significant proportion of the daily call volume — should verify peak throughput capacity with Ethana engineering before committing to on-prem deployment for this volume. Do not state a throughput guarantee in any customer-facing document without engineering confirmation.
**TFS rationale:** 42 (Thin) — the on-prem deployment model is Production and the average volume is plausible, but the unconfirmed throughput ceiling at peak is a real risk for a BFSI deployment where the Audit Log is a regulatory evidence store. "It will probably work" is not the standard for a bank presenting to an RBI examiner.

**Q5 — Audit Log: Immutability Enforcement Layer**
**Status:** Production | **TFS:** 82 (Viable)
**Technical description:** The Audit Log uses an insert-only write path. Events are written and cannot be modified or deleted within the retention period through normal application operations. The "insert-only" characterisation in canonical-product-model.md describes the application-layer behaviour — the write API accepts only insert operations; update and delete operations on audit records are not exposed through the platform API. Whether the underlying data store enforces immutability at the database layer (append-only storage engine, write-once media, or hardware-enforced WORM) is not specified in canonical-product-model.md and cannot be confirmed without engineering input.
**Hard technical constraint:** The distinction between application-layer immutability (API enforces insert-only) and database-layer immutability (storage engine enforces insert-only independently of the application) is material for a bank whose internal audit function or RBI examiner asks how immutability is enforced. Application-layer enforcement means a compromised application instance could theoretically modify the underlying store if it bypassed the API. Database-layer enforcement is stronger. This question should be escalated to Ethana engineering before the bank uses the Audit Log as a sole tamper-evidence control in a regulatory evidence argument.
**TFS rationale:** 82 (Viable) — insert-only at the application layer is a strong control and is production-confirmed; the DB-layer distinction is a clarification question, not a disqualifying limitation, for most RBI audit evidence contexts.

---

## 2. Technical Fit Summary

**Average TFS (arithmetic verification):**
72 (Q1) + 80 (Q2) + 78 (Q3) + 42 (Q4) + 82 (Q5) = 354
354 ÷ 5 features = 70.8

**Distribution:**

| Band | Score range | Count | Features |
|---|---|---|---|
| Ready | 90–100 | 0 | — |
| Viable | 70–89 | 4 | Q1 Schema (72), Q2 Retention (80), Q3 Splunk HEC (78), Q5 Immutability (82) |
| Partial | 50–69 | 0 | — |
| Thin | 25–49 | 1 | Q4 On-prem Throughput (42) |
| Not Viable | 0–24 | 0 | — |
| **Total** | | **5** | |

**Technical Characterisation:** POC-Ready with Conditions (average TFS 70.8, in the 55–74 band)

**Coverage story:** The Immutable Audit Log is technically fit for an Indian BFSI context on four of the five queried dimensions. The one constraint requiring attention before POC commitment is the on-prem single-node throughput ceiling: 50,000 calls/day is plausible in aggregate, but the burst-hour throughput profile is unconfirmed. The bank should validate peak throughput with Ethana engineering — this is a verification step, not a blocker. On the immutability question (Q5), the solution architect should clarify with engineering whether immutability is enforced at the DB layer before the bank positions the Audit Log as a tamper-proof evidence control to an RBI examiner.

---

## 3. Integration Compatibility Assessment

### Splunk (existing SIEM)

**Integration type:** Supported — SIEM Export
**Protocol:** HTTP Event Collector (HEC) over HTTPS
**Customer configuration required:**
1. Create a Splunk HEC input in Splunk Web (Settings > Data Inputs > HTTP Event Collector)
2. Generate a HEC token with write permissions to the target index
3. Note the HEC endpoint URL (typically `https://[splunk-host]:8088/services/collector`)
4. Create or designate the target Splunk index
5. Provide endpoint URL, token, and index name to the Ethana tenant configuration

**What Ethana sends:** JSON event records per Audit Log schema; one event per LLM call; event timestamp is the UTC time of the gateway call; events are sent on write, not batched.

**Schema mapping:** Ethana does not provide a pre-built Splunk data model. The bank's Splunk team must build field extractions and a summary dashboard. Suggested mapping for RBI audit evidence: `call_id` → unique event identifier; `tenant_id` → business unit; `model_id` → AI system identifier; `guardrail_dispositions[]` → scanner control evidence; `response_hash` → output integrity reference.

**Evidence source:** canonical-product-model.md — SIEM export targets (Splunk, Elastic, Datadog)

---

## 4. Technical Constraints and Caveats

1. **Audit Log schema is fixed-structure:** Fields within the configurable set (names, redaction settings, retention) are adjustable; additional fields cannot be added. The bank cannot inject a regulatory-purpose-code or loan-application-ID directly into the event record without mapping to an existing field or external join.

2. **On-prem single-node throughput ceiling is unconfirmed:** The canonical model does not quantify a throughput ceiling for on-prem deployments. Burst-hour credit AI traffic may exceed single-node write capacity. Verify with Ethana engineering before finalising the POC architecture for high-volume on-prem deployments.

3. **Immutability layer is application-layer only (as documented):** The canonical model confirms insert-only API behaviour. Whether the underlying storage engine enforces immutability independently is not confirmed. This distinction matters for a regulatory tamper-evidence argument. Verify with Ethana engineering.

4. **Splunk HEC export is event-on-write, not streaming:** The SIEM export writes events as they are created. There is no Kafka stream or streaming API. Splunk receives events with a latency equal to the write path time.

5. **SCIM provisioning is In Build:** Azure AD or Okta SSO/OIDC integration is Production; automated SCIM user provisioning is not yet available. User lifecycle management during the POC and initial deployment must be manual via the Ethana admin console.

6. **Retention applies uniformly — differential retention by call type is not supported:** The retention period is configured globally per tenant, not per call category, AI system, or use case. A bank with multiple AI deployments at different regulatory retention obligations (e.g., 5 years for credit AI decisions, 7 years for AML-related AI activity) cannot enforce different retention periods within a single Ethana tenant in the standard configuration. If differential retention is required, a downstream archival pipeline with selective filtering against the event record's call metadata would be needed.

7. **Splunk integration requires customer-built data model and dashboards:** Ethana does not provide a pre-built Splunk app or native Splunk data model. The bank's Splunk team must build field extractions and dashboards against the Ethana JSON event schema before the SIEM integration is usable for reporting or examiner demonstrations. For a BFSI RBI evidence demonstration, plan 2–3 days of Splunk team effort to build a baseline dashboard mapping Audit Log fields to the examiner's evidence checklist.

---

## 5. POC Feature Set

*Not applicable — no poc_scope was provided with this input. For POC scope validation using the Audit Log, run Ethana Feature Mapping with `poc_scope` or `upstream_skill_output` as the primary input. Refer to Example 3 for a full POC scope validation that includes the Audit Log.*

---

## 6. Prohibited Feature Claims Register

| Feature | Status | Prohibition |
|---|---|---|
| SCIM automated user provisioning | In Build | Cannot be demonstrated; cannot appear in POC scope; cannot appear in technical evaluation as available |
| SOC 2 Type II certification | In Build | Cannot be claimed as a current certification; must be disclosed as In Build if raised by the evaluator |
| ISO 27001 certification | In Build | Cannot be claimed as a current certification; must be disclosed as In Build if raised by the evaluator |
| Ethana Edge (all capabilities) | In Build | Cannot be demonstrated; cannot be described as currently available; do not reference in any technical evaluation, RFI response, or POC scope as an available capability |
| Ethana Workspace (all features) | Aspirational | Must not be described or referenced as available or demonstrable in any context |
| Visual Agent Builder | Aspirational | Must not be described or referenced as available or demonstrable in any context |

---

## 7. Substitution Analysis

*Not applicable — no existing_tool_feature_list was provided with this input.*

---

## 8. Evidence References

| Claim | Source | Section |
|---|---|---|
| Audit Log is insert-only; captures request metadata, response, scanner dispositions, gateway latency | canonical-product-model.md — Immutable Audit Log capability entry | Sections 1, 9 |
| Field names and retention period are configurable within the standard event record structure | canonical-product-model.md — Immutable Audit Log capability entry | Sections 1, 4 |
| SIEM export targets: Splunk, Elastic, Datadog — confirmed | canonical-product-model.md — Immutable Audit Log, SIEM export section | Sections 1, 3 |
| On-prem deployment is single-node — throughput ceiling not quantified in canonical model | canonical-product-model.md — Deployment Models entry | Sections 1, 4 |
| Insert-only is documented as application-layer behaviour; DB-layer enforcement not stated | canonical-product-model.md — Immutable Audit Log capability entry | Sections 1, 4 |
| Splunk HEC protocol (HTTPS JSON event forwarding) | canonical-product-model.md — Immutable Audit Log SIEM export | Section 3 |
| SCIM is In Build; SSO/OIDC is Production | canonical-product-model.md — Account Management capability entry | Section 6 |
| On-prem throughput at 50K calls/day — NOT confirmed in approved sources | Not found in approved sources — flagged as unconfirmed | Section 4 |
| DB-layer vs. application-layer immutability distinction — NOT confirmed in approved sources | Not found in approved sources — flagged as unconfirmed; verify with Ethana engineering | Sections 1, 4 |

**Sources used:** canonical-product-model.md: yes | product-architecture-investigation.md: no | use-cases.md: no | Engineering confirmation: no

**Prohibited sources — confirmed not used:** capability-status.md: not used | source-of-truth.md: not used | ethana-status-reconciliation.md: not used | Marketing playbook (for status or performance claims): not used

---

## 9. Technical Proposal Language

### Immutable Audit Log — Insert-Only Event Record

"Ethana's Immutable Audit Log captures every LLM call routed through the Ethana Gateway in an insert-only event store. Each event record includes the call timestamp, tenant and model identifiers, a configurable representation of the request and response (full content or configurable redacted/hashed form), the disposition of all active guardrail scanners applied to the call (scanner name, verdict, latency), and the gateway processing time. Events are written to the store via an insert-only write path — the Ethana API exposes no update or delete operations for audit records within the retention period.

**Mandatory caveat:** The Audit Log's insert-only property is enforced at the application layer. Whether the underlying data store enforces immutability independently of the application layer is not confirmed — if your audit committee or regulatory examiners require DB-layer or hardware-level WORM enforcement, verify the specific implementation with Ethana engineering before positioning the Audit Log as a sole tamper-evidence control."

### Immutable Audit Log — SIEM Export (Splunk)

"The Audit Log exports events to Splunk via the HTTP Event Collector (HEC) protocol. Each event is forwarded on write as a JSON record. Customer configuration required: a Splunk HEC endpoint URL, an HEC token with write permissions to the designated index, and the target index name. Ethana sends events over HTTPS. The bank's Splunk team builds field extractions and dashboards against the Ethana event schema — Ethana does not provide a pre-built Splunk app or data model.

**Mandatory caveat:** The SIEM export is event-on-write; it is not a real-time streaming connection and does not support Kafka or a native streaming protocol. On-prem single-node throughput at peak credit-analysis-window call volumes (50,000 calls/day in aggregate; burst-hour peak is unconfirmed) should be validated with Ethana engineering before the bank commits on-prem deployment for this volume."

### Audit Log — Retention Policy

"Retention period is configurable per tenant at onboarding. The bank sets the retention period to align with its regulatory record-keeping obligations (RBI guidance for credit AI-related records is typically five to seven years). Retention is applied uniformly across all event types — selective retention by call type within the same tenant is not supported in the standard configuration."

### Audit Log — On-premises Write Throughput (Q4 — Thin: TFS 42)

"The Ethana Audit Log on-premises deployment uses a single-node architecture. At a sustained average of 50,000 LLM calls per day — approximately 0.58 calls per second — average write volume to the event store is within the plausible range for a single-node deployment. However, the Ethana canonical product model does not confirm a throughput ceiling for on-premises deployments. Write performance at concentrated burst-hour volumes — for example, 500–1,000 simultaneous credit analysis calls during the morning underwriting window — cannot be stated as confirmed based on approved product documentation.

**Mandatory caveat — do not commit to on-premises deployment for this volume without engineering confirmation:** The on-premises single-node write throughput ceiling is not quantified in approved Ethana product documentation. Before finalising the POC architecture or any production deployment commitment for on-premises at 50,000 calls/day, the bank should: (1) share the intraday call distribution profile with Ethana engineering; (2) request explicit confirmation that the on-prem single-node architecture supports the peak burst-hour write rate; (3) include a throughput validation test in the POC scope before committing to on-prem as the production deployment model. If the bank's compliance position requires a confirmed write-availability guarantee for the Audit Log as a regulatory evidence store, this engineering confirmation is a prerequisite to any formal deployment commitment, not a post-POC step."

---

## 10. Technical Summary

The Immutable Audit Log is technically fit for an Indian BFSI on-premises deployment across four of five queried dimensions, scoring Viable on schema comprehensiveness, retention configurability, Splunk HEC integration, and insert-only immutability. One question — write throughput at the declared 50,000 calls/day on a single-node on-prem deployment — scores Thin (TFS 42) because the canonical product model does not confirm the throughput ceiling for on-prem deployments, creating unresolved risk for a bank with a concentrated intraday credit analysis window.

Recommended next step: the solution architect should schedule a 30-minute technical call with Ethana engineering to confirm (a) on-prem single-node write throughput ceiling at the bank's peak-hour call rate, and (b) whether Audit Log immutability is enforced at the database layer or only at the application layer. Both questions can be resolved before POC commitments are made. The Splunk SIEM integration is straightforward and the bank's Splunk team should allow two to three days to build field extractions and a basic RBI evidence dashboard against the Ethana event schema.

---
---

# Example 2: LangSmith Substitution Analysis

**Context:** General enterprise SaaS company (approximately 500 employees). The AI platform team is evaluating whether to replace LangSmith with Ethana Build for LLM observability and governance. They submit a list of LangSmith features they currently use and want to know the Ethana substitution picture.

**Input:**
```
existing_tool_feature_list:
  Tool: LangSmith (by LangChain)
  Features used:
  F1. LLM call tracing — traces, spans, run trees; correlation across multi-step agent calls
  F2. Latency and cost tracking — per model, per prompt, per team; budget alerts
  F3. Prompt playground — interactive prompt testing and version management
  F4. Dataset management — test datasets for offline evaluation and regression testing
  F5. Custom evaluators — user-defined evaluation functions and LLM-as-judge scoring
  F6. Export and webhooks — export to SIEM; webhook for external alerting
  F7. Multi-model routing — model fallback on error; latency-based routing

customer_sector: General Enterprise
deployment_constraint: Cloud
output_mode: Technical Evaluation
```

**Query type:** Substitution Analysis — all phases active

---

## 1. Feature Validation Table

| # | Ethana feature | Status | TFS | Evidence |
|---|---|---|---|---|
| F1 | Immutable Audit Log (LLM call tracing) | Production | 85 | canonical-product-model.md — Immutable Audit Log |
| F2 | Cost and Budget Tracking (spend tracking) | Production | 82 | canonical-product-model.md — Cost and Budget Tracking |
| F3 | No Ethana Production equivalent (Prompt Playground) | — | 0 | canonical-product-model.md — no prompt playground in Build |
| F4 | No Ethana Production equivalent (Dataset Management) | — | 0 | canonical-product-model.md — no dataset management in Build |
| F5 | Guardrails: 6 Production Scanners (Custom Evaluators) | Production | 55 | canonical-product-model.md — Runtime Guardrails |
| F6 | Immutable Audit Log: SIEM Export (Export and webhooks) | Production | 90 | canonical-product-model.md — Immutable Audit Log |
| F7 | LLM Gateway (Multi-model routing) | Production | 65 | canonical-product-model.md — LLM Gateway |

**F1 — Immutable Audit Log vs. LLM Call Tracing**
**Status:** Production | **TFS:** 85 (Viable)
**Technical description:** The Audit Log captures every Gateway-routed LLM call in an insert-only event store with call metadata, request/response representations, scanner dispositions, and latency. For multi-step agent calls routed through the Ethana Gateway, each individual LLM call in the agent's execution is captured as a separate event linked by session or call-chain identifier.
**Constraint:** The Audit Log is a compliance-oriented event record, not a developer observability tool. LangSmith's trace waterfall view with span nesting, run tree visualisation, and interactive trace exploration is a developer debugging interface — Ethana does not have a comparable frontend UI. The bank of data is equivalent or richer (insert-only vs. mutable LangSmith traces); the interface for exploring that data must be built on top of the Splunk/Elastic/Datadog export. Engineers who use LangSmith's trace UI daily will feel the absence.

**F2 — Cost and Budget Tracking vs. Latency and Cost Tracking**
**Status:** Production | **TFS:** 82 (Viable)
**Technical description:** Ethana's Cost and Budget Tracking is Production for per-tenant spend tracking. Model-level cost breakdown is included where model pricing is configured. Budget alerts are a standard feature.
**Constraint:** Per-user cost tracking is In Build — LangSmith supports per-user attribution which Ethana cannot match today. Team-level rollup is available via tenant configuration; individual user attribution within a tenant is not.

**F3 — Prompt Playground**
**Status:** No Ethana Production equivalent | **TFS:** 0 (Not Viable)
**Technical description:** N/A — Ethana has no prompt playground, prompt version management, or interactive prompt testing interface in Production. This capability exists in Ethana Workspace (Aspirational) but Workspace must not be referenced as available.
**Constraint:** This is a Gap. The customer must retain LangSmith for this use case or adopt a separate prompt engineering tool (PromptLayer, Promptfoo, or equivalent). Do not describe Workspace as covering this feature.

**F4 — Dataset Management**
**Status:** No Ethana Production equivalent | **TFS:** 0 (Not Viable)
**Technical description:** N/A — Ethana has no dataset management, test set curation, or offline regression evaluation framework in Production. This capability does not exist in Ethana Build or any current status tier.
**Constraint:** This is a Gap with no Ethana roadmap coverage confirmed. Customer must retain LangSmith for offline evaluation workflows or adopt a separate evaluation framework (Promptfoo, RAGAS, or equivalent).

**F5 — Guardrails: 6 Production Scanners vs. Custom Evaluators**
**Status:** Production | **TFS:** 55 (Partial)
**Technical description:** Ethana has six production guardrail scanners: PII, Prompt Injection, Jailbreak, Toxicity, Bias, and Secret Leakage. These run bidirectionally on every Gateway-routed call at sub-200ms p95 combined. Each scanner produces a binary verdict (flagged / not flagged) with the disposition captured in the Audit Log.
**Constraint:** LangSmith's custom evaluators allow user-defined evaluation logic and LLM-as-judge scoring — arbitrary evaluation functions the engineering team writes. Ethana's six scanners are configurable (sensitivity thresholds, enable/disable per tenant) but not custom — the bank cannot write a new scanner or evaluation function. A team that relies on LLM-as-judge scoring for quality evaluation, domain-specific compliance checks (legal language, financial advice disclaimers), or regression scoring will find Ethana's scanner set insufficient. The six scanners cover the security and safety dimensions; they do not cover quality, domain accuracy, or custom policy evaluation.

**F6 — Immutable Audit Log: SIEM Export vs. Export and Webhooks**
**Status:** Production | **TFS:** 90 (Ready)
**Technical description:** The Audit Log natively exports to Splunk, Elastic, and Datadog via HEC/API. Every LLM call event is exported on write. The insert-only property means what arrives in the SIEM cannot be retroactively modified by the Ethana application — LangSmith's export does not offer this immutability guarantee. For an organisation with compliance or audit obligations, the SIEM export is a capability improvement over LangSmith's export.
**Constraint:** Webhook-based alerting (for real-time external notification on specific events) is not confirmed as a specific feature in the canonical model. SIEM export covers the majority of export use cases. Verify webhook support with Ethana engineering if real-time external alerting is a hard requirement.

**F7 — LLM Gateway vs. Multi-model Routing**
**Status:** Production | **TFS:** 65 (Partial)
**Technical description:** The Ethana LLM Gateway routes requests to LLM providers with approximately 50ms overhead. Gateway-level routing is Production.
**Constraint:** Whether the Gateway supports model fallback on provider error (automatic retry to a secondary model when the primary returns 5xx) and latency-based routing (routing to the model with lower observed latency) is not confirmed in the canonical product model for these specific routing policy types. LangSmith's model routing features include explicit fallback chains and latency-optimised routing. Verify whether these specific routing behaviours are available in the Ethana Gateway with Ethana engineering — do not claim equivalence without confirmation.

---

## 2. Technical Fit Summary

**Average TFS (arithmetic verification):**
85 (F1) + 82 (F2) + 0 (F3) + 0 (F4) + 55 (F5) + 90 (F6) + 65 (F7) = 377
377 ÷ 7 features = 53.9

**Distribution:**

| Band | Score range | Count | Features |
|---|---|---|---|
| Ready | 90–100 | 1 | F6 SIEM Export (90) |
| Viable | 70–89 | 2 | F1 Audit Log/Tracing (85), F2 Cost Tracking (82) |
| Partial | 50–69 | 2 | F5 Guardrails/Evaluators (55), F7 Gateway/Routing (65) |
| Thin | 25–49 | 0 | — |
| Not Viable | 0–24 | 2 | F3 Prompt Playground (0), F4 Dataset Management (0) |
| **Total** | | **7** | |

**Technical Characterisation:** Limited POC Scope (average TFS 53.9, in the 35–54 band)

**Coverage story:** Ethana Build is a strong substitute for LangSmith on the compliance and audit dimensions — SIEM export is an improvement (insert-only, Ready), call tracing coverage is Viable, and cost tracking is Viable with a per-user gap. The substitution breaks down on developer tooling: prompt playground and dataset management are complete Gaps with no Ethana Production equivalent, and custom evaluators are a Partial at best (six fixed scanners vs. arbitrary evaluation logic). The recommendation is a targeted substitution, not a full replacement: Ethana covers the compliance, security, and gateway layers; LangSmith or a separate tool is retained for prompt engineering and offline evaluation workflows.

---

## 3. Integration Compatibility Assessment

*Not applicable in this query context — the customer's existing stack beyond LangSmith was not specified. For integration compatibility with the customer's SIEM, IdP, or CI/CD stack, run with `existing_stack` populated.*

---

## 4. Technical Constraints and Caveats

1. **Prompt Playground — Gap, no Ethana equivalent:** Teams who use LangSmith's interactive prompt testing interface daily have no Ethana equivalent. This is not a roadmap gap — it is a persistent difference in product scope. Budget for a separate prompt engineering tool if this workflow is retained.

2. **Dataset Management — Gap, no Ethana equivalent at any status tier:** Offline regression evaluation and test dataset curation are not part of the Ethana Build scope in any current status tier. Evaluate Promptfoo, RAGAS, or Braintrust for this workflow.

3. **Custom Evaluators — Partial, not equivalent:** Ethana's six scanners are pre-built and configurable but not extensible. A team with domain-specific evaluation requirements (legal disclaimer presence, financial advice scope compliance, brand tone scoring) cannot implement these as Ethana scanner rules. This is a real capability loss from LangSmith custom evaluators and LLM-as-judge scoring.

4. **Per-user cost tracking — In Build:** Per-tenant cost tracking is Production; per-user attribution within a tenant is In Build. Teams that do per-engineer or per-feature-team cost attribution in LangSmith will lose this granularity until the In Build feature ships.

5. **Model fallback and latency-based routing — Not confirmed:** The specific LangSmith routing policies (fallback chains, latency-optimised routing) are not confirmed as Gateway features. Do not claim equivalent routing capability without engineering verification.

6. **Audit Log UI — No developer trace explorer:** The Audit Log is a compliance event store with a SIEM export. It does not include a LangSmith-style trace waterfall UI. Engineers debugging agent call flows will need to query the SIEM dashboard — a workflow adjustment that requires Splunk/Datadog proficiency.

---

## 5. POC Feature Set

*Not applicable — no poc_scope was provided with this input. If the customer wants to run a POC of the Ethana features that are Full or Partial Substitutes, provide a poc_scope input specifying the features, timeline, and success criteria. Example 3 demonstrates a full POC scope validation.*

---

## 6. Prohibited Feature Claims Register

| Feature | Status | Prohibition |
|---|---|---|
| Prompt Playground / Prompt Version Management | Not in Ethana Build at any tier | Must not be described as available; Workspace does not cover this; do not claim an Ethana equivalent |
| Dataset Management / Offline Evaluation | Not in Ethana Build at any tier | Must not be described as available; do not claim an Ethana equivalent |
| LLM-as-judge scoring / Custom Evaluators (user-defined) | Not in Ethana Build at any tier | Must not be claimed; the six Production scanners are not equivalent to arbitrary evaluation logic |
| Per-user cost tracking | In Build | Cannot be demonstrated or claimed as available |
| SCIM provisioning | In Build | Cannot be demonstrated; SSO/OIDC is Production but SCIM is not |
| SOC 2 Type II certification | In Build | Cannot be claimed as current |
| Ethana Workspace (all features) | Aspirational | Must not be used to cover any Gap in the substitution analysis; must not be referenced as available |
| Visual Agent Builder | Aspirational | Must not be referenced |
| Model fallback / latency routing | Not confirmed in canonical model | Cannot be claimed without engineering confirmation; do not use to claim F7 as a Full Substitute |

---

## 7. Substitution Analysis

| LangSmith Feature | Category | Ethana equivalent | Customer gains | Customer loses |
|---|---|---|---|---|
| F1: LLM call tracing | Full Substitute | Immutable Audit Log | Insert-only tamper-proof record; compliance-grade evidence chain; native SIEM export | Interactive trace waterfall UI; span nesting UI; developer debugging workflow requires SIEM queries |
| F2: Latency and cost tracking | Partial Substitute | Cost and Budget Tracking | Per-tenant cost tracking; budget alerts | Per-user attribution (In Build — not available today) |
| F3: Prompt playground | Gap | None | — | Full prompt testing and version management workflow |
| F4: Dataset management | Gap | None | — | Offline regression test datasets and evaluation runs |
| F5: Custom evaluators | Partial Substitute | Guardrails (6 scanners) | Six production security/safety scanners with sub-200ms p95; bidirectional; audit log integration | Custom evaluation logic; LLM-as-judge scoring; domain-specific evaluation functions |
| F6: Export and webhooks | Full Substitute (improvement) | Audit Log SIEM Export | Insert-only immutability guarantee on exported data; confirmed Splunk, Elastic, Datadog targets; compliance-grade export | Webhook-based real-time alerting (verify with engineering) |
| F7: Multi-model routing | Partial Substitute | LLM Gateway | Gateway-level routing; ~50ms overhead; all calls through a single audited path | Confirmed model fallback chains and latency-optimised routing (not confirmed — verify with engineering) |

**Migration path for Full Substitutes (F1, F6):**

F1 — Audit Log tracing: Export the LangSmith trace archive before cutover if historical traces are needed (LangSmith export formats are JSON). After cutover, all new call traces are in the Ethana Audit Log and exported to the customer's SIEM. Build Splunk/Datadog dashboards before cutover using a test tenant to validate schema mapping. Plan two to four weeks for the Splunk team to build equivalent query surfaces.

F6 — SIEM Export: Configure Ethana's SIEM export connector at the same time as Gateway deployment. No data migration — existing LangSmith export data stays in the SIEM; new Ethana export data begins from Gateway onboarding date.

**Bridge recommendations for Gaps (F3, F4):**

F3 — Prompt Playground: Retain LangSmith's prompt playground, or adopt Promptfoo (open source, runs against any LLM endpoint) or PromptLayer. These tools can coexist with an Ethana gateway deployment.

F4 — Dataset Management: Retain LangSmith's dataset management, or adopt Promptfoo's dataset evaluation module, RAGAS (for RAG evaluation), or Braintrust. These are standalone evaluation frameworks and do not conflict with Ethana.

---

## 8. Evidence References

| Claim | Source | Section |
|---|---|---|
| Audit Log: insert-only event store; captures call metadata, scanner dispositions; SIEM export to Splunk, Elastic, Datadog | canonical-product-model.md — Immutable Audit Log entry | Sections 1, 7, 9 |
| Cost and Budget Tracking: per-tenant Production; per-user In Build | canonical-product-model.md — Cost and Budget Tracking entry | Sections 1, 6, 7 |
| Runtime Guardrails: 6 scanners; sub-200ms p95 combined; bidirectional; configurable thresholds | canonical-product-model.md — Runtime Guardrails entry | Sections 1, 7, 9 |
| LLM Gateway: Production; ~50ms overhead | canonical-product-model.md — LLM Gateway entry | Sections 1, 7 |
| Prompt Playground: not present in Ethana Build at any status tier | canonical-product-model.md — no matching entry | Sections 1, 6, 7 |
| Dataset Management: not present in Ethana Build at any status tier | canonical-product-model.md — no matching entry | Sections 1, 6, 7 |
| Model fallback and latency-based routing: NOT confirmed in canonical model | Not found in approved sources — flagged as unconfirmed | Sections 1, 4, 6 |
| Webhook-based real-time alerting: NOT confirmed in canonical model | Not found in approved sources — flagged as unconfirmed | Sections 1, 4 |
| SCIM: In Build; SSO/OIDC: Production | canonical-product-model.md — Account Management entry | Section 6 |

**Sources used:** canonical-product-model.md: yes | product-architecture-investigation.md: no | use-cases.md: no | Engineering confirmation: no

**Prohibited sources — confirmed not used:** capability-status.md: not used | source-of-truth.md: not used | ethana-status-reconciliation.md: not used | Marketing playbook (for status or performance claims): not used

---

## 9. Technical Proposal Language

### Immutable Audit Log — For compliance comparison with LangSmith tracing

"Ethana's Immutable Audit Log captures every LLM call routed through the Ethana Gateway in an insert-only event store. Each event includes the call timestamp, tenant and model identifiers, request and response representations (full content or configurable redacted/hashed form), the disposition of all active guardrail scanners (scanner name, verdict, latency), and total gateway processing time. The insert-only write path means exported data arriving in Splunk, Elastic, or Datadog cannot be retroactively modified by the Ethana application — providing a tamper-resistant audit trail that LangSmith's mutable trace store does not match. Native SIEM export to Splunk (HEC), Elastic (API), and Datadog (API) is Production and requires no separate integration middleware."

### Guardrails — For comparison with LangSmith custom evaluators

"Ethana includes six production guardrail scanners applied bidirectionally to every Gateway-routed LLM call at sub-200ms p95 combined latency: PII detection, Prompt Injection, Jailbreak, Toxicity, Bias Signal, and Secret Leakage. Each scanner produces a binary verdict captured in the Audit Log, creating a scanner-disposition-to-audit-record chain for each LLM call.

**Mandatory caveat:** The six scanners are configurable (sensitivity thresholds, per-tenant enable/disable) but are not user-extensible. Teams requiring custom evaluation logic — LLM-as-judge scoring, domain-specific policy checks, or arbitrary evaluation functions — cannot implement these as Ethana scanner rules. For custom evaluation requirements, Promptfoo or RAGAS should be evaluated separately and can operate alongside an Ethana deployment."

---

## 10. Technical Summary

Ethana Build is a strong partial substitute for LangSmith with a clear capability boundary: it replaces LangSmith on the compliance, security, and audit export dimensions and adds a layer of regulatory-grade immutability that LangSmith does not provide. It does not replace LangSmith on developer tooling — prompt playground, dataset management, and custom evaluators remain Gaps with no Ethana Production equivalent. The recommended approach is not a full cutover but a targeted deployment: Ethana as the compliance and security layer (Gateway, Guardrails, Audit Log), LangSmith retained for prompt engineering and offline evaluation, with the SIEM export chain serving both audit trail and developer observability from a single event store. Confirm model fallback and latency-based routing capabilities with Ethana engineering before representing the LLM Gateway as a full routing substitute. The cutover of F1 (tracing) and F6 (SIEM export) should proceed first, with F2 and F5 following at the same time. F3 and F4 are not on the Ethana roadmap at any confirmed status tier.

---
---

# Example 3: Post-Solution-Mapping POC Scope Validation

**Context:** UK financial services firm (mid-size, 2,000 employees). A completed Ethana Solution Mapping engagement recommended Ethana Build — specifically the LLM Gateway, three Guardrails scanners (PII, Injection, Jailbreak), the Immutable Audit Log, and the MCP Security Broker core — for a 60-day POC. The firm's CTO has submitted the proposed POC scope for technical validation before committing. Existing stack: Azure AD (identity), Datadog (monitoring), GitHub Actions (CI/CD), LangChain (existing agent framework).

**Input:**
```
upstream_skill_output: Ethana Solution Mapping Section 3 — proposed Production capabilities:
  - LLM Gateway
  - Guardrails: PII Scanner
  - Guardrails: Prompt Injection Scanner
  - Guardrails: Jailbreak Scanner
  - Immutable Audit Log
  - MCP Security Broker (core)

poc_scope:
  Features: as above from Solution Mapping Section 3
  Duration: 60 days
  Success definition: Demonstrate runtime AI governance controls and audit trail
    sufficient to present to FCA operational resilience examiner

existing_stack: Azure AD, Datadog, GitHub Actions, LangChain
customer_sector: BFSI
deployment_constraint: Cloud (Customer VPC)
volume_parameters: 8,000 LLM calls per day
poc_duration: 60 days
output_mode: POC Scope
```

**Query type:** Post-Solution-Mapping Technical Validation + POC Feasibility Assessment

---

## 1. Feature Validation Table

| # | Feature | Status | TFS | Evidence |
|---|---|---|---|---|
| F1 | LLM Gateway | Production | 90 | canonical-product-model.md — LLM Gateway entry |
| F2 | Guardrails: PII Scanner | Production | 85 | canonical-product-model.md — Runtime Guardrails entry |
| F3 | Guardrails: Prompt Injection Scanner | Production | 88 | canonical-product-model.md — Runtime Guardrails entry |
| F4 | Guardrails: Jailbreak Scanner | Production | 82 | canonical-product-model.md — Runtime Guardrails entry |
| F5 | Immutable Audit Log | Production | 90 | canonical-product-model.md — Immutable Audit Log entry |
| F6 | MCP Security Broker (core) | Production | 72 | canonical-product-model.md — MCP Security Broker entry |

**F1 — LLM Gateway**
**Status:** Production | **TFS:** 90 (Ready)
**Technical description:** The LLM Gateway routes LLM API requests from the firm's applications through the Ethana platform, applying guardrail scanners bidirectionally on each call and recording every call to the Audit Log. Gateway overhead is approximately 50ms per call. At 8,000 calls per day (approximately 0.09 calls per second on average; burst peak TBD), the Gateway operates comfortably within the confirmed performance envelope for cloud/VPC deployments. Customer VPC deployment isolates traffic within the firm's cloud boundary.
**Constraint:** None material for this customer's volume and deployment model.

**F2 — Guardrails: PII Scanner**
**Status:** Production | **TFS:** 85 (Viable)
**Technical description:** The PII Scanner runs on every Gateway-routed LLM request and response, detecting personally identifiable information (names, financial identifiers, contact details) in text content. It operates bidirectionally — scanning both the prompt entering the LLM and the response returned to the user. Sub-200ms p95 latency for all six scanners combined. Sensitivity threshold is configurable per tenant. Scanner disposition (flagged / not flagged) is recorded in the Audit Log with the call event.
**Constraint:** Text modality only — the PII Scanner operates on text content. PDFs, images, audio, or structured database field values submitted as binary attachments are not scanned. For FCA operational resilience evidence, the scope of what the PII Scanner covers (text-in, text-out) must be clearly stated if the firm processes multi-modal input data.

**F3 — Guardrails: Prompt Injection Scanner**
**Status:** Production | **TFS:** 88 (Viable)
**Technical description:** The Prompt Injection Scanner detects adversarial inputs designed to override the LLM's system instructions or manipulate its behaviour through the user prompt. Runs on the request (input) side of every Gateway call. Sub-200ms p95 combined with all active scanners. Disposition recorded in Audit Log.
**Constraint:** The scanner targets direct injection patterns in the user prompt. Indirect injection (malicious content embedded in retrieved documents in a RAG pipeline that is then incorporated into the LLM's context) is a different attack vector and may not be fully covered by the prompt-side injection scanner alone. For a firm with RAG-based workflows, verify indirect injection coverage with Ethana engineering.

**F4 — Guardrails: Jailbreak Scanner**
**Status:** Production | **TFS:** 82 (Viable)
**Technical description:** The Jailbreak Scanner detects prompts designed to cause the LLM to produce outputs that bypass its safety guidelines or operational constraints. Operates on the request side. Sub-200ms p95 combined. Disposition recorded in Audit Log.
**Constraint:** Jailbreak detection is probabilistic — scanner operates on known jailbreak patterns. Novel or low-prevalence jailbreak techniques may not be detected until they are incorporated into scanner training. Standard caveat for all scanner-based detection.

**F5 — Immutable Audit Log**
**Status:** Production | **TFS:** 90 (Ready)
**Technical description:** The Audit Log captures every Gateway-routed call in an insert-only event store. For each call: timestamp, tenant and model identifiers, request and response (configurable representation), all scanner dispositions (name, verdict, latency), and gateway processing time. Native SIEM export to Datadog via API — every event is forwarded to the firm's existing Datadog environment on write. Insert-only write path at the application layer. Retention period configurable to align with FCA record-keeping obligations.
**Constraint:** See Example 1 for the DB-layer vs. application-layer immutability distinction. For an FCA operational resilience examination, application-layer insert-only is a strong control; verify DB-layer enforcement with Ethana engineering before representing it as hardware-level WORM to an examiner.

**F6 — MCP Security Broker (core)**
**Status:** Production | **TFS:** 72 (Viable)
**Technical description:** The MCP Security Broker provides tracing and policy enforcement for LLM calls in agent pipelines. The core ~8,000-line implementation is Production. The firm's existing LangChain-based agent framework is MCP-compatible, satisfying the primary prerequisite for the MCP Broker. Each agent LLM call is routed through the Broker, which records the call chain in the Audit Log.
**Constraint:** Non-Human Identity (NHI) lifecycle management — the management of agent identities, credentials, and access rights as autonomous actors — is In Build. This means the POC can demonstrate agent call tracing and policy enforcement but cannot demonstrate automated agent identity lifecycle management. If the firm's CTO or CISO asks specifically about agent identity governance beyond call tracing, disclose the NHI In Build status explicitly.

---

## 2. Technical Fit Summary

**Average TFS (arithmetic verification):**
90 (F1) + 85 (F2) + 88 (F3) + 82 (F4) + 90 (F5) + 72 (F6) = 507
507 ÷ 6 features = 84.5

**Distribution:**

| Band | Score range | Count | Features |
|---|---|---|---|
| Ready | 90–100 | 2 | F1 Gateway (90), F5 Audit Log (90) |
| Viable | 70–89 | 4 | F2 PII Scanner (85), F3 Injection Scanner (88), F4 Jailbreak Scanner (82), F6 MCP Broker (72) |
| Partial | 50–69 | 0 | — |
| Thin | 25–49 | 0 | — |
| Not Viable | 0–24 | 0 | — |
| **Total** | | **6** | |

**Technical Characterisation:** POC-Ready (average TFS 84.5 ≥ 75; 6 of 6 features at Viable or Ready)

**Coverage story:** All six Production features proposed in Solution Mapping Section 3 are technically fit for a 60-day POC in a UK BFSI Customer VPC deployment. The feature set is POC-Ready with two conditions to resolve before Day 1: (a) LangChain version confirmation for MCP Broker compatibility, and (b) Azure AD OIDC app configuration. Three In Build features must be explicitly excluded from the POC scope and from any FCA examiner demonstration. The Datadog integration is confirmed via SIEM export. The firm should budget two to three weeks of pre-POC setup for Datadog dashboard build and Azure AD configuration.

---

## 3. Integration Compatibility Assessment

### Azure AD (identity)

**Integration type:** Supported — OIDC/SSO (Production)
**Protocol:** OpenID Connect (OIDC) / SAML-compatible. Azure AD is a standard OIDC identity provider — Ethana's SSO/OIDC Account Management integrates with Azure AD using a registered application in the firm's Azure AD tenant.
**Customer configuration required:**
1. Register an Ethana application in Azure AD (Azure Portal > App Registrations > New Registration)
2. Configure the redirect URI to the Ethana tenant SSO endpoint
3. Grant the registered application the required Graph API permissions (User.Read minimum)
4. Provide the Azure AD tenant ID and client credentials to the Ethana onboarding team

**Compatibility constraint:** SCIM-based automated user provisioning is In Build — Azure AD SCIM connector cannot be used during the POC. User accounts must be created manually in the Ethana admin console and linked to Azure AD identities via the OIDC mapping.

**Evidence source:** canonical-product-model.md — Account Management entry (SSO/OIDC: Production; SCIM: In Build)

---

### Datadog (monitoring)

**Integration type:** Supported — SIEM Export (Production)
**Protocol:** Datadog API (event/log ingestion). Confirmed SIEM export target.
**Customer configuration required:**
1. Generate a Datadog API key with Logs Write permissions in the firm's Datadog organisation
2. Identify the target Datadog site (e.g., `datadoghq.eu` for EU-region deployments)
3. Provide the API key and site endpoint to the Ethana tenant configuration

**Schema mapping:** Ethana Audit Log events arrive in Datadog as log entries. The firm's Datadog team must build log facets and dashboards against the Ethana event schema. Suggested mapping for FCA operational resilience evidence: source tag `ethana-audit-log`; key facets: `call_id`, `model_id`, `tenant_id`, `scanner_dispositions`, `processing_latency_ms`.

**Evidence source:** canonical-product-model.md — Immutable Audit Log SIEM export (Splunk, Elastic, Datadog confirmed)

---

### GitHub Actions (CI/CD)

**Integration type:** Gap (In Build)
**The Ethana Red Teaming Orchestrator CI/CD gate integration is In Build.** GitHub Actions cannot be connected to an Ethana CI/CD gate during this POC. Automated red teaming as part of the firm's CI/CD pipeline is not demonstrable in the 60-day POC.

**Use exactly:** "Integration of Ethana Red Teaming Orchestrator with GitHub Actions CI/CD is In Build. It is not available for the POC and must not be committed to as a POC deliverable. Manual red teaming runs using the Red Teaming Orchestrator are available as a Production alternative."

**Evidence source:** canonical-product-model.md — Red Teaming Orchestrator (21 probes: Production; CI/CD gate: In Build)

---

### LangChain (agent framework)

**Integration type:** Supported — MCP-compatible
**LangChain is MCP-compatible.** The MCP Security Broker's core implementation works with MCP-compatible agent runtimes, and LangChain (with the MCP integration package) is the primary reference framework.
**Customer configuration required:**
1. Confirm LangChain version ≥ 0.1 is installed in the firm's agent environment (verify against Ethana engineering for exact minimum version at time of POC)
2. Configure LangChain to route agent LLM calls through the Ethana MCP Broker endpoint
3. Provide the Broker endpoint URL and tenant credentials to the LangChain configuration

**Compatibility constraint:** Not all LangChain versions have stable MCP support. Verify the exact minimum version requirement with Ethana engineering before POC kickoff.

**Evidence source:** canonical-product-model.md — MCP Security Broker entry (core: Production; MCP-compatible runtimes: LangChain referenced)

---

## 4. Technical Constraints and Caveats

1. **Azure AD SCIM In Build:** Azure AD OIDC/SSO is Production and can be configured on Day 1. Automated user provisioning via SCIM is In Build — user lifecycle management during the POC is manual via the Ethana admin console.

2. **GitHub Actions CI/CD gate In Build:** The Red Teaming Orchestrator CI/CD gate integration is In Build. Manual red teaming runs are Production and can be demonstrated in the POC; automated CI/CD gate checks cannot.

3. **MCP Security Broker — NHI In Build:** Agent call tracing and policy enforcement through the MCP Broker core is Production. Non-human identity lifecycle management (agent identity creation, credential rotation, access revocation) is In Build. The POC can show call tracing; it cannot show agent identity governance.

4. **PII Scanner — text modality only:** The PII Scanner processes text content in LLM requests and responses. Binary attachments (PDFs, images, audio files) submitted to the LLM are not scanned by the PII Scanner. If the firm's AI applications submit multi-modal inputs to the LLM, the text-to-multimodal scope boundary must be clearly stated.

5. **Indirect prompt injection — verify coverage:** The Prompt Injection Scanner targets direct injection in the user prompt. For RAG-based workflows where retrieved document content is included in the LLM context, verify indirect injection coverage with Ethana engineering before the POC.

6. **Audit Log immutability layer:** See Section 1 F5 constraint. Application-layer insert-only is confirmed; DB-layer enforcement should be confirmed with Ethana engineering before the FCA examiner presentation.

7. **Datadog dashboard build time:** The Datadog SIEM integration is straightforward to configure; building the Datadog dashboards and facets for an FCA examiner presentation typically requires two to three days of Datadog engineering time. Include this in the POC timeline.

---

## 5. POC Feature Set

### Included Features

**F1 — LLM Gateway**

**Test scenario:** Configure the Ethana Gateway as the routing layer for the firm's sandbox LLM application. Submit 50 test LLM calls through the Gateway (mix of benign and test-flag payloads). Verify: all 50 calls are recorded in the Audit Log with correct metadata; gateway latency overhead is ≤ 100ms for all calls; the firm's sandbox application receives the LLM response without degradation.

**Technical prerequisites:**
- Firm provides: a sandbox LLM API key (GPT-4 or equivalent), a sandbox application environment in the Customer VPC, and network routing configuration to direct LLM API calls through the Ethana Gateway endpoint
- Ethana provides: tenant provisioning, Gateway endpoint URL, configuration documentation

**Measurable success criterion:** All 50 test calls appear in the Audit Log within 120 seconds of submission, with correct model_id, tenant_id, and timestamp fields populated. Gateway latency does not exceed 100ms overhead (measured as round-trip minus LLM provider latency) for 95% of calls.

**Estimated setup time:** 1 day (network routing configuration + tenant provisioning)

---

**F2 — Guardrails: PII Scanner**

**Test scenario:** Submit 10 test prompts containing synthetic PII data (names, UK National Insurance numbers, credit card numbers in text form) through the Gateway. Verify: scanner flags each PII-containing prompt or response; scanner verdict appears in the Audit Log for each call; non-PII control prompts are not flagged (false positive check).

**Technical prerequisites:**
- Test prompts with synthetic (not real) PII data prepared by the firm
- Guardrails enabled and PII Scanner activated in the Ethana tenant configuration

**Measurable success criterion:** PII Scanner flags 100% of the 10 synthetic PII test cases; zero false positives on 10 control prompts without PII; all scanner dispositions appear in the Audit Log within 60 seconds.

**Estimated setup time:** 4 hours (scanner activation + test prompt preparation)

---

**F3 — Guardrails: Prompt Injection Scanner**

**Test scenario:** Submit 10 test prompts containing known direct prompt injection patterns (instruction override phrases, role-play jailbreak preambles) through the Gateway. Verify: scanner flags each injection-pattern prompt; 10 control prompts without injection patterns are not flagged.

**Technical prerequisites:**
- Test injection prompts prepared (standard prompt injection test cases are publicly documented in OWASP LLM Top 10)
- Injection Scanner activated in Ethana tenant configuration

**Measurable success criterion:** Scanner flags 10/10 injection-pattern prompts; 0/10 false positives on controls; scanner dispositions in Audit Log for all 20 calls.

**Estimated setup time:** 4 hours (scanner activation + test case preparation)

---

**F4 — Guardrails: Jailbreak Scanner**

**Test scenario:** Submit 10 test prompts containing known jailbreak patterns through the Gateway. Verify scanner detection and Audit Log capture, with false positive control. Same test structure as F3.

**Technical prerequisites:** As F3. Jailbreak Scanner activated.

**Measurable success criterion:** Scanner flags 10/10 jailbreak test cases; 0/10 false positives; dispositions in Audit Log.

**Estimated setup time:** Concurrent with F3 setup

---

**F5 — Immutable Audit Log → Datadog**

**Test scenario:** After running F1–F4 test scenarios, open the Datadog dashboard (to be built by the firm's Datadog team pre-POC) and verify: all test call events from F1–F4 appear in Datadog with correct metadata; scanner dispositions are visible per call event; events cannot be modified by any Ethana API operation (attempt an update call against a recorded event and verify rejection). Present the Datadog view to a simulated FCA examiner review (internal stakeholder standing in for the examiner role).

**Technical prerequisites:**
- Datadog API key configured in Ethana tenant
- Firm's Datadog team has built basic log facets and an event table dashboard against the Ethana Audit Log schema (2–3 days of Datadog engineering time pre-POC)
- Test LLM calls from F1–F4 have been completed

**Measurable success criterion:** All F1–F4 test call events (minimum 80 events) appear in the Datadog dashboard within 120 seconds of call completion. A simulated examiner reviewing the Datadog dashboard can trace a specific call's scanner dispositions from the call record without leaving the dashboard. An attempted update API call against a recorded event returns a 405 Method Not Allowed or equivalent rejection from the Ethana API.

**Estimated setup time:** 1 day (Datadog API key configuration); 2–3 additional days (firm's Datadog team builds dashboards — can run in parallel with other POC setup)

---

**F6 — MCP Security Broker (core)**

**Test scenario:** Configure the firm's LangChain-based agent to route LLM calls through the MCP Security Broker endpoint. Execute a multi-step agent workflow (minimum 5 agent LLM calls in sequence). Verify: all agent LLM calls appear in the Audit Log with the agent call-chain identifier; guardrail scanner dispositions are recorded for each agent call; the call sequence is traceable as a linked chain in the Datadog dashboard.

**Technical prerequisites:**
- LangChain version confirmed compatible with Ethana MCP Broker (verify exact version with Ethana engineering before POC kickoff)
- Firm's LangChain agent configured to route through the MCP Broker endpoint
- MCP Broker endpoint URL and tenant credentials provided by Ethana

**Measurable success criterion:** All 5+ agent LLM calls in the test workflow appear in the Audit Log within 120 seconds; calls are linked by a common call-chain identifier; all scanner dispositions are recorded; the agent workflow completes successfully with no degradation from the Broker overhead.

**Estimated setup time:** 1.5 days (LangChain configuration + version verification)

---

### Excluded Features

| Feature | Reason |
|---|---|
| Red Teaming Orchestrator — CI/CD gate (GitHub Actions) | **In Build — cannot be demonstrated.** The CI/CD gate integration is In Build. Manual Red Teaming Orchestrator runs are Production but were not included in Solution Mapping Section 3 for this engagement. |
| Azure AD SCIM automated provisioning | **In Build — cannot be demonstrated.** SCIM is In Build. User provisioning during the POC is manual via the Ethana admin console. |
| MCP Security Broker: NHI lifecycle management | **In Build — cannot be demonstrated.** The NHI module is In Build. Agent call tracing (F6 above) is Production and is in scope; agent identity lifecycle management is not. |
| Ethana Edge (all capabilities) | **In Build — must not be referenced.** Edge is In Build. No Edge capability is in scope for this POC. |
| Ethana Workspace (all features) | **Aspirational — must not be referenced.** Must not appear in any POC document or demonstration. |

---

## 6. Prohibited Feature Claims Register

| Feature | Status | Prohibition |
|---|---|---|
| Red Teaming Orchestrator — CI/CD gate integration | In Build | Cannot be demonstrated; cannot be committed as a POC deliverable; manual Red Teaming Orchestrator runs are the Production alternative |
| Azure AD SCIM provisioning | In Build | Cannot be demonstrated; SSO/OIDC is the available Production integration |
| MCP Security Broker — NHI lifecycle management | In Build | Cannot be demonstrated or referenced as available; core tracing (F6) is the Production scope |
| SOC 2 Type II certification | In Build | Cannot be claimed; must be disclosed as In Build if the FCA examiner or the firm's CISO asks |
| ISO 27001 certification | In Build | Cannot be claimed; must be disclosed as In Build if asked |
| Ethana Edge (all capabilities) | In Build | Must not be referenced in any POC document |
| Ethana Workspace (enterprise chat, RAG, copilots) | Aspirational | Must not be described, demonstrated, or referenced as available in any context |
| Visual Agent Builder | Aspirational | Must not be described, demonstrated, or referenced |

---

## 7. Substitution Analysis

*Not applicable — no existing_tool_feature_list was provided with this input.*

---

## 8. Evidence References

| Claim | Source | Section |
|---|---|---|
| LLM Gateway: Production; ~50ms overhead; cloud/VPC deployment | canonical-product-model.md — LLM Gateway entry | Sections 1, 9 |
| Guardrails: 6 scanners; sub-200ms p95 combined; bidirectional; PII, Injection, Jailbreak, Toxicity, Bias, Secret | canonical-product-model.md — Runtime Guardrails entry | Sections 1, 9 |
| Immutable Audit Log: Production; insert-only write path; SIEM export to Datadog confirmed | canonical-product-model.md — Immutable Audit Log entry | Sections 1, 3, 9 |
| MCP Security Broker core: Production (~8,000 lines); NHI: In Build | canonical-product-model.md — MCP Security Broker entry | Sections 1, 4, 6 |
| SSO/OIDC: Production; SCIM: In Build | canonical-product-model.md — Account Management entry | Sections 3, 4, 6 |
| Red Teaming Orchestrator CI/CD gate: In Build | canonical-product-model.md — Red Teaming Orchestrator entry | Sections 3, 5, 6 |
| Datadog: confirmed SIEM export target | canonical-product-model.md — Immutable Audit Log SIEM export section | Section 3 |
| LangChain: MCP-compatible runtime | canonical-product-model.md — MCP Security Broker entry | Section 3 |
| DB-layer vs. application-layer immutability — NOT confirmed in approved sources | Not found in approved sources — flagged as unconfirmed; verify with Ethana engineering | Sections 1, 4 |
| Indirect injection coverage for RAG pipelines — NOT confirmed in approved sources | Not found in approved sources — flagged as unconfirmed; verify with Ethana engineering | Sections 1, 4 |
| Exact minimum LangChain version for MCP Broker — NOT confirmed in approved sources | Not found in approved sources — verify with Ethana engineering before POC kickoff | Sections 3, 5 |

**Sources used:** canonical-product-model.md: yes | product-architecture-investigation.md: no | use-cases.md: no | Engineering confirmation: no

**Prohibited sources — confirmed not used:** capability-status.md: not used | source-of-truth.md: not used | ethana-status-reconciliation.md: not used | Marketing playbook (for status or performance claims): not used

---

## 9. Technical Proposal Language

### LLM Gateway — for POC technical addendum

"The Ethana LLM Gateway routes LLM API requests from the firm's applications through the Ethana platform before forwarding them to the designated LLM provider. Gateway overhead is approximately 50ms per call. All gateway-routed calls are recorded in the Immutable Audit Log. The gateway operates in the firm's Customer VPC — LLM request and response traffic does not leave the VPC boundary. At 8,000 calls per day (approximately 0.09 calls per second average), the gateway operates within the confirmed performance envelope for Customer VPC deployments."

### Guardrails: PII, Injection, Jailbreak Scanners — for POC technical addendum

"Ethana applies three guardrail scanners to every Gateway-routed call: the PII Scanner (detects personally identifiable information in request and response text), the Prompt Injection Scanner (detects adversarial prompt override patterns in the request), and the Jailbreak Scanner (detects patterns designed to bypass the LLM's safety guidelines in the request). All three scanners run bidirectionally at sub-200ms p95 latency combined. Each scanner produces a binary verdict recorded in the Audit Log with the call event — the scanner name, verdict, and scanner latency are captured per call.

**Mandatory caveat:** The PII Scanner, Prompt Injection Scanner, and Jailbreak Scanner operate on text content only. Binary attachments submitted to the LLM (PDFs, images, audio) are not scanned. For applications that submit multi-modal inputs to the LLM, the text-only scope of these scanners must be documented in the firm's AI system risk register."

### Immutable Audit Log → Datadog — for POC technical addendum

"The Immutable Audit Log captures every Gateway-routed call in an insert-only event store. Call records include: timestamp, model and tenant identifiers, request and response content (configurable redacted or full form), scanner dispositions for all active scanners (scanner name, verdict, latency), and gateway processing time. Events are exported to the firm's Datadog environment via the Datadog Log Ingestion API on write. The Audit Log's insert-only write path means the exported Datadog log records cannot be retroactively modified by the Ethana application API — providing an application-layer tamper-resistant audit trail for FCA operational resilience evidence.

**Mandatory caveat:** Application-layer insert-only means the Ethana API does not expose update or delete operations on audit records within the retention period. Whether the underlying storage engine enforces immutability independently at the database layer is not confirmed in current documentation — verify with Ethana engineering before representing the Audit Log as hardware-level WORM to an FCA examiner."

### MCP Security Broker (core) — for POC technical addendum

"The Ethana MCP Security Broker provides call tracing and policy enforcement for LLM calls in MCP-compatible agent pipelines. The firm's LangChain-based agents route LLM calls through the Broker, which records each call in the Immutable Audit Log with a call-chain identifier linking calls within a single agent workflow. This creates a traceable record of the full agent execution chain — which LLM calls were made, in what sequence, with what scanner dispositions — available in the Datadog dashboard.

**Mandatory caveat:** The MCP Security Broker core (call tracing and policy enforcement) is in Production. Non-human identity lifecycle management — the governance of agent identities, credentials, and access rights as autonomous actors — is In Build and is not in scope for this POC. LangChain version compatibility should be confirmed with Ethana engineering before POC kickoff."

---

## 10. Technical Summary

All six Production features proposed in the Solution Mapping Section 3 are technically validated as POC-Ready for a 60-day Customer VPC deployment. The average TFS of 84.5 — with 6 of 6 features at Viable or Ready — gives the solution architect high confidence in the POC scope as proposed. Three pre-POC steps must be completed before Day 1: (a) confirm the minimum LangChain version with Ethana engineering for MCP Broker compatibility; (b) configure Azure AD OIDC SSO in the firm's Azure AD tenant; and (c) allow two to three days for the firm's Datadog team to build Audit Log log facets and the FCA-examiner-ready dashboard. Three In Build features — CI/CD gate, SCIM provisioning, and NHI lifecycle management — are explicitly excluded from the POC scope and must not appear in the POC success criteria or any document shown to the FCA examiner. Before the FCA examiner demonstration at the end of the 60-day POC, the solution architect should verify the DB-layer immutability question and the indirect injection RAG coverage question with Ethana engineering.
