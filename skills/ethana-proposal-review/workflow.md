# Ethana Proposal Review — Workflow

## Overview

This workflow defines the step-by-step process for executing the Ethana Proposal Review skill. It is the terminal gate in the commercial chain and must be completed before any customer-facing document containing Ethana capability claims is released.

The workflow has seven phases. Each phase has defined inputs, procedures, outputs, and quality gates. A full review of a complete proposal typically takes 80–95 minutes when all upstream skill outputs are available. A single-section abbreviated review takes 30–35 minutes.

The Mandatory Traceability Gate (TG-1 through TG-7) is completed in Phase 1 before any substantive review begins. The hard disqualifier check (HD1 through HD7) is completed in Phase 4 (Claims Firewall Gate) and in Phase 6 (scoring). Do not issue a Release Classification without completing both.

---

## Absolute Release Rule

**Any Critical Firewall Breach (CFB) automatically results in Release Classification = Rejected regardless of PCS or CTCS.**

This rule applies at every point in the workflow. Phase 4 is the primary CFB detection phase, but a CFB may surface at any step. When a CFB is confirmed, record it immediately in Section 8 and continue through all remaining phases to document the full picture. Do not halt the review early on a CFB — complete all sections before issuing the Rejected classification. CTCS and PCS are still calculated and recorded.

---

## Phase 1 — Intake & Traceability Gate

**Objective:** Confirm that all required inputs are present and that the review can proceed with integrity.

### Step 1.1 — Execute the Mandatory Traceability Gate

Complete TG-1 through TG-7 in order. Do not proceed to Phase 2 if TG-1, TG-2, TG-3, or TG-7 fails.

| Gate | Check | Action if failed |
|---|---|---|
| TG-1 | Draft proposal is complete — all sections that contain Ethana capability claims are present | Stop. Request the complete document. A partial document cannot receive a valid Release Classification. |
| TG-2 | Solution Mapping output is available and includes Section 3 and Section 5 | Stop. Run `skills/ethana-solution-mapping/` first or obtain the output from the engagement team. |
| TG-3 | Feature Mapping output is available and includes Section 1 and Section 6 | Stop. Run `skills/ethana-feature-mapping/` first or obtain the output from the engagement team. |
| TG-4 | Capability Validation output availability confirmed | If available: load Section 4 and Section 5. If not available: note in Phase 3 that CTCS is capped — unvalidated claims cannot receive Traced status. |
| TG-5 | Regulatory Mapping output availability confirmed | If available: load Section 6. If not available: note that Section 5 (Regulatory Coverage Validation) will be skipped. |
| TG-6 | Governance Control Mapping output availability confirmed | If available: load Section 10. If not available: note that Section 6 (Control Coverage Validation) will be skipped. |
| TG-7 | canonical-product-model.md is directly accessible — confirm it will be consulted in Phase 4 | If inaccessible: stop. This file is mandatory for the Claims Firewall Gate. A review without direct access to the canonical model cannot issue a compliant Release Classification. |

Record the gate result for each step. TG-4, TG-5, and TG-6 may note "absent — section skipped" without blocking the review. TG-1, TG-2, TG-3, and TG-7 are mandatory pass conditions.

### Step 1.2 — Load and Segment the Proposal

Read the full draft proposal. Identify:
- Every section that contains an Ethana capability claim
- Every section that references platform certifications, compliance standards, or deployment configurations
- Sections that reference Cursory services or advisory deliverables (these are in scope if they frame Ethana platform capabilities)

Note the total section count and the sections that will be audited. Sections containing no Ethana capability claims are noted as "out of scope for capability audit" but are not omitted from Section 1 (Executive Assessment).

### Step 1.3 — Assess Input Completeness

Rate the input quality for this review:

| Rating | Condition | Effect on CTCS ceiling |
|---|---|---|
| Full | All six inputs present (draft, solution mapping, feature mapping, capability validation, regulatory mapping, control mapping) | CTCS ceiling: 100 |
| Standard | Draft + solution mapping + feature mapping present; capability validation absent | CTCS ceiling: ~80 (unvalidated claims cannot be Traced) |
| Minimal | Draft + solution mapping + feature mapping present; remaining inputs absent | CTCS ceiling: ~70; Sections 5 and 6 skipped |

