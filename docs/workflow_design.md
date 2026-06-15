# Workflow Design

## Task Lifecycle

### 1. Request

```python
TaskRequest(
    task_id="task_001",
    user_input="Create a new customer named Acme Corp...",
    created_at=datetime.utcnow(),
)
```

### 2. Parse

```python
ParsedTask(
    task_id="task_001",
    intent="create_customer",
    entities={
        "customer_name": "Acme Corp",
        "contact": "Alice",
        "email": "alice@acme.com",
        "region": "APAC",
    },
    confidence=0.95,
)
```

### 3. Plan

```python
WorkflowPlan(
    task_id="task_001",
    intent="create_customer",
    steps=[
        WorkflowStep(step_id="1", tool_name="open_customer_page", input={}),
        WorkflowStep(step_id="2", tool_name="fill_customer_form", input={...}),
        WorkflowStep(step_id="3", tool_name="submit_form", input={}),
        WorkflowStep(step_id="4", tool_name="verify_customer_created", input={...}),
    ],
)
```

### 4. Execute

```python
ExecutionResult(
    task_id="task_001",
    status="success",
    steps=[StepResult(...), ...],
    screenshots=["artifacts/task_001/screenshots/01_...png", ...],
    logs=["[task_001] Step 1: open_customer_page started", ...],
    error=None,
)
```

## Why Not Direct LLM Browser Control?

**Direct LLM control:**
- User input → LLM plans → LLM clicks → Result
- Unpredictable, non-deterministic, hard to test, hard to debug

**Structured workflow (this project):**
- User input → Parser → Planner → Fixed tools → Playwright → Logs
- Deterministic, testable, auditable, recoverable

## v1 vs v2

**v1 (current):**
- Rule-based parser
- Fixed workflow per intent
- Deterministic and stable
- Full test coverage

**v2 (future):**
- LLM-powered parser for flexible language
- LLM-assisted planner for multi-step reasoning
- Dynamic tool selection
- Still validated against test cases
