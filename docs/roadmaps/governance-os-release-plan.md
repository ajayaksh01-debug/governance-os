# Governance OS Release Plan

**Date:** 2026-06-21  
**Basis:** Program Review (2026-06-21), Master Status Baseline, PR-008 Architecture Design, v1 Internal Tool Roadmap  
**Authoritative sources:**
- `reviews/governance-os-program-review-2026-06-21.md`
- `reviews/governance-os-master-status.md`
- `docs/decisions/PR-008-regulatory-watch-agent-l4-readiness.md`
- `docs/roadmaps/v1-internal-tool-roadmap.md`

---

## Executive Summary

### Current Repository Maturity

Governance OS is a well-specified, partially-implemented internal prototype at approximately 55–60% completion toward a v1 internal tool and 20–25% toward a SaaS product. The architecture is sound. The Claims Firewall — the system's non-negotiable zero-tolerance guarantee against false capability claims — is production-hardened and enforced consistently across all six agents. Four of six agents have verified runtimes, passing test suites, and fully exercised failure-handling paths.

The remaining two agents represent the current ceiling. The Regulatory Watch Agent (RWA) has a 969-line orchestrator that has never been exercised by a test at the happy-path level. The Client Assessment Agent (CA) has the most complete specification in the codebase — 835 lines of orchestrator code, a novel 6-skill adapter chain, and a 59-state state machine — but the chain has never executed end-to-end, the package assembly step is unwired, and Client Memory does not exist.

### Current Readiness

| Dimension | Rating |
|---|---|
| Architecture and specification | ~90% |
| Claims Firewall and trust layer | Production-hardened |
| Core agents (CVA, IIA, EPA, GRA) | Internal Tool Ready |
| Partial agents (RWA, CA) | Prototype |
| Test infrastructure | ~65% |
| Production infrastructure | ~5% |
| **Overall: Internal Tool** | **~55–60%** |
| **Overall: SaaS Product** | **~20–25%** |

### Long-Term Vision

Governance OS becomes Cursory's operational intelligence layer for enterprise AI governance — a multi-tenant SaaS platform through which enterprise clients assess their AI portfolios against applicable regulatory frameworks, receive Claims-Firewall-verified control specifications and remediation plans, and track governance maturity over time. Every capability claim exiting the platform — in an assessment package, a proposal, or a remediation plan — has been validated against the canonical Ethana product model by the Claims Firewall before delivery.

### Strategic Objective

Ship a usable v0.9 Internal Tool in 5–6 focused development weeks. Use v0.9 as the first real-data validation of the full CA 6-skill chain. Use findings from that first end-to-end run to inform the architecture hardening required for v1.0 enterprise pilot. Reach v1.0 in approximately 6 months. Reach v2.0 SaaS in 12–18 months from today.

---

## Release Strategy

---

### v0.8 — Current Prototype

**Version:** 0.8  
**Status:** In production (current repository state as of 2026-06-21)

#### Current State

**What exists and works:**

- **Claims Firewall** — `claims_linter.py` (417 lines, hardened 2026-06-18); zero-tolerance, independently enforced by all 6 agents; resistant to bypass via approval notes, Skill 1 output, and Skill 2 output; 9 hardening tests pass
- **CVA runtime** — Capability Validation Agent; verified L4; 3 passing tests covering production/in-build/mixed-status paths; all approval flows exercised
- **IIA runtime** — Incident Intelligence Agent; verified L4; 5 passing tests including Samsung happy path, 3 failure modes, approval bypass
- **EPA runtime** — Ethana Proposal Agent; verified L4; 15 passing tests; FM→PR integration contract proven; approval bypass tested
- **GRA runtime** — Governance Review Agent; verified L4; 45 passing tests; 3 fixture paths; dotted-import runtime immune to sys.modules pollution
- **Schema and contract layer** — 10 schemas; PR-003 repaired field mismatch; PR-007 fixed test suite pollution
- **Evaluation infrastructure** — `claims_linter.py`, `workflow_validator.py`, `regression_tester.py`, `agent_certifier.py`, `scorecard_compiler.py` (all operational as standalone tools)
- **Knowledge layer** — 3 regulatory frameworks, EU AI Act + GDPR + DPDP Act + FCA/PRA + RBI, ~25 Ethana product knowledge files, 6 ADRs
- **Test suite** — 282 total tests across 11 files; 281 passing; 1 known fixture defect (CONFORMANT_FMO `markdown_output` field)

**What does not work:**

- RWA happy path is untested — the 969-line orchestrator has never been executed end-to-end under test conditions
- Mode B (regulatory change re-assessment queue) is entirely untested
- The CA 6-skill chain has never executed end-to-end; the adapter chain has never been run with real inter-skill data
- `scorecard_compiler.py` is not wired into the CA `ASSEMBLING_PACKAGE` orchestrator state — a complete CA run cannot produce a client scorecard
- Client Memory (Assessment Memory and Client Memory persistence tiers 2/3) does not exist
- The agent certifier grants L4 for any non-empty agent directory — it certifies RWA and CA as L4 despite both being at Prototype status

**Current Limitations:**

