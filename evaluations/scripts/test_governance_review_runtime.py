#!/usr/bin/env python3
"""
Integration tests for the Governance Review Agent runtime.

Test coverage:
  - Fixture: governance-ready-meridian-bank (Governance Ready)
  - Fixture: conditional-governance-axiom-fintech (Conditional Governance)
  - Fixture: not-governance-ready-apex-agency (Not Governance Ready — COMPLETE state)
  - GHD5: CCR arithmetic identity for all three fixtures
  - GHD6: ISO 42001 pass-through for all three fixtures
  - GTG-3 secondary guard: bare executor call with iso_42001_output=None
  - Intake rejection: start_run() without iso_42001_output → HALTED_INTAKE_INVALID
"""
import json
import tempfile
import unittest
from pathlib import Path


class GovReviewRuntimeTest(unittest.TestCase):
    """Base class providing fixture loader."""

    @classmethod
    def setUpClass(cls):
        import sys
        repo_root = Path(__file__).resolve().parents[2]
        sys.path.insert(0, str(repo_root))
        cls.repo_root = repo_root

    def _make_orchestrator(self, tmp_dir: Path):
        from agents.governance_review_agent.runtime.orchestrator import Orchestrator
        config_path = self.repo_root / "agents" / "governance_review_agent" / "runtime" / "config.yaml"
        orch = Orchestrator(config_path=str(config_path))
        orch.runs_dir = tmp_dir / "runs"
        orch.packages_dir = tmp_dir / "packages"
        orch.logs_dir = tmp_dir / "logs"
        orch.runs_dir.mkdir(parents=True, exist_ok=True)
        orch.packages_dir.mkdir(parents=True, exist_ok=True)
        orch.logs_dir.mkdir(parents=True, exist_ok=True)
        from agents.governance_review_agent.runtime.skill_executor import SkillExecutor
        orch.executor = SkillExecutor(orch.runs_dir, orch.logs_dir)
        return orch

    def _get_review_json(self, orchestrator, traceability_id: str) -> dict:
        from agents.governance_review_agent.runtime.state_manager import StateManager
        sm = StateManager(str(orchestrator.runs_dir), traceability_id)
        state = sm.load_state()
        return state["intermediate_data"].get("governance_review_json", {})


# ---------------------------------------------------------------------------
# Fixture: governance-ready-meridian-bank
# ---------------------------------------------------------------------------

