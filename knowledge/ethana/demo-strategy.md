# Sales Plays and Demo Strategy

*Note: This playbook translates the marketing playbook's sales motions into demonstration strategies that align with the platform's actual capability status as documented in `capability-status.md`.*

## Critical Demo Rules for Regulated Accounts
1. **Never lead with Ethana Edge in BFSI, Insurance, Healthcare, or Government.** Edge (endpoint agent) is Beta and requires complex HR/employment-law sign-off for monitoring. 
2. **Do not demo Discovery or AI Firewall as live products.** Both are firmly on the Roadmap. Use the Shadow AI *problem* to create urgency, but do not show live populating inventories or claim the capability is ready for deployment.
3. **The strongest opening is always Gateway + Immutable Audit Log.** It maps to hard regulatory requirements (FCA SYSC 9, EU AI Act Art.12) and is fully in production.

---

## Validated Sales Plays

### 1. Regulatory Audit Readiness Play (The Anchor Motion)
**Target:** CISO or Chief Compliance Officer at BFSI, Insurance, or Healthcare.
**Opening Question:** "If the regulator asked for an AI usage register tomorrow—by user, model, business unit, and data category—how quickly could you produce it for your internal applications?"
**Demo Focus:** 
- **Immutable Audit Log:** Show a live API call routing through the Gateway, and then immediately show the resulting immutable log entry with timestamp, user identity, project, and guardrail verdicts.
- **SIEM Export:** Show how this data forwards seamlessly to Splunk or Datadog.
**Why it works:** It converts a manual evidence-collection exercise into an automated, tamper-proof record.

### 2. AI Infrastructure Play (Build-Led)
**Target:** Engineering leads, platform teams, or internal AI application teams.
**Opening Question:** "How are you managing prompt versions, model routing, and evaluations across your AI applications in production?"
**Demo Focus:**
- **Gateway:** Show multi-model routing (switching a backend app from OpenAI to Anthropic without changing the app code).
- **PromptOps:** Show centralized prompt versioning and how a prompt rollback works.
- **MCP Broker:** Show a tool call being intercepted, recorded, and rate-limited.
**Why it works:** Replaces a fragmented stack of open-source tools with a unified governance layer.

### 3. Full Platform Bundle Play
**Target:** CIO, CTO, or CISO with an enterprise-wide AI mandate.
**Opening Question:** "Which layer of your AI stack do you have the least visibility into right now—the tools employees use, or the AI your teams are building?"
**Demo Focus:**
- Focus on the unified audit dashboard showing logs from multiple sources.
- Discuss the deployment flexibility: the entire platform is available on-premises or in a VPC.
**Pricing Anchor:** The Enterprise AI Control Plane Bundle delivers all capabilities for a predictable node-based price ($45,000/year/node), rather than unpredictable consumption pricing.

---

## Outbound Prospecting Principles
When writing outbound emails to secure the initial meeting/demo:
- **Diagnose, don't pitch:** Open with honest diagnostic questions specific to their industry (e.g., IRDAI readiness for insurance).
- **Be specific:** Name the real tools (Cursor, Copilot, ChatGPT Enterprise) rather than generic "AI tools."
- **State deployment early:** Mention "deployed inside your VPC or air-gapped" to immediately differentiate from SaaS-only tools.
- **One clear ask:** Ask for a 25-minute conversation with a live demo. Do not offer trials or proposals in outbound.
