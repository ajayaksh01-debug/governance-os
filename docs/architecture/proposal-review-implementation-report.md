# Ethana Proposal Agent Runtime v0.1 — Implementation Report

**Date:** 2026-06-18  
**Release Version:** v0.1-prod (Dynamic Engine PR-001)  
**Agent:** [Ethana Proposal Agent](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/AGENT.md)  
**Objective:** Establish a production-grade, dynamic runtime environment for auditing client proposals, verifying traceability, and enforcing the Claims Firewall without static fixture recognition.

---

## 1. Files Added & Modified

| File Path | Status | Description |
|---|---|---|
| [`agents/ethana_proposal_agent/runtime/orchestrator.py`](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/runtime/orchestrator.py) | **Added** | Manages intake schema checks, dynamic review execution, score validations, and final human sign-off processes. |
| [`agents/ethana_proposal_agent/runtime/skill_executor.py`](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/runtime/skill_executor.py) | **Modified** | Replaced mock fixture matching with the **Dynamic Claim Analysis Engine**. Performs header/paragraph extraction, canonical model parsing, dynamic findings generation, and dynamically calculates compliance scores. |
| [`agents/ethana_proposal_agent/runtime/state_manager.py`](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/runtime/state_manager.py) | **Added** | Handles state transition validations, including schema halts and firewall breach transitions. |
| [`agents/ethana_proposal_agent/runtime/audit_logger.py`](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/runtime/audit_logger.py) | **Added** | Logs structured, append-only JSONL files verifying intake, gates, and sign-offs. |
| [`agents/ethana_proposal_agent/runtime/schema_validator.py`](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/runtime/schema_validator.py) | **Added** | Validates payloads against proposal-review input/output JSON schemas. |
| [`agents/ethana_proposal_agent/runtime/output_builder.py`](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/runtime/output_builder.py) | **Added** | Compiles signed handoff deliverable folders under `packages/`. |
| [`agents/ethana_proposal_agent/runtime/config.yaml`](file:///Users/ajayrajsingh/Documents/governance-os/agents/ethana_proposal_agent/runtime/config.yaml) | **Added** | Specifies setting thresholds (PCS: 95, CTCS: 95) and folders. |
| [`evaluations/scripts/test_proposal_review_runtime.py`](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/scripts/test_proposal_review_runtime.py) | **Added** | Integration tests validating clean proposal, firewall breach, and mixed-roadmap claims post-corrections. |
| [`evaluations/scripts/agent_certifier.py`](file:///Users/ajayrajsingh/Documents/governance-os/evaluations/scripts/agent_certifier.py) | **Modified** | Updated the certifier registry for L4 readiness and target levels. |

---

## 2. Dynamic Claim Analysis Engine Implementation Details

*   **Claim Extraction Engine:** Isolates the proposal excerpt (excluding frontmatter) and splits the markdown text into sections by headers. Within sections, it splits paragraphs and list items dynamically to catalog every distinct capability claim without fixture-matching.
*   **Canonical Model Parser:** Automatically parses [`canonical-product-model.md`](file:///Users/ajayrajsingh/Documents/governance-os/knowledge/ethana/canonical-product-model.md) line by line to extract the authoritative status, permitted claim uses, and notes for all capabilities, certifications, and deployment models.
*   **Dynamic Claim Classification:** Evaluates claims against the canonical capabilities database and maps their properties to `SUPPORTED`, `ROADMAP`, `PROHIBITED`, or `UNSUPPORTED`.
*   **Dynamic Findings Engine:**
    *   **Critical Firewall Breach (CFB):** Flagged for `Aspirational` capabilities, `In Build` capabilities presented in current capability sections without disclaimers, uncertified standards (e.g., SOC 2 Type II claimed as held), and unverified customer references.
    *   **Major Risk Finding (MRF):** Triggered for In Build capabilities (e.g., SCIM Provisioning) listed in Roadmap sections without proper "not yet available" disclaimers.
    *   **Minor Finding:** Triggered for understated compliance framework scopes (e.g., EU AI Act Annex IV technical documentation scope).
*   **Dynamic Scoring Heuristics:**
    *   **Proposal Compliance Score (PCS):** Calculated dynamically using $\text{PCS} = \max(0, 100 - (5 \times \text{MRFs}) - (1 \times \text{Minors}))$. Overridden to `0` if any CFBs are present.
    *   **Claim Traceability Coverage Score (CTCS):** Evaluates whether capability claims trace back to approved platform specifications, calculated as:
        $$\text{CTCS} = \frac{\text{Traced Claims} + (0.5 \times \text{Partially Traced Claims})}{\text{Total Production-Claimed Claims}} \times 100$$
*   **Dynamic Release Classification:** Derived dynamically based on score thresholds (Approved $\ge 98$, Approved with Revisions $\ge 95$, Conditional Release $\ge 80$, Rejected otherwise).
