# Framework Crosswalk

This replaces the earlier `feature-mapping.md`, which mapped frameworks to capabilities Ethana does not have. Here, every framework requirement is mapped to one of three things: a real platform capability (with status), a Cursory Service, or an explicit gap requiring a third party.

Status flags: **[P]** Production, **[IB]** In Build, **[RM]** Roadmap. **[SVC]** marks a Cursory Service. **[GAP]** marks something neither layer provides.

Rule: only **[P]** items may be claimed as available platform capabilities. **[IB]** and **[RM]** are future. **[SVC]** is human-delivered. **[GAP]** requires a third party.

---

## EU AI Act (high-risk AI, Articles 9 to 15 and 72)

| Requirement | Mapped to |
|---|---|
| Art.9 risk management system | Guardrails **[P]** (runtime risk controls); Risk assessment **[SVC]** (the documented system) |
| Art.10 data governance and bias | Bias scanner **[P]** for runtime screening; model bias audit **[GAP]** (third-party auditor); data governance assessment **[SVC]** |
| Art.11 technical documentation | Compliance Pack **[IB]**; documentation **[SVC]** today |
| Art.12 record-keeping | Immutable Audit Log **[P]**. Strongest direct mapping in the platform. |
| Art.13 transparency | Gateway **[P]** (call transparency, routing record); disclosure design **[SVC]** |
| Art.14 human oversight | **[GAP]** in the application; oversight mechanism design **[SVC]**. The platform logs decisions, it does not enforce oversight. |
| Art.15 accuracy and robustness | Red Teaming **[P]** (robustness testing); Guardrails **[P]** |
| Art.72 post-market monitoring | Immutable Audit Log **[P]** plus Compliance Pack **[IB]** |
| Conformity assessment for high-risk | **[GAP]** notified-body involvement required |

Honest summary: Ethana maps cleanly to Art.12 today and supports Art.9, Art.13, and Art.15 through Production capabilities. Art.10 bias audit, Art.14 oversight enforcement, and conformity assessment are not platform capabilities.

---

## ISO 42001

| Clause / control | Mapped to |
|---|---|
| Cl.4 context, Cl.5 leadership, Cl.6 planning | **[SVC]** (policy, governance structure, risk methodology) |
| Cl.8 operation — AI lifecycle | Gateway **[P]**, MCP Broker **[P]**; lifecycle governance **[SVC]** |
| Cl.8 — third-party provider management | **[SVC]**; vendor tracking via Discovery **[RM]** |
| Cl.9.1 monitoring and measurement | Immutable Audit Log **[P]**; Cost dashboard **[P]** |
| Cl.9.2 internal audit | Audit Log evidence **[P]**; Compliance Pack **[IB]**; audit support **[SVC]** |
| Cl.10 improvement / corrective action | **[SVC]** |
| Annex A — bias evaluation | Bias scanner **[P]** (runtime); model bias audit **[GAP]** |
| Annex A — human oversight | **[GAP]** in app; design **[SVC]** |
| Annex A — incident management | Red Teaming **[P]** (proactive); incident response process **[SVC]** |

Honest summary: ISO 42001 is a management-system standard. Most clauses are satisfied by the governance program (Service), not by software. The platform contributes monitoring evidence (Cl.9), runtime controls (Annex A), and audit trails. Certification readiness is a Cursory engagement.

---

## NIST AI RMF

| Function | Mapped to |
|---|---|
| GOVERN | Governance structure **[SVC]**; accountability documentation via Audit Log **[P]** |
| MAP — use-case identification | Discovery **[RM]**; AI Inventory engagement **[SVC]** |
| MAP — regulatory obligation identification | Framework Mapping **[SVC]**; Compliance Pack **[IB]** |
| MAP 1.6 — agent / tool mapping | MCP Broker **[P]** |
| MEASURE — robustness, adversarial testing | Red Teaming **[P]** |
| MEASURE — bias and fairness metrics | Bias scanner **[P]** (runtime); formal bias measurement **[GAP]** |
| MEASURE — performance monitoring | Audit Log **[P]**; Cost dashboard **[P]** |
| MANAGE — control implementation | Guardrails **[P]**; implementation **[SVC]** |
| MANAGE — incident response | Red Teaming **[P]**; response process **[SVC]** |

Honest summary: strongest platform coverage is in MEASURE (Red Teaming, Guardrails, Audit Log). MAP inventory is Roadmap or Service. GOVERN is mostly Service.

---

## OWASP LLM Top 10

