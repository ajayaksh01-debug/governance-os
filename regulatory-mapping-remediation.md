# Regulatory Mapping — Remediation Assessment

**Date:** 2026-06-17
**Scope:** Review of `skills/regulatory-mapping/` for references to deprecated Ethana knowledge files
**Constraint:** Assessment only — no files modified

---

## 1. Findings Summary

| # | Finding | File | Line | Severity |
|---|---|---|---|---|
| F1 | `capability-status.md` listed as knowledge dependency | [SKILL.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L204) | 204 | **High** — prohibited source |
| F2 | `framework-crosswalk.md` listed as knowledge dependency without authority classification | [SKILL.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L205) | 205 | **Medium** — valid file, missing governance |
| F3 | No reference to `canonical-product-model.md` anywhere in the skill | All 4 files | — | **Medium** — architectural gap |
| F4 | No tiered authority classification for Ethana knowledge sources | [SKILL.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L203-L205) | 203–205 | **Medium** — inconsistent with Ethana chain pattern |
| F5 | Two phantom downstream skills referenced that do not exist | [SKILL.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L212-L214) | 212–214 | **Low** — documentation accuracy |

**Files checked:**

| File | Deprecated references found? |
|---|---|
| [SKILL.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md) | Yes — F1, F2, F3, F4, F5 |
| [workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/workflow.md) | No |
| [evaluation.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/evaluation.md) | No |
| [examples.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/examples.md) | No |

> [!IMPORTANT]
> The deprecated reference is isolated to `SKILL.md` lines 203–205 (the Ethana knowledge dependencies section). No workflow phase, evaluation dimension, or worked example references the deprecated file. The contamination is declarative, not operational — but it creates a risk if an operator treats the dependency list as authoritative.

---

## 2. Detailed Findings

### F1 — `capability-status.md` Listed as Knowledge Dependency

**Location:** [SKILL.md line 204](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L204)

**Current text:**
```
**Ethana:**
- `knowledge/ethana/capability-status.md`
- `knowledge/ethana/framework-crosswalk.md`
```

**Problem:**

