#!/usr/bin/env python3
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Compile multiple skill scorecards into a single Client Governance Scorecard.")
    parser.add_argument("--skill1", help="Path to regulatory-mapping JSON output")
    parser.add_argument("--skill2", help="Path to governance-control-mapping JSON output")
    parser.add_argument("--skill3", help="Path to ethana-solution-mapping JSON output")
    parser.add_argument("--skill4", help="Path to iso-42001-gap-assessment JSON output")
    parser.add_argument("--skill5", help="Path to ethana-capability-validation JSON output (file or directory)")
    parser.add_argument("--skill6", help="Path to ethana-proposal-review JSON output")
    parser.add_argument("--approvals", help="Path to approvals decisions JSON output")
    parser.add_argument("--run-memory", help="Path to combined run memory JSON file")
    parser.add_argument("--traceability-id", default="TR-CA-2026-0001", help="Traceability ID format TR-CA-{YYYY}-{NNNN}")
    parser.add_argument("--client-name", default="Default Client", help="Name of the client")
    parser.add_argument("--output", help="Output JSON path (defaults to {traceability_id}-client-scorecard.json)")
    return parser.parse_args()

def load_json(path_str):
    if not path_str:
        return None
    p = Path(path_str)
    if not p.exists():
        print(f"Warning: File not found at {path_str}", file=sys.stderr)
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Warning: Error parsing JSON from {path_str}: {e}", file=sys.stderr)
        return None

def compile_scorecard(args):
    run_memory = {}
    if args.run_memory:
        run_memory = load_json(args.run_memory) or {}

    # Load individual skill payloads, falling back to run_memory keys if available
    s1 = load_json(args.skill1) or run_memory.get("skill_1_output") or {}
    s2 = load_json(args.skill2) or run_memory.get("skill_2_output") or {}
    s3 = load_json(args.skill3) or run_memory.get("skill_3_output") or {}
    s4 = load_json(args.skill4) or run_memory.get("skill_4_output") or {}
    s5_input = load_json(args.skill5) or run_memory.get("skill_5_output")
    s6 = load_json(args.skill6) or run_memory.get("skill_6_output") or {}
    approvals = load_json(args.approvals) or run_memory.get("all_approval_decisions") or {}

    # Normalize skill 5 output (could be a single object, list of objects, or dict representing them)
    s5_list = []
    if s5_input:
        if isinstance(s5_input, list):
            s5_list = s5_input
        elif isinstance(s5_input, dict):
            s5_list = [s5_input]

    # Process Skill 1: Regulatory Mapping
    reg_score = s1.get("score")
    if reg_score is None:
        # Fallback heuristic: calculate a dummy or look inside control requirements
        reg_score = 100 if s1.get("applicable_regulations") else 0
    jurisdictions = list(set(
        item.get("jurisdiction") 
        for item in s1.get("applicable_regulations", []) 
        if item.get("jurisdiction")
    ))
    risk_tier = s1.get("risk_tier", "High Risk") # default or parsed

    # Process Skill 2: Governance Control Mapping
    gcm_score = s2.get("score", 100 if s2.get("control_taxonomy_matrix") else 0)
    controls = s2.get("control_taxonomy_matrix", [])
    raci = s2.get("raci_matrix", [])
    control_count = len(controls)
    
    # Calculate orphan controls (controls in taxonomy that lack an accountable/responsible owner in RACI)
    raci_map = {item.get("control_id"): item for item in raci if item.get("control_id")}
    orphan_controls = 0
    for ctrl in controls:
        ctrl_id = ctrl.get("control_id")
        if ctrl_id:
            raci_entry = raci_map.get(ctrl_id)
            if not raci_entry or not raci_entry.get("responsible") or not raci_entry.get("accountable"):
                orphan_controls += 1

    # Process Skill 3: Ethana Solution Mapping
    matched_caps = s3.get("matched_capabilities", [])
    ccs_scores = [item.get("ccs_score", 0) for item in matched_caps if item.get("ccs_score") is not None]
    ccs_average = round(sum(ccs_scores) / len(ccs_scores), 2) if ccs_scores else 0
    
    req_at_least_70 = sum(1 for ccs in ccs_scores if ccs >= 70)
    production_coverage_percent = round((req_at_least_70 / len(ccs_scores)) * 100, 2) if ccs_scores else 0
    
    overall_summary = s3.get("overall_coverage_summary", {})
    commercial_motion = "Advisory-First" if overall_summary.get("advisory_first_recommended") else "Platform-Primary"

    # Process Skill 4: ISO 42001 Gap Assessment
    ams = s4.get("ams", 0)
    ars = s4.get("ars", 0)
    cert_class = s4.get("certification_classification", "Major Gaps")
    critical_gaps = s4.get("critical_gaps", 0)
    major_gaps = s4.get("major_gaps", 0)

    # Process Skill 5: Ethana Capability Validation
    capabilities_validated = len(s5_list)
    all_production_confirmed = all(item.get("validated_status") == "Production" for item in s5_list) if s5_list else False
    escalations_required = sum(1 for item in s5_list if item.get("escalation_required") is True)

    # Process Skill 6: Ethana Proposal Review
    pcs = s6.get("pcs", 0)
    ctcs = s6.get("ctcs", 0)
    release_classification = s6.get("classification", "Rejected")
    claims_firewall_status = "breach" if s6.get("cfb_count", 0) > 0 else "pass"

    # Compute Overall Readiness Band
    if pcs < 80 or claims_firewall_status == "breach" or release_classification == "Rejected":
        overall_readiness_band = "Delivery Blocked (PCS < 80 or firewall_breach)"
    elif ams >= 80 and pcs >= 90:
        overall_readiness_band = "Certification Ready (AMS >= 80, PCS >= 90)"
    elif 60 <= ams <= 79 and pcs >= 80:
        overall_readiness_band = "Assessment Complete — Gaps Identified (AMS 60–79, PCS >= 80)"
    else:
        overall_readiness_band = "Foundation Building (AMS < 60, PCS >= 80)"

    # Build Unified Scorecard JSON
    scorecard = {
        "traceability_id": args.traceability_id,
        "client_name": args.client_name,
        "assessment_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regulatory_assessment": {
            "score": reg_score,
            "jurisdictions": jurisdictions,
            "risk_tier": risk_tier
        },
        "control_assessment": {
            "score": gcm_score,
            "control_count": control_count,
            "orphan_controls": orphan_controls
        },
        "platform_coverage": {
            "ccs_average": ccs_average,
            "production_coverage_percent": production_coverage_percent,
            "commercial_motion": commercial_motion
        },
        "iso42001_assessment": {
            "ams": ams,
            "ars": ars,
            "certification_classification": cert_class,
            "critical_gaps": critical_gaps,
            "major_gaps": major_gaps
        },
        "capability_validation": {
            "capabilities_validated": capabilities_validated,
            "all_production_confirmed": all_production_confirmed,
            "escalations_required": escalations_required
        },
        "proposal_review": {
            "pcs": pcs,
            "ctcs": ctcs,
            "release_classification": release_classification,
            "claims_firewall_status": claims_firewall_status
        },
        "overall_readiness_band": overall_readiness_band
    }

    # Write output to file
    out_path_str = args.output or f"{args.traceability_id}-client-scorecard.json"
    out_path = Path(out_path_str)
    try:
        out_path.write_text(json.dumps(scorecard, indent=2), encoding="utf-8")
        print(f"Successfully compiled scorecard and wrote to {out_path.resolve()}")
    except Exception as e:
        print(f"Error writing output scorecard: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    args = parse_args()
    compile_scorecard(args)

if __name__ == "__main__":
    main()
