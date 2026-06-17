# Client Assessment Agent — State Machine

**Version:** 1.0-spec  
**Total states:** 32 active + 31 halted = 63 states  
**Approval gates:** 4 (AG-1 through AG-4)  
**Claims Firewall enforced in:** Gate 2c, Gate 3b, Gate 4b, Gate 5b, Gate 6b  
**Terminal states (success):** `COMPLETE`  
**Terminal states (failure):** all `HALTED_*` states that have no auto-recovery

---

## State Diagram

```
                        ┌──────────────────────┐
        [Trigger] ───►  │  INTAKE_VALIDATING   │
                        └──────────┬───────────┘
                                   │ valid
                        ┌──────────▼───────────┐
                        │   INTAKE_COMPLETE    │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_1_RUNNING     │  (regulatory-mapping)
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_1_COMPLETE    │
                        └──────────┬───────────┘
                    Gate 1a ───────┤
                    (schema)       │ pass
                        ┌──────────▼───────────┐
                        │   GATE_1_PASSED      │  (schema ✓ + score ✓)
                        └──────────┬───────────┘
                    Gate 2a ───────┘ (score ≥70)
                        ┌──────────▼───────────┐
                        │ APPROVAL_1_PENDING   │  (General Counsel)
                        └──────────┬───────────┘
                                   │ approved
                        ┌──────────▼───────────┐
                        │ APPROVAL_1_APPROVED  │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_2_RUNNING     │  (governance-control-mapping)
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_2_COMPLETE    │
                        └──────────┬───────────┘
              Gates 2b,2c,2d ──────┤
              (schema, CFW, score) │ all pass
                        ┌──────────▼───────────┐
                        │   GATE_2_PASSED      │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_3_RUNNING     │  (ethana-solution-mapping)
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_3_COMPLETE    │
                        └──────────┬───────────┘
              Gates 3a,3b,3c ──────┤
              (schema, CFW, score) │ all pass
                        ┌──────────▼───────────┐
                        │   GATE_3_PASSED      │
                        └──────────┬───────────┘
                        ┌──────────▼───────────┐
                        │ APPROVAL_2_PENDING   │  (DPO + CISO joint)
                        └──────────┬───────────┘
                                   │ both approved
                        ┌──────────▼───────────┐
                        │ APPROVAL_2_APPROVED  │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_4_RUNNING     │  (iso-42001-gap-assessment)
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_4_COMPLETE    │
                        └──────────┬───────────┘
              Gates 4a,4b,4c ──────┤
              (schema, CFW, score) │ all pass
                        ┌──────────▼───────────┐
                        │   GATE_4_PASSED      │
                        └──────────┬───────────┘
                        ┌──────────▼───────────┐
                        │ APPROVAL_3_PENDING   │  (Client Risk Committee Lead)
                        └──────────┬───────────┘
                                   │ approved
                        ┌──────────▼───────────┐
                        │ APPROVAL_3_APPROVED  │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_5_RUNNING     │  (ethana-capability-validation)
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_5_COMPLETE    │
                        └──────────┬───────────┘
              Gates 5a,5b,5c ──────┤
              (schema, CFW, score) │ all pass
                        ┌──────────▼───────────┐
                        │   GATE_5_PASSED      │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_6_RUNNING     │  (ethana-proposal-review)
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  SKILL_6_COMPLETE    │
                        └──────────┬───────────┘
              Gates 6a,6b,6c ──────┤
              (schema, CFW, class) │ all pass
                        ┌──────────▼───────────┐
                        │   GATE_6_PASSED      │
                        └──────────┬───────────┘
                        ┌──────────▼───────────┐
                        │ APPROVAL_4_PENDING   │  (Compliance Dir + Sales Dir)
                        └──────────┬───────────┘
                                   │ both approved
                        ┌──────────▼───────────┐
                        │ APPROVAL_4_APPROVED  │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  ASSEMBLING_PACKAGE  │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │      COMPLETE        │
                        └──────────────────────┘
```