- No REST API — agents are invocable only via direct Python calls
- No approval notifications — `APPROVAL_N_PENDING` states require human approvers to poll for state rather than receive notification
- No deployment infrastructure — no Dockerfile, no CI/CD, no containerisation
- Filesystem-only state persistence — no multi-process safety; no cross-session durability guarantee
- Jurisdiction coverage: EU, UK, India only; no US federal, no APAC

#### Exit Criteria for v0.9

The following must all be true before v0.9 begins:

- [ ] PR-008 merged: `test_regulatory_watch_runtime.py` has 34 passing tests; `minimal-risk-internal-tool.md` exists; RWA L4A/B/C criteria satisfied
- [ ] PR-009 merged: CONFORMANT_FMO defect resolved (282/282 tests pass); `governance-assessment-workflow.md` updated to 6-skill chain; GRA `AGENT.md` created; CA `AGENT.md` stale blockers corrected
- [ ] PR-010 merged: 3 `ethana-solution-mapping` fixtures and 3 `ethana-feature-mapping` fixtures created; all regression tests pass
- [ ] PR-011 merged: `scorecard_compiler.py` wired into CA `ASSEMBLING_PACKAGE`; package assembly validated
- [ ] PR-012 merged: certifier requires test file presence for L4; pass-rate validation active; summary message bug fixed
- [ ] CA end-to-end integration test: at least one complete CA run with real EU BFSI data through all 6 real adapters, reaching `COMPLETE` and producing all 12 package artifacts

---

### v0.9 — Internal Tool

**Version:** 0.9  
**Target timeline:** 5–6 weeks from v0.8  
**Target audience:** Internal Cursory team operators; Compliance Directors, Practice Leads, and senior advisory staff who can invoke the system via Python scripts and interpret JSON state files

#### Goal

Enable a human operator to execute a complete Governance Assessment for a real enterprise AI subject — from intake through all approval gates through package assembly — and receive a complete, Claims-Firewall-verified Executive Assessment Package including all 12 defined artifacts and a client scorecard.

#### Required

- **PR-008 complete** — RWA has 34 passing tests; Mode A (all 3 fixture profiles) and Mode B basic operation verified; genuine L4 by evidence
- **PR-009 complete** — 282/282 tests passing; `governance-assessment-workflow.md` reflects actual 6-skill chain; GRA has a specification; CA AGENT.md stale blockers corrected
- **PR-010 complete** — `ethana-solution-mapping` and `ethana-feature-mapping` have fixture coverage; CA Skill 3 and Skill FM are validated against test inputs
- **PR-011 complete** — `scorecard_compiler.py` wired; all 12 Executive Assessment Package artifacts assembled by the CA orchestrator
- **PR-012 complete** — certifier grants L4 only with test evidence; all 6 agents report genuine L4
- **CA end-to-end validation** — at minimum one successful CA run: real EU BFSI input → 6 skills via real adapters → 4 approval gates → `COMPLETE` → all 12 artifacts present

#### Capabilities

At v0.9, a Cursory operator can:

1. **Regulatory Watch:** trigger RWA against a new AI use case registration; advance through Approval Gate 1 (Regulatory Scoping Matrix) and Approval Gate 2 (Operational Control Specification); receive the Compliance and Coverage Package
2. **Regulatory Watch (Mode B):** trigger a regulatory change re-assessment event; RWA queues re-assessment for all affected prior assessments; up to 3 concurrent re-assessments start automatically
3. **Governance Assessment:** initiate a full CA 6-skill chain against a client AI portfolio; advance through all 4 approval gates; receive the Executive Assessment Package including regulatory scoping matrix, control specification, ISO 42001 gap assessment, solution mapping, feature validation table, proposal review certificate, and client scorecard
4. **Proposal Review:** submit a draft commercial proposal for Claims Firewall review; receive a Proposal Review Certificate (approved/rejected/approved-with-revisions)
5. **Capability Validation:** validate a specific Ethana capability claim against the canonical product model; receive an ECS/CPL classification
6. **Incident Intelligence:** trigger incident triage and control design for an AI incident; receive a verified incident package after CISO and DPO approval
7. **Governance Review:** assess a client's AI governance maturity against an applicable framework; receive a scorecard and gap analysis

**Constraints at v0.9:** all interactions are Python method calls; approvals are submitted via Python API; package artifacts are JSON files and markdown documents in a local directory; no web interface; no external notification; no persistent cross-session memory beyond run-scoped JSON files.

#### Exit Criteria for v1.0

- [ ] At least 3 complete CA governance assessments executed against real or representative client data; all packages verified by a Compliance Director
- [ ] RWA Mode B triggered at least once against a real regulatory change event; re-assessment queue confirmed correct
- [ ] All approval gate flows exercised with real named approvers (not test actors)
- [ ] REST API design specified and at least a draft implementation exists
- [ ] Assessment Memory schema designed (even if not yet implemented)
- [ ] Approval notification routing designed (even if not yet wired)
- [ ] At least 1 pilot customer candidate identified and a real assessment use case agreed

---

### v1.0 — Enterprise Pilot

**Version:** 1.0  
**Target timeline:** 4–6 months from v0.9  
**Target audience:** 2–5 pilot enterprise customers; Cursory delivery team who can operate the system without reading source code; named human approvers (General Counsel, DPO, CISO, Compliance Director) who interact via a notification and approval interface

