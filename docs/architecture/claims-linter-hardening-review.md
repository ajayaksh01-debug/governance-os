---
document_id: claims-linter-hardening-review
version: 1.0
date: 2026-06-18
scope: evaluations/scripts/claims_linter.py
authority: architecture review — no code changes in this document
---

# Claims Linter Architecture Review

> **Scope:** Audit of `evaluations/scripts/claims_linter.py` for false-positive and false-negative risk. This document does not modify any code. All findings are based on static analysis of the linter source and direct tracing of all 98 capability entries extracted from `knowledge/ethana/canonical-product-model.md`.

---

## 1. Current Risks

Risks are classified by severity: **Critical** (wrong security decision produced), **High** (frequent incorrect output), **Medium** (structural fragility or intermittent incorrect output), **Low** (edge case or cosmetic).

---

### 1.1 Critical Risks

#### C-01 — Non-Standard Status Strings Silently Bypass the Violation Trigger

The violation check in `lint_file()` uses an exact-match list:

```python
if status_canonical in ["in build", "roadmap", "aspirational"]:
```

The canonical model contains status column values that do not normalize to any of these four strings. The linter silently skips these capabilities — never checking whether they are correctly disclosed. The affected capabilities are:

| Canonical Model Row | Raw Status Column | Normalized Result | Trigger Match | Outcome |
|---|---|---|---|---|
| `PromptOps — Canary releases` | `Aspirational (pending confirmation)` | `aspirational (pending confirmation)` | No | **False negative — never checked** |
| `Guardrails — Custom policy enforcement` | `Aspirational (pending confirmation)` | `aspirational (pending confirmation)` | No | False negative — but also single-word key → skipped anyway |
| `MCP — Composable MCP creation` | `Aspirational (pending confirmation)` | `aspirational (pending confirmation)` | No | False negative — but also single-word key → skipped anyway |
| `Role-based access control on knowledge sources` | `Aspirational (as Workspace-specific capability)` | `aspirational (as workspace-specific capability)` | No | **False negative — never checked** |
| `Discovery — AI Inventory output` | `In Build (output of Discovery connectors)` | `in build (output of discovery connectors)` | No | False negative — but also single-word key → skipped anyway |

The PromptOps Canary Releases false negative is the most operationally significant: `PromptOps — Canary releases` (Aspirational) could be claimed as a current production capability in any document the linter processes, and the linter would report no violation. The `role-based access control on knowledge sources` row is multi-word (not skipped by the single-word guard) but still escapes detection due to the "(as Workspace-specific capability)" qualifier in the status string.

The root cause is that `parse_canonical_model()` does not strip text after status qualifiers, and the violation trigger list uses exact matching rather than prefix or contains logic:

```python
# Current — exact match only
if status_canonical in ["in build", "roadmap", "aspirational"]:

# Needed — prefix match
if any(status_canonical.startswith(s) for s in ["in build", "roadmap", "aspirational"]):
```

---

#### C-02 — Key Collision via Last-Write-Wins Dict

The parser stores capabilities as `capabilities[name_base.lower()] = {...}`. When two rows in the canonical model produce the same base name after em-dash splitting, the later row silently overwrites the earlier one. The collisions confirmed by tracing:

| Key | Earlier Entry (overwritten) | Later Entry (wins) | Impact |
|---|---|---|---|
| `promptops` | Section 1.1 — Production `(present in platform)` | Section 1.3 — `Aspirational (pending confirmation)` | Both produce non-standard status strings; neither triggers violations. False negative. |
| `finops` | Section 1.2 — `In Build` | Section 4 — `Production` | In Build entry permanently lost. FinOps full-granularity features (per-user attribution, GPU cost) can be claimed as Production. False negative. — but `finops` is single-word → also skipped by guard |
| `discovery` | Section 2.2 — `In Build — **first connector, highest priority**` | Later Discovery section — `In Build (output of Discovery connectors)` | Both In Build but with different qualifiers. Status-prefix check handles this; exact check does not. |

The collision on `finops` is the most dangerous in the current state of the codebase: if the single-word guard were ever removed (as part of a hardening effort that adds explicit handling for single-word capability names), the `finops` key would suddenly register as Production, creating a persistent false negative for In Build FinOps sub-features regardless of what a document claims.

The order-dependency also means that reorganising the canonical model file can silently change the linter's behavior for any colliding key, with no error or warning.

---

#### C-03 — Hard Rule Regexes Match Third-Party Products

The `edge_re` and `workspace_re` hard rules use broad patterns:

```python
workspace_re = re.compile(r'workspace', re.IGNORECASE)
edge_re = re.compile(r'edge|sentry', re.IGNORECASE)
```

These match third-party products and common English phrases, producing Hard Rule Violations for content that has nothing to do with Ethana. Documented trigger scenarios:

| Third-Party Reference | Hard Rule Triggered | Why It Fires |
|---|---|---|
| `Sentry.io for error monitoring (in production)` | Ethana Sentry Hard Rule | `edge_re` matches "sentry"; "production" in line |
| `Microsoft Edge browser deployed in production` | Ethana Edge Hard Rule | `edge_re` matches "edge"; "production" in line |
| `Cloudflare Edge (production WAF deployment)` | Ethana Edge Hard Rule | `edge_re` matches "edge"; "production" in line |
| `GitHub workspaces are actively used by developers` | Ethana Workspace Hard Rule | `workspace_re` matches; "active" in line |
| `Azure DevOps workspace is the active development environment` | Ethana Workspace Hard Rule | `workspace_re` matches; "active" in line |
| `review this document in your JIRA workspace` | Ethana Workspace Hard Rule | If any of "production"/"ga"/"shipped"/"active" also in the line |

