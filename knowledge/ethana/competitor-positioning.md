# Ethana Competitor Positioning Playbook

This document details Ethana's competitive positioning across its three core product lines (**Ethana Edge**, **Ethana Workspace**, **Ethana Build**) and **Cursory Services**. It outlines specific differentiation, battle-cards, and pricing comparison models based on actual capability coverage (Production vs. In Build/Roadmap/Unverified) as of June 2026.

---

## 1. The Core Differentiator: Integrated Operational Control Plane

Ethana's primary value proposition is that it consolidates fragmented point solutions into a single, cohesive **Enterprise AI Control Plane**. Instead of purchasing, integrating, and auditing five different tools, enterprises deploy one unified platform that governs the entire AI estate across endpoints, workspaces, and developer APIs, backed by an immutable audit trail and on-premises deployment options.

```
+---------------------------------------------------------------------------------+
|                                 CURSORY SERVICES                                |
|          (Assessments, Framework Mapping, Implementation, Retainers)            |
+---------------------------------------------------------------------------------+
|                          ETHANA AI CONTROL PLANE (VPC/On-Prem)                  |
|   +--------------------------+-----------------------+-----------------------+  |
|   |       ETHANA EDGE        |   ETHANA WORKSPACE    |     ETHANA BUILD      |  |
|   |   (Observability - BETA) | (Chat/RAG-UNVERIFIED) | (Gateway, Guardrails) |  |
|   +--------------------------+-----------------------+-----------------------+  |
+---------------------------------------------------------------------------------+
```

---

## 2. Competitor Category Battle-Cards

### Category 1: AI Gateways & Routing Tools
*Competitors: Portkey, LiteLLM, Kong (AI Gateway)*

- **Competitor Stance:** High maturity in LLM routing, latency optimization, provider load-balancing, and basic developer logging.
- **Ethana Build Differentiation:**
  - **Governance Integration:** Competitors focus on developer convenience and API routing. Ethana Build integrates multi-model routing with 6 runtime guardrails, PromptOps versioning, active red-teaming simulations, and an MCP security broker in a single gateway.
  - **Immutable Audit Log:** Ethana provides a write-once, tamper-proof audit trail designed for regulatory inspection (FCA, RBI, EU AI Act), whereas standard gateways offer transient application-level developer logs.
- **Radical Honesty Boundary:** Do not claim feature superiority on pure routing speed or developer-centric gateway bells and whistles. Portkey and LiteLLM are highly mature in API optimization. Win on the integrated security, compliance audit log, and on-premises VPC parity.

### Category 2: AI Observability & Tracing Tools
*Competitors: Langfuse, Arize, Helicone, PromptLayer*

- **Competitor Stance:** Excellent developer tools for tracing application execution graphs, inspecting prompt steps, logging outputs, and tracking LLM call latency.
- **Ethana Build Differentiation:**
  - **Active Control vs. Passive Observation:** Observability tools are passive and read-only. Ethana Build is an inline control plane that enforces policies (guardrails) and brokers tools (MCP Broker) at runtime, blocking or redacting content before it reaches the model or user.
  - **Enterprise Compliant Logs:** Ethana's log store is insert-only and write-once, with direct SIEM integrations. Competitors store debug logs in developer-accessible databases, which fail regulator tamper-proofing checks.
- **Radical Honesty Boundary:** For debugging complex multi-agent execution graphs, Langfuse is highly detailed. Ethana's focus is compliance and security governance, not developer application debugging.

### Category 3: AI Security, DLP & CASBs
*Competitors: LayerX, Nightfall, Calypso AI, HiddenLayer*

- **Competitor Stance:** Strong network proxies or API integrations to block PII exfiltration, malicious attachments, or unsafe browsing behaviors.
- **Ethana Edge Differentiation:**
  - **AI-Aware Context:** Traditional DLP and CASB tools scan network streams for regex patterns. Ethana Edge is AI-aware, capturing the context of the prompt/response, identifying the model being used, attributing it to specific users, and inventorying the active MCP servers on developer endpoints.
  - **Developer Tooling Audits:** Ethana Edge is the only tool that actively audits local developer environments using Cursor, Copilot, Cline, and local models.
