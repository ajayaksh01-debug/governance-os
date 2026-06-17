#!/usr/bin/env python3
"""
Audit Logger for Capability Validation Agent Runtime.
Logs structured execution trails to persistent storage in JSON Lines (JSONL) format.
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir: str, traceability_id: str):
        """Initializes the audit logger for a specific traceability ID."""
        self.log_dir = Path(log_dir)
        self.traceability_id = traceability_id
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{self.traceability_id}_audit.jsonl"

    def log(self, step: str, status: str, message: str, details: dict = None) -> None:
        """
        Logs a single audit event with timestamp (ISO 8601 UTC).
        Writes to a run-specific JSONL file and prints to standard output.
        """
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        entry = {
            "traceability_id": self.traceability_id,
            "timestamp": timestamp,
            "step": step,
            "status": status.upper(),
            "message": message,
            "details": details or {}
        }
        
        # Write to JSONL
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Error writing to audit log: {e}")

        # Print to stdout for visibility
        status_symbol = "✅"
        if status.upper() in ["FAILED", "ERROR", "BREACH"]:
            status_symbol = "❌"
        elif status.upper() in ["WARNING", "HALTED", "PENDING"]:
            status_symbol = "⚠️"
            
        print(f"[{timestamp}] {status_symbol} [{status.upper()}] {step} - {message}")

    def get_logs(self) -> list:
        """Reads and returns all log entries for this run."""
        if not self.log_file.exists():
            return []
            
        logs = []
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
        except Exception as e:
            print(f"Error reading audit log: {e}")
            
        return logs