#### Goal

Deploy Governance OS with pilot customers. A pilot customer's compliance team can submit an AI use case, track its progress through the governance assessment workflow, receive approval notifications, and take delivery of a complete Executive Assessment Package — without writing or reading code.

#### Required

**REST API:**
- `POST /runs` — initiate a new agent run (trigger type, inputs)
- `GET /runs/{id}` — retrieve current state, history, and intermediate outputs
- `POST /runs/{id}/approve` — submit an approval gate decision (action, actor, notes)
- `GET /runs/{id}/package` — retrieve the assembled output package
- `GET /runs` — list active and recent runs for an organisation

**Approval notification layer:**
- Slack webhook integration per `APPROVAL_N_PENDING` state; configurable approver routing by role
- Email notification fallback for approvers without Slack
- Approval URL embedded in notification links to a minimal approval form (web or Slack modal)
- Timeout alerting: notify Compliance Analyst when `APPROVAL_TIMED_OUT` is reached

**Assessment Memory (tier 2 persistence):**
- PostgreSQL or document store for cross-run client state
- Indexed by: `traceability_id`, `subject_description`, `jurisdictions`, `regulations_applicable`
- Required for RWA Mode B (affected subject query against prior assessments)
- Required for CA incremental re-assessment (load prior regulatory mapping output for update runs)

**Client Memory (tier 3 persistence):**
- Longitudinal governance tracking per client organisation
- Stores: AMS/ARS progression over time, maturity baseline history, prior assessment summaries
- Retention: 5–7 years per regulatory requirement (EU AI Act Article 12 mandates documentation retention)

**Package delivery:**
- Secure document delivery mechanism for the Executive Assessment Package; minimum: SFTP or signed S3 URL per completed run
- Client-accessible document store with access control per organisation

**Deployment infrastructure:**
- Dockerfile for each agent runtime
- Docker Compose for local and staging environments
- Managed deployment target (Heroku, Railway, or equivalent); full Kubernetes not required for v1.0
- Environment-based configuration for: database URLs, Slack webhook tokens, approval routing, score thresholds

**Operational monitoring:**
- Structured logging per run to a central log store
- Alert on: `HALTED_FIREWALL_BREACH`, approval timeout, skill execution error, package assembly failure
- Basic run dashboard: active runs by state, completion rate, average cycle time

#### Capabilities at v1.0

A pilot customer can:

1. **Submit AI use cases** via a simple intake form or API; receive a traceability ID
2. **Receive approval notifications** in Slack when their submission requires review by named approvers
3. **Approve or reject** governance milestones via Slack modal or email link without technical knowledge
4. **Track assessment progress** in real time via the run status API or a basic status page
5. **Receive the Executive Assessment Package** automatically upon `COMPLETE`; documents delivered to a secure document store
6. **Trigger regulatory change re-assessments** when a regulation update is announced; receive re-assessment queue status

**Operator capabilities at v1.0:**
- Monitor all active runs across clients from a single dashboard
- Configure approval routing per client, per agent, per gate
- Set score thresholds and timeout periods per client in `config.yaml`

#### Exit Criteria for v2.0

- [ ] At least 5 pilot customers with at least 1 completed governance assessment each
- [ ] System has processed at least 20 completed runs with no data loss or Firewall bypass incident
- [ ] Approval average turnaround within SLA: AG-1 ≤ 2 business days, AG-2 ≤ 3 business days
- [ ] Client Memory data for at least 2 clients spanning more than 90 days
- [ ] REST API p95 latency < 500ms for `GET /runs/{id}`
- [ ] LLM integration design specified: which skills replace deterministic executors first, evaluation harness design, regression guardrails design
- [ ] Multi-tenancy data model designed and reviewed for security
- [ ] SOC 2 Type II audit scope defined

---

### v2.0 — SaaS Platform

**Version:** 2.0  
**Target timeline:** 12–18 months from today (6–12 months from v1.0)  
**Target audience:** Self-serve enterprise customers; multi-tenant; CISOs, DPOs, and Compliance Directors who onboard independently without Cursory delivery involvement

#### Goal

Multi-tenant Governance OS platform. A new enterprise customer can sign up, connect their AI portfolio registry, configure their jurisdiction and industry profile, and initiate their first governance assessment — all without Cursory involvement. Assessment packages are delivered through a client portal. Approval workflows are managed through an embedded workflow UI. All capability claims are validated by the Claims Firewall before any output reaches the client.

#### Required

**Authentication and authorisation:**
- OAuth 2.0 / OIDC for customer authentication; SSO support (Okta, Azure AD, Google Workspace)
- Role-based access control (RBAC): Client Admin, Compliance Director, Approver, Viewer; Cursory Operator as cross-tenant superuser
- API key management for programmatic integrations

**Multi-tenancy:**
- Full data isolation per customer organisation at database level (row-level security or schema-per-tenant)
- Customer onboarding flow: organisation creation, user invitations, jurisdiction and industry profile setup
- Cross-tenant analytics for Cursory operations (aggregate; no cross-tenant data leakage)

