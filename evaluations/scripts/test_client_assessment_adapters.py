#!/usr/bin/env python3
"""
Adapter-layer tests for the Client Assessment Runtime (Option C, Phase 1).

Covers the four reuse adapters (Skills 1, 2, 5, 6):
  - Input mapping (CA vocabulary -> source vocabulary)
  - Output normalization (source keys -> CA envelope, markdown_output present)
  - Skill 6 classification 4->3 remap (table-driven)
  - Markdown sourcing (compiler for 1/2/5; state_mgr for 6)
  - Schema conformance against the real workflow schemas
  - Error contract (SkillAdapterError on missing upstream / unknown classification)
  - Skill 5 worst-case aggregation across multiple capabilities
"""

import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / "agents" / "client-assessment-agent" / "runtime"))
sys.path.append(str(repo_root))

from skill_adapters import (  # noqa: E402
    Skill1Adapter, Skill2Adapter, Skill4Adapter, Skill5Adapter, Skill6Adapter,
    SkillAdapterError, build_adapter_registry,
)
from state_manager import StateManager  # noqa: E402
from audit_logger import AuditLogger  # noqa: E402
from schema_validator import SchemaValidator  # noqa: E402


CA_INPUTS = {
    "client_ai_portfolio": (
        "Credit scoring AI for EU banking; high-risk; affects consumers; "
        "deployed in production with human oversight."
    ),
    "existing_policies": "ISO 27001 certified; partial AI governance framework.",
    "jurisdictions": ["EU", "UK"],
    "industry": "BFSI",
    "data_types": ["Personal", "Financial"],
    "target_maturity_level": "L3",
}


class AdapterTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.runs = self.tmp / "runs"
        self.logs = self.tmp / "logs"
        self.runs.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)
        self.sm = StateManager(str(self.runs), "TR-CA-ADP-0001")
        self.sm.initialize_run(dict(CA_INPUTS))
        self.lg = AuditLogger(str(self.logs), "TR-CA-ADP-0001")
        self.sv = SchemaValidator(str(repo_root / "workflows" / "schemas"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run_skill_1(self):
        out = Skill1Adapter(self.runs, self.logs).execute(self.sm, CA_INPUTS, self.lg)
        self.sm.update_intermediate_data("skill_1_json", out)
        self.sm.update_intermediate_data("skill_1_md", out["markdown_output"])
        return out

    def _run_skill_2(self):
        out = Skill2Adapter(self.runs, self.logs).execute(self.sm, CA_INPUTS, self.lg)
        self.sm.update_intermediate_data("skill_2_json", out)
        self.sm.update_intermediate_data("skill_2_md", out["markdown_output"])
        return out


# ---------------------------------------------------------------------------
# Skill 1 adapter
# ---------------------------------------------------------------------------

class TestSkill1Adapter(AdapterTestBase):
    def test_input_mapping_prefixes_existing_policies(self):
        a = Skill1Adapter(self.runs, self.logs)
        mapped = a.map_inputs(CA_INPUTS, {})
        self.assertIn("subject_description", mapped)
        self.assertIn("Existing governance context:", mapped["subject_description"])
        self.assertEqual(mapped["industry"], "BFSI")
        self.assertEqual(mapped["jurisdictions"], ["EU", "UK"])

    def test_output_envelope_and_score_rename(self):
        out = self._run_skill_1()
        self.assertIn("quality_score", out)  # renamed from source "score"
        self.assertIsInstance(out["quality_score"], int)
        self.assertTrue(out["markdown_output"].strip())

    def test_schema_conformance(self):
        out = self._run_skill_1()
        self.assertEqual(self.sv.validate(out, "regulatory_mapping_output"), [])


# ---------------------------------------------------------------------------
# Skill 2 adapter
# ---------------------------------------------------------------------------

class TestSkill2Adapter(AdapterTestBase):
    def test_requires_skill_1_upstream(self):
        a = Skill2Adapter(self.runs, self.logs)
        with self.assertRaises(SkillAdapterError):
            a.execute(self.sm, CA_INPUTS, self.lg)  # no skill_1_json yet

    def test_controls_reshape_includes_platform_coverage(self):
        self._run_skill_1()
        out = self._run_skill_2()
        self.assertIn("controls", out)
        self.assertGreater(len(out["controls"]), 0)
        for c in out["controls"]:
            self.assertIn("platform_coverage", c)
            self.assertIsInstance(c["platform_coverage"], bool)

    def test_output_envelope_and_score_rename(self):
        self._run_skill_1()
        out = self._run_skill_2()
        self.assertIn("quality_score", out)
        self.assertTrue(out["markdown_output"].strip())

    def test_schema_conformance(self):
        self._run_skill_1()
        out = self._run_skill_2()
        self.assertEqual(self.sv.validate(out, "control_mapping_output"), [])


# ---------------------------------------------------------------------------
# Skill 5 adapter
# ---------------------------------------------------------------------------

class TestSkill5Adapter(AdapterTestBase):
    def test_requires_a_capability(self):
        a = Skill5Adapter(self.runs, self.logs)
        with self.assertRaises(SkillAdapterError):
            a.execute(self.sm, CA_INPUTS, self.lg)  # no capability provided

    def test_claim_context_is_schema_valid(self):
        a = Skill5Adapter(self.runs, self.logs)
        mapped = a.map_inputs({**CA_INPUTS, "capability_name": "X"}, {})
        self.assertEqual(mapped["per_capability_inputs"][0]["claim_context"],
                         "Formal Proposal")

    def test_output_envelope_and_markdown(self):
        a = Skill5Adapter(self.runs, self.logs)
        out = a.execute(self.sm, {**CA_INPUTS, "capability_name": "Red Teaming Orchestrator"}, self.lg)
        self.assertIn("ecs", out)
        self.assertIn("escalation_required", out)
        self.assertTrue(out["markdown_output"].strip())

    def test_schema_conformance(self):
        a = Skill5Adapter(self.runs, self.logs)
        out = a.execute(self.sm, {**CA_INPUTS, "capability_name": "Red Teaming Orchestrator"}, self.lg)
        self.assertEqual(self.sv.validate(out, "capability_validation_output"), [])

    def test_worst_case_aggregation_prefers_escalation(self):
        # Two capabilities: one clean, one that escalates. Worst-case must win.
        a = Skill5Adapter(self.runs, self.logs)
        caps = {"capabilities": [
            {"capability_name": "Red Teaming Orchestrator", "proposed_claim": "in production"},
            {"capability_name": "Ethana Workspace", "proposed_claim": "in production"},
        ]}
        out = a.execute(self.sm, {**CA_INPUTS, **caps}, self.lg)
        self.assertEqual(len(out["all_capability_results"]), 2)
        # Aggregated payload must reflect a non-Production / lower-trust capability.
        self.assertNotEqual(out["validated_status"], "Production")


# ---------------------------------------------------------------------------
# Skill 6 adapter
# ---------------------------------------------------------------------------

class TestSkill6Adapter(AdapterTestBase):
    def _prep_upstream(self):
        self._run_skill_1()
        self._run_skill_2()
        s5 = Skill5Adapter(self.runs, self.logs).execute(
            self.sm, {**CA_INPUTS, "capability_name": "Red Teaming Orchestrator"}, self.lg)
        self.sm.update_intermediate_data("skill_5_json", s5)
        self.sm.update_intermediate_data("skill_5_md", s5["markdown_output"])

    def test_classification_remap_table(self):
        a = Skill6Adapter(self.runs, self.logs)
        self.assertEqual(a.CLASSIFICATION_MAP["Approved"], "Approved")
        self.assertEqual(a.CLASSIFICATION_MAP["Approved with Revisions"], "Conditional")
        self.assertEqual(a.CLASSIFICATION_MAP["Conditional Release"], "Conditional")
        self.assertEqual(a.CLASSIFICATION_MAP["Rejected"], "Rejected")

    def test_map_output_remaps_classification(self):
        a = Skill6Adapter(self.runs, self.logs)
        for source_val, ca_val in [
            ("Approved", "Approved"),
            ("Approved with Revisions", "Conditional"),
            ("Conditional Release", "Conditional"),
            ("Rejected", "Rejected"),
        ]:
            self.sm.update_intermediate_data("proposal_review_md", "# Review\n\nbody")
            raw = {"pcs": 90, "ctcs": 85, "classification": source_val}
            out = a.map_output(raw, {}, None, self.sm)
            self.assertEqual(out["release_classification"], ca_val)

    def test_unknown_classification_raises(self):
        a = Skill6Adapter(self.runs, self.logs)
        self.sm.update_intermediate_data("proposal_review_md", "# Review")
        with self.assertRaises(SkillAdapterError):
            a.map_output({"pcs": 1, "ctcs": 1, "classification": "Bogus"}, {}, None, self.sm)

    def test_markdown_sourced_from_state_mgr(self):
        self._prep_upstream()
        a = Skill6Adapter(self.runs, self.logs)
        out = a.execute(self.sm, CA_INPUTS, self.lg)
        # Source writes proposal_review_md into state; adapter must surface it.
        state_md = self.sm.get_state()["intermediate_data"].get("proposal_review_md", "")
        self.assertTrue(out["markdown_output"].strip())
        self.assertEqual(out["markdown_output"], state_md)

    def test_output_envelope(self):
        self._prep_upstream()
        a = Skill6Adapter(self.runs, self.logs)
        out = a.execute(self.sm, CA_INPUTS, self.lg)
        for k in ("pcs", "ctcs", "release_classification", "markdown_output"):
            self.assertIn(k, out)

    def test_schema_conformance(self):
        self._prep_upstream()
        a = Skill6Adapter(self.runs, self.logs)
        out = a.execute(self.sm, CA_INPUTS, self.lg)
        self.assertEqual(self.sv.validate(out, "proposal_review_output"), [])


# ---------------------------------------------------------------------------
# Strict additionalProperties:false contract (regression for the Skill 4/5/6
# envelope-field schema collision). The runtime's fallback validator ignores
# additionalProperties, so these tests assert directly that no adapter output
# key falls outside the schema's declared properties.
# ---------------------------------------------------------------------------

class TestStrictAdditionalPropertiesContract(AdapterTestBase):
    def _schema_props(self, filename: str) -> set:
        path = repo_root / "workflows" / "schemas" / filename
        schema = json.loads(path.read_text())
        return set(schema.get("properties", {}).keys()), schema.get("additionalProperties")

    def _assert_no_extra_keys(self, out: dict, filename: str):
        allowed, addl = self._schema_props(filename)
        # Only strict (additionalProperties:false) schemas constrain extra keys.
        self.assertIs(addl, False, f"{filename} is expected to be strict")
        extra = sorted(set(out.keys()) - allowed)
        self.assertEqual(
            extra, [],
            f"{filename}: adapter emitted keys outside the strict schema: {extra}",
        )

    def test_skill5_output_has_no_keys_outside_strict_schema(self):
        out = Skill5Adapter(self.runs, self.logs).execute(
            self.sm, {**CA_INPUTS, "capability_name": "Red Teaming Orchestrator"}, self.lg)
        self._assert_no_extra_keys(out, "ethana-capability-validation-output.schema.json")

    def test_skill5_markdown_and_aggregation_are_declared(self):
        allowed, _ = self._schema_props("ethana-capability-validation-output.schema.json")
        self.assertIn("markdown_output", allowed)
        self.assertIn("all_capability_results", allowed)

    def test_skill6_output_has_no_keys_outside_strict_schema(self):
        self._run_skill_1()
        self._run_skill_2()
        s5 = Skill5Adapter(self.runs, self.logs).execute(
            self.sm, {**CA_INPUTS, "capability_name": "Red Teaming Orchestrator"}, self.lg)
        self.sm.update_intermediate_data("skill_5_json", s5)
        self.sm.update_intermediate_data("skill_5_md", s5["markdown_output"])
        out = Skill6Adapter(self.runs, self.logs).execute(self.sm, CA_INPUTS, self.lg)
        self._assert_no_extra_keys(out, "proposal-review-output.schema.json")

    def test_skill6_release_classification_and_markdown_declared(self):
        allowed, _ = self._schema_props("proposal-review-output.schema.json")
        self.assertIn("release_classification", allowed)
        self.assertIn("markdown_output", allowed)

    def test_skill4_output_has_no_keys_outside_strict_schema(self):
        self._run_skill_1()
        self._run_skill_2()
        out = Skill4Adapter(self.runs, self.logs).execute(self.sm, CA_INPUTS, self.lg)
        self._assert_no_extra_keys(out, "iso-42001-gap-assessment-output.schema.json")


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class TestAdapterRegistry(AdapterTestBase):
    def test_registry_has_all_six_skills_wired(self):
        reg = build_adapter_registry(self.runs, self.logs)
        self.assertEqual(set(reg.keys()), {1, 2, 3, 4, 5, 6, "fm"})

    def test_net_new_skills_3_and_4_wired(self):
        reg = build_adapter_registry(self.runs, self.logs)
        self.assertIn(3, reg)
        self.assertIn(4, reg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
