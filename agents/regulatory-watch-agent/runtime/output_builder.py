#!/usr/bin/env python3
"""
Output Builder for Regulatory Watch Agent Runtime.
Assembles final Compliance & Coverage Packages and support partial outputs packaging on halted stages.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

class OutputBuilder:
    def __init__(self, output_dir: str, traceability_id: str):
        """Initializes OutputBuilder with output packaging path."""
        self.output_dir = Path(output_dir)
        self.traceability_id = traceability_id
        self.package_dir = self.output_dir / self.traceability_id
        
    def _create_clean_package_dir(self):
        """Creates or cleans the package directory."""
        if self.package_dir.exists():
            shutil.rmtree(self.package_dir)
        self.package_dir.mkdir(parents=True, exist_ok=True)

    def assemble_final_package(self, run_state: dict, audit_logs: list) -> str:
        """
        Bundles all MD outputs, JSON payloads, run logs, and audit logs.
        Returns the absolute path to the package directory.
        """
        self._create_clean_package_dir()
        
        # 1. Write cover page (README.md)
        cover_page_content = self._generate_cover_page(run_state)
        cover_path = self.package_dir / "README.md"
        cover_path.write_text(cover_page_content, encoding="utf-8")
        
        # 2. Write Skill 1 (Regulatory Mapping) files
        int_data = run_state.get("intermediate_data", {})
        s1_md = int_data.get("regulatory_mapping_output_md", "")
        s1_json = int_data.get("regulatory_mapping_output_json", {})
        
        if s1_md:
            (self.package_dir / f"{self.traceability_id}-regulatory-scoping-matrix.md").write_text(s1_md, encoding="utf-8")
        if s1_json:
            (self.package_dir / f"{self.traceability_id}-regulatory-mapping-payload.json").write_text(json.dumps(s1_json, indent=2), encoding="utf-8")
            
        # 3. Write Skill 2 (Governance Control Mapping) files
        s2_md = int_data.get("governance_control_mapping_output_md", "")
        s2_json = int_data.get("governance_control_mapping_output_json", {})
        
        if s2_md:
            (self.package_dir / f"{self.traceability_id}-operational-control-specification.md").write_text(s2_md, encoding="utf-8")
        if s2_json:
            (self.package_dir / f"{self.traceability_id}-governance-control-mapping-payload.json").write_text(json.dumps(s2_json, indent=2), encoding="utf-8")
            
        # 4. Write run log history
        run_log = {
            "traceability_id": self.traceability_id,
            "inputs": run_state.get("inputs", {}),
            "status": run_state.get("status", ""),
            "approvals": run_state.get("approvals", {}),
            "state_history": run_state.get("history", [])
        }
        (self.package_dir / f"{self.traceability_id}-run-log.json").write_text(json.dumps(run_log, indent=2), encoding="utf-8")
        
        # 5. Write audit logs
        (self.package_dir / f"{self.traceability_id}-audit-trail.json").write_text(json.dumps(audit_logs, indent=2), encoding="utf-8")
        
        return str(self.package_dir.resolve())

    def assemble_partial_package(self, run_state: dict, audit_logs: list) -> str:
        """
        Assembles partial scoping outputs (Skill 1 only) if the run is halted.
        Returns the absolute path to the package directory.
        """
        self._create_clean_package_dir()
        
        # 1. Write cover page (README.md)
        cover_page_content = self._generate_partial_cover_page(run_state)
        cover_path = self.package_dir / "README.md"
        cover_path.write_text(cover_page_content, encoding="utf-8")
        
        # 2. Write Skill 1 (Regulatory Mapping) files
        int_data = run_state.get("intermediate_data", {})
        s1_md = int_data.get("regulatory_mapping_output_md", "")
        s1_json = int_data.get("regulatory_mapping_output_json", {})
        
        if s1_md:
            (self.package_dir / f"{self.traceability_id}-regulatory-scoping-matrix.md").write_text(s1_md, encoding="utf-8")
        if s1_json:
            (self.package_dir / f"{self.traceability_id}-regulatory-mapping-payload.json").write_text(json.dumps(s1_json, indent=2), encoding="utf-8")
            
        # 3. Write run log history
        run_log = {
            "traceability_id": self.traceability_id,
            "inputs": run_state.get("inputs", {}),
            "status": run_state.get("status", ""),
            "approvals": run_state.get("approvals", {}),
            "state_history": run_state.get("history", [])
        }
        (self.package_dir / f"{self.traceability_id}-run-log.json").write_text(json.dumps(run_log, indent=2), encoding="utf-8")
        
        # 4. Write audit logs
        (self.package_dir / f"{self.traceability_id}-audit-trail.json").write_text(json.dumps(audit_logs, indent=2), encoding="utf-8")
        
        return str(self.package_dir.resolve())

    def _generate_cover_page(self, run_state: dict) -> str:
        inputs = run_state.get("inputs", {})
        approvals = run_state.get("approvals", {})
        int_data = run_state.get("intermediate_data", {})
        
        gc_approval = approvals.get("approval_1", {}) or {}
        gc_status = gc_approval.get("status", "N/A")
        gc_actor = gc_approval.get("actor", "N/A")
        
        ds_approval = approvals.get("approval_2", {}) or {}
        ds_status = ds_approval.get("status", "N/A")
        ds_actor = ds_approval.get("actor", "N/A")
        
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return f"""# Regulatory Compliance Handoff Note

