# India AI Governance Landscape

## Overview

India does not yet have a comprehensive AI-specific law. Its AI governance landscape is instead shaped by a combination of national policy ambitions, emerging data protection legislation, and sector-specific guidance from financial, healthcare, and telecommunications regulators.

India's official posture — "responsible AI" framed around its 2018 NITI Aayog policy papers and the 2023 IndiaAI Mission — emphasises AI adoption as a national competitiveness priority. Governance is treated as an enabler of trust, not a brake on innovation.

This creates a distinctive regulatory environment: high ambition, early-stage regulatory infrastructure, and significant sectoral variation. For enterprises deploying AI in India or managing AI operations from India (GCCs, shared services), understanding this landscape is essential.

---

## Digital Personal Data Protection Act (DPDP Act), 2023

The DPDP Act is the most significant legal development for AI governance in India. Enacted in August 2023, it establishes a data protection framework that directly affects AI systems processing personal data of Indian citizens.

### Key Provisions Relevant to AI

**Consent and purpose limitation:** Personal data may be processed only for the purpose for which consent was obtained. AI systems trained on personal data must have a lawful basis — typically explicit consent or a statutory exemption (employment, public interest, legal obligation).

**Data fiduciary obligations:** Organisations processing personal data ("Data Fiduciaries") must implement reasonable security safeguards. For AI systems, this means protecting training data, model outputs, and inference logs that contain personal data.

**Data Principal rights:** Individuals have rights to access information about how their data is processed, to correct inaccurate data, and to erasure (with limitations). AI systems that make decisions based on personal data must accommodate these rights.

**Significant Data Fiduciaries (SDFs):** Organisations processing large volumes of sensitive personal data, or processing data of children, may be designated as SDFs and face additional obligations including data protection impact assessments and data protection officers.

**Penalties:** Up to ₹250 crore (~$30 million) for data breach failures; up to ₹200 crore for violations of children's data obligations.

**Cross-border data flows:** The Act allows data transfers to approved jurisdictions. The approved jurisdiction list has not yet been published. For AI systems using cloud infrastructure or training data from outside India, this remains a material uncertainty.

### Implications for AI Governance

The DPDP Act does not address AI directly, but its requirements apply to AI systems in practice:
- AI training data containing Indian personal data requires a lawful basis
- AI systems making decisions about individuals must accommodate data principal rights
- Automated decision-making is not explicitly regulated (unlike EU GDPR Article 22), but consent-based processing requirements apply
- DPIAs are required for SDFs and represent best practice for high-risk AI deployments

---

## MEITY Advisories on AI

The Ministry of Electronics and Information Technology (MEITY) has issued advisories on AI use, primarily targeting intermediaries and platforms deploying generative AI.

**March 2024 Advisory:** MEITY directed online intermediaries to obtain government approval before deploying "under-tested" or "unreliable" AI models or explicitly label AI-generated content as such. This advisory generated significant controversy and was subsequently softened — the approval requirement was removed, but the labelling expectation remains.

**Key ongoing expectations from MEITY:**
- AI-generated content must be clearly labelled
- AI systems must not generate content that threatens the sovereignty and integrity of India, is defamatory, or is sexually explicit
- Intermediaries using AI are expected to ensure AI outputs are consistent with Indian law and the IT Act, 2000

MEITY's AI governance posture is still evolving. Formal AI regulation through the IT Act or a standalone AI statute is anticipated but not yet finalised.

---

## Sectoral Regulatory Guidance

### Reserve Bank of India (RBI)

The RBI has not issued a comprehensive AI framework but has published guidance directly relevant to AI in financial services:

**Master Direction on IT Governance (2023):** Applies to banks and non-banking financial companies. Requires governance of all technology systems including AI — risk assessment, change management, audit, and vendor oversight obligations apply.

**Model Risk Management (MRM) expectations:** The RBI increasingly expects banks to apply model risk management practices (validation, documentation, monitoring) to AI and ML models used in credit, fraud, and customer-facing applications. Supervisory focus has intensified on AI-driven credit decisions.

**Data Localisation:** RBI mandates that payment system data be stored in India. This has direct implications for AI systems used in payments that process or model on this data — cloud-based inference using non-localised data creates compliance risk.

**AI in Lending:** The RBI's co-lending framework and NBFC regulations increasingly interact with AI-driven credit scoring. Explainability of credit decisions and fair lending expectations apply regardless of whether the decision is made by a human or an AI system.

### Securities and Exchange Board of India (SEBI)

**Circular on AI and ML (2019, updated):** Requires stock brokers and other registered entities using algorithmic trading to have risk controls, audit trails, and human oversight of AI-driven trading systems.

**AI in Registered Investment Advisers:** SEBI expects investment advisers using AI for recommendations to maintain audit trails and ensure suitability obligations are met — AI does not remove the adviser's regulatory responsibility.

**Surveillance AI:** SEBI actively uses AI for market surveillance. Its expectations for AI governance in market infrastructure institutions are increasingly referenced in supervisory examinations.

### Insurance Regulatory and Development Authority (IRDAI)

IRDAI has signalled intent to regulate AI in insurance underwriting and claims. Current expectations (not yet formalised as a circular):
- Fairness in AI-driven underwriting — no discrimination based on protected characteristics
- Explainability for claim denial decisions
- Human review for AI-flagged fraud investigations before adverse action

---

## IndiaAI Mission

The ₹10,371 crore IndiaAI Mission (announced 2024) is the government's primary vehicle for AI capability building. Key components relevant to governance:

- **IndiaAI Safety:** A centre focused on AI safety research, red-teaming, and evaluation — modelled in part on the UK AI Safety Institute
- **IndiaAI Datasets Platform:** Curated, consent-compliant datasets for AI training — aimed at reducing dependence on web-scraped data
- **Responsible AI:** Ethics guidelines and governance toolkits for public sector AI deployments

The Mission signals that India intends to develop AI governance capacity alongside AI capability, but the governance infrastructure lags the ambition.

---

## GCC Considerations

India hosts over 1,700 Global Capability Centres (GCCs) for multinational corporations. These centres increasingly build, operate, or govern AI systems on behalf of their parent companies. The governance implications:

- **Extraterritorial obligations:** GCC teams building AI systems used in the EU are subject to EU AI Act requirements regardless of where the development occurs.
- **Data localisation tension:** RBI and proposed sector rules require Indian data to remain in India; EU AI Act documentation and auditability requirements may conflict with data residency constraints.
- **Employment AI:** AI used in GCC workforce management (performance monitoring, attrition prediction, hiring) must comply with DPDP Act obligations and emerging labour law intersections.
- **Audit and oversight:** Parent company AI governance requirements must be translated into GCC operating procedures — a governance gap that regulators are beginning to examine.

---

## Recommendations

1. Treat DPDP Act compliance as the baseline governance requirement for all AI systems processing Indian personal data — it is enacted law and enforcement is expected to begin by late 2025.
2. For BFSI clients, align AI governance programmes with RBI IT Governance and model risk management expectations — these are the most actionable, enforceable obligations in the near term.
3. Build data localisation compliance into AI architecture decisions from the outset — retrofitting data flows after deployment is expensive and technically complex.
4. For GCCs, establish a clear accountability framework: which governance obligations apply in India, which derive from the parent company's home jurisdiction, and how conflicts (e.g., data residency vs. EU audit access) are resolved.
5. Monitor MEITY's evolving AI regulatory posture — India's AI regulation is likely to accelerate given the IndiaAI Mission's governance component, and early engagement with emerging standards reduces future compliance cost.