---

## State Definitions

### Active States

| State | Entered from | Exits to |
|---|---|---|
| `INTAKE_VALIDATING` | Trigger event received | `INTAKE_COMPLETE` (all validation rules pass) |
| `INTAKE_COMPLETE` | `INTAKE_VALIDATING` | `SKILL_1_RUNNING` |
| `SKILL_1_RUNNING` | `INTAKE_COMPLETE` | `SKILL_1_COMPLETE` |
| `SKILL_1_COMPLETE` | `SKILL_1_RUNNING` | `GATE_1_PASSED` (via Gates 1a, 2a) |
| `GATE_1_PASSED` | `SKILL_1_COMPLETE` (Gates 1a + 2a pass) | `APPROVAL_1_PENDING` |
| `APPROVAL_1_PENDING` | `GATE_1_PASSED` | `APPROVAL_1_APPROVED` (approve) |
| `APPROVAL_1_APPROVED` | `APPROVAL_1_PENDING` | `SKILL_2_RUNNING` |
| `SKILL_2_RUNNING` | `APPROVAL_1_APPROVED` | `SKILL_2_COMPLETE` |
| `SKILL_2_COMPLETE` | `SKILL_2_RUNNING` | `GATE_2_PASSED` (via Gates 2b, 2c, 2d) |
| `GATE_2_PASSED` | `SKILL_2_COMPLETE` (Gates 2b+2c+2d pass) | `SKILL_3_RUNNING` |
| `SKILL_3_RUNNING` | `GATE_2_PASSED` | `SKILL_3_COMPLETE` |
| `SKILL_3_COMPLETE` | `SKILL_3_RUNNING` | `GATE_3_PASSED` (via Gates 3a, 3b, 3c) |
| `GATE_3_PASSED` | `SKILL_3_COMPLETE` (Gates 3a+3b+3c pass) | `APPROVAL_2_PENDING` |
| `APPROVAL_2_PENDING` | `GATE_3_PASSED` | `APPROVAL_2_APPROVED` (both approve) |
| `APPROVAL_2_APPROVED` | `APPROVAL_2_PENDING` | `SKILL_4_RUNNING` |
| `SKILL_4_RUNNING` | `APPROVAL_2_APPROVED` | `SKILL_4_COMPLETE` |
| `SKILL_4_COMPLETE` | `SKILL_4_RUNNING` | `GATE_4_PASSED` (via Gates 4a, 4b, 4c) |
| `GATE_4_PASSED` | `SKILL_4_COMPLETE` (Gates 4a+4b+4c pass) | `APPROVAL_3_PENDING` |
| `APPROVAL_3_PENDING` | `GATE_4_PASSED` | `APPROVAL_3_APPROVED` (approved) |
| `APPROVAL_3_APPROVED` | `APPROVAL_3_PENDING` | `SKILL_5_RUNNING` |
| `SKILL_5_RUNNING` | `APPROVAL_3_APPROVED` | `SKILL_5_COMPLETE` |
| `SKILL_5_COMPLETE` | `SKILL_5_RUNNING` | `GATE_5_PASSED` (via Gates 5a, 5b, 5c) |
| `GATE_5_PASSED` | `SKILL_5_COMPLETE` (Gates 5a+5b+5c pass) | `SKILL_6_RUNNING` |
| `SKILL_6_RUNNING` | `GATE_5_PASSED` | `SKILL_6_COMPLETE` |
| `SKILL_6_COMPLETE` | `SKILL_6_RUNNING` | `GATE_6_PASSED` (via Gates 6a, 6b, 6c) |
| `GATE_6_PASSED` | `SKILL_6_COMPLETE` (Gates 6a+6b+6c pass, PCS ≥ 80) | `APPROVAL_4_PENDING` |
| `APPROVAL_4_PENDING` | `GATE_6_PASSED` or `HALTED_PROPOSAL_CONDITIONAL` (Compliance Dir decision) | `APPROVAL_4_APPROVED` |
| `APPROVAL_4_APPROVED` | `APPROVAL_4_PENDING` | `ASSEMBLING_PACKAGE` |
| `ASSEMBLING_PACKAGE` | `APPROVAL_4_APPROVED` | `COMPLETE` |
| `COMPLETE` | `ASSEMBLING_PACKAGE` | Terminal — package delivered; Client Memory updated |
| `APPROVAL_TIMED_OUT` | Any `APPROVAL_N_PENDING` state | Same `APPROVAL_N_PENDING` (waiting) or `HALTED_ESCALATION` |