The impact is severe for governance and regulatory documents, which routinely reference Sentry.io (widely-used application monitoring), Microsoft Edge (standard enterprise browser), and "workspace" as a generic term for any collaborative environment. A GCM output for a client that uses Sentry.io would incorrectly fail the Claims Firewall linter, blocking the approval gate.

Sentry.io is particularly problematic: it is a common production monitoring tool that will appear naturally in the Technology Stack sections of GCM outputs alongside Ethana capabilities.

---

### 1.2 High Risks

#### H-01 — Single-Word Skip Guard Introduces False Negatives for Real Capability Names

The current guard introduced to prevent "Per" and "Evaluation" false positives:

```python
if ' ' not in cap_key and '-' not in cap_key:
    continue
```

Correctly prevents false positives. However, it also prevents the linter from checking legitimate single-word Ethana capability names. The single-word capabilities in the canonical model:

| Key | Status | Commercial Significance |
|---|---|---|
| `promptops` | aspirational (pending confirmation) — non-triggering status | High — A/B testing referenced in regulated proposals |
| `finops` | production (overwritten — In Build sub-features lost) | High — per-user attribution and GPU cost are In Build |
| `discovery` | in build (non-triggering qualifier) | High — commonly referenced as "Ethana Discovery" |
| `evaluation` | aspirational | Medium — could be mispresented as Production |
| `guardrails` | aspirational (pending confirmation) — non-triggering | High — overlaps with the Production "Runtime Guardrails" |
| `mcp` | aspirational (pending confirmation) — non-triggering | Medium |

The skip guard is a necessary workaround for the current parsing design, but it silently creates a category of capabilities that can never be checked by the linter. All six of these represent meaningful commercial risks if claimed incorrectly.

---

#### H-02 — `has_workaround` Term "service" Is Universally Satisfying

```python
has_workaround = any(term in line_lower for term in ["workaround", "alternative", "manual", "cursory", "bridge", "service"])
```

"service" appears in almost every line of a regulatory, compliance, or governance document. Any sentence about a financial service, advisory service, professional service, or cloud service satisfies this check, regardless of whether a genuine workaround for the In Build capability has been described.

The `Missing Workaround` violation can only fire when `has_status` is True (capability disclosed as non-production) AND `has_workaround` is False AND `"production" in line_lower` is False. Because "service" satisfies `has_workaround`, this third violation category is effectively disabled in any real compliance document.

Example of false clearance:
```
SCIM Provisioning is In Build — this is a mandatory financial service requirement
```
`has_status` = True ("in build"), `has_workaround` = True ("service"). No Missing Workaround violation. No workaround is described — the client has no guidance on what to do while SCIM is not yet available.

---

#### H-03 — `has_status` Term "development" Is Too Broad

```python
has_status = any(term in line_lower for term in ["roadmap", "aspirational", "in build", "development", "planned"])
```

"development" satisfies the status disclosure requirement in numerous contexts that are not status disclosures:

- `"SCIM Provisioning is part of the development bank's integration stack"` → `has_status = True`. No Ambiguity Warning fires.
- `"The client's development environment requires SCIM Provisioning"` → `has_status = True`.
- `"SCIM Provisioning is used in the development of this architecture"` → `has_status = True`.

In each case the sentence is asserting the capability as available or required — not disclosing that it is In Build. The Ambiguity Warning is suppressed incorrectly.

---

### 1.3 Medium Risks

#### M-01 — Canonical Model Table Pollution (25+ Spurious Capability Entries)

The parser reads every table in the canonical model with no section scoping. Tables that are not capability status tables produce spurious entries:

| Table source | Representative spurious keys | Spurious status values |
|---|---|---|
| Section 7 — Pricing | `ethana edge`, `ethana workspace`, `ethana build`, `enterprise ai control plane bundle` | `$10,000`, `$30,000`, `$45,000` |
| Section 8 — Cursory Services | `ai readiness assessment`, `regulatory gap analysis`, `red teaming as a service`, `managed ethana ops` | Service description text (e.g., `"asset register mapping regulatory exposure..."`) |
| Section 10 — Historical Files | `capability-status.md`, `source-of-truth.md`, `ethana-status-reconciliation.md`, etc. | Historical file descriptions |
| Section 11 — Update Triggers | `edge endpoint agent shipped to production`, `soc 2 type ii certification obtained`, `iso 27001 certification obtained` | `"section 2.1 → production"`, `"section 5 → production"` |
| Status Definitions table | `production`, `in build`, `roadmap`, `aspirational` | The description text for each status |
| Architecture Summary table | `commercial name [pb]`, `ethana build (ai infrastructure & control)` | Architecture description text |

These spurious entries currently produce non-triggering status strings and do not cause false positives. However, they make the capabilities dict fragile:

1. The Section 11 key `soc 2 type ii certification obtained` has the value `"section 5 → production"`. If "production" appeared in a future table's description field, it could normalize to a triggering status.
2. The Cursory Services keys (`ai readiness assessment`, `regulatory gap analysis`, etc.) could match lines in GCM documents that legitimately reference Cursory service names as workarounds. These lines would then be evaluated against garbage status strings rather than the correct Production/In Build status.
3. The Architecture Summary key `ethana build (ai infrastructure & control)` → any document line containing this phrase is evaluated against the architecture description text as a status.

The correct fix is to scope parsing to specific sections of the canonical model (Sections 1–5 only) or to use a sentinel comment or section marker to delineate parseable from non-parseable content.

---

#### M-02 — Bold Markdown Not Stripped from Status Column

