# Governance OS — Principal AI Systems Architecture Review

**Assessor Role:** Principal AI Systems Architect  
**Date:** 2026-06-17  
**Scope:** Production-grade enterprise AI Governance Operating System readiness assessment  
**Method:** Full repository analysis across all layers — knowledge, skills, workflows, agents, evaluation, and supporting infrastructure. Assessment against enterprise AI platform standards for reliability, security, scalability, observability, and correctness.

---

## 1. Complete Architecture Map (Current State)

### Four-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 4: AGENTS + EVALUATION                    [CRITICAL GAP]     │
│                                                                     │
│  agents/              ← EMPTY DIRECTORY                             │
│  evaluations/                                                       │
│    evaluation-index.md    ← Framework defined                       │
│    scripts/               ← 4 Python scripts (claims_linter,        │
│      claims_linter.py       regression_tester, workflow_validator,  │
│      regression_tester.py   agent_certifier, scorecard_compiler     │
│      workflow_validator.py  stub)                                   │
│      agent_certifier.py                                             │
│      scorecard_compiler.py ← STUB (incomplete)                     │
│    baselines/             ← 1 baseline JSON (governance-control-    │
│      governance-control-mapping/structure.json  mapping only)       │
│    test-cases/            ← README only; no test data               │
└─────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 3: WORKFLOWS                              [DOCUMENTED ONLY]  │
│                                                                     │
│  workflows/                                                         │
│    README.md                  ← 5 workflow sequences + dependency   │
│                                 graph (Mermaid); 3 shared           │
│                                 components documented               │
│    incident-assessment-workflow.md   ← Prose only; not executable   │
│    regulatory-compliance-workflow.md ← Prose only; not executable   │
│    governance-assessment-workflow.md ← Prose only; not executable   │
│    proposal-development-workflow.md  ← Prose only; not executable   │
│    schemas/                   ← 5 inter-skill JSON schemas          │
│      (ai_incident_analysis_output.json, regulatory_mapping_output   │
│       .json, governance_control_mapping_output.json, ethana_        │
│       solution_mapping_output.json, ethana_capability_validation    │
│       _output.json)                                                  │
└─────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 2: SKILLS                                 [WELL SPECIFIED]   │
│                                                                     │
│  skills/                                                            │
│    ai-incident-analysis/          ← SKILL.md, workflow.md,          │
│    regulatory-mapping/              evaluation.md, examples.md      │
│    ethana-capability-validation/  ← Strictest (90/100 threshold)    │
│    ethana-solution-mapping/       ← Commercial mapping              │
│    ethana-feature-mapping/        ← Technical POC scoping           │
│    governance-control-mapping/    ← Central control design skill    │
│                                                                     │
│  MISSING SKILLS (planned or absent):                                │
│    iso-42001-gap-assessment/  ← Planned; blocks Client Agent        │
│    proposal-review/           ← Planned; blocks Proposal Agent      │
└─────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 1: KNOWLEDGE                              [STRONGEST LAYER]  │
│                                                                     │
│  knowledge/                                                         │
│    frameworks/                                                       │
│      iso-42001.md             ← Clauses 4–10 + Annex A (38 ctrls)  │
│      nist-ai-rmf.md           ← GOVERN/MAP/MEASURE/MANAGE           │
│    regulations/                                                     │
│      eu-ai-act.md             ← Risk tiers, Art.9–15, GPAI          │
│      uk-ai-guidance.md        ← FCA, PRA SS1/23, ICO, DPA 2018     │
│      india-ai-landscape.md    ← DPDP, RBI, SEBI, IRDAI             │
│    controls/                                                        │
│      prompt-injection-controls.md                                   │
│      agent-governance-controls.md                                   │
│      data-protection-controls.md                                    │
│      audit-controls.md                                              │
│      model-risk-controls.md                                         │
│    bfsi/                                                            │
│      banking-ai-governance-use-cases.md                             │
│      insurance-ai-governance.md                                     │
│      wealth-management-ai-governance.md                             │
│      gcc-ai-governance-patterns.md                                  │
│    ethana/                                                          │
│      canonical-product-model.md ← SINGLE TRUTH SOURCE (Tier 1)     │
│      framework-crosswalk.md                                         │
│      red-teaming.md                                                 │
│      mcp-security.md                                                │
│      immutable-audit-logs.md                                        │
│      deployment-and-certifications.md                               │
│      [PROHIBITED: capability-status.md, source-of-truth.md,        │
│       ethana-status-reconciliation.md]                              │
│    ai-incidents/                                                    │
│      samsung-chatgpt-leak.md                                        │
│      llm-supply-chain-compromise.md                                 │
│      mcp-vulnerability-risks.md                                     │
│      healthcare-ai-misdiagnosis.md                                  │
│      financial-ai-fraud.md                                          │
└─────────────────────────────────────────────────────────────────────┘
```

### Cross-Layer Dependency Map

```
Knowledge Layer → Skills Layer → Workflows Layer → Agent Layer

