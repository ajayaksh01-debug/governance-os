# Key Files to Read

Start here if you want to look at actual code. Listed in order of importance for an engineering review.

---

## Core Runtime (read these first)

| File | LOC | What it does |
|---|---|---|
| `agents/client-assessment-agent/runtime/orchestrator.py` | 835 | Main entry point. Runs the 6-step pipeline. Owns all gate logic, approval routing, firewall checks. Single class. |
| `agents/client-assessment-agent/runtime/state_manager.py` | 399 | State machine definition + JSON file persistence. Every state transition reads then writes a file. No locking. |
| `agents/client-assessment-agent/runtime/skill_adapters.py` | 574 | Adapter layer between orchestrator and sub-agents. Dynamic imports via `importlib.util.spec_from_file_location`. |
| `agents/client-assessment-agent/runtime/skill_executor.py` | 61 | Thin dispatcher. Delegates to adapter registry. ID generation via `random.randint(1, 9999)`. |
| `agents/client-assessment-agent/runtime/audit_logger.py` | 49 | Append-only JSONL logger. Also prints to stdout. Swallows write errors silently. |
| `agents/client-assessment-agent/runtime/output_builder.py` | 151 | Assembles final output package. Writes 14 files to `packages/{run_id}/`. |
| `agents/client-assessment-agent/runtime/config.yaml` | 53 | Score thresholds, directory paths, approval gate roles. Loaded once at startup. |

---

## Sub-Agent Executors (called by CA via file-path imports)

| File | LOC | What it does |
|---|---|---|
| `agents/capability_validation_agent/runtime/skill_executor.py` | 565 | Step 5 logic. Parses `canonical-product-model.md` from disk on every call using regex. Scores capabilities. |
| `agents/ethana_proposal_agent/runtime/skill_executor.py` | 641 | Step 6 logic. Receives CA's `state_mgr` object and writes to it directly (cross-agent state mutation). |
| `agents/regulatory-watch-agent/runtime/skill_executor.py` | 626 | Steps 1 & 2 logic. Also imports `claims_linter.py` from `evaluations/scripts/` at runtime. |

---

## CA-Local Skill Executors (steps 3, 4, FM)

| File | LOC | What it does |
|---|---|---|
| `agents/client-assessment-agent/runtime/skills/solution_mapping_executor.py` | 337 | Step 3 logic. Imports `claims_linter.py` from `evaluations/scripts/` to parse a markdown knowledge file. |
| `agents/client-assessment-agent/runtime/skills/iso42001_executor.py` | — | Step 4 logic. |
| `agents/client-assessment-agent/runtime/skills/feature_mapping_executor.py` | — | Step FM logic. |

---

## Schemas and Contracts

| File | What it is |
|---|---|
| `workflows/schemas/*.json` | JSON Schema files for each step's output. Validated at runtime. |
| `agents/*/runtime/contracts/*.json` | Per-agent output contracts (subset of schemas). |

---

## Tests

| File | Tests | Notes |
|---|---|---|
| `evaluations/scripts/test_client_assessment_runtime.py` | 88 | Main CA pipeline tests. 84 of 88 use lambda fixture overrides — real adapters not invoked. |
| `evaluations/scripts/test_client_assessment_adapters.py` | — | Adapter unit tests |
| `evaluations/scripts/test_client_assessment_skill3.py` | 18 | Skill 3 unit tests, including PR-010 direct CPM path |
| `evaluations/scripts/test_regulatory_watch_runtime.py` | 34 | RWA isolated tests. All pass. |
| `evaluations/scripts/conftest.py` | — | 6 lines: just `sys.path` setup |
| `evaluations/scripts/claims_linter.py` | — | Parses markdown knowledge files. Used by production code AND tests. Lives in the test folder. |

---

## Knowledge Files (used by production code at runtime)

| File | Format | Used by |
|---|---|---|
| `knowledge/ethana/canonical-product-model.md` | Markdown table | CVA executor — parsed with regex on every call |
| `knowledge/ethana/control-capability-map.md` | Markdown table | RWA executor + CA Skill 3 — loaded once per process |

---

## Things That Don't Exist

| What's missing | Where you'd expect it |
|---|---|
| `requirements.txt` / `pyproject.toml` | repo root |
| `Dockerfile` | repo root |
| CI/CD config (`.github/workflows/`) | `.github/` |
| Any HTTP server / API layer | anywhere |
| Database models | anywhere |
| Auth/authz | anywhere |
| Run cleanup / TTL job | anywhere |
| `scorecard_compiler.py` wiring | `output_builder.py` (it exists in `evaluations/scripts/` but is not called from the runtime) |

---

## Duplication Map

These four files are **copy-pasted across all 5 agents** with minor variations:

```
agents/*/runtime/state_manager.py     — 5 copies
agents/*/runtime/audit_logger.py      — 5 copies
agents/*/runtime/schema_validator.py  — 5 copies
agents/*/runtime/output_builder.py    — 5 copies
```

No shared library. Each agent evolved independently.
