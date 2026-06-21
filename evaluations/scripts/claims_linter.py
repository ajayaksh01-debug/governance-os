#!/usr/bin/env python3
"""
Claims Firewall Linter for Governance OS.

Checks target Markdown files for undisclosed or misrepresented Ethana capability
claims against the canonical product model.

Hardening applied 2026-06-18 (see docs/architecture/claims-linter-hardening-review.md):
  C-01 Status prefix matching (replaces exact-match violation trigger).
  C-02 Section-scoped parsing (Sections 1-5 only) + most-restrictive-wins
       collision resolution.
  C-03 Ethana-specific context required for Edge/Sentry/Workspace hard rules.
  H-01 Word-boundary regex matching (replaces substring matching).
  H-02/H-03 Tightened has_status and has_workaround detection terms.
  L-02 Capability alias registry for common abbreviated references.
  M-04 Fenced code blocks excluded from linting.
"""
import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Only parse capability tables from Sections 1-5 of the canonical model.
# Sections 6-11 contain pricing, Cursory services, deployment models, historical
# files, and update triggers — not capability status tables. Parsing them
# produces spurious capability entries that pollute the detection dict.
_PARSEABLE_SECTION_RE = re.compile(r'^## Section [1-5]:')

# Status prefixes that require disclosure and/or workaround documentation.
# Uses prefix matching so qualifiers like "(pending confirmation)" or
# "— first connector, highest priority" are handled correctly.
_NON_PRODUCTION_PREFIXES = ("aspirational", "roadmap", "in build")

# Priority used for collision resolution when two canonical model rows produce
# the same base-name key. Lower number = more restrictive = retained.
_STATUS_PRIORITY_ORDER = [
    ("aspirational", 0),
    ("roadmap",      1),
    ("in build",     2),
]

# Capability aliases: short or abbreviated forms that map to the full canonical
# key. Injected into the capabilities dict after parsing so that abbreviated
# references (e.g., "NHI", "CI/CD gate") are checked against the correct status.
#
# Note: single-word aliases with no space and no hyphen (e.g., "nhi") are
# still skipped by the single-word guard in the general matching loop.
# These are included here for completeness and future hard-rule expansion.
CAPABILITY_ALIASES = {
    "nhi":                    "non-human identity (nhi) for agents",
    "non-human identity":     "non-human identity (nhi) for agents",
    "ci/cd gate":             "ci/cd red-teaming gate",
    "ethana eval gate":       "ci/cd red-teaming gate",
    "policy engine":          "governance policy engine",
}

# Single-word capabilities allowlist and denylist
SINGLE_WORD_ALLOWLIST = {"promptops", "finops", "evaluation", "guardrails", "mcp", "discovery", "nhi"}
SINGLE_WORD_DENYLIST = {"evaluation", "discovery", "guardrails"}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _status_priority(status_norm: str) -> int:
    """Return collision-resolution priority (lower = more restrictive)."""
    for prefix, priority in _STATUS_PRIORITY_ORDER:
        if status_norm.startswith(prefix):
            return priority
    return 3  # production or unrecognised — least restrictive


# ---------------------------------------------------------------------------
# Canonical model parsing
# ---------------------------------------------------------------------------

def parse_canonical_model(cpm_path: Path) -> dict:
    """
    Parse canonical-product-model.md to extract capability names and statuses.

    Scoped to Sections 1-5 only. When two rows produce the same base-name key
    the most restrictive status is retained (most-restrictive-wins collision
    resolution).
    """
    capabilities: dict = {}
    if not cpm_path.exists():
        print(f"Error: Canonical model not found at {cpm_path}", file=sys.stderr)
        return capabilities

    content = cpm_path.read_text(encoding="utf-8")
    in_parseable_section = False

    for raw_line in content.splitlines():
        line = raw_line.strip()

        # Section boundary: only h2 headers change scope.
        # h3 subsections (e.g., "### 1.1 Production Capabilities") stay within
        # the scope set by their parent h2.
        if line.startswith("## "):
            in_parseable_section = bool(_PARSEABLE_SECTION_RE.match(line))
            continue

        if not in_parseable_section:
            continue

        # Skip non-table lines and separator rows
        if not line.startswith("|"):
            continue
        if "|---|" in line or line.startswith("|---"):
            continue

        # Parse table row
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 2:
            continue

        # Skip header rows
        if parts[0].lower() in {
            "capability", "service", "certification", "model",
            "commercial name [pb]",
        }:
            continue

        # --- Name column: strip bold/backtick, split on em-dash only ---
        # Regular hyphens are part of compound names (e.g., "Per-user attribution")
        # and must not be used as split points.
        name_raw = parts[0].replace("**", "").replace("`", "")
        name_base = re.split(r"—", name_raw)[0].strip()
        if not name_base:
            continue

        # --- Status column: strip bold/backtick before normalising ---
        # The status column can contain bold emphasis, e.g.
        # "In Build — **first connector, highest priority**"
        status_raw = parts[1].replace("**", "").replace("`", "").strip()
        status_norm = status_raw.lower()

        # Normalise "In Progress" → "in build" (used for certifications).
        # Do NOT normalise "confirmed" → "production": "confirmed" appears as a
        # substring of "Aspirational (pending confirmation)" and would wrongly
        # promote Aspirational capabilities to Production, hiding violations.
        # Production capabilities in Sections 1-5 use the literal word "Production".
        if "in progress" in status_norm:
            status_norm = "in build"

        key = name_base.lower()
        if not key or not status_norm:
            continue

        # --- Collision resolution: most restrictive status wins ---
        # Prevents a later Production row (e.g., Section 4 FinOps project-level)
        # from overwriting an earlier In Build row (Section 1.2 FinOps full-granularity).
        if key in capabilities:
            existing_priority = _status_priority(capabilities[key]["status"])
            new_priority = _status_priority(status_norm)
            if new_priority >= existing_priority:
                # Existing entry is equal or more restrictive — keep it.
                continue

        capabilities[key] = {
            "original_name": name_base,
            "status": status_norm,
        }

    return capabilities


