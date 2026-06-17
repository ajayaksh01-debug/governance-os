# Skill: Ethana Capability Validation

**Version:** 1.0
**Category:** Truth Validation
**Owner:** Cursory Governance Team

---

## Purpose

This skill determines whether a specific Ethana capability can be legitimately claimed, what evidence supports the claim, what status the capability should carry (Production / In Build / Aspirational), and what customer-facing language is permitted or prohibited.

It is the foundational truth-validation layer that both Ethana Solution Mapping and Ethana Feature Mapping depend on. Before any capability is proposed commercially or validated technically, this skill adjudicates whether the claim itself is permissible and documents the evidence trail supporting that determination.

The skill resolves three types of problems:
1. **Status uncertainty** — when a team is unsure whether a capability is Production, In Build, or Aspirational
2. **Source conflict** — when a non-canonical source (marketing playbook, board deck, verbal product claim) says something different from canonical-product-model.md
3. **Scope ambiguity** — when a proposed claim attributes capabilities, depth, or scope to a feature that the canonical model does not explicitly confirm

This skill is intended to be run **proactively** — before a claim is made — not retroactively to explain a compliance breach.

**Primary authority source:** `knowledge/ethana/canonical-product-model.md` is the only permitted source for capability status determinations. No secondary source, marketing document, or verbal claim can override it.

---

## When to Use This Skill

Use this skill when:
- A team member is unsure whether a specific Ethana capability is Production, In Build, or Aspirational before including it in a proposal, conversation, or document
- A source document (marketing playbook, sales deck, board briefing, press release) makes a capability claim and that claim needs validation against canonical-product-model.md
- Two sources conflict about the status or scope of an Ethana capability and the conflict needs formal adjudication
- A proposed claim sentence needs to be checked for scope expansion — whether it attributes more to a capability than the canonical model confirms
- A downstream skill (Ethana Solution Mapping or Ethana Feature Mapping) needs a status determination it cannot resolve from the canonical model alone
- A capability is being considered for customer-facing use and the team wants a documented, auditable validation record

---

## Relationship to Other Skills

| | Capability Validation | Solution Mapping | Feature Mapping |
|---|---|---|---|
| **Question** | Can this capability be claimed? | What can we propose? | Does this feature work here? |
| **Layer** | Foundation — truth gate | Commercial | Technical |
| **Input** | Capability name, proposed claim, or source document | Governance requirements | Feature questions, POC scope |
| **Output** | Status verdict + evidence register + allowed/prohibited claim language | Proposal language + deal structure | Technical validation + POC readiness |
| **Audience** | Product, sales, advisory, technical — any claimant | Advisory team | Solution architects |
| **When used** | Before any claim is made | Pre-proposal | Pre-POC |
| **Scoring metric** | Evidence Confidence Score (ECS) + Claim Permission Level (CPL) | Coverage Confidence Score (CCS) | Technical Fit Score (TFS) |
| **Pass threshold** | 90/100 | 70/100 | 85/100 |

**Why 90/100?** An error in Capability Validation propagates downstream into every Solution Mapping and Feature Mapping output referencing that capability. The blast radius is the highest of the three skills. The release standard is correspondingly the strictest.

---

## Input Specification

### Required Inputs

At least one of the following three is required:

| Field | Description |
|---|---|
| `capability_name` | The name of the capability to validate — "Bias Scanner," "ISO 27001 certification," "NHI lifecycle management," "Visual Agent Builder" |
| `proposed_claim` | A specific sentence someone wants to say or write — "Ethana is ISO 27001 certified," "The Bias Scanner performs statistical model bias audits," "Ethana Edge is available for enterprise deployments" |
| `source_document` | A document making a capability claim that needs validation against canonical-product-model.md — marketing playbook, board deck, RFP response, sales slide, verbal claim transcribed to text |

### Contextual Inputs

