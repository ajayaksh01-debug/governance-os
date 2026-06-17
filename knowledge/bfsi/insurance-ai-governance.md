# Insurance AI Governance

## Overview

Insurance is built on risk assessment — and AI is transforming how that assessment is done. From underwriting and pricing to claims processing and fraud detection, AI enables insurers to assess risk with greater precision, speed, and granularity than was previously possible.

That precision creates governance challenges. The same AI that enables more accurate risk segmentation can also encode discrimination, erode privacy, and make decisions that are difficult to explain or contest. Regulators globally are increasing scrutiny of AI in insurance precisely because these risks are systemic — affecting millions of policyholders — and because the harms can be severe and difficult to reverse.

---

## Use Case 1 — Underwriting and Risk Assessment

### How AI Is Used
AI models analyse diverse data signals to assess risk and inform underwriting decisions: telematics data for motor insurance, satellite imagery and weather data for property insurance, clinical and lifestyle data for life and health insurance, and behavioural signals across all lines.

### Governance Risks

**Proxy discrimination:** AI underwriting models that do not use protected characteristics as direct inputs can still discriminate through correlated proxies. Credit score, postcode, occupation, and even smartphone usage patterns can be proxies for race, income, or disability. Proxy discrimination is unlawful in most jurisdictions regardless of intent.

In the UK, the FCA has specifically investigated whether insurers' data practices result in differential pricing that is unfair or discriminatory. The EU AI Act explicitly lists insurance underwriting as high-risk AI (Annex III) where full conformity assessment is required.

**Unfair pricing:** Variable pricing models that use granular individual data to set premiums — "price optimisation" — have been challenged by regulators. The concern is that AI-driven pricing can identify customers with low price sensitivity (often older, less digitally engaged, or more loyal customers) and charge them more, regardless of their actual risk level.

**Data privacy in health underwriting:** Life and health underwriting increasingly incorporates data from wearables, health apps, and genetic testing. This data is among the most sensitive personal data and is subject to heightened protection in most jurisdictions. Its use in underwriting raises significant consent, purpose limitation, and discrimination concerns.

### Governance Requirements
- Proxy discrimination testing as part of model development — identify and address variables that correlate with protected characteristics
- Fairness metrics incorporated into underwriting model validation
- Legal review of all data inputs for lawfulness and proportionality
- Regulatory compliance review of pricing model methodology

---

## Use Case 2 — Claims Processing

### How AI Is Used
AI accelerates and automates claims handling: natural language processing to triage and categorise claims, image analysis for property damage assessment, automated liability determination for straightforward claims, and pattern recognition for fraud detection in claims data.

### Governance Risks

**Accuracy of automated decisions:** Automated claims decisions — particularly decisions to deny or reduce a claim — must be accurate. An AI system that incorrectly denies a legitimate claim causes direct harm to the policyholder and creates regulatory and reputational exposure for the insurer.

**Explainability for adverse decisions:** In most jurisdictions, insurers must explain why a claim was denied. AI systems that cannot produce an explanation appropriate to the customer and to regulatory standards cannot be used for automated adverse decisions. The UK FCA's Consumer Duty expects that customers can understand decisions made about them.

**Bias in damage assessment:** Computer vision models used for property damage assessment have been found to produce biased estimates — consistently undervaluing damage in lower-value properties or properties in certain geographic areas. This creates systemic unfairness that disproportionately affects lower-income or minority communities.

**Handling vulnerable customers in AI claims:** Customers making insurance claims are frequently in distress — following an accident, bereavement, or property loss. AI systems that cannot identify vulnerability indicators and escalate to human handling cause disproportionate harm.

### Governance Requirements
- Accuracy validation for automated claims decisions before production deployment
- Explainability requirement for all adverse claim decisions
- Bias testing of image analysis and damage assessment models
- Vulnerability escalation protocols in all customer-facing claims AI
- Human review pathway for disputed automated decisions

