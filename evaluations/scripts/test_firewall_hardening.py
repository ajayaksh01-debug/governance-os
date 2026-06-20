#!/usr/bin/env python3
"""
Final Firewall Verification Test Suite.
Validates:
1. PromptOps Canary Releases (Aspirational) -> Firewall Breach
2. FinOps Per-User Attribution (In Build) -> Firewall Breach
3. Discovery Connector (In Build) -> Firewall Breach
4. MCP Security Broker NHI (In Build) -> Firewall Breach
5. Plain English usage of "evaluation", "discovery", and "guardrails" does NOT trigger.
"""

import os
import sys
import shutil
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "evaluations" / "scripts"))

import claims_linter

class TestClaimsLinterFinalVerification(unittest.TestCase):
    def setUp(self):
        self.cpm_path = repo_root / "knowledge" / "ethana" / "canonical-product-model.md"
        self.capabilities = claims_linter.parse_canonical_model(self.cpm_path)
        
        # Create a temp dir for lint targets
        self.temp_dir = repo_root / "evaluations" / "scripts" / "temp_test_runs"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_promptops_canary_releases_breach(self):
        # PromptOps Canary Releases (Aspirational) claimed as Production -> Firewall Breach
        test_file = self.temp_dir / "test_promptops.md"
        test_file.write_text("PromptOps Canary Releases are available in production today.", encoding="utf-8")
        violations = claims_linter.lint_file(test_file, self.capabilities)
        
        self.assertTrue(len(violations) > 0, "No violations detected for PromptOps Canary Releases!")
        self.assertTrue(any("Firewall Breach" in msg and "PromptOps" in msg for _, _, msg in violations),
                        f"Expected PromptOps Firewall Breach, got: {violations}")

    def test_finops_per_user_attribution_breach(self):
        # FinOps Per-User Attribution (In Build) claimed as Production -> Firewall Breach
        test_file = self.temp_dir / "test_finops.md"
        test_file.write_text("FinOps Per-User Attribution is fully active in production.", encoding="utf-8")
        violations = claims_linter.lint_file(test_file, self.capabilities)
        
        self.assertTrue(len(violations) > 0, "No violations detected for FinOps Per-User Attribution!")
        self.assertTrue(any("Firewall Breach" in msg and "FinOps" in msg for _, _, msg in violations),
                        f"Expected FinOps Firewall Breach, got: {violations}")

    def test_discovery_connector_breach(self):
        # Discovery Connector (In Build) claimed as Production -> Firewall Breach
        test_file = self.temp_dir / "test_discovery.md"
        test_file.write_text("Discovery Connector has been deployed in the production environment.", encoding="utf-8")
        violations = claims_linter.lint_file(test_file, self.capabilities)
        
        self.assertTrue(len(violations) > 0, "No violations detected for Discovery Connector!")
        self.assertTrue(any("Firewall Breach" in msg and "Discovery" in msg for _, _, msg in violations),
                        f"Expected Discovery Firewall Breach, got: {violations}")

    def test_mcp_security_broker_nhi_breach(self):
        # MCP Security Broker NHI (In Build) claimed as Production -> Firewall Breach
        test_file = self.temp_dir / "test_nhi.md"
        test_file.write_text("MCP Security Broker NHI workload identity is operational in production.", encoding="utf-8")
        violations = claims_linter.lint_file(test_file, self.capabilities)
        
        self.assertTrue(len(violations) > 0, "No violations detected for MCP Security Broker NHI!")
        # NHI maps to "non-human identity (nhi) for agents" In Build status
        self.assertTrue(any("Firewall Breach" in msg and "non-human identity" in msg.lower() for _, _, msg in violations),
                        f"Expected NHI workload identity Firewall Breach, got: {violations}")

    def test_plain_english_evaluation(self):
        # "evaluation" used in plain English does NOT trigger
        test_file = self.temp_dir / "test_plain_evaluation.md"
        test_file.write_text("We completed a thorough performance evaluation of the model.", encoding="utf-8")
        violations = claims_linter.lint_file(test_file, self.capabilities)
        
        # Verify no violations on the word "evaluation"
        evaluation_violations = [msg for _, _, msg in violations if "Evaluation" in msg]
        self.assertEqual(len(evaluation_violations), 0, f"Plain English 'evaluation' triggered false positive: {evaluation_violations}")

    def test_plain_english_discovery(self):
        # "discovery" used in plain English does NOT trigger
        test_file = self.temp_dir / "test_plain_discovery.md"
        test_file.write_text("The discovery of the configuration issue resolved the outage.", encoding="utf-8")
        violations = claims_linter.lint_file(test_file, self.capabilities)
        
        discovery_violations = [msg for _, _, msg in violations if "Discovery" in msg]
        self.assertEqual(len(discovery_violations), 0, f"Plain English 'discovery' triggered false positive: {discovery_violations}")

    def test_plain_english_guardrails(self):
        # "guardrails" used in plain English does NOT trigger
        test_file = self.temp_dir / "test_plain_guardrails.md"
        test_file.write_text("We established operational guardrails for deployment processes.", encoding="utf-8")
        violations = claims_linter.lint_file(test_file, self.capabilities)
        
        guardrails_violations = [msg for _, _, msg in violations if "Guardrails" in msg]
        self.assertEqual(len(guardrails_violations), 0, f"Plain English 'guardrails' triggered false positive: {guardrails_violations}")


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


