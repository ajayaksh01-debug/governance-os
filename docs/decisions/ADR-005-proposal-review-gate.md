# Architecture Decision Record: ADR-005

## Title
ADR-005: Mandatory Proposal Review Release Gate

---

## Status
**Accepted**

---

## Context
Sales discovery, RFP responses, Statements of Work (SOWs), and formal proposals are the primary interface where Ethana platform capabilities are committed to clients. Historically, these documents have faced significant commercial pressure to over-promise unreleased features, roadmap items, or speculative integrations to win competitive deals. 

In highly regulated enterprise sectors (e.g., Banking, Financial Services, and Insurance [BFSI] subject to RBI outsourcing guidelines, FCA/PRA supervision, or the EU AI Act), making inaccurate technical commitments or claiming non-existent certifications (such as SOC 2 Type II or ISO 27001 before they are formally obtained) represents an unacceptable compliance liability. Once a non-compliant claim is sent to a client, it cannot be easily corrected downstream and results in broken procurement trust, failed vendor audits, and legal exposure.

Previous workflows lacked a systematic, standardized pre-release validation gate, relying instead on ad-hoc manual reviews. This resulted in inconsistent enforcement of the Claims Firewall and left the company exposed to capability inflation.

---

## Decision
Establish **Proposal Review** as a mandatory, non-bypassable pre-release gate for any customer-facing document (proposals, RFPs, SOWs, pitch decks) containing Ethana capability claims. 

1. **Mandatory Audit against Upstream Truth:** Every product claim in a draft must be audited and traced back to validated upstream outputs:
   - **Capability Validation** (for capability status and Claim Permission Levels [CPL]).
   - **Solution Mapping** (for proposal-safe phrasing and Coverage Confidence Scores [CCS]).
   - **Feature Mapping** (for deployment constraints and Technical Fit Scores [TFS]).
2. **Automated Metrics & Classification:** Every document must receive two document-level scores and a release classification:
   - **Proposal Compliance Score (PCS):** A 0-100 score reflecting deductions for Claims Firewall violations (Critical Firewall Breaches [CFBs], Major/Minor Risk Findings).
   - **Claim Traceability Coverage Score (CTCS):** A 0-100 score measuring the percentage of claims that successfully map to a validated upstream output.
   - **Release Classification:** A final verdict categorized as *Approved* (PCS $\ge 98$, CTCS $\ge 95$), *Approved with Revisions* (PCS $\ge 95$, CTCS $\ge 80$), *Conditional Release* (PCS $\ge 80$, CTCS $\ge 60$, internal use only), or *Rejected* (PCS $< 80$ or any CFB present).
3. **Strict Zero-Tolerance Firewall Gate:** Any Critical Firewall Breach (such as claiming Aspirational features like Workspace as Production, or claiming unheld security certifications) results in an automatic **Rejected** classification, blocking the document's release.
4. **Mandatory Traceability Gate & Hard Disqualifiers:** A set of 7 Traceability Gate steps (TG-1 through TG-7) and 7 Hard Disqualifiers (HD1 through HD7) must be checked before scoring to ensure the review process itself was not bypassed or corrupted (e.g., failing to consult [canonical-product-model.md](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md)).

---

## Consequences
- **Positive:**
  - Prevents non-compliant proposals or unvalidated platform claims from reaching clients.
  - Protects procurement trust and ensures 100% alignment with actual engineering capability status.
  - Automatically identifies capability gaps, forcing sales teams to position advisory services (e.g., Cursory services) to bridge those gaps.
  - Enforces auditability and compliance through a standardized Release Audit Certificate.
- **Negative:**
  - Adds an operational step (estimated at 80-95 minutes for a full review, or 30-35 minutes for an abbreviated single-section review) to the proposal development workflow.
  - Creates a hard dependency on upstream skill outputs; a proposal review cannot complete with high traceability if Capability Validation, Solution Mapping, or Feature Mapping have not been run.

---

## Alternatives Considered
- **Post-Release Compliance Auditing:** Rejected. Auditing documents after they are delivered to the customer does not prevent the initial compliance breach or the damage to client trust.
- **Ad-Hoc Human Peer Review:** Rejected. Relying solely on manual oversight is slow, expensive, inconsistent, and highly prone to missing subtle technical over-claims or omitted caveats.
- **Soft Warnings (Non-Blocking Firewall):** Rejected. Allowing documents with Claims Firewall violations to be released with a warning introduces unacceptable legal and regulatory risk in audited enterprise environments.
