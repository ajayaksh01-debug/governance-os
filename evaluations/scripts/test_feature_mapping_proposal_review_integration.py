#!/usr/bin/env python3
"""
PR-004: Feature Mapping → Proposal Review Integration Test Suite.

Verifies that a schema-conformant Feature Mapping output (per the corrected
feature_mapping_output.json after PR-003) passes the Proposal Review intake
validator and correctly triggers TG-3 gate logic in the skill executor.

Before PR-003:
  feature_mapping_output.json required "technical_validation_map" (wrong field name)
  and used uppercase JSON Schema types ("OBJECT", "ARRAY", "STRING", "INTEGER").
  A valid Feature Mapping output would fail Proposal Review intake because
  proposal-review-input.schema.json requires "feature_validation_table".

After PR-003:
  Both schemas use "feature_validation_table". A schema-conformant FMO now
  passes Proposal Review intake. This suite proves the contract is sound.
"""

import json
import shutil
import sys
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root))
sys.path.append(str(repo_root / "agents" / "ethana_proposal_agent" / "runtime"))

from orchestrator import Orchestrator
from state_manager import StateManager
from audit_logger import AuditLogger


# Schema-conformant Feature Mapping output per the corrected feature_mapping_output.json.
# Requires both "feature_validation_table" (array) and "overall_tfs_score" (integer).
CONFORMANT_FMO = {
    "feature_validation_table": [
        {
            "proposed_feature": "AI Risk Monitoring Dashboard",
            "canonical_capability": "Risk Monitoring Dashboard",
            "integration_path": "Native API Integration",
            "tfs_score": 85,
            "poc_readiness": "Ready"
        },
        {
            "proposed_feature": "Model Explainability Reports",
            "canonical_capability": "Explainability Engine",
            "integration_path": "Sidecar Service",
            "tfs_score": 72,
            "poc_readiness": "Ready"
        }
    ],
    "overall_tfs_score": 78,
    "production_tfs_score": 78
}


