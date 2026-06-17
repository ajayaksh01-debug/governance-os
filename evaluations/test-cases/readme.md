# Evaluations — Test Cases Database

This directory serves as the database of static test payloads used for cross-skill regression testing, schema validation, and claims firewall linting.

## 1. Directory Structure

- **`incident-reports/`**: Mock incident logs, security advisories, and agent failure descriptions.
- **`regulatory-subjects/`**: Mock AI use cases and system descriptions across various industry verticals (BFSI, Healthcare, General Enterprise).
- **`gold-standards/`**: Baseline output documents that have been verified by human experts, used by `regression_tester.py` to match structural layouts, headers, and required tables.

## 2. Test Execution
Test payloads are loaded by the automated test scripts located under `evaluations/scripts/`. 

To run a test suite, configure the baseline in `evaluations/evaluation-index.md` and execute the runner.
