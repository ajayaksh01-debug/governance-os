# Gap Analysis — Ethana Proposal Agent Runtime v0.1

**Document type:** Gap Analysis / Audit Report  
**Agent:** [Ethana Proposal Agent](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/AGENT.md) (To be created)  
**Objective:** Identify implementation gaps and blockers to L4 certification for the Ethana Proposal Agent.

---

## 1. Missing Runtime Components

Currently, the repository lacks the runtime implementation for the **Ethana Proposal Agent**:
*   **Agent Directory:** `agents/ethana_proposal_agent/` does not exist.
*   **Orchestrator (`orchestrator.py`):** Coordinates trigger intake, runs dynamic review parsing, validates gates, and manages transitions.
*   **State Manager (`state_manager.py`):** Handles persistence and validates state transition rules.
*   **Skill Executor (`skill_executor.py`):** Programmatically executes the core Proposal Review logic:
    *   Parses the draft proposal and catalogs claims (Section 2).
    *   Performs a dynamic Claim Traceability Matrix audit (Section 3) and calculates the **Claim Traceability Coverage Score (CTCS)**.
    *   Performs direct Capability Status Validation (Section 4) against [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) to detect Claims Firewall breaches.
    *   Calculates the **Proposal Compliance Score (PCS)**.
    *   Generates a serialized Release Decision and a human-readable review report.
*   **Output Builder (`output_builder.py`):** Assembles final handoff deliverables including the Release Audit Certificate under the packages directory.
*   **Schema Validator (`schema_validator.py`):** Validates input and output payloads.
*   **Audit Logger (`audit_logger.py`):** Structured append-only logging of runtime events.
*   **Configuration (`config.yaml`):** Setting thresholds for gate validation (PCS >= 95, CTCS >= 95).

---

## 2. Missing Schemas

The input and output schemas exist under [workflows/schemas/](file:///Users/ajayrajsingh/Documents/governance-os/workflows/schemas/):
*   `proposal-review-input.schema.json`
*   `proposal-review-output.schema.json`

However, the validator must map the schemas correctly to validate runtime inputs/outputs.

---

## 3. Missing Fixtures (Test Cases)

The core proposal draft text files exist under [evaluations/test-cases/proposal-review/](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/test-cases/proposal-review/):
1.  `clean-proposal.md`
2.  `firewall-breach.md`
3.  `mixed-roadmap-claims.md`

However, integration tests require mock upstream skill outputs (Solution Mapping, Feature Mapping, Capability Validation, Regulatory Mapping, Control Mapping) that match the contents of these proposals to test traceability auditing dynamically. These mock outputs must be programmatically generated or parsed inside the test execution context.

---

## 4. Missing Baselines

The regression baseline [ethana-proposal-review-baseline.md](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/baselines/ethana-proposal-review-baseline.md) is already present. The skill executor must produce outputs matching these expected metrics and score ranges exactly.

---

## 5. Blockers to L4 Certification

1.  **Agent Directory & Runtime Absence:** `/agents/ethana_proposal_agent/runtime/` is not implemented.
2.  **Certifier Target Level:** In `evaluations/scripts/agent_certifier.py`, the target readiness level for the Ethana Proposal Agent is set to L3, not L4. This must be updated to L4 with codebase dependencies verified.
