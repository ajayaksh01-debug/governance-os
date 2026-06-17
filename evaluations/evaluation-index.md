# Evaluation Layer Index

## Overview

This directory contains the central evaluation framework for the Governance OS. It provides automated scripts and baseline configurations to validate skill outputs, check workflow schemas, enforce the commercial **Claims Firewall**, and certify agent readiness.

---

## 1. Directory Structure

- **[baselines/](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/baselines/)**: Skill-specific structural baselines for regression testing.
- **[test-cases/](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/test-cases/)**: Database of mock input payloads (incident reports, client RFPs, use cases).
- **[scripts/](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/scripts/)**: Automated testing scripts:
  - `claims_linter.py` (Claims Firewall compliance check)
  - `workflow_validator.py` (JSON schema check for payloads)
  - `regression_tester.py` (Structural markdown conformance check)
  - `agent_certifier.py` (Agent readiness certification)
  - `scorecard_compiler.py` (Phase 2 Priority: scorecard compiler)
- **[scorecards/](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/scorecards/)**: Run log records and compiled scorecards.

---

## 2. Test Execution Commands

To run evaluations locally during development, run the following Python scripts from the repository root:

### 2.1 Claims Firewall Linting
Run the linter on any draft markdown output to ensure no unreleased capabilities are committed as production features:
```bash
python evaluations/scripts/claims_linter.py path/to/draft_output.md
```

### 2.2 Workflow Payload Conformance Check
Validate that an inter-skill payload matches its structural schema before routing:
```bash
python evaluations/scripts/workflow_validator.py path/to/payload.json workflows/schemas/control_mapping_output.json
```

### 2.3 Structural Regression Testing
Verify that edits to database files or markdown structures have not broken structural requirements (headings, tables, column headers):
```bash
python evaluations/scripts/regression_tester.py skills/governance-control-mapping/examples.md evaluations/baselines/governance-control-mapping/structure.json
```

### 2.4 Agent Readiness Certification
Verify the readiness level of all candidate agents:
```bash
python evaluations/scripts/agent_certifier.py
```

---

## 3. Quality Thresholds & Gates

| Test | Objective | Pass Threshold | Consequence of Failure |
|---|---|---|---|
| **Claims Linter** | Enforce Claims Firewall | 100% compliant (0 violations) | **Hard Fail.** Output rejected; score set to 0. |
| **Workflow Validator** | Schema compliance | 100% compliant (0 validation errors) | **Halt.** Workflow execution blocked. |
| **Regression Tester** | Prevent structural drift | All required sections & tables present; score $\ge$ local threshold | **Reject.** Code modification rejected; commit blocked. |
| **Agent Certifier** | Protect agent execution | Target readiness level achieved (e.g. Level 3/4) | **Block.** Agent execution disabled. |
