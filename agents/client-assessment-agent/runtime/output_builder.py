#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path


class OutputBuilder:
    def __init__(self, packages_dir: str, traceability_id: str):
        self.packages_dir = Path(packages_dir)
        self.traceability_id = traceability_id
        self.pkg_dir = self.packages_dir / traceability_id
        self.payloads_dir = self.pkg_dir / "payloads"

    def assemble_package(self, state: dict, audit_logs: list) -> str:
        self.pkg_dir.mkdir(parents=True, exist_ok=True)
        self.payloads_dir.mkdir(parents=True, exist_ok=True)

        tid = self.traceability_id
        data = state.get("intermediate_data", {})
        inputs = state.get("inputs", {})

        # 6 Markdown skill artifacts
        md_artifacts = [
            ("skill_1_md", f"{tid}-regulatory-scoping-matrix.md"),
            ("skill_2_md", f"{tid}-operational-control-spec.md"),
            ("skill_3_md", f"{tid}-solution-mapping-report.md"),
            ("skill_4_md", f"{tid}-iso42001-gap-assessment.md"),
            ("skill_5_md", f"{tid}-capability-validation-report.md"),
            ("skill_6_md", f"{tid}-proposal-review-certificate.md"),
        ]
        for key, filename in md_artifacts:
            content = data.get(key, f"# {filename}\n\nNo content available.\n")
            (self.pkg_dir / filename).write_text(content, encoding="utf-8")

        # 6 JSON payload artifacts
        json_artifacts = [
            ("skill_1_json", f"{tid}-regulatory-mapping-payload.json"),
            ("skill_2_json", f"{tid}-control-mapping-payload.json"),
            ("skill_3_json", f"{tid}-solution-mapping-payload.json"),
            ("skill_4_json", f"{tid}-iso42001-gap-assessment-payload.json"),
            ("skill_5_json", f"{tid}-capability-validation-payload.json"),
            ("skill_6_json", f"{tid}-proposal-review-payload.json"),
        ]
        for key, filename in json_artifacts:
            payload = data.get(key, {})
            (self.payloads_dir / filename).write_text(
                json.dumps(payload, indent=2), encoding="utf-8"
            )

        # Client scorecard (inline computation — no subprocess dependency)
        scorecard = self._build_scorecard(state)
        (self.pkg_dir / f"{tid}-client-scorecard.json").write_text(
            json.dumps(scorecard, indent=2), encoding="utf-8"
        )

        # Run log
        run_log = {
            "traceability_id": tid,
            "client_name": inputs.get("client_name", ""),
            "trigger_type": inputs.get("trigger_type", ""),
            "final_status": state.get("status", ""),
            "approvals": state.get("approvals", {}),
            "history": state.get("history", []),
            "audit_log_entries": len(audit_logs),
        }
        (self.pkg_dir / f"{tid}-run-log.json").write_text(
            json.dumps(run_log, indent=2), encoding="utf-8"
        )

        return str(self.pkg_dir)

    def _build_scorecard(self, state: dict) -> dict:
        tid = self.traceability_id
        inputs = state.get("inputs", {})
        data = state.get("intermediate_data", {})

        s1 = data.get("skill_1_json", {})
        s2 = data.get("skill_2_json", {})
        s3 = data.get("skill_3_json", {})
        s4 = data.get("skill_4_json", {})
        s5 = data.get("skill_5_json", {})
        s6 = data.get("skill_6_json", {})

        controls = s2.get("controls", [])
        orphan_controls = len(
            [c for c in controls if not c.get("platform_coverage")]
        ) if controls else s2.get("orphan_controls", 0)

        pcs = s6.get("pcs", 0)
        ctcs = s6.get("ctcs", 0)
        firewall_status = (
            "pass"
            if s6.get("cfb_count", 0) == 0 and not s6.get("hard_disqualifiers_triggered")
            else "fail"
        )

        readiness_band = self._compute_readiness_band(
            s4.get("ams", 0), pcs, s4.get("certification_classification", "")
        )

        return {
            "traceability_id": tid,
            "client_name": inputs.get("client_name", ""),
            "assessment_date": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "regulatory_assessment": {
                "score": s1.get("quality_score", 0),
                "jurisdictions": inputs.get("jurisdictions", []),
                "risk_tier": s1.get("risk_tier", ""),
            },
            "control_assessment": {
                "score": s2.get("quality_score", 0),
                "control_count": len(controls),
                "orphan_controls": orphan_controls,
            },
            "platform_coverage": {
                "ccs_average": s3.get("overall_ccs", s3.get("ccs_average", 0)),
                "production_coverage_percent": s3.get("production_coverage_percent", 0),
                "commercial_motion": s3.get("commercial_motion", ""),
            },
            "iso42001_assessment": {
                "ams": s4.get("ams", 0),
                "ars": s4.get("ars", 0),
                "certification_classification": s4.get("certification_classification", ""),
                "critical_gaps": s4.get("critical_gaps", s4.get("critical_gap_count", 0)),
                "major_gaps": s4.get("major_gaps", s4.get("major_gap_count", 0)),
            },
            "capability_validation": {
                "capabilities_validated": s5.get("capabilities_validated", 1 if s5 else 0),
                "all_production_confirmed": s5.get("all_production_confirmed", False),
                "escalations_required": 1 if s5.get("escalation_required", False) else 0,
            },
            "proposal_review": {
                "pcs": pcs,
                "ctcs": ctcs,
                "release_classification": s6.get("release_classification", ""),
                "claims_firewall_status": firewall_status,
            },
            "overall_readiness_band": readiness_band,
        }

    def _compute_readiness_band(
        self, ams: float, pcs: int, certification_classification: str
    ) -> str:
        if certification_classification == "Certification Ready" and pcs >= 90:
            return "Ready"
        if ams >= 70 and pcs >= 80:
            return "Near Ready"
        if ams >= 50 and pcs >= 70:
            return "Developing"
        return "Significant Gaps"
