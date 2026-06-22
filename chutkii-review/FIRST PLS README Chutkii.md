# Engineering Review — Governance OS

## What is this repo?

A **multi-step pipeline executor** with human-in-the-loop approval gates.

In plain engineering terms: you submit a job, it runs a sequence of 6 processing steps ("skills") one by one, pauses at 4 human approval checkpoints, and produces a package of output files when complete. Each step calls into one of 5 specialised sub-agents. The whole thing is coordinated by a state machine.

No web frontend. No database. No API yet. This is currently a Python library you call directly.

---

## What I'm asking you to review

Pure software engineering perspective only — please ignore the domain logic entirely.

Specifically:

- How does the overall architecture look?
- Are any components too tightly coupled?
- What scalability challenges do you foresee?
- How maintainable is the codebase?
- If this needed to support 100 enterprise customers, what would break first?
- Do you see any major engineering red flags?

Focus areas: architecture, scalability, reliability, maintainability, testing, deployment readiness, operational concerns.

---

## How to navigate this folder

| File | What it is |
|---|---|
| `repo-tree.txt` | Full directory tree of the repo |
| `architecture.md` | How the system works — components, data flow, coupling points |
| `key-files.md` | Map of the most important files to read, with one-line descriptions |

---

## Tech stack

- Python (3.14 from `__pycache__` filenames)
- `PyYAML` for config
- `pytest` for tests
- JSON files for state persistence
- JSONL files for audit logs
- Markdown files as runtime knowledge sources (parsed with regex)
- No web framework, no database, no queue, no deployment infrastructure
