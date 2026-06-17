# Governance Control Mapping — Examples

## Overview

This document provides three complete, implementation-grade examples of the Governance Control Mapping skill in action. These examples serve as calibration baselines for analysts and automated evaluators.

---

## Example 1: UK Bank Deploying Microsoft Copilot

### 1. Intake & Context
- **Upstream Payload:** [regulatory-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md) Section 6 (identifying need for monitoring, data protection, and model risk oversight for SaaS AI under PRA SS1/23).
- **Client Sector:** BFSI (UK Banking).
- **Jurisdiction:** UK (PRA, FCA, UK GDPR).
- **Deployment Topology:** Public SaaS (Microsoft 365 cloud).
- **Target Maturity:** L3: Defined.
- **Existing Tooling:** Okta (Identity), Zscaler (Secure Web Gateway), Splunk (SIEM).

---

### Completed Assessment Output

#### Section 1: Executive Summary & Control Landscape
This assessment details the control framework designed for the deployment of Microsoft 365 Copilot to 5,000 banking employees. The primary risks concern unauthorized access to customer personal data, data exfiltration through prompt outputs, and shadow AI usage. Because Microsoft Copilot is a third-party SaaS tool whose APIs do not route through the Cursory LLM Gateway, control enforcement relies heavily on corporate Secure Web Gateways (Zscaler), native Microsoft Purview DLP policies, and manual identity crosswalks. Platform monitoring capabilities (Ethana Sentry and Edge browser extensions) are In Build and are treated as roadmap items with manual workarounds.

#### Section 2: Control Taxonomy Matrix
| Control ID | Control Name | Control Type | Control Method | Primary Risk Mitigated |
|---|---|---|---|---|
| `CTRL-COP-01` | SWG Allowlist & Coaching | Preventive | Technical | Employee usage of shadow/unapproved AI endpoints |
| `CTRL-COP-02` | IdP Entitlement Reviews | Preventive | Process | Unauthorized user access to Copilot licensing |
| `CTRL-COP-03` | Purview DLP Sensitive Prompts | Preventive | Technical | Transmission of PII or credit card numbers in prompts |
| `CTRL-COP-04` | SWG Traffic Log Auditing | Detective | Technical | Detection of bypassed or unapproved SaaS AI usage |
| `CTRL-COP-05` | SaaS API License Auditing | Detective | Process | Discrepancies between approved users and active licenses |
| `CTRL-COP-06` | SWG Block Rule Activation | Corrective | Technical | Exfiltration event containment (automatic URL block) |
| `CTRL-COP-07` | Copilot License Suspension | Corrective | Process | Credential compromise or policy breach response |

#### Section 3: Control Coverage Classification
- `CTRL-COP-01` (SWG Allowlist): **Third-Party Control Required** (Configured in Zscaler).
- `CTRL-COP-02` (IdP Entitlement): **Customer-Owned Control** (Okta policy and manual review).
- `CTRL-COP-03` (Purview DLP): **Third-Party Control Required** (Configured in MS Purview).
- `CTRL-COP-04` (SWG Log Audit): **Third-Party Control Required** (Zscaler logs routed to Splunk).
- `CTRL-COP-05` (SaaS API Audit): **Covered by Cursory Service** (Manual audit via Cursory AI Inventory Service).
- `CTRL-COP-06` (SWG Block Rule): **Third-Party Control Required** (Zscaler automated API block).
- `CTRL-COP-07` (License Suspension): **Customer-Owned Control** (IT Service Desk procedure).

#### Section 4: Preventive Control Specifications
- **CTRL-COP-01: SWG Allowlist & Coaching**
  - *Trigger:* User attempts to access an AI URL (e.g., `copilot.microsoft.com` or `chat.openai.com`).
  - *Mechanism:* Zscaler URL Filtering policy blocks all AI categories except approved tenant endpoints. Users redirection leads to an internal training portal.
  - *Failure Mode:* Fail-Closed. If Zscaler fails to categorize, category access is blocked by default.
