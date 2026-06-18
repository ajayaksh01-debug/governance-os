#!/usr/bin/env python3
"""
Output Builder for Ethana Proposal Agent Runtime.
Assembles, signs, and writes final proposal handoff packages.
"""

import os
import json
from pathlib import Path

class OutputBuilder:
    def __init__(self, packages_dir: str, traceability_id: str):
        """Initializes the output builder for the run."""
        self.packages_dir = Path(packages_dir)
        self.traceability_id = traceability_id
        self.pkg_dir = self.packages_dir / self.traceability_id

    def assemble_final_package(self, final_state: dict, session_logs: list) -> str:
        """
        Builds the handoff package containing:
        - README.md
        - {traceability_id}-proposal-review-report.md
        - {traceability_id}-proposal-review-payload.json
        - {traceability_id}-audit-log.jsonl
        """
        self.pkg_dir.mkdir(parents=True, exist_ok=True)
        int_data = final_state.get("intermediate_data", {})
        
        # 1. Write README.md
        readme_content = f"""# Proposal Review Handoff Package: {self.traceability_id}

This directory contains the final release deliverables for Proposal Review run **{self.traceability_id}**.

## Deliverables
1. **Proposal Review Report:** [{self.traceability_id}-proposal-review-report.md](./{self.traceability_id}-proposal-review-report.md)
2. **Release Audit Certificate (JSON payload):** [{self.traceability_id}-proposal-review-payload.json](./{self.traceability_id}-proposal-review-payload.json)
3. **Structured Audit Trail:** [{self.traceability_id}-audit-log.jsonl](./{self.traceability_id}-audit-log.jsonl)
"""
        (self.pkg_dir / "README.md").write_text(readme_content, encoding="utf-8")
        
        # 2. Write Report md
        report_md = int_data.get("proposal_review_md", "# Proposal Review Report")
        (self.pkg_dir / f"{self.traceability_id}-proposal-review-report.md").write_text(report_md, encoding="utf-8")
        
        # 3. Write Output payload JSON
        payload_json = int_data.get("proposal_review_json", {})
        (self.pkg_dir / f"{self.traceability_id}-proposal-review-payload.json").write_text(
            json.dumps(payload_json, indent=2), encoding="utf-8"
        )
        
        # 4. Write Audit Log jsonl
        audit_file = self.pkg_dir / f"{self.traceability_id}-audit-log.jsonl"
        try:
            with open(audit_file, "w", encoding="utf-8") as f:
                for entry in session_logs:
                    f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Error writing package audit log: {e}")
            
        return str(self.pkg_dir)
