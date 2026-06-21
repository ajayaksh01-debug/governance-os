#!/usr/bin/env python3
import os
import sys
import json
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

runtime_dir = Path(__file__).resolve().parent
repo_root = runtime_dir.parents[2]
if str(runtime_dir) not in sys.path:
    sys.path.insert(0, str(runtime_dir))
if str(repo_root) not in sys.path:
    sys.path.append(str(repo_root))

from audit_logger import AuditLogger  # noqa: E402
from state_manager import StateManager  # noqa: E402
from schema_validator import SchemaValidator  # noqa: E402
from output_builder import OutputBuilder  # noqa: E402
from skill_executor import SkillExecutor  # noqa: E402

SUPPORTED_JURISDICTIONS = {"EU", "UK", "India"}
SUPPORTED_TRIGGER_TYPES = {
    "new_client_onboarding",
    "annual_governance_audit",
    "certification_readiness_check",
    "regulatory_change_impact",
    "pre_proposal_assessment",
}
REQUIRED_INTAKE_FIELDS = [
    "trigger_type",
    "client_name",
    "client_ai_portfolio",
    "existing_policies",
    "target_framework",
    "target_maturity_level",
    "jurisdictions",
]


class Orchestrator:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = str(Path(__file__).parent / "config.yaml")
        self.config_path = Path(config_path)
        self.config = self._load_config()

        dirs = self.config.get("directories", {})
        self.runs_dir = repo_root / dirs.get(
            "runs", "agents/client-assessment-agent/runtime/runs"
        )
        self.packages_dir = repo_root / dirs.get(
            "packages", "agents/client-assessment-agent/runtime/packages"
        )
        self.logs_dir = repo_root / dirs.get(
            "logs", "agents/client-assessment-agent/runtime/logs"
        )
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        schemas_path = repo_root / "workflows" / "schemas"
        self.validator = SchemaValidator(str(schemas_path))
        self.executor = SkillExecutor(self.runs_dir, self.logs_dir)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start_run(self, trigger_type: str, inputs: dict) -> str:
        """Validates intake and begins the 6-skill assessment chain."""
        traceability_id = self.executor.generate_traceability_id()
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        state_mgr = StateManager(str(self.runs_dir), traceability_id)

        logger.log("INTAKE_VALIDATING", "SUCCESS", "Intake validation initiated.")
        state_mgr.initialize_run(inputs)

        errors = self._validate_intake(inputs)
        if errors:
            state_mgr.transition_to(
                "HALTED_INTAKE_INVALID",
                f"Intake validation failed: {errors}",
            )
            logger.log("INTAKE_VALIDATING", "FAILED", f"Intake rejected: {errors}")
            return traceability_id

        jurisdictions = inputs.get("jurisdictions", [])
        unsupported = [j for j in jurisdictions if j not in SUPPORTED_JURISDICTIONS]
        if unsupported:
            state_mgr.transition_to(
                "HALTED_INTAKE_UNSUPPORTED_JURISDICTION",
                f"Unsupported jurisdiction(s): {unsupported}",
            )
            logger.log(
                "INTAKE_VALIDATING",
                "FAILED",
                f"Unsupported jurisdiction(s): {unsupported}",
            )
            return traceability_id

        logger.log(
            "INTAKE_VALIDATING",
            "SUCCESS",
            f"Intake passed. Traceability ID: {traceability_id}",
        )
        state_mgr.transition_to("INTAKE_COMPLETE", "Intake validation passed.")
        self._run_skill_1(state_mgr, logger)
        return traceability_id

    def submit_approval(
        self,
        traceability_id: str,
        gate_num: int,
        role: str,
        action: str,
        actor: str,
        notes: str = None,
    ) -> None:
        """
        Submits an approval decision for any of the 4 approval gates.
        For joint gates (2, 4): tracks per-role decisions; proceeds only when both decide.
        """
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        current = state_mgr.load_state().get("status")
        expected = f"APPROVAL_{gate_num}_PENDING"

        if current != expected:
            raise ValueError(
                f"Run {traceability_id} is in '{current}', not '{expected}'."
            )

        if gate_num in (2, 4):
            self._handle_joint_approval(
                state_mgr, logger, gate_num, role, action, actor, notes
            )
        else:
            self._handle_single_approval(
                state_mgr, logger, gate_num, action, actor, notes
            )

    def release_conditional(
        self, traceability_id: str, actor: str, attestation_notes: str
    ) -> None:
        """
        Compliance Director attestation that elevates HALTED_PROPOSAL_CONDITIONAL
        to GATE_6_PASSED, then APPROVAL_4_PENDING.
        """
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        current = state_mgr.load_state().get("status")

        if current != "HALTED_PROPOSAL_CONDITIONAL":
            raise ValueError(
                f"Run {traceability_id} is in '{current}', not "
                f"'HALTED_PROPOSAL_CONDITIONAL'."
            )

        logger.log(
            "CONDITIONAL_RELEASE",
            "SUCCESS",
            f"Compliance Director ({actor}) attested to conditional items.",
            {"attestation_notes": attestation_notes},
        )
        state_mgr.transition_to(
            "GATE_6_PASSED",
            f"Compliance Director conditional release: {attestation_notes}",
            actor,
            attestation_notes,
        )
        state_mgr.transition_to(
            "APPROVAL_4_PENDING",
            "AG-4 notification sent following conditional release.",
        )
        logger.log(
            "APPROVAL_4_PENDING",
            "PENDING",
            "Run transitioned to APPROVAL_4_PENDING after conditional release.",
        )

    # ------------------------------------------------------------------
    # Approval helpers
    # ------------------------------------------------------------------

    def _handle_single_approval(
        self,
        state_mgr: StateManager,
        logger: AuditLogger,
        gate_num: int,
        action: str,
        actor: str,
        notes: str,
    ) -> None:
        gate_label = f"AG-{gate_num}"
        if action in ("Approve", "Approve with notes"):
            logger.log(gate_label, "SUCCESS", f"{actor} approved. Notes: {notes}")
            state_mgr.transition_to(
                f"APPROVAL_{gate_num}_APPROVED",
                f"{gate_label} approved.",
                actor,
                notes,
            )
            if gate_num == 1:
                self._run_skill_2(state_mgr, logger)
            elif gate_num == 3:
                self._run_skill_5(state_mgr, logger)
        elif action == "Reject":
            logger.log(gate_label, "REJECTED", f"{actor} rejected. Notes: {notes}")
            state_mgr.transition_to(
                f"HALTED_APPROVAL_{gate_num}_REJECTED",
                f"{gate_label} rejected: {notes}",
                actor,
                notes,
            )
        else:
            raise ValueError(f"Invalid action '{action}' for AG-{gate_num}.")

    def _handle_joint_approval(
        self,
        state_mgr: StateManager,
        logger: AuditLogger,
        gate_num: int,
        role: str,
        action: str,
        actor: str,
        notes: str,
    ) -> None:
        gate_label = f"AG-{gate_num}"
        resolution = state_mgr.record_approval_decision(
            gate_num, role, action, actor, notes
        )
        logger.log(
            gate_label,
            "PENDING" if resolution == "awaiting_second" else "SUCCESS",
            f"{actor} ({role}): {action}. Joint resolution: {resolution}.",
        )

        if resolution == "awaiting_second":
            return

        if resolution == "approved":
            state_mgr.transition_to(
                f"APPROVAL_{gate_num}_APPROVED",
                f"{gate_label} joint approval complete.",
            )
            if gate_num == 2:
                self._run_skill_4(state_mgr, logger)
            elif gate_num == 4:
                self._assemble_package(state_mgr, logger)
        elif resolution == "partial":
            state_mgr.transition_to(
                f"HALTED_APPROVAL_{gate_num}_PARTIAL",
                f"{gate_label} partial: one approved, one rejected.",
            )
        elif resolution == "rejected":
            state_mgr.transition_to(
                f"HALTED_APPROVAL_{gate_num}_REJECTED",
                f"{gate_label} both approvers rejected.",
            )

    # ------------------------------------------------------------------
    # Skill execution steps
    # ------------------------------------------------------------------

    def _run_skill_1(self, state_mgr: StateManager, logger: AuditLogger) -> None:
        inputs = state_mgr.get_state().get("inputs", {})
        state_mgr.transition_to("SKILL_1_RUNNING", "Skill 1 (regulatory-mapping) started.")
        logger.log("SKILL_1", "SUCCESS", "Skill 1 execution started.")

        try:
            s1_json = self.executor.execute_skill_1(state_mgr, inputs, logger)
        except Exception as e:
            state_mgr.transition_to("HALTED_ESCALATION", f"Skill 1 execution error: {e}")
            logger.log("SKILL_1", "FAILED", f"Skill 1 execution error: {e}")
            return

        state_mgr.update_intermediate_data("skill_1_json", s1_json)
        state_mgr.update_intermediate_data("skill_1_md", s1_json.get("markdown_output", ""))

        # Skill execution complete; gate evaluation runs from SKILL_1_COMPLETE so
        # that HALTED_GATE_1_SCHEMA is a valid transition target on failure.
        state_mgr.transition_to("SKILL_1_COMPLETE", "Skill 1 execution complete.")

        if not self._check_schema_gate(
            state_mgr, logger, s1_json, "regulatory_mapping_output",
            "HALTED_GATE_1_SCHEMA", "Gate 1a",
        ):
            return

        score = s1_json.get("quality_score", inputs.get("mock_skill_1_score", 88))
        thresholds = self.config.get("thresholds", {})
        pass_threshold = int(thresholds.get("skill_1_pass", 70))
        prelim_threshold = int(thresholds.get("skill_1_preliminary", 55))

        if score < prelim_threshold:
            state_mgr.transition_to(
                "HALTED_GATE_1_SCORE_INSUFFICIENT",
                f"Gate 2a: score {score}/100 < {prelim_threshold} (insufficient).",
            )
            logger.log("GATE_2A", "FAILED", f"Score {score}/100 insufficient.")
            return
        if score < pass_threshold:
            state_mgr.transition_to(
                "HALTED_GATE_1_SCORE_PRELIMINARY",
                f"Gate 2a: score {score}/100 in preliminary band ({prelim_threshold}–{pass_threshold - 1}).",
            )
            logger.log("GATE_2A", "FAILED", f"Score {score}/100 preliminary.")
            return

        state_mgr.transition_to("GATE_1_PASSED", f"Gate 2a score {score}/100 passed.")
        state_mgr.transition_to("APPROVAL_1_PENDING", "AG-1 notification sent.")
        logger.log("GATE_2A", "PENDING", f"Score {score}/100 passed. Awaiting AG-1.")

    def _run_skill_2(self, state_mgr: StateManager, logger: AuditLogger) -> None:
        inputs = state_mgr.get_state().get("inputs", {})
        state_mgr.transition_to("SKILL_2_RUNNING", "Skill 2 (governance-control-mapping) started.")
        logger.log("SKILL_2", "SUCCESS", "Skill 2 execution started.")

        try:
            s2_json = self.executor.execute_skill_2(state_mgr, inputs, logger)
        except Exception as e:
            state_mgr.transition_to("HALTED_ESCALATION", f"Skill 2 execution error: {e}")
            logger.log("SKILL_2", "FAILED", f"Skill 2 execution error: {e}")
            return

        state_mgr.update_intermediate_data("skill_2_json", s2_json)
        state_mgr.update_intermediate_data("skill_2_md", s2_json.get("markdown_output", ""))

        # Skill execution complete; gate evaluation runs from SKILL_2_COMPLETE so
        # that HALTED_GATE_2_SCHEMA is a valid transition target on failure.
        state_mgr.transition_to("SKILL_2_COMPLETE", "Skill 2 execution complete.")

        if not self._check_schema_gate(
            state_mgr, logger, s2_json, "control_mapping_output",
            "HALTED_GATE_2_SCHEMA", "Gate 2b",
        ):
            return

        if not self._run_firewall_check(
            state_mgr, logger,
            s2_json.get("markdown_output", ""),
            "2c", "HALTED_FIREWALL_BREACH",
        ):
            return

        score = s2_json.get("quality_score", inputs.get("mock_skill_2_score", 88))
        thresholds = self.config.get("thresholds", {})
        pass_threshold = int(thresholds.get("skill_2_pass", 85))
        below_threshold = int(thresholds.get("skill_2_below_threshold", 70))

        if score < below_threshold:
            state_mgr.transition_to(
                "HALTED_GATE_2_SCORE_INSUFFICIENT",
                f"Gate 2d: score {score}/100 < {below_threshold} (insufficient).",
            )
            logger.log("GATE_2D", "FAILED", f"Score {score}/100 insufficient.")
            return
        if score < pass_threshold:
            state_mgr.transition_to(
                "HALTED_GATE_2_SCORE_BELOW_THRESHOLD",
                f"Gate 2d: score {score}/100 in below-threshold band ({below_threshold}–{pass_threshold - 1}).",
            )
            logger.log("GATE_2D", "FAILED", f"Score {score}/100 below threshold.")
            return

        state_mgr.transition_to("GATE_2_PASSED", f"Gate 2d score {score}/100 passed.")
        self._run_skill_3(state_mgr, logger)

    def _run_skill_3(self, state_mgr: StateManager, logger: AuditLogger) -> None:
        inputs = state_mgr.get_state().get("inputs", {})
        state_mgr.transition_to("SKILL_3_RUNNING", "Skill 3 (ethana-solution-mapping) started.")
        logger.log("SKILL_3", "SUCCESS", "Skill 3 execution started.")

        try:
            s3_json = self.executor.execute_skill_3(state_mgr, inputs, logger)
        except Exception as e:
            state_mgr.transition_to("HALTED_ESCALATION", f"Skill 3 execution error: {e}")
            logger.log("SKILL_3", "FAILED", f"Skill 3 execution error: {e}")
            return

        state_mgr.update_intermediate_data("skill_3_json", s3_json)
        state_mgr.update_intermediate_data("skill_3_md", s3_json.get("markdown_output", ""))

        # Skill execution complete; gate evaluation runs from SKILL_3_COMPLETE so
        # that HALTED_GATE_3_SCHEMA is a valid transition target on failure.
        state_mgr.transition_to("SKILL_3_COMPLETE", "Skill 3 execution complete.")

        if not self._check_schema_gate(
            state_mgr, logger, s3_json, "solution_mapping_output",
            "HALTED_GATE_3_SCHEMA", "Gate 3a",
        ):
            return

        if not self._run_firewall_check(
            state_mgr, logger,
            s3_json.get("markdown_output", ""),
            "3b", "HALTED_FIREWALL_BREACH",
        ):
            return

        score = s3_json.get("quality_score", inputs.get("mock_skill_3_score", 82))
        pass_threshold = int(self.config.get("thresholds", {}).get("skill_3_pass", 70))

        if score < pass_threshold:
            state_mgr.transition_to(
                "HALTED_GATE_3_SCORE_INSUFFICIENT",
                f"Gate 3c: score {score}/100 < {pass_threshold}.",
            )
            logger.log("GATE_3C", "FAILED", f"Score {score}/100 insufficient.")
            return

        state_mgr.transition_to("GATE_3_PASSED", f"Gate 3c score {score}/100 passed.")
        state_mgr.transition_to("APPROVAL_2_PENDING", "AG-2 notification sent.")
        logger.log("GATE_3C", "PENDING", f"Score {score}/100 passed. Awaiting AG-2.")

    def _run_skill_4(self, state_mgr: StateManager, logger: AuditLogger) -> None:
        inputs = state_mgr.get_state().get("inputs", {})
        state_mgr.transition_to("SKILL_4_RUNNING", "Skill 4 (iso-42001-gap-assessment) started.")
        logger.log("SKILL_4", "SUCCESS", "Skill 4 execution started.")

        try:
            s4_json = self.executor.execute_skill_4(state_mgr, inputs, logger)
        except Exception as e:
            state_mgr.transition_to("HALTED_ESCALATION", f"Skill 4 execution error: {e}")
            logger.log("SKILL_4", "FAILED", f"Skill 4 execution error: {e}")
            return

        state_mgr.update_intermediate_data("skill_4_json", s4_json)
        state_mgr.update_intermediate_data("skill_4_md", s4_json.get("markdown_output", ""))

        # Skill execution complete; gate evaluation runs from SKILL_4_COMPLETE so
        # that HALTED_GATE_4_SCHEMA is a valid transition target on failure.
        state_mgr.transition_to("SKILL_4_COMPLETE", "Skill 4 execution complete.")

        if not self._check_schema_gate(
            state_mgr, logger, s4_json, "iso42001_output",
            "HALTED_GATE_4_SCHEMA", "Gate 4a",
        ):
            return

        if not self._run_firewall_check(
            state_mgr, logger,
            s4_json.get("markdown_output", ""),
            "4b", "HALTED_FIREWALL_BREACH",
        ):
            return

        score = s4_json.get("quality_score", inputs.get("mock_skill_4_score", 88))
        thresholds = self.config.get("thresholds", {})
        pass_threshold = int(thresholds.get("skill_4_pass", 85))
        below_threshold = int(thresholds.get("skill_4_below_threshold", 70))

        if score < below_threshold:
            state_mgr.transition_to(
                "HALTED_GATE_4_SCORE_INSUFFICIENT",
                f"Gate 4c: score {score}/100 < {below_threshold} (insufficient).",
            )
            logger.log("GATE_4C", "FAILED", f"Score {score}/100 insufficient.")
            return
        if score < pass_threshold:
            state_mgr.transition_to(
                "HALTED_GATE_4_SCORE_BELOW_THRESHOLD",
                f"Gate 4c: score {score}/100 in below-threshold band.",
            )
            logger.log("GATE_4C", "FAILED", f"Score {score}/100 below threshold.")
            return

        state_mgr.transition_to("GATE_4_PASSED", f"Gate 4c score {score}/100 passed.")
        state_mgr.transition_to("APPROVAL_3_PENDING", "AG-3 notification sent.")
        logger.log("GATE_4C", "PENDING", f"Score {score}/100 passed. Awaiting AG-3.")

    def _run_skill_5(self, state_mgr: StateManager, logger: AuditLogger) -> None:
        inputs = state_mgr.get_state().get("inputs", {})
        state_mgr.transition_to("SKILL_5_RUNNING", "Skill 5 (ethana-capability-validation) started.")
        logger.log("SKILL_5", "SUCCESS", "Skill 5 execution started.")

        try:
            s5_json = self.executor.execute_skill_5(state_mgr, inputs, logger)
        except Exception as e:
            state_mgr.transition_to("HALTED_ESCALATION", f"Skill 5 execution error: {e}")
            logger.log("SKILL_5", "FAILED", f"Skill 5 execution error: {e}")
            return

        state_mgr.update_intermediate_data("skill_5_json", s5_json)
        state_mgr.update_intermediate_data("skill_5_md", s5_json.get("markdown_output", ""))

        # Skill execution complete; gate evaluation runs from SKILL_5_COMPLETE so
        # that HALTED_GATE_5_SCHEMA is a valid transition target on failure.
        state_mgr.transition_to("SKILL_5_COMPLETE", "Skill 5 execution complete.")

        if not self._check_schema_gate(
            state_mgr, logger, s5_json, "capability_validation_output",
            "HALTED_GATE_5_SCHEMA", "Gate 5a",
        ):
            return

        if not self._run_firewall_check(
            state_mgr, logger,
            s5_json.get("markdown_output", ""),
            "5b", "HALTED_FIREWALL_BREACH",
        ):
            return

        ecs = s5_json.get("ecs", inputs.get("mock_skill_5_score", 95))
        pass_threshold = int(self.config.get("thresholds", {}).get("skill_5_pass", 90))
        escalation_required = s5_json.get("escalation_required", False)

        if ecs < pass_threshold or escalation_required:
            reason = f"ECS {ecs}/100 < {pass_threshold}" if ecs < pass_threshold else "escalation_required"
            state_mgr.transition_to(
                "HALTED_GATE_5_SCORE_INSUFFICIENT",
                f"Gate 5c: {reason}.",
            )
            logger.log("GATE_5C", "FAILED", f"Gate 5c failed: {reason}.")
            return

        state_mgr.transition_to("GATE_5_PASSED", f"Gate 5c ECS {ecs}/100 passed.")
        self._run_skill_fm(state_mgr, logger)

    def _run_skill_fm(self, state_mgr: StateManager, logger: AuditLogger) -> None:
        inputs = state_mgr.get_state().get("inputs", {})
        state_mgr.transition_to("SKILL_FM_RUNNING", "Skill FM (ethana-feature-mapping) started.")
        logger.log("SKILL_FM", "SUCCESS", "Skill FM execution started.")

        try:
            sfm_json = self.executor.execute_skill_fm(state_mgr, inputs, logger)
        except Exception as e:
            state_mgr.transition_to("HALTED_ESCALATION", f"Skill FM execution error: {e}")
            logger.log("SKILL_FM", "FAILED", f"Skill FM execution error: {e}")
            return

        state_mgr.update_intermediate_data("skill_fm_json", sfm_json)
        state_mgr.update_intermediate_data("skill_fm_md", sfm_json.get("markdown_output", ""))

        # Gate evaluation runs from SKILL_FM_COMPLETE so halt states are valid targets.
        state_mgr.transition_to("SKILL_FM_COMPLETE", "Skill FM execution complete.")

        # Gate FM-a — schema conformance
        if not self._check_schema_gate(
            state_mgr, logger, sfm_json, "feature_mapping_output",
            "HALTED_GATE_FM_SCHEMA", "Gate FM-a",
        ):
            return

        # Gate FM-a — non-empty feature_validation_table
        if not sfm_json.get("feature_validation_table"):
            state_mgr.transition_to(
                "HALTED_GATE_FM_EMPTY_TABLE",
                "Gate FM-a: feature_validation_table is empty.",
            )
            logger.log("GATE_FM_A", "FAILED", "feature_validation_table is empty.")
            return

        # Gate FM-b — Claims Firewall
        if not self._run_firewall_check(
            state_mgr, logger,
            sfm_json.get("markdown_output", ""),
            "FM-b", "HALTED_FIREWALL_BREACH",
        ):
            return

        # Gate FM-c — production TFS threshold
        production_tfs = sfm_json.get(
            "production_tfs_score", inputs.get("mock_skill_fm_score", 92)
        )
        tfs_pass = int(self.config.get("thresholds", {}).get("skill_fm_tfs_pass", 85))

        if production_tfs < tfs_pass:
            state_mgr.transition_to(
                "HALTED_GATE_FM_LOW_TFS",
                f"Gate FM-c: production TFS {production_tfs}/100 < {tfs_pass}.",
            )
            logger.log("GATE_FM_C", "FAILED", f"Production TFS {production_tfs}/100 < {tfs_pass}.")
            return

        state_mgr.transition_to(
            "GATE_FM_PASSED",
            f"Gate FM-c: production TFS {production_tfs}/100 passed.",
        )
        logger.log("GATE_FM_C", "SUCCESS", f"Production TFS {production_tfs}/100 passed.")
        self._run_skill_6(state_mgr, logger)

    def _run_skill_6(self, state_mgr: StateManager, logger: AuditLogger) -> None:
        inputs = state_mgr.get_state().get("inputs", {})
        state_mgr.transition_to("SKILL_6_RUNNING", "Skill 6 (ethana-proposal-review) started.")
        logger.log("SKILL_6", "SUCCESS", "Skill 6 execution started.")

        try:
            s6_json = self.executor.execute_skill_6(state_mgr, inputs, logger)
        except Exception as e:
            state_mgr.transition_to("HALTED_ESCALATION", f"Skill 6 execution error: {e}")
            logger.log("SKILL_6", "FAILED", f"Skill 6 execution error: {e}")
            return

        state_mgr.update_intermediate_data("skill_6_json", s6_json)
        state_mgr.update_intermediate_data("skill_6_md", s6_json.get("markdown_output", ""))

        # Skill execution complete; gate evaluation runs from SKILL_6_COMPLETE so
        # that HALTED_GATE_6_SCHEMA is a valid transition target on failure.
        state_mgr.transition_to("SKILL_6_COMPLETE", "Skill 6 execution complete.")

        if not self._check_schema_gate(
            state_mgr, logger, s6_json, "proposal_review_output",
            "HALTED_GATE_6_SCHEMA", "Gate 6a",
        ):
            return

        # Gate 6b — terminal Claims Firewall (hardest fail)
        if not self._run_firewall_check(
            state_mgr, logger,
            s6_json.get("markdown_output", ""),
            "6b", "HALTED_FIREWALL_BREACH_TERMINAL",
        ):
            return

        # Gate 6c — release classification
        pcs = s6_json.get("pcs", inputs.get("mock_skill_6_pcs", 92))
        ctcs = s6_json.get("ctcs", inputs.get("mock_skill_6_ctcs", 88))
        release_classification = s6_json.get(
            "release_classification",
            inputs.get("mock_skill_6_classification", "Approved"),
        )
        thresholds = self.config.get("thresholds", {})
        pcs_pass = int(thresholds.get("skill_6_pcs_pass", 80))
        ctcs_pass = int(thresholds.get("skill_6_ctcs_pass", 80))

        if pcs < pcs_pass or ctcs < ctcs_pass or release_classification == "Rejected":
            state_mgr.transition_to(
                "HALTED_PROPOSAL_REJECTED",
                f"Gate 6c: Rejected classification (PCS={pcs}, CTCS={ctcs}).",
            )
            logger.log("GATE_6C", "FAILED", f"Proposal Rejected: PCS={pcs}, CTCS={ctcs}.")
            return

        if release_classification == "Conditional":
            state_mgr.transition_to(
                "HALTED_PROPOSAL_CONDITIONAL",
                f"Gate 6c: Conditional classification (PCS={pcs}, CTCS={ctcs}). "
                "Compliance Director review required.",
            )
            logger.log(
                "GATE_6C",
                "PENDING",
                f"Conditional release: PCS={pcs}, CTCS={ctcs}. Awaiting CD attestation.",
            )
            return

        state_mgr.transition_to(
            "GATE_6_PASSED",
            f"Gate 6c: Approved classification (PCS={pcs}, CTCS={ctcs}).",
        )
        state_mgr.transition_to("APPROVAL_4_PENDING", "AG-4 notification sent.")
        logger.log("GATE_6C", "PENDING", f"PCS={pcs}, CTCS={ctcs} passed. Awaiting AG-4.")

    def _assemble_package(self, state_mgr: StateManager, logger: AuditLogger) -> None:
        tid = state_mgr.traceability_id
        state_mgr.transition_to("ASSEMBLING_PACKAGE", "Assembling Executive Assessment Package.")
        logger.log("ASSEMBLING_PACKAGE", "SUCCESS", "Package assembly started.")

        builder = OutputBuilder(str(self.packages_dir), tid)
        pkg_path = builder.assemble_package(state_mgr.get_state(), logger.get_logs())

        state_mgr.transition_to("COMPLETE", "Executive Assessment Package delivered.")
        logger.log("COMPLETE", "SUCCESS", f"Package assembled at: {pkg_path}")

    # ------------------------------------------------------------------
    # Gate helpers
    # ------------------------------------------------------------------

    def _validate_intake(self, inputs: dict) -> list:
        errors = []
        for field in REQUIRED_INTAKE_FIELDS:
            if field not in inputs or not inputs[field]:
                errors.append(f"Missing required field: '{field}'")
        if inputs.get("trigger_type") and inputs["trigger_type"] not in SUPPORTED_TRIGGER_TYPES:
            errors.append(
                f"Invalid trigger_type '{inputs['trigger_type']}'. "
                f"Supported: {sorted(SUPPORTED_TRIGGER_TYPES)}"
            )
        return errors

    def _check_schema_gate(
        self,
        state_mgr: StateManager,
        logger: AuditLogger,
        payload: dict,
        schema_name: str,
        halt_state: str,
        gate_label: str,
    ) -> bool:
        """Returns True if validation passes. Transitions to halt_state on failure."""
        inputs = state_mgr.get_state().get("inputs", {})
        if inputs.get("skip_schema_validation"):
            logger.log(gate_label, "WARNING", "Schema validation skipped (test mode).")
            return True

        errors = self.validator.validate(payload, schema_name)
        if errors:
            state_mgr.transition_to(
                halt_state,
                f"{gate_label} schema validation failed: {errors}",
            )
            logger.log(gate_label, "FAILED", f"Schema validation failed: {errors}")
            return False

        logger.log(gate_label, "SUCCESS", f"{gate_label} schema validation passed.")
        return True

    def _run_firewall_check(
        self,
        state_mgr: StateManager,
        logger: AuditLogger,
        md_content: str,
        gate_label: str,
        breach_state: str,
    ) -> bool:
        """
        Runs the Claims Firewall check on md_content.
        Returns True if the gate passes, False if a breach was detected and run halted.
        Test escape hatch: set inputs["simulate_firewall_breach_at_gate"] = gate_label.
        """
        inputs = state_mgr.get_state().get("inputs", {})

        if inputs.get("simulate_firewall_breach_at_gate") == gate_label:
            state_mgr.transition_to(
                breach_state,
                f"Gate {gate_label}: simulated Claims Firewall breach.",
            )
            logger.log(f"GATE_{gate_label}_FIREWALL", "BREACH", "Simulated firewall breach.")
            return False

        if not md_content:
            state_mgr.transition_to(
                breach_state,
                f"Gate {gate_label}: empty markdown content; firewall cannot execute.",
            )
            logger.log(
                f"GATE_{gate_label}_FIREWALL",
                "ERROR",
                "Empty markdown content; firewall gate halted (fail-closed).",
            )
            return False

        tmp_path = None
        try:
            claims_linter_path = repo_root / "evaluations" / "scripts"
            if str(claims_linter_path) not in sys.path:
                sys.path.insert(0, str(claims_linter_path))
            from claims_linter import parse_canonical_model, lint_file  # noqa: PLC0415

            cpm_path = repo_root / "knowledge" / "ethana" / "canonical-product-model.md"
            cpm = parse_canonical_model(Path(cpm_path))

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False, encoding="utf-8"
            ) as tmp:
                tmp.write(md_content)
                tmp_path = tmp.name

            violations = lint_file(Path(tmp_path), cpm)

            if violations:
                state_mgr.transition_to(
                    breach_state,
                    f"Gate {gate_label}: {len(violations)} Claims Firewall violation(s).",
                )
                logger.log(
                    f"GATE_{gate_label}_FIREWALL",
                    "BREACH",
                    f"{len(violations)} violation(s) detected.",
                    {"violations": [str(v) for v in violations]},
                )
                return False

            logger.log(
                f"GATE_{gate_label}_FIREWALL",
                "SUCCESS",
                "Claims Firewall check passed.",
            )
            return True

        except ImportError:
            state_mgr.transition_to(
                breach_state,
                f"Gate {gate_label}: claims_linter unavailable; firewall cannot execute.",
            )
            logger.log(
                f"GATE_{gate_label}_FIREWALL",
                "ERROR",
                "claims_linter unavailable; firewall gate halted (fail-closed).",
            )
            return False
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    # ------------------------------------------------------------------
    # Config loader
    # ------------------------------------------------------------------

    def _load_config(self) -> dict:
        default = {
            "directories": {
                "runs": "agents/client-assessment-agent/runtime/runs",
                "packages": "agents/client-assessment-agent/runtime/packages",
                "logs": "agents/client-assessment-agent/runtime/logs",
            },
            "thresholds": {
                "skill_1_pass": 70,
                "skill_1_preliminary": 55,
                "skill_2_pass": 85,
                "skill_2_below_threshold": 70,
                "skill_3_pass": 70,
                "skill_4_pass": 85,
                "skill_4_below_threshold": 70,
                "skill_5_pass": 90,
                "skill_6_pcs_pass": 80,
                "skill_6_ctcs_pass": 80,
            },
        }
        if not self.config_path.exists():
            return default
        if yaml is not None:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or default
            except Exception:
                pass
        # Minimal fallback: return defaults rather than risk a broken parse
        return default