- **Radical Honesty Boundary:** **Ethana Edge is currently in Beta.** Competitors have active network-level and browser-level blocking and masking live in production. Ethana Edge's active blocking, browser-level redirection, and PII masking before API transit are **Roadmap** capabilities (currently in development). Edge today is **observability and discovery only**.

### Category 4: Enterprise AI Chat & RAG Platforms
*Competitors: Microsoft Copilot, Glean, ChatGPT Enterprise*

- **Competitor Stance:** Out-of-the-box corporate search, knowledge base integration, and user chat. Deeply integrated into existing SaaS suites (Microsoft 365, Slack, etc.).
- **Ethana Workspace Differentiation:**
  - **True On-Premises & Air-Gapped Parity:** Competitors are SaaS-first or SaaS-only, routing corporate prompts through public cloud infrastructure. Ethana Workspace runs entirely inside the client's own VPC or physical data center.
  - **Immutable Prompt/Response Audit:** Every chat session, prompt, response, and document export is permanently captured in an insert-only audit log, with role-based access controls and automatic storage PII masking.
- **Radical Honesty Boundary:** **Ethana Workspace is Unverified in the codebase.** While marketed as GA, there is no engineering corroboration of Workspace in the repository. Do not represent Workspace as available to clients. Microsoft Copilot, Glean, and ChatGPT Enterprise are fully operational production platforms.

### Category 5: AI Governance & GRC Policy Platforms
*Competitors: Credo AI, AIShield, OneTrust, Archer*

- **Competitor Stance:** Documentation platforms for mapping AI risk, writing policies, managing compliance registers, and logging vendor assessments.
- **Ethana Platform Differentiation:**
  - **Operational Runtime Evidence:** GRC platforms are static databases of questionnaires and compliance forms. Ethana is an operational control plane. It sits inline, intercepts the data, blocks the threat, and generates the exact, tamper-proof evidence that compliance teams otherwise collect manually to upload to GRCs.
- **Radical Honesty Boundary:** Ethana does **not** replace a GRC platform. It does not manage risk registers or vendor assessments. Ethana feeds evidence *into* GRC platforms. Position as complementary, not a replacement.

### Category 6: Agent Development Platforms
*Competitors: LangChain, CrewAI*

- **Competitor Stance:** Code frameworks for developers to build multi-agent applications, connect tools, and define workflows.
- **Ethana Build Differentiation:**
  - **Visual Orchestration & MCP Brokerage:** LangChain is a code library. Ethana Build provides the MCP Security Broker to control, rate-limit, and trace agent tool calls in production.
- **Radical Honesty Boundary:** **The Visual Agent Builder (DAG Builder) is Unverified in the codebase.** Do not claim visual workflow capabilities exist. Developers must write agent logic in code and route tool calls through Ethana's MCP Broker. Note that agent identity separation (NHI) and ephemeral tokens are **In Build**.

---

## 3. Commercial & Pricing Differentiation

Ethana's commercial model is designed to disrupt traditional SaaS pricing:

| Pricing Dimension | Traditional AI Governance / SaaS Vendors | Ethana Platform Model |
|---|---|---|
| **Pricing Metric** | Per-seat, per-user, or consumption-based (token volume). | **Per-node flat annual fee.** Edge ($10k), Workspace ($10k), Build ($30k), Bundle ($45k). *Note: Edge is Beta; Workspace is Unverified.* |
| **Budget Predictability** | High variability. Costs spike as user adoption or token usage increases. | **100% predictable.** Flat rate irrespective of user count or token throughput. |
| **Deployment Premium** | Severe price premium (often 50-100% markup) for VPC/On-Premises deployment. | **Pricing Parity.** SaaS, VPC, and On-Premises deployments cost the exact same. |
| **Expansion Cost** | Linear cost growth as the organization scales. | **Low marginal cost.** Additional nodes are flat-rate ($2k/yr for Edge/Workspace, $5k/yr for Build). |