Record the input completeness rating. It will be noted in Section 1 (Executive Assessment) and Section 10 (Release Decision).

### Phase 1 Output
- Traceability Gate (TG-1 through TG-7) completion record
- Input completeness rating
- List of proposal sections in scope for capability audit
- Go / stop decision

---

## Phase 2 — Claim Inventory Construction

**Objective:** Produce a complete, numbered catalogue of every Ethana capability claim in the proposal. No assessment in this phase — only enumeration.

### Step 2.1 — Read Each In-Scope Section

For each section identified in Step 1.2, read the full text and extract every sentence or phrase that:
- Names a specific Ethana feature or capability (Immutable Audit Log, Runtime Guardrails, LLM Gateway, Red Teaming Orchestrator, MCP Security Broker, Bias Scanner, etc.)
- Makes a claim about platform status (e.g., "Production," "available," "deployed," "certified," "compliant")
- References a deployment model, throughput figure, integration target, or SLA attributable to Ethana
- Claims a certification or compliance standard for Ethana or Cursory (SOC 2, ISO 27001, GDPR-compliant)
- References Ethana Edge, Ethana Build, Ethana Sentry, or Workspace by capability

### Step 2.2 — Assign Claim IDs

Number all extracted claims sequentially: `CLM-[DOC]-001`, `CLM-[DOC]-002`, etc. Where DOC is a 2-4 character abbreviation of the document type (e.g., RFP, SOW, PROP, DECK).

Record for each: the verbatim text, the claim type (from the taxonomy in SKILL.md Section 2), and the proposal section where it appears.

### Step 2.3 — Check for Completeness

Apply the completeness test:
- [ ] Every Ethana product name in the document has at least one claim entry
- [ ] Every certification or compliance reference is captured as a Certification claim type
- [ ] Every performance figure attributed to Ethana is captured as a Performance Claim type
- [ ] No claim has been omitted because it appeared in a boilerplate or standard section

A claim missed here cannot be assessed in Phase 3 or flagged in Phase 4. Completeness in this phase determines the integrity of the CTCS calculation.

### Phase 2 Output
- Section 2 (Claim Inventory): complete numbered catalogue
- Total claim count

---

## Phase 3 — Claim Traceability Audit

**Objective:** For every claim in Section 2, identify the upstream source that confirms, partially confirms, or prohibits it.

### Step 3.1 — Match Each Claim to Upstream Outputs

For each claim in the Claim Inventory, search the upstream outputs in priority order:

1. **Capability Validation Section 4** (Allowed Claims): Does an Allowed Claim entry match or encompass this claim's language and scope? If yes → **Traced** (CPL-grounded).
2. **Solution Mapping Section 3** (Proposal-Safe Platform Capabilities): Does the claim match a specific quotable entry? If yes → **Traced**.
3. **Feature Mapping Section 1** (Feature Validation Table, TFS ≥ 70): Does the claim reference a feature with a Viable or Ready TFS? If yes → **Traced**.
4. **Capability Validation Section 5** or **Solution Mapping Section 5** or **Feature Mapping Section 6** (Prohibited Claims Registers): Does the claim match a prohibited entry? If yes → **Prohibited**.
5. No match in any upstream output → **Untraced**.

If a claim is directionally consistent with an upstream source but expands scope, omits a mandatory caveat, or uses language not present in the upstream output → **Partially Traced**.

### Step 3.2 — Document Each Traceability Assignment

Complete the Claim Traceability Matrix (Section 3 of the output) for every claim. Every assignment must cite the specific upstream output section and entry — not "see solution mapping" but "solution-mapping Section 3, entry: 'Ethana's Immutable Audit Log captures every gateway-routed AI call...'"

### Step 3.3 — Calculate CTCS

