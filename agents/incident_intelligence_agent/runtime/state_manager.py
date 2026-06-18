#!/usr/bin/env python3
"""
State Manager for Incident Intelligence Agent Runtime.
Handles run-level state persistence, transitions validation, and approval gate records.
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

# Valid transitions matching incident intelligence agent lifecycle
VALID_TRANSITIONS = {
    "INTAKE_VALIDATING": {
        "INTAKE_COMPLETE",
        "HALTED_INTAKE_INVALID"
    },
    "INTAKE_COMPLETE": {
        "SKILL_1_RUNNING"
    },
    "SKILL_1_RUNNING": {
        "SKILL_1_COMPLETE",
        "HALTED_GATE_1_INSUFFICIENT",
        "HALTED_GATE_1_SCHEMA"
    },
    "SKILL_1_COMPLETE": {
        "GATE_1_PASSED",
        "HALTED_GATE_1_SCHEMA",
        "HALTED_GATE_1_INSUFFICIENT"
    },
    "GATE_1_PASSED": {
        "APPROVAL_1_PENDING"
    },
    "APPROVAL_1_PENDING": {
        "APPROVAL_1_APPROVED",
        "HALTED_APPROVAL_1_REJECTED"
    },
    "APPROVAL_1_APPROVED": {
        "SKILL_2_RUNNING"
    },
    "SKILL_2_RUNNING": {
        "SKILL_2_COMPLETE",
        "HALTED_GATE_2_INSUFFICIENT",
        "HALTED_GATE_2_SCHEMA"
    },
    "SKILL_2_COMPLETE": {
        "GATE_2_PASSED",
        "HALTED_GATE_2_SCHEMA",
        "HALTED_GATE_2_INSUFFICIENT"
    },
    "GATE_2_PASSED": {
        "SKILL_3_RUNNING"
    },
    "SKILL_3_RUNNING": {
        "SKILL_3_COMPLETE",
        "HALTED_FIREWALL_BREACH",
        "HALTED_GATE_3_SCHEMA"
    },
    "SKILL_3_COMPLETE": {
        "GATE_3_PASSED",
        "HALTED_GATE_3_SCHEMA",
        "HALTED_FIREWALL_BREACH"
    },
    "GATE_3_PASSED": {
        "APPROVAL_2_PENDING"
    },
    "APPROVAL_2_PENDING": {
        "APPROVAL_2_APPROVED",
        "HALTED_APPROVAL_2_REJECTED",
        "HALTED_FIREWALL_BREACH"
    },
    "APPROVAL_2_APPROVED": {
        "COMPLETE"
    },
    "COMPLETE": set(),
    "HALTED_INTAKE_INVALID": {"INTAKE_VALIDATING"},
    "HALTED_GATE_1_SCHEMA": {"INTAKE_VALIDATING", "SKILL_1_RUNNING"},
    "HALTED_GATE_1_INSUFFICIENT": set(),
    "HALTED_APPROVAL_1_REJECTED": {"INTAKE_VALIDATING", "SKILL_1_RUNNING"},
    "HALTED_GATE_2_SCHEMA": {"INTAKE_VALIDATING", "SKILL_2_RUNNING"},
    "HALTED_GATE_2_INSUFFICIENT": set(),
    "HALTED_GATE_3_SCHEMA": {"INTAKE_VALIDATING", "SKILL_3_RUNNING"},
    "HALTED_FIREWALL_BREACH": set(),
    "HALTED_APPROVAL_2_REJECTED": {"INTAKE_VALIDATING", "SKILL_2_RUNNING"}
}

# Forbidden transitions explicitly checked to raise an error
FORBIDDEN_TRANSITIONS = [
    ("APPROVAL_1_PENDING", "COMPLETE"),
    ("APPROVAL_2_PENDING", "COMPLETE"),
    ("GATE_1_PASSED", "COMPLETE"),
    ("GATE_2_PASSED", "COMPLETE"),
    ("GATE_3_PASSED", "COMPLETE"),
    ("SKILL_1_RUNNING", "COMPLETE"),
    ("SKILL_2_RUNNING", "COMPLETE"),
    ("SKILL_3_RUNNING", "COMPLETE")
]

class StateManager:
    def __init__(self, state_dir: str, traceability_id: str):
        """Initializes the State Manager for a specific run."""
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
                "approval_1": None,  # CISO Triage Approval
                "approval_2": None   # DPO + IT Operations Director Containment Approval
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

    def update_intermediate_data(self, key: str, value) -> None:
        """Updates run intermediate data and saves to disk."""
        self.load_state()
        self.state["intermediate_data"][key] = value
        self._save_state()

    def get_state(self) -> dict:
        """Returns the current state."""
        return self.load_state()

    def transition_to(self, to_state: str, trigger: str, actor: str = None, notes: str = None) -> dict:
        """Transitions to a new state after validating transition contracts."""
        self.load_state()  # Ensure latest state
        from_state = self.state["status"]

        if from_state == "COMPLETE":
            raise ValueError(f"Forbidden Transition: Run is in COMPLETE state. No revisions allowed. Traceability ID: {self.traceability_id}")

        if (from_state, to_state) in FORBIDDEN_TRANSITIONS:
            raise ValueError(f"Forbidden Transition: Direct transition from {from_state} to {to_state} is blocked. Traceability ID: {self.traceability_id}")

        if from_state == "HALTED_FIREWALL_BREACH" and to_state != "INTAKE_VALIDATING":
            raise ValueError(f"Forbidden Transition: Cannot recover from HALTED_FIREWALL_BREACH to '{to_state}'. Traceability ID: {self.traceability_id}")

        valid_targets = VALID_TRANSITIONS.get(from_state, set())
        if to_state not in valid_targets:
            raise ValueError(f"Invalid Transition: State {from_state} cannot transition to {to_state}. Traceability ID: {self.traceability_id}")

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

        if to_state == "APPROVAL_1_APPROVED":
            self.state["approvals"]["approval_1"] = {"status": "Approved", "actor": actor, "timestamp": timestamp, "notes": notes}
        elif to_state == "APPROVAL_2_APPROVED":
            self.state["approvals"]["approval_2"] = {"status": "Approved", "actor": actor, "timestamp": timestamp, "notes": notes}

        self._save_state()
        return self.state
