# Ethana Platform — Overview

## What Ethana is

Ethana is a runtime AI control plane. It is software that sits inline in the request path between enterprise applications and AI models. Every AI call that is routed through Ethana can be governed, scanned, logged, and cost-attributed at the point the call is made.

Ethana is infrastructure, not advisory. It runs without a consultant present. The governance judgement (which controls apply, how policy is designed, how risk is framed) is not part of the platform. That is Cursory Services. See `../cursory-services/overview.md`.

## What Ethana is not

- It is not a GRC platform. It produces evidence that feeds a GRC platform (Archer, ServiceNow, OneTrust). It does not replace one.
- It is not a compliance platform. It is a control layer. A CRO will expect governance framework design, vendor compliance assessment, bias auditing, and policy documentation that Ethana does not provide.
- It is not an assessment or advisory tool. It does not run AI risk assessments, gap analyses, or maturity scoring. Those are human-delivered Cursory engagements.
- It is not a model-bias auditor. It cannot inspect model weights or test disparate impact across demographic groups.

## Architecture, in one line

Applications send AI calls to Ethana. Ethana applies guardrails, routes the call to the chosen model, logs the call immutably, attributes its cost, and (for agent tool calls) brokers and traces the MCP request. Red-teaming runs against these systems out of band.

## Core capability set

The platform's confirmed core, the part that is Production and consistently maps to a hard regulatory requirement, is the **Gateway plus Immutable Audit Log plus Guardrails** combination. Everything else is additive.

| Capability | Headline status | Detail |
|---|---|---|
| AI Gateway | Production | `capabilities/ai-gateway.md` |
| Guardrails | Production | `capabilities/guardrails.md` |
| Immutable Audit Logs | Production | `capabilities/immutable-audit-logs.md` |
| MCP Security | Production core, identity In Build | `capabilities/mcp-security.md` |
| Red Teaming | Production core, CI/CD gate In Build | `capabilities/red-teaming.md` |
| Cost Controls | Production at project level, full FinOps In Build | `capabilities/cost-controls.md` |

Account management (tenants, projects, RBAC, SSO via OIDC) is Production. SCIM provisioning is In Build. See `deployment-and-certifications.md`.

## The capability boundary that matters most

Ethana governs AI calls that pass through its gateway. It has no visibility into:

- calls that bypass the gateway
- AI that runs locally on a device with no network call
- legacy rules-based and non-LLM systems that have no AI API call to intercept
- the quality of a RAG knowledge base behind a governed call

This boundary is the difference between a defensible procurement conversation and a disqualifying one. It is stated in full in `boundaries.md` and must be raised proactively, not when asked.
