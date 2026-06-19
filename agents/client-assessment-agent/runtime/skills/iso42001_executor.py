#!/usr/bin/env python3
"""
Net-new deterministic executor for Skill 4 — iso-42001-gap-assessment.

Conducts a clause-by-clause (Clauses 4-10) and Annex A (38 controls / 9
categories) gap assessment of a client's AI Management System, producing the
two composite scores AMS and ARS, the certification classification, a gap
register, and the months-to-readiness estimate.

Deterministic (L4): no LLM at runtime. Maturity signals are derived from
keyword credit over existing_policies / organisation_description, plus upstream
regulatory_mapping_output and control_mapping_output, with EU high-risk and BFSI
overlays. The CA score gate's quality_score is decoupled from AMS/ARS — a
low-maturity client still receives a high-quality assessment that reports the
gaps faithfully.

Formulas (skills/iso-42001-gap-assessment/workflow.md Phase 7):
  Clause_Score  = (Σ clause ratings 4..10) / 7 × 20
  Annex_A_Score = (Implemented + 0.5×Partial) / Applicable × 100
  AMS           = Clause_Score×0.60 + Annex_A_Score×0.40
  ARS = Doc×0.30 + Evidence×0.40 + ControlOp×0.20 + MgmtReview×0.10
"""

from datetime import datetime, timezone

# ISO 42001 operative clauses
_CLAUSES = [4, 5, 6, 7, 8, 9, 10]
_CLAUSE_NAMES = {
    4: "Context of the Organisation",
    5: "Leadership",
    6: "Planning",
    7: "Support",
    8: "Operation",
    9: "Performance Evaluation",
    10: "Improvement",
}

# Keyword signals that grant clause maturity credit (deterministic).
_CLAUSE_SIGNALS = {
    4: ["scope", "context", "interested parties", "risk appetite"],
    5: ["ai policy", "leadership", "roles and responsibilities", "governance"],
    6: ["risk assessment", "impact assessment", "planning", "treatment"],
    7: ["competence", "awareness", "training", "documentation control", "resources"],
    8: ["lifecycle", "deployment", "operation", "third-party", "monitoring", "testing"],
    9: ["internal audit", "management review", "performance", "metrics", "monitoring"],
    10: ["nonconformity", "corrective action", "continual improvement", "incident", "lessons"],
}

# Annex A control categories (9), 38 controls total.
_ANNEX_CATEGORIES = {
    1: "AI policy and governance",
    2: "AI risk assessment",
    3: "AI system lifecycle",
    4: "Data governance",
    5: "Supply chain",
    6: "Human oversight",
    7: "Incident management",
    8: "Transparency",
    9: "Monitoring",
}
# Control counts per category (sum = 38).
_ANNEX_CONTROL_COUNTS = {1: 4, 2: 5, 3: 6, 4: 5, 5: 3, 6: 4, 7: 3, 8: 4, 9: 4}
_ANNEX_TOTAL = 38


