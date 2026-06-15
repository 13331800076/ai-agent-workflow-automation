"""Artifact store: manages task artifact directories."""
from pathlib import Path
from typing import Any


class ArtifactStore:
    """Manage artifact directories for each task execution."""

    def __init__(self, artifacts_dir: str) -> None:
        self.base_dir = Path(artifacts_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_task_dir(self, task_id: str) -> Path:
        return self.base_dir / task_id

    def get_result_path(self, task_id: str) -> Path:
        return self.get_task_dir(task_id) / "result.json"
