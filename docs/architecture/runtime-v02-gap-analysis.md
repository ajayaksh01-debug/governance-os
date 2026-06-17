# Runtime v0.2 Gap Analysis: Moving from Mock to Real Skill Execution

**Date:** 2026-06-18  
**Scope:** Architectural gap analysis for the transition from Regulatory Watch Agent Runtime v0.1 (fixture-driven) to v0.2 (programmatic skill execution).

---

## 1. Audit of Current Runtime v0.1

The current v0.1 runtime is a closed system that uses pre-defined inputs and static gold standards to mock execution stages. It cannot process unseen regulatory subjects dynamically.

The following table lists the locations in [agents/regulatory-watch-agent/runtime/orchestrator.py](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/orchestrator.py) and [state_manager.py](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/state_manager.py) where mocks, canned gold standards, and simulated execution occur:

| Location / Method | Type | Current Mock Behavior |
|---|---|---|
| `Orchestrator._map_to_fixture` (lines 205-216) | Test Fixture Lookup | Substring matches on `jurisdictions`, `subject_description`, and `industry` to force the inputs into one of three test cases: `india-dpdp-customer-support-ai`, `uk-insurance-claims-model`, or `eu-ai-act-high-risk-banking`. |
| `Orchestrator._run_skill_1` (lines 218-264) | Skill 1 Simulation | Loads the mapped gold-standard file from `config.yaml`, extracts `Part A` as static markdown scoping matrix output, and loads the hardcoded JSON from `StateManager.MOCK_REGULATORY_JSON`. |
| `Orchestrator._run_skill_2` (lines 371-412) | Skill 2 Simulation | Loads the mapped gold-standard file, extracts `Part B` as static control specification markdown (or falls back to `_generate_mock_part_b_md`), and loads the hardcoded JSON from `StateManager.MOCK_CONTROL_JSON`. |
| `Orchestrator._generate_mock_part_b_md` (lines 691-730) | Static Output Generation | Returns a static markdown template for control specs with a hardcoded score of `88/100`. |
| `StateManager.MOCK_REGULATORY_JSON` (lines 734-879) | Canned Obligations | Holds static, pre-defined compliance obligation and regulatory classification JSONs for the three test fixtures. |
| `StateManager.MOCK_CONTROL_JSON` (lines 881-957) | Canned Controls | Holds static, pre-defined operational control specification JSONs for the test fixtures. |
| `Orchestrator.submit_approval_2` modifications validation (lines 524-575) | Mock Re-gating | Validates modifications by re-linting the original pre-existing markdown and checking the pre-existing JSON, completely bypassing the actual modification notes content. |

---

## 2. Gaps and Phase-by-Phase Plan to v0.2

To transition the runtime to v0.2, the mock dependencies must be replaced with programmatic logic that parses incoming subject descriptions and dynamically generates assessments.

### Phase 1 — Regulatory Mapping Execution
*   **Gap**: No execution module exists to parse subject text and jurisdictions to produce regulatory scoping outputs.
*   **Remediation**: Create [skill_executor.py](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/skill_executor.py) containing a rule-based engine. This engine will:
    1.  Parse target jurisdictions, AI technologies (LLMs vs. ML Classifiers), and industries (BFSI vs. General Enterprise) from inputs.
    2.  Apply decision trees (from `skills/regulatory-mapping/workflow.md`) to dynamically identify applicable regulations (GDPR, EU AI Act, DPDP Act, Equality Act, FCA, RBI).
    3.  Generate specific obligations, frameworks (ISO 42001, NIST AI RMF, and context-dependent OWASP LLM Top 10), and risk classifications.
    4.  Produce a structured dictionary conforming to the output schema.

### Phase 2 — Governance Control Mapping Execution
*   **Gap**: Downstream control specifications are loaded from hardcoded mock objects.
*   **Remediation**: Add a control-mapping generator in `skill_executor.py`. This module will:
    1.  Ingest the structured control requirements from the Skill 1 output object.
    2.  For each requirement, map and design preventive, detective, and corrective controls.
    3.  Assign RACI owners and define telemetry metrics and collection methods for evidence.
    4.  Construct the control taxonomy matrix and output a structured control specification object conforming to the schema.

### Phase 3 — Structured Contracts
*   **Gap**: Runtime v0.1 passes unstructured markdown text between stages and performs regex parsing of Markdown sections.
*   **Remediation**:
    1.  Create a `contracts` directory under [runtime/contracts/](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/contracts/).
    2.  Define the formal JSON schemas: `regulatory_mapping_output.json` and `governance_control_output.json`.
    3.  Eliminate markdown parsing between Skill 1 and Skill 2. The pipeline will pass only structured data objects, compiling markdown output only for the final handoff packaging.

### Phase 4 — Validation
*   **Gap**: The linter currently runs only on Markdown files.
*   **Remediation**:
    1.  Enforce structured schema checks at each step: validate trigger inputs, Skill 1 outputs, and Skill 2 outputs against their schemas.
    2.  Compile the structured JSON outputs to temporary markdown documents to execute the `claims_linter.py` Firewall checks at both stages.
    3.  Halt execution, transition the run to `HALTED_FIREWALL_BREACH`, and log audit events if any linter breach occurs.
