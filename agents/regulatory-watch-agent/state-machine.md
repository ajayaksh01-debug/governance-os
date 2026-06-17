# Regulatory Watch Agent — State Machine

**Version:** 1.0-spec  
**Implementation reference:** `agents/regulatory-watch-agent/orchestrator.py` (Level 4B)

Every state transition must be persisted to durable storage before the agent acts on it. Each persistence record must include: new state value, timestamp (ISO 8601), transition trigger, and identity of any human actor.

---

## 1. State Diagram

```
                          ┌──────────────────────────────────┐
                          │         INTAKE_VALIDATING         │
                          └────────────┬─────────────────────┘
                                       │
                  ┌────────────────────┼──────────────────────────┐
                  │                    │                          │
                  ▼                    ▼                          ▼
     HALTED_INTAKE_INVALID   HALTED_INTAKE_UNSUPPORTED   INTAKE_COMPLETE
                              _JURISDICTION
                                                               │
                                                               ▼
                                                      SKILL_1_RUNNING
                                                               │
                                              ┌────────────────┴──────────┐
                                              │                           │
                                              ▼                           ▼
                                     SKILL_1_COMPLETE          HALTED_ESCALATION
                                              │
                               ┌──────────────┴──────────────┐
                               │                             │
                               ▼                             ▼
                         GATE_1_PASSED          HALTED_GATE_1_SCHEMA
                               │
              ┌────────────────┴──────────────────────────┐
              │                │                          │
              ▼                ▼                          ▼
    GATE_2_PASSED   HALTED_GATE_2_PRELIMINARY   HALTED_GATE_2_INSUFFICIENT
              │
              ▼
    APPROVAL_1_PENDING
              │
      ┌───────┼────────────────────────┐
      │       │                        │
      ▼       ▼                        ▼
  APPROVAL  HALTED_APPROVAL_1_     APPROVAL_TIMED_OUT
  _1_APPROVED  REJECTED
      │
      ▼
SKILL_2_RUNNING
      │
  ┌───┴──────────────────────────────────────────────┐
  │                                                  │
  ▼                                                  ▼
SKILL_2_COMPLETE                          HALTED_ESCALATION
  │
  ├──────────────────────────────────────────────────┐
  │                         │                        │
  ▼                         ▼                        ▼
GATE_3_PASSED    HALTED_GATE_3A_SCHEMA    HALTED_FIREWALL_BREACH
  │
  ├──────────────────────────────────────────────────┐
  │                         │                        │
  ▼                         ▼                        ▼
GATE_4_PASSED   HALTED_GATE_4_BELOW_     HALTED_GATE_4_INSUFFICIENT
  │                    _THRESHOLD
  ▼
APPROVAL_2_PENDING
  │
  ├──────────────────────────────────────────────────┐
  │          │               │               │       │
  ▼          ▼               ▼               ▼       ▼
APPROVAL  HALTED_        HALTED_        APPROVAL_TIMED_OUT
_2_APPROVED APPROVAL_2_ APPROVAL_2_
           REJECTED      PARTIAL
  │
  ▼
COMPLETE
```

---

## 2. State Definitions

### Active States (Happy Path)

