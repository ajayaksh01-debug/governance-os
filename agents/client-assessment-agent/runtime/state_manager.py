#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

VALID_TRANSITIONS = {
    # Intake
    "INTAKE_VALIDATING": {
        "INTAKE_COMPLETE",
        "HALTED_INTAKE_INVALID",
        "HALTED_INTAKE_UNSUPPORTED_JURISDICTION",
    },
    "INTAKE_COMPLETE": {"SKILL_1_RUNNING"},
    # Skill 1 — regulatory-mapping
    "SKILL_1_RUNNING": {"SKILL_1_COMPLETE", "HALTED_ESCALATION"},
    "SKILL_1_COMPLETE": {
        "GATE_1_PASSED",
        "HALTED_GATE_1_SCHEMA",
        "HALTED_GATE_1_SCORE_PRELIMINARY",
        "HALTED_GATE_1_SCORE_INSUFFICIENT",
    },
    "GATE_1_PASSED": {"APPROVAL_1_PENDING"},
    "APPROVAL_1_PENDING": {
        "APPROVAL_1_APPROVED",
        "HALTED_APPROVAL_1_REJECTED",
        "APPROVAL_TIMED_OUT",
    },
    "APPROVAL_1_APPROVED": {"SKILL_2_RUNNING"},
    # Skill 2 — governance-control-mapping
    "SKILL_2_RUNNING": {"SKILL_2_COMPLETE", "HALTED_ESCALATION"},
    "SKILL_2_COMPLETE": {
        "GATE_2_PASSED",
        "HALTED_GATE_2_SCHEMA",
        "HALTED_FIREWALL_BREACH",
        "HALTED_GATE_2_SCORE_BELOW_THRESHOLD",
        "HALTED_GATE_2_SCORE_INSUFFICIENT",
    },
    "GATE_2_PASSED": {"SKILL_3_RUNNING"},
    # Skill 3 — ethana-solution-mapping
    "SKILL_3_RUNNING": {"SKILL_3_COMPLETE", "HALTED_ESCALATION"},
    "SKILL_3_COMPLETE": {
        "GATE_3_PASSED",
        "HALTED_GATE_3_SCHEMA",
        "HALTED_FIREWALL_BREACH",
        "HALTED_GATE_3_SCORE_INSUFFICIENT",
    },
    "GATE_3_PASSED": {"APPROVAL_2_PENDING"},
    "APPROVAL_2_PENDING": {
        "APPROVAL_2_APPROVED",
        "HALTED_APPROVAL_2_PARTIAL",
        "HALTED_APPROVAL_2_REJECTED",
        "APPROVAL_TIMED_OUT",
    },
    "APPROVAL_2_APPROVED": {"SKILL_4_RUNNING"},
    # Skill 4 — iso-42001-gap-assessment
    "SKILL_4_RUNNING": {"SKILL_4_COMPLETE", "HALTED_ESCALATION"},
    "SKILL_4_COMPLETE": {
        "GATE_4_PASSED",
        "HALTED_GATE_4_SCHEMA",
        "HALTED_FIREWALL_BREACH",
        "HALTED_GATE_4_SCORE_BELOW_THRESHOLD",
        "HALTED_GATE_4_SCORE_INSUFFICIENT",
    },
    "GATE_4_PASSED": {"APPROVAL_3_PENDING"},
    "APPROVAL_3_PENDING": {
        "APPROVAL_3_APPROVED",
        "HALTED_APPROVAL_3_REJECTED",
        "HALTED_APPROVAL_3_PARTIAL",
        "APPROVAL_TIMED_OUT",
    },
    "APPROVAL_3_APPROVED": {"SKILL_5_RUNNING"},
    # Skill 5 — ethana-capability-validation
    "SKILL_5_RUNNING": {"SKILL_5_COMPLETE", "HALTED_ESCALATION"},
    "SKILL_5_COMPLETE": {
        "GATE_5_PASSED",
        "HALTED_GATE_5_SCHEMA",
        "HALTED_FIREWALL_BREACH",
        "HALTED_GATE_5_SCORE_INSUFFICIENT",
    },
    "GATE_5_PASSED": {"SKILL_6_RUNNING"},
    # Skill 6 — ethana-proposal-review
    "SKILL_6_RUNNING": {"SKILL_6_COMPLETE", "HALTED_ESCALATION"},
    "SKILL_6_COMPLETE": {
        "GATE_6_PASSED",
        "HALTED_GATE_6_SCHEMA",
        "HALTED_FIREWALL_BREACH_TERMINAL",
        "HALTED_PROPOSAL_REJECTED",
        "HALTED_PROPOSAL_CONDITIONAL",
    },
    "GATE_6_PASSED": {"APPROVAL_4_PENDING"},
    "APPROVAL_4_PENDING": {
        "APPROVAL_4_APPROVED",
        "HALTED_APPROVAL_4_REJECTED",
        "HALTED_APPROVAL_4_PARTIAL",
        "APPROVAL_TIMED_OUT",
    },
    "APPROVAL_4_APPROVED": {"ASSEMBLING_PACKAGE"},
    "ASSEMBLING_PACKAGE": {"COMPLETE"},
    # Terminal success
    "COMPLETE": set(),
    # Cross-cutting
    "APPROVAL_TIMED_OUT": {
        "APPROVAL_1_PENDING",
        "APPROVAL_2_PENDING",
        "APPROVAL_3_PENDING",
        "APPROVAL_4_PENDING",
        "HALTED_ESCALATION",
    },
    # Special halted state with recovery (Conditional Release)
    "HALTED_PROPOSAL_CONDITIONAL": {"GATE_6_PASSED"},
    # Terminal halted states — no outgoing transitions
    "HALTED_INTAKE_INVALID": set(),
    "HALTED_INTAKE_UNSUPPORTED_JURISDICTION": set(),
    "HALTED_GATE_1_SCHEMA": set(),
    "HALTED_GATE_1_SCORE_PRELIMINARY": set(),
    "HALTED_GATE_1_SCORE_INSUFFICIENT": set(),
    "HALTED_APPROVAL_1_REJECTED": set(),
    "HALTED_GATE_2_SCHEMA": set(),
    "HALTED_FIREWALL_BREACH": set(),
    "HALTED_GATE_2_SCORE_BELOW_THRESHOLD": set(),
    "HALTED_GATE_2_SCORE_INSUFFICIENT": set(),
    "HALTED_GATE_3_SCHEMA": set(),
    "HALTED_GATE_3_SCORE_INSUFFICIENT": set(),
    "HALTED_APPROVAL_2_PARTIAL": set(),
    "HALTED_APPROVAL_2_REJECTED": set(),
    "HALTED_GATE_4_SCHEMA": set(),
    "HALTED_GATE_4_SCORE_BELOW_THRESHOLD": set(),
    "HALTED_GATE_4_SCORE_INSUFFICIENT": set(),
    "HALTED_APPROVAL_3_REJECTED": set(),
    "HALTED_APPROVAL_3_PARTIAL": set(),
    "HALTED_GATE_5_SCHEMA": set(),
    "HALTED_GATE_5_SCORE_INSUFFICIENT": set(),
    "HALTED_GATE_6_SCHEMA": set(),
    "HALTED_FIREWALL_BREACH_TERMINAL": set(),
    "HALTED_PROPOSAL_REJECTED": set(),
    "HALTED_APPROVAL_4_REJECTED": set(),
    "HALTED_APPROVAL_4_PARTIAL": set(),
    "HALTED_ESCALATION": set(),
}

