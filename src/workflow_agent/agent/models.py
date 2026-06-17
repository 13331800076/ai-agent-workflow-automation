from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Intent(StrEnum):
    CREATE_CUSTOMER = "create_customer"
    SEARCH_ORDER = "search_order"
    EXPORT_REPORT = "export_report"
    CHECK_FIELD_DIFF = "check_field_diff"
    FILL_FORM = "fill_form"


class TaskRequest(BaseModel):
    task_id: str
    user_input: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ParsedTask(BaseModel):
    task_id: str
    intent: str
    entities: dict[str, Any]
    confidence: float


class WorkflowStep(BaseModel):
    step_id: str
    tool_name: str
    input: dict[str, Any]
    expected_result: str = ""


class WorkflowPlan(BaseModel):
    task_id: str
    intent: str
    steps: list[WorkflowStep]


class StepResult(BaseModel):
    step_id: str
    tool_name: str
    status: Literal["success", "failed", "partial"]
    duration_ms: int
    input: dict[str, Any]
    output: dict[str, Any] | None = None
    error: str | None = None
    screenshot: str | None = None


class ExecutionResult(BaseModel):
    task_id: str
    status: Literal["success", "failed", "partial"]
    steps: list[StepResult]
    screenshots: list[str]
    logs: list[str]
    error: str | None = None


class ToolResult(BaseModel):
    status: Literal["success", "failed", "partial"]
    data: dict[str, Any] | None = None
    error: str | None = None
    screenshot: str | None = None
