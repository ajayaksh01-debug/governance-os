# Workflow: Governance Assessment

## 1. Purpose
The **Governance Assessment Workflow** delivers a comprehensive baseline audit of a client's AI governance program against industry standards (ISO 42001, NIST AI RMF). It identifies compliance gaps, designs target controls, establishes a maturity roadmap, validates current platform integration claims, and produces a final Executive Assessment Package for executive sign-off.

---

## 2. Trigger
- **New Client Onboarding:** A new client onboarding process is initiated.
- **Annual Governance Audit:** Triggered by a recurring compliance calendar milestone.
- **Certification Readiness Check:** The client requests a certification audit mock run before submitting to an external registrar.

---

## 3. Inputs
- `client_name` (Required): Client organisation name.
- `industry` (Required): Client industry sector (e.g., Financial Services, Healthcare).
- `jurisdictions` (Required): List of regulatory jurisdictions (e.g., `["EU", "UK"]`).
- `regulatory_frameworks` (Required): Target frameworks (e.g., `["EU AI Act", "ISO 42001"]`).
- `use_case_description` (Required): Description of the client's AI use cases and governance requirements.
- `client_ai_portfolio` (Optional): Inventory of deployed models, use cases, and technical details.
- `existing_policies` (Optional): Current AI guidelines, risk registers, and control evidence.

---

## 4. Skill Sequence

The Client Assessment Agent executes a 6-skill chain plus one embedded feature-mapping step (Skill FM). Skills 1 and 2 are routed via the Regulatory Watch Agent (RWA); Skills 5 and 6 are routed via the Capability Validation Agent (CVA) and Ethana Proposal Agent (EPA) respectively. Skills 3, 4, and FM execute locally.

```
[Client Intake]
       │
       ▼
   Skill 1 — regulatory-mapping           (via RWA)
       │ Regulatory Scoping Matrix
       │
  Gate 1: schema ✓, score ≥70, Claims Firewall
  AG-1:   General Counsel approval
       │
       ▼
   Skill 2 — governance-control-mapping   (via RWA)
       │ Operational Control Specification
       │
  Gate 2: schema ✓, Claims Firewall, score ✓
       │
       ▼
   Skill 3 — ethana-solution-mapping      (local)
       │ Platform Coverage Map + matched_capabilities
       │
  Gate 3: schema ✓, Claims Firewall, score ✓
  AG-2:   CSM / Commercial Director approval
       │
       ▼
   Skill 4 — iso-42001-gap-assessment     (local)
       │ AMS / ARS / Gap Register
       │
  Gate 4: schema ✓, Claims Firewall, score ✓
       │
       ▼
   Skill 5 — ethana-capability-validation (via CVA) — Truth Gate
       │ Capability Validation Report + ECS
       │
  Gate 5: schema ✓, Claims Firewall, ECS ≥90
  AG-3:   Delivery Director / Compliance Officer approval
       │
       ▼
   Skill FM — ethana-feature-mapping      (local)
       │ Feature Validation Table + TFS
       │
  Gate FM: schema ✓, Claims Firewall
       │
       ▼
   Skill 6 — ethana-proposal-review       (via EPA) — Release Gate
       │ Executive Assessment Package
       │
  Gate 6: schema ✓, Claims Firewall, release classification
  AG-4:   Client Executive / Account Director approval
       │
       ▼
   [COMPLETE — 12-artifact Executive Assessment Package]
```

---

## 5. Step Details

### Step 4.1 — Regulatory Scoping (Skill 1)
**Skill:** [regulatory-mapping](../skills/regulatory-mapping/)
**Runtime:** Regulatory Watch Agent (RWA)
**Process:** Ingest the client's AI portfolio, policies, industry, and jurisdictions. Map them against target framework clauses (EU AI Act, ISO 42001, NIST AI RMF, DPDP, etc.) to establish applicability boundaries and produce a Regulatory Scoping Matrix. Gate 1 validates the output schema, confirms a regulatory mapping score ≥70, and runs the Claims Firewall before routing to AG-1 (General Counsel) for approval.