**Client portal:**
- Assessment status dashboard: all runs, current state, time in state, SLA status
- Document viewer: in-browser rendering of Markdown assessment packages
- Approval workflow UI: named approvers receive in-portal notifications; approve/reject/comment without leaving the browser
- Assessment history: all prior runs for a client; downloadable packages; maturity trend charts

**Workflow UI:**
- Intake form: structured assessment submission; jurisdiction selector; industry profile; AI subject description with length and quality guidance
- Progress tracker: visual state machine progression from `INTAKE_VALIDATING` through `COMPLETE`
- Approval management: pending approvals list; deadline tracker; reminder sending

**Billing and subscription:**
- Subscription tiers: per-seat or per-assessment pricing
- Usage metering: assessment count, jurisdiction count, approval gate count per billing period
- Stripe or equivalent integration for invoicing and payment

**Audit logging:**
- Immutable audit trail per run: every state transition, approval decision, Firewall check result, and package delivery event
- Exportable audit log per run for client's own compliance records (required by EU AI Act Article 12)
- Cursory-level audit log for all operator actions across tenants

**CRM integrations:**
- JIRA integration: new AI use case reaches "Compliance Review Required" status → automatically triggers RWA `new_use_case_registration` run
- HubSpot integration: AI system in pipeline reaches proposal stage → triggers EPA `new_proposal_review` run
- Webhook API: generic outbound webhook for any run state transition; customers wire their own CRM/ticketing

**Expanded regulatory coverage:**
- US federal: AI Executive Order, NIST AI RMF 1.0, emerging state-level AI regulations (Colorado, California)
- APAC: Singapore MAS FEAT Principles, Australia Privacy Act AI guidance
- Sovereign AI: evolving national AI strategies (Saudi Arabia SDAIA, UAE AI Office)
- Framework updates: ISO 42001:2023 full implementation, NIST CSF 2.0 AI profile

**LLM-backed execution layer:**
- Replace deterministic keyword-based skill executors with LLM-backed analysis for: regulatory-mapping, governance-control-mapping, iso-42001-gap-assessment
- Requires: model evaluation harness, per-skill regression guardrails, human-in-the-loop quality sampling, baseline comparison against deterministic outputs
- Claims Firewall continues to operate at the output layer regardless of execution mode; the Firewall is not a skill and is not replaced by LLM execution
- Deterministic executors remain as fallback for jurisdictions not yet covered by LLM prompts

#### Platform Vision at v2.0

The complete Governance OS v2.0 platform enables:

1. **Self-serve AI governance:** An enterprise AI team registers a new use case in their existing ticketing system; a governance assessment runs automatically; the CISO and DPO receive Slack notifications for their approval gate; the Compliance and Coverage Package is delivered to the client portal. No Cursory involvement required.

2. **Continuous regulatory watch:** When the EU AI Act implementing acts are published, the RWA Mode B queue fires for all affected assessments across all clients. Critical-severity re-assessments start immediately; operators are notified of the queue status. Re-assessment results are appended to each client's longitudinal governance record.

3. **AI portfolio governance tracking:** A client's Compliance Director logs into the client portal and sees their entire AI portfolio: each use case with its current assessment status, maturity level, open control gaps, and upcoming regulatory deadlines. The AMS/ARS progression chart shows maturity improvement over 18 months of using Governance OS.

4. **Claims-Firewall-verified commercial proposals:** The Cursory sales team submits a draft proposal; the EPA runs PCS/CTCS scoring and Claims Firewall check; the approved proposal exits the system with a Proposal Review Certificate number traceable to the run log. No capability claim in any delivered proposal has bypassed the Firewall.

---

## Architecture Evolution

### v0.8 → v0.9: Prototype Completion

```
v0.8 Architecture (current):
┌─────────────────────────────────────────────────────────┐
│ Python scripts — direct invocation only                  │
│                                                         │
│  CVA  │  IIA  │  EPA  │  GRA  │  RWA* │   CA*          │
│       │       │       │       │  (untested) │ (unwired) │
│                                                         │
│  Claims Firewall — evaluation/scripts/ (layer violation) │
│  State: filesystem JSON per run                         │
│  Tests: 281/282 passing                                 │
└─────────────────────────────────────────────────────────┘
* RWA: untested happy path. CA: scorecard unwired, no end-to-end test.

v0.9 Architecture (after PR-008 through PR-012 + CA validation):
┌─────────────────────────────────────────────────────────┐
│ Python scripts — direct invocation only (unchanged)     │
│                                                         │
│  CVA  │  IIA  │  EPA  │  GRA  │  RWA  │   CA           │
│       │       │       │       │  (L4) │ (L4, wired)    │
│                                                         │
│  Claims Firewall — evaluation/scripts/ (unchanged)      │
│  State: filesystem JSON per run (unchanged)             │
│  Tests: 316+ passing (282 + 34 RWA + CA integration)   │
│  Scorecard: wired into CA ASSEMBLING_PACKAGE            │
│  Certifier: evidence-based L4 (test file required)     │
└─────────────────────────────────────────────────────────┘
What changes: test coverage, scorecard wiring, certifier upgrade.
What does not change: invocation model, state persistence, infrastructure.
```

### v0.9 → v1.0: Production Readiness Layer

