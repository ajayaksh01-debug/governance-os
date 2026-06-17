# AI Incident Analysis — Worked Examples

This document contains three fully worked incident analyses produced using the AI Incident Analysis skill. Each example demonstrates application of the complete workflow and output structure.

---

---

# Example 1: Samsung Source Code Leak via ChatGPT

**Date of Analysis:** 2024-01-15  
**Incident Date:** April 2023  
**Incident Type:** Data Exfiltration / Governance Failure  
**Evidence Quality:** High (confirmed by Samsung, widely reported)  
**Analysis Status:** Final

---

## 1. Incident Summary

In April 2023, Samsung Electronics experienced three separate data exfiltration incidents within twenty days, all caused by employees using ChatGPT to assist with work tasks. In the first incident, an engineer submitted proprietary source code for semiconductor measurement equipment to ChatGPT and asked the model to identify bugs. In the second, an employee uploaded confidential internal meeting notes for summarisation. In the third, additional proprietary source code was submitted for language conversion assistance.

In all three cases, the data was processed by OpenAI's servers and, under the terms of service in effect at the time, was eligible for use in model training. Samsung had no policy governing external AI tool use, no technical controls to prevent submission of sensitive data to external services, and no mechanism to detect or respond to the disclosures.

The incidents occurred within weeks of Samsung lifting an internal ban on ChatGPT use without replacement controls. The intellectual property exposed relates to Samsung's semiconductor manufacturing operations — a domain of extreme competitive and strategic sensitivity.

---

## 2. Root Cause Analysis

**Proximate Cause:**  
Engineers submitted proprietary source code and confidential documents to an external AI service without understanding that the data would be processed on external servers and potentially retained for model training.

**5 Whys:**
1. Why did engineers submit sensitive data to ChatGPT?  
   → They did not understand that data submitted to ChatGPT left Samsung's environment.

2. Why did they not understand this?  
   → No training or awareness programme explained the data handling implications of public AI services.

3. Why was no training provided?  
   → Samsung had no AI use policy that would have prompted training requirements.

4. Why was there no AI use policy?  
   → The ChatGPT ban was lifted without replacement controls — governance decision-making did not include policy development as a prerequisite.

5. Why did the governance process not require policy development?  
   → No organisational process existed to govern the introduction of new AI tools at the employee level.

**Root Cause:** Governance gap — no framework or process for governing employee adoption of external AI tools, resulting in unrestricted use without any supporting policy, training, or technical controls.

**Contributing Factors:**
- ChatGPT ban lifted without any replacement governance measures
- No Data Loss Prevention (DLP) controls covering external AI service endpoints
- No vendor assessment of OpenAI's data handling terms before permitting use
- No approved AI tool list or tool approval process existed

---

## 3. Risk Category

**Primary:** Data Exfiltration  
**Secondary:** Governance Failure, Supply Chain (third-party AI service with adverse data handling terms)

---

## 4. Control Failures

| Control | Type | Failure Mode | Description |
|---|---|---|---|
| AI Use Policy | Preventive | Absent | No policy existed defining permitted/prohibited data types for external AI tools |
| AI Tool Approval Process | Preventive | Absent | No process for assessing and approving AI tools before employee use |
| Data Loss Prevention (DLP) | Preventive | Absent | No technical controls detecting or blocking sensitive data submission to external web services |
| Third-Party AI Vendor Assessment | Preventive | Absent | OpenAI's data handling and training data practices were not assessed before use was permitted |
| Employee Awareness Training | Preventive | Absent | No training on data handling when using cloud-based AI services |
| Shadow AI Detection | Detective | Absent | No monitoring for use of unsanctioned AI tools in the corporate environment |

---

## 5. Applicable Frameworks

### ISO 42001
- **Clause 8.4 — Supply chain:** Requires assessment of third-party AI providers. The absence of a vendor assessment for ChatGPT is a direct Clause 8.4 failure.
- **Clause 7.3 — Awareness:** Requires that relevant personnel are aware of AI-related risks. The failure to train employees on AI tool data handling violates this clause.
- **Annex A — Data governance controls:** Specifically, data minimisation and controls governing what data enters external AI systems.
- **Annex A — Human oversight:** The absence of any review or approval process before employee AI tool use represents a human oversight failure.

