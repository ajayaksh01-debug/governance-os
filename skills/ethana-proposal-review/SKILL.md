# Skill: Ethana Proposal Review

**Version:** 1.0  
**Category:** Compliance Gate  
**Owner:** Cursory Governance Team

---

## Purpose

This skill performs a mandatory pre-release compliance audit on any customer-facing document — proposal, RFP response, Statement of Work, or pitch deck — that contains Ethana platform capability claims. It is the terminal enforcement gate for the Claims Firewall, positioned at the end of the commercial chain after all upstream skills have been run.

Where upstream skills (Regulatory Mapping, Governance Control Mapping, Ethana Solution Mapping, Ethana Feature Mapping, Ethana Capability Validation) produce the intelligence and claim language used in a proposal, this skill audits that the proposal's final form respects the boundaries established by those upstream outputs. It does not produce new intelligence — it enforces that existing intelligence was applied correctly.

The skill produces two document-level scores and a Release Classification that determines whether the document may be released to the client:

- **Proposal Compliance Score (PCS):** A 0–100 score reflecting deductions for every Claims Firewall violation, untraced claim, and risk finding detected in the proposal.
- **Claim Traceability Coverage Score (CTCS):** A 0–100 score measuring the percentage of Ethana capability claims in the proposal that successfully trace back to a validated upstream skill output.

**Mandatory authority sources:**
- `knowledge/ethana/canonical-product-model.md` — the sole permitted source for capability status determinations during Sections 4 and 8.
- `docs/decisions/ADR-002-claims-firewall.md` — defines the Claims Firewall policy enforced in Section 8.
- `docs/decisions/ADR-005-proposal-review-gate.md` — establishes this skill as a mandatory, non-bypassable gate and defines the release classification thresholds.

---

## When to Use This Skill

Use this skill when:
- A proposal, RFP response, or SOW is ready to submit and contains any Ethana platform capability claims
- A pitch deck or marketing collateral references specific Ethana production features, certifications, or deployment configurations
- The proposal development workflow has reached Step 4.5 (Proposal Review Gate)
- An existing proposal is being reused or adapted for a new client and its claims need re-validation
- A Conditional Release is being elevated to a formal submission and requires a re-review of the revised sections

Do not bypass this skill. ADR-005 establishes this gate as non-bypassable and mandatory for all customer-facing documents containing Ethana capability claims. No exception process exists short of written sign-off from the Compliance Director, Sales Director, and CISO jointly.

---

## Relationship to Other Skills

This skill is the terminal node of the commercial chain. All other skills are upstream.

| | Solution Mapping | Feature Mapping | Capability Validation | Proposal Review |
|---|---|---|---|---|
| **Question answered** | What can we propose? | Does this feature work here? | Can this be claimed? | Is this proposal safe to release? |
| **Layer** | Commercial | Technical | Truth Gate | Release Gate |
| **Input** | Governance requirements | Feature questions, POC scope | Capability name / claim / source | Draft proposal + upstream skill outputs |
| **Output** | Proposal language + CCS | Technical validation + TFS | Status + ECS + CPL | PCS + CTCS + Release Classification |
| **Audience** | Advisory team | Solution architects | Any claimant | Compliance, Sales Director, Legal |
| **Timing** | Pre-proposal | Pre-POC | Before any claim is made | Before client delivery |
| **Pass threshold** | 70/100 | 85/100 | 90/100 | **95/100** |
| **Primary metric** | CCS | TFS | ECS + CPL | PCS + CTCS |

**Why 95/100?** Errors at this gate reach the client. Every Claims Firewall violation in a delivered proposal creates a compliance liability, damages procurement trust, and may trigger regulatory exposure in BFSI environments. The release standard is the strictest in the skill chain.

---

## Input Specification

### Required Inputs