```
v1.0 Architecture (Phase C additions):
┌─────────────────────────────────────────────────────────┐
│ REST API (FastAPI or Flask)                             │
│  POST /runs │ GET /runs/{id} │ POST /runs/{id}/approve  │
│  GET /runs/{id}/package │ GET /runs                    │
├─────────────────────────────────────────────────────────┤
│ Agent runtimes (unchanged from v0.9)                    │
│  CVA │ IIA │ EPA │ GRA │ RWA │ CA — all L4              │
├─────────────────────────────────────────────────────────┤
│ Approval notification layer (NEW)                       │
│  Slack webhook per APPROVAL_N_PENDING state             │
│  Email fallback │ Timeout alerting                      │
├─────────────────────────────────────────────────────────┤
│ Assessment Memory — tier 2 (NEW)                       │
│  PostgreSQL │ cross-run indexed by traceability_id      │
│  Required for RWA Mode B affected-subject query         │
├─────────────────────────────────────────────────────────┤
│ Client Memory — tier 3 (NEW)                           │
│  Longitudinal AMS/ARS tracking │ 5-7 year retention    │
├─────────────────────────────────────────────────────────┤
│ Package delivery (NEW)                                  │
│  Signed S3 URL or SFTP per completed run               │
├─────────────────────────────────────────────────────────┤
│ Deployment infrastructure (NEW)                        │
│  Dockerfile per agent │ Docker Compose │ managed host   │
├─────────────────────────────────────────────────────────┤
│ Claims Firewall — now shared library (Phase B target)  │
│  Moved from evaluations/scripts/ to shared/            │
└─────────────────────────────────────────────────────────┘
What changes: everything above the agent runtimes is new.
Agent runtimes themselves are largely unchanged.
```

### v1.0 → v2.0: Multi-Tenant SaaS

```
v2.0 Architecture:
┌─────────────────────────────────────────────────────────┐
│ Client Portal (React or Next.js)                        │
│  Assessment dashboard │ Document viewer │ Approval UI   │
├─────────────────────────────────────────────────────────┤
│ REST API + WebSocket (real-time state updates)         │
│  Authentication: OAuth 2.0/OIDC │ RBAC per org        │
├─────────────────────────────────────────────────────────┤
│ Agent runtimes — LLM-backed (selective)                │
│  regulatory-mapping: LLM                               │
│  governance-control-mapping: LLM                       │
│  iso-42001-gap-assessment: LLM                         │
│  CVA/EPA/GRA: deterministic or hybrid                  │
│  Claims Firewall: deterministic (never replaced)       │
├─────────────────────────────────────────────────────────┤
│ Multi-tenant data layer                                │
│  Schema-per-tenant PostgreSQL │ Row-level security     │
│  Client Memory per org │ Assessment Memory per org     │
├─────────────────────────────────────────────────────────┤
│ Integrations                                           │
│  JIRA │ HubSpot │ Slack │ Email │ Webhook API         │
│  CRM trigger → RWA/EPA run auto-initiation            │
├─────────────────────────────────────────────────────────┤
│ Platform services                                      │
│  Billing (Stripe) │ SSO (Okta/Azure AD)               │
│  Immutable audit log │ Usage metering                  │
├─────────────────────────────────────────────────────────┤
│ Deployment                                             │
│  Kubernetes │ CI/CD pipeline │ multi-region option    │
│  SOC 2 Type II │ ISO 27001 in scope                   │
└─────────────────────────────────────────────────────────┘
What changes: everything. The agent runtimes are the one stable layer.
```

---

## Risks

### Technical Risks

**T1 — CA adapter-chain integration failure (High likelihood, High impact)**
The CA 6-skill chain has never run with real inter-skill data flowing through real adapters. `skill_adapters.py` imports SkillExecutor classes from RWA, CVA, and EPA runtimes with no interface contract enforcement. When the first real end-to-end CA run is attempted, the most likely failure mode is a silent payload format mismatch — RWA's `regulatory_mapping_output_json` may not map cleanly to CA's GCM adapter's expected input structure. This is the single highest-risk item on the path to v0.9.

**Mitigation:** Budget 2 weeks for CA end-to-end validation, not 1. Define interface contracts (input schema, output schema, required execution signature) for each skill before running the integration test. If mismatches are found, the fix is in `skill_adapters.py` — the source skill executors should not be modified.

**T2 — LLM skill executor quality regression risk (Medium likelihood, High impact for v2.0)**
When deterministic keyword-based skill executors are replaced by LLM-backed analysis for regulatory-mapping, governance-control-mapping, and iso-42001-gap-assessment, output quality becomes probabilistic and non-reproducible. Baseline regression tests that currently pass deterministically will require a probabilistic equivalence framework. The Claims Firewall itself must remain deterministic — the risk is that LLM-generated text in the sections the Firewall checks produces new false-positive or false-negative patterns.

**Mitigation:** Do not replace any deterministic executor before a model evaluation harness exists and has established baselines. Claims Firewall is exempt from LLM replacement. Maintain deterministic executors as fallback.

**T3 — scorecard_compiler.py CLI-to-module integration (Medium likelihood, Medium impact)**
`scorecard_compiler.py` is implemented as a standalone CLI tool with `argparse`. Wiring it into CA's `ASSEMBLING_PACKAGE` orchestrator state requires either subprocess invocation (fragile, adds latency, complicates error handling) or refactoring to expose a programmatic API. Neither path has been attempted.

