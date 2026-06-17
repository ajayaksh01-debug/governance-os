# Model Risk Controls

## Purpose

Model risk is the risk of adverse consequences — financial loss, regulatory action, reputational damage, harm to individuals — arising from errors in the development or use of models. It is not a new concept: financial institutions have managed model risk for decades under frameworks like the US Federal Reserve's SR 11-7 and the UK PRA's SS1/23.

Generative AI and large language models expand the model risk universe significantly. This document defines model risk controls applicable to both traditional ML models and LLM-based systems.

---

## Model Risk in the AI Era

Traditional model risk management addressed quantitative models — credit scoring, market risk, fraud detection — with defined inputs, outputs, and measurable performance metrics. LLMs introduce additional dimensions:

- **Hallucination risk:** LLMs generate plausible-sounding false content. Unlike a traditional model that produces an incorrect score, an LLM can produce a convincing, authoritative-sounding incorrect statement.
- **Prompt sensitivity:** LLM outputs are sensitive to minor changes in input phrasing. The same question, phrased differently, may produce different answers — making reproducibility and auditability harder.
- **Emergent capabilities:** LLMs develop capabilities that were not explicitly trained for. These can be beneficial or harmful and are difficult to predict in advance.
- **Third-party model dependency:** Most organisations deploying LLMs use third-party foundation models. This creates a dependency on an external organisation's model risk management practices.
- **Context dependence:** LLM behaviour is context-dependent — the model behaves differently based on conversation history, system prompt, and retrieved context.

---

## Model Inventory and Classification

### Model Inventory

Every model in production must be inventoried. The inventory is the foundation of model risk management — without a complete inventory, there is no way to assess, monitor, or govern model risk.

Minimum inventory fields:

| Field | Description |
|---|---|
| Model ID | Unique identifier |
| Model name | Business name |
| Type | Statistical ML, deep learning, LLM, rule-based, hybrid |
| Provider | Internal, or third-party provider name |
| Version | Current version in production |
| Purpose | What decision or task the model supports |
| Business owner | Accountable business line owner |
| Technical owner | Responsible technical team |
| Risk tier | High, medium, low (per classification criteria) |
| Deployment date | When current version was deployed |
| Last validated | Date of most recent formal validation |
| Dependencies | Other models or data pipelines this model depends on |

### Risk Tier Classification

Classify models by the consequence of model failure:

**High risk:** Models where errors directly cause significant harm — financial loss, discriminatory decisions affecting individuals, safety-critical decisions. Examples: credit scoring, fraud detection (with direct action), insurance underwriting, trading systems with direct execution.

**Medium risk:** Models that inform decisions but with human oversight, or where errors have moderate impact. Examples: customer segmentation, risk monitoring dashboards, recommendation engines with human review.

**Low risk:** Models where errors have limited impact or are easily detected and corrected. Examples: internal productivity tools, document summarisation, internal search.

High-risk models require more rigorous validation, monitoring, and governance than medium or low-risk models. Controls should be proportionate to risk tier.

---

## Model Development Controls

### Development Standards

Establish and enforce standards for model development:
- Model purpose and success criteria defined before development begins
- Training, validation, and test datasets must be separate — no data leakage
- Data quality assessment completed and documented before model training
- Feature selection and engineering must be documented and justified
- Model choices (algorithm, architecture, hyperparameters) must be documented

### Bias Evaluation

For any model making decisions about individuals or groups:
- Test model performance across demographic subgroups
- Calculate and document fairness metrics appropriate to the use case (demographic parity, equalised odds, individual fairness)
- Identify and document any disparate impact
- Define acceptable thresholds for disparity — and require remediation if thresholds are exceeded

### Documentation Requirements

Before a model proceeds to validation, it must have:
- Model development report (methodology, data, results, limitations)
- Data lineage documentation
- Fairness evaluation results
- Security assessment (for externally-facing or high-risk models)
- Intended use and out-of-scope use documentation

---

## Model Validation

Model validation is an independent assessment of a model's appropriateness, accuracy, and reliability — conducted by a team independent of the model developers.

### Validation Independence

Validation must be independent of model development. The same team cannot validate a model they built. Independence can be achieved through:
- A dedicated model validation function
- Internal audit involvement for high-risk models
- Third-party validation for the highest-risk models

