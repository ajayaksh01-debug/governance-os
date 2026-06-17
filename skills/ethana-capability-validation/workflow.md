# Ethana Capability Validation — Workflow

---

## Workflow Overview

| Phase | Name | Duration |
|---|---|---|
| 1 | Intake and Claim Parsing | 5 min |
| 2 | Source Inventory | 5 min |
| 3 | Canonical Model Lookup | 5 min |
| 4 | Secondary Source Cross-Reference | 10 min |
| 5 | Contradiction Detection and Resolution | 10–15 min |
| 6 | ECS Computation | 5 min |
| 7 | CPL Assignment and Claims Adjudication | 10 min |
| 8 | Escalation Decision | 5 min |
| 9 | Mandatory Traceability Gate and Audit Trail | 10 min |

**Total:** 65–80 minutes for a full validation with potential contradictions.

**Abbreviated path (single capability, no contradiction, no scope-expansion check):** Phases 1, 3, 6, 7, 9 only — 25–30 minutes. Use only when all three conditions hold: (1) a single capability name is the input with no proposed claim text requiring scope analysis; (2) canonical-product-model.md has an unambiguous entry for the capability; (3) no `contradiction_sources` are flagged.

---

## Phase 1: Intake and Claim Parsing

Parse all inputs and identify exactly what is being validated before touching any source document.

**Steps:**

1. Extract the capability name from the input. If only a `proposed_claim` or `source_document` is provided, identify the capability name from the content. If multiple capabilities are referenced, scope the validation to each one separately — this skill validates one canonical capability per run.

2. Extract every proposed claim from the input. A claim is any affirmative or implied statement about what a capability does, at what status, with what scope. From a source document, extract all distinct claims, not just the most prominent one.

3. Record the `claim_context`, `requesting_team`, `jurisdiction`, and `contradiction_sources` from the input. If `claim_context` is not provided, default to Formal Proposal (the strictest standard).

4. Pre-flag claim types for scope-expansion risk. Any claim that uses "all," "any," "every," "full," a specific certification name, a specific compliance standard, or a specific performance figure requires DT4 (Scope-Expansion Detection) to be run before CPL assignment.

5. Record the number of distinct claims to validate. The output will have one Section 4 or Section 5 entry per claim.

---

## Phase 2: Source Inventory

Identify all sources that reference this capability before reading any of them. Classify each by authority level before reading its content — classification must be based on source type, not on whether its claim is favourable.

**Authority classification:**
- **Primary**: canonical-product-model.md — the only permitted basis for status determination
- **Approved Secondary**: product-architecture-investigation.md, use-cases.md — corroboration only
- **Reference Only**: marketing playbook, board deck/briefing, press releases, pitch decks, sales materials — context only; may inform commercial claim language; cannot establish status
- **Non-authoritative**: verbal claims, meeting notes, social media, competitor intelligence about Ethana — documentation only; must not influence status determination
- **Prohibited**: capability-status.md, source-of-truth.md, ethana-status-reconciliation.md — derived files; must not be used as positive evidence for any status

Log every source identified, even if it will not be consulted. A source that exists but is not consulted must be logged as "identified but not consulted — [reason]." If it could affect ECS or contain a contradicting claim, it must be consulted.

---

## Phase 3: Canonical Model Lookup

Consult canonical-product-model.md and record the exact entry for the capability being validated.

**Steps:**

1. Search for the capability by canonical name, known aliases, and product line (Build / Edge / Workspace).

2. Record the exact entry verbatim — do not paraphrase. The verbatim text is the authority. Any paraphrase introduces interpretation risk.

3. Record the status explicitly as one of: Production / In Build / Aspirational. If the file uses any other language, map it to the closest status and note the original language.

4. Record all mandatory caveats attached to this capability. Mandatory caveats are statements in the canonical model that qualify the capability's scope, modality, or technical implementation. They must accompany every Allowed Claim regardless of the CPL or claim context.

5. Record the scope boundary — what the canonical model explicitly says this capability covers and (if documented) does not cover. This is the outer limit of any Allowed Claim. Anything not explicitly confirmed by the canonical model is unconfirmed scope.

