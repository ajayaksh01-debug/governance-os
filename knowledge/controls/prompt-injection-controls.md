# Prompt Injection Controls

## Purpose

This document defines the technical and operational controls for defending against prompt injection attacks in LLM-based systems. Controls are organised in layers — no single control is sufficient; defence-in-depth is required.

For incident examples and attack mechanics, see `knowledge/ai-incidents/prompt-injection-examples.md`.

---

## Control Architecture

```
┌─────────────────────────────────────────────────────┐
│              Layer 5: Monitoring & Response          │
│   Anomaly detection · Alerting · Incident response  │
├─────────────────────────────────────────────────────┤
│              Layer 4: Human Oversight               │
│   Review gates · Approval workflows · Audit trails  │
├─────────────────────────────────────────────────────┤
│              Layer 3: Output Controls               │
│   Output filtering · Content validation · Sandboxing│
├─────────────────────────────────────────────────────┤
│              Layer 2: Architectural Controls        │
│   Privilege separation · Least privilege · Isolation│
├─────────────────────────────────────────────────────┤
│              Layer 1: Input Controls                │
│   Input validation · Sanitisation · Length limits  │
└─────────────────────────────────────────────────────┘
```

---

## Layer 1 — Input Controls

### Input Validation and Sanitisation

**Control:** Validate and sanitise user inputs before passing them to the LLM. Detect and flag inputs containing patterns associated with injection attempts.

**Implementation:**
- Pattern matching for known injection signatures ("ignore previous instructions," "disregard your system prompt," "new task:")
- Semantic classification of inputs — flag inputs that attempt to change the model's role or override instructions
- Character and encoding normalisation to prevent obfuscation via Unicode or encoding tricks
- Removal of HTML/markdown that could be used to hide injection content

**Limitation:** Pattern matching is inherently a cat-and-mouse game. Novel injection techniques will evade filters. Input validation is a useful first layer, not a primary defence.

### Input Length Controls

**Control:** Enforce maximum input length appropriate to the use case.

**Implementation:**
- Set token limits per request that match the application's legitimate use case
- Alert on inputs significantly longer than typical for the application (potential context flooding attacks)
- Reject or truncate inputs that exceed defined limits

### Input Source Labelling

**Control:** For systems that combine user input with external data (RAG, tool outputs, web retrieval), explicitly label the source of each content segment in the model's context.

**Implementation:**
- Use XML-style tags or structured formats to delineate user content, system instructions, and retrieved data: `<user_input>...</user_input>`, `<retrieved_content>...</retrieved_content>`
- Instruct the model in the system prompt to treat differently-labelled content with different levels of trust
- Log which content segments the model's output appears to reference

---

## Layer 2 — Architectural Controls

### Privilege Separation

**Control:** Separate the model's instruction context from data it processes. Instructions from the system operator should be architecturally distinct from data retrieved from external sources.

**Implementation:**
- Use system prompt exclusively for operator instructions — never pass user-controlled or externally-retrieved content in the system prompt
- Pass retrieved external data in the human/user turn, explicitly labelled as external data
- For agentic systems, define a strict hierarchy: system prompt > operator instructions > user instructions > tool outputs > external data

### Least Privilege for Agent Capabilities

**Control:** AI agents should be granted only the minimum capabilities required to accomplish their defined task.

**Implementation:**
- Map each agent's required capabilities before deployment — avoid granting access "in case it's needed"
- Scope API credentials to the minimum necessary permissions
- Restrict file system access to the minimum directories required
- Limit network access to defined endpoints
- Disable capabilities that are not required for the specific use case

**Rationale:** Privilege separation contains the blast radius of a successful injection attack. An agent with read-only access to a limited data set is far less valuable to an attacker than one with broad read/write access.

### Context Isolation

**Control:** For multi-user or multi-session LLM deployments, enforce strict isolation between user sessions.

**Implementation:**
- Never persist context across user sessions without explicit design intent and controls
- Clear conversation history between sessions
- Implement session-level access controls on tools and data
- Audit for cross-session data leakage

---

## Layer 3 — Output Controls

