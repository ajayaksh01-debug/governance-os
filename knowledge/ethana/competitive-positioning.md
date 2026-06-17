# Competitive Positioning

*Note: This document supplements the high-level competitor categories listed in `buyer-solution-mapping.md` with specific battle-card intelligence extracted from the Ethana Marketing Playbook and Product Study.*

## Core Differentiation Principle
Ethana overlaps with several point solution categories. The competitive framing is always: **Ethana provides these capabilities in an integrated runtime control plane**, not as isolated tools requiring separate procurement, integration, and governance models.

## Competitor Categories & Handling

### 1. AI Security & DLP (CASBs)
**Competitors:** LayerX, Nightfall, Calypso AI, HiddenLayer  
**Ethana Differentiation:** 
Traditional DLP and CASB tools are not AI-aware. They do not understand model selection, MCP servers, or the specific context of an AI interaction. Ethana provides AI-specific observability and control (e.g., model attribution, agent tool inventory) that standard DLP cannot produce. Ethana acts inline at the API layer, not just as a network proxy.

### 2. Enterprise AI Chat
**Competitors:** Microsoft Copilot, Glean, ChatGPT Enterprise  
**Ethana Differentiation:**
*Warning: The marketing playbook positions "Ethana Workspace" against these tools, but Workspace is currently unverified in `capability-status.md`.* 
Where applicable, the differentiation is that Ethana provides a fully self-hosted, governed boundary where customer data, prompts, and responses never leave the organization's infrastructure, unlike SaaS wrappers around public APIs.

### 3. AI Governance & Policy Platforms
**Competitors:** Credo AI, AIShield, OneTrust, Archer  
**Ethana Differentiation:**
Ethana provides **operational runtime governance**, not just policy documentation. GRC platforms manage your risk register and compliance workflows. Ethana intercepts the actual API calls, enforces the guardrails at runtime, and produces the immutable evidence that feeds *into* those GRC platforms. 

### 4. Agent Development Platforms
**Competitors:** LangChain, CrewAI  
**Ethana Differentiation:**
These frameworks help developers build agents but provide zero enterprise governance. Ethana Build provides the infrastructure to govern them: MCP lifecycle management, non-human identity (NHI - *in build*), tool allow-listing, and audit trails for autonomous agent actions.

### 5. Open-Source AI Gateways
**Competitors:** LiteLLM, Kong (AI features)  
**Ethana Differentiation:**
While open-source gateways provide routing, they lack enterprise governance. Ethana provides PromptOps, LLM evaluation pipelines, 21 OWASP red-teaming probes, and MCP governance built-in. Internal engineering teams attempting to build their own gateway using open-source components rarely replicate the full governance and audit stack required by compliance teams.
