# Workflow: Governance Assessment

## 1. Purpose
The **Governance Assessment Workflow** delivers a comprehensive baseline audit of a client's AI governance program against industry standards (ISO 42001, NIST AI RMF). It identifies compliance gaps, designs target controls, establishes a maturity roadmap, and validates current platform integration claims.

---

## 2. Trigger
- **New Client Onboarding:** A new client onboarding process is initiated.
- **Annual Governance Audit:** Triggered by a recurring compliance calendar milestone.
- **Certification Readiness Check:** The client requests a certification audit mock run before submitting to an external registrar.

---

## 3. Inputs
- `client_ai_portfolio` (Required): Inventory of deployed models, use cases, and technical details.
- `existing_policies` (Required): Current AI guidelines, risk registers, and control evidence.
- `target_framework` (Required): One of: `ISO 42001`, `NIST AI RMF`, `Custom Baseline`.
- `target_maturity_level` (Required): Target score (e.g., `L4: Managed`).

---

## 4. Skill Sequence

```
[Client AI Portfolio & Policies]
               │
               ▼
   1. regulatory-mapping (Framework Scoping)
               │
               ▼ (Section 2 framework payload)
   2. [FUTURE: ISO 42001 Gap Assessment] (Placeholder)
               │
               ▼ (Identified gaps payload)
   3. governance-control-mapping (Maturity Roadmap & RACI)
               │
               ▼ (Technical control specs)
   4. ethana-capability-validation (Truth Gate Validator)
               │
               ▼
   [Client Governance Audit Binder]
```

### Step 4.1: Framework Scoping
- **Skill Engaged:** [regulatory-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/)
- **Process:** Ingest the client's AI portfolio and policies. Map them against target framework clauses (e.g., ISO 42001 Clause 8, Annex A controls) to establish applicability boundaries.

### Step 4.2: Framework Gap Analysis (Placeholder Integration)
- **Skill Engaged:** **[FUTURE: ISO 42001 Gap Assessment]**
- **Process:** Ingest Section 2 (Applicable Governance Frameworks) from Regulatory Mapping. Run a clause-by-clause compliance audit against current client evidence. Output a detailed gap register highlighting missing controls, inadequate documentation, or unverified audit records.

### Step 4.3: Maturity Roadmap & RACI Design
- **Skill Engaged:** [governance-control-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/governance-control-mapping/)
- **Process:** Ingest the gap register from the previous step. Design target technical and process controls to close gaps. Construct the RACI ownership matrix and design a prioritized 30-60-90 day maturity roadmap.

### Step 4.4: Truth Gate Integration Check
- **Skill Engaged:** [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/)
- **Process:** Extract all proposed platform controls from Section 10 of the control mapping. Audit them against [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) using the Truth Gate (`comp.truth_gate`). Verify that no unreleased or Aspirational features are claimed as current compliance evidence.

---

## 5. Outputs
- **Framework Compliance Scorecard:** Clause-by-clause compliance status against ISO 42001 or NIST AI RMF.
- **Control Maturity Registry:** Assessment of current vs. target maturity levels for each control.
- **30-60-90 Day Maturity Roadmap:** prioritized implementation timeline to achieve target maturity.
- **Audit Evidence Binder:** Structured registry of digital verification artifacts.
- **Ethana Claims Audit:** Validated platform configurations and manual workarounds for roadmap dependencies.

---

## 6. Quality Gates
- **Framework Mapping Gate:** Framework scoping must identify specific relevant Annex A controls (score $\ge 70$ in Regulatory Mapping).
- **Maturity Alignment Gate:** Control mapping score must be $\ge 85/100$, with all designed controls bound to measurable evidence artifacts.
- **Claims Firewall Gate:** 100% compliance with `canonical-product-model.md`. Zero unreleased features committed as production compliance evidence.

---

## 7. Failure Conditions
- **Missing Evidence Artifacts:** Halts if any active control lacks a defined digital verification log or report.
- **Unmeasurable Roadmap Milestones:** Halts if roadmap milestones are subjective or lack clear target completion dates.
- **Claims Firewall Breach:** Halts if an In Build/Aspirational feature is presented as an active, production compliance control.

---

## 8. Human Approvals
- **Approval Point 1:** Client Risk Committee Lead approves the Gap Assessment and Maturity Targets.
- **Approval Point 2:** Chief Information Security Officer (CISO) and DPO sign off on the RACI assignments and 30-60-90 day roadmap.

---

## 9. Escalation Path
1.  If a Quality Gate fails, the pipeline halts and notifies the **Audit Lead**.
2.  If the client disputes a gap finding or RACI assignment, the issue is escalated to the **VP of Operations** for mediation.
3.  Any Claims Firewall breach is automatically locked and routed to the **Compliance Director** for revision.

---

## 10. Success Metrics
- **Framework Compliance Rate:** Percentage of target clauses successfully satisfied by active controls.
- **Maturity Advancement Rate:** Client progression from L1/L2 to L4 within 90 days.
- **Audit Defensibility Index:** Percentage of controls supported by automated, tamper-proof logs.
- **Claims Firewall Compliance Rate:** 100%.
