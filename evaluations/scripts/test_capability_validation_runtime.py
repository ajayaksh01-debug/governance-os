#!/usr/bin/env python3
"""
Unit and Integration Test Suite for Capability Validation Agent Runtime v0.1.
Validates the dynamic execution, ECS/CPL assignments, gate validations, and peer sign-offs.
"""

import os
import sys
import shutil
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]


class TestCapabilityValidationRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sys as _sys
        _rt = str(repo_root / "agents" / "capability_validation_agent" / "runtime")
        if _rt not in _sys.path:
            _sys.path.insert(0, _rt)
        for _k in ("orchestrator", "state_manager", "audit_logger", "schema_validator",
                   "output_builder", "skill_executor"):
            _sys.modules.pop(_k, None)
        from agents.capability_validation_agent.runtime.orchestrator import Orchestrator
        from agents.capability_validation_agent.runtime.state_manager import StateManager
        from agents.capability_validation_agent.runtime.audit_logger import AuditLogger
        _m = _sys.modules[__name__]
        _m.Orchestrator = Orchestrator
        _m.StateManager = StateManager
        _m.AuditLogger = AuditLogger
    def setUp(self):
        self.config_path = str(repo_root / "agents" / "capability_validation_agent" / "runtime" / "config.yaml")
        self.orchestrator = Orchestrator(self.config_path)
        self.trace_id = "TR-CV-TEST-9999"
        
        # Ensure clean state
        self.cleanup_test_run()

    def tearDown(self):
        self.cleanup_test_run()

    def cleanup_test_run(self):
        state_file = Path(self.orchestrator.runs_dir) / f"{self.trace_id}_state.json"
        if state_file.exists():
            state_file.unlink()
        audit_file = Path(self.orchestrator.logs_dir) / f"{self.trace_id}_audit.jsonl"
        if audit_file.exists():
            audit_file.unlink()
        pkg_dir = Path(self.orchestrator.packages_dir) / self.trace_id
        if pkg_dir.exists():
            shutil.rmtree(pkg_dir)

    def test_fixture_1_production_capability_request(self):
        """Tests clean Production capability validation (Immutable Audit Log)."""
        inputs = {
            "capability_name": "Immutable Audit Log",
            "claim_context": "Formal Proposal",
            "requesting_team": "Advisory"
        }
        
        # Override ID generation for test predictability
        self.orchestrator._generate_traceability_id = lambda: self.trace_id
        
        trace_id = self.orchestrator.start_run("new_capability_validation_request", inputs)
        self.assertEqual(trace_id, self.trace_id)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        self.assertEqual(state["status"], "APPROVAL_1_PENDING")
        
        int_data = state["intermediate_data"]
        self.assertEqual(int_data["validated_status"], "Production")
        self.assertTrue(80 <= int_data["ecs"] <= 90)
        self.assertEqual(int_data["ecs_band"], "Authoritative")
        
        # Verify JSON payload has correct fields
        s1_json = int_data["capability_validation_output_json"]
        self.assertEqual(len(s1_json["allowed_claims"]), 2)
        self.assertEqual(len(s1_json["prohibited_claims"]), 1)
        self.assertEqual(s1_json["allowed_claims"][0]["cpl"], "CPL-1")
        self.assertEqual(s1_json["allowed_claims"][1]["cpl"], "CPL-2")
        
        # Peer Approval Sign-Off
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "Peer Reviewer User", "Approved clean Production claim.")
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "COMPLETE")
        
        # Check package output files
        pkg_dir = Path(self.orchestrator.packages_dir) / self.trace_id
        self.assertTrue((pkg_dir / "README.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-capability-validation-report.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-capability-validation-payload.json").exists())

    def test_fixture_2_roadmap_capability_request(self):
        """Tests In Build capability validation (Ethana Discovery)."""
        inputs = {
            "capability_name": "Ethana Discovery",
            "proposed_claim": "Ethana Discovery is available now.",
            "claim_context": "Formal Proposal",
            "requesting_team": "Sales"
        }
        
        self.orchestrator._generate_traceability_id = lambda: self.trace_id
        trace_id = self.orchestrator.start_run("new_capability_validation_request", inputs)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        # Since it is a roadmap capability, ecs is 0 for the production claim,
        # but because score threshold check expects 90 and ecs=0 falls below 90,
        # it transitions to HALTED_GATE_2_INSUFFICIENT!
        self.assertEqual(state["status"], "HALTED_GATE_2_INSUFFICIENT")
        
        int_data = state["intermediate_data"]
        self.assertEqual(int_data["validated_status"], "In Build")
        self.assertEqual(int_data["ecs"], 0)
        
        s1_json = int_data["capability_validation_output_json"]
        self.assertTrue(s1_json["escalation_required"])
        self.assertEqual(len(s1_json["allowed_claims"]), 1)
        self.assertEqual(s1_json["allowed_claims"][0]["cpl"], "CPL-3")

    def test_fixture_3_mixed_status_capability_request(self):
        """Tests mixed-status sub-capability validation (MCP Security Broker)."""
        inputs = {
            "capability_name": "MCP Security Broker",
            "claim_context": "Formal Proposal",
            "requesting_team": "Technical"
        }
        
        self.orchestrator._generate_traceability_id = lambda: self.trace_id
        trace_id = self.orchestrator.start_run("new_capability_validation_request", inputs)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        # Mixed status can pass to approval if we mock/set threshold score or default ecs core passes
        # Core has score 75 which is < 90 threshold, so it halts. Let's verify it transitions as expected.
        self.assertEqual(state["status"], "HALTED_GATE_2_INSUFFICIENT")
        
        int_data = state["intermediate_data"]
        self.assertEqual(int_data["validated_status"], "Production")
        self.assertEqual(int_data["ecs"], 75)
        
        s1_json = int_data["capability_validation_output_json"]
        self.assertEqual(len(s1_json["allowed_claims"]), 2)
        self.assertEqual(s1_json["allowed_claims"][0]["cpl"], "CPL-2")
        self.assertEqual(s1_json["allowed_claims"][1]["cpl"], "CPL-3")

if __name__ == "__main__":
    unittest.main()