# ---------------------------------------------------------------------------
# Control-to-capability map loading
# ---------------------------------------------------------------------------

def load_control_capability_map(map_path: Path) -> dict:
    """
    Parse control-capability-map.md into a lookup dict.

    Returns:
        {control_name_lower: {"primary": "cpm-key-or-empty", "secondary": []}}

    Phase A: "secondary" is always [] regardless of column 4 content.
    Phase B: "secondary" will be populated from column 4.

    Returns {} if map_path does not exist (Risk 5: graceful degradation).
    Emits a warning to stderr if a primary key is not found in the CPM.
    """
    if not map_path.exists():
        print(f"Warning: control-capability-map not found at {map_path}", file=sys.stderr)
        return {}

    # Derive CPM path to validate primary keys at load time.
    cpm_path = map_path.parent / "canonical-product-model.md"
    cpm = parse_canonical_model(cpm_path) if cpm_path.exists() else {}

    result: dict = {}
    content = map_path.read_text(encoding="utf-8")

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        if "|---|" in line or line.startswith("|---"):
            continue

        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 4:
            continue

        # Skip header row
        if parts[0].lower() == "control name":
            continue

        key = parts[0].lower()
        primary = parts[2].lower()
        # Phase A: secondary is always [] — column 4 is read but not consumed.

        if not key:
            continue

        # Risk 2 mitigation: warn if primary key is not in the CPM.
        if primary and cpm and primary not in cpm:
            print(
                f"Warning: control-capability-map primary key '{primary}' for "
                f"'{parts[0]}' not found in canonical-product-model.md",
                file=sys.stderr,
            )

        result[key] = {"primary": primary, "secondary": []}

    return result


# ---------------------------------------------------------------------------
# Linting
# ---------------------------------------------------------------------------

