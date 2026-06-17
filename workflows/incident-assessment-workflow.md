# Workflow: Incident Assessment

## 1. Purpose
The **Incident Assessment Workflow** is designed to rapidly triage an observed AI system failure or security exploit, isolate its underlying root causes, design operational containment and remediation controls, and validate the platform capability statuses of the proposed defenses.

---

## 2. Trigger
- **Automated Trigger:** Alert from a logging/SIEM connector (e.g., Datadog or Splunk) indicating repeated blocked injections, exfiltration anomalies, or agent execution failures.
- **Manual Trigger:** An internal incident report logged by the SOC, a customer support ticket alleging unexpected AI behavior, or a public security research disclosure.

---

## 3. Inputs
- `incident_description` (Required): Raw text report or article describing the event.
- `incident_type` (Required): One of: `AI Security Incident`, `Agent Failure`, `Model Failure`, `Data Incident`, `Governance Event`, `Bias/Fairness Incident`.
- `affected_system` (Optional): ID or description of the AI model/application.
- `client_context` (Optional): Vertical sector and deployment configuration.
- `target_maturity_level` (Optional): Defaults to `L3: Defined`.

---

## 4. Skill Sequence

```
[Raw Incident Input]
         │
         ▼
 1. ai-incident-analysis (Triage & Root Cause)
         │
         ▼ (Section 4 & 9 payload)
 2. governance-control-mapping (Remediation Design)
         │
         ▼ (Section 10 platform configurations)
 3. ethana-capability-validation (Truth Gate Validator)
         │
         ▼
[Incident Remediation Package]
```

### Step 4.1: Root Cause & Triage
- **Skill Engaged:** [ai-incident-analysis](file:///Users/ajayrajsingh/Documents/governance-os/skills/ai-incident-analysis/)
- **Process:** Ingest the raw description. Map the incident against the Cursory risk taxonomy (e.g., prompt injection, excessive agency) and perform a 5-Whys analysis to isolate the technical or governance root cause. Identify which existing controls failed.

### Step 4.2: Control Design & Operationalization
- **Skill Engaged:** [governance-control-mapping](file:///Users/ajayrajsingh/Documents/governance-os/skills/governance-control-mapping/)
- **Process:** Ingest Section 4 (Control Failures) and Section 9 (Recommended Controls) from the previous step. Design specific preventive (blocking), detective (monitoring), and corrective (rollback/isolation) controls. Map them across the Cursory/Ethana coverage classification.

### Step 4.3: Platform Validation (Truth Gate)
- **Skill Engaged:** [ethana-capability-validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/)
- **Process:** Extract all platform-dependent controls from Section 10 of the previous step. Query the Truth Gate (`comp.truth_gate`) against [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md). Verify that no In Build or Aspirational capabilities are committed as active defenses without mandatory manual workarounds.

---

## 5. Outputs
- **Incident Triage Report:** Standardized summary, 5-Whys root cause, and failed control registry.
- **Operational Remediation Plan:** Detailed specifications for preventive, detective, and corrective controls, along with RACI assignments.
- **Verification Binder:** Evidence logs registry and checklist to prove control operational effectiveness.
- **Ethana Configuration Guide:** Validated platform parameters and manual workarounds for roadmap dependencies.

---

## 6. Quality Gates
- **Incident Analysis Gate:** Incident triage score must be $\ge 70/100$. Root cause must be traced to a systemic technical or governance vulnerability.
- **Control Mapping Gate:** Control specification score must be $\ge 85/100$, containing explicit logging schemas, alert thresholds, and containment runbooks.
- **Claims Firewall Gate:** 100% compliance with `canonical-product-model.md`. Zero unreleased capabilities committed as active production defenses.

---

## 7. Failure Conditions
- **Vague Root Cause:** Halts if the analysis fails to establish a clear proximate and systemic root cause.
- **Firewall Breach:** Halts immediately if an In Build capability is mapped as a Production control without an accompanying manual workaround.
- **RACI Blanks:** Halts if any designed control lacks a designated Accountable (A) role.

---

## 8. Human Approvals
- **Approval Point 1:** CISO approves the Triage and Root Cause report.
- **Approval Point 2:** DPO and IT Operations Director approve the RACI ownership and evidence logging configurations before deployment.

---

## 9. Escalation Path
1.  If a Quality Gate fails, the pipeline halts and sends a notification to the **Incident Coordinator**.
2.  If the team disputes the root cause or capability status, the issue is escalated to the **Risk Review Board** for formal adjudication.
3.  If a Claims Firewall breach is flagged, the output is automatically locked and routed to the **Compliance Lead** for mandatory remediation.

---

## 10. Success Metrics
- **Mean Time to Triage (MTTT):** Target under 2 hours.
- **Mean Time to Remediate (MTTR):** Target under 24 hours.
- **Claims Firewall Compliance Rate:** 100%.
- **Evidence Verification Rate:** 100% of controls pass audit validation.
