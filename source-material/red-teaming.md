# Red Teaming

**Status: Production core, CI/CD gate In Build.** Probes and orchestrator are live. Pipeline integration is not.

## What it is

An automated red-teaming orchestrator that runs attack probes against AI systems and scores the results. It targets the model, the LLM application, and the agent.

Confirmed in production:
- Orchestrator with scoring and a cost cap.
- 21 OWASP probes.
- Multi-turn attacks.
- Targets model, LLM-app, and agent layers.

In build (not available):
- CI/CD gate (the "ethana eval action" that runs on every pull request).
- Bank-specific custom YAML probes require configuration investment; they are not pre-built.

## What it does not do

- It is testing, not runtime defence. Red-teaming finds weaknesses. Guardrails prevent them inline. Do not conflate the two.
- It is not a model bias audit.
- RAG-specific attack coverage and the ability to test non-LLM ML classifiers are unconfirmed.

## How it maps to OWASP LLM Top 10

The 21 probes give structured coverage against LLM attack categories. Coverage is deepest where it matters most in enterprise deployments: prompt injection (LLM01), supply-chain and plugin risks (LLM05, LLM07), and excessive agency (LLM08). Confirm the exact probe-to-category mapping with the product team before presenting coverage claims against a specific framework.

## Regulatory hooks

- EU AI Act Art.15 (accuracy, robustness) supports the robustness-testing requirement
- NIST AI RMF MEASURE (robustness, adversarial testing)
- OWASP LLM Top 10 (testing coverage)

## Procurement questions it must survive

- What is the probe coverage for RAG-specific attacks, and can it test our non-LLM ML classifiers?
- Are bank-specific probes pre-built or a configuration engagement?
- When does the CI/CD gate ship, and what does it gate on?

## Note on the service version

Cursory also offers Red Teaming as a recurring service (quarterly exercises with custom probe development and findings-to-policy remediation). That is human-delivered work using this platform capability. See `../cursory-services/services-catalog.md`. Do not present the service and the product capability as the same thing.