---

## Use Case 3 — Fraud Detection

### How AI Is Used
AI identifies potentially fraudulent claims and applications through pattern recognition, anomaly detection, network analysis (identifying linked entities), and text analysis of claim narratives.

### Governance Risks

**False positives — wrongful fraud flagging:** An AI system that incorrectly identifies a legitimate claim as potentially fraudulent — and triggers investigation or denial — causes significant harm to the claimant. Wrongful fraud accusations are damaging, distressing, and can expose the insurer to counter-claims.

**Demographic bias in fraud detection:** Fraud detection models trained on historical fraud data will reflect historical investigation and detection patterns, which may themselves have been biased. A community that was historically over-investigated for insurance fraud will generate more "confirmed fraud" data points, causing future models to flag that community at higher rates — a self-reinforcing bias cycle.

**Privacy of fraud databases:** Insurance industry fraud databases (Claims and Underwriting Exchange / CUE in the UK) are used to inform AI fraud detection. Incorrect entries — or entries that unfairly stigmatise individuals — can follow a customer for years. Governance of these shared databases, and AI systems that use them, must include correction mechanisms.

### Governance Requirements
- Demographic bias testing of fraud detection models
- Human review for all fraud decisions before adverse action
- Dispute and correction process for customers flagged by fraud AI
- Periodic audit of fraud database inputs and AI scoring methodology

---

## Use Case 4 — Customer Service and Renewal

### How AI Is Used
AI handles customer enquiries, processes renewals, provides coverage advice, and manages policy changes. Conversational AI is increasingly used for first-line customer contact across all insurance lines.

### Governance Risks

**Consumer Duty compliance:** UK FCA Consumer Duty, and equivalent consumer protection frameworks elsewhere, requires that insurance products and services deliver fair value and good outcomes. AI-driven renewal and upsell systems must be designed around customer outcomes, not only revenue optimisation.

**Premium renewal practices:** The FCA's ban on price walking (charging loyal renewal customers more than equivalent new customers) applies equally to AI-driven pricing systems. AI that optimises renewal pricing without controlling for customer loyalty effects creates regulatory exposure.

**Advice boundary in coverage recommendations:** AI that recommends coverage changes or upgrades is potentially providing regulated financial advice. The advice/guidance boundary must be carefully managed.

### Governance Requirements
- Consumer Duty impact assessment for AI-driven renewal and upsell systems
- Testing for premium renewal bias by customer tenure and demographic
- Clear disclosure of AI's role in customer interactions
- Human escalation pathway for complex coverage questions

---

## Regulatory Landscape

| Jurisdiction | Key Requirements |
|---|---|
| UK FCA | Consumer Duty; General Insurance Pricing Practices; Data Fairness |
| UK PRA | SS1/23 Model Risk Management |
| EU AI Act | Insurance underwriting explicitly listed as high-risk (Annex III) |
| EU | Solvency II (operational risk); GDPR (data use in underwriting) |
| US NAIC | AI in insurance principles and model bulletin; state-level AI regulations |
| India IRDAI | Emerging AI guidelines; fairness expectations for underwriting and claims |

---

## Recommendations

1. Prioritise proxy discrimination testing for all underwriting models — this is the single highest regulatory risk for insurance AI and the most common governance gap.
2. Implement explainability for all adverse claim and underwriting decisions before deployment — this is both a regulatory requirement and a customer rights obligation in most jurisdictions.
3. Apply Consumer Duty / equivalent frameworks to renewal pricing AI — the FCA's price walking ban extends to AI-driven pricing, and equivalents are being adopted in other jurisdictions.
4. Design vulnerability protocols into all customer-facing AI from the start — retrofitting vulnerability handling after deployment is technically complex and reputationally expensive.
5. Treat health data used in underwriting as requiring the highest governance standard — purpose limitation, consent, and security controls for health data must exceed the baseline for other data types.