The parser strips bold markers from the name column but not from the status column:

```python
name_raw = parts[0].replace('**', '').replace('`', '')   # cleans name ✓
status = parts[1].strip()                                  # does NOT clean status ✗
```

The canonical model has one documented instance where bold markdown appears in a status column value:

```
| **Discovery — Identity Provider connector** (Okta, Entra, Workspace) | In Build — **first connector, highest priority** | ...
```

`parts[1]` = `In Build — **first connector, highest priority**`. After `status_norm = status.lower()`: `"in build — **first connector, highest priority**"`. This does not match "in build" exactly and does not start with "in build" (for a startswith check). The Discovery IdP connector is silently not checked.

This is currently a single confirmed instance. Any future canonical model update that uses bold emphasis in a status column would create additional silent exclusions.

---

#### M-03 — Duplicate Violation Reports from Key Overlap

The canonical model contains pairs of keys where the longer key is a superset of the shorter key:

| Shorter key | Longer key | Both checked independently |
|---|---|---|
| `governance policy engine` | `governance policy engine (opa / rego)` | Yes — a line mentioning "Governance Policy Engine" triggers both |
| `runtime guardrails` | `guardrails engine (all six production scanners)` | Yes — a line mentioning "runtime guardrails" could match both |
| `mcp security broker` | (no longer key from current canonical model) | N/A |

When a document line mentions "Governance Policy Engine (OPA/Rego) — currently In Build", both keys fire:
1. `governance policy engine` → In Build → checks `has_status`, `has_workaround` → reports
2. `governance policy engine (opa / rego)` → In Build → same checks → reports again

The user sees the same capability violation reported twice on the same line. This is not a false positive (both reports are correct) but produces confusing output and inflates violation counts.

---

#### M-04 — Code Block Content Is Evaluated

Lines inside Markdown fenced code blocks (` ``` ` or ` ~~~ `) are evaluated as regular content. A code example containing an In Build capability name will generate violations even if the example is illustrating correct usage:

```python
# Configure SCIM provisioning endpoint (In Build — roadmap only)
scim_endpoint = config.SCIM_PROVISIONING_URL
```

Line 2 would be evaluated: `'scim provisioning' in 'scim_endpoint = config.scim_provisioning_url'`? No, that doesn't contain "scim provisioning" as a phrase. But:

```python
# SCIM Provisioning integration — In Build, not available for production use
```

This line correctly discloses In Build status (`has_status` = True) and would be evaluated. The linter would not report a violation here (correct — the disclosure is present). But a code comment like `# SCIM Provisioning: enabled = True` would trigger an Ambiguity Warning for a line that is a code comment, not a customer claim.

---

#### M-05 — Line-Level Analysis Cannot Evaluate Multi-Line Disclosures

All checks are per-line. A disclosure that spans two lines satisfies nothing:

```
SCIM Provisioning automates user lifecycle management and vendor offboarding.
This capability is currently In Build and not yet available for deployment.
```

Line 1: `'scim provisioning' in line_lower` → True → In Build → `has_status`: no "roadmap"/"in build"/etc. in line 1 → Ambiguity Warning fires.
Line 2: `'scim provisioning' in line_lower` → False → not checked.

The Ambiguity Warning fires on line 1 even though the disclosure appears two lines later. This will generate false positives in any well-written document that introduces a capability on one line and discloses its status in a follow-up sentence.

---

#### M-06 — Substring Match Without Word Boundary

`if cap_key in line_lower` is a substring check with no word-boundary enforcement. For most multi-word capability names this is safe (the phrases are specific enough). Documented edge cases where substring matching causes over-broad matches:

| Capability key | Over-broad match scenario |
|---|---|
| `compliance pack` | `"This assessment delivers a full compliance pack of documentation"` — "compliance pack" used as a generic English phrase, not the Ethana Compliance Pack product |
| `ai firewall` | `"Client uses Zscaler's AI Firewall capability in production"` — third-party AI Firewall, not Ethana's |
| `governance policy engine` | `"The organization's governance policy engine drives risk decisions"` — generic governance language |
| `cost and budget tracking` | `"Cost and budget tracking is a core FinOps discipline"` — generic phrase |
| `red teaming orchestrator` | Unlikely false positive — phrase is specific enough |

Word-boundary matching (`\b` anchors) would prevent most of these. "compliance pack" as a generic phrase would not occur with the exact capitalisation and spacing if the author is writing about a document package rather than the Ethana product — though this is not a reliable distinction.

---

#### M-07 — Violation Check Cannot Distinguish Product References from General Usage

Even with correct word-boundary matching, the linter cannot distinguish:

```
The Compliance Pack (In Build — see roadmap section) will automate evidence export.
```
from:
```
We provide a compliance pack of advisory deliverables for this engagement.
```

Both contain "compliance pack" followed by status-related context. The first is a correct Ethana product disclosure. The second is about a Cursory deliverable bundle. The linter would report the second line as a Missing Workaround warning (status is present via unrelated "roadmap", but the line is not about the Ethana product).

This is a fundamental semantic limitation of keyword-based linting. It cannot be solved with regex alone.

---

### 1.4 Low Risks

#### L-01 — Incomplete Header Row Detection

The parser skips rows where `parts[0].lower() in ["capability", "service", "certification", "model"]`. The Section 7 Pricing table header is `"Product / Bundle | Annual License | ..."` — `parts[0] = "Product / Bundle"` — not in the skip list. The header row is parsed as a capability with status "Annual License". Because "Annual License" is not in the violation trigger list, no violations fire. However, key `product / bundle` → status `annual license` is stored in the dict and could cause confusing debug output.

