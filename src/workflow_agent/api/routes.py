"""API routes for agent task execution."""
import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from ..agent.models import TaskRequest
from ..agent.parser import TaskParser
from ..agent.planner import WorkflowPlanner
from ..executor.workflow_executor import WorkflowExecutor
from ..logging.artifact_store import ArtifactStore
from ..logging.audit_logger import AuditLogger

router = APIRouter(prefix="/tasks")

ARTIFACTS_DIR = Path("artifacts")


class RunTaskRequest(BaseModel):
    user_input: str


class RunTaskResponse(BaseModel):
    task_id: str
    status: str
    parsed: dict[str, Any]
    plan: dict[str, Any]
    result: dict[str, Any]


@router.post("/run", response_model=RunTaskResponse)
async def run_task(req: RunTaskRequest) -> dict[str, Any]:
    import uuid
    from datetime import datetime

    task_id = f"task_{uuid.uuid4().hex[:8]}"
    task_request = TaskRequest(
        task_id=task_id, user_input=req.user_input, created_at=datetime.utcnow()
    )

    parser = TaskParser()
    parsed = parser.parse(task_request)

    planner = WorkflowPlanner()
    plan = planner.create_plan(parsed)

    artifact_store = ArtifactStore(str(ARTIFACTS_DIR))
    audit_logger = AuditLogger(artifact_store)
    executor = WorkflowExecutor(audit_logger)
    result = await executor.execute(plan, task_id)

    return {
        "task_id": task_id,
        "status": result.status,
        "parsed": parsed.model_dump(),
        "plan": plan.model_dump(),
        "result": result.model_dump(),
    }


@router.get("/{task_id}")
async def get_task(task_id: str) -> dict[str, Any]:
    artifact_store = ArtifactStore(str(ARTIFACTS_DIR))
    result_path = artifact_store.get_result_path(task_id)
    if not result_path.exists():
        return {"error": "Task not found"}
    return json.loads(result_path.read_text())


@router.get("/{task_id}/artifacts")
async def get_task_artifacts(task_id: str) -> dict[str, Any]:
    artifact_store = ArtifactStore(str(ARTIFACTS_DIR))
    task_dir = artifact_store.get_task_dir(task_id)
    if not task_dir.exists():
        return {"error": "Task not found"}
    artifacts = []
    for f in task_dir.rglob("*"):
        if f.is_file():
            artifacts.append(str(f.relative_to(task_dir)))
    return {"task_id": task_id, "artifacts": artifacts}
