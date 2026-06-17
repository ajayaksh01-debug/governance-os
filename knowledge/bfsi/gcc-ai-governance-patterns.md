# GCC AI Governance Patterns

## Overview

Global Capability Centres (GCCs) — also called Global In-house Centres (GICs) or captive centres — are subsidiary operations established by multinational corporations in lower-cost jurisdictions, predominantly India. India hosts over 1,700 GCCs spanning banking, financial services, insurance, technology, and professional services.

GCCs are increasingly central to enterprise AI operations: building AI models, developing AI-enabled products, operating AI infrastructure, and managing AI governance programmes on behalf of their parent companies. This creates a distinctive and complex governance environment.

---

## The GCC AI Governance Challenge

GCCs operate at the intersection of multiple overlapping governance obligations:

1. **Parent company obligations:** The parent's home jurisdiction requirements (EU AI Act for European parents, SEC/FRB requirements for US parents) apply to AI built or operated by the GCC.
2. **Host country obligations:** India's DPDP Act, RBI requirements, SEBI rules, and MEITY guidance apply to operations conducted in India.
3. **Customer jurisdiction obligations:** AI systems serving customers in the EU, UK, US, or other regulated markets face those markets' requirements — regardless of where the system was built.
4. **Internal governance standards:** Parent company AI governance policies, model risk frameworks, and ethical AI principles apply to GCC operations.

The governance challenge is not just understanding each obligation individually — it is managing the conflicts, overlaps, and gaps between them.

---

## Pattern 1 — Data Localisation vs. Cross-Border Audit Access

### The Tension
Indian data protection and financial sector regulations increasingly require that certain data — particularly payment data (RBI requirement) and sensitive personal data of Indian citizens (DPDP Act) — be stored and processed in India.

Parent company AI governance obligations — particularly under the EU AI Act and US SR 11-7 — may require that AI systems and their training data be accessible to regulators and internal audit functions outside India. EU AI Act Article 74 gives the Commission rights to access documentation of AI systems used in the EU.

### Governance Pattern
- **Data residency mapping:** Create a data flow map for each AI system that distinguishes between data that must be localised, data that can be transferred under standard contractual clauses or other mechanisms, and data flows that are genuinely unconstrained.
- **Tiered data architecture:** Design AI systems to separate locally-mandated data stores from globally-shareable model artefacts. Model weights, evaluation reports, and governance documentation may be shareable even when underlying training data cannot leave India.
- **Audit evidence packs:** Maintain audit evidence packs for parent-jurisdiction regulators that contain sufficient information for audit without requiring access to locally-restricted data.

---

## Pattern 2 — Multi-Jurisdictional Model Governance

### The Tension
GCCs build models that are deployed by the parent company in multiple jurisdictions simultaneously. A credit scoring model built in Bangalore may be deployed in France (EU AI Act high-risk), the UK (PRA SS1/23), the US (SR 11-7), and India (RBI guidance) — each with different model risk management requirements.

### Governance Pattern
- **Common development standard:** Adopt the most demanding applicable standard as the baseline for model development documentation and validation — typically EU AI Act or SR 11-7. Meeting this standard satisfies less demanding requirements automatically.
- **Jurisdiction-specific conformity supplements:** For each deployment jurisdiction, maintain a supplementary document mapping the baseline validation to local requirements and documenting any jurisdiction-specific additional requirements met.
- **Centralised model registry:** Maintain a single global model registry visible to both GCC and parent governance functions, with jurisdiction-specific deployment records for each model.

---

## Pattern 3 — AI Talent Governance Asymmetry

### The Tension
GCCs typically house a high concentration of AI engineering talent — data scientists, ML engineers, and AI architects. Governance expertise — model risk management, AI ethics, regulatory compliance — is often concentrated at the parent company level.

This creates an asymmetry: the people building AI systems (in the GCC) have limited governance context, while the people who understand governance obligations (at the parent) are distant from the AI building process.

### Governance Pattern
- **Embedded governance capability:** Invest in AI governance expertise within the GCC — model risk management, data protection, and AI ethics competencies must exist close to where AI systems are built.
- **Governance integration in development lifecycle:** Governance checkpoints (risk assessment, bias evaluation, validation requirements) must be embedded in the AI development process, not applied after the fact by a remote compliance team.
- **Training programmes:** Systematic AI governance training for GCC AI teams — not general compliance training, but AI-specific governance training covering the frameworks relevant to the parent's regulatory environment.

---

