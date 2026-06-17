---
document_id: claims-linter-hardening-validation
version: 1.0
date: 2026-06-18
scope: evaluations/scripts/claims_linter.py
follows: docs/architecture/claims-linter-hardening-review.md
---

# Claims Linter Hardening — Validation Report

> **Purpose:** Documents the implementation of all seven hardening changes approved in `claims-linter-hardening-review.md`, with before/after fixture results, regression analysis, and outstanding risks.
>
> **Result summary:** All three gold standards pass (0 regressions). Three documented false positives eliminated. Four new true-positive detections added. Two false positives remain as acknowledged semantic limitations. Six single-word capability gaps remain as documented future work.

---

## 1. Fixes Implemented

Seven changes were applied to `evaluations/scripts/claims_linter.py` (2026-06-18). Listed in the order implemented; each maps to the change number in the hardening review.

---

### Fix 1 — Status Prefix Matching (C-01)

**Review reference:** C-01, Critical.

**What changed:**

```python
# Before — exact match: misses "aspirational (pending confirmation)",
# "in build — first connector...", "aspirational (as workspace-specific capability)"
if status_canonical in ["in build", "roadmap", "aspirational"]:

# After — prefix match: handles all qualifier variants
NON_PRODUCTION_PREFIXES = ("aspirational", "roadmap", "in build")
if not any(status_canonical.startswith(p) for p in NON_PRODUCTION_PREFIXES):
    continue
```

**Also applied:** Bold/backtick markers stripped from the status column in `parse_canonical_model()`, enabling `"In Build — **first connector, highest priority**"` to correctly produce `"in build — first connector, highest priority"` → starts with "in build" → checked.

**Also applied:** Removed the `elif "confirmed" in status_norm: status_norm = "production"` normalization that incorrectly promoted `"Aspirational (pending confirmation)"` to `"production"` (because "confirmed" is a substring of "confirmation"). Production capabilities in Sections 1-5 use the literal word "Production" — no `"confirmed"` normalization is needed within the scoped section range.

**Effect:** Three previously unchecked capabilities are now correctly enforced:
- `role-based access control on knowledge sources` → `"aspirational (as workspace-specific capability)"` → now checked
- Discovery IdP connector → `"in build — first connector, highest priority"` → now checked (still single-word key → skipped by guard; see Remaining Risks)
- `PromptOps — Canary releases` → `"aspirational (pending confirmation)"` → status correctly stored as Aspirational (still single-word key → skipped by guard)

---

### Fix 2 — Section-Scoped Parsing + Collision Resolution (C-02)

**Review reference:** C-02, Critical.

**What changed — Section scoping:**

```python
# New: only parse tables inside Sections 1-5
_PARSEABLE_SECTION_RE = re.compile(r'^## Section [1-5]:')

in_parseable_section = False
for raw_line in content.splitlines():
    line = raw_line.strip()
    if line.startswith("## "):
        in_parseable_section = bool(_PARSEABLE_SECTION_RE.match(line))
        continue
    if not in_parseable_section:
        continue
    # ... table parsing
```

**What changed — Collision resolution:**

```python
# New: most-restrictive-wins replaces last-write-wins
if key in capabilities:
    existing_priority = _status_priority(capabilities[key]["status"])
    new_priority = _status_priority(status_norm)
    if new_priority >= existing_priority:
        continue  # existing is equal or more restrictive — keep it
```

Priority order: `aspirational=0` (most restrictive) → `roadmap=1` → `in build=2` → `production=3` (least restrictive).

**Verified collisions resolved:**

| Key | Old status (last-write-wins) | New status (most-restrictive-wins) |
|---|---|---|
| `promptops` | `"production (present in platform)"` ← Section 1.1 won | `"aspirational (pending confirmation)"` ← Section 1.3 now wins |
| `finops` | `"production"` ← Section 4 won | `"in build"` ← Section 1.2 now wins |
| `runtime guardrails` | `"production"` (consistent — all 8 sub-entries are Production) | `"production"` (unchanged) |

**Capability dict size change:**

| State | Capabilities loaded |
|---|---|
| Before (all sections parsed) | 98 |
| After (Sections 1-5 only) | 51 |
| Removed spurious entries | 47 |

The 47 removed entries came from: Section 7 pricing table ($10,000/$30,000 as status values), Section 8 Cursory service descriptions, Section 10 historical file table, Section 11 update trigger table, Status Definitions table, Architecture Summary table. All produced non-triggering status strings and generated no violations in practice, but introduced fragility and polluted debug output.