| Field | Required | Description |
|---|---|---|
| `draft_proposal` | Yes | The complete draft customer-facing document — RFP response, proposal, SOW, or pitch deck — containing Ethana capability claims. All sections that reference Ethana capabilities, platform features, certifications, or deployment configurations must be included. Partial documents cannot receive a valid Release Classification. |
| `solution_mapping_output` | Yes | Full output from `skills/ethana-solution-mapping/`. Section 3 (Proposal-Safe Platform Capabilities) and Section 5 (Prohibited Claims Register) are the primary reference sections for the traceability audit. |
| `feature_mapping_output` | Yes | Full output from `skills/ethana-feature-mapping/`. Section 1 (Feature Validation Table + TFS scores) and Section 6 (Prohibited Feature Claims Register) are the primary reference sections. |

### Contextual Inputs

| Field | Required | Description |
|---|---|---|
| `capability_validation_output` | Strongly Recommended | Output from `skills/ethana-capability-validation/`. Section 4 (Allowed Claims + CPL) and Section 5 (Prohibited Claims) are consulted when a specific capability was formally validated during the engagement. Without this input, CTCS ≥ 95 is not achievable — unvalidated claims can only reach CPL-3 traceability at best. |
| `regulatory_mapping_output` | Recommended | Output from `skills/regulatory-mapping/`. Section 6 (Control Requirements) is the reference for Section 5 of this review (Regulatory Coverage Validation) — confirms regulatory control requirements are addressed in the proposal. |
| `control_mapping_output` | Recommended | Output from `skills/governance-control-mapping/`. Section 10 (Ethana Configuration Guide) is the reference for Section 6 of this review (Control Coverage Validation) — confirms that all Ethana configurations in the proposal align with the designed control specifications. |
| `output_mode` | No | RFP Response / Formal Proposal / Statement of Work / Pitch Deck. Affects the language register in Section 1 and the strictness applied to In Build roadmap mentions — Formal Proposals and SOWs require explicit "Roadmap — not yet available" labels; Pitch Decks may use lighter disclosure language. |
| `customer_sector` | No | BFSI / Healthcare / Government / General Enterprise. BFSI engagements trigger additional certification claim checks (SOC 2, ISO 27001, RBI audit readiness) that are absent in non-regulated sector proposals. |
| `jurisdictions` | No | EU / UK / India. Shapes which regulatory capability claims require jurisdiction-specific disclosure (e.g., "GDPR-compliant" claims require specific scoping in EU; "RBI-audit-ready" claims require specific evidence disclosure in India). |

### Input Format

All upstream skill outputs should be submitted in their complete form — not summarised or excerpted. The traceability audit in Phase 3 requires access to the exact claim language in Section 3 of Solution Mapping, the exact TFS scores in Section 1 of Feature Mapping, and the exact CPL assignments in Section 4 of Capability Validation (where available). Excerpted inputs reduce CTCS and may prevent an Approved classification.

Minimum viable input: draft proposal + solution_mapping_output + feature_mapping_output.

---

## Output Specification

Every review produces the following ten sections. For a single-section abbreviated review, Sections 2, 3, 4, 8, 9, and 10 are sufficient. For a full proposal review, all ten sections are required.

### 1. Executive Assessment

A 200–250 word non-technical summary of the review findings, written for the Sales Director, Compliance Director, and Legal Counsel audience. Covers:
- The document reviewed (type, client, date)
- The total number of capability claims audited
- High-level summary of compliance status (all clear / findings present / firewall breaches detected)
- The Release Classification verdict
- The single most important action required before release (or confirmation that no action is required)

Written last, after all other sections are complete.

### 2. Claim Inventory

A complete numbered catalogue of every Ethana capability claim found in the draft proposal. Each entry:
- **Claim ID**: `CLM-[document abbreviation]-[number]` (e.g., `CLM-RFP-001`)
- **Claim text**: verbatim from the draft proposal, including section reference
- **Claim type**: Production Capability / Certification / Deployment Configuration / Roadmap Item / Integration Claim / Performance Claim
- **Source section in proposal**: the specific proposal section and page or heading where this claim appears

This section is mechanical — it does not assess claims, only catalogues them. Completeness is mandatory. A claim missed here cannot be assessed in Section 3 or flagged in Section 8.

