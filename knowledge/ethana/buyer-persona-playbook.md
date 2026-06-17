# Buyer Persona and Industry Playbook

*Note: This document extracts Ideal Customer Profile (ICP) and industry-specific targeting criteria from the Marketing Playbook. It complements `buyer-solution-mapping.md`.*

## Ideal Customer Profile (Firmographic Fit)
- **Scale:** Annual revenue above $50M, or a significant internal AI developer footprint.
- **Industry:** Regulated industries, or those contractually obligated to demonstrate AI accountability (e.g., IT Services via MSAs).
- **Workforce:** 200+ employees where shadow AI is statistically certain.
- **Maturity:** Technology or engineering team actively building internal AI applications or deploying autonomous agents.
- **Infrastructure:** Preference for on-premises, VPC, or air-gapped deployment over SaaS-only solutions.

## Target Segments & Industry Hooks

### 1. BFSI (Banking, Financial Services)
- **Primary Buyer:** CISO / CIO
- **Key Pain:** Regulatory AI audit registers (RBI IT Outsourcing, SEBI, DPDP, FCA SYSC 9).
- **Outbound Hook:** Focus on diagnostic questions about the ability to produce an AI usage register for regulators (by user, model, business unit).
- **Entry Strategy:** Gateway + Immutable Audit Log (The only capability combination that is production-ready and maps directly to a hard regulatory requirement).

### 2. Insurance
- **Primary Buyer:** CISO / Head of Compliance
- **Key Pain:** IRDAI inspection readiness, AI usage audit trails. Visibility into which AI tools handle policy documents, claims data, and underwriting materials.
- **Outbound Hook:** Reference IRDAI Information & Cybersecurity Guidelines and Master Circular on Operational Resilience.
- **Entry Strategy:** Immutable Audit Log for claims and underwriting applications.

### 3. IT Services / ITeS
- **Primary Buyer:** CIO / Delivery Head
- **Key Pain:** Client MSA compliance, per-engagement data isolation. Conflict between developer AI tool adoption (Cursor, Copilot) and client data confidentiality clauses.
- **Outbound Hook:** "Your developers, Cursor, and your client's MSA." Highlight the ability to produce an audit trail for any client's CISO.
- **Entry Strategy:** Ethana Build + Gateway to govern internal developer access to models.

### 4. Healthcare
- **Primary Buyer:** CISO / CTO
- **Key Pain:** PHI leakage via AI tools.
- **Outbound Hook:** *Note: Ethana is currently HIPAA-ready in progress, not complete. Do not claim HIPAA compliance.* Focus on DPDP obligations and general sensitive data protection.
- **Entry Strategy:** Guardrails (PII masking) + Audit Logs. 

### 5. Enterprise Tech / Professional Services
- **Primary Buyer:** Platform Lead / DevEx Lead / CIO
- **Key Pain:** Governing developer AI tools, agentic infrastructure, sensitive client data exposure.
- **Outbound Hook:** Time to deploy governed AI applications safely; evaluation and PromptOps maturity.
- **Entry Strategy:** Ethana Build (Agent builder, MCP lifecycle, Gateway).