### Output Filtering

**Control:** Validate and filter LLM outputs before they are acted upon or displayed to users.

**Implementation:**
- Filter outputs for PII, sensitive data patterns, and business-confidential content
- Detect outputs that appear to be following instructions from injected content rather than the system prompt
- Flag outputs that reference system prompt contents (potential system prompt extraction)
- For code-generating models, validate generated code in a sandbox before execution

### Safe Downstream Integration

**Control:** Treat all LLM outputs as untrusted when integrating with downstream systems.

**Implementation:**
- Use parameterised queries — never interpolate LLM output directly into SQL, shell commands, or API calls
- HTML-encode LLM outputs before rendering in web applications
- Validate LLM-generated function calls against an allowlist of permitted operations
- Never execute code generated by an LLM without sandboxed validation

### Output Sandboxing

**Control:** Execute LLM-generated actions (code, API calls, system commands) in sandboxed environments that limit the impact of malicious outputs.

**Implementation:**
- Code execution in isolated containers with no network access and minimal file system access
- Time and resource limits on execution
- Capture and validate all execution outputs before returning results to the model or user

---

## Layer 4 — Human Oversight

### Human-in-the-Loop for High-Impact Actions

**Control:** Require human approval before AI agents take irreversible or high-impact actions.

**Implementation:**
- Define a list of action types that require human approval (sending messages, modifying data, making financial transactions, deleting resources)
- Implement approval workflows with explicit human confirmation step
- Log all approval decisions with timestamp and approver identity
- Default to requiring approval for novel or undefined action types

### Anomalous Behaviour Escalation

**Control:** Flag AI behaviour that deviates from expected patterns for human review.

**Implementation:**
- Establish baseline patterns for the AI system's normal behaviour (typical action types, data volumes, response patterns)
- Alert when the system deviates significantly from baseline
- Escalate flagged sessions for human review before continuing

---

## Layer 5 — Monitoring and Response

### Injection Attempt Logging

**Control:** Log all inputs, outputs, and actions with sufficient detail to detect and reconstruct injection attacks.

**Implementation:**
- Log full input text, model output, and all tool calls/actions taken
- Tag logs with session, user, and timestamp
- Implement structured logging that can be queried for injection patterns
- Retain logs for a period appropriate to the organisation's incident response requirements

### Anomaly Detection

**Control:** Monitor for patterns indicative of prompt injection in production.

**Key signals to monitor:**
- Inputs containing known injection keywords or patterns
- Outputs that deviate significantly from expected format or content type
- Tool calls to resources outside the agent's expected scope
- Unusual data volumes in retrieval operations (potential exfiltration via injection)
- Agent actions occurring outside of expected operational parameters

### Incident Response

**Control:** Include prompt injection in AI incident response playbooks.

**Response steps:**
1. Detect and confirm injection (distinguish from legitimate use and model hallucination)
2. Isolate affected session or agent instance
3. Assess scope — what data was accessed, what actions were taken
4. Contain — revoke credentials or access granted during the compromised session
5. Investigate — reconstruct the injection chain from logs
6. Remediate — patch the injection vector, update filters, retrain if necessary
7. Report — notify affected parties and regulators as required

---

## Control Prioritisation by Risk Level

| AI System Type | Priority Controls |
|---|---|
| Customer-facing chatbot | L1 input validation; L3 output filtering; L5 logging |
| RAG system | L2 privilege separation; L3 downstream integration safety; L5 monitoring |
| Autonomous agent with tool access | L2 least privilege; L4 human-in-the-loop; L5 anomaly detection |
| Agentic multi-model pipeline | All layers; particular emphasis on L2 isolation and L4 oversight |

---

## Framework Mapping

| Framework | Relevant Requirements |
|---|---|
| OWASP LLM Top 10 | LLM01 — Primary; LLM07 — Plugin design; LLM08 — Excessive agency |
| ISO 42001 | AI system security controls; operational risk management |
| NIST AI RMF | MEASURE — Adversarial testing; MANAGE — Operational controls |
| EU AI Act | Article 15 — Robustness and cybersecurity for high-risk AI |
