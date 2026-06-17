# Architecture Decision Record: ADR-002

## Title
ADR-002: Mandatory Claims Firewall Compliance

---

## Status
**Accepted**

---

## Context
Sales discovery and proposal processes frequently experience pressure to commit to roadmap features or unreleased capabilities to win competitive deals. When these commitments are made without explicit caveats or workarounds, they contaminate client proposals and contracts. 

In regulated markets, making unverified platform claims violates basic data security and vendor governance standards (e.g. RBI outsourcing guidelines, EU AI Act conformity self-assessments). To maintain compliance and protect commercial relationships, every output containing platform references must run through a validation gate.

---

## Decision
All customer-facing documents, solution designs, RFP responses, and platform configuration guides must comply with the **Claims Firewall**:

1.  Every platform reference must be checked against `canonical-product-model.md`.
2.  If a feature status is **Production**, the claim is permitted with any canonical caveats attached.
3.  If a feature status is **In Build** or **Roadmap**, it must be explicitly labeled as a "roadmap item" in the proposal, and the output must detail a mandatory manual or third-party workaround control that the client can deploy today.
4.  If a feature status is **Aspirational**, it cannot be committed to a proposal or listed as a roadmap deliverable under any circumstances.
5.  An automated script (`claims_linter.py`) will run as a pre-release gate. Any firewall violation or ambiguity overrides all other quality scores and results in an automatic **0/100 (Rejection)** of the document.

---

## Consequences
- **Positive:**
  - Prevents the release of non-compliant proposals or unvalidated platform claims.
  - Forces sales teams to proactively pitch Cursory advisory services to bridge platform gaps.
  - Automates compliance monitoring, reducing human auditing errors.
- **Negative:**
  - May slow down proposal generation if a sales team is forced to rewrite sections to incorporate manual workarounds.
  - Requires strict maintenance of the regex patterns in the linter to prevent false positives or negatives.

---

## Alternatives Considered
- **Post-hoc Human Compliance Review:** Rejected. Relying entirely on manual peer review is slow, expensive, and subject to oversight and human error, especially during high-volume RFP response cycles.
- **Flexible Claims (Soft Warning):** Rejected. Downgrading firewall violations to a warning allows non-compliant text to slip through, exposing the company to regulatory audit failures.