### 3. Claim Traceability Matrix

For every claim in Section 2, the upstream source that validates or prohibits it:

| Claim ID | Claim text (abbreviated) | Upstream source | Section reference | Traceability status |
|---|---|---|---|---|
| CLM-RFP-001 | [...] | solution-mapping Section 3 / feature-mapping Section 1 / capability-validation Section 4 | [specific entry] | Traced / Partially Traced / Untraced / Prohibited |

**Traceability statuses:**
- **Traced**: Claim matches — in scope, language, and status — a validated entry in an upstream skill output
- **Partially Traced**: Claim is directionally consistent with an upstream entry but expands scope, omits a mandatory caveat, or uses unconfirmed language not present in the upstream source
- **Untraced**: No upstream skill output confirms or validates this claim
- **Prohibited**: Claim matches an entry in an upstream skill's Prohibited Claims Register — it must be removed

**CTCS calculation:**
CTCS = (Traced + (Partially Traced × 0.5)) / Total Claims × 100

Untraced and Prohibited claims score 0. Show the arithmetic explicitly — numerator, denominator, and result — before stating the final CTCS.

### 4. Capability Status Validation

A direct audit of every Production capability claim against `knowledge/ethana/canonical-product-model.md`. This section enforces the Claims Firewall independently of the upstream skill audit in Section 3 — it does not trust that upstream skills got the status right; it checks the source directly.

For each unique Ethana capability referenced in the proposal:
- **Capability name**: the specific capability (not product line)
- **Claimed status in proposal**: Production / In Build / Roadmap / "Available" / "Certified"
- **Canonical model status**: verbatim entry from canonical-product-model.md
- **Match verdict**: Confirmed / Mismatch / Scope Expansion / Certification Claim / Not Found
- **Firewall determination**: Compliant / Critical Firewall Breach / Major Finding

Any mismatch, scope expansion beyond the canonical model, or capability not found in canonical-product-model.md is escalated directly to Section 8 (Critical Firewall Breaches) or Section 9 (Major Risk Findings) depending on severity.

### 5. Regulatory Coverage Validation

Confirms that regulatory control requirements identified in Regulatory Mapping Section 6 are addressed in the proposal with appropriate capability claims or Cursory service bridges.

For each regulatory control requirement in the upstream Regulatory Mapping output:
- **Control requirement**: from Regulatory Mapping Section 6
- **How addressed in proposal**: specific proposal section or claim
- **Coverage adequacy**: Fully addressed / Partially addressed / Unaddressed
- **Risk finding**: None / Major (control gap not disclosed) / Minor (coverage language could be strengthened)

Where `regulatory_mapping_output` was not provided as an input, this section states: "Regulatory Coverage Validation not performed — regulatory-mapping output not provided. This section may be omitted for engagements where regulatory mapping was not required."

### 6. Control Coverage Validation

Confirms that control configurations and Ethana platform references in the proposal are consistent with the specifications designed in Governance Control Mapping Section 10 (Ethana Configuration Guide).

For each Ethana configuration or control implementation claim in the proposal:
- **Configuration claim in proposal**: the specific configuration described
- **Control Mapping reference**: the corresponding entry in governance-control-mapping Section 10
- **Consistency verdict**: Consistent / Inconsistent / Configuration Not in Control Mapping
- **Risk finding**: None / Major / Minor

Where `control_mapping_output` was not provided as an input, this section states: "Control Coverage Validation not performed — governance-control-mapping output not provided."

### 7. Commercial Risk Register

Findings that do not constitute Claims Firewall breaches but represent commercial, procurement, or reputational risk if released as-is. Three risk tiers:

**Major Risk Findings (MRF):** Findings that a client procurement team, compliance officer, or regulator would challenge at contract stage. Each MRF carries a -5 point PCS deduction. Examples:
- An In Build capability is disclosed in a section labelled "Current Capabilities" rather than a clearly-labelled Roadmap section
- A Cursory service bridge is described using language implying it is a platform feature
- A performance claim (e.g., "sub-100ms latency") is not sourced to canonical-product-model.md