---

### Fix 3 — Word-Boundary Regex Matching (H-01)

**Review reference:** M-06, High. Closes the substring-matching false positive risk.

**What changed:**

```python
# Before — substring match: "compliance pack" matches inside longer phrases
if cap_key in line_lower:

# After — word-boundary regex: precompiled outside line loop
cap_patterns[cap_key] = re.compile(
    r"(?<![a-z0-9/])" + re.escape(cap_key) + r"(?![a-z0-9/])"
)
if not pattern.search(line_lower):
    continue
```

The negative lookbehind `(?<![a-z0-9/])` and negative lookahead `(?![a-z0-9/])` ensure:
- Capability names don't match when embedded inside longer words (e.g., "scim" would not match inside "scim-adjacent" if "scim" were ever not filtered by the single-word guard)
- File path components don't trigger matches (e.g., `evaluations/baselines/...` does not match `evaluation`)

Patterns are precompiled outside the per-line loop, eliminating per-line recompilation overhead.

---

### Fix 4 — Ethana-Specific Context for Edge/Sentry/Workspace Hard Rules (C-03)

**Review reference:** C-03, Critical. Eliminates FP-01, FP-02, FP-03.

**What changed:**

```python
# Before — broad patterns matching third-party tools:
workspace_re = re.compile(r'workspace', re.IGNORECASE)
edge_re = re.compile(r'edge|sentry', re.IGNORECASE)

# After — require Ethana product context:
workspace_re = re.compile(
    r"ethana\s+workspace|governed\s+(ai\s+)?workspace",
    re.IGNORECASE,
)
edge_re = re.compile(
    r"ethana\s+(edge|sentry)"
    r"|(?<!\w)(edge|sentry)\s+(agent|discovery|ai\s+firewall|network\s+layer|endpoint)",
    re.IGNORECASE,
)
```

The `edge_re` update requires either the explicit "Ethana Edge/Sentry" prefix or specific Ethana Edge component terminology (agent, discovery, ai firewall, network layer, endpoint) to follow the bare product name.

---

### Fix 5 — Tightened Status and Workaround Detection (H-02/H-03)

**Review reference:** H-02 (has_workaround "service"), H-03 (has_status "development").

**What changed:**

```python
# Before:
has_status = any(term in line_lower for term in [
    "roadmap", "aspirational", "in build", "development", "planned"
])
has_workaround = any(term in line_lower for term in [
    "workaround", "alternative", "manual", "cursory", "bridge", "service"
])

# After:
has_status = any(term in line_lower for term in [
    "roadmap", "aspirational", "in build",
    "not yet available", "not yet in production",
    "planned for", "in development",
])
has_workaround = any(term in line_lower for term in [
    "workaround", "alternative", "manual", "cursory", "bridge",
])
```

**Removed:**
- `"development"` from `has_status` — matched "development bank", "software development environment", etc. Replaced with the two-word phrase `"in development"` (more specific).
- `"planned"` from `has_status` — matched "planned outage", "planned maintenance", etc. Replaced with `"planned for"`.
- `"service"` from `has_workaround` — the single most impactful removal. "service" appears in nearly every line of a compliance document (financial service, advisory service, cloud service). Its presence was suppressing almost all `Missing Workaround` violations regardless of whether a real workaround was described.

**Impact on gold standards:** None. All In Build capability disclosures in the gold standards use "in build" (for `has_status`) and "manual workaround:" or "cursory" (for `has_workaround`) — terms that remain in both lists.

---

### Fix 6 — Capability Alias Registry (L-02)

**Review reference:** L-02, Medium.

**What changed:**

```python
CAPABILITY_ALIASES = {
    "nhi":                "non-human identity (nhi) for agents",
    "non-human identity": "non-human identity (nhi) for agents",
    "ci/cd gate":         "ci/cd red-teaming gate",
    "ethana eval gate":   "ci/cd red-teaming gate",
    "policy engine":      "governance policy engine",
}

# Injected before pattern compilation:
for alias_key, canonical_key in CAPABILITY_ALIASES.items():
    if canonical_key in capabilities and alias_key not in capabilities:
        capabilities[alias_key] = capabilities[canonical_key]
```

