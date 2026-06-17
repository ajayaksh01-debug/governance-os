# Ethana Industry Use-Case Mappings

This document maps the **Ethana Enterprise AI Control Plane** and **Cursory Services** to specific, high-value use cases in regulated industries. Each use case details the target buyer persona, key pain points, the audited product/capability fit, what is delivered, and the explicit gaps that must be communicated to maintain trust.

---

## 1. Banking and Financial Services (BFSI)

### Use Case 1.1: Model Risk Management (MRM) for LLMs
- **Target Buyer:** Head of Model Risk, Chief Risk Officer (CRO).
- **Regulatory Drivers:** US Fed SR 11-7, UK PRA SS1/23 (Model Risk Management).
- **Key Pain:** Traditional MRM frameworks are quantitative and designed for regression models (Credit, Market Risk). They lack the tools, methodologies, and audit trails to validate, monitor, and stress-test Large Language Models (LLMs) in production.
- **Ethana Product Fit:**
  - **Ethana Build (Red Teaming [GA]):** Proactive testing of LLM applications using 21 OWASP-aligned probes (prompt injection, jailbreaking, output leakage) to support model validation.
  - **Ethana Build (Gateway & Immutable Audit Logs [GA]):** Continuous production monitoring and event logging of LLM prompts and responses.
  - **Cursory Services (Framework Mapping):** Advisory mapping of LLM controls to SR 11-7 / SS1/23 standards.
- **What is Delivered:** A structured validation framework for LLM robustness, combined with a tamper-proof audit trail for ongoing production monitoring.
- **Gaps & Boundaries:**
  - Traditional quantitative model validation (data drift, statistical bias, mathematical convergence) is a **GAP**. Ethana is a qualitative text and security control plane.
  - The CI/CD pull-request evaluation gate is **In Build**. Proactive red-teaming orchestrators must be run manually or triggered via custom scripts.

### Use Case 1.2: RBI Digital Risk & IT Outsourcing Compliance
- **Target Buyer:** CISO, Chief Compliance Officer, CRO (India Region).
- **Regulatory Drivers:** RBI Master Direction on IT Outsourcing, RBI Draft Circular on FREE-AI (August 2025).
- **Key Pain:** RBI mandates strict data localisation, vendor risk management, and traceability of AI-driven outcomes. Financial data and customer queries cannot route through public cloud gateways or foreign SaaS environments.
- **Ethana Product Fit:**
  - **Ethana Build (VPC / On-Premises Deployment [GA]):** The entire control plane (Gateway, Logs, Guardrails) is deployed inside the bank's own data center or India VPC, ensuring no data leaves the controlled network.
  - **Ethana Build (Gateway PII Masking [GA]):** Real-time, inline redaction of customer account numbers and sensitive identifiers before model routing.
  - **Ethana Build (Immutable Audit Logs [GA]):** Configurable retention (up to 7 years) and direct forwarding to local SIEM systems.
- **What is Delivered:** A fully self-hosted, local AI gateway and compliance log engine that satisfies RBI inspection criteria for AI transparency and data residency.
- **Gaps & Boundaries:**
  - On-premises deployment at G-SIB/Tier 1 bank scale remains unproven and requires 4-8 weeks of custom Cursory Implementation Services.
  - Schema customization for specific RBI reporting templates is a configuration engagement, not out-of-the-box.

### Use Case 1.3: High-Risk AI System Auditing (EU AI Act Readiness)
- **Target Buyer:** Chief Compliance Officer, DPO, CRO (EU Region).
- **Regulatory Drivers:** EU AI Act (Articles 9, 10, 11, 12, 13, 15).
- **Key Pain:** Credit scoring, insurance underwriting, and automated hiring tools are classified as "High-Risk" under Annex III, requiring strict record-keeping (Art.12), robustness testing (Art.15), risk systems (Art.9), and data governance (Art.10) before the 2026 enforcement deadline.
- **Ethana Product Fit:**
  - **Ethana Build (Immutable Audit Logs [GA]):** Automatically maps to Art. 12 record-keeping requirements, logging every prompt, response, user ID, and model metadata.
  - **Ethana Build (Red Teaming & Guardrails [GA]):** Direct testing and runtime protection for Art. 15 (accuracy & robustness) and Art. 9 (risk controls).
  - **Cursory Services (Ready Assessments):** Point-in-time gap analysis and classification of high-risk assets.
- **What is Delivered:** The primary logging and robustness evidence layer required to comply with EU AI Act High-Risk obligations.
- **Gaps & Boundaries:**
  - **Art. 10 Bias Auditing:** Ethana **cannot** audit training weights, test disparate impact on demographic groups, or validate training data. This requires external specialized audit firms.
  - **Art. 11 Technical Documentation:** The automated compliance evidence exporter (Compliance Pack) is **In Build**. Compliance documentation today must be prepared manually via Cursory advisory engagements.
  - **Art. 14 Human Oversight:** Ethana logs decisions but does not enforce UI-level human-in-the-loop validation or customer "contest decision" routes.

---

## 2. Insurance

