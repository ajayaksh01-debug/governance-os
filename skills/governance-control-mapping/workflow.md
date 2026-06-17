# Governance Control Mapping — Workflow

## Overview

This workflow defines the step-by-step operational process for executing the Governance Control Mapping skill. It translates upstream risk analyses and regulatory obligations into practical control specifications, ensuring alignment with Cursory's risk standards and the Ethana platform's canonical capabilities.

The workflow has seven distinct phases. Each phase has specified inputs, procedures, outputs, and quality gates.

---

## Phase 1 — Intake & Baseline Calibration

**Objective:** Understand the subject AI system, upstream inputs, and client context before designing controls.

### Step 1.1 — Validate Upstream Input
- Review the `upstream_source_type` and ensure the `upstream_payload` is loaded.
- Verify payload completeness. If the payload is from [regulatory-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md), confirm Section 6 (Control Requirements) is present. If it is from [ai-incident-analysis](file:///Users/ajayrajsingh/Documents/governance-os/skills/ai-incident-analysis/SKILL.md), confirm Section 4 (Control Failures) and Section 9 (Recommended Controls) are present.

### Step 1.2 — Calibrate Client Context
Identify operational parameters that will shape the control design:
- **Jurisdictions:** EU (triggers EU AI Act / GDPR), UK (UK GDPR / FCA / PRA), or India (DPDP Act / RBI).
- **Sectoral Overlays:** Is the client in a regulated sector like BFSI? If so, retrieve sectoral rules (e.g., model validation under PRA SS1/23 or RBI MRM guidelines).
- **Deployment Topology:** Determine if the system is Cloud SaaS, Customer VPC, or On-premises. On-premises deployments restrict certain cloud-native logging or dynamic model fallbacks.
- **Existing Tooling:** Inventory existing customer security tools (e.g., Splunk, Zscaler) to map integrations.

### Phase 1 Output:
- Standardized intake summary including source, payload health, jurisdictions, sector overlays, and target maturity.

---

## Phase 2 — Risk & Trigger Extraction

**Objective:** Isolate specific failure modes and obligations requiring control coverage.

### Step 2.1 — Extract Upstream Risks
Parse the payload to compile a master list of raw requirements:
- **Regulatory Obligations:** Legal requirements (e.g., "Must notify of breach within 72 hours" or "Perform bias audits").
- **Incident Root Causes:** Specific failure triggers from incident analysis (e.g., "Indirect prompt injection via email input").
- **Commercial Commitments:** Platform coverage targets from solution mapping.

### Step 2.2 — Define Risk Scenarios & Engagements
For each extracted risk, define the exact trigger condition. For example:
- *Risk:* Prompt Injection leading to data exfiltration.
- *Trigger Condition:* User inputs adversarial text designed to override system instructions via the chat API.

### Phase 2 Output:
- Risk Scenario Registry mapping risks to specific trigger conditions.

---

## Phase 3 — Control Strategy Formulation

**Objective:** Design a balanced set of preventive, detective, and corrective controls.

### Step 3.1 — Map Controls from Library
For each risk in the registry, retrieve base control patterns from the controls library (`knowledge/controls/*`):
- For prompt injection, reference [prompt-injection-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/prompt-injection-controls.md).
- For training and inference privacy, reference [data-protection-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/data-protection-controls.md).
- For model drift and bias, reference [model-risk-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/model-risk-controls.md).
- For audit logging, reference [audit-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/audit-controls.md).
- For agents, reference [agent-governance-controls.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/controls/agent-governance-controls.md).

### Step 3.2 — Design Control Mechanics
Elaborate on the controls to make them implementation-ready:
- **Preventive:** Specify the blocking mechanism (e.g., regex filters, OPA policies) and the failure mode (Fail-Open vs. Fail-Closed).
- **Detective:** Define telemetry formats, log sources, and alerting thresholds.
- **Corrective:** Design containment steps (e.g., model routing fallbacks, credential revocation) and recovery SLAs.

### Phase 3 Output:
- Draft specifications for Preventive, Detective, and Corrective controls.

---

## Phase 4 — Control Coverage Classification

**Objective:** Map controls to the Cursory/Ethana coverage classification model.

### Step 4.1 — Apply Classification Schema
Evaluate every designed control and assign exactly one classification:
1.  **Fully Covered by Ethana:** The control is fully enforceable via verified production Ethana features.
2.  **Partially Covered by Ethana:** Ethana provides the core engine, but additional custom code or custom configurations are required.
3.  **Covered by Cursory Service:** The control requires manual Cursory consulting or red-teaming services.
4.  **Third-Party Control Required:** The control relies on non-Ethana enterprise software (e.g., SWGs, cloud firewalls, IdPs).
5.  **Customer-Owned Control:** The control is purely organizational or process-based, managed internally by the customer.

### Phase 4 Output:
- Control Coverage Classification Matrix (Section 3 of the final output).

---

## Phase 5 — Platform Status Audit (Claims Firewall Gate)

**Objective:** Enforce the commercial truth firewall by validating all platform mappings against canonical product engineering status.

### Step 5.1 — Canonical Status Check
For every control classified as *Fully Covered* or *Partially Covered* by Ethana:
- Open [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md).
- Locate the matching capability. Check if its canonical status is **Production**.
- **Hard Gate Check:** If the status is **In Build**, **Roadmap**, or **Aspirational** (e.g., Visual Agent Builder, Sentry URL filtering, Endpoint device agent enforcement), you **must** apply the following:
  1. Reclassify the control coverage to match its non-production reality (e.g., *Third-Party Control Required* or *Covered by Cursory Service*).
  2. Flag the Ethana capability as a "Roadmap item only" in Section 10.
  3. Design and document a mandatory manual or third-party workaround control that the customer can deploy today (e.g., manual ID mapping, Zscaler DLP rules).

### Phase 5 Output:
- Verified Ethana Configuration Guide (Section 10) passing all firewall checks.

---

## Phase 6 — Ownership & Evidence Assignment

**Objective:** Bind controls to concrete organizational roles and verification artifacts.

### Step 6.1 — Formulate RACI Matrix
Assign ownership for each control to prevent implementation failure:
- **Accountable (A):** Assign to a single C-suite or director-level role (e.g., CISO, DPO, VP of AI Engineering) who owns the ultimate risk.
- **Responsible (R):** Assign to the executing team (e.g., AI Platform Engineering, SOC, Compliance Operations).
- **Consulted (C) & Informed (I):** Assign relevant stakeholders (e.g., Cursory Advisory team, legal counsel).

### Step 6.2 — Define Audit Evidence Requirements
For every control, define the verification artifact:
- Specify the format (e.g., SIEM log export, signed PDF, model card).
- Define the extraction frequency (e.g., real-time audit logs, quarterly reviews).
- Define the retention period (e.g., 5 years under GDPR/RBI rules).

### Phase 6 Output:
- Control Ownership Matrix (Section 8) and Evidence & Verification Registry (Section 7).

---

## Phase 7 — Maturity Phasing & Quality Gates

**Objective:** Structure implementation timing and validate the output against quality criteria.

### Step 7.1 — Sequence the Roadmap
Analyze control complexity and map dependencies to draft a 30-60-90 day roadmap:
- **Days 1–30 (Phase 1):** Deploy foundational blocking controls (e.g., Gateway PII filters), enable logging, and assign Accountable roles.
- **Days 31–60 (Phase 2):** Setup SOC alerting routing, draft runbooks, and train developers.
- **Days 61–90 (Phase 3):** Implement automated rollbacks, perform red-teaming reviews, and test evidence collection.

### Step 7.2 — Run Quality Gate Check
Before releasing the output, verify the assessment satisfies the checklist:
1.  Are all 10 output sections present?
2.  Does every control have exactly one coverage classification?
3.  Is there any orphan control with no owner or missing evidence?
4.  **Critical Firewall Check:** Do all Ethana configuration steps map to Production capabilities, with In Build features explicitly restricted to roadmap mentions?

### Phase 7 Output:
- Maturity Roadmap (Section 9) and validated, release-ready Governance Control Mapping report.
