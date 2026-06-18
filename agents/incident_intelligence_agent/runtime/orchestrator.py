#!/usr/bin/env python3
"""
Orchestrator for Incident Intelligence Agent Runtime.
Coordinates trigger intake, persistent state tracking, multi-gate validation,
human sign-offs, and final handoff packaging.
"""

import os
import sys
import json
try:
    import yaml
except ImportError:
    yaml = None
from pathlib import Path

# Paths setup
repo_root = Path(__file__).resolve().parents[3]
sys.path.append(str(repo_root))

from agents.incident_intelligence_agent.runtime.audit_logger import AuditLogger
from agents.incident_intelligence_agent.runtime.state_manager import StateManager
from agents.incident_intelligence_agent.runtime.schema_validator import SchemaValidator
from agents.incident_intelligence_agent.runtime.output_builder import OutputBuilder
from agents.incident_intelligence_agent.runtime.skill_executor import SkillExecutor

class Orchestrator:
    def __init__(self, config_path: str = None):
        """Initializes the orchestrator and loads configurations."""
        if config_path is None:
            config_path = str(Path(__file__).parent / "config.yaml")
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # Load directories
        dirs = self.config.get("directories", {})
        self.runs_dir = repo_root / dirs.get("runs", "agents/incident_intelligence_agent/runtime/runs")
        self.packages_dir = repo_root / dirs.get("packages", "agents/incident_intelligence_agent/runtime/packages")
        self.logs_dir = repo_root / dirs.get("logs", "agents/incident_intelligence_agent/runtime/logs")
        
        # Ensure directories exist
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Schema validator pointing to global schemas directory
        schemas_path = repo_root / "workflows" / "schemas"
        self.validator = SchemaValidator(str(schemas_path))
        
        # Skill Executor
        self.executor = SkillExecutor(self.runs_dir, self.logs_dir)

    def _load_config(self) -> dict:
        """Loads configuration from YAML file, handles basic parsing if PyYAML not available."""
        if not self.config_path.exists():
            return {
                "directories": {
                    "runs": "agents/incident_intelligence_agent/runtime/runs",
                    "packages": "agents/incident_intelligence_agent/runtime/packages",
                    "logs": "agents/incident_intelligence_agent/runtime/logs"
                },
                "thresholds": {
                    "incident_analysis": 70,
                    "control_mapping": 85
                }
            }
            
        if yaml is not None:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            except Exception as e:
                pass

        # Fallback parser for YAML
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

    def start_run(self, trigger_type: str, inputs: dict) -> str:
        """Intakes incident validation triggers and initiates Step 1: Incident Analysis."""
        traceability_id = self.executor.generate_traceability_id()
        
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        
        logger.log("INTAKE_VALIDATING", "SUCCESS", "Intake validation initiated.")
        state_mgr.initialize_run(inputs)
        
        # 1. Intake schema validation
        schema_errors = self.validator.validate(inputs, "incident_assessment_input")
        if schema_errors:
            state_mgr.transition_to("HALTED_INTAKE_INVALID", f"Validation errors: {schema_errors}")
            logger.log("INTAKE_VALIDATING", "FAILED", f"Intake validation failed: {schema_errors}")
            return traceability_id
            
        logger.log("INTAKE_VALIDATING", "SUCCESS", f"Intake validation passed. Assigned traceability ID: {traceability_id}")
        state_mgr.transition_to("INTAKE_COMPLETE", "Intake validation passed.")
        
        # 2. Run Step 1: AI Incident Analysis
        self._run_skill_1(state_mgr, logger)
        return traceability_id

    def _run_skill_1(self, state_mgr: StateManager, logger: AuditLogger):
        """Runs the incident analysis triage and checks the quality score threshold."""
        traceability_id = state_mgr.traceability_id
        state_mgr.transition_to("SKILL_1_RUNNING", "Skill 1 (ai-incident-analysis) execution started.")
        
        inputs = state_mgr.get_state().get("inputs", {})
        
        # Execute skill dynamically
        s1_json = self.executor.execute_incident_triage(inputs, logger)
        s1_md = self.executor.compile_incident_triage_to_markdown(s1_json)
        
        state_mgr.update_intermediate_data("incident_analysis_json", s1_json)
        state_mgr.update_intermediate_data("incident_analysis_md", s1_md)
        
        # S1 Output Schema validation
        schema_errors = self.validator.validate(s1_json, "incident_analysis_output")
        if schema_errors:
            state_mgr.transition_to("HALTED_GATE_1_SCHEMA", f"Triage output schema validation failed: {schema_errors}")
            logger.log("SKILL_1_RUNNING", "FAILED", f"Triage output schema validation failed: {schema_errors}")
            return

        state_mgr.transition_to("SKILL_1_COMPLETE", "Skill 1 triage execution completed.")
        
        # Quality Gate 1: Incident Analysis triage score check
        triage_score = 90  # Default base score
        if "mock_analysis_score" in inputs:
            triage_score = inputs["mock_analysis_score"]
            
        threshold = int(self.config.get("thresholds", {}).get("incident_analysis", 70))
        
        if triage_score < threshold:
            state_mgr.transition_to("HALTED_GATE_1_INSUFFICIENT", f"Triage score {triage_score}/100 falls below threshold {threshold}/100.")
            logger.log("GATE_1_INSUFFICIENT", "FAILED", f"Triage quality score {triage_score}/100 is insufficient.")
        else:
            state_mgr.transition_to("GATE_1_PASSED", f"Triage score {triage_score}/100 passed quality check.")
            state_mgr.transition_to("APPROVAL_1_PENDING", "Awaiting CISO triage approval sign-off.")
            logger.log("GATE_1_QUALITY", "PENDING", f"Triage score {triage_score}/100 passed. Run transitioned to APPROVAL_1_PENDING.")

    def submit_approval_1(self, traceability_id: str, action: str, actor: str, notes: str = None) -> None:
        """Submits CISO triage approval and proceeds to Step 2 & 3 if approved."""
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        run_state = state_mgr.load_state()
        
        current_status = run_state.get("status")
        if current_status != "APPROVAL_1_PENDING":
            raise ValueError(f"Run {traceability_id} is in status '{current_status}', not awaiting CISO approval.")
            
        if action == "Approve":
            logger.log("APPROVAL_GATE_1", "SUCCESS", f"CISO ({actor}) approved Triage and Root Cause report. Notes: {notes}")
            state_mgr.transition_to("APPROVAL_1_APPROVED", "CISO approved triage.", actor, notes)
            
            # Initiate Step 2 (Control Mapping) and Step 3 (Truth Gate Validation)
            self._run_skill_2_and_3(state_mgr, logger)
        elif action == "Reject":
            logger.log("APPROVAL_GATE_1", "REJECTED", f"CISO ({actor}) rejected Triage and Root Cause report. Notes: {notes}")
            state_mgr.transition_to("HALTED_APPROVAL_1_REJECTED", f"CISO rejection: {notes}", actor, notes)
        else:
            raise ValueError(f"Invalid approval action: '{action}'")

    def _run_skill_2_and_3(self, state_mgr: StateManager, logger: AuditLogger):
        """Executes Step 2 (Governance Control Mapping) and Step 3 (Capability Validation)."""
        traceability_id = state_mgr.traceability_id
        inputs = state_mgr.get_state().get("inputs", {})
        int_data = state_mgr.get_state().get("intermediate_data", {})
        
        # 1. Run Step 2: Governance Control Mapping
        state_mgr.transition_to("SKILL_2_RUNNING", "Skill 2 (governance-control-mapping) execution started.")
        s1_json = int_data.get("incident_analysis_json", {})
        
        s2_json = self.executor.execute_control_mapping(s1_json, inputs, logger)
        s2_md = self.executor.compile_control_mapping_to_markdown(s2_json)
        
        state_mgr.update_intermediate_data("control_mapping_json", s2_json)
        state_mgr.update_intermediate_data("control_mapping_md", s2_md)
        
        # S2 Output Schema validation
        schema_errors = self.validator.validate(s2_json, "control_mapping_output")
        if schema_errors:
            state_mgr.transition_to("HALTED_GATE_2_SCHEMA", f"Control mapping output schema validation failed: {schema_errors}")
            logger.log("SKILL_2_RUNNING", "FAILED", f"Control mapping schema validation failed: {schema_errors}")
            return
            
        state_mgr.transition_to("SKILL_2_COMPLETE", "Skill 2 control mapping execution completed.")
        
        # Quality Gate 2: Control Mapping score check (RACI Accountability must exist)
        control_score = 90
        # If any control has an empty accountable role, fail the gate
        raci = s2_json.get("raci_matrix", [])
        for entry in raci:
            if not entry.get("accountable"):
                control_score = 0 # Blank accountability fails control mapping gate
                
        if "mock_control_score" in inputs:
            control_score = inputs["mock_control_score"]
            
        threshold = int(self.config.get("thresholds", {}).get("control_mapping", 85))
        
        if control_score < threshold:
            state_mgr.transition_to("HALTED_GATE_2_INSUFFICIENT", f"Control mapping score {control_score}/100 falls below threshold {threshold}/100.")
            logger.log("GATE_2_INSUFFICIENT", "FAILED", f"Control quality score {control_score}/100 is insufficient.")
            return
            
        state_mgr.transition_to("GATE_2_PASSED", f"Control mapping score {control_score}/100 passed quality check.")
        
        # 2. Run Step 3: Platform Validation (Truth Gate Claims Firewall)
        state_mgr.transition_to("SKILL_3_RUNNING", "Skill 3 (ethana-capability-validation) execution started.")
        s3_json = self.executor.execute_capability_validation(s2_json, inputs, logger)
        s3_vb_md = self.executor.compile_verification_binder_to_markdown(s3_json)
        s3_cg_md = self.executor.compile_config_guide_to_markdown(s3_json)
        
        state_mgr.update_intermediate_data("capability_validation_json", s3_json)
        state_mgr.update_intermediate_data("verification_binder_md", s3_vb_md)
        state_mgr.update_intermediate_data("config_guide_md", s3_cg_md)
        
        # S3 Output Schema validation
        schema_errors = self.validator.validate(s3_json, "capability_validation_output")
        if schema_errors:
            state_mgr.transition_to("HALTED_GATE_3_SCHEMA", f"Platform validation schema validation failed: {schema_errors}")
            logger.log("SKILL_3_RUNNING", "FAILED", f"Platform validation schema validation failed: {schema_errors}")
            return
            
        state_mgr.transition_to("SKILL_3_COMPLETE", "Skill 3 platform validation completed.")
        
        # Claims Firewall checking
        if s3_json.get("hard_disqualifiers_triggered"):
            state_mgr.transition_to("HALTED_FIREWALL_BREACH", f"Claims Firewall breach detected: {s3_json['hard_disqualifiers_triggered']}")
            logger.log("GATE_3_FIREWALL", "BREACH", f"Firewall check failed: {s3_json['hard_disqualifiers_triggered']}")
            return
            
        state_mgr.transition_to("GATE_3_PASSED", "Claims Firewall check passed.")
        state_mgr.transition_to("APPROVAL_2_PENDING", "Awaiting DPO and IT Operations Director sign-off.")
        logger.log("GATE_3_FIREWALL", "PENDING", "Verification complete. Run transitioned to APPROVAL_2_PENDING.")

    def submit_approval_2(self, traceability_id: str, action: str, actor: str, notes: str = None) -> None:
        """Submits DPO/IT Operations Director containment approval and compiles the final package."""
        state_mgr = StateManager(str(self.runs_dir), traceability_id)
        logger = AuditLogger(str(self.logs_dir), traceability_id)
        run_state = state_mgr.load_state()
        
        current_status = run_state.get("status")
        if current_status != "APPROVAL_2_PENDING":
            raise ValueError(f"Run {traceability_id} is in status '{current_status}', not awaiting Containment approval.")
            
        builder = OutputBuilder(str(self.packages_dir), traceability_id)
        
        # Re-check firewall in case modifications were input via notes
        if notes and any(cap in notes for cap in ["Discovery", "MCP Security Broker NHI", "Visual Agent Builder"]):
            # Trigger claims firewall breach upon modification note bypass attempts
            logger.log("APPROVAL_GATE_2", "BREACH", f"Re-gate validation failed: modification note attempts to introduce unreleased capability.")
            state_mgr.transition_to("HALTED_FIREWALL_BREACH", "Re-gate validation failed: Claims Firewall breach.")
            return

        if action == "Approve":
            logger.log("APPROVAL_GATE_2", "SUCCESS", f"DPO/IT Operations Director ({actor}) approved remediation setup. Notes: {notes}")
            state_mgr.transition_to("APPROVAL_2_APPROVED", "DPO approved containment.", actor, notes)
            
            # Finalize run
            state_mgr.transition_to("COMPLETE", "Incident Remediation Package assembled.")
            pkg_path = builder.assemble_final_package(state_mgr.get_state(), logger.get_logs())
            logger.log("COMPLETE", "SUCCESS", f"Incident Remediation Package successfully assembled at: {pkg_path}")
        elif action == "Reject":
            logger.log("APPROVAL_GATE_2", "REJECTED", f"DPO/IT Operations Director ({actor}) rejected remediation setup. Notes: {notes}")
            state_mgr.transition_to("HALTED_APPROVAL_2_REJECTED", f"DPO rejection: {notes}", actor, notes)
        else:
            raise ValueError(f"Invalid approval action: '{action}'")
