# Regulatory Watch Runtime v0.2 — Capability Audit Report

**Date:** 2026-06-18  
**Scope:** Functional audit of Regulatory Watch Agent Runtime v0.2 against skill requirements in `regulatory-mapping` and `governance-control-mapping`.

---

## 1. Implemented Requirements from SKILL.md

The [SkillExecutor](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/skill_executor.py#L18) class programmatically operationalizes the majority of the requirements outlined in both `SKILL.md` specifications:

### Upstream (Regulatory Mapping)
*   **Dynamic Intake Processing:** Extracts AI technology descriptors (`LLM` vs. `ML Classifier`) and data types (`Personal`, `Financial`, `Health`) from the use case descriptions.
*   **Applicable Regulations (Section 1):** Scans region-specific triggers dynamically (EU AI Act, GDPR, UK GDPR, FCA PRIN 12, PRA SS1/23, DPDP Act 2023, RBI IT Governance Master Direction).
*   **Governance Frameworks (Section 2):** Maps ISO 42001, NIST AI RMF, and OWASP LLM Top 10 (conditionally activated only for LLMs).
*   **Regulatory Obligations (Section 3):** Generates legal basis citations (such as GDPR Article 35, DPDP Section 6, RBI IT Gov MD) with transition timelines and penalty ranges.
*   **Risk Classification (Section 4):** Resolves risk classifications (High-risk, Limited-risk, Significant Data Fiduciary, Model Risk SS1/23 Tiers).
*   **Control Requirements (Section 6):** Specifies operational controls (Human Oversight, Drift monitoring, Fairness checks, Prompt Filters, Consent Verification) mapped to originating rules.
*   **Executive Summary (Section 9):** Provides high-level summaries highlighting exposure.

### Downstream (Governance Control Mapping)
*   **Structured Interface Passing:** Directly ingests the Stage 1 output JSON into the Stage 2 executor, bypassing markdown text serialization.
*   **Control Taxonomy (Section 2):** Tabulates technical/process preventive, detective, and corrective controls.
*   **Coverage Classification (Section 3):** Maps features to platform integration states (e.g. *Fully Covered by Ethana*, *Partially Covered*, *Third-Party*, *Customer-Owned*).
*   **Operational Specs (Sections 4, 5, & 6):** Generates actionable triggers, enforcement rules, logging sources, containment steps, recovery protocols, and target SLAs.
*   **Evidence Registry (Section 7):** Details automated/manual verification artifacts and retention periods (e.g., GDPR 7-year limits).
*   **RACI Owner Matrix (Section 8):** Maps responsibilities (e.g., AI Platform Engineer, CRO, DPO, Credit Analyst) preventing ownership gaps.

---

## 2. Omitted SKILL.md Requirements

The following requirements remain unaddressed or simplified in the current programmatic v0.2 release:

*   **Contextual Inputs:** Input parameters like `affected_individuals`, `deployment_model`, `client_context` (from `regulatory-mapping`), and `infrastructure_model`, `existing_tooling` (from `governance-control-mapping`) are parsed or accepted in validation but are ignored by the `SkillExecutor` processing logic.
*   **Alternative Source Ingestions:** `upstream_source_type` is assumed to be `Regulatory Mapping`. Alternate ingestion pipelines (e.g. `AI Incident Analysis`, `Ethana Feature Mapping`) are omitted.
*   **AIMS Scope Determination:** ISO 42001 clause mapping does not determine whether a subject officially fits within a certifiable AI Management System (AIMS) boundary.
*   **Phased Deployment Roadmap Details (Section 9):** The 30-60-90 day deployment roadmap remains a static templated statement rather than generating dynamic timelines reflecting the subject's target maturity level.
*   **Detailed Config Guides (Section 10):** The Ethana configuration guide returns template outlines rather than compiling actual execution config files (e.g. gateway policies or agent token parameters) dynamically.

---

## 3. Workflow Execution vs. Heuristic Classification

The [SkillExecutor](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/skill_executor.py#L18) does **not** employ a full cognitive reasoning/analysis workflow (since no LLM or vector database integrations are permitted under runtime constraints).

Instead, it utilizes a **heuristic keyword classification engine** matching use case strings (e.g. searching for `"credit"`, `"bank"`, `"llm"`, `"personal"`, `"user"`) and applying deterministic decision trees to yield structured obligation schemas and specifications. This successfully simulates workflow gates while ensuring strict repeatable performance.

---

## 4. Processing Unseen Jurisdictions

No, a completely unseen jurisdiction **cannot** be processed.
*   [Orchestrator._validate_inputs](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/orchestrator.py#L167) rejects any jurisdiction that is not strictly one of `"EU"`, `"UK"`, or `"India"`, throwing validation errors and halting the pipeline with `HALTED_INTAKE_UNSUPPORTED_JURISDICTION`.
*   [SkillExecutor.execute_regulatory_mapping](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/skill_executor.py#L68) only contains deterministic decision rule blocks for the three supported jurisdictions.

---

## 5. Processing Multi-Jurisdiction Assessments

Yes. If the input payload's `jurisdictions` list contains multiple values (e.g. `["EU", "India"]`), [SkillExecutor](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/skill_executor.py#L18) iterates over each in sequence, dynamically accumulating applicable regulations, obligations, frameworks, and controls into a single unified JSON dataset, which is compiled into a single combined assessment report.

---

## 6. Detecting Conflicting Obligations

No. There is **no conflict detection logic** implemented in the runtime. Obligations and regulatory requirements from different jurisdictions are presented concurrently in the structured outputs but are not evaluated for contradictions, overrides, or redundant specifications.

---

## 7. Tracing Controls to Obligations

Yes. 
*   In Stage 1, [SkillExecutor.execute_regulatory_mapping](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/skill_executor.py#L68) maps every `control_requirement` back to its legal origin using the `source` field.
*   In Stage 2, [SkillExecutor.execute_governance_control_mapping](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/skill_executor.py#L327) iterates over these requirement nodes, mapping each `control_name` directly to operational details in the RACI, preventive/detective lists, and evidence grids. This allows complete lineage tracing from operational controls back to the source regulations.

---

## 8. Remaining Fixture Dependencies

*   **Runtime Pipeline:** There are **zero** active fixture dependencies in the main runtime path. Static markdown templates and canned JSON payloads are bypassed completely.
*   **Dead Code & Metadata:** 
  *   The logging routine in [Orchestrator.start_run](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/orchestrator.py#L134) calls `_map_to_fixture(inputs)` to log a simulated fixture name match for metadata traceability.
  *   The legacy dictionary configurations (`StateManager.MOCK_REGULATORY_JSON` and `StateManager.MOCK_CONTROL_JSON`) still reside as dead code at the bottom of [orchestrator.py](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/orchestrator.py) but are not queried during execution.
  *   The structural regression tests (`regression_tester.py`) compare the structure of dynamically generated markdown output against static structure expectations.

---

## 9. Requirements for Runtime v1.0 Certification

To graduate the runtime from v0.2 to v1.0 (Production-Ready), the following developments are required:

1.  **AI Reasoning Engine Integration:** Replace the heuristic keyword scanning in [SkillExecutor](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/skill_executor.py#L18) with a sandboxed Large Language Model (LLM) or cognitive agent framework to evaluate free-text descriptions.
2.  **Conflict & Overlap Resolution:** Implement conflict detection algorithms to identify and warn when cross-jurisdictional rules overlap or contradict (e.g. data localization rules).
3.  **Dynamic Configuration Generator:** Upgrade Section 10 to emit actual deployment configuration files (e.g., YAML policies, gateway configurations) rather than text guidelines.
4.  **Flexible Ingestion Pipeline:** Equip the engine to digest multiple inputs beyond regulatory maps, such as incident logs.
5.  **Multi-Jurisdictional Expansion:** Add knowledge bases and processing logic for extra territories (e.g., US Federal, State, Canada, GCC regions).
6.  **Enterprise State Persistence:** Replace flat-file JSON state saving with a production-grade relational database with transactions and rollbacks.
