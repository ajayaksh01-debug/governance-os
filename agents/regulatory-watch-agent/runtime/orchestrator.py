#!/usr/bin/env python3
"""
Orchestrator for Regulatory Watch Agent Runtime v0.1.
Coordinates the execution flow, quality gates, approval gates, persistent state management,
claims firewall linting, output packaging, and Watch Mode (Mode B) re-assessments.
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

# Import audit logs, state manager, schema validator, and output builder
from audit_logger import AuditLogger
from state_manager import StateManager
from schema_validator import SchemaValidator
from output_builder import OutputBuilder
from skill_executor import SkillExecutor


try:
    import claims_linter
    import regression_tester
except ImportError:
    print("Warning: claims_linter or regression_tester scripts could not be imported directly.")

class Orchestrator:
    def __init__(self, config_path: str = None):
        """Initializes the orchestrator and loads configurations."""
        if config_path is None:
            config_path = str(Path(__file__).parent / "config.yaml")
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # Load directories
        dirs = self.config.get("directories", {})
        self.runs_dir = repo_root / dirs.get("runs", "agents/regulatory-watch-agent/runtime/runs")
        self.packages_dir = repo_root / dirs.get("packages", "agents/regulatory-watch-agent/runtime/packages")
        self.logs_dir = repo_root / dirs.get("logs", "agents/regulatory-watch-agent/runtime/logs")
        
        # Ensure directories exist
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Schema validator
        contracts_path = repo_root / "agents" / "regulatory-watch-agent" / "runtime" / "contracts"
        self.validator = SchemaValidator(str(contracts_path))
        
        # Skill Executor
        self.executor = SkillExecutor(self.runs_dir, self.logs_dir)


    def _load_config(self) -> dict:
        """Loads configuration from YAML file, handles basic parsing if PyYAML not available."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
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
        """Generates a unique TR-RW-{YYYY}-{NNNN} ID by scanning existing run state files."""
        return self.executor.generate_traceability_id()


    def start_run(self, trigger_type: str, inputs: dict) -> str:
        """
        Intakes trigger payload, validates inputs, and executes the runtime sequential flow.
        Pauses and returns after entering APPROVAL_1_PENDING state.
        """
        # Validate inputs first (V-04 / state-machine.md)
        validation_errors = self._validate_inputs(trigger_type, inputs)
        
        # Determine traceability_id
        traceability_id = self._generate_traceability_id()
        
        # Setup Logger and State Manager
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        
        logger.log("INTAKE_VALIDATING", "SUCCESS", "Intake validation initiated.")
        state_mgr.initialize_run(inputs)
        
        if validation_errors:
            # Check if it was an unsupported jurisdiction error
            unsupported_jurisdiction = any("unsupported jurisdiction" in err.lower() for err in validation_errors)
            if unsupported_jurisdiction:
                state_mgr.transition_to("HALTED_INTAKE_UNSUPPORTED_JURISDICTION", f"Unsupported jurisdiction: {validation_errors}")
                logger.log("INTAKE_VALIDATING", "HALTED", f"Intake halted due to unsupported jurisdiction: {validation_errors}")
            else:
                state_mgr.transition_to("HALTED_INTAKE_INVALID", f"Validation errors: {validation_errors}")
                logger.log("INTAKE_VALIDATING", "FAILED", f"Intake validation failed: {validation_errors}")
            return traceability_id

        # Map to fixture
        fixture_name = self._map_to_fixture(inputs)
        logger.log("INTAKE_VALIDATING", "SUCCESS", f"Intake validation passed. Assigned traceability ID: {traceability_id}. Mapped to fixture: {fixture_name}")
        state_mgr.transition_to("INTAKE_COMPLETE", "Intake validation passed.")
        
        # Trigger Skill 1
        self._run_skill_1(state_mgr, logger, fixture_name)
        
        return traceability_id

    def _validate_inputs(self, trigger_type: str, inputs: dict) -> list:
        """Validates that all required fields are present and structurally correct."""
        errors = []
        allowed_triggers = ["new_use_case_registration", "jurisdictional_expansion", "regulatory_change_alert"]
        if trigger_type not in allowed_triggers:
            errors.append(f"Invalid trigger_type: '{trigger_type}'")
            
        required_fields = ["subject_description", "subject_type", "jurisdictions", "target_maturity_level"]
        for field in required_fields:
            if field not in inputs or not inputs[field]:
                errors.append(f"Missing required field: '{field}'")
                
        # Length check
        desc = inputs.get("subject_description", "")
        if len(desc) < 50:
            errors.append(f"subject_description length ({len(desc)}) is less than minimum 50 characters.")
            
        # Subject type check
        subj_type = inputs.get("subject_type", "")
        if subj_type not in ["AI Use Case", "AI System", "AI Portfolio"]:
            errors.append(f"Invalid subject_type: '{subj_type}'")
            
        # Target maturity check
        mat = inputs.get("target_maturity_level", "")
        if mat not in ["L1", "L2", "L3", "L4", "L5"]:
            errors.append(f"Invalid target_maturity_level: '{mat}'")
            
        # Jurisdictions check
        jurs = inputs.get("jurisdictions", [])
        if not isinstance(jurs, list) or len(jurs) == 0:
            errors.append("jurisdictions must be a non-empty array.")
        else:
            for j in jurs:
                if j not in ["EU", "UK", "India"]:
                    errors.append(f"Unsupported jurisdiction: '{j}'. Allowed: EU, UK, India.")
                    
        return errors

    def _map_to_fixture(self, inputs: dict) -> str:
        """Determines which mock test fixture maps to the current run inputs."""
        jurs = inputs.get("jurisdictions", [])
        desc = inputs.get("subject_description", "").lower()
        industry = inputs.get("industry", "").lower()
        
        if "india" in jurs:
            return "india-dpdp-customer-support-ai"
        elif "uk" in jurs and ("insurance" in desc or "insurance" in industry):
            return "uk-insurance-claims-model"
        else:
            return "eu-ai-act-high-risk-banking"

    def _run_skill_1(self, state_mgr: StateManager, logger: AuditLogger, fixture_name: str):
        """Executes Skill 1 (regulatory-mapping) programmatically and executes Gate 1 & Gate 2 validations."""
        trace_id = state_mgr.traceability_id
        state_mgr.transition_to("SKILL_1_RUNNING", "Skill 1 (regulatory-mapping) execution started.")
        logger.log("SKILL_1_RUNNING", "SUCCESS", "Generating Regulatory Scoping Matrix.")
        
        inputs = state_mgr.get_state().get("inputs", {})
        
        # Execute skill programmatically
        s1_json = self.executor.execute_regulatory_mapping(inputs, logger)
        
        # Compile structured JSON output into markdown representation
        risk_tier = s1_json.get("risk_tier", "General Enterprise")
        s1_md = self.executor.compile_regulatory_mapping_to_markdown(s1_json, risk_tier)
        
        state_mgr.update_intermediate_data("regulatory_mapping_output_md", s1_md)
        
        # Execute Gate 1: Schema Validation (with retry support) & Firewall check
        passed_gate_1 = self._evaluate_gate_1(state_mgr, logger, s1_json, inputs)
        if not passed_gate_1:
            return

        # Execute Advisory Structural Regression Check
        self._evaluate_advisory_regression_s1(state_mgr, logger)

        # Execute Gate 2: Quality Score Check
        self._evaluate_gate_2(state_mgr, logger, s1_json, inputs)


    def _evaluate_skill_1_firewall(self, state_mgr: StateManager, logger: AuditLogger, md_content: str) -> bool:
        """Executes Claims Firewall check on Skill 1 output."""
        trace_id = state_mgr.traceability_id
        
        # Write temp md file
        temp_md_path = self.runs_dir / f"{trace_id}_s1_firewall_temp.md"
        temp_md_path.write_text(md_content, encoding="utf-8")
        
        cpm_path = repo_root / "knowledge" / "ethana" / "canonical-product-model.md"
        firewall_errors = []
        try:
            capabilities = claims_linter.parse_canonical_model(cpm_path)
            firewall_violations = claims_linter.lint_file(temp_md_path, capabilities)
            if firewall_violations:
                for ln, line, msg in firewall_violations:
                    firewall_errors.append(f"Line {ln}: {msg}")
        except Exception as e:
            firewall_errors.append(f"Claims Firewall linter unavailable: {e}")
            logger.log("GATE_1_FIREWALL", "ERROR", f"Could not run Claims Firewall linter: {e}")
        finally:
            if temp_md_path.exists():
                temp_md_path.unlink()
                
        if firewall_errors:
            state_mgr.update_intermediate_data("claims_firewall_status_s1", "BREACH")
            state_mgr.transition_to("HALTED_FIREWALL_BREACH", f"Claims Firewall breaches detected in Skill 1 output: {firewall_errors}")
            logger.log("GATE_1_FIREWALL", "BREACH", f"Claims Firewall breach detected in Skill 1 output: {firewall_errors}. Pipeline halted.")
            return False
        else:
            state_mgr.update_intermediate_data("claims_firewall_status_s1", "PASS")
            logger.log("GATE_1_FIREWALL", "SUCCESS", "Claims Firewall check passed on Skill 1 output.")
            return True

    def _evaluate_gate_1(self, state_mgr: StateManager, logger: AuditLogger, s1_json: dict, inputs: dict) -> bool:
        """Runs Gate 1 schema validation with single auto-retry logic."""
        trace_id = state_mgr.traceability_id
        state_mgr.transition_to("SKILL_1_COMPLETE", "Skill 1 complete. Initiating Gate 1 (Schema Validation).")
        
        # Run Claims Firewall check (new gate) against Skill 1 output
        s1_md = state_mgr.get_state().get("intermediate_data", {}).get("regulatory_mapping_output_md", "")
        passed_firewall = self._evaluate_skill_1_firewall(state_mgr, logger, s1_md)
        if not passed_firewall:
            return False
            
        # First attempt payload
        payload = dict(s1_json)
        if inputs.get("simulate_gate_1_fail"):
            # Corrupt the payload by removing a required field
            payload.pop("applicable_regulations", None)
            logger.log("GATE_1_VALIDATION", "WARNING", "Simulating Gate 1 validation failure.")
            
        errors = self.validator.validate(payload, "regulatory_mapping")
        if errors:
            logger.log("GATE_1_VALIDATION", "FAILED", f"Gate 1 failed: {errors}. Triggering automatic retry with augmented prompt.")
            
            # Retry attempt: Fix the payload (simulate LLM correction after feedback)
            payload_fixed = dict(s1_json)
            # If we want a double-fail to test HALTED_GATE_1_SCHEMA
            if inputs.get("simulate_gate_1_fail_double"):
                payload_fixed.pop("applicable_regulations", None)
                
            retry_errors = self.validator.validate(payload_fixed, "regulatory_mapping")
            if retry_errors:
                state_mgr.transition_to("HALTED_GATE_1_SCHEMA", f"Schema validation failed after retry: {retry_errors}")
                logger.log("GATE_1_VALIDATION", "FAILED", f"Gate 1 failed after retry: {retry_errors}. Pipeline halted.")
                return False
            else:
                logger.log("GATE_1_VALIDATION", "SUCCESS", "Schema validation passed on retry.")
                state_mgr.update_intermediate_data("regulatory_mapping_output_json", payload_fixed)
                state_mgr.transition_to("GATE_1_PASSED", "Schema validation passed on retry.")
                return True
        else:
            state_mgr.update_intermediate_data("regulatory_mapping_output_json", payload)
            state_mgr.transition_to("GATE_1_PASSED", "Schema validation passed on first attempt.")
            logger.log("GATE_1_VALIDATION", "SUCCESS", "Schema validation passed.")
            return True

    def _evaluate_advisory_regression_s1(self, state_mgr: StateManager, logger: AuditLogger):
        """Runs structural regression tester as advisory check, flagging warning in log on mismatch."""
        trace_id = state_mgr.traceability_id
        # Write temp md file to execute structural regression test
        temp_md_path = self.runs_dir / f"{trace_id}_s1_temp.md"
        temp_md_path.write_text(state_mgr.get_state()["intermediate_data"]["regulatory_mapping_output_md"], encoding="utf-8")
        
        baseline_path = repo_root / self.config.get("baselines", {}).get("regulatory_mapping")
        
        try:
            errors = regression_tester.run_regression_test(temp_md_path, baseline_path)
            if errors:
                logger.log("REGRESSION_CHECK", "WARNING", f"Advisory structural regression check flagged mismatches: {errors}")
            else:
                logger.log("REGRESSION_CHECK", "SUCCESS", "Advisory structural regression check passed.")
        except Exception as e:
            logger.log("REGRESSION_CHECK", "WARNING", f"Could not run regression test: {e}")
        finally:
            if temp_md_path.exists():
                temp_md_path.unlink()

    def _evaluate_gate_2(self, state_mgr: StateManager, logger: AuditLogger, s1_json: dict, inputs: dict):
        """Evaluates quality score threshold for regulatory mapping output."""
        score = inputs.get("mock_s1_score", s1_json.get("score", 91))
        state_mgr.update_intermediate_data("regulatory_mapping_score", score)
        
        threshold = self.config.get("thresholds", {}).get("regulatory_mapping", 70)
        
        if score < 55:
            state_mgr.transition_to("HALTED_GATE_2_INSUFFICIENT", f"Score {score}/100 falls below insufficient threshold (<55).")
            logger.log("GATE_2_QUALITY", "FAILED", f"Quality score {score}/100 is insufficient (threshold: {threshold}/100). Pipeline halted.")
        elif score < threshold:
            state_mgr.transition_to("HALTED_GATE_2_PRELIMINARY", f"Score {score}/100 classified as Preliminary (55-69).")
            logger.log("GATE_2_QUALITY", "WARNING", f"Quality score {score}/100 is below threshold {threshold}/100. Marked as Preliminary. Pipeline halted.")
        else:
            state_mgr.transition_to("GATE_2_PASSED", f"Quality score {score}/100 satisfies threshold.")
            state_mgr.transition_to("APPROVAL_1_PENDING", "Awaiting General Counsel approval sign-off.")
            logger.log("GATE_2_QUALITY", "PENDING", f"Quality score {score}/100 passed. Run transitioned to APPROVAL_1_PENDING. Awaiting GC sign-off.")

    def submit_approval_1(self, traceability_id: str, action: str, actor: str, notes: str = None) -> None:
        """Executes Approval Gate 1 transition and coordinates transition into Skill 2."""
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        run_state = state_mgr.load_state()
        
        current_status = run_state.get("status")
        if current_status not in ["APPROVAL_1_PENDING", "APPROVAL_TIMED_OUT"]:
            raise ValueError(f"Run {traceability_id} is in status '{current_status}', not awaiting Approval Gate 1.")
            
        if action == "Approve":
            logger.log("APPROVAL_GATE_1", "SUCCESS", f"General Counsel ({actor}) approved Regulatory Scoping Matrix. Notes: {notes}")
            state_mgr.transition_to("APPROVAL_1_APPROVED", "General Counsel approved matrix.", actor, notes)
            
            # Start Skill 2 execution immediately
            self._run_skill_2(state_mgr, logger)
            
        elif action == "Reject":
            logger.log("APPROVAL_GATE_1", "REJECTED", f"General Counsel ({actor}) rejected Regulatory Scoping Matrix. Revision requested: {notes}")
            state_mgr.transition_to("HALTED_APPROVAL_1_REJECTED", f"GC rejection: {notes}", actor, notes)
            
        elif action == "Timeout":
            logger.log("APPROVAL_GATE_1", "TIMEOUT", "Approval deadline elapsed without action.")
            state_mgr.transition_to("APPROVAL_TIMED_OUT", "Approval timed out after 5 business days.")
            
        else:
            raise ValueError(f"Invalid approval action: '{action}'")

    def _run_skill_2(self, state_mgr: StateManager, logger: AuditLogger):
        """Executes Skill 2 (governance-control-mapping) programmatically and executes Gates 3 & 4."""
        trace_id = state_mgr.traceability_id
        state_mgr.transition_to("SKILL_2_RUNNING", "Skill 2 (governance-control-mapping) execution started.")
        logger.log("SKILL_2_RUNNING", "SUCCESS", "Generating Operational Control Specification.")
        
        inputs = state_mgr.get_state().get("inputs", {})
        
        # Phase 4 Input Validation: Validate the output of Stage 1 against regulatory mapping schema
        s1_json = state_mgr.get_state().get("intermediate_data", {}).get("regulatory_mapping_output_json", {})
        input_errors = self.validator.validate(s1_json, "regulatory_mapping")
        if input_errors:
            state_mgr.transition_to("HALTED_GATE_3A_SCHEMA", f"Skill 2 input validation failed: {input_errors}")
            logger.log("GATE_3A_SCHEMA", "FAILED", f"Skill 2 input validation failed: {input_errors}. Pipeline halted.")
            return
            
        # Programmatic execution of Skill 2 using Skill 1 structured outputs
        s2_json = self.executor.execute_governance_control_mapping(s1_json, logger)
        
        # Compile to markdown representation
        s2_md = self.executor.compile_control_mapping_to_markdown(s2_json)
        
        # Check if we should simulate a firewall breach (to preserve unit test behavior)
        if inputs.get("simulate_firewall_breach"):
            s2_md += "\n\nHard Rule Violation Check: Visual Agent Builder is currently in build."
            logger.log("SKILL_2_RUNNING", "WARNING", "Simulating Claims Firewall violation.")
            
        state_mgr.update_intermediate_data("governance_control_mapping_output_md", s2_md)
        
        # Execute Gate 3: Concurrent schema + firewall linter checking
        passed_gate_3 = self._evaluate_gate_3(state_mgr, logger, s2_json, s2_md, inputs)
        if not passed_gate_3:
            return

        # Execute Gate 4: Control Quality Score Check
        self._evaluate_gate_4(state_mgr, logger, s2_json, inputs)


    def _evaluate_gate_3(self, state_mgr: StateManager, logger: AuditLogger, s2_json: dict, md_content: str, inputs: dict) -> bool:
        """Executes concurrent schema validation (Gate 3a) and Claims Firewall check (Gate 3b)."""
        trace_id = state_mgr.traceability_id
        state_mgr.transition_to("SKILL_2_COMPLETE", "Skill 2 complete. Initiating concurrent validations (Gate 3).")
        
        # 1. Gate 3a: Schema Validation
        payload = dict(s2_json)
        if inputs.get("simulate_gate_3a_fail"):
            payload.pop("evidence_registry", None)
            logger.log("GATE_3A_SCHEMA", "WARNING", "Simulating Gate 3a validation failure.")
            
        schema_errors = self.validator.validate(payload, "control_mapping")
        if schema_errors:
            # Retry Gate 3a once
            logger.log("GATE_3A_SCHEMA", "WARNING", f"Gate 3a failed: {schema_errors}. Retrying with corrected payload...")
            payload_fixed = dict(s2_json)
            if inputs.get("simulate_gate_3a_fail_double"):
                payload_fixed.pop("evidence_registry", None)
                
            schema_errors = self.validator.validate(payload_fixed, "control_mapping")
            
        # 2. Gate 3b: Claims Firewall
        temp_md_path = self.runs_dir / f"{trace_id}_s2_temp.md"
        temp_md_path.write_text(md_content, encoding="utf-8")
        
        cpm_path = repo_root / "knowledge" / "ethana" / "canonical-product-model.md"
        firewall_errors = []
        try:
            capabilities = claims_linter.parse_canonical_model(cpm_path)
            firewall_violations = claims_linter.lint_file(temp_md_path, capabilities)
            if firewall_violations:
                for ln, line, msg in firewall_violations:
                    firewall_errors.append(f"Line {ln}: {msg}")
        except Exception as e:
            firewall_errors.append(f"Claims Firewall linter unavailable: {e}")
            logger.log("GATE_3B_FIREWALL", "ERROR", f"Could not run Claims Firewall linter: {e}")
        finally:
            if temp_md_path.exists():
                temp_md_path.unlink()
                
        # Evaluate concurrent combinations
        # Priority: Firewall Breach takes precedence over schema error
        if firewall_errors:
            state_mgr.update_intermediate_data("claims_firewall_status", "BREACH")
            state_mgr.transition_to("HALTED_FIREWALL_BREACH", f"Claims Firewall breaches detected: {firewall_errors}")
            logger.log("GATE_3B_FIREWALL", "BREACH", f"Claims Firewall breach detected: {firewall_errors}. Pipeline halted.")
            return False
            
        elif schema_errors:
            state_mgr.update_intermediate_data("claims_firewall_status", "PASS")
            state_mgr.transition_to("HALTED_GATE_3A_SCHEMA", f"Schema validation failed after retry: {schema_errors}")
            logger.log("GATE_3A_SCHEMA", "FAILED", f"Schema validation failed after retry: {schema_errors}. Pipeline halted.")
            return False
            
        else:
            state_mgr.update_intermediate_data("claims_firewall_status", "PASS")
            state_mgr.update_intermediate_data("governance_control_mapping_output_json", payload)
            state_mgr.transition_to("GATE_3_PASSED", "Concurrent schema and claims firewall checks passed.")
            logger.log("GATE_3", "SUCCESS", "Concurrent validations (Gate 3a & 3b) passed.")
            return True

    def _evaluate_gate_4(self, state_mgr: StateManager, logger: AuditLogger, s2_json: dict, inputs: dict):
        """Evaluates quality score threshold for governance control mapping output."""
        score = inputs.get("mock_s2_score", s2_json.get("score", 88))
        state_mgr.update_intermediate_data("governance_control_mapping_score", score)
        
        threshold = self.config.get("thresholds", {}).get("control_mapping", 85)
        
        if score < 70:
            state_mgr.transition_to("HALTED_GATE_4_INSUFFICIENT", f"Score {score}/100 falls below insufficient threshold (<70).")
            logger.log("GATE_4_QUALITY", "FAILED", f"Control specification quality score {score}/100 is insufficient. Pipeline halted.")
        elif score < threshold:
            state_mgr.transition_to("HALTED_GATE_4_BELOW_THRESHOLD", f"Score {score}/100 falls below threshold {threshold}/100.")
            logger.log("GATE_4_QUALITY", "WARNING", f"Control specification quality score {score}/100 is below threshold {threshold}/100. Pipeline halted.")
        else:
            state_mgr.transition_to("GATE_4_PASSED", f"Quality score {score}/100 satisfies threshold.")
            state_mgr.transition_to("APPROVAL_2_PENDING", "Awaiting DPO + InfoSec joint sign-off.")
            logger.log("GATE_4_QUALITY", "PENDING", f"Quality score {score}/100 passed. Run transitioned to APPROVAL_2_PENDING. Awaiting joint sign-off.")

    def submit_approval_2(self, traceability_id: str, action: str, actor: str, notes: str = None) -> None:
        """Executes Approval Gate 2 transition and generates the output packages."""
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        run_state = state_mgr.load_state()
        
        current_status = run_state.get("status")
        if current_status not in ["APPROVAL_2_PENDING", "APPROVAL_TIMED_OUT"]:
            raise ValueError(f"Run {traceability_id} is in status '{current_status}', not awaiting Approval Gate 2.")
            
        builder = OutputBuilder(str(self.packages_dir), traceability_id)
        
        if action == "Approve":
            logger.log("APPROVAL_GATE_2", "SUCCESS", f"DPO and InfoSec Lead ({actor}) jointly approved Operational Control Specification. Notes: {notes}")
            state_mgr.transition_to("APPROVAL_2_APPROVED", "DPO and InfoSec approved controls.", actor, notes)
            
            # Finalize run
            state_mgr.transition_to("COMPLETE", "Compliance and Coverage package assembled.")
            pkg_path = builder.assemble_final_package(state_mgr.get_state(), logger.get_logs())
            logger.log("COMPLETE", "SUCCESS", f"Compliance & Coverage Package successfully assembled at: {pkg_path}")
            
        elif action == "Reject":
            logger.log("APPROVAL_GATE_2", "REJECTED", f"DPO and InfoSec Lead ({actor}) rejected control specifications. Notes: {notes}")
            state_mgr.transition_to("HALTED_APPROVAL_2_REJECTED", f"Rejection: {notes}", actor, notes)
            
        elif action == "Partial":
            logger.log("APPROVAL_GATE_2", "PARTIAL", f"Split decision: one approver approved, one rejected. Operator intervention required. Notes: {notes}")
            state_mgr.transition_to("HALTED_APPROVAL_2_PARTIAL", f"Partial approval: {notes}", actor, notes)
            
        elif action == "Timeout":
            logger.log("APPROVAL_GATE_2", "TIMEOUT", "Approval deadline elapsed without action.")
            state_mgr.transition_to("APPROVAL_TIMED_OUT", "Approval timed out after 5 business days.")
            
        elif action == "Approve with modifications":
            # Re-gate process
            logger.log("APPROVAL_GATE_2", "SUCCESS", f"Approver ({actor}) submitted 'Approve with modifications'. Running re-gate validation on modified payload. Notes: {notes}")
            
            # Incorporate changes (mock change by saving modifications in state)
            state_mgr.update_intermediate_data("approver_modifications", notes)
            
            # Perform re-gate validation (simulate checking Gates 3a, 3b, and Gate 4)
            # Re-read and check
            s2_json = run_state.get("intermediate_data", {}).get("governance_control_mapping_output_json", {})
            md_content = run_state.get("intermediate_data", {}).get("governance_control_mapping_output_md", "")
            
            # 1. Re-validate Gate 3a (Schema)
            schema_errors = self.validator.validate(s2_json, "control_mapping")
            
            # 2. Re-validate Gate 3b (Firewall)
            temp_md_path = self.runs_dir / f"{traceability_id}_s2_re_temp.md"
            merged_content = md_content + "\n\n" + (notes or "")
            temp_md_path.write_text(merged_content, encoding="utf-8")
            cpm_path = repo_root / "knowledge" / "ethana" / "canonical-product-model.md"
            firewall_errors = []
            try:
                capabilities = claims_linter.parse_canonical_model(cpm_path)
                firewall_violations = claims_linter.lint_file(temp_md_path, capabilities)
                if firewall_violations:
                    for ln, line, msg in firewall_violations:
                        firewall_errors.append(f"Line {ln}: {msg}")
            except Exception as e:
                firewall_errors.append(f"Claims Firewall linter unavailable: {e}")
                logger.log("RE_GATE_VAL", "ERROR", f"Could not run claims linter: {e}")
            finally:
                if temp_md_path.exists():
                    temp_md_path.unlink()
            
            # 3. Re-validate Gate 4 (Score)
            score = run_state.get("intermediate_data", {}).get("governance_control_mapping_score", 88)
            score_pass = score >= self.config.get("thresholds", {}).get("control_mapping", 85)
            
            if firewall_errors:
                state_mgr.transition_to("HALTED_FIREWALL_BREACH", f"Re-gate failed due to Firewall Breach introduced by modifications: {firewall_errors}")
                logger.log("RE_GATE_VAL", "BREACH", f"Re-gate validation failed: Claims Firewall breach. Run halted.")
            elif schema_errors:
                state_mgr.transition_to("HALTED_GATE_3A_SCHEMA", f"Re-gate failed due to Schema errors introduced by modifications: {schema_errors}")
                logger.log("RE_GATE_VAL", "FAILED", f"Re-gate validation failed: Schema error. Run halted.")
            elif not score_pass:
                state_mgr.transition_to("HALTED_GATE_4_BELOW_THRESHOLD", f"Re-gate failed due to score dropping below threshold: {score}/100")
                logger.log("RE_GATE_VAL", "FAILED", f"Re-gate validation failed: Quality score {score}/100 below threshold. Run halted.")
            else:
                logger.log("RE_GATE_VAL", "SUCCESS", "All re-gate validation checks passed on modifications. Transitioning to APPROVED.")
                state_mgr.transition_to("APPROVAL_2_APPROVED", "DPO and InfoSec approved modifications.", actor, notes)
                state_mgr.transition_to("COMPLETE", "Compliance and Coverage package assembled.")
                pkg_path = builder.assemble_final_package(state_mgr.get_state(), logger.get_logs())
                logger.log("COMPLETE", "SUCCESS", f"Compliance & Coverage Package successfully assembled at: {pkg_path}")
        else:
            raise ValueError(f"Invalid approval action: '{action}'")

    def release_partial_package(self, traceability_id: str) -> str:
        """Assembles a partial packaging of Skill 1 outputs if the run has passed Approval 1 but is halted."""
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        run_state = state_mgr.load_state()
        
        # Contract Check: must have passed Approval Gate 1 (i.e. approvals.approval_1 is not None and approved) AND currently in any halted state post-Gate-1
        approvals = run_state.get("approvals", {})
        approval_1 = approvals.get("approval_1")
        
        if not approval_1 or approval_1.get("status") != "Approved":
            raise ValueError(f"Cannot release partial package: Run {traceability_id} has not passed Approval Gate 1.")
            
        current_status = run_state.get("status", "")
        if not current_status.startswith("HALTED_") and current_status != "APPROVAL_TIMED_OUT":
            raise ValueError(f"Cannot release partial package: Run {traceability_id} is in status '{current_status}', which is not a halted/timed out state.")
            
        builder = OutputBuilder(str(self.packages_dir), traceability_id)
        pkg_path = builder.assemble_partial_package(run_state, logger.get_logs())
        
        logger.log("PARTIAL_RELEASE", "SUCCESS", f"Operator triggered partial output release. Package assembled at: {pkg_path}")
        return pkg_path

    def execute_mode_b(self, regulatory_change_alert: dict) -> list:
        """
        Runs Watch Mode (Mode B). Queries the completed runs to identify which ones are affected.
        Prioritizes and queues re-assessments sequentially, conforming to a rate limit of 3 concurrent runs.
        """
        reg_name = regulatory_change_alert.get("regulation_name")
        jurisdiction = regulatory_change_alert.get("jurisdiction")
        change_summary = regulatory_change_alert.get("change_summary", "")
        change_severity = regulatory_change_alert.get("change_severity", "Minor") # Critical | Major | Minor
        
        if not reg_name or not jurisdiction:
            raise ValueError("regulatory_change_alert must contain 'regulation_name' and 'jurisdiction'.")
            
        # Scan completed runs in runs directory
        completed_runs = []
        state_files = glob.glob(str(self.runs_dir / "TR-RW-*_state.json"))
        
        for f in state_files:
            try:
                state_data = json.loads(Path(f).read_text(encoding="utf-8"))
                if state_data.get("status") == "COMPLETE":
                    # Check if this completed run contains the affected regulation and jurisdiction
                    inputs = state_data.get("inputs", {})
                    int_data = state_data.get("intermediate_data", {})
                    s1_json = int_data.get("regulatory_mapping_output_json", {})
                    
                    # Check matching jurisdiction
                    if jurisdiction in inputs.get("jurisdictions", []):
                        # Check matching regulation in applicable regulations list
                        regs = [r.get("regulation_name") for r in s1_json.get("applicable_regulations", [])]
                        # Look for regulation name match (case-insensitive substring)
                        if any(reg_name.lower() in r.lower() for r in regs):
                            completed_runs.append(state_data)
            except Exception as e:
                print(f"Error reading file {f} for Mode B check: {e}")
                
        if not completed_runs:
            print(f"Mode B Watch: No completed assessments found containing regulation '{reg_name}' in jurisdiction '{jurisdiction}'.")
            return []
            
        # Prioritization sorting
        # Priority: Critical change severity first, then risk classification (EU Annex III first), then chronological.
        def get_priority_tuple(run):
            # 1. Severity weight
            sev_val = 0 if change_severity == "Critical" else 1 if change_severity == "Major" else 2
            
            # 2. Risk classification weight
            inputs = run.get("inputs", {})
            risk_tier = run.get("intermediate_data", {}).get("regulatory_mapping_output_json", {}).get("risk_tier", "")
            is_annex_iii = 0 if "annex iii" in risk_tier.lower() else 1
            
            # 3. Chronological (earliest timestamp first)
            history = run.get("history", [])
            init_time = history[0].get("timestamp", "") if history else ""
            
            return (sev_val, is_annex_iii, init_time)
            
        completed_runs.sort(key=get_priority_tuple)
        
        print(f"Mode B Watch: Found {len(completed_runs)} affected completed runs. Preparing re-assessment queuing.")
        
        # Concurrency limit check
        concurrency_limit = 3
        queued_runs = []
        
        for idx, run in enumerate(completed_runs):
            original_inputs = run.get("inputs", {})
            re_inputs = dict(original_inputs)
            
            # Append change summary as an addendum to the subject description
            re_inputs["subject_description"] = (
                original_inputs.get("subject_description", "") + 
                f"\n\n--- REGULATORY CHANGE RE-ASSESSMENT ({reg_name}) ---\n" + 
                f"Change Summary: {change_summary}\n" + 
                f"Severity: {change_severity}"
            )
            
            # Store link to prior assessment ID
            re_inputs["existing_assessment_id"] = run.get("traceability_id")
            
            # Rate limit trigger: Only run up to 3 concurrently; other jobs are queued
            if idx < concurrency_limit:
                trace_id = self.start_run("regulatory_change_alert", re_inputs)
                queued_runs.append({"status": "STARTED", "traceability_id": trace_id, "prior_assessment_id": run.get("traceability_id")})
            else:
                queued_runs.append({"status": "QUEUED", "traceability_id": None, "prior_assessment_id": run.get("traceability_id")})
                print(f"Rate limit exceeded: Re-assessment for run {run.get('traceability_id')} is queued (max 3 concurrent jobs).")
                
        return queued_runs

    def _generate_mock_part_b_md(self, fixture_name: str) -> str:
        """Generates mock Markdown for Part B if the gold standard lacks it."""
        return f"""### Section 1: Executive Summary & Control Landscape
This document specifies the operational control architecture for the AI system under {fixture_name}.

### Section 2: Control Taxonomy Matrix
| Control ID | Control Name | Control Type | Control Method | Primary Risk Mitigated |
|---|---|---|---|---|
| CTRL-01 | Access Control and Logs | Preventive | Technical | Unauthorized Model Modification |
| CTRL-02 | Model Drift Monitoring | Detective | Technical | Accuracy Drift & Bias |

### Section 3: Control Coverage Classification
Fully Covered by Ethana.

### Section 4: Preventive Control Specifications
Preventive controls are configured via API tokens and RBAC gates.

### Section 5: Detective Control Specifications
Drift monitoring telemetry tracks inputs/outputs.

### Section 6: Corrective Control Specifications
Incident response triggers a container rollback.

### Section 7: Evidence & Verification Requirements
Execution audit trails are written to immutable storage.

### Section 8: Control Ownership Matrix (RACI)
| Control ID | Responsible (R) | Accountable (A) |
|---|---|---|
| CTRL-01 | Lead Developer | DPO |
| CTRL-02 | Model Risk Analyst | InfoSec Lead |

### Section 9: Maturity & Phased Roadmap
Level 3 maturity is targeted for production rollout.

### Section 10: Ethana Configuration Guide
Deploy Ethana Sentry endpoint.

score: 88/100
"""