**Minor Risk Findings:** Findings that a careful reader would notice but that do not constitute misrepresentation. Each Minor Finding carries a -1 point PCS deduction. Examples:
- A caveat required by canonical-product-model.md is present but buried in a footnote rather than inline
- An Ethana product tier (Build vs. Edge) is named without clarifying which tier is being proposed
- A deployment constraint is omitted from a section that would typically include it

**Advisory Notes (no deduction):** Observations that do not affect the score but should be addressed before the next proposal cycle.

### 8. Critical Firewall Breaches (CFB)

Every Critical Firewall Breach detected during the review. A CFB triggers automatic Rejection — a single CFB overrides the PCS score and renders the Release Classification Rejected regardless of the numeric total.

For each CFB:
- **CFB ID**: `CFB-[number]`
- **Breach type**: Aspirational as Production / In Build as Production / Uncertified as Certified / Scope Expansion / Prohibited Claim Used / No Upstream Traceability / Canonical Model Not Consulted
- **Proposal location**: section and verbatim text from the draft
- **Canonical model status**: verbatim entry from canonical-product-model.md (or "Not found")
- **Why this is a breach**: the specific ADR-002 or ADR-005 provision violated
- **Required action**: exact corrective action (remove claim / reclassify as Roadmap / add explicit disclosure / substitute with compliant language)

If no CFBs are found: "No Critical Firewall Breaches detected across [N] claims audited against canonical-product-model.md."

### 9. Major Risk Findings (MRF)

A consolidated view of all Major Risk Findings from Section 7, structured for the revision team. For each MRF:
- **MRF ID**: `MRF-[number]`
- **Finding description**: what was found and where
- **Risk if unaddressed**: the specific procurement, compliance, or reputational consequence
- **Required action**: specific corrective action with the target section of the proposal
- **PCS deduction**: -5 points per MRF

If no MRFs: "No Major Risk Findings detected."

### 10. Release Decision

The final release verdict, scores, and traceability gate confirmation.

**Traceability Gate (TG-1 through TG-7):**

| Gate | Step | Status |
|---|---|---|
| TG-1 | Draft proposal confirmed complete — all sections included | Pass / Fail |
| TG-2 | Solution Mapping output (Section 3 + Section 5) confirmed available | Pass / Fail |
| TG-3 | Feature Mapping output (Section 1 + Section 6) confirmed available | Pass / Fail |
| TG-4 | Capability Validation output (Section 4 + Section 5) confirmed available or absence noted with rationale | Pass / Noted absent |
| TG-5 | Regulatory Mapping output (Section 6) confirmed available or absence noted with rationale | Pass / Noted absent |
| TG-6 | Governance Control Mapping output (Section 10) confirmed available or absence noted with rationale | Pass / Noted absent |
| TG-7 | canonical-product-model.md directly consulted — at least one verbatim quote recorded in Section 4 | Pass / Fail |

All Pass gates (TG-1, TG-2, TG-3, TG-7) must be confirmed before a Release Classification may be issued.

**Scoring:**

```
Base PCS:                        100
Critical Firewall Breaches:      [count] × auto-reject (if any CFB: PCS = 0)
Major Risk Findings (MRF):       [count] × -5 = -[total]
Minor Risk Findings:             [count] × -1 = -[total]
                                 ─────────────────────────
Final PCS:                       [score] / 100

Total claims audited:            [N]
Claims with Traced status:       [n]
Claims with Partially Traced:    [p] × 0.5 = [p/2]
CTCS numerator:                  n + (p/2)
CTCS:                            ([n + p/2] / [N]) × 100 = [score] / 100
```

**Release Classification:**

