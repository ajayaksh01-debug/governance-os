# Governance OS

Governance OS is Cursory's operational intelligence layer for AI governance and security. It is a structured knowledge, skills, and agent system designed to help enterprises understand, assess, and manage AI risk — at the speed AI is being deployed.

---

## Why It Exists

AI adoption is outpacing governance. Enterprises are deploying large language models, autonomous agents, and third-party AI tools without the risk controls, audit infrastructure, or regulatory clarity they would demand of any other enterprise system.

The consequences are real: data leaks, biased decisions, regulatory exposure, and reputational harm. Regulators are moving — the EU AI Act is in force, India's DPDP Act is live, and sectoral regulators (RBI, FCA, SEC) are publishing AI-specific guidance.

Governance OS exists to close this gap. It gives Cursory's team — and through them, Cursory's clients — a structured, reusable foundation for AI governance work: frameworks, incident intelligence, controls, and agent-driven assessment.

---

## Architecture

Governance OS is built in four layers. Each layer is independently useful and composable with the others.

```
┌─────────────────────────────────────────────────┐
│                  Agent Layer                    │
│   Autonomous governance agents and workflows    │
├─────────────────────────────────────────────────┤
│                  Skills Layer                   │
│   Reusable governance tasks and assessments     │
├─────────────────────────────────────────────────┤
│                 Knowledge Layer                 │
│   Frameworks · Regulations · Incidents ·        │
│   Controls · Industry Patterns                  │
├─────────────────────────────────────────────────┤
│               Evaluation Layer                  │
│   Scoring, benchmarking, and audit evidence     │
└─────────────────────────────────────────────────┘
```

---

## Knowledge Layer

The knowledge layer is the factual foundation. It contains structured markdown documents covering:

- **Frameworks** — ISO 42001, NIST AI RMF, OWASP LLM Top 10. The standards against which AI systems are assessed.
- **Regulations** — EU AI Act, UK AI Guidance, India AI Landscape. Jurisdiction-specific obligations and timelines.
- **AI Incidents** — Real-world AI failures with root cause analysis and control lessons. Used to ground risk assessments in what has actually gone wrong.
- **Controls** — Technical and operational controls mapped to risks. The actionable layer.
- **BFSI** — Financial services-specific governance patterns for banking, wealth management, insurance, and GCC operations.
- **Ethana** — Cursory's product, its capabilities, and how it maps to frameworks and buyer problems.

Knowledge documents are written for executive and practitioner audiences. They are not academic summaries — each document includes risks, controls, business impact, and recommendations.

---

## Skills Layer

The skills layer contains reusable, parameterised governance tasks that can be executed by humans or agents. Examples:

- Run a gap assessment of a client's AI inventory against ISO 42001
- Map a specific AI use case to OWASP LLM Top 10 risks
- Generate a regulatory exposure summary for a BFSI client under the EU AI Act
- Produce a model risk report for a credit scoring system

Skills take structured inputs (client context, use case, jurisdiction) and produce structured outputs (risk ratings, gap tables, recommendations). They are the executable primitives of the governance workflow.

---

## Agent Layer

The agent layer contains autonomous agents that orchestrate skills and knowledge to complete end-to-end governance tasks. Current and planned agents:

- **Ethana Assessment Agent** — Conducts an AI governance readiness assessment, maps findings to frameworks, and produces a report.
- **Incident Intelligence Agent** — Monitors for new AI incidents, classifies them by risk type, and updates the knowledge base.
- **Regulatory Watch Agent** — Tracks regulatory changes across jurisdictions and surfaces obligations relevant to a client's AI portfolio.
- **Control Validation Agent** — Tests whether stated controls are implemented and effective, using evidence from client systems.

Agents operate within defined scope boundaries and escalate to human review for high-stakes decisions.

---

## Evaluation Layer

The evaluation layer provides scoring, benchmarking, and audit evidence. It answers the question: how good is this AI governance programme, and how do we prove it?

Components:

- **Maturity Scoring** — Five-level maturity model across governance dimensions (inventory, risk assessment, controls, monitoring, culture).
- **Framework Coverage** — Percentage coverage of ISO 42001, NIST AI RMF, and applicable regulations.
- **Control Effectiveness** — Evidence-based scoring of whether controls are designed and operating effectively.
- **Benchmark Comparisons** — Peer comparison across industry and size cohort.
- **Audit Evidence Packs** — Structured evidence bundles ready for regulator or internal audit consumption.

---

## Repository Structure

```
governance-os/
├── README.md                        # This file
├── knowledge/
│   ├── frameworks/                  # ISO 42001, NIST AI RMF, OWASP LLM Top 10
│   ├── regulations/                 # EU AI Act, UK, India
│   ├── ai-incidents/                # Real-world AI failures and lessons
│   ├── controls/                    # Technical and operational controls
│   ├── bfsi/                        # Financial services governance patterns
│   └── ethana/                      # Cursory product knowledge
├── skills/                          # Reusable governance task templates
├── agents/                          # Autonomous governance agents
├── evaluations/                     # Scoring models and audit evidence
└── workflows/                       # End-to-end governance workflow definitions
```

---

## Principles

1. **Grounded in reality.** Every risk and control references real incidents and real regulatory text, not theoretical frameworks alone.
2. **Executive-ready.** All outputs are written for decision-makers, not just technical practitioners.
3. **Jurisdiction-aware.** Governance obligations vary by geography and sector. Guidance is always contextualised.
4. **Continuously updated.** The AI regulatory and incident landscape moves fast. This system is designed to be maintained, not published once.

---

*Governance OS is built and maintained by Cursory — AI Governance and Security.*
