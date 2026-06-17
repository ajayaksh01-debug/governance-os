# Boundaries — What Ethana Does Not Solve

This is the section most sales motions skip. For regulated enterprise buyers, overpromising here is immediately disqualifying. State these boundaries before procurement finds them.

## 1. Model bias auditing

Ethana cannot audit model weights, test disparate impact across demographic groups, or produce the bias audit that EU AI Act Art.10 or NYC Local Law 144 requires. The Bias guardrail scanner screens content at runtime; it is not a model bias audit. Bias auditing requires a specialist third-party auditing firm.

## 2. It is not a GRC platform

Ethana produces evidence that feeds a GRC platform (Archer, ServiceNow, OneTrust). It does not replace one. If a buyer expects Ethana to manage their full governance, risk, and compliance workflow, reset that expectation.

## 3. GDPR Art.22 enforcement

Ethana can log that a significant automated decision occurred. It cannot enforce the safeguard. It cannot build the human-review pathway or the "contest this decision" mechanism inside the customer's application. Ethana is part of the evidence layer, not the safeguards layer. Banks will try to use it as an Art.22 compliance tool. It is not one.

## 4. Legacy and non-LLM systems

SQL pipelines, batch jobs, rules engines, and deterministic decisioning systems have no AI API call for Ethana to intercept. The gateway, guardrails, and audit log do not apply. For a bank with a large legacy automated estate, the honest answer is: Ethana is the right tool for your LLM-based applications; for legacy systems, only Discovery (inventory, and that is Roadmap) is relevant, or a Cursory advisory inventory engagement.

## 5. Non-LLM REST APIs at the gateway

Whether the gateway can proxy and log non-LLM REST APIs (AVM valuation, NLP scoring engines, ASR) in the same audit schema is unconfirmed. Until product confirms in writing, the audit-trail and governance value applies to the LLM API layer only. This is a scoping statement that must appear in procurement conversations, because a bank's AI estate includes non-LLM systems and the gap is exposed in technical due diligence.

## 6. Knowledge base / RAG content quality

If a RAG knowledge base contains outdated, biased, or incorrect documents, Ethana cannot detect or fix that. It has no visibility into what is in the vector database or when documents were last updated. The content approval workflow (who approves documents, expiry, version control) requires a CMS-integrated process (Confluence, SharePoint) outside Ethana's architecture. Ethana governs the LLM interaction layer, not the knowledge layer.

## 7. Coverage equals gateway adoption

Every governance value (audit trail, guardrails, cost control) applies only to traffic routed through the gateway. Traffic on direct provider keys outside Ethana is ungoverned and unlogged. The completeness of governance equals the completeness of gateway adoption across the organisation.

## The honest one-line summary

Ethana is a control layer for LLM-based applications that route through its gateway. It is not a compliance platform, not a GRC platform, not a bias auditor, not an Art.22 safeguard, and not a governor of legacy or non-LLM systems. A CRO who expects more than a control layer will be disappointed unless that gap is filled by Cursory Services.