| State | Type | Description | Entered from | Exits to |
|---|---|---|---|---|
| `INTAKE_VALIDATING` | Transient | Parsing and validating the trigger payload; generating traceability ID | Run start | `INTAKE_COMPLETE` / `HALTED_INTAKE_INVALID` / `HALTED_INTAKE_UNSUPPORTED_JURISDICTION` |
| `INTAKE_COMPLETE` | Checkpoint | Payload valid; traceability ID assigned and persisted | `INTAKE_VALIDATING` | `SKILL_1_RUNNING` |
| `SKILL_1_RUNNING` | Active | regulatory-mapping skill executing | `INTAKE_COMPLETE` | `SKILL_1_COMPLETE` / `HALTED_ESCALATION` |
| `SKILL_1_COMPLETE` | Checkpoint | Skill 1 output ready; gates pending evaluation | `SKILL_1_RUNNING` | `GATE_1_PASSED` / `HALTED_GATE_1_SCHEMA` |
| `GATE_1_PASSED` | Checkpoint | RM schema valid (0 errors) | `SKILL_1_COMPLETE` | `GATE_2_PASSED` / `HALTED_GATE_2_PRELIMINARY` / `HALTED_GATE_2_INSUFFICIENT` |
| `GATE_2_PASSED` | Checkpoint | RM score ≥ 70/100 | `GATE_1_PASSED` | `APPROVAL_1_PENDING` |
| `APPROVAL_1_PENDING` | Waiting | Awaiting General Counsel sign-off; state persisted to durable store | `GATE_2_PASSED` | `APPROVAL_1_APPROVED` / `HALTED_APPROVAL_1_REJECTED` / `APPROVAL_TIMED_OUT` |
| `APPROVAL_1_APPROVED` | Checkpoint | General Counsel approved; inter-skill payload constructed | `APPROVAL_1_PENDING` | `SKILL_2_RUNNING` |
| `SKILL_2_RUNNING` | Active | governance-control-mapping skill executing | `APPROVAL_1_APPROVED` | `SKILL_2_COMPLETE` / `HALTED_ESCALATION` |
| `SKILL_2_COMPLETE` | Checkpoint | Skill 2 output ready; gates pending evaluation | `SKILL_2_RUNNING` | `GATE_3_PASSED` / `HALTED_GATE_3A_SCHEMA` / `HALTED_FIREWALL_BREACH` |
| `GATE_3_PASSED` | Checkpoint | GCM schema valid (0 errors) AND Claims Firewall clean (0 violations) | `SKILL_2_COMPLETE` | `GATE_4_PASSED` / `HALTED_GATE_4_BELOW_THRESHOLD` / `HALTED_GATE_4_INSUFFICIENT` |
| `GATE_4_PASSED` | Checkpoint | GCM score ≥ 85/100 | `GATE_3_PASSED` | `APPROVAL_2_PENDING` |
| `APPROVAL_2_PENDING` | Waiting | Awaiting DPO + InfoSec Lead joint sign-off; state persisted to durable store | `GATE_4_PASSED` | `APPROVAL_2_APPROVED` / `HALTED_APPROVAL_2_REJECTED` / `HALTED_APPROVAL_2_PARTIAL` / `APPROVAL_TIMED_OUT` |
| `APPROVAL_2_APPROVED` | Checkpoint | Both approvers signed off; assembling Compliance and Coverage Package | `APPROVAL_2_PENDING` | `COMPLETE` |
| `COMPLETE` | Terminal | Package delivered; assessment memory updated; handoff note generated | `APPROVAL_2_APPROVED` | — |

### Halted States

| State | Type | Description | Recovery path |
|---|---|---|---|
| `HALTED_INTAKE_INVALID` | Terminal (resolvable) | Required field missing, empty, or failed validation | Operator corrects inputs; new run submitted |
| `HALTED_INTAKE_UNSUPPORTED_JURISDICTION` | Terminal | Trigger payload specifies jurisdiction outside EU / UK / India | Escalation to Compliance Analyst; no extrapolation |
| `HALTED_GATE_1_SCHEMA` | Terminal (resolvable) | Skill 1 JSON output fails schema validation after one retry | Escalate to Compliance Analyst; revised run initiated |
| `HALTED_GATE_2_PRELIMINARY` | Terminal (resolvable) | Skill 1 score 55–69; output reclassified as Preliminary | Revision request with failing dimensions; operator reviews; new run |
| `HALTED_GATE_2_INSUFFICIENT` | Terminal | Skill 1 score < 55 | Escalate to Compliance Analyst; do not auto-retry |
| `HALTED_APPROVAL_1_REJECTED` | Terminal (resolvable) | General Counsel rejected Regulatory Scoping Matrix | Return to Skill 1 with reviewer notes; operator initiates revised run |
| `HALTED_GATE_3A_SCHEMA` | Terminal (resolvable) | Skill 2 JSON output fails schema validation after one retry | Escalate to Compliance Analyst; revised run initiated |
| `HALTED_FIREWALL_BREACH` | Terminal | Claims Firewall violation in GCM output | Auto-route to Compliance Director; Compliance Director sign-off required before any new run |
| `HALTED_GATE_4_BELOW_THRESHOLD` | Terminal (resolvable) | Skill 2 score 70–84 | Revision request with failing sections; operator reviews; new run |
| `HALTED_GATE_4_INSUFFICIENT` | Terminal | Skill 2 score < 70 | Escalate to Compliance Analyst; do not auto-retry |
| `HALTED_APPROVAL_2_PARTIAL` | Terminal (resolvable) | One approver approved, one rejected at Gate 2 | Conflict resolution meeting: both approvers + Compliance Analyst; outcome in run log; new run |
| `HALTED_APPROVAL_2_REJECTED` | Terminal (resolvable) | Both (or remaining) approver(s) rejected at Gate 2 | Return to Skill 2 with reviewer notes; operator initiates revised run |
| `HALTED_ESCALATION` | Terminal (resolvable) | Skill execution failed with unresolvable error | External resolution required; operator initiates revised run |
| `APPROVAL_TIMED_OUT` | Waiting | Approval gate not actioned within 5 business days | Compliance Analyst notified; agent waits; no auto-approval |