FORBIDDEN_TRANSITIONS = [
    ("APPROVAL_1_PENDING", "SKILL_2_RUNNING"),
    ("APPROVAL_2_PENDING", "SKILL_4_RUNNING"),
    ("APPROVAL_3_PENDING", "SKILL_5_RUNNING"),
    ("APPROVAL_4_PENDING", "ASSEMBLING_PACKAGE"),
    ("APPROVAL_4_PENDING", "COMPLETE"),
    ("GATE_6_PASSED", "COMPLETE"),
    ("SKILL_1_RUNNING", "SKILL_2_RUNNING"),
    ("SKILL_2_RUNNING", "SKILL_3_RUNNING"),
    ("SKILL_3_RUNNING", "SKILL_4_RUNNING"),
    ("SKILL_4_RUNNING", "SKILL_5_RUNNING"),
    ("SKILL_5_RUNNING", "SKILL_6_RUNNING"),
    ("HALTED_PROPOSAL_REJECTED", "APPROVAL_4_PENDING"),
]

# Valid approver roles per joint gate
JOINT_GATE_ROLES = {
    2: ("dpo", "ciso"),
    4: ("compliance_director", "sales_director"),
}


class StateManager:
    def __init__(self, state_dir: str, traceability_id: str):
        self.state_dir = Path(state_dir)
        self.traceability_id = traceability_id
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_dir / f"{self.traceability_id}_state.json"
        self.state = {
            "traceability_id": self.traceability_id,
            "status": "INTAKE_VALIDATING",
            "inputs": {},
            "intermediate_data": {},
            "approvals": {
                "approval_1": None,
                "approval_2": {"dpo": None, "ciso": None, "resolved": None},
                "approval_3": None,
                "approval_4": {
                    "compliance_director": None,
                    "sales_director": None,
                    "resolved": None,
                },
            },
            "history": [],
        }

    def initialize_run(self, inputs: dict) -> dict:
        self.state["inputs"] = inputs
        self.state["status"] = "INTAKE_VALIDATING"
        self.state["history"] = [
            {
                "traceability_id": self.traceability_id,
                "from_state": None,
                "to_state": "INTAKE_VALIDATING",
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "trigger": "Run initialized",
                "actor_identity": None,
                "notes": None,
            }
        ]
        self._save_state()
        return self.state

    def _save_state(self) -> None:
        try:
            self.state_file.write_text(json.dumps(self.state, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"Error saving run state: {e}")

    def load_state(self) -> dict:
        if self.state_file.exists():
            try:
                self.state = json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"Error loading run state: {e}")
        return self.state

    def transition_to(
        self, to_state: str, trigger: str, actor: str = None, notes: str = None
    ) -> dict:
        self.load_state()
        from_state = self.state["status"]

        if from_state == "COMPLETE":
            raise ValueError(
                f"Forbidden Transition: Run is in COMPLETE state. "
                f"Traceability ID: {self.traceability_id}"
            )

        if (from_state, to_state) in FORBIDDEN_TRANSITIONS:
            raise ValueError(
                f"Forbidden Transition: {from_state} → {to_state} is blocked. "
                f"Traceability ID: {self.traceability_id}"
            )

        if (
            from_state in ("HALTED_FIREWALL_BREACH", "HALTED_FIREWALL_BREACH_TERMINAL")
            and to_state not in VALID_TRANSITIONS.get(from_state, set())
        ):
            raise ValueError(
                f"Forbidden Transition: Firewall breach state {from_state} has no in-run recovery. "
                f"Traceability ID: {self.traceability_id}"
            )

        valid_targets = VALID_TRANSITIONS.get(from_state, set())
        if to_state not in valid_targets:
            raise ValueError(
                f"Invalid Transition: {from_state} cannot transition to {to_state}. "
                f"Traceability ID: {self.traceability_id}"
            )

        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        self.state["status"] = to_state
        self.state["history"].append(
            {
                "traceability_id": self.traceability_id,
                "from_state": from_state,
                "to_state": to_state,
                "timestamp": timestamp,
                "trigger": trigger,
                "actor_identity": actor,
                "notes": notes,
            }
        )

        # Record single-approver decisions
        if to_state == "APPROVAL_1_APPROVED":
            self.state["approvals"]["approval_1"] = {
                "status": "Approved",
                "actor": actor,
                "timestamp": timestamp,
                "notes": notes,
            }
        elif to_state == "HALTED_APPROVAL_1_REJECTED":
            self.state["approvals"]["approval_1"] = {
                "status": "Rejected",
                "actor": actor,
                "timestamp": timestamp,
                "notes": notes,
            }
        elif to_state == "APPROVAL_3_APPROVED":
            self.state["approvals"]["approval_3"] = {
                "status": "Approved",
                "actor": actor,
                "timestamp": timestamp,
                "notes": notes,
            }
        elif to_state == "HALTED_APPROVAL_3_REJECTED":
            self.state["approvals"]["approval_3"] = {
                "status": "Rejected",
                "actor": actor,
                "timestamp": timestamp,
                "notes": notes,
            }
        elif to_state == "HALTED_APPROVAL_3_PARTIAL":
            self.state["approvals"]["approval_3"] = {
                "status": "Partial",
                "actor": actor,
                "timestamp": timestamp,
                "notes": notes,
            }

        self._save_state()
        return self.state

    def record_approval_decision(
        self, gate_num: int, role: str, action: str, actor: str, notes: str = None
    ) -> str:
        """
        Records a per-role decision for joint approval gates (AG-2, AG-4).
        Returns: "awaiting_second" | "approved" | "partial" | "rejected"
        """
        self.load_state()
        valid_roles = JOINT_GATE_ROLES.get(gate_num, ())
        if role not in valid_roles:
            raise ValueError(
                f"Invalid role '{role}' for AG-{gate_num}. "
                f"Expected one of: {valid_roles}"
            )

        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        key = f"approval_{gate_num}"
        self.state["approvals"][key][role] = {
            "action": action,
            "actor": actor,
            "timestamp": timestamp,
            "notes": notes,
        }

        role_a, role_b = valid_roles
        decision_a = self.state["approvals"][key].get(role_a)
        decision_b = self.state["approvals"][key].get(role_b)

        if decision_a is None or decision_b is None:
            resolution = "awaiting_second"
        else:
            approved_a = decision_a["action"] in ("Approve", "Approve with notes")
            approved_b = decision_b["action"] in ("Approve", "Approve with notes")
            if approved_a and approved_b:
                resolution = "approved"
            elif not approved_a and not approved_b:
                resolution = "rejected"
            else:
                resolution = "partial"

        self.state["approvals"][key]["resolved"] = resolution

        # Record history entry for this individual decision
        self.state["history"].append(
            {
                "traceability_id": self.traceability_id,
                "from_state": self.state["status"],
                "to_state": self.state["status"],
                "timestamp": timestamp,
                "trigger": f"AG-{gate_num} {role} decision: {action}",
                "actor_identity": actor,
                "notes": notes,
            }
        )

        self._save_state()
        return resolution

    def get_approval_decisions(self, gate_num: int) -> dict:
        self.load_state()
        return self.state["approvals"].get(f"approval_{gate_num}", {})

    def update_intermediate_data(self, key: str, value) -> None:
        self.load_state()
        self.state["intermediate_data"][key] = value
        self._save_state()

    def get_state(self) -> dict:
        return self.load_state()

    @staticmethod
    def load_run(state_dir: str, traceability_id: str) -> dict:
        path = Path(state_dir) / f"{traceability_id}_state.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Error loading run {traceability_id}: {e}")
            return None