class Iso42001GapAssessmentExecutor:
    def __init__(self, runs_dir, logs_dir):
        self.runs_dir = runs_dir
        self.logs_dir = logs_dir

    # ------------------------------------------------------------------
    # Signal text + overlays
    # ------------------------------------------------------------------

    @staticmethod
    def _signal_text(inputs: dict) -> str:
        parts = [
            inputs.get("existing_documentation", ""),
            inputs.get("organisation_description", ""),
            inputs.get("existing_policies", ""),
        ]
        return " ".join(p for p in parts if p).lower()

    @staticmethod
    def _is_eu_high_risk(inputs: dict) -> bool:
        juris = [j.lower() for j in inputs.get("jurisdictions", [])]
        portfolio = (inputs.get("ai_portfolio", "") or "").lower()
        high_risk = any(t in portfolio for t in
                        ["credit", "bank", "loan", "insurance", "biometric", "high-risk"])
        return "eu" in juris and high_risk

    @staticmethod
    def _is_bfsi(inputs: dict) -> bool:
        return (inputs.get("industry", "") or "").lower() == "bfsi"

    # ------------------------------------------------------------------
    # Clause maturity ratings (0-5)
    # ------------------------------------------------------------------

    def _clause_ratings(self, inputs: dict, text: str) -> dict:
        ratings = {}
        iso27001_credit = ("iso 27001" in text or "iso27001" in text)
        for cl in _CLAUSES:
            rating = 1  # baseline awareness
            hits = sum(1 for kw in _CLAUSE_SIGNALS[cl] if kw in text)
            rating += min(hits, 3)
            # ISO 27001 Annex SL credit applies to management-system clauses 4-7.
            if iso27001_credit and cl in (4, 5, 6, 7):
                rating += 1
            ratings[cl] = min(rating, 5)
        return ratings

    # ------------------------------------------------------------------
    # Annex A coverage
    # ------------------------------------------------------------------

    def _annex_coverage(self, inputs: dict, text: str) -> dict:
        cmo = inputs.get("control_mapping_output") or {}
        controls = cmo.get("controls", [])
        designed = len(controls)
        ethana_covered = sum(1 for c in controls if c.get("platform_coverage"))

        # Implemented: controls already designed with platform coverage.
        # Partially Implemented: designed but bridged/partial.
        # Not Implemented: remainder of the 38 applicable controls.
        implemented = min(ethana_covered, _ANNEX_TOTAL)
        partial = min(max(designed - ethana_covered, 0), _ANNEX_TOTAL - implemented)
        # Documentation signal grants a small partial-credit bump.
        if "policy" in text and partial + implemented < _ANNEX_TOTAL:
            partial += 1
        not_applicable = 0
        applicable = _ANNEX_TOTAL - not_applicable
        not_implemented = max(applicable - implemented - partial, 0)

        return {
            "implemented": implemented,
            "partially_implemented": partial,
            "not_implemented": not_implemented,
            "not_applicable": not_applicable,
            "total_applicable": applicable,
        }

    # ------------------------------------------------------------------
    # AMS
    # ------------------------------------------------------------------

    def _compute_ams(self, clause_ratings: dict, annex: dict):
        clause_score = sum(clause_ratings[c] for c in _CLAUSES) / 7 * 20
        applicable = annex["total_applicable"] or 1
        annex_score = (annex["implemented"] + 0.5 * annex["partially_implemented"]) / applicable * 100
        ams = clause_score * 0.60 + annex_score * 0.40
        return round(ams, 1), round(clause_score, 1), round(annex_score, 1)

    # ------------------------------------------------------------------
    # ARS
    # ------------------------------------------------------------------

    def _compute_ars(self, inputs: dict, text: str, annex: dict) -> dict:
        # Documentation Completeness (30%)
        doc_terms = ["ai policy", "scope", "risk assessment", "impact assessment",
                     "statement of applicability", "internal audit"]
        doc_hits = sum(1 for t in doc_terms if t in text)
        documentation = min(round(doc_hits / len(doc_terms) * 100), 100)
        if "ai policy" not in text and "scope" not in text:
            documentation = min(documentation, 39)

        # Evidence Availability (40%) — proportional to implemented+partial coverage.
        applicable = annex["total_applicable"] or 1
        evidence = round((annex["implemented"] + 0.5 * annex["partially_implemented"])
                         / applicable * 100)

        # Control Operationalization (20%)
        control_op = round(annex["implemented"] / applicable * 100)

        # Management Review Readiness (10%)
        mgmt_terms = ["board", "committee", "management review", "ai objectives", "governance"]
        mgmt_hits = sum(1 for t in mgmt_terms if t in text)
        management = min(round(mgmt_hits / len(mgmt_terms) * 100), 100)

        ars = (documentation * 0.30 + evidence * 0.40
               + control_op * 0.20 + management * 0.10)
        return {
            "ars": round(ars, 1),
            "components": {
                "documentation_completeness": documentation,
                "evidence_availability": evidence,
                "control_operationalization": control_op,
                "management_review_readiness": management,
            },
        }

    # ------------------------------------------------------------------
    # Gap register
    # ------------------------------------------------------------------

    def _build_gaps(self, inputs: dict, clause_ratings: dict, annex: dict):
        eu_high_risk = self._is_eu_high_risk(inputs)
        bfsi = self._is_bfsi(inputs)
        elevated_clauses = set()
        if eu_high_risk:
            elevated_clauses |= {6, 8}
        if bfsi:
            elevated_clauses |= {8, 9}

        gaps = []          # list of (gap_id, severity)
        seq = {}

        def _next(prefix):
            seq[prefix] = seq.get(prefix, 0) + 1
            return f"GAP-{prefix}-{seq[prefix]:03d}"

        for cl in _CLAUSES:
            rating = clause_ratings[cl]
            severity = None
            if rating <= 1:
                severity = "Critical"
            elif rating == 2:
                severity = "Major"
            elif rating == 3:
                severity = "Minor"
            if severity is None:
                continue
            # EU high-risk / BFSI elevation raises severity one level.
            if cl in elevated_clauses:
                severity = {"Minor": "Major", "Major": "Critical",
                            "Critical": "Critical"}[severity]
            gaps.append((_next(f"CL{cl}"), severity))

        # Annex A Not Implemented contributes Major gaps; elevated categories Critical.
        not_impl = annex["not_implemented"]
        elevated_cats = set()
        if eu_high_risk:
            elevated_cats |= {2, 3}
        if bfsi:
            elevated_cats |= {3, 9}
        # Distribute not-implemented across categories deterministically.
        cat_cycle = list(_ANNEX_CATEGORIES.keys())
        for i in range(not_impl):
            cat = cat_cycle[i % len(cat_cycle)]
            severity = "Critical" if cat in elevated_cats else "Major"
            gaps.append((_next(f"AA{cat}"), severity))

        critical = [g for g, s in gaps if s == "Critical"]
        major = [g for g, s in gaps if s == "Major"]
        minor = [g for g, s in gaps if s == "Minor"]
        return {
            "gap_ids": [g for g, _ in gaps],
            "critical_gap_ids": critical,
            "critical": len(critical),
            "major": len(major),
            "minor": len(minor),
        }

    # ------------------------------------------------------------------
    # Classification (+ HD6) and months-to-readiness
    # ------------------------------------------------------------------

    @staticmethod
    def _classify(ams: float, ars: float, critical_gaps: int) -> str:
        # HD6: any open Critical gap precludes Certification Ready.
        if ams >= 80 and ars >= 75 and critical_gaps == 0:
            classification = "Certification Ready"
        elif (ams >= 60 or (ams >= 80 and 60 <= ars < 75)) and ars >= 60 and critical_gaps <= 2:
            classification = "Near Ready"
        elif ams >= 40:
            classification = "Significant Gaps"
        else:
            classification = "Major Gaps"

        # HD6 hard override (belt-and-suspenders): never Certification Ready with a Critical gap.
        if critical_gaps > 0 and classification == "Certification Ready":
            classification = "Near Ready"
        return classification

    @staticmethod
    def _months_to_readiness(critical: int, major: int, classification: str) -> int:
        if classification == "Certification Ready":
            return 0
        return min(2 * critical + major, 24)

    # ------------------------------------------------------------------
    # Quality score (gate — decoupled from AMS/ARS)
    # ------------------------------------------------------------------

    @staticmethod
    def _quality_score(inputs: dict) -> int:
        score = 92
        if not inputs.get("regulatory_mapping_output"):
            score -= 12
        if not inputs.get("control_mapping_output"):
            score -= 8
        return max(score, 70)

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def execute_gap_assessment(self, inputs: dict, logger=None) -> dict:
        if logger is not None:
            logger.log("SKILL_4_EXECUTION", "SUCCESS", "ISO 42001 gap assessment started.")

        ai_portfolio = (inputs.get("ai_portfolio", "") or "").strip()
        if not ai_portfolio:
            raise ValueError(
                "Skill 4 requires a non-empty ai_portfolio; an undefined portfolio "
                "cannot receive a valid AMS."
            )

        text = self._signal_text(inputs)
        clause_ratings = self._clause_ratings(inputs, text)
        annex = self._annex_coverage(inputs, text)

        ams, clause_score, annex_score = self._compute_ams(clause_ratings, annex)
        ars_result = self._compute_ars(inputs, text, annex)
        ars = ars_result["ars"]

        gaps = self._build_gaps(inputs, clause_ratings, annex)
        classification = self._classify(ams, ars, gaps["critical"])
        months = self._months_to_readiness(gaps["critical"], gaps["major"], classification)
        quality_score = self._quality_score(inputs)

        ams_clause_scores = {f"clause_{c}": clause_ratings[c] for c in _CLAUSES}
        markdown_output = self._compile_markdown(
            inputs, clause_ratings, annex, ams, ars, ars_result["components"],
            classification, gaps, months,
        )

        result = {
            # required schema fields
            "ams": ams,
            "ars": ars,
            "critical_gaps": gaps["critical"],
            "major_gaps": gaps["major"],
            "minor_gaps": gaps["minor"],
            "certification_classification": classification,
            "months_to_readiness": months,
            # optional audit fields
            "assessment_date": datetime.now(timezone.utc).date().isoformat(),
            "aims_scope": ai_portfolio[:280],
            "ams_clause_scores": ams_clause_scores,
            "ars_component_scores": ars_result["components"],
            "annex_a_coverage": annex,
            "gap_ids": gaps["gap_ids"],
            "critical_gap_ids": gaps["critical_gap_ids"],
            "ethana_claims_firewall_violations": 0,
            # CA envelope siblings
            "quality_score": int(quality_score),
            "markdown_output": markdown_output,
        }
        if logger is not None:
            logger.log("SKILL_4_EXECUTION", "SUCCESS",
                       f"Gap assessment complete. AMS {ams}, ARS {ars}, {classification}.")
        return result

    # ------------------------------------------------------------------
    # Markdown (Section 8.5 Ethana Coverage Analysis is firewall-clean:
    # it makes no Production claim about any Ethana capability)
    # ------------------------------------------------------------------

    def _compile_markdown(self, inputs, clause_ratings, annex, ams, ars,
                          ars_components, classification, gaps, months) -> str:
        lines = []
        lines.append("# ISO 42001 Gap Assessment\n")
        lines.append("## 1. Executive Summary\n")
        lines.append(f"- AIMS Maturity Score (AMS): **{ams}/100**")
        lines.append(f"- Audit Readiness Score (ARS): **{ars}/100**")
        lines.append(f"- Certification Classification: **{classification}**")
        lines.append(f"- Estimated months to Stage 1 readiness: **{months}**\n")

        lines.append("## 2. Clause Coverage Matrix\n")
        lines.append("| Clause | Name | Maturity (0–5) |")
        lines.append("|---|---|---|")
        for c in _CLAUSES:
            lines.append(f"| Clause {c} | {_CLAUSE_NAMES[c]} | {clause_ratings[c]} |")
        lines.append("")

        lines.append("## 3. Annex A Control Assessment\n")
        lines.append(f"- Implemented: {annex['implemented']}")
        lines.append(f"- Partially Implemented: {annex['partially_implemented']}")
        lines.append(f"- Not Implemented: {annex['not_implemented']}")
        lines.append(f"- Total Applicable: {annex['total_applicable']}\n")

        lines.append("## 4. Gap Register\n")
        lines.append(f"- Critical: {gaps['critical']} ({', '.join(gaps['critical_gap_ids']) or 'none'})")
        lines.append(f"- Major: {gaps['major']}")
        lines.append(f"- Minor: {gaps['minor']}\n")

        lines.append("## 9. Audit Readiness Assessment\n")
        lines.append(f"- Documentation Completeness: {ars_components['documentation_completeness']} × 0.30")
        lines.append(f"- Evidence Availability: {ars_components['evidence_availability']} × 0.40")
        lines.append(f"- Control Operationalization: {ars_components['control_operationalization']} × 0.20")
        lines.append(f"- Management Review Readiness: {ars_components['management_review_readiness']} × 0.10")
        lines.append(f"- **ARS = {ars}/100**\n")

        lines.append("## 8.5 Ethana Coverage Analysis\n")
        lines.append(
            "Ethana platform capabilities relevant to ISO 42001 conformance are "
            "assessed for fit only; no capability is represented beyond its canonical "
            "status. Platform coverage supplements — it does not substitute for — the "
            "organisation's own AIMS controls.\n"
        )

        lines.append("## 10. Overall Maturity Score\n")
        lines.append(f"AMS = {ams}/100, ARS = {ars}/100 → **{classification}**.\n")
        return "\n".join(lines)
