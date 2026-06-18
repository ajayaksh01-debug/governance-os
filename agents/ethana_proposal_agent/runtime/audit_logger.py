#!/usr/bin/env python3
"""
Audit Logger for Ethana Proposal Agent Runtime.
Generates structured, append-only logs for runtime events.
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir: str, traceability_id: str):
        """Initializes the audit logger for a specific run."""
        self.log_dir = Path(log_dir)
        self.traceability_id = traceability_id
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{self.traceability_id}_audit.jsonl"
        self.logs = []

    def log(self, event_type: str, status: str, details: str) -> dict:
        """Appends a structured event log entry to the log file."""
        entry = {
            "traceability_id": self.traceability_id,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "event_type": event_type,
            "status": status,
            "details": details
        }
        
        self.logs.append(entry)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Error writing audit log: {e}")
            
        return entry

    def get_logs(self) -> list:
        """Returns the list of logs generated in the current session."""
        return self.logs
