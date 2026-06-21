#!/usr/bin/env python3
"""
Test Suite: Regulatory Watch Agent Runtime — Mode A and Mode B
PR-008: RWA L4 Test Coverage and Certification

34 tests covering:
  Category 1  — Intake validation (5)
  Category 2  — Mode A happy paths: EU BFSI, India DPDP, UK Insurance (3)
  Category 3  — Package file verification (1)
  Category 4  — Gate 1 schema failures: retry pass + double fail (2)
  Category 5  — Gate 2 score bands: Preliminary + Insufficient (2)
  Category 6  — Approval Gate 1: Reject + Timeout (2)
  Category 7  — Gate 3b Claims Firewall via start_run (1)
  Category 8  — Gate 3a schema failures: retry pass + double fail (2)
  Category 9  — Gate 4 score bands: Below Threshold + Insufficient (2)
  Category 10 — Approval Gate 2: Reject + Partial + Timeout (3)
  Category 11 — AG-2 Approve with modifications: clean path to COMPLETE (1)
  Category 12 — Partial package release (2)
  Category 13 — State guard assertions (2)
  Mode B      — Watch mode (6)

NOTE (Gate 1 Firewall gap): The Gate 1 Claims Firewall path cannot be exercised
end-to-end via start_run because SkillExecutor.compile_regulatory_mapping_to_markdown
never produces firewall-violating output. TestSkill1FirewallBypass in
test_firewall_hardening.py covers this via direct _evaluate_gate_1 call. A future
hardening PR should add a simulate_s1_firewall_breach hook to orchestrator.py.

NOTE (V-05 operator confirmation): workflow.yaml V-05 requires human operator
confirmation before Mode B queue processing for Critical severity + ≥3 affected
runs. This gate is not yet enforced in execute_mode_b. When implemented,
test_mode_b_rate_limits_to_3_concurrent_starts_rest_queued must require an
operator confirmation step before asserting STARTED.
"""

import json
import shutil
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]


def _load_rwa_classes():
    import sys as _sys, importlib.util
    _rwa = repo_root / "agents" / "regulatory-watch-agent" / "runtime"
    _rwa_str = str(_rwa)
    if _rwa_str not in _sys.path:
        _sys.path.insert(0, _rwa_str)
    for _k in ("orchestrator", "state_manager", "audit_logger", "schema_validator",
               "output_builder", "skill_executor"):
        _sys.modules.pop(_k, None)
    for _alias, _file in [
        ("_rwa_audit_logger", "audit_logger.py"),
        ("_rwa_state_manager", "state_manager.py"),
        ("_rwa_orchestrator", "orchestrator.py"),
    ]:
        _spec = importlib.util.spec_from_file_location(_alias, _rwa / _file)
        _mod = importlib.util.module_from_spec(_spec)
        _sys.modules[_alias] = _mod
        _spec.loader.exec_module(_mod)
    _m = _sys.modules[__name__]
    _m.Orchestrator = _sys.modules["_rwa_orchestrator"].Orchestrator
    _m.StateManager = _sys.modules["_rwa_state_manager"].StateManager
    _m.AuditLogger = _sys.modules["_rwa_audit_logger"].AuditLogger


# ─────────────────────────────────────────────────────────────
# Base Input Profiles
# ─────────────────────────────────────────────────────────────

_EU_BFSI_INPUTS = {
    "subject_description": (
        "AI-powered credit scoring system using machine learning to assess loan applications "
        "for retail banking customers in the EU and UK. Processes financial history, credit "
        "bureau data, and employment records to predict default probability. Affects individual "
        "consumers applying for personal and mortgage loans."
    ),
    "subject_type": "AI Use Case",
    "jurisdictions": ["EU", "UK"],
    "industry": "BFSI",
    "target_maturity_level": "L4",
    "data_types": ["personal", "financial"],
}

_INDIA_DPDP_INPUTS = {
    "subject_description": (
        "AI customer support chatbot for an NBFC customer service platform in India, processing "
        "customer queries about loan accounts, EMI schedules, and account management. Handles "
        "personal financial data and interacts with individual retail customers across digital channels."
    ),
    "subject_type": "AI Use Case",
    "jurisdictions": ["India"],
    "industry": "BFSI",
    "target_maturity_level": "L3",
    "data_types": ["personal", "financial"],
}