canonical-product-model.md ──────────────────────────────────────►  truth_gate (concept only)
       ↓
ethana-capability-validation ──────► W4 (solution workflow)
       ↓                             W5 (proposal workflow)
ethana-solution-mapping ─────────► W2 (regulatory workflow)
       ↓                             W5 (proposal workflow)
ethana-feature-mapping ◄──────────►governance-control-mapping (CIRCULAR)
       ↑
governance-control-mapping ──────► W1 (incident workflow)
       ↑                             W2 (regulatory workflow)
regulatory-mapping ──────────────► W2, W3, W5
       ↑
ai-incident-analysis ────────────► W1 (incident workflow)

GHOST DEPENDENCIES (referenced but missing):
ai-incident-analysis → skills/risk-assessment/ [MISSING]
ai-incident-analysis → skills/framework-gap-analysis/ [MISSING]
ai-incident-analysis → skills/regulatory-exposure/ [MISSING]
```

---

## 2. Architecture Maturity Score

**Overall: 31/100**

This score measures production readiness as an enterprise AI platform — not documentation quality or specification completeness. Those are measured separately by the GMI (69/100 in `repository-maturity-review.md`).

| Dimension | Score | Weight | Weighted | Rationale |
|---|---|---|---|---|
| Functional completeness | 35 | 20% | 7.0 | 6 skills implemented; 8 critical capabilities absent |
| Agent layer | 0 | 20% | 0 | Empty directory; nothing executable |
| Workflow execution | 10 | 15% | 1.5 | Documented but not executable |
| Evaluation quality | 15 | 10% | 1.5 | Scripts exist; no test data; no LLM judge |
| Data architecture | 0 | 10% | 0 | No persistence layer, schema, or storage |
| Observability | 5 | 10% | 0.5 | No logging, metrics, or alerting |
| Security architecture | 12 | 5% | 0.6 | Claims firewall strong; no auth, isolation, or secrets mgmt |
| Scalability | 0 | 5% | 0 | Manual execution only |
| API layer | 0 | 5% | 0 | No API; no integration points |

**Enterprise Readiness Grade: F (31/100)**  
*The system is production-grade as a knowledge specification. It is pre-alpha as an operating system.*

---

## 3. Missing Architectural Components

### CRITICAL (blocks all production use)

| Component | Description | Impact of Absence |
|---|---|---|
| **Agent Runtime** | Executable agent code with tool bindings, loops, and state management | No automation; every skill invocation requires human manual execution |
| **Orchestration Engine** | Workflow execution engine that sequences, parallelises, and gates tool calls | Cannot run any workflow; all sequencing is manual |
| **Data Persistence Layer** | Database for client profiles, assessments, evidence, risk registers | Every session starts from zero; no client history; no evidence accumulation |
| **Memory Layer** | Working memory (session state), episodic memory (past assessments), semantic memory (knowledge retrieval) | Agents cannot learn, recall, or improve across engagements |
| **Tool Registry** | Versioned registry of all callable tools with JSON schemas | No discoverability; no versioning; tool updates break agents silently |

### HIGH (required for enterprise deployment)

| Component | Description | Impact of Absence |
|---|---|---|
| **Authentication & Authorization** | Identity, access control, role-based permissions per client | Cannot deploy to enterprise without auth; multi-tenancy impossible |
| **API Gateway** | REST or gRPC API for programmatic access to governance workflows | System cannot be integrated with client toolchains, CRMs, or SIEMs |
| **Multi-tenancy Architecture** | Client data isolation, per-client configuration, client-scoped access | All clients share the same system; data leakage risk |
| **Observability Stack** | Logging, metrics, tracing, alerting for all agent and skill executions | No visibility into what the system is doing; no debugging capability |
| **Secrets Management** | Secure storage and rotation for API keys, credentials, and certificates | Cannot securely connect to external services |
| **Audit Trail** | Immutable log of every governance assessment produced, by whom, when | Cannot demonstrate governance of the governance system itself |

### MEDIUM (required for enterprise scale)

| Component | Description | Impact of Absence |
|---|---|---|
| **Knowledge Retrieval System** | Vector embedding + semantic search over the knowledge base | Context pollution; knowledge lookups require full file reads |
| **Regulatory Update Feed** | Automated ingestion of regulatory changes and diff against current knowledge | Regulatory mapping becomes stale without detection |
| **Evidence Vault** | Structured storage for client governance evidence with chain of custody | Cannot produce audit-ready evidence packs |
| **Workflow State Machine** | Persistent workflow state enabling checkpoint/resume and failure recovery | A 7-hour workflow restarts from scratch on any failure |
| **Notification System** | Alerts for workflow completion, threshold breaches, and required human actions | Human oversight checkpoints have no delivery mechanism |

---

## 4. Duplicate Components

| Duplication | Location | Issue |
|---|---|---|
| **Regulatory risk assessment** | `regulatory-mapping` Section 4 AND `ai-incident-analysis` Section 5 | Both classify regulatory risk; output may contradict when both run; no reconciliation mechanism |
| **Ethana capability status lookup** | `ethana-capability-validation` (explicit skill) AND `governance-control-mapping` Section 10 (Ethana Configuration Guide) | Two pathways for the same canonical lookup; ECV is the correct gate but GCM can bypass it |
| **Control recommendations** | `ai-incident-analysis` Section 9 AND `governance-control-mapping` (entire skill) | IA recommends controls at low resolution; GCM designs controls at high resolution; no orchestration prevents both from being run producing duplicate and potentially conflicting outputs |
| **Executive summary** | Required section in every skill (Section 1 or Section 10) | Five separate executive summaries can be produced for one workflow; no synthesis layer |
| **Framework mapping** | `knowledge/ethana/framework-crosswalk.md` AND `skills/regulatory-mapping/SKILL.md` Section 5 | Crosswalk is static knowledge; regulatory-mapping generates dynamic mapping; updates to one do not propagate to the other |

---

## 5. Incorrect Agent Boundaries

| Agent | Current Boundary | Problem | Correct Boundary |
|---|---|---|---|
| **Incident Intelligence Agent** | Triage + analysis + control design + capability validation + report synthesis | Four distinct responsibilities; blast radius varies from read-only (triage) to design recommendation (controls) | Split into: IncidentTriageAgent (classify only) + IncidentAnalysisAgent (RCA + framework mapping) + downstream trigger to ControlDesignAgent |
| **Regulatory Watch Agent** | Regulatory monitoring + change detection + workflow trigger + client notification | Conflates a read-only monitoring function with a write-capable workflow execution function | Split into: RegulatoryMonitorAgent (read-only, scheduled scan) + event emission to GovernanceOrchestrator for workflow dispatch |
| **Capability Validation Agent** | Peer skill agent — validates on request | Ethana capability validation is a firewall constraint, not a peer capability. Making it an optional agent means it can be bypassed. | Demote to middleware: truth_gate() called automatically by the tool runtime on all outputs containing Ethana capability references |
| **Client Assessment Agent** | Full assessment lifecycle | Blocked by two missing skills (iso-42001-gap-assessment, proposal-review); combining onboarding + gap assessment + control design + evidence generation in one agent creates an unbounded scope | Split into: ClientOnboardingAgent (discovery + inventory) + GapAssessmentAgent (framework-specific) + ControlDesignAgent (control mapping + design) |
| **Ethana Proposal Agent** | Full proposal development from regulatory mapping to final proposal | Blocked by missing proposal-review skill; producing a commercial proposal is a high-stakes, partially irreversible action that needs a human checkpoint before delivery | Add mandatory human checkpoint step; separate ProposalDraftAgent from ProposalReviewAgent |

---

## 6. Incorrect Skill Boundaries

| Skill | Issue | Severity | Correct Boundary |
|---|---|---|---|
| **governance-control-mapping** | 10 output sections covering planning (Section 1–3), design (Section 4–6), evidence (Section 7), ownership (Section 8), roadmap (Section 9), and configuration (Section 10) — this is four distinct skills in one | High | Decompose into: control-taxonomy (Sections 1–3), control-design (Sections 4–6), evidence-specification (Section 7), control-ownership (Section 8) |
| **ai-incident-analysis** | 10 output sections covering triage (Section 1–3), classification (Section 3–4), regulatory mapping (Section 6), BFSI assessment (Section 7), lessons (Section 8), controls (Section 9), and synthesis (Section 10) | High | Decompose into: incident-triage, root-cause-analysis, framework-mapping, regulatory-implication-assessment, control-gap-identification |
| **ethana-capability-validation** | Should not be a skill — it is a constraint that must fire on every output, not a skill invoked by human decision | Critical | Implement as middleware function `truth_gate()` called automatically by the workflow engine |
| **regulatory-mapping** | Section 6 (Control Requirements) overlaps significantly with governance-control-mapping — both produce control requirement specifications | Medium | Section 6 should produce high-level control categories only; detailed control design deferred to governance-control-mapping |
| **ethana-feature-mapping** | Circular dependency with governance-control-mapping: GCM → EFM → GCM | High | EFM should be a pure validation function that reads GCM outputs and returns a gap report; revision loop lives in the orchestrator |

---

## 7. Missing Workflows

| Workflow | Addresses | Status |
|---|---|---|
| `ai-discovery-workflow` | Client AI discovery and inventory population | Not planned; no underlying skill |
| `governance-gap-assessment-workflow` | Full framework gap assessment (ISO 42001, NIST, RBI FREE-AI) | Partially referenced; iso-42001-gap-assessment skill missing |
| `continuous-monitoring-workflow` | Production AI system behavioural monitoring | Not planned |
| `third-party-ai-risk-workflow` | Vendor AI risk assessment and TPAI register management | Not planned |
| `model-governance-lifecycle-workflow` | AI/ML model MRM lifecycle (deployment → validation → monitoring → retirement) | Not planned |
| `agent-deployment-governance-workflow` | Agent governance review before production agent deployment | Not planned |
| `audit-readiness-workflow` | Evidence pack assembly for regulatory examination | Not planned |
| `incident-regulatory-notification-workflow` | Regulatory notification drafting on incident breach triggers | Not planned |
| `regulatory-change-management-workflow` | Knowledge base update and client assessment invalidation on regulatory change | Not planned |

---

## 8. Missing Evaluation Systems

| Evaluation System | Type | Gap |
|---|---|---|
| **LLM-as-judge** | Quality evaluation | No LLM-judged evaluation exists; structural validation only |
| **Test case database** | Data | `test-cases/` directory exists with README; no actual test data |
| **Gold-standard outputs** | Data | Referenced in README; not created |
| **Behavioral test suite** | Adversarial/edge case | No tests for injection, boundary conditions, or unsupported inputs |
| **Integration test suite** | Cross-skill | No tests verify full workflow output consistency |
| **Performance benchmarks** | Operational | No latency, throughput, or token consumption benchmarks |
| **scorecard_compiler.py** | Automation | Stub file; no automated scoring from rubric |
| **5 of 6 baselines** | Structural | Only `governance-control-mapping/structure.json` exists; other 5 skills have no baseline |
| **Calibration dataset** | Judge quality | No human-scored examples for evaluator calibration |
| **Claims firewall regression suite** | Security | No test cases for adversarial inputs designed to bypass the Claims Firewall |

---

## 9. Missing Governance Controls (Internal — for the OS itself)

These are controls that govern the Governance OS as a product, distinct from the governance controls it helps clients implement.

| Control | Purpose | Current State |
|---|---|---|
| **Knowledge base change control** | Who can modify knowledge files, what approval is required, how changes are tested before deployment | None; any contributor can modify `canonical-product-model.md` without review |
| **Prohibited file access control** | Enforce that `capability-status.md`, `source-of-truth.md`, `ethana-status-reconciliation.md` cannot be read by agent processes | Currently advisory only; no technical enforcement |
| **Client data classification** | What data received from clients is confidential, how it must be stored and handled | Not defined |
| **Assessment output ownership** | Who owns the outputs produced for clients; retention and deletion policy | Not defined |
| **Skill version governance** | How skill specification changes are approved, tested, and deployed | No process; changes can be made without evaluation regression |
| **Assessment provenance** | Every assessment must be traceable to: which skill version, which knowledge version, which canonical model version | No provenance tracking |
| **Human oversight log** | All human checkpoint decisions (approve / reject) must be logged with rationale | No log mechanism |

---

## 10. Missing Observability Components

| Component | Required For | Current State |
|---|---|---|
| **Structured logging** | Debugging, audit trail, compliance | No logging in any skill or workflow |
| **Skill execution metrics** | Performance monitoring, capacity planning | Not collected |
| **Claims firewall hit rate** | Security monitoring; high hit rates signal a content drift problem | Not collected |
| **Workflow completion rates** | Reliability monitoring; which workflows succeed vs fail | Not tracked |
| **Score distribution tracking** | Quality monitoring; are skill outputs trending below pass thresholds? | Not tracked |
| **Token consumption per skill** | Cost management; which skills are context-expensive? | Not measured |
| **Client engagement dashboard** | Operational visibility; which clients have active assessments? | Not built |
| **Regulatory coverage map** | Product visibility; which regulations are currently mapped? | Static documents only |
| **Knowledge freshness indicators** | Staleness detection; when was each knowledge file last validated? | Not tracked |

---

## 11. Missing Security Layers

| Layer | Issue | Severity |
|---|---|---|
| **Authentication** | No auth system; who invokes the governance OS is not controlled | Critical |
| **Authorization** | No RBAC; a client's governance assessments are not protected from access by other clients | Critical |
| **Client data isolation** | No multi-tenancy controls; all client data would share the same storage | Critical |
| **Secrets management** | API keys, credentials, model API access — no secrets management layer | Critical |
| **Claims firewall technical enforcement** | Currently enforced by convention and scripts run optionally; not enforced by the system runtime | High |
| **Prohibited file technical enforcement** | `capability-status.md` etc. are prohibited by policy only; no technical control prevents agent access | High |
| **Output sanitisation** | Client inputs that contain PII may be reflected in skill outputs; no output sanitisation layer | High |
| **Prompt injection protection** | Incident report inputs or client descriptions may contain adversarial content designed to manipulate skill outputs | High |
| **Inter-agent communication security** | When agents communicate, content is a potential injection vector; no injection barriers defined | Medium |
| **Assessment output encryption** | Client governance assessments may contain sensitive findings; no encryption at rest | Medium |

---

## 12. Missing Orchestration Layers

| Layer | Description | Impact of Absence |
|---|---|---|
| **Task queue** | Asynchronous task queue for skill invocations | All invocations synchronous; long tasks block |
| **Workflow state machine** | Persistent state between workflow steps with checkpoint/resume | Workflow failures restart from step 1 |
| **Parallel execution engine** | Concurrent invocation of independent tool calls | Sequential execution doubles or triples latency |
| **Retry and backoff** | Automatic retry of failed tool calls with exponential backoff | Transient failures cause workflow termination |
| **Conditional router** | Route workflow to different paths based on tool output values | All workflows are linear; no dynamic branching |
| **Human approval gate** | Pause workflow, notify human, resume on approval | Human checkpoints have no implementation mechanism |
| **Dead letter queue** | Handle workflows that cannot complete after retries | Failed workflows are silently lost |
| **Event bus** | Inter-agent event emission and subscription | No reactive capability; Regulatory Watch Agent cannot notify other agents |

---

## 13. Missing Data Models

| Data Model | Required For | Notes |
|---|---|---|
| **Client Profile** | All client engagements | Organisation name, sector, jurisdiction, AI system portfolio, regulatory scope, engagement status |
| **AI System Record** | Inventory, monitoring, lifecycle | System ID, type, provider, purpose, owner, risk tier, deployment date, last validated, regulations applicable |
| **Governance Assessment** | Evidence vault, audit readiness | Assessment ID, client, date, skill version, knowledge version, canonical model version, score, output hash |
| **Risk Register Entry** | Risk management | Risk ID, system, risk category, likelihood, impact, inherent score, controls applied, residual score, owner, review date |
| **Control Specification** | Control lifecycle | Control ID, type, description, trigger, mechanism, failure mode, telemetry schema, owner (RACI), evidence requirements |
| **Evidence Record** | Audit readiness | Evidence ID, control, collection date, collector, retention period, format, storage location, chain of custody |
| **Regulatory Obligation** | Regulatory mapping | Obligation ID, regulation, article, obligation type, applicability criteria, due date, evidence required |
| **Incident Record** | Incident management, trend analysis | Incident ID, date, type, evidence quality, root cause, control failures, notification status, corrective actions |
| **Regulatory Change Event** | Regulatory watch | Change ID, regulation, effective date, affected obligations, affected client assessments, review status |
| **Proposal Record** | Commercial integrity | Proposal ID, client, date, skills used, canonical model version, claims linter result, approval status |

---

## 14. Missing Product Capabilities

| Capability | Description | Priority |
|---|---|---|
| **Client Portal** | Web interface for clients to view their assessments, risk registers, and evidence vault | High |
| **Assessment Dashboard** | Governance maturity scores over time; control implementation status; framework coverage heatmap | High |
| **Regulatory Horizon Scanner** | Automated tracking of regulatory changes with relevance scoring and client impact alerts | High |
| **Evidence Vault** | Structured, searchable repository of governance evidence with chain of custody and expiry tracking | High |
| **Reporting Engine** | Automated generation of board-ready governance reports, regulator submissions, and audit packs | High |
| **Integration Connectors** | SIEM integration (Splunk, Elastic, Datadog), GRC platform connectors, CRM integration | Medium |
| **Skills Marketplace** | Version-controlled skill library with release notes, changelog, and backward compatibility | Medium |
| **Benchmark Database** | Industry-peer governance maturity benchmarks for context-setting in client assessments | Medium |
| **Knowledge Subscription** | Clients subscribe to regulatory feeds relevant to their jurisdiction; auto-updates trigger re-assessment flags | Medium |
| **Certification Tracker** | ISO 42001 certification journey tracker with milestone management and readiness scoring | Low |

---

## Target State Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     GOVERNANCE OS — TARGET STATE ARCHITECTURE                ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│  EXTERNAL INTERFACES                                                        │
│                                                                             │
│  Client Portal (Web)    API Gateway (REST/gRPC)    CRM / SIEM Connectors   │
│  ─────────────────      ────────────────────────    ──────────────────────  │
│  Assessments, risks,    Programmatic access for     Trigger workflows from  │
│  evidence, reports      partner integrations        external events          │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ Authenticated + Authorized
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER                                                        │
│                                                                             │
│  ┌────────────────────┐  ┌───────────────────┐  ┌────────────────────────┐ │
│  │ Governance         │  │ Task Queue        │  │ Workflow State Machine  │ │
│  │ Orchestrator       │  │ (async dispatch,  │  │ (checkpoint/resume,    │ │
│  │                    │  │  retry, backoff)  │  │  conditional routing)  │ │
│  │ Decomposes tasks   │  │                   │  │                        │ │
│  │ Dispatches agents  │  │                   │  │                        │ │
│  │ Manages checkpoints│  │                   │  │                        │ │
│  │ Enforces gates     │  │                   │  │                        │ │
│  └────────────────────┘  └───────────────────┘  └────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AGENT LAYER                                                                │
│                                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │Discovery │ │Compliance│ │ Control  │ │ Proposal │ │ Incident         │ │
│  │& Inventory│ │  Agent   │ │  Agent   │ │  Agent   │ │ Response Agent   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                                    │
│  │Monitoring│ │  Model   │ │  Audit   │                                    │
│  │  Agent   │ │Governance│ │Readiness │                                    │
│  │          │ │  Agent   │ │  Agent   │                                    │
│  └──────────┘ └──────────┘ └──────────┘                                    │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  MIDDLEWARE LAYER                                                           │
│                                                                             │
│  ┌─────────────────────────┐   ┌──────────────────────────────────────────┐ │
│  │  TRUTH GATE             │   │  EVALUATION ENGINE                       │ │
│  │  (auto-fires on every   │   │  LLM-as-judge · Structural validator     │ │
│  │   tool output)          │   │  Claims linter · Schema validator        │ │
│  │                         │   │  Score compiler · Regression tester      │ │
│  │  get_capability_status  │   │                                          │ │
│  │  check_claim_permission │   │  Fires at every workflow gate            │ │
│  │  lint_claims            │   │  Blocks below-threshold outputs          │ │
│  └─────────────────────────┘   └──────────────────────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  TOOL REGISTRY (all callable atomic tools)                                  │
│                                                                             │
│  Intelligence Tools     Control Tools         Validation Tools              │
│  ──────────────────     ──────────────        ────────────────              │
│  classify_incident      design_preventive     score_output                  │
│  analyze_root_cause     design_detective      validate_schema               │
│  identify_regs          design_corrective     check_consistency             │
│  map_to_frameworks      assign_raci           assess_evidence_gap           │
│  classify_ai_tier       classify_coverage                                   │
│  identify_obligations                         Commercial Tools              │
│  extract_ctrl_reqs      Synthesis Tools       ────────────────              │
│                         ───────────────       map_requirement               │
│  Truth Gate Tools       write_exec_summary    compute_coverage              │
│  ───────────────        generate_evidence     generate_proposal_lang        │
│  get_capability_status  produce_raci          recommend_motion              │
│  check_claim_perm       (etc.)                compute_tfs                   │
│  compute_ecs                                                                │
│  lint_claims                                                                │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  KNOWLEDGE + MEMORY LAYER                                                   │
│                                                                             │
│  ┌───────────────────┐  ┌─────────────────────┐  ┌──────────────────────┐  │
│  │ Knowledge Base    │  │ Vector Store        │  │ Data Persistence     │  │
│  │ (current)         │  │ (new)               │  │ (new)                │  │
│  │                   │  │                     │  │                      │  │
│  │ 30+ markdown files│  │ Chunked + embedded  │  │ Client profiles      │  │
│  │ across 6 domains  │  │ knowledge base for  │  │ Assessments          │  │
│  │                   │  │ semantic retrieval  │  │ Evidence vault       │  │
│  │ Canonical product │  │                     │  │ Risk registers       │  │
│  │ model (Tier 1)    │  │ Episodic memory:    │  │ Control specs        │  │
│  │                   │  │ past assessments    │  │ Incident records     │  │
│  │ Framework docs    │  │                     │  │ Proposal records     │  │
│  │ Regulatory docs   │  │ Working memory:     │  │ Audit packs          │  │
│  │ Controls          │  │ session workflow    │  │                      │  │
│  │ BFSI use cases    │  │ state               │  │                      │  │
│  │ Incident cases    │  │                     │  │                      │  │
│  └───────────────────┘  └─────────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  INFRASTRUCTURE LAYER                                                       │
│                                                                             │
│  Auth / RBAC    Multi-tenancy    Secrets Mgmt    Observability              │
│  ────────────   ─────────────    ─────────────   ─────────────             │
│  SSO/OIDC       Client isolation  Vault           Logging (structured)     │
│  API keys       Data partitioning API key mgmt   Metrics (Prometheus)      │
│  RBAC by role   Per-client config Rotation       Tracing (OpenTelemetry)  │
│                                                   Alerting (PagerDuty)    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Gap Analysis Matrix

| Component | Current State | Target State | Gap | Severity | Effort |
|---|---|---|---|---|---|
| Skills | 6 markdown specs | 6 skills + 8 new skills, all as typed tools | Large | Critical | 8 weeks |
| Workflows | 5 prose docs | 9 executable DAGs with gates | Large | Critical | 6 weeks |
| Agents | 0 | 9 agents (1 orchestrator + 8 specialists) | Total | Critical | 12 weeks |
| Tool Registry | None | Versioned registry of 35 atomic tools | Total | Critical | 4 weeks |
| Truth Gate | Optional skill | Unconditional middleware | Architectural | Critical | 2 weeks |
| Evaluation | Partial scripts | Full suite: LLM judge + behavioral + integration | Large | High | 6 weeks |
| Test Data | None | 50+ test cases across 3 categories | Total | High | 4 weeks |
| Data Persistence | None | Multi-tenant database with 10 data models | Total | High | 10 weeks |
| Memory Layer | None | Working + episodic + semantic memory | Total | High | 8 weeks |
| Knowledge Retrieval | Full-file read | Vector store + semantic chunking | Large | High | 4 weeks |
| Auth / RBAC | None | SSO/OIDC + RBAC | Total | High | 4 weeks |
| Multi-tenancy | None | Client isolation + partitioned data | Total | High | 6 weeks |
| API Gateway | None | REST API + integration connectors | Total | Medium | 6 weeks |
| Observability | None | Logging + metrics + tracing + alerting | Total | Medium | 4 weeks |
| Secrets Management | None | Vault or equivalent | Total | Medium | 2 weeks |
| Context Management | None | Token budget tracking + compression | Total | Medium | 3 weeks |
| Client Portal | None | Web application | Total | Medium | 12 weeks |
| Regulatory Update Feed | None | Automated ingestion + diff | Total | Low | 6 weeks |

---

## Prioritized Roadmap

### Phase 1 — Foundation (Weeks 1–12): Make it executable

**Objective:** Convert the prompting library into a runnable system with the minimum viable agent loop.

| Week | Work |
|---|---|
| 1–2 | Implement Truth Gate as unconditional middleware. Refactor `claims_linter.py` into a callable function, not a CLI script. |
| 1–2 | Define atomic tool JSON schemas for all 6 existing skills decomposed into 25 atomic tools. |
| 3–4 | Build Tool Registry. Register all 25 tools. Add versioning. |
| 3–4 | Implement working memory for session state (in-memory key-value store for single-session workflows). |
| 5–6 | Implement Governance Orchestrator (first agent). Wire to 5 existing specialist agents as stubs. |
| 5–6 | Implement incident-response-workflow as an executable DAG. This is the simplest full workflow — 3 skills, clear sequence. |
| 7–8 | Build `iso-42001-gap-assessment` skill (blocks Client Assessment Agent). |
| 7–8 | Build `proposal-review` skill (blocks Proposal Agent). |
| 9–10 | Populate evaluation test-cases directory: 10 incident reports, 5 regulatory subjects, 3 gold-standard outputs. |
| 9–10 | Implement LLM-as-judge for `ai-incident-analysis` and `regulatory-mapping`. |
| 11–12 | Fix ghost dependencies in `ai-incident-analysis` (remove references to 3 non-existent skills). Fix circular dependency between GCM and EFM. |

**Exit criteria:** Incident response workflow executes end-to-end without human intervention. Claims Firewall fires automatically on all outputs. All 5 existing agents certified to Level 3 by `agent_certifier.py`.

---

### Phase 2 — Data + Multi-tenancy (Weeks 13–24): Make it enterprise-safe

**Objective:** Add the persistence, security, and isolation layers required for enterprise deployment.

| Week | Work |
|---|---|
| 13–14 | Design and implement data models (10 schemas: Client, AI System, Assessment, Risk Register, Control, Evidence, Obligation, Incident, Change Event, Proposal). |
| 13–14 | Implement data persistence layer (PostgreSQL or equivalent). |
| 15–16 | Implement authentication and RBAC. SSO/OIDC integration. Role model: Admin, Analyst, Client Viewer, Auditor. |
| 15–16 | Implement multi-tenancy: client data isolation, per-client configuration namespacing. |
| 17–18 | Implement Secrets Management. Rotate all credentials. Remove any hardcoded configuration. |
| 17–18 | Implement structured logging across all agent executions and tool calls. |
| 19–20 | Implement vector embedding of knowledge base. Deploy semantic retrieval layer. |
| 19–20 | Implement episodic memory: completed assessments persisted to searchable store. |
| 21–22 | Build Evidence Vault: structured storage, chain of custody, expiry tracking. |
| 21–22 | Implement Observability stack: metrics (Prometheus), tracing (OpenTelemetry), alerting. |
| 23–24 | Implement Workflow State Machine with checkpoint/resume. Rebuild all 5 workflows as executable DAGs. |

**Exit criteria:** Multi-tenant deployment with isolated client data. All client assessments persisted and retrievable. Audit trail for all governance outputs. SSO enforced on all access paths.

---

### Phase 3 — Full Capability (Weeks 25–40): Make it complete

**Objective:** Build the 8 missing governance capability skills, the full agent roster, and the client-facing product layer.

| Week | Work |
|---|---|
| 25–26 | Build `ai-discovery` and `ai-inventory-management` skills. Implement Discovery Agent. |
| 25–26 | Build `ai-risk-assessment` skill. Wire into gap assessment workflow. |
| 27–28 | Build `continuous-monitoring-design` skill. Implement Monitoring Agent with Audit Log integration. |
| 27–28 | Build `third-party-ai-risk-assessment` skill. Implement Third Party AI Risk Agent. |
| 29–30 | Build `model-governance-assessment` and `bias-fairness-assessment` skills. Implement Model Governance Agent. |
| 29–30 | Build `agent-governance-assessment` skill. Implement Agent Deployment Governance Agent. |
| 31–32 | Build `audit-pack-assembly` skill. Implement Audit Readiness Agent. |
| 31–32 | Build `rbi-free-ai-assessment` skill. Add to Compliance Agent's tool set. |
| 33–34 | Implement Regulatory Update Feed (automated regulatory change ingestion). Implement Regulatory Watch Agent with event emission. |
| 33–34 | Build full behavioral test suite (50+ test cases including adversarial injection tests, boundary condition tests, firewall stress tests). |
| 35–36 | Implement parallel execution engine in Orchestrator. Rebuild workflows to exploit parallelism. |
| 35–36 | Implement human approval gates with notification delivery. |
| 37–38 | Build Client Portal (assessment dashboard, risk register view, evidence vault access). |
| 37–38 | Build API Gateway with REST endpoints for all major workflows. |
| 39–40 | Build Reporting Engine (board-ready governance reports, audit pack export, maturity trend charts). |
| 39–40 | Integration testing, load testing, security penetration testing, disaster recovery testing. |

**Exit criteria:** All 16 governance capability areas covered by skills. All 9 agents operational. Client Portal live. API Gateway serving production integrations. System deployable to enterprise-grade infrastructure (on-prem, VPC, or air-gapped per client requirement).

---

## Architecture Decision Records

### ADR-01: Truth Gate as Middleware, Not a Skill

**Decision:** `ethana-capability-validation` logic is extracted from a peer skill and implemented as unconditional middleware that fires on every tool output containing an Ethana capability reference.

**Rationale:** An optional skill creates an optional firewall. The Claims Firewall must be unconditional — no workflow should be able to produce capability claims without triggering validation.

**Consequence:** The `ethana-capability-validation` skill is deprecated as a peer skill. The middleware implementation is more limited in output (it returns a binary pass/fail + CPL + mandatory caveats) but is architecturally correct.

---

### ADR-02: Single Orchestrator Pattern

**Decision:** All specialist agents are subagents of a single Governance Orchestrator. Agents do not communicate directly with each other.

**Rationale:** Direct agent-to-agent communication creates trust boundary problems and makes the system's behavior non-deterministic. A single orchestrator provides a predictable control plane, enables human checkpoint enforcement, and simplifies audit trail production.

**Consequence:** The orchestrator becomes a critical component. It must be highly available and resilient.

---

### ADR-03: Atomic Tool Decomposition

**Decision:** Each existing multi-section skill is decomposed into 3–8 atomic tools. The orchestrator sequences these tools, not the tools themselves.

**Rationale:** Monolithic skills cannot be called selectively, cannot be parallelized, and produce context-bloating outputs. Atomic tools are composable, cacheable, and sized correctly for tool-use patterns.

**Consequence:** More total tools to maintain, but each is simpler and independently testable. The orchestrator's system prompt must encode the sequencing logic that currently lives in `workflow.md` files.

---

### ADR-04: Canonical Model as a Service

**Decision:** `canonical-product-model.md` is not read as a file. It is exposed as a structured lookup service with a typed API: `get_capability_status(capability_name)` → `{status, caveats, scope, source_quote}`.

**Rationale:** Full-file injection of the canonical model for every lookup wastes context tokens and introduces parsing errors. A service layer encapsulates the parsing logic once, caches results, and provides a typed interface.

**Consequence:** The canonical model must be maintained in a structured format (or a parser must be maintained separately). File-format changes require API changes.
