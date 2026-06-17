# AI Audit Controls

## Purpose

AI audit controls are the mechanisms by which an organisation creates evidence that its AI systems are operating as intended, within governance boundaries, and in compliance with applicable obligations. Without audit controls, governance is assertion — with audit controls, governance is demonstrable.

This document defines audit controls across three dimensions: what to log, how to evaluate, and how to report.

---

## Why AI Audit Is Distinctive

Traditional IT audit focuses on access, changes, and transactions — all of which are discrete and deterministic. AI audit is more complex:

- **Behaviour is probabilistic:** The same input to an LLM can produce different outputs. Audit must capture behaviour patterns, not just individual transactions.
- **Decisions are often non-deterministic:** For AI systems making decisions, the "why" is often not encoded in traditional audit logs — it requires inference from model inputs, outputs, and versions.
- **Training and inference are both audit-relevant:** Unlike a traditional system where only transactions matter, AI audit must also cover how the model was built, what data was used, and how it was validated.
- **Models change:** A model updated (fine-tuned, retrained, or replaced) may behave differently. Audit must track model versions alongside system behaviour.

---

## Dimension 1 — Operational Logging

### Inference Logs

Every AI model call in production should be logged. Minimum log content:

| Field | Description |
|---|---|
| Timestamp | ISO 8601, millisecond precision |
| Request ID | Unique identifier for the AI call |
| Model identifier | Model name and version |
| Input | The prompt or input submitted to the model |
| Output | The model's response |
| Latency | Time taken for the model to respond |
| User/session identifier | Who or what initiated the call (anonymised if required) |
| Tool calls (for agents) | Any tool invocations made during the call |
| Approval events | Any HITL approvals obtained |
| Outcome | What action was taken based on the output |

**Sensitive data handling:** Inference logs will frequently contain personal data. Apply appropriate access controls, retention limits, and masking. Log storage must be subject to the same data protection controls as other sensitive data stores.

### Agent Action Logs

For autonomous agents, log every action taken with:
- Action type and target
- Parameters passed
- Result
- Whether the action required human approval and the approval decision
- The model's stated rationale for the action (if captured)

### System Change Logs

Log all changes to the AI system:
- Model version changes (new model deployed, fine-tuning applied)
- Configuration changes (system prompt changes, temperature changes, tool access changes)
- Data pipeline changes (new training data, updated RAG index)
- Permission changes (new capabilities granted to agents)

---

## Dimension 2 — Model and Performance Audit

### Model Documentation

Each model deployed in production must have documented:
- Model purpose and intended use
- Training data sources (with data lineage records)
- Validation approach and results
- Known limitations and failure modes
- Bias evaluation results
- Performance metrics (accuracy, precision, recall, fairness metrics as applicable)
- Approval record (who approved deployment and on what basis)

This documentation is the foundation of a model audit — without it, evaluating whether a model is performing as intended is not possible.

### Model Performance Monitoring

AI models degrade over time as the world changes but the model doesn't. Monitor:

- **Accuracy metrics:** For models with ground truth available, track prediction accuracy over time
- **Drift detection:** Statistical monitoring of input distributions and output distributions — significant changes indicate model drift
- **Business outcome tracking:** Track the downstream outcomes of AI decisions (e.g., default rates for AI-approved credit decisions, complaint rates for AI-generated customer communications)
- **Bias indicators:** Monitor demographic distributions in model outputs and decision outcomes — increasing disparity may indicate bias drift

Establish thresholds for each metric that trigger review or intervention.

### Periodic Model Revalidation

Models must be revalidated periodically — not only at initial deployment. Revalidation requirements:
- At least annually for high-risk models
- Upon significant changes to the model or its deployment environment
- When monitoring detects significant performance degradation
- When the business context changes materially (new customer segments, new products, significant regulatory changes)

Revalidation must follow the same rigour as initial validation — it is not a rubber stamp.

---

## Dimension 3 — Regulatory and Internal Audit Evidence

### Evidence Packs

For regulatory examinations and internal audits, AI governance evidence should be organised into structured packs covering:

**Governance evidence:**
- AI governance policy and ownership
- AI risk appetite statement
- AI committee or forum minutes
- Training records for AI risk awareness

**Inventory evidence:**
- AI system inventory (all models deployed, their purpose, risk classification)
- Third-party AI provider inventory
- Change log for the inventory

**Risk assessment evidence:**
- Risk assessments for each AI system
- AI impact assessments (where required)
- Bias evaluation results

**Control evidence:**
- Control design documentation
- Control testing results
- Penetration testing and red-team results (for security controls)
- Remediation records for identified control gaps

**Monitoring evidence:**
- Performance monitoring dashboards and reports
- Alert records and resolution
- Incident records (AI-related incidents, near-misses)
- Post-incident review reports

**Model validation evidence:**
- Validation reports for each model
- Data quality assessments for training data
- Challenger model results (where applicable)

### Regulatory Reporting

For BFSI and other regulated entities, AI audit controls must support regulatory reporting requirements:

| Regulator | Reporting Requirement |
|---|---|
| PRA (UK) | Model risk management evidence; SS1/23 compliance |
| RBI (India) | IT governance audit evidence; model validation records |
| EU AI Act | Technical documentation; conformity assessment records; post-market monitoring |
| ICO (UK) | DPIA records; automated decision-making records; incident reports |

---

## Explainability Requirements

For AI systems making significant decisions about individuals, audit controls must include explainability — the ability to explain why a specific decision was made in terms understandable to the affected individual and to regulators.

**Levels of explainability:**

| Level | Requirement | Applicable To |
|---|---|---|
| Global | Explain how the model works in general terms | All AI systems with public-facing explanations |
| Local | Explain why this specific decision was made for this individual | High-risk AI; automated decisions with significant effect |
| Counterfactual | Explain what would need to change for a different outcome | Credit, insurance, employment AI |

**Technical approaches:**
- SHAP values (feature importance for individual predictions)
- LIME (local interpretable model-agnostic explanations)
- Decision traces for agentic systems
- Rule extraction for tree-based models
- Attention visualisation for transformer models (limited utility for compliance purposes)

---

## AI Incident Recording

All AI-related incidents must be documented with:
- Date and time of detection
- Description of the incident
- Root cause (as determined by investigation)
- Impact assessment (data affected, decisions affected, individuals affected)
- Regulatory notification obligation (was this a notifiable breach or incident?)
- Containment and remediation actions taken
- Preventive measures implemented to avoid recurrence

Near-misses — situations where an adverse outcome was narrowly avoided — should also be recorded. Near-miss data is among the most valuable inputs to AI risk management.

---

## Audit Programme Design

An AI audit programme should include:

**Continuous monitoring:** Automated monitoring of inference logs, performance metrics, and anomaly indicators.

**Quarterly reviews:** Review of monitoring data, incident trends, and control effectiveness by the AI governance function.

**Annual audits:** Formal audit of a sample of AI systems against documented controls and governance requirements. Include penetration testing of high-risk systems.

**Regulatory examination preparation:** Maintain evidence packs in a state of readiness — regulatory examinations increasingly include AI. Evidence should be retrievable within 24 hours for any AI system.

---

## Framework Mapping

| Framework | Relevant Requirements |
|---|---|
| ISO 42001 | Clause 9 — Performance evaluation; internal audit; management review |
| NIST AI RMF | MEASURE — Monitoring; MANAGE — Incident management |
| PRA SS1/23 | Model identification; validation; governance documentation |
| EU AI Act | Article 12 — Record-keeping; Article 72 — Post-market monitoring |
| GDPR / UK GDPR | Article 30 — Records of processing; Article 35 — DPIA |
