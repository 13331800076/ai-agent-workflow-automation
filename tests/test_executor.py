"""Tests for workflow executor and retry logic."""
import pytest
import asyncio
from datetime import datetime
from workflow_agent.agent.models import ParsedTask, WorkflowPlan
from workflow_agent.agent.planner import WorkflowPlanner
from workflow_agent.executor.workflow_executor import WorkflowExecutor
from workflow_agent.logging.audit_logger import AuditLogger
from workflow_agent.logging.artifact_store import ArtifactStore
from workflow_agent.executor.retry import retry_async


class TestRetryAsync:
    async def test_success_no_retry(self):
        async def ok():
            return 42
        result = await retry_async(ok, retries=1, delay=0.1)
        assert result == 42

    async def test_retry_then_success(self):
        calls = []
        async def flaky():
            calls.append(1)
            if len(calls) < 2:
                raise RuntimeError("fail")
            return 42
        result = await retry_async(flaky, retries=2, delay=0.1)
        assert result == 42
        assert len(calls) == 2

    async def test_retry_exhausted(self):
        async def always_fail():
            raise RuntimeError("fail")
        with pytest.raises(RuntimeError, match="fail"):
            await retry_async(always_fail, retries=1, delay=0.1)


class TestWorkflowExecutor:
    async def test_execute_create_customer(self, tmp_path):
        planner = WorkflowPlanner()
        parsed = ParsedTask(
            task_id="t1",
            intent="create_customer",
            entities={
                "customer_name": "Acme Corp",
                "contact": "Alice",
                "email": "alice@acme.com",
                "region": "APAC",
            },
            confidence=0.95,
        )
        plan = planner.create_plan(parsed)
        artifact_store = ArtifactStore(str(tmp_path / "artifacts"))
        audit_logger = AuditLogger(artifact_store)
        executor = WorkflowExecutor(audit_logger)
        result = await executor.execute(plan, "t1")
        assert result.status in ("success", "failed")
        assert result.task_id == "t1"
        assert len(result.steps) >= 1