### Step 4.2 — Control Specification (Skill 2)
**Skill:** [governance-control-mapping](../skills/governance-control-mapping/)
**Runtime:** Regulatory Watch Agent (RWA)
**Process:** Ingest the Regulatory Scoping Matrix from Skill 1. Design target technical and process controls, construct the RACI ownership matrix, and produce an Operational Control Specification with a control taxonomy matrix. Gate 2 validates schema, runs the Claims Firewall, and confirms the control mapping score before proceeding. Note: GCM precedes ISO 42001 gap assessment to supply `control_mapping_output` as a required input.

### Step 4.3 — Platform Coverage (Skill 3)
**Skill:** [ethana-solution-mapping](../skills/ethana-solution-mapping/)
**Runtime:** Client Assessment Agent (local executor)
**Process:** Map client regulatory requirements to Ethana's Canonical Product Model capabilities. Produce a `matched_capabilities` list recording each capability name, status (Production / In Build / Aspirational), and Coverage Confidence Score (CCS). The `matched_capabilities` list is the input source for Skill 5 (capability validation). Gate 3 validates schema and runs the Claims Firewall before routing to AG-2 (CSM / Commercial Director) for approval.

### Step 4.4 — ISO 42001 Gap Assessment (Skill 4)
**Skill:** [iso-42001-gap-assessment](../skills/iso-42001-gap-assessment/)
**Runtime:** Client Assessment Agent (local executor)
**Process:** Run a clause-by-clause and Annex A compliance audit against current client evidence. Output AMS (AI Management System maturity score), ARS (AI Risk Score), Certification Classification, and a structured gap register (Critical / Major / Minor). The ISO output is required by Skill 6 and the Governance Review Agent. Gate 4 validates schema and runs the Claims Firewall.

### Step 4.5 — Capability Validation / Truth Gate (Skill 5)
**Skill:** [ethana-capability-validation](../skills/ethana-capability-validation/)
**Runtime:** Capability Validation Agent (CVA)
**Process:** Validate each Ethana capability identified in Skill 3 against `canonical-product-model.md` using the CVA executor. Produce an Evidence Confidence Score (ECS, 0–100) and a Capability Validation Report classifying each capability as Production, In Build, or Aspirational. Gate 5 validates schema, runs the Claims Firewall (Gate 5b), and enforces ECS ≥90 (Gate 5c — Truth Gate threshold). Only Production capabilities with ECS ≥90 clear Gate 5c. In Build and Aspirational capabilities produce `escalation_required: true` and generate prohibited-claim documentation for the assessment package. AG-3 (Delivery Director / Compliance Officer) approves before Skill FM runs.

### Step 4.FM — Feature Mapping (Skill FM)
**Skill:** [ethana-feature-mapping](../skills/ethana-feature-mapping/)
**Runtime:** Client Assessment Agent (local executor)
**Process:** Map the validated capabilities to specific client feature requirements. Compute a Technical Fit Score (TFS) and produce a Feature Validation Table. Gate FM validates schema and runs the Claims Firewall.

### Step 4.6 — Executive Assessment Package (Skill 6)
**Skill:** [ethana-proposal-review](../skills/ethana-proposal-review/)
**Runtime:** Ethana Proposal Agent (EPA)
**Process:** Assemble the Executive Assessment Package from all upstream skill outputs (Regulatory Scoping Matrix, Control Specification, Platform Coverage Map, ISO Gap Assessment, Capability Validation Report, Feature Validation Table). The EPA executor scores the package (CTCS — Commercial Technical Completeness Score), runs the Claims Firewall, assigns a Release Classification (Approved for Delivery / Approved with Caveats / Not Approved), and produces the final proposal-review markdown. Gate 6 validates schema and confirms the release classification before routing to AG-4 (Client Executive / Account Director) for final approval. On approval, the 12-artifact package is assembled at `COMPLETE`.

---

## 6. Outputs
- **Regulatory Scoping Matrix:** Framework applicability boundaries and confirmed regulations.
- **Operational Control Specification:** Target controls, RACI matrix, and control taxonomy.
- **Platform Coverage Map:** Ethana capability-to-requirement mapping with CCS scores.
- **ISO 42001 Gap Assessment:** AMS/ARS/classification and structured gap register.
- **Capability Validation Report:** ECS scores, allowed claims, prohibited claims per capability.
- **Feature Validation Table:** Feature-to-capability mapping with TFS scores.
- **Executive Assessment Package:** Full governance assessment deliverable with Release Classification.
- **Client Scorecard:** Aggregated governance maturity indicators (wired in PR-011).

