#!/usr/bin/env python3
import glob
import json
from datetime import date, datetime, timezone
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]

# coverage_classification values that count as Implemented in the CCR numerator
_IMPLEMENTED = frozenset({
    "Fully Covered by Ethana",
    "Covered by Cursory Service",
    "Customer-Owned Control",
})
_PARTIAL = frozenset({"Partially Covered by Ethana"})


class SkillExecutor:
    def __init__(self, runs_dir: Path, logs_dir: Path):
        self.runs_dir = runs_dir
        self.logs_dir = logs_dir

    # ------------------------------------------------------------------
    # Traceability ID
    # ------------------------------------------------------------------

    def generate_traceability_id(self) -> str:
        current_year = datetime.now(timezone.utc).year
        existing = glob.glob(str(self.runs_dir / f"TR-GR-{current_year}-*_state.json"))
        numbers = []
        for f in existing:
            stem = Path(f).name.split("_")[0]
            parts = stem.split("-")
            if len(parts) >= 4:
                try:
                    numbers.append(int(parts[3]))
                except ValueError:
                    pass
        next_num = max(numbers) + 1 if numbers else 1
        return f"TR-GR-{current_year}-{next_num:04d}"

    # ------------------------------------------------------------------
    # Main execution entry point
    # ------------------------------------------------------------------

    def execute_governance_review(self, state_mgr, inputs: dict, logger) -> dict:
        reg_output = inputs.get("regulatory_mapping_output") or {}
        ctrl_output = inputs.get("control_mapping_output") or {}
        iso_output = inputs.get("iso_42001_output")
        cap_output = inputs.get("capability_validation_output")
        client_profile = inputs.get("client_profile") or {}

        applicable_regulations = reg_output.get("applicable_regulations") or []
        applicable_frameworks = reg_output.get("applicable_frameworks") or []
        control_requirements = reg_output.get("control_requirements") or []
        control_taxonomy_matrix = ctrl_output.get("control_taxonomy_matrix") or []
        evidence_registry = ctrl_output.get("evidence_registry") or []

        # ------------------------------------------------------------------
        # Input completeness signal
        # ------------------------------------------------------------------
        if cap_output:
            input_completeness = "Full"
        elif client_profile:
            input_completeness = "Standard"
        else:
            input_completeness = "Minimal"

        logger.log("RUNNING_REVIEW", "SUCCESS", f"Input completeness: {input_completeness}")

        # Secondary guard: GTG-3 pre-check inside executor
        # (intake schema already enforces iso_42001_output as required object, but
        # a direct executor call in tests may pass None to exercise this guard)
        if iso_output is None:
            return self._not_governance_ready_due_to_gate_failure(
                "GTG-3 Fail: iso_42001_output absent",
                applicable_regulations, applicable_frameworks,
                control_requirements, control_taxonomy_matrix, evidence_registry,
                cap_output, input_completeness, logger
            )

        # ------------------------------------------------------------------
        # CCR computation
        # ------------------------------------------------------------------
        mandatory_controls = [c for c in control_requirements if c.get("mandatory", False)]
        ccr_denominator = len(mandatory_controls)

        if ccr_denominator == 0:
            raise ValueError(
                "CCR denominator is 0: no mandatory controls found in control_requirements. "
                "Verify regulatory_mapping_output.control_requirements contains items with mandatory=true."
            )

        # Build taxonomy lookup: control_name → coverage_classification
        taxonomy_lookup = {
            e.get("control_name", ""): e.get("coverage_classification", "")
            for e in control_taxonomy_matrix
            if e.get("control_name")
        }

        # Per-domain statistics
        domain_stats = {}
        for ctrl in mandatory_controls:
            domain = ctrl.get("domain", "Unknown")
            name = ctrl.get("control_name", "")
            coverage = taxonomy_lookup.get(name)

            if domain not in domain_stats:
                domain_stats[domain] = {
                    "total": 0, "implemented": 0, "partial": 0, "missing": []
                }
            domain_stats[domain]["total"] += 1

            if coverage in _IMPLEMENTED:
                domain_stats[domain]["implemented"] += 1
            elif coverage in _PARTIAL:
                domain_stats[domain]["partial"] += 1
            else:
                domain_stats[domain]["missing"].append(name)

        # Domain CCR rates; identify CGC domains (rate < 50%)
        cgc_domains = set()
        for domain, stats in domain_stats.items():
            total = stats["total"]
            rate = (stats["implemented"] + stats["partial"] * 0.5) / total * 100 if total > 0 else 0.0
            stats["ccr"] = round(rate, 1)
            if rate < 50.0:
                cgc_domains.add(domain)

        # Overall CCR
        impl_count = sum(s["implemented"] for s in domain_stats.values())
        part_count = sum(s["partial"] for s in domain_stats.values())
        ccr_numerator = impl_count + part_count * 0.5
        ccr = round(ccr_numerator / ccr_denominator * 100, 1)

        logger.log(
            "CCR_COMPUTED", "SUCCESS",
            f"numerator={ccr_numerator}, denominator={ccr_denominator}, ccr={ccr}"
        )

        # ------------------------------------------------------------------
        # Gap register
        # ------------------------------------------------------------------
        gaps = []
        _cm_counter = [0]
        _is_counter = [0]

        def next_cm_id():
            _cm_counter[0] += 1
            return f"GGP-CM-{_cm_counter[0]:03d}"

        def next_is_id():
            _is_counter[0] += 1
            return f"GGP-IS-{_is_counter[0]:03d}"

        # CC-MGFs: mandatory controls not in taxonomy (only for non-CGC domains)
        mgf_ids = []
        mgf_count = 0
        for domain, stats in domain_stats.items():
            for missing_ctrl in stats["missing"]:
                if domain in cgc_domains:
                    # Subsumed by CGC — logged as context, not counted as MGF
                    gaps.append({
                        "id": next_cm_id(),
                        "description": f"Mandatory control not in taxonomy (subsumed by CGC): {missing_ctrl}",
                        "source": "Control Coverage Assessment",
                        "severity": "Major",
                        "domain": domain,
                        "remediation": "Technical",
                        "subsumed_by_cgc": True,
                    })
                else:
                    g_id = next_cm_id()
                    mgf_ids.append(g_id)
                    mgf_count += 1
                    gaps.append({
                        "id": g_id,
                        "description": f"Mandatory control not in taxonomy — never designed: {missing_ctrl}",
                        "source": "Control Coverage Assessment",
                        "severity": "Major",
                        "domain": domain,
                        "remediation": "Technical",
                        "subsumed_by_cgc": False,
                    })

        # GP-MGF: ISO major gaps → aggregated to ONE Minor Finding per GR-001
        minor_finding_count = 0
        if (iso_output.get("major_gaps") or 0) > 0:
            g_id = next_is_id()
            gaps.append({
                "id": g_id,
                "description": (
                    f"ISO 42001 major management-system gaps "
                    f"({iso_output['major_gaps']} identified) — "
                    f"downgraded to Minor Finding per GR-001 calibration"
                ),
                "source": "ISO 42001 Gap Assessment",
                "severity": "Minor",
                "domain": "Management System",
                "remediation": "Process",
                "subsumed_by_cgc": False,
            })
            minor_finding_count += 1

        # ISO minor gaps → aggregated to ONE Minor Finding
        if (iso_output.get("minor_gaps") or 0) > 0:
            g_id = next_is_id()
            gaps.append({
                "id": g_id,
                "description": (
                    f"ISO 42001 minor management-system gaps "
                    f"({iso_output['minor_gaps']} identified)"
                ),
                "source": "ISO 42001 Gap Assessment",
                "severity": "Minor",
                "domain": "Management System",
                "remediation": "Process",
                "subsumed_by_cgc": False,
            })
            minor_finding_count += 1

        # ------------------------------------------------------------------
        # CGC identification
        # ------------------------------------------------------------------
        cgc_list = []
        for idx, domain in enumerate(sorted(cgc_domains), start=1):
            stats = domain_stats[domain]
            cgc_list.append({
                "id": f"CGC-{idx:03d}",
                "source": "Control Coverage Assessment",
                "domain": domain,
                "description": (
                    f"Domain implementation rate {stats['ccr']}% — "
                    f"{stats['implemented']} of {stats['total']} mandatory controls designed; "
                    f"below 50% CGC threshold"
                ),
            })

        cgc_count = len(cgc_list)
        cgc_ids = [c["id"] for c in cgc_list]

        # Missing mandatory framework check (ISO 42001 absent when required)
        missing_mandatory_framework_count = 0
        # iso_output is confirmed non-None at this point; this counter stays 0.
        # Kept for completeness if executor is called with iso_output=None via secondary guard path.

        # ------------------------------------------------------------------
        # GAS computation
        # ------------------------------------------------------------------
        gas_arithmetic = (
            100
            - (15 * missing_mandatory_framework_count)
            - (10 * mgf_count)
            - (2 * minor_finding_count)
        )
        absolute_rule_applied = cgc_count > 0
        gas = 0 if absolute_rule_applied else gas_arithmetic

        logger.log(
            "GAS_COMPUTED", "SUCCESS",
            f"arithmetic={gas_arithmetic}, cgc_count={cgc_count}, "
            f"absolute_rule_applied={absolute_rule_applied}, final_gas={gas}"
        )

        # ------------------------------------------------------------------
        # High-risk count heuristic
        # iso_ams < threshold → 1 additional High risk (management system immaturity)
        # ------------------------------------------------------------------
        iso_ams = iso_output.get("ams") if iso_output else 100
        ams_threshold = 70
        high_risk_count = cgc_count + (1 if (iso_ams is not None and iso_ams < ams_threshold) else 0)

        # ------------------------------------------------------------------
        # GTG gate evaluation
        # ------------------------------------------------------------------
        confirmed_regs = [r for r in applicable_regulations if r.get("status") == "Confirmed"]
        gates = {
            "GTG-1": "Pass" if (applicable_regulations and confirmed_regs) else "Fail",
            "GTG-2": "Pass" if control_taxonomy_matrix else "Fail",
            "GTG-3": "Pass",  # iso_output confirmed present (secondary guard above handles None)
            "GTG-4": (
                "Pass"
                if (cap_output and cap_output.get("allowed_claims"))
                else "Noted absent"
            ),
            "GTG-5": (
                "Pass"
                if (cgc_count > 0 or mgf_count > 0 or minor_finding_count > 0 or high_risk_count > 0)
                else "Noted absent"
            ),
            "GTG-6": "Pass" if evidence_registry else "Noted absent",
            "GTG-7": (
                "Pass"
                if (applicable_regulations or applicable_frameworks)
                else "Fail"
            ),
        }

        for gate_id, status in gates.items():
            log_status = "PASS" if status == "Pass" else ("FAIL" if status == "Fail" else "NOTED")
            logger.log("GTG_EVALUATION", log_status, f"{gate_id}: {status}")

        mandatory_gates = ["GTG-1", "GTG-2", "GTG-3", "GTG-7"]
        governance_gate_passed = all(gates[g] == "Pass" for g in mandatory_gates)

        # ------------------------------------------------------------------
        # Classification
        # ------------------------------------------------------------------
        thresholds = {
            "gas_gr": 85, "ccr_gr": 80.0, "hr_gr": 1,
            "gas_cg": 65, "ccr_cg": 60.0, "hr_cg": 2,
        }

        if not governance_gate_passed or cgc_count > 0:
            classification = "Not Governance Ready"
        elif (gas >= thresholds["gas_gr"] and ccr >= thresholds["ccr_gr"]
              and mgf_count == 0 and high_risk_count <= thresholds["hr_gr"]):
            classification = "Governance Ready"
        elif (gas >= thresholds["gas_cg"] and ccr >= thresholds["ccr_cg"]
              and high_risk_count <= thresholds["hr_cg"]):
            classification = "Conditional Governance"
        else:
            classification = "Not Governance Ready"

        logger.log(
            "CLASSIFICATION_DETERMINED", "SUCCESS",
            f"gas={gas}, ccr={ccr}, cgc_count={cgc_count}, mgf_count={mgf_count}, "
            f"governance_gate_passed={governance_gate_passed}, "
            f"classification={classification}"
        )

        # ------------------------------------------------------------------
        # ISO pass-through (GHD6)
        # ------------------------------------------------------------------
        iso_42001_ams = iso_output.get("ams")
        iso_42001_ars = iso_output.get("ars")
        iso_42001_classification = iso_output.get("certification_classification")

        # ------------------------------------------------------------------
        # Frameworks assessed in Section 6
        # ------------------------------------------------------------------
        frameworks_assessed = [r.get("name", "") for r in applicable_regulations if r.get("name")]
        for fw in applicable_frameworks:
            fw_name = fw.get("name", "")
            if fw_name:
                frameworks_assessed.append(fw_name)

        # ------------------------------------------------------------------
        # Remediation actions
        # ------------------------------------------------------------------
        required_actions = self._build_required_actions(cgc_list, mgf_ids, gaps)

        # ------------------------------------------------------------------
        # Assemble JSON payload
        # ------------------------------------------------------------------
        output_json = {
            "gas": gas,
            "ccr": ccr,
            "ccr_numerator": ccr_numerator,
            "ccr_denominator": ccr_denominator,
            "cgc_count": cgc_count,
            "cgc_ids": cgc_ids,
            "mgf_count": mgf_count,
            "mgf_ids": mgf_ids,
            "minor_finding_count": minor_finding_count,
            "high_risk_count": high_risk_count,
            "classification": classification,
            "governance_gate_passed": governance_gate_passed,
            "iso_42001_ams": iso_42001_ams,
            "iso_42001_ars": iso_42001_ars,
            "iso_42001_classification": iso_42001_classification,
            "frameworks_assessed": frameworks_assessed,
            "review_date": date.today().isoformat(),
            "input_completeness": input_completeness,
            "required_actions": required_actions,
        }

        # ------------------------------------------------------------------
        # Markdown report
        # ------------------------------------------------------------------
        report_md = self._build_markdown_report(
            traceability_id=state_mgr.traceability_id,
            output_json=output_json,
            domain_stats=domain_stats,
            cgc_domains=cgc_domains,
            cgc_list=cgc_list,
            gaps=gaps,
            gates=gates,
            applicable_regulations=applicable_regulations,
            applicable_frameworks=applicable_frameworks,
            cap_output=cap_output,
            iso_output=iso_output,
            gas_arithmetic=gas_arithmetic,
            missing_mandatory_framework_count=missing_mandatory_framework_count,
            mgf_count=mgf_count,
            minor_finding_count=minor_finding_count,
            absolute_rule_applied=absolute_rule_applied,
        )

        state_mgr.update_intermediate_data("governance_review_json", output_json)
        state_mgr.update_intermediate_data("governance_review_md", report_md)

        return output_json

    # ------------------------------------------------------------------
    # Secondary guard path: GTG-3 failure (iso_42001_output absent)
    # ------------------------------------------------------------------

    def _not_governance_ready_due_to_gate_failure(
        self, reason, applicable_regulations, applicable_frameworks,
        control_requirements, control_taxonomy_matrix, evidence_registry,
        cap_output, input_completeness, logger
    ) -> dict:
        logger.log("GTG_EVALUATION", "FAIL", f"GTG-3: Fail — {reason}")
        mandatory_controls = [c for c in control_requirements if c.get("mandatory", False)]
        ccr_denominator = len(mandatory_controls) or 1
        ccr_numerator = 0.0
        ccr = 0.0
        return {
            "gas": 0,
            "ccr": ccr,
            "ccr_numerator": ccr_numerator,
            "ccr_denominator": ccr_denominator,
            "cgc_count": 1,
            "cgc_ids": [],
            "mgf_count": 0,
            "mgf_ids": [],
            "minor_finding_count": 0,
            "high_risk_count": 1,
            "classification": "Not Governance Ready",
            "governance_gate_passed": False,
            "iso_42001_ams": None,
            "iso_42001_ars": None,
            "iso_42001_classification": None,
            "frameworks_assessed": [],
            "review_date": date.today().isoformat(),
            "input_completeness": input_completeness,
            "required_actions": [f"IMMEDIATE: {reason}"],
        }

    # ------------------------------------------------------------------
    # Remediation actions
    # ------------------------------------------------------------------

    def _build_required_actions(self, cgc_list: list, mgf_ids: list, gaps: list) -> list:
        actions = []
        action_counter = [0]

        def add(description, priority):
            action_counter[0] += 1
            actions.append(f"GRA-{action_counter[0]:03d} [{priority}]: {description}")

        for cgc in cgc_list:
            add(
                f"Resolve {cgc['id']}: {cgc['description']}",
                "IMMEDIATE"
            )

        for gap in gaps:
            if gap.get("id") in mgf_ids:
                add(
                    f"Address {gap['id']}: {gap['description']}",
                    "BEFORE_DEPLOYMENT"
                )

        return actions

    # ------------------------------------------------------------------
    # 10-section Markdown report
    # ------------------------------------------------------------------

    def _build_markdown_report(
        self, traceability_id, output_json, domain_stats, cgc_domains,
        cgc_list, gaps, gates, applicable_regulations, applicable_frameworks,
        cap_output, iso_output, gas_arithmetic, missing_mandatory_framework_count,
        mgf_count, minor_finding_count, absolute_rule_applied
    ) -> str:
        classification = output_json["classification"]
        gas = output_json["gas"]
        ccr = output_json["ccr"]
        cgc_count = output_json["cgc_count"]
        governance_gate_passed = output_json["governance_gate_passed"]
        iso_ams = output_json.get("iso_42001_ams")
        iso_ars = output_json.get("iso_42001_ars")
        iso_cls = output_json.get("iso_42001_classification")

        sections = []

        # ------------------------------------------------------------------
        # Section 1: Executive Governance Summary
        # ------------------------------------------------------------------
        if classification == "Governance Ready":
            verdict_text = (
                f"This organisation's AI governance framework is assessed as **Governance Ready**. "
                f"GAS {gas}/100 and CCR {ccr}% both meet the required thresholds. "
                f"No Critical Governance Gaps or Major Governance Findings are present."
            )
            next_action = "Proceed to deployment. Schedule reassessment at next major platform or regulatory change."
        elif classification == "Conditional Governance":
            mgf_refs = ", ".join(output_json.get("mgf_ids", []))
            verdict_text = (
                f"This organisation's AI governance framework is assessed as **Conditional Governance**. "
                f"GAS {gas}/100 and CCR {ccr}% meet minimum thresholds, but "
                f"{mgf_count} Major Governance Finding(s) ({mgf_refs}) must be addressed before deployment."
            )
            next_action = f"Remediate findings {mgf_refs} before deployment. Reassess once remediation is confirmed."
        else:
            cgc_refs = ", ".join(cgc_ids for cgc_ids in output_json.get("cgc_ids", []))
            if not cgc_refs:
                cgc_refs = "mandatory gate failure"
            verdict_text = (
                f"This organisation's AI governance framework is assessed as **Not Governance Ready**. "
                f"Classification driver: {cgc_refs if cgc_count > 0 else 'mandatory GTG gate failure'}. "
                f"GAS = {gas}/100 (absolute rule applied: {absolute_rule_applied}). "
                f"CCR = {ccr}%. No deployment may proceed until all CGCs are resolved."
            )
            next_action = f"Resolve CGC(s) immediately. Reassess after remediation is confirmed. See Section 9."

        sections.append(f"""## 1. Executive Governance Summary

**Classification:** {classification}
**Governance Assessment Score (GAS):** {gas} / 100
**Control Coverage Rate (CCR):** {ccr}%
**Critical Governance Gaps (CGC):** {cgc_count}
**Major Governance Findings (MGF):** {mgf_count}
**High Residual Risks:** {output_json['high_risk_count']}
**Governance Gate Passed:** {governance_gate_passed}

{verdict_text}

**Immediate next action:** {next_action}""")

        # ------------------------------------------------------------------
        # Section 2: Regulatory Scope and Framework Matrix
        # ------------------------------------------------------------------
        reg_rows = []
        for reg in applicable_regulations:
            reg_rows.append(
                f"| {reg.get('name','')} | Regulation | {reg.get('jurisdiction','')} | Yes | {reg.get('status','')} |"
            )
        for fw in applicable_frameworks:
            mandatory_flag = "Yes" if fw.get("mandatory") else "No"
            reg_rows.append(
                f"| {fw.get('name','')} | Framework | — | {mandatory_flag} | In Scope |"
            )

        sections.append(f"""## 2. Regulatory Scope and Framework Matrix

| Entry | Type | Jurisdiction | Mandatory | Status |
|---|---|---|---|---|
{chr(10).join(reg_rows)}""")

        # ------------------------------------------------------------------
        # Section 3: Control Coverage Assessment
        # ------------------------------------------------------------------
        domain_rows = []
        for domain, stats in domain_stats.items():
            cgc_flag = " ← CGC" if domain in cgc_domains else ""
            domain_rows.append(
                f"| {domain} | {stats['total']} | {stats['implemented']} | "
                f"{stats['partial']} | {stats['ccr']}{cgc_flag} |"
            )

        impl_count = sum(s["implemented"] for s in domain_stats.values())
        part_count = sum(s["partial"] for s in domain_stats.values())
        ccr_num = output_json["ccr_numerator"]
        ccr_den = output_json["ccr_denominator"]

        sections.append(f"""## 3. Control Coverage Assessment

| Domain | Mandatory Controls | Implemented | Partially Implemented | Domain CCR |
|---|---|---|---|---|
{chr(10).join(domain_rows)}

```
CCR denominator:       {ccr_den}
Implemented:           {impl_count}
Partially Implemented: {part_count} × 0.5 = {part_count * 0.5}
CCR numerator:         {ccr_num}
CCR:                   round({ccr_num} / {ccr_den} × 100, 1) = {output_json['ccr']}
```""")

        # ------------------------------------------------------------------
        # Section 4: Governance Gap Register
        # ------------------------------------------------------------------
        gap_rows = []
        for gap in gaps:
            if gap.get("subsumed_by_cgc"):
                continue
            gap_rows.append(
                f"| {gap['id']} | {gap['description'][:60]}... | {gap['source']} | "
                f"{gap['severity']} | {gap['domain']} | {gap['remediation']} |"
            )

        sections.append(f"""## 4. Governance Gap Register

| Gap ID | Description | Source | Severity | Domain | Remediation Category |
|---|---|---|---|---|---|
{chr(10).join(gap_rows) if gap_rows else '| — | No active gaps identified | — | — | — | — |'}""")

        # ------------------------------------------------------------------
        # Section 5: Governance Risk Register
        # ------------------------------------------------------------------
        risks = []
        risk_counter = [0]

        def add_risk(desc, severity, owner, status):
            risk_counter[0] += 1
            risks.append({
                "id": f"GRK-{risk_counter[0]:03d}",
                "description": desc,
                "severity": severity,
                "owner": owner,
                "status": status,
            })

        for cgc in cgc_list:
            add_risk(
                f"Critical Governance Gap: {cgc['domain']} — {cgc['description']}",
                "High", "Chief Risk Officer", "Escalated"
            )

        if iso_ams is not None and iso_ams < 70:
            add_risk(
                f"AI management system at significant risk: AMS {iso_ams}/100 — "
                f"management system gaps may impact audit readiness",
                "High", "CISO", "Escalated"
            )

        for gap in gaps:
            if gap.get("id") in output_json.get("mgf_ids", []):
                add_risk(
                    f"Major governance finding: {gap['description'][:80]}",
                    "Medium", "Governance Lead", "Residual"
                )

        risk_rows = [
            f"| {r['id']} | {r['description'][:70]}... | {r['severity']} | {r['owner']} | {r['status']} |"
            for r in risks
        ]

        sections.append(f"""## 5. Governance Risk Register

| Risk ID | Description | Severity | Owner | Status |
|---|---|---|---|---|
{chr(10).join(risk_rows) if risk_rows else '| — | No significant residual risks | Low | — | Accepted |'}""")

        # ------------------------------------------------------------------
        # Section 6: Framework Compliance Scores
        # ------------------------------------------------------------------
        fw_rows = []
        for reg in applicable_regulations:
            fw_rows.append(
                f"| {reg.get('name','')} | {reg.get('jurisdiction','')} | "
                f"Assessed via regulatory mapping | {reg.get('status','')} |"
            )

        if iso_output is not None:
            fw_rows.append(
                f"| ISO 42001 | — | "
                f"AMS: {iso_ams}/100, ARS: {iso_ars}/100, Classification: {iso_cls} | "
                f"Assessed |"
            )

        sections.append(f"""## 6. Framework Compliance Scores

| Framework / Regulation | Jurisdiction | Assessment Summary | Status |
|---|---|---|---|
{chr(10).join(fw_rows)}

**ISO 42001 pass-through (GHD6):** Values sourced directly from iso_42001_output — not recalculated.
- AIMS Maturity Score (AMS): {iso_ams} / 100
- Audit Readiness Score (ARS): {iso_ars} / 100
- ISO 42001 Classification: {iso_cls}""")

        # ------------------------------------------------------------------
        # Section 7: Governance TG Gate Table
        # ------------------------------------------------------------------
        gate_descriptions = {
            "GTG-1": "Regulatory scope confirmed",
            "GTG-2": "Control mapping present",
            "GTG-3": "Gap assessment present",
            "GTG-4": "Capability alignment confirmed",
            "GTG-5": "Risk register complete",
            "GTG-6": "Evidence traceability confirmed",
            "GTG-7": "Framework coverage confirmed",
        }
        gate_rows = [
            f"| {gid} | {gate_descriptions.get(gid, '')} | {status} |"
            for gid, status in gates.items()
        ]

        sections.append(f"""## 7. Governance TG Gate Table

| Gate | Step | Status |
|---|---|---|
{chr(10).join(gate_rows)}

`governance_gate_passed: {governance_gate_passed}` — GTG-1, GTG-2, GTG-3, and GTG-7 are mandatory.""")

        # ------------------------------------------------------------------
        # Section 8: Capability Governance Alignment
        # ------------------------------------------------------------------
        if cap_output and cap_output.get("allowed_claims"):
            claim_rows = []
            for claim in cap_output["allowed_claims"]:
                claim_text = claim.get("claim", "") if isinstance(claim, dict) else str(claim)
                cpl = claim.get("cpl", "—") if isinstance(claim, dict) else "—"
                claim_rows.append(f"| {claim_text[:70]} | {cpl} | Mapped |")

            sec8 = f"""## 8. Capability Governance Alignment

| Capability Claim | CPL | Governance Status |
|---|---|---|
{chr(10).join(claim_rows)}"""
        else:
            sec8 = """## 8. Capability Governance Alignment

GTG-4 not passed — `capability_validation_output` not provided. Section 8 cannot be completed. \
Capability governance alignment is unknown. CCR ceiling is limited to `control_taxonomy_matrix` entries only."""

        sections.append(sec8)

        # ------------------------------------------------------------------
        # Section 9: Required Remediation Actions
        # ------------------------------------------------------------------
        action_lines = "\n".join(
            f"{i+1}. {action}"
            for i, action in enumerate(output_json.get("required_actions", []))
        ) or "No immediate remediation actions required."

        sections.append(f"""## 9. Required Remediation Actions

{action_lines}""")

        # ------------------------------------------------------------------
        # Section 10: Governance Release Decision
        # ------------------------------------------------------------------
        abs_note = " [absolute rule — CGC present overrides arithmetic]" if absolute_rule_applied else ""
        gas_arithmetic_line = f"[{gas_arithmetic}]" if absolute_rule_applied else str(gas_arithmetic)

        sections.append(f"""## 10. Governance Release Decision

```
AIMS Maturity Score (AMS):          {iso_ams} / 100
Audit Readiness Score (ARS):        {iso_ars} / 100
ISO 42001 Classification:           {iso_cls}

CCR denominator:                    {output_json['ccr_denominator']}
  Implemented:                      {impl_count}
  Partially Implemented:            {part_count} × 0.5 = {part_count * 0.5}
CCR numerator:                      {output_json['ccr_numerator']}
Control Coverage Rate (CCR):        round({output_json['ccr_numerator']} / {output_json['ccr_denominator']} × 100, 1) = {output_json['ccr']}

GAS base:                           100
  Missing mandatory frameworks:     {missing_mandatory_framework_count} × −15 = −{15 * missing_mandatory_framework_count}
  Major Governance Findings:        {mgf_count} × −10 = −{10 * mgf_count}
  Minor Governance Findings:        {minor_finding_count} × −2  = −{2 * minor_finding_count}
  Critical Governance Gap present:  {'Yes' if absolute_rule_applied else 'No'}
GAS arithmetic result:              {gas_arithmetic_line}
Final GAS:                          {gas} / 100{abs_note}

Critical Governance Gaps (CGC):     {cgc_count}
Major Governance Findings (MGF):    {mgf_count}
High Residual Risks:                {output_json['high_risk_count']}
governance_gate_passed:             {governance_gate_passed}
Governance Readiness:               {classification}
```

**Governance Readiness Certificate — JSON Payload**

```json
{json.dumps(output_json, indent=2)}
```""")

        header = (
            f"# Governance Review Report: {traceability_id}\n\n"
            f"**Classification:** {classification}  \n"
            f"**GAS:** {gas}/100  \n"
            f"**CCR:** {ccr}%  \n"
            f"**Review Date:** {output_json['review_date']}  \n"
            f"**Input Completeness:** {output_json['input_completeness']}  \n\n"
            f"---\n"
        )

        return header + "\n\n---\n\n".join(sections)
