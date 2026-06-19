#!/usr/bin/env python3
"""
Suite A — FeatureMappingExecutor unit tests (PR-006 Phase 3).

Covers:
  - TFS band mapping (all bands, boundary values, non-Production always 0)
  - POC readiness enum (all five statuses + unknown fallback)
  - Integration path routing (all deployment variants + canonical-name lookup)
  - Aggregation (overall_tfs_score, production_tfs_score, empty-input guard)
  - Quality score computation (all deduction combos, floor, type)
  - Error paths (empty caps, missing key, non-numeric ccs_score)

CPM fixture strategy: executor._cpm = {} for all tests except canonical-name
lookup tests, which use MINIMAL_CPM (2-entry dict injected the same way).
No file I/O and no mocking of parse_canonical_model.
"""

import shutil
import tempfile
import unittest
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / "agents" / "client-assessment-agent" / "runtime" / "skills"))
sys.path.insert(0, str(repo_root / "agents" / "client-assessment-agent" / "runtime"))
sys.path.append(str(repo_root))

from feature_mapping_executor import FeatureMappingExecutor  # noqa: E402


# Two-entry CPM for canonical-name lookup tests only.
MINIMAL_CPM = {
    "audit log": {
        "original_name": "Audit Log",
        "status": "production",
    },
    "pii scanner": {
        "original_name": "PII Scanner",
        "status": "in build",
    },
}


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class FMExecutorTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.runs = self.tmp / "runs"
        self.logs = self.tmp / "logs"
        self.runs.mkdir(parents=True)
        self.logs.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _make_executor(self, cpm=None):
        exe = FeatureMappingExecutor(str(self.runs), str(self.logs))
        exe._cpm = {} if cpm is None else cpm
        return exe

    def _run(self, matched_capabilities,
             deployment_constraint="Cloud",
             customer_sector="BFSI",
             poc_duration="30 days",
             cpm=None):
        exe = self._make_executor(cpm)
        return exe.execute_feature_mapping({
            "matched_capabilities": matched_capabilities,
            "deployment_constraint": deployment_constraint,
            "customer_sector": customer_sector,
            "poc_duration": poc_duration,
        })

    def _row(self, cap_status="Production", ccs_score=90, matched_cap="Test Feature"):
        return {
            "capability_status": cap_status,
            "ccs_score": ccs_score,
            "matched_capability": matched_cap,
        }


# ---------------------------------------------------------------------------
# TestFMScoring
# ---------------------------------------------------------------------------

class TestFMScoring(FMExecutorTestBase):
    """TFS band mapping via _tfs_from_ccs (static) and through execute."""

    # --- Full band (CCS >= 90 → TFS 92) ---

    def test_ccs_90_maps_to_92(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(90), 92)

    def test_ccs_95_maps_to_92(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(95), 92)

    def test_ccs_100_maps_to_92(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(100), 92)

    # --- High band (CCS 70–89 → TFS 80) ---

    def test_ccs_70_maps_to_80(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(70), 80)

    def test_ccs_75_maps_to_80(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(75), 80)

    def test_ccs_89_maps_to_80(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(89), 80)

    # --- Partial band (CCS 50–69 → TFS 58) ---

    def test_ccs_50_maps_to_58(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(50), 58)

    def test_ccs_69_maps_to_58(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(69), 58)

    # --- Thin band (CCS 25–49 → TFS 35) ---

    def test_ccs_25_maps_to_35(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(25), 35)

    def test_ccs_49_maps_to_35(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(49), 35)

    # --- None band (CCS < 25 → TFS 0) ---

    def test_ccs_0_maps_to_0(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(0), 0)

    def test_ccs_24_maps_to_0(self):
        self.assertEqual(FeatureMappingExecutor._tfs_from_ccs(24), 0)

    # --- Non-Production statuses always yield TFS 0 (via execute) ---

    def test_in_build_tfs_always_zero(self):
        result = self._run([self._row("In Build", 95)])
        self.assertEqual(result["feature_validation_table"][0]["tfs_score"], 0)

    def test_roadmap_tfs_always_zero(self):
        result = self._run([self._row("Roadmap", 95)])
        self.assertEqual(result["feature_validation_table"][0]["tfs_score"], 0)

    def test_aspirational_tfs_always_zero(self):
        result = self._run([self._row("Aspirational", 95)])
        self.assertEqual(result["feature_validation_table"][0]["tfs_score"], 0)

    def test_not_addressed_tfs_always_zero(self):
        result = self._run([self._row("Not addressed", 95)])
        self.assertEqual(result["feature_validation_table"][0]["tfs_score"], 0)


# ---------------------------------------------------------------------------
# TestFMPocReadiness
# ---------------------------------------------------------------------------

