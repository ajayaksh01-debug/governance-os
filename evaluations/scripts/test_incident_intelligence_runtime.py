#!/usr/bin/env python3
"""
Unit and Integration Test Suite for Incident Intelligence Agent Runtime v0.1.
Validates dynamic execution, state persistence, gate checkpoints, firewall, and approvals.
"""

import os
import sys
import shutil
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]


class TestIncidentIntelligenceRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sys as _sys
        _rt = str(repo_root / "agents" / "incident_intelligence_agent" / "runtime")
        if _rt not in _sys.path:
            _sys.path.insert(0, _rt)
        for _k in ("orchestrator", "state_manager", "audit_logger", "schema_validator",
                   "output_builder", "skill_executor"):
            _sys.modules.pop(_k, None)
        from agents.incident_intelligence_agent.runtime.orchestrator import Orchestrator
        from agents.incident_intelligence_agent.runtime.state_manager import StateManager
        from agents.incident_intelligence_agent.runtime.audit_logger import AuditLogger
        _m = _sys.modules[__name__]
        _m.Orchestrator = Orchestrator
        _m.StateManager = StateManager
        _m.AuditLogger = AuditLogger
    def setUp(self):
        self.config_path = str(repo_root / "agents" / "incident_intelligence_agent" / "runtime" / "config.yaml")
        self.orchestrator = Orchestrator(self.config_path)
        self.trace_id = "TR-II-TEST-9999"
        
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

    def test_samsung_leak_successful_path(self):
        """Tests successful end-to-end incident assessment flow (Samsung Leak)."""
        inputs = {
            "incident_description": "In April 2023, Samsung Electronics experienced data leak incidents where employees submitted proprietary semiconductor measurement code to ChatGPT.",
            "incident_type": "Data Incident",
            "affected_system": "ChatGPT",
            "client_context": "Semiconductor manufacturing",
            "target_maturity_level": "L3: Defined"
        }
        
        # Override ID generation
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        
        trace_id = self.orchestrator.start_run("new_incident", inputs)
        self.assertEqual(trace_id, self.trace_id)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        # Quality Gate 1 passes -> Transitioned to APPROVAL_1_PENDING
        self.assertEqual(state["status"], "APPROVAL_1_PENDING")
        
        # Submit CISO Triage Approval
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "CISO Officer", "Approved Samsung triage report.")
        
        state = state_mgr.load_state()
        # Control mapping (RACI is complete) and Claims Firewall check pass -> transitioned to APPROVAL_2_PENDING
        self.assertEqual(state["status"], "APPROVAL_2_PENDING")
        
        # Submit DPO Containment Approval
        self.orchestrator.submit_approval_2(self.trace_id, "Approve", "DPO Officer", "Approved containment controls.")
        
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "COMPLETE")
        
        # Verify package folder files exist
        pkg_dir = Path(self.orchestrator.packages_dir) / self.trace_id
        self.assertTrue((pkg_dir / "README.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-incident-triage-report.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-remediation-plan.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-remediation-payload.json").exists())

    def test_amazon_bias_vague_insufficient_triage_halt(self):
        """Tests quality gate 1 halt (Triage score below 70)."""
        inputs = {
            "incident_description": "Amazon bias incident description.",
            "incident_type": "Bias/Fairness Incident",
            "mock_analysis_score": 50 # Below 70 threshold
        }
        
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self.orchestrator.start_run("new_incident", inputs)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        self.assertEqual(state["status"], "HALTED_GATE_1_INSUFFICIENT")

    def test_amazon_bias_missing_accountability_triage_halt(self):
        """Tests quality gate 2 halt (Control mapping score below 85 due to blank accountability)."""
        inputs = {
            "incident_description": "Amazon CV screening gender bias incident.",
            "incident_type": "Bias/Fairness Incident",
            "mock_accountable_role": "" # Blank RACI accountability role
        }
        
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self.orchestrator.start_run("new_incident", inputs)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "APPROVAL_1_PENDING")
        
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "CISO Officer", "Approved.")
        
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "HALTED_GATE_2_INSUFFICIENT")

    def test_unreleased_capability_claims_firewall_breach(self):
        """Tests claims firewall gate 3 halt (unreleased capability leak)."""
        inputs = {
            "incident_description": "Slack prompt injection vulnerability.",
            "incident_type": "AI Security Incident",
            "simulate_hq3_leak": True # Triggers HQ3 claims firewall breach
        }
        
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self.orchestrator.start_run("new_incident", inputs)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "CISO Officer", "Approved.")
        
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "HALTED_FIREWALL_BREACH")

    def test_approval_modification_note_firewall_breach(self):
        """Tests claims firewall breach triggered during approval modifications."""
        inputs = {
            "incident_description": "Samsung source code leak.",
            "incident_type": "Data Incident"
        }
        
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self.orchestrator.start_run("new_incident", inputs)
        
        self.orchestrator.submit_approval_1(self.trace_id, "Approve", "CISO Officer", "Approved.")
        
        # DPO attempts to insert unreleased capability (e.g. "Visual Agent Builder") in modification notes
        self.orchestrator.submit_approval_2(self.trace_id, "Approve", "DPO Officer", "Approved, but let's implement Visual Agent Builder.")
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "HALTED_FIREWALL_BREACH")

if __name__ == "__main__":
    unittest.main()