---

## 3. Valid Transitions

Every transition must be an explicit recorded operation. No implicit or assumed transitions.

```
INTAKE_VALIDATING
  → INTAKE_COMPLETE                       (validation passed; traceability ID assigned)
  → HALTED_INTAKE_INVALID                 (required field missing, unsupported value, or V-04 failure)
  → HALTED_INTAKE_UNSUPPORTED_JURISDICTION (jurisdiction not in [EU, UK, India])

INTAKE_COMPLETE
  → SKILL_1_RUNNING                       (automatic; no condition)

SKILL_1_RUNNING
  → SKILL_1_COMPLETE                      (skill execution returned output)
  → HALTED_ESCALATION                     (skill execution failed with unresolvable error)

SKILL_1_COMPLETE
  → GATE_1_PASSED                         (schema validation: 0 errors)
  → HALTED_GATE_1_SCHEMA                  (schema invalid after retry)
    Note: first schema failure triggers one automatic retry with augmented prompt;
          second failure → HALTED_GATE_1_SCHEMA

GATE_1_PASSED
  → GATE_2_PASSED                         (score ≥ 70)
  → HALTED_GATE_2_PRELIMINARY             (score 55–69)
  → HALTED_GATE_2_INSUFFICIENT            (score < 55)

GATE_2_PASSED
  → APPROVAL_1_PENDING                    (automatic; no condition)

APPROVAL_1_PENDING
  → APPROVAL_1_APPROVED                   (General Counsel: Approve or Approve with notes)
  → HALTED_APPROVAL_1_REJECTED            (General Counsel: Reject with revision request)
  → APPROVAL_TIMED_OUT                    (5 business days elapsed without action)

APPROVAL_1_APPROVED
  → SKILL_2_RUNNING                       (automatic; inter-skill payload constructed)

SKILL_2_RUNNING
  → SKILL_2_COMPLETE                      (skill execution returned output)
  → HALTED_ESCALATION                     (skill execution failed with unresolvable error)

SKILL_2_COMPLETE
  → GATE_3_PASSED                         (schema valid AND Claims Firewall: 0 violations)
    Note: Gate 3a (schema) and Gate 3b (Claims Firewall) run concurrently.
          GATE_3_PASSED requires BOTH to pass.
  → HALTED_GATE_3A_SCHEMA                 (schema invalid after retry; regardless of firewall result)
  → HALTED_FIREWALL_BREACH                (Claims Firewall: ≥ 1 violation; regardless of schema result)
    Priority: HALTED_FIREWALL_BREACH takes precedence over HALTED_GATE_3A_SCHEMA if both fail

GATE_3_PASSED
  → GATE_4_PASSED                         (score ≥ 85)
  → HALTED_GATE_4_BELOW_THRESHOLD         (score 70–84)
  → HALTED_GATE_4_INSUFFICIENT            (score < 70)

GATE_4_PASSED
  → APPROVAL_2_PENDING                    (automatic; no condition)

APPROVAL_2_PENDING
  → APPROVAL_2_APPROVED                   (both DPO and InfoSec Lead: Approve)
  → APPROVAL_2_APPROVED                   (both DPO and InfoSec Lead: Approve with modifications — after re-gate)
  → HALTED_APPROVAL_2_REJECTED            (either or both approvers: Reject)
  → HALTED_APPROVAL_2_PARTIAL             (exactly one approver approved, one rejected)
  → APPROVAL_TIMED_OUT                    (5 business days elapsed without both actions)

APPROVAL_2_APPROVED
  → COMPLETE                              (package assembled, delivered, assessment memory updated)
```

---

## 4. Transition Persistence Contract

Each transition record must persist:

| Field | Type | Description |
|---|---|---|
| `traceability_id` | string | Run identifier |
| `from_state` | enum | Previous state |
| `to_state` | enum | New state |
| `timestamp` | ISO 8601 | UTC timestamp of transition |
| `trigger` | string | What caused the transition (gate result, approval action, error message, timeout) |
| `actor_identity` | string or null | Identity of human actor if transition was caused by an approval action; null for automated transitions |
| `notes` | string or null | Approver notes if `Approve with notes`; revision request text if rejected; null otherwise |

The run log in the final package is constructed from all transition records for the run.

---

## 5. Gate 3 Concurrent Evaluation

Gate 3a (schema validation) and Gate 3b (Claims Firewall) are evaluated concurrently after `SKILL_2_COMPLETE`. The combined result determines the transition from `SKILL_2_COMPLETE`:

