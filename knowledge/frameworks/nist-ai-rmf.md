# NIST AI Risk Management Framework (AI RMF 1.0)

## What It Is

The NIST AI Risk Management Framework (AI RMF 1.0), published in January 2023, is a voluntary framework from the US National Institute of Standards and Technology that helps organisations manage risks arising from artificial intelligence. It is not a compliance standard — it is a structured vocabulary and set of practices for thinking about, measuring, and managing AI risk across the full lifecycle.

The AI RMF is widely referenced by US federal agencies, large enterprises, and increasingly by non-US organisations seeking a practical risk management methodology to complement or precede formal standards like ISO 42001.

---

## Why It Matters

The AI RMF matters because it is practical where other frameworks are abstract. It does not prescribe a management system — it provides actionable guidance on what to do at each stage of an AI system's life. It is the framework most commonly used by enterprise risk and technology teams to operationalise AI governance.

It also underpins US executive orders on AI and is the foundation for sector-specific AI guidance from US federal regulators. For organisations with US operations, regulatory examinations increasingly reference AI RMF alignment.

---

## Core Structure

The AI RMF is organised into two parts:

- **Part 1 — Framing Risk:** Defines AI risk, its characteristics, and how it differs from traditional software risk.
- **Part 2 — Core (GOVERN, MAP, MEASURE, MANAGE):** The operational heart of the framework — four functions that describe what responsible AI risk management looks like.

---

## The Four Core Functions

### GOVERN
**Purpose:** Establish organisational culture, accountability, and processes for AI risk management.

GOVERN is the foundation. It addresses whether the organisation has the right structures, policies, and accountability mechanisms in place before AI systems are built or deployed.

Key practices:
- AI risk management strategy and policies established and communicated
- Organisational roles and responsibilities for AI risk clearly defined
- AI risk is integrated into enterprise risk management, not siloed
- Workforce trained on AI risk awareness and governance obligations
- Third-party AI risks are identified and managed through vendor governance
- Feedback mechanisms exist to surface concerns from internal teams and affected users

GOVERN failures are the most common root cause of high-impact AI incidents. The Samsung source code leak and AI hiring bias incidents both reflect GOVERN failures — no policy, no accountability, no training.

### MAP
**Purpose:** Identify and classify AI risks in context.

MAP is where governance meets the specific AI use case. It requires the organisation to understand what an AI system does, who it affects, and what can go wrong — before and during deployment.

Key practices:
- AI use cases categorised by risk level (following a defined taxonomy)
- Affected populations and potential harms identified for each AI system
- Business context and deployment environment documented
- Data provenance and quality risks assessed
- Third-party model dependencies mapped
- Regulatory and legal obligations identified per use case and jurisdiction

MAP outputs feed directly into risk treatment decisions. Without MAP, organisations cannot prioritise — they either over-govern low-risk AI or under-govern high-risk AI.

### MEASURE
**Purpose:** Analyse, assess, and track AI risks.

MEASURE operationalises the risk identification from MAP into quantified or qualified risk assessments that can be tracked over time.

Key practices:
- Risk assessment methodologies defined and applied consistently
- AI system performance measured against fairness, reliability, and safety metrics
- Bias and discriminatory output testing conducted at development and periodically in production
- Explainability of AI outputs assessed relative to use case requirements
- Model drift and performance degradation monitored
- Incident and near-miss data collected and analysed
- Red-teaming and adversarial testing conducted for high-risk systems

MEASURE closes the gap between stated governance and actual system behaviour. Many organisations have governance documents that do not reflect how their AI systems actually perform.

### MANAGE
**Purpose:** Prioritise and address AI risks, and respond to incidents.

MANAGE converts risk assessments into action — risk treatment, incident response, and continuous improvement.

Key practices:
- Risk treatment plans developed and tracked for identified risks
- Residual risks accepted by appropriate organisational authority
- AI incidents detected, responded to, and documented
- Post-incident reviews conducted and lessons incorporated
- AI systems retired or retrained when they no longer meet performance or safety thresholds
- Stakeholder communication processes for AI-related harms or incidents

---

## AI RMF Profiles

The framework introduces the concept of Profiles — customised versions of the AI RMF tailored to specific sectors, use cases, or risk levels. NIST has published or is developing sector-specific profiles for:

- Financial services
- Healthcare
- Critical infrastructure
- Generative AI (GenAI Profile, 2024)

The GenAI Profile is particularly relevant for organisations deploying LLMs — it maps GOVERN/MAP/MEASURE/MANAGE practices specifically to generative AI risks including hallucination, prompt injection, and model misuse.

---

## Relationship to Other Frameworks

| Framework | Relationship |
|---|---|
| ISO 42001 | Complementary. AI RMF provides the risk vocabulary and practices; ISO 42001 provides the certifiable management system structure. Many organisations use both. |
| EU AI Act | The EU AI Act's risk-based approach is philosophically aligned with MAP. AI RMF practices support the operational implementation of EU AI Act obligations. |
| OWASP LLM Top 10 | OWASP provides the technical threat list; AI RMF provides the governance framework to assess and manage those threats systematically. |
| SR 11-7 (Model Risk) | AI RMF MEASURE function maps directly to SR 11-7 model validation requirements. BFSI organisations can satisfy both with a unified approach. |

---

## Business Impact

The AI RMF gives enterprise AI governance teams a common language and a structured workflow. Without it, AI risk assessments are inconsistent, non-comparable, and difficult to aggregate into a portfolio view. With it, organisations can:

- Conduct consistent risk assessments across a diverse AI portfolio
- Communicate AI risk to boards and regulators in a structured format
- Demonstrate due diligence in the event of an AI-related incident or regulatory examination
- Prioritise governance investment based on actual risk exposure

---

## Recommendations

1. Use the AI RMF as the operational methodology within an ISO 42001 management system — they are designed to be complementary, not competing.
2. Adopt the GenAI Profile for any LLM or generative AI deployment — it addresses risks (prompt injection, hallucination, misuse) that the base framework does not fully cover.
3. Implement MAP first — organisations that cannot enumerate their AI systems and their risk levels cannot manage AI risk effectively.
4. For BFSI clients, align MEASURE with SR 11-7 model validation requirements from the outset to avoid duplicative testing.
5. Make GOVERN visible to the board — AI risk that lives only in technology teams is not governed, it is managed tactically. Board-level accountability is the differentiator between mature and immature AI governance programmes.
