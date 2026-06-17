# Workflow: Regulatory Compliance

## 1. Purpose
The **Regulatory Compliance Workflow** performs a compliance scoping and controls-design review for a planned or deployed AI system. It identifies applicable laws and frameworks across target jurisdictions, extracts specific compliance obligations, designs operational controls, and maps them to the Ethana platform to evaluate native coverage.

---

## 2. Trigger
- **New Use Case Registration:** A project team registers a new AI use case in the enterprise AI portfolio registry.
- **Jurisdictional Expansion:** An existing AI system is proposed for deployment in a new jurisdiction (e.g., expanding from the UK to the EU or India).
- **Regulatory Change Alert:** The compliance team triggers a review after a major regulatory update (e.g., final enforcement guidelines issued under the EU AI Act or DPDP Act).

---

## 3. Inputs
- `subject_description` (Required): Detailed description of the AI system, its data flows, and its business context.
- `subject_type` (Required): One of: `AI Use Case`, `AI System`, `AI Portfolio`.
- `jurisdictions` (Required): List of target jurisdictions (e.g., `EU`, `UK`, `India`).
- `industry` (Optional): Sector vertical (e.g., `BFSI`, `Healthcare`, `Retail`).
- `data_types` (Optional): Categories of data processed (e.g., personal, biometric, financial).
- `deployment_model` (Optional): `Cloud SaaS`, `VPC`, `On-premises`.

---

## 4. Skill Sequence

```
[AI Subject Input]
         │
         ▼
 1. regulatory-mapping (Obligations & Classifications)
         │
         ▼ (Section 6 payload)
 2. governance-control-mapping (Control Design Specs)
         │
         ▼ (Technical Control specs)
 3. ethana-solution-mapping (Platform Solution Mapping)
         │
         ▼
[Compliance & Coverage Package]
```

### Step 4.1: Regulatory Obligation Mapping
- **Skill Engaged:** [regulatory-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/)
- **Process:** Ingest use case description, jurisdictions, and sector. Scan global regulatory landscapes to identify applicable laws (GDPR, EU AI Act, DPDP Act, FCA, RBI) and governance frameworks (ISO 42001, NIST AI RMF). Assign risk tiers (e.g., EU AI Act High-Risk, DPDP Significant Data Fiduciary).

### Step 4.2: Operational Control Specification
- **Skill Engaged:** [governance-control-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/governance-control-mapping/)
- **Process:** Ingest Section 6 (Control Requirements) from Regulatory Mapping. Design specific technical and process controls to satisfy each legal obligation. Assign RACI and define evidence requirements.

### Step 4.3: Platform Coverage Assessment
- **Skill Engaged:** [ethana-solution-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-solution-mapping/)
- **Process:** Ingest the designed technical controls. Match each control to an Ethana platform capability and generate the Coverage Confidence Score (CCS). Identify commercial motions and flag any roadmap dependencies.

---

## 5. Outputs
- **Regulatory Scoping Matrix:** Jurisdiction-specific applicability, obligations, and risk classifications.
- **Operational Control Specification:** Technical and process controls, RACI owners, and evidence criteria.
- **Ethana Coverage Scorecard:** Overall Coverage Confidence Score (CCS) and mapping of production capabilities.
- **Compliance Documentation Checklist:** Required conformity assessments, risk assessments, and registers.

---

## 6. Quality Gates
- **Regulatory Mapping Gate:** Regulatory mapping score must be $\ge 70/100$. All obligations must cite specific legal provisions.
- **Control Design Gate:** Control specification score must be $\ge 85/100$, with no orphan controls.
- **Claims Firewall Gate:** Hard-fail check. 100% compliance with `canonical-product-model.md`.

---

## 7. Failure Conditions
- **Missing Regulatory Citations:** Halts if obligations are listed without specific legal articles or regulatory guidelines.
- **Firewall Breach:** Halts if the Solution Mapping scorecard references unreleased or Aspirational features as active production deliverables.
- **Maturity Gap:** Halts if the designed controls cannot meet the target maturity level within the client's timeline.

---

## 8. Human Approvals
- **Approval Point 1:** General Counsel signs off on the Regulatory Scoping Matrix.
- **Approval Point 2:** DPO and Information Security Lead approve the Operational Control Specification and RACI roles.

---

## 9. Escalation Path
1.  If a Quality Gate fails, the pipeline halts and notifies the **Compliance Analyst**.
2.  If legal counsel disputes the risk classification (e.g., whether a model falls under Annex III High-Risk), the issue is escalated to the **Chief Compliance Officer** for formal sign-off.
3.  Any Claims Firewall breach is automatically routed to the **Sales Operations Lead** for proposal revision.

---

## 10. Success Metrics
- **Compliance Coverage Rate:** 100% of applicable regulatory obligations mapped to active controls.
- **Platform Coverage Accuracy:** 100% correlation between proposed Ethana capabilities and canonical status.
- **Audit Readiness Index:** 100% of designed controls have verified evidence collection mechanisms.