**Mitigation:** Read `scorecard_compiler.py` in full before PR-011 implementation begins. If the CLI-to-module refactor is straightforward (< 30 lines), refactor directly. If complex, create a thin wrapper function that converts the CA state's skill output keys to the CLI argument format and invokes via subprocess.

**T4 — claims_linter.py layer boundary violation blocks Phase B hardening (Low likelihood short-term, High impact for v1.0)**
`claims_linter.py` lives in `evaluations/scripts/` but is imported at runtime by production orchestrators in RWA and CA. Any restructuring of the evaluation scripts directory — for CI/CD integration, for packaging, for deployment — risks breaking production agent runtimes at import time. This latent fragility is acceptable for v0.9 but must be resolved before v1.0.

**Mitigation:** Phase B architecture hardening must include moving `claims_linter.py` to a shared library importable by both evaluation scripts and production runtimes. This is a non-trivial refactor because it changes the import path for all existing tests.

### Product Risks

**P1 — CA is the product-defining agent and is the furthest from completion**
CA delivers the Executive Assessment Package — the primary value artefact for enterprise clients. It is also the most complex, least tested, and most architecturally risky component. If the CA end-to-end integration test surfaces serious adapter chain failures, v0.9 could slip by 4–6 weeks beyond the current estimate.

**Mitigation:** Treat the CA end-to-end validation as the highest-priority, most time-uncertain item in the v0.9 work. Begin CA adapter chain analysis before PR-010 is complete so that integration risks are identified early.

**P2 — Human approval gates have no delivery mechanism at v0.9**
At v0.9, approval gates are technically operational but require the approver to be notified by the operator via out-of-band communication (phone, Slack DM, email) and to submit the approval via a Python method call or API curl. This is workable for internal use by a Cursory operator but is not acceptable for any external pilot customer. The approval notification layer is a v1.0 requirement, not a v0.9 requirement — but if the pilot customer evaluation for v1.0 starts at v0.9, the lack of notifications will be a significant friction point.

**Mitigation:** Build a minimal Slack notification POC alongside CA end-to-end validation rather than waiting for the full v1.0 notification layer. A basic Slack webhook call on `APPROVAL_N_PENDING` transitions is a few hours of work and dramatically improves operator experience even at v0.9.

**P3 — No US federal jurisdiction limits addressable market for v1.0**
Current jurisdiction support: EU, UK, India. US federal regulation (AI Executive Order, NIST AI RMF, emerging state-level laws) is not covered. A significant proportion of enterprise AI governance demand originates in US-based companies with US regulatory obligations. Pilot customers with US operations will encounter a gap at v1.0.

**Mitigation:** Roadmap US federal coverage as the first v2.0 regulatory expansion. Communicate the limitation explicitly in v1.0 pilot customer scoping — engage customers whose primary regulatory exposure is EU/UK/India for the pilot cohort.

### Adoption Risks

**A1 — The approval gate workflow requires named executive approvers who are not LLM users**
The approval architecture requires General Counsel (AG-1), DPO and InfoSec Lead (AG-2), CISO (IIA), and Compliance Director (Claims Firewall re-run). These are senior, compliance-oriented roles who are unlikely to interact comfortably with a Python API or a raw JSON state file. Without a notification and approval UI (v1.0 feature), the approval workflow is inaccessible to its intended users.

**Mitigation:** The Slack notification POC described in P2 mitigation partially addresses this. For v1.0, the approval form must be something these users can complete in under 60 seconds without understanding the underlying state machine.

**A2 — Claims Firewall may generate friction with sales teams who want to describe aspirational capabilities**
The Firewall is zero-tolerance by design. An In Build capability referenced in a proposal — even aspirationally, even in a roadmap section — can halt a proposal review run. Sales teams accustomed to describing the full product vision may find the Firewall generates friction in the proposal development workflow.

**Mitigation:** This is by design and non-negotiable. The appropriate mitigation is user education (capability status clearly surfaced in the Ethana product model) and product roadmap transparency (sales teams should know which capabilities are Production vs. In Build). The Firewall is a feature, not a bug.

### Regulatory Risks

**R1 — EU AI Act implementing acts may expand Annex III scope before v1.0 ships**
The EU AI Act is in force as of August 2024 but implementing acts (technical standards, notified body requirements, high-risk system definitions) are still being published through 2026–2027. If Annex III scope is expanded or clarified, the RWA regulatory-mapping logic and the `knowledge/regulations/` directory must be updated within 5 business days per `evaluation.md §11` Certification Suspension Condition 3.

**Mitigation:** Treat `canonical-product-model.md` and `knowledge/regulations/` as living documents with a defined update owner. Add a monitoring step to the v1.0 operational runbook for regulatory change events.

**R2 — GovernanceOS outputs may be interpreted as legal advice**
The `evaluation.md` AG-1 approval scope disclaimer: "General Counsel approval of Regulatory Scoping Matrix is not a formal legal opinion and does not constitute legal advice." This disclaimer exists because a General Counsel's approval of a machine-generated regulatory analysis creates a latent liability if the output is later found to be incorrect. At v2.0 scale with self-serve customers, this risk increases significantly.

