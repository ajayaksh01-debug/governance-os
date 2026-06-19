#!/usr/bin/env python3
"""
Skill 4 (iso-42001-gap-assessment) executor + adapter tests.

Covers:
  - AMS arithmetic identity (clause 0.60 + annex 0.40)
  - ARS weighted identity (0.30/0.40/0.20/0.10)
  - Classification table rows
  - HD6 override (Critical gap precludes Certification Ready)
  - Gap register generation + ID scheme + EU/BFSI severity elevation
  - months_to_readiness formula
  - quality_score decoupled from AMS/ARS
  - ISO 27001 Annex SL credit raises Clauses 4-7
  - schema conformance (post envelope-field extension)
  - real Claims Firewall: generated Section 8.5 markdown is clean
  - adapter upstream guard (empty ai_portfolio)
"""

import os
import sys
import shutil
import tempfile
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / "agents" / "client-assessment-agent" / "runtime"))
sys.path.insert(0, str(repo_root / "agents" / "client-assessment-agent" / "runtime" / "skills"))
sys.path.append(str(repo_root))
sys.path.append(str(repo_root / "evaluations" / "scripts"))

from iso42001_executor import (  # noqa: E402
    Iso42001GapAssessmentExecutor, _CLAUSES,
)
from skill_adapters import Skill4Adapter, SkillAdapterError  # noqa: E402
from state_manager import StateManager  # noqa: E402
from audit_logger import AuditLogger  # noqa: E402
from schema_validator import SchemaValidator  # noqa: E402


STRONG_INPUTS = {
    "ai_portfolio": "Credit scoring AI; EU banking; high-risk model",
    "organisation_description": (
        "Acme Bank. AI policy signed by leadership; AIMS scope documented; "
        "risk assessment and impact assessment complete; statement of applicability; "
        "internal audit programme; management review minutes; board AI committee; "
        "monitoring and drift detection; corrective action process; ISO 27001 certified"
    ),
    "existing_policies": "ISO 27001 certified; AI policy; internal audit",
    "existing_documentation": (
        "AI policy, scope, risk assessment, impact assessment, statement of "
        "applicability, internal audit, board committee, management review, "
        "monitoring, corrective action, ai objectives"
    ),
    "control_mapping_output": {
        "controls": [{"platform_coverage": True}] * 30 + [{"platform_coverage": False}] * 8
    },
    "regulatory_mapping_output": {"applicable_regulations": [1]},
    "jurisdictions": ["EU"],
    "industry": "BFSI",
    "target_certification": "Third-party certification",
}

WEAK_INPUTS = {
    "ai_portfolio": "Customer-service chatbot pilot",
    "organisation_description": "Early-stage startup; no formal AI policy yet",
    "existing_policies": "",
    "existing_documentation": "",
    "control_mapping_output": {"controls": []},
    "jurisdictions": ["EU"],
    "industry": "BFSI",
}


class Skill4Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.runs = self.tmp / "runs"
        self.logs = self.tmp / "logs"
        self.runs.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)
        self.lg = AuditLogger(str(self.logs), "TR-CA-S4T-0001")
        self.sv = SchemaValidator(str(repo_root / "workflows" / "schemas"))
        self.exec = Iso42001GapAssessmentExecutor(self.runs, self.logs)


# ---------------------------------------------------------------------------
# AMS / ARS arithmetic
# ---------------------------------------------------------------------------