- **CTRL-COP-03: Purview DLP Sensitive Prompts**
  - *Trigger:* User inputs a prompt containing customer accounts, UK National Insurance numbers, or card data.
  - *Mechanism:* Microsoft Purview DLP matches patterns in real-time and blocks the prompt submission.
  - *Failure Mode:* Fail-Open. If Purview DLP engine lags, traffic is permitted but flagged in administrative logs.

#### Section 5: Detective Control Specifications
- **CTRL-COP-04: SWG Traffic Log Auditing**
  - *Logging Source:* Zscaler Nanolog streaming API.
  - *Telemetry Format:* `timestamp`, `user_id`, `destination_url`, `action_taken` (block/allow), `bytes_sent`.
  - *Alerting Thresholds:* Any unapproved AI endpoint URL matched more than 10 times in 1 hour by a single user.
  - *Routing Target:* Splunk SIEM alert routed to the Security Operations Center (SOC) triage queue.

#### Section 6: Corrective Control Specifications
- **CTRL-COP-06: SWG Block Rule Activation**
  - *Activation Trigger:* Detective alert for data egress threshold exceeded (e.g., >50MB uploaded to AI SaaS in 5 minutes).
  - *Containment Protocol:* Splunk triggers a webhook to Zscaler API to immediately revoke the user's internet egress to all AI endpoints.
  - *Recovery Procedure:* SOC analyst verifies the upload. If authorized, they manually release the block via Zscaler.
  - *Rollback SLA:* 5 minutes for containment; 1 hour for recovery.

#### Section 7: Evidence & Verification Requirements
- **EVID-COP-01: Zscaler Policy Configurations**
  - *Description:* Export of current Zscaler AI category blocking rules.
  - *Collection Method & Frequency:* Manual export by Network Team, quarterly.
  - *Retention Period:* 3 years (FCA operational resilience compliance).
- **EVID-COP-02: Purview DLP Block Logs**
  - *Description:* Splunk export of blocked prompt attempts.
  - *Collection Method & Frequency:* Automated weekly export to Compliance Sharepoint.
  - *Retention Period:* 5 years (UK GDPR obligation).

#### Section 8: Control Ownership Matrix (RACI)
| Control ID | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|---|---|---|---|---|
| `CTRL-COP-01` | Network Security Team | Head of Infrastructure | Cursory Advisory | CISO |
| `CTRL-COP-02` | Identity Management Team | Head of IAM | Compliance Lead | DPO |
| `CTRL-COP-03` | M365 Platform Admin | Head of Digital Workplace | Data Protection Officer | CISO |
| `CTRL-COP-04` | Security Operations (SOC) | CISO | Cursory Security Team | Head of Risk |
| `CTRL-COP-05` | Cursory Delivery Team | Head of Procurement | IT SAM Lead | Compliance |
| `CTRL-COP-06` | SOC Engineering Team | CISO | Network Security | IT Director |
| `CTRL-COP-07` | IT Service Desk | Head of Support | HR / Legal Counsel | Manager |

#### Section 9: Maturity & Phased Roadmap
- **Phase 1 (Days 1–30):** Establish Zscaler URL category blocks (`CTRL-COP-01`) and implement IAM group permissions (`CTRL-COP-02`). Identify Accountable roles.
- **Phase 2 (Days 31–60):** Activate Purview DLP rules (`CTRL-COP-03`) and connect Zscaler traffic feeds to Splunk (`CTRL-COP-04`). Establish Cursory-assisted manual audits.
- **Phase 3 (Days 61–90):** Implement automated containment scripts in Splunk/Zscaler (`CTRL-COP-06`). Conduct the first mock compliance audit.

#### Section 10: Ethana Configuration Guide
Because Microsoft Copilot is client/browser-side SaaS, native Ethana Build (LLM Gateway/Guardrails) is N/A for runtime enforcement as Copilot traffic does not route through the gateway.
- **Roadmap Platform Mappings (In Build):**
  - *Ethana Sentry Discovery Connector:* okta/Entra IdP connectors listed as In Build in [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) Section 2.2. Once released, this will automate SaaS discovery.
  - *Ethana Edge Agent / Browser Extension:* Listed as In Build in [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) Section 2.1. Once released, this will enforce local policies and block unapproved browser Copilot prompts.