The Section 7 data rows (`| Ethana Edge | $10,000 | ...`) also pass the header check and produce keys `ethana edge` → `$10,000` (overwriting any earlier `ethana edge` entry, if one existed). Currently no earlier `ethana edge` entry with a meaningful status exists, so this is benign.

---

#### L-02 — Capability Alias References Not Checked

Several In Build and Aspirational capabilities are commonly referenced by short names, acronyms, or abbreviated forms that do not appear in the canonical model as registered keys:

| Full canonical key | Common alias | Alias checked? |
|---|---|---|
| `non-human identity (nhi) for agents` | `NHI`, `non-human identity` | No |
| `scim provisioning` | `SCIM` | No — but full phrase "SCIM provisioning" is checked |
| `ci/cd red-teaming gate` | `CI/CD gate`, `ethana eval gate` | Partial — only exact match on `ci/cd red-teaming gate` |
| `governance policy engine` | `OPA/Rego engine`, `policy engine` | No |

A document claiming "NHI provides ephemeral scoped tokens in production today" would not be caught because the capability key `non-human identity (nhi) for agents` requires the exact phrase including the parenthetical.

---

## 2. False Positive Examples

False positives are cases where the linter reports a violation on content that is correct or irrelevant to Ethana capability claims.

---

### FP-01 — Sentry.io Error Monitoring in Production

**Context:** GCM output for a client whose technology stack includes Sentry.io.

**Line:**
```
| CTRL-05 | Operational Monitoring | Sentry.io (error monitoring, production-deployed) | Third-Party |
```

**What fires:** `edge_re = re.compile(r'edge|sentry', re.IGNORECASE)` matches "Sentry.io". "production" is in the line. None of the exclusion terms ("build gateway", "n/a", "roadmap") are present.

**Violation reported:** `Hard Rule Violation: Ethana Edge or Sentry is claimed as Production. Neither component is in production today.`

**Correct interpretation:** The line references Sentry.io, the widely-used third-party application monitoring platform. Ethana's engineering component "Sentry" (the discovery/AI firewall network layer) is a different product with the same name. The violation is a false positive.

**Frequency:** High. Sentry.io is deployed in the production stacks of a significant proportion of technology companies. Any GCM output that describes a client's existing monitoring stack will likely include Sentry.io.

---

### FP-02 — Microsoft Edge Browser

**Context:** GCM output for a bank documenting browser monitoring controls.

**Line:**
```
Employee browsers (Chrome, Microsoft Edge, Firefox) are in production deployment across 12,000 endpoints.
```

**What fires:** `edge_re` matches "Edge". "production" in line. No exclusion terms.

**Violation reported:** `Hard Rule Violation: Ethana Edge or Sentry is claimed as Production.`

**Correct interpretation:** Microsoft Edge browser. Unrelated to Ethana Edge (endpoint AI monitoring agent).

---

### FP-03 — GitHub or Azure Workspace as Active Environment

**Context:** Regulatory mapping or GCM output describing client infrastructure.

**Line:**
```
Development teams operate within Azure DevOps workspaces and maintain active code repositories.
```

**What fires:** `workspace_re` matches "workspaces". "active" in line. "aspirational"/"roadmap"/"n/a" not in line.

**Violation reported:** `Hard Rule Violation: Ethana Workspace is claimed as Production or GA.`

**Correct interpretation:** Azure DevOps workspaces. Unrelated to Ethana Workspace (governed enterprise chat, Aspirational).

---

### FP-04 — "Compliance Pack" as Generic English Phrase

**Context:** GCM output Section 9 describing Cursory deliverables.

**Line:**
```
Cursory will provide a compliance pack of assessment reports and control evidence for regulatory submission.
```

**What fires:** `compliance pack` key → In Build status. `has_status` = False (no "in build"/"roadmap" etc. in line). Ambiguity Warning fires.

**Violation reported:** `Ambiguity Warning: Capability 'Compliance Pack' is mentioned without explicit status declaration (should state IN BUILD).`

**Correct interpretation:** "Compliance pack" is being used as a generic English description of a bundle of compliance deliverables (a Cursory advisory output), not as a reference to the Ethana Compliance Pack platform feature.

---

### FP-05 — Third-Party AI Firewall in Client's Existing Stack

**Context:** GCM Control Requirements table referencing existing customer controls.

**Line:**
```
| CTRL-09 | Network Egress Control | Client deploys Palo Alto AI Firewall in production for SaaS traffic |
```

**What fires:** `ai firewall` key → In Build status. "production" in line → Firewall Breach.

**Violation reported:** `Firewall Breach: Non-production capability 'AI Firewall' (canonical status: IN BUILD) is referred to as Production.`

**Correct interpretation:** Palo Alto Networks AI Firewall, a competing/complementary product. Not Ethana AI Firewall. The client's existing production security stack is being documented, not Ethana capabilities.

---

### FP-06 — Ambiguity Warning on Fixture Description Fields

**Context:** The linter is run on a test fixture file (e.g., `firewall-breach.md`).

**Line (YAML frontmatter description field):**
```
description: > UK insurance pitch deck containing three Critical Firewall Breaches: an Aspirational
  capability (Visual Agent Builder) presented as Production...
```

**What fires:** `agent_builder_re` matches "Visual Agent Builder". "aspirational" is NOT in this line (it is on the next line after `>` YAML block scalar). "production" IS in the line.

**Violation reported:** `Hard Rule Violation: Visual Agent Builder is claimed as Production, In Build, or Roadmap.`

**Correct interpretation:** This is a fixture description explaining that a violation exists in the test content. The linter is flagging the fixture's own description of the violation, not the violation itself. The linter should not be run on fixture files that describe expected violation scenarios — or fixture description fields should be excluded.