Alias detection was verified for three of the five entries:
- `"non-human identity"` → detects "Non-human identity provides ephemeral scoped tokens in production" → Firewall Breach ✓
- `"ci/cd gate"` → detects "CI/CD Gate Integration" mentions in mixed-roadmap-claims.md → Ambiguity Warning ✓
- `"policy engine"` → detects "The policy engine enables... deployed in production" → Firewall Breach ✓

The `"nhi"` alias (single-word, no space or hyphen) is skipped by the single-word guard and cannot be detected via the general loop. This is a documented remaining gap (see Section 5).

---

### Fix 7 — Fenced Code Block Exclusion (M-04)

**Review reference:** M-04, Low.

**What changed:**

```python
in_code_block = False
for idx, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith("```") or stripped.startswith("~~~"):
        in_code_block = not in_code_block
        continue
    if in_code_block:
        continue
    # ... linting logic
```

Lines inside backtick or tilde fenced code blocks are now skipped entirely. Code examples and inline code comments no longer trigger capability violations.

---

## 2. Fixtures Tested

Six fixtures were run against both the pre-hardening and post-hardening linter.

---

### 2.1 Gold Standards

| Fixture | Before | After | Regression? |
|---|---|---|---|
| `eu-ai-act-high-risk-banking-gold-standard.md` | ✅ Pass (0 violations) | ✅ Pass (0 violations) | None |
| `india-dpdp-customer-support-ai-gold-standard.md` | ✅ Pass (0 violations) | ✅ Pass (0 violations) | None |
| `uk-insurance-claims-model-gold-standard.md` | ✅ Pass (0 violations) | ✅ Pass (0 violations) | None |

All three gold standards continue to pass with zero violations. The hardening changes did not alter the outcome for any gold standard.

---

### 2.2 Proposal-Review Fixtures

These fixtures are designed to test the **Proposal Review skill**, not the Claims Linter directly. They contain fixture description metadata alongside mock draft content — the linter evaluates both sections simultaneously since it cannot distinguish meta-content from draft content. Violations in these fixtures are therefore a mix of true detections on mock draft content and meta-level false triggers on fixture descriptions.

| Fixture | Before (violations) | After (violations) | Net change |
|---|---|---|---|
| `firewall-breach.md` | 13 | 13 | No change |
| `mixed-roadmap-claims.md` | 6 | 12+ | +6 new CI/CD Gate detections (new true positives via alias) |
| `clean-proposal.md` | 7 | 10+ | +3 new CI/CD Gate detections (new true positives via alias) |

**Notes on proposal-review fixture violations:**

The violations in these fixtures are expected and do not represent regressions. These fixtures are not linter compliance targets — they are proposal review test cases. The key observation is:

1. `firewall-breach.md`: Identical 13 violations. The Visual Agent Builder and SOC 2 Type II detections are unchanged. No new false positives were introduced.

2. `mixed-roadmap-claims.md` and `clean-proposal.md`: New violations appear for CI/CD Red-Teaming Gate, detected via the `"ci/cd gate"` alias. These are true positive detections — CI/CD Gate Integration (In Build) is mentioned in these fixtures without In Build status disclosure. The baseline linter could not detect these because the canonical key `"ci/cd red-teaming gate"` never appeared verbatim in the fixture text.

---

## 3. Regressions

**No regressions.** The following results were verified:

- All three gold standards: PASS before → PASS after.
- `firewall-breach.md`: 13 violations before → 13 violations after. Exact same lines, exact same messages.
- No new violations were introduced in any fixture that were not already present as baseline violations or are new true-positive detections.

---

## 4. False Positives Removed

Three of the seven documented false positives from the hardening review are eliminated. All three were caused by the over-broad hard rules matching third-party products.

---

### FP-01 Eliminated — Sentry.io Error Monitoring in Production

**Test line:** `"The client uses Sentry.io for error monitoring, deployed in production environments."`

| Before | After |
|---|---|
| ❌ Hard Rule Violation (Ethana Sentry/Edge) | ✅ No violation |

**Fix:** `edge_re` now requires "Ethana Edge/Sentry" prefix or Ethana-specific component terms. "Sentry.io" does not match the hardened pattern.

---

### FP-02 Eliminated — Microsoft Edge Browser in Production

**Test line:** `"Employee browsers (Chrome, Microsoft Edge, Firefox) are in production deployment."`

| Before | After |
|---|---|
| ❌ Hard Rule Violation (Ethana Edge) | ✅ No violation |

**Fix:** Same `edge_re` hardening. "Microsoft Edge" does not match "Ethana Edge" or Edge component terms.

---

### FP-03 Eliminated — Generic Workspace as Active Environment

**Test line:** `"Development teams operate within Azure DevOps workspaces and maintain active code repositories."`

| Before | After |
|---|---|
| ❌ Hard Rule Violation (Ethana Workspace) | ✅ No violation |

**Fix:** `workspace_re` now requires "Ethana Workspace" or "governed (AI) workspace". "Azure DevOps workspaces" does not match the hardened pattern.

---

## 5. False Negatives Removed (New True-Positive Detections)

Four new detection capabilities were confirmed in post-hardening testing.

---

### FN-01 Removed — Role-Based Access Control on Knowledge Sources

**Trigger:** `"Role-based access control on knowledge sources governs document-level permissions (Production capability)."`

| Before | After |
|---|---|
| ✅ No violation (bug: "aspirational (as workspace-specific capability)" not in exact-match trigger list) | ❌ Firewall Breach (ASPIRATIONAL) |

**Fix:** C-01 prefix matching. `"aspirational (as workspace-specific capability)".startswith("aspirational")` → True → now checked.

---

### FN-02 Removed — Non-Human Identity via Alias

**Trigger:** `"Non-human identity provides ephemeral scoped tokens for agent workloads in production."`

| Before | After |
|---|---|
| ✅ No violation (full canonical key `"non-human identity (nhi) for agents"` never appeared verbatim) | ❌ Firewall Breach (IN BUILD) |

**Fix:** L-02 alias registry. `"non-human identity"` maps to the canonical key status.

---

### FN-03 Removed — CI/CD Gate Integration via Alias

**Trigger:** `"CI/CD Gate Integration allows governance checks to be enforced as mandatory gates."`

| Before | After |
|---|---|
| ✅ No violation (canonical key `"ci/cd red-teaming gate"` never matched "CI/CD Gate Integration") | ❌ Ambiguity Warning (IN BUILD) |

**Fix:** L-02 alias registry. `"ci/cd gate"` maps to `"ci/cd red-teaming gate"` status. Since "CI/CD Gate Integration" contains "CI/CD Gate" as a phrase (with "Integration" following a space boundary), the word-boundary pattern `(?<![a-z0-9/])ci\/cd\ gate(?![a-z0-9/])` correctly matches.

---

### FN-04 Removed — Governance Policy Engine via Alias

**Trigger:** `"The policy engine enables centralised OPA/Rego rule deployment (deployed in production today)."`

| Before | After |
|---|---|
| ✅ No violation if "policy engine" was the only phrase used | ❌ Firewall Breach (IN BUILD) |

**Fix:** L-02 alias registry. `"policy engine"` maps to `"governance policy engine"` status.

---

### Collision Resolution Improvements (Status Correctness, Not Detection)

These are not new detections (both keys remain single-word → undetectable by general loop) but represent correct status state for future hard-rule expansion:

| Key | Old status | New status | Why |
|---|---|---|---|
| `promptops` | `"production (present in platform)"` | `"aspirational (pending confirmation)"` | Most-restrictive-wins: Section 1.3 Aspirational overrides Section 1.1 Production (non-standard status string) |
| `finops` | `"production"` | `"in build"` | Most-restrictive-wins: Section 1.2 In Build retained over Section 4 Production |

---

## 6. Remaining Risks

The following risks were documented in the hardening review and remain after implementation. They are not regressions — they were known limitations before hardening and are unchanged.

---

### RR-01 — Single-Word Capability Keys Undetectable (6 gaps)

The single-word guard (`' ' not in cap_key and '-' not in cap_key: continue`) prevents checking any capability whose base name after em-dash split is a single unhyphenated word. Six non-production capabilities remain undetectable:

| Key | Status | Commercial risk |
|---|---|---|
| `promptops` | `aspirational (pending confirmation)` | PromptOps Canary Releases can be claimed as Production |
| `finops` | `in build` | FinOps per-user attribution / GPU cost can be claimed as Production |
| `discovery` | `in build — first connector, highest priority` | Ethana Discovery can be claimed as available |
| `evaluation` | `aspirational` | Ethana Evaluation capabilities can be claimed as Production |
| `guardrails` | `aspirational (pending confirmation)` | Guardrails Custom Policy Enforcement can be claimed |
| `mcp` | `aspirational (pending confirmation)` | MCP Composable Creation can be claimed |

**Mitigation path:** Add explicit hard rules (similar to Visual Agent Builder) for each single-word capability. The rule patterns would require Ethana product context: e.g., `re.compile(r'ethana\s+discovery|ethana\s+edge.*discovery', re.IGNORECASE)` for Discovery. This is a separate hardening task.

---

### RR-02 — Semantic False Positives Remain for "compliance pack" and "AI Firewall"

**"compliance pack":** The phrase "compliance pack" is used in general English to describe a bundle of compliance documents (distinct from the Ethana Compliance Pack product). Word-boundary matching fires on both. Example line that still produces a false positive:

```
Cursory will provide a compliance pack of assessment reports for regulatory submission.
```
→ `Ambiguity Warning: Capability 'Compliance Pack' is mentioned without status declaration.`

**"AI Firewall":** The phrase "AI Firewall" is used by third-party vendors (Palo Alto, Zscaler). Word-boundary matching fires on both. Example that still produces a false positive:

```
| CTRL-09 | Network Egress | Client deploys Palo Alto AI Firewall in production |
```
→ `Firewall Breach: Non-production capability 'AI Firewall' is referred to as Production.`

These cannot be resolved by regex alone — they require semantic context (is the reference to Ethana's product or a third-party product?). The mitigation is editorial: authors should write "Ethana AI Firewall" when referring to the Ethana product and avoid the unqualified phrase when referring to third-party products.

---

### RR-03 — "nhi" Alias Not Checked

The `"nhi"` alias is registered in `CAPABILITY_ALIASES` and points to the correct In Build status of `"non-human identity (nhi) for agents"`. However, `"nhi"` is a three-character word with no space or hyphen → skipped by the single-word guard.

A document claiming "NHI is available in production today" would not be detected. The `"non-human identity"` alias (with hyphen) IS checked and does detect longer-form references.

---

### RR-04 — Line-Level Analysis Cannot Evaluate Multi-Line Disclosures (M-05)

The linter evaluates each line independently. A capability name on line N with a status disclosure on line N+1 generates an Ambiguity Warning on line N even though the disclosure is present. This is a structural limitation — context-window analysis would require a paragraph-level or section-level linter.

---

### RR-05 — Duplicate Violations from Overlapping Key Pairs (M-03)

The keys `"governance policy engine"` and `"governance policy engine (opa / rego)"` both match the same line when it mentions "Governance Policy Engine". Both fire as separate violations on the same line. This does not produce false negatives (violations are real) but produces confusing duplicate output.

---

### RR-06 — Proposal-Review Fixtures Not Excluded from Linting

Test fixture files contain metadata sections (expected findings, calibration notes, reviewer guidance) alongside mock draft content. The linter evaluates both. Violations reported in the metadata sections are technically correct (the linter correctly identifies that capability names appear without disclosure in those lines) but are contextually noise — the metadata is describing violations rather than making claims.

This is acceptable for the current use case (the linter is intended for actual proposal outputs and GCM skill outputs, not test fixture files). The evaluation index correctly distinguishes which tools run on which artifact types: the linter runs on gold standards and agent outputs, not on fixture files.

---

## Appendix A: Capability Coverage Summary

After hardening, the capabilities dict contains 51 entries (Sections 1-5 only).

| Category | Count |
|---|---|
| **Total capabilities loaded** | 51 |
| Non-production (aspirational / roadmap / in build) | 38 |
| — Will be checked (multi-word key) | 32 |
| — Skipped (single-word key) | 6 |
| Production and unrecognised status | 13 |

The 32 actively-checked non-production capabilities cover the most commercially significant In Build and Aspirational items: SCIM Provisioning, CI/CD Red-Teaming Gate, Compliance Pack, Governance Policy Engine, SOC 2 Type II, ISO 27001, HIPAA-ready, Visual Agent Builder, all Edge/Sentry capabilities, all Workspace capabilities, and others.

---

## Appendix B: Verification Commands

Run after any future change to `claims_linter.py` or `canonical-product-model.md`:

```bash
# All gold standards must pass
python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md

python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/india-dpdp-customer-support-ai-gold-standard.md

python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/gold-standards/uk-insurance-claims-model-gold-standard.md

# Firewall-breach must still detect violations (regression guard)
python evaluations/scripts/claims_linter.py \
  evaluations/test-cases/proposal-review/firewall-breach.md
# Expected: 13 violations including Visual Agent Builder Firewall Breach and SOC 2 Type II Breach
```