class TestApprovalModificationBypass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _load_rwa_classes()

    def setUp(self):
        self.config_path = str(repo_root / "agents" / "regulatory-watch-agent" / "runtime" / "config.yaml")
        self.orchestrator = Orchestrator(self.config_path)
        self.trace_id = "TR-RW-TEST-9999"
        self.state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        self.logger = AuditLogger(str(self.orchestrator.logs_dir), self.trace_id)

    def tearDown(self):
        state_file = Path(self.orchestrator.runs_dir) / f"{self.trace_id}_state.json"
        if state_file.exists():
            state_file.unlink()
        audit_file = Path(self.orchestrator.logs_dir) / f"{self.trace_id}_audit.jsonl"
        if audit_file.exists():
            audit_file.unlink()

    def test_approval_modifications_firewall_breach_blocked(self):
        initial_state = self.state_mgr.get_state()
        initial_state["status"] = "APPROVAL_2_PENDING"
        initial_state["intermediate_data"] = {
            "governance_control_mapping_output_md": "### Section 1: Executive Summary\nOriginal content with no violations.",
            "governance_control_mapping_output_json": {"score": 88},
            "governance_control_mapping_score": 88
        }
        self.state_mgr.state = initial_state
        self.state_mgr._save_state()

        bad_modification_notes = "Please integrate Visual Agent Builder into production setup."
        
        try:
            self.orchestrator.submit_approval_2(
                traceability_id=self.trace_id,
                action="Approve with modifications",
                actor="DPO Test Runner",
                notes=bad_modification_notes
            )
        except Exception:
            pass
            
        final_state = self.state_mgr.load_state()
        self.assertEqual(final_state["status"], "HALTED_FIREWALL_BREACH")


class TestSkill1FirewallBypass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _load_rwa_classes()

    def setUp(self):
        self.config_path = str(repo_root / "agents" / "regulatory-watch-agent" / "runtime" / "config.yaml")
        self.orchestrator = Orchestrator(self.config_path)
        self.trace_id = "TR-RW-TEST-8888"
        self.state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        self.logger = AuditLogger(str(self.orchestrator.logs_dir), self.trace_id)

    def tearDown(self):
        state_file = Path(self.orchestrator.runs_dir) / f"{self.trace_id}_state.json"
        if state_file.exists():
            state_file.unlink()
        audit_file = Path(self.orchestrator.logs_dir) / f"{self.trace_id}_audit.jsonl"
        if audit_file.exists():
            audit_file.unlink()

    def test_skill_1_firewall_check_fails_on_breach(self):
        initial_state = self.state_mgr.get_state()
        initial_state["status"] = "SKILL_1_RUNNING"
        initial_state["intermediate_data"] = {
            "regulatory_mapping_output_md": "### Part A - Regulatory Mapping\nWe will deploy Visual Agent Builder in production.",
            "regulatory_mapping_output_json": {}
        }
        self.state_mgr.state = initial_state
        self.state_mgr._save_state()

        s1_json = {"score": 90}
        passed = self.orchestrator._evaluate_gate_1(self.state_mgr, self.logger, s1_json, {})
        
        self.assertFalse(passed)
        final_state = self.state_mgr.load_state()
        self.assertEqual(final_state["status"], "HALTED_FIREWALL_BREACH")


if __name__ == "__main__":
    unittest.main()
