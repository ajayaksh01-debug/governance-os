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

### 2.5 Proposal Review Input Validation
Validate a proposal review input payload conforms to schema before execution:
```bash
python evaluations/scripts/workflow_validator.py path/to/proposal_input.json workflows/schemas/proposal-review-input.schema.json
```

### 2.6 Proposal Review Output Validation
Validate a completed proposal review output payload before routing to the Ethana Proposal Agent:
```bash
python evaluations/scripts/workflow_validator.py path/to/proposal_output.json workflows/schemas/proposal-review-output.schema.json
```

### 2.7 Proposal Review Regression Testing
Run all three proposal-review test fixtures against the regression baseline:
```bash
python evaluations/scripts/regression_tester.py evaluations/test-cases/proposal-review/clean-proposal.md evaluations/baselines/ethana-proposal-review-baseline.md
python evaluations/scripts/regression_tester.py evaluations/test-cases/proposal-review/firewall-breach.md evaluations/baselines/ethana-proposal-review-baseline.md
python evaluations/scripts/regression_tester.py evaluations/test-cases/proposal-review/mixed-roadmap-claims.md evaluations/baselines/ethana-proposal-review-baseline.md
```

### 2.8 ISO 42001 Gap Assessment Input Validation
Validate a gap assessment input payload conforms to schema before execution:
```bash
python evaluations/scripts/workflow_validator.py path/to/gap_assessment_input.json workflows/schemas/iso-42001-gap-assessment-input.schema.json
```

### 2.9 ISO 42001 Gap Assessment Output Validation
Validate a completed gap assessment output payload before routing to the Client Assessment Agent:
```bash
python evaluations/scripts/workflow_validator.py path/to/gap_assessment_output.json workflows/schemas/iso-42001-gap-assessment-output.schema.json
```

### 2.10 ISO 42001 Gap Assessment Regression Testing
Run all three gap assessment test fixtures against the regression baseline:
```bash
python evaluations/scripts/regression_tester.py evaluations/test-cases/iso-42001-gap-assessment/bank-certification-readiness.md evaluations/baselines/iso-42001-gap-assessment-baseline.md
python evaluations/scripts/regression_tester.py evaluations/test-cases/iso-42001-gap-assessment/fintech-extension-from-iso27001.md evaluations/baselines/iso-42001-gap-assessment-baseline.md
python evaluations/scripts/regression_tester.py evaluations/test-cases/iso-42001-gap-assessment/greenfield-organisation.md evaluations/baselines/iso-42001-gap-assessment-baseline.md
```

### 2.11 Capability Validation Output Validation
Validate a completed capability validation output payload against schema before routing to downstream skills:
```bash
python evaluations/scripts/workflow_validator.py path/to/capability_validation_output.json workflows/schemas/ethana-capability-validation-output.schema.json
```

### 2.12 Capability Validation Regression Testing
Run all three capability validation test fixtures against the regression baseline:
```bash
python evaluations/scripts/regression_tester.py evaluations/test-cases/ethana-capability-validation/production-capability-request.md evaluations/baselines/ethana-capability-validation-baseline.md
python evaluations/scripts/regression_tester.py evaluations/test-cases/ethana-capability-validation/roadmap-capability-request.md evaluations/baselines/ethana-capability-validation-baseline.md
python evaluations/scripts/regression_tester.py evaluations/test-cases/ethana-capability-validation/mixed-status-capability-request.md evaluations/baselines/ethana-capability-validation-baseline.md
```

### 2.13 Regulatory Watch — Regulatory Mapping Gold Standard Validation
Verify that each regulatory-mapping gold standard output is structurally correct against the regulatory-mapping baseline. Run before declaring any gold standard fit for use as a calibration reference:
```bash
python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/gold-standards/india-dpdp-customer-support-ai-gold-standard.md \
  evaluations/baselines/regulatory-mapping/structure.json

python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/gold-standards/uk-insurance-claims-model-gold-standard.md \
  evaluations/baselines/regulatory-mapping/structure.json
```

### 2.14 Regulatory Watch — GCM Gold Standard Validation
Verify that the governance-control-mapping gold standard (Part B of the EU AI Act fixture) is structurally correct and Claims Firewall compliant:
```bash
python evaluations/scripts/regression_tester.py \
  evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md \
  evaluations/baselines/governance-control-mapping/structure.json

python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md
```