class TestFMPocReadiness(FMExecutorTestBase):
    """POC readiness enum mapping via _poc_readiness (static) and through execute."""

    def test_production_maps_to_ready(self):
        self.assertEqual(FeatureMappingExecutor._poc_readiness("Production"), "Ready")

    def test_in_build_maps_to_roadmap_blocked(self):
        self.assertEqual(FeatureMappingExecutor._poc_readiness("In Build"), "Roadmap-Blocked")

    def test_roadmap_maps_to_roadmap_blocked(self):
        self.assertEqual(FeatureMappingExecutor._poc_readiness("Roadmap"), "Roadmap-Blocked")

    def test_aspirational_maps_to_incompatible(self):
        self.assertEqual(FeatureMappingExecutor._poc_readiness("Aspirational"), "Incompatible")

    def test_not_addressed_maps_to_incompatible(self):
        self.assertEqual(FeatureMappingExecutor._poc_readiness("Not addressed"), "Incompatible")

    def test_unknown_status_maps_to_incompatible(self):
        self.assertEqual(FeatureMappingExecutor._poc_readiness("UnknownStatus"), "Incompatible")

    def test_poc_readiness_in_all_table_rows(self):
        rows = [
            self._row("Production", 90),
            self._row("In Build", 80),
            self._row("Aspirational", 70),
        ]
        result = self._run(rows)
        fvt = result["feature_validation_table"]
        self.assertEqual(fvt[0]["poc_readiness"], "Ready")
        self.assertEqual(fvt[1]["poc_readiness"], "Roadmap-Blocked")
        self.assertEqual(fvt[2]["poc_readiness"], "Incompatible")


# ---------------------------------------------------------------------------
# TestFMIntegrationPath
# ---------------------------------------------------------------------------

class TestFMIntegrationPath(FMExecutorTestBase):
    """Integration path routing and canonical-name lookup."""

    def _exe(self):
        return self._make_executor()

    # --- Deployment constraint routing (Production status) ---

    def test_on_premise_connector_dash_variant(self):
        self.assertEqual(
            self._exe()._integration_path("Production", "On-Premise"), "On-Premise Connector"
        )

    def test_on_prem_underscore_variant(self):
        self.assertEqual(
            self._exe()._integration_path("Production", "on_prem_deployment"), "On-Premise Connector"
        )

    def test_on_premise_space_variant(self):
        self.assertEqual(
            self._exe()._integration_path("Production", "on premise"), "On-Premise Connector"
        )

    def test_hybrid_bridge(self):
        self.assertEqual(
            self._exe()._integration_path("Production", "Hybrid Cloud"), "Hybrid Bridge"
        )

    def test_cloud_returns_native_api(self):
        self.assertEqual(
            self._exe()._integration_path("Production", "Cloud"), "Native API"
        )

    def test_empty_constraint_returns_native_api(self):
        self.assertEqual(
            self._exe()._integration_path("Production", ""), "Native API"
        )

    def test_none_constraint_returns_native_api(self):
        self.assertEqual(
            self._exe()._integration_path("Production", None), "Native API"
        )

    # --- Non-Production always returns Not applicable ---

    def test_in_build_returns_not_applicable(self):
        self.assertEqual(
            self._exe()._integration_path("In Build", "Cloud"), "Not applicable"
        )

    def test_aspirational_returns_not_applicable(self):
        self.assertEqual(
            self._exe()._integration_path("Aspirational", "On-Premise"), "Not applicable"
        )

    # --- Canonical name lookup (MINIMAL_CPM) ---

    def test_canonical_name_lookup_hit(self):
        result = self._run(
            [self._row("Production", 90, "Audit Log")],
            cpm=MINIMAL_CPM,
        )
        self.assertEqual(
            result["feature_validation_table"][0]["canonical_capability"], "Audit Log"
        )

    def test_canonical_name_fallback_when_no_match(self):
        result = self._run(
            [self._row("Production", 90, "Unknown Feature XYZ")],
            cpm=MINIMAL_CPM,
        )
        self.assertEqual(
            result["feature_validation_table"][0]["canonical_capability"], "Unknown Feature XYZ"
        )

    def test_canonical_name_with_empty_cpm_returns_original(self):
        result = self._run(
            [self._row("Production", 90, "Audit Log")],
            cpm={},
        )
        self.assertEqual(
            result["feature_validation_table"][0]["canonical_capability"], "Audit Log"
        )


# ---------------------------------------------------------------------------
# TestFMAggregation
# ---------------------------------------------------------------------------