class TestSkill4Scoring(Skill4Base):
    def test_ams_arithmetic_identity(self):
        o = self.exec.execute_gap_assessment(STRONG_INPUTS, self.lg)
        clause_score = sum(o["ams_clause_scores"].values()) / 7 * 20
        a = o["annex_a_coverage"]
        annex_score = (a["implemented"] + 0.5 * a["partially_implemented"]) / a["total_applicable"] * 100
        expected = round(clause_score * 0.60 + annex_score * 0.40, 1)
        self.assertEqual(o["ams"], expected)
        self.assertTrue(0 <= o["ams"] <= 100)

    def test_ars_weighted_identity(self):
        o = self.exec.execute_gap_assessment(STRONG_INPUTS, self.lg)
        c = o["ars_component_scores"]
        expected = round(
            c["documentation_completeness"] * 0.30
            + c["evidence_availability"] * 0.40
            + c["control_operationalization"] * 0.20
            + c["management_review_readiness"] * 0.10, 1)
        self.assertEqual(o["ars"], expected)

    def test_iso27001_credit_raises_management_clauses(self):
        with_iso = self.exec.execute_gap_assessment(STRONG_INPUTS, self.lg)
        without = dict(STRONG_INPUTS)
        without["existing_documentation"] = without["existing_documentation"].replace("ISO 27001 certified", "")
        without["existing_policies"] = ""
        o2 = self.exec.execute_gap_assessment(without, self.lg)
        # Clause 4 (management-system clause) should be >= without the ISO 27001 credit.
        self.assertGreaterEqual(with_iso["ams_clause_scores"]["clause_4"],
                                o2["ams_clause_scores"]["clause_4"])


# ---------------------------------------------------------------------------
# Classification + HD6
# ---------------------------------------------------------------------------

class TestSkill4Classification(Skill4Base):
    def test_certification_ready_row(self):
        self.assertEqual(self.exec._classify(85, 80, 0), "Certification Ready")

    def test_near_ready_row(self):
        self.assertEqual(self.exec._classify(65, 65, 1), "Near Ready")

    def test_significant_gaps_row(self):
        self.assertEqual(self.exec._classify(50, 50, 4), "Significant Gaps")

    def test_major_gaps_row(self):
        self.assertEqual(self.exec._classify(30, 20, 8), "Major Gaps")

    def test_hd6_critical_gap_blocks_certification_ready(self):
        # High AMS + ARS but a Critical gap -> must NOT be Certification Ready.
        self.assertNotEqual(self.exec._classify(90, 85, 1), "Certification Ready")

    def test_weak_client_major_gaps(self):
        o = self.exec.execute_gap_assessment(WEAK_INPUTS, self.lg)
        self.assertIn(o["certification_classification"],
                      ["Significant Gaps", "Major Gaps"])


# ---------------------------------------------------------------------------
# Gap register + months
# ---------------------------------------------------------------------------

class TestSkill4Gaps(Skill4Base):
    def test_gap_id_scheme(self):
        o = self.exec.execute_gap_assessment(WEAK_INPUTS, self.lg)
        self.assertGreater(len(o["gap_ids"]), 0)
        for gid in o["gap_ids"]:
            self.assertTrue(gid.startswith("GAP-CL") or gid.startswith("GAP-AA"))

    def test_critical_gap_ids_subset(self):
        o = self.exec.execute_gap_assessment(WEAK_INPUTS, self.lg)
        self.assertEqual(o["critical_gaps"], len(o["critical_gap_ids"]))
        self.assertTrue(set(o["critical_gap_ids"]).issubset(set(o["gap_ids"])))

    def test_months_to_readiness_formula(self):
        o = self.exec.execute_gap_assessment(WEAK_INPUTS, self.lg)
        expected = min(2 * o["critical_gaps"] + o["major_gaps"], 24)
        self.assertEqual(o["months_to_readiness"], expected)

    def test_certification_ready_zero_months(self):
        self.assertEqual(self.exec._months_to_readiness(0, 0, "Certification Ready"), 0)

    def test_eu_high_risk_elevation_produces_critical(self):
        # Weak EU high-risk client: elevated clauses 6/8 should yield Critical gaps.
        o = self.exec.execute_gap_assessment(WEAK_INPUTS, self.lg)
        self.assertGreater(o["critical_gaps"], 0)


# ---------------------------------------------------------------------------
# Quality score decoupling + envelope + schema
# ---------------------------------------------------------------------------

