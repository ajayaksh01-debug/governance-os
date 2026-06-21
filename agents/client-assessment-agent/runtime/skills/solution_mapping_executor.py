#!/usr/bin/env python3
"""
Net-new deterministic executor for Skill 3 — ethana-solution-mapping.

Maps each governance control (from Skill 2's control_mapping_output) to an Ethana
platform capability, scores requirement-specific Coverage Confidence (CCS),
decides a proposal disposition, and produces the aggregate coverage profile plus
a commercial-motion recommendation.

Deterministic (L4): no LLM at runtime. Signals come from:
  - Skill 2 controls' coverage_classification (Fully/Partially Covered by Ethana
    / Covered by Cursory Service)
  - the canonical product model (capability Production / In Build / Roadmap /
    Aspirational status) — enforces the In-Build/Aspirational -> CCS 0 rule.

Returns the solution_mapping_output schema fields plus the CA envelope siblings
(quality_score, overall_ccs, production_coverage_percent, commercial_motion,
markdown_output).
"""

import sys
from pathlib import Path

# agents/client-assessment-agent/runtime/skills/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[4]

# CCS band anchors (workflow.md Phase 4 / SKILL.md calibration)
_BAND_FULL = 95      # Full 90-100
_BAND_PARTIAL = 60   # Partial 50-69
_BAND_NONE = 15      # None 0-24

# capability_status enum (solution_mapping_output schema)
_STATUS_DISPLAY = {
    "production": "Production",
    "in build": "In Build",
    "roadmap": "Roadmap",
    "aspirational": "Aspirational",
}

# Hard-status overrides for the Ethana product families that the Claims Firewall
# enforces via dedicated hard rules rather than the Section 1-5 capability tables
# (so parse_canonical_model does not return them as base-name entries). Consulted
# BEFORE the parsed CPM dict. Defaulting any of these to Production would leak a
# firewall violation into the generated markdown.
_HARD_STATUS = {
    "ethana workspace": ("Ethana Workspace", "aspirational"),
    "visual agent builder": ("Visual Agent Builder", "aspirational"),
    "ethana edge": ("Ethana Edge", "in build"),
    "ethana sentry": ("Ethana Sentry", "in build"),
}