**Mitigation:** Legal disclaimer must be embedded in every output package and in every approval notification. Consider formal legal review of the disclaimer language before v1.0 pilot customer onboarding.

---

## Success Metrics

### v0.8 Metrics (current baseline)

| Metric | Current Value |
|---|---|
| Test suite pass rate | 281/282 (99.6%) |
| Agents at genuine L4 | 4/6 (67%) |
| Mode A happy-path test coverage: RWA | 0 tests |
| CA 6-skill end-to-end runs | 0 runs |
| Claims Firewall tests | 9 passing |
| Executive Assessment Packages produced | 0 (scorecard unwired) |

### v0.9 Metrics (Internal Tool targets)

| Metric | Target |
|---|---|
| Test suite pass rate | 316+/316+ (100%) |
| Agents at genuine L4 | 6/6 (100%) |
| RWA test coverage | 34 tests; all 24 state machine states reached |
| CA 6-skill end-to-end runs | ≥ 1 complete run with real data |
| Executive Assessment Packages produced | ≥ 1 complete package with all 12 artifacts |
| certifier L4 accuracy | 6/6 correct (test-evidence-based) |
| Claims Firewall bypass attempts blocked | 100% (all bypass vectors tested) |

### v1.0 Metrics (Enterprise Pilot targets)

| Metric | Target |
|---|---|
| Pilot customer completed assessments | ≥ 10 (across ≥ 2 customers) |
| Approval gate SLA: AG-1 | ≤ 2 business days average |
| Approval gate SLA: AG-2 | ≤ 3 business days average |
| Claims Firewall breach in production | 0 undetected breaches |
| API p95 response time | < 500ms for GET /runs/{id} |
| System uptime | ≥ 99.5% (monthly) |
| End-to-end cycle time | ≤ 7 business days average per assessment |
| Package delivery rate | 100% of COMPLETE runs produce retrievable packages |
| Assessment Memory data retention | Zero data loss across environment restarts |

### v2.0 Metrics (SaaS Platform targets)

| Metric | Target |
|---|---|
| Enterprise customers | ≥ 20 active |
| Assessments per month | ≥ 50 |
| AI use cases registered per customer | ≥ 5 (average portfolio) |
| Regulatory coverage | EU + UK + India + US federal + 1 APAC jurisdiction |
| Self-serve onboarding rate | ≥ 80% of new customers onboard without Cursory assistance |
| Approval gate SLA compliance | ≥ 90% within defined SLA |
| Platform availability | ≥ 99.9% (monthly) |
| Claims Firewall accuracy | 0 false negatives (In Build claimed as Production) in any delivered output |
| LLM skill quality: regulatory-mapping | ≥ 80/100 on evaluation rubric (Gate 2 pass threshold) across ≥ 95% of runs |
| SOC 2 Type II | Certified before first enterprise customer at v2.0 scale |

---

## Recommended Execution Order

```
PR-008 — RWA test suite (34 tests, minimal-risk fixture)
  │
  │ [Parallel: PR-009 — doc repairs, CONFORMANT_FMO fix, GRA AGENT.md]
  │
  ↓
PR-010 — fixture expansion (ESM + FM fixtures)
  ↓
PR-011 — scorecard compiler integration
  ↓
PR-012 — certifier upgrade (evidence-based L4)
  ↓
CA End-to-End Validation
(one complete CA run: real data → 6 real adapters → all 12 artifacts)
  ↓
v0.9 Internal Tool
(all 6 agents at genuine L4; CA chain verified; scorecard produced)
  ↓
Phase B: Architecture Hardening (6–10 weeks)
  ├── Define skill interface contracts
  ├── Refactor CA skill_adapters.py to contract-validated adapters
  ├── Move claims_linter.py to shared library
  ├── RWA Mode B end-to-end test
  └── Consolidate agent naming convention
  ↓
Phase C: Production Readiness (12–16 weeks)
  ├── REST API
  ├── Approval notification layer (Slack + email)
  ├── Assessment Memory (PostgreSQL)
  ├── Client Memory (longitudinal tracking)
  ├── Package delivery (S3/SFTP)
  ├── Deployment infrastructure (Docker + managed host)
  └── Operational monitoring
  ↓
v1.0 Enterprise Pilot
(pilot customers; real approval flows; package delivery; notifications)
  ↓
Phase D: SaaS Platform (24–36+ weeks)
  ├── Multi-tenancy and RBAC
  ├── Client portal and workflow UI
  ├── Billing and subscription
  ├── CRM integrations (JIRA, HubSpot, webhooks)
  ├── LLM-backed skill executor layer
  ├── Expanded regulatory coverage (US federal, APAC)
  └── SOC 2 Type II certification
  ↓
v2.0 SaaS Platform
```

**PR-008 and PR-009 run in parallel.** All other steps are sequential.  
**Phase B must complete before Phase C begins.** The CA adapter chain integration risk (Technical Risk T1) must be resolved and the claims_linter.py layer boundary (Technical Risk T4) must be corrected before production infrastructure is built on top of them.

---

## Final Assessment

### Current Maturity

