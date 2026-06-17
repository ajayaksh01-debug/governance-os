# Workflow: Proposal Development

## 1. Purpose
The **Proposal Development Workflow** orchestrates the end-to-end process from initial client discovery to a finalized, technically validated, and regulatory-compliant proposal package. It aligns client risk exposures and regulatory obligations with operational controls, maps them to verified Ethana capabilities, and audits the final proposal for compliance.

---

## 2. Trigger
- **RFP/Proposal Process Initiated:** Triggered by a sales opportunity reaching the Proposal phase in the CRM system.
- **Strategic Client Engagement:** The executive team requests a custom governance and solution proposal for a major client account.

---

## 3. Inputs
- `customer_use_case` (Required): Core use case description.
- `jurisdictions` (Required): Targeted jurisdictions (e.g., `EU`, `UK`, `India`).
- `deployment_constraint` (Required): `Cloud SaaS`, `VPC`, `On-premises`.
- `client_sector` (Optional): Sector vertical.
- `existing_subscription` (Optional): Current licensing tier.
- `competitive_context` (Optional): Active competitors.

---

## 4. Skill Sequence

```
[Customer Context & Use Case]
              │
              ▼
   1. regulatory-mapping (Obligation Scoping)
              │
              ▼ (Section 6 control needs)
   2. governance-control-mapping (Operational Control Specs)
              │
              ▼ (Technical controls specs)
   3. ethana-solution-mapping (Platform Solution Mapping)
              │
              ▼ (Proposal capabilities payload)
   4. ethana-feature-mapping (Technical Fit & POC Scoping)
              │
              ▼ (Draft proposal documents)
   5. [FUTURE: Proposal Review] (Placeholder Gate)
              │
              ▼
   [Final Approved Proposal Package]
```

### Step 4.1: Regulatory Obligation Scoping
- **Skill Engaged:** [regulatory-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/)
- **Process:** Ingest the customer use case. Identify applicable laws, obligations, risk classifications, and mandatory compliance documentation.

### Step 4.2: Operational Control Mapping
- **Skill Engaged:** [governance-control-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/governance-control-mapping/)
- **Process:** Ingest Section 6 from Regulatory Mapping. Design the operational control specs (preventive, detective, corrective), assign RACI roles, and map the control coverage classifications.

### Step 4.3: Platform Solution Mapping
- **Skill Engaged:** [ethana-solution-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/)
- **Process:** Ingest designed technical controls. Match controls to Ethana platform features, draft proposal-safe responses, assign Coverage Confidence Scores (CCS), and recommend the commercial motion.

### Step 4.4: Technical Fit & POC Scoping
- **Skill Engaged:** [ethana-feature-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-feature-mapping/)
- **Process:** Ingest the proposed capabilities. Validate technical integration paths, calculate Technical Fit Scores (TFS), and design the sandbox POC scope.

### Step 4.5: Proposal Review & Release Classification (Placeholder Integration)
- **Skill Engaged:** **[FUTURE: Proposal Review]**
- **Process:** Ingest the draft proposal package (RFP responses, control designs, and POC scope). Perform a final audit against the Claims Firewall and assign a **Release Classification**:
  - *Approved:* Proposal is fully compliant and ready for release.
  - *Approved with Revisions:* Requires minor adjustments before release.
  - *Conditional Release:* Approved subject to specific contractual caveats (e.g., scale caveats).
  - *Rejected:* Contains material firewall breaches; blocked from release.

---

## 5. Outputs
- **Completed RFP Response Document:** Technically validated, claims-compliant proposal text.
- **Commercial Motion & Pricing Sheet:** Recommended licensing tiers and Cursory service add-ons.
- **Operational Controls RACI:** Transition roadmap and ownership matrix.
- **Technical POC Scope Document:** Sandbox parameters and success criteria.
- **Release Audit Certificate:** Signed report detailing the Proposal Review rating and firewall compliance status.

---

## 6. Quality Gates
- **Compliance Scoping Gate:** Regulatory mapping score must be $\ge 70/100$.
- **Control Design Gate:** Control specification score must be $\ge 85/100$.
- **Coverage Confidence Gate:** Solution mapping score must be $\ge 70/100$.
- **Technical Validation Gate:** Technical fit score must be $\ge 85/100$.
- **Claims Firewall Gate:** 100% compliance with `canonical-product-model.md`. Any violation results in an automatic **Rejected** classification at the Proposal Review gate.

---

## 7. Failure Conditions
- **Claims Firewall Breach:** Halts if any draft section references In Build or Aspirational capabilities as active production features.
- **Technical Infeasibility:** Halts if the TFS falls below 85/100, indicating major integration blockages in the client environment.
- **Advisory Misalignment:** Halts if the overall CCS is low (<70) but the commercial motion fails to attach mandatory Cursory advisory services.

---

## 8. Human Approvals
- **Approval Point 1:** Solution Architecture Director approves the technical POC scope and integration guidelines.
- **Approval Point 2:** Sales Director and Legal Counsel sign off on the commercial proposal terms.

---

## 9. Escalation Path
1.  If a Quality Gate fails, the pipeline halts and notifies the **Proposal Coordinator**.
2.  If the sales team requests an exception to propose an unreleased feature, it is escalated to the **Product Management Lead** and the **CISO** for written sign-off.
3.  Any Claims Firewall breach automatically locks the opportunity in the CRM, notifying the **Compliance Director** for review.

---

## 10. Success Metrics
- **Proposal Win Rate:** Target $\ge 50\%$.
- **Technical Validation Speed:** Intake-to-validated proposal under 5 business days.
- **Claims Firewall Compliance Rate:** 100%.
- **Average Deal Value (ADV) Expansion:** Increase via Cursory service attachments.