| Gate 3a result | Gate 3b result | Transition |
|---|---|---|
| Pass | Pass | → `GATE_3_PASSED` |
| Pass | Fail (breach) | → `HALTED_FIREWALL_BREACH` |
| Fail | Pass | → `HALTED_GATE_3A_SCHEMA` |
| Fail | Fail | → `HALTED_FIREWALL_BREACH` (firewall breach takes precedence; both are recorded) |

The Claims Firewall breach state takes precedence because it requires escalation to the Compliance Director and different recovery requirements from a schema failure.

---

## 6. Approval Modification Re-Gate

When the DPO or InfoSec Lead selects "Approve with modifications" at Approval Gate 2:

1. Agent incorporates the modifications (RACI role changes or control caveats)
2. Agent re-runs Gate 3a, Gate 3b, and Gate 4 on the modified output
3. If all three re-gates pass → transition to `APPROVAL_2_APPROVED` → `COMPLETE`
4. If any re-gate fails → the appropriate halted state is entered (the modification introduced a problem)

The transition path is: `APPROVAL_2_PENDING` → *(modification)* → `GATE_3_PASSED` → `GATE_4_PASSED` → `APPROVAL_2_APPROVED` → `COMPLETE`.

The re-gate results are recorded in the run log. The modification content is recorded in the approval decision record.

---

## 7. Timeout Handling

`APPROVAL_TIMED_OUT` is not a terminal state — it is a waiting state. The agent remains in this state until a human action occurs:

| Human action | Transition from `APPROVAL_TIMED_OUT` |
|---|---|
| Compliance Analyst extends deadline | → Return to `APPROVAL_1_PENDING` or `APPROVAL_2_PENDING` (same gate) |
| Compliance Analyst initiates revised run | → New run; current run remains in `APPROVAL_TIMED_OUT` |
| Approver acts after timeout | → Approval action is accepted; transition proceeds normally |

The agent must not auto-approve, auto-escalate, or auto-reject on timeout.

---

## 8. Partial Output Release

The Skill 1 Regulatory Scoping Matrix may be released as a standalone document if:

1. The run has passed `APPROVAL_1_APPROVED` (General Counsel has signed off), AND
2. The run subsequently halted in any post-Gate-1 halted state

**Release protocol:**
- An operator explicitly requests partial release
- The agent packages `{traceability_id}-regulatory-scoping-matrix.md` and `{traceability_id}-regulatory-mapping-payload.json` with a cover note that the Operational Control Specification was not completed
- The run state remains in its halted state; it is not moved to `COMPLETE`
- The partial release is recorded in the run log

The agent must not automatically release any partial output.

---

## 9. State Persistence Requirements

States that must be persisted to durable storage (not in-process memory):

| State | Reason |
|---|---|
| `APPROVAL_1_PENDING` | May wait multiple business days; process restart must not lose state |
| `APPROVAL_2_PENDING` | Same |
| `APPROVAL_TIMED_OUT` | Long-running; requires human action to resolve |
| All `HALTED_*` states | Require operator action; must survive restart |
| `SKILL_1_COMPLETE` | Skill 1 output stored for inter-skill payload and approval delivery |
| `SKILL_2_COMPLETE` | Skill 2 output stored for gate evaluation and approval delivery |
| `COMPLETE` | Final state; run log must be durable |

States `SKILL_1_RUNNING` and `SKILL_2_RUNNING` are transient active states. If the process restarts during execution, the run resumes from the last persisted checkpoint state.

---

## 10. Forbidden Transitions

The following transitions are explicitly forbidden. An implementation that attempts these must raise an error:

| Forbidden transition | Reason |
|---|---|
| `APPROVAL_1_PENDING` → `SKILL_2_RUNNING` (without approval action) | Approval cannot be bypassed |
| `APPROVAL_2_PENDING` → `COMPLETE` (without approval action) | Approval cannot be bypassed |
| `GATE_1_PASSED` → `SKILL_2_RUNNING` (skipping Gate 2 or Approval Gate 1) | All gates and approvals are mandatory |
| `GATE_3_PASSED` → `APPROVAL_2_PENDING` (skipping Gate 4) | All gates are mandatory |
| `HALTED_FIREWALL_BREACH` → any active state | Claims Firewall breach cannot be cleared by the agent; requires Compliance Director sign-off and a new run |
| `SKILL_1_RUNNING` → `SKILL_2_RUNNING` (skipping all gates and Approval Gate 1) | Strict sequential execution required |
| Any `COMPLETE` → any other state | Terminal state; any revision requires a new run with a new traceability ID |