### NIST AI RMF
- **GOVERN:** Primary failure. No AI risk management policy, no accountability for AI tool governance, no strategy for managing AI adoption at the employee level.
- **MAP:** The risk of sensitive data submission to external AI services was not identified, classified, or communicated.
- **MANAGE:** No controls were in place to manage the identified risk. The ban that was lifted was a management control — it was removed without replacement.

### OWASP LLM Top 10
- **LLM06 — Sensitive Information Disclosure:** The core risk. Proprietary data was submitted to an external model where it could be incorporated into training data.
- **LLM05 — Supply Chain Vulnerabilities:** The risk introduced by using a third-party AI service without assessing its data handling practices.

---

## 6. Regulatory Implications

**GDPR / UK GDPR:** If any personal data (employee data, customer data) was included in the submitted materials, this constitutes a personal data breach. Samsung operates in the EU and is subject to GDPR. Depending on the nature of the data submitted, breach notification to the supervisory authority may have been required under Article 33 within 72 hours of becoming aware.

**EU AI Act:** Samsung is a provider of AI systems, not purely a deployer. As a large technology company, the Act's supply chain obligations apply. The absence of any third-party AI provider assessment would be non-compliant with expected practices under the deployer obligations.

**Trade Secret / IP Law:** The submission of proprietary source code to an external service may constitute a disclosure of trade secrets under applicable law (Korea Unfair Competition Prevention Act, US Defend Trade Secrets Act for US operations). The legal consequences depend on whether the disclosure was sufficiently public to constitute a trade secret waiver.

**Notification obligations:** Samsung disclosed the incidents and notified affected individuals. No regulatory enforcement action has been publicly reported as of the analysis date.

---

## 7. BFSI Impact

**Applicability:** High. The Samsung incident pattern — employees using public AI services for sensitive work — is directly applicable to financial institutions.

**BFSI-Specific Risks:**
- Submission of customer financial data, transaction records, or credit information to public AI services would constitute a customer data breach with immediate regulatory consequences under FCA, RBI, and relevant data protection law.
- Submission of proprietary trading algorithms, credit models, or risk management methodologies to public AI services would expose competitive IP and potentially constitute market misconduct if trading-sensitive information was involved.
- Bank examiners (PRA, RBI, OCC) are actively reviewing AI tool governance. Evidence of uncontrolled employee AI tool use is a significant examination finding.

**BFSI Regulatory Frameworks:**
- PRA SS1/23: AI tool governance is within scope of model risk management for models used in regulated activities.
- FCA Consumer Duty: Customer data submitted to unvetted AI services creates consumer harm risk.
- RBI IT Governance: Third-party tool risk management is explicitly required.

---

## 8. Lessons Learned

**Lesson 1 — Never lift a technology ban without replacement controls**  
Applicability: Any organisation that bans and then reinstates AI tools. The governance failure is not in banning ChatGPT — it is in lifting the ban without policy, training, and technical controls as prerequisites.  
Urgency: Critical. This pattern is common. Many organisations lifted ChatGPT bans in 2023 without governance infrastructure.

**Lesson 2 — Data classification is a prerequisite for AI tool governance**  
Employees cannot make appropriate judgements about what to submit to AI tools without a functioning data classification scheme. AI tool governance built on top of undefined data classification will fail.  
Applicability: All organisations deploying AI tools with employee access to sensitive data.  
Urgency: High.

**Lesson 3 — Technical controls must enforce policy, not rely on it**  
DLP tools, endpoint controls, and network monitoring can technically prevent sensitive data submission to external AI services. Policy alone, without technical enforcement, relies on employee compliance that is not realistic at scale.  
Applicability: All organisations. Employee compliance with AI use policies will be imperfect regardless of training quality.  
Urgency: High.

**Lesson 4 — Third-party AI services require vendor assessment, not assumed trust**  
OpenAI's training data practices and data retention policies were publicly available and contained material implications for enterprise data. The failure to read and assess the terms of service before organisational use is a basic vendor risk management failure.  
Applicability: All organisations using AI services provided by third parties.  
Urgency: Critical.

---

## 9. Recommended Controls