class TestSkill4Envelope(Skill4Base):
    def test_quality_score_high_despite_low_ams(self):
        o = self.exec.execute_gap_assessment(WEAK_INPUTS, self.lg)
        self.assertLess(o["ams"], 40)             # genuinely low maturity
        self.assertGreaterEqual(o["quality_score"], 70)  # assessment still high quality

    def test_quality_penalty_missing_upstream(self):
        # Both upstreams genuinely absent -> 92 - 12 - 8 = 72.
        bare = {"ai_portfolio": "Chatbot pilot", "jurisdictions": ["EU"], "industry": "BFSI"}
        o = self.exec.execute_gap_assessment(bare, self.lg)
        self.assertEqual(o["quality_score"], 72)

    def test_quality_penalty_only_regulatory_missing(self):
        # control_mapping_output present (even if empty) -> only the -12 applies.
        o = self.exec.execute_gap_assessment(WEAK_INPUTS, self.lg)
        self.assertEqual(o["quality_score"], 80)  # 92 - 12

    def test_empty_portfolio_raises(self):
        bad = dict(STRONG_INPUTS)
        bad["ai_portfolio"] = "   "
        with self.assertRaises(ValueError):
            self.exec.execute_gap_assessment(bad, self.lg)

    def test_schema_conformance_strong(self):
        o = self.exec.execute_gap_assessment(STRONG_INPUTS, self.lg)
        self.assertEqual(self.sv.validate(o, "iso42001_output"), [])

    def test_schema_conformance_weak(self):
        o = self.exec.execute_gap_assessment(WEAK_INPUTS, self.lg)
        self.assertEqual(self.sv.validate(o, "iso42001_output"), [])

    def test_envelope_keys_present(self):
        o = self.exec.execute_gap_assessment(STRONG_INPUTS, self.lg)
        for k in ("ams", "ars", "critical_gaps", "major_gaps", "minor_gaps",
                  "certification_classification", "months_to_readiness",
                  "quality_score", "markdown_output"):
            self.assertIn(k, o)


# ---------------------------------------------------------------------------
# Firewall + adapter
# ---------------------------------------------------------------------------

class TestSkill4FirewallAndAdapter(Skill4Base):
    def _lint(self, md: str) -> int:
        from claims_linter import parse_canonical_model, lint_file
        cpm = parse_canonical_model(Path(repo_root / "knowledge" / "ethana" / "canonical-product-model.md"))
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(md)
            p = f.name
        try:
            return len(lint_file(Path(p), cpm))
        finally:
            os.unlink(p)

    def test_markdown_section_8_5_is_firewall_clean(self):
        o = self.exec.execute_gap_assessment(STRONG_INPUTS, self.lg)
        self.assertEqual(self._lint(o["markdown_output"]), 0)

    def test_adapter_requires_ai_portfolio(self):
        sm = StateManager(str(self.runs), "TR-CA-S4A-0001")
        sm.initialize_run({})
        a = Skill4Adapter(self.runs, self.logs)
        with self.assertRaises(SkillAdapterError):
            a.execute(sm, {"client_ai_portfolio": ""}, self.lg)

    def test_adapter_end_to_end(self):
        sm = StateManager(str(self.runs), "TR-CA-S4A-0002")
        sm.initialize_run({})
        sm.update_intermediate_data("skill_1_json", {"applicable_regulations": [1]})
        sm.update_intermediate_data("skill_2_json", {"controls": [{"platform_coverage": True}] * 20})
        a = Skill4Adapter(self.runs, self.logs)
        out = a.execute(sm, {
            "client_ai_portfolio": "Credit scoring AI; EU banking; high-risk",
            "client_name": "Acme", "existing_policies": "ISO 27001; AI policy; internal audit",
            "jurisdictions": ["EU"], "industry": "BFSI",
        }, self.lg)
        self.assertIn("ams", out)
        self.assertTrue(out["markdown_output"].strip())
        self.assertEqual(self.sv.validate(out, "iso42001_output"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
