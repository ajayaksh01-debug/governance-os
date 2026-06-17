# AI Gateway

**Status: Production.** Non-LLM REST API coverage: unconfirmed (treat as out of scope until written confirmation).

## What it is

An OpenAI-compatible API front door for AI traffic. Applications send their model calls to Ethana instead of directly to a provider. Ethana routes the call to the chosen model, applies guardrails, captures the call for the audit log, and attributes its cost.

Confirmed in production:
- Model-agnostic routing across LLM providers: OpenAI, Anthropic, Gemini, Groq, and self-hosted models.
- Multi-tenant.
- Routing and fallback.
- CallTrace (per-call tracing) and per-call cost capture.
- Stated overhead of approximately 50ms for the gateway itself (separate from the guardrail stack, which adds its own latency).

## What it does not do

- It does not govern calls that bypass it. Coverage equals whatever traffic is actually routed through the gateway. A bank with direct provider API keys in use outside Ethana has ungoverned traffic.
- Non-LLM REST APIs are unconfirmed. Whether the gateway can proxy and log a rules-based ML scoring endpoint, a third-party AVM valuation API, or an ASR transcription API in the same audit schema as LLM calls is not confirmed. Until product confirms in writing, scope the gateway value to the LLM API layer only. This matters because a meaningful part of a bank's AI estate is non-LLM, and overclaiming here is exposed immediately in technical due diligence.
- It is not a model bias auditor or a content-quality checker for the data behind a call.

## Regulatory hooks

- RBI FREE-AI 3.1
- EU AI Act Art.13 (transparency)
- ISO 27001 A.12.4 (logging)

## Procurement questions it must survive

- Is the gateway LLM-only, or can it proxy non-LLM REST APIs and capture immutable logs for them in the same schema? (If LLM-only, state that the audit-trail value applies to a subset of the AI estate.)
- What is the p95 latency overhead of the full stack (gateway plus all guardrails plus audit logging) for a synchronous call at the bank's expected throughput, for example 500 rps in a contact-centre application? Ask for tested data, not a synthetic sub-200ms claim.
- What happens to the application when the gateway has an outage? Is there a circuit-breaker, a fallback bypass mode, or does the application fail with the governance layer?
