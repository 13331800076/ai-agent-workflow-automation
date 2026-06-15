# AI Agent Workflow Automation Demo

A production-style AI agent demo for automating ERP-like web operations with Playwright, tool calling, execution logs, screenshots, and failure recovery.

This project demonstrates how natural-language enterprise tasks can be converted into structured workflows and executed reliably against a web application.

## What it demonstrates

- **Task parsing and intent classification** — Convert natural language into structured intent and entities
- **Workflow planning** — Generate step-by-step tool execution plans
- **Tool calling for enterprise operations** — Abstract browser actions into reusable tools
- **Playwright-based browser automation** — Stable, testable web automation
- **Execution logs and audit trails** — Every step is recorded with timing and status
- **Screenshot-based traceability** — Visual proof of each automation step
- **Failure retry and recovery** — Robust handling of flaky web operations
- **Testable AI workflow engineering** — Unit, integration, and E2E tests throughout

## Architecture

```
User Task
   ↓
Task Parser
   ↓
Intent Classifier
   ↓
Workflow Planner
   ↓
Tool Router
   ↓
Playwright Tool Executor
   ↓
MiniERP Web App
   ↓
Execution Logger
   ↓
Screenshot Recorder
   ↓
Failure Handler / Retry
   ↓
Final Report
```

## Quick Start

### 1. Install dependencies

```bash
pip install -e ".[dev]"
playwright install chromium
```

### 2. Run the MiniERP web app

```bash
python -m workflow_agent.app.main
```

Open http://localhost:8000 to see the demo ERP.

### 3. Run a task via CLI

```bash
workflow-agent run "Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC."
```

### 4. Run the API server

```bash
uvicorn workflow_agent.app.main:app --reload
```

### 5. Run tests

```bash
pytest
pytest tests/test_e2e_playwright.py
```

## Demo Tasks

| Task | Example Input | What Agent Does |
|------|---------------|-----------------|
| Create Customer | `Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC.` | Opens customer page, fills form, submits, verifies success |
| Search Order | `Find order PO-1001 and summarize its status.` | Opens order page, searches by ID, extracts status, amount, supplier |
| Export Report | `Export the monthly sales report for May 2026.` | Selects report type and month, clicks export, verifies download |
| Check Field Diff | `Check whether customer Acme Corp has the expected region APAC and contact Alice.` | Queries customer, compares fields against expectations |
| Fill Form | `Fill in the supplier onboarding form with the provided company profile.` | Parses data, locates form fields, auto-fills, validates required |

## Execution Trace Example

Each task generates an artifact directory:

```
artifacts/task_001/
├── task.json
├── plan.json
├── execution.log
├── result.json
└── screenshots/
    ├── 01_open_customer_page.png
    ├── 02_fill_form.png
    └── 03_submit_success.png
```

## API Usage

### Health check
```bash
curl http://localhost:8000/health
```

### Run a task
```bash
curl -X POST http://localhost:8000/tasks/run \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Create a new customer named Acme Corp with contact Alice, email alice@acme.com, and region APAC."}'
```

### Get task result
```bash
curl http://localhost:8000/tasks/{task_id}
```

### Get task artifacts
```bash
curl http://localhost:8000/tasks/{task_id}/artifacts
```

## Project Structure

```
ai-agent-workflow-automation/
├── src/workflow_agent/
│   ├── app/           # FastAPI + MiniERP web app
│   ├── agent/         # Parser, planner, intent classifier
│   ├── tools/         # Playwright tools for each business operation
│   ├── browser/       # Playwright client, selectors, screenshots
│   ├── executor/      # Workflow executor, retry, error handling
│   ├── logging/       # Audit logger, artifact store
│   ├── api/           # FastAPI routes
│   └── cli.py         # CLI entry point
├── tests/             # Unit, integration, and E2E tests
├── data/              # Seed data for MiniERP
├── artifacts/           # Execution logs and screenshots
└── docs/              # Architecture and design docs
```

## What This Project Proves

This is not a chatbot or a one-off automation script. It is a **testable, auditable, and recoverable AI agent workflow engine**.

For AI Agent Engineer / Applied AI Engineer roles, it demonstrates:

1. **Agent Engineering** — You can build the core loop (parse → plan → execute → log → retry)
2. **Enterprise Domain Understanding** — You abstracted CRM/ERP operations into tools
3. **Browser Automation** — You used Playwright for stable, testable web automation
4. **Observability** — Every step is logged and screenshotted
5. **Quality** — The project has tests at every level (unit, integration, E2E)
6. **Vibe Coding** — The spec was translated into user stories, acceptance criteria, and tests

## Roadmap

- [x] v1: Rule-based parser + fixed workflow planner + Playwright tools + logs + retry
- [ ] v2: LLM-powered planner for flexible task expression
- [ ] v2: LangGraph / LangChain integration
- [ ] v2: Attachment upload tool
- [ ] v2: Approval workflow tool
- [ ] v2: Docker Compose deployment
- [ ] v2: GitHub Actions CI

## License

MIT