6. If the capability is not found in canonical-product-model.md: status = Unresolved. Do not proceed to Phase 4 hoping a secondary source will establish status. Log the absence and proceed to Phase 6 with ECS = 0 (Path D or E — see ECS Scoring Model).

---

## Phase 4: Secondary Source Cross-Reference

Consult Approved Secondary sources for corroboration or contradiction. Consult Reference Only sources for awareness of claims circulating in the market.

**Order of consultation:**
1. product-architecture-investigation.md — check for corroborating technical detail
2. use-cases.md — check for use case references that corroborate Production status
3. Reference Only sources — document claims made; note any that conflict with canonical-product-model.md

**Recording:**
- For each source: document what it says about this capability
- Mark as: Corroborates / Contradicts / Silent / Expands scope
- Note any claim in a Reference Only source that goes beyond what canonical-product-model.md confirms — these are scope expansion candidates for DT4

**Do not use Reference Only sources to upgrade a status determination.** If canonical-product-model.md says In Build and the marketing playbook says Production, the canonical model prevails. The playbook claim is noted in Section 3 (Evidence Register) and in Section 6 (Contradiction Log) — it does not change the status.

---

## Phase 5: Contradiction Detection and Resolution

Identify every conflict between sources and resolve each one using DT3.

A contradiction is any case where:
- A non-canonical source claims a higher status than canonical-product-model.md
- A non-canonical source attributes features, modalities, certifications, or performance figures to a capability that the canonical model does not confirm
- A non-canonical source omits a mandatory caveat that the canonical model attaches to a capability

For each contradiction found:
1. Document both positions (Source A claim vs. canonical model position)
2. Apply DT3 to adjudicate
3. Record the resolution and the ECS adjustment
4. This contradiction becomes a Section 6 (Contradiction Log) entry

If `contradiction_sources` were flagged in the input, verify the specific conflict and resolve it first. Then check all other sources for additional contradictions.

If no contradictions are found, document: "No contradictions found across [N] sources examined." This must appear in Section 6 — a blank Section 6 is not acceptable.

---

## Phase 6: ECS Computation

Compute the Evidence Confidence Score using the scoring model below. Show all arithmetic — base score, each adjustment, the running total, and the final ECS. The arithmetic in Section 7 must be independently verifiable.

### ECS Scoring Model

**Determine the computation path first:**

| Path | Condition | Starting point |
|---|---|---|
| A | Canonical model confirms the capability at the claimed status | Base: 50 — proceed to adjustments |
| B | Canonical model shows In Build; a Production claim is being evaluated | ECS = 0 — no adjustments; stop |
| C | Canonical model shows Aspirational; any claim is being evaluated | ECS = 0 — no adjustments; stop |
| D | Not in canonical model; Approved Secondary source confirms | Rebase: 15 — no further upward adjustments until canonical model updated |
| E | Not in canonical model; Reference Only or Non-authoritative source only | Rebase: 5 — no further upward adjustments |
| F | Not in canonical model; no source at all | ECS = 0 |

**Path A Adjustments (apply in sequence; floor at 0):**

| Condition | Adjustment |
|---|---|
| Canonical entry includes technical detail (architecture specifics, confirmed performance figures, scope documentation beyond a feature name) | +20 |
| One Approved Secondary source corroborates the Production status or its technical detail | +15 |
| A second Approved Secondary source corroborates independently (cap: secondary bonus may not exceed +20 total) | +10 (max total secondary bonus: +20) |
| Canonical entry is sparse — the capability is listed but has no technical detail beyond its name | −5 |
| One Approved Secondary source contradicts the canonical model position (canonical model prevails; contradiction documented in Section 6) | −20 |
| One Reference Only or Non-authoritative source contradicts the canonical model (lower penalty because lower authority) | −10 per source |

**ECS Bands:**

| Band | Score | Meaning |
|---|---|---|
| Authoritative | 85–100 | Canonical entry is detailed; at least one Approved Secondary corroborates; no unresolved contradiction |
| Corroborated | 65–84 | Canonical model confirms; at least one secondary corroborates; no or resolved contradiction |
| Canonical-only | 45–64 | Canonical model confirms; no secondary corroboration; no contradiction |
| Contested | 20–44 | Contradiction found and resolved; canonical model prevails but evidence quality is reduced |
| Insufficient | 0–19 | Not confirmed in canonical model; or In Build / Aspirational with a Production claim |

