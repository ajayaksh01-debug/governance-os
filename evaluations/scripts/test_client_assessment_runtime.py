#!/usr/bin/env python3
"""
Integration tests for the Client Assessment Agent Runtime v0.1.

Coverage:
  - Intake validation (missing fields, unsupported jurisdiction/trigger)
  - Happy path: all 6 skills pass → COMPLETE
  - Gate failures: schema gate, score gates (preliminary, below_threshold, insufficient)
  - Claims Firewall gates 2c, 3b, 4b, 5b → HALTED_FIREWALL_BREACH
  - Gate 6b terminal firewall → HALTED_FIREWALL_BREACH_TERMINAL
  - Proposal review: Approved, Conditional, Rejected
  - Conditional release: HALTED_PROPOSAL_CONDITIONAL → GATE_6_PASSED → APPROVAL_4_PENDING
  - Single-approver gates (AG-1, AG-3): approve and reject
  - Joint-approver gates (AG-2, AG-4): both approve, one rejects (partial), both reject
  - Forbidden transitions: approval bypass, post-COMPLETE
  - State persistence: load_run returns correct state
  - Output package: COMPLETE run produces all 13 artifacts
  - Audit log: entries written for each step
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]

import sys
sys.path.insert(0, str(repo_root / "agents" / "client-assessment-agent" / "runtime"))
sys.path.append(str(repo_root))

from orchestrator import Orchestrator
from state_manager import StateManager, VALID_TRANSITIONS, FORBIDDEN_TRANSITIONS
from audit_logger import AuditLogger


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_INPUTS = {
    "trigger_type": "new_client_onboarding",
    "client_name": "Meridian Bank",
    "client_ai_portfolio": "Credit scoring model (high-risk EU AI Act)",
    "existing_policies": "ISO 27001 certified, partial AI governance framework",
    "target_framework": "EU AI Act + ISO 42001",
    "target_maturity_level": "L3",
    "jurisdictions": ["EU", "UK"],
    "skip_schema_validation": True,
}

S1_FIXTURE = {
    "quality_score": 82,
    "risk_tier": "High",
    "markdown_output": "# Regulatory Scoping\n\nEU AI Act applies.",
}

S2_FIXTURE = {
    "quality_score": 88,
    "controls": [
        {"id": "C-001", "name": "Data Governance", "platform_coverage": True},
        {"id": "C-002", "name": "Model Risk", "platform_coverage": True},
    ],
    "markdown_output": "# Control Mapping\n\n42 controls mapped.",
}

S3_FIXTURE = {
    "quality_score": 78,
    "overall_ccs": 82.4,
    "production_coverage_percent": 91,
    "commercial_motion": "Expand",
    "markdown_output": "# Solution Mapping\n\nPlatform coverage confirmed.",
}

S4_FIXTURE = {
    "quality_score": 87,
    "ams": 76.2,
    "ars": 68.5,
    "critical_gaps": 1,
    "major_gaps": 3,
    "minor_gaps": 5,
    "certification_classification": "Near Ready",
    "months_to_readiness": 4,
    "markdown_output": "# ISO 42001 Gap Assessment\n\n76.2/100 AMS.",
}

S5_FIXTURE = {
    "capability_name": "ethana-credit-ai",
    "validated_status": "Production Validated",
    "ecs": 94,
    "ecs_band": "Exceptional",
    "ecs_path": "full_validation",
    "allowed_claims": ["EU AI Act compliant", "ISO 42001 aligned"],
    "prohibited_claims": [],
    "contradictions_count": 0,
    "sources_checked": 12,
    "escalation_required": False,
    "hard_disqualifiers_triggered": False,
    "phase_9_gate_completed": True,
    "validation_date": "2026-06-19",
    "markdown_output": "# Capability Validation\n\nECS: 94/100.",
}

SFM_FIXTURE = {
    "feature_validation_table": [
        {
            "proposed_feature": "Credit Risk Monitoring",
            "canonical_capability": "Risk Monitoring Dashboard",
            "integration_path": "Native API",
            "tfs_score": 92,
            "poc_readiness": "Ready",
        },
    ],
    "overall_tfs_score": 92,
    "production_tfs_score": 92,
    "quality_score": 90,
    "markdown_output": "# Feature Mapping\n\nTechnical fit validated.",
}

S6_FIXTURE_APPROVED = {
    "pcs": 91,
    "ctcs": 88,
    "release_classification": "Approved",
    "cfb_count": 0,
    "hard_disqualifiers_triggered": False,
    "markdown_output": "# Proposal Review\n\nApproved.",
}

S6_FIXTURE_CONDITIONAL = {
    "pcs": 84,
    "ctcs": 82,
    "release_classification": "Conditional",
    "cfb_count": 0,
    "hard_disqualifiers_triggered": False,
    "markdown_output": "# Proposal Review\n\nConditional approval required.",
}

S6_FIXTURE_REJECTED = {
    "pcs": 62,
    "ctcs": 58,
    "release_classification": "Rejected",
    "cfb_count": 3,
    "hard_disqualifiers_triggered": True,
    "markdown_output": "# Proposal Review\n\nRejected due to disqualifiers.",
}


# ---------------------------------------------------------------------------
# Base test class
# ---------------------------------------------------------------------------

class CARuntime(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.tmp_path = Path(self.tmp)
        config_path = str(
            repo_root / "agents" / "client-assessment-agent" / "runtime" / "config.yaml"
        )
        self.orch = Orchestrator(config_path=config_path)
        self.orch.runs_dir = self.tmp_path / "runs"
        self.orch.packages_dir = self.tmp_path / "packages"
        self.orch.logs_dir = self.tmp_path / "logs"
        self.orch.runs_dir.mkdir(parents=True, exist_ok=True)
        self.orch.packages_dir.mkdir(parents=True, exist_ok=True)
        self.orch.logs_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _wire_skills(self, s1=None, s2=None, s3=None, s4=None, s5=None,
                     sfm=None, s6=None):
        if s1 is not None:
            self.orch.executor.execute_skill_1 = lambda sm, inp, lg: s1
        if s2 is not None:
            self.orch.executor.execute_skill_2 = lambda sm, inp, lg: s2
        if s3 is not None:
            self.orch.executor.execute_skill_3 = lambda sm, inp, lg: s3
        if s4 is not None:
            self.orch.executor.execute_skill_4 = lambda sm, inp, lg: s4
        if s5 is not None:
            self.orch.executor.execute_skill_5 = lambda sm, inp, lg: s5
        if sfm is not None:
            self.orch.executor.execute_skill_fm = lambda sm, inp, lg: sfm
        if s6 is not None:
            self.orch.executor.execute_skill_6 = lambda sm, inp, lg: s6

    def _wire_all(self, s6=None):
        self._wire_skills(
            s1=S1_FIXTURE,
            s2=S2_FIXTURE,
            s3=S3_FIXTURE,
            s4=S4_FIXTURE,
            s5=S5_FIXTURE,
            sfm=SFM_FIXTURE,
            s6=s6 or S6_FIXTURE_APPROVED,
        )

    def _get_state(self, tid: str) -> dict:
        sm = StateManager(str(self.orch.runs_dir), tid)
        return sm.load_state()

    def _status(self, tid: str) -> str:
        return self._get_state(tid).get("status")

    def _approve_ag1(self, tid, action="Approve"):
        self.orch.submit_approval(tid, 1, "general_counsel", action, "GC Test", "Test approval")

    def _approve_ag2_both(self, tid, action_dpo="Approve", action_ciso="Approve"):
        self.orch.submit_approval(tid, 2, "dpo", action_dpo, "DPO Test", "Test approval")
        self.orch.submit_approval(tid, 2, "ciso", action_ciso, "CISO Test", "Test approval")

    def _approve_ag3(self, tid, action="Approve"):
        self.orch.submit_approval(tid, 3, "crc_lead", action, "CRC Test", "Test approval")

    def _approve_ag4_both(self, tid, action_cd="Approve", action_sd="Approve"):
        self.orch.submit_approval(tid, 4, "compliance_director", action_cd, "CD Test", "Notes")
        self.orch.submit_approval(tid, 4, "sales_director", action_sd, "SD Test", "Notes")

    def _run_to_ag1(self):
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self.assertEqual(self._status(tid), "APPROVAL_1_PENDING")
        return tid

    def _run_to_ag2(self):
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "APPROVAL_2_PENDING")
        return tid

    def _run_to_ag3(self):
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE, s4=S4_FIXTURE
        )
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self.assertEqual(self._status(tid), "APPROVAL_3_PENDING")
        return tid

    def _run_to_ag4(self):
        self._wire_all()
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "APPROVAL_4_PENDING")
        return tid


# ---------------------------------------------------------------------------
# Intake validation tests
# ---------------------------------------------------------------------------

class TestIntakeValidation(CARuntime):
    def test_missing_required_field_halts_intake(self):
        inputs = dict(VALID_INPUTS)
        del inputs["client_name"]
        tid = self.orch.start_run("new_client_onboarding", inputs)
        self.assertEqual(self._status(tid), "HALTED_INTAKE_INVALID")

    def test_unsupported_jurisdiction_halts(self):
        inputs = dict(VALID_INPUTS)
        inputs["jurisdictions"] = ["EU", "Singapore"]
        tid = self.orch.start_run("new_client_onboarding", inputs)
        self.assertEqual(self._status(tid), "HALTED_INTAKE_UNSUPPORTED_JURISDICTION")

    def test_invalid_trigger_type_halts(self):
        inputs = dict(VALID_INPUTS)
        inputs["trigger_type"] = "random_trigger"
        tid = self.orch.start_run("random_trigger", inputs)
        self.assertEqual(self._status(tid), "HALTED_INTAKE_INVALID")

    def test_empty_jurisdictions_still_passes(self):
        inputs = dict(VALID_INPUTS)
        inputs["jurisdictions"] = []
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", inputs)
        # No unsupported jurisdictions in an empty list — passes intake
        self.assertNotEqual(self._status(tid), "HALTED_INTAKE_UNSUPPORTED_JURISDICTION")

    def test_valid_intake_proceeds_to_skill_1(self):
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self.assertNotIn(
            self._status(tid),
            ["HALTED_INTAKE_INVALID", "HALTED_INTAKE_UNSUPPORTED_JURISDICTION"],
        )


# ---------------------------------------------------------------------------
# Skill 1 score gate tests
# ---------------------------------------------------------------------------

class TestSkill1ScoreGates(CARuntime):
    def _s1(self, score: int) -> dict:
        return {**S1_FIXTURE, "quality_score": score}

    def test_score_insufficient_below_55(self):
        self._wire_skills(s1=self._s1(40))
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self.assertEqual(self._status(tid), "HALTED_GATE_1_SCORE_INSUFFICIENT")

    def test_score_preliminary_band(self):
        self._wire_skills(s1=self._s1(62))
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self.assertEqual(self._status(tid), "HALTED_GATE_1_SCORE_PRELIMINARY")

    def test_score_pass_at_threshold(self):
        self._wire_skills(s1=self._s1(70))
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self.assertEqual(self._status(tid), "APPROVAL_1_PENDING")

    def test_score_pass_above_threshold(self):
        self._wire_skills(s1=self._s1(91))
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self.assertEqual(self._status(tid), "APPROVAL_1_PENDING")


# ---------------------------------------------------------------------------
# AG-1 approval gate tests
# ---------------------------------------------------------------------------

class TestAG1Approval(CARuntime):
    def test_ag1_approve_advances_to_skill_2(self):
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self.assertEqual(self._status(tid), "APPROVAL_1_PENDING")
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "APPROVAL_2_PENDING")

    def test_ag1_reject_halts(self):
        tid = self._run_to_ag1()
        self.orch.submit_approval(tid, 1, "general_counsel", "Reject", "GC", "Not ready")
        self.assertEqual(self._status(tid), "HALTED_APPROVAL_1_REJECTED")

    def test_ag1_invalid_action_raises(self):
        tid = self._run_to_ag1()
        with self.assertRaises(ValueError):
            self.orch.submit_approval(tid, 1, "general_counsel", "Maybe", "GC", "")

    def test_approval_bypass_raises_forbidden_transition(self):
        tid = self._run_to_ag1()
        sm = StateManager(str(self.orch.runs_dir), tid)
        with self.assertRaises(ValueError):
            sm.transition_to("SKILL_2_RUNNING", "bypass attempt")


# ---------------------------------------------------------------------------
# Skill 2 firewall and score gates
# ---------------------------------------------------------------------------

class TestSkill2Gates(CARuntime):
    def test_firewall_2c_breach_halts(self):
        inputs = {**VALID_INPUTS, "simulate_firewall_breach_at_gate": "2c"}
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", inputs)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH")

    def test_skill_2_score_insufficient(self):
        self._wire_skills(s1=S1_FIXTURE, s2={**S2_FIXTURE, "quality_score": 55})
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "HALTED_GATE_2_SCORE_INSUFFICIENT")

    def test_skill_2_score_below_threshold(self):
        self._wire_skills(s1=S1_FIXTURE, s2={**S2_FIXTURE, "quality_score": 75})
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "HALTED_GATE_2_SCORE_BELOW_THRESHOLD")

    def test_skill_2_score_pass(self):
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "APPROVAL_2_PENDING")


# ---------------------------------------------------------------------------
# Skill 3 firewall and score gates
# ---------------------------------------------------------------------------

class TestSkill3Gates(CARuntime):
    def test_firewall_3b_breach_halts(self):
        inputs = {**VALID_INPUTS, "simulate_firewall_breach_at_gate": "3b"}
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", inputs)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH")

    def test_skill_3_score_insufficient(self):
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE, s3={**S3_FIXTURE, "quality_score": 55})
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "HALTED_GATE_3_SCORE_INSUFFICIENT")

    def test_skill_3_pass_reaches_ag2(self):
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "APPROVAL_2_PENDING")


# ---------------------------------------------------------------------------
# AG-2 joint approval gate tests (DPO + CISO)
# ---------------------------------------------------------------------------

class TestAG2JointApproval(CARuntime):
    def test_ag2_awaiting_second_after_first_vote(self):
        tid = self._run_to_ag2()
        self.orch.submit_approval(tid, 2, "dpo", "Approve", "DPO", "")
        self.assertEqual(self._status(tid), "APPROVAL_2_PENDING")

    def test_ag2_both_approve_advances(self):
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE, s4=S4_FIXTURE
        )
        tid = self._run_to_ag2()
        self._approve_ag2_both(tid)
        self.assertEqual(self._status(tid), "APPROVAL_3_PENDING")

    def test_ag2_one_reject_partial(self):
        tid = self._run_to_ag2()
        self._approve_ag2_both(tid, action_dpo="Approve", action_ciso="Reject")
        self.assertEqual(self._status(tid), "HALTED_APPROVAL_2_PARTIAL")

    def test_ag2_both_reject(self):
        tid = self._run_to_ag2()
        self._approve_ag2_both(tid, action_dpo="Reject", action_ciso="Reject")
        self.assertEqual(self._status(tid), "HALTED_APPROVAL_2_REJECTED")

    def test_ag2_invalid_role_raises(self):
        tid = self._run_to_ag2()
        with self.assertRaises(ValueError):
            self.orch.submit_approval(tid, 2, "general_counsel", "Approve", "GC", "")

    def test_ag2_approval_bypass_raises(self):
        tid = self._run_to_ag2()
        sm = StateManager(str(self.orch.runs_dir), tid)
        with self.assertRaises(ValueError):
            sm.transition_to("SKILL_4_RUNNING", "bypass attempt")


# ---------------------------------------------------------------------------
# Skill 4 firewall and score gates
# ---------------------------------------------------------------------------

class TestSkill4Gates(CARuntime):
    def test_firewall_4b_breach_halts(self):
        inputs = {**VALID_INPUTS, "simulate_firewall_breach_at_gate": "4b"}
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE, s4=S4_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", inputs)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH")

    def test_skill_4_score_insufficient(self):
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE,
            s4={**S4_FIXTURE, "quality_score": 55},
        )
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self.assertEqual(self._status(tid), "HALTED_GATE_4_SCORE_INSUFFICIENT")

    def test_skill_4_score_below_threshold(self):
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE,
            s4={**S4_FIXTURE, "quality_score": 75},
        )
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self.assertEqual(self._status(tid), "HALTED_GATE_4_SCORE_BELOW_THRESHOLD")

    def test_skill_4_pass_reaches_ag3(self):
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE, s4=S4_FIXTURE
        )
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self.assertEqual(self._status(tid), "APPROVAL_3_PENDING")


# ---------------------------------------------------------------------------
# AG-3 approval gate tests (single — CRC Lead)
# ---------------------------------------------------------------------------

class TestAG3Approval(CARuntime):
    def test_ag3_approve_advances_to_approval_4(self):
        self._wire_all()
        tid = self._run_to_ag3()
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "APPROVAL_4_PENDING")

    def test_ag3_reject_halts(self):
        tid = self._run_to_ag3()
        self.orch.submit_approval(tid, 3, "crc_lead", "Reject", "CRC", "Too risky")
        self.assertEqual(self._status(tid), "HALTED_APPROVAL_3_REJECTED")

    def test_ag3_approval_bypass_raises(self):
        tid = self._run_to_ag3()
        sm = StateManager(str(self.orch.runs_dir), tid)
        with self.assertRaises(ValueError):
            sm.transition_to("SKILL_5_RUNNING", "bypass")


# ---------------------------------------------------------------------------
# Skill 5 firewall and score gates
# ---------------------------------------------------------------------------

class TestSkill5Gates(CARuntime):
    def test_firewall_5b_breach_halts(self):
        inputs = {**VALID_INPUTS, "simulate_firewall_breach_at_gate": "5b"}
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE, s4=S4_FIXTURE, s5=S5_FIXTURE
        )
        tid = self.orch.start_run("new_client_onboarding", inputs)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH")

    def test_skill_5_ecs_insufficient(self):
        s5_low = {**S5_FIXTURE, "ecs": 75}
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE, s4=S4_FIXTURE, s5=s5_low
        )
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "HALTED_GATE_5_SCORE_INSUFFICIENT")

    def test_skill_5_escalation_required_halts(self):
        s5_esc = {**S5_FIXTURE, "escalation_required": True}
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE, s4=S4_FIXTURE, s5=s5_esc
        )
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "HALTED_GATE_5_SCORE_INSUFFICIENT")


# ---------------------------------------------------------------------------
# Skill FM gate tests (Suite B — PR-006 Phase 3)
# ---------------------------------------------------------------------------

class TestSkillFMGates(CARuntime):
    """FM-a / FM-b / FM-c halt-path and mock-override coverage."""

    # Inputs with real schema validation enabled for all gates.
    INPUTS_REAL_FM_SCHEMA = {
        k: v for k, v in VALID_INPUTS.items() if k != "skip_schema_validation"
    }

    def _run_to_fm(self, sfm_fixture, inputs=None):
        """Wire all skills and drive approvals until FM executes."""
        self._wire_skills(
            s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE,
            s4=S4_FIXTURE, s5=S5_FIXTURE,
            sfm=sfm_fixture,
            s6=S6_FIXTURE_APPROVED,
        )
        run_inputs = inputs if inputs is not None else VALID_INPUTS
        tid = self.orch.start_run("new_client_onboarding", run_inputs)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        return tid

    def _with_fm_schema_only(self):
        """Patch validator: pass all schemas except feature_mapping_output (real validation)."""
        real_validate = self.orch.validator.validate
        def _selective(payload, schema_name):
            if schema_name == "feature_mapping_output":
                return real_validate(payload, schema_name)
            return []
        self.orch.validator.validate = _selective

    # --- Gate FM-a: schema conformance ---

    def test_fma_missing_required_field_halts_gate_fm_schema(self):
        self._with_fm_schema_only()
        sfm = {k: v for k, v in SFM_FIXTURE.items() if k != "feature_validation_table"}
        tid = self._run_to_fm(sfm, inputs=self.INPUTS_REAL_FM_SCHEMA)
        self.assertEqual(self._status(tid), "HALTED_GATE_FM_SCHEMA")

    def test_fma_wrong_type_halts_gate_fm_schema(self):
        self._with_fm_schema_only()
        sfm = {**SFM_FIXTURE, "overall_tfs_score": "not_an_int"}
        tid = self._run_to_fm(sfm, inputs=self.INPUTS_REAL_FM_SCHEMA)
        self.assertEqual(self._status(tid), "HALTED_GATE_FM_SCHEMA")

    def test_fma_empty_table_halts_gate_fm_empty_table(self):
        # Schema is skipped (VALID_INPUTS); empty-table check catches the empty array.
        sfm = {**SFM_FIXTURE, "feature_validation_table": []}
        tid = self._run_to_fm(sfm)
        self.assertEqual(self._status(tid), "HALTED_GATE_FM_EMPTY_TABLE")

    # --- Gate FM-b: Claims Firewall ---

    def test_fmb_simulated_breach_halts_firewall_breach(self):
        inputs = {**VALID_INPUTS, "simulate_firewall_breach_at_gate": "FM-b"}
        tid = self._run_to_fm(SFM_FIXTURE, inputs=inputs)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH")

    # --- Gate FM-c: production TFS threshold ---

    def test_fmc_low_tfs_halts_gate_fm_low_tfs(self):
        sfm = {**SFM_FIXTURE, "production_tfs_score": 80}
        tid = self._run_to_fm(sfm)
        self.assertEqual(self._status(tid), "HALTED_GATE_FM_LOW_TFS")

    def test_fmc_boundary_tfs_85_passes_gate(self):
        # Exactly 85 meets the >= 85 threshold — must advance to APPROVAL_4_PENDING.
        sfm = {**SFM_FIXTURE, "production_tfs_score": 85}
        tid = self._run_to_fm(sfm)
        self.assertEqual(self._status(tid), "APPROVAL_4_PENDING")

    def test_fmc_mock_score_used_when_production_tfs_absent(self):
        # production_tfs_score absent; mock_skill_fm_score above threshold → passes.
        sfm = {k: v for k, v in SFM_FIXTURE.items() if k != "production_tfs_score"}
        inputs = {**VALID_INPUTS, "mock_skill_fm_score": 92}
        tid = self._run_to_fm(sfm, inputs=inputs)
        self.assertEqual(self._status(tid), "APPROVAL_4_PENDING")

    def test_fmc_mock_score_below_threshold_halts(self):
        # production_tfs_score absent; mock below threshold → halts.
        sfm = {k: v for k, v in SFM_FIXTURE.items() if k != "production_tfs_score"}
        inputs = {**VALID_INPUTS, "mock_skill_fm_score": 70}
        tid = self._run_to_fm(sfm, inputs=inputs)
        self.assertEqual(self._status(tid), "HALTED_GATE_FM_LOW_TFS")

    def test_fmc_real_score_overrides_mock_when_present(self):
        # production_tfs_score present (80, below 85); mock is 92 (above) — real wins.
        sfm = {**SFM_FIXTURE, "production_tfs_score": 80}
        inputs = {**VALID_INPUTS, "mock_skill_fm_score": 92}
        tid = self._run_to_fm(sfm, inputs=inputs)
        self.assertEqual(self._status(tid), "HALTED_GATE_FM_LOW_TFS")


# ---------------------------------------------------------------------------
# Firewall fail-closed enforcement (PR-005)
# ---------------------------------------------------------------------------

class TestFirewallFailClosed(CARuntime):
    """Prove that the firewall halts (fail-closed) when the linter cannot execute."""

    def test_empty_markdown_output_fails_closed(self):
        """Skill output with no markdown_output halts at the firewall gate."""
        s2_no_md = {k: v for k, v in S2_FIXTURE.items() if k != "markdown_output"}
        self._wire_skills(s1=S1_FIXTURE, s2=s2_no_md)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH")

    def test_import_error_fails_closed(self):
        """ImportError during claims_linter load halts at the firewall gate."""
        import sys
        from unittest.mock import patch
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        # Skill 2 (and Gate 2c firewall) fires on AG-1 approval.
        # Mask claims_linter so the import inside _run_firewall_check fails.
        with patch.dict(sys.modules, {"claims_linter": None}):
            self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH")


# ---------------------------------------------------------------------------
# Skill 6 and AG-4 tests
# ---------------------------------------------------------------------------

class TestSkill6AndAG4(CARuntime):
    def test_firewall_6b_terminal_breach(self):
        inputs = {**VALID_INPUTS, "simulate_firewall_breach_at_gate": "6b"}
        self._wire_all()
        tid = self.orch.start_run("new_client_onboarding", inputs)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH_TERMINAL")

    def test_proposal_rejected(self):
        self._wire_all(s6=S6_FIXTURE_REJECTED)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "HALTED_PROPOSAL_REJECTED")

    def test_proposal_conditional_halts_awaiting_cd(self):
        self._wire_all(s6=S6_FIXTURE_CONDITIONAL)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "HALTED_PROPOSAL_CONDITIONAL")

    def test_conditional_release_advances_to_ag4(self):
        self._wire_all(s6=S6_FIXTURE_CONDITIONAL)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "HALTED_PROPOSAL_CONDITIONAL")
        self.orch.release_conditional(tid, "CD-Test", "All conditional items resolved.")
        self.assertEqual(self._status(tid), "APPROVAL_4_PENDING")

    def test_conditional_release_wrong_state_raises(self):
        tid = self._run_to_ag1()
        with self.assertRaises(ValueError):
            self.orch.release_conditional(tid, "CD", "")

    def test_ag4_both_approve_produces_complete(self):
        tid = self._run_to_ag4()
        self._approve_ag4_both(tid)
        self.assertEqual(self._status(tid), "COMPLETE")

    def test_ag4_partial_halts(self):
        tid = self._run_to_ag4()
        self._approve_ag4_both(tid, action_cd="Approve", action_sd="Reject")
        self.assertEqual(self._status(tid), "HALTED_APPROVAL_4_PARTIAL")

    def test_ag4_both_reject(self):
        tid = self._run_to_ag4()
        self._approve_ag4_both(tid, action_cd="Reject", action_sd="Reject")
        self.assertEqual(self._status(tid), "HALTED_APPROVAL_4_REJECTED")

    def test_ag4_approval_bypass_raises(self):
        tid = self._run_to_ag4()
        sm = StateManager(str(self.orch.runs_dir), tid)
        with self.assertRaises(ValueError):
            sm.transition_to("ASSEMBLING_PACKAGE", "bypass")

    def test_ag4_bypass_to_complete_raises(self):
        tid = self._run_to_ag4()
        sm = StateManager(str(self.orch.runs_dir), tid)
        with self.assertRaises(ValueError):
            sm.transition_to("COMPLETE", "bypass")

    def test_rejected_proposal_cannot_go_to_ag4(self):
        self._wire_all(s6=S6_FIXTURE_REJECTED)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self.assertEqual(self._status(tid), "HALTED_PROPOSAL_REJECTED")
        sm = StateManager(str(self.orch.runs_dir), tid)
        with self.assertRaises(ValueError):
            sm.transition_to("APPROVAL_4_PENDING", "bypass rejected proposal")


# ---------------------------------------------------------------------------
# Happy path and output package
# ---------------------------------------------------------------------------

class TestHappyPathAndOutputPackage(CARuntime):
    def test_complete_run_produces_correct_state(self):
        self._wire_all()
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self._approve_ag4_both(tid)
        self.assertEqual(self._status(tid), "COMPLETE")

    def test_complete_run_produces_output_package(self):
        self._wire_all()
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self._approve_ag4_both(tid)

        pkg_dir = self.orch.packages_dir / tid
        self.assertTrue(pkg_dir.exists(), "Package directory not created")

        expected_files = [
            f"{tid}-regulatory-scoping-matrix.md",
            f"{tid}-operational-control-spec.md",
            f"{tid}-solution-mapping-report.md",
            f"{tid}-iso42001-gap-assessment.md",
            f"{tid}-capability-validation-report.md",
            f"{tid}-proposal-review-certificate.md",
            f"{tid}-client-scorecard.json",
            f"{tid}-run-log.json",
        ]
        for fname in expected_files:
            self.assertTrue((pkg_dir / fname).exists(), f"Missing: {fname}")

        payloads_dir = pkg_dir / "payloads"
        expected_payloads = [
            f"{tid}-regulatory-mapping-payload.json",
            f"{tid}-control-mapping-payload.json",
            f"{tid}-solution-mapping-payload.json",
            f"{tid}-iso42001-gap-assessment-payload.json",
            f"{tid}-capability-validation-payload.json",
            f"{tid}-proposal-review-payload.json",
        ]
        for fname in expected_payloads:
            self.assertTrue((payloads_dir / fname).exists(), f"Missing payload: {fname}")

    def test_scorecard_fields_present(self):
        self._wire_all()
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self._approve_ag4_both(tid)

        scorecard_path = self.orch.packages_dir / tid / f"{tid}-client-scorecard.json"
        self.assertTrue(scorecard_path.exists())
        sc = json.loads(scorecard_path.read_text())

        for key in [
            "traceability_id", "client_name", "assessment_date",
            "regulatory_assessment", "control_assessment", "platform_coverage",
            "iso42001_assessment", "capability_validation", "proposal_review",
            "overall_readiness_band",
        ]:
            self.assertIn(key, sc, f"Scorecard missing: {key}")
        self.assertEqual(sc["traceability_id"], tid)
        self.assertEqual(sc["client_name"], "Meridian Bank")

    def test_scorecard_readiness_band(self):
        self._wire_all()
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self._approve_ag4_both(tid)

        scorecard_path = self.orch.packages_dir / tid / f"{tid}-client-scorecard.json"
        sc = json.loads(scorecard_path.read_text())
        self.assertIn(
            sc["overall_readiness_band"],
            ["Ready", "Near Ready", "Developing", "Significant Gaps"],
        )


# ---------------------------------------------------------------------------
# State persistence tests
# ---------------------------------------------------------------------------

class TestStatePersistence(CARuntime):
    def test_state_persists_to_disk(self):
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        state_file = self.orch.runs_dir / f"{tid}_state.json"
        self.assertTrue(state_file.exists())
        loaded = json.loads(state_file.read_text())
        self.assertEqual(loaded["traceability_id"], tid)
        self.assertEqual(loaded["status"], "APPROVAL_1_PENDING")

    def test_load_run_returns_state(self):
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        loaded = StateManager.load_run(str(self.orch.runs_dir), tid)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["traceability_id"], tid)

    def test_load_run_nonexistent_returns_none(self):
        result = StateManager.load_run(str(self.orch.runs_dir), "TR-CA-NONEXISTENT")
        self.assertIsNone(result)

    def test_history_length_matches_transitions(self):
        self._wire_all()
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self._approve_ag2_both(tid)
        self._approve_ag3(tid)
        self._approve_ag4_both(tid)
        state = self._get_state(tid)
        # Minimum: initialization + transitions. At least 20 entries for a full run.
        self.assertGreaterEqual(len(state["history"]), 20)

    def test_intermediate_data_preserved(self):
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        state = self._get_state(tid)
        self.assertIn("skill_1_json", state["intermediate_data"])
        self.assertEqual(state["intermediate_data"]["skill_1_json"]["quality_score"], 82)


# ---------------------------------------------------------------------------
# Audit log tests
# ---------------------------------------------------------------------------

class TestAuditLogger(CARuntime):
    def test_audit_log_created_for_run(self):
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        log_file = self.orch.logs_dir / f"{tid}_audit.jsonl"
        self.assertTrue(log_file.exists())

    def test_audit_log_entries_are_valid_jsonl(self):
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        logger = AuditLogger(str(self.orch.logs_dir), tid)
        logs = logger.get_logs()
        self.assertGreater(len(logs), 0)
        for entry in logs:
            self.assertIn("traceability_id", entry)
            self.assertIn("step", entry)
            self.assertIn("status", entry)


# ---------------------------------------------------------------------------
# Critical defect regression tests (post-review fixes)
# ---------------------------------------------------------------------------

# Same as VALID_INPUTS but with real schema validation ENABLED.
VALID_INPUTS_REAL_SCHEMA = {
    k: v for k, v in VALID_INPUTS.items() if k != "skip_schema_validation"
}

# Schema-conformant Skill 1 output (regulatory_mapping_output).
S1_FIXTURE_SCHEMA_VALID = {
    "applicable_regulations": [{"name": "EU AI Act", "jurisdiction": "EU"}],
    "applicable_frameworks": [{"name": "ISO 42001"}],
    "regulatory_obligations": [{"obligation": "Risk management system"}],
    "control_requirements": [{"control": "Data governance"}],
    "quality_score": 82,
    "risk_tier": "High",
    "markdown_output": "# Regulatory Scoping\n\nEU AI Act applies.",
}

# Skill 2 output whose markdown makes a real Claims Firewall hard-rule violation:
# "Ethana Workspace" (Aspirational in the canonical product model) claimed as Production.
S2_FIXTURE_FIREWALL_VIOLATION = {
    "quality_score": 88,
    "controls": [{"id": "C-001", "name": "Data Governance", "platform_coverage": True}],
    "markdown_output": (
        "# Operational Control Specification\n\n"
        "The Ethana Workspace is in production today and fully deployed "
        "for governed AI workspaces.\n"
    ),
}


class TestCriticalDefectRegressions(CARuntime):
    # --- Defect 1: schema gate ordering ------------------------------------

    def test_defect1_schema_failure_halts_not_crashes(self):
        """
        Reproduces the schema-gate ordering bug. S1_FIXTURE is missing the
        required regulatory_mapping_output fields. With real validation enabled,
        the run MUST halt cleanly at HALTED_GATE_1_SCHEMA — not raise ValueError
        from an invalid SKILL_1_RUNNING -> HALTED_GATE_1_SCHEMA transition.
        """
        self._wire_skills(s1=S1_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS_REAL_SCHEMA)
        self.assertEqual(self._status(tid), "HALTED_GATE_1_SCHEMA")

    def test_defect1_valid_schema_still_advances(self):
        """A schema-conformant Skill 1 output still reaches AG-1 under real validation."""
        self._wire_skills(s1=S1_FIXTURE_SCHEMA_VALID)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS_REAL_SCHEMA)
        self.assertEqual(self._status(tid), "APPROVAL_1_PENDING")

    # --- Defect 2: Claims Firewall integration -----------------------------

    def test_defect2_real_firewall_violation_detected(self):
        """
        Reproduces the broken firewall import path. With a real (non-simulated)
        hard-rule violation in the Skill 2 markdown, the run MUST halt at
        HALTED_FIREWALL_BREACH. Before the fix, claims_linter could not be
        imported and the gate silently passed.
        """
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE_FIREWALL_VIOLATION)
        # VALID_INPUTS skips schema (to isolate the firewall) but does NOT set
        # simulate_firewall_breach_at_gate — the real linter must run.
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "HALTED_FIREWALL_BREACH")

    def test_defect2_clean_markdown_passes_firewall(self):
        """Clean Skill 2 markdown passes the real firewall and advances to AG-2."""
        self._wire_skills(s1=S1_FIXTURE, s2=S2_FIXTURE, s3=S3_FIXTURE)
        tid = self.orch.start_run("new_client_onboarding", VALID_INPUTS)
        self._approve_ag1(tid)
        self.assertEqual(self._status(tid), "APPROVAL_2_PENDING")


# ---------------------------------------------------------------------------
# State machine structure tests
# ---------------------------------------------------------------------------

class TestStateMachineStructure(unittest.TestCase):
    def test_valid_transitions_has_65_states(self):
        # 59 base states + 6 Skill FM states (SKILL_FM_RUNNING, SKILL_FM_COMPLETE,
        # GATE_FM_PASSED, HALTED_GATE_FM_SCHEMA, HALTED_GATE_FM_EMPTY_TABLE,
        # HALTED_GATE_FM_LOW_TFS) added in PR-006.
        self.assertEqual(len(VALID_TRANSITIONS), 65)

    def test_all_halted_states_terminal_or_conditional(self):
        halted = [s for s in VALID_TRANSITIONS if s.startswith("HALTED_")]
        for state in halted:
            outgoing = VALID_TRANSITIONS[state]
            if state == "HALTED_PROPOSAL_CONDITIONAL":
                self.assertEqual(outgoing, {"GATE_6_PASSED"})
            else:
                self.assertEqual(outgoing, set(), f"{state} should be terminal")

    def test_complete_state_is_terminal(self):
        self.assertEqual(VALID_TRANSITIONS.get("COMPLETE"), set())

    def test_forbidden_transitions_listed(self):
        self.assertGreater(len(FORBIDDEN_TRANSITIONS), 0)

    def test_firewall_breach_has_no_outgoing(self):
        self.assertEqual(VALID_TRANSITIONS.get("HALTED_FIREWALL_BREACH"), set())
        self.assertEqual(VALID_TRANSITIONS.get("HALTED_FIREWALL_BREACH_TERMINAL"), set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
