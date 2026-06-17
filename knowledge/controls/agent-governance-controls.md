# Agent Governance Controls

## Purpose

Autonomous AI agents — systems that can plan, decide, and act across multiple steps without human intervention for each action — represent a qualitatively different governance challenge from passive AI models. They can take real-world actions: send emails, modify databases, execute code, make API calls, browse the web, and interact with external services.

This document defines the governance controls required to deploy autonomous agents safely and responsibly.

---

## The Agent Governance Problem

Traditional AI governance focused on model outputs: what does the model say, and is it accurate, fair, and safe? Agent governance must also address model actions: what does the agent do, to what systems, with what data, and with what authorisation?

The risks compound in agentic systems:
- **Multi-step amplification:** An error or injection in step one of an agent workflow propagates through subsequent steps, potentially amplifying harm
- **Irreversible actions:** Unlike a model output that a human can review before acting on, an agent may take action directly — sending a message, deleting a file, initiating a transaction
- **Opaque reasoning:** Agent "plans" are often not human-readable in real time, making it difficult to detect when an agent is pursuing unintended objectives
- **Extended surface:** Agents interact with many external systems, each of which is a potential attack vector (see `mcp-vulnerability-risks.md`)

---

## Control Framework

### 1. Scope and Capability Definition

**Control:** Every agent must have a clearly defined, documented scope: what tasks it is permitted to perform, what systems it is permitted to access, and what actions it may take without human approval.

**Implementation:**
- Maintain an Agent Registry that documents each agent's: purpose, permitted capabilities, tool access, data access, approval requirements, and owner
- Conduct scope review at deployment and at any change to agent capabilities
- Treat capability additions as significant changes requiring governance review
- Scope must be defined by the business owner, not only by the technical team

**Why:** Agents without defined scopes expand to fill available capabilities. "The agent can do everything the tools allow" is not a governance posture.

---

### 2. Least Privilege

**Control:** Agents must be granted only the minimum permissions required to accomplish their defined scope.

**Implementation:**
- Map each required agent action to a specific permission and grant only those permissions
- Use scoped API credentials (OAuth scopes, IAM roles with minimal permissions) rather than broad credentials
- Grant time-limited credentials where possible — an agent that runs a scheduled task does not need standing access
- Revoke unused permissions; audit agent permissions quarterly
- Separate credentials per agent — do not share credentials between agents

**Examples of least privilege failures to avoid:**
- An email-drafting agent with send permissions (should be draft-only until approved)
- A data analysis agent with production database write access
- An agent with full file system access when it only needs one directory

---

### 3. Human-in-the-Loop (HITL) Gates

**Control:** Define a policy for which agent actions require human approval before execution, and implement technical enforcement of that policy.

**Action Classification:**

| Action Type | Default HITL Requirement |
|---|---|
| Read-only data retrieval | Not required |
| Creating drafts (messages, documents) | Not required |
| Sending communications (email, Slack, SMS) | Required |
| Modifying or deleting data | Required |
| Executing code in production | Required |
| Making financial transactions | Required |
| Accessing credentials or secrets | Required |
| Contacting external parties | Required |
| Any novel action not previously classified | Required (default to caution) |

**Implementation:**
- Implement approval workflows as a technical gate — the agent cannot proceed without confirmed approval
- Approval requests must include: what action is requested, why, what data will be affected, and what the consequences of approval/rejection are
- Log all approval decisions (granted or denied) with approver identity and timestamp
- Implement timeout handling — if approval is not received within a defined window, the agent should pause or abort rather than proceeding

---

### 4. Action Audit Trail

**Control:** All agent actions must be logged with sufficient detail to reconstruct what the agent did, why, and what the outcome was.

**Minimum log content per action:**
- Timestamp
- Agent identifier
- Action type and target (e.g., "sent email to addresses@example.com")
- Input context that led to the action (the prompt/plan state at the time of action)
- Tool invoked and parameters passed
- Result of the action
- Whether human approval was obtained, and by whom

