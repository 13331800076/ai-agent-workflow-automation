"""CLI entry point for running agent tasks with rich output."""
import asyncio
import typer
from datetime import datetime, timezone
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from workflow_agent.agent.models import TaskRequest
from workflow_agent.agent.parser import TaskParser
from workflow_agent.agent.planner import WorkflowPlanner
from workflow_agent.executor.workflow_executor import WorkflowExecutor
from workflow_agent.logging.audit_logger import AuditLogger
from workflow_agent.logging.artifact_store import ArtifactStore

app = typer.Typer(help="AI Agent Workflow Automation CLI")
console = Console()


def print_task_header(task_id: str, user_input: str) -> None:
    console.print(Panel.fit(
        f"[bold blue]Task ID:[/bold blue] {task_id}\n"
        f"[bold blue]Input:[/bold blue] {user_input}",
        title="AI Agent Workflow",
        border_style="blue"
    ))


def print_intent(intent: str, entities: dict) -> None:
    console.print(f"[green]Intent:[/green] {intent}")
    console.print(f"[green]Entities:[/green] {entities}")
    console.print("-" * 50)


def print_plan(steps: list) -> None:
    console.print(f"[yellow]Plan:[/yellow] {len(steps)} steps")
    for step in steps:
        console.print(f"  - {step.step_id}: {step.tool_name}")
    console.print("-" * 50)


def print_result(result) -> None:
    if result.status == "success":
        status_color = "bold green"
    elif result.status == "partial":
        status_color = "bold yellow"
    else:
        status_color = "bold red"
    console.print(f"[{status_color}]Status:[/] {result.status}")

    if result.error:
        console.print(f"[bold red]Error:[/bold red] {result.error}")
    console.print(f"[blue]Steps:[/blue] {len(result.steps)}")
    for step in result.steps:
        icon = "✅" if step.status == "success" else "❌"
        console.print(f"  {icon} {step.step_id}: {step.tool_name} → {step.status} ({step.duration_ms}ms)")
    if result.screenshots:
        console.print(f"[blue]Screenshots:[/blue] {len(result.screenshots)}")
    console.print(f"[bold magenta]Artifacts:[/bold magenta] artifacts/{result.task_id}/")
    console.print(f"[bold cyan]View result:[/bold cyan] cat artifacts/{result.task_id}/result.json")


@app.command()
def run(
    user_input: str = typer.Argument(..., help="Natural language task to execute"),
    headless: bool = typer.Option(True, help="Run browser in headless mode"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
) -> None:
    """Run a single task and print the result."""
    import uuid

    task_id = f"task_{uuid.uuid4().hex[:8]}"
    task_request = TaskRequest(
        task_id=task_id, user_input=user_input, created_at=datetime.now(timezone.utc)
    )

    print_task_header(task_id, user_input)

    # Parse
    parser = TaskParser()
    parsed = parser.parse(task_request)
    print_intent(parsed.intent, parsed.entities)

    # Plan
    planner = WorkflowPlanner()
    plan = planner.create_plan(parsed)
    print_plan(plan.steps)

    # Execute
    artifact_store = ArtifactStore("artifacts")
    audit_logger = AuditLogger(artifact_store)
    executor = WorkflowExecutor(audit_logger)

    async def _execute() -> None:
        with console.status("[bold green]Executing workflow...") as status:
            result = await executor.execute(plan, task_id)
        print_result(result)

    asyncio.run(_execute())


@app.command()
def batch(
    tasks_file: str = typer.Argument(..., help="JSON file with array of task strings"),
    headless: bool = typer.Option(True, help="Run browser in headless mode"),
) -> None:
    """Run multiple tasks from a JSON file."""
    import json
    import uuid

    data = json.loads(open(tasks_file).read())
    if not isinstance(data, list):
        console.print("[red]Error: file must contain a JSON array of strings[/red]")
        raise typer.Exit(1)

    results = []
    for user_input in data:
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        task_request = TaskRequest(
            task_id=task_id, user_input=user_input, created_at=datetime.now(timezone.utc)
        )
        parser = TaskParser()
        parsed = parser.parse(task_request)
        planner = WorkflowPlanner()
        plan = planner.create_plan(parsed)
        artifact_store = ArtifactStore("artifacts")
        audit_logger = AuditLogger(artifact_store)
        executor = WorkflowExecutor(audit_logger)

        async def _execute_one():
            return await executor.execute(plan, task_id)

        result = asyncio.run(_execute_one())
        results.append({
            "task_id": task_id,
            "input": user_input,
            "status": result.status,
            "steps": len(result.steps),
            "screenshots": len(result.screenshots),
            "error": result.error,
        })
        icon = "✅" if result.status == "success" else "❌"
        console.print(f"{icon} {task_id}: {user_input[:50]}... → {result.status}")

    # Save summary
    summary_path = f"artifacts/batch_summary_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)
    console.print(f"[bold green]Batch summary saved to:[/bold green] {summary_path}")


@app.command()
def status(
    task_id: str = typer.Argument(..., help="Task ID to inspect"),
) -> None:
    """Inspect a previous task's artifacts."""
    import json
    from pathlib import Path

    artifact_store = ArtifactStore("artifacts")
    task_dir = artifact_store.get_task_dir(task_id)
    if not task_dir.exists():
        console.print(f"[red]Task {task_id} not found[/red]")
        raise typer.Exit(1)

    console.print(f"[bold blue]Task:[/bold blue] {task_id}")
    for f in sorted(task_dir.rglob("*")):
        if f.is_file():
            rel = f.relative_to(task_dir)
            if f.name.endswith(".json"):
                console.print(f"  📄 {rel}")
            elif f.name.endswith(".png"):
                console.print(f"  📸 {rel}")
            elif f.name.endswith(".log"):
                console.print(f"  📝 {rel}")
            else:
                console.print(f"  📎 {rel}")

    result_path = task_dir / "result.json"
    if result_path.exists():
        result = json.loads(result_path.read_text())
        console.print("-" * 50)
        console.print(f"[green]Status:[/green] {result.get('status', 'unknown')}")
        console.print(f"[blue]Steps completed:[/blue] {len(result.get('steps', []))}")
        if result.get('error'):
            console.print(f"[red]Error:[/red] {result['error']}")


@app.command()
def serve() -> None:
    """Start the MiniERP web app and API server."""
    import uvicorn
    console.print("[bold green]Starting MiniERP server at http://localhost:8000[/bold green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")
    uvicorn.run("workflow_agent.app.main:app", host="0.0.0.0", port=8000, reload=True)


def main() -> None:
    app()