| Classification | PCS | CTCS | Conditions |
|---|---|---|---|
| **Approved** | ≥ 98 | ≥ 95 | No CFBs. No MRFs. Document may be released as-is. |
| **Approved with Revisions** | ≥ 95 | ≥ 80 | No CFBs. MRFs must be addressed before release. Document may not be sent until revisions are complete and a follow-up spot-check is conducted. |
| **Conditional Release** | ≥ 80 | ≥ 60 | No CFBs. Material MRFs present. Document may be shared internally only. External release requires re-review after corrections. |
| **Rejected** | < 80 or any CFB | Any | Document is blocked from release. If CFBs are present, they must be corrected and a full re-review run before the document may be re-submitted. |

**Release Audit Certificate:**

```
Proposal Review — Release Audit Certificate
──────────────────────────────────────────────────────────
Document reviewed:    [Document name / client / date]
Reviewer:             Ethana Proposal Review Skill v1.0
Review date:          [Date]
Total claims audited: [N]
Critical Firewall Breaches: [count]
Major Risk Findings:  [count]
Minor Risk Findings:  [count]
PCS:                  [score] / 100
CTCS:                 [score] / 100
Traceability Gate:    Completed [date] — all mandatory gates passed
Release Classification: [Approved / Approved with Revisions /
                         Conditional Release / Rejected]
──────────────────────────────────────────────────────────
[If Rejected or Conditional]: Required actions before re-submission:
[numbered list from Section 8 and Section 9]
```

---

## PCS and CTCS — Two Separate Scoring Constructs

Understanding the distinction is essential for applying this skill correctly.

**PCS (Proposal Compliance Score):** A document-level score (0–100) measuring whether every capability claim in the proposal respects the Claims Firewall. PCS is reduced by every compliance failure — a CFB drops PCS to 0; each MRF deducts 5 points; each Minor Finding deducts 1 point. PCS measures "is the document compliant?"

**CTCS (Claim Traceability Coverage Score):** A coverage score (0–100) measuring the proportion of claims that trace back to validated upstream skill outputs. CTCS is independent of whether those claims are compliant — a document can have Traced claims that are still wrong if the upstream skill made an error. CTCS measures "was upstream validation actually applied?"

**The critical relationship:** A high PCS with a low CTCS indicates that the proposal is currently compliant but relies on undocumented judgement rather than validated upstream outputs — it is structurally fragile and will likely fail a future re-review or client audit. A low PCS with a high CTCS indicates that upstream validation was run correctly but the proposal authors did not respect its outputs. Both conditions produce a Release Classification below Approved.

**Why CTCS ≥ 95 is required for Approved:** At CTCS 95, fewer than 5% of claims are untraced. In a 20-claim proposal, that is one claim. At CTCS 80, 4 claims have no upstream validation. In a regulated enterprise procurement environment where each claim may be subject to vendor audit, 4 untraced claims represent unacceptable exposure.

---

## Absolute Release Rule

**Any Critical Firewall Breach (CFB) automatically results in Release Classification = Rejected regardless of PCS or CTCS.**

This rule cannot be overridden by any commercial, time, or stakeholder pressure. A single CFB detected in Section 8 renders the document Rejected. The PCS and CTCS values are still computed and recorded in Section 10 to document the scope of findings, but they do not affect the Release Classification — it is Rejected.

A document may only exit Rejected status after:
1. All CFBs identified in Section 8 have been corrected in the draft proposal
2. A full re-review from Phase 1 of the workflow has been completed
3. The re-review produces a Section 8 confirming zero CFBs

Authority: ADR-005 §3 — Zero-Tolerance Firewall Gate.

---

## Constraints and Scope

**In scope:**
- Customer-facing documents containing Ethana platform capability claims
- RFP responses, formal proposals, Statements of Work, pitch decks, technical addenda, and executive summaries
- Any document that, if sent to a client, would constitute a commercial representation of Ethana capabilities
- Re-reviews of revised documents following Approved with Revisions or Rejected classifications