- **Mandatory Manual / Third-Party Workarounds (Required Today):**
  - Use Zscaler URL category blocking and SSL inspection to log browser traffic.
  - Use Cursory AI Inventory Service (manual Okta log analysis and HR crosswalks) to audit SaaS tool sprawl quarterly.

---

## Example 2: Insurance Claims AI Workflow (EU High-Risk)

### 1. Intake & Context
- **Upstream Payload:** [regulatory-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md) Section 6 (obligation to perform pre-deployment bias audits and establish human oversight gates for automated decision-making under GDPR Article 22 and EU AI Act Annex III).
- **Client Sector:** Insurance.
- **Jurisdiction:** EU (Germany/France).
- **Deployment Topology:** Customer VPC (AWS).
- **Target Maturity:** L4: Managed.
- **Existing Tooling:** Datadog (monitoring), Jira (workflows), Gitlab (CI/CD).

---

### Completed Assessment Output

#### Section 1: Executive Summary & Control Landscape
This assessment designs the control framework for an automated claims-processing AI model that automatically accepts or denies health insurance claims. Because this system qualifies as High-Risk under the EU AI Act (Annex III, point 5), it requires strict data governance, pre-deployment bias auditing, and human oversight. Technical controls are implemented via Ethana Build LLM Gateway and custom validation pipelines. Process controls manage pre-deployment model validation, bias reviews, and human overrides.

#### Section 2: Control Taxonomy Matrix
| Control ID | Control Name | Control Type | Control Method | Primary Risk Mitigated |
|---|---|---|---|---|
| `CTRL-INS-01` | Pre-deployment Model Registry | Preventive | Process | Deployment of unvalidated or biased models |
| `CTRL-INS-02` | Human-in-the-Loop Override | Preventive | Process | Automated claim denial without human recourse |
| `CTRL-INS-03` | PII Gateway Redaction | Preventive | Technical | Leaking customer PII to LLM provider APIs |
| `CTRL-INS-04` | Subgroup Disparate Impact Auditing | Detective | Process | Algorithmic bias against protected demographic groups |
| `CTRL-INS-05` | Gateway Drift Telemetry | Detective | Technical | Performance decay or drift in claims classification |
| `CTRL-INS-06` | Gateway Fallback Routing | Corrective | Technical | Primary model API outage or performance failure |
| `CTRL-INS-07` | Claim Re-evaluation Workflow | Corrective | Process | Systemic bias or error remediation |

#### Section 3: Control Coverage Classification
- `CTRL-INS-01` (Model Registry): **Customer-Owned Control** (Gitlab CI/CD and Jira).
- `CTRL-INS-02` (Human Override): **Customer-Owned Control** (Jira Service Desk queue).
- `CTRL-INS-03` (PII Redaction): **Fully Covered by Ethana** (Ethana Build Runtime Guardrails).
- `CTRL-INS-04` (Bias Auditing): **Covered by Cursory Service** (Independent audit by specialist partner).
- `CTRL-INS-05` (Drift Telemetry): **Partially Covered by Ethana** (Ethana Audit logs mapped to Datadog metrics).
- `CTRL-INS-06` (Fallback Routing): **Fully Covered by Ethana** (Ethana Build LLM Gateway multi-model routing).
- `CTRL-INS-07` (Re-evaluation): **Customer-Owned Control** (Operational team playbook).

#### Section 4: Preventive Control Specifications
- **CTRL-INS-03: PII Gateway Redaction**
  - *Trigger:* System initiates a claims summarization API call containing customer names, policy numbers, or medical history.
  - *Mechanism:* Ethana Build Runtime Guardrails scan prompt payload, redact names/policy numbers, and replace them with placeholder tokens before routing.
  - *Failure Mode:* Fail-Closed. If the PII scanner fails or encounters a timeout, the API call is blocked and an error is logged.

