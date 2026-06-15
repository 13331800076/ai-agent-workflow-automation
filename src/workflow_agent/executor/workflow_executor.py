"""Workflow executor: runs workflow steps through tools and records results."""
import time
from typing import Any
from ..agent.models import WorkflowPlan, WorkflowStep, StepResult, ExecutionResult
from ..agent.router import ToolRouter
from ..browser.playwright_client import PlaywrightClient
from ..browser.screenshots import ScreenshotRecorder
from ..logging.audit_logger import AuditLogger
from ..executor.retry import retry_async
from ..executor.errors import ToolExecutionError


class WorkflowExecutor:
    """Execute a WorkflowPlan step by step with logging and screenshots."""

    def __init__(self, audit_logger: AuditLogger) -> None:
        self.audit_logger = audit_logger

    async def execute(self, plan: WorkflowPlan, task_id: str) -> ExecutionResult:
        browser = PlaywrightClient()
        await browser.start()
        try:
            router = ToolRouter(browser)
            recorder = ScreenshotRecorder(self.audit_logger.artifact_store.get_task_dir(task_id))
            step_results: list[StepResult] = []
            screenshots: list[str] = []
            logs: list[str] = []
            overall_status: Any = "success"
            final_error: str | None = None

            self.audit_logger.log_task_start(task_id, plan.model_dump())

            for step in plan.steps:
                start = time.time()
                step_id = step.step_id
                tool_name = step.tool_name
                log_prefix = f"[{task_id}] Step {step_id}: {tool_name}"
                logs.append(f"{log_prefix} started")

                try:
                    # Screenshot before step
                    before_ss = await recorder.capture(browser.page, f"{step_id}_{tool_name}_before")
                    screenshots.append(before_ss)

                    # Execute with retry
                    result = await retry_async(
                        lambda: router.execute(step),
                        retries=1,
                        delay=1.0,
                    )
                    duration_ms = int((time.time() - start) * 1000)
                    logs.append(f"{log_prefix} completed in {duration_ms}ms")

                    # Screenshot after step
                    after_ss = await recorder.capture(browser.page, f"{step_id}_{tool_name}_after")
                    screenshots.append(after_ss)

                    status = result.get("status", "failed")
                    step_result = StepResult(
                        step_id=step_id,
                        tool_name=tool_name,
                        status=status,
                        duration_ms=duration_ms,
                        input=step.input,
                        output=result,
                        error=result.get("error"),
                        screenshot=after_ss,
                    )
                    step_results.append(step_result)
                    self.audit_logger.log_step(task_id, step_result.model_dump())

                    if status == "failed":
                        overall_status = "failed"
                        final_error = result.get("error", "Unknown error")
                        break

                except Exception as exc:
                    duration_ms = int((time.time() - start) * 1000)
                    error_msg = str(exc)
                    logs.append(f"{log_prefix} failed: {error_msg}")
                    # Failure screenshot
                    try:
                        fail_ss = await recorder.capture(browser.page, f"{step_id}_{tool_name}_failed")
                        screenshots.append(fail_ss)
                    except Exception:
                        fail_ss = None
                    step_result = StepResult(
                        step_id=step_id,
                        tool_name=tool_name,
                        status="failed",
                        duration_ms=duration_ms,
                        input=step.input,
                        error=error_msg,
                        screenshot=fail_ss,
                    )
                    step_results.append(step_result)
                    self.audit_logger.log_step(task_id, step_result.model_dump())
                    overall_status = "failed"
                    final_error = error_msg
                    break

            self.audit_logger.log_task_end(task_id, overall_status, final_error)
            result = ExecutionResult(
                task_id=task_id,
                status=overall_status,
                steps=step_results,
                screenshots=screenshots,
                logs=logs,
                error=final_error,
            )
            self.audit_logger.save_result(task_id, result.model_dump())
            return result
        finally:
            await browser.stop()
