#!/usr/bin/env python3
import json
from pathlib import Path


class OutputBuilder:
    def __init__(self, packages_dir: str, traceability_id: str):
        self.packages_dir = Path(packages_dir)
        self.traceability_id = traceability_id
        self.pkg_dir = self.packages_dir / self.traceability_id

    def assemble_final_package(self, final_state: dict, session_logs: list) -> str:
        self.pkg_dir.mkdir(parents=True, exist_ok=True)
        int_data = final_state.get("intermediate_data", {})

        review_json = int_data.get("governance_review_json", {})
        classification = review_json.get("classification", "Unknown")

        readme = (
            f"# Governance Readiness Certificate Package: {self.traceability_id}\n\n"
            f"**Classification:** {classification}\n\n"
            f"This directory contains the final deliverables for Governance Review run "
            f"**{self.traceability_id}**.\n\n"
            f"## Deliverables\n"
            f"1. **Governance Review Report:** "
            f"[{self.traceability_id}-governance-review-report.md]"
            f"(./{self.traceability_id}-governance-review-report.md)\n"
            f"2. **Governance Readiness Certificate (JSON payload):** "
            f"[{self.traceability_id}-governance-readiness-certificate.json]"
            f"(./{self.traceability_id}-governance-readiness-certificate.json)\n"
            f"3. **Structured Audit Trail:** "
            f"[{self.traceability_id}-audit-log.jsonl]"
            f"(./{self.traceability_id}-audit-log.jsonl)\n"
        )
        (self.pkg_dir / "README.md").write_text(readme, encoding="utf-8")

        report_md = int_data.get("governance_review_md", "# Governance Review Report")
        (self.pkg_dir / f"{self.traceability_id}-governance-review-report.md").write_text(
            report_md, encoding="utf-8"
        )

        (self.pkg_dir / f"{self.traceability_id}-governance-readiness-certificate.json").write_text(
            json.dumps(review_json, indent=2), encoding="utf-8"
        )

        audit_file = self.pkg_dir / f"{self.traceability_id}-audit-log.jsonl"
        try:
            with open(audit_file, "w", encoding="utf-8") as f:
                for entry in session_logs:
                    f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Error writing package audit log: {e}")

        return str(self.pkg_dir)