def lint_file(target_path: Path, capabilities: dict) -> list:
    """
    Lint a target Markdown file for Claims Firewall violations.

    Three violation types:
      Firewall Breach      — non-production capability referred to as Production.
      Ambiguity Warning    — non-production capability mentioned without status
                             disclosure.
      Missing Workaround   — status disclosed but no bridge/workaround described.
    """
    if not target_path.exists():
        print(f"Error: Target file not found at {target_path}", file=sys.stderr)
        sys.exit(2)

    content = target_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    violations = []

    # -----------------------------------------------------------------------
    # Hard rules — require Ethana-specific context to avoid false positives
    # on third-party tools (Sentry.io, Microsoft Edge, GitHub workspaces, etc.)
    # -----------------------------------------------------------------------

    # Workspace: bare "workspace" matches GitHub, Azure DevOps, JIRA, etc.
    # Require "Ethana Workspace" or "governed (AI) workspace" pattern.
    workspace_re = re.compile(
        r"ethana\s+workspace|governed\s+(ai\s+)?workspace",
        re.IGNORECASE,
    )

    # Edge/Sentry: bare "edge|sentry" matches Microsoft Edge, Sentry.io,
    # Cloudflare Edge, network edge, etc. Require "Ethana Edge/Sentry" or
    # explicit Ethana component terminology.
    edge_re = re.compile(
        r"ethana\s+(edge|sentry)"
        r"|(?<!\w)(edge|sentry)\s+(agent|discovery|ai\s+firewall|network\s+layer|endpoint)",
        re.IGNORECASE,
    )

    # Visual Agent Builder: specific enough phrase — no additional context guard.
    agent_builder_re = re.compile(r"visual agent builder", re.IGNORECASE)

    # -----------------------------------------------------------------------
    # Inject aliases and precompile word-boundary patterns
    # -----------------------------------------------------------------------

    # Inject alias entries that point to the same status data as their
    # canonical key, so abbreviated references get checked.
    for alias_key, canonical_key in CAPABILITY_ALIASES.items():
        if canonical_key in capabilities and alias_key not in capabilities:
            capabilities[alias_key] = capabilities[canonical_key]

    # Precompile word-boundary patterns.
    # Single-word keys (no space, no hyphen) are only matched if they are in the allowlist.
    # If they are in the denylist, they require Ethana-specific context to prevent false positives.
    cap_patterns: dict = {}
    for cap_key in capabilities:
        if " " not in cap_key and "-" not in cap_key:
            if cap_key not in SINGLE_WORD_ALLOWLIST:
                continue
            if cap_key in SINGLE_WORD_DENYLIST:
                cap_patterns[cap_key] = re.compile(
                    r"(?<![a-z0-9/])(ethana\s+" + re.escape(cap_key) +
                    r"|governed\s+" + re.escape(cap_key) +
                    r"|" + re.escape(cap_key) + r"\s+(connector|agent|engine|gate|tool|capability|platform|scanners|feature|systems?))(?![a-z0-9/])",
                    re.IGNORECASE
                )
            else:
                cap_patterns[cap_key] = re.compile(
                    r"(?<![a-z0-9/])" + re.escape(cap_key) + r"(?![a-z0-9/])"
                )
        else:
            cap_patterns[cap_key] = re.compile(
                r"(?<![a-z0-9/])" + re.escape(cap_key) + r"(?![a-z0-9/])"
            )

    # -----------------------------------------------------------------------
    # Line-by-line linting
    # -----------------------------------------------------------------------

    in_code_block = False

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()

        # Exclude fenced code blocks — code examples and comments should not
        # trigger capability violations.
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        line_lower = line.lower()

        # --- Hard rule: Ethana Workspace ---
        if workspace_re.search(line):
            if not (
                "aspirational" in line_lower
                or "roadmap" in line_lower
                or "n/a" in line_lower
            ):
                if any(
                    term in line_lower
                    for term in ["production", "ga", "shipped", "active"]
                ):
                    violations.append((
                        idx, line,
                        "Hard Rule Violation: Ethana Workspace is claimed as "
                        "Production or GA. It is Aspirational and has no "
                        "engineering codebase.",
                    ))

        # --- Hard rule: Ethana Edge / Sentry ---
        if edge_re.search(line) and "production" in line_lower:
            if not (
                "build gateway" in line_lower
                or "n/a" in line_lower
                or "roadmap" in line_lower
            ):
                violations.append((
                    idx, line,
                    "Hard Rule Violation: Ethana Edge or Sentry is claimed as "
                    "Production. Neither component is in production today.",
                ))

        # --- Hard rule: Visual Agent Builder ---
        if agent_builder_re.search(line) and not (
            "aspirational" in line_lower or "n/a" in line_lower
        ):
            if any(
                term in line_lower
                for term in ["production", "ga", "shipped", "roadmap", "in build"]
            ):
                violations.append((
                    idx, line,
                    "Hard Rule Violation: Visual Agent Builder is claimed as "
                    "Production, In Build, or Roadmap. It is Aspirational and "
                    "absent from engineering briefs.",
                ))

        # --- General capability matching ---
        for cap_key, pattern in cap_patterns.items():
            if not pattern.search(line_lower):
                continue

            cap_data = capabilities[cap_key]
            status_canonical = cap_data["status"]
            original_name = cap_data["original_name"]

            # Only check non-production capabilities (prefix match handles
            # qualifiers like "(pending confirmation)" and "— first connector…")
            if not any(
                status_canonical.startswith(p) for p in _NON_PRODUCTION_PREFIXES
            ):
                continue

            # Disclosure and workaround detection.
            # has_status: line explicitly states the capability is non-production.
            # has_workaround: line describes or references an alternative approach.
            #
            # "development" removed from has_status — too broad; matches
            #   "development bank", "software development", etc.
            # "service" removed from has_workaround — universally present in
            #   compliance documents; suppressed nearly all Missing Workaround
            #   violations regardless of whether a real workaround was described.
            has_status = any(
                term in line_lower
                for term in [
                    "roadmap", "aspirational", "in build",
                    "not yet available", "not yet in production",
                    "planned for", "in development",
                ]
            )
            has_workaround = any(
                term in line_lower
                for term in [
                    "workaround", "alternative", "manual", "cursory", "bridge",
                ]
            )

            if "production" in line_lower and not (
                "road map" in line_lower or "planned" in line_lower
            ):
                violations.append((
                    idx, line,
                    f"Firewall Breach: Non-production capability '{original_name}' "
                    f"(canonical status: {status_canonical.upper()}) "
                    f"is referred to as Production.",
                ))
            elif not has_status:
                violations.append((
                    idx, line,
                    f"Ambiguity Warning: Capability '{original_name}' is mentioned "
                    f"without explicit status declaration "
                    f"(should state {status_canonical.upper()}).",
                ))
            elif not has_workaround:
                violations.append((
                    idx, line,
                    f"Missing Workaround: Capability '{original_name}' is "
                    f"roadmap-blocked, but no manual/third-party or Cursory "
                    f"workaround is detailed.",
                ))

    return violations


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python claims_linter.py <path_to_draft_file.md>")
        sys.exit(1)

    target_path = Path(sys.argv[1])
    cpm_path = (
        Path(__file__).resolve().parents[2]
        / "knowledge" / "ethana" / "canonical-product-model.md"
    )

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