MERIDIAN_INPUTS = {
    "regulatory_mapping_output": {
        "applicable_regulations": [
            {"name": "EU AI Act", "jurisdiction": "EU", "status": "Confirmed",
             "applicability": "High-Risk AI — Annex III credit scoring"},
            {"name": "UK FCA Model Risk Guidance", "jurisdiction": "UK", "status": "Confirmed",
             "applicability": "BFSI sector — model governance"},
        ],
        "applicable_frameworks": [
            {"name": "ISO 42001", "mandatory": True, "basis": "High-Risk AI deployment"}
        ],
        "control_requirements": [
            {"control_name": "Model Risk Framework Policy", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Model Validation Protocol", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Credit Decision Audit Trail", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 12"},
            {"control_name": "Real-Time Model Performance Dashboard", "domain": "Model Risk", "mandatory": True, "source": "UK FCA MRG"},
            {"control_name": "Model Explainability Documentation", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 13"},
            {"control_name": "Adversarial Probe Coverage", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Data Quality Assessment Process", "domain": "Data Governance", "mandatory": True, "source": "EU AI Act Art. 10"},
            {"control_name": "PII Detection and Output Sanitisation", "domain": "Data Governance", "mandatory": True, "source": "UK GDPR Art. 25"},
            {"control_name": "Data Retention and Lifecycle Policy", "domain": "Data Governance", "mandatory": True, "source": "UK GDPR Art. 5"},
            {"control_name": "Training Data Lineage Documentation", "domain": "Data Governance", "mandatory": True, "source": "EU AI Act Art. 10"},
            {"control_name": "Data Access Controls", "domain": "Data Governance", "mandatory": True, "source": "UK GDPR Art. 32"},
            {"control_name": "Transparency Disclosure Statement", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 13"},
            {"control_name": "Automated Decision Explanation", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 13"},
            {"control_name": "Human Oversight Notification", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 14"},
            {"control_name": "Regulatory Reporting Interface", "domain": "Transparency", "mandatory": True, "source": "UK FCA MRG"},
            {"control_name": "Real-Time Anomaly Detection", "domain": "Monitoring", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Regulatory Threshold Alerting", "domain": "Monitoring", "mandatory": True, "source": "UK FCA MRG"},
            {"control_name": "Continuous Performance Review", "domain": "Monitoring", "mandatory": True, "source": "EU AI Act Art. 9"},
        ],
    },
    "control_mapping_output": {
        "control_taxonomy_matrix": [
            {"control_name": "Model Risk Framework Policy", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Model Validation Protocol", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Credit Decision Audit Trail", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Real-Time Model Performance Dashboard", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Model Explainability Documentation", "coverage_classification": "Covered by Cursory Service"},
            {"control_name": "Adversarial Probe Coverage", "coverage_classification": "Partially Covered by Ethana"},
            {"control_name": "Data Quality Assessment Process", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "PII Detection and Output Sanitisation", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Data Retention and Lifecycle Policy", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Training Data Lineage Documentation", "coverage_classification": "Covered by Cursory Service"},
            {"control_name": "Data Access Controls", "coverage_classification": "Partially Covered by Ethana"},
            {"control_name": "Transparency Disclosure Statement", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Automated Decision Explanation", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Human Oversight Notification", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Regulatory Reporting Interface", "coverage_classification": "Covered by Cursory Service"},
            {"control_name": "Real-Time Anomaly Detection", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Regulatory Threshold Alerting", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Continuous Performance Review", "coverage_classification": "Partially Covered by Ethana"},
        ],
        "evidence_registry": [
            {"evidence_id": "EVID-MR-01", "control_name": "Model Risk Framework Policy", "source": "Ethana Audit Log v2.1"},
            {"evidence_id": "EVID-MR-02", "control_name": "Model Validation Protocol", "source": "Ethana Red Team Orchestrator"},
            {"evidence_id": "EVID-DG-01", "control_name": "Data Quality Assessment Process", "source": "Ethana Data Pipeline Controls"},
        ],
    },
    "iso_42001_output": {
        "ams": 82, "ars": 76, "critical_gaps": 0, "major_gaps": 1, "minor_gaps": 2,
        "certification_classification": "Certification Ready", "critical_gap_ids": [],
    },
    "capability_validation_output": {
        "allowed_claims": [
            {"claim": "LLM Gateway rate limiting and content policy enforcement", "cpl": "CPL-1"},
            {"claim": "Immutable Audit Log — application-layer audit trail", "cpl": "CPL-2"},
        ],
        "prohibited_claims": [
            {"claim": "SOC 2 certified", "reason": "Not certified — assessment in progress"},
        ],
    },
    "client_profile": {
        "sector": "BFSI", "jurisdictions": ["EU", "UK"],
        "ai_deployment_type": "High-Risk", "deployment_model": "Customer VPC",
    },
}


class TestMeridianGovernanceReady(GovReviewRuntimeTest):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._orch = self._make_orchestrator(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def _run_and_approve(self):
        tid = self._orch.start_run("trigger", MERIDIAN_INPUTS)
        self._orch.submit_approval(tid, "Approve", "Test CSM", "Integration test approval")
        return tid

    def test_classification(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["classification"], "Governance Ready")

    def test_gas(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["gas"], 96)

    def test_ccr(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["ccr"], 91.7)

    def test_ghd5_ccr_arithmetic_identity(self):
        """GHD5: round(ccr_numerator / ccr_denominator * 100, 1) == ccr"""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["ccr_numerator"], 16.5)
        self.assertEqual(rj["ccr_denominator"], 18)
        self.assertEqual(round(rj["ccr_numerator"] / rj["ccr_denominator"] * 100, 1), rj["ccr"])

    def test_ghd6_iso_passthrough(self):
        """GHD6: iso_42001_ams/ars/classification must be sourced from iso_42001_output verbatim."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["iso_42001_ams"], 82)
        self.assertEqual(rj["iso_42001_ars"], 76)
        self.assertEqual(rj["iso_42001_classification"], "Certification Ready")

    def test_cgc_count_zero(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["cgc_count"], 0)

    def test_mgf_count_zero(self):
        """GP-MGF rule: major_gaps=1 downgrades to Minor Finding, not MGF."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["mgf_count"], 0)

    def test_minor_finding_count(self):
        """major_gaps=1 (1 entry) + minor_gaps=2 (1 entry) = 2 minor findings."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["minor_finding_count"], 2)

    def test_high_risk_count(self):
        """ams=82 ≥ 70 and cgc=0 → high_risk_count = 0."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["high_risk_count"], 0)

    def test_governance_gate_passed(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertTrue(rj["governance_gate_passed"])

    def test_frameworks_assessed(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertIn("EU AI Act", rj["frameworks_assessed"])
        self.assertIn("UK FCA Model Risk Guidance", rj["frameworks_assessed"])
        self.assertIn("ISO 42001", rj["frameworks_assessed"])

    def test_input_completeness_full(self):
        """capability_validation_output present → input_completeness = Full."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["input_completeness"], "Full")

    def test_terminal_state_complete(self):
        """Run must reach COMPLETE after approval."""
        from agents.governance_review_agent.runtime.state_manager import StateManager
        tid = self._run_and_approve()
        sm = StateManager(str(self._orch.runs_dir), tid)
        state = sm.load_state()
        self.assertEqual(state["status"], "COMPLETE")

    def test_package_assembled(self):
        """Package directory must exist after COMPLETE."""
        tid = self._run_and_approve()
        pkg_dir = self._orch.packages_dir / tid
        self.assertTrue(pkg_dir.is_dir())
        self.assertTrue((pkg_dir / f"{tid}-governance-readiness-certificate.json").exists())


# ---------------------------------------------------------------------------
# Fixture: conditional-governance-axiom-fintech
# ---------------------------------------------------------------------------

AXIOM_INPUTS = {
    "regulatory_mapping_output": {
        "applicable_regulations": [
            {"name": "EU AI Act", "jurisdiction": "EU", "status": "Confirmed",
             "applicability": "Limited-Risk AI — Art. 52 transparency obligations"},
        ],
        "applicable_frameworks": [
            {"name": "ISO 42001", "mandatory": True, "basis": "AI management system baseline"},
            {"name": "NIST AI RMF", "mandatory": False, "basis": "Best practice — optional for Limited-Risk"},
        ],
        "control_requirements": [
            {"control_name": "AI System Transparency Disclosure", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 52"},
            {"control_name": "Automated Decision Notification", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 52"},
            {"control_name": "User Rights Information", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 52"},
            {"control_name": "Explanation of AI-Generated Recommendations", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 52"},
            {"control_name": "Transparency Disclosure Statement", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 52"},
            {"control_name": "Data Minimisation Policy", "domain": "Data Governance", "mandatory": True, "source": "GDPR Art. 5"},
            {"control_name": "User Data Consent Management", "domain": "Data Governance", "mandatory": True, "source": "GDPR Art. 7"},
            {"control_name": "Data Retention Schedule", "domain": "Data Governance", "mandatory": True, "source": "GDPR Art. 5"},
            {"control_name": "Data Quality Assessment Process", "domain": "Data Governance", "mandatory": True, "source": "EU AI Act Art. 10"},
            {"control_name": "System Performance Monitoring", "domain": "Monitoring", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Incident Detection and Alerting", "domain": "Monitoring", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Continuous Risk Assessment", "domain": "Monitoring", "mandatory": True, "source": "EU AI Act Art. 9"},
        ],
    },
    "control_mapping_output": {
        "control_taxonomy_matrix": [
            {"control_name": "AI System Transparency Disclosure", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Automated Decision Notification", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "User Rights Information", "coverage_classification": "Customer-Owned Control"},
            {"control_name": "Explanation of AI-Generated Recommendations", "coverage_classification": "Partially Covered by Ethana"},
            # Transparency Disclosure Statement and Data Quality Assessment Process absent → CC-MGFs
            {"control_name": "Data Minimisation Policy", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "User Data Consent Management", "coverage_classification": "Customer-Owned Control"},
            {"control_name": "Data Retention Schedule", "coverage_classification": "Partially Covered by Ethana"},
            {"control_name": "System Performance Monitoring", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Incident Detection and Alerting", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Continuous Risk Assessment", "coverage_classification": "Fully Covered by Ethana"},
        ],
        "evidence_registry": [
            {"evidence_id": "EVID-TP-01", "control_name": "AI System Transparency Disclosure", "source": "Ethana Guardrails"},
            {"evidence_id": "EVID-DG-01", "control_name": "Data Minimisation Policy", "source": "Ethana Data Controls"},
        ],
    },
    "iso_42001_output": {
        "ams": 63, "ars": 61, "critical_gaps": 0, "major_gaps": 3, "minor_gaps": 4,
        "certification_classification": "Near Ready", "critical_gap_ids": [],
    },
    # capability_validation_output intentionally absent
    "client_profile": {
        "sector": "General Enterprise", "jurisdictions": ["EU"],
        "ai_deployment_type": "Limited-Risk", "deployment_model": "Cloud",
    },
}


class TestAxiomConditionalGovernance(GovReviewRuntimeTest):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._orch = self._make_orchestrator(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def _run_and_approve(self):
        tid = self._orch.start_run("trigger", AXIOM_INPUTS)
        self._orch.submit_approval(tid, "Approve", "Test CSM", "Integration test approval")
        return tid

    def test_classification(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["classification"], "Conditional Governance")

    def test_gas(self):
        """100 − 0×15 − 2×10 − 2×2 = 76."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["gas"], 76)

    def test_ccr(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["ccr"], 75.0)

    def test_ghd5_ccr_arithmetic_identity(self):
        """GHD5: round(9.0 / 12 × 100, 1) == 75.0"""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["ccr_numerator"], 9.0)
        self.assertEqual(rj["ccr_denominator"], 12)
        self.assertEqual(round(rj["ccr_numerator"] / rj["ccr_denominator"] * 100, 1), rj["ccr"])

    def test_ghd6_iso_passthrough(self):
        """GHD6: iso pass-through from input; ams=63, ars=61, class=Near Ready."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["iso_42001_ams"], 63)
        self.assertEqual(rj["iso_42001_ars"], 61)
        self.assertEqual(rj["iso_42001_classification"], "Near Ready")

    def test_cgc_count_zero(self):
        """No domain below 50% CCR — no CGC."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["cgc_count"], 0)

    def test_mgf_count(self):
        """2 mandatory controls not in taxonomy → 2 CC-MGFs."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["mgf_count"], 2)

    def test_minor_finding_count(self):
        """major_gaps=3 (1 GP-MGF entry) + minor_gaps=4 (1 entry) = 2 minor findings."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["minor_finding_count"], 2)

    def test_high_risk_count(self):
        """ams=63 < 70 and cgc=0 → high_risk_count = 1."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["high_risk_count"], 1)

    def test_governance_gate_passed(self):
        """GTG-4 Noted absent does NOT fail governance_gate_passed."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertTrue(rj["governance_gate_passed"])

    def test_frameworks_assessed_includes_nist(self):
        """All applicable_frameworks included regardless of mandatory flag."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertIn("EU AI Act", rj["frameworks_assessed"])
        self.assertIn("ISO 42001", rj["frameworks_assessed"])
        self.assertIn("NIST AI RMF", rj["frameworks_assessed"])

    def test_input_completeness_standard(self):
        """capability_validation_output absent → input_completeness = Standard."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["input_completeness"], "Standard")

    def test_terminal_state_complete(self):
        from agents.governance_review_agent.runtime.state_manager import StateManager
        tid = self._run_and_approve()
        sm = StateManager(str(self._orch.runs_dir), tid)
        self.assertEqual(sm.load_state()["status"], "COMPLETE")


# ---------------------------------------------------------------------------
# Fixture: not-governance-ready-apex-agency
# ---------------------------------------------------------------------------

APEX_INPUTS = {
    "regulatory_mapping_output": {
        "applicable_regulations": [
            {"name": "EU AI Act", "jurisdiction": "EU", "status": "Confirmed",
             "applicability": "High-Risk AI — Annex III public sector automated decisions"},
            {"name": "UK CDEI AI Assurance Framework", "jurisdiction": "UK", "status": "Confirmed",
             "applicability": "Government sector AI deployment"},
        ],
        "applicable_frameworks": [
            {"name": "ISO 42001", "mandatory": True, "basis": "High-Risk AI — mandatory AIMS assessment"},
        ],
        "control_requirements": [
            {"control_name": "Model Risk Framework Policy", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Algorithmic Fairness Assessment", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 10"},
            {"control_name": "Human Oversight Procedure for Automated Decisions", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 14"},
            {"control_name": "Model Validation Protocol", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Model Performance Monitoring", "domain": "Model Risk", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Transparency Disclosure Statement", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 13"},
            {"control_name": "AI System Notification to Citizens", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 52"},
            {"control_name": "Decision Explanation for Benefits Eligibility", "domain": "Transparency", "mandatory": True, "source": "EU AI Act Art. 13"},
            {"control_name": "Public Register of AI Systems", "domain": "Transparency", "mandatory": True, "source": "UK CDEI Framework"},
            {"control_name": "Human Review Procedure for Automated Decisions", "domain": "Human Oversight", "mandatory": True, "source": "EU AI Act Art. 14"},
            {"control_name": "Appeal and Redress Mechanism", "domain": "Human Oversight", "mandatory": True, "source": "EU AI Act Art. 14"},
            {"control_name": "Operator Intervention Capability", "domain": "Human Oversight", "mandatory": True, "source": "EU AI Act Art. 14"},
            {"control_name": "Escalation Protocol for High-Risk Decisions", "domain": "Human Oversight", "mandatory": True, "source": "UK CDEI Framework"},
            {"control_name": "Continuous Operational Monitoring", "domain": "Monitoring", "mandatory": True, "source": "EU AI Act Art. 9"},
            {"control_name": "Post-Deployment Performance Review", "domain": "Monitoring", "mandatory": True, "source": "EU AI Act Art. 9"},
        ],
    },
    "control_mapping_output": {
        "control_taxonomy_matrix": [
            {"control_name": "Model Risk Framework Policy", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Algorithmic Fairness Assessment", "coverage_classification": "Fully Covered by Ethana"},
            # 3 Model Risk controls absent → subsumed by CGC-001 (Model Risk domain CCR = 40%)
            {"control_name": "Transparency Disclosure Statement", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "AI System Notification to Citizens", "coverage_classification": "Customer-Owned Control"},
            {"control_name": "Decision Explanation for Benefits Eligibility", "coverage_classification": "Partially Covered by Ethana"},
            # Public Register of AI Systems absent → CC-MGF (Transparency not in CGC domain)
            {"control_name": "Human Review Procedure for Automated Decisions", "coverage_classification": "Fully Covered by Ethana"},
            {"control_name": "Appeal and Redress Mechanism", "coverage_classification": "Customer-Owned Control"},
            {"control_name": "Operator Intervention Capability", "coverage_classification": "Partially Covered by Ethana"},
            # Escalation Protocol absent → CC-MGF (Human Oversight not in CGC domain)
            {"control_name": "Continuous Operational Monitoring", "coverage_classification": "Fully Covered by Ethana"},
            # Post-Deployment Performance Review absent → CC-MGF (Monitoring not in CGC domain)
        ],
        "evidence_registry": [
            {"evidence_id": "EVID-MR-01", "control_name": "Model Risk Framework Policy", "source": "Ethana Audit Log"},
            {"evidence_id": "EVID-MR-02", "control_name": "Algorithmic Fairness Assessment", "source": "Ethana Red Team Orchestrator"},
            {"evidence_id": "EVID-TR-01", "control_name": "Transparency Disclosure Statement", "source": "Ethana Guardrails"},
            {"evidence_id": "EVID-HO-01", "control_name": "Human Review Procedure for Automated Decisions", "source": "Ethana Human-in-Loop Module"},
            {"evidence_id": "EVID-MN-01", "control_name": "Continuous Operational Monitoring", "source": "Ethana Monitoring Dashboard"},
        ],
    },
    "iso_42001_output": {
        "ams": 41, "ars": 38, "critical_gaps": 0, "major_gaps": 6, "minor_gaps": 4,
        "certification_classification": "Significant Gaps", "critical_gap_ids": [],
    },
    # capability_validation_output intentionally absent
    "client_profile": {
        "sector": "Government", "jurisdictions": ["EU", "UK"],
        "ai_deployment_type": "High-Risk", "deployment_model": "On-prem",
    },
}


class TestApexNotGovernanceReady(GovReviewRuntimeTest):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._orch = self._make_orchestrator(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def _run_and_approve(self):
        tid = self._orch.start_run("trigger", APEX_INPUTS)
        # governance_gate_passed=true → reaches APPROVAL_PENDING → must approve to reach COMPLETE
        self._orch.submit_approval(tid, "Approve", "Test CSM", "Approve Not Governance Ready certificate")
        return tid

    def test_classification(self):
        """CGC absolute rule: classification = Not Governance Ready when cgc_count > 0."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["classification"], "Not Governance Ready")

    def test_gas_absolute_rule(self):
        """GHD3: cgc_count > 0 → gas = 0 regardless of arithmetic (arithmetic = 66)."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["gas"], 0)

    def test_ccr(self):
        """CCR always computed even when CGC present."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["ccr"], 53.3)

    def test_ghd5_ccr_arithmetic_identity(self):
        """GHD5: round(8.0 / 15 × 100, 1) == 53.3"""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["ccr_numerator"], 8.0)
        self.assertEqual(rj["ccr_denominator"], 15)
        self.assertEqual(round(rj["ccr_numerator"] / rj["ccr_denominator"] * 100, 1), rj["ccr"])

    def test_ghd6_iso_passthrough(self):
        """GHD6: ams=41, ars=38, class=Significant Gaps sourced verbatim from iso_42001_output."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["iso_42001_ams"], 41)
        self.assertEqual(rj["iso_42001_ars"], 38)
        self.assertEqual(rj["iso_42001_classification"], "Significant Gaps")

    def test_cgc_count_and_ids(self):
        """Model Risk domain CCR = 40% → CGC-001."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["cgc_count"], 1)
        self.assertIn("CGC-001", rj["cgc_ids"])

    def test_mgf_count(self):
        """3 CC-MGFs from Transparency/Human Oversight/Monitoring (Model Risk subsumed in CGC)."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["mgf_count"], 3)

    def test_minor_finding_count(self):
        """major_gaps=6 (1 GP-MGF entry) + minor_gaps=4 (1 entry) = 2 minor findings."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["minor_finding_count"], 2)

    def test_high_risk_count(self):
        """cgc=1 + (ams=41 < 70 → +1) = high_risk_count = 2."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertEqual(rj["high_risk_count"], 2)

    def test_governance_gate_passed_true(self):
        """All 4 mandatory GTG gates pass — gate passage does not prevent Not Governance Ready."""
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertTrue(rj["governance_gate_passed"])

    def test_frameworks_assessed(self):
        tid = self._run_and_approve()
        rj = self._get_review_json(self._orch, tid)
        self.assertIn("EU AI Act", rj["frameworks_assessed"])
        self.assertIn("UK CDEI AI Assurance Framework", rj["frameworks_assessed"])
        self.assertIn("ISO 42001", rj["frameworks_assessed"])

    def test_terminal_state_complete(self):
        """Not Governance Ready must reach COMPLETE — HALTED_GOVERNANCE_INCOMPLETE is only for system failures."""
        from agents.governance_review_agent.runtime.state_manager import StateManager
        tid = self._run_and_approve()
        sm = StateManager(str(self._orch.runs_dir), tid)
        self.assertEqual(sm.load_state()["status"], "COMPLETE")

    def test_package_assembled(self):
        """Certificate package must be assembled even for Not Governance Ready."""
        tid = self._run_and_approve()
        pkg_dir = self._orch.packages_dir / tid
        self.assertTrue(pkg_dir.is_dir())
        cert_file = pkg_dir / f"{tid}-governance-readiness-certificate.json"
        self.assertTrue(cert_file.exists())
        cert = json.loads(cert_file.read_text())
        self.assertEqual(cert["classification"], "Not Governance Ready")
        self.assertEqual(cert["gas"], 0)


# ---------------------------------------------------------------------------
# GTG-3 Secondary Guard: bare executor call with iso_42001_output=None
# ---------------------------------------------------------------------------

class TestGTG3BareSecondaryGuard(GovReviewRuntimeTest):
    """
    Bare executor test — bypasses orchestrator intake schema validation.
    Exercises the in-executor GTG-3 secondary guard that catches iso_42001_output=None.
    Follows TG-3 precedent from EPA runtime tests.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp_path = Path(self._tmp.name)
        self._runs_dir = tmp_path / "runs"
        self._logs_dir = tmp_path / "logs"
        self._runs_dir.mkdir(parents=True)
        self._logs_dir.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def _make_executor_and_deps(self, trace_id="TR-GR-2026-0001"):
        from agents.governance_review_agent.runtime.skill_executor import SkillExecutor
        from agents.governance_review_agent.runtime.state_manager import StateManager
        from agents.governance_review_agent.runtime.audit_logger import AuditLogger
        executor = SkillExecutor(self._runs_dir, self._logs_dir)
        state_mgr = StateManager(str(self._runs_dir), trace_id)
        state_mgr.initialize_run({})
        logger = AuditLogger(str(self._logs_dir), trace_id)
        return executor, state_mgr, logger

    def test_gtg3_iso_none_returns_not_governance_ready(self):
        """Executor secondary guard: iso_42001_output=None → governance_gate_passed=false."""
        executor, state_mgr, logger = self._make_executor_and_deps()
        inputs = {
            "regulatory_mapping_output": {
                "applicable_regulations": [
                    {"name": "EU AI Act", "jurisdiction": "EU", "status": "Confirmed"}
                ],
                "applicable_frameworks": [],
                "control_requirements": [
                    {"control_name": "Model Risk Framework Policy", "domain": "Model Risk",
                     "mandatory": True, "source": "EU AI Act Art. 9"},
                ],
            },
            "control_mapping_output": {
                "control_taxonomy_matrix": [],
                "evidence_registry": [],
            },
            "iso_42001_output": None,  # Secondary guard trigger
        }
        result = executor.execute_governance_review(state_mgr, inputs, logger)
        self.assertFalse(result["governance_gate_passed"])
        self.assertEqual(result["classification"], "Not Governance Ready")

    def test_gtg3_iso_none_has_zero_gas(self):
        executor, state_mgr, logger = self._make_executor_and_deps("TR-GR-2026-0002")
        inputs = {
            "regulatory_mapping_output": {
                "applicable_regulations": [
                    {"name": "EU AI Act", "jurisdiction": "EU", "status": "Confirmed"}
                ],
                "applicable_frameworks": [],
                "control_requirements": [
                    {"control_name": "Model Risk Framework Policy", "domain": "Model Risk",
                     "mandatory": True, "source": "EU AI Act Art. 9"},
                ],
            },
            "control_mapping_output": {
                "control_taxonomy_matrix": [],
                "evidence_registry": [],
            },
            "iso_42001_output": None,
        }
        result = executor.execute_governance_review(state_mgr, inputs, logger)
        self.assertEqual(result["gas"], 0)
        self.assertIsNone(result["iso_42001_ams"])
        self.assertIsNone(result["iso_42001_ars"])
        self.assertIsNone(result["iso_42001_classification"])


# ---------------------------------------------------------------------------
# Intake rejection: iso_42001_output absent → HALTED_INTAKE_INVALID
# ---------------------------------------------------------------------------

class TestIntakeRejection(GovReviewRuntimeTest):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._orch = self._make_orchestrator(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def _minimal_valid_inputs_without_iso(self) -> dict:
        return {
            "regulatory_mapping_output": {
                "applicable_regulations": [
                    {"name": "EU AI Act", "jurisdiction": "EU", "status": "Confirmed"}
                ],
                "applicable_frameworks": [],
                "control_requirements": [
                    {"control_name": "Model Risk Framework Policy", "domain": "Model Risk",
                     "mandatory": True, "source": "EU AI Act Art. 9"},
                ],
            },
            "control_mapping_output": {
                "control_taxonomy_matrix": [
                    {"control_name": "Model Risk Framework Policy",
                     "coverage_classification": "Fully Covered by Ethana"},
                ],
            },
            # iso_42001_output intentionally omitted
        }

    def test_missing_iso_42001_output_halts_at_intake(self):
        """start_run() without iso_42001_output must halt at HALTED_INTAKE_INVALID."""
        from agents.governance_review_agent.runtime.state_manager import StateManager
        tid = self._orch.start_run("trigger", self._minimal_valid_inputs_without_iso())
        sm = StateManager(str(self._orch.runs_dir), tid)
        state = sm.load_state()
        self.assertEqual(state["status"], "HALTED_INTAKE_INVALID")

    def test_halted_intake_run_not_in_approval_pending(self):
        """A HALTED_INTAKE_INVALID run must not be in APPROVAL_PENDING (approval cannot proceed)."""
        from agents.governance_review_agent.runtime.state_manager import StateManager
        tid = self._orch.start_run("trigger", self._minimal_valid_inputs_without_iso())
        sm = StateManager(str(self._orch.runs_dir), tid)
        state = sm.load_state()
        self.assertNotEqual(state["status"], "APPROVAL_PENDING")

    def test_submit_approval_raises_for_halted_run(self):
        """submit_approval() on a HALTED_INTAKE_INVALID run must raise ValueError."""
        tid = self._orch.start_run("trigger", self._minimal_valid_inputs_without_iso())
        with self.assertRaises(ValueError):
            self._orch.submit_approval(tid, "Approve", "Test CSM", "Should not succeed")


if __name__ == "__main__":
    unittest.main()
