# AI Incident Analysis — Workflow

## Overview

This workflow defines the step-by-step process for executing the AI Incident Analysis skill. It is designed to produce consistent, high-quality governance assessments regardless of the analyst, the input format, or the incident type.

The workflow has six phases. Each phase has defined inputs, outputs, and quality gates. The full workflow typically takes 45–90 minutes for a well-documented incident. For complex or high-impact incidents, a deeper analysis may take 2–4 hours.

---

## Phase 1 — Intake and Triage

**Objective:** Understand what you have before you start analysing.

### Step 1.1 — Read and Annotate the Source Material

Read the full incident description or source material without analysing. On first pass, annotate:
- What is confirmed (stated as fact)
- What is inferred (implied but not stated)
- What is unknown (material to the analysis but not addressed in the source)

Resist the urge to begin categorising or assessing during this step. Understanding the incident fully before assessing it produces more accurate analysis.

### Step 1.2 — Determine Incident Type

Classify the incident against the input type taxonomy:

```
Is an AI system the primary or contributing cause?
├── No → Out of scope. Document and close.
└── Yes → Continue.
    │
    Is the incident primarily a security attack on an AI system?
    ├── Yes → Security Incident (Prompt Injection, Data Extraction, Supply Chain)
    └── No → Continue.
        │
        Did an AI agent take actions beyond its intended scope?
        ├── Yes → Agent Failure (+ check for Excessive Agency)
        └── No → Continue.
            │
            Did a model produce incorrect, biased, or harmful outputs?
            ├── Yes → Model Failure or Bias/Fairness Incident
            └── No → Continue.
                │
                Was the harm caused by absent or failed governance?
                ├── Yes → Governance Failure (+ identify which control categories failed)
                └── No → Data Incident or Privacy Breach
```

### Step 1.3 — Assess Evidence Quality

Rate the evidence available for this incident:

| Rating | Description | Effect on Analysis |
|---|---|---|
| High | Official reports, regulatory notices, technical disclosures, or court documents | Full analysis; high-confidence findings |
| Medium | Credible journalism, vendor statements, or industry reporting | Full analysis; note key uncertainties |
| Low | Limited public information; preliminary reports | Condensed analysis; flag information gaps explicitly |

Document the evidence quality rating in the analysis. Low-evidence analyses must clearly distinguish confirmed facts from reasonable inferences.

### Phase 1 Output
- Incident type classification
- Evidence quality rating
- List of confirmed facts, inferences, and unknowns
- Go/no-go decision on full vs. condensed analysis

---

## Phase 2 — Incident Summary

**Objective:** Produce a factual, concise account of the incident.

### Step 2.1 — Draft the Summary

Write a 150–200 word summary covering:
1. **Who:** The organisation or system type involved
2. **What:** What the AI system did or failed to do
3. **When:** Timing, if known
4. **How:** The mechanism by which the incident occurred
5. **Impact:** The immediate consequences — data affected, decisions affected, individuals harmed, financial loss, regulatory action

### Step 2.2 — Quality Check

Apply the summary quality test:
- [ ] Could a non-technical executive understand this without the source material?
- [ ] Are confirmed facts distinguished from inferences?
- [ ] Is the AI-specific dimension clear (why is this an AI incident, not just an IT incident)?
- [ ] Is the impact quantified or characterised as precisely as the evidence allows?

Revise until all boxes are checked.

---

## Phase 3 — Root Cause Analysis

**Objective:** Identify not just what happened, but why — at the level where governance intervention is possible.

### Step 3.1 — Identify the Proximate Cause

The proximate cause is the immediate trigger. It is often technical: a vulnerability was exploited, a model produced incorrect output, an agent took an unauthorised action.

State the proximate cause in one sentence.

### Step 3.2 — Apply the 5 Whys

Starting from the proximate cause, ask "why did this happen?" iteratively until reaching a level that governance can address. Document each level:

```
Proximate cause: [State what happened]
Why? → [First-level contributing factor]
Why? → [Second-level contributing factor]
Why? → [Third-level contributing factor]
Why? → [Root cause — the fundamental failure]
```

Typical root cause categories for AI incidents:
- **Policy gap:** No policy existed governing this use of AI
- **Control absent:** A required control was not implemented
- **Control failure:** A control existed but did not operate as designed
- **Governance gap:** Accountability for this type of AI risk was undefined
- **Supply chain gap:** A third-party AI component introduced risk that was not assessed
- **Training/awareness gap:** Users or operators did not understand the risks of the AI system
- **Design failure:** The AI system was designed in a way that created inherent risk

### Step 3.3 — Identify Contributing Factors

Between the proximate cause and the root cause, identify the conditions that enabled the incident. These are distinct from the root cause — they are the circumstances that made the root cause consequential.

Example structure:
- Root cause: No policy governing employee use of external AI tools
- Contributing factor 1: ChatGPT had recently been unblocked without replacement controls
- Contributing factor 2: Engineers were not trained on the data handling implications of public AI services
- Contributing factor 3: No DLP controls were in place to detect data submission to external AI endpoints

### Phase 3 Output
- Proximate cause (one sentence)
- 5 Whys chain
- Root cause with category
- Contributing factors list (2–5 factors)

---

## Phase 4 — Classification and Framework Mapping

**Objective:** Locate the incident within governance frameworks to connect it to applicable requirements and controls.

### Step 4.1 — Assign Risk Category

Select the primary risk category from the taxonomy defined in `SKILL.md`. Assign secondary categories if applicable (maximum two secondary categories).

### Step 4.2 — Map to ISO 42001

Identify which ISO 42001 clauses and Annex A controls are implicated:
- Which clause covers the governance area where the root cause sits?
- Which Annex A control, if implemented, would have prevented or mitigated the incident?

