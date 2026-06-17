# Sales Objection Handling Playbook

*Note: This playbook extracts objection handling from the Marketing Playbook and Product Study. It must be used in alignment with `boundaries.md` and `capability-status.md`.*

## Procurement and Certification Blockers

### "You don't have SOC 2 Type II or ISO 27001?"
**Response Strategy:**
Acknowledge it immediately. Do not hide it. It is a hard gate for G-SIB banks. 
**Talk Track:** "You're right, we are currently in progress on SOC 2 Type II and ISO 27001. We understand this is a prerequisite for your Third Party Risk Management (TPRM) process before any data routes through our platform. We factor this 6–12 week TPRM assessment into our joint deployment timeline, and we can provide our current security architecture documentation to begin the assessment while the certification completes."

### "We need everything on-prem / air-gapped due to data residency."
**Response Strategy:**
Confirm full support without price penalty.
**Talk Track:** "Ethana is explicitly designed for on-premises, VPC, and air-gapped deployment. We have pricing parity between SaaS and on-prem. No customer prompts, data, or telemetry are required to leave your controlled environment. This is our default recommendation for BFSI clients."

## Technical and Engineering Objections

### "Adding a gateway will add unacceptable latency to our live-call apps."
**Response Strategy:**
Acknowledge the concern and offer benchmarks, but verify production load first.
**Talk Track:** "Latency is critical, especially for live customer-facing systems. The gateway itself adds ~50ms overhead. With the full 6-scanner guardrail stack enabled (including PII and hallucination checks), we target sub-200ms p95 latency. However, we validate this against your specific production throughput during the PoC."

### "We will just use the gateway our cloud provider (AWS/Azure) offers."
**Response Strategy:**
Highlight vendor neutrality and advanced governance.
**Talk Track:** "Cloud-native gateways lock you into a single provider. Ethana Build provides provider-independent multi-model routing across OpenAI, Anthropic, Gemini, and self-hosted models. More importantly, cloud gateways don't provide PromptOps, agent MCP lifecycle management, or the specific immutable audit log schema required by financial regulators."

### "We are already building our own internal gateway."
**Response Strategy:**
Highlight the hidden cost of the governance layer.
**Talk Track:** "Many teams build a basic routing gateway. However, internal builds rarely replicate the governance layer required for compliance: PromptOps, evaluation pipelines, 21 OWASP red-teaming probes, and MCP lifecycle management. Ethana gives your engineering team the routing they want, with the governance compliance needs built-in."

### "Won't this create vendor lock-in if all our AI calls go through you?"
**Response Strategy:**
Emphasize architectural flexibility.
**Talk Track:** "Ethana actually prevents lock-in to underlying model providers. By sitting inline, you can switch from OpenAI to Anthropic or a self-hosted model without rewriting your application. Furthermore, we support on-prem deployment, giving you full control over the infrastructure."

## Security and Governance Objections

### "We already have Zscaler / DLP for data loss prevention."
**Response Strategy:**
Differentiate AI-specific observability from traditional DLP.
**Talk Track:** "Traditional DLP is not AI-aware—it has no concept of model selection, MCP servers, or agent interactions. Ethana provides AI-specific observability: a full inventory of every AI tool on every device, prompt and response visibility, and per-user attribution that a standard DLP cannot produce."

### "We are not ready for AI governance yet."
**Response Strategy:**
Create urgency around the Shadow AI reality and regulatory pressure.
**Talk Track:** "Shadow AI is already present. Your employees are using AI tools today, and your developers have direct API keys. Even if you aren't ready to enforce policies, the EU AI Act and local regulations require you to have an audit trail. We can deploy the Gateway and Audit Log today to start capturing the baseline evidence you will need tomorrow."

### "We have a small team and limited budget for new tools."
**Response Strategy:**
Highlight the node-based pricing model.
**Talk Track:** "Ethana is licensed per platform node, not per seat or per token. This means predictable costs without per-user fees as your AI adoption scales."
