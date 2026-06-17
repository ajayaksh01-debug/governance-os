# Skill: AI Incident Analysis

**Version:** 1.0  
**Category:** Governance Intelligence  
**Owner:** Cursory Governance Team

---

## Purpose

This skill analyses AI incidents — including security incidents, agent failures, model failures, and governance events — and produces a standardised governance assessment. The output is a structured, framework-aligned analysis that is useful to risk, compliance, security, and executive audiences.

The skill converts an incident report (any format, any level of detail) into a reusable governance artefact: a document that captures what happened, why it happened, which controls failed, what frameworks apply, and what should be done differently.

---

## When to Use This Skill

Use this skill when:
- An AI incident has occurred and requires formal governance analysis
- A reported incident (from public sources, industry sharing, or internal sources) is relevant to the organisation's AI risk profile
- A near-miss or close call involving an AI system requires documentation
- An agent failure, model failure, or unexpected AI behaviour has been observed
- A regulatory enforcement action or legal case involving AI requires assessment
- Proactive incident intelligence review is being conducted against an AI portfolio

---

## Input Specification

### Required Inputs

The skill requires at minimum a description of the incident. This may come from:
- An internal incident report
- A public news article or technical disclosure
- A regulatory enforcement notice
- A security research publication
- A customer complaint or operational alert

### Input Fields

| Field | Required | Description |
|---|---|---|
| `incident_description` | Yes | Raw description of what happened. Can be a news article, internal report, or informal summary. |
| `incident_type` | Yes | One of: AI Security Incident, Agent Failure, Model Failure, Data Incident, Governance Event, Bias/Fairness Incident |
| `organisation_context` | No | Industry, size, and AI maturity of the affected organisation, if known |
| `date` | No | When the incident occurred or was disclosed |
| `source` | No | Origin of the incident information (internal, public, research, regulator) |
| `affected_system` | No | The AI system or product involved, if known |
| `client_context` | No | If this analysis is for a specific client, their sector and AI portfolio profile |

### Input Format

Inputs do not need to be structured. The skill accepts free-form incident descriptions and extracts structured information during analysis. For internal incidents, a minimum viable input is:

> "What happened, what system was involved, and what was the observed impact."

---

## Output Specification

Every analysis produces the following ten sections. Each section has a defined structure and quality standard (see `evaluation.md`).

### 1. Incident Summary
A concise, factual description of the incident — what happened, when, to whom, and what the immediate impact was. Written for an executive audience. Maximum 200 words.

### 2. Root Cause Analysis
A structured analysis of the underlying causes. Uses the "5 Whys" method as a baseline, distinguishing:
- **Proximate cause:** The immediate trigger
- **Contributing factors:** Conditions that enabled the proximate cause
- **Root cause:** The fundamental governance, process, or technical failure

### 3. Risk Category
Classification of the incident against a defined taxonomy:

| Risk Category | Description |
|---|---|
| Prompt Injection | Input manipulation causing unintended model behaviour |
| Data Exfiltration | Sensitive data accessed or extracted via AI |
| Model Failure | Model performing incorrectly, inconsistently, or outside intended parameters |
| Bias / Fairness | Model producing discriminatory or unfair outcomes |
| Excessive Agency | AI agent taking actions beyond its intended scope |
| Supply Chain | Third-party model, dataset, or tool introducing risk |
| Privacy Breach | Personal data exposed or misused through AI |
| Governance Failure | Absence of policy, process, or oversight enabling AI harm |
| Misinformation / Hallucination | AI generating false content with material consequences |
| Security Exploitation | Adversarial attack on AI system or infrastructure |

One primary category and up to two secondary categories are assigned.

### 4. Control Failures
The specific controls that were absent, inadequately designed, or not operating effectively at the time of the incident. Each control failure is documented with:
- Control name
- Control category (Preventive / Detective / Corrective)
- Failure type (Absent / Inadequate design / Inadequate operation)
- Description of the failure

### 5. Applicable Frameworks
Mapping of the incident to relevant governance frameworks:
- **ISO 42001:** Relevant clauses and Annex A controls
- **NIST AI RMF:** Relevant functions and categories
- **OWASP LLM Top 10:** Relevant risk categories (if LLM-related)

### 6. Regulatory Implications
Assessment of regulatory exposure arising from the incident or applicable to similar incidents, covering:
- Jurisdictions where regulatory obligations are engaged
- Specific regulatory provisions implicated
- Notification obligations (if applicable)
- Potential enforcement consequences

### 7. BFSI Impact
Where the incident is relevant to financial services organisations, an assessment of:
- Which BFSI use cases are exposed to this type of incident
- Applicable BFSI regulatory frameworks (SR 11-7, SS1/23, FCA, RBI)
- Specific BFSI control gaps the incident illustrates

If the incident is not BFSI-relevant, this section is marked N/A with a brief rationale.

### 8. Lessons Learned
The transferable insights from the incident — what other organisations deploying similar AI systems should take away. Structured as:
- **Lesson:** What the incident teaches
- **Applicability:** Which types of AI systems or organisations this applies to
- **Urgency:** How urgently this lesson should be acted on

### 9. Recommended Controls
A prioritised list of controls that would have prevented or significantly mitigated the incident. For each control:
- Control name and description
- Implementation complexity (Low / Medium / High)
- Priority (Critical / High / Medium)
- Framework reference (which frameworks require or recommend this control)

### 10. Executive Summary
A 150–200 word summary of the entire analysis, written for a board or C-suite audience. Covers: what happened, why it matters, and what action is recommended. No technical jargon.

---

## Constraints and Scope

**In scope:**
- Incidents involving AI systems (LLMs, ML models, AI agents, AI-enabled products)
- Incidents where AI is the proximate or contributing cause
- Governance events where AI oversight failed
- Incidents with governance lessons applicable beyond the specific organisation

**Out of scope:**
- Pure cybersecurity incidents with no AI-specific dimension
- Software bugs in non-AI systems
- Incidents where AI is mentioned incidentally but is not causal

**Depth calibration:**
Analysis depth should be proportionate to incident severity and evidence availability. A high-impact, well-documented incident warrants a full 10-section analysis. A low-impact incident with limited public information may produce a condensed assessment noting information gaps.

---

## Knowledge Dependencies

This skill draws on the following knowledge base documents:

- `knowledge/frameworks/iso-42001.md`
- `knowledge/frameworks/nist-ai-rmf.md`
- `knowledge/frameworks/owasp-llm-top-10.md`
- `knowledge/regulations/eu-ai-act.md`
- `knowledge/regulations/uk-ai-guidance.md`
- `knowledge/regulations/india-ai-landscape.md`
- `knowledge/controls/prompt-injection-controls.md`
- `knowledge/controls/agent-governance-controls.md`
- `knowledge/controls/data-protection-controls.md`
- `knowledge/controls/audit-controls.md`
- `knowledge/controls/model-risk-controls.md`
- `knowledge/ai-incidents/` (for precedent and pattern recognition)

---

## Related Skills

- `skills/risk-assessment/` — for translating incident findings into a client risk register
- `skills/framework-gap-analysis/` — for converting control failure findings into a gap assessment
- `skills/regulatory-exposure/` — for deeper jurisdictional regulatory analysis
