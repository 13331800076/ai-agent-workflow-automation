# Architecture

## System Overview

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

## Design Philosophy

Natural language task ≠ direct LLM browser control.

Instead: Natural language → Structured task → Verified workflow → Tool calls → Playwright execution → Logs / Screenshots / Tests / Audit.

## Core Components

### Task Parser
- Input: `TaskRequest` (task_id + user_input)
- Output: `ParsedTask` (intent + entities + confidence)
- v1: Rule-based regex parsing
- v2: LLM-based parsing

### Intent Classifier
- Supported intents: create_customer, search_order, export_report, check_field_diff, fill_form
- Maps natural language patterns to intent enum

### Workflow Planner
- Input: `ParsedTask`
- Output: `WorkflowPlan` (ordered list of `WorkflowStep`)
- Each step has: step_id, tool_name, input, expected_result
- No direct page manipulation

### Tool Router
- Routes each `WorkflowStep` to the correct tool class
- Tool classes: CustomerTools, OrderTools, ReportTools, FormTools
- All tools receive a `PlaywrightClient` instance

### Playwright Tool Executor
- `PlaywrightClient`: Browser lifecycle, navigation, actions, screenshots
- `ScreenshotRecorder`: Captures before/after/failure screenshots per step
- `SELECTORS`: Centralized data-testid selector map

### Execution Logger
- `AuditLogger`: Structured JSON logs per task
- `ArtifactStore`: Directory management for artifacts
- Output per task: task.json, plan.json, execution.log, result.json, screenshots/

### Failure Handler
- `retry_async`: Retry wrapper with configurable attempts and delay
- `ToolExecutionError` hierarchy: ElementNotFound, FormValidation, DownloadError
- Failure screenshots captured automatically

## MiniERP Web App

FastAPI + Jinja2 + SQLite demo ERP providing:
- /customers — Customer CRUD
- /orders — Order search
- /reports — CSV export
- /supplier-onboarding — Form demo
- /health — Health check
- /tasks/* — Agent API endpoints

## Data Flow

1. User submits task via CLI or API
2. `TaskParser` extracts intent and entities
3. `WorkflowPlanner` generates step plan
4. `WorkflowExecutor` launches browser, iterates steps
5. `ToolRouter` dispatches each step to the correct tool
6. Tool uses `PlaywrightClient` to interact with MiniERP
7. `ScreenshotRecorder` captures visual evidence
8. `AuditLogger` writes structured execution log
9. `WorkflowExecutor` returns `ExecutionResult`
10. API/CLI presents result to user
