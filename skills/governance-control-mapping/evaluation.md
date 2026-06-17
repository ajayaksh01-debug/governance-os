# Governance Control Mapping — Evaluation Criteria and Scoring Rubric

## Purpose

This document defines the quality standards and evaluation criteria for Governance Control Mapping assessments. It establishes:
- A structured 100-point scoring rubric across all output sections.
- A passing threshold of 85/100 for production-grade assessments.
- The **Ethana Claims Firewall** as a hard-fail gate (automatic rejection on breach).
- Common control mapping failure modes and corrective actions.
- A peer-review checklist for compliance sign-off.

---

## Scoring Overview

| Section | Maximum Score | Weight Rationale |
|---|---|---|
| **1. Executive Summary & Control Landscape** | 10 | Sets the strategic context; must frame risks and mitigation balance clearly for executives. |
| **2. Control Taxonomy Matrix** | 10 | Establishes the structural foundation; must demonstrate a balance of preventive/detective/corrective and technical/process controls. |
| **3. Control Coverage Classification** | 15 | Amendment 1: Critical for scoping; must accurately classify every control across the Cursory/Ethana model. |
| **4. Preventive Control Specifications** | 10 | Operational actionability; must detail specific blocking triggers, mechanisms, and failure modes. |
| **5. Detective Control Specifications** | 10 | Operational actionability; must define telemetry schemas, thresholds, and routing targets. |
| **6. Corrective Control Specifications** | 10 | Operational actionability; must detail incident containment steps, recovery steps, and SLAs. |
| **7. Evidence & Verification Requirements** | 15 | Audit reliability; must specify concrete verification artifacts, frequencies, and retention rules. |
| **8. Control Ownership Matrix (RACI)** | 10 | Execution accountability; must bind controls to clear, non-overlapping roles. |
| **9. Maturity & Phased Roadmap** | 10 | Execution pragmatism; must sequence deployment over a realistic 30-60-90 day schedule. |
| **10. Ethana Configuration Guide** | 10 | Technical precision; maps controls to platform configurations. *Subject to the Claims Firewall Gate.* |
| **Total** | **100** | |

---

## The Ethana Claims Firewall Gate (Hard Fail)

The Cursory Technologies commercial claims policy requires absolute truthfulness regarding the capabilities of the Ethana platform. All entries in Section 10 (Ethana Configuration Guide) must correspond exactly to verified capabilities in [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md).

### Firewall Breach Triggers
A Firewall Breach occurs if the assessment:
1. Claims that an **In Build** capability (e.g., Sentry network Discovery, Endpoint Agent enforcement, Non-Human Identity agent tokens) is active and deployable in production today without qualifiers.
2. Claims that an **Aspirational** capability (e.g., Visual Agent Builder, developer tool configurations) exists as an engineering deliverable today.
3. Fails to document alternative manual or third-party workarounds for controls mapped to In Build or Aspirational capabilities.

### Firewall Breach Consequence
- **Automatic Failure:** Any breach of the Claims Firewall instantly overrides the numeric score, resulting in an automatic score of **0/100 (REJECTED)**.
- No peer review or revision cycle can bypass this gate; the report is blocked from release.

---

## Section-by-Section Rubric

### Section 1 — Executive Summary & Control Landscape (10 points)
*   **9–10 points:** The summary is 200–250 words, completely non-technical, and frames the system’s primary risks, the overall balance of control types, and business impacts.
*   **7–8 points:** Minor formatting issues or excessive technical jargon.
*   **5–6 points:** Fails to clearly summarize the control types or primary risks; length is significantly off.
*   **0–4 points:** Missing, generic, or written for developers rather than business executives.

### Section 2 — Control Taxonomy Matrix (10 points)
*   **9–10 points:** Tabular grid lists all controls. Categorizations across Type (preventive/detective/corrective) and Method (technical/process) are accurate. The mapping covers all major risks without single-point-of-failure gaps.
*   **7–8 points:** Minor misalignment in classification (e.g., classifying a manual audit as a technical control).
*   **5–6 points:** Matrix is incomplete; several controls are omitted or categorized in a way that suggests a misunderstanding of control taxonomy.
*   **0–4 points:** Missing or fails to categorize controls structurally.

### Section 3 — Control Coverage Classification (15 points)
*   **13–15 points:** Every single control listed in Section 2 is assigned exactly one of the five coverage classifications. The classification is technically accurate based on platform engineering realities and third-party tooling capabilities.
*   **10–12 points:** One or two controls have ambiguous classifications or are mapped incorrectly (e.g., classifying an unreleased feature control as *Fully Covered* instead of *Third-Party* or *Cursory Service*).
*   **7–9 points:** Systematic misclassification of control coverage; multiple controls missing coverage classification.
*   **0–6 points:** Missing, incomplete, or ignores the coverage classification schema.