CTCS = (Traced + (Partially Traced × 0.5)) / Total Claims × 100

Write the arithmetic explicitly:
- Traced count: [n]
- Partially Traced count: [p], contributing [p × 0.5]
- Untraced count: [u]
- Prohibited count: [r]
- Total: [n + p + u + r] must equal total from Phase 2
- CTCS: ([n + p/2] / total) × 100

A CTCS below 60 indicates that fewer than 60% of the proposal's capability claims are grounded in validated upstream outputs. This will result in a Conditional Release at best regardless of the PCS.

### Phase 3 Output
- Section 3 (Claim Traceability Matrix): complete for all claims
- CTCS value with arithmetic

---

## Phase 4 — Claims Firewall Gate (Capability Status Validation)

**Objective:** Directly audit every Production capability claim against canonical-product-model.md. This is the hard disqualifier check — it is independent of the traceability audit and must be run even if all claims received Traced status in Phase 3.

### Step 4.1 — Open canonical-product-model.md

Open `knowledge/ethana/canonical-product-model.md` directly. Do not rely on upstream skill outputs for status determination in this phase — they have already been assessed for traceability; this phase checks the ground truth.

### Step 4.2 — Check Each Unique Capability

For each unique Ethana capability referenced in the proposal (not each claim — one capability may appear in multiple claims):

1. Locate the capability in canonical-product-model.md
2. Read its canonical status: Production / In Build / Aspirational / Not Found
3. Compare against how it is presented in the proposal

Apply the hard disqualifier triggers:

**HD1 — Aspirational as Production:**
If the proposal presents an Aspirational capability (e.g., Workspace, Visual Agent Builder, any capability listed as Aspirational in canonical-product-model.md) as currently available, active, or deployable → CFB.

**HD2 — In Build as Production:**
If the proposal presents an In Build capability as currently available, certified, or deployable without an explicit "In Build — roadmap, not yet available" disclosure → CFB.
If the In Build capability is disclosed in a clearly labelled Roadmap section with no delivery commitment → not a CFB (may be an MRF depending on context).

**HD3 — Certification Claimed Without Evidence:**
If the proposal states that Ethana or Cursory holds a certification (SOC 2 Type II, ISO 27001, ISO 42001) that is not confirmed as currently held in canonical-product-model.md → CFB.

**HD4 — Scope Expansion:**
If the proposal attributes capabilities, performance characteristics, modalities, or integrations to a Production feature that canonical-product-model.md does not explicitly confirm → CFB if material; MRF if minor.

**HD5 — Capability Not Found:**
If a capability is referenced in the proposal and has no entry in canonical-product-model.md → CFB. Do not invent or infer status.

### Step 4.3 — Record Firewall Determination

For each unique capability: record the canonical status, the proposal claim, and the firewall determination (Compliant / CFB / MRF / Minor). Populate Section 4 (Capability Status Validation).

For every CFB identified: immediately draft the Section 8 entry with the required fields.

### Phase 4 Output
- Section 4 (Capability Status Validation): complete with verbatim canonical model quotes
- Section 8 (Critical Firewall Breaches): populated for all CFBs found
- Hard disqualifier check: HD1 through HD5 applied

---

## Phase 5 — Regulatory & Control Coverage Validation

**Objective:** Confirm that the proposal addresses the regulatory requirements and control specifications established by upstream governance skills. Skip if the relevant inputs were not provided.

### Step 5.1 — Regulatory Coverage Check

If `regulatory_mapping_output` was provided:

For each control requirement in Regulatory Mapping Section 6:
- Identify which proposal section or claim addresses this requirement
- Assess adequacy: is the requirement addressed with a Production Ethana capability, a Cursory service bridge, or acknowledged as a customer-owned control?
- Flag: if a mandatory control requirement is not addressed in the proposal and not acknowledged as a gap → Major Risk Finding

Record findings in Section 5 (Regulatory Coverage Validation).

### Step 5.2 — Control Configuration Check

If `control_mapping_output` was provided:

For each Ethana configuration described in Governance Control Mapping Section 10:
- Identify the corresponding proposal section that references this configuration
- Assess consistency: does the proposal's description of the configuration match the specification in Section 10?
- Flag: if a configuration in the proposal contradicts the control specification (e.g., the control spec requires Fail-Closed but the proposal describes optional configuration) → Major Risk Finding

Record findings in Section 6 (Control Coverage Validation).

### Phase 5 Output
- Section 5 (Regulatory Coverage Validation)
- Section 6 (Control Coverage Validation)

---

## Phase 6 — Risk Classification & Scoring

**Objective:** Classify all remaining findings, populate the Commercial Risk Register, and compute the PCS.

### Step 6.1 — Classify Remaining Findings

Review all Partially Traced claims from Phase 3 and all Minor findings from Phase 4 and Phase 5. Classify each as:
- **Major Risk Finding (MRF):** Commercial, procurement, or regulatory risk that a client team would challenge — -5 points PCS deduction each
- **Minor Risk Finding:** Style or precision issue that careful readers would notice — -1 point PCS deduction each
- **Advisory Note:** Observation with no score deduction

Populate Section 7 (Commercial Risk Register) with all MRFs, Minor Findings, and Advisory Notes.

### Step 6.2 — Apply Hard Disqualifiers HD6 and HD7

**HD6 — Mandatory Traceability Gate Not Completed:**
Confirm that TG-1, TG-2, TG-3, and TG-7 were completed and passed (verified in Phase 1). If any mandatory gate was not completed → automatic Rejected classification; do not score.

**HD7 — Incomplete Proposal Audit:**
Confirm that every proposal section containing an Ethana capability claim was included in the Claim Inventory (Phase 2). If any section containing claims was excluded from the audit → the review is incomplete; do not issue a Release Classification. Restart from Phase 2 with the full document.

### Step 6.3 — Compute PCS

```
Base PCS:                          100
CFBs detected:                     [count]
  → If any CFB: PCS = 0 (auto-Rejected)
  → If no CFBs: continue scoring
MRFs (from Section 9):             [count] × -5 = -[total]
Minor Findings (from Section 7):   [count] × -1 = -[total]
Final PCS:                         [score] / 100
```

### Phase 6 Output
- Section 7 (Commercial Risk Register): complete
- Section 9 (Major Risk Findings): consolidated
- PCS with arithmetic
- HD6 and HD7 checked

---

## Phase 7 — Release Decision & Release Audit Certificate

**Objective:** Issue the Release Classification and produce the Release Audit Certificate.

### Step 7.1 — Determine Release Classification

Apply the threshold table from SKILL.md:

| Classification | Required PCS | Required CTCS | Additional conditions |
|---|---|---|---|
| Approved | ≥ 98 | ≥ 95 | No CFBs, no MRFs |
| Approved with Revisions | ≥ 95 | ≥ 80 | No CFBs; MRFs must be corrected before external release |
| Conditional Release | ≥ 80 | ≥ 60 | No CFBs; internal use only; re-review required before external release |
| Rejected | < 80 or any CFB | Any | Document blocked from release |

Both PCS and CTCS thresholds must be met. A document scoring PCS 97, CTCS 72 cannot receive Approved — it receives Approved with Revisions (if PCS ≥ 95) or Conditional Release (if CTCS < 80).

### Step 7.2 — Write Section 1 (Executive Assessment)

Write last. Summarise the review findings in 200–250 words. Cover:
- Document type, client, and date
- Total claims audited
- Summary of compliance status
- The Release Classification and its immediate implication
- The single most important action (if not Approved)

### Step 7.3 — Confirm Traceability Gate Record in Section 10

Populate the Section 10 Traceability Gate table with the results from Phase 1. Complete the Release Audit Certificate with all fields filled. The certificate must include:
- All score fields (PCS, CTCS)
- CFB count, MRF count, Minor Finding count
- Gate completion confirmation
- Release Classification
- Required actions before re-submission (if Rejected or Conditional Release)

### Step 7.4 — Final Quality Check

