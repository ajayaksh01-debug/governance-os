# Gap Analysis — Incident Intelligence Agent Runtime v0.1

**Document type:** Gap Analysis / Audit Report  
**Agent:** [Incident Intelligence Agent](file:///Users/ajayrajsingh/Documents/governance-os/agents/incident_intelligence_agent/AGENT.md) (To be created)  
**Objective:** Identify implementation gaps and blockers to L4 certification for the Incident Intelligence Agent.  

---

## 1. Missing Schemas

*   **Intake Trigger Schema:** The repository lacks an input schema to validate the trigger payload. A new schema file `workflows/schemas/incident_assessment_input.schema.json` must be created. It should validate:
    *   `incident_description` (Required, string, minLength 10)
    *   `incident_type` (Required, string, enum: AI Security Incident, Agent Failure, Model Failure, Data Incident, Governance Event, Bias/Fairness Incident)
    *   `affected_system` (Optional, string)
    *   `client_context` (Optional, string)
    *   `target_maturity_level` (Optional, string)
*   **Skill Contract Uniformity:** Ensure the output of Step 1 (`ai-incident-analysis`) cleanly maps to the input expectations of Step 2 (`governance-control-mapping`) and Step 3 (`ethana-capability-validation`).

---

## 2. Missing Baselines

*   **Incident Analysis Markdown Baseline:** While `evaluations/baselines/ai-incident-analysis/structure.json` exists, there is no corresponding human-readable markdown baseline or E2E regression check definitions for the combined Incident Remediation Package.
*   **Handoff Package Verification:** No baseline exists to verify that the final Verification Binder and Ethana Configuration Guide meet structural formatting constraints.

---

## 3. Missing Fixtures (Test Cases)

The entire `evaluations/test-cases/incident-reports/` directory listed in `evaluations/test-cases/readme.md` is **absent**. To run integration testing, we must implement at least three static mock incident files:
1.  **Samsung Source Code Leak (Data Exfiltration / Governance Failure):**
    *   File: `evaluations/test-cases/incident-reports/samsung-leak.json`
2.  **Slack AI Indirect Prompt Injection (AI Security Incident):**
    *   File: `evaluations/test-cases/incident-reports/slack-prompt-injection.json`
3.  **Amazon Bias CV Screening (Bias/Fairness / Model Failure):**
    *   File: `evaluations/test-cases/incident-reports/amazon-bias.json`

---

## 4. Mocked Dependencies & Programmatic Logic Gaps

*   **5 Whys & Risk Taxonomy Classifier:** Since live LLMs are not available in this sandboxed validation environment, the triage logic (finding proximate cause, generating the 5-Whys chain, mapping NIST/ISO clauses) must be programmatically simulated in the skill executor using deterministic rule-based mapping.
*   **Remediation Control Generation:** The control design (preventive/detective/corrective controls) must map dynamically from the identified control failures to maintain high fidelity.
*   **Truth Gate Validation:** The Truth Gate checks must parse the generated controls, extract platform dependencies, and dynamically cross-reference them with [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md).

---

## 5. Blockers to L4 Certification

1.  **Agent Codebase Absence:** The directory `agents/incident_intelligence_agent/` is missing.
2.  **Runtime Components Absence:** No orchestrator, state manager, or executor is defined for Incident Intelligence.
3.  **Certifier Target Level:** In `evaluations/scripts/agent_certifier.py`, the target readiness level for the Incident Intelligence Agent is set to L3, not L4. This must be updated to L4 with all relevant dependencies mapped.