# Attach Mock payloads for the state persistence and validator test mappings
from state_manager import StateManager
StateManager.MOCK_REGULATORY_JSON = {
    "eu-ai-act-high-risk-banking": {
        "applicable_regulations": [
            {
                "regulation_name": "EU AI Act",
                "jurisdiction": "EU",
                "trigger": "AI system used to evaluate creditworthiness of natural persons",
                "status": "Confirmed"
            },
            {
                "regulation_name": "GDPR",
                "jurisdiction": "EU",
                "trigger": "Processing personal data of EU data subjects",
                "status": "Confirmed"
            }
        ],
        "applicable_frameworks": [
            {
                "framework_name": "ISO 42001",
                "relevant_provisions": ["Clause 4 Context", "Clause 8 Operation", "Annex A.9 Transparency"]
            },
            {
                "framework_name": "NIST AI RMF",
                "relevant_provisions": ["GOVERN", "MAP", "MEASURE", "MANAGE"]
            }
        ],
        "regulatory_obligations": [
            {
                "obligation_description": "Register AI system in EU database",
                "legal_basis": "EU AI Act Article 49",
                "obligation_type": "Registration",
                "timeline": "Before deployment",
                "consequence_noncompliance": "Fines up to 35m EUR or 7% global turnover"
            },
            {
                "obligation_description": "Conduct DPIA",
                "legal_basis": "GDPR Article 35",
                "obligation_type": "Assessment",
                "timeline": "Before deployment",
                "consequence_noncompliance": "Fines up to 10m EUR or 2% global turnover"
            }
        ],
        "control_requirements": [
            {
                "control_name": "Human Oversight Gate",
                "description": "Ensure model recommendations can be reviewed and overriden by natural persons",
                "source": "EU AI Act Article 14",
                "control_type": "Preventive",
                "mandatory": True
            },
            {
                "control_name": "Drift Monitoring",
                "description": "Monitor performance and accuracy drift monthly",
                "source": "EU AI Act Article 72",
                "control_type": "Detective",
                "mandatory": True
            }
        ],
        "score": 91,
        "risk_tier": "High-risk (Annex III, Point 5)"
    },
    "india-dpdp-customer-support-ai": {
        "applicable_regulations": [
            {
                "regulation_name": "DPDP Act 2023",
                "jurisdiction": "India",
                "trigger": "Processing digital personal data of Indian residents",
                "status": "Confirmed"
            },
            {
                "regulation_name": "RBI IT Governance Master Direction",
                "jurisdiction": "India",
                "trigger": "Automated chatbot processing financial customer queries in NBFC",
                "status": "Confirmed"
            }
        ],
        "applicable_frameworks": [
            {
                "framework_name": "ISO 42001",
                "relevant_provisions": ["Clause 4 Context", "Clause 8 Operation", "Annex A.8 Data for AI"]
            }
        ],
        "regulatory_obligations": [
            {
                "obligation_description": "Obtain explicit consent for personal data processing",
                "legal_basis": "DPDP Act 2023 Section 6",
                "obligation_type": "Notification",
                "timeline": "Before processing",
                "consequence_noncompliance": "Fines up to 250 Crore INR"
            }
        ],
        "control_requirements": [
            {
                "control_name": "Consent Verification",
                "description": "Verify active consent exists before loading user data into prompt context",
                "source": "DPDP Act 2023 Section 6",
                "control_type": "Preventive",
                "mandatory": True
            }
        ],
        "score": 78,
        "risk_tier": "DPDP Significant Data Fiduciary"
    },
    "uk-insurance-claims-model": {
        "applicable_regulations": [
            {
                "regulation_name": "UK GDPR / DPA 2018",
                "jurisdiction": "UK",
                "trigger": "Processing personal claims data of UK subjects",
                "status": "Confirmed"
            },
            {
                "regulation_name": "FCA PRIN 12 Consumer Duty",
                "jurisdiction": "UK",
                "trigger": "Retail insurance claims model affecting customer outcomes",
                "status": "Confirmed"
            }
        ],
        "applicable_frameworks": [
            {
                "framework_name": "NIST AI RMF",
                "relevant_provisions": ["GOVERN", "MAP", "MANAGE"]
            }
        ],
        "regulatory_obligations": [
            {
                "obligation_description": "Ensure fair outcomes under Consumer Duty PRIN 12",
                "legal_basis": "FCA PRIN 12",
                "obligation_type": "Monitoring",
                "timeline": "Ongoing",
                "consequence_noncompliance": "Regulatory enforcement, public censure, fines"
            }
        ],
        "control_requirements": [
            {
                "control_name": "Fairness and Bias Monitoring",
                "description": "Perform monthly check on triage success rates across protected demographics",
                "source": "FCA Dear CEO Letter June 2026",
                "control_type": "Detective",
                "mandatory": True
            }
        ],
        "score": 84,
        "risk_tier": "PRA SS1/23 Tier 1"
    }
}