| Risk | Mapped to |
|---|---|
| LLM01 Prompt Injection | Prompt Injection scanner **[P]**; Red Teaming probes **[P]** |
| LLM02 Insecure Output Handling | Guardrails output scanning **[P]** |
| LLM03 Training Data Poisoning | **[GAP]** (training-side); supply-chain review **[SVC]** |
| LLM04 Model Denial of Service | Rate limits via Gateway / MCP Broker **[P]** |
| LLM05 Supply Chain | **[SVC]**; Discovery vendor tracking **[RM]** |
| LLM06 Sensitive Information Disclosure | PII and Secrets scanners **[P]** |
| LLM07 Insecure Plugin / Tool Design | MCP Broker allow-list and tracing **[P]**; NHI **[IB]** |
| LLM08 Excessive Agency | MCP Broker **[P]** (scope control); NHI **[IB]** (identity) |
| LLM09 Overreliance | **[GAP]** (process); oversight design **[SVC]** |
| LLM10 Model Theft | Gateway access control **[P]**; Red Teaming extraction probes **[P]** |

Honest summary: the platform gives direct runtime or testing coverage for most categories. The deepest gaps are training-side (LLM03) and process-side (LLM09), neither of which is a runtime control problem.

---

## BFSI model risk — SR 11-7 / PRA SS1/23

| Requirement | Mapped to |
|---|---|
| Model identification and inventory | Discovery **[RM]**; AI Inventory engagement **[SVC]** |
| Model development documentation | **[SVC]** |
| Model validation | Red Teaming **[P]** (LLM-specific testing); traditional quantitative validation **[GAP]** |
| Ongoing monitoring | Audit Log **[P]** |
| Governance and culture | **[SVC]** |

Honest summary: Ethana extends model-risk practice to LLMs through testing and monitoring. It does not replace quantitative model validation and does not produce the model inventory as software today.

---

## RBI FREE-AI (August 2025) and RBI IT Outsourcing

| Requirement | Mapped to |
|---|---|
| FREE-AI 3.1 (transparency / traceability of AI) | Gateway **[P]**; Audit Log **[P]** |
| Audit and record retention | Immutable Audit Log **[P]** (configurable retention, SIEM export) |
| Risk assessment | **[SVC]** |
| Vendor / outsourcing risk | **[SVC]**; Discovery **[RM]** |
| Data localisation | On-prem / India VPC deployment **[P]** (caveat: Tier 1 scale unproven) |

Honest summary: RBI accounts are the strongest immediate fit. The Audit Log plus Guardrails plus on-prem / India VPC combination maps directly to the live regulatory drivers. The deployment-at-scale caveat must be stated.

---

## FCA (SYSC 9 and Consumer Duty)

| Requirement | Mapped to |
|---|---|
| SYSC 9 record-keeping (7 years) | Immutable Audit Log **[P]** (retention configurable; schema-fit is a config engagement) |
| Consumer Duty — fair outcomes / vulnerable customers | **[SVC]** (customer-impact assessment); Guardrails **[P]** contribute on harmful-output screening |

---

## DPDP (Rules notified November 2025)

| Requirement | Mapped to |
|---|---|
| Data minimisation / PII handling | PII scanner **[P]**; masking at gateway **[P]** |
| Data localisation | On-prem / India VPC **[P]** (scale caveat) |
| Accountability records | Audit Log **[P]** |

---

## MAS FEAT / Veritas (Singapore)

| Requirement | Mapped to |
|---|---|
| Fairness, ethics, accountability, transparency | Guardrails **[P]** and Audit Log **[P]** contribute to accountability and transparency; the FEAT assessment itself is **[SVC]** |

Note: Singapore accounts (DBS, OCBC, UOB) are a post-SOC-2 market. Do not pursue before certification.

---

## Coverage heat map (platform capabilities only, Production unless flagged)

| Capability | ISO 42001 | NIST AI RMF | OWASP LLM | EU AI Act | SR 11-7 / SS1/23 | RBI FREE-AI |
|---|---|---|---|---|---|---|
| AI Gateway | Medium | Medium | Medium | High (Art.13) | Low | High |
| Guardrails | Medium | High (MEASURE) | High | High (Art.9) | Low | High |
| Immutable Audit Log | High (Cl.9) | High | Low | High (Art.12) | Medium | High |
| MCP Security | Low | Medium (MAP 1.6) | High (LLM07/08) | Medium | Low | Low |
| Red Teaming | Medium | High (MEASURE) | High | High (Art.15) | Medium | Medium |
| Cost Controls | Low | Low | Low | Low | Low | Low |

Key: High = primary capability, Medium = meaningful, Low = incidental. This heat map reflects only Production platform capabilities. Framework areas marked **[SVC]** or **[GAP]** above are not represented here because they are not platform coverage.