Governance OS is architecturally complete and specification-complete at the agent level. The Claims Firewall is production-hardened. Four agents are genuinely operational. The gap between current state and v0.9 is a test coverage and wiring gap — not a design gap, not a capability gap. The work needed for v0.9 is known, bounded, and achievable.

The gap between v0.9 and v1.0 is a delivery infrastructure gap. The agent runtimes will be the stable layer. What needs to be built is everything around them: API, notifications, persistence, deployment. This is real engineering work — 12–16 developer weeks — but it is not research. The path is clear.

The gap between v1.0 and v2.0 is a platform maturity gap. Multi-tenancy, client portal, LLM-backed execution, CRM integrations, SOC 2 — each of these is a substantial engineering and business investment. The timeline is 12–18 months from today if v1.0 completes on schedule.

### Time to v0.9

**Estimate: 5–6 focused development weeks from today.**

This estimate is grounded in the program review and the PR-008 architecture design. PR-008 (34 tests, 3–4 days) and PR-009 (4 deliverables, 2–3 days) run in parallel in week 1. PR-010 (6 fixtures, 3–4 days) fills week 2. PR-011 (scorecard wiring, 2–3 days) and PR-012 (certifier upgrade, 2–3 days) fill week 3. The CA end-to-end validation is the wild card — nominally 2 weeks, but budget 3 weeks to account for adapter chain integration failures that are not yet visible.

**The most likely cause of slip is the CA adapter chain.** The 205 existing CA tests all use mocked skill outputs. When real skill executor outputs flow through real adapters for the first time, format mismatches or missing fields are virtually certain to appear. The question is how many and how severe. Budget conservatively.

**Challenge to this estimate:** The 5–6 week estimate assumes no parallel work on non-v0.9 features. If the same developer is also building Phase B architecture items, the timeline doubles. The estimate also assumes the CA adapter chain issues are addressable in `skill_adapters.py` without requiring changes to source skill runtimes. If a source skill executor (e.g., RWA's SkillExecutor) needs to change its output format for CA compatibility, that change cascades into RWA's 34 new tests.

### Time to v1.0

**Estimate: 4–6 months from v0.9 (5–7 months from today).**

Phase B architecture hardening (6–10 weeks) must precede Phase C production readiness (12–16 weeks). Phase B is a prerequisite because the layer boundary violation (claims_linter.py) and the cross-runtime coupling (skill_adapters.py) create deployment fragility that makes containerisation unreliable. Fixing these in Phase B before adding a REST API, databases, and a notification layer avoids rebuilding infrastructure that was built on a fragile foundation.

**The most likely cause of slip is Assessment Memory design.** RWA Mode B's affected-subject query requires indexing completed run data by `jurisdictions` and `applicable_regulations`. The design of this index — and the migration path from the current filesystem JSON state files — is not yet specified. Budget 2–3 extra weeks for data model design and migration before the persistence layer is built.

**Challenge to this estimate:** Phase C estimates (12–16 developer weeks) are based on the program review's Phase C section. Those estimates may be optimistic if:
- The REST API design exposes coupling issues in the agent orchestrator APIs that require refactoring
- The PostgreSQL Assessment Memory schema requires several iterations to match the RWA Mode B query patterns
- Pilot customer feedback from v0.9 validation trials drives scope additions before v1.0 ships

Realistic v1.0 timeline: 6–9 months from today.

### Time to v2.0

**Estimate: 12–18 months from today (6–12 months from v1.0).**

Phase D (24–36+ developer weeks) encompasses multi-tenancy, client portal, LLM integration, CRM connectors, billing, and SOC 2. The LLM integration alone is a major undertaking: replacing deterministic skill executors requires a model evaluation harness, prompt engineering, regression guardrails, and a human-in-the-loop quality sampling process that doesn't exist yet. SOC 2 Type II requires 6–12 months of audit observation period after controls are in place.

**The most likely bottleneck is the LLM integration, not the platform engineering.** The deterministic skill executors produce structured, reproducible output. LLM-backed equivalents will produce better analysis but probabilistic output with quality variance. Managing that variance — ensuring the regulatory-mapping skill still produces a ≥ 70/100 quality score on ≥ 95% of real inputs — requires evaluation infrastructure that is not yet designed.

**Challenge to this estimate:** v2.0 requires enterprise customers to trust LLM-generated regulatory analysis at scale. That trust is built through audit trail transparency, explainability, and demonstrated accuracy. The 12–18 month estimate assumes this trust-building work is a product and sales challenge, not an engineering blocker. If regulators impose AI system transparency requirements (EU AI Act Article 13 for high-risk AI systems) on GovernanceOS itself, additional compliance infrastructure may be required before v2.0 ships.

### Bottleneck Summary

| Milestone | Primary Bottleneck | Secondary Bottleneck |
|---|---|---|
| v0.9 | CA adapter chain integration (T1) | Scorecard compiler wiring (T3) |
| v1.0 | Assessment Memory data model design | Phase B architecture hardening (layer violations) |
| v2.0 | LLM skill executor quality management | SOC 2 Type II audit timeline |

The Claims Firewall is not a bottleneck at any release milestone. It is production-hardened today, and its design is stable. It is the one component that should not be touched during the v0.8 → v2.0 journey except to update it when `canonical-product-model.md` changes.