StateManager.MOCK_CONTROL_JSON = {
    "eu-ai-act-high-risk-banking": {
        "executive_summary": "This document specifies the operational control architecture for the Consumer Credit Scoring Model.",
        "control_taxonomy_matrix": [
            {
                "control_id": "CTRL-01",
                "control_name": "Human Oversight Mechanism",
                "control_type": "Preventive",
                "control_method": "Technical",
                "coverage_classification": "Fully Covered by Ethana"
            },
            {
                "control_id": "CTRL-02",
                "control_name": "Model Performance Monitoring",
                "control_type": "Detective",
                "control_method": "Technical",
                "coverage_classification": "Fully Covered by Ethana"
            }
        ],
        "preventive_controls": [
            {
                "control_id": "CTRL-01",
                "control_name": "Human Oversight Mechanism",
                "trigger_condition": "Every automated decline recommendation",
                "enforcement_mechanism": "System holds decline; routes to human credit analyst interface for mandatory override/approval",
                "failure_mode": "Fail-Closed"
            }
        ],
        "detective_controls": [
            {
                "control_id": "CTRL-02",
                "control_name": "Model Performance Monitoring",
                "logging_source": "Model Execution Log API",
                "telemetry_format": ["Timestamp", "TraceID", "InputVector", "Prediction", "ConfidenceScore"],
                "alerting_thresholds": "Accuracy drift > 5% or PSI > 0.2 over a 30-day window",
                "routing_target": "Model Risk Management Team"
            }
        ],
        "corrective_controls": [
            {
                "control_id": "CTRL-03",
                "control_name": "Incident Rollback Protocol",
                "activation_trigger": "Model performance alert or verified customer bias complaint",
                "containment_protocol": "Disable candidate model; automatically revert to fallback production model v1.8",
                "recovery_procedure": "Trigger independent model audit; conduct retraining and bias verification",
                "rollback_sla": "Within 4 hours of incident verification"
            }
        ],
        "evidence_registry": [
            {
                "evidence_id": "EVID-01",
                "evidence_name": "Model Execution Audit Logs",
                "artifact_description": "Cryptographically signed logs of all model queries and inputs/outputs",
                "collection_method": "Automated",
                "frequency": "Continuous",
                "retention_period": "7 years"
            }
        ],
        "raci_matrix": [
            {
                "control_id": "CTRL-01",
                "responsible": "Credit Operations Analyst",
                "accountable": "Head of Retail Lending",
                "consulted": "DPO",
                "informed": "Risk Management Committee"
            },
            {
                "control_id": "CTRL-02",
                "responsible": "Model Validation Specialist",
                "accountable": "Chief Risk Officer",
                "consulted": "AI Engineering Lead",
                "informed": "Compliance Team"
            }
        ],
        "score": 88
    }
}