| Field | Values | Why it matters |
|---|---|---|
| `claim_context` | Formal Proposal / RFP Response / Marketing / Discovery Conversation / Internal Briefing / Engineering Documentation | Determines the minimum CPL required before the claim is permitted in that context — Formal Proposal requires CPL-1 or CPL-2; Internal Briefing tolerates CPL-4 |
| `requesting_team` | Product / Sales / Advisory / Technical | Shapes which sections are emphasised and how technical the Audit Trail is written |
| `jurisdiction` | EU / UK / India / Global | Regulatory capability claims (GDPR compliance, RBI audit readiness) have jurisdiction-specific truth conditions |
| `contradiction_sources` | Named sources making conflicting claims | Pre-flags a contradiction before Phase 5 and triggers DT3 as the primary workflow path |

---

## Output Specification — 9 Sections

### Section 1 — Capability Status Determination

The validated capability status sourced from canonical-product-model.md:
- **Validated status**: Production / In Build / Aspirational / Unresolved
- **Status source**: the exact entry from canonical-product-model.md, quoted verbatim
- **Mandatory caveats**: any caveats attached to this capability in canonical-product-model.md that must accompany every claim regardless of context
- **Scope boundaries**: what this capability does and does not cover, per the canonical model
- **Status confidence**: Authoritative / Corroborated / Canonical-only / Contested / Insufficient (mapped from Section 7 ECS band)

For Unresolved: the specific reason — not found / entry silent on this claim / contradiction without resolution.

### Section 2 — Evidence Sufficiency Summary

A quick-reference synthesis placed immediately after Section 1. A product manager or sales lead reads Sections 1 and 2 to get a complete answer without reading all nine sections.

When multiple claims are being validated, this section shows one entry per claim — each with its own CPL and sufficiency verdict, demonstrating that CPL is claim-specific.

```
Capability:              [canonical name]
Proposed claim context:  [claim_context value]
Validated status:        [Production / In Build / Aspirational / Unresolved]
ECS:                     [score] / 100 — [band name]

Claim:                   [claim A text]
CPL:                     [CPL-1 through CPL-5] — [one-line definition]
Sufficiency verdict:     [Sufficient / Conditionally Sufficient / Insufficient]
Permitted in:            [list of contexts]
Restricted from:         [list of contexts]

Claim:                   [claim B text — if a second claim is being validated]
CPL:                     [CPL level — may differ from claim A for the same capability]
Sufficiency verdict:     [...]
Permitted in:            [...]
Restricted from:         [...]

Contradictions found:    [count] — none / resolved / pending escalation
Escalation required:     [Yes — reason / No]
```

**Sufficiency verdicts:**
- **Sufficient**: CPL-1 or CPL-2. Claim may be used as stated (CPL-1) or with mandatory caveat added inline (CPL-2).
- **Conditionally Sufficient**: CPL-3 or CPL-4. Claim may be used in limited contexts only.
- **Insufficient**: CPL-5. Claim must not be used in any external context.

### Section 3 — Evidence Register

All sources examined during validation, in order consulted:

| Source | Type | Claim made | Consistent with canonical model? | Authority level |
|---|---|---|---|---|
| canonical-product-model.md | Primary | [verbatim quote] | — | Primary |
| product-architecture-investigation.md | Approved Secondary | [claim or "Silent"] | Yes / No / Silent | Secondary |
| [other source] | [type] | [claim] | Yes / No / Expands / Contradicts | Reference Only |

**Authority levels:** Primary (canonical-product-model.md only) / Approved Secondary (product-architecture-investigation.md, use-cases.md) / Reference Only (playbook, board deck, press release — context only; cannot establish status) / Non-authoritative (verbal claims, social media).

### Section 4 — Allowed Claims

Every claim permitted for this capability, with its CPL. Claims listed from CPL-1 (broadest) to CPL-3 (narrowest permitted use). No claim without a CPL tag appears here.