**Out of scope:**
- Internal advisory documents that are not sent to clients (these may use CPL-3 or CPL-4 language per the Capability Validation framework)
- Documents that reference Ethana in passing as a vendor name without making capability claims
- Legal contract language drafted by qualified legal counsel — commercial capability claims embedded in contracts are in scope; standard legal terms and indemnities are not
- Reviewing upstream skill quality — this skill accepts upstream outputs as-is; if an upstream skill made an error, it is flagged as a CFB or MRF here but the fix is applied in the upstream skill, not in this review

**Hard constraint — Claims Firewall:**
canonical-product-model.md is the only source that can establish Production status in Section 4. No upstream skill output, marketing document, board deck, or verbal claim can override it. If canonical-product-model.md and an upstream skill output conflict, canonical-product-model.md governs and a CFB is raised.

**Depth calibration:**
- Single-section spot check (pre-submission check on one RFP response section) → abbreviated path: Sections 2, 3, 4, 8, 9, 10 — 30–35 minutes
- Full proposal review (complete draft, all upstream outputs available) → all ten sections — 80–95 minutes
- High-complexity RFP (20+ capability claims, multiple jurisdictions, BFSI sector) → all ten sections at maximum depth — 2–3 hours

**Non-bypassability:**
ADR-005 establishes this gate as mandatory and non-bypassable. No Release Classification of Approved or Approved with Revisions may be issued by any other means. A document sent to a client without a Release Audit Certificate from this skill constitutes a Claims Firewall bypass — a compliance breach regardless of whether the document's content was compliant.

---

## Knowledge Dependencies

### Tier 1 — PRIMARY (mandatory for every invocation)

- `knowledge/ethana/canonical-product-model.md` — the sole permitted source for capability status verification in Section 4. Do not rely solely on upstream skill outputs for status confirmation — always check the canonical model directly.
- `docs/decisions/ADR-002-claims-firewall.md` — the policy authority defining what constitutes a Claims Firewall breach.
- `docs/decisions/ADR-005-proposal-review-gate.md` — the policy authority defining release classification thresholds, hard disqualifiers, and the mandatory traceability gate.

### Tier 2 — UPSTREAM SKILL OUTPUTS (required as inputs)

- `skills/ethana-solution-mapping/` Section 3 and Section 5 — primary traceability references
- `skills/ethana-feature-mapping/` Section 1 and Section 6 — technical traceability references
- `skills/ethana-capability-validation/` Section 4 and Section 5 — CPL-grounded traceability references (when available)

### Tier 3 — CONTEXTUAL REFERENCES (when relevant inputs are provided)

- `skills/regulatory-mapping/` Section 6 — regulatory control requirements for Section 5 validation
- `skills/governance-control-mapping/` Section 10 — Ethana configuration specifications for Section 6 validation
- `knowledge/ethana/framework-crosswalk.md` — framework-to-capability mapping reference; useful when a proposal makes ISO 42001 or NIST AI RMF alignment claims

### Tier 4 — PROHIBITED SOURCES (must not be used as authority for status determination)

- `knowledge/ethana/capability-status.md` — prior derived file; not canonical; archived
- `knowledge/ethana/source-of-truth.md` — prior derived file; not canonical; archived
- `knowledge/ethana/ethana-status-reconciliation.md` — prior reconciliation file; not canonical; archived
- Marketing playbook — commercial language reference only; cannot establish capability status

---

## Related Skills

- `skills/ethana-solution-mapping/` — upstream: produces Section 3 (Proposal-Safe Platform Capabilities) that is the primary traceability reference for this review
- `skills/ethana-feature-mapping/` — upstream: produces Section 1 (Feature Validation Table) and Section 6 (Prohibited Feature Claims Register) used in traceability audit
- `skills/ethana-capability-validation/` — upstream: produces Section 4 (Allowed Claims + CPL) used for claim-level traceability when formal validation was run
- `skills/regulatory-mapping/` — upstream: produces Section 6 (Control Requirements) used in Section 5 (Regulatory Coverage Validation)
- `skills/governance-control-mapping/` — upstream: produces Section 10 (Ethana Configuration Guide) used in Section 6 (Control Coverage Validation)
