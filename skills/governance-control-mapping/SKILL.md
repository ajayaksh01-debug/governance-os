# Skill: Governance Control Mapping

**Version:** 1.0  
**Category:** Control Operationalization  
**Owner:** Cursory Governance Team  

---

## Purpose

This skill translates AI incidents, regulatory obligations, governance assessment findings, and risk profiles into actionable, implementation-ready control specifications. 

While upstream skills (e.g., [regulatory-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md) and [ai-incident-analysis](file:///Users/ajayrajsingh/Documents/governance-os/skills/ai-incident-analysis/SKILL.md)) identify *what* compliance requirements and risk exposures exist, the Governance Control Mapping skill defines *how* to construct, configure, and verify those controls. It takes abstract compliance goals (such as "ensure human oversight" or "prevent unauthorized data access") and outputs structured specifications detailing preventive, detective, and corrective controls across technical and organizational boundaries.

Additionally, this skill provides a definitive mapping of technical controls to the Ethana platform (Build and Edge) using [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) as the sole truth reference, strictly enforcing the **Claims Firewall** to protect commercial integrity.

---

## When to Use This Skill

Use this skill when:
- High-level control requirements from a regulatory mapping need translation into engineering-level implementation plans.
- Root cause recommendations from an AI incident analysis need to be turned into active, operationalized defenses.
- A client requires a detailed, auditable RACI and evidence verification checklist for their AI governance controls.
- Designing sandbox proofs-of-concept (POCs) or production configuration guidelines for the Ethana platform.
- Performing a maturity gap analysis of existing AI system controls against industry standards (ISO 42001, NIST AI RMF).

---

## Relationship to Other Skills

| Dimension | Regulatory Mapping | AI Incident Analysis | Governance Control Mapping | Ethana Solution Mapping | Ethana Feature Mapping |
|---|---|---|---|---|---|
| **Core Question** | What regulations apply? | What happened and why? | **How do we implement the controls?** | What can we propose? | Does this feature work here? |
| **Primary Input** | AI subject description | Incident report / details | **Upstream control requirements / findings** | Governance requirements | Technical queries / POC scope |
| **Key Output** | Obligations & risk tiers | Failure analysis & lessons | **Technical & process control specifications** | Proposal text & CCS | Verification matrix & TFS |
| **Audience** | Legal & Compliance | Security, Risk, C-Suite | **AI Engineering, Security, Operations** | Advisory & Sales | Solution Architects |

---

## Input Specification

### Required Inputs

| Field | Required | Description |
|---|---|---|
| `upstream_source_type` | Yes | The source of the requirements. Must be one of: `AI Incident Analysis`, `Regulatory Mapping`, `Ethana Solution Mapping`, `Ethana Feature Mapping`, `External Risk Assessment`, `Custom Findings` |
| `upstream_payload` | Yes | The raw findings or output files to translate. This typically contains Section 6 of `regulatory-mapping`, Section 9 of `ai-incident-analysis`, or equivalent compliance/gap registers. |
| `target_maturity_level` | Yes | The target maturity for the designed controls, using the Cursory control maturity model: `L1: Initial`, `L2: Repeatable`, `L3: Defined`, `L4: Managed`, `L5: Optimizing`. |

### Contextual Inputs

| Field | Required | Description |
|---|---|---|
| `jurisdictions` | No | List of target jurisdictions (EU, UK, India). |
| `client_sector` | No | Vertical sector (e.g., BFSI, Healthcare, General Enterprise) to apply sectoral guidance overlays. |
| `infrastructure_model` | No | Deployment architecture (e.g., Public Cloud SaaS, Customer VPC, On-premises, Air-gapped). |
| `existing_tooling` | No | Third-party security and logging tools already in use (e.g., Splunk, Datadog, Zscaler, Netskope). |

---

## Output Specification (10 Sections)

Every assessment must output the following ten sections in sequence:

### 1. Executive Summary & Control Landscape
A 200–250 word non-technical summary of the control architecture designed for the subject AI system. It summarizes key risk areas mitigated, the total distribution of controls, and a high-level operational impact assessment for C-suite stakeholders.

### 2. Control Taxonomy Matrix
A tabular grid classifying all designed controls across two axes:
- **Control Type:** Preventive, Detective, or Corrective.
- **Control Method:** Technical (enforced via software, network, platform, or configurations) or Process (enforced via policy, training, manual gates, or reviews).

| Control ID | Control Name | Control Type | Control Method | Primary Risk Mitigated |
|---|---|---|---|---|
| `CTRL-GCM-01` | [Control Name] | Preventive / Detective / Corrective | Technical / Process | [Risk description] |

### 3. Control Coverage Classification
Every control designed in the specification must be assigned exactly one of the following classifications, clarifying platform alignment:
- **Fully Covered by Ethana:** The control can be completely implemented using verified Production features of the Ethana platform.
- **Partially Covered by Ethana:** Ethana provides core elements of the control, but customer-side configurations, custom integrations, or Cursory services are required.
- **Covered by Cursory Service:** The control is delivered via Cursory manual services (e.g., Red Teaming exercises or bespoke Advisory design).
- **Third-Party Control Required:** The control relies entirely on external systems (e.g., Zscaler DLP, Okta IDP, or cloud hosting configurations).
- **Customer-Owned Control:** The control is purely organizational or process-based, operated internally by the customer (e.g., board-level sign-offs or internal training).

### 4. Preventive Control Specifications
Detailed designs for controls that block or prevent risks before they execute. Each specification must include:
- **Control ID & Name**
- **Trigger Condition:** The specific action or telemetry that engages the control.
- **Enforcement Mechanism:** The operational mechanism (e.g., regex checks, token restrictions, approval gates).
- **Failure Mode:** Behavior if the control fails (Fail-Open vs. Fail-Closed) and downstream consequences.

### 5. Detective Control Specifications
Detailed designs for monitoring, logging, and alerting systems. Each specification must include:
- **Control ID & Name**
- **Logging Source:** Telemetry generating systems (e.g., API logs, audit tables).
- **Telemetry Format:** Fields captured (e.g., user identity, timestamp, payload hash).
- **Alerting Thresholds:** Specific conditions under which an alert is generated.
- **Routing Target:** Incident management systems or SOC queues.

### 6. Corrective Control Specifications
Incident response, mitigation, and recovery procedures. Each specification must include:
- **Control ID & Name**
- **Activation Trigger:** The detective alert or threshold that initiates corrective actions.
- **Containment Protocol:** Automated or manual steps taken to limit immediate blast radius (e.g., model fallback, API rate limits, user lockout).
- **Recovery Procedure:** Steps required to restore the AI system to a trusted state.
- **Rollback SLA:** Maximum target times for containment and recovery.

### 7. Evidence & Verification Requirements
The concrete artifacts required to prove control operating effectiveness to auditors or regulators:
- **Evidence ID & Name**
- **Artifact Description:** Physical or digital artifact (e.g., log extract, signed approval document, audit report).
- **Collection Method & Frequency:** Automated export vs. manual extraction, and timing (e.g., real-time, daily, quarterly).
- **Retention Period:** Required retention timeline based on jurisdictional laws (e.g., GDPR, RBI, DPA).

### 8. Control Ownership Matrix (RACI)
A RACI matrix mapping every control to specific organizational roles to prevent ownership gaps:
- **Responsible (R):** Operates and maintains the control.
- **Accountable (A):** Direct risk owner who signs off on control effectiveness and owns the risk (must be a single role per control).
- **Consulted (C):** Subject matter experts who advise on design.
- **Informed (I):** Stakeholders notified of control status and performance.

### 9. Maturity & Phased Roadmap
A 30-60-90 day deployment roadmap designed to transition controls from their current state to the `target_maturity_level`:
- **Phase 1 (Days 1–30):** Deployment of foundational preventive controls, audit logs, and critical RACI assignments.
- **Phase 2 (Days 31–60):** Alerting rules, process integrations, and employee training.
- **Phase 3 (Days 61–90):** Corrective automation, maturity optimization, and mock audits.

### 10. Ethana Configuration Guide
Specific configuration instructions mapping designed technical controls directly to Ethana capabilities, governed by the **Claims Firewall**:
- **Production Mappings:** Configurations utilizing verified, active Production features from Section 1.1 of [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) (e.g., LLM Gateway routing fallbacks, Runtime Guardrails PII filters, Immutable Audit Log configurations).
- **In Build / Roadmap Mappings:** Configurations utilizing features listed as In Build or Aspirational in the canonical model (e.g., Non-Human Identity agent tokens, Sentry Discovery log connectors). These **must** be marked as "Roadmap" and accompanied by alternative manual or third-party configurations (e.g., manual ID scoping, Zscaler DLP setups) until the Ethana feature is production-ready.

---

## Constraints and Scope

**In Scope:**
- Designing operational controls for AI systems (LLMs, ML models, agentic systems).
- Mapping control specifications to general frameworks (ISO 42001, NIST AI RMF, OWASP LLM Top 10).
- Mapping controls to the Ethana platform (Build/Edge) based on the canonical model.
- Technical controls (e.g., gateway configuration) and process controls (e.g., model registries).

**Out Scope:**
- General corporate IT compliance (e.g., general network security, corporate firewall design) unless directly impacting the AI gateway.
- Pure legal advice — this skill outputs risk mitigation and control designs, not legal opinions.
- Developing or testing custom control code (e.g., writing OPA Rego rules or custom regex filters) — the skill designs the specifications, but does not execute development.

**The Ethana Claims Firewall Gate:**
All platform integrations in Section 10 must align exactly with [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md). Any recommendation, configuration step, or proposal language that claims In Build or Aspirational capabilities as active production features is a Firewall Breach. 
- *Firewall breaches trigger an automatic evaluation failure (score capped at 0/100)*.

---

## Knowledge Dependencies

This skill draws on the following knowledge base files:

**Ethana Authority:**
- [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) — The single authoritative source for platform capability status.

**Controls Library:**
- [data-protection-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/data-protection-controls.md) — Base control patterns for training and inference privacy.
- [model-risk-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/model-risk-controls.md) — Base control patterns for model drift, explainability, and bias.
- [audit-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/audit-controls.md) — Base control patterns for logging, evidence, and SIEM integration.
- [agent-governance-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/agent-governance-controls.md) — Base control patterns for autonomous agents and MCP security.
- [prompt-injection-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/prompt-injection-controls.md) — Base control patterns for injection and jailbreak defenses.

**Frameworks & Regulations:**
- [iso-42001.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/frameworks/iso-42001.md)
- [nist-ai-rmf.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/frameworks/nist-ai-rmf.md)
- [owasp-llm-top-10.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/frameworks/owasp-llm-top-10.md)
- [eu-ai-act.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/regulations/eu-ai-act.md)
- [uk-ai-guidance.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/regulations/uk-ai-guidance.md)
- [india-ai-landscape.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/regulations/india-ai-landscape.md)

---

## Related Skills

- [regulatory-mapping/](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/) — Upstream: identifies regulatory obligations that trigger control mapping.
- [ai-incident-analysis/](file:///Users/ajayrajsingh/Documents/governance-os/skills/ai-incident-analysis/) — Upstream: provides root causes and high-level controls after an incident.
- [ethana-solution-mapping/](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/) — Upstream: identifies commercially proposed capabilities.
- [ethana-feature-mapping/](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-feature-mapping/) — Downstream: validates specific technical feature integrations.