| Control | Description | Complexity | Priority | Framework Reference |
|---|---|---|---|---|
| AI Use Policy | Formal policy defining approved AI tools, prohibited data types for AI submission, and consequences of non-compliance | Low | Critical | ISO 42001 Cl.5; NIST GOVERN |
| AI Tool Approval Process | Formal security and privacy assessment process that any AI tool must pass before employee use is permitted | Low | Critical | ISO 42001 Cl.8.4; NIST MAP |
| DLP for AI Endpoints | Extend existing DLP to detect and block submission of classified data to AI service endpoints | Medium | Critical | ISO 42001 Annex A; NIST MANAGE |
| Third-Party AI Vendor Assessment | Standard vendor assessment covering data handling, training data practices, retention, and security for all AI service providers | Low | High | ISO 42001 Cl.8.4; NIST MAP |
| Employee Awareness Training | AI-specific training covering: what data can be submitted, what cannot, why, and how to identify appropriate use | Low | High | ISO 42001 Cl.7.3; NIST GOVERN |
| Approved AI Tool List | Maintained list of approved AI tools with data classification restrictions per tool | Low | High | ISO 42001 Cl.8; NIST MANAGE |
| Shadow AI Monitoring | Technical monitoring for employee use of unapproved AI services on corporate networks and devices | Medium | Medium | ISO 42001 Annex A; NIST MEASURE |

---

## 10. Executive Summary

In April 2023, Samsung employees used ChatGPT to assist with sensitive engineering tasks — submitting proprietary source code and confidential meeting notes to OpenAI's servers, where the data could be retained and used for model training. Three separate incidents occurred within twenty days.

The root cause was not an employee error — it was a governance failure. Samsung lifted its internal ChatGPT ban without implementing any replacement controls: no policy, no training, no technical safeguards, and no assessment of OpenAI's data handling practices. When employees used a tool that was no longer banned, they did so without understanding the risks.

The incident illustrates a pattern now seen across many organisations: AI bans being lifted in response to productivity pressure, without the governance infrastructure that makes safe AI use possible. The result is unrestricted access to powerful tools by employees who have not been told what they can and cannot do with them.

Three actions are most critical: establish an AI use policy before lifting tool bans; implement technical controls (DLP) that enforce policy rather than relying on compliance; and conduct basic vendor assessment of AI services before permitting organisational use.

---

---

# Example 2: Slack AI Indirect Prompt Injection

**Date of Analysis:** 2024-09-20  
**Incident Date:** August 2024  
**Incident Type:** AI Security Incident — Prompt Injection (Indirect)  
**Evidence Quality:** High (detailed technical disclosure by PromptArmor, confirmed by Salesforce)  
**Analysis Status:** Final

---

## 1. Incident Summary

In August 2024, security researchers at PromptArmor disclosed a critical vulnerability in Slack AI, Salesforce's AI assistant embedded in Slack workspaces. By posting a message to a public Slack channel containing prompt injection instructions — text designed to manipulate Slack AI's behaviour — an attacker could cause Slack AI to exfiltrate private channel contents when any user subsequently asked Slack AI a question.

The attack required no privileged access. Any user with the ability to post in a public channel could plant the injection. When Slack AI retrieved workspace content to answer an unrelated user question, it also retrieved the injected message and followed its instructions — accessing and including private channel contents in its response.

The vulnerability was responsibly disclosed to Salesforce, which patched it. The attack was demonstrated in a controlled environment, but the underlying vulnerability was present in the production system. No public disclosure of confirmed exploitation by malicious actors has been made.

---

## 2. Root Cause Analysis

**Proximate Cause:**  
Slack AI's retrieval system did not distinguish between trusted system instructions and untrusted user-generated content when processing workspace data, allowing injected instructions embedded in channel messages to override AI behaviour.

**5 Whys:**
1. Why could an injected message override Slack AI's behaviour?  
   → Slack AI's context window combined retrieved workspace content with system instructions without separating trust levels.

2. Why were trust levels not separated?  
   → The system was not designed with a security model that treated user-generated data as potentially adversarial.

3. Why was adversarial user content not considered in the threat model?  
   → Indirect prompt injection was not included in the threat model for the RAG retrieval pipeline during design.

4. Why was indirect injection not in the threat model?  
   → At the time of system design, indirect injection was an emerging attack class not yet established in industry security standards.

5. Why was there no post-launch adversarial testing to catch this?  
   → No structured red-teaming or injection testing programme existed for the production system.

**Root Cause:** Security design failure — the RAG retrieval architecture was not designed to treat retrieved content as potentially adversarial, and no adversarial testing programme existed to identify the gap post-deployment.

**Contributing Factors:**
- Broad data access permissions for Slack AI (access to all channels a user could access)
- No output filtering to detect instruction-following patterns in data-derived responses
- No monitoring for anomalous data access patterns during AI inference
- Indirect prompt injection not yet included in standard security testing methodologies at time of design

