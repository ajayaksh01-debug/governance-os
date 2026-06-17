# Cost Controls

**Status: Production at project level, full FinOps In Build.** Project-level governance is live. Per-user granularity is not.

## What it is

Spend governance for AI traffic routed through the gateway, built on virtual API keys.

Confirmed in production:
- Virtual API keys per team and per project.
- Per-project budget caps.
- Real-time spend dashboard.
- Budget alerts.
- Per-tenant and per-project cost tracking with alert hooks.

In build (not available):
- Per-user attribution.
- Per-team breakdowns.
- GPU cost tracking.
- Dormant-licence detection.

These four together are the full FinOps capability. They are in build, not live.

## Why this matters in BFSI

The buyer pain is unattributable AI spend: no per-user or per-team visibility, licences persisting after employees leave, and no line-item control for the CFO. Project-level governance addresses the platform and team layer of that problem today. The per-user and dormant-licence layer arrives with full FinOps. Be precise about which layer you are solving.

A secondary procurement value: platform-based, node-priced cost (not per-seat or per-token) lets a procurement team model total cost with certainty. That is a genuine differentiator in regulated enterprises where usage is unpredictable. It belongs in the commercial conversation, not as a platform capability claim.

## What it does not do

- No per-user spend attribution today.
- No GPU or infrastructure cost tracking today.
- It governs cost of traffic through the gateway only. Spend on direct provider keys outside Ethana is invisible to it.

## Procurement questions it must survive

- Can we attribute spend to an individual user today, or only to a project?
- Can it detect and flag dormant or orphaned AI licences?
- Does it track GPU and infrastructure cost, or only token / API spend?