class TestFMAggregation(FMExecutorTestBase):
    """overall_tfs_score and production_tfs_score computation."""

    def test_overall_tfs_includes_zeros_from_non_production(self):
        # Production CCS=90 → TFS 92; In Build → TFS 0; mean = 46
        result = self._run([self._row("Production", 90), self._row("In Build", 90)])
        self.assertEqual(result["overall_tfs_score"], 46)

    def test_production_tfs_excludes_non_ready_rows(self):
        # Only the Production row (TFS 92) counts
        result = self._run([self._row("Production", 90), self._row("In Build", 90)])
        self.assertEqual(result["production_tfs_score"], 92)

    def test_production_tfs_zero_when_no_ready_rows(self):
        result = self._run([self._row("In Build", 95), self._row("Aspirational", 80)])
        self.assertEqual(result["production_tfs_score"], 0)

    def test_overall_tfs_zero_when_all_non_production(self):
        result = self._run([self._row("Aspirational", 95), self._row("In Build", 80)])
        self.assertEqual(result["overall_tfs_score"], 0)

    def test_single_production_row_equals_that_tfs(self):
        # CCS 70 → TFS 80
        result = self._run([self._row("Production", 70)])
        self.assertEqual(result["overall_tfs_score"], 80)
        self.assertEqual(result["production_tfs_score"], 80)

    def test_multiple_production_rows_averaged(self):
        # CCS 90 → 92; CCS 70 → 80; mean = (92+80)/2 = 86
        result = self._run([self._row("Production", 90), self._row("Production", 70)])
        self.assertEqual(result["overall_tfs_score"], 86)
        self.assertEqual(result["production_tfs_score"], 86)

    def test_tfs_scores_are_integers(self):
        result = self._run([self._row("Production", 90)])
        self.assertIsInstance(result["overall_tfs_score"], int)
        self.assertIsInstance(result["production_tfs_score"], int)

    def test_empty_matched_capabilities_raises_before_aggregation(self):
        exe = self._make_executor()
        with self.assertRaises(ValueError):
            exe.execute_feature_mapping({"matched_capabilities": []})


# ---------------------------------------------------------------------------
# TestFMQualityScore
# ---------------------------------------------------------------------------

class TestFMQualityScore(FMExecutorTestBase):
    """quality_score computation: base 90, -10 per missing contextual input, floor 70."""

    def test_both_present_returns_90(self):
        result = self._run(
            [self._row()],
            deployment_constraint="Cloud",
            poc_duration="30 days",
        )
        self.assertEqual(result["quality_score"], 90)

    def test_no_deployment_constraint_deducts_10(self):
        result = self._run(
            [self._row()],
            deployment_constraint="",
            poc_duration="30 days",
        )
        self.assertEqual(result["quality_score"], 80)

    def test_no_poc_duration_deducts_10(self):
        result = self._run(
            [self._row()],
            deployment_constraint="Cloud",
            poc_duration="",
        )
        self.assertEqual(result["quality_score"], 80)

    def test_neither_present_returns_floor_70(self):
        result = self._run(
            [self._row()],
            deployment_constraint="",
            poc_duration="",
        )
        self.assertEqual(result["quality_score"], 70)

    def test_quality_score_is_integer(self):
        result = self._run([self._row()])
        self.assertIsInstance(result["quality_score"], int)

    def test_quality_score_present_in_return_dict(self):
        result = self._run([self._row()])
        self.assertIn("quality_score", result)


# ---------------------------------------------------------------------------
# TestFMErrorPaths
# ---------------------------------------------------------------------------

class TestFMErrorPaths(FMExecutorTestBase):
    """Error conditions and output contract completeness."""

    def test_empty_matched_capabilities_raises_value_error(self):
        exe = self._make_executor()
        with self.assertRaises(ValueError) as ctx:
            exe.execute_feature_mapping({"matched_capabilities": []})
        self.assertIn("non-empty", str(ctx.exception).lower())

    def test_missing_matched_capabilities_key_raises_value_error(self):
        exe = self._make_executor()
        with self.assertRaises(ValueError):
            exe.execute_feature_mapping({})

    def test_none_ccs_score_propagates_type_error(self):
        exe = self._make_executor()
        row = {"capability_status": "Production", "ccs_score": None, "matched_capability": "X"}
        with self.assertRaises(TypeError):
            exe.execute_feature_mapping({
                "matched_capabilities": [row],
                "deployment_constraint": "Cloud",
                "poc_duration": "30 days",
            })

    def test_string_ccs_score_raises_value_error(self):
        exe = self._make_executor()
        row = {"capability_status": "Production", "ccs_score": "N/A", "matched_capability": "X"}
        with self.assertRaises(ValueError):
            exe.execute_feature_mapping({
                "matched_capabilities": [row],
                "deployment_constraint": "Cloud",
                "poc_duration": "30 days",
            })

    def test_output_keys_complete(self):
        result = self._run([self._row()])
        expected = {
            "feature_validation_table", "overall_tfs_score", "production_tfs_score",
            "quality_score", "markdown_output",
        }
        self.assertEqual(set(result.keys()), expected)

    def test_feature_validation_table_row_keys_complete(self):
        result = self._run([self._row("Production", 90, "Test Feature")])
        row = result["feature_validation_table"][0]
        expected = {
            "proposed_feature", "canonical_capability",
            "integration_path", "tfs_score", "poc_readiness",
        }
        self.assertEqual(set(row.keys()), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
