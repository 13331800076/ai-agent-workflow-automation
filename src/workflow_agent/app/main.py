from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import json
import csv
import io
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from ..agent.models import TaskRequest, ParsedTask, WorkflowPlan
from ..agent.parser import TaskParser
from ..agent.planner import WorkflowPlanner
from ..executor.workflow_executor import WorkflowExecutor
from ..logging.audit_logger import AuditLogger
from ..logging.artifact_store import ArtifactStore

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent.parent.parent / "data"
ARTIFACTS_DIR = BASE_DIR.parent.parent.parent / "artifacts"
DB_PATH = BASE_DIR.parent.parent.parent / "minierp.db"

app = FastAPI(title="MiniERP Demo", description="AI Agent Workflow Automation Demo")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            contact TEXT,
            email TEXT,
            region TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL UNIQUE,
            order_status TEXT,
            amount REAL,
            supplier TEXT
        )
        """
    )
    conn.commit()
    # Seed data
    seed_customers = json.loads((DATA_DIR / "seed_customers.json").read_text())
    for c in seed_customers:
        conn.execute(
            "INSERT OR IGNORE INTO customers (customer_name, contact, email, region) VALUES (?, ?, ?, ?)",
            (c["customer_name"], c["contact"], c["email"], c["region"]),
        )
    seed_orders = json.loads((DATA_DIR / "seed_orders.json").read_text())
    for o in seed_orders:
        conn.execute(
            "INSERT OR IGNORE INTO orders (order_id, order_status, amount, supplier) VALUES (?, ?, ?, ?)",
            (o["order_id"], o["order_status"], o["amount"], o["supplier"]),
        )
    conn.commit()
    conn.close()


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/health")
async def health():
    return {"status": "ok"}


# Customer management
@app.get("/customers", response_class=HTMLResponse)
async def customers_page(request: Request):
    conn = get_db()
    rows = conn.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
    conn.close()
    customers = [dict(r) for r in rows]
    return templates.TemplateResponse(
        request,
        "customers.html",
        {"customers": customers},
    )


@app.post("/customers", response_class=HTMLResponse)
async def create_customer(
    request: Request,
    customer_name: str = Form(...),
    contact: str = Form(...),
    email: str = Form(...),
    region: str = Form(...),
):
    conn = get_db()
    conn.execute(
        "INSERT INTO customers (customer_name, contact, email, region) VALUES (?, ?, ?, ?)",
        (customer_name, contact, email, region),
    )
    conn.commit()
    rows = conn.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
    conn.close()
    customers = [dict(r) for r in rows]
    return templates.TemplateResponse(
        request,
        "customers.html",
        {
            "customers": customers,
            "success": f"Customer '{customer_name}' created successfully.",
        },
    )


@app.get("/api/customers")
async def api_customers(name: Optional[str] = None):
    conn = get_db()
    if name:
        rows = conn.execute(
            "SELECT * FROM customers WHERE customer_name = ?", (name,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Order management
@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, order_id: Optional[str] = None):
    conn = get_db()
    order = None
    if order_id:
        row = conn.execute(
            "SELECT * FROM orders WHERE order_id = ?", (order_id,)
        ).fetchone()
        if row:
            order = dict(row)
    conn.close()
    return templates.TemplateResponse(
        request,
        "orders.html",
        {"order": order, "searched": order_id is not None},
    )


@app.get("/api/orders")
async def api_orders(order_id: Optional[str] = None):
    conn = get_db()
    if order_id:
        row = conn.execute(
            "SELECT * FROM orders WHERE order_id = ?", (order_id,)
        ).fetchone()
        conn.close()
        if row:
            return dict(row)
        return {"error": "Order not found"}
    rows = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Report export
@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    return templates.TemplateResponse(request, "reports.html", {})


@app.post("/reports/export")
async def export_report(report_type: str = Form(...), month: str = Form(...)):
    filename = f"{report_type}_{month.replace('-', '_')}.csv"
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Report Type", "Month", "Generated At"])
    writer.writerow([report_type, month, "2026-06-15T10:00:00"])
    writer.writerow([])
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Orders", "42"])
    writer.writerow(["Total Revenue", "128500"])
    writer.writerow(["New Customers", "8"])
    content = output.getvalue()
    output.close()

    # Save to downloads dir for Playwright to pick up
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    file_path = downloads_dir / filename
    file_path.write_text(content)

    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename=filename,
    )


# Supplier onboarding form (for fill_form task)
@app.get("/supplier-onboarding", response_class=HTMLResponse)
async def supplier_onboarding_page(request: Request):
    return templates.TemplateResponse(request, "supplier_onboarding.html", {})


@app.post("/supplier-onboarding")
async def submit_supplier_onboarding(
    company_name: str = Form(...),
    tax_id: str = Form(...),
    region: str = Form(...),
):
    return {"status": "success", "message": f"Supplier '{company_name}' onboarded."}


# Agent API endpoints
class RunTaskRequest(BaseModel):
    user_input: str


@app.post("/tasks/run")
async def run_task(req: RunTaskRequest):
    import uuid
    from datetime import datetime, timezone

    task_id = f"task_{uuid.uuid4().hex[:8]}"
    task_request = TaskRequest(task_id=task_id, user_input=req.user_input, created_at=datetime.now(timezone.utc))

    # Parse
    parser = TaskParser()
    parsed = parser.parse(task_request)

    # Plan
    planner = WorkflowPlanner()
    plan = planner.create_plan(parsed)

    # Execute
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


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    artifact_store = ArtifactStore(str(ARTIFACTS_DIR))
    result_path = artifact_store.get_result_path(task_id)
    if not result_path.exists():
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    import json
    return json.loads(result_path.read_text())


@app.get("/tasks/{task_id}/artifacts")
async def get_task_artifacts(task_id: str):
    artifact_store = ArtifactStore(str(ARTIFACTS_DIR))
    task_dir = artifact_store.get_task_dir(task_id)
    if not task_dir.exists():
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    artifacts = []
    for f in task_dir.rglob("*"):
        if f.is_file():
            artifacts.append(str(f.relative_to(task_dir)))
    return {"task_id": task_id, "artifacts": artifacts}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("workflow_agent.app.main:app", host="0.0.0.0", port=8000, reload=True)