### Halted States

#### Intake

| State | Entered from | Recovery |
|---|---|---|
| `HALTED_INTAKE_INVALID` | `INTAKE_VALIDATING` (required field missing or V-05/V-06 fail) | Operator corrects inputs; new run |
| `HALTED_INTAKE_UNSUPPORTED_JURISDICTION` | `INTAKE_VALIDATING` (unsupported jurisdiction value) | Escalate to Compliance Analyst; new run with supported jurisdiction |

#### Skill 1 (regulatory-mapping)

| State | Entered from | Recovery |
|---|---|---|
| `HALTED_GATE_1_SCHEMA` | `SKILL_1_COMPLETE` (schema fails after 1 retry) | Escalate to Compliance Analyst |
| `HALTED_GATE_1_SCORE_PRELIMINARY` | `SKILL_1_COMPLETE` (score 55–69) | Revision request with failing dimension breakdown; new run |
| `HALTED_GATE_1_SCORE_INSUFFICIENT` | `SKILL_1_COMPLETE` (score < 55) | Escalate to Compliance Analyst; do not auto-retry |
| `HALTED_APPROVAL_1_REJECTED` | `APPROVAL_1_PENDING` (General Counsel rejects) | Operator initiates revised run with revised inputs |

#### Skill 2 (governance-control-mapping)

| State | Entered from | Recovery |
|---|---|---|
| `HALTED_GATE_2_SCHEMA` | `SKILL_2_COMPLETE` (schema fails after 1 retry) | Escalate to Compliance Analyst |
| `HALTED_FIREWALL_BREACH_GCM` | `SKILL_2_COMPLETE` (Gate 2c: any violation in Section 10) | Auto-route to Compliance Director; no auto-retry; new run |
| `HALTED_GATE_2_SCORE_BELOW_THRESHOLD` | `SKILL_2_COMPLETE` (score 70–84) | Revision request with per-section breakdown; new run |
| `HALTED_GATE_2_SCORE_INSUFFICIENT` | `SKILL_2_COMPLETE` (score < 70) | Escalate to Compliance Analyst |

#### Skill 3 (ethana-solution-mapping)

| State | Entered from | Recovery |
|---|---|---|
| `HALTED_GATE_3_SCHEMA` | `SKILL_3_COMPLETE` (schema fails after 1 retry) | Escalate to Compliance Analyst |
| `HALTED_FIREWALL_BREACH_SOLUTION` | `SKILL_3_COMPLETE` (Gate 3b: any violation) | Auto-route to Compliance Director; no auto-retry; new run |
| `HALTED_GATE_3_SCORE_INSUFFICIENT` | `SKILL_3_COMPLETE` (score < 70) | Escalate to Compliance Analyst |
| `HALTED_APPROVAL_2_PARTIAL` | `APPROVAL_2_PENDING` (DPO approves, CISO rejects or vice versa) | Conflict resolution meeting; new run |
| `HALTED_APPROVAL_2_REJECTED` | `APPROVAL_2_PENDING` (both DPO and CISO reject) | Operator initiates revised run |

#### Skill 4 (iso-42001-gap-assessment)