---

## 7. Quality Gates

| Gate | Description | Threshold |
|---|---|---|
| Gate 1a | Regulatory Mapping schema validation | Schema pass |
| Gate 1b | Regulatory Mapping score | ≥70 / 100 |
| Gate 2b | Control Mapping schema validation | Schema pass |
| Gate 2c | Control Mapping Claims Firewall | Zero breaches |
| Gate 2d | Control Mapping score | Pass |
| Gate 3a | Solution Mapping schema validation | Schema pass |
| Gate 3b | Solution Mapping Claims Firewall | Zero breaches |
| Gate 3c | Solution Mapping quality score | Pass |
| Gate 4a | ISO Gap Assessment schema validation | Schema pass |
| Gate 4b | ISO Gap Assessment Claims Firewall | Zero breaches |
| Gate 5a | Capability Validation schema validation | Schema pass |
| Gate 5b | Capability Validation Claims Firewall | Zero breaches |
| Gate 5c | Capability Validation ECS — Truth Gate | ECS ≥90 / 100 |
| Gate FM | Feature Mapping schema + Claims Firewall | Schema pass + zero breaches |
| Gate 6a | Proposal Review schema validation | Schema pass |
| Gate 6b | Proposal Review Claims Firewall | Zero breaches |
| Gate 6c | Release Classification | Not "Not Approved" |

**Claims Firewall Gate:** 100% compliance with `canonical-product-model.md`. Zero unreleased features claimed as production compliance evidence across all six skills.

---

## 8. Approval Gates

| Gate | Approver | Trigger |
|---|---|---|
| AG-1 | General Counsel | After Skill 1 passes Gate 1 |
| AG-2 | CSM / Commercial Director | After Skill 3 passes Gate 3 |
| AG-3 | Delivery Director / Compliance Officer | After Skill 5 passes Gate 5 |
| AG-4 | Client Executive / Account Director | After Skill 6 passes Gate 6 |

---

## 9. Failure Conditions
- **Schema validation failure:** Halts the run at the corresponding gate state (e.g., `HALTED_GATE_1_SCHEMA`).
- **Claims Firewall breach:** Halts at the corresponding Firewall gate state (e.g., `HALTED_FIREWALL_BREACH`). Any In Build or Aspirational capability claimed as current production compliance evidence triggers a halt.
- **Score below threshold:** Halts at the corresponding score gate state (e.g., `HALTED_GATE_5_SCORE_INSUFFICIENT`). ECS below 90 at Gate 5c halts until Phase B ECS recalibration (ADR-009) is implemented.
- **Approval rejected:** Halts at `HALTED_AG_X_REJECTED`. A re-gate path is available for modifications within the same run.

---

## 10. Escalation Path
1. If a Quality Gate fails, the pipeline halts and the Audit Lead is notified.
2. If the client disputes a gap finding or RACI assignment, the issue is escalated to the VP of Operations.
3. Any Claims Firewall breach is locked and routed to the Compliance Director for revision.
4. ECS below Gate 5c threshold escalates to the Capability Validation escalation path; the capability appears in the assessment package as a prohibited-claim item.

---

## 11. Success Metrics
- **Framework Compliance Rate:** Percentage of target clauses successfully satisfied by active controls.
- **Maturity Advancement Rate:** Client progression from L1/L2 to L4 within 90 days.
- **Audit Defensibility Index:** Percentage of controls supported by automated, tamper-proof logs.
- **Claims Firewall Compliance Rate:** 100% across all six skills.
- **ECS Pass Rate:** Percentage of surfaced Production capabilities clearing Gate 5c (ECS ≥90).

---

## 12. Related Documents
- `agents/client-assessment-agent/AGENT.md` — Authoritative specification (supersedes any conflicting workflow detail)
- `agents/client-assessment-agent/state-machine.md` — Full 59-state machine with all transition conditions
- `agents/client-assessment-agent/workflow.yaml` — Machine-readable workflow definition
- `agents/client-assessment-agent/evaluation.md` — Evaluation gates and certifier criteria
- `docs/decisions/ADR-007-skill5-capability-source.md` — Capability source decision for Skill 5
- `docs/decisions/ADR-008-gate5-ecs-calibration.md` — ECS threshold calibration decision
