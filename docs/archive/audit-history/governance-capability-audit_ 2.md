# Governance OS — Governance Capability Audit

**Assessor Role:** AI Governance Operating System Architect  
**Date:** 2026-06-17  
**Scope:** Capability coverage audit against ISO 42001, NIST AI RMF, EU AI Act, RBI FREE-AI, BFSI Model Risk Management, and AI Security Governance  
**Method:** Framework-requirement decomposition mapped against existing knowledge, skills, workflows, and agents. Implementation quality excluded. Capability presence and coverage depth assessed only.

---

## Audit Basis

### Frameworks Decomposed

| Framework | Full Name | Governance Scope |
|---|---|---|
| **ISO 42001** | ISO/IEC 42001:2023 — AI Management Systems | Clauses 4–10, Annex A (38 controls across 9 domains) |
| **NIST AI RMF** | NIST AI Risk Management Framework 1.0 | GOVERN, MAP, MEASURE, MANAGE functions |
| **EU AI Act** | Regulation (EU) 2024/1689 | Articles 9–15, 72; GPAI obligations; prohibited AI provisions |
| **RBI FREE-AI** | RBI Framework for Responsible and Ethical Enablement of AI | Governance structure, model risk, fairness, transparency, audit, third-party AI |
| **BFSI MRM** | BFSI Model Risk Management (SR 11-7, PRA SS1/23, RBI MRM) | Model inventory, validation, monitoring, documentation, challenger models |
| **AI Security** | AI Security Governance (OWASP LLM Top 10, MITRE ATLAS, AI-specific threat modelling) | Prompt injection, data poisoning, supply chain, agent exploitation, exfiltration |

### Capability Domains Assessed

| # | Capability | Definition |
|---|---|---|
| 1 | **Discovery** | Automated or structured identification of AI systems across an organisation |
| 2 | **Inventory** | Cataloguing AI systems with structured metadata, ownership, and lifecycle status |
| 3 | **Classification** | Risk-tiering AI systems by harm potential, regulatory category, and deployment context |
| 4 | **Risk Assessment** | Systematic identification and evaluation of AI-specific risks |
| 5 | **Gap Assessment** | Comparing current governance posture against a specific framework's requirements |
| 6 | **Control Mapping** | Mapping identified risks and obligations to required controls |
| 7 | **Control Design** | Producing implementation-ready control specifications |
| 8 | **Control Validation** | Testing whether designed controls are implemented and operating effectively |
| 9 | **Evidence Generation** | Producing structured, auditor-ready evidence of control effectiveness |
| 10 | **Audit Readiness** | Assembling a complete evidence pack for regulatory or certification audit |
| 11 | **Continuous Monitoring** | Ongoing production monitoring of AI system behaviour, drift, and control performance |
| 12 | **Incident Management** | Detection, triage, analysis, response, and post-incident review for AI incidents |
| 13 | **Regulatory Mapping** | Mapping AI systems to applicable legal and regulatory obligations |
| 14 | **Third Party AI Risk** | Assessing and managing risk from vendor AI systems, foundation models, and AI supply chain |
| 15 | **Agent Governance** | Governing autonomous AI agents: scope, identity, least privilege, HITL gates |
| 16 | **Model Governance** | AI/ML model lifecycle governance: development controls, validation, monitoring, retirement |

---

## 1. Current Capability Map

What the repository can do today, capability by capability.

---

### CAP-01: Discovery

**Coverage: ABSENT (8/100)**

The repository has no skill, workflow, or agent for AI system discovery — the process of identifying what AI systems exist within an organisation. The word "discovery" appears only in two places: Ethana Sentry Discovery (In Build — not production) in the canonical product model, and as a reference to the NIST AI RMF MAP function in the knowledge base.

**What exists:**
- `knowledge/frameworks/nist-ai-rmf.md` describes MAP function requirements including use-case identification — conceptual coverage only
- `knowledge/ethana/framework-crosswalk.md` maps NIST MAP 1.6 (agent/tool mapping) to Ethana's MCP Broker (Production) — a narrow technical proxy only
- The `knowledge/controls/agent-governance-controls.md` mentions an "Agent Registry" as a control concept

**What is missing:**
- No skill for conducting an AI discovery exercise with a client
- No methodology for scanning enterprise environments for deployed AI systems
- No structured intake questionnaire for AI system identification
- No workflow for maintaining a live discovery posture (scheduled re-discovery)
- No connection between discovery outputs and inventory population

**Framework obligations unaddressed:**
- ISO 42001 Clause 4 (context understanding) and Clause 8 (lifecycle management) require knowing what AI systems exist before governing them
- NIST AI RMF MAP 1.5 (AI system identification), MAP 2.1 (inventory of AI systems)
- EU AI Act Article 6 (high-risk classification requires knowing what systems exist)
- RBI FREE-AI Pillar 1 (AI governance structure requires an AI register)
- BFSI MRM (model inventory is foundational; SR 11-7 explicitly requires it)

---

### CAP-02: Inventory

**Coverage: LOW (18/100)**

Knowledge exists describing what an AI inventory should contain. No skill or workflow operationalises it.

**What exists:**
- `knowledge/controls/model-risk-controls.md` defines a minimum inventory field specification (Model ID, type, provider, purpose, owner, risk tier, deployment date, last validated, dependencies) — this is the strongest inventory content in the repository
- `knowledge/controls/agent-governance-controls.md` defines an Agent Registry concept with required fields
- `knowledge/bfsi/banking-ai-governance-use-cases.md` references model inventory obligations for BFSI firms

**What is missing:**
- No skill for conducting an AI inventory engagement with a client
- No structured inventory schema that can be populated, versioned, and maintained
- No workflow for keeping an inventory current (intake of new systems, retirement of old ones)
- No connection between the inventory and classification, risk assessment, or monitoring
- No third-party AI inventory capability (vendor-supplied AI systems are typically the majority of enterprise AI)

**Framework obligations unaddressed:**
- ISO 42001 Clause 8.2 (AI system lifecycle), Annex A 6.1.2 (AI system documentation)
- NIST AI RMF MAP 1.5, MAP 2.1
- EU AI Act Article 11 (technical documentation), Article 16 (obligations of providers)
- BFSI MRM SR 11-7 Section 3 (model inventory is explicitly required)
- RBI FREE-AI (AI register requirement)

---

### CAP-03: Classification

**Coverage: MODERATE (48/100)**

Risk classification is partially addressed. The regulatory mapping skill produces a risk classification section, and the knowledge base defines classification criteria for both model risk tiers and EU AI Act risk categories. The gap is that classification is embedded inside other skills rather than existing as a standalone, reusable capability.

**What exists:**
- `skills/regulatory-mapping/SKILL.md` Section 4 (Risk Classification) — classifies AI subjects under EU AI Act tiers, UK regulatory frameworks, and India DPDP/RBI/SEBI regimes. Well-specified.
- `knowledge/controls/model-risk-controls.md` defines a three-tier classification model (High / Medium / Low) with explicit criteria and consequence-based rationale
- `knowledge/bfsi/banking-ai-governance-use-cases.md` maps BFSI use cases (credit scoring, fraud detection) to risk levels
- `knowledge/frameworks/eu-ai-act.md` documents Annex III high-risk categories in detail
- `skills/governance-control-mapping/SKILL.md` accepts a `target_maturity_level` parameter that implies classification has already occurred upstream

**What is missing:**
- No standalone classification skill — classification is always a section within regulatory-mapping or an implicit input to other skills
- No BFSI MRM model risk tier classification skill (SR 11-7 tiers vs. EU AI Act tiers are different classification systems with different criteria)
- No classification workflow that produces a stable, versioned classification decision for each AI system
- No re-classification trigger when AI systems change materially
- No GPAI classification capability (EU AI Act GPAI rules require systemic risk determination)

---

### CAP-04: Risk Assessment

**Coverage: MODERATE (42/100)**

Risk assessment is split across two skills in a way that leaves a structural gap: `regulatory-mapping` assesses regulatory risk exposure, and `ai-incident-analysis` assesses risk after an incident. There is no skill that conducts a proactive, forward-looking AI risk assessment for a system that has not yet produced an incident and whose regulatory obligations are already known.

**What exists:**
- `skills/regulatory-mapping/SKILL.md` Sections 1, 3, 4 — identifies applicable regulations, obligations, and risk classification. Strong for regulatory risk.
- `skills/ai-incident-analysis/SKILL.md` Sections 2, 3, 4 — root cause analysis, risk category classification, control failures. Strong for incident-driven risk.
- `knowledge/frameworks/nist-ai-rmf.md` — MEASURE function documentation is thorough
- `knowledge/controls/model-risk-controls.md` — defines model risk assessment methodology including bias, explainability, hallucination dimensions
- `knowledge/bfsi/banking-ai-governance-use-cases.md` — risk profiles for specific BFSI use cases

