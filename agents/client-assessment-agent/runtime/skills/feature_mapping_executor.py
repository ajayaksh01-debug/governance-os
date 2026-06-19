#!/usr/bin/env python3
"""
Net-new deterministic executor for Skill FM — ethana-feature-mapping.

Maps each Ethana capability (from Skill 3 Solution Mapping output) to a
Technical Fit Score (TFS), determines POC readiness, and produces the ten-
section Feature Mapping report.

Deterministic (L4): no LLM at runtime.  TFS is derived from SM's CCS band
values as a proxy measure (PR-006 scope).  True customer-specific TFS —
incorporating deployment_constraint, volume_parameters, and existing_stack —
is deferred to the standalone Feature Mapping Agent.

PR-006 proxy model (CCS band → TFS anchor):
  CCS ≥ 90  (Full)    → TFS 92
  CCS ≥ 70  (High)    → TFS 80
  CCS ≥ 50  (Partial) → TFS 58
  CCS ≥ 25  (Thin)    → TFS 35
  CCS < 25  (None)    → TFS  0
  In Build / Roadmap / Aspirational → TFS 0 regardless of CCS

Two aggregate fields are produced:
  overall_tfs_score    — arithmetic mean of ALL tfs_score values (SKILL.md §2)
  production_tfs_score — arithmetic mean of Ready-row tfs_scores (Gate FM-c)

CPM failure raises ValueError (no silent fallback) so the orchestrator
catches it and transitions to HALTED_ESCALATION.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

_TFS_BANDS = [
    (90, 92),
    (70, 80),
    (50, 58),
    (25, 35),
    (0,   0),
]

_POC_READINESS = {
    "Production":    "Ready",
    "In Build":      "Roadmap-Blocked",
    "Roadmap":       "Roadmap-Blocked",
    "Aspirational":  "Incompatible",
    "Not addressed": "Incompatible",
}


class FeatureMappingExecutor:
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
        except Exception as e:
            raise ValueError(
                f"Feature Mapping executor requires canonical-product-model.md; "
                f"file not found or unreadable at {self.cpm_path}: {e}"
            ) from e
        return self._cpm

    def _canonical_name(self, matched_capability: str) -> str:
        cpm = self._load_cpm()
        name_l = matched_capability.lower()
        for key, entry in cpm.items():
            if key and (key in name_l or name_l in key):
                return entry.get("original_name", matched_capability)
        return matched_capability

    # ------------------------------------------------------------------
    # Per-row computation
    # ------------------------------------------------------------------

    @staticmethod
    def _tfs_from_ccs(ccs_score: int) -> int:
        for threshold, tfs in _TFS_BANDS:
            if ccs_score >= threshold:
                return tfs
        return 0

    @staticmethod
    def _poc_readiness(capability_status: str) -> str:
        return _POC_READINESS.get(capability_status, "Incompatible")

    def _integration_path(self, capability_status: str, deployment_constraint: str) -> str:
        if capability_status != "Production":
            return "Not applicable"
        dc = (deployment_constraint or "").lower()
        if "on-prem" in dc or "on_prem" in dc or "on premise" in dc:
            return "On-Premise Connector"
        if "hybrid" in dc:
            return "Hybrid Bridge"
        return "Native API"

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def execute_feature_mapping(self, inputs: dict, logger=None) -> dict:
        if logger is not None:
            logger.log("SKILL_FM_EXECUTION", "SUCCESS", "Feature Mapping started.")

        matched_capabilities = inputs.get("matched_capabilities", [])
        if not matched_capabilities:
            raise ValueError(
                "Feature Mapping requires a non-empty matched_capabilities list "
                "from Solution Mapping output."
            )

        self._load_cpm()

        deployment_constraint = inputs.get("deployment_constraint", "")
        customer_sector = inputs.get("customer_sector", "")
        poc_duration = inputs.get("poc_duration", "")

        feature_validation_table = []
        for row in matched_capabilities:
            cap_status = row.get("capability_status", "Not addressed")
            ccs_score = int(row.get("ccs_score", 0))
            matched_cap = row.get("matched_capability", "")

            if cap_status == "Production":
                tfs_score = self._tfs_from_ccs(ccs_score)
            else:
                tfs_score = 0

            poc_readiness = self._poc_readiness(cap_status)
            integration_path = self._integration_path(cap_status, deployment_constraint)
            canonical_cap = self._canonical_name(matched_cap)

            feature_validation_table.append({
                "proposed_feature": matched_cap,
                "canonical_capability": canonical_cap,
                "integration_path": integration_path,
                "tfs_score": tfs_score,
                "poc_readiness": poc_readiness,
            })

        all_tfs = [r["tfs_score"] for r in feature_validation_table]
        overall_tfs_score = round(sum(all_tfs) / len(all_tfs)) if all_tfs else 0

        ready_tfs = [r["tfs_score"] for r in feature_validation_table
                     if r["poc_readiness"] == "Ready"]
        production_tfs_score = round(sum(ready_tfs) / len(ready_tfs)) if ready_tfs else 0

        quality_score = 90
        if not deployment_constraint:
            quality_score -= 10
        if not poc_duration:
            quality_score -= 10
        quality_score = max(quality_score, 70)

        markdown_output = self._compile_markdown(
            feature_validation_table, overall_tfs_score, production_tfs_score,
            deployment_constraint, customer_sector, poc_duration,
        )

        result = {
            "feature_validation_table": feature_validation_table,
            "overall_tfs_score": int(overall_tfs_score),
            "production_tfs_score": int(production_tfs_score),
            "quality_score": int(quality_score),
            "markdown_output": markdown_output,
        }

        if logger is not None:
            logger.log(
                "SKILL_FM_EXECUTION", "SUCCESS",
                f"Feature Mapping complete. "
                f"Overall TFS {overall_tfs_score}, Production TFS {production_tfs_score}.",
            )
        return result

    # ------------------------------------------------------------------
    # Markdown (firewall-clean: Aspirational/In-Build never in proposal
    # sections 5, 9; disclosed in sections 6 and 7 only)
    # ------------------------------------------------------------------

    def _compile_markdown(
        self, fvt, overall_tfs, production_tfs,
        deployment_constraint, customer_sector, poc_duration,
    ) -> str:
        production = [r for r in fvt if r["poc_readiness"] == "Ready"]
        roadmap    = [r for r in fvt if r["poc_readiness"] == "Roadmap-Blocked"]
        prohibited = [r for r in fvt if r["poc_readiness"] == "Incompatible"]

        lines = []
        lines.append("# Feature Mapping\n")

        lines.append("## 1. Feature Validation Table\n")
        lines.append("| Feature | Status | TFS | Integration Path |")
        lines.append("|---|---|---|---|")
        for r in fvt:
            lines.append(
                f"| {r['proposed_feature']} | {r['poc_readiness']} | "
                f"{r['tfs_score']} | {r['integration_path']} |"
            )
        lines.append("")

        lines.append("## 2. Technical Fit Summary\n")
        lines.append(f"- Overall TFS (all features): **{overall_tfs}/100**")
        lines.append(f"- Production TFS (Ready features only): **{production_tfs}/100**")
        lines.append(f"- Production-Ready: {len(production)}")
        lines.append(f"- Roadmap-Blocked: {len(roadmap)}")
        lines.append(f"- Incompatible: {len(prohibited)}\n")

        lines.append("## 3. Integration Compatibility Assessment\n")
        if deployment_constraint:
            lines.append(f"- Deployment constraint: {deployment_constraint}")
        if customer_sector:
            lines.append(f"- Customer sector: {customer_sector}")
        if production:
            for r in production:
                lines.append(
                    f"- **{r['proposed_feature']}**: {r['integration_path']} "
                    f"(TFS {r['tfs_score']}/100)."
                )
        else:
            lines.append("- No Production-Ready capabilities assessed.")
        lines.append("")

        lines.append("## 4. Technical Constraints and Caveats\n")
        if deployment_constraint:
            lines.append(
                f"- Deployment constraint ({deployment_constraint}) affects "
                "integration path selection. Verify connectivity and latency SLAs before POC."
            )
        if poc_duration:
            lines.append(
                f"- POC duration: {poc_duration}. "
                "Scope is limited to Production-Ready integrations listed in Section 5."
            )
        if not deployment_constraint and not poc_duration:
            lines.append("- No deployment constraints or POC duration provided.")
        lines.append("")

        lines.append("## 5. POC Feature Set\n")
        if production:
            for r in production:
                lines.append(
                    f"- **{r['proposed_feature']}** — "
                    f"{r['integration_path']}, TFS {r['tfs_score']}/100."
                )
        else:
            lines.append(
                "- No capabilities qualify for POC scope at the Production-Ready threshold."
            )
        lines.append("")

        lines.append("## 6. Prohibited Feature Claims Register\n")
        if prohibited:
            for r in prohibited:
                lines.append(
                    f"- {r['proposed_feature']} — **Incompatible** "
                    "(Aspirational or no engineering basis); "
                    "must not appear in any technical proposal claim."
                )
        else:
            lines.append("- None.")
        lines.append("")

        lines.append("## 7. Substitution Analysis\n")
        if roadmap:
            for r in roadmap:
                lines.append(
                    f"- {r['proposed_feature']} — **Roadmap-Blocked** (In Build or Roadmap); "
                    "propose Cursory advisory bridge or defer to roadmap milestone."
                )
        else:
            lines.append(
                "- No substitution required; all assessed capabilities are "
                "Production-Ready or excluded."
            )
        lines.append("")

        lines.append("## 8. Evidence References\n")
        lines.append("| Claim | Source | Section |")
        lines.append("|---|---|---|")
        if production:
            for r in production:
                lines.append(
                    f"| {r['proposed_feature']} is Production-Ready "
                    f"| Ethana Canonical Product Model | Status: Production |"
                )
        else:
            lines.append("| No Production-Ready claims | — | — |")
        lines.append("")

        lines.append("## 9. Technical Proposal Language\n")
        if production:
            for r in production:
                lines.append(
                    f"- {r['proposed_feature']} ({r['integration_path']}) "
                    f"carries a Technical Fit Score of {r['tfs_score']}/100 "
                    "against the assessed governance requirements and is "
                    "suitable for inclusion in a technical proposal."
                )
        else:
            lines.append(
                "- No Production-Ready capabilities are available for "
                "technical proposal inclusion based on the assessed capability set."
            )
        lines.append("")

        lines.append("## 10. Technical Summary\n")
        lines.append(
            f"Overall TFS: {overall_tfs}/100 (all features). "
            f"Production TFS: {production_tfs}/100 (Ready features only). "
            f"POC-Ready: {len(production)}. "
            f"Roadmap-Blocked: {len(roadmap)}. "
            f"Incompatible: {len(prohibited)}.\n"
        )

        return "\n".join(lines)