#### Section 5: Detective Control Specifications
- **CTRL-INS-05: Gateway Drift Telemetry**
  - *Logging Source:* Ethana Immutable Audit Log.
  - *Telemetry Format:* `timestamp`, `model_id`, `input_length`, `output_length`, `response_time`, `sentiment_score`.
  - *Alerting Thresholds:* Average response latency exceeding 1,500ms or failure rate exceeding 2% over a 5-minute window.
  - *Routing Target:* Datadog APM alerting engine, routed to the AI Engineering on-call team.

#### Section 6: Corrective Control Specifications
- **CTRL-INS-06: Gateway Fallback Routing**
  - *Activation Trigger:* Primary model endpoint (e.g., Anthropic Claude API) returns a 5xx error or times out.
  - *Containment Protocol:* Ethana Build LLM Gateway automatically reroutes the claims payload to the secondary model endpoint (e.g., Azure OpenAI) without system interruption.
  - *Recovery Procedure:* Gateway runs periodic health probes to primary model. Once primary model responds successfully 5 times consecutively, traffic is restored.
  - *Rollback SLA:* Sub-100ms automated failover.

#### Section 7: Evidence & Verification Requirements
- **EVID-INS-01: Verbatim Gateway Logs**
  - *Description:* Tamper-proof logs of claims summary calls proving PII redaction.
  - *Collection Method & Frequency:* Automated export from Ethana Immutable Audit Log, daily.
  - *Retention Period:* 10 years (EU AI Act Article 20 record-keeping).
- **EVID-INS-02: Bias Audit Report**
  - *Description:* Signed report certifying statistical fairness across demographics.
  - *Collection Method & Frequency:* Manual upload by Risk Team, annually.
  - *Retention Period:* 10 years (EU AI Act requirement).

#### Section 8: Control Ownership Matrix (RACI)
| Control ID | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|---|---|---|---|---|
| `CTRL-INS-01` | MLOps Team | Head of Data Science | Compliance Lead | VP Engineering |
| `CTRL-INS-02` | Claims Review Team | Head of Claims Operations | Legal Counsel | Customer Support |
| `CTRL-INS-03` | AI Platform Team | VP of AI Engineering | Data Protection Officer | CISO |
| `CTRL-INS-04` | Risk Management Team | Chief Risk Officer | Cursory Advisory | Board Audit Comm |
| `CTRL-INS-05` | Site Reliability (SRE) | Head of Operations | AI Platform Team | CTO |
| `CTRL-INS-06` | AI Platform Team | VP of AI Engineering | Cloud Provider | CTO |
| `CTRL-INS-07` | Claims Quality Team | Head of Claims Operations | Legal / Compliance | CRO |

#### Section 9: Maturity & Phased Roadmap
- **Phase 1 (Days 1–30):** Route all traffic through Ethana Build Gateway. Configure `CTRL-INS-03` (PII masking) and `CTRL-INS-06` (Fallback routing). Assign Accountable roles.
- **Phase 2 (Days 31–60):** Deploy GitLab CI/CD checks for model registry (`CTRL-INS-01`). Hook Ethana audit logs to Datadog (`CTRL-INS-05`). Establish human override Jira workflow (`CTRL-INS-02`).
- **Phase 3 (Days 61–90):** Perform pre-deployment bias audit (`CTRL-INS-04`). Conduct end-to-end evidence export verification.

#### Section 10: Ethana Configuration Guide
- **Production Platform Mappings (Verified):**
  - *LLM Gateway Routing Configuration:* In Ethana Build console, define routing rules: Primary `claude-3-5-sonnet`, Fallback `gpt-4o`. Set timeout threshold to `1000ms`.
  - *PII Masking Guardrails:* Enable `PII Scanner` on Ethana Gateway. Define entities: `PERSON`, `EMAIL`, `PHONE_NUMBER`, `CREDIT_CARD`. Set redaction action to `REPLACE_WITH_TOKEN`.
  - *Immutable Audit Log:* Enable SIEM forwarding. Route syslog JSON payload containing transaction metadata to Datadog ingestion endpoint.