class SolutionMappingExecutor:
    def __init__(self, runs_dir, logs_dir):
        self.runs_dir = runs_dir
        self.logs_dir = logs_dir
        self.cpm_path = REPO_ROOT / "knowledge" / "ethana" / "canonical-product-model.md"
        self._cpm = None

    # ------------------------------------------------------------------
    # Canonical product model
    # ------------------------------------------------------------------

    def _load_cpm(self) -> dict:
        if self._cpm is not None:
            return self._cpm
        scripts = REPO_ROOT / "evaluations" / "scripts"
        if str(scripts) not in sys.path:
            sys.path.insert(0, str(scripts))
        try:
            from claims_linter import parse_canonical_model  # noqa: PLC0415
            self._cpm = parse_canonical_model(Path(self.cpm_path))
        except Exception:
            self._cpm = {}
        return self._cpm

    def _match_capability(self, control_name: str):
        """Return (display_name, status_norm) for the Ethana capability that best
        matches a control name, or (None, None) if no canonical match.

        Hard-status product families are checked first — they are firewall-enforced
        and must never default to Production.
        """
        name_l = (control_name or "").lower()
        for term, (display, status) in _HARD_STATUS.items():
            if term in name_l:
                return display, status
        cpm = self._load_cpm()
        for key, entry in cpm.items():
            # substring match in either direction (key is the canonical base name)
            if key and (key in name_l or name_l in key):
                return entry.get("original_name", key), entry.get("status", "")
        return None, None

    # ------------------------------------------------------------------
    # Per-requirement scoring
    # ------------------------------------------------------------------

    def _score_requirement(self, control: dict) -> dict:
        requirement = control.get("name") or control.get("id") or "Unnamed requirement"
        classification = control.get("coverage_classification", "")
        cap_display, status_norm = self._match_capability(requirement)

        if "Fully Covered by Ethana" in classification:
            base_ccs = _BAND_FULL
        elif "Partially Covered by Ethana" in classification:
            base_ccs = _BAND_PARTIAL
        else:  # Covered by Cursory Service / unknown
            base_ccs = _BAND_NONE

        # Determine capability_status (schema enum) and apply the hard rule:
        # In Build / Roadmap / Aspirational current CCS is always 0.
        if "Ethana" in classification and status_norm in _STATUS_DISPLAY:
            capability_status = _STATUS_DISPLAY[status_norm]
        elif "Ethana" in classification:
            # Covered by Ethana but no canonical match — treat as Production platform.
            capability_status = "Production"
        else:
            capability_status = "Not addressed"

        if capability_status in ("In Build", "Roadmap", "Aspirational"):
            ccs_score = 0
        elif capability_status == "Not addressed":
            ccs_score = min(base_ccs, _BAND_NONE)
        else:
            ccs_score = base_ccs

        matched_capability = cap_display or (
            "Ethana Platform" if "Ethana" in classification
            else "Cursory advisory service"
        )

        # Disposition (schema enum)
        if capability_status == "Production" and ccs_score >= 50:
            disposition = "Include in proposal"
        elif capability_status in ("In Build", "Roadmap"):
            disposition = "Roadmap mention only"
        elif capability_status == "Aspirational":
            disposition = "Gap register"
        else:
            disposition = "Bridge to Cursory"

        return {
            "requirement": requirement,
            "matched_capability": matched_capability,
            "capability_status": capability_status,
            "ccs_score": int(ccs_score),
            "disposition": disposition,
        }

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------

    @staticmethod
    def _band_of(ccs: int) -> str:
        if ccs >= 90:
            return "Full"
        if ccs >= 70:
            return "High"
        if ccs >= 50:
            return "Partial"
        if ccs >= 25:
            return "Thin"
        return "None"

    def _commercial_motion(self, production_coverage_percent: int,
                           has_cert_blocker: bool, has_in_build: bool) -> str:
        if has_cert_blocker or production_coverage_percent < 30:
            return "Advisory-First"
        if production_coverage_percent >= 70:
            return "Platform-First"
        if has_in_build:
            return "Land-and-Expand"
        return "Design Partner"

    @staticmethod
    def _has_cert_blocker(inputs: dict) -> bool:
        existing = (inputs.get("existing_policies") or "").lower()
        target = (inputs.get("target_certification") or "")
        has_posture = ("soc 2" in existing or "soc2" in existing
                       or "iso 27001" in existing or "iso27001" in existing)
        return target == "Third-party certification" and not has_posture

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def execute_solution_mapping(self, inputs: dict, logger=None) -> dict:
        if logger is not None:
            logger.log("SKILL_3_EXECUTION", "SUCCESS", "Solution mapping started.")

        cmo = inputs.get("control_mapping_output") or {}
        controls = cmo.get("controls", [])
        if not controls:
            raise ValueError("Skill 3 requires a non-empty control set from Skill 2.")

        matched = [self._score_requirement(c) for c in controls]

        total = len(matched)
        ccs_values = [m["ccs_score"] for m in matched]
        overall_ccs = round(sum(ccs_values) / total, 1) if total else 0.0

        production_covered = sum(
            1 for m in matched
            if m["capability_status"] == "Production" and m["ccs_score"] >= 50
        )
        production_coverage_percent = round(100 * production_covered / total) if total else 0

        ccs_distribution = {"Full": 0, "High": 0, "Partial": 0, "Thin": 0, "None": 0}
        for m in matched:
            ccs_distribution[self._band_of(m["ccs_score"])] += 1

        coverage_characterization = (
            "Platform-Primary" if production_coverage_percent >= 50 else "Cursory-Primary"
        )
        has_in_build = any(m["capability_status"] in ("In Build", "Roadmap") for m in matched)
        has_cert_blocker = self._has_cert_blocker(inputs)
        commercial_motion = self._commercial_motion(
            production_coverage_percent, has_cert_blocker, has_in_build
        )
        advisory_first = commercial_motion == "Advisory-First"

        # Assessment-quality gate score (decoupled from coverage CCS).
        quality_score = 90
        if not inputs.get("regulatory_mapping_output"):
            quality_score -= 10
        if total < 3:
            quality_score -= 15
        quality_score = max(quality_score, 60)

        overall_coverage_summary = {
            "coverage_characterization": coverage_characterization,
            "advisory_first_recommended": advisory_first,
            "ccs_distribution": ccs_distribution,
        }

        markdown_output = self._compile_markdown(
            matched, overall_ccs, production_coverage_percent,
            coverage_characterization, commercial_motion,
        )

        result = {
            "matched_capabilities": matched,
            "overall_coverage_summary": overall_coverage_summary,
            # CA envelope siblings
            "quality_score": int(quality_score),
            "overall_ccs": overall_ccs,
            "production_coverage_percent": int(production_coverage_percent),
            "commercial_motion": commercial_motion,
            "markdown_output": markdown_output,
        }
        if logger is not None:
            logger.log("SKILL_3_EXECUTION", "SUCCESS",
                       f"Solution mapping complete. Overall CCS {overall_ccs}.")
        return result

    # ------------------------------------------------------------------
    # Markdown (firewall-clean: Production-only in proposal sections,
    # non-production items explicitly status-disclosed in roadmap/prohibited)
    # ------------------------------------------------------------------

    def _compile_markdown(self, matched, overall_ccs, pcp,
                          characterization, motion) -> str:
        production = [m for m in matched if m["capability_status"] == "Production"]
        roadmap = [m for m in matched if m["capability_status"] in ("In Build", "Roadmap")]
        prohibited = [m for m in matched if m["capability_status"] == "Aspirational"]
        bridges = [m for m in matched if m["capability_status"] == "Not addressed"]

        lines = []
        lines.append("# Ethana Solution Mapping Report\n")
        lines.append("## 1. Requirement Coverage Matrix\n")
        lines.append("| Requirement | Matched Capability | Status | CCS | Disposition |")
        lines.append("|---|---|---|---|---|")
        for m in matched:
            lines.append(
                f"| {m['requirement']} | {m['matched_capability']} | "
                f"{m['capability_status']} | {m['ccs_score']} | {m['disposition']} |"
            )
        lines.append("")
        lines.append("## 2. Overall Coverage Summary\n")
        lines.append(f"- Aggregate CCS: **{overall_ccs}/100**")
        lines.append(f"- Production coverage: **{pcp}%**")
        lines.append(f"- Coverage characterisation: **{characterization}**")
        lines.append(f"- Recommended commercial motion: **{motion}**\n")

        lines.append("## 3. Proposal-Safe Platform Capabilities\n")
        if production:
            for m in production:
                lines.append(
                    f"- **{m['matched_capability']}** (Production) addresses "
                    f"*{m['requirement']}* — CCS {m['ccs_score']}/100."
                )
        else:
            lines.append("- No Production capability qualifies for proposal claims.")
        lines.append("")

        lines.append("## 4. Roadmap Disclosure (mention only — not proposal deliverables)\n")
        if roadmap:
            for m in roadmap:
                lines.append(
                    f"- {m['matched_capability']} — **In Build** (not yet in production); "
                    f"relevant to *{m['requirement']}*. Anticipated CCS when shipped."
                )
        else:
            lines.append("- None.")
        lines.append("")

        lines.append("## 5. Prohibited Claims Register\n")
        if prohibited:
            for m in prohibited:
                lines.append(
                    f"- {m['matched_capability']} — **Aspirational** (no engineering basis); "
                    f"must not appear in any proposal context for *{m['requirement']}*."
                )
        else:
            lines.append("- None.")
        lines.append("")

        lines.append("## 6. Cursory Bridge Recommendations\n")
        if bridges:
            for m in bridges:
                lines.append(
                    f"- *{m['requirement']}* — bridge via Cursory advisory service "
                    f"(no Production platform capability today)."
                )
        else:
            lines.append("- None.")
        lines.append("")
        return "\n".join(lines)