---

## 3. Risk Category

**Primary:** Prompt Injection (Indirect)  
**Secondary:** Data Exfiltration, Insecure Plugin / Integration Design

---

## 4. Control Failures

| Control | Type | Failure Mode | Description |
|---|---|---|---|
| Context trust separation | Preventive | Absent | No architectural separation between system instructions (trusted) and retrieved workspace content (untrusted) |
| Least privilege data access | Preventive | Inadequate design | Slack AI accessed all data the user could access, rather than minimum data required for the query |
| Adversarial testing / red-teaming | Detective | Absent | No injection testing programme covering the RAG retrieval pipeline |
| Output content filtering | Detective | Absent | No filter to detect anomalous instruction-following patterns in AI responses derived from retrieved content |
| Anomaly monitoring | Detective | Absent | No monitoring for AI accessing unusual volumes or types of data during inference |

---

## 5. Applicable Frameworks

### ISO 42001
- **Clause 8 — Operation:** AI system design must address security risks. The absence of adversarial threat modelling in the design phase is a Clause 8 failure.
- **Annex A — AI system security:** Controls covering adversarial robustness and testing against known attack classes.
- **Annex A — Supply chain:** Organisations deploying Slack AI as a third-party tool must assess its security posture as part of vendor risk management.

### NIST AI RMF
- **MEASURE:** Adversarial testing and red-teaming should have identified this vulnerability. The absence of structured injection testing is a MEASURE function failure.
- **MANAGE:** The vulnerability was not detected in production and was only identified through external research. Operational monitoring should have provided earlier detection capability.
- **GOVERN:** Secure design principles were not applied to the RAG architecture.

### OWASP LLM Top 10
- **LLM01 — Prompt Injection:** Primary. Specifically indirect injection via retrieved data.
- **LLM07 — Insecure Plugin Design:** The Slack AI integration with workspace data lacked appropriate security controls.
- **LLM08 — Excessive Agency:** Slack AI had access to more data than was necessary for any individual query, enabling the exfiltration.

---

## 6. Regulatory Implications

**GDPR / UK GDPR:** If exploited in a production environment, private channel data accessed without authorisation would constitute a personal data breach. Depending on data volume and sensitivity, Article 33 breach notification would be required within 72 hours.

**EU AI Act:** AI systems integrated into enterprise software products are subject to deployer obligations. An AI system with a known vulnerability enabling data exfiltration does not meet Article 15 cybersecurity requirements for high-risk AI, and would be relevant to conformity assessment for deployers in high-risk categories.

**Sectoral regulations:** For financial services organisations using Slack AI with access to regulated communications (investment advice, transaction records, client data), exploitation of this vulnerability could trigger specific regulatory obligations around data security under FCA, PRA, RBI, and SEC requirements.

---

## 7. BFSI Impact

**Applicability:** High. Financial services organisations are intensive Slack users. Private channels frequently contain client communications, deal information, regulatory correspondence, and confidential strategy discussions.

**Specific BFSI Risks:**
- Exfiltration of private channel content in a banking context could expose customer data, M&A communications, credit committee discussions, or risk reports — all of which are highly sensitive and subject to specific confidentiality obligations.
- FCA and PRA regulated communications requirements mean that AI-related access to private communications creates both data protection and regulatory compliance exposure.
- Banks using Slack AI in environments connected to trading or deal information may face market conduct implications if injection attacks expose non-public information.

**Recommended BFSI Response:**
- Audit which channels Slack AI has access to and restrict to approved channels only
- Review data classification of Slack channels and restrict AI access to channels containing sensitive regulated data
- Confirm patching status and verify the fix is effective in the specific deployment environment

---

## 8. Lessons Learned

**Lesson 1 — Retrieved content must be treated as adversarial**  
Any AI system that retrieves and processes external data — documents, messages, web content, database records — must treat that content as potentially containing injection instructions. This is the defining lesson of indirect injection: the attack surface is the data, not the user.  
Applicability: All RAG systems, AI assistants with document access, agents that browse or retrieve content.  
Urgency: Critical.

**Lesson 2 — Least privilege applies to AI data access**  
Slack AI's ability to access all channels a user could access was the enabler of the exfiltration — not just the injection. Minimising what data the AI can access limits what an attacker can extract, even if injection is successful.  
Applicability: All AI systems with access to internal data repositories.  
Urgency: High.