### 2.15 Regulatory Watch — Agent Output Regression Testing
When the Regulatory Watch Agent generates a regulatory-mapping or governance-control-mapping output from one of the regulatory-subjects fixtures, validate the actual output against baselines. Replace `{path-to-output}` with the agent-generated output path:
```bash
# Regulatory Mapping output validation
python evaluations/scripts/regression_tester.py \
  {path-to-regulatory-mapping-output} \
  evaluations/baselines/regulatory-mapping/structure.json

# Governance Control Mapping output validation
python evaluations/scripts/regression_tester.py \
  {path-to-gcm-output} \
  evaluations/baselines/governance-control-mapping/structure.json

# Claims Firewall check on GCM output
python evaluations/scripts/claims_linter.py \
  {path-to-gcm-output}
```

Reference gold standards to calibrate expected content profile for each fixture:
- EU AI Act fixture: `evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md`
- India DPDP fixture: `evaluations/test-cases/gold-standards/india-dpdp-customer-support-ai-gold-standard.md`
- UK Insurance fixture: `evaluations/test-cases/gold-standards/uk-insurance-claims-model-gold-standard.md`

---

## 3. Quality Thresholds & Gates

| Test | Objective | Pass Threshold | Consequence of Failure |
|---|---|---|---|
| **Claims Linter** | Enforce Claims Firewall | 100% compliant (0 violations) | **Hard Fail.** Output rejected; score set to 0. |
| **Workflow Validator** | Schema compliance | 100% compliant (0 validation errors) | **Halt.** Workflow execution blocked. |
| **Regression Tester** | Prevent structural drift | All required sections & tables present; score $\ge$ local threshold | **Reject.** Code modification rejected; commit blocked. |
| **Agent Certifier** | Protect agent execution | Target readiness level achieved (e.g. Level 3/4) | **Block.** Agent execution disabled. |
| **Proposal Review Regression** | Validate CFB detection and Absolute Release Rule | All three fixtures produce correct classification; `firewall-breach` and `mixed-roadmap-claims` (pre-correction) classify as Rejected | **Hard Fail.** Any Rejected fixture scoring non-Rejected is a Claims Firewall bypass. |
| **ISO 42001 Gap Assessment Regression** | Validate AMS/ARS scoring ranges, Certification Classification, and Claims Firewall compliance (Section 8.5) | All three fixtures produce classification within expected range; `greenfield-organisation` must be Major Gaps; no Aspirational/In Build capability cited as Production | **Hard Fail.** Incorrect classification or uncorrected Claims Firewall violation blocks assessment release. |
| **Capability Validation Regression** | Validate ECS computation, CPL assignment accuracy, Phase 9 gate completion, and sub-capability split handling | All three fixtures produce validated_status and ECS within expected ranges; `roadmap-capability-request` must produce ECS = 0 for Production claim; `mixed-status-capability-request` NHI claim must be CPL-5 in Section 5, not Section 4 | **Hard Fail.** Any Production claim for In Build capability in Allowed Claims, or missing Phase 9 gate confirmation, blocks validation release. |
| **Regulatory Mapping Gold Standard Regression** | Verify structural correctness of all three RM gold standards against `regulatory-mapping/structure.json` | All three gold standards pass structural regression; all 9 required headers present; required tables with required columns present in each | **Hard Fail.** A gold standard that fails structural regression is not a valid calibration reference and must not be used as a reviewer benchmark. |
| **GCM Gold Standard Regression + Claims Firewall** | Verify structural correctness of GCM gold standard (Part B of EU AI Act fixture) and Claims Firewall compliance | GCM gold standard passes regression against `governance-control-mapping/structure.json`; all 10 Section headers present; both required tables present; Claims Firewall linter returns 0 violations | **Hard Fail.** GCM gold standard with Claims Firewall violations cannot serve as a calibration reference — it would train reviewers to accept prohibited claims. |
| **Regulatory Watch Agent Output Regression** | When agent generates outputs, verify structure and Claims Firewall compliance before delivery | RM outputs pass regression against `regulatory-mapping/structure.json` (score ≥ 70); GCM outputs pass regression against `governance-control-mapping/structure.json` (score ≥ 85); GCM Claims Firewall linter returns 0 violations | **Hard Fail.** Non-compliant agent outputs must not be presented to human approvers at Approval Gates 1 or 2. |