class TestFeatureMappingProposalReviewIntegration(unittest.TestCase):
    """PR-004 integration suite: Feature Mapping → Proposal Review contract."""

    TRACE_ID = "TR-PR-TEST-PR004"

    def setUp(self):
        self.config_path = str(
            repo_root / "agents" / "ethana_proposal_agent" / "runtime" / "config.yaml"
        )
        self.orchestrator = Orchestrator(self.config_path)
        self.fmo_schema_path = repo_root / "workflows" / "schemas" / "feature_mapping_output.json"
        self.fmo_schema = json.loads(self.fmo_schema_path.read_text(encoding="utf-8"))
        self.pr_input_schema_path = (
            repo_root / "workflows" / "schemas" / "proposal-review-input.schema.json"
        )
        self.pr_input_schema = json.loads(self.pr_input_schema_path.read_text(encoding="utf-8"))
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        for path in [
            Path(self.orchestrator.runs_dir) / f"{self.TRACE_ID}_state.json",
            Path(self.orchestrator.logs_dir) / f"{self.TRACE_ID}_audit.jsonl",
        ]:
            if path.exists():
                path.unlink()
        pkg_dir = Path(self.orchestrator.packages_dir) / self.TRACE_ID
        if pkg_dir.exists():
            shutil.rmtree(pkg_dir)

    def _base_inputs(self, fmo: dict) -> dict:
        draft = (
            repo_root
            / "evaluations"
            / "test-cases"
            / "proposal-review"
            / "clean-proposal.md"
        ).read_text(encoding="utf-8")
        return {
            "draft_proposal": draft,
            "solution_mapping_output": {
                "matched_capabilities": [],
                "overall_coverage_summary": {},
            },
            "feature_mapping_output": fmo,
        }

    def _validate_against_schema(self, payload: dict, schema: dict) -> list:
        """Returns a list of error strings; empty means valid."""
        try:
            import jsonschema
            jsonschema.validate(instance=payload, schema=schema)
            return []
        except ImportError:
            errors = []
            for req in schema.get("required", []):
                if req not in payload:
                    errors.append(f"Missing required field: {req}")
            return errors
        except Exception as e:
            return [str(e)]

    # ------------------------------------------------------------------
    # PR-003 contract verification (schema-level assertions)
    # ------------------------------------------------------------------

    def test_fmo_schema_requires_feature_validation_table_not_technical_validation_map(self):
        """PR-003 Defect 1: feature_mapping_output.json must use feature_validation_table."""
        required = self.fmo_schema.get("required", [])
        self.assertIn("feature_validation_table", required)
        self.assertNotIn("technical_validation_map", required)

    def test_fmo_schema_uses_lowercase_types_throughout(self):
        """PR-003 Defect 2: all JSON Schema types in feature_mapping_output.json must be lowercase."""
        schema_text = self.fmo_schema_path.read_text(encoding="utf-8")
        for bad in ['"OBJECT"', '"ARRAY"', '"STRING"', '"INTEGER"', '"NUMBER"', '"BOOLEAN"']:
            self.assertNotIn(
                bad,
                schema_text,
                f"Uppercase type {bad} still present in feature_mapping_output.json",
            )

    def test_pr_input_schema_and_fmo_schema_share_feature_validation_table(self):
        """Both schemas agree on the field name: feature_validation_table."""
        fmo_required = self.fmo_schema.get("required", [])
        pr_fmo_props = (
            self.pr_input_schema.get("properties", {})
            .get("feature_mapping_output", {})
            .get("required", [])
        )
        self.assertIn("feature_validation_table", fmo_required)
        self.assertIn("feature_validation_table", pr_fmo_props)

    # ------------------------------------------------------------------
    # Fixture conformance
    # ------------------------------------------------------------------

    def test_conformant_fmo_satisfies_feature_mapping_output_schema(self):
        """CONFORMANT_FMO is valid per the corrected feature_mapping_output.json."""
        errors = self._validate_against_schema(CONFORMANT_FMO, self.fmo_schema)
        self.assertEqual(errors, [], f"CONFORMANT_FMO violates feature_mapping_output.json: {errors}")

    def test_conformant_fmo_satisfies_proposal_review_input_feature_mapping_sub_schema(self):
        """CONFORMANT_FMO satisfies the feature_mapping_output sub-schema in proposal-review-input."""
        sub_schema = (
            self.pr_input_schema.get("properties", {}).get("feature_mapping_output", {})
        )
        errors = self._validate_against_schema(CONFORMANT_FMO, sub_schema)
        self.assertEqual(
            errors,
            [],
            f"CONFORMANT_FMO violates proposal-review-input feature_mapping_output sub-schema: {errors}",
        )

    # ------------------------------------------------------------------
    # Intake gate: schema-conformant FMO must not trigger HALTED_INTAKE_INVALID
    # ------------------------------------------------------------------

    def test_conformant_fmo_passes_proposal_review_intake(self):
        """Schema-conformant FMO does not trigger HALTED_INTAKE_INVALID."""
        inputs = self._base_inputs(CONFORMANT_FMO)
        self.orchestrator.executor.generate_traceability_id = lambda: self.TRACE_ID
        self.orchestrator.start_run("new_proposal_review", inputs)

        state = StateManager(str(self.orchestrator.runs_dir), self.TRACE_ID).load_state()
        self.assertNotEqual(
            state["status"],
            "HALTED_INTAKE_INVALID",
            "Schema-conformant FMO must not be rejected at intake",
        )

    # ------------------------------------------------------------------
    # TG-3: traceability_gate_passed logic
    # ------------------------------------------------------------------

    def test_traceability_gate_passed_when_feature_validation_table_populated(self):
        """TG-3 passes when feature_validation_table is present and contains valid rows."""
        inputs = self._base_inputs(CONFORMANT_FMO)
        self.orchestrator.executor.generate_traceability_id = lambda: self.TRACE_ID
        self.orchestrator.start_run("new_proposal_review", inputs)

        state = StateManager(str(self.orchestrator.runs_dir), self.TRACE_ID).load_state()
        review_json = state["intermediate_data"]["proposal_review_json"]
        self.assertTrue(
            review_json["traceability_gate_passed"],
            "TG-3 must pass when feature_validation_table is present and populated",
        )

    def test_traceability_gate_fails_when_feature_validation_table_absent_from_fmo_object(self):
        """TG-3 fails when feature_mapping_output is an object but lacks feature_validation_table.

        The intake schema rejects a payload without feature_validation_table (it is a required
        field in proposal-review-input.schema.json). This path is exercised via executor direct
        call — the same pattern used by test_tg3_fail_when_feature_mapping_absent.
        """
        fmo_without_table = {"overall_tfs_score": 85}  # required field missing
        inputs = self._base_inputs(fmo_without_table)

        state_mgr = StateManager(str(self.orchestrator.runs_dir), self.TRACE_ID)
        logger = AuditLogger(str(self.orchestrator.logs_dir), self.TRACE_ID)
        state_mgr.initialize_run(inputs)

        result = self.orchestrator.executor.execute_proposal_review(state_mgr, inputs, logger)

        self.assertFalse(
            result["traceability_gate_passed"],
            "TG-3 must fail when feature_validation_table is absent from the FMO object",
        )
        self.assertEqual(result["classification"], "Rejected")
        self.assertEqual(result["cfb_count"], 0, "TG-3 gate failure must not set cfb_count")

    # ------------------------------------------------------------------
    # Full chain: FM → PR handoff reaches APPROVAL_PENDING
    # ------------------------------------------------------------------

    def test_end_to_end_fm_to_pr_handoff_reaches_approval_pending(self):
        """Full chain: schema-conformant FMO → Proposal Review → APPROVAL_PENDING.

        Before PR-003 this chain was broken: a Feature Mapping output would carry
        technical_validation_map but the Proposal Review runtime expected
        feature_validation_table, making the integration path unreachable. After
        PR-003 both schemas agree, and the full handoff completes without halt.
        """
        inputs = self._base_inputs(CONFORMANT_FMO)
        self.orchestrator.executor.generate_traceability_id = lambda: self.TRACE_ID
        self.orchestrator.start_run("new_proposal_review", inputs)

        state = StateManager(str(self.orchestrator.runs_dir), self.TRACE_ID).load_state()
        self.assertEqual(
            state["status"],
            "APPROVAL_PENDING",
            "Full FM→PR handoff with schema-conformant FMO must reach APPROVAL_PENDING",
        )


if __name__ == "__main__":
    unittest.main()