**Example arithmetic display (Section 7):**

```
Claimed status:    Production
Path:              A (canonical model confirms Production)

Base score:                                            +50
Rich canonical entry (architecture detail confirmed):  +20
Corroboration: product-architecture-investigation.md:  +15
No contradictions found:                               ±0
                                                      ────
ECS:                                                   85 → Authoritative
```

---

## Phase 7: CPL Assignment and Claims Adjudication

For each claim identified in Phase 1, run DT4 (Scope-Expansion Detection) and then DT6 (CPL Assignment). Write the output into Sections 4 (Allowed Claims) and 5 (Prohibited Claims).

**Process per claim:**
1. Run DT4 — does the claim expand scope beyond what canonical-product-model.md explicitly confirms? If yes → CPL-5, move to Section 5. Do not continue to DT6.
2. If DT4 passes — run DT6 to determine the CPL based on ECS and status.
3. Write the claim into Section 4 (if CPL-1 through CPL-3) or Section 5 (if CPL-5).
4. Record the CPL and evidence basis for each Section 4 entry.
5. Record the prohibition reason and risk for each Section 5 entry.

For capabilities where the canonical model distinguishes sub-features at different status levels (e.g., MCP Security Broker core is Production but NHI module is In Build), treat each sub-claim separately — each gets its own DT4 and DT6 evaluation and its own Section 4 or 5 entry.

---

## Phase 8: Escalation Decision

Apply DT5 to determine whether escalation is required. If it is, write Section 8 with the specific escalation package: recipient, question, interim position, and downstream blocks.

If escalation is not required, write Section 8 as a one-line confirmation: "No escalation required. ECS [X] ([band]). Claims at CPL-[level] are permitted in [contexts]."

---

## Phase 9: Mandatory Traceability Gate and Audit Trail

**This gate must be completed before any output from this skill is released, shared with any team member, or consumed by a downstream skill. Do not release output that has not passed every step.**

### Gate Step 1 — ECS Arithmetic Verification

Re-sum every ECS adjustment from the path determination and adjustment table in Phase 6. Confirm the total matches Section 7. If the totals do not match: correct Section 7 before proceeding. Do not proceed with an arithmetic error.

Checklist:
- [ ] Path correctly identified (A/B/C/D/E/F)
- [ ] Base score correctly applied for the identified path
- [ ] Each adjustment correctly applied and labelled
- [ ] Running total sums to the ECS stated in Section 7
- [ ] ECS band correctly assigned from the total

### Gate Step 2 — CPL Completeness Verification

Every entry in Section 4 must have a CPL. Every entry in Section 5 must be tagged CPL-5. Every CPL assignment must be traceable to DT6 given the ECS and capability status.

Checklist:
- [ ] Every Section 4 entry has a CPL tag (CPL-1, CPL-2, or CPL-3)
- [ ] Every Section 5 entry is tagged CPL-5
- [ ] No CPL-5-eligible claim appears in Section 4 (check DT6 output for each claim)
- [ ] CPL-2 entries include the mandatory caveat text in the "Required caveat" field
- [ ] No CPL assignment was made without running DT6

### Gate Step 3 — Source Traceability

Every source listed in Section 3 (Evidence Register) must trace to an actual named document in the approved source hierarchy. Every status determination in Section 1 must trace to the Primary source (canonical-product-model.md).

Checklist:
- [ ] canonical-product-model.md is present in Section 3
- [ ] Every other source in Section 3 is named (not "a secondary source" — the actual document name)
- [ ] No source is listed as "Primary" or "Approved Secondary" if it is actually Reference Only or Non-authoritative
- [ ] Section 1 status quotes the canonical model verbatim — not from a secondary source

### Gate Step 4 — Prohibited Source Check

Confirm no prohibited source appears in Section 3 as a basis for status determination.

Checklist:
- [ ] capability-status.md is not in Section 3 as a status authority
- [ ] source-of-truth.md is not in Section 3 as a status authority
- [ ] ethana-status-reconciliation.md is not in Section 3 as a status authority
- [ ] The marketing playbook is not listed as "Primary" or "Approved Secondary" in Section 3
- [ ] If any prohibited source was reviewed, it appears in Section 3 as "Reference Only — not used for status determination"