_UK_INSURANCE_INPUTS = {
    "subject_description": (
        "AI claims assessment model for UK general insurance operations, evaluating motor and "
        "property claims using computer vision and NLP to classify damage severity and estimate "
        "repair costs. Processes policyholder data and claims documentation for automated triage."
    ),
    "subject_type": "AI System",
    "jurisdictions": ["UK"],
    "industry": "BFSI",
    "target_maturity_level": "L4",
    "data_types": ["personal", "financial"],
}


# ─────────────────────────────────────────────────────────────
# Mode A Test Class
# ─────────────────────────────────────────────────────────────

class TestRegulatoryWatchRuntimeModeA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _load_rwa_classes()

    def setUp(self):
        config_path = str(repo_root / "agents" / "regulatory-watch-agent" / "runtime" / "config.yaml")
        self.orchestrator = Orchestrator(config_path=config_path)
        self.trace_id = "TR-RW-TEST-8001"
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        state_file = self.orchestrator.runs_dir / f"{self.trace_id}_state.json"
        audit_file = self.orchestrator.logs_dir / f"{self.trace_id}_audit.jsonl"
        package_dir = self.orchestrator.packages_dir / self.trace_id
        if state_file.exists():
            state_file.unlink()
        if audit_file.exists():
            audit_file.unlink()
        if package_dir.exists():
            shutil.rmtree(package_dir)

    def _run_to_approval_2_pending(self, inputs, trigger_type="new_use_case_registration"):
        """Runs start_run and submit_approval_1("Approve"), asserts APPROVAL_2_PENDING."""
        self.orchestrator.start_run(trigger_type, inputs)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_2_PENDING")
        return state

    # ─────────────────────────────────────────────────────────────
    # Category 1: Intake Validation (5 tests)
    # ─────────────────────────────────────────────────────────────

    def test_intake_missing_required_field_halts_intake_invalid(self):
        inputs = dict(_EU_BFSI_INPUTS)
        del inputs["subject_description"]
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_INTAKE_INVALID")

    def test_intake_subject_description_too_short_halts_intake_invalid(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["subject_description"] = "AI credit scoring system."
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_INTAKE_INVALID")

    def test_intake_invalid_subject_type_halts_intake_invalid(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["subject_type"] = "AI Product"
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_INTAKE_INVALID")

    def test_intake_invalid_maturity_level_halts_intake_invalid(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["target_maturity_level"] = "L9"
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_INTAKE_INVALID")

    def test_intake_unsupported_jurisdiction_halts_unsupported_jurisdiction(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["jurisdictions"] = ["US"]
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_INTAKE_UNSUPPORTED_JURISDICTION")

    # ─────────────────────────────────────────────────────────────
    # Category 2: Mode A Happy Paths (3 tests)
    # ─────────────────────────────────────────────────────────────

    def test_eu_bfsi_happy_path_reaches_complete(self):
        self.orchestrator.start_run("new_use_case_registration", _EU_BFSI_INPUTS)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_1_PENDING")

        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_2_PENDING")

        self.orchestrator.submit_approval_2(self.trace_id, "Approve", "DPO Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "COMPLETE")

    def test_india_dpdp_happy_path_reaches_complete(self):
        self.orchestrator.start_run("new_use_case_registration", _INDIA_DPDP_INPUTS)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        self.orchestrator.submit_approval_2(self.trace_id, "Approve", "DPO Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "COMPLETE")

        s1_json = state["intermediate_data"]["regulatory_mapping_output_json"]
        reg_names = [r.get("regulation_name", "") for r in s1_json.get("applicable_regulations", [])]
        has_dpdp = any("DPDP" in r or "Digital Personal Data" in r for r in reg_names)
        self.assertTrue(has_dpdp, f"Expected DPDP regulation in output; got: {reg_names}")

    def test_uk_insurance_trigger3_trigger_type_accepted_reaches_complete(self):
        """regulatory_change_alert trigger type passes intake validation; run reaches COMPLETE.
        Note: the change_summary addendum is added by execute_mode_b, not by start_run directly.
        Mode B-specific addendum behaviour is tested in TestRegulatoryWatchRuntimeModeB."""
        self.orchestrator.start_run("regulatory_change_alert", _UK_INSURANCE_INPUTS)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        self.orchestrator.submit_approval_2(self.trace_id, "Approve", "DPO Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "COMPLETE")

    # ─────────────────────────────────────────────────────────────
    # Category 3: Package File Verification (1 test)
    # ─────────────────────────────────────────────────────────────

    def test_complete_run_package_files_exist(self):
        self.orchestrator.start_run("new_use_case_registration", _EU_BFSI_INPUTS)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        self.orchestrator.submit_approval_2(self.trace_id, "Approve", "DPO Test", None)

        pkg_dir = self.orchestrator.packages_dir / self.trace_id
        self.assertTrue(pkg_dir.exists(), f"Package directory not found: {pkg_dir}")
        self.assertTrue((pkg_dir / "README.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-regulatory-scoping-matrix.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-operational-control-specification.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-regulatory-mapping-payload.json").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-governance-control-mapping-payload.json").exists())

    # ─────────────────────────────────────────────────────────────
    # Category 4: Gate 1 Schema Failures (2 tests)
    # ─────────────────────────────────────────────────────────────

    def test_gate_1_schema_single_fail_retry_passes(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["simulate_gate_1_fail"] = True
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_1_PENDING")

    def test_gate_1_schema_double_fail_halts_gate_1_schema(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["simulate_gate_1_fail"] = True
        inputs["simulate_gate_1_fail_double"] = True
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_GATE_1_SCHEMA")

    # ─────────────────────────────────────────────────────────────
    # Category 5: Gate 2 Score Failures (2 tests)
    # ─────────────────────────────────────────────────────────────

    def test_gate_2_preliminary_band_halts_gate_2_preliminary(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["mock_s1_score"] = 65
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_GATE_2_PRELIMINARY")

    def test_gate_2_insufficient_band_halts_gate_2_insufficient(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["mock_s1_score"] = 40
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_GATE_2_INSUFFICIENT")

    # ─────────────────────────────────────────────────────────────
    # Category 6: Approval Gate 1 Failures (2 tests)
    # ─────────────────────────────────────────────────────────────

    def test_approval_1_reject_halts_approval_1_rejected(self):
        self.orchestrator.start_run("new_use_case_registration", _EU_BFSI_INPUTS)
        self.orchestrator.submit_approval_1(
            self.trace_id, "Reject", "General Counsel Test", "Risk classification insufficient."
        )
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_APPROVAL_1_REJECTED")

    def test_approval_1_timeout_transitions_approval_timed_out(self):
        self.orchestrator.start_run("new_use_case_registration", _EU_BFSI_INPUTS)
        self.orchestrator.submit_approval_1(self.trace_id, "Timeout", "System Scheduler", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_TIMED_OUT")

    # ─────────────────────────────────────────────────────────────
    # Category 7: Gate 3b Claims Firewall — S2 Output (1 test)
    # ─────────────────────────────────────────────────────────────

    def test_gate_3b_firewall_breach_halts_firewall_breach(self):
        """Exercises Gate 3b via full start_run → submit_approval_1 path.
        Complements TestSkill1FirewallBypass in test_firewall_hardening.py which
        tests Gate 1 firewall via direct _evaluate_gate_1 call."""
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["simulate_firewall_breach"] = True
        self.orchestrator.start_run("new_use_case_registration", inputs)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_1_PENDING")

        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_FIREWALL_BREACH")

    # ─────────────────────────────────────────────────────────────
    # Category 8: Gate 3a Schema Failures (2 tests)
    # ─────────────────────────────────────────────────────────────

    def test_gate_3a_schema_single_fail_retry_passes(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["simulate_gate_3a_fail"] = True
        self.orchestrator.start_run("new_use_case_registration", inputs)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_2_PENDING")

    def test_gate_3a_schema_double_fail_halts_gate_3a_schema(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["simulate_gate_3a_fail"] = True
        inputs["simulate_gate_3a_fail_double"] = True
        self.orchestrator.start_run("new_use_case_registration", inputs)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_GATE_3A_SCHEMA")

    # ─────────────────────────────────────────────────────────────
    # Category 9: Gate 4 Score Failures (2 tests)
    # ─────────────────────────────────────────────────────────────

    def test_gate_4_below_threshold_halts_gate_4_below_threshold(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["mock_s2_score"] = 75
        self.orchestrator.start_run("new_use_case_registration", inputs)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_GATE_4_BELOW_THRESHOLD")

    def test_gate_4_insufficient_halts_gate_4_insufficient(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["mock_s2_score"] = 55
        self.orchestrator.start_run("new_use_case_registration", inputs)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_GATE_4_INSUFFICIENT")

    # ─────────────────────────────────────────────────────────────
    # Category 10: Approval Gate 2 Failures (3 tests)
    # ─────────────────────────────────────────────────────────────

    def test_approval_2_reject_halts_approval_2_rejected(self):
        self._run_to_approval_2_pending(_EU_BFSI_INPUTS)
        self.orchestrator.submit_approval_2(
            self.trace_id, "Reject", "DPO Test", "RACI assignments unacceptable."
        )
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_APPROVAL_2_REJECTED")

    def test_approval_2_partial_halts_approval_2_partial(self):
        self._run_to_approval_2_pending(_EU_BFSI_INPUTS)
        self.orchestrator.submit_approval_2(
            self.trace_id, "Partial", "DPO Test", "One approver rejected."
        )
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_APPROVAL_2_PARTIAL")

    def test_approval_2_timeout_transitions_approval_timed_out(self):
        self._run_to_approval_2_pending(_EU_BFSI_INPUTS)
        self.orchestrator.submit_approval_2(self.trace_id, "Timeout", "System Scheduler", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_TIMED_OUT")

    # ─────────────────────────────────────────────────────────────
    # Category 11: AG-2 Modifications — Clean Path (1 test)
    # ─────────────────────────────────────────────────────────────

    def test_approval_2_modifications_clean_reaches_complete(self):
        self._run_to_approval_2_pending(_EU_BFSI_INPUTS)
        self.orchestrator.submit_approval_2(
            self.trace_id,
            "Approve with modifications",
            "DPO Test",
            "Change CTRL-01 Accountable role from Head of Retail Lending to Chief Risk Officer. "
            "No capability changes requested.",
        )
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "COMPLETE")

    # ─────────────────────────────────────────────────────────────
    # Category 12: Partial Package Release (2 tests)
    # ─────────────────────────────────────────────────────────────

    def test_partial_package_release_after_gate_4_fail(self):
        inputs = dict(_EU_BFSI_INPUTS)
        inputs["mock_s2_score"] = 55
        self.orchestrator.start_run("new_use_case_registration", inputs)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_GATE_4_INSUFFICIENT")

        self.orchestrator.release_partial_package(self.trace_id)

        pkg_dir = self.orchestrator.packages_dir / self.trace_id
        self.assertTrue(pkg_dir.exists(), f"Partial package directory not found: {pkg_dir}")
        self.assertTrue((pkg_dir / f"{self.trace_id}-regulatory-scoping-matrix.md").exists())

        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "HALTED_GATE_4_INSUFFICIENT")

    def test_partial_package_release_before_approval_1_approved_raises(self):
        self.orchestrator.start_run("new_use_case_registration", _EU_BFSI_INPUTS)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_1_PENDING")
        with self.assertRaises(ValueError):
            self.orchestrator.release_partial_package(self.trace_id)

    # ─────────────────────────────────────────────────────────────
    # Category 13: State Guard Assertions (2 tests)
    # ─────────────────────────────────────────────────────────────

    def test_submit_approval_1_on_wrong_state_raises(self):
        self._run_to_approval_2_pending(_EU_BFSI_INPUTS)
        with self.assertRaises(ValueError):
            self.orchestrator.submit_approval_1(self.trace_id, "Approve", "General Counsel Test", None)

    def test_submit_approval_2_on_wrong_state_raises(self):
        self.orchestrator.start_run("new_use_case_registration", _EU_BFSI_INPUTS)
        state = StateManager.load_run(str(self.orchestrator.runs_dir), self.trace_id)
        self.assertEqual(state["status"], "APPROVAL_1_PENDING")
        with self.assertRaises(ValueError):
            self.orchestrator.submit_approval_2(self.trace_id, "Approve", "DPO Test", None)


# ─────────────────────────────────────────────────────────────
# Mode B Test Class
# ─────────────────────────────────────────────────────────────

class TestRegulatoryWatchRuntimeModeB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _load_rwa_classes()

    def setUp(self):
        config_path = str(repo_root / "agents" / "regulatory-watch-agent" / "runtime" / "config.yaml")
        self.orchestrator = Orchestrator(config_path=config_path)
        self.pre_created_paths = []
        self.mode_b_results = []

    def tearDown(self):
        for path in self.pre_created_paths:
            if path.exists():
                path.unlink()
        for result in self.mode_b_results:
            tid = result.get("traceability_id")
            if tid:
                state_file = self.orchestrator.runs_dir / f"{tid}_state.json"
                audit_file = self.orchestrator.logs_dir / f"{tid}_audit.jsonl"
                pkg_dir = self.orchestrator.packages_dir / tid
                if state_file.exists():
                    state_file.unlink()
                if audit_file.exists():
                    audit_file.unlink()
                if pkg_dir.exists():
                    shutil.rmtree(pkg_dir)

    def _create_completed_run_state(self, trace_id, jurisdictions, regulations_list, risk_tier, timestamp):
        """
        Creates a pre-built COMPLETE run state file in runs_dir for Mode B testing.

        Naming convention: use TR-RW-PRIOR-NNNN to avoid collision with
        generate_traceability_id() which globs TR-RW-{year}-*.json. Mode B's glob
        TR-RW-*_state.json still finds these files.

        Args:
            trace_id: e.g. "TR-RW-PRIOR-0001"
            jurisdictions: list of jurisdiction strings e.g. ["EU"]
            regulations_list: list of (regulation_name, jurisdiction) tuples
            risk_tier: e.g. "High-risk (Annex III, Point 5)" or "General Enterprise"
            timestamp: ISO8601 string for history[0] e.g. "2026-01-01T10:00:00Z"
        """
        state = {
            "status": "COMPLETE",
            "traceability_id": trace_id,
            "inputs": {
                "jurisdictions": jurisdictions,
                "subject_description": (
                    "AI credit scoring system for BFSI retail lending in the financial services sector. "
                    "Processes personal and financial data for loan application decisions affecting "
                    "individual retail customers."
                ),
                "subject_type": "AI Use Case",
                "target_maturity_level": "L4",
                "industry": "BFSI",
            },
            "intermediate_data": {
                "regulatory_mapping_output_json": {
                    "applicable_regulations": [
                        {"regulation_name": reg_name, "jurisdiction": jur}
                        for reg_name, jur in regulations_list
                    ],
                    "risk_tier": risk_tier,
                    "score": 85,
                }
            },
            "history": [{"timestamp": timestamp}],
        }
        path = self.orchestrator.runs_dir / f"{trace_id}_state.json"
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        self.pre_created_paths.append(path)
        return path

    # ─────────────────────────────────────────────────────────────
    # Mode B Tests (6 tests)
    # ─────────────────────────────────────────────────────────────

    def test_mode_b_finds_matching_runs_and_starts_reassessments(self):
        self._create_completed_run_state(
            "TR-RW-PRIOR-0001", ["EU"], [("EU AI Act", "EU")], "General Enterprise", "2026-01-01T10:00:00Z"
        )
        self._create_completed_run_state(
            "TR-RW-PRIOR-0002", ["EU"], [("EU AI Act", "EU")], "General Enterprise", "2026-01-02T10:00:00Z"
        )
        alert = {
            "regulation_name": "EU AI Act",
            "jurisdiction": "EU",
            "change_summary": "Annex III credit scoring criteria updated.",
            "change_severity": "Major",
        }
        results = self.orchestrator.execute_mode_b(alert)
        self.mode_b_results.extend(results)

        self.assertEqual(len(results), 2)
        prior_ids = {"TR-RW-PRIOR-0001", "TR-RW-PRIOR-0002"}
        for r in results:
            self.assertEqual(r["status"], "STARTED")
            self.assertIsNotNone(r["traceability_id"])
            self.assertIn(r["prior_assessment_id"], prior_ids)

    def test_mode_b_rate_limits_to_3_concurrent_starts_rest_queued(self):
        # NOTE: workflow.yaml V-05 requires operator confirmation before queue processing
        # for Critical severity + ≥3 affected runs. This gate is not yet enforced in
        # execute_mode_b. When implemented, this test must require an operator confirmation
        # step before asserting STARTED.
        for i in range(1, 6):
            self._create_completed_run_state(
                f"TR-RW-PRIOR-{i:04d}",
                ["EU"],
                [("EU AI Act", "EU")],
                "General Enterprise",
                f"2026-01-0{i}T10:00:00Z",
            )
        alert = {
            "regulation_name": "EU AI Act",
            "jurisdiction": "EU",
            "change_summary": "Comprehensive compliance framework update.",
            "change_severity": "Major",
        }
        results = self.orchestrator.execute_mode_b(alert)
        self.mode_b_results.extend(results)

        self.assertEqual(len(results), 5)
        for r in results[:3]:
            self.assertEqual(r["status"], "STARTED")
            self.assertIsNotNone(r["traceability_id"])
        for r in results[3:]:
            self.assertEqual(r["status"], "QUEUED")
            self.assertIsNone(r["traceability_id"])

    def test_mode_b_returns_empty_when_no_matching_runs(self):
        self._create_completed_run_state(
            "TR-RW-PRIOR-0001", ["EU"], [("EU AI Act", "EU")], "General Enterprise", "2026-01-01T10:00:00Z"
        )
        self._create_completed_run_state(
            "TR-RW-PRIOR-0002", ["EU"], [("EU AI Act", "EU")], "General Enterprise", "2026-01-02T10:00:00Z"
        )
        alert = {
            "regulation_name": "UK GDPR",
            "jurisdiction": "UK",
            "change_summary": "Data transfer rules updated.",
            "change_severity": "Minor",
        }
        results = self.orchestrator.execute_mode_b(alert)
        self.assertEqual(results, [])

    def test_mode_b_missing_required_field_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.orchestrator.execute_mode_b({
                "jurisdiction": "EU",
                "change_summary": "Missing regulation_name field.",
                "change_severity": "Minor",
            })

    def test_mode_b_includes_change_summary_in_reassessment_subject(self):
        prior_trace_id = "TR-RW-PRIOR-0001"
        self._create_completed_run_state(
            prior_trace_id, ["EU"], [("EU AI Act", "EU")], "General Enterprise", "2026-01-01T10:00:00Z"
        )
        change_summary = "New Article 10 data governance requirements for high-risk AI."
        alert = {
            "regulation_name": "EU AI Act",
            "jurisdiction": "EU",
            "change_summary": change_summary,
            "change_severity": "Major",
        }
        results = self.orchestrator.execute_mode_b(alert)
        self.mode_b_results.extend(results)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "STARTED")
        self.assertEqual(results[0]["prior_assessment_id"], prior_trace_id)

        new_tid = results[0]["traceability_id"]
        new_state = StateManager.load_run(str(self.orchestrator.runs_dir), new_tid)
        self.assertIsNotNone(new_state)

        expected_suffix = (
            f"\n\n--- REGULATORY CHANGE RE-ASSESSMENT (EU AI Act) ---\n"
            f"Change Summary: {change_summary}\n"
            f"Severity: Major"
        )
        actual_desc = new_state["inputs"]["subject_description"]
        self.assertTrue(
            actual_desc.endswith(expected_suffix),
            f"Subject description suffix mismatch.\n"
            f"Expected suffix: {expected_suffix!r}\n"
            f"Actual tail: {actual_desc[-300:]!r}",
        )
        self.assertEqual(new_state["inputs"]["existing_assessment_id"], prior_trace_id)

    def test_mode_b_prioritizes_annex_iii_over_general_risk(self):
        # TR-RW-PRIOR-0001: General Enterprise, earlier timestamp
        self._create_completed_run_state(
            "TR-RW-PRIOR-0001",
            ["EU"],
            [("EU AI Act", "EU")],
            "General Enterprise",
            "2026-01-01T10:00:00Z",
        )
        # TR-RW-PRIOR-0002: Annex III, later timestamp — must be prioritized first
        self._create_completed_run_state(
            "TR-RW-PRIOR-0002",
            ["EU"],
            [("EU AI Act", "EU")],
            "High-risk (Annex III, Point 5)",
            "2026-06-01T10:00:00Z",
        )
        alert = {
            "regulation_name": "EU AI Act",
            "jurisdiction": "EU",
            "change_summary": "Annex III classification criteria updated.",
            "change_severity": "Major",
        }
        results = self.orchestrator.execute_mode_b(alert)
        self.mode_b_results.extend(results)

        self.assertEqual(len(results), 2)
        self.assertEqual(
            results[0]["prior_assessment_id"],
            "TR-RW-PRIOR-0002",
            "Expected Annex III run to be prioritized despite later timestamp",
        )
        self.assertEqual(results[1]["prior_assessment_id"], "TR-RW-PRIOR-0001")


if __name__ == "__main__":
    unittest.main()