- **Mandatory Manual / Third-Party Workarounds (Claims Firewall Gate):**
  - *Bias Auditing:* Ethana's native "Bias scanner" is a **runtime text filter only** (per [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) Section 1.1) and cannot audit model weights or test disparate impact across demographic subgroups. Therefore, a manual audit using Cursory Python notebooks and a specialist auditing firm must be run quarterly. Do not assert that Ethana's Bias scanner achieves EU AI Act Article 10 compliance.

---

## Example 3: Prompt Injection Incident in Enterprise RAG System

### 1. Intake & Context
- **Upstream Payload:** [ai-incident-analysis](file:///Users/ajayrajsingh/Documents/governance-os/skills/ai-incident-analysis/SKILL.md) Section 9 (identifying prompt injection vulnerability and data exfiltration risk in customer-facing support agent).
- **Client Sector:** General Enterprise (Retail).
- **Jurisdiction:** Global.
- **Deployment Topology:** Customer VPC (Azure).
- **Target Maturity:** L5: Optimizing.
- **Existing Tooling:** Azure API Management, Splunk (SIEM).

---

### Completed Assessment Output

#### Section 1: Executive Summary & Control Landscape
This assessment specifies the control framework implemented to remediate a prompt injection vulnerability in the enterprise customer support assistant. The system was exploited when a user manipulated a chat query to bypass system instructions and exfiltrate internal inventory databases. The designed framework deploys real-time input and context filters via the Ethana Build Gateway to block adversarial prompts and payload anomalies, coupled with automated containment scripts in Splunk.

#### Section 2: Control Taxonomy Matrix
| Control ID | Control Name | Control Type | Control Method | Primary Risk Mitigated |
|---|---|---|---|---|
| `CTRL-RAG-01` | Gateway Input Injection Filter | Preventive | Technical | System instruction override via customer chat input |
| `CTRL-RAG-02` | Gateway Context Injection Filter | Preventive | Technical | Injection attacks embedded within retrieved RAG documents |
| `CTRL-RAG-03` | Scoped API Access Tokens | Preventive | Technical | Excessive API privilege utilization if agent is compromised |
| `CTRL-RAG-04` | Injection Probe Telemetry | Detective | Technical | Real-time logging of blocked injection attempts |
| `CTRL-RAG-05` | Egress Volume Anomaly Detection | Detective | Technical | Large-scale database dumps via prompt extraction |
| `CTRL-RAG-06` | Automated API Token Revocation | Corrective | Technical | Rapid containment of compromised agent sessions |
| `CTRL-RAG-07` | Incident Post-Mortem | Corrective | Process | Systemic loop vulnerability remediation |

#### Section 3: Control Coverage Classification
- `CTRL-RAG-01` (Input Filter): **Fully Covered by Ethana** (Ethana Build Runtime Guardrails).
- `CTRL-RAG-02` (Context Filter): **Fully Covered by Ethana** (Ethana Build Runtime Guardrails).
- `CTRL-RAG-03` (Scoped Tokens): **Partially Covered by Ethana** (Ethana MCP Broker + Azure IAM).
- `CTRL-RAG-04` (Probe Telemetry): **Fully Covered by Ethana** (Ethana Immutable Audit Log).
- `CTRL-RAG-05` (Anomaly Detection): **Third-Party Control Required** (Splunk SIEM correlations).
- `CTRL-RAG-06` (Token Revocation): **Third-Party Control Required** (Azure Active Directory/Entra webhook).
- `CTRL-RAG-07` (Post-Mortem): **Customer-Owned Control** (Internal Security and PM review).

#### Section 4: Preventive Control Specifications
- **CTRL-RAG-01: Gateway Input Injection Filter**
  - *Trigger:* Customer chat client sends user input to the backend model.
  - *Mechanism:* Ethana Build Runtime Guardrail Prompt Injection Scanner evaluates the text before it reaches the model, applying heuristics and classifier models.
  - *Failure Mode:* Fail-Closed. If the scanner times out, the message is blocked and an error is sent to the chat frontend.
- **CTRL-RAG-03: Scoped API Access Tokens**
  - *Trigger:* The AI agent requests database search or transaction execution.
  - *Mechanism:* Scoped tokens restrict database writes and API calls to a predefined, minimal set of user scopes.
  - *Failure Mode:* Fail-Closed. Any call to an unauthorized scope is immediately rejected.

#### Section 5: Detective Control Specifications
- **CTRL-RAG-05: Egress Volume Anomaly Detection**
  - *Logging Source:* Splunk SIEM consuming Ethana Immutable Audit logs.
  - *Telemetry Format:* `timestamp`, `session_id`, `tokens_output`, `payload_byte_size`.
  - *Alerting Thresholds:* Total response size exceeding 10,000 tokens in a single session within a 2-minute window.
  - *Routing Target:* Security Operations Center (SOC) urgent incident ticket queue.

#### Section 6: Corrective Control Specifications
- **CTRL-RAG-06: Automated API Token Revocation**
  - *Activation Trigger:* Splunk alert for exfiltration volume anomaly (`CTRL-RAG-05`) or repeated blocked injections (`CTRL-RAG-04`).
  - *Containment Protocol:* Splunk triggers a webhook to Azure Entra to immediately revoke the session token, terminating agent access.
  - *Recovery Procedure:* SRE team reviews logs, updates prompt templates, and manually generates a new token.
  - *Rollback SLA:* Automated revocation within 30 seconds; recovery within 2 hours.

#### Section 7: Evidence & Verification Requirements
- **EVID-RAG-01: Injection Alert Logs**
  - *Description:* Splunk logs showing trigger times, blocked payloads, and source IPs.
  - *Collection Method & Frequency:* Automated weekly compliance report to Security Lead.
  - *Retention Period:* 1 year.
- **EVID-RAG-02: Scoped Token Configuration**
  - *Description:* JSON definition files of the Active Directory scoped permission profiles.
  - *Collection Method & Frequency:* Manual review by Identity Team, semi-annually.
  - *Retention Period:* 3 years.

#### Section 8: Control Ownership Matrix (RACI)
| Control ID | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|---|---|---|---|---|
| `CTRL-RAG-01` | AI Platform Team | Head of AI Systems | Cursory Advisory | CISO |
| `CTRL-RAG-02` | RAG Dev Team | Head of AI Systems | Cursory Advisory | CTO |
| `CTRL-RAG-03` | Identity Team | Head of IAM | Security Architect | CISO |
| `CTRL-RAG-04` | Security Operations (SOC) | CISO | AI Platform Team | VP Engineering |
| `CTRL-RAG-05` | SOC Engineering | CISO | Database Lead | CIO |
| `CTRL-RAG-06` | Identity / SRE Team | CISO | IT Ops Lead | VP Engineering |
| `CTRL-RAG-07` | Security & Dev Teams | VP of AI Engineering | Head of Product | CRO |

#### Section 9: Maturity & Phased Roadmap
- **Phase 1 (Days 1–30):** Route traffic through Ethana Gateway and activate `CTRL-RAG-01` (Prompt Injection Scanner) and `CTRL-RAG-04` (Logging).
- **Phase 2 (Days 31–60):** Restructure agent architecture using scoped API tokens (`CTRL-RAG-03`). Setup Splunk anomaly alerts (`CTRL-RAG-05`).
- **Phase 3 (Days 61–90):** Implement automated session revocation script (`CTRL-RAG-06`). Perform mock prompt injection red-teaming exercise.

#### Section 10: Ethana Configuration Guide
- **Production Platform Mappings (Verified):**
  - *Prompt Injection Scanner:* Enable the `Prompt Injection Scanner` and `Jailbreak Scanner` in the Ethana Build Console. Set blocking policy to return a static generic failure string to the client.
  - *Immutable Audit Log:* Forward transaction logs to Splunk.
- **Roadmap Platform Mappings (In Build / Claims Firewall Gate):**
  - *Non-Human Identity (NHI) Scoped Tokens:* Scoped workload identity and ephemeral agent tokens are listed as In Build in [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) Section 1.2. 
  - *Mandatory Workaround:* Until NHI is shipped, developers must manually partition scopes by creating static, separate Azure Active Directory service accounts and passing specific API keys to different agent instances. Do not claim Ethana natively manages scoped ephemeral identities today.