---

### FP-07 — "Development" Satisfying has_status Incorrectly

**Context:** GCM Section 6 compliance text.

**Line:**
```
SCIM Provisioning is aligned to the development bank sector's identity management standards.
```

**What should fire:** Ambiguity Warning — "SCIM Provisioning" mentioned without In Build status disclosure.

**What actually fires:** Nothing. `has_status` = True because "development" is in the line. The linter considers the disclosure requirement satisfied.

**Correct interpretation:** "Development bank" is a type of financial institution (e.g., development finance institution), not a disclosure that SCIM Provisioning is In Build. The false clearance suppresses a legitimate warning.

*(Note: this is a false negative induced by the false-positive-suppression logic, catalogued here because it manifests as the linter granting an incorrect pass.)*

---

## 3. False Negative Examples

False negatives are cases where the linter reports no violation on content that contains a real Claims Firewall problem.

---

### FN-01 — PromptOps Canary Releases Claimed as Production

**Context:** Proposal section listing current platform capabilities.

**Line:**
```
PromptOps includes canary releases for staged AI model rollout (available in production today).
```

**Why not caught:** `promptops` is a single-word key (no space, no hyphen) → skipped by the single-word guard. The Canary Releases Aspirational capability (`PromptOps — Canary releases`) produces key `promptops` which is never checked.

**Canonical status:** Aspirational (pending confirmation). This should be a Hard Rule Violation.

---

### FN-02 — FinOps Per-User Attribution and GPU Cost Tracking Claimed as Production

**Context:** FinOps section of a proposal.

**Line:**
```
Ethana's FinOps dashboard provides per-user token attribution and GPU cost tracking across all teams (Production).
```

**Why not caught:** `finops` is a single-word key → skipped. `cost and budget tracking` (the Section 1.1 Production entry) would not match this specific phrase about per-user attribution and GPU cost. The In Build FinOps sub-capabilities (`FinOps — full granularity`) never have their status checked because `finops` is always skipped.

**Canonical status of claimed features:** In Build.

---

### FN-03 — Ethana Discovery Claimed as Available Today

**Context:** RFP response section on shadow AI inventory.

**Line:**
```
Ethana Discovery provides a real-time shadow AI inventory report within 48 hours of deployment.
```

**Why not caught:** `discovery` is a single-word key → skipped. No other key matches "Ethana Discovery" specifically.

**Canonical status:** In Build (all Discovery connectors). This is a direct claim of In Build as Production.

---

### FN-04 — NHI Referenced by Abbreviation

**Context:** Agent identity section of a technical proposal.

**Line:**
```
NHI (Non-Human Identity) provides ephemeral scoped tokens for agent workloads in production.
```

**Why not caught:** The canonical key is `non-human identity (nhi) for agents`. This exact phrase (including the parenthetical "(nhi)" and "for agents") is not present in the line. The line says "NHI (Non-Human Identity)" — the abbreviation comes first. `'non-human identity (nhi) for agents' in 'nhi (non-human identity) provides ephemeral...'` → False.

**Canonical status:** In Build. The claim "in production" is a direct False Negative.

---

### FN-05 — SCIM Provisioning Cleared by "service" in has_workaround

**Context:** Current capabilities section.

**Line:**
```
SCIM Provisioning — In Build — enables automated user lifecycle management. This is a financial service feature available in Q4 2026.
```

**What happens:** `'scim provisioning' in line_lower` → True → In Build → `has_status`: "in build" in line → True → `has_workaround`: "service" in line → True. No violation.

**Correct interpretation:** The line correctly discloses In Build status (`has_status` passed correctly). But the "workaround" check is satisfied by "financial service" — not by any actual manual workaround or Cursory bridge service described. The `Missing Workaround` violation that should fire is suppressed. The client has no guidance on how to handle the capability gap today.

---

### FN-06 — PromptOps and FinOps Status Never Registered (Non-Standard Status Strings)

**Context:** Any document mentioning PromptOps.

**Background:** Even if the single-word guard were removed, `promptops` → status `"aspirational (pending confirmation)"`. This string is NOT in `["in build", "roadmap", "aspirational"]`. The violation trigger would not fire. The capability would be evaluated as if it had no status — no violation reported.

**Canonical status:** Aspirational (Canary Releases sub-capability). A claim of PromptOps Canary Releases as Production would produce zero violations regardless of the single-word guard.

---

### FN-07 — Role-Based Access Control on Knowledge Sources (Aspirational Qualifier in Status)

**Context:** Proposal claiming Workspace-specific RBAC as Production.

**Line:**
```
Role-based access control on knowledge sources governs which departments can access which document collections (Production capability).
```

**Why not caught:** Key `role-based access control on knowledge sources` → status `"aspirational (as workspace-specific capability)"`. This is a multi-word key (not skipped by guard) with a status string that starts with "aspirational" but does not exactly equal "aspirational". The violation trigger fails: `"aspirational (as workspace-specific capability)" in ["in build", "roadmap", "aspirational"]` → False.

**Canonical status:** Aspirational. Production claim should be a Firewall Breach.

---

### FN-08 — In Build Capability Status Not Enforced for In-Build-With-Qualifier Status Strings

**Context:** Any document mentioning the Discovery IdP Connector.

**Line:**
```
Discovery IdP Connector (Okta, Entra) provides real-time identity mapping (Production, available for deployment).
```

**Why not caught:** `discovery — identity provider connector` (full key from canonical model) → after em-dash split → key `discovery` → single-word → skipped. Even without the skip guard: the first Discovery entry processed had raw status `"In Build — **first connector, highest priority**"` → `status_norm = "in build — **first connector, highest priority**"` → not in trigger list → not checked. Bold markers in the status string compound the issue.