### Sections 4, 5, & 6 — Control Specifications (30 points total — 10 points each)
*   **9–10 points:** Specifications are implementation-ready.
    *   *Preventive:* Details exact trigger conditions, blocking mechanisms (e.g., regex, OAuth scopes), and failure behaviors (Fail-Open vs. Fail-Closed).
    *   *Detective:* Defines telemetry schemas (e.g., fields logged), source systems, alert thresholds, and SOC routing.
    *   *Corrective:* Outlines clear containment steps, rollback procedures, recovery actions, and target SLAs.
*   **7–8 points:** One or two specifications lack detail (e.g., "log API requests" without specifying schema or alert thresholds).
*   **5–6 points:** Generic control recommendations (e.g., "implement prompt filtering" without detailing the regex or gateway settings).
*   **0–4 points:** Missing, duplicate, or vague advisory-style recommendations.

### Section 7 — Evidence & Verification Requirements (15 points)
*   **13–15 points:** Every designed control has a designated verification artifact (e.g., SIEM log extract, signed approval PDF). Specifies extraction frequency, collection methodology, and retention periods that align with target regulations.
*   **10–12 points:** Minor gaps in verification frequency or retention rules; evidence descriptions are slightly vague.
*   **7–9 points:** Generic verification guidance (e.g., "keep logs for review" without specifying log type or extraction method).
*   **0–6 points:** Missing evidence requirements or fails to map them to designed controls.

### Section 8 — Control Ownership Matrix (RACI) (10 points)
*   **9–10 points:** Full RACI table. Every control has exactly one Accountable (A) role (assigned to a senior C-suite or director role). Responsible (R) roles are assigned to operational teams (e.g., AI Engineering, SOC). No blank cells or overlapping accountabilities.
*   **7–8 points:** Minor RACI issues, such as listing multiple Accountable roles for a single control.
*   **5–6 points:** Systematic ownership gaps; controls are assigned to generic groups (e.g., "Engineering") rather than specific roles (e.g., "AI Platform Lead").
*   **0–4 points:** Missing RACI matrix or complete confusion of roles.

### Section 9 — Maturity & Phased Roadmap (10 points)
*   **9–10 points:** A structured 30-60-90 day timeline. Foundational controls (blocking/logging) are deployed in Phase 1 (Days 1-30). Process and automated alert controls are in Phase 2. Advanced corrective automation and audits are in Phase 3. Milestones are measurable.
*   **7–8 points:** Roadmap timeline is slightly unrealistic, or phases contain poorly prioritized controls (e.g., placing advanced audit checks before core blocking controls).
*   **5–6 points:** High-level roadmap lacking specific 30-60-90 day milestones or measurable targets.
*   **0–4 points:** Missing or unphased list of tasks.

### Section 10 — Ethana Configuration Guide (10 points)
*   **9–10 points:** Provides step-by-step configuration instructions. Production capabilities (LLM Gateway routing, PII runtime guardrails) are mapped accurately. All In Build or Aspirational capabilities are strictly designated as "Roadmap" and are accompanied by complete manual or third-party workarounds.
*   **7–8 points:** Configuration steps lack technical detail (e.g., "configure the PII filter" without listing regexes or PII entity options).
*   **5–6 points:** Configuration steps are vague or omit required manual workarounds.
*   **0 points (Breach):** Any violation of the Claims Firewall (claiming an In Build/Aspirational feature is live) triggers a firewall breach, automatically failing the entire evaluation.

---

## Release Criteria

To be approved for client delivery, the assessment must:
1.  Achieve a minimum total score of **85/100**.
2.  Pass the **Ethana Claims Firewall Gate** (no breach detected).

---

## Peer Review Checklist

Before signing off on the assessment, the reviewer must verify:
- [ ] Is there an Executive Summary written for non-technical leadership?
- [ ] Does every control in the taxonomy map to at least one risk trigger?
- [ ] Is every control assigned exactly one of the five Coverage Classifications?
- [ ] Are alert thresholds and schemas explicitly defined for detective controls?
- [ ] Is there exactly one Accountable (A) role assigned for each control?
- [ ] Does the roadmap prioritize preventive and detective controls in Phase 1?
- [ ] **Firewall Check:** Have you verified the status of every Ethana capability in Section 10 against `canonical-product-model.md`? Are all In Build capabilities flagged as roadmap items with manual workarounds?
