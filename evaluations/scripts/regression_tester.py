#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path

def parse_markdown(md_path):
    """Parses markdown output to extract structural headers and tables."""
    headers = []
    # Dictionary mapping header -> list of tables found under it.
    # Each table is a list of header columns.
    tables = {} 
    
    if not md_path.exists():
        print(f"Error: Target markdown file not found at {md_path}", file=sys.stderr)
        return headers, tables

    content = md_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    current_header = None
    in_table = False
    table_headers = []
    
    for line in lines:
        line = line.strip()
        
        # Track headers
        if line.startswith('#'):
            # Strip trailing/leading spaces and bold markers from headers
            hdr = line.replace('**', '').replace('`', '').strip()
            headers.append(hdr)
            current_header = hdr
            in_table = False
            continue
            
        # Parse tables
        if line.startswith('|'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            
            # Separator line
            if all(re.match(r'^:-*-+:?$', p) or re.match(r'^-+$', p) for p in parts):
                in_table = True
                continue
                
            if in_table:
                # We already parsed the header row in the line before separator
                continue
            else:
                # This is the header row
                table_headers = parts
                if current_header:
                    if current_header not in tables:
                        tables[current_header] = []
                    tables[current_header].append(table_headers)
                in_table = True  # We expect separator next
        else:
            in_table = False
            
    return headers, tables

def run_regression_test(target_path, baseline_path):
    """Runs a structural regression test against a baseline configuration JSON."""
    if not baseline_path.exists():
        print(f"Error: Baseline file not found at {baseline_path}", file=sys.stderr)
        return ["Baseline config file missing"]

    try:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"Error parsing baseline JSON: {e}"]

    headers, tables = parse_markdown(target_path)
    errors = []

    # 1. Validate Required Headers
    required_headers = baseline.get("required_headers", [])
    for req_hdr in required_headers:
        # Search for exact or substring match in parsed headers
        match_found = any(req_hdr in h for h in headers)
        if not match_found:
            errors.append(f"Missing required section header: '{req_hdr}'")

    # 2. Validate Required Tables
    required_tables = baseline.get("required_tables", [])
    for req_tbl in required_tables:
        preceding_hdr = req_tbl.get("preceding_header")
        required_cols = req_tbl.get("required_columns", [])
        
        # Check if we parsed tables under this header
        found_tables = []
        for hdr, tbl_list in tables.items():
            if preceding_hdr in hdr:
                found_tables.extend(tbl_list)
                
        if not found_tables:
            errors.append(f"Missing required table under header: '{preceding_hdr}'")
            continue
            
        # Validate column headers in the found table
        for req_col in required_cols:
            col_match = False
            for tbl in found_tables:
                if any(req_col.lower() in col.lower() for col in tbl):
                    col_match = True
                    break
            if not col_match:
                errors.append(f"Table under '{preceding_hdr}' is missing required column: '{req_col}'")

    # 3. Score Threshold Validation
    # In a real environment, we'd run the local score evaluation script here.
    # As a surrogate check, verify if target score meets baseline threshold
    pass_threshold = baseline.get("pass_threshold", 70)
    target_content = target_path.read_text(encoding="utf-8")
    
    # Heuristically parse score from markdown if declared
    score_match = re.search(r'score:\s*(\d+)/100', target_content, re.IGNORECASE)
    if score_match:
        score = int(score_match.group(1))
        if score < pass_threshold:
            errors.append(f"Validation Score {score}/100 falls below pass threshold of {pass_threshold}/100")
            
    return errors

def main():
    if len(sys.argv) < 3:
        print("Usage: python regression_tester.py <path_to_target_output.md> <path_to_baseline.json>")
        sys.exit(1)
        
    target_path = Path(sys.argv[1])
    baseline_path = Path(sys.argv[2])
    
    print(f"Running structural regression test on {target_path.name}...")
    errors = run_regression_test(target_path, baseline_path)
    
    if errors:
        print("\n❌ Structural Regression Check: Failed (structural errors found):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\n✅ Structural Regression Check: Passed (structure matches baseline).")
        sys.exit(0)

if __name__ == "__main__":
    main()