### Use Case 2.1: IRDAI Inspection Readiness & Operational Resilience
- **Target Buyer:** CISO, Head of Compliance (India Region).
- **Regulatory Drivers:** IRDAI Information & Cybersecurity Guidelines, IRDAI Master Circular on Operational Resilience.
- **Key Pain:** Insurance companies are adopting AI for claims processing, document triage, and customer chat, but have no centralized inventory or audit trails showing which AI tools handle policyholders' private medical or financial records.
- **Ethana Product Fit:**
  - **Ethana Edge (Device-Level Discovery [BETA]):** Scans employee machines to build a baseline inventory of active AI tools and browser tabs.
  - **Ethana Build (Immutable Audit Logs [GA]):** Captures a permanent record of all claims processing AI API calls for IRDAI inspections.
  - **Cursory Services (AI Inventory and Classification):** Replaces automated Discovery connectors to Okta/SaaS APIs with a manual, consultant-led inventory.
- **What is Delivered:** Baseline endpoint AI discovery, manual governance inventories, and inspection-ready audit logs.
- **Gaps & Boundaries:**
  - **Ethana Workspace (unverified)** cannot be positioned for secure chat or document RAG. Any internal chat application must be custom-built by the client and routed through the **Ethana Build Gateway [GA]**.
  - Active browser-level blocking of unauthorized portals and PII redaction at the browser screen are **Roadmap** capabilities.

---

## 3. IT Services and ITeS

### Use Case 3.1: Client MSA Compliance & Developer AI Auditing
- **Target Buyer:** CIO, Head of Delivery, DevEx Lead.
- **Regulatory Drivers:** Client Master Services Agreements (MSAs), Intellectual Property (IP) Indemnification clauses.
- **Key Pain:** Developers are rapidly adopting AI assistants (Cursor, GitHub Copilot, Claude Code, Cline) to write client code. This violates client MSAs that prohibit code exfiltration, third-party model training on proprietary code, or ingestion of client secrets.
- **Ethana Product Fit:**
  - **Ethana Edge (Developer Monitoring [BETA]):** Audits and captures prompt history and IDE assistant sessions.
  - **Ethana Edge (Asset Inventory [BETA]):** Identifies active endpoint MCP servers and configurations in controlled developer groups.
  - **Ethana Build (LLM Gateway [GA]):** Centralizes developer model access using virtual API keys mapped to specific client projects.
- **What is Delivered:** Audit records of developer AI assistant usage in Beta testing groups, backed by project-level gateway controls.
- **Gaps & Boundaries:**
  - **Ethana Edge is in Beta.** It is not verified for institutional-scale deployment across thousands of developer machines.
  - Active source code masking and secret blocking before developer assistants transmit data to APIs are **Roadmap** capabilities. Today, Ethana provides auditing and discovery, not active endpoint blocking.

---

## 4. Healthcare and Life Sciences

### Use Case 4.1: Patient Data (PHI) Protection & Clinical AI Auditing
- **Target Buyer:** CISO, Head of Digital Health, DPO.
- **Regulatory Drivers:** DPDP Act, HIPAA (health data regulations).
- **Key Pain:** Doctors and clinical researchers paste patient notes, diagnostic files, and PHI into public AI chatbots or RAG pipelines. Standard security systems cannot detect PHI masked inside unstructured conversational text.
- **Ethana Product Fit:**
  - **Ethana Build (Gateway PII Scanner [GA]):** Scans unstructured inputs and masks PHI fields before routing to external models.
- **What is Delivered:** Secure, VPC-deployed API gateways that filter out patient PHI before data routes to external models.
- **Gaps & Boundaries:**
  - **Ethana Workspace (unverified)** cannot be used for clinical document ingestion or RAG storage. PII masking inside corporate vector databases is not supported.
  - **HIPAA Compliance:** Ethana is currently **HIPAA-ready in progress**, not certified. Do not claim HIPAA compliance in clinical sales conversations.
  - Clinical accuracy and medical logic validation are out of scope. Ethana governs the data flow, not the medical correctness of the AI.

---

## 5. Enterprise Tech and Professional Services

### Use Case 5.1: Governing Developer Sprawl & Agentic Infrastructure
- **Target Buyer:** Chief AI Officer, Platform Lead.
- **Regulatory Drivers:** Internal Data Governance Policies, ISO 27001 (Control A.12.4).
- **Key Pain:** Engineering teams are deploying autonomous agents connected to databases and tools via Model Context Protocol (MCP). Agents act with full human permissions, and there is no audit log showing whether a database drop or email send was done by a human or an autonomous agent.
- **Ethana Product Fit:**
  - **Ethana Build (MCP Security Broker [GA]):** Provides a central registry, allow-list, rate limits, and per-call tracing for agent tool calls.
  - **Ethana Build (PromptOps [GA]):** Tracks system prompt versioning and changes over time, enabling rollbacks.
- **What is Delivered:** Operational control and tracing of all autonomous agent actions at the infrastructure level.
- **Gaps & Boundaries:**
  - **The Visual Agent Builder (DAG Builder) is Unverified.** Do not pitch visual agent creation or drag-and-drop workflows. Developers must build agents in code.
  - Ephemeral tokens, OAuth 2.0 token exchange, and SPIFFE-style workload identities (Non-Human Identity) are **In Build**. Until NHI ships, agent identity separation is unsolved.
