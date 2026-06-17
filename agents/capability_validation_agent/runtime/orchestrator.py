#!/usr/bin/env python3
"""
Orchestrator for Capability Validation Agent Runtime v0.1.
Coordinates capability validation flow, schema validator gates, claims firewall checking,
state management, peer approval gate, and handoff package generation.
"""

import os
import sys
import glob
import json
try:
    import yaml
except ImportError:
    yaml = None
from datetime import datetime, timezone
from pathlib import Path

# Paths setup
repo_root = Path(__file__).resolve().parents[3]
sys.path.append(str(repo_root / "evaluations" / "scripts"))

# Import audit logs, state manager, schema validator, output builder, and skill executor
from audit_logger import AuditLogger
from state_manager import StateManager
from schema_validator import SchemaValidator
from output_builder import OutputBuilder
from skill_executor import SkillExecutor

try:
    import claims_linter
except ImportError:
    print("Warning: claims_linter script could not be imported.")

class Orchestrator:
    def __init__(self, config_path: str = None):
        """Initializes the orchestrator and loads configurations."""
        if config_path is None:
            config_path = str(Path(__file__).parent / "config.yaml")
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # Load directories
        dirs = self.config.get("directories", {})
        self.runs_dir = repo_root / dirs.get("runs", "agents/capability_validation_agent/runtime/runs")
        self.packages_dir = repo_root / dirs.get("packages", "agents/capability_validation_agent/runtime/packages")
        self.logs_dir = repo_root / dirs.get("logs", "agents/capability_validation_agent/runtime/logs")
        
        # Ensure directories exist
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Schema validator pointing to contracts
        contracts_path = repo_root / "agents" / "capability_validation_agent" / "runtime" / "contracts"
        self.validator = SchemaValidator(str(contracts_path))
        
        # Skill Executor
        self.executor = SkillExecutor(self.runs_dir, self.logs_dir)

    def _load_config(self) -> dict:
        """Loads configuration from YAML file, handles basic parsing if PyYAML not available."""
        if not self.config_path.exists():
            return {
                "directories": {
                    "runs": "agents/capability_validation_agent/runtime/runs",
                    "packages": "agents/capability_validation_agent/runtime/packages",
                    "logs": "agents/capability_validation_agent/runtime/logs"
                },
                "thresholds": {
                    "capability_validation": 90
                }
            }
            
        if yaml is not None:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            except Exception as e:
                pass

        # Fallback indentation-based parser for nested YAML
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
                
            parent_dict = stack[-1][1]
            
            if ":" in stripped:
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip()
                
                if not val or val.startswith("#"):
                    new_dict = {}
                    parent_dict[key] = new_dict
                    stack.append((indent + 1, new_dict))
                else:
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    if val.lower() == "true":
                        val = True
                    elif val.lower() == "false":
                        val = False
                    elif val.isdigit():
                        val = int(val)
                    parent_dict[key] = val
        return result


    def _generate_traceability_id(self) -> str:
        """Generates a unique TR-CV-{YYYY}-{NNNN} ID."""
        return self.executor.generate_traceability_id()

    def start_run(self, trigger_type: str, inputs: dict) -> str:
        """Intakes capability validation request trigger, runs execution, validates output, and pauses for Peer sign-off."""
        # Validate inputs first
        validation_errors = self._validate_inputs(trigger_type, inputs)
        
        # Determine traceability ID
        traceability_id = self._generate_traceability_id()
        
        # Setup Logger and State Manager
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        
        logger.log("INTAKE_VALIDATING", "SUCCESS", "Intake validation initiated.")
        state_mgr.initialize_run(inputs)
        
        if validation_errors:
            state_mgr.transition_to("HALTED_INTAKE_INVALID", f"Validation errors: {validation_errors}")
            logger.log("INTAKE_VALIDATING", "FAILED", f"Intake validation failed: {validation_errors}")
            return traceability_id

        logger.log("INTAKE_VALIDATING", "SUCCESS", f"Intake validation passed. Assigned traceability ID: {traceability_id}")
        state_mgr.transition_to("INTAKE_COMPLETE", "Intake validation passed.")
        
        # Trigger Skill validation
        self._run_skill(state_mgr, logger)
        
        return traceability_id

    def _validate_inputs(self, trigger_type: str, inputs: dict) -> list:
        """Validates trigger and input requirements."""
        errors = []
        allowed_triggers = ["new_capability_validation_request", "source_document_validation"]
        if trigger_type not in allowed_triggers:
            errors.append(f"Invalid trigger_type: '{trigger_type}'")
            
        if "capability_name" not in inputs and "proposed_claim" not in inputs:
            errors.append("At least 'capability_name' or 'proposed_claim' must be provided.")
            
        return errors

    def _run_skill(self, state_mgr: StateManager, logger: AuditLogger):
        """Runs dynamic capability validation and executes Gate 1 & Gate 2 validations."""
        trace_id = state_mgr.traceability_id
        state_mgr.transition_to("SKILL_1_RUNNING", "Skill 1 (capability-validation) execution started.")
        logger.log("SKILL_1_RUNNING", "SUCCESS", "Executing Capability Adjudication logic.")
        
        inputs = state_mgr.get_state().get("inputs", {})
        
        # Ingest inputs and perform dynamic validation
        s1_json = self.executor.execute_validation(inputs, logger)
        
        # Compile report markdown
        s1_md = self.executor.compile_report_to_markdown(s1_json)
        
        state_mgr.update_intermediate_data("capability_validation_output_json", s1_json)
        state_mgr.update_intermediate_data("capability_validation_output_md", s1_md)
        state_mgr.update_intermediate_data("validated_status", s1_json.get("validated_status", "Unresolved"))
        state_mgr.update_intermediate_data("ecs", s1_json.get("ecs", 0))
        state_mgr.update_intermediate_data("ecs_band", s1_json.get("ecs_band", "Insufficient"))
        
        # Execute Gate 1: Schema Validation & Claims Firewall check
        passed_gate_1 = self._evaluate_gate_1(state_mgr, logger, s1_json, s1_md, inputs)
        if not passed_gate_1:
            return

        # Execute Gate 2: Quality score Threshold check
        self._evaluate_gate_2(state_mgr, logger, s1_json, inputs)

    def _evaluate_gate_1(self, state_mgr: StateManager, logger: AuditLogger, s1_json: dict, s1_md: str, inputs: dict) -> bool:
        """Gate 1: Runs schema check and Claims Firewall check on the validation output."""
        trace_id = state_mgr.traceability_id
        state_mgr.transition_to("SKILL_1_COMPLETE", "Skill 1 complete. Initiating Gate 1 (Schema & Firewall).")
        
        # 1. Run Schema validation
        schema_errors = self.validator.validate(s1_json, "capability_validation")
        if schema_errors:
            # Automatic retry check
            logger.log("GATE_1_VALIDATION", "FAILED", f"Schema validation failed: {schema_errors}. Retrying...")
            schema_errors = self.validator.validate(s1_json, "capability_validation")
            if schema_errors:
                state_mgr.transition_to("HALTED_GATE_1_SCHEMA", f"Schema validation failed after retry: {schema_errors}")
                logger.log("GATE_1_VALIDATION", "FAILED", f"Schema validation failed after retry: {schema_errors}. Pipeline halted.")
                return False

        # 2. Run Claims Firewall validation using hard disqualifiers
        firewall_errors = []
        if s1_json.get("hard_disqualifiers_triggered"):
            firewall_errors.append(f"Hard Disqualifiers Triggered: {s1_json['hard_disqualifiers_triggered']}")

        if firewall_errors:
            state_mgr.transition_to("HALTED_FIREWALL_BREACH", f"Firewall breaches or disqualifiers detected: {firewall_errors}")
            logger.log("GATE_1_FIREWALL", "BREACH", f"Firewall check failed: {firewall_errors}. Pipeline halted.")
            return False
            
        state_mgr.transition_to("GATE_1_PASSED", "Schema and Claims Firewall validation passed.")
        logger.log("GATE_1_VALIDATION", "SUCCESS", "Schema and Claims Firewall checks passed.")
        return True

    def _evaluate_gate_2(self, state_mgr: StateManager, logger: AuditLogger, s1_json: dict, inputs: dict):
        """Gate 2: Evaluates Quality score threshold check."""
        # Calculate a validation score based on compliance quality
        # ECS + output quality
        ecs = s1_json.get("ecs", 0)
        
        # Quality score: Base of ECS, +10 if details present, +5 if audit complete
        score = ecs
        if s1_json.get("canonical_entry_verbatim"):
            score += 10
        if s1_json.get("phase_9_gate_completed"):
            score += 5
        if s1_json.get("contradictions_count", 0) > 0:
            score -= 10
        score = min(score, 100)
        
        # Allow test overrides
        score = inputs.get("mock_score", score)
        
        threshold = int(self.config.get("thresholds", {}).get("capability_validation", 90))
        
        if score < threshold:
            state_mgr.transition_to("HALTED_GATE_2_INSUFFICIENT", f"Validation score {score}/100 falls below threshold {threshold}/100.")
            logger.log("GATE_2_QUALITY", "FAILED", f"Quality score {score}/100 is insufficient. Pipeline halted.")
        else:
            state_mgr.transition_to("GATE_2_PASSED", f"Quality score {score}/100 satisfied threshold.")
            state_mgr.transition_to("APPROVAL_1_PENDING", "Awaiting Peer Reviewer approval sign-off.")
            logger.log("GATE_2_QUALITY", "PENDING", f"Quality score {score}/100 passed. Run transitioned to APPROVAL_1_PENDING. Awaiting Peer sign-off.")

    def submit_approval_1(self, traceability_id: str, action: str, actor: str, notes: str = None) -> None:
        """Executes peer review approval gate and generates output package."""
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        run_state = state_mgr.load_state()
        
        current_status = run_state.get("status")
        if current_status not in ["APPROVAL_1_PENDING", "APPROVAL_TIMED_OUT"]:
            raise ValueError(f"Run {traceability_id} is in status '{current_status}', not awaiting Peer approval.")
            
        builder = OutputBuilder(str(self.packages_dir), traceability_id)
        
        if action == "Approve":
            logger.log("APPROVAL_GATE_1", "SUCCESS", f"Peer Reviewer ({actor}) approved Capability Validation. Notes: {notes}")
            state_mgr.transition_to("APPROVAL_1_APPROVED", "Peer approved validation.", actor, notes)
            
            # Finalize run
            state_mgr.transition_to("COMPLETE", "Capability Validation Package assembled.")
            pkg_path = builder.assemble_final_package(state_mgr.get_state(), logger.get_logs())
            logger.log("COMPLETE", "SUCCESS", f"Capability Validation Package successfully assembled at: {pkg_path}")
            
        elif action == "Reject":
            logger.log("APPROVAL_GATE_1", "REJECTED", f"Peer Reviewer ({actor}) rejected Capability Validation. Notes: {notes}")
            state_mgr.transition_to("HALTED_APPROVAL_1_REJECTED", f"Peer rejection: {notes}", actor, notes)
            
        elif action == "Timeout":
            logger.log("APPROVAL_GATE_1", "TIMEOUT", "Approval deadline elapsed without action.")
            state_mgr.transition_to("APPROVAL_TIMED_OUT", "Approval timed out after 5 business days.")
            
        else:
            raise ValueError(f"Invalid approval action: '{action}'")