`capability-status.md` is explicitly classified as a **Tier 4 — PROHIBITED SOURCE** by [Ethana Capability Validation](file:///Users/ajayrajsingh/Documents/governance-os/skills/ethana-capability-validation/SKILL.md#L286-L292):

> - `knowledge/ethana/capability-status.md` — a prior derived file; not canonical
> - These files may exist in the knowledge base but are products of earlier processes, not authoritative sources. If they conflict with canonical-product-model.md, they are wrong.

It is also explicitly **superseded** by the header of [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md#L5-L8):

> **Supersedes (as primary reference):**
> - `knowledge/ethana/capability-status.md` — historical artifact, engineering-era status matrix. Do not update; do not use as primary status source.

**Why this matters for Regulatory Mapping specifically:**

Regulatory Mapping produces Section 6 (Control Requirements) which feeds directly into Ethana Solution Mapping and Ethana Feature Mapping. If a Regulatory Mapping operator consults `capability-status.md` while writing a control requirement and includes a capability reference based on that file's status matrix, the downstream skills would receive a control requirement grounded in a deprecated status determination.

For example, `capability-status.md` describes the Bias Scanner simply as one of "six native scanners" in Production. It does not include the critical caveat from the canonical model:

> [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md#L56): "This is a **runtime text filter only**. It does not audit model weights, test disparate impact across demographic groups, or validate training data."

A Regulatory Mapping output that references EU AI Act Art.10 (data governance and bias) and cites the Bias Scanner as addressing "bias evaluation" — based on `capability-status.md` — would produce a control requirement that overstates Ethana's capability. That overstated requirement would then flow into Solution Mapping Section 1, inflating the CCS score.

**Risk level:** High. The file contains outdated status information and lacks the mandatory caveats present in the canonical model.

---

### F2 — `framework-crosswalk.md` Listed Without Authority Classification

**Location:** [SKILL.md line 205](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L205)

**Problem:**

`framework-crosswalk.md` is a **valid, active knowledge file**. It is not deprecated or prohibited. It maps governance frameworks (EU AI Act, ISO 42001, NIST AI RMF, OWASP LLM Top 10, BFSI model risk, RBI, FCA, DPDP) to Ethana capabilities with explicit status flags (`[P]`, `[IB]`, `[RM]`, `[SVC]`, `[GAP]`).

However, it has two issues in this context:

1. **No authority classification.** The Ethana chain skills (Capability Validation, Solution Mapping, Feature Mapping) classify every Ethana knowledge source into a tier (Primary / Secondary / Reference Only / Prohibited). Regulatory Mapping lists it as a flat dependency without specifying its authority level for status determinations.

2. **Status flags in `framework-crosswalk.md` are not sourced from `canonical-product-model.md`.** The file was created independently and its `[P]`, `[IB]`, `[RM]` flags may diverge from the canonical model. For example:
   - `framework-crosswalk.md` uses the status `[RM]` (Roadmap) for Discovery. The canonical model classifies the Sentry component of Discovery as **In Build** and the Workspace component as **Aspirational** — a more granular determination.
   - `framework-crosswalk.md` refers to "Bias scanner **[P]** for runtime screening" under EU AI Act Art.10 without the mandatory caveat that it is a runtime text filter only.

**Risk level:** Medium. The file is useful for framework-to-capability mapping but its status flags have not been reconciled with the canonical model, and it is not classified in the authority hierarchy.

---

### F3 — No Reference to `canonical-product-model.md`

**Location:** Entire skill — all 4 files

**Problem:**

Regulatory Mapping does not reference `canonical-product-model.md` anywhere in its knowledge dependencies, workflow, evaluation rubric, or examples. This is the only skill in the repository that references Ethana knowledge files without referencing the canonical authority source.

Comparison:

| Skill | References `canonical-product-model.md`? | Ethana knowledge tier system? |
|---|---|---|
| Ethana Capability Validation | Yes — Tier 1 PRIMARY, sole authority | Yes — 4 tiers |
| Ethana Solution Mapping | Yes — Tier 1 PRIMARY | Yes — 4 tiers |
| Ethana Feature Mapping | Yes — Tier 1 PRIMARY | Yes — 4 tiers |
| AI Incident Analysis | No — does not reference Ethana files at all | N/A — no Ethana dependency |
| **Regulatory Mapping** | **No** | **No** |

**Why this matters:**

Regulatory Mapping's output (particularly Section 6 — Control Requirements and Section 8 — BFSI Considerations) often contains references to Ethana capabilities when mapping regulatory obligations to platform controls. Without the canonical model as a declared authority, operators may source capability information from `capability-status.md` (as currently listed) or from `framework-crosswalk.md` (whose status flags are unreconciled).

**Risk level:** Medium. Regulatory Mapping's primary function is regulatory analysis, not capability validation. Most of its output does not make Ethana status claims. However, when it does reference Ethana capabilities (Section 6, Section 8), those references lack the governance controls that the Ethana chain enforces.

---

### F4 — No Tiered Authority Classification for Ethana Sources

**Location:** [SKILL.md lines 203–205](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L203-L205)

**Problem:**

The Ethana knowledge dependencies are listed as a flat group:

```
**Ethana:**
- `knowledge/ethana/capability-status.md`
- `knowledge/ethana/framework-crosswalk.md`
```

The three Ethana chain skills use a tiered classification system:

```
### Tier 1 — PRIMARY (mandatory for every invocation)
### Tier 2 — APPROVED SECONDARY (consulted for corroboration; cannot override Tier 1)
### Tier 3 — REFERENCE ONLY (context only; cannot establish status)
### Tier 4 — PROHIBITED SOURCES (must not be used for status determination)
```

**Why this matters:**

Without classification, an operator has no guidance on which Ethana file to trust when two files disagree. Today, `capability-status.md` says the Bias Scanner is simply "Production" while `canonical-product-model.md` says "Production — with mandatory caveat." Both are in the Ethana knowledge directory. The tier system resolves this ambiguity; the flat list does not.

**Risk level:** Medium.

---

### F5 — Phantom Downstream Skill References

**Location:** [SKILL.md lines 212–214](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L212-L214)

**Current text:**
```
- `skills/governance-control-mapping/` — for translating regulatory control requirements into specific control implementations
- `skills/iso-42001-gap-assessment/` — for detailed ISO 42001 gap analysis following framework identification
```

**Problem:**

Neither `skills/governance-control-mapping/` nor `skills/iso-42001-gap-assessment/` exists in the repository. These are planned skills documented in [repository-skill-architecture.md](file:///Users/ajayrajsingh/Documents/governance-os/repository-skill-architecture.md) but have not been created.

**Risk level:** Low. This is a documentation accuracy issue — an operator looking for these skills will find empty paths. It does not affect the Regulatory Mapping skill's own output quality.

---

## 3. Cross-Check: Other Deprecated Ethana Files

For completeness, I verified that the following deprecated files are **not** referenced anywhere in `skills/regulatory-mapping/`:

| File | Status per canonical model | Referenced in regulatory-mapping? |
|---|---|---|
| `knowledge/ethana/source-of-truth.md` | Superseded — historical artifact | **No** ✓ |
| `knowledge/ethana/ethana-status-reconciliation.md` | Superseded — status elevations explicitly rejected | **No** ✓ |
| `knowledge/ethana/ethana-status-harmonization.md` | Derived analysis file | **No** ✓ |
| `knowledge/ethana/evidence-based-status-review.md` | Derived analysis file | **No** ✓ |
| `knowledge/ethana/primary-source-validation.md` | Derived analysis file | **No** ✓ |

Only `capability-status.md` is referenced.

---

## 4. Recommended Changes

### Change 1 — Remove `capability-status.md` from knowledge dependencies

**Priority:** High
**File:** [SKILL.md line 204](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L204)

**Action:** Remove `knowledge/ethana/capability-status.md` from the Ethana knowledge dependencies section.

**Rationale:** This file is a Tier 4 PROHIBITED source under the canonical authority model. It is explicitly superseded by `canonical-product-model.md`. Listing it as a dependency legitimises its use by operators.

```diff
 **Ethana:**
-- `knowledge/ethana/capability-status.md`
 - `knowledge/ethana/framework-crosswalk.md`
```

---

### Change 2 — Add `canonical-product-model.md` as the primary Ethana authority

**Priority:** High
**File:** [SKILL.md lines 203–205](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L203-L205)

**Action:** Replace the flat Ethana dependency list with a tiered classification consistent with the Ethana chain skills.

```diff
-**Ethana:**
-- `knowledge/ethana/capability-status.md`
-- `knowledge/ethana/framework-crosswalk.md`
+**Ethana:**
+- `knowledge/ethana/canonical-product-model.md` — primary authority for all Ethana capability status references in Section 6 or Section 8. When this skill references an Ethana capability to illustrate a control mapping, the capability status must be sourced from this file.
+- `knowledge/ethana/framework-crosswalk.md` — framework-to-capability mapping reference. Status flags in this file (`[P]`, `[IB]`, `[RM]`) should be cross-checked against canonical-product-model.md before inclusion in any output section. This file is useful for identifying which Ethana capabilities map to which framework controls, but it is not an authority for capability status.
```

**Rationale:** Aligns Regulatory Mapping with the authority model enforced by Capability Validation, Solution Mapping, and Feature Mapping. Does not require Regulatory Mapping to perform full capability validation — it only requires that when Ethana capabilities are referenced, the status is sourced correctly.

---

### Change 3 — Add a caveat to the Constraints section

**Priority:** Medium
**File:** [SKILL.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md), Constraints and Scope section (lines 155–172)

**Action:** Add a constraint clarifying that Regulatory Mapping does not make Ethana capability status determinations.

**Proposed addition:**

```markdown
**Ethana capability references:**
When Section 6 (Control Requirements) or Section 8 (BFSI Considerations) references an Ethana capability
to illustrate how a control requirement maps to the platform, the capability status must be sourced from
`knowledge/ethana/canonical-product-model.md`. This skill does not validate Ethana capability claims —
that is the function of `skills/ethana-capability-validation/`. If a capability's status is uncertain,
reference the capability by name and note "status to be confirmed by Capability Validation" rather than
asserting a status.
```

**Rationale:** Establishes a clear boundary: Regulatory Mapping can *reference* Ethana capabilities but should not *determine* their status. This prevents operators from using Regulatory Mapping output as an implicit capability validation.

---

### Change 4 — Annotate phantom skill references

**Priority:** Low
**File:** [SKILL.md lines 212–214](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md#L212-L214)

**Action:** Add "(planned)" annotations to related skills that do not yet exist.

```diff
-- `skills/governance-control-mapping/` — for translating regulatory control requirements into specific control implementations
-- `skills/iso-42001-gap-assessment/` — for detailed ISO 42001 gap analysis following framework identification
+- `skills/governance-control-mapping/` — for translating regulatory control requirements into specific control implementations (planned)
+- `skills/iso-42001-gap-assessment/` — for detailed ISO 42001 gap analysis following framework identification (planned)
```

---

### Change 5 — Add `framework-crosswalk.md` reconciliation caveat to workflow

**Priority:** Medium
**File:** [workflow.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/workflow.md)

**Action:** In the workflow phase where the operator maps regulatory controls to Ethana capabilities (if such a phase exists), add a step requiring cross-check of `framework-crosswalk.md` status flags against `canonical-product-model.md`.

**Rationale:** `framework-crosswalk.md` is a practical mapping tool, but its status flags (`[P]`, `[IB]`, `[RM]`) were authored independently from the canonical model. A reconciliation step prevents unreconciled status flags from propagating into Section 6 output.

---

## 5. Implementation Order

| Order | Change | File | Blocked by |
|---|---|---|---|
| 1 | Remove `capability-status.md` | SKILL.md | Nothing |
| 2 | Add `canonical-product-model.md` as primary Ethana authority | SKILL.md | Nothing — can be combined with Change 1 |
| 3 | Add Ethana capability reference constraint | SKILL.md | Nothing |
| 4 | Annotate phantom skill references | SKILL.md | Nothing |
| 5 | Add `framework-crosswalk.md` reconciliation step to workflow | workflow.md | Nothing |

> [!NOTE]
> Changes 1–4 are all modifications to [SKILL.md](file:///Users/ajayrajsingh/Documents/governance-os/skills/regulatory-mapping/SKILL.md) and can be applied in a single commit. Change 5 requires reading the full workflow to identify the correct insertion point.

---

## 6. Impact Assessment

| Downstream consumer | Risk from current state | Mitigated by remediation? |
|---|---|---|
| Ethana Solution Mapping (accepts Section 6) | An Ethana capability reference in Section 6 could carry an incorrect status sourced from `capability-status.md` | Yes — Change 2 establishes canonical-product-model.md as the authority |
| Ethana Feature Mapping (accepts Section 6) | Same risk — a control requirement referencing a deprecated status could inflate TFS grounding | Yes |
| Ethana Proposal Review (planned, consumes all upstream) | Would inherit any status error propagated through Solution Mapping or Feature Mapping | Yes — Proposal Review also performs its own traceability check |

**Blast radius:** Contained. Regulatory Mapping's primary output is regulatory analysis, not capability status determination. The risk materialises only when Section 6 or Section 8 includes an Ethana capability reference with an incorrect status. The remediation establishes a clear authority source and a boundary statement to prevent this.
