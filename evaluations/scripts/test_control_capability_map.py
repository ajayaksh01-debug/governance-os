#!/usr/bin/env python3
"""
T6 — Loader unit tests and covenant validation for control-capability-map.md.

Covers:
  T6(a) Happy path: 6 keys parsed, correct primaries, Phase A secondary always []
  T6(b) Missing file: returns empty dict, does not raise
  T6(c) Unknown key lookup convention: missing key handled by caller with .get() default
  T6(d) Invalid CPM key warning: warning emitted to stderr, does not raise
  T6(e) Covenant validation: Skill 1 control name set == knowledge file Control Name set
"""

import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / "evaluations" / "scripts"))

from claims_linter import load_control_capability_map  # noqa: E402

MAP_PATH = repo_root / "knowledge" / "ethana" / "control-capability-map.md"

# Complete Skill 1 control name set — derived from full source scan of
# execute_regulatory_mapping() in agents/regulatory-watch-agent/runtime/skill_executor.py
# (Section 2.1 of PR-010). Used by T6(e) covenant validation without live executor calls.
SKILL1_CONTROL_NAMES = {
    "human oversight gate",
    "drift monitoring",
    "fairness and bias monitoring",
    "consent verification",
    "vendor risk assessment",
    "prompt injection filter",
}


class TestLoadControlCapabilityMapHappyPath(unittest.TestCase):
    """T6(a) — Happy path."""

    def setUp(self):
        self.ccm = load_control_capability_map(MAP_PATH)

    def test_returns_six_keys(self):
        self.assertEqual(len(self.ccm), 6, f"Expected 6 keys, got: {list(self.ccm.keys())}")

    def test_human_oversight_gate_primary(self):
        self.assertEqual(self.ccm["human oversight gate"]["primary"], "immutable audit log")

    def test_drift_monitoring_primary(self):
        self.assertEqual(self.ccm["drift monitoring"]["primary"], "immutable audit log")

    def test_fairness_and_bias_monitoring_primary(self):
        self.assertEqual(self.ccm["fairness and bias monitoring"]["primary"], "runtime guardrails")

    def test_prompt_injection_filter_primary(self):
        self.assertEqual(self.ccm["prompt injection filter"]["primary"], "runtime guardrails")

    def test_consent_verification_primary_empty(self):
        self.assertEqual(self.ccm["consent verification"]["primary"], "")

    def test_vendor_risk_assessment_primary_empty(self):
        self.assertEqual(self.ccm["vendor risk assessment"]["primary"], "")

    def test_phase_a_secondary_always_empty_list(self):
        # Phase A loader ignores the populated Phase B secondary column.
        # Fairness and Bias Monitoring has 'immutable audit log' in column 4 —
        # the loader must return [] regardless.
        self.assertEqual(self.ccm["fairness and bias monitoring"]["secondary"], [])

    def test_all_secondaries_are_empty_list(self):
        for key, val in self.ccm.items():
            self.assertEqual(
                val["secondary"], [],
                f"Expected secondary=[] for '{key}', got {val['secondary']}"
            )

    def test_keys_are_lowercase(self):
        for key in self.ccm:
            self.assertEqual(key, key.lower(), f"Key not lowercased: '{key}'")


class TestLoadControlCapabilityMapMissingFile(unittest.TestCase):
    """T6(b) — Missing file: returns empty dict, does not raise."""

    def test_missing_file_returns_empty_dict(self):
        result = load_control_capability_map(Path("/nonexistent/path/control-capability-map.md"))
        self.assertEqual(result, {})

    def test_missing_file_does_not_raise(self):
        try:
            load_control_capability_map(Path("/nonexistent/path.md"))
        except Exception as e:
            self.fail(f"load_control_capability_map raised unexpectedly: {e}")

    def test_missing_file_emits_warning(self):
        buf = io.StringIO()
        with patch("sys.stderr", buf):
            load_control_capability_map(Path("/nonexistent/path.md"))
        self.assertIn("Warning", buf.getvalue())


class TestLoadControlCapabilityMapUnknownKey(unittest.TestCase):
    """T6(c) — Unknown key handling: caller uses .get() with a default."""

    def setUp(self):
        self.ccm = load_control_capability_map(MAP_PATH)

    def test_unknown_key_get_with_default(self):
        result = self.ccm.get("this control does not exist", {"primary": "", "secondary": []})
        self.assertEqual(result, {"primary": "", "secondary": []})

    def test_unknown_key_does_not_raise(self):
        try:
            _ = self.ccm.get("nonexistent key", {"primary": "", "secondary": []})
        except Exception as e:
            self.fail(f"Raised unexpectedly: {e}")

    def test_known_keys_not_affected_by_unknown_access(self):
        _ = self.ccm.get("nonexistent", {"primary": "", "secondary": []})
        self.assertEqual(self.ccm["human oversight gate"]["primary"], "immutable audit log")


class TestLoadControlCapabilityMapInvalidCPMKey(unittest.TestCase):
    """T6(d) — Invalid CPM key warning: warning emitted to stderr, does not raise."""

    def test_invalid_primary_key_emits_warning_not_raises(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, dir=MAP_PATH.parent
        ) as f:
            f.write(
                "# Test Map\n\n"
                "| Control Name | Framework Reference | Primary Capability | Phase B: Secondary Capabilities | Notes |\n"
                "|---|---|---|---|---|\n"
                "| Test Control | Test Framework | nonexistent cpm capability | | Test notes |\n"
            )
            tmp_path = Path(f.name)

        try:
            buf = io.StringIO()
            with patch("sys.stderr", buf):
                result = load_control_capability_map(tmp_path)
            warning_output = buf.getvalue()
            self.assertIn("Warning", warning_output, "Expected a warning about invalid CPM key")
            self.assertIn("nonexistent cpm capability", warning_output)
            # Must not raise — result still has the entry
            self.assertIn("test control", result)
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_valid_primary_key_emits_no_warning(self):
        buf = io.StringIO()
        with patch("sys.stderr", buf):
            load_control_capability_map(MAP_PATH)
        # No warnings for valid keys (CPM cross-validation passes)
        self.assertEqual(buf.getvalue(), "", f"Unexpected warnings: {buf.getvalue()}")


class TestControlCapabilityMapCovenant(unittest.TestCase):
    """T6(e) — Covenant validation: bijective correspondence between
    Skill 1 control name set and knowledge file Control Name column."""

    def setUp(self):
        self.ccm = load_control_capability_map(MAP_PATH)
        self.map_keys = set(self.ccm.keys())

    def test_every_map_key_is_in_skill1_set(self):
        orphans = self.map_keys - SKILL1_CONTROL_NAMES
        self.assertEqual(
            orphans, set(),
            f"Knowledge file contains control names not producible by Skill 1: {orphans}"
        )

    def test_every_skill1_control_has_map_entry(self):
        missing = SKILL1_CONTROL_NAMES - self.map_keys
        self.assertEqual(
            missing, set(),
            f"Skill 1 controls with no knowledge file entry: {missing}"
        )

    def test_bijective_correspondence(self):
        self.assertEqual(
            self.map_keys, SKILL1_CONTROL_NAMES,
            f"Sets differ.\n  Map only: {self.map_keys - SKILL1_CONTROL_NAMES}\n"
            f"  Skill 1 only: {SKILL1_CONTROL_NAMES - self.map_keys}"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