| State | Entered from | Recovery |
|---|---|---|
| `HALTED_GATE_4_SCHEMA` | `SKILL_4_COMPLETE` (schema fails after 1 retry) | Escalate to Compliance Analyst |
| `HALTED_FIREWALL_BREACH_ISO` | `SKILL_4_COMPLETE` (Gate 4b: any violation in Section 8) | Auto-route to Compliance Director; no auto-retry; new run |
| `HALTED_GATE_4_SCORE_BELOW_THRESHOLD` | `SKILL_4_COMPLETE` (AMS or ARS score 70–84) | Revision request with per-clause breakdown; new run |
| `HALTED_GATE_4_SCORE_INSUFFICIENT` | `SKILL_4_COMPLETE` (AMS or ARS score < 70) | Escalate to Compliance Analyst |
| `HALTED_APPROVAL_3_REJECTED` | `APPROVAL_3_PENDING` (Client Risk Committee Lead rejects) | Operator initiates revised run |
| `HALTED_APPROVAL_3_PARTIAL` | `APPROVAL_3_PENDING` (joint approver conflict) | Conflict resolution meeting; new run |

#### Skill 5 (ethana-capability-validation)

| State | Entered from | Recovery |
|---|---|---|
| `HALTED_GATE_5_SCHEMA` | `SKILL_5_COMPLETE` (any per-capability schema fails after 1 retry) | Escalate to Compliance Analyst |
| `HALTED_FIREWALL_BREACH_CAPVAL` | `SKILL_5_COMPLETE` (Gate 5b: any violation in validation report) | Auto-route to Compliance Director; no auto-retry; new run |
| `HALTED_GATE_5_SCORE_INSUFFICIENT` | `SKILL_5_COMPLETE` (ECS < 90 or escalation_required == true) | Escalate to Compliance Director + Product team; no auto-retry |

#### Skill 6 (ethana-proposal-review)

| State | Entered from | Recovery |
|---|---|---|
| `HALTED_GATE_6_SCHEMA` | `SKILL_6_COMPLETE` (schema fails after 1 retry) | Escalate to Compliance Analyst |
| `HALTED_FIREWALL_BREACH_TERMINAL` | `SKILL_6_COMPLETE` (Gate 6b: any violation — HARDEST FAIL) | Auto-route to Compliance Director + Sales Director; new run only after CD sign-off |
| `HALTED_PROPOSAL_REJECTED` | `SKILL_6_COMPLETE` (PCS < 80 or CTCS < 80 → Rejected) | Escalate to Compliance Director + Sales Director; revised run required |
| `HALTED_PROPOSAL_CONDITIONAL` | `SKILL_6_COMPLETE` (PCS 80–94 or CTCS 80–94 → Conditional) | Present to AG-4; Compliance Director reviews conditional items; may recover to `APPROVAL_4_PENDING` |
| `HALTED_APPROVAL_4_REJECTED` | `APPROVAL_4_PENDING` (both Compliance Dir + Sales Dir reject) | Operator initiates revised run |
| `HALTED_APPROVAL_4_PARTIAL` | `APPROVAL_4_PENDING` (one approves, one rejects) | Conflict resolution; executive sign-off required |

#### Cross-Cutting

| State | Entered from | Recovery |
|---|---|---|
| `APPROVAL_TIMED_OUT` | Any `APPROVAL_N_PENDING` state (timeout exceeded) | Compliance Analyst extends deadline or initiates revised run; state returns to pending |
| `HALTED_ESCALATION` | Any state (unresolvable execution error, or no capabilities found in Skill 5 extraction) | External resolution required |

---

## Transition Table

### Happy Path Transitions

