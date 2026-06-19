#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path


class AuditLogger:
    def __init__(self, log_dir: str, traceability_id: str):
        self.log_dir = Path(log_dir)
        self.traceability_id = traceability_id
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{self.traceability_id}_audit.jsonl"

    def log(self, step: str, status: str, message: str, details: dict = None) -> None:
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        entry = {
            "traceability_id": self.traceability_id,
            "timestamp": timestamp,
            "step": step,
            "status": status.upper(),
            "message": message,
            "details": details or {},
        }
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Error writing to audit log: {e}")

        symbol = "✅"
        if status.upper() in ("FAILED", "ERROR", "BREACH"):
            symbol = "❌"
        elif status.upper() in ("WARNING", "HALTED", "PENDING"):
            symbol = "⚠️"
        print(f"[{timestamp}] {symbol} [{status.upper()}] {step} — {message}")

    def get_logs(self) -> list:
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
