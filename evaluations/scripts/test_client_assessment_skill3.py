#!/usr/bin/env python3
"""
Skill 3 (ethana-solution-mapping) executor + adapter tests.

Covers:
  - CCS band mapping from GCM coverage_classification
  - In Build / Aspirational -> CCS 0 hard rule
  - Cursory-covered -> Bridge to Cursory disposition
  - Aggregate CCS arithmetic identity
  - production_coverage_percent and coverage_characterization threshold
  - commercial motion decision tree (Platform-First / Advisory-First / Land-and-Expand)
  - quality_score decoupled from coverage CCS
  - schema conformance (solution_mapping_output)
  - real Claims Firewall: generated markdown is clean; an injected violation is caught
  - adapter upstream guard (missing skill_2_json)
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

from solution_mapping_executor import SolutionMappingExecutor  # noqa: E402
from skill_adapters import Skill3Adapter, SkillAdapterError  # noqa: E402
from state_manager import StateManager  # noqa: E402
from audit_logger import AuditLogger  # noqa: E402
from schema_validator import SchemaValidator  # noqa: E402


def _control(name, classification, control_type="Preventive"):
    return {
        "id": f"C-{abs(hash(name)) % 1000:03d}",
        "name": name,
        "control_type": control_type,
        "coverage_classification": classification,
        "platform_coverage": "Ethana" in classification,
    }


# Production-status canonical capability names (present in the CPM).
PROD_FULL = _control("Red Teaming Orchestrator", "Fully Covered by Ethana")
PROD_PARTIAL = _control("Immutable Audit Log", "Partially Covered by Ethana")
# "Ethana Workspace" is Aspirational in the canonical product model.
ASPIRATIONAL = _control("Ethana Workspace", "Fully Covered by Ethana")
# Cursory-covered control (no Ethana platform capability).
CURSORY = _control("Vendor Due Diligence Process", "Covered by Cursory Service")


class Skill3Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.runs = self.tmp / "runs"
        self.logs = self.tmp / "logs"
        self.runs.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)
        self.lg = AuditLogger(str(self.logs), "TR-CA-S3T-0001")
        self.sv = SchemaValidator(str(repo_root / "workflows" / "schemas"))
        self.exec = SolutionMappingExecutor(self.runs, self.logs)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, controls, **inputs):
        payload = {"control_mapping_output": {"controls": controls}}
        payload.update(inputs)
        return self.exec.execute_solution_mapping(payload, self.lg)


# ---------------------------------------------------------------------------
# CCS scoring + dispositions
# ---------------------------------------------------------------------------

class TestSkill3Scoring(Skill3Base):
    def test_fully_covered_production_high_ccs(self):
        out = self._run([PROD_FULL])
        m = out["matched_capabilities"][0]
        self.assertEqual(m["capability_status"], "Production")
        self.assertGreaterEqual(m["ccs_score"], 90)
        self.assertEqual(m["disposition"], "Include in proposal")

    def test_partially_covered_partial_ccs(self):
        out = self._run([PROD_PARTIAL])
        m = out["matched_capabilities"][0]
        self.assertEqual(m["capability_status"], "Production")
        self.assertTrue(50 <= m["ccs_score"] <= 69)

    def test_aspirational_forced_to_zero_ccs(self):
        out = self._run([ASPIRATIONAL])
        m = out["matched_capabilities"][0]
        self.assertEqual(m["capability_status"], "Aspirational")
        self.assertEqual(m["ccs_score"], 0)
        self.assertEqual(m["disposition"], "Gap register")

    def test_cursory_covered_bridge(self):
        out = self._run([CURSORY])
        m = out["matched_capabilities"][0]
        self.assertEqual(m["capability_status"], "Not addressed")
        self.assertEqual(m["disposition"], "Bridge to Cursory")
        self.assertLess(m["ccs_score"], 25)

    def test_aggregate_ccs_arithmetic_identity(self):
        out = self._run([PROD_FULL, PROD_PARTIAL, CURSORY])
        scores = [m["ccs_score"] for m in out["matched_capabilities"]]
        expected = round(sum(scores) / len(scores), 1)
        self.assertEqual(out["overall_ccs"], expected)


# ---------------------------------------------------------------------------
# Aggregation + motion
# ---------------------------------------------------------------------------

class TestSkill3Aggregation(Skill3Base):
    def test_platform_primary_and_platform_first(self):
        out = self._run([PROD_FULL, PROD_FULL, PROD_PARTIAL],
                        existing_policies="ISO 27001 certified")
        self.assertEqual(out["production_coverage_percent"], 100)
        self.assertEqual(
            out["overall_coverage_summary"]["coverage_characterization"],
            "Platform-Primary",
        )
        self.assertEqual(out["commercial_motion"], "Platform-First")

    def test_cursory_primary_and_advisory_first(self):
        out = self._run([CURSORY, CURSORY, ASPIRATIONAL])
        self.assertLess(out["production_coverage_percent"], 50)
        self.assertEqual(
            out["overall_coverage_summary"]["coverage_characterization"],
            "Cursory-Primary",
        )
        self.assertEqual(out["commercial_motion"], "Advisory-First")
        self.assertTrue(out["overall_coverage_summary"]["advisory_first_recommended"])

    def test_cert_blocker_forces_advisory_first(self):
        # Strong production coverage but a third-party cert gate with no posture.
        out = self._run([PROD_FULL, PROD_FULL],
                        existing_policies="No certifications yet",
                        target_certification="Third-party certification")
        self.assertEqual(out["commercial_motion"], "Advisory-First")

    def test_ccs_distribution_counts(self):
        out = self._run([PROD_FULL, PROD_PARTIAL, CURSORY])
        dist = out["overall_coverage_summary"]["ccs_distribution"]
        self.assertEqual(sum(dist.values()), 3)
        self.assertEqual(dist["full"], 1)
        self.assertEqual(dist["partial"], 1)
        self.assertEqual(dist["none"], 1)


# ---------------------------------------------------------------------------
# Quality-score decoupling + envelope
# ---------------------------------------------------------------------------

class TestSkill3QualityScore(Skill3Base):
    def test_quality_score_high_despite_low_coverage(self):
        out = self._run([CURSORY, CURSORY, ASPIRATIONAL],
                        regulatory_mapping_output={"applicable_regulations": [1]})
        self.assertLess(out["overall_ccs"], 25)        # coverage is poor
        self.assertGreaterEqual(out["quality_score"], 70)  # assessment quality still high

    def test_quality_penalty_without_regulatory_input(self):
        out = self._run([PROD_FULL, PROD_FULL, PROD_PARTIAL])  # no regulatory_mapping_output
        self.assertEqual(out["quality_score"], 80)  # 90 - 10

    def test_envelope_keys_present(self):
        out = self._run([PROD_FULL])
        for k in ("quality_score", "overall_ccs", "production_coverage_percent",
                  "commercial_motion", "markdown_output",
                  "matched_capabilities", "overall_coverage_summary"):
            self.assertIn(k, out)


# ---------------------------------------------------------------------------
# Schema + firewall
# ---------------------------------------------------------------------------

class TestSkill3SchemaAndFirewall(Skill3Base):
    def test_schema_conformance(self):
        out = self._run([PROD_FULL, PROD_PARTIAL, CURSORY, ASPIRATIONAL],
                        regulatory_mapping_output={"applicable_regulations": [1]})
        self.assertEqual(self.sv.validate(out, "solution_mapping_output"), [])

    def test_generated_markdown_is_firewall_clean(self):
        # Includes an Aspirational capability — must be disclosed, never claimed Production.
        out = self._run([PROD_FULL, PROD_PARTIAL, ASPIRATIONAL, CURSORY])
        violations = self._lint(out["markdown_output"])
        self.assertEqual(violations, 0, "Generated markdown leaked a firewall violation")

    def test_injected_violation_is_detected(self):
        # Sanity: the linter would catch an Aspirational-as-Production claim.
        bad_md = ("# Solution Mapping\n\n## 3. Proposal-Safe Platform Capabilities\n\n"
                  "The Ethana Workspace is in production today and fully deployed.\n")
        self.assertGreater(self._lint(bad_md), 0)

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


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

class TestSkill3Adapter(Skill3Base):
    def _state(self, with_skill_2=True):
        sm = StateManager(str(self.runs), "TR-CA-S3A-0001")
        sm.initialize_run({})
        if with_skill_2:
            sm.update_intermediate_data("skill_2_json", {"controls": [PROD_FULL, CURSORY]})
            sm.update_intermediate_data("skill_1_json", {"applicable_regulations": [1]})
        return sm

    def test_adapter_requires_skill_2_upstream(self):
        sm = self._state(with_skill_2=False)
        a = Skill3Adapter(self.runs, self.logs)
        with self.assertRaises(SkillAdapterError):
            a.execute(sm, {"industry": "BFSI"}, self.lg)

    def test_adapter_end_to_end(self):
        sm = self._state()
        a = Skill3Adapter(self.runs, self.logs)
        out = a.execute(sm, {"industry": "BFSI", "jurisdictions": ["EU"]}, self.lg)
        self.assertIn("overall_ccs", out)
        self.assertTrue(out["markdown_output"].strip())
        self.assertEqual(self.sv.validate(out, "solution_mapping_output"), [])

    def test_adapter_envelope_check_enforced(self):
        # Empty controls -> executor raises -> adapter wraps as SkillAdapterError.
        sm = StateManager(str(self.runs), "TR-CA-S3A-0002")
        sm.initialize_run({})
        sm.update_intermediate_data("skill_2_json", {"controls": []})
        a = Skill3Adapter(self.runs, self.logs)
        with self.assertRaises(SkillAdapterError):
            a.execute(sm, {}, self.lg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
