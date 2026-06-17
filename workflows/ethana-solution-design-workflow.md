# Workflow: Ethana Solution Design

## 1. Purpose
The **Ethana Solution Design Workflow** translates a list of customer requirements or discovery findings into a technically validated, proposal-ready platform solution. It verifies specific capability claims, maps requirements to platform features, assesses coverage confidence, and designs the proof-of-concept (POC) sandbox scope.

---

## 2. Trigger
- **RFP/RFI Receipt:** The sales team receives a customer Request for Proposal or Request for Information.
- **Discovery Complete:** An account executive logs discovery call notes containing specific customer technical requirements.
- **POC Scoping Request:** A sales engineer initiates a scoping request for a customer sandbox evaluation.

---

## 3. Inputs
- `requirement_list` (Required): Customer governance, compliance, or technical requirements.
- `deployment_constraint` (Required): One of: `Cloud SaaS`, `Customer VPC`, `On-premises`, `Air-gapped`.
- `customer_sector` (Optional): Sector vertical (triggers compliance constraints).
- `existing_subscription` (Optional): `Build`, `Edge`, `Bundle`, or `None`.
- `competitive_context` (Optional): Competitors evaluated by the customer.

---

## 4. Skill Sequence

```
[Customer Requirements & Context]
                │
                ▼
  1. ethana-capability-validation (Truth Gate Validator)
                │
                ▼ (Validated statuses payload)
  2. ethana-solution-mapping (Commercial Solution Mapping)
                │
                ▼ (Proposal capabilities payload)
  3. ethana-feature-mapping (Technical Fit Scoping)
                │
                ▼
  [Validated Solution Design Package]
```

### Step 4.1: Capability Validation (Truth Gate)
- **Skill Engaged:** [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/)
- **Process:** Ingest the customer requirement list. Query the Truth Gate (`comp.truth_gate`) against [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) to confirm status (Production vs. In Build vs. Aspirational) for each requested feature.

### Step 4.2: Commercial Solution Mapping
- **Skill Engaged:** [ethana-solution-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/)
- **Process:** Ingest validated capability statuses. Map requirements to platform features, assign Coverage Confidence Scores (CCS), draft proposal-safe language, and recommend the commercial motion (Advisory-First vs. Platform-Primary).

### Step 4.3: Technical Fit Scoping
- **Skill Engaged:** [ethana-feature-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-feature-mapping/)
- **Process:** Ingest the proposed platform capabilities. Evaluate technical integration paths, assign Technical Fit Scores (TFS), and design the sandbox POC configuration.

---

## 5. Outputs
- **RFP Response Language:** Proposal-ready, technically validated answers to customer questions.
- **Coverage Confidence Matrix:** Requirement-by-requirement coverage confidence and licensing allocations.
- **Technical POC Scope:** Scoping checklist, APIs tested, and success criteria for the sandbox.
- **Commercial Motion Recommendation:** Guidance on deal structures and Cursory advisory service attachments.

---

## 6. Quality Gates
- **Capability Validation Gate:** 100% of capability claims must achieve a verified status (ECS $\ge 90$ in Capability Validation).
- **Solution Mapping Gate:** Overall Coverage Confidence Score (CCS) must be $\ge 70/100$ before recommending a Platform-Primary motion.
- **Technical Fit Gate:** Technical Fit Score (TFS) must be $\ge 85/100$ for all production deliverables.

---

## 7. Failure Conditions
- **Claims Firewall Breach:** Halts immediately if the solution map or proposal text commits an In Build or Aspirational capability as a current production deliverable.
- **Unfeasible Deployments:** Halts if the deployment constraint (e.g., On-premises) restricts a required control (e.g., gateway SIEM export) without documenting the mandatory Cursory advisory service workaround.

---

## 8. Human Approvals
- **Approval Point 1:** Sales Engineering Lead approves the Technical POC Scope.
- **Approval Point 2:** Sales Director approves the commercial pricing and proposal package.

---

## 9. Escalation Path
1.  If a Quality Gate fails, the pipeline halts and notifies the **Lead Sales Engineer**.
2.  If the sales team requests an exception to propose a roadmap feature, the issue is escalated to the **Product Management Lead** for written confirmation of shipping dates and CISO approval.
3.  Any Claims Firewall breach is automatically blocked and sent back to the **Solution Architect** for revision.

---

## 10. Success Metrics
- **RFP Win Rate:** Target $\ge 45\%$.
- **POC Success Rate:** Sandbox conversions $\ge 80\%$.
- **Claims Compliance Rate:** 100% compliance with canonical product status.
- **Sales Cycle Duration:** Discovery-to-proposal time under 5 business days.