| From | Event | To |
|---|---|---|
| _(system)_ | Trigger event received with all required fields | `INTAKE_VALIDATING` |
| `INTAKE_VALIDATING` | All V-01 through V-06 pass | `INTAKE_COMPLETE` |
| `INTAKE_COMPLETE` | Agent initialised | `SKILL_1_RUNNING` |
| `SKILL_1_RUNNING` | regulatory-mapping execution completes | `SKILL_1_COMPLETE` |
| `SKILL_1_COMPLETE` | Gate 1a schema passes + Gate 2a score ≥ 70 | `GATE_1_PASSED` |
| `GATE_1_PASSED` | AG-1 notification sent | `APPROVAL_1_PENDING` |
| `APPROVAL_1_PENDING` | General Counsel clicks Approve (or Approve with notes) | `APPROVAL_1_APPROVED` |
| `APPROVAL_1_APPROVED` | Agent proceeds | `SKILL_2_RUNNING` |
| `SKILL_2_RUNNING` | governance-control-mapping execution completes | `SKILL_2_COMPLETE` |
| `SKILL_2_COMPLETE` | Gate 2b schema passes + Gate 2c CFW passes + Gate 2d score ≥ 85 | `GATE_2_PASSED` |
| `GATE_2_PASSED` | Agent proceeds | `SKILL_3_RUNNING` |
| `SKILL_3_RUNNING` | ethana-solution-mapping execution completes | `SKILL_3_COMPLETE` |
| `SKILL_3_COMPLETE` | Gate 3a schema passes + Gate 3b CFW passes + Gate 3c score ≥ 70 | `GATE_3_PASSED` |
| `GATE_3_PASSED` | AG-2 notification sent | `APPROVAL_2_PENDING` |
| `APPROVAL_2_PENDING` | Both DPO and CISO approve | `APPROVAL_2_APPROVED` |
| `APPROVAL_2_APPROVED` | Agent proceeds | `SKILL_4_RUNNING` |
| `SKILL_4_RUNNING` | iso-42001-gap-assessment execution completes | `SKILL_4_COMPLETE` |
| `SKILL_4_COMPLETE` | Gate 4a schema passes + Gate 4b CFW passes + Gate 4c score ≥ 85 | `GATE_4_PASSED` |
| `GATE_4_PASSED` | AG-3 notification sent | `APPROVAL_3_PENDING` |
| `APPROVAL_3_PENDING` | Client Risk Committee Lead approves | `APPROVAL_3_APPROVED` |
| `APPROVAL_3_APPROVED` | Agent proceeds | `SKILL_5_RUNNING` |
| `SKILL_5_RUNNING` | All capability validations complete | `SKILL_5_COMPLETE` |
| `SKILL_5_COMPLETE` | Gate 5a schema passes + Gate 5b CFW passes + Gate 5c ECS ≥ 90 | `GATE_5_PASSED` |
| `GATE_5_PASSED` | Agent proceeds | `SKILL_6_RUNNING` |
| `SKILL_6_RUNNING` | ethana-proposal-review execution completes | `SKILL_6_COMPLETE` |
| `SKILL_6_COMPLETE` | Gate 6a schema passes + Gate 6b CFW passes + Gate 6c PCS ≥ 80 (Approved or Conditional) | `GATE_6_PASSED` |
| `GATE_6_PASSED` | AG-4 notification sent | `APPROVAL_4_PENDING` |
| `APPROVAL_4_PENDING` | Both Compliance Director and Sales Director approve | `APPROVAL_4_APPROVED` |
| `APPROVAL_4_APPROVED` | Agent assembles package | `ASSEMBLING_PACKAGE` |
| `ASSEMBLING_PACKAGE` | All artifacts compiled; scorecard_compiler.py completes | `COMPLETE` |

### Failure Transitions

#### Intake Failures

| From | Event | To |
|---|---|---|
| `INTAKE_VALIDATING` | Required field missing or V-05/V-06 fail | `HALTED_INTAKE_INVALID` |
| `INTAKE_VALIDATING` | Unsupported jurisdiction value in array | `HALTED_INTAKE_UNSUPPORTED_JURISDICTION` |

#### Skill 1 Failures

