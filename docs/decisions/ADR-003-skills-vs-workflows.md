# Architecture Decision Record: ADR-003

## Title
ADR-003: Separation of Architectural Layers

---

## Status
**Accepted**

---

## Context
As the Governance OS expanded, it became clear that monolithic scripts or prompt definitions were difficult to manage, maintain, and test. In early designs, the reasoning logic (how to analyze an incident), the execution guidelines (who runs the steps), the scoring logic (rubrics), and the execution runtime (agent loops) were all combined in a single file. 

This monolithic structure created:
- Brittle tests: changing a formatting rule broke the analysis logic.
- Poor context management: models were forced to digest huge prompts containing scoring rubrics and execution guidelines alongside the actual task instructions.
- Infinite execution loops: circular dependencies between control mapping and technical fit checks had no clean breakout interface.

---

## Decision
Separate the Governance OS codebase into five distinct, decoupled architectural layers:

1.  **Knowledge Layer (`knowledge/`):** Contains static, retrieval-optimized files (regulations, framework definitions, controls library, and the canonical product model). It represents the baseline facts of the system and contains no reasoning prompts.
2.  **Skill Layer (`skills/`):** Represents parameterized, atomic tools. Each skill contains a spec (`SKILL.md`), a local guide (`workflow.md`), a local rubric (`evaluation.md`), and examples (`examples.md`). Skills do one thing precisely and are exposed as MCP tool definitions.
3.  **Workflow Layer (`workflows/`):** Coordinates and sequences multiple skills to execute complex business logic (e.g., incident triage, compliance scoping). It defines data routing (inputs/outputs) and human-in-the-loop checkpoints.
4.  **Evaluation Layer (`evaluations/`):** An independent test and validation suite containing python scripts, JSON payload schemas, and structural baselines. It validates outputs from the skill and workflow layers.
5.  **Agent Layer (`agents/`):** The execution runtime. It contains the code loops, memory modules, and tool registries for specialist agents and the coordinator router.

---

## Consequences
- **Positive:**
  - Ensures a clean separation of concerns: skills are reusable tools, workflows manage state, and evaluations verify quality.
  - Mitigates context window pollution by keeping evaluation rubrics out of active skill prompts.
  - Allows parallel development: engineers can work on the agent runtime while compliance analysts work on skills and regulations.
- **Negative:**
  - Increases the total file footprint and directory nesting of the repository.
  - Requires explicit JSON schema handoffs between layers to validate payloads.

---

## Alternatives Considered
- **Monolithic Skill Prompting:** Rejected. Bundling prompts, rubrics, and data paths together makes the prompts too large for LLM context budgets and prevents automation.
- **Flat Repository Structure:** Rejected. Organizing all assets in a single folder leads to folder clutter, index bloat, and confusion between commercial strategy and engineering compliance files.