**Implementation:**
- Logs must be tamper-evident (write-once or append-only)
- Logs must be retained for a period appropriate to regulatory requirements and internal audit needs
- Logs must be searchable and filterable by agent, action type, time, and outcome
- Log access must be controlled — logs may contain sensitive data from agent context

---

### 5. Scope Boundaries and Kill Switches

**Control:** Agents must have technical scope boundaries that prevent them from acting outside their defined scope, regardless of instructions received during operation.

**Implementation:**
- Allowlist-based tool access — agents can only invoke tools on an approved list; new tool access requires explicit governance review
- Allowlist-based data access — agents can only read from and write to approved data sources
- Network access controls — agents operating in restricted environments should have egress controls limiting outbound connections
- Kill switches — operational teams must be able to immediately halt any agent instance without dependency on the agent itself

**The principle:** Scope boundaries must be enforced architecturally (by the agent infrastructure), not only instructionally (by the agent's system prompt). An instruction saying "don't access the production database" is not a security control.

---

### 6. Agent Identity and Authentication

**Control:** Each agent must have a distinct identity that is used consistently for authentication, authorisation, and audit purposes.

**Implementation:**
- Unique machine identity (service account, API key) per agent — not shared with humans or other agents
- Agents must authenticate to all systems they access using their distinct identity
- Agent identity must appear in downstream system audit logs — it must be possible to attribute any system action to the specific agent that performed it
- Agent credentials must be rotated regularly and revoked immediately upon agent decommissioning

---

### 7. Monitoring and Anomaly Detection

**Control:** Agent behaviour must be monitored in production to detect deviations from expected behaviour patterns.

**Key metrics to monitor:**
- Action volume and type distribution (significant changes may indicate injection or scope drift)
- Access patterns — agents accessing data or systems outside their normal operating parameters
- Error rates — elevated error rates may indicate manipulation or infrastructure issues
- Approval rates — significant changes in approval/rejection ratios may indicate changes in agent behaviour
- External communications — volume, destinations, and content of externally-directed actions

**Response:** Anomalous agent behaviour should trigger automated pause (the agent stops acting and awaits human review), not just an alert.

---

### 8. Agent Lifecycle Management

**Control:** Agents must be subject to formal lifecycle management: creation, change, periodic review, and retirement.

**Lifecycle stages:**

| Stage | Governance Requirements |
|---|---|
| Design | Scope definition; risk assessment; HITL policy |
| Development | Security review; adversarial testing; capability documentation |
| Pre-deployment | Approval from business owner and security team |
| Production | Monitoring; periodic review; credential rotation |
| Change | Change assessment; re-approval if scope changes |
| Retirement | Credential revocation; data retention; decommission record |

**Periodic review:** All deployed agents must be reviewed at least annually (or upon any significant change) to verify: scope is still appropriate, permissions are still necessary, HITL policy is still correct, and the agent is still needed.

---

## Controls by Agent Risk Level

| Agent Risk Level | Examples | Additional Controls |
|---|---|---|
| Low | Read-only research agent, internal search | Standard logging and monitoring |
| Medium | Email draft agent, document generation | HITL for all external communications |
| High | Code execution agent, data modification agent | HITL for all actions; sandboxed execution; elevated monitoring |
| Critical | Financial transaction agent, production system access | HITL for all actions; dual approval; real-time monitoring; frequent audits |

---

## Framework Mapping

| Framework | Relevant Requirements |
|---|---|
| ISO 42001 | Human oversight controls; operational AI risk management; supply chain (MCP tools) |
| NIST AI RMF | GOVERN — Accountability; MANAGE — Operational controls; MEASURE — Monitoring |
| OWASP LLM Top 10 | LLM08 — Excessive Agency (primary); LLM07 — Insecure Plugin Design |
| EU AI Act | Article 14 — Human oversight; Article 9 — Risk management system |