### Gate Step 5 — Contradiction Completeness

Every source conflict visible in Section 3 (where a source "Contradicts" or "Expands" the canonical model) must have a corresponding entry in Section 6 (Contradiction Log).

Checklist:
- [ ] Count of "Contradicts" or "Expands" rows in Section 3 matches count of entries in Section 6
- [ ] Each Section 6 entry records the adjudication (which source prevailed and why)
- [ ] Each Section 6 entry records the ECS adjustment applied
- [ ] If Section 3 has no contradictions: Section 6 states "No contradictions found across [N] sources examined"

### Gate Step 6 — Scope-Expansion Check

For every claim in Section 4 (Allowed Claims), verify the claim does not expand scope beyond what canonical-product-model.md explicitly confirms.

Common expansion patterns to check for each claim in Section 4:
- **Modality expansion**: claim implies the feature operates on data types the canonical model does not confirm (e.g., text-only feature claimed for all document types)
- **Depth expansion**: claim implies a deeper or more formal capability than confirmed (e.g., a runtime filter claimed as an audit-grade evaluation tool)
- **Certification expansion**: claim implies a certification, compliance standard, or external attestation the canonical model does not confirm as held
- **Coverage expansion**: claim implies broader integration, compatibility, or deployment scope than confirmed (e.g., "all SIEM platforms" when only Splunk, Elastic, and Datadog are confirmed)
- **Performance expansion**: claim states a performance figure not found in canonical-product-model.md

If any expansion is found in a Section 4 entry: remove that entry from Section 4, rewrite it to match canonical scope (if a valid version exists), and add the expanded version to Section 5 as a Prohibited Claim. If no valid in-scope version exists, Section 4 has no entry for this claim — Section 5 gets the prohibition.

### Gate Step 7 — Audit Trail Population

Section 9 (Validation Audit Trail) must be present and complete before output is released.

Checklist:
- [ ] Validation date recorded
- [ ] Claims validated listed verbatim
- [ ] Sources checked listed in order
- [ ] ECS arithmetic noted or referenced to Section 7
- [ ] Final status determination recorded
- [ ] CPL for each Allowed Claim in Section 4 listed in Section 9
- [ ] Hard disqualifiers checked (all seven confirmed not triggered, or the triggered one documented)
- [ ] Phase 9 gate completion confirmed with date
- [ ] Escalation status recorded

**After completing all 7 gate steps:** Write the gate completion line in Section 9: "Phase 9 Mandatory Traceability Gate completed [date]. All 7 steps passed."

If any gate step fails: correct the specific failure, re-run from the failed step, and confirm all subsequent steps are still valid after the correction. Do not release until all 7 steps pass.

---

## Decision Trees

### DT1 — Source Authority Hierarchy

```
Is the capability in canonical-product-model.md?

  YES → canonical-product-model.md is authoritative.
        Record the verbatim entry and status.
        Proceed to Phase 4 for secondary source cross-reference.

  NO  → canonical-product-model.md is authoritative and is silent.
        Status: Unresolved.

        Is the capability in product-architecture-investigation.md?
          YES → Approved Secondary source only.
                ECS Path D: base 15. Cannot establish status.
                Escalate: canonical model update required before any external claim.

        Is the capability in any Reference Only source (playbook, board deck)?
          YES → Reference Only source only.
                ECS Path E: base 5. Cannot establish status.
                Escalate immediately: no claim is permitted.

        Is there any source at all?
          NO  → ECS Path F: ECS = 0.
                Status: Unresolved. Do not claim. Escalate.
```

### DT2 — Status Classification from Canonical Model

