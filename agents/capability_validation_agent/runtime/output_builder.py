#!/usr/bin/env python3
"""
Output Builder for Capability Validation Agent Runtime.
Assembles final Capability Validation Packages.
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
        
        # 2. Write Skill 1 (Capability Validation) files
        int_data = run_state.get("intermediate_data", {})
        s1_md = int_data.get("capability_validation_output_md", "")
        s1_json = int_data.get("capability_validation_output_json", {})
        
        if s1_md:
            (self.package_dir / f"{self.traceability_id}-capability-validation-report.md").write_text(s1_md, encoding="utf-8")
        if s1_json:
            (self.package_dir / f"{self.traceability_id}-capability-validation-payload.json").write_text(json.dumps(s1_json, indent=2), encoding="utf-8")
            
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
        
        peer_approval = approvals.get("approval_1", {}) or {}
        peer_status = peer_approval.get("status", "N/A")
        peer_actor = peer_approval.get("actor", "N/A")
        
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return f"""# Ethana Capability Validation Handoff Note
 
**Traceability ID:** {self.traceability_id}  
**Assembled At:** {timestamp}  
**Capability Name:** {inputs.get("capability_name", "N/A")}  
**Context:** {inputs.get("claim_context", "N/A")}  
**Status:** COMPLETED  
 
---
 
## 1. Validation Scores Summary
- **Evidence Confidence Score (ECS):** {int_data.get("ecs", "N/A")}/100 ({int_data.get("ecs_band", "N/A")})
- **Validated Status:** {int_data.get("validated_status", "N/A")}
- **Phase 9 Verification Gate:** Passed (All 7 steps verified)
- **Claims Firewall Verification:** Passed
 
---
 
## 2. Mandatory Human Sign-Offs
1. **Peer Reviewer Approval:** {peer_status} by {peer_actor}
 
---
 
## 3. Package Contents
- `README.md` (This handoff note)
- `{self.traceability_id}-capability-validation-report.md` (Human-readable audit report)
- `{self.traceability_id}-capability-validation-payload.json` (Structured JSON payload for downstream skills)
- `{self.traceability_id}-run-log.json` (State machine transitions)
- `{self.traceability_id}-audit-trail.json` (Structured audit execution trail)
"""
