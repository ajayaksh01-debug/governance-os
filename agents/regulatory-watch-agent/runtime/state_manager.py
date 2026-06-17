#!/usr/bin/env python3
"""
State Manager for Regulatory Watch Agent Runtime.
Handles run-level state persistence, transitions validation, and approval gate records.
Ensures compliance with state-machine.md transition constraints and forbidden paths.
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

# Valid transitions matching state-machine.md
VALID_TRANSITIONS = {
    "INTAKE_VALIDATING": {
        "INTAKE_COMPLETE",
        "HALTED_INTAKE_INVALID",
        "HALTED_INTAKE_UNSUPPORTED_JURISDICTION"
    },
    "INTAKE_COMPLETE": {
        "SKILL_1_RUNNING"
    },
    "SKILL_1_RUNNING": {
        "SKILL_1_COMPLETE",
        "HALTED_ESCALATION"
    },
    "SKILL_1_COMPLETE": {
        "GATE_1_PASSED",
        "HALTED_GATE_1_SCHEMA",
        "HALTED_FIREWALL_BREACH"
    },
    "GATE_1_PASSED": {
        "GATE_2_PASSED",
        "HALTED_GATE_2_PRELIMINARY",
        "HALTED_GATE_2_INSUFFICIENT"
    },
    "GATE_2_PASSED": {
        "APPROVAL_1_PENDING"
    },
    "APPROVAL_1_PENDING": {
        "APPROVAL_1_APPROVED",
        "HALTED_APPROVAL_1_REJECTED",
        "APPROVAL_TIMED_OUT"
    },
    "APPROVAL_1_APPROVED": {
        "SKILL_2_RUNNING"
    },
    "SKILL_2_RUNNING": {
        "SKILL_2_COMPLETE",
        "HALTED_ESCALATION"
    },
    "SKILL_2_COMPLETE": {
        "GATE_3_PASSED",
        "HALTED_GATE_3A_SCHEMA",
        "HALTED_FIREWALL_BREACH"
    },
    "GATE_3_PASSED": {
        "GATE_4_PASSED",
        "HALTED_GATE_4_BELOW_THRESHOLD",
        "HALTED_GATE_4_INSUFFICIENT"
    },
    "GATE_4_PASSED": {
        "APPROVAL_2_PENDING"
    },
    "APPROVAL_2_PENDING": {
        "APPROVAL_2_APPROVED",
        "HALTED_APPROVAL_2_REJECTED",
        "HALTED_APPROVAL_2_PARTIAL",
        "APPROVAL_TIMED_OUT",
        "HALTED_FIREWALL_BREACH"
    },
    "APPROVAL_2_APPROVED": {
        "COMPLETE"
    },
    "APPROVAL_TIMED_OUT": {
        "APPROVAL_1_PENDING",
        "APPROVAL_2_PENDING",
        "APPROVAL_1_APPROVED",
        "APPROVAL_2_APPROVED",
        "HALTED_APPROVAL_1_REJECTED",
        "HALTED_APPROVAL_2_REJECTED",
        "HALTED_APPROVAL_2_PARTIAL"
    },
    "COMPLETE": set(),
    "HALTED_INTAKE_INVALID": {"INTAKE_VALIDATING"},
    "HALTED_INTAKE_UNSUPPORTED_JURISDICTION": set(),
    "HALTED_GATE_1_SCHEMA": {"INTAKE_VALIDATING", "SKILL_1_RUNNING"},
    "HALTED_GATE_2_PRELIMINARY": {"INTAKE_VALIDATING", "SKILL_1_RUNNING"},
    "HALTED_GATE_2_INSUFFICIENT": set(),
    "HALTED_APPROVAL_1_REJECTED": {"INTAKE_VALIDATING", "SKILL_1_RUNNING"},
    "HALTED_GATE_3A_SCHEMA": {"INTAKE_VALIDATING", "SKILL_2_RUNNING"},
    "HALTED_FIREWALL_BREACH": set(),  # Claims Firewall breach is terminal, requires new run
    "HALTED_GATE_4_BELOW_THRESHOLD": {"INTAKE_VALIDATING", "SKILL_2_RUNNING"},
    "HALTED_GATE_4_INSUFFICIENT": set(),
    "HALTED_APPROVAL_2_PARTIAL": {"INTAKE_VALIDATING", "SKILL_2_RUNNING"},
    "HALTED_APPROVAL_2_REJECTED": {"INTAKE_VALIDATING", "SKILL_2_RUNNING"},
    "HALTED_ESCALATION": {"INTAKE_VALIDATING", "SKILL_1_RUNNING", "SKILL_2_RUNNING"}
}

# Forbidden transitions explicitly checked to raise an error
FORBIDDEN_TRANSITIONS = [
    ("APPROVAL_1_PENDING", "SKILL_2_RUNNING"),
    ("APPROVAL_2_PENDING", "COMPLETE"),
    ("GATE_1_PASSED", "SKILL_2_RUNNING"),
    ("GATE_3_PASSED", "APPROVAL_2_PENDING"),
    ("SKILL_1_RUNNING", "SKILL_2_RUNNING")
]

class StateManager:
    def __init__(self, state_dir: str, traceability_id: str):
        """Initializes the State Manager for a specific run and path."""
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
                "approval_1": None,  # General Counsel
                "approval_2": None   # DPO + InfoSec Lead
            },
            "history": []
        }

    def initialize_run(self, inputs: dict) -> dict:
        """Initializes and saves the run state with the given inputs."""
        self.state["inputs"] = inputs
        self.state["status"] = "INTAKE_VALIDATING"
        self.state["history"] = [{
            "traceability_id": self.traceability_id,
            "from_state": None,
            "to_state": "INTAKE_VALIDATING",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "trigger": "Run initialized",
            "actor_identity": None,
            "notes": None
        }]
        self._save_state()
        return self.state

    def _save_state(self) -> None:
        """Writes current state to the JSON file on disk."""
        try:
            self.state_file.write_text(json.dumps(self.state, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"Error saving run state: {e}")

    def load_state(self) -> dict:
        """Loads state from disk if exists, replacing internal state."""
        if self.state_file.exists():
            try:
                self.state = json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"Error loading run state: {e}")
        return self.state

    def transition_to(self, to_state: str, trigger: str, actor: str = None, notes: str = None) -> dict:
        """
        Transitions to a new state after validating transition contracts.
        Raises ValueError if transition is forbidden or invalid.
        """
        self.load_state()  # Ensure we have the latest state from disk
        from_state = self.state["status"]

        # Check terminal state COMPLETE block
        if from_state == "COMPLETE":
            raise ValueError(f"Forbidden Transition: Run is in COMPLETE state. No revisions allowed. Traceability ID: {self.traceability_id}")

        # Check explicit forbidden transitions
        if (from_state, to_state) in FORBIDDEN_TRANSITIONS:
            raise ValueError(f"Forbidden Transition: Direct transition from {from_state} to {to_state} is blocked. Traceability ID: {self.traceability_id}")

        # Check firewall breach recovery restriction
        if from_state == "HALTED_FIREWALL_BREACH" and to_state != "INTAKE_VALIDATING":
            raise ValueError(f"Forbidden Transition: Cannot recover from HALTED_FIREWALL_BREACH to active state '{to_state}'. Compliance Director review required. Traceability ID: {self.traceability_id}")

        # Validate transition exists in mapping
        valid_targets = VALID_TRANSITIONS.get(from_state, set())
        if to_state not in valid_targets:
            raise ValueError(f"Invalid Transition: State {from_state} cannot transition to {to_state}. Traceability ID: {self.traceability_id}")

        # Execute transition
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        self.state["status"] = to_state
        self.state["history"].append({
            "traceability_id": self.traceability_id,
            "from_state": from_state,
            "to_state": to_state,
            "timestamp": timestamp,
            "trigger": trigger,
            "actor_identity": actor,
            "notes": notes
        })

        # Update approvals dict in state if relevant
        if to_state == "APPROVAL_1_APPROVED":
            self.state["approvals"]["approval_1"] = {"status": "Approved", "actor": actor, "timestamp": timestamp, "notes": notes}
        elif to_state == "HALTED_APPROVAL_1_REJECTED":
            self.state["approvals"]["approval_1"] = {"status": "Rejected", "actor": actor, "timestamp": timestamp, "notes": notes}
        elif to_state == "APPROVAL_2_APPROVED":
            self.state["approvals"]["approval_2"] = {"status": "Approved", "actor": actor, "timestamp": timestamp, "notes": notes}
        elif to_state == "HALTED_APPROVAL_2_REJECTED":
            self.state["approvals"]["approval_2"] = {"status": "Rejected", "actor": actor, "timestamp": timestamp, "notes": notes}
        elif to_state == "HALTED_APPROVAL_2_PARTIAL":
            self.state["approvals"]["approval_2"] = {"status": "Partial", "actor": actor, "timestamp": timestamp, "notes": notes}

        self._save_state()
        return self.state

    def update_intermediate_data(self, key: str, value: any) -> None:
        """Saves intermediate values or outputs generated during skill/gate execution."""
        self.load_state()
        self.state["intermediate_data"][key] = value
        self._save_state()

    def get_state(self) -> dict:
        """Returns the current state dict."""
        return self.state

    @staticmethod
    def load_run(state_dir: str, traceability_id: str) -> dict:
        """Loads a run state from the filesystem, returning None if not found."""
        path = Path(state_dir) / f"{traceability_id}_state.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Error loading run {traceability_id}: {e}")
            return None