```
canonical-product-model.md entry says Production?
  YES → Status: Production.
        Record all mandatory caveats from the canonical entry.
        Mandatory caveats must accompany every Allowed Claim.
        Proceed to Phase 6 (ECS Computation) — Path A applies.

canonical-product-model.md entry says In Build?
  YES → Status: In Build.
        Written Production claim → ECS Path B: ECS = 0 → CPL-5.
        Conversational roadmap mention with explicit In Build disclosure:
          ECS Path A for an accurate In Build disclosure (base 50).
          Apply to "Ethana [capability] is currently In Build — not yet available."
          CPL: CPL-3 (conversation-only).
        Cannot be a proposal deliverable. Cannot be demonstrated in a POC.

canonical-product-model.md entry says Aspirational?
  YES → Status: Aspirational.
        All external claims → ECS Path C: ECS = 0 → CPL-5.
        No external mention in any context without exception.
        May be discussed in Internal Briefing or Engineering Documentation
        with explicit "Aspirational — not on committed roadmap" labelling.

Entry present but status ambiguous or not explicitly labelled?
  → Status: Unresolved.
    Document the ambiguity verbatim.
    Do not interpolate a status. Escalate for canonical model clarification.
```

### DT3 — Contradiction Adjudication

```
Source A (non-canonical) says Production; canonical-product-model.md says In Build:
  → Canonical model prevails. Status: In Build.
    Document: "[Source A] claims Production status.
    canonical-product-model.md classifies as In Build.
    canonical-product-model.md is authoritative. Source A is not."
    ECS adjustment: −20 if Source A is Approved Secondary; −10 if Reference Only.
    Prohibited Claim: Source A's Production language → CPL-5 in Section 5.
    Escalate: recommend Source A be corrected.

Source A (non-canonical) says capability has Feature X;
canonical-product-model.md confirms capability but does not mention Feature X:
  → Status of base capability: as canonical model states.
    Status of Feature X: Unresolved — canonical model is silent.
    Document: "Feature X is not confirmed in canonical-product-model.md.
    Base capability is [status]. Feature X cannot be claimed until canonical model updated."
    ECS for Feature X claim: Path D or E (no canonical entry for this specific claim).
    Feature X → CPL-5 pending canonical model update.

Source A (non-canonical) says Feature X is Production;
canonical-product-model.md says Feature X is In Build:
  → Canonical model prevails. Status of Feature X: In Build.
    Document: "[Source A] claims Feature X is available.
    canonical-product-model.md classifies Feature X as In Build. Source A is incorrect."
    ECS for Feature X Production claim: Path B → ECS = 0 → CPL-5.
    Source A's claim about Feature X: CPL-5 → Prohibited Claim.

Source A omits mandatory caveat that canonical-product-model.md attaches to a capability:
  → Status unchanged (still Production if canonical says so).
    Source A's version of the claim is incomplete, not false.
    Resolution: the claim must include the mandatory caveat to be permitted.
    Without caveat: CPL-2 (requires caveat) or CPL-5 if the caveat is
    material enough that omitting it misrepresents the capability.
    ECS adjustment: −10 (incomplete claim from a Reference Only source).

Both sources are Approved Secondary and directly contradict each other:
  → Canonical model position prevails if it is clear.
    If canonical model is also ambiguous: Status = Unresolved. Escalate.
    Do not adjudicate Production status without canonical model clarity.

No contradiction found:
  → Document: "No contradictions found across [N] sources examined."
    Proceed with no ECS adjustment for contradiction.
```

### DT4 — Scope-Expansion Detection

Run this decision tree for every proposed claim before running DT6. A claim that fails any check receives CPL-5 and goes to Section 5 — do not continue to DT6 for that claim.