Format per entry:
```
Claim text:      [exact quotable language]
CPL:             [CPL-1 / CPL-2 / CPL-3] — [one-line definition]
Permitted in:    [list of claim contexts]
Required caveat: [mandatory inline caveat text — applies when CPL-2]
Evidence basis:  canonical-product-model.md — [entry]; ECS [score]
```

### Section 5 — Prohibited Claims

Every claim that must not be used, tagged CPL-5:

```
Prohibited claim:   [exact language or pattern]
CPL:                CPL-5 — Prohibited in all contexts
Prohibition reason: [Aspirational capability / In Build not yet available /
                    Scope expansion beyond canonical confirmation /
                    Certification not held / No canonical source]
Risk if used:       [regulatory claim / misrepresentation / expectation mismatch]
Source of claim:    [where this prohibited claim originates]
```

### Section 6 — Contradiction Log

Populated when sources conflict. One entry per contradiction:
- **Source A**: what it says
- **Source B**: what the canonical model (or other source) says
- **Nature**: direct conflict / scope expansion / omission of mandatory caveat
- **Adjudication**: which source is authoritative and why
- **Resolution**: the position adopted in Section 1
- **ECS impact**: the downward adjustment applied

If no contradictions: "No contradictions found across [N] sources examined."

### Section 7 — Evidence Confidence Score (ECS)

The aggregate evidence quality score (0–100) for the capability status determination. Shows full arithmetic — base, each adjustment applied, the sum, and the resulting ECS band. The arithmetic must be reproducible from this section alone without access to any other section.

### Section 8 — Escalation Recommendation

Triggered when ECS < 45 or status is Unresolved:
- **Escalation trigger**: the specific condition
- **Escalation recipient**: Product team / Engineering / Canonical model maintainer / Marketing
- **Specific question**: exactly what needs to be confirmed or corrected — not "clarify this" but a specific answerable question with the context of the conflict included
- **Interim position**: what may be said while escalation is pending
- **Downstream blocks**: which Solution Mapping or Feature Mapping outputs are blocked

If no escalation needed: "No escalation required. ECS [X] ([band]). Claim permitted in [contexts]."

### Section 9 — Validation Audit Trail

The complete validation record. Required for Phase 9 gate confirmation:
- Validation date
- Claims validated (verbatim input)
- Sources checked, in order
- Status found in each source
- Contradictions identified: count and nature
- ECS arithmetic (or reference to Section 7)
- Final status determination
- CPL assigned to each Allowed Claim in Section 4
- Hard disqualifiers checked: confirmed not triggered / triggered — reason
- Phase 9 Mandatory Traceability Gate: completed [date] / not completed
- Allowed Claims count
- Prohibited Claims count
- Escalation status: not required / required — pending / resolved

---

## ECS and CPL — Two Separate Constructs

Understanding the distinction between ECS and CPL is essential for applying this skill correctly.

**ECS (Evidence Confidence Score):** A capability-level score (0–100) measuring how well the evidence supports the status determination in Section 1. The ECS is the same for all claims about a given capability in a given validation run. It measures "how good is the evidence?"

**CPL (Claim Permission Level):** A claim-level designation (CPL-1 through CPL-5) determining where and how a specific claim may be used. The CPL is derived from the ECS plus the capability status plus the content of the specific claim being evaluated. It measures "what can be said, to whom, in what context?"

**The critical distinction:** Two claims about the same capability carry the same ECS but may carry different CPLs if one embeds a mandatory caveat and the other does not. CPL is assigned per claim, not per capability. See DT6 in workflow.md.

**CPL Levels:**

| CPL | Name | Definition | Permitted contexts |
|---|---|---|---|
| CPL-1 | Unrestricted | Fully permitted in all contexts with no additional conditions | Formal Proposal, RFP Response, Marketing, Discovery, Internal, Engineering |
| CPL-2 | Advisory-restricted | Permitted in formal proposal and advisory contexts; mandatory caveat must be included inline; not for marketing use | Formal Proposal, RFP Response, Discovery, Internal, Engineering |
| CPL-3 | Conversation-only | Permitted in discovery conversations and internal briefings only; must not appear in any written formal deliverable | Discovery Conversation, Internal Briefing |
| CPL-4 | Internal-only | Permitted in internal engineering and product discussions only; must not be used externally | Internal Briefing, Engineering Documentation |
| CPL-5 | Prohibited | Must not appear in any context, internal or external | None |