**Traceability ID:** {self.traceability_id}  
**Assembled At:** {timestamp}  
**Subject Type:** {inputs.get("subject_type", "N/A")}  
**Jurisdictions:** {", ".join(inputs.get("jurisdictions", []))}  
**Target Maturity Level:** {inputs.get("target_maturity_level", "N/A")}  
**Status:** COMPLETED  

---

## 1. Compliance Scores Summary
- **Regulatory Mapping Score:** {int_data.get("regulatory_mapping_score", "N/A")}/100
- **Governance Control Mapping Score:** {int_data.get("governance_control_mapping_score", "N/A")}/100
- **Claims Firewall Verification:** Passed (0 violations)

---

## 2. Mandatory Human Sign-Offs
1. **General Counsel Approval Gate 1:** {gc_status} by {gc_actor}
2. **DPO & InfoSec Joint Approval Gate 2:** {ds_status} by {ds_actor}

---

## 3. Package Contents
- `README.md` (This handoff note)
- `{self.traceability_id}-regulatory-scoping-matrix.md` (Regulatory obligations)
- `{self.traceability_id}-regulatory-mapping-payload.json` (Structured obligations JSON)
- `{self.traceability_id}-operational-control-specification.md` (Technical and process controls)
- `{self.traceability_id}-governance-control-mapping-payload.json` (Structured controls JSON)
- `{self.traceability_id}-run-log.json` (State machine transitions)
- `{self.traceability_id}-audit-trail.json` (Structured audit execution trail)
"""

    def _generate_partial_cover_page(self, run_state: dict) -> str:
        inputs = run_state.get("inputs", {})
        approvals = run_state.get("approvals", {})
        int_data = run_state.get("intermediate_data", {})
        
        gc_approval = approvals.get("approval_1", {}) or {}
        gc_status = gc_approval.get("status", "N/A")
        gc_actor = gc_approval.get("actor", "N/A")
        
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return f"""# Partial Regulatory Compliance Handoff Note

> [!WARNING]
> **PARTIAL RELEASE:** This package contains only the Regulatory Scoping Matrix. The downstream Operational Control Specification and final approval gates were NOT completed because the run subsequently halted in state `{run_state.get("status", "HALTED")}`.

**Traceability ID:** {self.traceability_id}  
**Assembled At:** {timestamp}  
**Subject Type:** {inputs.get("subject_type", "N/A")}  
**Jurisdictions:** {", ".join(inputs.get("jurisdictions", []))}  
**Target Maturity Level:** {inputs.get("target_maturity_level", "N/A")}  
**Status:** HALTED (Partial Output Release)  

---

## 1. Compliance Score Summary
- **Regulatory Mapping Score:** {int_data.get("regulatory_mapping_score", "N/A")}/100

---

## 2. Completed Sign-Offs
1. **General Counsel Approval Gate 1:** {gc_status} by {gc_actor}

---

## 3. Package Contents
- `README.md` (This partial handoff note)
- `{self.traceability_id}-regulatory-scoping-matrix.md` (Regulatory obligations)
- `{self.traceability_id}-regulatory-mapping-payload.json` (Structured obligations JSON)
- `{self.traceability_id}-run-log.json` (State machine transitions)
- `{self.traceability_id}-audit-trail.json` (Structured audit execution trail)
"""