```
Check 1 — Modality:
Does the claim imply the capability operates on data types, formats, or inputs
that canonical-product-model.md does not explicitly confirm?

  Example: "PII Scanner detects sensitive data in documents and images"
  when canonical model confirms text outputs only.

  SCOPE EXPANSION → CPL-5. Add to Section 5.
  Reason: Scope expansion — modality not confirmed in canonical model.

  NO EXPANSION → continue.

Check 2 — Depth:
Does the claim imply a deeper, more formal, or more authoritative version of
the capability than the canonical model confirms?

  Example: "Bias Scanner performs statistical model bias audits for regulatory compliance"
  when canonical model confirms runtime text filtering for bias indicators — not audit-grade evaluation.

  SCOPE EXPANSION → CPL-5. Add to Section 5.
  Reason: Scope expansion — depth/formality exceeds canonical confirmation.

  NO EXPANSION → continue.

Check 3 — Certification and Compliance:
Does the claim imply a certification, compliance standard, regulatory attestation,
or external validation that the canonical model does not confirm as currently held?

  Example: "Ethana is ISO 27001 certified" when canonical model says In Build.
  Example: "Ethana is HIPAA compliant" when no HIPAA entry exists.
  Example: "Ethana is RBI-compliant" when no such confirmation exists.

  SCOPE EXPANSION → CPL-5. Add to Section 5.
  Reason: Scope expansion — certification / compliance status not confirmed.
  (This is also a DT2 In Build violation if the standard is In Build — both apply.)

  NO EXPANSION → continue.

Check 4 — Coverage:
Does the claim imply broader integration, compatibility, deployment, or ecosystem
coverage than the canonical model explicitly confirms?

  Example: "Ethana integrates with all major SIEM platforms" when only
  Splunk, Elastic, and Datadog are confirmed.

  Example: "Ethana secures all agent runtimes" when only MCP-compatible
  runtimes are confirmed.

  SCOPE EXPANSION → CPL-5. Add to Section 5.
  Reason: Scope expansion — coverage claim exceeds canonical confirmation.
  Rewrite: replace "all" with the specifically confirmed list.

  NO EXPANSION → continue.

Check 5 — Performance:
Does the claim state a specific performance figure, latency, throughput, or
metric that is not present in canonical-product-model.md?

  Example: "The Gateway adds less than 10ms overhead" when canonical model says ~50ms.
  Example: "Supports 500,000 API calls per day" when no throughput figure is confirmed.

  SCOPE EXPANSION → CPL-5. Add to Section 5.
  Reason: Scope expansion (and potential factual error) — performance figure not in canonical model.
  If a figure IS in canonical model, it is permitted with the exact figure stated.

  NO EXPANSION → continue.

All checks passed:
  → No scope expansion detected. Proceed to DT6 for CPL assignment.
```

### DT5 — Escalation Gate

```
ECS ≥ 65 (Corroborated or Authoritative) AND no open contradiction?
  → No escalation required.
    Record: "No escalation required. ECS [X] ([band])."
    Claim permitted per CPL from DT6.

ECS 45–64 (Canonical-only)?
  → No immediate escalation required.
    Recommend: "Seek engineering corroboration for future confidence improvement.
    Single canonical source. ECS [X] → Canonical-only. Claims at CPL-2 or below."

ECS 20–44 (Contested)?
  → Escalate to canonical model maintainer.
    Message: "Contradiction found: [Source A] and canonical model conflict on [specific point].
    Canonical model position maintained: [position].
    Recommended action: correct or annotate [Source A] to match canonical model.
    Until resolved, claims from this validation restricted to Discovery Conversation and
    Internal Briefing contexts (CPL-3 maximum)."
    Downstream block: Formal Proposal and RFP use blocked until resolved.

ECS < 20 (Insufficient)?
  → Escalate immediately to product team and canonical model maintainer.
    Message: "Capability claim: [claim]. No canonical model entry confirms this.
    Claim source: [source].
    Required action: canonical model update confirming or denying this capability.
    Interim position: [claim] must not be used in any external context.
    Downstream blocks: [list any Solution Mapping or Feature Mapping outputs
    pending this validation]."

Status = Unresolved (capability not in canonical model)?
  → Escalate. Same package as ECS < 20.
    The distinction: the canonical model is silent, not contradicting — the
    escalation message frames this as a gap to fill, not a conflict to resolve.

Status = Aspirational; Production or In Build claim being validated?
  → No escalation path exists. The Aspirational classification is definitive.
    "Status: Aspirational. The proposed claim is prohibited in all contexts.
    No escalation will change the Aspirational status — this is not a gap to fill.
    If the product team has upgraded this capability's status, the canonical model
    must be updated first, then this validation re-run."

Urgency: pre_proposal or pre_poc?
  → Tighten the ECS threshold: claims require ECS ≥ 65 (not 45) before
    use in any formal deliverable. ECS 45–64 → escalate before Formal Proposal use
    even though no immediate escalation would otherwise be triggered.
```

### DT6 — CPL Assignment

**Critical note: CPL is assigned per claim, not per capability.**