## Pattern 4 — Third-Party AI Provider Governance in GCC Context

### The Tension
GCC teams extensively use third-party AI services — cloud AI APIs, open-source models, commercial AI tools — for development productivity. These tools process data that may be subject to data localisation requirements or that the parent's governance policies restrict.

Samsung's source code leak (see `ai-incidents/samsung-source-code-leak.md`) illustrates the failure mode: engineers using public AI tools for sensitive work without governance controls.

### Governance Pattern
- **Approved AI tool list:** Maintain and enforce a list of approved AI tools and services. Engineers should default to approved tools; new tools require a governance review before use.
- **Data classification integration:** Connect AI tool governance to data classification — certain data classifications may not be submitted to external AI services regardless of whether the tool is approved.
- **Private deployment preference:** For sensitive workloads, prefer private or on-premises AI deployments over public APIs — the cost premium is justified by the data protection benefit.
- **GCC-specific usage policies:** Parent AI usage policies often assume a US or European work environment. Adapt them explicitly for GCC context, addressing India-specific tools and common GCC workflows.

---

## Pattern 5 — Operational AI in GCC Shared Services

### The Tension
Many GCCs operate shared service functions — finance, HR, legal, IT support — using AI automation. These AI systems process personal data of employees across multiple countries, creating complex cross-border processing obligations.

HR AI used in GCCs — performance monitoring, attendance analysis, attrition prediction — may implicate employment laws across multiple jurisdictions. An AI system monitoring GCC employee productivity and flagging performance concerns must comply with Indian labour law, the DPDP Act, and potentially the parent's home jurisdiction employment regulations.

### Governance Pattern
- **Cross-border HR AI assessment:** Any AI system processing employee data across jurisdictions requires a multi-jurisdiction legal assessment before deployment — not just a data protection assessment, but also a labour law and works council / employee representative review.
- **Transparency to employees:** Employees must be informed when AI is used in ways that affect their employment. Covert AI monitoring of employee behaviour creates significant legal and ethical risk.
- **Minimisation of individual-level performance AI:** Aggregate team performance analytics are less legally and ethically fraught than individual performance surveillance. Design choices that aggregate data reduce risk.

---

## Pattern 6 — GCC AI Incident Response

### The Tension
AI incidents (data breaches, biased decisions, model failures) originating in the GCC may trigger regulatory notification obligations in multiple jurisdictions simultaneously. A model failure affecting EU customers triggers EU AI Act incident reporting; the same failure affecting Indian customers may trigger DPDP Act breach notification; the parent company faces its own home jurisdiction obligations.

### Governance Pattern
- **Multi-jurisdiction incident playbook:** Develop incident response playbooks that address simultaneous notification obligations across key jurisdictions.
- **GCC incident authority:** Define clearly whether the GCC team has authority to trigger regulatory notifications or whether all notifications must be escalated to the parent. Unclear authority leads to delayed responses.
- **Incident notification thresholds:** Document the threshold for each jurisdiction — what constitutes a notifiable AI incident under each relevant regulation — so that GCC teams can make timely assessments.

---

## Governance Framework for GCC AI Operations

### Minimum Governance Baseline
Every GCC conducting AI operations should establish:
- An AI inventory covering all models built, operated, or used by the GCC
- An AI use policy aligned with parent company policy and adapted for local context
- Training for AI teams on applicable governance frameworks
- An approved AI tool list with enforcement mechanism
- A clear escalation path to parent governance functions

### Aspirational Maturity Target
- Embedded model risk management capability within the GCC
- Participation in parent company AI governance committees
- GCC-originated AI governance improvements flowing back to the parent
- GCC as a centre of excellence for AI governance, not merely a building location for AI

---

## Recommendations

1. Treat GCC AI governance as a distinct problem requiring dedicated attention — the jurisdictional complexity of GCC operations is not well served by applying parent-company governance frameworks without adaptation.
2. Invest in model risk and AI governance expertise within the GCC — governance expertise co-located with engineering teams is more effective than remote oversight.
3. Resolve data localisation architecture decisions before building AI systems — retrofitting data residency compliance into deployed AI systems is expensive and disruptive.
4. Establish a GCC AI incident playbook before an incident occurs — multi-jurisdiction notifications under time pressure are a governance failure mode.
5. Use the GCC's scale and AI talent as an asset in the parent's AI governance programme — GCC teams can build governance tooling, run bias assessments, and develop evaluation frameworks that improve governance across the enterprise.