Reference `knowledge/frameworks/iso-42001.md` for clause and control details.

### Step 4.3 — Map to NIST AI RMF

Identify which NIST AI RMF function and category the incident relates to:
- **GOVERN:** If the incident reflects absent strategy, policy, or accountability
- **MAP:** If the incident reflects failure to identify or classify the risk
- **MEASURE:** If the incident reflects failure to test, monitor, or detect the risk
- **MANAGE:** If the incident reflects failure to respond, remediate, or prevent recurrence

An incident may implicate multiple functions. Note which function represents the primary failure.

### Step 4.4 — Map to OWASP LLM Top 10 (if applicable)

For incidents involving LLMs or AI applications, identify the relevant OWASP LLM Top 10 risk category. Reference `knowledge/frameworks/owasp-llm-top-10.md`.

If the incident does not involve an LLM-based system, mark this section N/A.

### Phase 4 Output
- Primary and secondary risk categories
- ISO 42001 clause(s) and Annex A control(s)
- NIST AI RMF function(s) and category
- OWASP LLM Top 10 category (or N/A)

---

## Phase 5 — Regulatory and BFSI Analysis

**Objective:** Translate the incident into regulatory and sector-specific implications.

### Step 5.1 — Identify Applicable Regulations

For each jurisdiction potentially relevant to the incident:
1. Was personal data involved? → GDPR, UK GDPR, DPDP Act
2. Was a high-risk AI system (EU AI Act Annex III) involved? → EU AI Act
3. Was a financial institution involved? → SR 11-7, SS1/23, FCA, RBI, SEBI, IRDAI
4. Were individuals discriminated against? → Employment equality law, Consumer protection law
5. Was a breach notifiable? → Assess against relevant breach notification thresholds

For each regulation identified, state:
- The specific provision implicated
- The obligation it creates
- Whether the incident would constitute a breach or trigger enforcement

### Step 5.2 — BFSI Relevance Assessment

Ask: Could this incident occur in a BFSI context? If yes:
- Which BFSI use cases are exposed? (Credit, fraud, KYC, customer service, underwriting, etc.)
- Which BFSI regulatory frameworks create specific obligations? (SR 11-7, SS1/23, FCA Consumer Duty, RBI)
- What is the specific BFSI risk — financial loss, regulatory breach, customer harm?

If the incident is not BFSI-relevant, state why and mark the section N/A.

### Phase 5 Output
- List of applicable regulations with specific provisions
- Notification obligation assessment
- BFSI impact assessment (or N/A)

---

## Phase 6 — Synthesis and Output Production

**Objective:** Produce the final analysis document.

### Step 6.1 — Identify Control Failures

Working from the root cause and contributing factors, list each control that was absent or failed. For each:
- Name the control
- Classify it (Preventive / Detective / Corrective)
- Describe the failure (Absent / Inadequate design / Inadequate operation)
- Briefly explain what the control should have done

### Step 6.2 — Extract Lessons Learned

Identify 3–5 transferable lessons. A good lesson:
- Is actionable (someone reading this can do something about it)
- Is generalisable (it applies beyond this specific incident)
- Is specific (it is more than "have better governance")

### Step 6.3 — Develop Recommended Controls

For each control failure, recommend a specific control. Prioritise controls by:
1. **Critical:** Would have prevented the incident entirely
2. **High:** Would have significantly reduced impact
3. **Medium:** Would have improved detection or recovery

For each recommended control:
- Write a clear, implementable description (not just a category name)
- Assess implementation complexity honestly
- Reference the framework requirement it satisfies

### Step 6.4 — Write the Executive Summary

Write last. By this point, the analysis is complete and the executive summary can accurately reflect the full findings.

Structure:
- Sentence 1–2: What happened and why it matters
- Sentence 3–4: The root cause in governance terms (not technical terms)
- Sentence 5–6: The most important control gap
- Sentence 7–8: The recommended action

### Step 6.5 — Final Quality Check

Before releasing the analysis, apply the evaluation rubric from `evaluation.md`. The analysis must score at least 70/100 to be released. Analyses scoring below 70 must be revised or reclassified as preliminary.

---

## Output Document Structure

The completed analysis is produced in the following structure:

```markdown
# AI Incident Analysis: [Incident Name]

**Date of Analysis:** [Date]
**Incident Date:** [Date or approximate period]
**Incident Type:** [Primary type]
**Evidence Quality:** [High / Medium / Low]
**Analysis Status:** [Final / Preliminary]

---

## 1. Incident Summary
[200 words max]

## 2. Root Cause Analysis
### Proximate Cause
### Contributing Factors
### Root Cause

## 3. Risk Category
**Primary:** [Category]
**Secondary:** [Category, Category]

## 4. Control Failures
[Table: Control | Type | Failure Mode | Description]

## 5. Applicable Frameworks
### ISO 42001
### NIST AI RMF
### OWASP LLM Top 10

## 6. Regulatory Implications
[Jurisdiction-by-jurisdiction]

## 7. BFSI Impact
[Or N/A]

## 8. Lessons Learned
[Numbered list with Lesson / Applicability / Urgency]

## 9. Recommended Controls
[Table: Control | Complexity | Priority | Framework Reference]

## 10. Executive Summary
[200 words max]
```

---

## Time Estimates

| Incident Type | Evidence Quality | Estimated Time |
|---|---|---|
| Security incident (well-documented) | High | 60–90 minutes |
| Governance failure (public reporting) | Medium | 45–75 minutes |
| Bias/fairness incident | Medium | 75–120 minutes |
| Agent failure (novel/emerging) | Low | 90–150 minutes |
| Condensed analysis (limited evidence) | Low | 30–45 minutes |