The same capability may support multiple claims with different CPLs. A claim with the mandatory caveat embedded may receive CPL-1 while the identical claim without the caveat receives CPL-2. A core capability claim may receive CPL-1 or CPL-2 while a scope-expanded version of that same claim receives CPL-5. Always run DT6 for each individual claim text. Never assign a single CPL to a capability as a whole and apply it to all claims. The CPL belongs to the claim, not the capability.

```
Has DT4 detected scope expansion for this specific claim?
  YES → CPL-5. Add to Section 5. Stop. Do not continue DT6 for this claim.

What is the capability status from DT2?

  Status = Aspirational:
    → CPL-5. All claims prohibited in all contexts. Stop.

  Status = In Build:

    Is this claim a written formal deliverable (proposal, RFP, marketing, contract)?
      YES → CPL-5. In Build cannot be claimed in writing as available. Stop.

    Is this claim a conversational In Build disclosure with explicit
    "not yet available" or "currently in development" language?
      YES → CPL-3. Discovery Conversation and Internal Briefing only.
            Required wording: "Ethana [capability] is currently in development
            and not yet available. No committed delivery date."
            Stop.

    Is there any other form of claim about an In Build capability?
      → CPL-5. Stop.

  Status = Production:

    Has DT2 confirmed Production and has the ECS been computed?

      ECS = Authoritative (85–100):
        Does a mandatory caveat exist in canonical-product-model.md for this capability?

          NO:
            → CPL-1. Unrestricted. Claim is permitted in all contexts as written.

          YES:
            Is the mandatory caveat embedded inline in this specific claim text?
              YES → CPL-1. The claim already carries the qualification.
              NO  → CPL-2. The claim is permitted in formal contexts only.
                           The caveat must be added inline before use.
                           "Required caveat: [caveat text]"

      ECS = Corroborated (65–84):
        Does a mandatory caveat exist?
          NO  → CPL-1.
          YES:
            Is the caveat embedded in this specific claim?
              YES → CPL-1.
              NO  → CPL-2. Add caveat inline before use.

      ECS = Canonical-only (45–64):
        → CPL-2 regardless of caveat status.
          If caveat exists and is not embedded: caveat must be added.
          Single-source confidence — formal proposal use requires explicit note
          "Validated from canonical source — engineering corroboration pending."

      ECS = Contested (20–44):
        → CPL-3. Conversation-only.
          Contradiction exists — formal written use blocked until escalation resolved.
          Must not appear in Section 4 for Formal Proposal or RFP use.

      ECS = Insufficient (0–19):
        → CPL-4 for internal discussion of the uncertainty only.
          CPL-5 for any affirmative claim about this capability.
          No external claim is permitted.

  Status = Unresolved:
    → CPL-4 for internal discussion of what is unknown.
      CPL-5 for any affirmative claim about this capability externally.
      Stop. Escalation required before any external use.
```

---

## Pre-Release Quality Checklist

Complete before releasing any output from this skill. This is separate from but complementary to the Phase 9 gate — the gate is procedural (did you complete the steps?); this checklist is substantive (is the output correct?).

**Claims Firewall:**
- [ ] No Aspirational capability appears in Section 4 (Allowed Claims) in any context
- [ ] No In Build capability appears in Section 4 as a written formal deliverable
- [ ] No certification is claimed in Section 4 that the canonical model does not confirm as held
- [ ] Every entry in Section 4 was individually evaluated through DT4 and DT6

**ECS and CPL:**
- [ ] ECS arithmetic is displayed in Section 7 and is correct (verified in Gate Step 1)
- [ ] Every Section 4 entry has a CPL
- [ ] Every Section 5 entry is tagged CPL-5
- [ ] CPL-2 entries include the caveat text in the "Required caveat" field

**Source Integrity:**
- [ ] canonical-product-model.md appears in Section 3 (Evidence Register)
- [ ] No prohibited source (capability-status.md, source-of-truth.md, ethana-status-reconciliation.md) is used as a status authority
- [ ] All contradictions found in Section 3 are resolved in Section 6

**Phase 9 Gate:**
- [ ] All 7 gate steps completed
- [ ] Gate completion recorded in Section 9 with date
- [ ] No gate step was skipped due to time pressure or abbreviated path (abbreviated path only removes phases, not gate steps)