| From | Event | To |
|---|---|---|
| `SKILL_1_COMPLETE` | Gate 1a schema fails → 1 retry → still fails | `HALTED_GATE_1_SCHEMA` |
| `SKILL_1_COMPLETE` | Gate 2a score 55–69 (preliminary band) | `HALTED_GATE_1_SCORE_PRELIMINARY` |
| `SKILL_1_COMPLETE` | Gate 2a score < 55 (insufficient band) | `HALTED_GATE_1_SCORE_INSUFFICIENT` |
| `APPROVAL_1_PENDING` | General Counsel rejects | `HALTED_APPROVAL_1_REJECTED` |

#### Skill 2 Failures

| From | Event | To |
|---|---|---|
| `SKILL_2_COMPLETE` | Gate 2b schema fails → 1 retry → still fails | `HALTED_GATE_2_SCHEMA` |
| `SKILL_2_COMPLETE` | Gate 2c Claims Firewall violation | `HALTED_FIREWALL_BREACH_GCM` |
| `SKILL_2_COMPLETE` | Gate 2d score 70–84 | `HALTED_GATE_2_SCORE_BELOW_THRESHOLD` |
| `SKILL_2_COMPLETE` | Gate 2d score < 70 | `HALTED_GATE_2_SCORE_INSUFFICIENT` |

#### Skill 3 Failures

| From | Event | To |
|---|---|---|
| `SKILL_3_COMPLETE` | Gate 3a schema fails → 1 retry → still fails | `HALTED_GATE_3_SCHEMA` |
| `SKILL_3_COMPLETE` | Gate 3b Claims Firewall violation | `HALTED_FIREWALL_BREACH_SOLUTION` |
| `SKILL_3_COMPLETE` | Gate 3c score < 70 | `HALTED_GATE_3_SCORE_INSUFFICIENT` |
| `APPROVAL_2_PENDING` | DPO approves but CISO rejects (or vice versa) | `HALTED_APPROVAL_2_PARTIAL` |
| `APPROVAL_2_PENDING` | Both DPO and CISO reject | `HALTED_APPROVAL_2_REJECTED` |

#### Skill 4 Failures

| From | Event | To |
|---|---|---|
| `SKILL_4_COMPLETE` | Gate 4a schema fails → 1 retry → still fails | `HALTED_GATE_4_SCHEMA` |
| `SKILL_4_COMPLETE` | Gate 4b Claims Firewall violation | `HALTED_FIREWALL_BREACH_ISO` |
| `SKILL_4_COMPLETE` | Gate 4c AMS or ARS 70–84 | `HALTED_GATE_4_SCORE_BELOW_THRESHOLD` |
| `SKILL_4_COMPLETE` | Gate 4c AMS or ARS < 70 | `HALTED_GATE_4_SCORE_INSUFFICIENT` |
| `APPROVAL_3_PENDING` | Client Risk Committee Lead rejects | `HALTED_APPROVAL_3_REJECTED` |
| `APPROVAL_3_PENDING` | Joint approver conflict | `HALTED_APPROVAL_3_PARTIAL` |

#### Skill 5 Failures

| From | Event | To |
|---|---|---|
| `SKILL_5_COMPLETE` | Gate 5a schema fails → 1 retry → still fails | `HALTED_GATE_5_SCHEMA` |
| `SKILL_5_COMPLETE` | Gate 5b Claims Firewall violation | `HALTED_FIREWALL_BREACH_CAPVAL` |
| `SKILL_5_COMPLETE` | Gate 5c: any capability ECS < 90 or escalation_required == true | `HALTED_GATE_5_SCORE_INSUFFICIENT` |

#### Skill 6 Failures