### Validation Scope

Validation of ML models should cover:
- **Conceptual soundness:** Is the modelling approach appropriate for the problem?
- **Data quality:** Is the training data representative, accurate, and appropriately licensed?
- **Model performance:** Does the model perform as intended on held-out test data?
- **Fairness:** Does the model produce equitable outcomes across demographic groups?
- **Robustness:** How does the model behave on edge cases, out-of-distribution inputs, and adversarial inputs?
- **Implementation:** Is the model correctly implemented in the production environment?

### LLM-Specific Validation

For LLM deployments, standard ML validation is insufficient. Additional validation scope:
- **Hallucination rate:** Test the model's tendency to generate false or fabricated content in the specific deployment context
- **Instruction adherence:** Test whether the model reliably follows its system prompt and intended constraints
- **Safety and content controls:** Test whether safety controls can be bypassed through adversarial prompting (red-teaming)
- **Prompt injection vulnerability:** Test whether the model is vulnerable to injection attacks in its deployment context
- **Output consistency:** Test the consistency of outputs for equivalent inputs across multiple runs
- **Third-party model assessment:** For models built on external foundation models, assess the provider's model risk management practices

### Champion/Challenger

For high-risk quantitative models, implement champion/challenger testing:
- The current production model is the "champion"
- A new candidate model is the "challenger"
- Both models score the same inputs in parallel (shadow mode)
- Challenger performance is compared against champion before promotion
- Promotion requires documented approval from model risk governance

---

## Production Monitoring

### Performance Monitoring

Once in production, models must be monitored continuously:
- **Accuracy metrics:** Where ground truth is available (e.g., eventual loan outcomes for credit models), track prediction accuracy over time
- **Drift detection:** Monitor input distribution drift (the world the model was trained on is changing) and output drift (model scores are shifting without a corresponding change in inputs)
- **Business outcome alignment:** Do downstream business outcomes align with model predictions?

### LLM Monitoring

For LLM deployments in production:
- Monitor for hallucination indicators (factual accuracy, citation quality for RAG systems)
- Monitor for safety control failures (harmful content generation rates)
- Monitor for prompt injection attempts and successes
- Monitor output quality metrics relevant to the use case
- Track user feedback signals (corrections, rejections, complaints)

### Threshold-Triggered Review

Define thresholds for each monitoring metric that trigger formal review:
- Minor threshold breach → review within defined period, document finding
- Significant threshold breach → immediate escalation, consider suspension pending review
- Critical failure → automatic suspension, immediate investigation

---

## Model Change Management

All changes to models in production must follow a formal change management process:
- Change request with description of the change and business justification
- Impact assessment — does the change affect model behaviour, outputs, or risk tier?
- Validation requirement — does the change require full or partial revalidation?
- Testing in a non-production environment
- Approval from model risk governance
- Deployment with rollback capability

Minor changes (configuration changes, system prompt updates for LLMs) must still go through change management — they can materially affect model behaviour.

---

## Model Retirement

When a model is decommissioned:
- Document the retirement decision and rationale
- Ensure all dependencies are updated or decommissioned
- Archive model documentation and validation evidence for the regulatory retention period
- Revoke credentials and access associated with the model
- Notify relevant stakeholders

---

## SR 11-7 and SS1/23 Alignment

For BFSI clients, model risk controls must align with the applicable regulatory model risk management framework:

| Requirement | SR 11-7 (US) | SS1/23 (UK) | Implementation |
|---|---|---|---|
| Model identification | Required | Required | Model inventory |
| Conceptual soundness | Required | Required | Development documentation |
| Ongoing monitoring | Required | Required | Performance monitoring |
| Change management | Required | Required | Change management process |
| Validation independence | Required | Required | Independent validation function |
| Governance | Required | Required | Model Risk Committee |

---

## Framework Mapping

| Framework | Relevant Requirements |
|---|---|
| SR 11-7 | US model risk management — the primary BFSI standard |
| PRA SS1/23 | UK model risk management for banks and insurers |
| ISO 42001 | AI system lifecycle; performance evaluation; human oversight |
| NIST AI RMF | MEASURE — Testing and monitoring; MANAGE — Risk treatment |
| EU AI Act | Article 9 — Risk management system; Article 15 — Accuracy and robustness |