---

## 4. Recommended Matching Strategy

### 4.1 Replace `if cap_key in line_lower` with Word-Boundary Matching

The current substring check should be replaced with a word-boundary regex for all multi-word checks:

```python
# Current (substring — no boundary enforcement):
if cap_key in line_lower:

# Recommended (word-boundary match):
import re
cap_pattern = re.compile(r'(?<![a-z0-9/])' + re.escape(cap_key) + r'(?![a-z0-9/])')
if cap_pattern.search(line_lower):
```

The lookahead and lookbehind (`(?<![a-z0-9/])` / `(?![a-z0-9/])`) prevent matches where the capability name is embedded in a larger word or path (e.g., "non-compliancepack" would not match "compliance pack" because "compliance" is not at a word boundary in that context). The `/` exclusion prevents path components (e.g., `evaluations/baselines/...`) from matching capability names.

Precompile all patterns outside the per-line loop to avoid recompilation on every line:

```python
cap_patterns = {
    key: re.compile(r'(?<![a-z0-9/])' + re.escape(key) + r'(?![a-z0-9/])')
    for key, data in capabilities.items()
    if ' ' in key or '-' in key  # respect the existing skip guard
}
```

### 4.2 Replace Exact Status Match with Prefix Match

```python
# Current (exact match — misses "aspirational (pending confirmation)", "in build — *"):
if status_canonical in ["in build", "roadmap", "aspirational"]:

# Recommended (prefix match):
NON_PRODUCTION_PREFIXES = ("in build", "roadmap", "aspirational")
if any(status_canonical.startswith(p) for p in NON_PRODUCTION_PREFIXES):
```

This correctly handles:
- `"aspirational (pending confirmation)"` → startswith "aspirational" → True ✓
- `"aspirational (as workspace-specific capability)"` → startswith "aspirational" → True ✓
- `"in build — **first connector, highest priority**"` → startswith "in build" → True ✓
- `"in build (output of discovery connectors)"` → startswith "in build" → True ✓

Pair with bold-marker stripping on the status column (see Section 5).

### 4.3 Strip Bold Markdown from Status Column

```python
status = parts[1].replace('**', '').replace('`', '').strip()
```

Apply the same cleaning to `parts[1]` that is currently applied to `parts[0]`. This ensures "In Build — **first connector, highest priority**" becomes "In Build — first connector, highest priority" before normalization.

### 4.4 Tighten has_status and has_workaround

Remove over-broad terms:

```python
# Current:
has_status = any(term in line_lower for term in ["roadmap", "aspirational", "in build", "development", "planned"])
has_workaround = any(term in line_lower for term in ["workaround", "alternative", "manual", "cursory", "bridge", "service"])

# Recommended:
has_status = any(term in line_lower for term in ["roadmap", "aspirational", "in build", "not yet available", "not yet in production", "planned for"])
has_workaround = any(term in line_lower for term in ["workaround", "manual workaround", "cursory", "bridge service", "alternative:", "advisory service"])
```

Removing "development" from `has_status` and "service" from `has_workaround` is the minimum viable change. The narrower replacements reduce false clearance while still matching well-formed disclosures in Cursory documents.

### 4.5 Harden Hard Rules with Ethana-Specific Context

Require Ethana product context before firing hard rules for Edge, Sentry, and Workspace:

```python
# Current — matches any reference:
edge_re = re.compile(r'edge|sentry', re.IGNORECASE)

# Recommended — require Ethana product context or product-specific terms:
ethana_edge_re = re.compile(r'ethana\s+edge|ethana\s+sentry|endpoint\s+agent.*production|sentry.*ai\s+firewall', re.IGNORECASE)
ethana_workspace_re = re.compile(r'ethana\s+workspace|governed\s+(ai\s+)?workspace', re.IGNORECASE)
```

This prevents matches on "Sentry.io", "Microsoft Edge", "GitHub workspace", and "Azure DevOps workspace" while still catching explicit Ethana product name claims.

For the Workspace rule, an alternative is to require the exact phrase "Ethana Workspace" rather than the bare word "workspace" — Ethana's own documents consistently use the full product name.

### 4.6 Scope Canonical Model Parsing to Capability Tables Only

Add section markers to restrict parsing to Sections 1–5 (capability sections). Ignore Sections 6–11 (deployment models, pricing, certifications management, Cursory services, historical files, update triggers). This eliminates ~25 spurious entries:

```python
PARSEABLE_SECTIONS = {"## Section 1:", "## Section 2:", "## Section 3:", "## Section 4:", "## Section 5:"}
in_parseable_section = False

for line in lines:
    if any(line.strip().startswith(s) for s in PARSEABLE_SECTIONS):
        in_parseable_section = True
    elif line.strip().startswith("## Section") or line.strip().startswith("## Licensing"):
        in_parseable_section = False
    
    if not in_parseable_section:
        continue
    # ... existing parsing logic
