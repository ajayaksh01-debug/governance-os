#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def parse_canonical_model(cpm_path):
    """Parses canonical-product-model.md to extract capabilities and statuses."""
    capabilities = {}
    if not cpm_path.exists():
        print(f"Error: Canonical model not found at {cpm_path}", file=sys.stderr)
        return capabilities

    content = cpm_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    # Simple table parser
    in_table = False
    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            in_table = False
            continue
        if '|---|' in line or line.startswith('|---'):
            in_table = True
            continue
        
        # We are in a table row
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) >= 2:
            # Check if this looks like a header
            if parts[0].lower() in ["capability", "service", "certification", "model"]:
                continue
            
            # Clean capability name
            name_raw = parts[0].replace('**', '').replace('`', '')
            # Extract base name before any description dashboard or '—'
            name_base = re.split(r'—|-', name_raw)[0].strip()
            status = parts[1].strip()
            
            if name_base and status:
                # Normalize status
                status_norm = status.lower()
                if "in progress" in status_norm:
                    status_norm = "in build"
                elif "confirmed" in status_norm:
                    status_norm = "production"
                
                capabilities[name_base.lower()] = {
                    "original_name": name_base,
                    "status": status_norm
                }
    return capabilities

def lint_file(target_path, capabilities):
    """Lints a target file for firewall violations and capability ambiguities."""
    if not target_path.exists():
        print(f"Error: Target file not found at {target_path}", file=sys.stderr)
        sys.exit(2)

    content = target_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    violations = []
    
    # Specific Hard Rules
    workspace_re = re.compile(r'workspace', re.IGNORECASE)
    edge_re = re.compile(r'edge|sentry', re.IGNORECASE)
    agent_builder_re = re.compile(r'visual agent builder', re.IGNORECASE)

    for idx, line in enumerate(lines, 1):
        line_lower = line.lower()
        
        # Check specific hard rules
        if workspace_re.search(line) and not ("aspirational" in line_lower or "roadmap" in line_lower or "n/a" in line_lower):
            if any(term in line_lower for term in ["production", "ga", "shipped", "active"]):
                violations.append((idx, line, "Hard Rule Violation: Ethana Workspace is claimed as Production or GA. It is Aspirational and has no engineering codebase."))
        
        if edge_re.search(line) and "production" in line_lower:
            if not ("build gateway" in line_lower or "n/a" in line_lower or "roadmap" in line_lower):
                violations.append((idx, line, "Hard Rule Violation: Ethana Edge or Sentry is claimed as Production. Neither component is in production today."))
        
        if agent_builder_re.search(line) and not ("aspirational" in line_lower or "n/a" in line_lower):
            if any(term in line_lower for term in ["production", "ga", "shipped", "roadmap", "in build"]):
                violations.append((idx, line, "Hard Rule Violation: Visual Agent Builder is claimed as Production, In Build, or Roadmap. It is Aspirational and absent from engineering briefs."))

        # General capability status matching
        for cap_key, cap_data in capabilities.items():
            if cap_key in line_lower:
                status_canonical = cap_data["status"]
                original_name = cap_data["original_name"]
                
                # If capability is non-production, check for disclosure and workaround
                if status_canonical in ["in build", "roadmap", "aspirational"]:
                    # Must contain status keyword
                    has_status = any(term in line_lower for term in ["roadmap", "aspirational", "in build", "development", "planned"])
                    # Must contain workaround keyword
                    has_workaround = any(term in line_lower for term in ["workaround", "alternative", "manual", "cursory", "bridge", "service"])
                    
                    if "production" in line_lower and not ("road map" in line_lower or "planned" in line_lower):
                        violations.append((idx, line, f"Firewall Breach: Non-production capability '{original_name}' (canonical status: {status_canonical.upper()}) is referred to as Production."))
                    elif not has_status:
                        violations.append((idx, line, f"Ambiguity Warning: Capability '{original_name}' is mentioned without explicit status declaration (should state {status_canonical.upper()})."))
                    elif not has_workaround:
                        violations.append((idx, line, f"Missing Workaround: Capability '{original_name}' is roadmap-blocked, but no manual/third-party or Cursory workaround is detailed."))

    return violations

def main():
    if len(sys.argv) < 2:
        print("Usage: python claims_linter.py <path_to_draft_file.md>")
        sys.exit(1)
        
    target_path = Path(sys.argv[1])
    cpm_path = Path(__file__).resolve().parents[2] / "knowledge" / "ethana" / "canonical-product-model.md"
    
    print(f"Loading canonical product model from: {cpm_path.name}...")
    capabilities = parse_canonical_model(cpm_path)
    print(f"Loaded {len(capabilities)} capabilities from canonical model.")
    
    print(f"Linting target file: {target_path.name}...")
    violations = lint_file(target_path, capabilities)
    
    if violations:
        print("\n❌ Claims Firewall Breach or Ambiguity Detected:")
        for line_no, line_content, msg in violations:
            print(f"  Line {line_no}: {msg}")
            print(f"    Content: {line_content.strip()}")
        sys.exit(1)
    else:
        print("\n✅ Claims Firewall Check: Passed (0 violations detected).")
        sys.exit(0)

if __name__ == "__main__":
    main()