**Lesson 3 — Red-teaming must include indirect injection as a standard test**  
This vulnerability was found by external researchers, not by Salesforce's own security testing. Indirect injection must be a first-class test case in any AI security assessment — not a novel attack but an established and well-understood risk.  
Applicability: All organisations deploying LLM-based applications.  
Urgency: High.

---

## 9. Recommended Controls

| Control | Description | Complexity | Priority | Framework Reference |
|---|---|---|---|---|
| Context trust separation | Architecturally separate system instructions from retrieved data in the model's context; label all retrieved content as untrusted | High | Critical | OWASP LLM01; ISO 42001 Annex A |
| Retrieval least privilege | Limit AI retrieval scope to the minimum data required for the query; do not grant access to all data by default | Medium | Critical | OWASP LLM08; ISO 42001 Cl.8 |
| Injection testing programme | Include indirect injection as a standard test case in all AI security assessments and red-team exercises | Low | Critical | NIST MEASURE; OWASP LLM01 |
| Output content filtering | Detect and flag responses that appear to follow instructions embedded in retrieved content | Medium | High | OWASP LLM02; ISO 42001 Annex A |
| Data access monitoring | Monitor AI inference for anomalous data access patterns (unusual volume, cross-channel access) | Medium | High | NIST MEASURE; ISO 42001 Cl.9 |

---

## 10. Executive Summary

In August 2024, a security researcher demonstrated that Slack AI — Salesforce's AI assistant for Slack workspaces — could be manipulated to exfiltrate private channel contents without the attacker having any access to those channels. By posting a message containing hidden instructions in a public channel, the attacker caused Slack AI to follow those instructions when any user asked it an unrelated question — accessing and revealing private data as a result.

This is an indirect prompt injection attack: the malicious instructions were not typed by the attacker into the AI interface — they were embedded in content that the AI retrieved from the workspace. This attack class affects any AI system that retrieves and processes content from external or user-controlled sources.

The root cause is a security design failure. Slack AI's architecture did not treat retrieved workspace content as potentially adversarial, and Salesforce had no testing programme that would have caught this vulnerability before external researchers identified it.

For organisations using Slack AI or similar AI assistants with access to internal data, two actions are most urgent: restrict AI data access to the minimum required for legitimate use, and engage your security team to assess all AI systems for indirect injection vulnerabilities. Any AI system that retrieves data should be assessed as a priority.

---

---

# Example 3: Amazon Recruitment AI Bias

**Date of Analysis:** 2024-02-10  
**Incident Date:** 2014–2017 (development); disclosed October 2018  
**Incident Type:** Bias / Fairness Incident, Governance Failure  
**Evidence Quality:** High (Reuters investigation, confirmed by Amazon)  
**Analysis Status:** Final

---

## 1. Incident Summary

Between 2014 and 2017, Amazon developed an AI recruitment tool designed to automate CV screening by rating candidates on a five-star scale. The system was trained on ten years of Amazon's hiring decisions.

By 2015, Amazon's engineers discovered that the model was systematically penalising CVs containing female-associated signals: the word "women's" (as in "women's chess club"), graduates of all-women's colleges, and patterns correlated with female applicants. The model had learned to replicate the gender bias embedded in Amazon's historical hiring data, where men dominated senior technical roles.

Multiple attempts to patch the specific biases failed to assure engineers that other gender-correlated biases did not remain in the model. Amazon disbanded the team in 2017 and confirmed that the tool was never used to evaluate real candidates. Reuters disclosed the project and its failure in October 2018.

The incident is one of the most significant documented cases of AI replicating historical discrimination at scale and remains a canonical reference point in AI fairness and governance literature.

---

## 2. Root Cause Analysis

**Proximate Cause:**  
The model was trained on historically biased hiring data and learned to replicate the gender bias present in that data as a predictive signal.

**5 Whys:**
1. Why did the model penalise female-associated signals?  
   → It was trained to predict hires based on historical data in which men were significantly more likely to be hired into senior technical roles.

2. Why was the historical data used without adjustment?  
   → The team treated historical hiring decisions as ground truth — a valid representation of what "good" candidates look like.

3. Why were historical decisions treated as unbiased ground truth?  
   → No bias review of the training data was conducted before model development began.

4. Why was no bias review conducted?  
   → The concept of training data bias — and its consequence in model outputs — was not part of the project's risk assessment.