```

### 4.7 Register Explicit Aliases for Critical Abbreviated References

Add an alias map that supplements the capability dict with short-form references:

```python
CAPABILITY_ALIASES = {
    "nhi": "non-human identity (nhi) for agents",
    "non-human identity": "non-human identity (nhi) for agents",
    "ci/cd gate": "ci/cd red-teaming gate",
    "ethana eval": "ci/cd red-teaming gate",
    "policy engine": "governance policy engine",
    "scim": "scim provisioning",
}
```

During the lint loop, check aliases first with word-boundary matching, then map to the canonical key's status for violation evaluation.

---

## 5. Required Code Changes

Listed in priority order. Each change is described precisely enough to implement without ambiguity.

---

### Change 1 — Fix Violation Trigger to Use Prefix Matching (Critical — closes C-01, FN-06, FN-07)

**File:** `evaluations/scripts/claims_linter.py`  
**Location:** `lint_file()`, line 101

Replace:
```python
if status_canonical in ["in build", "roadmap", "aspirational"]:
```

With:
```python
NON_PRODUCTION_PREFIXES = ("in build", "roadmap", "aspirational")
if any(status_canonical.startswith(p) for p in NON_PRODUCTION_PREFIXES):
```

**Dependent change:** Also strip bold markers from the status column in `parse_canonical_model()`:
```python
# In parse_canonical_model(), after: status = parts[1].strip()
# Add:
status = status.replace('**', '').replace('`', '').strip()
```

**Impact:** PromptOps Canary Releases, Guardrails Custom Policy Enforcement, MCP Composable Creation, and Role-Based Access Control on Knowledge Sources will now register as Aspirational and be subject to violation checks. Discovery IdP connector will register as In Build.

---

### Change 2 — Scope Canonical Model Parsing to Sections 1–5 (Critical — closes M-01)

**File:** `evaluations/scripts/claims_linter.py`  
**Location:** `parse_canonical_model()`, the main parsing loop

Before entering the table-parsing loop, add section tracking to skip rows from Sections 6–11. When a line matches `^## Section [6-9]:|^## Licensing|^## Pricing|^## Section 1[0-1]:`, set `in_parseable_section = False`. When a line matches `^## Section [1-5]:`, set it to True.

Eliminates all 25+ spurious entries including pricing rows, Cursory service descriptions, Section 11 update triggers, and historical file table entries.

---

### Change 3 — Replace `if cap_key in line_lower` with Word-Boundary Matching (High — closes M-06, and reduces FP-04, FP-05)

**File:** `evaluations/scripts/claims_linter.py`  
**Location:** `lint_file()`, the general capability matching loop, line 96

Precompile patterns before the line loop:
```python
import re

# Precompile once before iterating lines
cap_patterns = {}
for cap_key, cap_data in capabilities.items():
    if ' ' not in cap_key and '-' not in cap_key:
        continue
    cap_patterns[cap_key] = re.compile(
        r'(?<![a-z0-9/])' + re.escape(cap_key) + r'(?![a-z0-9/])'
    )
```

Replace the inner match check:
```python
# Replace:
if cap_key in line_lower:
# With:
if cap_patterns[cap_key].search(line_lower):
```

---

### Change 4 — Harden Hard Rules with Ethana-Specific Context (Critical — closes C-03, FP-01, FP-02, FP-03)

**File:** `evaluations/scripts/claims_linter.py`  
**Location:** `lint_file()`, lines 67–69

Replace:
```python
workspace_re = re.compile(r'workspace', re.IGNORECASE)
edge_re = re.compile(r'edge|sentry', re.IGNORECASE)
```

With:
```python
workspace_re = re.compile(r'ethana\s+workspace|governed\s+(ai\s+)?workspace', re.IGNORECASE)
edge_re = re.compile(r'ethana\s+(edge|sentry)|(?<!\w)(edge|sentry)\s+(agent|discovery|firewall|network\s+layer)', re.IGNORECASE)
```

Also update the Edge hard rule condition to require "ethana" or explicit product context:
```python
# Current:
if edge_re.search(line) and "production" in line_lower:
    if not ("build gateway" in line_lower or "n/a" in line_lower or "roadmap" in line_lower):
# Recommended (no functional change needed after regex tightening — the regex itself now requires product context):
if edge_re.search(line) and "production" in line_lower:
    ...
```

---

### Change 5 — Tighten has_status and has_workaround (High — closes H-02, H-03, FN-05, FP-07)

**File:** `evaluations/scripts/claims_linter.py`  
**Location:** `lint_file()`, lines 103–105

Replace:
```python
has_status = any(term in line_lower for term in ["roadmap", "aspirational", "in build", "development", "planned"])
has_workaround = any(term in line_lower for term in ["workaround", "alternative", "manual", "cursory", "bridge", "service"])
```

With:
```python
has_status = any(term in line_lower for term in [
    "roadmap", "aspirational", "in build", "not yet available",
    "not yet in production", "planned for", "in development"
])
has_workaround = any(term in line_lower for term in [
    "workaround", "manual workaround", "cursory",
    "bridge service", "manual alternative", "advisory"
])
```

The change removes "development" (too broad) and "service" (universal match). It adds "in development" (two-word phrase, more specific) and tightens "alternative" to "manual alternative" to prevent generic alternative-provider references from satisfying the workaround requirement.

---

### Change 6 — Register Capability Aliases (Medium — closes L-02, FN-04)

**File:** `evaluations/scripts/claims_linter.py`  
**Location:** Top of `lint_file()`, before the line loop

Add an alias expansion step after loading capabilities:
```python
CAPABILITY_ALIASES = {
    "nhi": "non-human identity (nhi) for agents",
    "non-human identity": "non-human identity (nhi) for agents",
    "ci/cd gate": "ci/cd red-teaming gate",
    "ethana eval gate": "ci/cd red-teaming gate",
    "policy engine": "governance policy engine",
}

# Inject aliases into capabilities dict
for alias_key, canonical_key in CAPABILITY_ALIASES.items():
    if canonical_key in capabilities:
        capabilities[alias_key] = capabilities[canonical_key]
```

---

### Change 7 — Exclude Code Block Content from Linting (Low — closes M-04)