**What is missing:**
- No standalone AI Risk Assessment skill for proactive risk identification before deployment
- No AI Impact Assessment capability (required by ISO 42001 Clause 6, EU AI Act for high-risk, and India DPDP SDF requirements)
- No bias and fairness risk assessment skill (Ethana's Bias Scanner is a runtime filter, not a formal bias risk assessment methodology)
- No supply chain / third-party risk assessment for AI vendor models
- No risk quantification methodology (likelihood × impact scoring)

---

### CAP-05: Gap Assessment

**Coverage: LOW (22/100)**

Gap assessment is the capability most prominently missing given the repository's stated purpose. The repository helps organisations understand governance requirements (regulatory-mapping) and design controls (governance-control-mapping) but has no skill for measuring the distance between current state and required state against a specific framework.

**What exists:**
- `skills/governance-control-mapping/SKILL.md` Section 9 (Maturity & Phased Roadmap) — a 30-60-90 day roadmap that implies a gap has been identified, but does not conduct the gap assessment itself
- `knowledge/frameworks/iso-42001.md` — documents the standard thoroughly enough that a gap assessment could be conducted with it
- `repository-maturity-review.md` — the repository assesses its own maturity but there is no corresponding skill for assessing a client's

**What is missing:**
- `skills/iso-42001-gap-assessment/` — explicitly planned but not built; blocks the Client Assessment Agent
- NIST AI RMF gap assessment skill — no equivalent
- EU AI Act conformity self-assessment skill — no equivalent
- RBI FREE-AI maturity assessment skill — no equivalent
- BFSI MRM maturity assessment skill (SR 11-7 / SS1/23 readiness) — no equivalent
- No gap assessment workflow that sequences discovery → inventory → classification → gap against a chosen framework

---

### CAP-06: Control Mapping

**Coverage: HIGH (80/100)**

Control mapping is the repository's strongest capability. The `governance-control-mapping` skill is mature, detailed, and well-structured. The controls knowledge base provides five domain-specific control libraries. The framework-crosswalk provides a mapping of controls to frameworks.

**What exists:**
- `skills/governance-control-mapping/SKILL.md` — 10-section output including Control Taxonomy Matrix, Coverage Classification, and Ethana Configuration Guide. Pass threshold 85/100. Claims Firewall enforced.
- `knowledge/controls/` — five files covering prompt injection, agent governance, data protection, audit, and model risk controls
- `knowledge/ethana/framework-crosswalk.md` — maps EU AI Act, ISO 42001, NIST AI RMF, and India regulatory requirements to Ethana capabilities and Cursory services
- Workflow: incident-assessment-workflow and regulatory-compliance-workflow both route through governance-control-mapping

**What is missing:**
- No control mapping for BFSI MRM-specific controls (SR 11-7 validation requirements, SS1/23 model documentation) — the knowledge exists in `bfsi/` but is not integrated into governance-control-mapping as a sectoral overlay
- No control mapping for RBI FREE-AI-specific controls
- No OWASP LLM Top 10 control mapping skill (OWASP knowledge exists; no skill maps a system's LLM stack against all 10 categories and produces control specifications)
- The circular dependency with ethana-feature-mapping is unresolved (noted in prior architectural review)

---

### CAP-07: Control Design

**Coverage: HIGH (75/100)**

Control design is well-served by the governance-control-mapping skill. Sections 4, 5, and 6 produce detailed preventive, detective, and corrective control specifications with trigger conditions, enforcement mechanisms, failure modes, telemetry schemas, and rollback SLAs.

**What exists:**
- `skills/governance-control-mapping/SKILL.md` Sections 4–6 — detailed control specifications for preventive, detective, and corrective controls
- `skills/governance-control-mapping/SKILL.md` Section 8 — RACI matrix for control ownership
- `knowledge/controls/` — five libraries providing base patterns for control design
- `skills/governance-control-mapping/SKILL.md` Section 10 — Ethana Configuration Guide linking controls to platform configurations

**What is missing:**
- No human oversight control design capability — EU AI Act Article 14 requires human oversight measures to be designed into systems, but neither the skill nor the knowledge base provides a structured methodology for designing oversight mechanisms
- No explainability control design — explanations for AI decisions are required under GDPR Article 22, UK Consumer Duty, EU AI Act Article 13, and BFSI adverse action requirements; no skill addresses this
- No data governance control design — ISO 42001 Annex A and EU AI Act Article 10 require data quality controls for training and validation data; the data-protection-controls.md covers inference-time privacy but not training data governance

---

### CAP-08: Control Validation

**Coverage: LOW (15/100)**

The evidence and verification framework is specified (what evidence to collect, how to collect it, retention periods) but there is no capability for actually testing whether controls are implemented and operating as designed.

**What exists:**
- `skills/governance-control-mapping/SKILL.md` Section 7 — Evidence & Verification Requirements specifies what artifacts are needed to prove controls work
- `knowledge/ethana/red-teaming.md` — covers adversarial testing as a form of security control validation
- `skills/ai-incident-analysis/SKILL.md` Section 4 — identifies control failures, which implies a form of retrospective validation
- `evaluations/scripts/claims_linter.py` — validates claims firewall compliance (a control for the OS itself, not for client AI systems)

**What is missing:**
- No control validation skill — the Control Validation Agent is mentioned in the README but not defined in `agent_certifier.py` and has no underlying skill
- No methodology for testing preventive controls (e.g., testing whether PII masking actually fires on real payloads)
- No methodology for testing detective controls (e.g., verifying alert thresholds are correctly configured)
- No methodology for testing corrective controls (e.g., running a tabletop exercise against the rollback procedure)
- No continuous control testing capability
- No integration with Ethana's Red Teaming Orchestrator as a control validation mechanism (the skill references it for platform recommendations but does not operationalise it for client control testing)

---

### CAP-09: Evidence Generation

**Coverage: MODERATE (40/100)**

Evidence requirements are well-documented within skills. Automated evidence generation does not exist. The Compliance Pack (In Build in Ethana) would address this when shipped.

**What exists:**
- `skills/governance-control-mapping/SKILL.md` Section 7 — specifies evidence artifacts, collection methods, frequencies, and retention periods
- `skills/regulatory-mapping/SKILL.md` Section 7 — specifies audit evidence types, purposes, regulatory sources, and format guidance
- `knowledge/ethana/immutable-audit-logs.md` — Ethana Audit Log is the primary evidence source for runtime AI behaviour
- `knowledge/ethana/framework-crosswalk.md` — maps ISO 42001 Cl.9.2 and EU AI Act Art.12 to the Audit Log as evidence source
- `skills/governance-control-mapping/SKILL.md` Section 10 — Ethana Configuration Guide includes evidence generation configurations

**What is missing:**
- No evidence collection workflow that assembles artifacts from multiple sources into a structured pack
- No evidence chain-of-custody mechanism — evidence must be attributable, dated, and tamper-proof; the system has no mechanism to ensure this for non-Ethana evidence
- No evidence gap detection — if a required evidence artifact is missing (e.g., a quarterly bias review was not conducted), there is no system that detects and escalates this
- No regulatory-format evidence templates (FCA SYSC 9, RBI MRM documentation requirements have specific formats)

---

### CAP-10: Audit Readiness

**Coverage: LOW (25/100)**

Audit readiness is partially described in knowledge and skills but cannot be operationalised as a coherent capability. The system can identify what evidence is needed but cannot assemble, verify, or deliver an audit pack.

**What exists:**
- `skills/regulatory-mapping/SKILL.md` Section 7 — audit evidence specification per framework
- `skills/governance-control-mapping/SKILL.md` Section 7 — verification artifacts per control
- `knowledge/ethana/immutable-audit-logs.md` — runtime evidence source
- `knowledge/ethana/deployment-and-certifications.md` — covers certification context
- Framework knowledge (ISO 42001 certification pathway, EU AI Act conformity assessment) is thorough

**What is missing:**
- No Audit Pack assembly skill — the skill would take a client's evidence vault, a target framework, and an assessment period, and produce a structured pack
- No audit readiness gap detection — "these 7 evidence items are required, 3 are missing"
- No mock audit workflow — the maturity review mentions "mock audits" as a Phase 3 activity in the governance-control-mapping roadmap, but no mock audit skill or workflow exists
- No certification pathway workflow for ISO 42001 — the standard's certification process requires Stage 1 and Stage 2 audits with specific documentation; no workflow addresses this
- No EU AI Act conformity assessment workflow (required for high-risk AI before deployment)

---

### CAP-11: Continuous Monitoring

**Coverage: ABSENT (10/100)**

Continuous monitoring is the single largest gap in the repository relative to framework obligations. Every major framework requires it. The repository has no skill, workflow, or agent that addresses ongoing production monitoring of deployed AI systems.

**What exists:**
- `knowledge/frameworks/nist-ai-rmf.md` — MANAGE function covers production monitoring requirements; well-documented
- `knowledge/frameworks/iso-42001.md` — Clause 9.1 (monitoring and measurement) documented
- `knowledge/controls/model-risk-controls.md` — defines monitoring controls (drift detection, performance degradation, bias monitoring in production)
- `knowledge/controls/audit-controls.md` — defines logging and alerting controls
- `knowledge/ethana/immutable-audit-logs.md` — Ethana Audit Log is a monitoring data source

**What is missing:**
- No monitoring skill — no structured output for designing a monitoring programme for a specific AI system
- No monitoring workflow — no process for conducting periodic performance reviews, generating drift reports, or escalating anomalies
- No monitoring agent — the Regulatory Watch Agent monitors regulatory changes but not AI system behaviour
- No KPI/KRI specification capability — what metrics to track, at what threshold to alert, and what the escalation path is
- No model drift detection capability — knowledge exists but no skill produces a drift assessment
- No bias monitoring programme design — in production, bias can drift as population distributions change; no capability addresses this
- No monitoring for agent behaviour — autonomous agents operating in production need specific behavioural monitoring; this is not addressed even in the agent governance knowledge

---

### CAP-12: Incident Management

**Coverage: MODERATE-HIGH (65/100)**

This is the repository's second-strongest capability after control mapping. The ai-incident-analysis skill is well-designed and the incident-assessment-workflow sequences it through governance-control-mapping and capability validation. The gaps are in operational readiness: notification, escalation, and post-incident review process.

**What exists:**
- `skills/ai-incident-analysis/SKILL.md` — 10-section output covering root cause analysis, control failures, framework mapping, regulatory implications, BFSI impact, recommended controls. Pass threshold 70/100.
- `workflows/incident-assessment-workflow.md` — sequences IA → GCM → ECV
- `knowledge/ai-incidents/` — 5 incident case studies for precedent and pattern recognition
- `knowledge/controls/prompt-injection-controls.md`, `agent-governance-controls.md` — incident-specific control libraries
- `knowledge/ethana/red-teaming.md` — proactive incident simulation

**What is missing:**
- No regulatory notification skill — incidents may trigger mandatory reporting obligations (EU AI Act Art.73 GPAI incident reporting; DPDP Act breach notification; RBI incident reporting under IT governance directions); no skill or workflow addresses the notification process
- No DFIR (Digital Forensics and Incident Response) procedure — incident response in AI systems differs from traditional DFIR; no structured IR playbook exists
- No incident classification and severity scoring at intake — before analysis, incidents need to be triaged for severity, urgency, and regulatory notification trigger
- No post-incident review workflow — the five-whys in ai-incident-analysis is good but there is no structured process for tracking corrective action implementation and closure
- No incident register — incidents are analysed individually with no accumulation into a searchable, trend-able incident database

---

### CAP-13: Regulatory Mapping

**Coverage: HIGH (75/100)**

Regulatory mapping is the repository's strongest advisory capability alongside control mapping. The skill is well-specified across three jurisdictions with strong BFSI integration.

**What exists:**
- `skills/regulatory-mapping/SKILL.md` — 9-section output covering applicable regulations, framework mapping, obligations, risk classification, documentation requirements, control requirements, audit evidence, BFSI considerations, and executive summary. Strong pass threshold enforcement.
- `knowledge/regulations/eu-ai-act.md` — thorough EU AI Act coverage including risk tiers, GPAI obligations, conformity assessment requirements
- `knowledge/regulations/uk-ai-guidance.md` — FCA, PRA SS1/23, ICO, DPA 2018 coverage
- `knowledge/regulations/india-ai-landscape.md` — DPDP Act, RBI IT Governance, SEBI AI/ML, IRDAI coverage
- `knowledge/bfsi/` — four files covering banking, insurance, wealth management, and GCC governance patterns
- `workflows/regulatory-compliance-workflow.md` — sequences RM → GCM → ESM

**What is missing:**
- No US jurisdiction — NIST AI RMF is a framework (covered) but US state AI laws (Colorado AI Act, Illinois BIPA, New York Local Law 144), EEOC AI guidance, FTC AI principles, and sector-specific rules (OCC model risk for US banks) are absent
- No regulatory change management — when a regulation changes (new RBI circular, EU implementing act), there is no process to update affected assessments
- No RBI FREE-AI dedicated skill — the India landscape file covers RBI MRM but FREE-AI as a distinct framework has no dedicated coverage
- No regulatory watch capability — the system maps regulations as they were when written; it does not monitor for new obligations

---

### CAP-14: Third Party AI Risk

**Coverage: ABSENT (10/100)**

Third-party AI risk is the second-largest gap in the repository. Most enterprise AI deployments are dominated by vendor-supplied AI: foundation models (OpenAI, Anthropic, Google), AI-embedded SaaS (Microsoft Copilot, Salesforce Einstein), and AI APIs. The repository treats third-party AI risk as a control category to mention but not a capability to operationalise.

**What exists:**
- `knowledge/frameworks/iso-42001.md` — Clause 8 includes third-party AI provider management as a requirement
- `knowledge/controls/agent-governance-controls.md` — MCP third-party tool risks are addressed (tool allow-list, rate limits)
- `knowledge/ai-incidents/mcp-vulnerability-risks.md` — MCP protocol supply chain risks documented
- `knowledge/ethana/mcp-security.md` — MCP security controls for the Ethana platform
- `skills/regulatory-mapping/SKILL.md` — when `deployment_model` = "third-party SaaS" the skill will note obligations, but there is no dedicated section

**What is missing:**
- No vendor AI assessment skill — no structured output for assessing a specific third-party AI tool's governance posture
- No foundation model risk assessment — risks specific to third-party foundation models (training data lineage, model weights provenance, model card adequacy, vendor incident notification) are not addressed
- No vendor AI contract review capability — what contractual controls should be required of AI vendors
- No supply chain AI risk workflow — discovering, assessing, and continuously monitoring third-party AI risks requires a distinct workflow
- No TPAI (Third Party AI) register — tracking approved, under-review, and prohibited external AI tools
- ISO 42001 Clause 8, NIST AI RMF GOVERN 6.2 (third-party risk), EU AI Act importer/distributor obligations are all unaddressed

---

### CAP-15: Agent Governance

**Coverage: LOW (30/100)**

Agent governance has strong knowledge depth but minimal operationalisation. The controls are specified; no skill or workflow applies them to a specific client's agentic deployment.

**What exists:**
- `knowledge/controls/agent-governance-controls.md` — comprehensive: scope and capability definition, least privilege, HITL gates, monitoring, identity management, tool isolation, incident response. Best-in-class knowledge content.
- `knowledge/ai-incidents/mcp-vulnerability-risks.md` — MCP-specific attack vectors and defences
- `knowledge/ethana/mcp-security.md` — Ethana MCP Security Broker production capabilities
- `skills/governance-control-mapping/SKILL.md` — accepts agent governance controls as a control domain; references `agent-governance-controls.md` as a knowledge dependency
- `skills/ethana-feature-mapping/SKILL.md` — includes MCP Security Broker as a validated feature

**What is missing:**
- No agent governance assessment skill — no structured output that evaluates a specific agentic deployment against the agent governance control framework
- No Agent Registry skill — building and maintaining an agent registry (the foundational control in agent governance) has no skill behind it
- No agentic risk assessment — agents introduce risks not addressed by the standard AI risk assessment (multi-step amplification, irreversible actions, opaque reasoning, identity abuse)
- No agent HITL policy design skill — defining which actions require human approval, at what thresholds, through what mechanism
- No non-human identity governance capability — NHI lifecycle management (credential issuance, rotation, revocation) for agents is In Build in Ethana; no advisory skill bridges this gap today
- NIST AI RMF MAP 1.6 (agent/tool mapping) has only a partial technical mapping to MCP Broker; the governance posture for agentic systems is not addressed

---

### CAP-16: Model Governance

**Coverage: LOW (28/100)**

Model governance has thorough knowledge content across the BFSI model risk files but no operationalised skill or workflow for conducting a model governance assessment or managing the model lifecycle.

**What exists:**
- `knowledge/controls/model-risk-controls.md` — comprehensive: model inventory, risk tier classification, development controls, validation controls, monitoring controls, governance structure, third-party model obligations
- `knowledge/bfsi/banking-ai-governance-use-cases.md` — detailed risk profiles for BFSI model use cases (credit scoring, fraud detection, AML, customer service, trading)
- `knowledge/bfsi/wealth-management-ai-governance.md`, `insurance-ai-governance.md`, `gcc-ai-governance-patterns.md` — sector-specific model governance patterns
- `skills/regulatory-mapping/SKILL.md` Section 8 — BFSI Considerations includes model risk management requirements for PRA SS1/23, FCA, RBI
- `skills/governance-control-mapping/SKILL.md` — references `model-risk-controls.md` as a knowledge dependency; model risk controls are a valid control domain input

**What is missing:**
- No model governance assessment skill — no structured skill for assessing a specific model's governance posture against SR 11-7 or SS1/23
- No model validation workflow — independent model validation is a core SR 11-7 and SS1/23 requirement; it requires a structured process (challenger model, out-of-time sample testing, sensitivity analysis) that no skill addresses
- No model documentation skill — technical documentation for models (EU AI Act Article 11, SR 11-7 model documentation) requires a specific structured output
- No model retirement/decommissioning workflow — model retirement is a governance event requiring documentation, notification, and control removal
- No LLM-specific model risk assessment — the model-risk-controls.md notes LLM-specific risks (hallucination, prompt sensitivity, emergent capabilities, context dependence) but no skill produces an LLM model risk assessment

---

## 2. Missing Capability Map

Capabilities that must be built, ranked by framework criticality.

| Priority | Missing Capability | Required By | Blocking |
|---|---|---|---|
| 1 | **AI Discovery** | ISO 42001 Cl.8, NIST MAP 1.5, EU AI Act Art.6, RBI FREE-AI, BFSI MRM | Inventory, Classification, Gap Assessment, all downstream |
| 2 | **AI Inventory Management** | ISO 42001 Cl.8.2, NIST MAP 2.1, SR 11-7, RBI FREE-AI | Classification, Risk Assessment, all monitoring |
| 3 | **Continuous Monitoring** | ISO 42001 Cl.9.1, NIST MANAGE 4.1–4.2, EU AI Act Art.72, RBI FREE-AI | Audit Readiness, Model Governance |
| 4 | **ISO 42001 Gap Assessment** | ISO 42001 certification pathway | Client Assessment Agent |
| 5 | **AI Impact Assessment** | ISO 42001 Cl.6, EU AI Act Art.9, India DPDP SDF, RBI FREE-AI | Risk Assessment completeness |
| 6 | **Third Party AI Risk Assessment** | ISO 42001 Cl.8, NIST GOVERN 6.2, EU AI Act importer/distributor | Vendor AI engagement |
| 7 | **Model Governance Assessment** | SR 11-7, PRA SS1/23, RBI MRM, EU AI Act Art.9–11 | BFSI client readiness |
| 8 | **Agent Governance Assessment** | NIST AI RMF MAP 1.6, ISO 42001 Annex A, AI security governance | Agentic deployment clients |
| 9 | **Control Validation** | ISO 42001 Cl.9, NIST MEASURE 4, EU AI Act Art.9 | Audit Readiness, Evidence Generation |
| 10 | **Audit Pack Assembly** | ISO 42001 Cl.9.2, EU AI Act Art.12, RBI FREE-AI | Audit Readiness |
| 11 | **Regulatory Notification** | EU AI Act Art.73, DPDP Act breach notification, RBI IT Governance | Incident Management completeness |
| 12 | **Bias and Fairness Assessment** | EU AI Act Art.10, ISO 42001 Annex A, BFSI fairness obligations | Risk Assessment, Model Governance |
| 13 | **Model Documentation** | EU AI Act Art.11, SR 11-7, SS1/23, ISO 42001 | Audit Readiness, Model Governance |
| 14 | **Human Oversight Design** | EU AI Act Art.14, ISO 42001 Annex A, NIST GOVERN | Control Design completeness |
| 15 | **RBI FREE-AI Assessment** | RBI FREE-AI framework | India BFSI clients |
| 16 | **NIST AI RMF Gap Assessment** | NIST AI RMF, referenced by US operations | International clients |

---

## 3. Coverage Matrix

Rating scale: **FULL** (>85%) · **HIGH** (70–84%) · **MODERATE** (40–69%) · **LOW** (15–39%) · **ABSENT** (<15%)

| Capability | ISO 42001 | NIST AI RMF | EU AI Act | RBI FREE-AI | BFSI MRM | AI Security | **Overall** |
|---|---|---|---|---|---|---|---|
| **Discovery** | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | **ABSENT** |
| **Inventory** | ABSENT | LOW | ABSENT | ABSENT | LOW | ABSENT | **LOW** |
| **Classification** | MODERATE | MODERATE | MODERATE | LOW | MODERATE | LOW | **MODERATE** |
| **Risk Assessment** | LOW | MODERATE | MODERATE | LOW | LOW | MODERATE | **MODERATE** |
| **Gap Assessment** | ABSENT | ABSENT | LOW | ABSENT | ABSENT | ABSENT | **LOW** |
| **Control Mapping** | HIGH | HIGH | HIGH | MODERATE | MODERATE | HIGH | **HIGH** |
| **Control Design** | HIGH | HIGH | MODERATE | MODERATE | MODERATE | HIGH | **HIGH** |
| **Control Validation** | ABSENT | LOW | ABSENT | ABSENT | ABSENT | LOW | **LOW** |
| **Evidence Generation** | MODERATE | MODERATE | MODERATE | LOW | MODERATE | LOW | **MODERATE** |
| **Audit Readiness** | LOW | LOW | LOW | ABSENT | LOW | ABSENT | **LOW** |
| **Continuous Monitoring** | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | LOW | **ABSENT** |
| **Incident Management** | MODERATE | HIGH | MODERATE | LOW | MODERATE | HIGH | **HIGH** |
| **Regulatory Mapping** | HIGH | HIGH | HIGH | MODERATE | HIGH | MODERATE | **HIGH** |
| **Third Party AI Risk** | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | LOW | **ABSENT** |
| **Agent Governance** | LOW | LOW | ABSENT | ABSENT | ABSENT | MODERATE | **LOW** |
| **Model Governance** | LOW | LOW | LOW | LOW | LOW | LOW | **LOW** |

### Framework Coverage Summary

| Framework | Capabilities Fully/Highly Covered | Capabilities Absent/Low | Coverage Score |
|---|---|---|---|
| **ISO 42001** | Control Mapping, Control Design, Regulatory Mapping | Discovery, Inventory, Gap Assessment, Control Validation, Monitoring, Third Party AI | 38/100 |
| **NIST AI RMF** | Control Mapping, Control Design, Incident Management, Regulatory Mapping | Discovery, Gap Assessment, Control Validation, Monitoring, Third Party AI | 44/100 |
| **EU AI Act** | Control Mapping, Control Design, Regulatory Mapping, Incident Management | Discovery, Inventory, Gap Assessment, Control Validation, Monitoring, Third Party AI | 41/100 |
| **RBI FREE-AI** | Control Mapping, Regulatory Mapping (partial) | Discovery, Inventory, Gap Assessment, Control Validation, Monitoring, Third Party AI, Agent, Model | 28/100 |
| **BFSI MRM** | Control Mapping, Regulatory Mapping, Incident Management | Discovery, Inventory, Control Validation, Monitoring, Model Governance | 32/100 |
| **AI Security** | Control Mapping, Control Design, Incident Management, Regulatory Mapping | Discovery, Control Validation, Monitoring, Third Party AI, Agent Governance | 46/100 |

---

## 4. Maturity Score

### Per-Capability Maturity

| # | Capability | Knowledge | Skill | Workflow | Agent | **Score** | **Grade** |
|---|---|---|---|---|---|---|---|
| 1 | Discovery | 8 | 0 | 0 | 0 | **8** | F |
| 2 | Inventory | 18 | 0 | 0 | 0 | **18** | F |
| 3 | Classification | 20 | 15 | 8 | 0 | **43** | D |
| 4 | Risk Assessment | 20 | 12 | 5 | 0 | **37** | D |
| 5 | Gap Assessment | 15 | 0 | 0 | 0 | **15** | F |
| 6 | Control Mapping | 20 | 35 | 20 | 0 | **75** | B |
| 7 | Control Design | 20 | 30 | 20 | 0 | **70** | B |
| 8 | Control Validation | 8 | 2 | 0 | 0 | **10** | F |
| 9 | Evidence Generation | 15 | 15 | 5 | 0 | **35** | D |
| 10 | Audit Readiness | 12 | 8 | 0 | 0 | **20** | F |
| 11 | Continuous Monitoring | 12 | 0 | 0 | 0 | **12** | F |
| 12 | Incident Management | 20 | 25 | 15 | 0 | **60** | C |
| 13 | Regulatory Mapping | 20 | 35 | 15 | 0 | **70** | B |
| 14 | Third Party AI Risk | 5 | 0 | 0 | 0 | **5** | F |
| 15 | Agent Governance | 18 | 5 | 2 | 0 | **25** | F |
| 16 | Model Governance | 18 | 5 | 0 | 0 | **23** | F |

*Scoring: Knowledge (0–20) · Skill (0–35) · Workflow (0–25) · Agent (0–20)*

### Overall Governance OS Maturity

| Dimension | Score | Comment |
|---|---|---|
| **Advisory capability** (knowledge + skills) | 61/100 | Strong in control mapping, regulatory mapping, incident management. Weak in discovery, monitoring, third-party, agent/model governance. |
| **Operational capability** (workflows + execution) | 28/100 | Five workflows documented but none executable. Agent layer empty. No monitoring. |
| **Automation** (agents + evaluation) | 8/100 | Three agents ready-to-build but unbuilt. Evaluation scripts exist with no test data. |
| **Framework completeness** | 38/100 | Control mapping and regulatory mapping are strong; seven capability areas are absent. |

**Overall Governance OS Maturity: 34/100**

This score reflects the gap between a strong advisory specification layer and the absence of seven entire capability domains required by the target frameworks. The system is not yet a governance operating system — it is a governance advisory toolkit with an excellent control mapping and regulatory mapping core.

---

## 5. Recommended New Skills

Each skill is specified with its purpose, required inputs, expected outputs, knowledge dependencies, and the frameworks it addresses.

---

### SKILL-NEW-01: `ai-discovery`

**Priority:** Critical  
**Category:** Governance Intelligence  
**Addresses:** Discovery (CAP-01), Inventory foundation (CAP-02)  
**Frameworks:** ISO 42001 Cl.4+8, NIST MAP 1.5+2.1, EU AI Act Art.6, RBI FREE-AI, BFSI MRM

**Purpose:** Conducts a structured AI discovery exercise for a client organisation, identifying all deployed, in-development, and planned AI systems across business units and technology stacks. Produces a discovery report that populates the AI inventory.

**Required inputs:**
- `organisation_profile` — size, sector, geography, technology landscape overview
- `discovery_scope` — business units in scope, included/excluded environments
- `discovery_method` — interview-based, document-based, technical scan (API logs, cloud billing), or combined
- `ai_system_categories` — LLMs, ML models, AI-embedded SaaS, AI APIs, autonomous agents

**Output sections (8):**
1. Discovery Methodology and Scope
2. Identified AI Systems Register (structured table with system name, type, business function, data processed, owner, deployment status)
3. Shadow AI Assessment (unsanctioned AI use identified)
4. Third-Party AI Footprint (vendor-supplied AI not in IT register)
5. Agent and Automation Inventory (autonomous agents, RPA with AI components)
6. Data Flow Map (where AI systems access, process, and output sensitive data)
7. Discovery Gaps and Confidence Assessment
8. Handoff to Inventory Population

**Knowledge dependencies:** `knowledge/controls/model-risk-controls.md`, `knowledge/controls/agent-governance-controls.md`, `knowledge/frameworks/nist-ai-rmf.md`

---

### SKILL-NEW-02: `ai-inventory-management`

**Priority:** Critical  
**Category:** Governance Intelligence  
**Addresses:** Inventory (CAP-02), Model Governance foundation (CAP-16)  
**Frameworks:** ISO 42001 Cl.8.2, NIST MAP 2.1, SR 11-7, PRA SS1/23, RBI FREE-AI

**Purpose:** Builds and maintains a structured AI inventory for a client organisation. Accepts discovery outputs and produces a versioned, maintained AI System Register with full governance metadata, lifecycle status, and risk tier assignment.

**Required inputs:**
- `discovery_output` — structured output from `ai-discovery` skill (or equivalent)
- `inventory_schema` — target schema (default Cursory standard; custom for enterprise integration)
- `classification_criteria` — risk tier thresholds applicable to client sector

**Output sections (7):**
1. AI System Register (full structured inventory with all required fields)
2. Risk Tier Assignment (High / Medium / Low per defined criteria)
3. Regulatory Profile per System (which regulations apply to each system)
4. Ownership and Accountability Matrix (business owner, technical owner, risk owner per system)
5. Lifecycle Status Summary (development, testing, production, deprecated)
6. Inventory Maintenance Protocol (triggers for update, governance of new system additions)
7. Gap and Completeness Assessment

**Knowledge dependencies:** `knowledge/controls/model-risk-controls.md`, `knowledge/bfsi/banking-ai-governance-use-cases.md`, all regulations files

---

### SKILL-NEW-03: `iso-42001-gap-assessment`

**Priority:** Critical  
**Category:** Gap Assessment  
**Addresses:** Gap Assessment (CAP-05)  
**Frameworks:** ISO 42001 (all clauses and Annex A)

**Purpose:** Measures a client organisation's current AI Management System posture against ISO 42001 clause-by-clause and Annex A control-by-control. Produces a structured gap register, a maturity score per clause, a certification readiness assessment, and a prioritised remediation roadmap.

**Required inputs:**
- `organisation_profile` — size, sector, existing management systems (ISO 27001, ISO 9001)
- `aims_scope` — which AI systems and business units are in scope for the AIMS
- `evidence_provided` — policies, procedures, records, and other evidence the client provides

**Output sections (8):**
1. AIMS Scope and Context Assessment (Clauses 4–5)
2. Planning and Risk Assessment Gap (Clause 6)
3. Support Requirements Gap (Clause 7)
4. Operational Controls Gap (Clause 8 — lifecycle, third parties, impact assessments)
5. Performance Evaluation Gap (Clause 9 — monitoring, internal audit, management review)
6. Improvement Mechanisms Gap (Clause 10)
7. Annex A Controls Gap Register (38 controls, RAG status per control)
8. Certification Readiness Assessment and Remediation Roadmap

**Knowledge dependencies:** `knowledge/frameworks/iso-42001.md`, `knowledge/controls/` (all five files), `knowledge/regulations/` (all three files)

---

### SKILL-NEW-04: `ai-risk-assessment`

**Priority:** Critical  
**Category:** Governance Intelligence  
**Addresses:** Risk Assessment (CAP-04), Gap Assessment foundation (CAP-05)  
**Frameworks:** ISO 42001 Cl.6, NIST MAP+MEASURE, EU AI Act Art.9, RBI FREE-AI

**Purpose:** Conducts a proactive, forward-looking AI risk assessment for a specific AI system or use case. Distinct from regulatory-mapping (which identifies what laws apply) and ai-incident-analysis (which analyses past failures). This skill assesses what could go wrong before it happens.

**Required inputs:**
- `ai_system_description` — what the system does, how it works, what data it processes
- `risk_assessment_scope` — inherent risk identification, control effectiveness, residual risk, or all
- `risk_framework` — ISO 42001, NIST AI RMF, RBI FREE-AI, EU AI Act Art.9, BFSI MRM, or custom
- `assessment_horizon` — as-built (current), as-planned (pre-deployment), or change-triggered

**Output sections (9):**
1. AI System Profile and Risk Context
2. Threat and Harm Identification (what could go wrong, who could be harmed)
3. Inherent Risk Assessment (likelihood × impact before controls)
4. AI Impact Assessment (for affected individuals and society — ISO 42001 Cl.6, EU AI Act requirement)
5. Current Control Effectiveness Assessment
6. Residual Risk Determination
7. Risk Treatment Recommendations (accept / mitigate / transfer / avoid)
8. Risk Register (structured table with ownership and review dates)
9. Executive Risk Summary

**Knowledge dependencies:** `knowledge/frameworks/` (all three), `knowledge/controls/` (all five), `knowledge/bfsi/` (all four), `knowledge/regulations/` (all three)

---

### SKILL-NEW-05: `continuous-monitoring-design`

**Priority:** Critical  
**Category:** Control Operationalization  
**Addresses:** Continuous Monitoring (CAP-11), Control Validation foundation (CAP-08)  
**Frameworks:** ISO 42001 Cl.9.1, NIST MANAGE 4.1–4.2, EU AI Act Art.72, RBI FREE-AI, BFSI MRM

**Purpose:** Designs a comprehensive production monitoring programme for a deployed AI system. Produces monitoring specifications including KPIs, KRIs, alert thresholds, reporting cadences, escalation paths, and a monitoring dashboard design.

**Required inputs:**
- `ai_system_profile` — system type, deployment context, risk tier
- `monitoring_scope` — performance, fairness, security, regulatory, or all
- `existing_monitoring_tools` — SIEM, APM, BI tools in use
- `reporting_audience` — technical team, risk committee, board, regulator

**Output sections (8):**
1. Monitoring Strategy and Governance
2. Performance KPIs (accuracy, latency, throughput — system-specific)
3. Fairness and Bias KRIs (demographic disparity metrics, production monitoring thresholds)
4. Security Monitoring Specifications (anomaly detection, injection attempt rates, exfiltration indicators)
5. Regulatory Compliance Monitoring (ongoing obligation status, evidence generation schedule)
6. Alert Design and Escalation Matrix
7. Reporting Cadence and Dashboard Design
8. Monitoring Programme Maturity Assessment

**Knowledge dependencies:** `knowledge/controls/audit-controls.md`, `knowledge/controls/model-risk-controls.md`, `knowledge/frameworks/nist-ai-rmf.md`, `knowledge/ethana/immutable-audit-logs.md`

---

### SKILL-NEW-06: `third-party-ai-risk-assessment`

**Priority:** High  
**Category:** Governance Intelligence  
**Addresses:** Third Party AI Risk (CAP-14)  
**Frameworks:** ISO 42001 Cl.8, NIST GOVERN 6.2, EU AI Act importer/distributor obligations, BFSI MRM (model vendor risk), RBI FREE-AI

**Purpose:** Assesses the governance posture and risk profile of a specific third-party AI system, foundation model, or AI vendor. Produces a vendor AI risk rating, a contractual control requirement specification, and an ongoing monitoring framework for the vendor relationship.

**Required inputs:**
- `vendor_ai_description` — what the third-party AI system does, the vendor's identity, the contract scope
- `usage_context` — how the client uses the third-party AI, what data it accesses, what decisions it informs
- `vendor_documentation` — model card, system card, SOC 2 report, ISO 27001 certificate, privacy policy (as available)
- `client_sector` — sector for regulatory overlay

**Output sections (8):**
1. Third-Party AI System Profile
2. Vendor Governance Assessment (does the vendor have documented AI governance practices?)
3. Model Provenance and Training Data Risk
4. Data Processing and Privacy Risk (what client/customer data the vendor AI accesses)
5. Dependency and Concentration Risk
6. Contractual Control Requirements (what must be in the vendor contract)
7. Ongoing Monitoring Requirements
8. Vendor AI Risk Rating and Recommendation

**Knowledge dependencies:** `knowledge/frameworks/iso-42001.md`, `knowledge/controls/data-protection-controls.md`, `knowledge/ai-incidents/mcp-vulnerability-risks.md`, all regulations files

---

### SKILL-NEW-07: `agent-governance-assessment`

**Priority:** High  
**Category:** Governance Intelligence  
**Addresses:** Agent Governance (CAP-15)  
**Frameworks:** NIST AI RMF MAP 1.6, ISO 42001 Annex A, AI Security Governance, RBI FREE-AI (agentic AI)

**Purpose:** Assesses a specific agentic AI deployment against the full agent governance control framework. Produces an agent risk profile, a control gap register, an Agent Registry entry, and a HITL policy specification.

**Required inputs:**
- `agent_description` — what the agent does, what tools it has access to, what systems it can interact with
- `agent_architecture` — orchestration framework, tool protocol (MCP, function calling, ReAct), identity model
- `deployment_context` — production vs. development, user-facing vs. back-office, human oversight level
- `actions_permitted` — the full list of actions the agent can take

**Output sections (8):**
1. Agent Profile and Capability Scope
2. Risk Classification (criticality of actions, blast radius of failures, irreversibility)
3. Scope and Capability Control Assessment
4. Identity and Least Privilege Assessment (NHI design, credential model, permission scope)
5. HITL Gate Policy Design (which actions require human approval, at what thresholds)
6. Monitoring and Audit Trail Assessment
7. Incident Response Plan for Agent Failures
8. Agent Registry Entry (structured record for the client's Agent Register)

**Knowledge dependencies:** `knowledge/controls/agent-governance-controls.md`, `knowledge/ai-incidents/mcp-vulnerability-risks.md`, `knowledge/ethana/mcp-security.md`, `knowledge/frameworks/nist-ai-rmf.md`

---

### SKILL-NEW-08: `model-governance-assessment`

**Priority:** High  
**Category:** Governance Intelligence  
**Addresses:** Model Governance (CAP-16)  
**Frameworks:** SR 11-7, PRA SS1/23, RBI MRM, ISO 42001 Cl.8, EU AI Act Art.9–11

**Purpose:** Assesses a specific AI/ML model against model risk management requirements. Produces a model validation readiness assessment, a documentation gap analysis, a monitoring programme design, and a model governance score.

**Required inputs:**
- `model_description` — model type, purpose, inputs, outputs, decision impact
- `model_tier` — risk tier (high / medium / low) or assessment to be determined
- `mrm_framework` — SR 11-7, PRA SS1/23, RBI MRM, or client-specific
- `evidence_provided` — existing model documentation, validation reports, monitoring data

**Output sections (9):**
1. Model Profile and Risk Tier Assessment
2. Model Development Controls Assessment (data governance, bias testing, performance benchmarking)
3. Model Documentation Gap Analysis (technical documentation against EU AI Act Art.11 / SR 11-7)
4. Independent Validation Readiness Assessment
5. Challenger Model and Benchmarking Assessment
6. Production Monitoring Programme Assessment
7. Model Change Management and Version Control Assessment
8. Model Retirement and Decommissioning Controls
9. MRM Compliance Score and Remediation Roadmap

**Knowledge dependencies:** `knowledge/controls/model-risk-controls.md`, `knowledge/bfsi/banking-ai-governance-use-cases.md`, `knowledge/bfsi/wealth-management-ai-governance.md`, `knowledge/regulations/eu-ai-act.md`, `knowledge/regulations/uk-ai-guidance.md`

---

### SKILL-NEW-09: `bias-fairness-assessment`

**Priority:** High  
**Category:** Governance Intelligence  
**Addresses:** Risk Assessment (CAP-04), Control Validation (CAP-08), Model Governance (CAP-16)  
**Frameworks:** EU AI Act Art.10, ISO 42001 Annex A, BFSI MRM, NYC Local Law 144, UK Equality Act

**Purpose:** Conducts a structured bias and fairness assessment for a specific AI system. Distinct from Ethana's runtime Bias Scanner (a detection filter). This skill designs a methodology for statistical bias evaluation, interprets results, and produces a regulatory-ready bias assessment report.

**Required inputs:**
- `model_description` — model type, purpose, affected populations
- `fairness_metrics` — which metrics to assess (demographic parity, equalized odds, individual fairness)
- `protected_characteristics` — which characteristics to evaluate (race, gender, age, disability)
- `evidence_provided` — model outputs, demographic breakdown data (if available)
- `regulatory_context` — which fairness obligations apply (EU AI Act, NYC LL144, FCA Consumer Duty)

**Output sections (7):**
1. Fairness Assessment Scope and Methodology
2. Protected Characteristic Analysis
3. Statistical Bias Findings (or methodology specification when data not provided)
4. Regulatory Compliance Assessment per Framework
5. Bias Mitigation Options
6. Ongoing Fairness Monitoring Design
7. Bias Assessment Report (formatted for regulator or internal audit submission)

**Knowledge dependencies:** `knowledge/controls/model-risk-controls.md`, `knowledge/regulations/eu-ai-act.md`, `knowledge/regulations/uk-ai-guidance.md`, `knowledge/bfsi/banking-ai-governance-use-cases.md`

---

### SKILL-NEW-10: `audit-pack-assembly`

**Priority:** High  
**Category:** Audit Readiness  
**Addresses:** Audit Readiness (CAP-10), Evidence Generation (CAP-09)  
**Frameworks:** ISO 42001 Cl.9.2, EU AI Act Art.12+72, RBI FREE-AI, BFSI MRM

**Purpose:** Assembles a structured, complete audit evidence pack for a specific AI system, framework, and assessment period. Takes evidence references from prior skill outputs and the client's evidence vault, identifies gaps, and produces a submission-ready audit pack.

**Required inputs:**
- `target_framework` — ISO 42001, EU AI Act, RBI FREE-AI, BFSI MRM, or custom
- `assessment_period` — start and end dates for the evidence period
- `ai_system_scope` — which systems are in scope for this audit
- `evidence_provided` — list of available evidence artifacts with locations
- `audit_type` — internal audit, external certification, regulatory examination, or board review

**Output sections (7):**
1. Audit Scope and Framework Mapping
2. Evidence Inventory (all required artifacts, with availability status: present / missing / partial)
3. Evidence Gap Register (missing artifacts with remediation path)
4. Audit Pack Structure (how to organise the evidence submission)
5. Attestation Requirements (what must be signed off and by whom)
6. Pre-Audit Remediation Plan (actions before submission date)
7. Audit Pack Submission Checklist

**Knowledge dependencies:** `skills/governance-control-mapping/evaluation.md`, `skills/regulatory-mapping/SKILL.md`, `knowledge/ethana/immutable-audit-logs.md`, all framework files

---

### SKILL-NEW-11: `rbi-free-ai-assessment`

**Priority:** High (India BFSI clients)  
**Category:** Gap Assessment  
**Addresses:** Gap Assessment (CAP-05), Regulatory Mapping (CAP-13)  
**Frameworks:** RBI FREE-AI (all pillars)

**Purpose:** Assesses a client's AI governance posture specifically against RBI's Framework for Responsible and Ethical Enablement of AI. Produces a pillar-by-pillar gap assessment, a compliance score, and a remediation roadmap specifically calibrated for RBI-regulated entities.

**Output sections (8):**
1. RBI FREE-AI Applicability Assessment
2. Governance Structure and Accountability Gap (Pillar 1: AI governance framework)
3. AI Risk Management Gap (Pillar 2: risk identification and management)
4. Model Risk and Validation Gap (Pillar 3: model governance, SR 11-7 India equivalent)
5. Transparency and Explainability Gap (Pillar 4: explainable AI for decisions)
6. Fairness and Ethics Gap (Pillar 5: bias, fairness, discrimination)
7. Data Governance Gap (Pillar 6: data quality, provenance, localisation)
8. RBI FREE-AI Compliance Score and Remediation Roadmap

**Knowledge dependencies:** `knowledge/regulations/india-ai-landscape.md`, `knowledge/bfsi/banking-ai-governance-use-cases.md`, `knowledge/controls/model-risk-controls.md`, `knowledge/controls/data-protection-controls.md`

---

### SKILL-NEW-12: `proposal-review`

**Priority:** High  
**Category:** Quality Assurance  
**Addresses:** Audit Readiness (CAP-10) — claims audit before commercial delivery  
**Frameworks:** Internal claims firewall enforcement

**Purpose:** Performs a final compliance review of a draft proposal or RFP response before client delivery. Validates every capability claim against canonical-product-model.md, flags prohibited claims, confirms BFSI sector-specific guardrails are applied, and produces a release-authorised version.

**Knowledge dependencies:** `knowledge/ethana/canonical-product-model.md` (Tier 1 mandatory), all skill outputs being reviewed

---

## 6. Recommended New Workflows

Each workflow sequences existing and new skills into an end-to-end operational process.

---

### WF-NEW-01: `ai-discovery-and-inventory-workflow`

**Addresses:** CAP-01, CAP-02  
**Trigger:** New client onboarding OR annual inventory refresh  
**Skill sequence:**
```
[Client Profile + Scope Agreement]
        │
        ▼
1. ai-discovery (identify all AI systems)
        │
        ▼ (Discovery Report)
2. ai-inventory-management (build structured inventory with risk tiers)
        │
        ▼ (AI System Register)
3. regulatory-mapping (per system — which regulations apply to each)
        │
        ▼
[Client AI Inventory + Per-System Regulatory Profile]
```
**Output:** Versioned AI System Register, per-system regulatory obligation summaries, discovery confidence assessment

---

### WF-NEW-02: `governance-gap-assessment-workflow`

**Addresses:** CAP-05, CAP-03, CAP-04  
**Trigger:** Client requests framework alignment assessment OR pre-certification engagement  
**Skill sequence:**
```
[Client Profile + Target Framework]
        │
        ▼
1. ai-inventory-management (confirm inventory current)
        │
        ▼
2. ai-risk-assessment (per-system risk profile)
        │
        ▼
3. [Branch by framework]
   ├── iso-42001-gap-assessment
   ├── rbi-free-ai-assessment
   └── nist-ai-rmf-gap-assessment (planned)
        │
        ▼
4. governance-control-mapping (design controls for identified gaps)
        │
        ▼
[Gap Register + Control Roadmap + Certification Readiness Score]
```

---

### WF-NEW-03: `continuous-monitoring-programme-workflow`

**Addresses:** CAP-11, CAP-08, CAP-09  
**Trigger:** Post-deployment of any High or Medium risk AI system  
**Skill sequence:**
```
[Deployed AI System + Risk Tier]
        │
        ▼
1. continuous-monitoring-design (KPIs, KRIs, alerts, escalation)
        │
        ▼ (Monitoring Specifications)
2. governance-control-mapping (detective and corrective controls)
        │
        ▼ (Control Specifications)
3. ethana-feature-mapping (validate monitoring features against Ethana Audit Log)
        │
        ▼
[Live Monitoring Programme + Evidence Generation Schedule]
```

---

### WF-NEW-04: `third-party-ai-risk-workflow`

**Addresses:** CAP-14  
**Trigger:** Client procuring new vendor AI tool OR annual vendor review  
**Skill sequence:**
```
[Vendor AI Tool + Contract Documentation]
        │
        ▼
1. third-party-ai-risk-assessment (vendor risk rating)
        │
        ▼ (Risk Rating + Control Requirements)
2. regulatory-mapping (subject_type: third-party AI tool)
        │
        ▼ (Regulatory obligations from vendor AI)
3. governance-control-mapping (client-side controls for third-party AI)
        │
        ▼
[Vendor Risk Rating + Contractual Requirements + Client-Side Controls]
```

---

### WF-NEW-05: `model-governance-lifecycle-workflow`

**Addresses:** CAP-16, CAP-08  
**Trigger:** New model deployment OR annual model review  
**Skill sequence:**
```
[Model Documentation + Validation Evidence]
        │
        ▼
1. model-governance-assessment (MRM gap analysis)
        │
        ▼ (MRM Gap Register)
2. bias-fairness-assessment (fairness evaluation)
        │
        ▼
3. governance-control-mapping (model-specific controls)
        │
        ▼ (Control Specifications)
4. continuous-monitoring-design (production monitoring programme)
        │
        ▼
[Model Governance Package: validation readiness + controls + monitoring programme]
```

---

### WF-NEW-06: `agent-deployment-governance-workflow`

**Addresses:** CAP-15, CAP-08  
**Trigger:** Client deploying autonomous AI agent to production  
**Skill sequence:**
```
[Agent Architecture + Tool List + Permission Scope]
        │
        ▼
1. agent-governance-assessment (agent risk profile + HITL policy)
        │
        ▼ (Agent Risk Profile)
2. ai-risk-assessment (agent-specific risk scenarios)
        │
        ▼
3. governance-control-mapping (agent-specific preventive + detective controls)
        │
        ▼ (Control Specifications)
4. ethana-feature-mapping (validate MCP Security Broker and Audit Log for agent monitoring)
        │
        ▼
[Agent Governance Package: registry entry + HITL policy + controls + monitoring]
```

---

### WF-NEW-07: `incident-regulatory-notification-workflow`

**Addresses:** CAP-12 (completeness), CAP-13  
**Trigger:** Incident severity assessment indicates potential regulatory notification obligation  
**Skill sequence:**
```
[Incident Analysis Output (Section 6 — Regulatory Implications)]
        │
        ▼
1. regulatory-mapping (subject_type: AI Incident — deep regulatory implication analysis)
        │
        ▼ (Notification obligations, timelines, formats)
2. [FUTURE: regulatory-notification skill] (draft notification per regulator requirements)
        │
        ▼
[Notification Drafts + Filing Deadlines + Post-Notification Monitoring Plan]
```

---

### WF-NEW-08: `audit-readiness-workflow`

**Addresses:** CAP-10, CAP-09  
**Trigger:** Upcoming regulatory examination OR ISO 42001 Stage 1/Stage 2 audit  
**Skill sequence:**
```
[Target Framework + Assessment Period + Evidence Inventory]
        │
        ▼
1. audit-pack-assembly (evidence gap detection + pack structure)
        │
        ▼ (Gap Register)
2. governance-control-mapping (design controls for evidence gaps)
        │
        ▼
3. ethana-feature-mapping (confirm evidence generation from Audit Log)
        │
        ▼
[Audit-Ready Evidence Pack + Gap Remediation Plan + Submission Checklist]
```

---

## 7. Recommended New Evaluations

---

### EVAL-NEW-01: `discovery-completeness-score`

**Evaluates:** `ai-discovery` skill outputs  
**Metric:** Completeness of discovery relative to organisation profile (systems per business unit, coverage of known AI-heavy domains)  
**Pass threshold:** 75/100  
**Key criteria:** Shadow AI section present, third-party AI footprint included, data flow map complete, confidence assessment honest about gaps  
**Automated check:** Validate that the AI Systems Register contains minimum required fields; flag entries with missing owner or risk tier

---

### EVAL-NEW-02: `gap-assessment-accuracy-rubric`

**Evaluates:** `iso-42001-gap-assessment`, `rbi-free-ai-assessment` skill outputs  
**Metric:** Accuracy of gap determination against framework requirements  
**Pass threshold:** 80/100  
**Key criteria:** Every clause/control explicitly addressed (not omitted), RAG status justified with evidence references, remediation roadmap is sequenced and realistic, certification readiness assessment is calibrated (not optimistic)  
**Automated check:** Verify all 38 Annex A controls appear in the gap register; flag any that are missing

---

### EVAL-NEW-03: `monitoring-programme-completeness`

**Evaluates:** `continuous-monitoring-design` skill outputs  
**Metric:** Coverage of required monitoring dimensions  
**Pass threshold:** 80/100  
**Key criteria:** Performance, fairness, security, and regulatory monitoring all addressed; thresholds are specific (not "monitor for anomalies" but "alert when false positive rate exceeds 8%"); escalation paths named; reporting cadence defined  
**Automated check:** Validate that each monitoring dimension (performance/fairness/security/regulatory) has at least one named KPI with a defined threshold

---

### EVAL-NEW-04: `agent-governance-coverage-check`

**Evaluates:** `agent-governance-assessment` skill outputs  
**Metric:** Coverage of agent governance control framework  
**Pass threshold:** 85/100  
**Key criteria:** All controls from `agent-governance-controls.md` explicitly addressed (scope, least privilege, HITL, monitoring, identity, tool isolation, incident response); HITL policy is specific (names actions requiring approval, not just "high-risk actions"); Agent Registry entry is complete  
**Automated check:** Parse output for presence of HITL gate table, identity model section, and Agent Registry entry

---

### EVAL-NEW-05: `third-party-ai-risk-completeness`

**Evaluates:** `third-party-ai-risk-assessment` skill outputs  
**Metric:** Completeness of vendor risk coverage  
**Pass threshold:** 75/100  
**Key criteria:** Vendor governance posture assessed, data processing risk addressed, contractual controls specified, ongoing monitoring requirements defined, risk rating justified  
**Automated check:** Validate that contractual control section contains minimum 5 named requirements; flag assessments that omit the data provenance or dependency concentration sections

---

### EVAL-NEW-06: `model-governance-mrm-alignment`

**Evaluates:** `model-governance-assessment` skill outputs  
**Metric:** Alignment with the MRM framework specified in the input (SR 11-7, SS1/23, or RBI MRM)  
**Pass threshold:** 82/100  
**Key criteria:** All SR 11-7/SS1/23 documentation requirements addressed, independent validation readiness honestly assessed, challenger model section present for high-risk models, production monitoring programme specific and measurable  
**Automated check:** Verify that the MRM Compliance Score arithmetic is reproducible from the scoring section alone

---

### EVAL-NEW-07: `cross-capability-consistency-check`

**Evaluates:** Complete workflow outputs (end-to-end pipeline)  
**Metric:** Internal consistency across skills in the same workflow  
**Pass threshold:** 90/100 (no inconsistencies)  
**Key criteria:** Risk tier assigned in ai-risk-assessment matches risk tier used in governance-control-mapping; Ethana capability status in any section matches canonical-product-model.md; regulatory obligations identified in regulatory-mapping are addressed in governance-control-mapping; no capability claim in ethana-solution-mapping that was prohibited in ethana-capability-validation  
**Automated check:** Run claims_linter.py across full pipeline output; cross-reference risk tiers from assessment vs. control design

---

### EVAL-NEW-08: `regulatory-notification-timeliness-check`

**Evaluates:** `incident-regulatory-notification-workflow` outputs  
**Metric:** Completeness and timeliness accuracy of notification drafts  
**Pass threshold:** 95/100 (notification obligations are safety-critical)  
**Key criteria:** Every applicable notification obligation identified in regulatory-mapping Section 6 has a corresponding notification draft; timelines match regulatory requirements (72-hour GDPR, 6-hour RBI for payment system breaches); notification format matches regulator specifications  
**Automated check:** Validate that filing deadline for each identified obligation is present and correctly calculated from incident date

---

## 8. Recommended Future Agents

---

### AGENT-NEW-01: `discovery-and-inventory-agent`

**Type:** ProactiveAgent (scheduled + triggered)  
**Purpose:** Maintains a continuously current AI inventory for a client organisation. Runs scheduled re-discovery (quarterly or on-demand), detects new AI systems added since last scan, updates the inventory, and flags changes requiring governance action.

**Required skills:** `ai-discovery`, `ai-inventory-management`, `regulatory-mapping`  
**Required workflows:** `ai-discovery-and-inventory-workflow`  
**Trigger modes:** Scheduled (quarterly), event-triggered (new vendor onboarding, new cloud deployment), manual  
**Key outputs:** Updated AI System Register, delta report (what changed since last run), new governance obligations triggered by inventory changes  
**Build readiness:** Blocked by `ai-discovery` and `ai-inventory-management` skill development

---

### AGENT-NEW-02: `monitoring-and-alerting-agent`

**Type:** ProactiveAgent (continuous)  
**Purpose:** Monitors deployed AI systems against their defined monitoring programmes. Collects evidence from Ethana Audit Log and connected SIEMs, evaluates KPIs and KRIs against thresholds, escalates anomalies, and maintains the evidence generation schedule.

**Required skills:** `continuous-monitoring-design`, `governance-control-mapping`  
**Required workflows:** `continuous-monitoring-programme-workflow`  
**Trigger modes:** Continuous (polling Audit Log and SIEM), scheduled (monthly monitoring summary)  
**Key outputs:** Real-time alerts on threshold breaches, monthly monitoring summary reports, evidence generation log  
**Build readiness:** Blocked by `continuous-monitoring-design` skill and data persistence layer

---

### AGENT-NEW-03: `governance-gap-assessment-agent`

**Type:** ReactiveAgent (triggered by client request or onboarding event)  
**Purpose:** Conducts a complete governance gap assessment for a client against a specified framework. Sequences discovery → inventory → risk assessment → framework gap assessment → control mapping → maturity report.

**Required skills:** `ai-discovery`, `ai-inventory-management`, `ai-risk-assessment`, `iso-42001-gap-assessment` or `rbi-free-ai-assessment`, `governance-control-mapping`  
**Required workflows:** `governance-gap-assessment-workflow`  
**Trigger modes:** Client onboarding, annual review, regulatory examination preparation  
**Key outputs:** Governance gap register, maturity score, certification readiness assessment, prioritised remediation roadmap  
**Build readiness:** Blocked by five skill dependencies

---

### AGENT-NEW-04: `third-party-ai-risk-agent`

**Type:** ProactiveAgent (event-triggered + scheduled)  
**Purpose:** Manages the client's third-party AI risk posture. Tracks approved vendor AI tools, triggers risk assessments for new procurement decisions, monitors vendor governance changes (new SOC 2 reports, model card updates, security disclosures), and maintains the TPAI Register.

**Required skills:** `third-party-ai-risk-assessment`, `regulatory-mapping`, `governance-control-mapping`  
**Required workflows:** `third-party-ai-risk-workflow`  
**Trigger modes:** New vendor procurement event, scheduled (annual vendor review), vendor security disclosure  
**Key outputs:** TPAI Register, vendor risk ratings, contractual control requirements, vendor change alerts  
**Build readiness:** Blocked by `third-party-ai-risk-assessment` skill

---

### AGENT-NEW-05: `model-governance-agent`

**Type:** ProactiveAgent (lifecycle-event-driven)  
**Purpose:** Governs the AI/ML model lifecycle for a client's model portfolio. Tracks model versions, triggers validation workflows at defined intervals, monitors models for performance degradation and bias drift, and manages model retirement.

**Required skills:** `model-governance-assessment`, `bias-fairness-assessment`, `continuous-monitoring-design`, `governance-control-mapping`  
**Required workflows:** `model-governance-lifecycle-workflow`  
**Trigger modes:** Model deployment event, version change event, scheduled (annual revalidation), performance threshold breach  
**Key outputs:** Model governance status per model, validation due alerts, drift detection reports, model retirement notifications  
**Build readiness:** Blocked by `model-governance-assessment` and `bias-fairness-assessment` skills

---

### AGENT-NEW-06: `agent-deployment-governance-agent`

**Type:** ReactiveAgent (deployment-triggered)  
**Purpose:** Executes the agent governance workflow for every autonomous AI agent deployment. Reviews the agent architecture, produces an Agent Registry entry with full governance metadata, enforces the HITL policy design, and monitors agent behaviour post-deployment.

**Required skills:** `agent-governance-assessment`, `ai-risk-assessment`, `governance-control-mapping`, `ethana-feature-mapping`  
**Required workflows:** `agent-deployment-governance-workflow`  
**Trigger modes:** New agent deployment request, agent capability change event  
**Key outputs:** Agent Registry entry, HITL policy document, agent-specific control specifications, post-deployment monitoring specification  
**Build readiness:** Blocked by `agent-governance-assessment` skill

---

### AGENT-NEW-07: `audit-readiness-agent`

**Type:** ReactiveAgent (examination-triggered)  
**Purpose:** Prepares a client for an upcoming regulatory examination or certification audit. Assembles the evidence pack, identifies gaps, coordinates remediation, tracks evidence collection progress, and produces the final submission-ready pack.

**Required skills:** `audit-pack-assembly`, `governance-control-mapping`, `ethana-feature-mapping`, `regulatory-mapping`  
**Required workflows:** `audit-readiness-workflow`  
**Trigger modes:** Client notification of upcoming audit, scheduled (90 days before known examination date)  
**Key outputs:** Evidence pack (submission-ready), gap remediation tracker, submission checklist, attestation request workflow  
**Build readiness:** Blocked by `audit-pack-assembly` skill and evidence vault data layer

---

## Appendix A — Framework Requirement Decomposition Used in This Audit

### ISO 42001 — Governance Capabilities Required
Cl.4 Context → Discovery, Inventory | Cl.5 Leadership → Governance Structure | Cl.6 Planning → Risk Assessment, Impact Assessment | Cl.7 Support → Training, Documentation | Cl.8 Operation → Inventory, Classification, Control Design, Third Party AI, Model Governance | Cl.9 Performance → Continuous Monitoring, Evidence Generation, Audit Readiness | Cl.10 Improvement → Control Validation, Incident Management | Annex A → Control Mapping, Control Design (all 38 controls)

### NIST AI RMF — Governance Capabilities Required
GOVERN → Regulatory Mapping, Governance Structure, Third Party AI Risk | MAP → Discovery, Inventory, Classification, Risk Assessment, Agent Governance | MEASURE → Risk Assessment, Continuous Monitoring, Bias/Fairness Assessment, Control Validation | MANAGE → Control Mapping, Control Design, Incident Management, Audit Readiness

### EU AI Act — Governance Capabilities Required
Art.6 Classification → Discovery, Classification | Art.9 Risk Management → Risk Assessment, Control Mapping, Control Design | Art.10 Data Governance → Bias Assessment, Data Controls | Art.11 Technical Documentation → Model Governance, Documentation | Art.12 Record-Keeping → Evidence Generation, Audit Readiness | Art.13 Transparency → Model Governance | Art.14 Human Oversight → Control Design (oversight mechanisms) | Art.15 Accuracy/Robustness → Control Validation | Art.72 Post-Market Monitoring → Continuous Monitoring | Art.73 Incident Reporting → Incident Management (regulatory notification)

### RBI FREE-AI — Governance Capabilities Required
Pillar 1 Governance Structure → Discovery, Inventory, Regulatory Mapping | Pillar 2 Risk Management → Risk Assessment, Control Mapping | Pillar 3 Model Risk → Model Governance, Control Validation | Pillar 4 Transparency → Model Governance, Documentation | Pillar 5 Fairness → Bias/Fairness Assessment | Pillar 6 Data Governance → Third Party AI Risk, Data Controls | Pillar 7 Audit and Accountability → Evidence Generation, Audit Readiness

### BFSI MRM (SR 11-7 / PRA SS1/23 / RBI MRM) — Governance Capabilities Required
Model Inventory → Inventory, Classification | Model Development → Control Design | Independent Validation → Control Validation | Model Documentation → Model Governance | Challenger Models → Model Governance | Production Monitoring → Continuous Monitoring | Model Risk Reporting → Evidence Generation, Audit Readiness | Vendor Models → Third Party AI Risk

### AI Security Governance (OWASP LLM Top 10 / MITRE ATLAS) — Governance Capabilities Required
LLM01 Prompt Injection → Control Mapping, Control Design | LLM02 Sensitive Info Disclosure → Control Mapping | LLM03 Supply Chain → Third Party AI Risk | LLM04 Data/Model Poisoning → Model Governance | LLM05 Insecure Output Handling → Control Design | LLM06 Excessive Agency → Agent Governance | LLM07 System Prompt Leakage → Control Design | LLM08 Vector/Embedding Weakness → Model Governance | LLM09 Misinformation → Control Validation | LLM10 Unbounded Consumption → Control Design, Continuous Monitoring | MITRE ATLAS → Continuous Monitoring, Incident Management, Control Validation
