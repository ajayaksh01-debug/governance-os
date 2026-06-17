# Deployment and Certifications

This file holds the deployment model and the certification status. The certifications section contains hard procurement blockers for financial services. Surface them proactively.

## Deployment

Confirmed:
- On-prem and VPC deployment supported.
- Pricing parity between deployment models. A regulated buyer does not pay a premium for the deployment they are required to use. This removes a common objection.

Differentiator for RBI-regulated and data-localisation accounts:
- India VPC deployment with PII masking at the gateway. This is the positioning against global SaaS governance tools for accounts that cannot route customer data through external cloud.

Hard caveat:
- On-prem deployment at Tier 1 bank scale is unproven. The deployment model is supported; it has not been demonstrated at the scale and complexity of a large bank. State this. Do not present on-prem at institutional scale as proven.

Why on-prem is the default offer in BFSI:
- Across the Barclays use cases that reached deployment consideration, the conclusion was consistent: on-prem or VPC is non-negotiable. Call content is GDPR personal data, mortgage data is FCA-regulated, customer query data cannot route through external cloud. For BFSI, offer on-prem or VPC as the default, not as a premium add-on.

## Account and identity management

Confirmed in production:
- Tenants, projects.
- RBAC.
- SSO via OIDC.

In build (not available):
- SCIM provisioning, including automated AI-vendor offboarding. Do not claim automated offboarding.

## Certifications — hard procurement blockers

All three are in progress, not complete. None may be stated as held.

| Certification | Status | Procurement impact |
|---|---|---|
| SOC 2 Type II | In progress | Standard gate for financial services vendor onboarding. Its absence blocks or delays procurement at most banks. This is the single most common blocker for financial-services accounts. |
| ISO 27001 | In progress / unverified | Frequently mandated for vendor information-security assurance. |
| HIPAA-ready | In progress | Relevant for healthcare / life-sciences accounts handling PHI. |

Rules:
- Do not list any of these as obtained.
- Raise them proactively in qualification. A blocker discovered by procurement late in a cycle costs more credibility than one disclosed early.
- For accounts where SOC 2 is a hard gate (most Tier 1 financial services), sequence the opportunity to land after completion, or scope an initial engagement that does not depend on the certification (for example a Cursory advisory engagement, or a non-production pilot), with the platform purchase following certification.

## Procurement questions to expect

- When will SOC 2 Type II be complete, and can we see the Type I report and the auditor in the meantime?
- Is on-prem deployment running in production at any institution of comparable scale to ours?
- Where does data reside in the VPC model, and how is PII masked at the gateway?
