#!/usr/bin/env python3
import sys
import json
try:
    import yaml
except ImportError:
    yaml = None
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
sys.path.append(str(repo_root))

from agents.governance_review_agent.runtime.audit_logger import AuditLogger
from agents.governance_review_agent.runtime.state_manager import StateManager
from agents.governance_review_agent.runtime.schema_validator import SchemaValidator
from agents.governance_review_agent.runtime.output_builder import OutputBuilder
from agents.governance_review_agent.runtime.skill_executor import SkillExecutor


class Orchestrator:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = str(Path(__file__).parent / "config.yaml")

        self.config_path = Path(config_path)
        self.config = self._load_config()

        dirs = self.config.get("directories", {})
        self.runs_dir = repo_root / dirs.get("runs", "agents/governance_review_agent/runtime/runs")
        self.packages_dir = repo_root / dirs.get("packages", "agents/governance_review_agent/runtime/packages")
        self.logs_dir = repo_root / dirs.get("logs", "agents/governance_review_agent/runtime/logs")

        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        schemas_path = repo_root / "workflows" / "schemas"
        self.validator = SchemaValidator(str(schemas_path))
        self.executor = SkillExecutor(self.runs_dir, self.logs_dir)

    def _load_config(self) -> dict:
        defaults = {
            "directories": {
                "runs": "agents/governance_review_agent/runtime/runs",
                "packages": "agents/governance_review_agent/runtime/packages",
                "logs": "agents/governance_review_agent/runtime/logs",
            },
            "thresholds": {
                "gas_governance_ready": 85, "gas_conditional": 65,
                "ccr_governance_ready": 80, "ccr_conditional": 60,
                "high_risk_governance_ready": 1, "high_risk_conditional": 2,
                "iso_ams_high_risk_threshold": 70,
            },
        }
        if not self.config_path.exists():
            return defaults

        if yaml is not None:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            except Exception:
                pass

        # Fallback indentation-based YAML parser
        content = self.config_path.read_text(encoding="utf-8")
        result = {}
        stack = [(0, result)]
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            indent = len(line) - len(line.lstrip())
            while stack and stack[-1][0] >= indent and len(stack) > 1:
                stack.pop()
            parent = stack[-1][1]
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip()
                if not val or val.startswith("#"):
                    new_dict = {}
                    parent[key] = new_dict
                    stack.append((indent + 1, new_dict))
                else:
                    if (val.startswith('"') and val.endswith('"')) or \
                       (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    elif val.lower() == "true":
                        val = True
                    elif val.lower() == "false":
                        val = False
                    elif val.isdigit():
                        val = int(val)
                    parent[key] = val
        return result

    def start_run(self, trigger_type: str, inputs: dict) -> str:
        traceability_id = self.executor.generate_traceability_id()
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        state_mgr = StateManager(str(self.runs_dir), traceability_id)

        logger.log("INTAKE_VALIDATING", "SUCCESS", "Intake validation initiated.")
        state_mgr.initialize_run(inputs)

        # Primary guard: intake schema validation
        schema_errors = self.validator.validate(inputs, "governance_review_input")
        if schema_errors:
            state_mgr.transition_to("HALTED_INTAKE_INVALID", f"Validation errors: {schema_errors}")
            logger.log("INTAKE_VALIDATING", "FAILED", f"Intake validation failed: {schema_errors}")
            return traceability_id

        logger.log(
            "INTAKE_VALIDATING", "SUCCESS",
            f"Intake validation passed. Assigned traceability ID: {traceability_id}"
        )
        state_mgr.transition_to("INTAKE_COMPLETE", "Intake validation passed.")

        self._run_review(state_mgr, logger)
        return traceability_id

    def _run_review(self, state_mgr: StateManager, logger: AuditLogger):
        state_mgr.transition_to("RUNNING_REVIEW", "Governance Review skill execution started.")
        inputs = state_mgr.get_state().get("inputs", {})

        try:
            review_json = self.executor.execute_governance_review(state_mgr, inputs, logger)
        except Exception as e:
            state_mgr.transition_to(
                "HALTED_GOVERNANCE_INCOMPLETE",
                f"Executor raised an unrecoverable error: {e}"
            )
            logger.log("RUNNING_REVIEW", "FAILED", f"Execution failed: {e}")
            return

        # Validate output schema
        schema_errors = self.validator.validate(review_json, "governance_review_output")
        if schema_errors:
            state_mgr.transition_to(
                "HALTED_REVIEW_SCHEMA",
                f"Output schema validation failed: {schema_errors}"
            )
            logger.log("RUNNING_REVIEW", "FAILED", f"Output schema validation failed: {schema_errors}")
            return

        state_mgr.transition_to("REVIEW_COMPLETE", "Governance Review skill execution completed.")

        # Gate check: governance_gate_passed
        if not review_json.get("governance_gate_passed", False):
            state_mgr.transition_to(
                "HALTED_GATE_INSUFFICIENT",
                f"One or more mandatory GTG gates failed. governance_gate_passed=false. "
                f"classification={review_json.get('classification')}"
            )
            logger.log(
                "GATE_VAL_COMPLETE", "FAILED",
                f"governance_gate_passed=false. Run halted at HALTED_GATE_INSUFFICIENT."
            )
            return

        state_mgr.transition_to(
            "GATE_VALIDATION_PASSED",
            f"All mandatory GTG gates passed. classification={review_json.get('classification')}"
        )
        logger.log(
            "GATE_VAL_COMPLETE", "SUCCESS",
            f"governance_gate_passed=true. "
            f"gas={review_json.get('gas')}, ccr={review_json.get('ccr')}, "
            f"cgc_count={review_json.get('cgc_count')}, "
            f"classification={review_json.get('classification')}"
        )
        state_mgr.transition_to("APPROVAL_PENDING", "Awaiting CSM/Account Director sign-off.")
        logger.log("APPROVAL_GATE", "PENDING", "Run transitioned to APPROVAL_PENDING.")

    def submit_approval(
        self, traceability_id: str, action: str, actor: str, notes: str = None
    ) -> None:
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        run_state = state_mgr.load_state()

        current_status = run_state.get("status")
        if current_status != "APPROVAL_PENDING":
            raise ValueError(
                f"Run {traceability_id} is in status '{current_status}', "
                f"not awaiting approval."
            )

        builder = OutputBuilder(str(self.packages_dir), traceability_id)

        if action == "Approve":
            logger.log(
                "APPROVAL_GATE", "SUCCESS",
                f"CSM/Account Director ({actor}) approved Governance Readiness Certificate. "
                f"Notes: {notes}"
            )
            state_mgr.transition_to("APPROVAL_APPROVED", "Approval received.", actor, notes)
            state_mgr.transition_to("COMPLETE", "Governance Readiness Certificate package assembled.")
            pkg_path = builder.assemble_final_package(state_mgr.get_state(), logger.get_logs())
            logger.log(
                "COMPLETE", "SUCCESS",
                f"Governance Readiness Certificate package assembled at: {pkg_path}"
            )

        elif action == "Reject":
            logger.log(
                "APPROVAL_GATE", "REJECTED",
                f"CSM/Account Director ({actor}) rejected certificate delivery. Notes: {notes}"
            )
            state_mgr.transition_to(
                "HALTED_APPROVAL_REJECTED",
                f"Approval rejected: {notes}", actor, notes
            )

        else:
            raise ValueError(f"Invalid approval action: '{action}'")
