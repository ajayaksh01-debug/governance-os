# Guardrails

**Status: Production.** All scanners shipped. Sub-200ms p95 stated, pending load validation.

## What it is

A set of native scanners that inspect AI traffic bidirectionally (both the prompt going in and the response coming out) at the gateway. Each scanner can be configured per project.

Confirmed in production: six native scanners.

The six per the board briefing and the production-status table (the two most authoritative internal sources):
1. Secrets
2. PII Detection
3. Prompt Injection
4. Jailbreak
5. Toxicity
6. Bias

**Source discrepancy to resolve.** One internal document (the commercial playbook) lists the sixth scanner as Hallucination Grounding rather than Secrets. The brochure lists Relevance Validation and Output Toxicity as additional items. Confirm the exact production scanner set with the product team before committing it in a proposal. Do not list a scanner you cannot demonstrate.

## What it does not do

- The Bias scanner is not a model bias audit. It screens content at runtime. It does not inspect model weights, test disparate impact across demographic groups, or produce the bias audit that EU AI Act Art.10 or NYC Local Law 144 requires. That requires a specialist third-party auditing firm.
- PII detection false-positive rate at volume is unconfirmed. A bank will ask. Do not quote a figure you do not have.
- Targeting specific JSON field keys (rather than free-text scanning) is unconfirmed.
- Guardrails are prevention at the call boundary. They are not a substitute for red-teaming (which tests) or for knowledge-base governance (which Ethana does not provide).

## Regulatory hooks

- EU AI Act Art.9 (risk management system)
- NIST AI RMF GOVERN 1.4
- DPDP (data minimisation, via PII handling)

## Procurement questions it must survive

- Exactly which scanners are in production, and can each be shown live?
- Does the stated sub-200ms p95 hold with the full guardrail stack running simultaneously (for example PII plus hallucination grounding) on a high-volume synchronous RAG pipeline? Ask for benchmark data under production-like load.
- What is the PII detection false-positive rate, and can rules target specific structured fields?
