# Claims Firewall Hardening Phase 1 — Remediation Report

**Date:** 2026-06-18  
**Scope:** Remediations for Claims Firewall vulnerabilities, specifically addressing the Approval Modification Bypass, Single-Word Capability Bypass, and Skill 1 Firewall Bypass.

---

## 1. Files Changed

The following files were modified in the codebase to implement the remediations:

1.  **[claims_linter.py](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/scripts/claims_linter.py)**:
    *   Defined `SINGLE_WORD_ALLOWLIST` and `SINGLE_WORD_DENYLIST` constants.
    *   Updated the pre-compilation regex loop to replace the blanket single-word exclusion with a contextual validation engine for allowlisted capability keys.
2.  **[state_manager.py](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/state_manager.py)**:
    *   Updated `VALID_TRANSITIONS` to allow transitioning to `HALTED_FIREWALL_BREACH` from `SKILL_1_COMPLETE` and `APPROVAL_2_PENDING`.
3.  **[orchestrator.py](file:///Users/ajayrajsingh/Documents/governance-os/agents/regulatory-watch-agent/runtime/orchestrator.py)**:
    *   Updated `submit_approval_2` under `"Approve with modifications"` to merge the original markdown and the modification notes prior to running the Claims Firewall linter.
    *   Added `_evaluate_skill_1_firewall` to execute claims linting on the `regulatory-mapping` (Skill 1) output.
    *   Wired the firewall check into `_evaluate_gate_1` immediately upon transitioning to `SKILL_1_COMPLETE` to halt the run if violations are detected.

---

## 2. Tests Executed

To validate the remediations, we developed a regression and unit test suite and executed the following validation tests:

### 2.1 Remediation Test Suite (`test_firewall_hardening.py`)
We created a new test suite under `evaluations/scripts/test_firewall_hardening.py` which executes four test scenarios:
*   `test_single_word_allowlist_matches`: Verifies that `PromptOps`, `FinOps`, `Discovery` (with context), and `MCP` are correctly detected as firewall breaches when asserted as Production.
*   `test_generic_english_words_no_false_positives`: Verifies that generic English words (`discovery`, `evaluation`, `guardrails`) used in general sentences do not trigger false positives.
*   `test_approval_modifications_firewall_breach_blocked`: Verifies that if an approver inserts a roadmap capability (e.g. `Visual Agent Builder`) inside modification notes in `submit_approval_2`, the orchestrator halts execution, transitions the state to `HALTED_FIREWALL_BREACH`, and writes a `BREACH` audit event.
*   `test_skill_1_firewall_check_fails_on_breach`: Verifies that if the Skill 1 markdown output contains a claims breach, the runtime transitions the state to `HALTED_FIREWALL_BREACH` and terminates before schema validation.

**Execution output:**
```bash
python3 evaluations/scripts/test_firewall_hardening.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.007s

OK
[2026-06-17T21:55:44.698153Z] ✅ [SUCCESS] APPROVAL_GATE_2 - Approver (DPO Test Runner) submitted 'Approve with modifications'. Running re-gate validation on modified payload. Notes: Please integrate Visual Agent Builder into production setup.
[2026-06-17T21:55:44.701076Z] ❌ [BREACH] RE_GATE_VAL - Re-gate validation failed: Claims Firewall breach. Run halted.
[2026-06-17T21:55:44.703888Z] ❌ [BREACH] GATE_1_FIREWALL - Claims Firewall breach detected in Skill 1 output: ['Line 2: Hard Rule Violation: Visual Agent Builder is claimed as Production, In Build, or Roadmap. It is Aspirational and absent from engineering briefs.', "Line 2: Firewall Breach: Non-production capability 'Visual Agent Builder' (canonical status: ASPIRATIONAL) is referred to as Production."]. Pipeline halted.
```

### 2.2 Gold Standards Regression Run
Verified that all three existing regulatory-watch gold standards continue to pass theClaims Firewall linter with 0 violations:
```bash
python3 evaluations/scripts/claims_linter.py evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md
# Output: Passed (0 violations detected)

python3 evaluations/scripts/claims_linter.py evaluations/test-cases/gold-standards/india-dpdp-customer-support-ai-gold-standard.md
# Output: Passed (0 violations detected)

python3 evaluations/scripts/claims_linter.py evaluations/test-cases/gold-standards/uk-insurance-claims-model-gold-standard.md
# Output: Passed (0 violations detected)
```

### 2.3 Existing Linter Fixtures Regression Run
Verified that the existing breach fixture correctly detects the expected 13 violations:
```bash
python3 evaluations/scripts/claims_linter.py evaluations/test-cases/proposal-review/firewall-breach.md
# Output: Failed with exit code 1 (13 expected violations detected)
```

---

## 3. Before / After Behavior

### 3.1 Approval Modification Bypass
*   **Before**: When DPO + InfoSec chose `"Approve with modifications"`, the orchestrator persisted the notes in the run database but re-ran the Claims linter only against the original markdown content. Modification notes containing roadmap or aspirational capabilities (e.g. claiming "Visual Agent Builder" or "CI/CD Gate Integration" as production-ready) completely bypassed the linter.
*   **After**: In `submit_approval_2`, original markdown and modification notes are merged. The claims linter scans the merged text. Any detected breach halts execution, transitions the run to `HALTED_FIREWALL_BREACH`, and logs a `BREACH` audit event.

### 3.2 Single-Word Capability Bypass
*   **Before**: Single-word capabilities parsed from the canonical product model were skipped entirely to prevent common English false positives. Aspirational or In Build capabilities like `PromptOps`, `FinOps`, `Discovery`, and `MCP` were completely undetectable, presenting a major false-negative risk.
*   **After**: Replaced the blanket exclusion with an explicit `SINGLE_WORD_ALLOWLIST`. Specific single-word capability names are checked. To preserve protection against common English words (`evaluation`, `discovery`, `guardrails`), a `SINGLE_WORD_DENYLIST` is declared. These words are checked only if they appear within an Ethana-specific context (e.g. preceded by "Ethana", "governed", or followed by "connector", "agent", "engine", "gate", "tool", etc.).

### 3.3 Skill 1 Firewall Bypass
*   **Before**: The Claims Firewall check only ran at Gate 3b (downstream of Skill 2), meaning the `regulatory-mapping` scoping matrix (Skill 1 output) went entirely unverified.
*   **After**: A new gate (`GATE_1_FIREWALL`) is integrated immediately after Skill 1 completion inside `_evaluate_gate_1`. It lint checks the output matrix markdown. Any breach transitions the run to `HALTED_FIREWALL_BREACH` and halts the pipeline immediately.

---

## 4. Remaining Firewall Risks

The following limitations are inherited from the architectural design and require future phases to address:

1.  **Abbreviated Acronyms (e.g. "nhi")**: Acronyms consisting of short letters are in the allowlist but may bypass checks if they appear in text in lowercase and without spaces/hyphens (like the bare term `"nhi"`). The linter checks `"non-human identity"` but short abbreviations remain hard to catch due to standard English overlap (though `"nhi"` is mapped to `"non-human identity (nhi) for agents"`).
2.  **Code Block Exclusions**: Fenced code blocks (` ``` ` or `~~~`) are excluded from linter evaluation. If capability claims are erroneously introduced inside code block examples, the firewall will not detect them.
3.  **Semantic Context Limits**: Line-by-line checks cannot easily resolve multi-line statements. If a non-production capability is mentioned on one line and its workaround is on the next line, an `Ambiguity Warning` is still generated on the first line. Additionally, general English references to competing/unrelated products (e.g., Palo Alto's "AI Firewall" or generic "compliance packages") will trigger false positives.