**File:** `evaluations/scripts/claims_linter.py`  
**Location:** `lint_file()`, main line loop

Add a code block tracker:
```python
in_code_block = False
for idx, line in enumerate(lines, 1):
    if line.strip().startswith('```') or line.strip().startswith('~~~'):
        in_code_block = not in_code_block
        continue
    if in_code_block:
        continue
    # ... existing linting logic
```

---

## 6. Impact on Existing Test Fixtures

The following test fixtures are subject to the claims linter in the current evaluation suite:

| Fixture | Path | Currently Passes? | After Changes |
|---|---|---|---|
| Firewall breach | `evaluations/test-cases/proposal-review/firewall-breach.md` | Passes (violations correctly detected) | ✅ Still passes — hard rule tightening does not affect Visual Agent Builder or SOC 2 Type II detection |
| EU AI Act GCM gold standard | `evaluations/test-cases/gold-standards/eu-ai-act-high-risk-banking-gold-standard.md` | Passes | Requires verification — see below |
| India DPDP gold standard | `evaluations/test-cases/gold-standards/india-dpdp-customer-support-ai-gold-standard.md` | Passes | ✅ No change expected — no Edge/Sentry/Workspace references |
| UK Insurance gold standard | `evaluations/test-cases/gold-standards/uk-insurance-claims-model-gold-standard.md` | Passes | ✅ No change expected |

---

### EU AI Act GCM Gold Standard — Detailed Impact Assessment

This fixture contains GCM content and is the only fixture that references Ethana capabilities. The changes that could affect it:

**Change 1 (prefix matching):** PromptOps appears in the gold standard as `PromptOps — Canary releases` in the canonical model but not as a reference in the gold standard content itself. No impact.

**Change 3 (word-boundary matching):** No capability name in the gold standard appears as an embedded substring. No impact.

**Change 4 (hard rule tightening):** The gold standard does not reference Sentry.io, Microsoft Edge, or generic workspaces. Ethana Workspace and Ethana Edge are not referenced. No impact.

**Change 5 (has_status / has_workaround tightening):** The gold standard's In Build references (Compliance Pack, CI/CD Gate Integration in Section 10) explicitly use the phrase "In Build" on the same line as the capability name. `has_status` will still pass for these. The workaround descriptions use "manual workaround:" — the tightened `has_workaround` list includes "manual workaround". No impact.

**Change 2 (section scoping):** Changes the population of the capabilities dict. After scoping to Sections 1–5, spurious entries from pricing, services, and historical file tables are removed. This removes ~25 capability keys. The gold standard does not reference any of these spurious keys. No impact.

**Net expected result:** All current fixtures should continue to pass the linter after all six changes are applied. Verification by running the full test suite after implementation is required before committing the changes.

---

### New Violations That Would Fire After Changes

After implementing Changes 1–5, the following new violations would fire on any document that references these capabilities without proper disclosure (these are currently missed):

| Capability | Status | New violation type |
|---|---|---|
| PromptOps Canary Releases | Aspirational | Ambiguity Warning or Firewall Breach (if claimed as Production) |
| Role-Based Access Control on Knowledge Sources | Aspirational (as Workspace-specific) | Ambiguity Warning or Firewall Breach |
| Discovery IdP Connector | In Build | Ambiguity Warning |
| Guardrails Custom Policy Enforcement | Aspirational | Ambiguity Warning (multi-word key, though `guardrails` single-word remains skipped) — NB: `guardrails — custom policy enforcement` base name after em-dash split is `guardrails` which IS single-word → still skipped by guard |

The only immediately actionable new detection is for Role-Based Access Control on Knowledge Sources and PromptOps Canary Releases. The `guardrails` base-name issue cannot be resolved by the violation trigger fix alone — it also requires the single-word guard to be replaced with explicit handling.

---

## Appendix: Key Collision Summary

Verified by tracing all 98 canonical model rows through the current parser:

| Key | Collision type | Effect |
|---|---|---|
| `promptops` | Section 1.1 Production → Section 1.3 Aspirational (pending confirmation) | Final status: `"aspirational (pending confirmation)"` — non-triggering; single-word → skipped |
| `finops` | Section 1.2 In Build → Section 4 Production | Final status: `"production"` — In Build sub-features permanently undetectable; single-word → skipped |
| `runtime guardrails` | 8 sub-capability entries (all Production) | Final status: Production — consistent; no impact |
| `discovery` | Three Discovery entries (all In Build variants) | Final status: `"in build (output of discovery connectors)"` — non-triggering; single-word → skipped |
| `governance policy engine` | Section 1.2 and Section 4 (both In Build) | Final status: In Build (consistent); no collision harm — two separate keys produced (`governance policy engine` vs `governance policy engine (opa / rego)`) |

---

## Appendix: Capabilities That Cannot Be Detected by the Current Linter

Regardless of the matching strategy, the following capabilities cannot be reliably detected as long as the single-word skip guard or its functional equivalent is required:

| Capability | Reason |
|---|---|
| PromptOps (all sub-capabilities) | Single-word key `promptops` |
| FinOps (In Build sub-features) | Single-word key `finops` |
| Discovery (all sub-capabilities) | Single-word key `discovery` |
| MCP (Composable Creation) | Single-word key `mcp` |
| Evaluation (all sub-capabilities) | Single-word key `evaluation` |
| Guardrails (Custom Policy) | Single-word key `guardrails` |

Detection for these capabilities requires either: (a) explicit hard rules with specific multi-word detection patterns (as done for Visual Agent Builder), or (b) canonical model reorganisation to ensure every commercially significant capability has a unique multi-word key after parsing.
