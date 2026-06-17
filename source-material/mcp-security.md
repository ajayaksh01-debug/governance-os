# MCP Security

**Status: Production core, identity (NHI) In Build.** Separate these two explicitly. The broker works. The agent-identity feature does not.

## What it is

MCP (Model Context Protocol) is a standard way for AI agents to call tools (read a calendar, query a database, post to a channel). Ethana's MCP Broker is the checkpoint every tool call passes through. It registers servers, enforces an allow-list, rate-limits, and traces each call.

Confirmed in production:
- Server registry.
- Hosted runtime.
- Tool allow-list.
- Rate limits.
- Per-call tracing.
- Admin UI.
- Approximately 8,000 lines in production.

In build (not available):
- Non-Human Identity (NHI) for agents: ephemeral scoped tokens, OAuth 2.0 token exchange / SPIFFE-style workload identity, on-behalf-of delegation.

## Why the In Build gap matters

The core risk a bank cares about is that agents act autonomously using a human's full credentials. A compromised agent then equals a compromised employee. NHI is the feature that solves this by giving agents their own scoped, ephemeral identity. Until NHI ships, agent identity separation is not solved. Do not imply that it is.

So the honest position is: the broker gives you registry, control, and a per-call trace today. It does not yet give agents their own identity. That arrives with NHI, which is in build.

## What it does not do

- It does not govern agent behaviour at the model level (whether the agent interprets a tool result correctly).
- It does not capture actions an agent takes outside MCP, for example a direct API call that bypasses the broker.

## Regulatory hooks

- NIST AI RMF MAP 1.6

## Procurement questions it must survive

- When does NHI ship? Without it, how do you separate agent identity from user identity today?
- What stops an agent from making a direct API call that bypasses the broker entirely?
- Is the per-call trace forwarded to the immutable audit log and our SIEM?