| From | Event | To |
|---|---|---|
| `SKILL_6_COMPLETE` | Gate 6a schema fails → 1 retry → still fails | `HALTED_GATE_6_SCHEMA` |
| `SKILL_6_COMPLETE` | Gate 6b Terminal Claims Firewall violation | `HALTED_FIREWALL_BREACH_TERMINAL` |
| `SKILL_6_COMPLETE` | Gate 6c: Rejected classification (PCS < 80 or CTCS < 80) | `HALTED_PROPOSAL_REJECTED` |
| `SKILL_6_COMPLETE` | Gate 6c: Conditional classification (PCS 80–94 or CTCS 80–94) | `HALTED_PROPOSAL_CONDITIONAL` |
| `APPROVAL_4_PENDING` | Both approvers reject | `HALTED_APPROVAL_4_REJECTED` |
| `APPROVAL_4_PENDING` | One approves, one rejects | `HALTED_APPROVAL_4_PARTIAL` |

#### Cross-Cutting Failures

| From | Event | To |
|---|---|---|
| Any `APPROVAL_N_PENDING` | Timeout exceeded | `APPROVAL_TIMED_OUT` |
| `APPROVAL_TIMED_OUT` | Compliance Analyst extends deadline | Back to same `APPROVAL_N_PENDING` |
| `APPROVAL_TIMED_OUT` | Operator initiates revised run | Same `APPROVAL_N_PENDING` archived; new run starts |
| `SKILL_5_RUNNING` | Capability extraction returns 0 capabilities | `HALTED_ESCALATION` |
| Any active state | Unresolvable execution error | `HALTED_ESCALATION` |

---

## Special Paths

### Conditional Proposal Review Recovery

```
SKILL_6_COMPLETE
      │ Gate 6c: Conditional (PCS 80–94)
      ▼
HALTED_PROPOSAL_CONDITIONAL
      │ Compliance Director reviews each conditional item
      │ and manually attests to each finding
      ▼
GATE_6_PASSED (Conditional Release elevated by CD decision)
      ▼
APPROVAL_4_PENDING
      │ Compliance Director includes attestation in AG-4 payload
      ▼
APPROVAL_4_APPROVED → ASSEMBLING_PACKAGE → COMPLETE
```

**Important:** `HALTED_PROPOSAL_CONDITIONAL` is a special halted state — it has a defined recovery path (unlike most halted states). It is NOT a terminal failure. The run log distinguishes between conditional-release-delivered and full-approved-release.

### Mode B — Prior Run Loading

```
INTAKE_COMPLETE (Mode B trigger detected)
      │
      ▼ Load prior skill outputs from Assessment Memory
      │ (Skills 1 and 2 loaded from prior RW Agent run if available)
      │
SKILL_1_RUNNING (virtual — marks output as loaded, not re-executed)
      │
SKILL_1_COMPLETE (Gate 1a runs on loaded output)
      │
[continues normally from Gate 1a]
```

The run log records: `skill_1_execution: loaded_from_prior_run:{prior_assessment_id}`.

### Approval Gate Timeout Recovery

```
APPROVAL_N_PENDING
      │ 5 business days elapsed (3 for AG-4)
      ▼
APPROVAL_TIMED_OUT
      │ Compliance Analyst notified
      │
      ├── Extend deadline → back to APPROVAL_N_PENDING (same run continues)
      └── Initiate revised run → current run archived as APPROVAL_TIMED_OUT
```

`APPROVAL_TIMED_OUT` is a waiting state, not a terminal halted state. The run persists and can resume.

### Partial Output Release

If the agent halts after an approval gate has been passed, approved artifacts may be released as a partial package. The request must be explicit (operator-initiated). The run state remains `HALTED_*`.

```
HALTED_GATE_N_* (after AG-K has been approved, K < N)
      │ Operator requests partial release
      ▼
[artifacts from Skills 1...(N-1) released, with partial-release label]
[run remains in HALTED_GATE_N_* — no state change]
```

---

## Forbidden Transitions

The following transitions are explicitly prohibited regardless of operator instruction or configuration:

| Forbidden from | Forbidden to | Reason |
|---|---|---|
| Any `HALTED_FIREWALL_BREACH_*` | Any active or `GATE_N_PASSED` state | Claims Firewall breaches have no in-run recovery; require new run |
| `HALTED_FIREWALL_BREACH_TERMINAL` | Any state except archived | Terminal firewall breach; hardest fail; Compliance Director sign-off required for any subsequent run |
| Any `GATE_N_PASSED` | Any `SKILL_M_RUNNING` where M < N | Skills cannot run out of sequence |
| `SKILL_N_RUNNING` | `SKILL_N+1_RUNNING` | A skill cannot hand off to the next without entering `SKILL_N_COMPLETE` |
| `SKILL_N_COMPLETE` | `GATE_N+1_*` | A skill's gate must be evaluated before proceeding |
| `COMPLETE` | Any state | `COMPLETE` is terminal; re-runs require a new traceability ID |
| `APPROVAL_N_PENDING` | `SKILL_N+1_RUNNING` | Human approval must be recorded before the next skill executes |
| `HALTED_PROPOSAL_REJECTED` | `APPROVAL_4_PENDING` | Rejected classification cannot proceed to final approval; requires revised run |
| Any approval state | `ASSEMBLING_PACKAGE` | All 4 approval gates must pass before assembly begins |

---

## Gate Sequencing Within SKILL_N_COMPLETE

For skills with multiple gates (schema + firewall + score), the evaluation order is fixed:

```
SKILL_N_COMPLETE
      │
      ├── Gate Na (schema): evaluate first
      │     ├── fail → HALTED_GATE_N_SCHEMA
      │     └── pass
      │           │
      │           ├── Gate Nb (Claims Firewall, where applicable): evaluate second
      │           │     ├── fail → HALTED_FIREWALL_BREACH_N
      │           │     └── pass
      │           │           │
      │           │           └── Gate Nc (score): evaluate third
      │           │                 ├── below threshold → HALTED_GATE_N_SCORE_BELOW_THRESHOLD
      │           │                 ├── insufficient → HALTED_GATE_N_SCORE_INSUFFICIENT
      │           │                 └── pass → GATE_N_PASSED
      │           │
      │           └── (if no Nb) Gate Nc (score): evaluate second
      │                 └── (same as above)
```

**The Claims Firewall check always precedes the score check.** A high-scoring output with a firewall violation does not pass. A low-scoring output with no firewall violation halts at the score gate, not the firewall gate.

---

## State Persistence Requirements

The following states require durable persistence (must survive process restarts):

| State | Why |
|---|---|
| All `APPROVAL_N_PENDING` states | Human approval may take days; process cannot restart and lose the pending approval |
| `APPROVAL_TIMED_OUT` | Compliance Analyst action is pending |
| `HALTED_PROPOSAL_CONDITIONAL` | Compliance Director review is pending |
| All `GATE_N_PASSED` states | Completed gates must not be re-evaluated after process restart |
| All `APPROVAL_N_APPROVED` states | Approval record must be durable for audit trail |

The following states do NOT need to survive process restarts:

| State | Reason |
|---|---|
| `SKILL_N_RUNNING` | If interrupted, re-execute the skill |
| `ASSEMBLING_PACKAGE` | If interrupted, re-assemble; all approved outputs are already stored |

---

## Claims Firewall Gate Precedence

When the Claims Firewall gate (Nb) fires concurrently with the schema gate:

- Schema failures → `HALTED_GATE_N_SCHEMA` takes precedence
- Claims Firewall violations detected after schema passes → `HALTED_FIREWALL_BREACH_N`
- A document that fails both schema and firewall → HALTED at schema; firewall status recorded in log (but schema fix must come first)

The HALTED state naming convention encodes which check caused the halt. The run log always records ALL gate results (schema status + firewall report + score) for the failed skill, even when only one gate is the primary halt trigger.