5. Why was bias not in the risk assessment?  
   → No governance framework existed requiring fairness analysis as part of AI development for HR applications.

**Root Cause:** Governance gap — no requirement for bias analysis or fairness evaluation in the AI development process, resulting in a model that systematically discriminated without anyone identifying the risk during development.

**Contributing Factors:**
- Training on ten years of historically male-dominated hiring data without demographic adjustment
- No fairness metrics defined or measured during development or validation
- The model used proxy variables correlated with gender that evaded simple keyword filtering
- No independent review of the model's outputs for demographic disparities before testing

---

## 3. Risk Category

**Primary:** Bias / Fairness Incident  
**Secondary:** Governance Failure, Model Failure

---

## 4. Control Failures

| Control | Type | Failure Mode | Description |
|---|---|---|---|
| Training data bias audit | Preventive | Absent | No assessment of demographic representation and historical bias in training data before model development |
| Fairness metrics definition | Preventive | Absent | No fairness metrics (demographic parity, equalised odds) defined as acceptance criteria for the model |
| Disparate impact testing | Preventive / Detective | Absent | No testing of model outputs for differential performance across gender or other protected characteristics |
| AI impact assessment | Preventive | Absent | No structured assessment of the risk that the AI system could harm protected groups |
| Independent model validation | Detective | Inadequate design | Validation did not include fairness or bias evaluation |
| Proxy variable analysis | Preventive | Absent | No analysis of features correlated with protected characteristics that the model might learn to use |

---

## 5. Applicable Frameworks

### ISO 42001
- **Annex A — Bias evaluation:** ISO 42001 explicitly requires bias evaluation as part of the AI system development lifecycle. This control was entirely absent.
- **Clause 6.1 — Risk assessment:** The risk that an AI hiring tool would replicate or amplify historical discrimination was foreseeable and should have been identified in a risk assessment.
- **Clause 8 — AI system lifecycle:** Development and validation controls must address fairness — the model's development process did not.

### NIST AI RMF
- **MAP:** The risk of bias in a recruitment AI trained on historical data — a well-understood risk in the AI fairness literature — was not mapped. This is a fundamental MAP function failure.
- **MEASURE:** No fairness metrics were defined or measured. The entire MEASURE function was absent for the fairness risk dimension.
- **GOVERN:** No organisational policy or requirement existed for fairness evaluation in AI development.

### OWASP LLM Top 10
- **LLM09 — Overreliance:** The project team over-relied on the model's technical performance (accuracy on historical data) without recognising that "accuracy" against biased ground truth replicates, not resolves, the bias.

---

## 6. Regulatory Implications

**US Employment Law (Title VII, Civil Rights Act):** An AI system that systematically penalises female candidates based on gender-correlated signals constitutes discriminatory employment practice under Title VII. Had the system been used, Amazon would have faced significant legal exposure. The Equal Employment Opportunity Commission (EEOC) has issued guidance making clear that AI-driven discrimination is not a legal defence.

**EU AI Act (prospective):** Employment and recruitment AI is explicitly listed as high-risk AI in EU AI Act Annex III. A system producing gender-discriminatory outputs would fail conformity assessment requirements for accuracy, robustness, and non-discrimination.

**UK Equality Act 2010:** Using an AI system that produces differential outcomes by gender in recruitment constitutes direct or indirect sex discrimination — regardless of intent. The Equality Act applies to the outcome, not the mechanism.

**India — DPDP Act and Labour Law:** Processing of candidates' personal data in AI recruitment systems requires a lawful basis under the DPDP Act. Discriminatory AI in hiring intersects with emerging Indian labour law developments around algorithmic employment decisions.

---

## 7. BFSI Impact

**Applicability:** High. Financial services organisations use AI extensively in recruitment — particularly for high-volume graduate and junior hiring, where automated screening is economically attractive.

**Specific BFSI Risks:**
- BFSI firms already face regulatory scrutiny on diversity and inclusion from the FCA (diversity and inclusion reporting requirements), PRA, and ECB. AI recruitment tools that produce discriminatory outcomes would directly worsen regulatory standing.
- Gender bias in AI hiring tools in BFSI would disproportionately affect sectors already characterised by documented gender gaps (trading, investment banking, technology roles within banks).
- FCA and PRA supervisory expectations increasingly include governance of technology systems used in employment decisions. An AI hiring tool without fairness evaluation is inconsistent with SS1/23 model governance expectations when used at scale.

