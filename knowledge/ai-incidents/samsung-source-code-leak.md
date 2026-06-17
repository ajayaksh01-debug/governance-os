# Samsung Source Code Leak via ChatGPT

## Incident Summary

In April 2023, Samsung Electronics reported three separate data leak incidents within a span of twenty days, all involving employees using ChatGPT to assist with work tasks. In each case, employees inadvertently submitted sensitive proprietary information to ChatGPT's servers — where it was used to train OpenAI's models under the terms of service in effect at the time.

The incidents occurred within weeks of Samsung lifting its internal ban on ChatGPT use.

---

## What Happened

**Incident 1 — Source Code for Semiconductor Equipment**
A Samsung engineer submitted source code from a semiconductor measuring tool to ChatGPT and asked the model to identify bugs. The code was proprietary and represented significant intellectual property.

**Incident 2 — Internal Meeting Notes**
An employee uploaded notes from an internal meeting — including sensitive business strategy discussions — and asked ChatGPT to summarise them.

**Incident 3 — Source Code for Internal Application**
A third employee submitted additional source code and asked ChatGPT to convert it into a different programming language.

In all three cases, the data was processed by OpenAI's systems and, under the terms of service applicable at the time, could be used for model training. Samsung had no mechanism to prevent, detect, or respond to these disclosures at the time they occurred.

---

## Root Cause Analysis

### Governance Failure — Policy
Samsung had no policy governing employee use of external AI tools at the time the incidents occurred. The internal ChatGPT ban had been lifted without replacement controls — employees had access to the tool but no guidance on what data could be submitted.

### Governance Failure — Awareness and Training
Employees did not understand that data submitted to ChatGPT was processed on external servers and potentially retained for model training. The distinction between a private tool and an external service was not communicated.

### Technical Failure — No Data Loss Prevention (DLP)
Samsung had no technical controls to prevent submission of classified or proprietary data to external AI services. DLP tools that could have detected and blocked code or confidential documents being submitted to external endpoints were not deployed for this vector.

### Governance Failure — Vendor Assessment
OpenAI's data handling and training practices were not assessed before employees were permitted to use the service. The terms of service — which permitted training data use — were not reviewed.

---

## Controls That Were Absent

| Control | Description |
|---|---|
| AI Use Policy | Formal policy defining permitted and prohibited uses of external AI tools, including data classification restrictions |
| Employee Training | Awareness training on data handling when using AI tools, specifically covering the cloud-processing nature of public AI services |
| Data Loss Prevention | Technical controls to detect and block submission of code, confidential documents, or classified data to external AI endpoints |
| Vendor Assessment | Security and privacy assessment of AI service providers before organisational use is permitted |
| Tool Approval Process | A formal process for approving AI tools before employees may use them for work tasks |

---

## Consequence and Response

Samsung banned employees from using ChatGPT and other generative AI tools on company devices following the incidents. The company subsequently began developing internal AI tools (based on a private deployment model) to provide similar functionality without data leaving Samsung's environment.

The financial and reputational impact of the specific incidents has not been publicly quantified. However, the disclosed source code relates to Samsung's semiconductor manufacturing — a domain of extreme competitive sensitivity given the global semiconductor supply chain dynamics at the time.

---

## Business Impact

- **Intellectual property risk:** Source code for proprietary manufacturing equipment and internal applications submitted to an external service. Potential for competitive intelligence exposure.
- **Regulatory exposure:** Depending on jurisdiction, submission of employee or business personal data may constitute a personal data breach under GDPR or equivalent laws.
- **Reputational:** Public disclosure of the incidents created reputational pressure on Samsung and accelerated regulatory and enterprise scrutiny of AI tool governance globally.

---

## Lessons and Recommendations

1. **Never lift a technology ban without replacement controls.** The removal of Samsung's ChatGPT ban without an AI use policy was the proximate cause of all three incidents. A phased approach — pilot with controlled user group, assess risks, then scale with controls — is the correct sequence.

2. **Classify data before deploying AI tools.** Employees cannot make appropriate judgements about what to submit to AI tools if they do not know what data is sensitive. A functioning data classification scheme is a prerequisite for AI tool governance.

3. **Extend DLP to AI endpoints.** Modern DLP tools can detect code, documents, and data patterns being submitted to external web services. This is a technical control that can be implemented quickly and is highly effective.

4. **Assess AI vendors before permitting use.** Terms of service for public AI tools vary significantly in their data handling, training use, and retention provisions. This is a vendor risk assessment, not a legal formality.

5. **Prefer private deployments for sensitive workloads.** Samsung's post-incident response — building internal AI tools — is the right long-term answer for organisations handling sensitive IP. For many use cases, a private LLM deployment on enterprise infrastructure removes the data exfiltration risk entirely.

6. **Assume employees will use AI tools regardless of policy.** Shadow AI use is the norm, not the exception. Governance programmes that rely solely on prohibition will fail. Providing approved, safe AI tools is the most effective way to reduce unsanctioned use.

---

## Framework Mapping

| Framework | Relevant Control |
|---|---|
| ISO 42001 | Annex A — Supply chain controls; Data governance |
| NIST AI RMF | GOVERN — Policy; MAP — Third-party AI risks |
| OWASP LLM Top 10 | LLM06 — Sensitive Information Disclosure; LLM05 — Supply Chain |
| EU AI Act | Article 26 — Deployer obligations; data governance |
