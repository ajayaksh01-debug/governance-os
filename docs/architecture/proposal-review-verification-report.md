# Proposal Review Agent Runtime — Verification Report

**Date:** 2026-06-18  
**Verification Framework:** Centralized Integration Test Suite  
**Target Script:** [`evaluations/scripts/test_proposal_review_runtime.py`](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/scripts/test_proposal_review_runtime.py)  
**Readiness Verified:** L4 (Certified Production Ready)  

---

## 1. Executive Summary

This report documents the verification of the **Ethana Proposal Agent Runtime v0.1** after replacing the mock fixture matching with the **Dynamic Claim Analysis Engine (PR-001)**. Five distinct scenarios were tested, covering the intake trigger schema, dynamic review execution, score validations (Proposal Compliance Score (PCS) and Claim Traceability Coverage Score (CTCS)), absolute Claims Firewall checks against the canonical product model, and re-gate validation on human modification notes. 

All 6 integration test cases passed successfully using the dynamic analysis logic.

---

## 2. Test Case Adjudication Matrix

| Test Case Name | Final Runtime State | Complete State Reached? | Claims Firewall Breach? | Schema Validation Failure? | Status |
|---|---|---|---|---|---|
| `test_fixture_1_clean_proposal_approved_path` | `COMPLETE` | **Yes** | No | No | **Passed** |
| `test_fixture_2_firewall_breach_halt` | `HALTED_FIREWALL_BREACH` | No | **Yes** | No | **Passed** |
| `test_fixture_3_mixed_roadmap_claims_rejected_path` | `HALTED_FIREWALL_BREACH` | No | **Yes** | No | **Passed** |
| `test_fixture_3_mixed_roadmap_claims_post_correction` | `COMPLETE` | **Yes** | No | No | **Passed** |
| `test_approval_modification_note_firewall_breach` | `HALTED_FIREWALL_BREACH` | No | **Yes** | No | **Passed** |
| `test_tg3_fail_when_feature_mapping_absent` | n/a (executor direct) | No | No | No | **Passed** |

---

## 3. Detailed Test Case Analysis (Dynamic Verification)

### 3.1 `test_fixture_1_clean_proposal_approved_path`
* **Objective:** Verify the successful end-to-end flow of a clean proposal (Indian Private Bank RFP) using production-ready capabilities.
* **Analysis:** The Dynamic Claim Analysis Engine parses 13 claims from the proposal excerpt. All claims (including the SCIM/CI-CD roadmap items in Section 4 and SOC 2 Type II in Section 5) are verified as compliant against the canonical model. No CFBs or MRFs are generated. PCS is 100, and CTCS is 100.0, yielding an "Approved" classification. Sales/Legal sign-off transitions the run to `COMPLETE`.

### 3.2 `test_fixture_2_firewall_breach_halt`
* **Objective:** Verify that proposals with unreleased, uncertified, or unverified capability claims (UK Insurance Pitch Deck) are blocked by the Claims Firewall.
* **Analysis:** The engine dynamically detects 3 unique Critical Firewall Breaches (CFBs):
    1. `Visual Agent Builder` classified as Aspirational (Aspirational as Production breach).
    2. `SOC 2 Type II (certified)` claimed as certified in a non-roadmap slide (Uncertified as Certified breach).
    3. `Customer Reference` unverified deployment claim ("four major UK insurance companies").
    The run is correctly halted at `HALTED_FIREWALL_BREACH` with a PCS of 0 and a "Rejected" classification.

### 3.3 `test_fixture_3_mixed_roadmap_claims_rejected_path`
* **Objective:** Verify that mixed roadmap claims (EU Bank Proposal) are blocked if the In Build capabilities are presented as production capabilities prior to correction.
* **Analysis:** The engine detects 2 unique CFBs: `SCIM Provisioning` and `CI/CD Gate Integration` placed in a Current Capabilities section without roadmap disclaimers. The run is correctly halted at `HALTED_FIREWALL_BREACH` with a PCS of 0.

### 3.4 `test_fixture_3_mixed_roadmap_claims_post_correction`
* **Objective:** Verify that mixed roadmap claims are approved with revisions if they are correctly moved to the Roadmap section.
* **Analysis:** After moving SCIM and CI/CD to Section 4 (Roadmap Capabilities), the CFB count drops to 0. However, the SCIM claim does not contain a "not yet available" disclaimer, triggering a Major Risk Finding (MRF: SCIM roadmap disclosure includes unauthorized delivery commitment). The PCS is dynamically calculated as 95 ($100 - 5$), and CTCS is 80.0. The classification matches "Approved with Revisions".

### 3.5 `test_approval_modification_note_firewall_breach`
* **Objective:** Verify that attempts to insert unreleased capability claims in human sign-off notes are blocked by the Claims Firewall.
* **Analysis:** The initial proposal is clean. During the sign-off step, the approver includes notes referencing `Visual Agent Builder`. The orchestrator intercepts the note, triggers a Claims Firewall breach, and halts the run in `HALTED_FIREWALL_BREACH`.

### 3.6 `test_tg3_fail_when_feature_mapping_absent`
* **Objective:** Verify that the skill executor enforces TG-3 when `feature_mapping_output` is null, independent of the orchestrator's intake schema validation.
* **Analysis:** The intake schema (`proposal-review-input.schema.json`) is the primary guard — it rejects `null` as a type mismatch for a required `object` field, halting at `HALTED_INTAKE_INVALID` before the skill executes. This test exercises the executor's secondary enforcement: when called directly with `feature_mapping_output = None`, the executor correctly sets `traceability_gate_passed = False` and overrides `classification` to `"Rejected"` while leaving `cfb_count = 0`, distinguishing a TG gate failure from a Claims Firewall breach. The clean-proposal fixture is used to confirm that TG-3 Fail overrides an otherwise Approved classification.