**BFSI Regulatory Frameworks:**
- FCA: Diversity and inclusion reporting; Consumer Duty (internal culture feeding into service delivery)
- PRA SS1/23: Model risk management covers material models including employment screening AI
- EU AI Act: Annex III explicitly covers employment AI

---

## 8. Lessons Learned

**Lesson 1 — Historical data encodes historical discrimination**  
Any AI system trained on historical human decisions inherits the biases in those decisions. This is not a bug in the model — it is the model doing exactly what it was trained to do. Using historical hiring data to train a hiring model, without bias analysis, will reproduce whatever discrimination existed in those decisions.  
Applicability: All AI systems trained on historical human decision data (credit, hiring, insurance, parole, medical triage).  
Urgency: Critical.

**Lesson 2 — Removing protected characteristics does not remove discrimination**  
Amazon's team knew about gender bias and removed explicit gender signals from the feature set. The model continued to discriminate through proxy variables. Proxy discrimination requires disparate impact testing — examining outcomes across demographic groups — not just feature engineering.  
Applicability: All AI systems where discrimination risk exists. Feature engineering alone is not a fairness control.  
Urgency: Critical.

**Lesson 3 — "Accurate against historical data" is not a fairness measure**  
The model was technically successful — it accurately predicted which candidates would be hired based on historical patterns. This is precisely the problem. Technical performance metrics and fairness metrics are orthogonal. High accuracy against biased ground truth is high accuracy at discrimination.  
Applicability: All AI evaluation and validation processes. Fairness metrics must be defined independently of accuracy metrics.  
Urgency: High.

**Lesson 4 — AI impact assessments must precede development, not follow it**  
The risk that a recruitment AI trained on historical data would reproduce gender bias was foreseeable before a single line of code was written. An impact assessment conducted before development begins would have identified this risk and required mitigation strategies as a condition of proceeding.  
Applicability: All AI systems making decisions about individuals.  
Urgency: High.

---

## 9. Recommended Controls

| Control | Description | Complexity | Priority | Framework Reference |
|---|---|---|---|---|
| Training data demographic audit | Before model development, audit training data for demographic representation and historical disparate outcomes | Low | Critical | ISO 42001 Annex A; NIST MAP |
| Fairness metrics as acceptance criteria | Define fairness metrics (demographic parity, equalised odds, etc.) as hard acceptance criteria that the model must meet before deployment | Low | Critical | ISO 42001 Annex A; NIST MEASURE |
| Disparate impact testing | Test model outputs across all protected characteristic subgroups before and after deployment | Medium | Critical | ISO 42001 Annex A; NIST MEASURE; EU AI Act |
| AI impact assessment for HR AI | Conduct structured impact assessment covering discrimination risk before development begins | Low | High | ISO 42001 Cl.6; EU AI Act Annex III |
| Proxy variable analysis | Analyse all features for correlation with protected characteristics; assess model sensitivity to proxy variables | Medium | High | ISO 42001 Annex A; NIST MEASURE |
| Independent fairness validation | Commission independent fairness validation by a team not involved in model development | Medium | High | ISO 42001 Cl.8; NIST MEASURE |
| Production monitoring for bias drift | Monitor demographic distributions in model outputs in production; alert on emerging disparities | Medium | Medium | ISO 42001 Cl.9; NIST MEASURE |

---

## 10. Executive Summary

Between 2014 and 2017, Amazon developed an AI system to automate recruitment screening. The system learned from ten years of the company's hiring decisions — decisions made in a male-dominated technology industry. As a result, the model learned to penalise female candidates, systematically downgrading CVs containing female-associated signals. Amazon scrapped the project when engineers could not guarantee the bias had been eliminated.

The root cause is not a technical failure — it is a governance failure. No one required a bias analysis before training began. No fairness metrics were defined for the model to meet. No assessment was made of the risk that a model trained on biased historical data would reproduce that bias. The model did exactly what it was designed to do: replicate the pattern of past hiring decisions. The problem was that past hiring decisions were discriminatory.

This pattern — AI trained on historical human decisions replicating historical human bias — is the single most common source of AI fairness failures. It applies to credit scoring, insurance underwriting, parole recommendations, and medical triage, not only recruitment.

The essential action is to require bias evaluation as a mandatory step in AI development — not a post-hoc check, but an upfront condition. Any AI system making decisions about individuals must demonstrate that it produces equitable outcomes across demographic groups before it is deployed. A model that cannot demonstrate this must not be used.
