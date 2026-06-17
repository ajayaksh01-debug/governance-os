# Immutable Audit Logs

**Status: Production.** This is Ethana's clearest and strongest enterprise capability. Lead with it.

## What it is

An insert-only event store. Records can be written but never deleted or changed. Every AI call routed through the gateway is logged with timestamp, identity, project, and guardrail verdict.

Confirmed in production:
- Insert-only (write-once) event store.
- Multi-tenant.
- Per-call record: timestamp, identity, project, guardrail verdict.
- SIEM forwarding to Splunk, Elastic, and Datadog.
- Configurable retention.

Across every Barclays use case assessed, the absence of event-level audit logging was cited as a governance failure. This is the one capability that is Production, maps to a hard regulatory requirement, and is not a native feature of a standard API gateway.

## What it does not do

- It logs only what passes through the gateway. Calls that bypass Ethana are not recorded. The completeness of the audit trail equals the completeness of gateway adoption.
- It captures nothing about what happened before traffic entered Ethana.
- Schema fit is not automatic. Whether the log schema captures the exact fields a specific regulator requires (for example the full FCA SYSC 9 record set) requires schema configuration work with the bank's data architecture team. Scope this as an implementation engagement, not an out-of-the-box guarantee.
- It is evidence, not enforcement. For GDPR Art.22 it can log that a significant automated decision occurred. It cannot build the human-review or contest mechanism. See `../boundaries.md`.

## Regulatory hooks

- EU AI Act Art.12 (record-keeping for high-risk AI)
- FCA SYSC 9 (7-year record retention)
- RBI IT Outsourcing Direction
- ISO 42001 Cl.9.1
- GDPR Art.5 (accuracy / accountability records)

## Procurement questions it must survive

- Is it write-once at the database layer, or enforced only at the application layer?
- Can the schema be customised for the specific fields our regulator examines, and is that config work or product work?
- Is retention configurable to 7 years, and where is the data stored (relevant for data-localisation requirements)?
