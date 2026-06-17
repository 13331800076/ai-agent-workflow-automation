"""Audit logger: records structured logs for every task execution."""
import json
from datetime import UTC, datetime
from typing import Any

from .artifact_store import ArtifactStore


class AuditLogger:
    """Structured audit logger for AI Agent workflow execution."""

    def __init__(self, artifact_store: ArtifactStore) -> None:
        self.artifact_store = artifact_store

    def log_task_start(self, task_id: str, plan: dict[str, Any]) -> None:
        task_dir = self.artifact_store.get_task_dir(task_id)
        task_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "task.json").write_text(
            json.dumps(
                {
                    "task_id": task_id,
                    "started_at": datetime.now(UTC).isoformat(),
                },
                indent=2,
            )
        )
        (task_dir / "plan.json").write_text(json.dumps(plan, indent=2))

    def log_step(self, task_id: str, step_record: dict[str, Any]) -> None:
        log_path = self.artifact_store.get_task_dir(task_id) / "execution.log"
        entry = json.dumps(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "step": step_record,
            },
            indent=2,
        )
        with log_path.open("a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def log_task_end(self, task_id: str, status: str, error: str | None) -> None:
        log_path = self.artifact_store.get_task_dir(task_id) / "execution.log"
        entry = json.dumps(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "event": "task_end",
                "status": status,
                "error": error,
            },
            indent=2,
        )
        with log_path.open("a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def save_result(self, task_id: str, result: dict[str, Any]) -> None:
        result_path = self.artifact_store.get_task_dir(task_id) / "result.json"
        result_path.write_text(json.dumps(result, indent=2))
