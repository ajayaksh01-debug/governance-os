#!/usr/bin/env python3
"""
Unit and Integration Test Suite for Ethana Proposal Agent Runtime v0.1.
Validates the dynamic execution, state persistence, validation gates, firewall, and approvals.
"""

import os
import sys
import shutil
import unittest
from pathlib import Path

# Setup paths to import orchestrator, state manager
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root))
sys.path.append(str(repo_root / "agents" / "ethana_proposal_agent" / "runtime"))
sys.path.append(str(repo_root / "evaluations" / "scripts"))

from orchestrator import Orchestrator
from state_manager import StateManager
from audit_logger import AuditLogger

class TestProposalReviewRuntime(unittest.TestCase):
    def setUp(self):
        self.config_path = str(repo_root / "agents" / "ethana_proposal_agent" / "runtime" / "config.yaml")
        self.orchestrator = Orchestrator(self.config_path)
        self.trace_id = "TR-PR-TEST-9999"
        
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

    def load_fixture_proposal(self, name: str) -> str:
        path = repo_root / "evaluations" / "test-cases" / "proposal-review" / f"{name}.md"
        return path.read_text(encoding="utf-8")

    def get_base_inputs(self, name: str) -> dict:
        draft = self.load_fixture_proposal(name)
        return {
            "draft_proposal": draft,
            "solution_mapping_output": {
                "matched_capabilities": [],
                "overall_coverage_summary": {}
            },
            "feature_mapping_output": {
                "feature_validation_table": []
            }
        }

    def test_fixture_1_clean_proposal_approved_path(self):
        """Tests clean proposal Approved path (Indian Private Bank RFP)."""
        inputs = self.get_base_inputs("clean-proposal")
        
        # Override ID generation
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        
        trace_id = self.orchestrator.start_run("new_proposal_review", inputs)
        self.assertEqual(trace_id, self.trace_id)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        # Compliance Gate passes -> Transitioned to APPROVAL_PENDING
        self.assertEqual(state["status"], "APPROVAL_PENDING")
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["pcs"], 100)
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["ctcs"], 100.0)
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["classification"], "Approved")
        
        # Submit Peer sign-off Approval
        self.orchestrator.submit_approval(self.trace_id, "Approve", "Legal Counsel", "Approved clean proposal release.")
        
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "COMPLETE")
        
        # Verify package folder files exist
        pkg_dir = Path(self.orchestrator.packages_dir) / self.trace_id
        self.assertTrue((pkg_dir / "README.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-proposal-review-report.md").exists())
        self.assertTrue((pkg_dir / f"{self.trace_id}-proposal-review-payload.json").exists())

    def test_fixture_2_firewall_breach_halt(self):
        """Tests firewall breach halt (UK Insurance Pitch Deck)."""
        inputs = self.get_base_inputs("firewall-breach")
        
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self.orchestrator.start_run("new_proposal_review", inputs)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        # CFBs trigger immediate halt to HALTED_FIREWALL_BREACH
        self.assertEqual(state["status"], "HALTED_FIREWALL_BREACH")
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["pcs"], 0)
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["cfb_count"], 3)
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["classification"], "Rejected")

    def test_fixture_3_mixed_roadmap_claims_rejected_path(self):
        """Tests mixed roadmap claims Rejected path prior to correction (In Build in Current section)."""
        inputs = self.get_base_inputs("mixed-roadmap-claims")
        
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self.orchestrator.start_run("new_proposal_review", inputs)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        # SCIM and CI/CD in Current section trigger CFBs -> Halted
        self.assertEqual(state["status"], "HALTED_FIREWALL_BREACH")
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["pcs"], 0)
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["cfb_count"], 2)
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["classification"], "Rejected")

    def test_fixture_3_mixed_roadmap_claims_post_correction(self):
        """Tests mixed roadmap claims post-correction state (moved to Roadmap section)."""
        base_draft = self.load_fixture_proposal("mixed-roadmap-claims")
        
        # Simulate correction by moving SCIM and CI/CD into Section 4 Roadmap
        corrected_draft = base_draft.replace(
            "Ethana's platform provides the following capabilities, available today for deployment within your environment:",
            "Ethana's platform provides the following capabilities, available today for deployment within your environment:\n\n### Section 4 — Roadmap Capabilities\n"
        )
        
        inputs = {
            "draft_proposal": corrected_draft,
            "solution_mapping_output": {
                "matched_capabilities": [],
                "overall_coverage_summary": {}
            },
            "feature_mapping_output": {
                "feature_validation_table": []
            }
        }
        
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self.orchestrator.start_run("new_proposal_review", inputs)
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        
        # Under Section 4 Roadmap, CFBs = 0. PCS = 95, CTCS = 80.0 -> transitions to gate validation passed and approval pending
        self.assertEqual(state["status"], "APPROVAL_PENDING")
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["pcs"], 95)
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["cfb_count"], 0)
        self.assertEqual(state["intermediate_data"]["proposal_review_json"]["classification"], "Approved with Revisions")
        
        self.orchestrator.submit_approval(self.trace_id, "Approve", "Sales Director", "Approved with revisions completed.")
        
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "COMPLETE")

    def test_approval_modification_note_firewall_breach(self):
        """Tests claims firewall breach triggered during approval note bypass attempts."""
        inputs = self.get_base_inputs("clean-proposal")
        
        self.orchestrator.executor.generate_traceability_id = lambda: self.trace_id
        self.orchestrator.start_run("new_proposal_review", inputs)
        
        # Peer attempts to bypass firewall in notes
        self.orchestrator.submit_approval(self.trace_id, "Approve", "Sales Director", "Approved, but we will configure Visual Agent Builder as well.")
        
        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.trace_id)
        state = state_mgr.load_state()
        self.assertEqual(state["status"], "HALTED_FIREWALL_BREACH")

if __name__ == "__main__":
    unittest.main()