**ECS Bands:**

| Band | Score | Minimum CPL available from this band |
|---|---|---|
| Authoritative | 85–100 | CPL-1 (when caveat embedded) or CPL-2 (when caveat not embedded) |
| Corroborated | 65–84 | CPL-1 (when caveat embedded) or CPL-2 (when caveat not embedded) |
| Canonical-only | 45–64 | CPL-2 minimum |
| Contested | 20–44 | CPL-3 maximum |
| Insufficient | 0–19 | CPL-4 or CPL-5 only |

---

## Constraints and Scope

**In scope:**
- Validating any capability claim about any Ethana product or capability
- Adjudicating status when sources conflict
- Producing Allowed Claim language for any capability at any status tier
- Detecting scope expansion in proposed claims
- Escalating to product team when canonical model is insufficient
- Serving as the status authority for downstream skills

**Out of scope:**
- Updating canonical-product-model.md directly — this skill escalates; the canonical model maintainer updates
- Making commercial proposal decisions (Ethana Solution Mapping)
- Technical feasibility assessment (Ethana Feature Mapping)
- Determining what Ethana should build

**Hard constraint — claims firewall:**
canonical-product-model.md is the only source that can establish Production status for a capability. No secondary source, marketing document, board deck, or verbal claim may override it. When this file is silent, the status is Unresolved and no external claim is permitted until the file is updated.

**Depth calibration:**
- Single capability status question, no contradiction → Phases 1, 3, 6, 7, 9 only — 25–30 minutes; condensed output
- Proposed claim requiring scope-expansion check → all phases — 65–80 minutes; full output
- Source document with multiple claims → all phases; one Section 4/5 entry per claim — 75–90 minutes

---

## Knowledge Dependencies

### Tier 1 — PRIMARY (mandatory for every invocation)

`knowledge/ethana/canonical-product-model.md`

The only source that can establish or confirm capability status. When this file is silent on a specific detail, the answer is "unconfirmed." Do not invent, infer, or interpolate.

### Tier 2 — APPROVED SECONDARY (consulted for corroboration; cannot override Tier 1)

- `knowledge/ethana/product-architecture-investigation.md` — technical architecture detail; ECS +15 when it corroborates
- `knowledge/ethana/use-cases.md` — use case pattern matching; ECS +10 when it corroborates a Production claim in context

### Tier 3 — REFERENCE ONLY (context only; cannot establish status)

- Marketing playbook — commercial claim language and framing reference; not for status determination
- Board deck / Board briefing — historical engineering context; cannot override canonical model
- `knowledge/ethana/competitor-positioning.md` — competitive context only; not for Ethana status determination

### Tier 4 — PROHIBITED SOURCES (must not be used for status determination)

- `knowledge/ethana/capability-status.md` — a prior derived file; not canonical
- `knowledge/ethana/source-of-truth.md` — a prior derived file; not canonical
- `knowledge/ethana/ethana-status-reconciliation.md` — a prior reconciliation file; not canonical

These files may exist in the knowledge base but are products of earlier processes, not authoritative sources. If they conflict with canonical-product-model.md, they are wrong.

---

## Related Skills

- `skills/ethana-solution-mapping/` — consumer of Capability Validation outputs; should cite Section 9 (Audit Trail) as the status authority when challenged
- `skills/ethana-feature-mapping/` — consumer of Capability Validation outputs; uses validated status to confirm TFS scoring is grounded in correct Production capabilities
- `skills/regulatory-mapping/` — may generate capability questions when mapping regulatory controls to Ethana features
