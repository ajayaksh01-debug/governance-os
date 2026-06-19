#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

VALID_TRANSITIONS = {
    "INTAKE_VALIDATING": {
        "INTAKE_COMPLETE",
        "HALTED_INTAKE_INVALID"
    },
    "INTAKE_COMPLETE": {
        "RUNNING_REVIEW"
    },
    "RUNNING_REVIEW": {
        "REVIEW_COMPLETE",
        "HALTED_REVIEW_SCHEMA",
        "HALTED_GOVERNANCE_INCOMPLETE"
    },
    "REVIEW_COMPLETE": {
        "GATE_VALIDATION_PASSED",
        "HALTED_GATE_INSUFFICIENT"
    },
    "GATE_VALIDATION_PASSED": {
        "APPROVAL_PENDING"
    },
    "APPROVAL_PENDING": {
        "APPROVAL_APPROVED",
        "HALTED_APPROVAL_REJECTED"
    },
    "APPROVAL_APPROVED": {
        "COMPLETE"
    },
    "COMPLETE": set(),
    "HALTED_INTAKE_INVALID": set(),
    "HALTED_REVIEW_SCHEMA": set(),
    "HALTED_GOVERNANCE_INCOMPLETE": set(),
    "HALTED_GATE_INSUFFICIENT": set(),
    "HALTED_APPROVAL_REJECTED": set(),
}

# These transitions are blocked regardless of VALID_TRANSITIONS — approval gate cannot be skipped.
FORBIDDEN_TRANSITIONS = [
    ("APPROVAL_PENDING", "COMPLETE"),
    ("GATE_VALIDATION_PASSED", "COMPLETE"),
    ("RUNNING_REVIEW", "COMPLETE"),
]


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
            "approvals": {"final_approval": None},
            "history": [],
        }

    def initialize_run(self, inputs: dict) -> dict:
        self.state["inputs"] = inputs
        self.state["status"] = "INTAKE_VALIDATING"
        self.state["history"] = [{
            "traceability_id": self.traceability_id,
            "from_state": None,
            "to_state": "INTAKE_VALIDATING",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "trigger": "Run initialized",
            "actor_identity": None,
            "notes": None,
        }]
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

    def update_intermediate_data(self, key: str, value) -> None:
        self.load_state()
        self.state["intermediate_data"][key] = value
        self._save_state()

    def get_state(self) -> dict:
        return self.load_state()

    def transition_to(self, to_state: str, trigger: str, actor: str = None, notes: str = None) -> dict:
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

        valid_targets = VALID_TRANSITIONS.get(from_state, set())
        if to_state not in valid_targets:
            raise ValueError(
                f"Invalid Transition: {from_state} cannot transition to {to_state}. "
                f"Traceability ID: {self.traceability_id}"
            )

        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        self.state["status"] = to_state
        self.state["history"].append({
            "traceability_id": self.traceability_id,
            "from_state": from_state,
            "to_state": to_state,
            "timestamp": timestamp,
            "trigger": trigger,
            "actor_identity": actor,
            "notes": notes,
        })

        if to_state == "APPROVAL_APPROVED":
            self.state["approvals"]["final_approval"] = {
                "status": "Approved",
                "actor": actor,
                "timestamp": timestamp,
                "notes": notes,
            }

        self._save_state()
        return self.state