Before releasing the completed review, verify:
- [ ] All 10 output sections are present
- [ ] Every claim in Section 2 has a traceability entry in Section 3
- [ ] Every unique capability in Section 3 has a firewall determination in Section 4
- [ ] Every CFB in Section 8 has a specific corrective action
- [ ] PCS arithmetic is correct and traceable
- [ ] CTCS arithmetic shows numerator, denominator, and result
- [ ] Release Classification is consistent with PCS and CTCS values
- [ ] Release Audit Certificate is complete
- [ ] Section 1 (Executive Assessment) was written after all other sections

---

## Output Document Structure

```markdown
# Ethana Proposal Review: [Document Name] — [Client] — [Date]

**Review Date:** [Date]
**Document Type:** [RFP Response / Formal Proposal / SOW / Pitch Deck]
**Client:** [Client name and sector]
**Input Completeness:** [Full / Standard / Minimal]
**Review Status:** [Final / Preliminary]

---

## 1. Executive Assessment
[200–250 words]

## 2. Claim Inventory
[Table: Claim ID | Claim text | Claim type | Proposal section]

## 3. Claim Traceability Matrix
[Table: Claim ID | Claim text | Upstream source | Section ref | Status]
CTCS: [arithmetic and result]

## 4. Capability Status Validation
[Per-capability table: Capability | Claimed status | Canonical status | Match verdict | Firewall determination]

## 5. Regulatory Coverage Validation
[Per-requirement table or "Section skipped — regulatory-mapping output not provided"]

## 6. Control Coverage Validation
[Per-configuration table or "Section skipped — control-mapping output not provided"]

## 7. Commercial Risk Register
### Major Risk Findings
[MRF entries or "No MRFs detected"]
### Minor Risk Findings
[Minor Finding entries or "No Minor Findings detected"]
### Advisory Notes
[Notes or "None"]

## 8. Critical Firewall Breaches
[CFB entries or "No Critical Firewall Breaches detected"]

## 9. Major Risk Findings (Consolidated)
[Consolidated MRF list with required actions or "No Major Risk Findings detected"]

## 10. Release Decision
### Traceability Gate
[TG-1 through TG-7 table]
### Scoring
[PCS arithmetic]
[CTCS arithmetic]
### Release Classification
[Approved / Approved with Revisions / Conditional Release / Rejected]
### Release Audit Certificate
[Certificate block]
```

---

## Time Estimates

| Scenario | Input Completeness | Estimated Time |
|---|---|---|
| Full proposal review, all inputs available | Full | 80–95 minutes |
| Full proposal review, capability validation absent | Standard | 65–80 minutes |
| Full proposal review, only draft + solution + feature mapping | Minimal | 55–70 minutes |
| Single-section spot check (abbreviated path) | Any | 30–35 minutes |
| High-complexity RFP (20+ claims, multi-jurisdiction BFSI) | Full | 2–3 hours |
| Re-review after corrections (Rejected → re-submission) | Full | 40–60 minutes |

---

## Schema Integration

### Input Schema

Input payloads for this skill must conform to `workflows/schemas/proposal-review-input.schema.json`. The three required fields are `draft_proposal`, `solution_mapping_output`, and `feature_mapping_output`. Validate before Phase 1:

```bash
python evaluations/scripts/workflow_validator.py path/to/input.json workflows/schemas/proposal-review-input.schema.json
```

### Output Schema

Every completed review must serialize the Release Decision (Section 10) to a structured payload conforming to `workflows/schemas/proposal-review-output.schema.json`. Required minimum fields:

```json
{
  "pcs": 0,
  "ctcs": 0,
  "classification": "Approved|Approved with Revisions|Conditional Release|Rejected",
  "cfb_count": 0,
  "mrf_count": 0,
  "minor_count": 0,
  "traceability_gate_passed": true
}
```

Validate before routing to the Ethana Proposal Agent or any downstream orchestration step:

```bash
python evaluations/scripts/workflow_validator.py path/to/output.json workflows/schemas/proposal-review-output.schema.json
```
