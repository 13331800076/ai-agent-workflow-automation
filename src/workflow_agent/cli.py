"""CLI entry point for running agent tasks."""
import asyncio
import typer
from datetime import datetime, timezone
from workflow_agent.agent.models import TaskRequest
from workflow_agent.agent.parser import TaskParser
from workflow_agent.agent.planner import WorkflowPlanner
from workflow_agent.executor.workflow_executor import WorkflowExecutor
from workflow_agent.logging.audit_logger import AuditLogger
from workflow_agent.logging.artifact_store import ArtifactStore

app = typer.Typer(help="AI Agent Workflow Automation CLI")


@app.command()
def run(
    user_input: str = typer.Argument(..., help="Natural language task to execute"),
    headless: bool = typer.Option(True, help="Run browser in headless mode"),
) -> None:
    """Run a single task and print the result."""
    import uuid

    task_id = f"task_{uuid.uuid4().hex[:8]}"
    task_request = TaskRequest(
        task_id=task_id, user_input=user_input, created_at=datetime.now(timezone.utc)
    )

    typer.echo(f"Task ID: {task_id}")
    typer.echo(f"Input: {user_input}")
    typer.echo("-" * 40)

    # Parse
    parser = TaskParser()
    parsed = parser.parse(task_request)
    typer.echo(f"Intent: {parsed.intent}")
    typer.echo(f"Entities: {parsed.entities}")
    typer.echo("-" * 40)

    # Plan
    planner = WorkflowPlanner()
    plan = planner.create_plan(parsed)
    typer.echo(f"Plan: {len(plan.steps)} steps")
    for step in plan.steps:
        typer.echo(f"  - {step.step_id}: {step.tool_name}")
    typer.echo("-" * 40)

    # Execute
    artifact_store = ArtifactStore("artifacts")
    audit_logger = AuditLogger(artifact_store)
    executor = WorkflowExecutor(audit_logger)

    async def _execute() -> None:
        result = await executor.execute(plan, task_id)
        typer.echo(f"Status: {result.status}")
        if result.error:
            typer.echo(f"Error: {result.error}")
        typer.echo(f"Steps: {len(result.steps)}")
        for step in result.steps:
            typer.echo(f"  - {step.step_id}: {step.tool_name} -> {step.status} ({step.duration_ms}ms)")
        if result.screenshots:
            typer.echo(f"Screenshots: {len(result.screenshots)}")
            for ss in result.screenshots:
                typer.echo(f"  - {ss}")
        typer.echo(f"Artifacts: artifacts/{task_id}/")

    asyncio.run(_execute())


def main() -> None:
    app()
